# 龙虾-知识库MCP原生接入协议 v1.0

> **对标来源**：Obsidian+MCP + Claude Code Files MCP
> **创建日期**：2026-06-01 (R13)
> **版本**：v1.0

---

## 一、协议概述

通过MCP（Model Context Protocol）桥接，让AI Agent直接读取、搜索、交叉引用本地Obsidian知识库中的Markdown笔记，实现基于个人知识库的深度问答与知识综合。

## 二、技术架构

### 2.1 数据流

```
网页内容 → Save(干净Markdown) → Obsidian知识库 → MCP Server → AI Agent
```

### 2.2 各组件职责

| 组件 | 职责 |
|------|------|
| Save/剪藏工具 | 将杂乱网页转换为结构化Markdown |
| Obsidian | 本地存储和组织Markdown文件 |
| MCP Server | 暴露知识库目录为AI可读取资源 |
| AI Agent | 搜索、读取、交叉引用、综合 |

### 2.3 为什么Markdown是关键

- 纯文本：任何AI无需特殊解析器即可读取
- 保留结构：标题、列表、代码块、链接都承载语义
- 轻量：AI可快速处理数百个Markdown文件
- 通用：无供应商锁定，与任何工具兼容

## 三、四类核心场景

### 3.1 研究综合
"根据我保存的15篇关于无服务器架构的文章，提到了哪些主要的成本优化策略？"
→ 搜索知识库 → 读取相关笔记 → 综合答案并附引用

### 3.2 写作辅助
"从我保存的内容中找出支持本地优先软件正在获得更多关注这一论点的例子。"
→ 提取相关引用和数据点

### 3.3 决策支持
"我保存了关于Postgres托管服务商的比较文章。请根据我保存的研究总结Neon、Supabase和PlanetScale之间的权衡。"
→ 基于已收集内容综合分析

### 3.4 学习路线
"根据我保存的关于Astro的教程和文档，制定一个学习路线图。"
→ 将已保存内容整理为学习顺序

## 四、知识库优化建议

| 策略 | 说明 |
|------|------|
| 描述性文件名 | `react-server-components-performance-guide.md` |
| 结构化内容 | 使用标题层级、列表、代码块 |
| 标签和链接 | 利用Obsidian的`[[双向链接]]`和标签 |
| 定期整理 | 清理过时笔记，保持知识库新鲜度 |

## 五、豆包Agent适配方案

1. File Agent升级支持Obsidian知识库目录的MCP协议接入
2. 新增知识库搜索能力：跨笔记关键词检索+语义关联
3. 支持基于知识库的RAG问答
4. 自动识别知识库目录结构并建立索引
5. 与MemoryOS联动：知识库内容可转化为长期记忆

## 六、配置示例

```json
{
  "mcp_server": "files-mcp",
  "vault_path": "E:/Obsidian/MyVault",
  "index_strategy": "incremental",
  "auto_sync": true,
  "sync_interval_minutes": 30
}
```

---

> 协议编号：55 | 对标：Obsidian+MCP | 优先级：P1
