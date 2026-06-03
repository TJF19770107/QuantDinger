# AutoFileScanner v4.0 — FileSense 智能文件感知系统

> **版本**: v4.0 (FileSense) | **迭代来源**: R18 迭代报告 §4.1  
> **升级类型**: P0 架构跃升 | **前身**: AutoFileScanner v1.0 (R17)  
> **创建日期**: 2026-05-31 | **拥有者**: 豆包Agent  
> **对标系统**: LangChain Document Loaders + LlamaIndex File Agents + ChromaDB RAG  
> **能力基线映射**: 文件读取缺口 — 补齐增量监听、语义索引、沙箱化文件访问

---

## 目录

1. [架构概览](#1-架构概览)
2. [R18 升级说明](#2-r18-升级说明)
3. [系统架构图](#3-系统架构图)
4. [核心模块设计](#4-核心模块设计)
   - 4.1 FileWatcher — 文件变更监听
   - 4.2 ParserPool — 多格式解析器池
   - 4.3 SemanticIndexer — 语义索引引擎
   - 4.4 RAGRetriever — Agent 检索接口
   - 4.5 PermissionController — 沙箱权限白名单
   - 4.6 AuditTrail — 操作审计追踪
5. [Python 实现代码](#5-python-实现代码)
6. [部署指南](#6-部署指南)
7. [R18 报告对应关系](#7-r18-报告对应关系)
8. [性能基线](#8-性能基线)

---

## 1. 架构概览

### 1.1 设计哲学

AutoFileScanner v4.0 从「被动扫描」升级为 **自主感知 + 语义理解 + 安全访问** 三位一体的文件智能系统。

```
v1.0 模式: 用户指令 → 五阶段静态流水线 → 返回结果
v4.0 模式: 文件变更事件 → 实时感知 → 增量索引 → 语义 RAG 检索 → 沙箱安全返回
```

核心突破：
- **实时性**：watchdog 事件驱动替换定时轮询，延迟从分钟级降至毫秒级
- **语义性**：文件分块 → 向量嵌入 → ChromaDB 存储，支持自然语言检索
- **安全性**：路径白名单 + Windows Integrity Levels + 操作审计，防止越权访问

### 1.2 与 R17 能力基线对比

| 维度 | R17 (v1.0) | R18 (v4.0 FileSense) | 提升 |
|------|-----------|---------------------|------|
| 扫描模式 | 五阶段静态流水线 | 事件驱动 + 增量扫描 | 实时性 ↑ |
| 内容索引 | 文件名/元数据 | 语义分块 + 向量嵌入 | 语义性 ↑ |
| 检索方式 | SQL LIKE / glob | 自然语言 RAG | 可用性 ↑ |
| 权限模型 | 全路径访问 | 白名单 + 沙箱隔离 | 安全性 ↑ |
| 审计能力 | 无 | 结构化操作日志 | 可追溯 ↑ |
| 代码规模 | ~230 行 | ~800 行 | 功能密度 ↑ |
| 对接系统 | 独立 | SafeGuard + MemoryOS | 协同性 ↑ |

---

## 2. R18 升级说明

### 2.1 变更来源

基于 R18 迭代报告 §4.1「文件读取能力路线 (AutoFileScanner v1.0 → v2.0)」，执行以下 P0 升级：

| R18 任务编号 | 升级项 | 优先级 | 预估耗时 |
|-------------|--------|--------|---------|
| 1.1 | watchdog 文件变更监听 | P0 | 30min |
| 1.2 | ChromaDB 语义索引 + RAG 检索 | P0 | 30min |
| 1.4 (扩展) | 权限白名单 + 沙箱路径隔离 | P1 | 10min |

### 2.2 保留的 v1.0 能力

- ✅ 目录树遍历与文件发现
- ✅ 多格式文件类型识别（扩展名 + magic bytes）
- ✅ 文件元数据提取（大小/时间/类型）
- ✅ 文件注册表（file_index.json）

### 2.3 新增的 v4.0 能力

- 🆕 **watchdog 实时文件监听**：`FileSystemEventHandler`，支持 create/modify/delete/move 四类事件
- 🆕 **语义分块引擎**：`RecursiveCharacterTextSplitter`，chunk_size=512，chunk_overlap=64
- 🆕 **ChromaDB 向量存储**：本地持久化，HNSW 索引，支持增量 upsert
- 🆕 **Agent RAG 检索接口**：`query("最近修改的合同")` 自然语言 → 语义 Top-K 结果
- 🆕 **安全权限白名单**：`PermissionController` 路径级访问控制 + Windows Integrity Levels
- 🆕 **审计日志**：结构化操作记录（操作类型/路径/时间戳/风险评分）

---

## 3. 系统架构图

### 3.1 整体架构

```
┌──────────────────────────────────────────────────────────────────────┐
│                     AutoFileScanner v4.0 — FileSense                  │
│                        智能文件感知系统架构                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐  │
│  │   FileWatcher   │───▶│   EventRouter    │───▶│   ParserPool     │  │
│  │  (watchdog)     │    │  (事件分类分发)    │    │  (多格式解析器池)  │  │
│  └──────┬──────────┘    └────────┬──────────┘    └────────┬─────────┘  │
│         │ create/modify           │                        │           │
│         │ delete/move             │                        ▼           │
│         │                         │              ┌──────────────────┐  │
│         │                         │              │  ChunkEngine     │  │
│         │                         │              │ (RecursiveSplit) │  │
│         │                         │              └────────┬─────────┘  │
│         │                         │                        │           │
│         │                         │                        ▼           │
│         │                         │              ┌──────────────────┐  │
│         │                         │              │   Embedder       │  │
│         │                         │              │ (text-embedding) │  │
│         │                         │              └────────┬─────────┘  │
│         │                         │                        │           │
│         │                         │                        ▼           │
│         │                         │              ┌──────────────────┐  │
│         │                         └─────────────▶│  VectorStore     │  │
│         │                                        │  (ChromaDB)      │  │
│         │                                        └────────┬─────────┘  │
│         │                                                  │           │
│         │                                                  ▼           │
│         │                                        ┌──────────────────┐  │
│         │                                        │  RAGRetriever   │  │
│         │                                        │ (Agent查询接口)   │  │
│         │                                        └────────┬─────────┘  │
│         │                                                  │           │
│         ▼                                                  ▼           │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                   PermissionController (安全层)                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐│  │
│  │  │Path Whitelist│  │Integrity Level│  │   AuditTrail (审计日志)  ││  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘│  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              外部队列 (跨模块协同)                                  │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐│  │
│  │  │ SafeGuard    │  │ MemoryOS     │  │  MissionControl           ││  │
│  │  │ (沙箱验证)    │  │ (记忆索引)    │  │  (任务调度)                ││  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘│  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 数据流（文件变更 → 索引 → 检索）

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ watchdog │───▶│ Event    │───▶│ Parser   │───▶│ Chunker  │───▶│ Embedder │
│ 事件检测  │    │ 分类     │    │ 内容提取  │    │ 语义分块  │    │ 向量化    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └─────┬────┘
                                                                        │
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────▼────┐
│ Agent    │◀───│ RAG      │◀───│ Similarity│◀───│ ChromaDB │◀───│ Upsert   │
│ 自然语言  │    │ 检索接口  │    │ 计算      │    │ 向量存储  │    │ 增量写入  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### 3.3 安全沙箱模型

```
┌────────────────────────────────────────────────────────┐
│               PermissionController                     │
│                                                        │
│  请求路径: D:\Documents\合同\2024年采购合同.pdf         │
│       │                                                │
│       ▼                                                │
│  ┌──────────────────┐     ┌──────────────────┐        │
│  │ 1. 白名单检查     │────▶│ 2. 完整性检查     │        │
│  │ allowed_paths     │     │ Integrity Level   │        │
│  │ ✓ D:\Documents    │     │ Medium (默认)     │        │
│  │ ✗ C:\Windows      │     │                   │        │
│  └──────────────────┘     └──────────────────┘        │
│                                        │                │
│                                        ▼                │
│                                 ┌──────────────────┐   │
│                                 │ 3. 审计记录       │   │
│                                 │ AuditTrail       │   │
│                                 │ {                │   │
│                                 │  "op": "read",   │   │
│                                 │  "path": "...",  │   │
│                                 │  "risk": "low",  │   │
│                                 │  "ts": "..."     │   │
│                                 │ }                │   │
│                                 └──────────────────┘   │
└────────────────────────────────────────────────────────┘
```

---

## 4. 核心模块设计

### 4.1 FileWatcher — 文件变更监听

**职责**：实时检测文件系统的 create / modify / delete / move 事件。

**技术选型**：`watchdog` 库 → `FileSystemEventHandler`

**设计要点**：
- **事件去重**：短时间内同一文件的多次 modify 合并为单次事件（500ms 窗口）
- **防抖动**：`debounce_sec=0.5` 避免大文件写入时触发多次索引
- **目录过滤**：自动跳过 `.git`、`node_modules`、`__pycache__` 等开发目录
- **优先级队列**：move/delete 优先处理，create/modify 按 FIFO

**事件类型映射**：

| 系统事件 | FileWatcher 响应 | 索引操作 |
|----------|-----------------|----------|
| `on_created` | NEW_FILE | 全量解析 → 分块 → 嵌入 → Upsert |
| `on_modified` | MODIFIED | 删除旧 chunks → 重新解析 → Upsert |
| `on_deleted` | DELETED | 按 file_id 删除 ChromaDB 中所有 chunks |
| `on_moved` | RENAMED | 更新路径映射 + 重新解析（若内容变化） |

**配置参数**：

```python
FILEWATCHER_CONFIG = {
    "watch_paths": [
        "D:\\Documents",
        "E:\\龙虾AI主控中心",
        "C:\\Users\\Administrator\\Desktop",
    ],
    "exclude_patterns": [
        "*.tmp", "*.lock", "~$*",
        ".git", "__pycache__", "node_modules",
        "Thumbs.db",
    ],
    "debounce_sec": 0.5,
    "max_event_queue_size": 1000,
    "enable_recursive": True,
}
```

---

### 4.2 ParserPool — 多格式解析器池

**职责**：根据文件类型分发到对应解析器，提取结构化文本内容。

**解析器注册表**：

| 文件类型 | 扩展名 | 解析器 | 技术栈 |
|----------|--------|--------|--------|
| 纯文本 | .txt .md .py .json .yaml .toml .csv .log | `TextParser` | 原生 open() + charset 检测 |
| Word 文档 | .docx .doc | `DocxParser` | python-docx / (保留 complex read_file) |
| PDF | .pdf | `PDFParser` | PyPDF2 / pdfplumber |
| Excel | .xlsx .xls .xlsm .csv | `ExcelParser` | openpyxl / pandas |
| PPT | .pptx .ppt | `PPTParser` | python-pptx |
| 图片(OCR) | .jpg .png .bmp | `OCRWrapper` | pytesseract (可选) |
| 代码 | .py .js .ts .java .cpp .go .rs | `CodeParser` | AST-aware 分块 |

**解析器接口**：

```python
class BaseParser(ABC):
    @abstractmethod
    def can_handle(self, file_path: str) -> bool: ...
    
    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument: ...
    
    @abstractmethod
    def get_metadata(self, file_path: str) -> FileMetadata: ...

@dataclass
class ParsedDocument:
    file_path: str
    file_type: str
    raw_text: str           # 完整提取文本
    metadata: FileMetadata   # 大小/时间/页数等
    parse_time_ms: float
    error: Optional[str]

@dataclass
class FileMetadata:
    file_size: int
    modify_time: float
    create_time: float
    page_count: Optional[int]
    author: Optional[str]
```

**解析器选择逻辑**：

```
文件路径 → can_handle() 遍历 ParserPool 所有解析器
         → 第一个返回 True 的解析器
         → 若无匹配 → fallback 到 TextParser (尝试 UTF-8/Latin-1/GBK)
```

---

### 4.3 SemanticIndexer — 语义索引引擎

**职责**：将文件文本分块、嵌入向量化、存储到 ChromaDB。

**分块策略**：

```python
CHUNK_CONFIG = {
    "chunk_size": 512,          # 每块最大字符数（中文友好）
    "chunk_overlap": 64,        # 块间重叠字符数（保持语义连贯）
    "separators": [
        "\n\n", "\n", "。", ".",  # 优先按段落/句子边界切分
        " ", ""
    ],
    "keep_separator": True,     # 保留分隔符
}

# 特殊处理
CODE_CHUNK_CONFIG = {
    "chunk_size": 1024,         # 代码块更大
    "chunk_overlap": 128,
    "separators": ["\n\n", "\n", "    "],
}
```

**嵌入模型选型矩阵**：

| 模型 | 维度 | 本地/API | 中文质量 | 速度 | 推荐场景 |
|------|------|----------|---------|------|----------|
| text-embedding-3-small | 1536 | API | ⭐⭐⭐⭐ | 快 | 通用、可联网 |
| bge-large-zh-v1.5 | 1024 | 本地 | ⭐⭐⭐⭐⭐ | 中 | 纯中文、离线 |
| all-MiniLM-L6-v2 | 384 | 本地 | ⭐⭐ | 极快 | 英文为主 |
| **bge-small-zh-v1.5** | **512** | **本地** | **⭐⭐⭐⭐** | **快** | **推荐默认** |

**ChromaDB 存储 Schema**：

```python
COLLECTION_NAME = "filesense_docs_v4"

# 每个 chunk 的元数据
CHUNK_METADATA = {
    "file_path": "D:\\Documents\\合同\\2024年采购合同.pdf",
    "file_type": "pdf",
    "chunk_index": 3,           # 该文件第几个 chunk
    "total_chunks": 12,         # 文件总 chunk 数
    "char_start": 1024,         # 原始文本起始位置
    "char_end": 1536,           # 原始文本结束位置
    "modify_time": 1717200000,  # Unix 时间戳
    "source_section": "第三条 付款条款",  # 章节标识
}

# 向量索引
CHROMA_CONFIG = {
    "persist_directory": "./chroma_db/filesense",
    "collection_metadata": {
        "hnsw:space": "cosine",         # 余弦相似度
        "hnsw:construction_ef": 200,    # 构建时搜索宽度
        "hnsw:search_ef": 100,          # 查询时搜索宽度
        "hnsw:M": 16,                   # 每层最大连接数
    }
}
```

**增量索引流程**：

```
1. NEW_FILE 事件到达
2. ParserPool.parse() → ParsedDocument.raw_text
3. ChunkEngine.split(raw_text) → List[Chunk]
4. Embedder.embed_batch(chunks) → List[ndarray]
5. ChromaDB.delete(where={"file_path": file_path})  # 清理旧数据
6. ChromaDB.add(embeddings, metadatas, documents)    # 写入新数据
7. AuditTrail.log("index", file_path, chunk_count)
```

---

### 4.4 RAGRetriever — Agent 检索接口

**职责**：对外暴露自然语言检索接口，供 MissionControl / 用户直接调用。

**检索模式**：

| 模式 | 接口 | 说明 |
|------|------|------|
| 语义检索 | `semantic_search(query, top_k=10)` | 向量相似度检索 |
| 元数据过滤 | `filtered_search(query, file_type, date_range)` | 语义 + 元数据筛 |
| 混合检索 | `hybrid_search(query, keywords, top_k=10)` | 语义 + 关键词 RRF 融合 |
| 文件全文 | `get_full_text(file_path)` | 返回完整文件内容（需权限检查） |

**检索接口签名**：

```python
@dataclass
class SearchResult:
    chunk_id: str
    file_path: str
    content: str            # chunk 文本内容
    score: float            # 相似度分数 (0-1)
    metadata: dict          # file_type, modify_time, page_num 等
    context_before: str     # 前一个 chunk（可选）
    context_after: str      # 后一个 chunk（可选）

class RAGRetriever:
    def semantic_search(
        self, query: str, top_k: int = 10,
        file_types: Optional[List[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> List[SearchResult]: ...

    def hybrid_search(
        self, query: str, keywords: List[str],
        top_k: int = 10, rrf_k: int = 60,
    ) -> List[SearchResult]: ...

    def get_file_summary(
        self, file_path: str
    ) -> FileSummary: ...
```

**RRF (Reciprocal Rank Fusion) 混合检索算法**：

```python
def rrf_fusion(
    semantic_results: List[Tuple[str, float]],
    keyword_results: List[Tuple[str, float]],
    k: int = 60
) -> List[str]:
    """融合语义检索和关键词检索结果"""
    scores = {}
    for rank, (chunk_id, _) in enumerate(semantic_results):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1.0 / (k + rank + 1)
    for rank, (chunk_id, _) in enumerate(keyword_results):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
```

---

### 4.5 PermissionController — 沙箱权限白名单

**职责**：所有文件访问必须经过权限检查，确保沙箱安全。

**白名单模型**：

```python
PERMISSION_WHITELIST = {
    # 读写权限路径
    "read_write": [
        "D:\\Documents",
        "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent",
        "C:\\Users\\Administrator\\Desktop",
        "C:\\Users\\Administrator\\Downloads",
    ],
    # 只读权限路径
    "read_only": [
        "C:\\Users\\Administrator\\AppData\\Roaming",
        "D:\\Data",
    ],
    # 明确禁止的路径（最高优先级）
    "denied": [
        "C:\\Windows",
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "C:\\ProgramData",
        "C:\\Users\\Default",
        "C:\\$Recycle.Bin",
    ],
}

# 敏感文件扩展名保护
SENSITIVE_EXTENSIONS = [
    ".key", ".pem", ".pfx", ".p12",  # 密钥
    ".env", ".secret", ".credentials",  # 凭据
    ".kube", ".aws", ".ssh",  # 云配置
]
```

**权限检查流程**：

```python
class PermissionController:
    def check_access(self, file_path: str, operation: str) -> PermissionResult:
        """
        权限检查四级流程:
        1. DENIED 检查 → 绝对禁止，直接拒绝
        2. SENSITIVE 检查 → 敏感文件，需用户确认
        3. WHITELIST 检查 → 白名单内，放行
        4. DEFAULT → 只读，禁止写入
        """
        
    def get_allowed_paths(self) -> List[str]: ...
    
    def get_audit_log(self, hours: int = 24) -> List[AuditEntry]: ...
```

---

### 4.6 AuditTrail — 操作审计追踪

**职责**：记录所有文件访问操作的结构化日志。

**日志格式**：

```json
{
    "timestamp": "2026-05-31T12:00:00.000Z",
    "operation": "read",
    "file_path": "D:\\Documents\\合同.pdf",
    "file_size": 204800,
    "file_type": "pdf",
    "requester": "mission_control",
    "risk_level": "low",
    "result": "allowed",
    "duration_ms": 42,
    "chunks_indexed": 12,
    "session_id": "conv_19e7dbf3706"
}
```

**审计查询接口**：

```python
class AuditTrail:
    def log_operation(self, entry: AuditEntry): ...
    def query(self, file_path: str = None, operation: str = None,
              hours: int = 24) -> List[AuditEntry]: ...
    def get_risk_summary(self, hours: int = 24) -> RiskSummary: ...
    def export(self, format: str = "json") -> str: ...
```

---

## 5. Python 实现代码

### 5.1 核心类：AutoFileScanner

```python
"""
AutoFileScanner v4.0 — FileSense
智能文件感知系统 · 主入口

R18 迭代: §4.1 文件读取能力路线
P0 任务: 1.1 watchdog 监听 + 1.2 ChromaDB 语义索引
P1 任务: 权限白名单 + 沙箱隔离

依赖:
  pip install watchdog chromadb sentence-transformers langchain-text-splitters
"""

import os
import time
import json
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict

# ============================================================
# 1. 数据结构定义
# ============================================================

class FileEventType(Enum):
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FileMetadata:
    file_path: str
    file_type: str
    file_size: int
    modify_time: float
    create_time: float
    checksum: str = ""
    page_count: Optional[int] = None
    author: Optional[str] = None

@dataclass
class ParsedDocument:
    file_path: str
    file_type: str
    raw_text: str
    metadata: FileMetadata
    parse_time_ms: float = 0.0
    error: Optional[str] = None

@dataclass
class SearchResult:
    chunk_id: str
    file_path: str
    content: str
    score: float
    metadata: Dict = field(default_factory=dict)
    context_before: str = ""
    context_after: str = ""

@dataclass
class AuditEntry:
    timestamp: str
    operation: str
    file_path: str
    file_size: int
    file_type: str
    requester: str
    risk_level: str
    result: str
    duration_ms: float = 0.0
    chunks_indexed: int = 0
    session_id: str = ""

@dataclass
class PermissionResult:
    allowed: bool
    reason: str
    risk_level: RiskLevel = RiskLevel.LOW
    requires_confirmation: bool = False

# ============================================================
# 2. PermissionController — 权限白名单
# ============================================================

class PermissionController:
    """沙箱权限白名单控制器
    
    四级检查: DENIED → SENSITIVE → WHITELIST → DEFAULT
    与 SafeGuard v5.0 联动的安全边界
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.denied_paths: Set[str] = {
            "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
            "C:\\ProgramData", "C:\\Users\\Default", "C:\\$Recycle.Bin",
        }
        self.read_write_paths: Set[str] = set()
        self.read_only_paths: Set[str] = set()
        self.sensitive_extensions: Set[str] = {
            ".key", ".pem", ".pfx", ".p12",
            ".env", ".secret", ".credentials",
            ".kube", ".aws", ".ssh",
        }
        self._load_config()
    
    def _load_config(self):
        if self.config.get("read_write"):
            self.read_write_paths = set(self.config["read_write"])
        if self.config.get("read_only"):
            self.read_only_paths = set(self.config["read_only"])
        if self.config.get("denied"):
            self.denied_paths.update(self.config["denied"])
    
    def check_access(
        self, file_path: str, operation: str = "read"
    ) -> PermissionResult:
        """四级权限检查"""
        normalized = os.path.abspath(file_path)
        
        # Level 1: DENIED — 系统核心路径
        for denied in self.denied_paths:
            if normalized.lower().startswith(denied.lower()):
                return PermissionResult(
                    allowed=False,
                    reason=f"禁止访问系统目录: {denied}",
                    risk_level=RiskLevel.CRITICAL,
                )
        
        # Level 2: SENSITIVE — 敏感文件扩展名
        ext = os.path.splitext(normalized)[1].lower()
        if ext in self.sensitive_extensions:
            return PermissionResult(
                allowed=True,
                reason=f"敏感文件 {ext}，需用户确认",
                risk_level=RiskLevel.HIGH,
                requires_confirmation=True,
            )
        
        # Level 3: WHITELIST — 白名单路径
        for rw_path in self.read_write_paths:
            if normalized.lower().startswith(rw_path.lower()):
                return PermissionResult(allowed=True, reason=f"白名单路径: {rw_path}")
        
        for ro_path in self.read_only_paths:
            if normalized.lower().startswith(ro_path.lower()):
                if operation in ("write", "delete", "move"):
                    return PermissionResult(
                        allowed=False, reason=f"路径只读: {ro_path}"
                    )
                return PermissionResult(allowed=True, reason=f"只读路径: {ro_path}")
        
        # Level 4: DEFAULT — 未知路径 → 只读
        if operation in ("write", "delete", "move"):
            return PermissionResult(
                allowed=False,
                reason=f"未授权路径，禁止写入: {normalized}",
                risk_level=RiskLevel.MEDIUM,
            )
        return PermissionResult(allowed=True, reason="默认只读")


# ============================================================
# 3. FileWatcher — watchdog 文件监听
# ============================================================

class DebouncedFileEventHandler:
    """带防抖动的文件事件处理器
    
    P0 任务 1.1: 增量监听替代静态流水线
    防抖窗口 500ms，合并重复事件
    """
    
    def __init__(self, callback, debounce_sec: float = 0.5):
        self.callback = callback
        self.debounce_sec = debounce_sec
        self._pending: Dict[str, FileEventType] = {}
        self._timer = None
        self._exclude_patterns: List[str] = [
            "*.tmp", "*.lock", "~$*", "Thumbs.db"
        ]
    
    def _should_exclude(self, path: str) -> bool:
        """检查是否应排除该文件"""
        import fnmatch
        fname = os.path.basename(path)
        for pattern in self._exclude_patterns:
            if fnmatch.fnmatch(fname, pattern):
                return True
        
        # 排除开发目录
        exclude_dirs = {".git", "__pycache__", "node_modules", ".idea", ".vscode"}
        path_parts = Path(path).parts
        return bool(exclude_dirs.intersection(path_parts))
    
    def on_any_event(self, event):
        if event.is_directory:
            return
        if self._should_exclude(event.src_path):
            return
        
        et = None
        if event.event_type == "created":
            et = FileEventType.CREATED
        elif event.event_type == "modified":
            et = FileEventType.MODIFIED
        elif event.event_type == "deleted":
            et = FileEventType.DELETED
        elif event.event_type == "moved":
            et = FileEventType.MOVED
        
        if et:
            self._pending[event.src_path] = et
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self.debounce_sec, self._flush)
            self._timer.start()
    
    def _flush(self):
        for path, event_type in self._pending.items():
            try:
                self.callback(path, event_type)
            except Exception as e:
                logging.error(f"处理文件事件失败: {path} -> {e}")
        self._pending.clear()


# ============================================================
# 4. ParserPool — 多格式解析器池
# ============================================================

class BaseParser(ABC):
    """解析器基类"""
    
    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """判断是否能处理该文件"""
        ...
    
    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument:
        """解析文件并返回结构化文档"""
        ...
    
    def get_metadata(self, file_path: str) -> FileMetadata:
        """提取文件元数据"""
        stat = os.stat(file_path)
        ext = os.path.splitext(file_path)[1].lower().lstrip(".")
        return FileMetadata(
            file_path=file_path,
            file_type=ext,
            file_size=stat.st_size,
            modify_time=stat.st_mtime,
            create_time=stat.st_ctime,
            checksum=self._compute_md5(file_path),
        )
    
    def _compute_md5(self, file_path: str, chunk_size: int = 8192) -> str:
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                md5.update(chunk)
        return md5.hexdigest()


class TextParser(BaseParser):
    """纯文本解析器 — 支持 charset 自动检测"""
    
    TEXT_EXTENSIONS = {
        ".txt", ".md", ".py", ".js", ".ts", ".json", ".yaml", ".yml",
        ".toml", ".ini", ".cfg", ".csv", ".log", ".html", ".xml",
        ".css", ".sh", ".ps1", ".bat", ".sql", ".r", ".java",
        ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php",
    }
    
    def can_handle(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.TEXT_EXTENSIONS
    
    def parse(self, file_path: str) -> ParsedDocument:
        metadata = self.get_metadata(file_path)
        start = time.time()
        try:
            # 尝试 UTF-8 → GBK → Latin-1
            raw_text = None
            for encoding in ["utf-8", "gbk", "gb2312", "latin-1"]:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        raw_text = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if raw_text is None:
                raise ValueError(f"无法解码文件: {file_path}")
            
            return ParsedDocument(
                file_path=file_path,
                file_type=metadata.file_type,
                raw_text=raw_text,
                metadata=metadata,
                parse_time_ms=(time.time() - start) * 1000,
            )
        except Exception as e:
            return ParsedDocument(
                file_path=file_path,
                file_type=metadata.file_type,
                raw_text="",
                metadata=metadata,
                error=str(e),
            )


class ParserPool:
    """解析器池 — 自动路由"""
    
    def __init__(self):
        self.parsers: List[BaseParser] = [TextParser()]
        self._fallback = TextParser()
    
    def register(self, parser: BaseParser):
        self.parsers.insert(0, parser)  # 新注册的优先
    
    def parse(self, file_path: str) -> ParsedDocument:
        for parser in self.parsers:
            if parser.can_handle(file_path):
                return parser.parse(file_path)
        return self._fallback.parse(file_path)
    
    def can_handle(self, file_path: str) -> bool:
        return any(p.can_handle(file_path) for p in self.parsers)


# ============================================================
# 5. SemanticIndexer — 语义索引引擎
# ============================================================

class SemanticIndexer:
    """语义分块 + 向量嵌入 + ChromaDB 存储
    
    P0 任务 1.2: ChromaDB 语义索引 + RAG 检索
    """
    
    def __init__(
        self,
        persist_dir: str = "./chroma_db/filesense",
        chunk_size: int = 512,
        chunk_overlap: int = 64,
        embed_model: str = "bge-small-zh-v1.5",
    ):
        self.persist_dir = persist_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embed_model = embed_model
        
        # 延迟初始化
        self._collection = None
        self._embedder = None
        self._splitter = None
    
    def _init_splitter(self):
        """初始化分块器"""
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except ImportError:
            raise ImportError(
                "需要安装 langchain-text-splitters: "
                "pip install langchain-text-splitters"
            )
        
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", "。", ".", " ", ""],
            keep_separator=True,
        )
    
    def _init_embedder(self):
        """初始化嵌入模型"""
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "需要安装 sentence-transformers: "
                "pip install sentence-transformers"
            )
        
        self._embedder = SentenceTransformer(self.embed_model)
    
    def _init_collection(self):
        """初始化 ChromaDB 集合"""
        try:
            import chromadb
        except ImportError:
            raise ImportError("需要安装 chromadb: pip install chromadb")
        
        self._chroma_client = chromadb.PersistentClient(path=self.persist_dir)
        self._collection = self._chroma_client.get_or_create_collection(
            name="filesense_docs_v4",
            metadata={"hnsw:space": "cosine"}
        )
    
    def ensure_init(self):
        if self._splitter is None:
            self._init_splitter()
        if self._embedder is None:
            self._init_embedder()
        if self._collection is None:
            self._init_collection()
    
    def index_file(self, doc: ParsedDocument):
        """索引单个文件: 分块 → 嵌入 → Upsert"""
        self.ensure_init()
        
        if doc.error:
            logging.warning(f"跳过解析失败的文件: {doc.file_path} -> {doc.error}")
            return
        
        # 1. 清理旧索引
        try:
            self._collection.delete(
                where={"file_path": doc.file_path}
            )
        except Exception:
            pass
        
        # 2. 分块
        chunks = self._splitter.split_text(doc.raw_text)
        if not chunks:
            return
        
        # 3. 嵌入
        embeddings = self._embedder.encode(
            chunks, show_progress_bar=False
        ).tolist()
        
        # 4. 构建元数据
        metadatas = []
        ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc.metadata.checksum}_chunk_{i}"
            ids.append(chunk_id)
            metadatas.append({
                "file_path": doc.file_path,
                "file_type": doc.file_type,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "modify_time": doc.metadata.modify_time,
            })
        
        # 5. Upsert
        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        
        logging.info(
            f"索引完成: {doc.file_path} -> {len(chunks)} chunks, "
            f"耗时 {doc.parse_time_ms:.0f}ms"
        )
    
    def semantic_search(
        self,
        query: str,
        top_k: int = 10,
        file_types: Optional[List[str]] = None,
        date_from: Optional[float] = None,
    ) -> List[SearchResult]:
        """语义检索"""
        self.ensure_init()
        
        # 构建 where 条件
        where = {}
        if file_types:
            where["file_type"] = {"$in": file_types}
        
        query_embedding = self._embedder.encode([query]).tolist()[0]
        
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where if where else None,
            include=["documents", "metadatas", "distances"],
        )
        
        search_results = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            
            # 时间过滤
            if date_from and meta.get("modify_time", 0) < date_from:
                continue
            
            # 距离转相似度分数 (cosine distance → similarity)
            distance = results["distances"][0][i]
            score = 1.0 - min(distance / 2.0, 1.0)
            
            search_results.append(SearchResult(
                chunk_id=results["ids"][0][i],
                file_path=meta.get("file_path", ""),
                content=results["documents"][0][i],
                score=round(score, 4),
                metadata=meta,
            ))
        
        search_results.sort(key=lambda x: x.score, reverse=True)
        return search_results[:top_k]
    
    def hybrid_search(
        self, query: str, keywords: List[str],
        top_k: int = 10, rrf_k: int = 60,
    ) -> List[SearchResult]:
        """混合检索: 语义 + 关键词 RRF 融合"""
        # 语义检索
        semantic_results = self.semantic_search(query, top_k=top_k * 2)
        
        # 关键词匹配 (基于 ChromaDB metadata 过滤 + 文本匹配)
        keyword_results = self._keyword_search(keywords, top_k=top_k * 2)
        
        # RRF 融合
        fused = self._rrf_fusion(semantic_results, keyword_results, rrf_k)
        return fused[:top_k]
    
    def _keyword_search(
        self, keywords: List[str], top_k: int = 20
    ) -> List[SearchResult]:
        """关键词匹配检索"""
        self.ensure_init()
        
        all_results = []
        for kw in keywords:
            try:
                raw = self._collection.get(
                    where_document={"$contains": kw},
                    limit=top_k,
                    include=["documents", "metadatas"],
                )
                for i in range(len(raw.get("ids", []))):
                    all_results.append(SearchResult(
                        chunk_id=raw["ids"][i],
                        file_path=raw["metadatas"][i].get("file_path", ""),
                        content=raw["documents"][i],
                        score=0.8,  # 关键词匹配默认高分
                        metadata=raw["metadatas"][i],
                    ))
            except Exception:
                pass
        return all_results
    
    def _rrf_fusion(
        self, semantic: List[SearchResult],
        keyword: List[SearchResult], k: int = 60
    ) -> List[SearchResult]:
        """Reciprocal Rank Fusion"""
        scores: Dict[str, float] = {}
        result_map: Dict[str, SearchResult] = {}
        
        for rank, r in enumerate(semantic):
            scores[r.chunk_id] = scores.get(r.chunk_id, 0) + 1.0 / (k + rank + 1)
            result_map[r.chunk_id] = r
        
        for rank, r in enumerate(keyword):
            scores[r.chunk_id] = scores.get(r.chunk_id, 0) + 1.0 / (k + rank + 1)
            if r.chunk_id not in result_map:
                result_map[r.chunk_id] = r
        
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return [result_map[cid] for cid in sorted_ids if cid in result_map]


# ============================================================
# 6. AuditTrail — 审计追踪
# ============================================================

class AuditTrail:
    """操作审计日志"""
    
    def __init__(self, log_dir: str = "./audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._buffer: List[AuditEntry] = []
        self._buffer_size = 50
    
    def log_operation(self, entry: AuditEntry):
        """记录一次文件操作"""
        self._buffer.append(entry)
        if len(self._buffer) >= self._buffer_size:
            self._flush()
    
    def _flush(self):
        """批量写入磁盘"""
        if not self._buffer:
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"audit_{today}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            for entry in self._buffer:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        
        self._buffer.clear()
    
    def query(
        self, file_path: str = None, operation: str = None,
        hours: int = 24,
    ) -> List[AuditEntry]:
        """查询审计日志"""
        self._flush()
        cutoff = datetime.now() - timedelta(hours=hours)
        results = []
        
        for log_file in self.log_dir.glob("audit_*.jsonl"):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        ts = datetime.fromisoformat(
                            entry["timestamp"].replace("Z", "+00:00")
                        )
                        if ts.replace(tzinfo=None) < cutoff:
                            continue
                        if file_path and file_path not in entry.get("file_path", ""):
                            continue
                        if operation and operation != entry.get("operation"):
                            continue
                        results.append(entry)
                    except Exception:
                        pass
        
        return results


# ============================================================
# 7. 主控类 — AutoFileScanner v4.0
# ============================================================

class AutoFileScanner:
    """AutoFileScanner v4.0 — FileSense 主控
    
    整合 FileWatcher + ParserPool + SemanticIndexer +
    RAGRetriever + PermissionController + AuditTrail
    """
    
    def __init__(
        self,
        watch_paths: Optional[List[str]] = None,
        persist_dir: str = "./chroma_db/filesense",
        enable_watchdog: bool = True,
    ):
        # 核心组件
        self.permission = PermissionController()
        self.parser_pool = ParserPool()
        self.indexer = SemanticIndexer(persist_dir=persist_dir)
        self.audit = AuditTrail()
        
        # 配置
        self.watch_paths = watch_paths or ["C:\\Users\\Administrator\\Desktop"]
        self.enable_watchdog = enable_watchdog
        self._observer = None
        self._scan_stats = {"total": 0, "indexed": 0, "skipped": 0, "errors": 0}
        
        # 会话 ID
        self.session_id = datetime.now().strftime("session_%Y%m%d_%H%M%S")
    
    def start(self):
        """启动 FileSense"""
        logging.info("AutoFileScanner v4.0 FileSense 启动中...")
        
        # 初始化索引器
        self.indexer.ensure_init()
        
        # 启动 watchdog
        if self.enable_watchdog:
            self._start_watchdog()
        
        logging.info("FileSense 启动完成")
    
    def _start_watchdog(self):
        """启动文件监听"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
        except ImportError:
            logging.warning("watchdog 未安装，跳过实时监听。pip install watchdog")
            return
        
        import threading
        
        handler = DebouncedFileEventHandler(
            callback=self._on_file_event,
            debounce_sec=0.5,
        )
        
        # 包装为 watchdog 兼容的 handler
        class _Handler(FileSystemEventHandler):
            def on_created(self, event):
                handler.on_any_event(event)
            def on_modified(self, event):
                handler.on_any_event(event)
            def on_deleted(self, event):
                handler.on_any_event(event)
            def on_moved(self, event):
                handler.on_any_event(event)
        
        self._observer = Observer()
        for path in self.watch_paths:
            if os.path.isdir(path):
                self._observer.schedule(
                    _Handler(), path, recursive=True
                )
                logging.info(f"watchdog 监听: {path}")
        
        self._observer.start()
    
    def _on_file_event(self, file_path: str, event_type: FileEventType):
        """文件事件回调"""
        # 权限检查
        perm = self.permission.check_access(file_path)
        if not perm.allowed:
            logging.warning(f"权限拒绝: {file_path} -> {perm.reason}")
            return
        
        start = time.time()
        
        if event_type == FileEventType.DELETED:
            # 从索引中移除
            try:
                self.indexer._collection.delete(
                    where={"file_path": file_path}
                )
            except Exception:
                pass
            self.audit.log_operation(AuditEntry(
                timestamp=datetime.now().isoformat(),
                operation="delete_index",
                file_path=file_path,
                file_size=0,
                file_type="",
                requester="watchdog",
                risk_level="low",
                result="success",
            ))
            return
        
        # CREATE / MODIFY / MOVED → 重新索引
        try:
            doc = self.parser_pool.parse(file_path)
            if not doc.error:
                self.indexer.index_file(doc)
                self._scan_stats["indexed"] += 1
            else:
                self._scan_stats["errors"] += 1
        except Exception as e:
            self._scan_stats["errors"] += 1
            logging.error(f"索引失败: {file_path} -> {e}")
        
        duration = (time.time() - start) * 1000
        self.audit.log_operation(AuditEntry(
            timestamp=datetime.now().isoformat(),
            operation=f"index_{event_type.value}",
            file_path=file_path,
            file_size=os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            file_type=os.path.splitext(file_path)[1].lower().lstrip("."),
            requester="watchdog",
            risk_level="low",
            result="success",
            duration_ms=duration,
            session_id=self.session_id,
        ))
    
    # ── 检索接口 ──────────────────────────────
    
    def search(
        self, query: str, top_k: int = 10,
        file_types: Optional[List[str]] = None,
    ) -> List[SearchResult]:
        """自然语言搜索文件内容"""
        return self.indexer.semantic_search(query, top_k, file_types)
    
    def hybrid_search(
        self, query: str, keywords: List[str], top_k: int = 10,
    ) -> List[SearchResult]:
        """混合检索"""
        return self.indexer.hybrid_search(query, keywords, top_k)
    
    def get_stats(self) -> Dict:
        return {
            **self._scan_stats,
            "chroma_dir": self.indexer.persist_dir,
            "watch_paths": self.watch_paths,
            "watchdog_active": self._observer is not None and self._observer.is_alive(),
        }
    
    def stop(self):
        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=5)
        self.audit._flush()
        logging.info("FileSense 已停止")


# ============================================================
# 8. 命令行入口
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    
    scanner = AutoFileScanner(
        watch_paths=[
            "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent",
            "C:\\Users\\Administrator\\Desktop",
        ],
        persist_dir="./chroma_db/filesense",
    )
    
    scanner.start()
    
    # 示例: 语义检索
    results = scanner.search("最近修改的合同文件", top_k=5)
    for r in results:
        print(f"[{r.score:.3f}] {r.file_path}")
        print(f"  {r.content[:100]}...")
        print()
    
    scanner.stop()
```

### 5.2 部署配置

```python
# file_sense_config.py — 部署配置

FILE_SENSE_CONFIG = {
    # watchdog 监听路径
    "watch_paths": [
        "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent",
        "D:\\Documents",
        "C:\\Users\\Administrator\\Desktop",
        "C:\\Users\\Administrator\\Downloads",
    ],
    # watchdog 排除
    "watch_exclude": [
        ".git", "__pycache__", "node_modules", ".idea",
        "*.tmp", "*.lock", "~$*", "Thumbs.db",
        "*.pyc", "__pycache__",
    ],
    # 分块配置
    "chunk": {
        "size": 512,
        "overlap": 64,
        "code_size": 1024,
        "code_overlap": 128,
    },
    # ChromaDB 配置
    "chroma": {
        "persist_dir": "./data/chroma_db/filesense",
        "collection": "filesense_docs_v4",
        "hnsw_space": "cosine",
    },
    # 嵌入模型
    "embed_model": "bge-small-zh-v1.5",
    # 权限白名单
    "permissions": {
        "read_write": [
            "E:\\龙虾AI主控中心",
            "D:\\Documents",
            "C:\\Users\\Administrator\\Desktop",
            "C:\\Users\\Administrator\\Downloads",
        ],
        "read_only": [
            "D:\\Data",
            "C:\\Users\\Administrator\\AppData\\Roaming",
        ],
    },
    # 审计日志
    "audit": {
        "log_dir": "./data/audit_logs/filesense",
        "buffer_size": 50,
        "retention_days": 30,
    },
}
```

---

## 6. 部署指南

### 6.1 环境准备

```powershell
# PowerShell — 依赖安装
pip install watchdog chromadb sentence-transformers langchain-text-splitters

# 可选: OCR 支持
pip install pytesseract pillow

# 可选: PDF 解析增强
pip install pypdf2 pdfplumber python-docx openpyxl
```

### 6.2 首次启动

```python
from auto_file_scanner_v4 import AutoFileScanner

scanner = AutoFileScanner(
    watch_paths=[
        "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent",
        "D:\\Documents",
    ],
    persist_dir="./data/chroma_db/filesense",
)

# 启动实时监听
scanner.start()

# 语义搜索
results = scanner.search("采购合同", top_k=5)
```

### 6.3 与 SafeGuard v5.0 联动

```python
# SafeGuard 集成示例
from safe_guard_v5 import SafeGuard

safe = SafeGuard()

# 文件操作前沙箱验证
def safe_file_read(file_path: str) -> str:
    # 1. 权限检查
    perm = scanner.permission.check_access(file_path)
    if not perm.allowed:
        raise PermissionError(perm.reason)
    
    # 2. SafeGuard 检查点
    checkpoint = safe.create_checkpoint("file_read")
    
    try:
        return open(file_path, "r", encoding="utf-8").read()
    except Exception:
        safe.rollback(checkpoint)
        raise
```

### 6.4 与 MemoryOS v4.0 联动

```python
# 索引内容同步到 MemoryOS 知识图谱
from memory_os_v4 import MemoryOS

memory = MemoryOS()

for result in scanner.search("合同条款", top_k=20):
    # 萃取实体 → 写入知识图谱
    memory.extract_and_store(
        source=result.file_path,
        content=result.content,
        entity_types=["合同", "条款", "日期", "金额"],
    )
```

---

## 7. R18 报告对应关系

| R18 报告章节 | 对应内容 | 本文档位置 |
|-------------|----------|-----------|
| §4.1 文件读取能力路线 | watchdog + 语义索引 + 沙箱 | §2 升级说明 |
| P0 任务 1.1 | watchdog 增量监听 | §5.1 FileWatcher |
| P0 任务 1.2 | ChromaDB 语义索引 + RAG | §5.1 SemanticIndexer |
| P1 权限白名单 | 沙箱化文件访问 | §5.1 PermissionController |
| §4.1 目标架构图 | 事件驱动 → 语义索引 | §3.1 整体架构 |
| §4.1 技术选型表 | watchdog + ChromaDB + bge | §4.3 嵌入模型选型 |
| §4.1 实施步骤 | 30min+30min+10min | §2.1 变更来源 |
| §6 R18 行动计划 | Phase 1 任务 1.1-1.2 | §6 部署指南 |

---

## 8. 性能基线

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 文件变更 → 索引延迟 | < 2s | watchdog 事件 + 分块 + 嵌入 |
| 语义检索延迟 | < 200ms | ChromaDB HNSW 索引 |
| 单文件索引吞吐 | ~50 文件/min | bge-small-zh 512维 |
| ChromaDB 存储膨胀 | ~3× | 向量比原始文本大 |
| 内存占用 (空闲) | ~200MB | bge 模型加载 |
| 内存占用 (活跃) | ~500MB | 含 ChromaDB 缓存 |
| 磁盘占用 (每1K文件) | ~50MB | 512维 × 分块数 |

---

> **文档版本**: AutoFileScanner_v4_FileSense.md v1.0  
> **创建时间**: 2026-05-31  
> **对应 R18 任务**: §4.1 P0#1.1 + P0#1.2 + P1 权限白名单  
> **下一版规划**: v5.0 — 引入多模态索引（图片 OCR + 音频转录）