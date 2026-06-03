
# AutoFileScanner v1.0 — 本地文件自主读取能力

> 技能ID：SKILL_AUTO_FILE_SCANNER_v1.0  
> 状态：ACTIVE  
> 创建：2026-05-31 R08  
> 依赖：MemoryOS v2.0  
> 被依赖：SkillForge v3.0, SafeGuard v3.0, DesktopController v2.0

---

## 一、技能定位

AutoFileScanner 是豆包Agent的文件感知层，负责自主扫描、索引、监测Agent目录下所有文件的结构与内容变化，并将结构化结果注入 MemoryOS，使Agent具备"知道自己有什么文件、文件里有 什么内容"的元认知能力。

```
AutoFileScanner ───→ MemoryOS (文件元数据写入记忆)
       │
       ├──→ SkillForge (技能文件变更通知)
       ├──→ SafeGuard (关键文件校验)
       └──→ DesktopController (文件操作预备)
```

---

## 二、核心能力

### 2.1 目录结构扫描

自动扫描以下目录的完整文件树：

| 扫描范围 | 路径模式 | 用途 |
|---------|---------|------|
| 技能库 | `技能库/*.md` | 所有已注册技能文件 |
| 记忆存储 | `memory/*.json`, `memory/*.db` | 长短期记忆数据 |
| 架构引擎 | `architecture/*.py`, `architecture/*.md` | 核心Python引擎+设计文档 |
| 迭代报告 | `*报告*.md`, `*R*_*.md` | 全轮次迭代报告 |
| 检查点 | `checkpoints/*.json` | 版本快照与回滚数据 |

### 2.2 文件内容解析

| 格式 | 解析方式 | 提取内容 |
|------|---------|---------|
| Markdown (.md) | 正则提取 YAML Front Matter + 标题层级 | 文档元数据、章节结构、关键词 |
| JSON (.json) | `json.load()` | 结构化数据摘要 |
| Python (.py) | AST 解析 | 类/函数签名、import依赖、docstring |
| SQLite (.db) | sqlite3 连接 | 表结构、行数统计 |
| PDF/DOCX/XLSX | 委托 read_file 工具 | 文本摘要（前500字） |

### 2.3 文件索引缓存

```
memory/
├── file_index.json          ← 全量文件索引缓存
│   {
│     "schema_version": "1.0",
│     "last_scan": "2026-05-31T12:00:00",
│     "files": {
│       "技能库/auto-file-scanner-v1.0.md": {
│         "hash": "md5:abc123...",
│         "size_bytes": 12345,
│         "modified": "2026-05-31T10:00:00",
│         "type": "skill",
│         "dependencies": ["memory-os-v2.0"],
│         "keywords": ["扫描", "索引", "文件"]
│       }
│     }
│   }
└── scan_diff.json           ← 增量变更记录
```

### 2.4 增量更新机制

每次扫描对比 `file_index.json` 中的 hash，仅处理变更文件：

```
全量扫描（首次） → file_index.json
       ↓
后续定时扫描 → 对比 hash
       ↓
    变更集 → 仅解析变更文件
       ↓
    更新 file_index.json + 写入 MemoryOS
```

---

## 三、接口定义

### 3.1 Python 类接口

```python
class AutoFileScanner:
    """本地文件自主扫描器"""

    def __init__(self, root_path: str, memory_os=None, safe_guard=None):
        """
        Args:
            root_path: 豆包Agent根目录绝对路径
            memory_os: MemoryOS实例，用于写入文件元数据记忆
            safe_guard: SafeGuard实例，用于关键文件校验
        """
        self.root = Path(root_path)
        self.memory_os = memory_os
        self.safe_guard = safe_guard
        self.index_path = self.root / "memory" / "file_index.json"
        self.scan_diff_path = self.root / "memory" / "scan_diff.json"

    def full_scan(self) -> ScanReport:
        """全量扫描所有目录，生成完整文件索引。
        
        Returns:
            ScanReport: 包含文件清单、解析摘要、统计信息
        """
        ...

    def incremental_scan(self) -> ScanReport:
        """增量扫描，仅处理自上次扫描以来变更的文件。
        
        对比 index 中的 hash，筛选出 added/modified/deleted 文件，
        仅解析变更文件以节省资源。
        
        Returns:
            ScanReport: 仅包含变更部分
        """
        ...

    def load_skill_files(self) -> Dict[str, SkillMetadata]:
        """加载技能库中所有 .md 文件的 Front Matter 元数据。
        
        Returns:
            {文件名: SkillMetadata对象}，包含 name/version/status/deps
        """
        ...

    def load_memory_files(self) -> MemoryBundle:
        """加载 memory/ 下所有 JSON 和 SQLite 数据。
        
        Returns:
            MemoryBundle: 包含 short_term, long_term, episodic
        """
        ...

    def load_architecture_modules(self) -> Dict[str, str]:
        """加载 architecture/ 下所有 .py 文件的代码内容。
        
        Returns:
            {模块名: Python源码}
        """
        ...

    def parse_file(self, file_path: Path) -> ParsedFile:
        """根据文件类型自动路由到对应解析器。
        
        路由规则:
        - .md → _parse_markdown()
        - .json → _parse_json()
        - .py → _parse_python()
        - .db → _parse_sqlite()
        - .pdf/.docx → 委托 read_file 工具
        """
        ...

    def write_to_memory(self, report: ScanReport) -> None:
        """将扫描结果写入 MemoryOS。
        
        写入内容包括:
        - 文件清单摘要（作为短期记忆）
        - 技能库依赖图（作为长期记忆）
        - 架构模块签名（作为长期记忆）
        """
        ...
```

