# Layer7 知识联动层：Obsidian MCP 双相同步方案

> **对标**：Obsidian MCP (社区) + Claude Code filesystem MCP
> **目标**：豆包Agent通过MCP协议与Obsidian知识库实现双向实时同步
> **版本**：v1.0 Draft

---

## 一、技术栈

```
Obsidian Vault (E:\龙虾AI主控中心\Obsidian\)
        │
        │ MCP (Model Context Protocol)
        │
        ▼
filesystem MCP Server (@anthropic-ai/files-mcp)
        │
        ├─ 读取: 全文检索 + 结构化解析
        ├─ 写入: Markdown创建 + 元数据更新
        └─ 监听: 文件变更事件 → 触发同步
        │
        ▼
豆包Agent知识索引 (SQLite + 向量)
        │
        ├─ 向量嵌入 (AllenAI Specter2 / BGE-M3)
        ├─ 关联图谱 (NetworkX)
        └─ 缓存层 (LRU内存缓存)
```

## 二、MCP 连接器配置

### 2.1 基础安装

```bash
# 安装 filesystem MCP Server
npm install -g @anthropic-ai/files-mcp

# 或者使用 Python MCP SDK
pip install mcp

# 配置 MCP 连接
# 注册 Obsidian Vault 路径
```

### 2.2 MCP 配置

```json
{
  "mcp_servers": {
    "obsidian-vault": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/files-mcp",
        "E:/龙虾AI主控中心/Obsidian/"
      ],
      "description": "Obsidian知识库MCP连接器 - 龙虾AI主控中心",
      "env": {
        "MCP_FILESYSTEM_ROOT": "E:/龙虾AI主控中心/Obsidian/",
        "MCP_FILESYSTEM_ALLOWED_OPERATIONS": "read,write,list,search"
      }
    }
  },
  "sync_config": {
    "auto_sync": true,
    "sync_interval_hours": 6,
    "watch_patterns": [
      "*.md",
      "templates/**/*.md",
      "MOC/**/*.md",
      "Areas/**/*.md",
      "Projects/**/*.md",
      "Resources/**/*.md"
    ],
    "exclude_patterns": [
      ".obsidian/**",
      ".trash/**",
      "node_modules/**"
    ],
    "index_on_startup": true,
    "vector_model": "BAAI/bge-m3",
    "batch_size": 50,
    "max_file_size_mb": 10
  }
}
```

## 三、双向同步机制

### 3.1 下行同步（Obsidian → 豆包Agent）

```
Obsidian 文件变更
    │
    ▼
MCP Server 检测 (inotify/polling)
    │
    ├─ 新建文件 → 全量索引
    ├─ 修改文件 → 增量索引（diff-based）
    └─ 删除文件 → 标记删除
    │
    ▼
豆包知识索引更新
    │
    ├─ 向量嵌入更新（chunk-based, 512 tokens/chunk）
    ├─ 关联图谱更新（MOC links → NetworkX edges）
    └─ 缓存失效（touch 相关缓存键）
```

### 3.2 上行同步（豆包Agent → Obsidian）

```
豆包Agent产出
    │
    ├─ 迭代报告 → Projects/豆包Agent迭代/
    ├─ 架构设计 → Areas/AI Agent研发/
    ├─ 外部情报 → Resources/Agent生态/
    └─ 能力对标 → Areas/AI Agent研发/
    │
    ▼
MCP Server 写入
    │
    ├─ 创建 Markdown 文件
    ├─ 添加 YAML frontmatter（元数据）
    └─ 更新 MOC 导航索引
```

### 3.3 知识注入流程

```
豆包Agent任务执行
    │
    ▼
查询知识库 (语义搜索)
    │
    ├─ "当前任务需要架构设计参考吗？"
    │   → 搜索 Areas/AI Agent研发/ 下的架构文档
    │
    ├─ "当前任务需要历史迭代经验吗？"
    │   → 搜索 Projects/豆包Agent迭代/ 下相关报告
    │
    └─ "当前任务需要外部情报吗？"
        → 搜索 Resources/Agent生态/ 下相关分析
    │
    ▼
注入Agent上下文
    ├─ 相关笔记以 Markdown 片段注入
    ├─ MOC 导航作为能力地图参考
    └─ 模板作为 Agent 配置模板
```

## 四、PARA架构映射

