# auto_wake.py

> 原始文件: `auto_wake.py`  |  类型: `.py`  |  自动转换

```python
# auto_wake.py - 豆包Agent自主唤醒引擎
# 版本：v1.0 | 自动生成：R06 | 来源：R05设计
"""管理唤醒-执行-归档-休眠循环，维护任务优先级队列。"""
import json, time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class AutoWakeEngine:
    """自主唤醒引擎 —— 优先级队列 + 定时/事件/监听三模式"""

    PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

    def __init__(self, agent_root: str):
        self.root = Path(agent_root)
        self.queue_file = self.root / "task_queue.json"
        self.log_dir = self.root / "迭代记录"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.task_queue: List[Dict] = self._load_queue()

    def _load_queue(self) -> List[Dict]:
        if self.queue_file.exists():
            return json.loads(self.queue_file.read_text(encoding="utf-8")).get("tasks", [])
        return self._default_queue()

    def _default_queue(self) -> List[Dict]:
        return [
            {"id": "iter_global", "priority": "P1", "type": "iteration",
             "description": "每3小时全域闭环迭代（P0专项补全+技能锻造+情报采集）",
             "status": "pending", "created_at": datetime.now().isoformat(), "timeout": 900, "retry_count": 0},
            {"id": "scan_files", "priority": "P2", "type": "auto_scan",
             "description": "AutoFileScanner 扫描目录变化并注册能力",
             "status": "pending", "trigger": "wake", "timeout": 120, "retry_count": 0},
            {"id": "skill_forge", "priority": "P2", "type": "skill_forge",
             "description": "SkillForge 从迭代日志自动锻造新技能",
             "status": "pending", "trigger": "post_iteration", "timeout": 300, "retry_count": 0},
            {"id": "memory_compress", "priority": "P3", "type": "maintenance",
             "description": "MemoryOS 压缩长期记忆、清理过期条目",
             "status": "pending", "trigger": "wake", "timeout": 180, "retry_count": 0},
            {"id": "health_check", "priority": "P2", "type": "health",
             "description": "SafeGuard 系统健康检查 + 检查点验证",
             "status": "pending", "trigger": "wake", "timeout": 120, "retry_count": 0},
        ]

    def save_queue(self):
        self.queue_file.write_text(json.dumps({"tasks": self.task_queue, "updated": datetime.now().isoformat()}, ensure_ascii=False, indent=2), encoding="utf-8")

    def prioritize(self) -> List[Dict]:
        """按优先级P0>P1>P2>P3排序，同优先级按创建时间"""
        self.task_queue.sort(key=lambda t: (self.PRIORITY_ORDER.get(t["priority"], 99), t.get("created_at", "")))
        return self.task_queue

    def get_pending(self, max_priority: str = "P3") -> List[Dict]:
        """获取待执行任务（不超过指定优先级）"""
        max_p = self.PRIORITY_ORDER.get(max_priority, 99)
        return [t for t in self.task_queue if t["status"] == "pending" and self.PRIORITY_ORDER.get(t["priority"], 99) <= max_p]

    def mark_completed(self, task_id: str, result: Dict):
        for t in self.task_queue:
            if t["id"] == task_id:
                t["status"] = "completed"
                t["completed_at"] = datetime.now().isoformat()
                t["result"] = result
                break
        self.save_queue()

    def mark_failed(self, task_id: str, error: str):
        for t in self.task_queue:
            if t["id"] == task_id:
                t["retry_count"] += 1
                t["status"] = "failed" if t["retry_count"] >= 3 else "pending"
                t["last_error"] = error
                break
        self.save_queue()

    def add_task(self, priority: str, description: str, task_type: str = "manual", timeout: int = 600):
        task = {"id": f"task_{int(time.time())}", "priority": priority, "type": task_type,
                "description": description, "status": "pending",
                "created_at": datetime.now().isoformat(), "timeout": timeout, "retry_count": 0}
        self.task_queue.append(task)
        self.save_queue()
        return task

    def archive_log(self, summary: Dict) -> Path:
        """归档执行日志"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = self.log_dir / f"auto_exec_log_{ts}.md"
        content = f"# AutoWake 执行日志\n> 时间：{datetime.now().isoformat()}\n\n## 任务执行摘要\n"
        for t in self.task_queue[-10:]:
            content += f"- [{t['priority']}] {t['id']}: {t['status']}\n"
        content += f"\n## 系统状态\n{json.dumps(summary, ensure_ascii=False, indent=2)}\n"
        log_path.write_text(content, encoding="utf-8")
        return log_path

if __name__ == "__main__":
    aw = AutoWakeEngine(str(ROOT))
    aw.prioritize()
    aw.save_queue()
    pending = aw.get_pending()
    print(f"AutoWake 就绪：{len(aw.task_queue)} 任务，{len(pending)} 待执行")

```
