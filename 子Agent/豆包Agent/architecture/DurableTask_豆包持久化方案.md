# Durable Task 豆包持久化方案

> **对标**：Azure Durable Task for AI Agents
> **目标**：豆包任务队列从 JSON 文件升级为持久化状态机
> **版本**：v1.0 Draft

---

## 一、当前痛点 → Durable方案

| 痛点 | 当前状态 | Durable方案 |
|------|---------|------------|
| 任务中断 | 崩溃后任务丢失 | 自动检查点+故障恢复重放 |
| 长时间等待 | ask_user阻塞无超时 | WaitForExternalEvent + TTL |
| 重试管理 | 无限制手动重试 | 指数退避+最大重试3次 |
| 状态追踪 | task_queue.json快照 | SQLite实时状态+变更日志 |
| 并发控制 | 无锁 | 乐观锁+版本号 |

## 二、持久化架构

```
┌─────────────────────────────────────────────┐
│             豆包任务调度器                      │
│  ┌───────────────────────────────────────┐  │
│  │    Orchestrator (任务编排)             │  │
│  │    - 任务创建 → 状态初始化              │  │
│  │    - 子任务分解 → Fan-out              │  │
│  │    - 结果聚合 → Fan-in                 │  │
│  └───────────────┬───────────────────────┘  │
│                  ↓                           │
│  ┌───────────────────────────────────────┐  │
│  │    Durable Task Runtime                │  │
│  │    - 检查点自动保存                     │  │
│  │    - 故障恢复重放                       │  │
│  │    - 心跳监控 + 超时检测                │  │
│  └───────────────┬───────────────────────┘  │
│                  ↓                           │
│  ┌───────────────────────────────────────┐  │
│  │    SQLite FTS5 持久化存储               │  │
│  │    - tasks 表：任务状态                 │  │
│  │    - checkpoints 表：检查点快照          │  │
│  │    - events 表：外部事件                │  │
│  │    - heartbeats 表：心跳记录             │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## 三、SQLite Schema

```sql
-- 任务表
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    parent_task_id TEXT,
    task_type TEXT NOT NULL,  -- 'shell', 'python', 'file_op', 'agent_dispatch'
    status TEXT NOT NULL,     -- 'pending','running','completed','failed','waiting_human','timeout'
    payload TEXT NOT NULL,    -- JSON: 任务参数
    result TEXT,              -- JSON: 执行结果
    error TEXT,               -- 错误信息
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT,
    ttl_seconds INTEGER,      -- 超时时间
    version INTEGER DEFAULT 1 -- 乐观锁版本号
);

-- 检查点表
CREATE TABLE checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    state_snapshot TEXT NOT NULL,  -- JSON: 完整状态快照
    created_at TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

-- 外部事件表（人类交互）
CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    event_type TEXT NOT NULL,  -- 'human_confirm', 'human_input', 'timeout'
    payload TEXT,              -- JSON: 事件数据
    status TEXT DEFAULT 'pending', -- 'pending','processed','expired'
    created_at TEXT NOT NULL,
    processed_at TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

