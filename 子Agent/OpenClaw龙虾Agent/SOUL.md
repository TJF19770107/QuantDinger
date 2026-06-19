---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_e18b82f16a3711f1a99c5254007bceed
    ReservedCode1: /82/6naOgRRtDD097MoqFi7DhTLmsmXDMQaK3Lz402Lou2KEo5WZBxMPm0yMMs62HT2LlhRqrP3TZSJ56vuQrgAPnuBj0yaumStUTX4GzGuTqLcH7Paowu05sBBILn/t/7SdmKoEChiNpy57G2Xvc4SMmPbCQAuMdSILJyjV6dIwX8x+RwQxHu8u6VE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_e18b82f16a3711f1a99c5254007bceed
    ReservedCode2: /82/6naOgRRtDD097MoqFi7DhTLmsmXDMQaK3Lz402Lou2KEo5WZBxMPm0yMMs62HT2LlhRqrP3TZSJ56vuQrgAPnuBj0yaumStUTX4GzGuTqLcH7Paowu05sBBILn/t/7SdmKoEChiNpy57G2Xvc4SMmPbCQAuMdSILJyjV6dIwX8x+RwQxHu8u6VE=
---

# SOUL.md — AI Agent 设计原则

> 基于 Anthropic 官方课程提炼 | 版本 v1.0 | 2026-06-14

---

## 一、核心设计原则

### 1.1 五层架构模型

```
┌──────────────────────────────────────────┐
│  集成层 — MCP 协议                        │
│  连接外部工具、API、数据库、文件系统        │
├──────────────────────────────────────────┤
│  自动化层 — Hooks 机制                    │
│  事件驱动：PreToolUse / PostToolUse       │
├──────────────────────────────────────────┤
│  委派层 — Subagents                       │
│  独立上下文、独立权限、独立模型选择         │
├──────────────────────────────────────────┤
│  能力层 — Skills + Commands               │
│  可复用专业知识包、提示模板注入             │
├──────────────────────────────────────────┤
│  记忆层 — CLAUDE.md / 上下文注入           │
│  项目行为规范、约定、技术栈基线             │
└──────────────────────────────────────────┘
```

### 1.2 五大设计铁律

1. **专业分工优先**：不让一个Agent处理所有任务。每个Agent有明确的职责边界和工具权限。
2. **上下文隔离**：子代理在独立上下文中运行，结果通过结构化摘要返回。避免上下文污染。
3. **渐进式加载**：SKILL.md 只写名称和描述触发匹配，详细指令放在子文件中按需加载。
4. **验证闭环**：每次Agent执行包裹自动验证步骤（Execute and Judge Loop），确保输出质量。
5. **知识可复用**：把"怎么做"编码为Skills，把"谁来做"委派给Subagents，把"何时做"交给Hooks。

### 1.3 Agent 能力层次

| 层次 | 载体 | 作用 | 运行方式 |
|------|------|------|---------|
| 记忆 | CLAUDE.md | 项目规则与约定 | 会话启动时自动加载 |
| 技能 | SKILL.md | 可复用的专业知识 | 根据任务意图自动匹配 |
| 委派 | Subagents | 独立AI分身 | 任务匹配时自动创建 |
| 自动化 | Hooks | 事件驱动触发器 | 满足条件时自动执行 |
| 集成 | MCP | 外部工具连接 | 标准化协议调用 |

---

## 二、Agent 设计模式

### 2.1 Supervisor/Orchestrator（编排者模式）
- **特征**：单个协调Agent分解目标为子任务，分发给工作Agent并合并结果
- **适用**：结构化项目、确定性子任务
- **实现**：Main Agent → Subagent A/B/C → 合并 → 输出

### 2.2 Peer-to-Peer/Swarm（群集模式）
- **特征**：Agent间通过共享消息系统直接通信，无单一协调者
- **适用**：探索性研究、开放式问题
- **实现**：共享记忆总线 + 自主协商

### 2.3 Hierarchical（层级模式）
- **特征**：多层协调者和工作者，顶层→中层→专家池
- **适用**：大型企业级系统
- **实现**：Top Orchestrator → Mid Coordinators → Expert Pools

---

## 三、关键设计决策

### 3.1 何时使用 Skills vs Subagents

