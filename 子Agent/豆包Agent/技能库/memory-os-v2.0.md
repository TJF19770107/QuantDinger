
# MemoryOS v2.0 — 记忆自动加载与长期记忆能力

> 技能ID：SKILL_MEMORY_OS_v2.0  
> 状态：ACTIVE  
> 创建：2026-05-31 R08（v1.0 升级至 v2.0）  
> 上一版本：v1.0 (R06)  
> 依赖：AutoFileScanner v1.0  
> 被依赖：SkillForge v3.0, AutoWake v2.0, SafeGuard v3.0, 自进化闭环

---

## 一、技能定位

MemoryOS 是豆包Agent的"记忆中枢"，负责所有历史迭代记忆的加载、压缩、持久化和检索。它使Agent具备跨会话的长 期记忆能力，并且越迭代越"聪明"——每次迭代自动更新用户画像和Agent能力画像，形成正向增强循环。

```
MemoryOS v2.0
    │
    ├── 短期记忆 (ShortTermMemory)
    │   ├── 最近N轮对话上下文
    │   └── 当前会话的临时状态
    │
    ├── 长期记忆 (LongTermMemory)
    │   ├── 用户画像 (user_profile.json)
    │   ├── Agent能力画像 (agent_profile.json)
    │   ├── 迭代历史 (iteration_history.json)
    │   ├── 技能演变史 (skill_evolution.json)
    │   └── 事件日志 (events.db / events.jsonl)
    │
    └── 情景记忆 (EpisodicMemory)
        ├── 关键里程碑事件
        ├── 失败/成功模式记录
        └── 跨域迁移经验
```

---

## 二、核心能力（v2.0 增强项）

### 2.1 三层次记忆架构

```
┌──────────────────────────────────────────┐
│          MemoryOS 三层记忆架构            │
├──────────────────────────────────────────┤
│                                          │
│  Layer 1: 短期记忆（Working Memory）      │
│  ├── 容量：最近32K tokens                │
│  ├── 生命周期：当前会话                   │
│  └── 存储：内存中（Python dict + deque）  │
│                                          │
│  Layer 2: 长期记忆（Long-term Memory）    │
│  ├── 容量：无限（仅受磁盘限制）           │
│  ├── 生命周期：永久                       │
│  ├── 存储：SQLite + JSON 双存储           │
│  └── 自动压缩：超过7天的详细日志→摘要     │
│                                          │
│  Layer 3: 情景记忆（Episodic Memory）     │
│  ├── 容量：关键事件 ~1000条               │
│  ├── 生命周期：永久（高价值事件）         │
│  └── 存储：SQLite events表               │
│                                          │
└──────────────────────────────────────────┘
```

### 2.2 自动记忆压缩

```python
class MemoryCompressor:
    """记忆自动压缩器"""
    
    COMPRESSION_RULES = {
        "age_threshold_days": 7,       # 超过7天的详细日志
        "retain_recent_count": 100,    # 保留最近100条原始记录
        "summary_template": """
            [压缩区间] {start_date} ~ {end_date}
            总事件数: {event_count}
            成功: {success_count} | 失败: {failure_count}
            主要活动: {top_activities}
            关键产出: {key_artifacts}
        """,
    }
    
    def compress(self) -> CompressionReport:
        """执行记忆压缩。
        
        1. 扫描 events 表，找出超过7天的记录
        2. 按天分组，生成每日摘要
        3. 将原始记录归档到 events_archive 表
        4. 释放短期记忆空间
        """
        ...
```

### 2.3 跨会话永久保留

```
memory/
├── short_term/
│   └── session_context.json      ← 当前会话临时上下文
├── long_term/
│   ├── user_profile.json         ← 用户画像（永久）
│   ├── agent_profile.json        ← Agent能力画像（永久）
│   ├── iteration_history.json    ← 迭代历史摘要（永久）
│   ├── skill_evolution.json      ← 技能演变史（永久）
│   └── gap_backlog.json          ← 缺口清单（永久）
├── episodic/
│   └── events.db                 ← 事件日志 SQLite（永久）
├── file_index.json               ← AutoFileScanner写入
└── scan_diff.json                ← AutoFileScanner写入
```

### 2.4 记忆检索接口

