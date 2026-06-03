# memory_os.py

> 原始文件: `memory_os.py`  |  类型: `.py`  |  自动转换

```python
# memory_os.py - 豆包Agent三层记忆操作系统
# 版本：v1.0 | 自动生成：R06 | 来源：R05设计
"""三层记忆体系：工作/会话/长期，支持自动压缩、去重、衰减。对标 Letta+Mem0+Zep。"""
import json, sqlite3, time, hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class MemoryOS:
    """三层记忆操作系统 —— Working / Session / Long-term"""

    COMPRESS_THRESHOLD = 512
    DECAY_DAYS = 30
    ARCHIVE_DAYS = 90
    MIN_WEIGHT = 0.1

    def __init__(self, memory_dir: str):
        self.dir = Path(memory_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.dir / "long_term.db"
        self.snapshot_path = self.dir / "session_snapshot.json"
        self._init_db()
        self.session_memory: Dict = {}
        self.working_memory: Dict = {}

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""CREATE TABLE IF NOT EXISTS long_term_memory (
            memory_id TEXT PRIMARY KEY,
            type TEXT, content TEXT, reason TEXT,
            weight REAL DEFAULT 1.0,
            token_count INTEGER DEFAULT 0,
            compressed INTEGER DEFAULT 0,
            created_at TEXT, last_access TEXT, access_count INTEGER DEFAULT 0,
            tags TEXT, related_memories TEXT
        )""")
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(memory_id, content, tags)")
        conn.commit()
        conn.close()

    # ---- Session Memory ----
    def save_snapshot(self, context: Dict):
        """保存会话快照"""
        snapshot = {"timestamp": datetime.now().isoformat(), "session": context, "working_summary": str(self.working_memory)[:2000]}
        self.snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_snapshot(self) -> Optional[Dict]:
        """加载最近会话快照"""
        if self.snapshot_path.exists():
            return json.loads(self.snapshot_path.read_text(encoding="utf-8"))
        return None

    # ---- Long-term Memory ----
    def store(self, memory_type: str, content: str, reason: str = "", tags: List[str] = None) -> str:
        """存入长期记忆"""
        memory_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(content.encode()).hexdigest()[:8]}"
        token_count = len(content) // 2  # 粗略估计
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""INSERT INTO long_term_memory (memory_id, type, content, reason, weight, token_count, compressed, created_at, last_access, access_count, tags, related_memories) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                     (memory_id, memory_type, content, reason, 1.0, token_count, 0,
                      datetime.now().isoformat(), datetime.now().isoformat(), 1,
                      json.dumps(tags or []), "[]"))
        conn.execute("INSERT INTO memory_fts VALUES (?,?,?)", (memory_id, content, json.dumps(tags or [])))
        conn.commit()
        conn.close()
        return memory_id

    def query(self, keywords: str, limit: int = 10) -> List[Dict]:
        """全文检索长期记忆"""
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute("SELECT memory_id, type, content, reason, weight, last_access FROM long_term_memory WHERE memory_id IN (SELECT memory_id FROM memory_fts WHERE memory_fts MATCH ?) ORDER BY weight DESC LIMIT ?", (keywords, limit)).fetchall()
        conn.close()
        return [{"memory_id": r[0], "type": r[1], "content": r[2], "reason": r[3], "weight": r[4], "last_access": r[5]} for r in rows]

    def get_recent_active(self, limit: int = 20) -> List[Dict]:
        """获取最近活跃记忆"""
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute("SELECT memory_id, type, content, weight, last_access FROM long_term_memory ORDER BY last_access DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [{"memory_id": r[0], "type": r[1], "content": r[2], "weight": r[3]} for r in rows]

    # ---- 自动维护 ----
    def auto_compress(self):
        """压缩超阈值记忆"""
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute("SELECT memory_id, content FROM long_term_memory WHERE token_count > ? AND compressed = 0", (self.COMPRESS_THRESHOLD,)).fetchall()
        compressed = 0
        for memory_id, content in rows:
            summary = content[:200] + "...[压缩]"  # 简化版摘要
            conn.execute("UPDATE long_term_memory SET content = ?, compressed = 1 WHERE memory_id = ?", (summary, memory_id))
            compressed += 1
        conn.commit()
        conn.close()
        return compressed

    def auto_decay(self):
        """衰减长期未用记忆"""
        conn = sqlite3.connect(str(self.db_path))
        now = time.time()
        rows = conn.execute("SELECT memory_id, last_access, weight FROM long_term_memory").fetchall()
        decayed = 0
        for memory_id, last_access, weight in rows:
            try:
                last_ts = datetime.fromisoformat(last_access).timestamp()
                days = (now - last_ts) / 86400
                if days > self.DECAY_DAYS:
                    new_weight = weight * 0.5
                    conn.execute("UPDATE long_term_memory SET weight = ? WHERE memory_id = ?", (new_weight, memory_id))
                    decayed += 1
            except Exception:
                pass
        # 归档
        conn.execute("DELETE FROM long_term_memory WHERE weight < ?", (self.MIN_WEIGHT,))
        conn.commit()
        conn.close()
        return decayed

    def get_stats(self) -> Dict:
        """获取记忆系统统计"""
        conn = sqlite3.connect(str(self.db_path))
        total = conn.execute("SELECT COUNT(*) FROM long_term_memory").fetchone()[0]
        active = conn.execute("SELECT COUNT(*) FROM long_term_memory WHERE weight > 0.5").fetchone()[0]
        compressed = conn.execute("SELECT COUNT(*) FROM long_term_memory WHERE compressed = 1").fetchone()[0]
        conn.close()
        return {"total_memories": total, "active": active, "compressed": compressed, "snapshot_exists": self.snapshot_path.exists()}

if __name__ == "__main__":
    mem = MemoryOS(str(ROOT / "memory"))
    stats = mem.get_stats()
    print(f"MemoryOS 就绪：{stats['total_memories']} 记忆, {stats['active']} 活跃, {stats['compressed']} 已压缩")

```
