# kanban_task_board.py

> 原始文件: `kanban_task_board.py`  |  类型: `.py`  |  自动转换

```python
"""
Kanban TaskBoard v1.0
对标: Hermes SWARM Kanban Board + SQLite持久化
"""

import sqlite3
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, List


class TaskStatus(Enum):
    TODO = "todo"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    TIMEOUT = "timeout"


class KanbanTaskBoard:
    """
    Kanban看板式任务管理
    状态流: todo → ready → in_progress → done/failed/timeout

    CREATE TABLE tasks (
        id TEXT PRIMARY KEY,
        profile TEXT,
        params TEXT,
        status TEXT,
        agent_id TEXT,
        created_at TEXT,
        updated_at TEXT,
        timeout_at TEXT,
        retry_count INTEGER DEFAULT 0,
        handoff TEXT
    );
    """

    DB_PATH = "checkpoints/kanban.db"
    SCAN_INTERVAL = 60
    MAX_RETRY = 3
    TIMEOUT_MINUTES = 30

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                profile TEXT NOT NULL,
                params TEXT DEFAULT '{}',
                status TEXT DEFAULT 'todo',
                agent_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                timeout_at TEXT,
                retry_count INTEGER DEFAULT 0,
                max_retry INTEGER DEFAULT 3,
                handoff TEXT,
                priority INTEGER DEFAULT 5
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS task_history (
                id TEXT,
                status TEXT,
                agent_id TEXT,
                changed_at TEXT,
                result TEXT
            )
        """)
        self.conn.commit()

    def create_task(self, profile: str, params: dict = None,
                    priority: int = 5, max_retry: int = None) -> str:
        """创建任务 → todo"""
        import uuid
        task_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO tasks (id, profile, params, status, created_at, updated_at, priority, max_retry) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (task_id, profile, json.dumps(params or {}), TaskStatus.TODO.value, now, now, priority, max_retry or self.MAX_RETRY)
        )
        self.conn.commit()
        return task_id

    def dispatch_ready(self) -> list:
        """扫描ready状态 → 分配给Worker"""
        self.conn.execute(
            "UPDATE tasks SET status=? WHERE status=?",
            (TaskStatus.READY.value, TaskStatus.TODO.value)
        )
        cursor = self.conn.execute(
            "SELECT * FROM tasks WHERE status=? ORDER BY priority ASC, created_at ASC",
            (TaskStatus.READY.value,)
        )
        tasks = [self._row_to_dict(row) for row in cursor.fetchall()]
        return tasks

    def start_task(self, task_id: str, agent_id: str) -> bool:
        """Worker开始执行 → in_progress"""
        now = datetime.now().isoformat()
        timeout = (datetime.now() + timedelta(minutes=self.TIMEOUT_MINUTES)).isoformat()
        self.conn.execute(
            "UPDATE tasks SET status=?, agent_id=?, updated_at=?, timeout_at=? WHERE id=?",
            (TaskStatus.IN_PROGRESS.value, agent_id, now, timeout, task_id)
        )
        self.conn.commit()

    def complete_task(self, task_id: str, handoff: str = None) -> None:
        """Worker完成 → done"""
        now = datetime.now().isoformat()
        self.conn.execute(
            "UPDATE tasks SET status=?, updated_at=?, handoff=? WHERE id=?",
            (TaskStatus.DONE.value, now, handoff, task_id)
        )
        self.conn.commit()

    def fail_task(self, task_id: str, reason: str) -> Optional[str]:
        """任务失败 → 判断重试"""
        row = self.conn.execute("SELECT retry_count, max_retry FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row[0] < row[1]:
            self.conn.execute(
                "UPDATE tasks SET status=?, retry_count=retry_count+1, updated_at=?, handoff=? WHERE id=?",
                (TaskStatus.TODO.value, datetime.now().isoformat(), f"Retry {row[0]+1}: {reason}", task_id)
            )
            self.conn.commit()
            return "retry"
        else:
            self.conn.execute(
                "UPDATE tasks SET status=?, updated_at=?, handoff=? WHERE id=?",
                (TaskStatus.FAILED.value, datetime.now().isoformat(), reason, task_id)
            )
            self.conn.commit()
            return "failed"

    def recover_timeout(self) -> list:
        """超时回收"""
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            "SELECT * FROM tasks WHERE status=? AND timeout_at < ?",
            (TaskStatus.IN_PROGRESS.value, now)
        )
        timeout_tasks = [self._row_to_dict(row) for row in cursor.fetchall()]
        for task in timeout_tasks:
            self.conn.execute(
                "UPDATE tasks SET status=?, updated_at=?, retry_count=retry_count+1 WHERE id=?",
                (TaskStatus.TODO.value, now, task["id"])
            )
        self.conn.commit()
        return timeout_tasks

    def _row_to_dict(self, row) -> dict:
        return {
            "id": row[0], "profile": row[1], "params": row[2],
            "status": row[3], "agent_id": row[4],
            "created_at": row[5], "updated_at": row[6],
            "timeout_at": row[7], "retry_count": row[8],
            "max_retry": row[9], "handoff": row[10],
            "priority": row[11]
        }

print("[KanbanTaskBoard] v1.0 加载完成")
```
