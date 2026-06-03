# 阶段二-B：技术对标摘要

> 生成时间：2026-06-02 | 对标路径：E:\龙虾AI主控中心\我的AI分身\技能库\
> 共读取 10 篇技能文件，覆盖 6 个对标维度

---

## 1. Codex / 编码Agent

### 1.1 Codex + 飞书 CLI 自动化技能手册 v1.2（主文件 · 9.1 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | 通过 Codex CLI 接入飞书全生态（文档/Base/日历/消息/任务/邮箱/知识库/会议纪要/搜索 共11大业务域） |
| **关键框架** | 四步接入流程（安装CLI → 配置应用 → 登录授权 → 验证）→ 5 大自动化 SOP（AI调研→文档、批量数据→Base、群消息总结、日程管理、运营素材生成） |
| **核心方法论** | 最小权限原则配置、Codex Triggers 事件驱动、Developer OS 集成模式（Claude.md → Skills → Subagents → 飞书CLI插件 → 全链路自动化） |
| **安全设计** | App Secret轮换、敏感操作二次确认、人工审核节点 |
| **R28新增** | Codex Triggers + Codex Mobile Appshots → 飞书消息推送联动 |

### 1.2 龙虾-Codex 可观测性生命周期协议 v1.0（辅文件 · 4.6 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | 11事件模型覆盖Agent完整生命周期（5观测事件 + 6拦截事件） |
| **关键框架** | SubagentStart/Stop → 成本追踪；PreToolUse → 参数审查/权限控制；AsyncApproval → 审计追踪 |
| **核心方法论** | 插件化架构（成本追踪插件/治理门禁插件/性能监控插件），观测事件异步不阻塞Agent循环，拦截事件可修改行为或阻止操作 |
| **适配方案** | 豆包Agent 5子Agent启动/停止/工具调用均发布标准事件 → 事件总线 + SafeGuard安全层 |

---

## 2. Hermes / SWARM / 多Agent调度

### 2.1 龙虾-HermesSwarm 多Agent协作协议 v1.0（主文件 · 4.2 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | SQLite持久化任务看板 + 一键Swarm工作流 + DAG拓扑自动分解 + 多Worker并行 + 独立校验/合成节点 |
| **关键框架** | Kanban Swarm拓扑：Orchestrator → Workers(A/B/C并行) → Gate → Verifier → Gate → Synthesizer → Shared Blackboard |
| **核心方法论** | ①CAS并发控制保证原子认领 ②Agent画像描述精准任务匹配 ③Per-Task模型覆盖（简单任务→本地模型，复杂算法→Claude Opus/Sonnet） ④任务状态持久化跨会话 ⑤Workspace隔离（Scratch/Dir/Worktree三级） |
| **状态机** | triage → todo → in_progress → review → done（含failed/rejected/retry分支） |
| **一次性vs持久化** | Kanban持久化：不阻塞主进程、支持崩溃恢复、人类中途介入/unblock、永久审计记录、跨角色接力、跨会话持久化 |

### 2.2 龙虾_Hermes 中枢调度模版 v1.0（辅文件 · 2.4 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | 1个Orchestrator管理无限Worker Agent，0人类干预的军团指挥模式 |
| **关键框架** | delegate_task工具（agent_name/task/memory_ids/inherit_agent_id参数）→ 子Agent独立上下文/终端会话/工具集/迭代预算 → 仅回报结构化摘要 |
| **核心方法论** | 三种协作模式：Orchestrator+Worker（复杂多步骤）/ Peer-to-Peer（多方共识）/ Hierarchical（多层嵌套） |
| **关键约束** | 子Agent完整历史不传主Agent、无依赖子任务必须并行派发、每轮并行上限5个 |

---

## 3. Obsidian / 知识库联动

> 无直接命中的 Obsidian 文件，以"知识库"关键词命中 2 篇，取内容更丰富的。

### 3.1 龙虾-知识库三层架构协议 v1.0（2.8 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | 多Agent协作环境下统一知识库体系，确保所有Agent在同一规则下运作 |
| **关键框架** | L1项目宪法（技术选型/架构决策/不可变原则）→ L2领域规则（模块边界/接口契约/命名规范）→ L3细节对齐（接口字段/参数格式/返回值） |
| **核心方法论** | ①三级读写权限矩阵（Host可读写全层，Worker只读L1-L2，L3可提交候选更新） ②片段级引用格式（`l1/current#tech-stack`）节省Token ③知识库裁决流程：Worker提案 → Knowledge Keeper初审 → Host终审 |
| **与现有协议关系** | MemoryOS v2.0的结构化扩展 + 多Agent协同看板互补 + 长时域Goal追踪对齐 |

---

## 4. AI on UI / 界面自动化