-- 心跳表
CREATE TABLE heartbeats (
    task_id TEXT PRIMARY KEY,
    last_heartbeat TEXT NOT NULL,
    worker_id TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

-- 索引
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_parent ON tasks(parent_task_id);
CREATE INDEX idx_checkpoints_task ON checkpoints(task_id, sequence_number);
CREATE INDEX idx_events_task ON events(task_id, status);
```

## 四、状态机实现

```python
# durable_task_runner.py

import sqlite3
import json
import time
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_HUMAN = "waiting_human"
    TIMEOUT = "timeout"

class DurableTaskRunner:
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.heartbeat_interval = 30  # 秒
    
    async def run_task(self, task_id: str) -> dict:
        """执行任务，支持自动检查点和故障恢复"""
        
        # 检查是否有未完成的检查点
        checkpoint = self.load_latest_checkpoint(task_id)
        if checkpoint:
            # 故障恢复：从检查点继续
            state = json.loads(checkpoint["state_snapshot"])
            self.update_task_status(task_id, TaskStatus.RUNNING)
        else:
            # 新任务
            task = self.get_task(task_id)
            state = {"step": 0, "subtasks": [], "results": []}
            self.update_task_status(task_id, TaskStatus.RUNNING)
        
        # 启动心跳
        heartbeat_task = asyncio.create_task(self.heartbeat_loop(task_id))
        
        try:
            # 任务编排（可被检查点中断和恢复）
            while state["step"] < len(self.get_task(task_id)["steps"]):
                step = self.get_task(task_id)["steps"][state["step"]]
                
                # 执行当前步骤
                result = await self.execute_step(step, task_id)
                state["results"].append(result)
                
                # 检查是否需要人类确认
                if step.get("requires_confirmation"):
                    self.update_task_status(task_id, TaskStatus.WAITING_HUMAN)
                    # 等待外部事件
                    event = await self.wait_for_event(task_id, "human_confirm")
                    if event["status"] == "expired":
                        self.update_task_status(task_id, TaskStatus.TIMEOUT)
                        return {"status": "timeout"}
                
                state["step"] += 1
                
                # 自动保存检查点
                self.save_checkpoint(task_id, state)
            
            # 完成
            self.update_task_status(task_id, TaskStatus.COMPLETED)
            return {"status": "completed", "results": state["results"]}
            
        except Exception as e:
            # 失败处理
            task = self.get_task(task_id)
            retry_count = task["retry_count"]
            
            if retry_count < task["max_retries"]:
                # 重试
                self.increment_retry(task_id)
                # 等待指数退避
                await asyncio.sleep(2 ** retry_count)
                # 递归重试（检查点机制保证从上次位置继续）
                return await self.run_task(task_id)
            else:
                self.update_task_status(task_id, TaskStatus.FAILED)
                return {"status": "failed", "error": str(e)}
        
        finally:
            heartbeat_task.cancel()
    
    def save_checkpoint(self, task_id: str, state: dict):
        """保存检查点"""
        task = self.get_task(task_id)
        sequence = len(self.db.execute(
            "SELECT COUNT(*) FROM checkpoints WHERE task_id=?",
            (task_id,)
        ).fetchone())
        
        self.db.execute(
            """INSERT INTO checkpoints (task_id, sequence_number, state_snapshot, created_at)
               VALUES (?, ?, ?, ?)""",
            (task_id, sequence + 1, json.dumps(state), datetime.now().isoformat())
        )
        self.db.commit()
    
    async def wait_for_event(self, task_id: str, event_type: str) -> dict:
        """等待外部事件（人类确认等）"""
        ttl = self.get_task(task_id).get("ttl_seconds", 300)
        deadline = datetime.now() + timedelta(seconds=ttl)
        
        while datetime.now() < deadline:
            event = self.db.execute(
                "SELECT * FROM events WHERE task_id=? AND event_type=? AND status='processed'",
                (task_id, event_type)
            ).fetchone()
            
            if event:
                return dict(event)
            
            await asyncio.sleep(1)
        
        # 超时
        self.db.execute(
            "UPDATE events SET status='expired' WHERE task_id=? AND event_type=?",
            (task_id, event_type)
        )
        self.db.commit()
        return {"status": "expired"}
```

## 五、与Azure Durable Task对标

| 特性 | Azure Durable Task | 豆包Durable方案 | 实现状态 |
|------|-------------------|---------------|---------|
| 自动检查点 | ✅ Orchestrator自动 | ✅ save_checkpoint | 📋 设计完成 |
| 故障恢复 | ✅ 重放Orchestrator函数 | ✅ load_latest_checkpoint | 📋 设计完成 |
| 人类交互 | ✅ WaitForExternalEvent | ✅ wait_for_event | 📋 设计完成 |
| 超时取消 | ✅ Timer + CancellationToken | ✅ ttl_seconds + 定时检查 | 📋 设计完成 |
| 心跳监控 | ✅ 内置 | ✅ heartbeat_loop | 📋 设计完成 |
| 持久化存储 | ✅ Azure Storage | ✅ SQLite FTS5 | 📋 设计完成 |
| 跨语言SDK | ✅ .NET/Python/Java/JS | 🔧 Python优先 | 待规划 |
| 分布式协调 | ✅ Azure Service Bus | 🔧 单机优先 | 待规划 |

---

> 创建时间：2026-05-31 17:00
> 状态：设计完成 · SQLite Schema + Python骨架代码完成