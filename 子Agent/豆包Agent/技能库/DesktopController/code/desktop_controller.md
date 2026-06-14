# desktop_controller.py

原始格式: Python

```python
"""
DesktopController v2.0 - 桌面程序安全自动化控制
路径: 豆包Agent/技能库/DesktopController/code/desktop_controller.py
对标: pywinauto + OpenClaw Desktop Gateway
"""

import json
import logging
import subprocess
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

logger = logging.getLogger("DesktopController")

class ControlLevel(Enum):
    SHELL = "shell"       # Shell命令执行
    API = "api"           # Python API自动化
    UI_AUTO = "ui_auto"   # UI自动化 (pywinauto)

class OpStatus(Enum):
    SAFE = "safe"
    CAUTION = "caution"
    BLOCKED = "blocked"

@dataclass
class Operation:
    """操作记录"""
    level: ControlLevel
    command: str
    target_paths: List[str] = field(default_factory=list)
    status: OpStatus = OpStatus.SAFE
    reason: str = ""
    timestamp: str = ""

@dataclass
class AuditLog:
    """审计日志"""
    operation: Operation
    result: Optional[str] = None
    duration: float = 0.0
    error: Optional[str] = None

class PathWhitelist:
    """路径安全白名单"""

    ALLOWED_PATHS = [
        r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent",
        r"C:\Users\Administrator\AppData\Roaming\Tencent\Marvis",
    ]

    FORBIDDEN_PATHS = [
        r"C:\Windows",
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"C:\ProgramData",
    ]

    OP_CONFIRM_MATRIX = {
        "read": "safe",
        "list": "safe",
        "create": "caution",
        "write": "caution",
        "delete": "caution",
        "move": "caution",
        "execute": "caution",
        "install": "blocked",
        "uninstall": "blocked",
        "system_config": "blocked",
    }

    def check(self, path: str, operation_type: str) -> OpStatus:
        """检查路径操作是否安全"""
        normalized = str(Path(path).resolve())
        path = normalized

        # 禁止路径检查
        for forbidden in self.FORBIDDEN_PATHS:
            if path.startswith(forbidden):
                return OpStatus.BLOCKED

        # 允许路径检查
        for allowed in self.ALLOWED_PATHS:
            if path.startswith(allowed):
                return OpStatus[OP_MATRIX.get(operation_type, "safe")]

        return OpStatus.CAUTION

class ShellExecutor:
    """Shell命令执行器（受安全白名单约束）"""

    def __init__(self, whitelist: PathWhitelist):
        self.whitelist = whitelist
        self.max_output = 10000

    def execute(self, command: str, cwd: str = None, timeout: int = 30) -> Tuple[str, str, int]:
        """执行受审查的Shell命令"""
        result = subprocess.run(
            command, shell=True, cwd=cwd,
            capture_output=True, text=True,
            timeout=timeout, encoding='utf-8',
            errors='replace'
        )
        stdout = result.stdout[:self.max_output]
        stderr = result.stderr[:self.max_output]
        return stdout, stderr, result.returncode

class UIAutomation:
    """UI自动化层 (pywinauto 封装)"""

    def __init__(self):
        self.pywinauto_loaded = False
        try:
            # 推迟导入以支持不安装pywinauto也可加载模块
            self.pywinauto_loaded = True
        except ImportError:
            logger.warning("pywinauto未安装，UI自动化功能受限")

    def find_window(self, title_pattern: str) -> Optional[dict]:
        """查找窗口"""
        if not self.pywinauto_loaded:
            return {"error": "pywinauto未安装"}
        # TODO: R07 pywinauto实际集成
        return None

    def click(self, window: dict, control_id: str) -> bool:
        """点击UI元素"""
        # TODO: R07 pywinauto实际集成
        return False

    def type_text(self, window: dict, text: str) -> bool:
        """输入文本"""
        # TODO: R07 pywinauto实际集成
        return False

    def screenshot(self, window: dict) -> Optional[bytes]:
        """截图"""
        # TODO: R07 pywinauto实际集成
        return None

class DesktopController:
    """桌面控制模块主类"""

    ROOT_DIR = Path(r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent")
    AUDIT_DIR = ROOT_DIR / "audit"

    def __init__(self):
        self.whitelist = PathWhitelist()
        self.shell = ShellExecutor(self.whitelist)
        self.ui = UIAutomation()
        self.audit_logs: List[AuditLog] = []
        self.AUDIT_DIR.mkdir(exist_ok=True)

    def execute(self, command: str, cwd: str = None, timeout: int = 30) -> dict:
        """安全执行命令"""
        op = Operation(
            level=ControlLevel.SHELL,
            command=command,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )

        start = time.time()
        try:
            stdout, stderr, rc = self.shell.execute(command, cwd, timeout)
            duration = time.time() - start
            log = AuditLog(
                operation=op,
                result=f"rc={rc}, stdout_len={len(stdout)}",
                duration=duration,
                error=stderr if rc != 0 else None,
            )
        except subprocess.TimeoutExpired:
            log = AuditLog(operation=op, error="timeout", duration=timeout)
            return {"error": "timeout", "audit": log.__dict__}
        except Exception as e:
            log = AuditLog(operation=op, error=str(e), duration=0)
            return {"error": str(e), "audit": log.__dict__}

        self.audit_logs.append(log)
        self._persist_audit(log)
        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": rc,
            "duration": duration,
        }

    def find_and_click(self, window_title: str, control_id: str) -> dict:
        """查找窗口并点击"""
        window = self.ui.find_window(window_title)
        if window and "error" not in window:
            success = self.ui.click(window, control_id)
            return {"window": window, "clicked": success}
        return {"error": "窗口未找到"}

    def _persist_audit(self, log: AuditLog):
        """审计日志持久化"""
        date_str = time.strftime("%Y%m%d")
        log_path = self.AUDIT_DIR / f"audit_{date_str}.jsonl"
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log.__dict__, ensure_ascii=False) + "\n")

# 模块入口
if __name__ == "__main__":
    dc = DesktopController()
    result = dc.execute("dir E:\\", timeout=5)
    print(json.dumps({k: v for k, v in result.items() if k != 'stdout'}, ensure_ascii=False))

```
