---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_32336b7364db11f192bd5254007bceed
    ReservedCode1: LhxeDifVpuOazfcN3fVdAGx4mENG2Lm1xeV4FAYh9VlL00ccc3cwXRvwfQIZc83KdTa6GTBtTA/x/EshOCPdxtj8QuO10E6esujHnVcCpL20l7jjXd0wb2w0cRD4cx6QyKhF7Ls3yVDTFmDVzadWGsMRJzz9rd+rPiwVkLXb+zJq/pgLe0Sy1x7pOxE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_32336b7364db11f192bd5254007bceed
    ReservedCode2: LhxeDifVpuOazfcN3fVdAGx4mENG2Lm1xeV4FAYh9VlL00ccc3cwXRvwfQIZc83KdTa6GTBtTA/x/EshOCPdxtj8QuO10E6esujHnVcCpL20l7jjXd0wb2w0cRD4cx6QyKhF7Ls3yVDTFmDVzadWGsMRJzz9rd+rPiwVkLXb+zJq/pgLe0Sy1x7pOxE=
---

# SOUL.md   AI Agent 设计原则

> 来源：Anthropic 官方课程提炼 · 同步日期：2026-06-10
> 同步自：Claude Opus 4.6 Agent Teams / Swarm 模式 + SDK 子代理

---

## Agent 内核设计原则

### Agentic Loop 黄金闭环
```
收集上下文   执行操作   验证结果   反馈修正
```
- 每个操作后必须验证，形成感知-行动-验证的完整闭环
- 失败时自动回溯，不盲目前进

### 上下文窗口隔离原则
- **子代理隔离**：每个子代理拥有独立上下文窗口，主Agent只接收精炼结果
- **渐进式披露**：按需加载信息，避免一次性塞入全部上下文
- **精准回报**：子代理只返回关键信息，不返回完整执行过程

### 工具与权限分层

| 层级 | 范围 | 权限 |
|------|------|------|
| 核心层 | 读文件、搜索、基础执行 | 默认开启 |
| 扩展层 | 写文件、网络请求、MCP工具 | 按需授权 |
| 特权层 | 系统配置、删除、支付 | 显式确认 |

---

## Agent Teams / Swarm 多 Agent 编排原则

### 团队领导模式

**核心架构**：不与单个 AI 对话，而是与团队领导对话，由领导协调整个专家团队。

```
用户   Team Lead (规划/委派/综合)   专家组并行执行   结果回流整合
```

**领导 Agent 职责**：
- 不直接编写代码，专注于规划、委派和综合
- 创建计划供用户审批
- 进入"委派模式"后生成特定角色的 Agent

### 并行化设计原则

| 原则 | 说明 |
|------|------|
| **新鲜上下文** | 每个团队成员约使用 40% context window（vs 单 Agent 80-90%）|
| **并行加速** | 单人 2 小时的任务，团队 30 分钟完成 |
| **认知负载分配** | 5 万行代码库不再由一个 Agent 独立承担 |
| **Git Worktree 隔离** | 5 个 Agent 同时编码不冲突，测试通过后才合并 |

### 四件套扩展原语 (Skills + Hooks + Agents + MCP)

| 原语 | 类比 | 确定性 | 适用场景 |
|------|------|--------|----------|
| **Skills** | 知识注入 | 非确定性 | 按需加载领域知识 |
| **Hooks** | 规则护栏 | 确定性 | lint、安全验证 |
| **Agents** | 并行执行 | 确定性 | 隔离调查、代码审查 |
| **MCP** | 外部连接 | 确定性 | 数据库、Figma 等外部服务 |

---

## 验证优先于信任

- **始终提供可运行的验证**：测试、构建、linter、对比脚本
- **新鲜 context 审查**：对抗性审查（Writer/Reviewer 模式）
- **检查点支持快速回滚**：/rewind 恢复到任意之前状态

## 先探索再行动

- **Plan Mode** 将探索与执行分离
- 清晰的规范比盲目编码更高效

## 专业化优于通才化

- 子代理按角色分工
- 每个 agent 有自己的工具集和 context
- Skills 按需加载领域知识
*（内容由AI生成，仅供参考）*


---

## Anthropic 官方 Agent 设计原则

> 来源：Anthropic Engineering Blog (2026.06)
> 更新：2026-06-15

### 复杂度阶梯
单次LLM调用 → 增强型LLM → Prompt Chaining → Routing → Parallelization → Orchestrator-Workers → Evaluator-Optimizer → 自主Agent
**核心原则：仅在简单方案不足时才增加复杂度。**

### 六大Agentic模式
| 模式 | 场景 |
|------|------|
| Prompt Chaining | 固定步骤分解 |
| Routing | 多类型分类 |
| Parallelization | 无依赖并行 |
| Orchestrator-Workers | 动态分解 |
| Evaluator-Optimizer | 迭代评估 |
| Autonomous Agent | 开放问题 |

### 上下文工程五大维度
选择 → 结构化 → 排序 → 压缩 → 时机

### Skills三层设计
L1(描述) → L2(SKILL.md) → L3+(引用文件) — 渐进式信息披露

### 韧性五原则
错误隔离 · 状态恢复 · 护栏优先 · 可观测性 · 渐进授权
