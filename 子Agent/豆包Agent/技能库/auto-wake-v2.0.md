
# AutoWake v2.0 — 自主唤醒与自主执行能力

> 技能ID：SKILL_AUTO_WAKE_v2.0  
> 状态：ACTIVE  
> 创建：2026-05-31 R08（v1.0 升级至 v2.0）  
> 上一版本：v1.0 (R06)  
> 依赖：MemoryOS v2.0, SafeGuard v3.0, DesktopController v2.0, SkillForge v3.0  
> 被依赖：自进化闭环

---

## 一、技能定位

AutoWake 是豆包Agent的"心跳"和"自主驱动系统"，负责定时唤醒Agent、自主判断任务优先级、管理任务队列、执行自动化任务循环。它使Agent在无人交互时仍能自主迭代、检索、学习和维护自身，是实现 "Agent在没有人类干预下自主进化" 的关键基础设施。

```
AutoWake v2.0
    │
    ├── 调度器 (scheduler)
    │   ├── 定时唤醒（2小时迭代循环）
    │   ├── 心跳检测（每分钟）
    │   └── 条件触发（文件变更/异常检测）
    │
    ├── 优先级引擎 (priority engine)
    │   └── 紧急度 × 影响度 矩阵
    │
    ├── 任务队列 (task queue - SQLite)
    │   └── 持久化任务状态，支持断点续跑
    │
    └── 执行引擎 (execution engine)
        ├── 迭代任务 → 自进化闭环
        ├── 检索任务 → MemoryOS / 全网搜索
        ├── 维护任务 → SafeGuard / DesktopController
        └── 学习任务 → SkillForge / SICA Evolver
```

---

## 二、核心能力（v2.0 增强项）

### 2.1 定时唤醒机制

```python
class WakeScheduler:
    """唤醒调度器"""
    
    SCHEDULES = {
        "iteration_cycle":    3600 * 2,    # 每2小时：全维度迭代
        "heartbeat":          60,           # 每分钟：心跳检测
        "file_scan":          3600,         # 每小时：文件扫描
        "memory_compress":    3600 * 6,     # 每6小时：记忆压缩
        "gap_analysis":       3600 * 4,     # 每4小时：缺口分析
        "safety_check":       3600 * 1,     # 每小时：安全检查
        "nightly_maintenance": "03:00",     # 每天凌晨3点：深度维护
    }
    
    def start(self):
        """启动所有定时任务。"""
        ...
    
    def stop(self):
        """停止所有定时任务。"""
        ...
    
    def get_next_wake_time(self) -> dict:
        """获取所有任务的下次唤醒时间。"""
        ...
```

### 2.2 优先级矩阵

```
               影响度
            低      中      高
         ┌───────┬───────┬───────┐
    高   │  P2   │  P1   │  P0   │  ← 立即执行
紧急度 中   │  P3   │  P2   │  P1   │  ← 排队执行
    低   │  P4   │  P3   │  P2   │  ← 可延后
         └───────┴───────┴───────┘

紧急度 = f(截止时间, 依赖任务数, 阻塞下游数)
影响度 = f(能力缺口权重, 系统稳定性, 用户可见性)
```

### 2.3 任务队列（SQLite 持久化）

```sql
CREATE TABLE task_queue (
    task_id         TEXT PRIMARY KEY,
    task_type       TEXT NOT NULL,     -- iteration/search/maintenance/learning
    priority        TEXT NOT NULL,     -- P0/P1/P2/P3/P4
    status          TEXT NOT NULL,     -- pending/running/completed/failed/paused
    payload         TEXT,              -- JSON: 任务参数
    result          TEXT,              -- JSON: 执行结果
    created_at      TEXT NOT NULL,
    started_at      TEXT,
    completed_at    TEXT,
    retry_count     INTEGER DEFAULT 0,
    max_retries     INTEGER DEFAULT 3,
    dependencies    TEXT,              -- JSON: 前置任务ID列表
    error_message   TEXT
);

CREATE TABLE heartbeat_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL,
    status          TEXT NOT NULL,     -- OK/WARNING/CRITICAL
    metrics         TEXT,              -- JSON: CPU/内存/磁盘
    active_tasks    INTEGER,
    pending_tasks   INTEGER,
    message         TEXT
);
```

