# safe_guard.py

原始格式: Python

```python
"""
SafeGuard v2.0 - 三环安全护栏与检查点管理器
路径: 豆包Agent/技能库/SafeGuard/code/safe_guard.py
对标: self_evolve_agent SAFE/CAUTION/UNSAFE + DGM沙箱
"""

import hashlib
import json
import logging
import shutil
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

logger = logging.getLogger("SafeGuard")

class RiskLevel(Enum):
    SAFE = "SAFE"         # 直接放行
    CAUTION = "CAUTION"   # 需确认
    UNSAFE = "UNSAFE"     # 直接拒绝

class ReviewResult(Enum):
    PASS = "pass"
    WARN = "warn"
    BLOCK = "block"

@dataclass
class ReviewReport:
    """安全审查报告"""
    risk_level: RiskLevel
    result: ReviewResult
    warnings: List[str] = field(default_factory=list)
    blocked_reasons: List[str] = field(default_factory=list)
    timestamp: str = ""

@dataclass
class Checkpoint:
    """检查点快照"""
    checkpoint_id: str
    status: str  # stable / failed / manual
    snapshot: Dict[str, str] = field(default_factory=dict)  # {path: md5}
    diff_summary: str = ""
    validation: Dict[str, any] = field(default_factory=dict)
    rollback_cmd: str = ""
    created_at: str = ""

class PreExecutionReview:
    """外环：执行前审查"""

    DANGEROUS_PATTERNS = [
        "eval(", "exec(", "os.system(", "subprocess.call(",
        "rm -rf", "del /f", "format", "__import__('os')",
        "base64.b64decode", "compile(", "execfile(",
    ]

    FORBIDDEN_PATHS = [
        r"C:\Windows", r"C:\Program Files", r"C:\Program Files (x86)",
        r"C:\ProgramData",
    ]

    def review(self, code: str, target_paths: List[str] = None) -> ReviewReport:
        """五维审查"""
        warnings = []
        blocked = []

        # 1. 危险操作检测
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern in code:
                blocked.append(f"检测到危险操作: {pattern}")

        # 2. 系统路径检测
        if target_paths:
            for path in target_paths:
                for forbidden in self.FORBIDDEN_PATHS:
                    if path.startswith(forbidden):
                        blocked.append(f"禁止操作系统路径: {path}")

        # 3. 无限循环检测
        if "while True" in code and "break" not in code:
            warnings.append("检测到可能无限循环")

        # 4. 安全配置修改检测
        safe_config_keywords = ["SafeGuard", "SAFE_GUARD_CONFIG"]
        for kw in safe_config_keywords:
            if kw in code:
                blocked.append(f"禁止修改安全配置: {kw}")

        # 5. 恶意模式检测
        malicious = ["base64", "hidden", "stealth"]
        hits = [m for m in malicious if m in code.lower()]
        if len(hits) >= 2:
            blocked.append("检测到恶意模式特征")

        # 判定
        if blocked:
            return ReviewReport(
                risk_level=RiskLevel.UNSAFE,
                result=ReviewResult.BLOCK,
                blocked_reasons=blocked,
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
            )
        elif warnings:
            return ReviewReport(
                risk_level=RiskLevel.CAUTION,
                result=ReviewResult.WARN,
                warnings=warnings,
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
            )
        else:
            return ReviewReport(
                risk_level=RiskLevel.SAFE,
                result=ReviewResult.PASS,
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
            )

class RuntimeMonitor:
    """中环：运行时监控"""

    THRESHOLDS = {
        "cpu_warn": 80, "cpu_kill": 90,
        "memory_warn": 85, "memory_kill": 95,
        "time_warn": 1.5, "time_kill": 2.0,
        "file_ops_warn": 300, "file_ops_kill": 500,
        "network_conns_warn": 10, "network_conns_kill": 20,
    }

    def check(self, metrics: dict) -> ReviewReport:
        """运行时指标检查"""
        warnings = []
        blocked = []

        for metric, value in metrics.items():
            warn_key = f"{metric}_warn"
            kill_key = f"{metric}_kill"
            if kill_key in self.THRESHOLDS and value > self.THRESHOLDS[kill_key]:
                blocked.append(f"{metric} 超过终止阈值: {value}")
            elif warn_key in self.THRESHOLDS and value > self.THRESHOLDS[warn_key]:
                warnings.append(f"{metric} 超过告警阈值: {value}")

        if blocked:
            return ReviewReport(RiskLevel.UNSAFE, ReviewResult.BLOCK, blocked_reasons=blocked)
        elif warnings:
            return ReviewReport(RiskLevel.CAUTION, ReviewResult.WARN, warnings=warnings)
        return ReviewReport(RiskLevel.SAFE, ReviewResult.PASS)

class CheckpointManager:
    """内环：检查点管理器"""

    def __init__(self, checkpoints_dir: Path, agent_dir: Path):
        self.checkpoints_dir = checkpoints_dir
        self.agent_dir = agent_dir
        self.stable_ptr_path = checkpoints_dir / "stable_checkpoint.json"
        self.rollback_log_path = checkpoints_dir / "rollback_history.json"

    def create_checkpoint(self, label: str = "") -> Checkpoint:
        """创建检查点：计算所有文件MD5 → 生成快照"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        cp_id = f"checkpoint_{label}_{timestamp}" if label else f"checkpoint_{timestamp}"

        snapshot = {}
        for file_path in self.agent_dir.rglob("*"):
            if file_path.is_file() and ".git" not in str(file_path):
                md5 = self._file_md5(file_path)
                rel = str(file_path.relative_to(self.agent_dir))
                snapshot[rel] = md5

        cp = Checkpoint(
            checkpoint_id=cp_id,
            status="stable",
            snapshot=snapshot,
            diff_summary="",
            created_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )

        cp_path = self.checkpoints_dir / f"{cp_id}.json"
        with open(cp_path, 'w', encoding='utf-8') as f:
            json.dump(cp.__dict__, f, ensure_ascii=False, indent=2)

        # 更新稳定版本指针
        self._update_stable_ptr(cp_id)

        return cp

    def rollback(self, target_checkpoint_id: str = None) -> dict:
        """回滚到指定检查点"""
        if target_checkpoint_id is None:
            with open(self.stable_ptr_path, 'r') as f:
                ptr = json.load(f)
                target_checkpoint_id = ptr["current_stable"]

        cp_path = self.checkpoints_dir / f"{target_checkpoint_id}.json"
        if not cp_path.exists():
            return {"error": f"检查点不存在: {target_checkpoint_id}"}

        with open(cp_path, 'r', encoding='utf-8') as f:
            cp_data = json.load(f)

        # 对比Diff
        current_files = set()
        for fp in self.agent_dir.rglob("*"):
            if fp.is_file():
                current_files.add(str(fp.relative_to(self.agent_dir)))

        restored = 0
        for rel_path, expected_md5 in cp_data["snapshot"].items():
            file_path = self.agent_dir / rel_path
            if file_path.exists():
                actual_md5 = self._file_md5(file_path)
                if actual_md5 != expected_md5:
                    # TODO: R07 从备份源还原文件
                    restored += 1

        # 记录回滚
        self._log_rollback(target_checkpoint_id, restored)
        return {"rollback_to": target_checkpoint_id, "files_restored": restored}

    def validate(self) -> dict:
        """冒烟测试：验证核心功能"""
        core_files = [
            "任务队列/task_queue.json",
            "memory/long_term.db",
        ]
        results = {}
        for rel_path in core_files:
            fp = self.agent_dir / rel_path
            results[rel_path] = "ok" if fp.exists() else "missing"
        return results

    def _file_md5(self, file_path: Path) -> str:
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "ERROR"

    def _update_stable_ptr(self, checkpoint_id: str):
        ptr = {"current_stable": checkpoint_id}
        with open(self.stable_ptr_path, 'w', encoding='utf-8') as f:
            json.dump(ptr, f, indent=2)

    def _log_rollback(self, checkpoint_id: str, restored: int):
        log = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "checkpoint": checkpoint_id, "files_restored": restored}
        history = []
        if self.rollback_log_path.exists():
            with open(self.rollback_log_path, 'r') as f:
                data = json.load(f)
                history = data.get("history", [])
        history.append(log)
        with open(self.rollback_log_path, 'w', encoding='utf-8') as f:
            json.dump({"history": history}, f, indent=2)

class SafeGuard:
    """三环安全护栏主类"""

    ROOT_DIR = Path(r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent")
    CHECKPOINTS_DIR = ROOT_DIR / "checkpoints"

    def __init__(self):
        self.pre_review = PreExecutionReview()
        self.runtime_monitor = RuntimeMonitor()
        self.checkpoint_mgr = CheckpointManager(
            self.CHECKPOINTS_DIR, self.ROOT_DIR
        )

    def review_skill(self, skill_code: str, target_paths: List[str] = None) -> ReviewReport:
        """审查自动生成的技能代码"""
        return self.pre_review.review(skill_code, target_paths)

    def monitor_metrics(self, metrics: dict) -> ReviewReport:
        """运行时监控"""
        return self.runtime_monitor.check(metrics)

    def create_checkpoint(self, label: str = "") -> Checkpoint:
        """创建检查点"""
        return self.checkpoint_mgr.create_checkpoint(label)

# 模块入口
if __name__ == "__main__":
    sg = SafeGuard()
    report = sg.review_skill("print('hello')")
    print(f"审查结果: {report.risk_level.value} / {report.result.value}")

```