| PARA目录 | Obsidian路径 | 豆包Agent用途 |
|----------|-------------|--------------|
| **P**rojects | `Projects/豆包Agent迭代/` | 迭代产物归档 + 进度追踪 |
| **A**reas | `Areas/AI Agent研发/` | 长期知识积累 + 架构沉淀 |
| **R**esources | `Resources/Agent生态/` | 外部情报库 + 竞争对手分析 |
| **A**rchives | `Archives/历史版本/` | 旧版文档保存 |
| **MOC** | `MOC/AI Agent 能力地图.md` | 全局导航 + 知识索引 |

## 五、MOC 导航索引结构

```markdown
# AI Agent 能力地图 (MOC)

## 一、豆包Agent核心能力
- [[豆包Agent架构总览]] - 整体架构
- [[豆包Agent迭代路线图]] - 版本演进
- [[豆包Agent能力矩阵]] - 对标分析

## 二、多Agent通信
- [[AONP协议分析]] - 五协议框架
- [[桥接协议v3.0设计]] - 豆包适配方案
- [[AWP劳动力市场]] - 任务经济

## 三、自进化体系
- [[GEPA算法分析]] - ICLR 2026
- [[SICA v2.0设计]] - 三层进化
- [[Reflexion反思范式]] - 运行时进化

## 四、执行与安全
- [[Durable Task持久化]] - 长周期任务
- [[Firecracker沙箱]] - 安全隔离

## 五、学习参考
- [[Hermes SWARM]] - 无限编排
- [[OpenClaw架构]] - 运行时规范
- [[Marvis分析]] - OS层Agent
```

## 六、知识检索实现

```python
# knowledge_retriever.py

import sqlite3
import json
import numpy as np
from pathlib import Path

class KnowledgeRetriever:
    """Obsidian知识库检索器"""
    
    def __init__(self, vault_path: str, index_db_path: str):
        self.vault_path = Path(vault_path)
        self.db = sqlite3.connect(index_db_path)
        self.db.row_factory = sqlite3.Row
    
    def semantic_search(self, query: str, top_k: int = 5, 
                        para_filter: str = None) -> list:
        """语义搜索知识库"""
        query_embedding = self.embed(query)
        
        # 向量相似度检索
        results = self.db.execute("""
            SELECT 
                d.file_path,
                d.title,
                d.para_category,
                d.moc_tags,
                v.embedding,
                1 - (v.embedding <=> ?) AS similarity
            FROM documents d
            JOIN vectors v ON d.id = v.document_id
            WHERE 1=1
            {}
            ORDER BY similarity DESC
            LIMIT ?
        """.format(
            "AND d.para_category = ?" if para_filter else ""
        ), 
            (query_embedding.tobytes(),) + 
            ((para_filter,) if para_filter else ()) +
            (top_k,)
        ).fetchall()
        
        return [dict(r) for r in results]
    
    def get_moc_nav(self) -> dict:
        """获取MOC导航结构"""
        moc_files = list(self.vault_path.glob("MOC/**/*.md"))
        nav = {}
        for moc in moc_files:
            content = moc.read_text(encoding="utf-8")
            # 解析 [[wikilink]] 构建导航
            nav[moc.stem] = self.parse_wikilinks(content)
        return nav
    
    def inject_to_context(self, task_description: str, 
                          max_tokens: int = 4000) -> str:
        """将相关知识注入Agent上下文"""
        # 1. 语义搜索相关笔记
        results = self.semantic_search(task_description, top_k=5)
        
        # 2. 获取MOC导航
        moc = self.get_moc_nav()
        
        # 3. 组装上下文
        context = "## 知识库相关上下文\n\n"
        
        context += "### 相关笔记\n"
        for r in results:
            note_path = self.vault_path / r["file_path"]
            content = note_path.read_text(encoding="utf-8")
            # 限制每个笔记最多1000 tokens
            truncated = self.truncate_tokens(content, 1000)
            context += f"- **{r['title']}** (相似度: {r['similarity']:.2f})\n"
            context += f"  {truncated[:200]}...\n\n"
        
        context += "### MOC导航\n"
        context += json.dumps(moc, ensure_ascii=False, indent=2)
        
        return context[:max_tokens]
```

## 七、实施路线

| 阶段 | 内容 | 产出 |
|------|------|------|
| Phase 1 | MCP Server安装 + 基础文件系统读写测试 | 可读写Obsidian Vault |
| Phase 2 | 本地知识索引构建 + 语义搜索 | 知识检索可用 |
| Phase 3 | 双向同步 + 变更监听 | 实时同步 |
| Phase 4 | Agent任务知识注入 + 自动化归档 | 全流程闭环 |

---

> 创建时间：2026-05-31 17:00
> 状态：设计完成 · MCP连接器Phase 1待部署