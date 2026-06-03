# 豆包Agent v4.0-R06 当前激活版本
> 版本：v4.0-R06
> 最后更新：2026-05-31 R06
> 状态：ACTIVE

## 核心架构：四层协同 + 端云路由 + 看板（规划中）

```
Layer 4: 看板层（KanbanBoard）       →  任务可视化、熔断保护（R06新增）
Layer 3: 云端顾问层（豆包Pro 2.0）   →  复杂推理、长文本、专家角色
Layer 2: 本地执行层（端侧模型）      →  代码执行、GUI、工具调用
Layer 1: 自进化核心（Self-Evolve v3.0）→ GEP协议、Meta进化、记忆系统
```

## 八大Agent模块（R06扩展：6→8）

| 模块 | 对标 | 状态 |
|------|------|------|
| PM Agent | Codex /goal + Hermes Orchestrator | 进入实现 |
| Code Agent | Claude Code + OpenCode LSP | 基础框架 |
| File Agent | Marvis File Agent | 基础框架 |
| GUI Agent | UI-TARS | 规划中 |
| Browser Agent | Marvis Browser | 规划中 |
| Self-Evolve Agent | Evolver GEP + HyperAgents Meta | v3.0设计 |
| TaskBoard Agent 🆕 | Hermes SWARM Kanban | R06设计 |
| IDE Agent 🆕 | Claude Code + OpenCode | R06设计 |

## R06关键注入

- Codex /goal → 持久目标引擎
- Hermes Kanban → 任务看板+熔断
- Claude Code → 检查点快照+崩溃恢复
- OpenClaw → ACP协议
- OpenCode → LSP智能感知
- Evolver + HyperAgents → GEP+Meta进化

## 最新迭代报告

见：2026-05-31_R06_全维度迭代升级报告_v6.0.md