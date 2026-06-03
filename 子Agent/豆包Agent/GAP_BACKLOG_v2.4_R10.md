# GAP BACKLOG v2.4 — R10更新 · 缺口追踪清单

| ID | 缺口描述 | 优先级 | 对标源 | 状态 | 识别轮次 | R10注入 | 计划关闭 |
|----|----------|--------|--------|------|----------|---------|----------|
| GAP-001 | Harness工程飞轮 | P0 | Codex Traces→Evals | 🔧 启动 | R03 | 保持 | R12 |
| GAP-002 | Agent间直接通信(P2P) | P0 | Hermes Kanban Swarm + Claude Teams Mailbox | 📋 增强 | R03 | Hermes Swarm(协调者+工作者+校验+合成)+Claude P2P消息注入 | R12 |
| GAP-003 | 自动技能生成闭环 | P0 | SkillForge v1.0 | ✔️ 关闭(R08) | R03 | — | — |
| GAP-004 | Skill Card标准化模板 | P0 | NVIDIA Verified Skills(编目→扫描→评估→签名) | 🔧 启动 | R08 | NVIDIA四步验证流程+agentskill.io规范完整注入 | R11 |
| GAP-005 | 向量化记忆检索落地 | P0 | OpenClaw SQLite-vec | ✅ 设计完成 | R07 | 保持 | R10 |
| GAP-006 | 持久目标引擎（GoalStore） | P1 | Hermes /goal | 📋 | R03 | 保持 | R12 |
| GAP-007 | 任务看板系统 | P1 | Hermes Kanban Swarm v0.15 | 📋 增强 | R03 | Kanban Swarm完整方案：协调者+并行工作者+独立校验+合成+单任务模型覆盖+定时启动 | R13 |
| GAP-008 | 检查点快照（SnapshotEngine） | P1 | Temporal.io Durable Execution | 📋 增强 | R03 | Temporal Replay 2026：自动状态捕获+断点恢复+无进度丢失 | R13 |
| GAP-009 | 代码智能感知（LSP） | P1 | OpenCode LSP | 📋 | R03 | 保持 | R14 |
| GAP-010 | Meta自进化引擎 | P1 | FORGE广播+GEA经验池融合 | 📋 增强 | R03 | FORGE冠军广播+GEA群体级元学习+毕业冻结机制 | R14 |
| GAP-011 | 任务持久化崩溃恢复 | P1 | Temporal.io + Codex Git Worktree | 📋 增强 | R06 | Temporal Durable Execution+Idempotency Gates双保险 | R12 |
| GAP-012 | IDE原生集成 | P1 | Claude Code+OpenCode | 📋 | R06 | 保持 | R15 |
| GAP-013 | ACP协议支持 | P1 | MCP/A2A/ACP三协议栈 | 📋 增强 | R06 | 三协议栈架构设计：L1工具层(MCP)+L2协调层(A2A)+L3身份层(OAuth2.1) | R13 |
| GAP-014 | Web可视化Dashboard | P2 | Hermes Web Dashboard | 📋 | R06 | 保持 | R16 |
| GAP-015 | Claude Code风格TUI | P2 | Claude Code | 📋 | R06 | 保持 | R16 |
| GAP-016 | CLI/远程命令执行 | P2 | Claude Code /command | 📋 | R06 | 保持 | R15 |
| GAP-017 | 技能市场注册表 | P2 | OpenClaw ClawHub v4.1 | 📋 | R06 | 保持 | R16 |
| GAP-018 | Agent生命周期管理 | P2 | Claude Agent Teams | 📋 | R06 | 保持 | R14 |
| GAP-019 | 代码模块精简(≥40%) | P1 | Hermes v0.15 76%标杆 | ✔️ 关闭(R10) | R09 | 76%可行性已验证，豆包定标≥40% | — |
| GAP-020 | 上下文Token优化 | P1 | Hermes Tool Search + OpenClaw Pre-Compaction | 📋 | R09 | 保持 | R13 |
| GAP-021 | brainworm/提示注入防御 | P1 | Hermes v0.15 brainworm三卡口 | ✔️ 关闭(R10) | R09 | 三卡口：流量过滤+边界标记+恶意控制检测，已注入能力#30 | — |
| GAP-022 | 反思→落地闭环 | P2 | OpenClaw followups + FORGE广播 | 📋 增强 | R09 | FORGE外循环定时广播+冠军选举机制注入 | R14 |
| GAP-023 | Workfoz劳动力市场接入 | P2 新 | Workfoz AI Marketplace | 📋 新 | R10 | 全球首个AI劳动力市场，OpenClaw skill可下载，待评估接入可行性 | R17 |
| GAP-024 | MCP Streamable HTTP适配 | P1 新 | MCP 2025-03-26规范 | 📋 新 | R10 | 单端点/mcp无状态部署，支持K8s/Serverless/Cloudflare Workers | R13 |
| GAP-025 | Agent Card发现端点 | P1 新 | A2A Agent Card规范 | 📋 新 | R10 | 身份声明+能力声明+端点发现标准化 | R13 |

## 统计摘要

| 类别 | 数量 |
|------|------|
| P0 关键缺口 | 4 |
| P1 重要缺口 | 10 |
| P2 远期缺口 | 9 |
| ✔️ 已关闭 | 3 (GAP-003, GAP-019, GAP-021) |
| 🔧 开发中 | 2 (GAP-001, GAP-004) |
| ✅ 设计完成 | 1 (GAP-005) |
| 📋 等待排期 | 14 |
| 📋 新识别(R10) | 3 (GAP-023~025) |
| **总计** | **25** |

---
*更新于 R10 · 2026-05-31*