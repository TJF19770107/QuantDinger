# 龙虾-AgenticRAG本地文件智能检索协议 v1.0

> **协议编号**：61
> **对标来源**：GraphRAG 2026 + Agentic RAG Architecture + LangGraph/CrewAI
> **创建日期**：2026-06-01
> **适用Agent**：豆包Agent / 全域子Agent
> **依赖**：AutoFileScanner v4.0+ / ChromaDB或Qdrant / KuzuDB或Neo4j

---

## 一、协议概述

本协议将本地文件检索从静态Pipeline RAG升级为Agentic RAG。核心变革：AI不再是"被动检索者"，而是"主动决策者"——由Agent自主决定读什么、怎么读、去哪里查、查完后是否需要二次检索或交叉验证。

## 二、架构设计

### 2.1 三层检索路由

```
用户Query → Orchestrator Agent
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
Vector Search  Graph Search  Keyword/BM25
(Dense/语义)   (实体关系)    (精确匹配)
    │           │           │
    └───────────┼───────────┘
                ▼
         Fusion & Rerank
                │
                ▼
         Self-RAG (自反思)
                │
                ▼
           最终回答 + 引用
```

### 2.2 Agentic决策循环

```
Thought → Action → Observation → Reflection → (重复或输出)

- Thought: Agent分析查询意图
- Action: 选择检索工具（Vector? Graph? BM25? 组合?）
- Observation: 获取检索结果
- Reflection: 
  - 如果结果足够 → 输出答案
  - 如果不够 → 换工具/换关键词/扩大范围重试
  - 如果交叉验证冲突 → 标记不确定性
```

## 三、核心能力

### 3.1 知识图谱增强（GraphRAG）

- **实体提取**：从本地文件中提取实体（人物、概念、技术、时间）和关系
- **图查询**：支持跨文档关系查询（如"A技术和B技术的关系是什么"）
- **图存储**：本地嵌入式图数据库（KuzuDB），无需独立服务

### 3.2 混合检索融合

| 检索方式 | 适合场景 | 技术 |
|---------|---------|------|
| Dense Vector | 语义相似、模糊匹配 | nomic-embed / voyage-2 |
| Knowledge Graph | 实体关系、逻辑推理 | KuzuDB / Neo4j |
| BM25/Sparse | 精确关键词、错误码 | Full Text Search |

### 3.3 Self-RAG自反思

- 检索后自动评判：这条信息真的相关吗？
- 不相关→自动换策略重试
- 部分相关→标注置信度
- 交叉验证：多个来源信息冲突时标记

### 3.4 Agentic Chunking

- 不再按字符数机械分块
- 使用LLM语义分组，相关句子保持在一起
- 保留文档结构（标题层级、表格、列表）

## 四、实施路径

### Phase 1：Agentic路由（当前可落地）
- 在现有AutoFileScanner v4.0基础上增加Agent决策层
- 实现Thought→Action→Observation→Reflection循环
- 多工具并行调用+结果融合

### Phase 2：知识图谱集成
- 文件索引时自动构建知识图谱
- 实体关系提取自动化
- 图查询工具接入Agent路由

### Phase 3：Self-RAG自反思
- 检索质量自评判模块
- 自动策略切换
- 置信度标注与不确定性透明化

## 五、安全约束

- 所有检索在本地执行，数据不出设备
- 知识图谱存储在本地嵌入式数据库
- 敏感文件自动过滤（.env/.ssh/.git等）
- Agent决策日志完整审计

---

> **版本**：v1.0
> **状态**：ACTIVE
> **关联文件**：AutoFileScanner_v4_FileSense.md, capabilities_R18.json