### 4.1 龙虾-三层GUI感知行动协议 v1.0（3.1 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | 感知-决策-执行三层架构，多模态UI解析（OCR+CV+Accessibility API），LLM推理生成操作指令，沙箱化安全执行 |
| **关键框架** | 感知层（结构化界面状态）→ 决策层（规则引擎+LLM推理→操作指令序列）→ 执行层（键鼠模拟/API调用→操作结果+状态验证） |
| **核心方法论** | ①元素定位优先级：文本匹配 > 布局路径 > 图像匹配 ②Cloud+Screenshot vs Local+Accessibility API两条路线对比（隐私/速度/可靠性/成本权衡） ③Codex Appshots融合方案（窗口文本+视觉） |
| **安全设计** | 沙箱隔离、敏感信息脱敏、全量审计日志、高危操作人工闸门、每步操作后验证预期状态 |
| **反模式** | 禁止无许可自动执行高影响操作、禁止仅靠事后审计无预览机制、禁止混淆模型置信度与业务规则 |

---

## 5. Claude / Agent OS

### 5.1 龙虾-Claude Opus4.8 编码增强协议 v1.0（主文件 · 17.0 KB · 最大文件）

| 维度 | 内容 |
|------|------|
| **核心能力** | 反思式编码循环 + Critic Model自评分 + 长链路推理（100+步骤） + SWE-bench Verified 87.6%对标 |
| **关键框架** | ①反思式编码引擎：生成→Critic评估→反馈注入→重生成（最多3轮，温度递进0.3→0.5→0.7） ②Critic Model五维评估：正确性(40%)/可读性(15%)/性能(20%)/安全性(15%)/可维护性(10%)，综合评分≥80通过 ③长链路推理引擎：200K上下文窗口、动态压缩（保留关键决策+错误信息）、检查点恢复 |
| **核心方法论** | 质量阈值门控（80分）、指数退避重试、工具调用成功率增强（预验证→智能重试→降级链） |
| **依赖链** | 协议34(动态工作流分支) + 协议60(反思自纠正) + 协议27(DurableExecution) → 协议69(本协议) |
| **目标指标** | 编码能力 94→96(+2)、工具调用成功率 93%→95%(+2%)、推理步骤 50→100+(+100%) |

### 5.2 龙虾_Claude工具对标矩阵 v1.0（辅文件 · 4.4 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | Claude Code 25个内置工具与豆包Agent的逐项对标差距分析 |
| **关键框架** | 五层架构：Model(LLM决策) → CLI Harness(编排) → Built-in Tools(25) → Skills(8个提示词包) → MCP Servers(外部进程) |
| **核心方法论** | "Model眼中只有Tools"——无论Bash/Skill/MCP对LLM都是扁平function call，Harness负责路由 |
| **补齐状态** | ✅已具备14个 / 🔧P0待补9个（Agent/Task×5/PlanMode）/ ⚠️P1待补4个（Cron管理/MCP/ScheduleWakeup）/ ❌P2待补2个（NotebookEdit/EnterWorktree） |

---

## 6. Llama / 本地推理 / 本地部署

### 6.1 龙虾-分层本地推理路由协议 v1.0（2.3 KB）

| 维度 | 内容 |
|------|------|
| **核心能力** | 根据并发量/延迟/隐私需求，自动路由到最优本地推理方案（Ollama/vLLM/llama.cpp） |
| **关键框架** | 决策矩阵：1-4并发→Ollama(62tok/s)，5+并发→vLLM(920tok/s，6.6x)，边缘部署→llama.cpp(GGUF量化)，多GPU→vLLM Tensor Parallelism |
| **核心方法论** | 优化叠加链：Q4_K_M量化(4.5x) → Flash Attention-3(1.5-2x) → Speculative Decoding(2-3x) → EAGLE-3(累计14.5x)，RTX4090上Llama 3.3 70B从4tok/s提升至41-58tok/s |
| **关键基准** | TTFT首Token延迟：vLLM 10.7ms vs Ollama 45ms(4.2x)，Continuous Batching 23x提升，PagedAttention 2-4x内存效率 |
| **最优配置栈** | llama-server + Q4_K_M + Speculative Decoding(draft=8) + Flash Attention + n-gpu-layers=99 |

---

## 7. 跨维度关键发现

| 发现 | 详情 |
|------|------|
| **Claude Opus 4.8 协议最重** | 17.0KB，包含完整Python代码实现、Critic Model评估引擎、长链路推理和SWE-bench验证 |
| **Codex生命周期协议最适配** | 11事件模型可直接映射到豆包Agent 5子Agent的事件总线 |
| **Hermes Kanban 是调度核心** | SQLite持久化看板 + DAG自动分解 + Worker画像匹配 = 多Agent协作最佳实践 |
| **三层架构模式贯穿** | 知识库(L1/L2/L3) + GUI(感知/决策/执行) + 推理路由(Ollama/vLLM/llama.cpp) 均采用三层分层设计 |
| **本地推理优化链成熟** | 从基础4tok/s到58tok/s的14.5x加速链完整可落地，覆盖量化/注意力/推测解码全栈 |
| **Obsidian 直接对标缺失** | 技能库中无 Obsidian 相关文件，知识库联动通过"知识库三层架构"协议间接覆盖，但缺乏Obsidian工具链的具体集成方案 |
