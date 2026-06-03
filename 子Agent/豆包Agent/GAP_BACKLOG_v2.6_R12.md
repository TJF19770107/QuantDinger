# GAP BACKLOG v2.6 — R12更新 · 缺口追踪清单

| ID | 缺口描述 | 优先级 | 对标源 | 状态 | 识别轮次 | R12注入 | 计划关闭 |
|----|----------|--------|--------|------|----------|---------|----------|
| GAP-001 | Harness工程飞轮 | P0 | Codex Traces→Evals + 3层审查模型 | 🔧 增强 | R03 | +三层审查(编排→执行→审查)模型设计完成 | R13 |
| GAP-002 | Agent间直接通信(P2P) | P0 | Hermes Kanban Swarm + Claude Teams Mailbox | 🔧 增强 | R03 | +技术选型完成：Hermes Kanban消息信箱方案 | R13 |
| GAP-003 | 自动技能生成闭环 | P0 | SkillForge v1.0 | ✔️ 关闭(R08) | R03 | — | — |
| **GAP-004** | **Skill Card标准化模板** | **P0** | **NVIDIA Verified Skills + Superpowers v5.1声明式标准** | **✔️ 关闭(R12)** | **R08** | **SkillForge v2.2→v2.3融合Superpowers声明式标准完成** | **R12** |
| GAP-005 | 向量化记忆检索落地 | P0 | OpenClaw SQLite-vec | 🔧 推进 | R07 | MemoryOS v2.2→v2.3：向量化检索落地实施中 | R12 |
| GAP-006 | 持久目标引擎（GoalStore） | P1 | Hermes /goal | 📋 | R03 | 保持 | R13 |
| GAP-007 | 任务看板系统 | P1 | Hermes Kanban Swarm v0.13 (Tenacity) | 📋 增强 | R03 | +OpenCode v2.0可视化编排参考 | R13 |
| GAP-008 | 检查点快照（SnapshotEngine） | P1 | Hermes v0.13 Checkpoints v2 真修剪 | 📋 增强 | R03 | 保持 | R13 |
| GAP-009 | 代码智能感知（LSP） | P1 | OpenCode LSP | 📋 | R03 | 保持 | R14 |
| GAP-010 | Meta自进化引擎 | P1 | FORGE广播+GEA经验池融合 | 📋 增强 | R03 | 保持 | R14 |
| GAP-011 | 任务持久化崩溃恢复 | P1 | Temporal.io + Codex Git Worktree | 📋 保持 | R06 | +Claude Agent OS生命周期管理参考 | R13 |
| GAP-012 | IDE原生集成 | P1 | Claude Code+OpenCode → 三层栈适配定位 | 📋 重定位 | R06 | 保持 | R15 |
| GAP-013 | ACP协议支持 | P1 | MCP/A2A/ACP三协议栈 | 📋 保持 | R06 | 保持 | R13 |
| GAP-014 | Web可视化Dashboard | P2 | Hermes Web Dashboard | 📋 | R06 | 保持 | R16 |
| GAP-015 | Claude Code风格TUI | P2 | OpenCode Desktop v2 + TUI | 📋 增强 | R06 | 保持 | R16 |
| GAP-016 | CLI/远程命令执行 | P2 | Claude Code /command | 📋 | R06 | 保持 | R15 |
| GAP-017 | 技能市场注册表 | P2 | OpenClaw ClawHub v4.1 + Superpowers生态 | 📋 增强 | R06 | 保持 | R16 |
| GAP-018 | Agent生命周期管理 | P2 | Claude Agent Teams | 📋 | R06 | +Claude Agent OS v1.2内核权限管理参考 | R14 |
| GAP-019 | 代码模块精简(≥40%) | P1 | Hermes v0.15 76%标杆 | ✔️ 关闭(R10) | R09 | — | — |
| GAP-020 | 上下文Token优化 | P1 | → 升级裂变为 GAP-026 + GAP-027 | 🔀 裂变 | R09 | — | — |
| GAP-021 | brainworm/提示注入防御 | P1 | Hermes v0.15 brainworm三卡口 | ✔️ 关闭(R10) | R09 | — | — |
| GAP-022 | 反思→落地闭环 | P2 | OpenClaw followups + FORGE广播 | 📋 增强 | R09 | 保持 | R14 |
| GAP-023 | Workfoz劳动力市场接入 | P2 | Workfoz AI Marketplace | 📋 | R10 | 保持 | R17 |
| GAP-024 | MCP Streamable HTTP适配 | P1 | MCP 2025-03-26规范 | 📋 | R10 | 保持 | R13 |
| GAP-025 | Agent Card发现端点 | P1 | A2A Agent Card规范 | 📋 | R10 | 保持 | R13 |
| GAP-026 | 编程式工具调用引擎 | P0 新 | Anthropic工具调用2.0 (TypeScript脚本编排多工具) | 📋 新 | R11 | 保持 | R13 |
| GAP-027 | 动态Token过滤管道 | P0 新 | Anthropic WebFetch动态过滤 + Tool Search懒加载 | 📋 新 | R11 | 保持 | R13 |
| GAP-028 | AI编程三层栈互操作适配 | P1 新 | Cursor→Claude Code→Codex 三层架构 | 📋 新 | R11 | 保持 | R15 |
| GAP-029 | Superpowers Skills标准对齐 | P1 新 | Superpowers v5.1 (191k星, 8平台) | 🔧 推进 | R11 | 随GAP-004关闭完成声明式标准融合 | R13 |
| GAP-030 | 后台子Agent非阻塞执行 | P1 新 | OpenCode v1.15.11 实验后台Agent + Hermes Kanban | 📋 新 | R11 | 保持 | R14 |
| **GAP-031** | **AI on UI跨平台自动化引擎** | **P1 新** | **AI on UI v3.0（跨平台识别97%+动态UI适配92%）** | **📋 新** | **R12** | **跨平台UI元素识别+无代码录制+动态UI自适应** | **R14** |
| **GAP-032** | **Llama本地推理部署适配** | **P2 新** | **Llama Edge + 端侧分布式推理 + 本地安全加密** | **📋 新** | **R12** | **一键本地部署+分布式推理加速+数据加密防窃取** | **R16** |
| **GAP-033** | **3D空间理解预留能力接口** | **P2 新** | **Claude 3D能力体系（多模态融合93%+空间重建误差1.2%）** | **📋 新** | **R12** | **多模态融合接口+3D场景重建管线+AR/VR交互适配** | **R17** |

