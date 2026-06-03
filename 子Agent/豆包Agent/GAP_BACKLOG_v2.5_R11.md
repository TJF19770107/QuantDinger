# GAP BACKLOG v2.5 — R11更新 · 缺口追踪清单

| ID | 缺口描述 | 优先级 | 对标源 | 状态 | 识别轮次 | R11注入 | 计划关闭 |
|----|----------|--------|--------|------|----------|---------|----------|
| GAP-001 | Harness工程飞轮 | P0 | Codex Traces→Evals + 3层审查模型 | 🔧 增强 | R03 | +3层审查(编排→执行→审查)分层飞轮 | R12 |
| GAP-002 | Agent间直接通信(P2P) | P0 | Hermes Kanban Swarm + Claude Teams Mailbox | 📋 保持 | R03 | 保持 | R12 |
| GAP-003 | 自动技能生成闭环 | P0 | SkillForge v1.0 | ✔️ 关闭(R08) | R03 | — | — |
| GAP-004 | Skill Card标准化模板 | P0 | NVIDIA Verified Skills + Superpowers v5.1声明式标准 | 🔧 增强 | R08 | +Superpowers 8平台通用Skill声明式标准 + MIT开源生态 | 🎯 R11 |
| GAP-005 | 向量化记忆检索落地 | P0 | OpenClaw SQLite-vec | ✅ 设计完成 | R07 | 保持 | R12 |
| GAP-006 | 持久目标引擎（GoalStore） | P1 | Hermes /goal | 📋 | R03 | 保持 | R12 |
| GAP-007 | 任务看板系统 | P1 | Hermes Kanban Swarm v0.13 (Tenacity) | 📋 增强 | R03 | +心跳回收 + 僵尸检测 + 单任务模型覆盖 + 幻觉恢复 | R13 |
| GAP-008 | 检查点快照（SnapshotEngine） | P1 | Hermes v0.13 Checkpoints v2 真修剪 | 📋 增强 | R03 | +Checkpoints v2真修剪(非标记) + Gateway断点自动恢复 | R13 |
| GAP-009 | 代码智能感知（LSP） | P1 | OpenCode LSP | 📋 | R03 | 保持 | R14 |
| GAP-010 | Meta自进化引擎 | P1 | FORGE广播+GEA经验池融合 | 📋 增强 | R03 | 保持R10注入 | R14 |
| GAP-011 | 任务持久化崩溃恢复 | P1 | Temporal.io + Codex Git Worktree | 📋 保持 | R06 | 保持 | R12 |
| GAP-012 | IDE原生集成 | P1 | Claude Code+OpenCode → 三层栈适配定位 | 📋 重定位 | R06 | **重定位：适配三层栈(编排→执行→审查)，放弃自建IDE** | R15 |
| GAP-013 | ACP协议支持 | P1 | MCP/A2A/ACP三协议栈 | 📋 保持 | R06 | 保持 | R13 |
| GAP-014 | Web可视化Dashboard | P2 | Hermes Web Dashboard | 📋 | R06 | 保持 | R16 |
| GAP-015 | Claude Code风格TUI | P2 | OpenCode Desktop v2 + TUI | 📋 增强 | R06 | +OpenCode v1.15 Desktop v2重设计(首页/标题栏/状态弹窗) | R16 |
| GAP-016 | CLI/远程命令执行 | P2 | Claude Code /command | 📋 | R06 | 保持 | R15 |
| GAP-017 | 技能市场注册表 | P2 | OpenClaw ClawHub v4.1 + Superpowers生态 | 📋 增强 | R06 | +Superpowers 8平台生态参考 | R16 |
| GAP-018 | Agent生命周期管理 | P2 | Claude Agent Teams | 📋 | R06 | 保持 | R14 |
| GAP-019 | 代码模块精简(≥40%) | P1 | Hermes v0.15 76%标杆 | ✔️ 关闭(R10) | R09 | — | — |
| GAP-020 | 上下文Token优化 | P1 | → 升级裂变为 GAP-026 + GAP-027 | 🔀 裂变 | R09 | → GAP-026(编程式调用) + GAP-027(动态过滤) | — |
| GAP-021 | brainworm/提示注入防御 | P1 | Hermes v0.15 brainworm三卡口 | ✔️ 关闭(R10) | R09 | — | — |
| GAP-022 | 反思→落地闭环 | P2 | OpenClaw followups + FORGE广播 | 📋 增强 | R09 | 保持 | R14 |
| GAP-023 | Workfoz劳动力市场接入 | P2 | Workfoz AI Marketplace | 📋 | R10 | 保持 | R17 |
| GAP-024 | MCP Streamable HTTP适配 | P1 | MCP 2025-03-26规范 | 📋 | R10 | 保持 | R13 |
| GAP-025 | Agent Card发现端点 | P1 | A2A Agent Card规范 | 📋 | R10 | 保持 | R13 |
| **GAP-026** | **编程式工具调用引擎** | **P0 新** | **Anthropic工具调用2.0 (TypeScript脚本编排多工具)** | **📋 新** | **R11** | 编程式调用→减少30-50%往返→沙箱执行环境→allowed_callers白名单 | **R13** |
| **GAP-027** | **动态Token过滤管道** | **P0 新** | **Anthropic WebFetch动态过滤 + Tool Search懒加载** | **📋 新** | **R11** | WebFetch中间层过滤(24%↓)+Tool Search懒加载(80%↓上下文) | **R13** |
| **GAP-028** | **AI编程三层栈互操作适配** | **P1 新** | **Cursor→Claude Code→Codex 三层架构** | **📋 新** | **R11** | 编排层适配器+执行层Skills对齐+审查层接口 | **R15** |
| **GAP-029** | **Superpowers Skills标准对齐** | **P1 新** | **Superpowers v5.1 (191k星, 8平台)** | **📋 新** | **R11** | Skills声明式描述→brainstorming→plans→子Agent开发→TDD | **R13** |
| **GAP-030** | **后台子Agent非阻塞执行** | **P1 新** | **OpenCode v1.15.11 实验后台Agent + Hermes Kanban** | **📋 新** | **R11** | 事件推送(无轮询)+后台任务队列+心跳监控+僵尸回收 | **R14** |

