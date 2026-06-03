# GAP BACKLOG v3.0 — R15更新 · 缺口追踪清单

| ID | 缺口描述 | 优先级 | 对标源 | 状态 | 识别轮次 | R15变更 | 计划关闭 |
|----|----------|--------|--------|------|----------|---------|----------|
| GAP-001 | Harness工程飞轮 | P0 | Codex Traces→Evals + 3层审查模型 | 📐 DESIGNED | R03 | R15: L1/L2/L3三层评估方案 | R16 |
| GAP-002 | Agent间直接通信(P2P) | P0 | Hermes Kanban Swarm + Claude Teams Mailbox | 📋 | R03 | 保持 | R16 |
| GAP-003 | 自动技能生成闭环 | P0 | SkillForge v1.0 | ✔️ 关闭(R08) | R03 | — | — |
| GAP-004 | Skill Card标准化模板 | P0 | NVIDIA Verified Skills + Superpowers v5.1 | ✔️ 关闭(R12) | R08 | — | — |
| GAP-005 | 向量化记忆检索落地 | P0 | OpenClaw SQLite-vec / Mem0 v3.0 混合检索 | 📐 DESIGNED | R07 | R15: Mem0 v3.0 语义+BM25+实体方案 | R16 |
| GAP-006 | 持久目标引擎（GoalStore） | P1 | Hermes /goal | 📋 | R03 | 保持 | R16 |
| GAP-007 | 任务看板系统 | P1 | Hermes Kanban Swarm v0.13 | 📋 | R03 | 保持 | R16 |
| GAP-008 | 检查点快照（SnapshotEngine） | P1 | Hermes Checkpoints v2 + JumpCloud State Rollback | 📋 增强 | R03 | R14: State Rollback机制注入 | R16 |
| GAP-009 | 代码智能感知（LSP） | P1 | OpenCode LSP | 📋 | R03 | 保持 | R17 |
| GAP-010 | Meta自进化引擎 | P1 | FORGE广播+GEA经验池融合 | 📋 | R03 | 保持 | R17 |
| GAP-011 | 任务持久化崩溃恢复 | P1 | Temporal.io + Codex Git Worktree | 📋 | R06 | 保持 | R16 |
| GAP-012 | IDE原生集成 | P1 | Claude Code+OpenCode | 📋 | R06 | 保持 | R18 |
| GAP-013 | ACP协议支持 | P1 | MCP/A2A/ACP三协议栈 | 📋 | R06 | 保持 | R16 |
| GAP-014 | Web可视化Dashboard | P2 | Hermes Web Dashboard | 📋 | R06 | 保持 | R19 |
| GAP-015 | Claude Code风格TUI | P2 | OpenCode Desktop v2 + TUI | 📋 | R06 | 保持 | R19 |
| GAP-016 | CLI/远程命令执行 | P2 | Claude Code /command | 📋 | R06 | 保持 | R18 |
| GAP-017 | 技能市场注册表 | P2 | OpenClaw ClawHub v4.1 | 📋 | R06 | 保持 | R19 |
| GAP-018 | Agent生命周期管理 | P2 | Claude Agent Teams | 📋 | R06 | 保持 | R17 |
| GAP-019 | 代码模块精简(≥40%) | P1 | Hermes v0.15 76%标杆 | ✔️ 关闭(R10) | R09 | — | — |
| GAP-020 | 上下文Token优化 | P1 | 裂变为 GAP-026 + GAP-027 | 🔀 裂变 | R09 | — | — |
| GAP-021 | brainworm/提示注入防御 | P1 | Hermes v0.15 brainworm三卡口 | ✔️ 关闭(R10) | R09 | — | — |
| GAP-022 | 反思→落地闭环 | P2 | OpenClaw followups + FORGE广播 | 📋 | R09 | 保持 | R17 |
| GAP-023 | Workfoz劳动力市场接入 | P2 | Workfoz AI Marketplace | 📋 | R10 | 保持 | R20 |
| GAP-024 | MCP Streamable HTTP适配 | P1 | MCP 2025-03-26规范 | 📋 | R10 | 保持 | R16 |
| GAP-025 | Agent Card发现端点 | P1 | A2A Agent Card规范 | 📋 | R10 | 保持 | R16 |
| GAP-026 | 编程式工具调用引擎 | P0 | Anthropic工具调用2.0 | 📋 | R11 | 保持 | R16 |
| GAP-027 | 动态Token过滤管道 | P0 | Anthropic WebFetch动态过滤 | 📋 | R11 | 保持 | R16 |
| GAP-028 | AI编程三层栈互操作适配 | P1 | Cursor→Claude Code→Codex | 📋 | R11 | 保持 | R18 |
| GAP-029 | Superpowers Skills标准对齐 | P1 | Superpowers v5.1 | 📋 | R11 | 保持 | R16 |
| GAP-030 | 后台子Agent非阻塞执行 | P1 | OpenCode v1.15.11 + Hermes Kanban | 📋 | R11 | 保持 | R17 |
| GAP-031 | AI on UI跨平台自动化引擎 | P1 | AI on UI v3.0 | 📋 | R12 | 保持 | R17 |
| GAP-032 | Llama本地推理部署适配 | P2 | Llama Edge + 端侧分布式推理 | 📋 | R12 | 保持 | R19 |
| GAP-033 | 3D空间理解预留能力接口 | P2 | Claude 3D能力体系 | 📋 | R12 | 保持 | R20 |
| **GAP-034** | **推理引擎代码实现** | **P0** | **Claude推理五层骨架** | **✔️ 关闭(R13)** | **R13** | **800行增强引擎完成** | **R13** |
| **GAP-035** | **可视化工作流看板** | **P0** | **Hermes Dashboard** | **✔️ 关闭(R13)** | **R13** | **530行HTML暗色看板完成** | **R13** |
| **GAP-036** | **技能自动萃取引擎** | **P0** | **SkillForge萃取管道** | **✔️ 关闭(R13)** | **R13** | **730行四阶段管道完成** | **R13** |
| **GAP-037** | **全域集成编排引擎** | **P0** | **推理→编排→进化流水线** | **✔️ 关闭(R13)** | **R13** | **440行编排引擎完成** | **R13** |
| **GAP-038** | **自进化能力注册升级** | **P0** | **SICA自进化协调器** | **✔️ 关闭(R13)** | **R13** | **688行六阶段闭环完成** | **R13** |
| **GAP-039** | **AutoFileScanner升级v2.0** | **P1** | **FileEcho增量索引+AI标注** | **✔️ 关闭(R14)** | **R14** | **v2.0方案完成：增量索引+7AI标注+watchdog** | **R14** |
| **GAP-040** | **SkillForge缺少反馈闭环** | **P1** | **阿里云SkillForge三阶段闭环** | **✔️ 关闭(R14)** | **R14** | **v4.0方案完成：失败分析→诊断→优化闭环** | **R14** |
| **GAP-041** | **DesktopController无原生UI感知** | **P1** | **Windows UI Automation** | **✔️ 关闭(R14)** | **R14** | **v3.0方案完成：控件树+多模型协作** | **R14** |
| **GAP-042** | **AutoWake缺少任务记忆树** | **P1** | **TMT+TRIM+Zep时间KG** | **✔️ 关闭(R14)** | **R14** | **v3.0方案完成：TMT+TRIM+8种协调模式** | **R14** |
| **GAP-043** | **MemoryOS无智能压缩** | **P1** | **Mem0压缩引擎+Zep KG** | **✔️ 关闭(R14)** | **R14** | **v3.0方案完成：Mem0压缩+向量检索+KG** | **R14** |
| **GAP-044** | **SafeGuard无State Rollback** | **P1** | **JumpCloud State Rollback** | **✔️ 关闭(R14)** | **R14** | **v4.0方案完成：checkpoint序列化+HOTL** | **R14** |
| **GAP-045** | **多模型协作架构未落地** | **P1 新** | **MIT DisCIPL + NVIDIA SLM Survey** | **📐 DESIGNED** | **R14** | **R15: 三级路由架构+5类协作模式方案完成** | **R16** |
| **GAP-046** | **时间知识图谱未实现** | **P1 新** | **Zep arxiv 2501.13956 + Graphiti** | **📐 DESIGNED** | **R14** | **R15: Zep三层图架构方案完成** | **R16** |
| GAP-047 | 技能SkillsBench基准测试缺失 | P2 新 | 阿里云SkillForge基准 | 📋 新 | R14 | 保持 | R19 |
| GAP-048 | 沙箱虚拟桌面未实现 | P2 新 | Windows CU沙箱标准 | 📋 新 | R14 | 保持 | R19 |