## 统计摘要

| 类别 | R11 | R12 | 变化 |
|------|-----|-----|------|
| P0 关键缺口 | 5 | 4 | -1 (GAP-004关闭) |
| P1 重要缺口 | 12 | 13 | +1 (GAP-031新增) |
| P2 远期缺口 | 9 | 11 | +2 (GAP-032/033新增) |
| ✔️ 已关闭 | 3 | 4 | +1 (GAP-004) |
| 🔧 开发中 | 2 | 3 | +1 (GAP-005推进) |
| ✅ 设计完成 | 1 | 0 | -1 (GAP-005→推进中) |
| 📋 等待排期 | 17 | 16 | -1 |
| 📋 新识别(R12) | — | 3 | GAP-031~033 |
| **总计** | **30** | **33** | **+3** |

## 重点行动

| 优先级 | ID | 行动 | 截止 |
|--------|----|------|------|
| 🔴 P0 | GAP-005 | MemoryOS向量化检索全功能落地验证 | R12收尾 |
| 🔴 P0 | GAP-001 | Harness工程飞轮 v0.1代码实现 | R13 |
| 🔴 P0 | GAP-002 | P2P通信协议落地（Hermes Kanban消息信箱） | R13 |
| 🔴 P0 | GAP-026 | 编程式工具调用引擎技术方案设计 | R13 |
| 🔴 P0 | GAP-027 | 动态Token过滤管道架构设计 | R13 |
| 🟡 P1 | GAP-031 | AI on UI自动化引擎 v0.1原型 | R14 |
| 🟡 P1 | GAP-029 | Superpowers Skills标准对齐实施 | R13 |
| 🟡 P1 | GAP-007 | 任务看板系统（融合OpenCode编排参考） | R13 |

---
*更新于 R12 · 2026-05-31*
