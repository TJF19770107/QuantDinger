# desktop_controller.py - 豆包Agent桌面控制模块
# 版本：v1.0 | 自动生成：R06 | 来源：R05设计
"""三层安全控制体系：Shell层/API层/自动化层，白名单+路径保护。"""
import os, subprocess, shutil, logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DesktopController")

class DesktopController:
    """桌面控制模块 —— 三层安全体系"""

    # 禁止路径（绝对不可操作）
    FORBIDDEN_PATHS = [
        r"C:\Windows", r"C:\Program Files", r"C:\Program Files (x86)", r"C:\ProgramData"
    ]
    # 允许路径
    ALLOWED_PATHS = [
        r"E:\龙虾AI主控中心",
        str(Path.home() / "Desktop"),
        str(Path.home() / "Documents"),
        str(Path.home() / "Downloads"),
    ]

    def __init__(self):
        self.op_log: List[Dict] = []

    # ---- 安全审查 ----
    def _is_safe_path(self, path: str) -> Tuple[bool, str]:
        """路径安全审查"""
        abs_path = str(Path(path).resolve())
        for forbidden in self.FORBIDDEN_PATHS:
            if abs_path.lower().startswith(forbidden.lower()):
                return False, f"禁止路径: {forbidden}"
        for allowed in self.ALLOWED_PATHS:
            if abs_path.lower().startswith(allowed.lower()):
                return True, "SAFE"
        return False, f"不在白名单: {abs_path}"

    def _is_safe_command(self, cmd: str) -> Tuple[bool, str]:
        """命令安全审查"""
        dangerous = ["format ", "del /f /s", "rmdir /s /q", "reg delete", "diskpart", "shutdown /s", "shutdown /r"]
        for d in dangerous:
            if d.lower() in cmd.lower():
                return False, f"危险命令: {d}"
        return True, "SAFE"

    def _log_op(self, operation: str, target: str, result: str, layer: str):
        entry = {"operation": operation, "target": target, "result": result, "layer": layer, "timestamp": datetime.now().isoformat()}
        self.op_log.append(entry)
        logger.info(f"[{layer}] {operation} {target} → {result}")

    # ---- Layer A: Shell层 ----
    def open_app(self, app_name: str) -> Dict:
        """打开应用程序"""
        safe, msg = self._is_safe_command(app_name)
        if not safe:
            self._log_op("open_app", app_name, f"REJECTED: {msg}", "A")
            return {"result": "rejected", "reason": msg}
        try:
            subprocess.Popen(app_name, shell=True)
            self._log_op("open_app", app_name, "success", "A")
            return {"result": "success", "operation": "open_app", "target": app_name}
        except Exception as e:
            self._log_op("open_app", app_name, f"error: {e}", "A")
            return {"result": "error", "reason": str(e)}

    def close_app(self, process_name: str) -> Dict:
        """关闭应用程序"""
        try:
            result = subprocess.run(["taskkill", "/IM", process_name, "/F"], capture_output=True, text=True, timeout=30)
            self._log_op("close_app", process_name, "success" if result.returncode == 0 else "not_found", "A")
            return {"result": "success" if result.returncode == 0 else "not_found", "operation": "close_app"}
        except Exception as e:
            return {"result": "error", "reason": str(e)}

    def create_folder(self, path: str) -> Dict:
        """创建文件夹（白名单内）"""
        safe, msg = self._is_safe_path(path)
        if not safe:
            self._log_op("create_folder", path, f"REJECTED: {msg}", "A")
            return {"result": "rejected", "reason": msg}
        Path(path).mkdir(parents=True, exist_ok=True)
        self._log_op("create_folder", path, "success", "A")
        return {"result": "success", "operation": "create_folder", "target": path}

    def copy_file(self, src: str, dst: str) -> Dict:
        """复制文件"""
        safe_src, msg1 = self._is_safe_path(src)
        safe_dst, msg2 = self._is_safe_path(dst)
        if not safe_src or not safe_dst:
            return {"result": "rejected", "reason": msg1 if not safe_src else msg2}
        shutil.copy2(src, dst)
        self._log_op("copy_file", f"{src}→{dst}", "success", "A")
        return {"result": "success"}

    def move_to_recycle_bin(self, path: str) -> Dict:
        """移动文件到回收站"""
        safe, msg = self._is_safe_path(path)
        if not safe:
            return {"result": "rejected", "reason": msg}
        try:
            import send2trash
            send2trash.send2trash(path)
        except ImportError:
            subprocess.run(['powershell', '-Command', f'Remove-Item -Path "{path}" -Recurse -Force'], capture_output=True)
        self._log_op("recycle", path, "success", "A")
        return {"result": "success"}

    # ---- Layer B: API层 ----
    def get_window_list(self) -> List[str]:
        """获取当前窗口列表"""
        try:
            import ctypes
            windows = []
            def enum_callback(hwnd, _):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                    buff = ctypes.create_unicode_buffer(length + 1)
                    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                    if buff.value:
                        windows.append(buff.value)
                return True
            ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)(enum_callback), 0)
            return windows
        except Exception:
            return []

    # ---- Layer C: 自动化层 ----
    def execute_script(self, script_path: str, timeout: int = 300) -> Dict:
        """执行Python脚本（安全审查后）"""
        safe, msg = self._is_safe_path(script_path)
        if not safe:
            return {"result": "rejected", "reason": msg}
        try:
            result = subprocess.run(["python", script_path], capture_output=True, text=True, timeout=timeout)
            self._log_op("execute_script", script_path, "success", "C")
            return {"result": "success", "stdout": result.stdout[:500], "stderr": result.stderr[:500]}
        except subprocess.TimeoutExpired:
            return {"result": "timeout", "reason": f"超过{timeout}s"}
        except Exception as e:
            return {"result": "error", "reason": str(e)}

    def get_op_summary(self) -> Dict:
        """获取操作摘要"""
        return {"total_ops": len(self.op_log), "last_ops": self.op_log[-10:]}

if __name__ == "__main__":
    dc = DesktopController()
    print(f"DesktopController 已初始化 | 白名单路径: {len(dc.ALLOWED_PATHS)} | 禁止路径: {len(dc.FORBIDDEN_PATHS)}")