```python
class MemoryRetriever:
    """记忆检索器 - 多模式检索"""
    
    def by_time(self, start: str, end: str) -> List[MemoryEntry]:
        """按时间范围检索"""
        ...
    
    def by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        """按标签检索"""
        ...
    
    def by_keywords(self, keywords: List[str]) -> List[MemoryEntry]:
        """按关键词全文检索"""
        ...
    
    def by_type(self, entry_type: str) -> List[MemoryEntry]:
        """按类型检索：event/gap/skill/iteration"""
        ...
    
    def recent(self, n: int = 10) -> List[MemoryEntry]:
        """最近N条记忆"""
        ...
    
    def relevant_to(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """语义相关性检索（与查询最相关的记忆）"""
        ...
```

---

## 三、接口定义

### 3.1 Python 类接口

```python
class MemoryOS:
    """记忆操作系统 v2.0"""

    def __init__(
        self,
        memory_dir: str,                 # memory/ 目录路径
        auto_file_scanner=None           # AutoFileScanner实例
    ):
        self.memory_dir = Path(memory_dir)
        self.scanner = auto_file_scanner
        self.short_term = ShortTermMemory(max_tokens=32000)
        self.long_term = LongTermMemory(self.memory_dir / "long_term")
        self.episodic = EpisodicMemory(self.memory_dir / "episodic" / "events.db")
        self.compressor = MemoryCompressor(self.episodic)
        self.retriever = MemoryRetriever(
            self.short_term, self.long_term, self.episodic
        )

    # ========== 记忆写入 ==========

    def record_event(self, event: MemoryEvent) -> str:
        """记录一个事件到情景记忆。
        
        Args:
            event: {type, timestamp, summary, tags, detail, importance}
        
        Returns:
            event_id
        """
        self.episodic.insert(event)
        if event.importance >= 0.7:
            self.short_term.add(event)  # 高重要性事件也推入短期记忆
        return event.event_id

    def update_user_profile(self, updates: dict) -> None:
        """增量更新用户画像。
        
        Args:
            updates: 新增或变更的用户偏好/习惯/需求字段
        """
        ...

    def update_agent_profile(self, updates: dict) -> None:
        """增量更新Agent能力画像。
        
        Args:
            updates: 新增能力/技能等级提升/缺口修补
        """
        ...

    def record_iteration(self, iteration_report: dict) -> None:
        """记录一次迭代的全量数据。
        
        写入内容：
        - 迭代摘要 → iteration_history.json
        - 缺口变化 → gap_backlog.json
        - 技能变化 → skill_evolution.json
        - 关键事件 → events.db
        """
        ...

    # ========== 记忆检索 ==========

    def retrieve_relevant(self, query: str, context_window: dict) -> str:
        """为推理引擎加载相关上下文。
        
        检索策略：
        1. 短期记忆中匹配最近会话上下文
        2. 长期记忆中检索相关历史
        3. 情景记忆中提取关键事件
        4. 合并为结构化上下文字符串
        
        Returns:
            格式化上下文文本（<32000 tokens）
        """
        ...

    def search(self, mode: str, **kwargs) -> List[MemoryEntry]:
        """多模式记忆搜索。
        
        mode: "time" / "tags" / "keywords" / "type" / "recent" / "relevant"
        """
        ...

    # ========== 记忆维护 ==========

    def compress_old_memories(self) -> CompressionReport:
        """执行记忆压缩（AutoWake定时触发）。"""
        return self.compressor.compress()

    def load_from_files(self) -> LoadReport:
        """从文件系统自动加载所有记忆。
        
        与 AutoFileScanner 联动：
        1. 调用 scanner.load_memory_files()
        2. 加载 JSON 文件到 long_term
        3. 加载 SQLite 数据库到 episodic
        4. 验证数据完整性
        """
        ...

    def export_memory_snapshot(self) -> str:
        """导出当前全部记忆为 JSON 快照文件。"""
        ...

    # ========== 统计查询 ==========

    def get_stats(self) -> MemoryStats:
        """获取记忆系统统计信息。"""
        ...

    def get_user_profile(self) -> dict:
        """获取当前用户画像。"""
        ...

    def get_agent_profile(self) -> dict:
        """获取当前Agent能力画像。"""
        ...
```

### 3.2 数据结构

```python
@dataclass
class MemoryEvent:
    event_id: str
    type: str            # iteration/skill/gap/safety/file/evolution
    timestamp: str       # ISO8601
    summary: str         # 一句话摘要
    tags: List[str]      # 标签
    detail: dict         # 详细信息
    importance: float    # 0-1，越高越不易被压缩

@dataclass
class MemoryEntry:
    entry_id: str
    source: str          # short_term / long_term / episodic
    content: str
    metadata: dict
    relevance_score: float = 0.0

@dataclass
class CompressionReport:
    events_compressed: int
    events_retained: int
    summary_generated: str
    released_bytes: int

@dataclass
class MemoryStats:
    short_term_count: int
    long_term_count: int
    episodic_count: int
    total_size_bytes: int
    last_compression: str
    user_profile_version: int
    agent_profile_version: int

@dataclass
class LoadReport:
    loaded_files: int
    loaded_events: int
    errors: List[str]
    total_size: int
```

