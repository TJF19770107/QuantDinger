---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_44c3eef35ede11f1a4f35254002afed2
    ReservedCode1: k2DD7t7kK6M2TMGV943A5a3CgWz44iEkXiHh/0EZQ9OAuf5hft2SQ7LE5LIM48RqiY6ez3ZNl7EImWus+jz48m7bY+zqrkW2TR0a6IyhjdGtqVQGhMFuTUS2Y9J6x+DXmfbrZFxSidI0kRAM2nGOsK/FljxGdkPO8WabeNP5PYDzPBVBWa0Kno2eHpI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_44c3eef35ede11f1a4f35254002afed2
    ReservedCode2: k2DD7t7kK6M2TMGV943A5a3CgWz44iEkXiHh/0EZQ9OAuf5hft2SQ7LE5LIM48RqiY6ez3ZNl7EImWus+jz48m7bY+zqrkW2TR0a6IyhjdGtqVQGhMFuTUS2Y9J6x+DXmfbrZFxSidI0kRAM2nGOsK/FljxGdkPO8WabeNP5PYDzPBVBWa0Kno2eHpI=
---



# 龙虾-Agent Harness六层运行时架构协议 v1.0

> **版本**: v1.0  
> **创建日期**: 2026-06-03  
> **对标来源**: Mitchell Hashimoto Harness Engineering + LangChain DeepAgents + Claude Code Harness + SanityHarness  
> **核心价值**: Agent运行时操作系统级管控 · 六大核心组件 · 生产级稳定交付 · 可观测可审计可回滚  

---

## 一、协议背景

### 1.1 Harness Engineering 范式确立

2026年2月，HashiCorp联合创始人Mitchell Hashimoto首次提出**Harness Engineering**术语，定义为"为Agent构建防止重复犯错机制的工程实践"。随后OpenAI、Martin Fowler、LangChain Harrison Chase等行业领袖跟进，行业共识确立：

```
Agent = Model + Harness
```

**模型决定了能力的理论上限，Harness决定了能力的实际落地效果。**

LangChain实测数据：仅优化Harness层逻辑，底层模型（Claude Sonnet 4.5）完全不变，Coding Agent任务得分从52.8跃升至66.5，行业排名从第30名升至第5名。

### 1.2 与前置协议的关系

本协议与以下已有协议互补而非替代：
- 协议#12 IDE→Agent容器架构: 侧重IDE集成
- 协议#36 文件系统原生沙盒: 侧重文件隔离
- 协议#14 多Agent并行隔离开发: 侧重多Agent隔离
- 协议#118 影子Agent安全复盘: 侧重安全审计

**本协议聚焦**: Agent运行时操作系统——Harness层全生命周期管控。

---

## 二、六层核心架构

### 2.1 架构总览

```
┌─────────────────────────────────────────────────┐
│                  LLM 模型层                       │
├─────────────────────────────────────────────────┤
│              Agent Framework 层                   │
│         (LangGraph / AutoGen / CrewAI)            │
├─────────────────────────────────────────────────┤
│            ★ Agent Harness 运行时层 ★             │
│  ┌──────┬──────┬──────┬──────┬──────┬──────┐    │
│  │ 工具  │ 上下文│ 状态  │ 子Agent│ 安全 │ 可观测│    │
│  │ 集成  │ 工程  │ 调度  │ 编排  │ 防护  │ 审计  │    │
│  └──────┴──────┴──────┴──────┴──────┴──────┘    │
└─────────────────────────────────────────────────┘
```

### 2.2 六大组件详解

#### Layer 1: 标准化工具集成层 (Tool Integration Layer)

| 能力 | 实现 |
|------|------|
| 工具发现注册 | MCP协议自动发现 + 版本管理 |
| 调用前校验 | pre_tool_use钩子：参数校验 + 权限检查 |
| 调用中控制 | 超时控制 + 重试策略 + 降级备用链 |
| 调用后校验 | post_tool_use钩子：结果合理性校验 + 格式化 |
| 工具开销控制 | 175工具MCP服务器仅定义即占26%上下文 → 按需加载 |

**创新点**: 钩子机制拦截所有工具调用，从根源避免工具滥用。

#### Layer 2: 上下文工程系统 (Context Engineering System)

| 能力 | 实现 |
|------|------|
| 自动压缩 | 长对话自动摘要压缩，保留关键信息 |
| 优先级排序 | 任务指令 > 项目规范 > 历史对话 > 参考信息 |
| 持久化注入 | claude.md风格项目级规则自动加载 |
| 分区隔离 | 主任务上下文 / 子任务上下文 / 工具上下文三者隔离 |
| 无关过滤 | 自动识别并过滤与当前任务无关的历史信息 |

**创新点**: 结构化状态替代聊天历史，数十小时任务不丢失核心目标。

#### Layer 3: 状态持久化与任务调度引擎 (State & Scheduling Engine)

