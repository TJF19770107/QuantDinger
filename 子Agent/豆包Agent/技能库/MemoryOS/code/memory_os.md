# memory_os.py

原始格式: Python

```python
"""
MemoryOS v2.0 - 三层记忆操作系统 (WISE-Flow增强)
路径: 豆包Agent/技能库/MemoryOS/code/memory_os.py
对标: Letta/Mem0/Zep + WISE-Flow + OpenClaw Memory
"""

import json
import sqlite3
import time
import hashlib
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum

logger = logging.getLogger("MemoryOS")

class MemoryType(Enum):
    WORKING = "working"     # 工作记忆（单任务）
    SESSION = "session"     # 会话记忆（单次唤醒）
    LONG_TERM = "long_term" # 长期语义记忆（跨会话）

@dataclass
class Memory:
    """记忆单元"""
    memory_id: str
    type: MemoryType
    content: str
    weight: float = 1.0
    created_at: str = ""
    last_access: str = ""
    access_count: int = 0
    token_count: int = 0
    tags: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)
    compressed: bool = False
    privacy_label: bool = False  # 敏感内容标记

class MemoryCompressor:
    """记忆压缩引擎"""

    COMPRESS_THRESHOLD = 512  # token数超过此值触发压缩
    DECAY_THRESHOLD_DAYS = 30  # 30天未访问 → 权重×0.5
    ARCHIVE_THRESHOLD_DAYS = 90  # 90天未访问且权重<0.1 → 归档

    def should_compress(self, memory: Memory) -> bool:
        return memory.token_count > self.COMPRESS_THRESHOLD and not memory.compressed

    def compress(self, memory: Memory, summary: str) -> Memory:
        """LLM摘要压缩"""
        memory.content = summary
        memory.compressed = True
        memory.token_count = len(summary)
        return memory

    def apply_decay(self, memory: Memory) -> Memory:
        """时间衰减：超过阈值天数权重折半"""
        from datetime import datetime, timedelta
        if not memory.last_access:
            return memory
        try:
            last = datetime.fromisoformat(memory.last_access)
            days_since = (datetime.now() - last).days
            if days_since > self.DECAY_THRESHOLD_DAYS:
                memory.weight *= 0.5
            if days_since > self.ARCHIVE_THRESHOLD_DAYS and memory.weight < 0.1:
                memory.weight = 0  # 标记淘汰
        except ValueError:
            pass
        return memory

class WorkflowMemoryExtractor:
    """WISE-Flow 工作流结构化记忆提取器"""

    def extract_workflow(self, task_log: dict) -> Optional[Memory]:
        """从任务执行日志中提取结构化工作流记忆
        对标 WISE-Flow: 工作流引导的结构化经验
        """
        if not task_log.get("pes_summary"):
            return None

        workflow = {
            "task_id": task_log.get("id"),
            "plan": task_log.get("pes_plan"),
            "execute_duration": task_log.get("duration"),
            "summarize": task_log.get("pes_summary"),
        }
        memory = Memory(
            memory_id=f"wf_{task_log.get('id', '')}",
            type=MemoryType.LONG_TERM,
            content=json.dumps(workflow, ensure_ascii=False),
            tags=["workflow", "pes", task_log.get("type", "")],
        )
        return memory

class MemoryOS:
    """三层记忆操作系统主类"""

    ROOT_DIR = Path(r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent")
    MEMORY_DIR = ROOT_DIR / "memory"
    DB_PATH = MEMORY_DIR / "long_term.db"
    SNAPSHOT_PATH = MEMORY_DIR / "session_snapshot.json"
    COMPRESS_LOG_PATH = MEMORY_DIR / "compress_log.json"

    def __init__(self):
        self.compressor = MemoryCompressor()
        self.workflow_extractor = WorkflowMemoryExtractor()
        self.working_memory: List[Memory] = []
        self.session_memory: Dict[str, Memory] = {}
        self._init_db()

    def _init_db(self):
        """初始化SQLite长期记忆数据库"""
        self.MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.DB_PATH))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS long_term_memory (
                memory_id TEXT PRIMARY KEY,
                type TEXT,
                content TEXT,
                weight REAL DEFAULT 1.0,
                created_at TEXT,
                last_access TEXT,
                access_count INTEGER DEFAULT 0,
                token_count INTEGER DEFAULT 0,
                tags TEXT,
                related_memories TEXT,
                compressed INTEGER DEFAULT 0,
                privacy_label INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts
            USING fts5(content, tags, content=long_term_memory, content_rowid=rowid)
        """)
        conn.commit()
        conn.close()

    def auto_load(self) -> dict:
        """唤醒时自动加载：恢复会话快照 + 检索长期记忆"""
        stats = {"session_restored": 0, "long_term_loaded": 0}

        # 恢复会话快照
        if self.SNAPSHOT_PATH.exists():
            with open(self.SNAPSHOT_PATH, 'r', encoding='utf-8') as f:
                snapshot = json.load(f)
                stats["session_restored"] = len(snapshot)

        # 检索长期记忆
        conn = sqlite3.connect(str(self.DB_PATH))
        cursor = conn.execute(
            "SELECT COUNT(*) FROM long_term_memory WHERE weight > 0.1"
        )
        stats["long_term_loaded"] = cursor.fetchone()[0]
        conn.close()

        # 应用衰减
        self._apply_decay_to_all()

        logger.info(f"记忆加载完成: {stats}")
        return stats

    def write(self, memory: Memory):
        """写入记忆到对应层级"""
        memory.created_at = memory.created_at or time.strftime("%Y-%m-%dT%H:%M:%S")
        memory.last_access = time.strftime("%Y-%m-%dT%H:%M:%S")
        memory.access_count += 1

        if memory.type == MemoryType.WORKING:
            self.working_memory.append(memory)
        elif memory.type == MemoryType.SESSION:
            self.session_memory[memory.memory_id] = memory
        elif memory.type == MemoryType.LONG_TERM:
            self._write_to_db(memory)

    def query(self, keyword: str, limit: int = 10) -> List[Memory]:
        """全文检索长期记忆"""
        conn = sqlite3.connect(str(self.DB_PATH))
        cursor = conn.execute(
            "SELECT * FROM memory_fts WHERE memory_fts MATCH ? LIMIT ?",
            (keyword, limit)
        )
        results = []
        for row in cursor:
            results.append(self._row_to_memory(row))
        conn.close()
        return results

    def compress_all(self) -> dict:
        """压缩所有超阈值记忆"""
        stats = {"compressed": 0, "skipped": 0}
        conn = sqlite3.connect(str(self.DB_PATH))
        cursor = conn.execute(
            "SELECT * FROM long_term_memory WHERE token_count > ? AND compressed = 0",
            (self.compressor.COMPRESS_THRESHOLD,)
        )
        for row in cursor:
            memory = self._row_to_memory(row)
            if self.compressor.should_compress(memory):
                # TODO: R07 LLM摘要
                stats["compressed"] += 1
            else:
                stats["skipped"] += 1
        conn.close()
        return stats

    def persist(self) -> bool:
        """持久化：保存会话快照到磁盘"""
        snapshot = {
            mid: {
                "content": m.content,
                "weight": m.weight,
                "tags": m.tags,
            }
            for mid, m in self.session_memory.items()
        }
        with open(self.SNAPSHOT_PATH, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        return True

    def _write_to_db(self, memory: Memory):
        conn = sqlite3.connect(str(self.DB_PATH))
        conn.execute("""
            INSERT OR REPLACE INTO long_term_memory
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory.memory_id, memory.type.value, memory.content, memory.weight,
            memory.created_at, memory.last_access, memory.access_count,
            memory.token_count, json.dumps(memory.tags),
            json.dumps(memory.related_memories),
            1 if memory.compressed else 0,
            1 if memory.privacy_label else 0
        ))
        conn.commit()
        conn.close()

    def _apply_decay_to_all(self):
        conn = sqlite3.connect(str(self.DB_PATH))
        cursor = conn.execute("SELECT * FROM long_term_memory")
        for row in cursor:
            memory = self._row_to_memory(row)
            memory = self.compressor.apply_decay(memory)
            if memory.weight == 0:
                conn.execute("DELETE FROM long_term_memory WHERE memory_id = ?", (memory.memory_id,))
        conn.commit()
        conn.close()

    def _row_to_memory(self, row: tuple) -> Memory:
        return Memory(
            memory_id=row[0],
            type=MemoryType(row[1]),
            content=row[2],
            weight=row[3],
            created_at=row[4],
            last_access=row[5],
            access_count=row[6],
            token_count=row[7],
            tags=json.loads(row[8]) if row[8] else [],
            related_memories=json.loads(row[9]) if row[9] else [],
            compressed=bool(row[10]),
            privacy_label=bool(row[11]),
        )

# 模块入口
if __name__ == "__main__":
    mos = MemoryOS()
    stats = mos.auto_load()
    print(json.dumps(stats, ensure_ascii=False))

```