### 2.4 静默运行模式

```python
class SilentMode:
    """静默运行模式：不打扰用户"""
    
    enabled: bool = True
    
    def should_notify_user(self, task: Task, result: ActionResult) -> bool:
        """判断是否需要通知用户。
        
        仅在以下情况通知：
        - 任务失败且重试耗尽
        - 检测到需要用户确认的高风险操作
        - 达到预定义的里程碑
        """
        if result.success:
            return False
        if task.retry_count < task.max_retries:
            return False
        return True
```

---

## 三、接口定义

### 3.1 Python 类接口

```python
class AutoWake:
    """自主唤醒引擎 v2.0"""

    def __init__(
        self,
        db_path: str = None,               # SQLite数据库路径
        memory_os=None,                    # MemoryOS实例
        safe_guard=None,                   # SafeGuard实例
        desktop_controller=None,           # DesktopController实例
        skill_forge=None,                  # SkillForge实例
        evolution_orchestrator=None,       # EvolutionOrchestrator实例
        heartbeat_path: str = None         # HEARTBEAT.md路径
    ):
        self.db = TaskQueueDB(db_path or "memory/task_queue.db")
        self.scheduler = WakeScheduler()
        self.priority_engine = PriorityEngine()
        self.memory = memory_os
        self.safe_guard = safe_guard
        self.desktop = desktop_controller
        self.forge = skill_forge
        self.evolution = evolution_orchestrator
        self.heartbeat_path = heartbeat_path
        self.silent_mode = SilentMode()

    # ========== 生命周期 ==========

    def start(self) -> None:
        """启动AutoWake引擎。
        
        1. 初始化SQLite数据库（如不存在则建表）
        2. 加载未完成任务到队列
        3. 启动所有定时任务
        4. 写入首次心跳
        """
        ...

    def stop(self) -> None:
        """优雅停止：完成当前任务后停止调度器。"""
        ...

    def pause(self) -> None:
        """暂停所有定时任务（不取消运行中的任务）。"""
        ...

    def resume(self) -> None:
        """恢复所有定时任务。"""
        ...

    # ========== 任务管理 ==========

    def enqueue(self, task: Task) -> str:
        """将任务加入队列。
        
        Args:
            task: 任务对象
        
        Returns:
            task_id
        """
        ...

    def dequeue(self) -> Optional[Task]:
        """从队列中取出优先级最高的就绪任务。
        
        规则：
        1. 优先级 P0 > P1 > P2 > P3 > P4
        2. 同优先级按创建时间 FIFO
        3. 跳过依赖未完成的任务
        """
        ...

    def execute_task(self, task: Task) -> ActionResult:
        """执行单个任务。
        
        根据 task_type 路由到对应执行器：
        - iteration → 自进化闭环
        - search → MemoryOS检索 / 全网搜索
        - maintenance → SafeGuard检查 / 文件整理
        - learning → SkillForge技能萃取
        """
        ...

    # ========== 心跳 ==========

    def heartbeat(self) -> HeartbeatReport:
        """执行心跳检测并写入 HEARTBEAT.md。
        
        检测项目：
        - Agent进程是否存活
        - 数据库连接是否正常
        - 磁盘空间是否充足（>100MB）
        - 任务队列是否有积压
        - 上次迭代是否正常完成
        
        Returns:
            HeartbeatReport
        """
        ...

    # ========== 主循环 ==========

    def main_loop(self) -> None:
        """自主执行主循环（守护进程模式）。
        
        while True:
            1. 检查是否有到期的定时任务
            2. 从队列取出最高优先级任务
            3. 执行任务
            4. 写入心跳
            5. 休眠直到下次唤醒
        """
        ...
```

### 3.2 数据结构

```python
@dataclass
class Task:
    task_id: str
    task_type: str        # iteration/search/maintenance/learning
    priority: str         # P0-P4
    status: str           # pending/running/completed/failed/paused
    payload: dict         # 任务参数
    result: Optional[dict] = None
    created_at: str = ""
    started_at: str = ""
    completed_at: str = ""
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    error_message: str = ""

@dataclass
class HeartbeatReport:
    timestamp: str
    status: str           # OK / WARNING / CRITICAL
    cpu_percent: float
    memory_mb: float
    disk_free_gb: float
    active_tasks: int
    pending_tasks: int
    last_iteration: str
    messages: List[str]
```

