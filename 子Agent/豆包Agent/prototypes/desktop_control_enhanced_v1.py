"""
龙虾-桌面控制系统底层增强 v1.0
协议补充：系统底层调用 + 跨软件联动 + 权限批量管理
"""

import os
import sys
import ctypes
import subprocess
import json
import time
from ctypes import wintypes
from typing import Dict, List, Optional, Tuple

# ============================================================
# 系统底层调用增强
# ============================================================

class SystemLowLevelAPI:
    """Windows底层API封装"""
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.advapi32 = ctypes.windll.advapi32
        self.shell32 = ctypes.windll.shell32
        
    # --- 窗口管理底层 ---
    
    def get_window_handle(self, window_title: str) -> Optional[int]:
        """按标题查找窗口句柄"""
        hwnd = self.user32.FindWindowW(None, window_title)
        return hwnd if hwnd else None
    
    def get_window_class(self, hwnd: int) -> str:
        """获取窗口类名"""
        buffer = ctypes.create_unicode_buffer(256)
        self.user32.GetClassNameW(hwnd, buffer, 256)
        return buffer.value
    
    def get_window_rect(self, hwnd: int) -> Dict:
        """获取窗口矩形位置"""
        rect = wintypes.RECT()
        self.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        return {"left": rect.left, "top": rect.top, 
                "right": rect.right, "bottom": rect.bottom,
                "width": rect.right - rect.left, "height": rect.bottom - rect.top}
    
    def set_window_pos(self, hwnd: int, x: int, y: int, w: int, h: int, flags: int = 0):
        """设置窗口位置和大小"""
        SWP_NOZORDER = 0x0004
        self.user32.SetWindowPos(hwnd, 0, x, y, w, h, flags | SWP_NOZORDER)
    
    def get_window_process_id(self, hwnd: int) -> int:
        """获取窗口进程ID"""
        pid = wintypes.DWORD()
        self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return pid.value
    
    def bring_to_front(self, hwnd: int):
        """窗口置顶"""
        SW_SHOW = 5
        self.user32.ShowWindow(hwnd, SW_SHOW)
        self.user32.SetForegroundWindow(hwnd)
    
    # --- 进程管理底层 ---
    
    def get_process_list(self) -> List[Dict]:
        """获取进程列表（底层）"""
        import psutil
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                info = proc.info
                processes.append({
                    "pid": info["pid"],
                    "name": info["name"],
                    "cpu": info["cpu_percent"] or 0,
                    "memory_mb": round(info["memory_info"].rss / 1024 / 1024, 1) if info["memory_info"] else 0
                })
            except:
                pass
        return processes
    
    # --- 注册表操作 ---
    
    def read_registry(self, key_path: str, value_name: str, 
                     hive: int = 0x80000002) -> Optional[str]:
        """读取注册表值 (hive默认HKEY_LOCAL_MACHINE)"""
        try:
            key = wintypes.HKEY()
            # 需要admin权限
            result = self.advapi32.RegOpenKeyExW(
                hive, key_path, 0, 0x20019, ctypes.byref(key)  # KEY_READ
            )
            if result != 0:
                return None
            
            buffer = ctypes.create_unicode_buffer(1024)
            buffer_size = wintypes.DWORD(1024)
            result = self.advapi32.RegQueryValueExW(
                key, value_name, None, None, ctypes.byref(buffer), ctypes.byref(buffer_size)
            )
            self.advapi32.RegCloseKey(key)
            
            return buffer.value if result == 0 else None
        except:
            return None
    
    # --- 服务管理 ---
    
    def service_status(self, service_name: str) -> Dict:
        """查询Windows服务状态"""
        try:
            result = subprocess.run(
                ["sc", "query", service_name],
                capture_output=True, text=True, timeout=10
            )
            status = "UNKNOWN"
            if "RUNNING" in result.stdout:
                status = "RUNNING"
            elif "STOPPED" in result.stdout:
                status = "STOPPED"
            elif "PAUSED" in result.stdout:
                status = "PAUSED"
            
            return {
                "service": service_name,
                "status": status,
                "raw": result.stdout.strip()
            }
        except:
            return {"service": service_name, "status": "ERROR"}


# ============================================================
# 跨软件联动管理器
# ============================================================

class CrossAppOrchestrator:
    """跨软件联动协调器"""
    
    # 预设联动链
    PRESET_CHAINS = {
        "research_pipeline": [
            {"app": "browser", "action": "搜索"{keyword}", tab_index=0"},
            {"app": "obsidian", "action": "新建笔记 {keyword}", "delay_ms": 2000},
            {"app": "browser", "action": "等待加载完成", "delay_ms": 3000},
            {"app": "obsidian", "action": "粘贴URL + 摘要", "delay_ms": 1000},
        ],
        "trade_pipeline": [
            {"app": "同花顺", "action": "启动+登录", "delay_ms": 5000},
            {"app": "同花顺", "action": "打开K线图 {symbol}", "delay_ms": 2000},
            {"app": "python", "action": "运行策略计算脚本", "delay_ms": 3000},
            {"app": "同花顺", "action": "API下单 (需确认)", "delay_ms": 1000},
        ],
        "dev_pipeline": [
            {"app": "vscode", "action": "打开项目 {project_dir}", "delay_ms": 2000},
            {"app": "terminal", "action": "git pull + pip install -r requirements.txt", "delay_ms": 5000},
            {"app": "vscode", "action": "打开最近编辑文件", "delay_ms": 1000},
            {"app": "browser", "action": "打开API文档", "delay_ms": 2000},
        ]
    }
    
    def __init__(self):
        self.low_level = SystemLowLevelAPI()
        self.active_chains: Dict[str, Dict] = {}
    
    def execute_chain(self, chain_name: str, variables: Optional[Dict] = None) -> Dict:
        """执行预设联动链"""
        if chain_name not in self.PRESET_CHAINS:
            return {"success": False, "error": f"Unknown chain: {chain_name}"}
        
        chain = self.PRESET_CHAINS[chain_name]
        var = variables or {}
        results = []
        
        chain_id = f"{chain_name}_{int(time.time())}"
        self.active_chains[chain_id] = {"name": chain_name, "started": time.time(), "steps": []}
        
        for i, step in enumerate(chain):
            action = step["action"]
            for k, v in var.items():
                action = action.replace(f"{{{k}}}", str(v))
            
            time.sleep(step.get("delay_ms", 1000) / 1000)
            
            step_result = {
                "step": i,
                "app": step["app"],
                "action": action,
                "status": "SCHEDULED",  # 实际需AppAgent执行
                "timestamp": time.time()
            }
            results.append(step_result)
            self.active_chains[chain_id]["steps"].append(step_result)
        
        return {
            "success": True,
            "chain_id": chain_id,
            "chain_name": chain_name,
            "steps": results,
            "total_steps": len(results)
        }
    
    def get_active_chains(self) -> List[str]:
        return list(self.active_chains.keys())