## 统计摘要

| 类别 | R10 | R11 | 变化 |
|------|-----|-----|------|
| P0 关键缺口 | 4 | 5 | +1 (GAP-020裂变净增, GAP-026/027替换) |
| P1 重要缺口 | 10 | 12 | +2 (GAP-028/029/030新增, GAP-020裂变移除) |
| P2 远期缺口 | 9 | 9 | — |
| ✔️ 已关闭 | 3 | 3 | — |
| 🔧 开发中 | 2 | 2 | — |
| ✅ 设计完成 | 1 | 1 | — |
| 📋 等待排期 | 14 | 17 | +3 |
| 📋 新识别(R11) | — | 5 | GAP-026~030 |
| 🔀 裂变(R11) | — | 1 | GAP-020→GAP-026+GAP-027 |
| **总计** | **25** | **30** | **+5** |

## 重点行动

| 优先级 | ID | 行动 | 截止 |
|--------|----|------|------|
| 🔴 P0 | GAP-004 | 完成Skill Card标准化 v1.0 (融合NVIDIA+Superpowers标准) | R11收尾 |
| 🔴 P0 | GAP-026 | 编程式工具调用引擎技术方案设计 | R13 |
| 🔴 P0 | GAP-027 | 动态Token过滤管道架构设计 | R13 |
| 🔴 P0 | GAP-001 | Harness工程飞轮 v0.1实施框架 | R12 |
| 🔴 P0 | GAP-002 | P2P通信协议选型与方案 | R12 |
| 🟡 P1 | GAP-029 | Superpowers Skills标准对齐评估及迁移方案 | R13 |
| 🟡 P1 | GAP-028 | AI编程三层栈适配分析报告 | R15 |

---
*更新于 R11 · 2026-05-31*
