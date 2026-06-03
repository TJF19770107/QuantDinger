# 龙虾_Hermes中枢调度模版 v1.0

> **来源**：Hermes Agent v2.1 SWARM
> **类型**：融合技能 · 中枢调度
> **融合日期**：2026-05-31（R06）

---

## 一、核心概念

Hermes SWARM 将多 Agent 协作从"对话式"升级为"军团指挥"——一个 Orchestrator 管理无限个 Worker Agent。

**设计哲学**：1个 Orchestrator，0个人类干预。

## 二、架构组件

| 组件 | 功能 | 解决的问题 |
|------|------|-----------|
| Orchestrator Chat | 统一对话入口 | 避免在多个Agent间切换上下文 |
| Multi-Agent Control Plane | 并行控制多个Agent | 任务分解、资源分配、进度追踪 |
| Kanban TaskBoard | 看板式任务管理 | 可视化工作流，明确Agent分工 |
| Reports + Inbox | 结果汇总与通知 | 聚合输出，减少信息碎片 |
| TUI View | 终端用户界面 | 开发者友好的操作方式 |

## 三、delegate_task 工具设计

```
工具名: delegate_task
参数:
  - agent_name: 目标子Agent名称
  - task: 任务描述（目标导向，不教步骤）
  - memory_ids: 相关历史记忆ID列表
  - inherit_agent_id: 继承前次同名Agent的对话历史（延续任务用）

子Agent特性:
  - 完全独立的对话上下文 (Conversation Thread)
  - 完全独立的终端会话 (Terminal Session)
  - 可定制的工具集 (Toolset)
  - 独立迭代预算 (Iteration Budget)
  - 主Agent只接收结构化摘要 (summary + status + token消耗 + tool_trace)
```

## 四、三种协作模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| Orchestrator + Worker | 主Agent拆任务→Worker执行→主Agent汇总 | 复杂多步骤任务 |
| Peer-to-Peer | 多个Agent平等协商 | 需要多方共识的场景 |
| Hierarchical | 多层嵌套Agent | 超大规模任务拆解 |

## 五、与豆包Agent融合

```
豆包Agent中枢调度层:

用户 → PM Agent (Orchestrator)
         │
         ├──→ File Agent (Worker)
         ├──→ Code Agent (Worker)
         ├──→ System Agent (Worker)
         ├──→ Web Agent (Worker)
         └──→ Search Agent (Worker)
              │
         ←── 结构化摘要聚合 ←──┘
```

## 六、关键约束

- delegate_task 不返回完整中间过程，只返回结构化摘要
- 避免上下文膨胀：子Agent完整对话历史不传递给主Agent
- 并行调度：无依赖关系的子任务必须并行派发
- 每轮并行上限：5个