### 3.2 数据结构

```python
@dataclass
class ScanReport:
    scan_id: str          # 扫描唯一ID
    scan_time: str        # ISO格式时间戳
    scan_type: str        # "full" / "incremental"
    total_files: int      # 总文件数
    added: List[str]      # 新增文件路径
    modified: List[str]   # 修改文件路径
    deleted: List[str]    # 删除文件路径
    parse_errors: List[Dict]  # 解析失败列表
    skill_manifest: Dict[str, SkillMetadata]  # 技能清单
    architecture_manifest: Dict[str, str]  # 架构模块清单
    summary: str          # 人类可读摘要

@dataclass
class SkillMetadata:
    name: str             # 技能名称
    version: str          # 版本号
    status: str           # ACTIVE/DRAFT/DEPRECATED
    dependencies: List[str]  # 依赖技能列表
    keywords: List[str]   # 关键词
    summary: str          # 摘要


@dataclass
class ParsedFile:
    path: str
    type: str             # markdown/json/python/sqlite/pdf/docx
    hash: str             # MD5
    size_bytes: int
    modified: str
    content_summary: str  # 内容摘要（前500字）
    metadata: dict        # 格式特定元数据

@dataclass
class MemoryBundle:
    short_term: List[dict]
    long_term: List[dict]
    episodic: List[dict]
    file_index: dict
```

---

## 四、使用方式

### 4.1 初始化扫描（Agent启动时）

```python
from auto_file_scanner import AutoFileScanner

scanner = AutoFileScanner(
    root_path="E:/龙虾AI主控中心/我的AI分身/子Agent/豆包Agent/",
    memory_os=memory_os_instance,
    safe_guard=safe_guard_instance
)

# Agent启动时执行全量扫描
report = scanner.full_scan()
scanner.write_to_memory(report)
print(f"[AutoFileScanner] 扫描完成: {report.total_files}个文件")
```

### 4.2 定时增量扫描（AutoWake调度）

```python
# AutoWake定时任务触发
def scheduled_scan():
    report = scanner.incremental_scan()
    if report.added or report.modified:
        scanner.write_to_memory(report)
        # 如有新技能文件，通知 SkillForge
        if any("技能库" in f for f in report.added):
            skill_forge.on_new_skill_detected(report.added)
```

### 4.3 文件变更监视（SafeGuard联动）

```python
# SafeGuard 调用校验
def verify_critical_files():
    report = scanner.incremental_scan()
    critical = [f for f in report.modified 
                if "architecture" in f or "checkpoints" in f]
    if critical:
        return safe_guard.review_changes(critical, report)
```

---

## 五、与其他技能的接口契约

| 调用方 | 接口 | 数据流向 |
|--------|------|---------|
| MemoryOS | `write_to_memory(report)` | 文件索引+摘要 → 记忆存储 |
| SkillForge | `load_skill_files()` | 技能元数据 → 技能锻造 |
| AutoWake | `incremental_scan()` | 变更通知 → 唤醒判断 |
| SafeGuard | `parse_file(path)` | 文件hash → 完整性校验 |
| DesktopController | `list_files(pattern)` | 文件列表 → 桌面操作 |

---

## 六、性能约束

| 指标 | 约束值 | 说明 |
|------|--------|------|
| 全量扫描上限 | 10,000文件 | 超过则分批+摘要 |
| 单文件解析上限 | 10MB | 超大文件仅提取hash |
| 增量扫描间隔 | ≥60秒 | 避免频繁IO |
| JSON索引文件上限 | 50MB | 超过则归档旧索引 |
| 并发解析数 | ≤4 | 避免CPU峰值 |

---

## 七、安全约束

- 不扫描系统目录（`C:\Windows`, `C:\Program Files` 等）
- 不读取 `.env`, `.git-credentials`, `.ssh` 等敏感文件
- 所有文件解析在只读模式进行，不修改原始文件
- 索引缓存写入前检查磁盘空间（>100MB 可用）

---

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-05-31 R08 | 初始版本：完整文件扫描+索引缓存+增量更新+MemoryOS联动 |