---

## 四、用户画像与Agent能力画像

### 4.1 用户画像

```json
{
  "version": 3,
  "updated_at": "2026-05-31T14:00:00",
  "preferences": {
    "language": "zh-CN",
    "output_style": "structured_markdown",
    "confirmation_mode": "auto_for_low_risk",
    "working_hours": "09:00-23:00",
    "silent_mode_hours": "23:00-09:00"
  },
  "habits": {
    "frequently_accessed_dirs": [
      "E:/龙虾AI主控中心/",
      "D:/Documents/"
    ],
    "preferred_tools": ["python_executor", "shell_executor"],
    "common_tasks": ["迭代报告生成", "文件整理", "技术调研"]
  },
  "goals": {
    "short_term": ["补齐R08 6大技能", "完成SICA首次进化"],
    "long_term": ["豆包Agent全自主运行", "10项缺口全部补齐"]
  }
}
```

### 4.2 Agent能力画像

```json
{
  "version": 5,
  "updated_at": "2026-05-31T14:00:00",
  "skills": {
    "total": 30,
    "active": 28,
    "deprecated": 2,
    "by_category": {
      "scanner": 1,
      "controller": 1,
      "memory": 1,
      "safety": 1,
      "forge": 1,
      "evolution": 3
    }
  },
  "gaps": {
    "total_identified": 10,
    "resolved": 6,
    "in_progress": 2,
    "unresolved": 2
  },
  "capability_scores": {
    "autonomous_execution": 0.80,
    "self_evolution": 0.70,
    "memory_retention": 0.75,
    "safety_awareness": 0.85,
    "desktop_control": 0.65,
    "skill_generation": 0.60
  },
  "evolution_metrics": {
    "total_iterations": 8,
    "success_rate": 0.875,
    "avg_improvement": 0.12,
    "genes_registered": 12
  }
}
```

---

## 五、记忆检索 SQLite Schema

```sql
-- 事件日志表
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    summary TEXT NOT NULL,
    tags TEXT,               -- JSON数组
    detail TEXT,             -- JSON
    importance REAL DEFAULT 0.5,
    session_id TEXT
);

-- 事件归档表（压缩后的原始数据）
CREATE TABLE IF NOT EXISTS events_archive (
    archive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compressed_range_start TEXT,
    compressed_range_end TEXT,
    event_count INTEGER,
    summary_text TEXT,
    original_detail TEXT     -- GZIP压缩后的JSON
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_events_type ON events(type);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_importance ON events(importance DESC);
```

---

## 六、与其他技能的接口契约

| 调用方 | 接口 | 数据流向 |
|--------|------|---------|
| AutoFileScanner | `load_from_files()` | 文件数据 → 记忆系统 |
| Claude推理引擎 | `retrieve_relevant(query, ctx)` | 上下文 → 推理引擎 |
| SkillForge | `record_event("skill_created")` | 技能事件 → 事件日志 |
| AutoWake | `compress_old_memories()` | 定时任务 → 记忆压缩 |
| SafeGuard | `record_event("safety_incident")` | 安全事件 → 事件日志 |
| 自进化闭环 | `record_iteration(report)` | 迭代数据 → 长期记忆 |

---

## 七、越迭代越强机制

```
每次迭代后:
1. 记录迭代结果 → events.db
2. 更新缺口修补进度 → gap_backlog.json
3. 如有新技能 → skill_evolution.json + agent_profile.json
4. 如有新发现 → user_profile.json (用户需求变化)
5. 更新能力评分 → agent_profile.json

效果：
R01: 能力评分 0.20 → 仅基础文件操作
R04: 能力评分 0.40 → SkillForge落地
R06: 能力评分 0.55 → 6模块代码骨架
R07: 能力评分 0.70 → 推理引擎+工作流+SICA
R08: 能力评分 0.80 → 6大自主能力补齐（目标）
```

---

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | R06 | 初始版本：JSON文件存储+基础检索 |
| v2.0 | R08 | 增强：三层架构、SQLite双存储、自动压缩、用户画像+Agent画像、AutoFileScanner联动 |
