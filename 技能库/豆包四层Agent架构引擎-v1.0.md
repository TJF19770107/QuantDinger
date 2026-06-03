# 豆包四层Agent架构引擎 v1.0

> **技能编号**：13
> **类型**：架构层
> **创建时间**：2026-05-31
> **来源**：R01全维度迭代

---

## 架构总览

```
┌────────────────────────────────────────────────┐
│            豆包APP · 四层Agent架构 v1.0          │
├────────────────────────────────────────────────┤
│ L4 编排层  │ Kanban任务看板 · Dynamic Workflows │
│           │ 定时调度 · Multi-Agent编排          │
├───────────┼────────────────────────────────────┤
│ L3 执行层  │ 6子Agent并行池 · Smart Approvals   │
│           │ Git Worktree隔离 · 角色分工        │
├───────────┼────────────────────────────────────┤
│ L2 能力层  │ Skills技能库 · 工具调用链 · Hooks  │
│           │ Computer Use · 自进化闭环           │
├───────────┼────────────────────────────────────┤
│ L1 推理层  │ 主模型规划 · 子模型执行 · Effort   │
│           │ Control · 判断力校准 · Context 1M  │
└───────────┴────────────────────────────────────┘
```

## 各层职责

### L1 推理层
- 主模型(大参数)负责：任务理解、规划拆解、最终判断
- 子模型(小参数)负责：窄任务执行、简单工具调用
- Effort Control：按任务复杂度动态调整推理深度
- 判断力校准：不确定性自主检测，证据不足时主动确认

### L2 能力层
- Skills技能库：标准化SKILL.md，上下文自动加载匹配
- 工具调用链：工具注册→发现→调用→结果验证闭环
- Hooks引擎：PrePrompt审计 → PostToolUse验证 → PreCommit检查
- Computer Use：屏幕查看、点击、输入、跨应用操作
- 自进化闭环：经验沉淀→技能生成→持续优化

### L3 执行层
- 6子Agent并行池：每个Agent运行在隔离沙箱中
- Git Worktree隔离：多Agent同时操作同一仓库无冲突
- 角色分工：Explorer(只读扫描) / Worker(读写执行) / Reviewer(审查) / Tester(测试) / Deployer(部署) / Custom(自定义)
- Smart Approvals：守护代理审查 → 静默批准/风险评估/直接拦截

### L4 编排层
- Kanban任务看板：任务上板→Agent自主认领→原子锁防冲突
- Dynamic Workflows：临时编排脚本→拆解→并行分配→汇总
- 定时调度：一次性/周期性任务自动触发
- 9种协作模式：扇出并行/流水线/投票仲裁/人在环审核/主从/竞争/接力/聚合/监督

## 对标参考

- L1推理层 ← Claude Effort Control + Codex GPT-5.4双层路由
- L2能力层 ← Codex Skills + Hooks + Computer Use
- L3执行层 ← Codex 6子Agent + Smart Approvals + Git Worktree
- L4编排层 ← Hermes Kanban + Claude Dynamic Workflows + Antigravity /schedule