## 统计摘要

| 类别 | R14 | R15 | 变化 |
|------|-----|-----|------|
| P0 关键缺口 | 0 | 0 | — |
| P0 DESIGNED | 0 | 2 | +2 (GAP-001/005) |
| P1 重要缺口 | 17 | 17 | — |
| P1 DESIGNED | 0 | 2 | +2 (GAP-045/046) |
| P2 远期缺口 | 13 | 13 | — |
| ✔️ 已关闭 | 16 | 16 | — |
| 📐 方案完成 | 0 | 4 | +4 |
| 📋 等待排期 | 21 | 17 | -4 |
| **总计** | **37** | **37** | — |

## R15重点行动 (全部完成)

| 优先级 | ID | 行动 | 状态 |
|--------|----|------|------|
| 🟢 P0 | GAP-001 | Harness工程飞轮：L1/L2/L3三层评估方案 | 📐 DESIGNED |
| 🟢 P0 | GAP-005 | MemoryOS向量检索：Mem0 v3.0混合检索方案 | 📐 DESIGNED |
| 🟢 P1 | GAP-045 | 多模型协作：三级路由+5类协作模式方案 | 📐 DESIGNED |
| 🟢 P1 | GAP-046 | 时间知识图谱：Zep三层图架构方案 | 📐 DESIGNED |

## R16 计划行动

| 优先级 | ID | 行动 | 预期产出 |
|--------|----|------|---------|
| P0 | GAP-005 | Mem0 v3.0 + Qdrant 部署 | 向量数据库上线 |
| P0 | GAP-001 | L1规则引擎100+规则 | 快速门禁投产 |
| P1 | GAP-045 | Router模块编码 | 置信度评分+任务分类器 |
| P1 | GAP-046 | Graphiti引擎本地部署 | 会话KG建模 |

---
*更新于 R15 · 2026-05-31 15:45*