---

## 四、任务类型定义

| 任务类型 | 触发频率 | 执行的Skill | 优先级 |
|---------|---------|------------|--------|
| `iteration` | 每2小时 | 自进化闭环 | P1 |
| `gap_analysis` | 每4小时 | MemoryOS检索 + 全网扫描 | P2 |
| `file_scan` | 每小时 | AutoFileScanner | P2 |
| `memory_compress` | 每6小时 | MemoryOS | P3 |
| `safety_check` | 每小时 | SafeGuard | P1 |
| `nightly_maintenance` | 每天03:00 | 全模块健康检查 | P3 |
| `skill_forge_cycle` | 每8小时 | SkillForge | P2 |
| `report_generation` | 每次迭代后 | 自进化闭环 | P1 |

---

## 五、HEARTBEAT.md 格式

```markdown
# 豆包Agent 心跳日志
> 最后更新：2026-05-31 14:30:00

| 时间 | 状态 | CPU | 内存 | 磁盘 | 活跃任务 | 待处理 | 备注 |
|------|------|-----|------|------|---------|--------|------|
| 14:30 | OK | 12% | 256MB | 45GB | 1 | 3 | 正常 |
| 14:29 | OK | 15% | 248MB | 45GB | 1 | 3 | 正常 |
| 14:28 | OK | 10% | 240MB | 45GB | 0 | 4 | 空闲 |

## 今日统计
- 总唤醒次数：28
- 完成任务：24
- 失败任务：1 (task_id: iter_R08_03, 错误: timeout)
- 平均CPU：14%
- 平均内存：250MB
```

---

## 六、自主执行模式

### 6.1 默认模式（全自动）

```python
aw = AutoWake(...)
aw.start()

# Agent 自主运行，每2小时执行一次全维度迭代：
# 1. 心跳检测（每分钟）
# 2. 扫描文件变化（每小时）
# 3. 安全检查（每小时）
# 4. 全维度迭代（每2小时）- 核心任务
# 5. 缺口分析（每4小时）
# 6. 记忆压缩（每6小时）
# 7. 技能萃取（每8小时）
```

### 6.2 按需唤醒

```python
# 外部事件触发（如接收到新指令）
aw.enqueue(Task(
    task_id="adhoc_001",
    task_type="iteration",
    priority="P0",
    payload={"target": "immediate"}
))
```

---

## 七、与其他技能的接口契约

| 调用方 | 被调用方 | 接口 | 触发时机 |
|--------|---------|------|---------|
| AutoWake | MemoryOS | `retrieve_relevant()` | 缺口分析时检索历史 |
| AutoWake | SafeGuard | `health_check()` | 安全检查任务 |
| AutoWake | DesktopController | `get_system_info()` | 心跳检测时采集指标 |
| AutoWake | SkillForge | `extract_from_iteration()` | 技能萃取任务 |
| AutoWake | AutoFileScanner | `incremental_scan()` | 文件扫描任务 |
| AutoWake | 自进化闭环 | `full_cycle()` | 迭代任务 |

---

## 八、SQLite 任务队列实现骨架

```python
class TaskQueueDB:
    """基于SQLite的任务持久化队列"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS task_queue (
                    task_id TEXT PRIMARY KEY,
                    task_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    payload TEXT,
                    result TEXT,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    started_at TEXT,
                    completed_at TEXT,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    dependencies TEXT,
                    error_message TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS heartbeat_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
                    status TEXT NOT NULL,
                    metrics TEXT,
                    active_tasks INTEGER DEFAULT 0,
                    pending_tasks INTEGER DEFAULT 0,
                    message TEXT
                )
            """)
    
    def push(self, task: Task) -> str:
        """入队"""
        ...
    
    def pop(self) -> Optional[Task]:
        """出队（最高优先级就绪任务）"""
        ...
    
    def update_status(self, task_id: str, status: str, result: dict = None):
        """更新任务状态"""
        ...
    
    def get_stats(self) -> dict:
        """获取队列统计"""
        ...
```

---

## 九、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | R06 | 初始版本：基础定时唤醒 |
| v2.0 | R08 | 增强：SQLite任务队列持久化、优先级矩阵、心跳日志、静默模式、全模块联动 |
