# 豆包Agent技能库同步 · 全维度迭代 v4.0
## 同步时间: 2026-05-31 03:00

---

## 一、自进化Agent核心架构

### 1.1 四层记忆系统
- 即时上下文 → 短期工作记忆 → 长期结构化记忆（知识图谱） → 经验技能库
- MEMORY.md (~800 tokens) + USER.md (~500 tokens) 硬上限 + 自动压缩
- SQLite + FTS5全文搜索 + LLM摘要跨会话召回

### 1.2 5步自进化闭环
Execute → Evaluate → Abstract → Refine → Recall
触发条件：≥5次tool call / 出错恢复 / 用户纠正 / 非显而易见工作流

### 1.3 Karpathy Loop自主优化范式
Agent + 可修改目标 + 可量化指标 + 时间预算 = 自主优化循环
适用于代码性能优化、Prompt工程、数据库调优、CI/CD流水线

---

## 二、MCP标准工具总线

- 协议：MCP JSON-RPC 2.0
- 传输：stdio / SSE / HTTP Stream
- 生态：5000+社区工具服务器
- 豆包专属MCP Server：文件系统 / Shell / 浏览器 / Git / 数据库 / 代码执行 / API网关

---

## 三、多Agent协作引擎

主Agent (Pro) → 编码Agent (Code) / 搜索Agent / 文件Agent / 部署Agent / 文档Agent
- 并发上限5，嵌套深度≤2
- 安全隔离：子Agent仅访问授权工作区

---

## 四、本地双层协作架构

Soul Layer (本地GPU, ≤7B量化) + Worker Layer (云端API, Doubao-Seed-2.0-Pro/Code)
对标 Eve Agent V2U (40轮工具调用循环 + 112子代理 + 273技能模块)

---

## 五、技能生态标准

SKILL.md = YAML frontmatter + Markdown步骤
渐进式披露：目录扫描(~50tokens/技能) → 匹配加载 → 未使用不占上下文

---

## 六、豆包AI IDE功能蓝图

代码补全（多文件感知+Tree-sitter） / 项目级生成 / Profiler性能分析 / PR自动审查
一键部署（Docker + CI/CD + K8s）

---

*同步至: E:\龙虾AI主控中心\我的AI分身\技能库\*
*主方案: 豆包Agent-v4.0-全维度迭代方案-20260531-0300.md*
