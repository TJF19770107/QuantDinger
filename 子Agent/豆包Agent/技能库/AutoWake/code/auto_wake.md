# auto_wake.py

> 原始文件: `auto_wake.py`  |  类型: `.py`  |  自动转换

```python
"""
AutoWake v2.0 - 自主唤醒与执行引擎 (PES范式)
路径: 豆包Agent/技能库/AutoWake/code/auto_wake.py
对标: LoongFlow PES + Karpathy autoresearch
"""

import json
import time
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum

logger = logging.getLogger("AutoWake")

class Priority(Enum):
    P0 = 0  # 紧急
    P1 = 1  # 重要
    P2 = 2  # 常规
    P3 = 3  # 低优

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class SubTask:
    """PES拆分后的原子子任务"""
    id: str
    description: str
    priority: Priority
    timeout: int = 600
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[dict] = None

@dataclass
class Task:
    """任务队列项"""
    id: str
    priority: Priority
    type: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    timeout: int = 600
    retry_count: int = 0
    max_retries: int = 3
    sub_tasks: List[SubTask] = field(default_factory=list)
    pes_plan: Optional[dict] = None
    pes_summary: Optional[dict] = None

class PESEngine:
    """Plan-Execute-Summarize 任务拆分引擎
    对标 LoongFlow PES 认知范式
    """

    def __init__(self):
        self.max_parallel = 2
        self.meltdown_threshold = 0.9  # 90% CPU触发熔断

    def plan(self, task: Task) -> List[SubTask]:
        """Plan: 分析任务依赖 → 拆分为原子子任务 → 分配优先级"""
        logger.info(f"PES Plan: {task.id}")
        sub_tasks = []
        # TODO: R07 实现实际的任务依赖分析和子任务拆分
        return sub_tasks

    def execute(self, sub_tasks: List[SubTask]) -> Dict[str, TaskStatus]:
        """Execute: 无依赖并行 → 有依赖串行 → 实时监控"""
        results = {}
        no_dep = [st for st in sub_tasks if not st.dependencies]
        has_dep = [st for st in sub_tasks if st.dependencies]

        # 无依赖子任务：并行执行（最多max_parallel个）
        for i in range(0, len(no_dep), self.max_parallel):
            batch = no_dep[i:i + self.max_parallel]
            # TODO: R07 实际执行
            pass

        # 有依赖子任务：串行执行
        for st in has_dep:
            if all(results.get(dep) == TaskStatus.COMPLETED for dep in st.dependencies):
                # TODO: R07 实际执行
                pass

        return results

    def summarize(self, task: Task, results: Dict[str, TaskStatus]) -> dict:
        """Summarize: 聚合结果 → 提取可复用模式 → 归档"""
        logger.info(f"PES Summarize: {task.id}")
        summary = {
            "task_id": task.id,
            "total": len(task.sub_tasks),
            "completed": sum(1 for s in results.values() if s == TaskStatus.COMPLETED),
            "failed": sum(1 for s in results.values() if s == TaskStatus.FAILED),
            "timeout": sum(1 for s in results.values() if s == TaskStatus.TIMEOUT),
        }
        return summary

class PriorityQueue:
    """优先级任务队列（支持抢占）"""

    def __init__(self):
        self.queue: List[Task] = []

    def enqueue(self, task: Task):
        self.queue.append(task)
        self.queue.sort(key=lambda t: t.priority.value)

    def dequeue(self) -> Optional[Task]:
        pending = [t for t in self.queue if t.status == TaskStatus.PENDING]
        return pending[0] if pending else None

    def preempt(self, new_task: Task) -> Optional[Task]:
        """P0任务抢占当前运行的P1-P3任务"""
        if new_task.priority == Priority.P0:
            running = [t for t in self.queue if t.status == TaskStatus.RUNNING]
            if running and running[0].priority.value > 0:
                preempted = running[0]
                preempted.status = TaskStatus.PENDING
                self.enqueue(new_task)
                return preempted
        self.enqueue(new_task)
        return None

class AutoWake:
    """自主唤醒引擎主类"""

    ROOT_DIR = Path(r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent")
    TASK_QUEUE_PATH = ROOT_DIR / "task_queue.json"

    def __init__(self):
        self.queue = PriorityQueue()
        self.pes = PESEngine()
        self.running = False
        self.wake_count = 0

    def trigger(self, reason: str = "manual") -> dict:
        """唤醒入口：加载任务队列 → 优先级排序 → 逐项PES执行"""
        self.wake_count += 1
        logger.info(f"AutoWake triggered (reason={reason}, count={self.wake_count})")

        tasks = self._load_task_queue()
        for task_data in tasks:
            task = self._parse_task(task_data)
            if task.status == TaskStatus.PENDING:
                self.queue.enqueue(task)

        results = self._execute_all()
        return {
            "wake_count": self.wake_count,
            "executed": len(results),
            "completed": sum(1 for r in results.values() if r == TaskStatus.COMPLETED),
        }

    def _load_task_queue(self) -> list:
        """从 task_queue.json 加载任务列表"""
        if self.TASK_QUEUE_PATH.exists():
            with open(self.TASK_QUEUE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("tasks", [])
        return []

    def _parse_task(self, data: dict) -> Task:
        """解析JSON任务数据为Task对象"""
        return Task(
            id=data.get("id", ""),
            priority=Priority[data.get("priority", "P3")],
            type=data.get("type", ""),
            description=data.get("description", ""),
            timeout=data.get("timeout", 600),
        )

    def _execute_all(self) -> Dict[str, TaskStatus]:
        """逐项PES执行所有待处理任务"""
        results = {}
        while True:
            task = self.queue.dequeue()
            if not task:
                break

            task.status = TaskStatus.RUNNING
            # PES: Plan → Execute → Summarize
            task.sub_tasks = self.pes.plan(task)
            sub_results = self.pes.execute(task.sub_tasks)
            task.pes_summary = self.pes.summarize(task, sub_results)

            all_ok = all(s == TaskStatus.COMPLETED for s in sub_results.values())
            task.status = TaskStatus.COMPLETED if all_ok else TaskStatus.FAILED
            results[task.id] = task.status

        return results

    def sleep(self):
        """保存状态 → 进入休眠"""
        self.running = False
        logger.info(f"AutoWake entering sleep (wake_count={self.wake_count})")
        return {"status": "sleeping", "wake_count": self.wake_count}

# 模块入口
if __name__ == "__main__":
    aw = AutoWake()
    result = aw.trigger(reason="manual_test")
    print(json.dumps(result, ensure_ascii=False, default=str))
    aw.sleep()

```
