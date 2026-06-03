# GAP BACKLOG v3.1 — R17更新 · 缺口追踪清单

## R17 新增缺口

| ID | 缺口描述 | 优先级 | 对标源 | 状态 | 识别轮次 | 计划关闭 |
|----|----------|--------|--------|------|----------|----------|
| GAP-049 | Claude Code五级压缩流水线 | P0 | Claude Code Runtime: Tool Result Budget→Snip→Microcompact→Collapse→Autocompact | 📐 DESIGNED | R17 | R18 |
| GAP-050 | Hook事件系统(0/1/2退出码) | P0 | Claude Code Hooks: Command/Prompt/Agent/HTTP | 📐 DESIGNED | R17 | R18 |
| GAP-051 | GEPA多目标进化优化器 | P0 | Hermes GEPA (ICLR 2026 Oral): 遗传进化+帕累托前沿+约束门控 | 📐 DESIGNED | R17 | R18 |
| GAP-052 | DGM档案树进化策略 | P1 | Darwin Gödel Machine: LLM变异算子+档案选择 | 📋 新 | R17 | R19 |
| GAP-053 | 自修改治理审计追踪 | P1 | 三学派风险分析: 版本化/可逆事务/审批关卡/奖励操纵检测 | 📋 新 | R17 | R18 |
| GAP-054 | Fork子Agent缓存优化 | P1 | Claude Code Fork机制: 共享请求前缀命中Prompt Cache | 📋 新 | R17 | R19 |
| GAP-055 | Swarm对等协作模式 | P1 | Claude Code Swarm: 共享API客户端+MCP连接+命名信箱 | 📋 新 | R17 | R19 |
| GAP-056 | 工作流动态路由+交互Chat | P1 | Google Opal: Agent Step自主分析+动态路径+多轮对话 | 📋 新 | R17 | R19 |
| GAP-057 | 记忆异步预取+新鲜度评分 | P1 | Claude Code Memory: 并行搜索+时效检测+"记忆是线索不是事实源" | 📋 新 | R17 | R18 |
| GAP-058 | Bash命令AST安全解析 | P1 | Claude Code tree-sitter: fail-closed策略+20+静态规则 | 📋 新 | R17 | R19 |

## 历史缺口状态 (R16末态 → R17)

| ID | 描述 | R16 | R17 | 说明 |
|----|------|-----|-----|------|
| GAP-001~044 | P0/P1 全部关闭 | ✔️ | ✔️ | 保持关闭 |
| GAP-045 | 多模型协作架构 | 📐 DESIGNED | 📐 DESIGNED | 保持 |
| GAP-046 | 时间知识图谱 | 📐 DESIGNED | 📐 DESIGNED | 保持 |
| GAP-047~048 | P2远期 | 📋 | 📋 | 保持跟踪 |
| GAP-009~033 | P1/P2远期 | 📋 | 📋 | 保持跟踪 |

## 统计摘要

| 类别 | R16 | R17 | 变化 |
|------|-----|-----|------|
| P0 新缺口 | 0 | 3 | +3 |
| P0 DESIGNED | 0 | 3 | +3 |
| P1 新缺口 | 0 | 7 | +7 |
| P2 远期缺口 | 13 | 13 | — |
| ✔️ 已关闭 | 37 | 37 | — |
| **总计** | **37** | **50** | **+13** |

## R17重点行动 (全部完成)

| 优先级 | ID | 行动 | 状态 |
|--------|----|------|------|
| 🟢 P0 | GAP-049 | 五级压缩流水线方案设计 | 📐 DESIGNED |
| 🟢 P0 | GAP-050 | Hook事件系统方案设计 | 📐 DESIGNED |
| 🟢 P0 | GAP-051 | GEPA多目标进化优化器方案设计 | 📐 DESIGNED |
| 🔵 采集 | — | 全网情报采集: 5篇深度+3研究系统 | ✅ 完成 |

## R18 计划行动

| 优先级 | ID | 行动 | 预期产出 |
|--------|----|------|---------|
| P0 | GAP-049 | 五级压缩流水线代码落地 | ~400行Python |
| P0 | GAP-050 | Hook事件框架代码落地 | ~300行Python |
| P0 | GAP-051 | GEPA优化器代码落地 | ~500行Python |
| P1 | GAP-053 | 治理审计追踪模块 | ~300行Python |
| P1 | GAP-057 | 记忆异步预取模块 | ~250行Python |

---
*更新于 R17 · 2026-05-31 19:10*