# ============================================================
# 权限批量管理器
# ============================================================

class BulkPermissionManager:
    """批量权限管理"""
    
    def __init__(self):
        self.permission_rules: Dict[str, Dict] = {}
    
    def check_admin(self) -> bool:
        """检查是否管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def set_file_permission(self, path: str, user: str, 
                           rights: str = "FullControl") -> Dict:
        """设置文件权限（需管理员）"""
        if not self.check_admin():
            return {"success": False, "error": "需要管理员权限"}
        
        try:
            cmd = f'icacls "{path}" /grant "{user}:{rights}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "success": result.returncode == 0,
                "path": path,
                "user": user,
                "rights": rights,
                "output": result.stdout.strip()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def reset_file_inheritance(self, path: str) -> Dict:
        """重置权限继承"""
        try:
            cmd = f'icacls "{path}" /reset /t /c'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            return {
                "success": result.returncode == 0,
                "path": path,
                "output": result.stdout.strip()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def take_ownership(self, path: str) -> Dict:
        """获取文件所有权（管理员）"""
        try:
            cmd = f'takeown /f "{path}" /r /d y'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            return {
                "success": result.returncode == 0,
                "path": path,
                "output": result.stdout.strip()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


# ============================================================
# 多窗口布局引擎
# ============================================================

class MultiWindowLayoutEngine:
    """多窗口智能布局"""
    
    LAYOUTS = {
        "dual_horizontal": lambda w, h: [
            (0, 0, w//2, h), (w//2, 0, w//2, h)
        ],
        "dual_vertical": lambda w, h: [
            (0, 0, w, h//2), (0, h//2, w, h//2)
        ],
        "triple_main_left": lambda w, h: [
            (0, 0, int(w*0.6), h), (int(w*0.6), 0, int(w*0.4), h//2), (int(w*0.6), h//2, int(w*0.4), h//2)
        ],
        "quad_grid": lambda w, h: [
            (0, 0, w//2, h//2), (w//2, 0, w//2, h//2),
            (0, h//2, w//2, h//2), (w//2, h//2, w//2, h//2)
        ],
        "focus_center": lambda w, h: [
            (int(w*0.1), int(h*0.1), int(w*0.8), int(h*0.8))
        ]
    }
    
    def __init__(self):
        self.low_level = SystemLowLevelAPI()
    
    def apply_layout(self, layout_name: str, 
                    window_titles: List[str] = None) -> Dict:
        """应用布局"""
        if layout_name not in self.LAYOUTS:
            return {"success": False, "error": f"Unknown layout: {layout_name}"}
        
        screen_w = self.low_level.user32.GetSystemMetrics(0)
        screen_h = self.low_level.user32.GetSystemMetrics(1)
        
        positions = self.LAYOUTS[layout_name](screen_w, screen_h)
        
        results = []
        for i, (x, y, w, h) in enumerate(positions):
            title = window_titles[i] if window_titles and i < len(window_titles) else None
            if title:
                hwnd = self.low_level.get_window_handle(title)
                if hwnd:
                    self.low_level.set_window_pos(hwnd, x, y, w, h)
                    results.append({"window": title, "position": f"({x},{y})-{w}x{h}", "status": "APPLIED"})
                else:
                    results.append({"window": title, "status": "NOT_FOUND"})
            else:
                results.append({"position": f"({x},{y})-{w}x{h}", "status": "VACANT"})
        
        return {
            "success": True,
            "layout": layout_name,
            "screen": f"{screen_w}x{screen_h}",
            "windows": results
        }


# ============================================================
# 演示
# ============================================================

if __name__ == "__main__":
    print("龙虾-桌面控制系统底层增强 v1.0 原型加载完成")
    print("模块: 系统底层API | 跨软件联动 | 权限批量管理 | 多窗口布局")
    
    ll = SystemLowLevelAPI()
    print(f"\n管理员权限: {'是' if ctypes.windll.shell32.IsUserAnAdmin() else '否'}")
    print(f"屏幕分辨率: {ll.user32.GetSystemMetrics(0)}x{ll.user32.GetSystemMetrics(1)}")
    
    orch = CrossAppOrchestrator()
    print(f"\n预设联动链: {list(orch.PRESET_CHAINS.keys())}")
    
    layout_engine = MultiWindowLayoutEngine()
    print(f"布局模式: {list(layout_engine.LAYOUTS.keys())}")