| 能力 | 实现 |
|------|------|
| 断点续传 | 每步自动Checkpoint，崩溃后从断点恢复 |
| 任务拆解 | write_todos自动拆解复杂任务为子任务 |
| 状态跟踪 | 待办/进行中/已完成/失败四态管理 |
| 多任务并行 | 依赖管理 + 优先级调度 |
| 企业集成 | K8s/Airflow 调度系统无缝集成 |

**创新点**: Durable Execution保障，Exactly-Once语义，进程崩溃自动恢复。

#### Layer 4: 子Agent编排与隔离系统 (Sub-Agent Orchestration)

| 能力 | 实现 |
|------|------|
| 动态生成 | 主Agent按需生成临时专用子Agent |
| 上下文隔离 | 子Agent工作不污染主Agent核心上下文 |
| 并行执行 | 多子Agent同时处理不同子任务 |
| 能力专业化 | 不同子Agent配置专属工具/提示词/模型 |
| 结果聚合 | 子Agent完成后结果汇总主Agent |

**创新点**: 千级Agent并行编排能力（对标Claude Dynamic Workflows 1000并行/Bun 75万行99.8%通过率）。

#### Layer 5: 验证与安全防护层 (Validation & Guardrails Layer)

| 能力 | 实现 |
|------|------|
| 输出校验 | 结构化校验 + 合规审核 |
| 业务规则注入 | 行业规则自动拦截违规操作 |
| 前置拦截 | 三个关键节点：LLM生成后 → 工具调用前 → 结果输出前 |
| 沙箱执行 | 代码执行全沙箱隔离 |
| 审计日志 | 全流程可审计，满足金融/政务监管 |

**创新点**: 非事后审核，全流程前置拦截，从根源避免幻觉与违规。

#### Layer 6: 可观测性与审计系统 (Observability & Audit System)

| 能力 | 实现 |
|------|------|
| 链路追踪 | Agent执行全流程Span追踪 |
| 实时监控 | 进度/Token消耗/工具成功率Dashboard |
| 自动告警 | 异常自动告警 + 根因分析 |
| 审计留存 | 全流程操作日志持久化 |
| 数据闭环 | 执行轨迹数据 → 优化Harness规则 → 微调模型 |

**创新点**: "推理→数据→优化"闭环，Harness采集数据反哺模型迭代。

---

## 三、与传统框架的边界

| 维度 | Agent Framework | Agent Harness |
|------|:---:|:---:|
| 定位 | 开发时脚手架 | **运行时操作系统** |
| 核心问题 | 能否快速开发出来 | **能不能稳定、安全、长期跑起来** |
| 生命周期 | 代码开发阶段 | **运行时全流程** |
| 设计理念 | 非侵入、最大自由度 | **强约束、内置最佳实践** |
| 工程价值 | 提升开发效率 | **保障生产级可用性** |
| 典型产品 | LangGraph/AutoGen/CrewAI | **DeepAgents/Claude Code Harness/Harness.io** |

---

## 四、硅谷主流Harness方案对标

| 方案 | 定位 | 核心优势 | 豆包对标 |
|------|------|---------|---------|
| LangChain DeepAgents | 开源通用Harness | 可插拔/多后端/开箱即用 | 工具集成层 |
| Claude Code Harness | 编码Agent标杆 | claude.md规则/子Agent/技能系统 | 上下文工程+子Agent编排 |
| Harness.io Agents | DevOps企业级 | Pipeline引擎/GitOps/可视化 | 状态调度+可观测 |
| SanityHarness | 轻量本地 | 结构化状态/多模型路由/输出校验 | 安全防护+多模型 |
| Water | Python高可用 | 生产级HA/高可控 | 断点续传+自愈 |

---

## 五、Harness Engineering 推动AI开发范式转变

```
传统软件开发: 框架(Spring/React) + 运行时(JVM/Node/容器)
现代AI Agent:  Agent框架(LangGraph) + Harness运行时 ← 新范式
```

Harness标志着AI从"实验式提示词工程"，正式走向**可版本、可部署、可监控、可回滚、可审计**的现代软件工程。

---

## 六、落地映射

### 6.1 豆包Agent Harness实现路径

| 阶段 | 内容 | 对标 |
|------|------|------|
| Phase 1 | 标准化工具集成层 (MCP+Hooks) | LangChain DeepAgents |
| Phase 2 | 上下文工程系统 (自动压缩+分区隔离) | Claude Code Harness |
| Phase 3 | 状态持久化+子Agent编排 | 千级并行编排协议v3.0 |
| Phase 4 | 可观测审计闭环 | Harness.io + Prometheus |

### 6.2 P0缺口闭合

Harness 99→100 的决定性一步：**六层运行时架构的系统化落地**，尤其是"可观测审计系统"的建立——当Agent执行过程不再黑盒，全链路可追踪可审计时，Harness才真正达到满分。

---

> 协议文件: 龙虾-Agent Harness六层运行时架构协议v1.0.md  
> 对标来源: Mitchell Hashimoto / LangChain / Claude Code / Harness.io  
> 生效范围: 豆包Agent Harness运行时层  
> 版本: v1.0 | 日期: 2026-06-03
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
