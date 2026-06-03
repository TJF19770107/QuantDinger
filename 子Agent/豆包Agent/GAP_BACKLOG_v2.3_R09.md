# GAP BACKLOG v2.3 — R09更新 · 缺口追踪清单

| ID | 缺口描述 | 优先级 | 对标源 | 状态 | 识别轮次 | R09注入 | 计划关闭 |
|----|----------|--------|--------|------|----------|---------|----------|
| GAP-001 | Harness工程飞轮 | P0 | Codex Traces→Evals | 🔧 启动 | R03 | Codex Evals基准设计参考 | R12 |
| GAP-002 | Agent间直接通信(P2P) | P0 | Claude Agent Teams Mailbox | 📋 增强 | R03 | Claude Mailbox完整方案注入：点对点+Shared Task List+@提到/广播 | R12 |
| GAP-003 | 自动技能生成闭环 | P0 | SkillForge v1.0 | ✔️ 关闭(R08) | R03 | 增强：Tool Search按需加载（Hermes标杆） | — |
| GAP-004 | Skill Card标准化模板 | P0 | NVIDIA Verified Skills | 🔧 启动 | R08 | NVIDIA验证流程完整注入：编目→扫描→评估→签名→卡片 | R11 |
| GAP-005 | 向量化记忆检索落地 | P0 | OpenClaw SQLite-vec | ✅ 设计完成 | R07 | SQLite-vec落地路径+RSC递归状态压缩增强 | R10 |
| GAP-006 | 持久目标引擎（GoalStore） | P1 | Hermes /goal | 📋 | R03 | Hermes /goal 完成检测 + HEARTBEAT 心跳 | R12 |
| GAP-007 | 任务看板系统 | P1 | Hermes Kanban v0.15 | 📋 | R03 | Hermes v0.15 Kanban Swarm增强 | R13 |
| GAP-008 | 检查点快照（SnapshotEngine） | P1 | Claude Code Snapshots | 📋 | R03 | Idempotency Gates Merkle回滚方案注入 | R13 |
| GAP-009 | 代码智能感知（LSP） | P1 | OpenCode LSP | 📋 | R03 | — | R14 |
| GAP-010 | Meta自进化引擎 | P1 | HyperAgents+Evolver | 📋 | R03 | 集体进化>个体修正（RSI综述Group-Evolving） | R14 |
| GAP-011 | 任务持久化崩溃恢复 | P1 | Codex Git Worktree | 📋 增强 | R06 | Codex Git Worktree隔离副本 + Idempotency Gates | R12 |
| GAP-012 | IDE原生集成 | P1 | Claude Code+OpenCode | 📋 | R06 | — | R15 |
| GAP-013 | ACP协议支持 | P1 | OpenClaw ACP v4.2 | 📋 增强 | R06 | OpenClaw v4.2 ACP完整方案：线程绑定持久会话+标签化子Agent | R13 |
| GAP-014 | Web可视化Dashboard | P2 | Hermes Web Dashboard | 📋 | R06 | — | R16 |
| GAP-015 | Claude Code风格TUI | P2 | Claude Code | 📋 | R06 | — | R16 |
| GAP-016 | CLI/远程命令执行 | P2 | Claude Code /command | 📋 | R06 | — | R15 |
| GAP-017 | 技能市场注册表 | P2 | OpenClaw ClawHub | 📋 | R06 | ClawHub v4.1 6大注册表跨源搜索参考 | R16 |
| GAP-018 | Agent生命周期管理 | P2 | Claude Agent Teams | 📋 | R06 | Agent Teams生命周期完整闭环参考 | R14 |
| GAP-019 | **代码模块精简** | P1 | Hermes v0.15 76%精简 | 📋 新 | R09 | 76%精简标杆 → 目标≥40% | R11 |
| GAP-020 | **上下文Token优化** | P1 | Hermes Tool Search + OpenClaw Pre-Compaction | 📋 新 | R09 | Tool Search按需加载 + Pre-Compaction方案 | R13 |
| GAP-021 | **brainworm/提示注入防御** | P1 | Hermes v0.15 brainworm防御 | 📋 新 | R09 | 流量过滤+边界标记+恶意控制检测 | R12 |
| GAP-022 | **反思→落地闭环** | P2 | OpenClaw followups/ | 📋 新 | R09 | followups/YYYY-MM-DD.md+次日09:30转动作 | R14 |

## 统计摘要

| 类别 | 数量 |
|------|------|
| P0 关键缺口 | 5 |
| P1 重要缺口 | 10 |
| P2 远期缺口 | 7 |
| ✔️ 已关闭 | 1 (GAP-003) |
| 🔧 开发中 | 2 (GAP-001, GAP-004) |
| ✅ 设计完成 | 1 (GAP-005) |
| 📋 等待排期 | 14 |
| 📋 新识别(R09) | 4 (GAP-019~022) |
| **总计** | **22** |

---
*更新于 R09 · 2026-05-31*