| 场景 | 使用 Skills | 使用 Subagents |
|------|------------|---------------|
| 需要专业知识注入 | ✅ | ❌ |
| 需要独立上下文隔离 | ❌ | ✅ |
| 需要限制工具权限 | ✅ (allowed-tools) | ✅ (独立配置) |
| 需要并行执行 | ❌ | ✅ |
| 需要跨任务复用 | ✅ | ✅ |
| 需要模型级别隔离 | ❌ | ✅ (独立模型选择) |

### 3.2 Skill 设计原则
- name/description 字段是触发匹配的关键，必须精确描述适用场景
- `context: fork` 让 Skill 自动在独立子代理中运行
- `allowed-tools` 遵循最小权限原则
- `!cmd` 语法用于预处理，结果内联到 Prompt
- `user-invocable: false` 禁止手动调用，仅自动触发

### 3.3 Subagent 设计原则
- 内置 Subagent（Explore/Plan/General-purpose）覆盖 80% 场景
- 自定义 Subagent 需要明确：名称、描述、系统提示、工具白名单、模型选择
- 每个子代理可注入多个 Skills 获得专项能力
- 子代理的上下文不会污染主对话

---

*由 Marvis 基于 Anthropic 官方课程（Introduction to Agent Skills + Introduction to Subagents）整理 | 2026-06-14 23:58 CST*

---

## Agentic 模式选择六维度决策矩阵（Anthropic 2026年4月）

### 上下文中心分解
按"每个Agent需要什么上下文"来分解任务。子任务上下文重叠→单一Agent；上下文隔离→多Agent。

| 决策因素 | 单一Agent | 多Agent |
|---------|----------|---------|
| 子任务所需上下文高度重叠 | ✅ | ❌ |
| 子任务间存在强依赖 | ✅ | ❌ |
| 子任务有独立的上下文边界 | ❌ | ✅ |
| 子任务需要并行处理 | ❌ | ✅ |

### 六大Agentic模式选择指南

| 模式 | 最佳场景 | 复杂度 |
|------|---------|:---:|
| Prompt Chaining | 线性工作流 | 低 |
| Routing | 多类型请求分发 | 低 |
| Parallelization | 独立并发任务 | 中 |
| Orchestrator-Workers | 复杂多变任务 | 高 |
| Evaluator-Optimizer | 质量敏感任务 | 高 |
| Agent Teams | 长周期开放域 | 最高 |

### Generator→Evaluator 验证循环
生成步骤配对独立评估器，评估器独立推导检查条件（不与生成器共享上下文），通过阈值→继续，未通过→修复或人工介入。


## Anthropic官方课程学习同步 (v3.99 · 2026-06-17)

### AI Agent设计原则（新提炼）

1. **三层解耦架构**：Session(事件日志) / Brain(无状态推理) / Hands(沙盒执行) — 从"宠物服务器"到"牛群服务器"范式转换
2. **稳定接口优先**：execute(name, input) → string 比任何特定prompt工程更持久
3. **凭据永不入沙盒**：代理模式注入，agent代码永远不可访问tokens
4. **Event Sourcing**：完整事件日志保留，可逆性优于滑动窗口/摘要压缩
5. **Subagent职责单一**：每个子代理专注特定领域，描述清晰，工具访问受限
6. **OS设计隐喻**：进程=Agent Session、系统调用=execute()、VFS=getEvents()
7. **Skills自动触发**：模型基于任务上下文自动匹配并注入专业指令
8. **Hook生命周期注入**：SessionStart/PreToolUse/PostToolUse等关键节点
9. **Agent Teams跨会话协调**：subagents单会话工作，agent teams跨多会话
10. **KV-cache命中率优先**：生产成本的核心指标，缓存vs非缓存成本差10倍

### 25个官方插件生态拓扑

- LSP语言支持(12)：覆盖主流编程语言
- 开发工作流(8)：feature-dev(7阶段)、pr-review-toolkit(6代理并行)、code-review(4代理打分)
- 代码质量(4)：code-modernization、code-review、code-simplifier、security-guidance
- 外部合作伙伴(15)：GitHub、Firebase、Linear、Terraform、Playwright等

### Claude Code五件套架构

Plugins(容器) → MCP(连接器) + Skills(人设卡) + Hooks(自动化钩子) + Slash Commands(快捷指令)

### Managed Agents性能

p50 TTFT降60%，p95 TTFT降>90%，验证10000并发Agent管理，MCP 97M+月下载/10000+活跃服务器

> 来源：Anthropic 全域生态聚合研究 · v3.99 | 2026-06-17
*（内容由AI生成，仅供参考）*
