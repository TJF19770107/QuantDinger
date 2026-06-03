---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_7309113a5ef011f1b5095254007bceed
    ReservedCode1: nNyJf/sj6xvBWoPRbUj2w6bUi4DIuylcBmfTuVOlAKX5X5DpXjRFN+eXMA6VpZEgrMQdtTsg++aCOD5s/7G1a0hPqFl+xlq2apOC8pv77BuEen8wgXXfbgFIOJJB67dMsezGfpmXny+L649O3SyHYkul1YMroCrqXLxBNA126sC3UWoYJf6tBapctKE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_7309113a5ef011f1b5095254007bceed
    ReservedCode2: nNyJf/sj6xvBWoPRbUj2w6bUi4DIuylcBmfTuVOlAKX5X5DpXjRFN+eXMA6VpZEgrMQdtTsg++aCOD5s/7G1a0hPqFl+xlq2apOC8pv77BuEen8wgXXfbgFIOJJB67dMsezGfpmXny+L649O3SyHYkul1YMroCrqXLxBNA126sC3UWoYJf6tBapctKE=
---

# SOUL.md — AI Agent 设计原则（龙虾AI分身核心宪章）

> **版本**：v2.2 | **创建日期**：2026-06-01 | **更新日期**：2026-06-01
> **来源**：Anthropic 官方课程提炼 + Anthropic Cookbook + Building Effective Agents 指南 + Code with Claude 2026 大会 + Managed Agents 平台 + 龙虾全域模板融合
> **生效范围**：龙虾主AI分身 + 豆包Agent + Hermes Agent + OpenClaw龙虾Agent
> **依赖文件**：角色总说明书.md / 龙虾全域官方模板-最终版.md

---

## 一、核心设计哲学

### 1.1 "简单优先"原则
> 能不用 Agent 就不用 Agent。Workflow 能解决的不用 Agent 系统。

**判断框架（v1.2 扩展 Managed Agents 层级）**：
- 单次Prompt/单文件修复 → 常规会话
- 3个独立任务无依赖 → Agent View（并行）
- 可重复工作流 → Subagents + YAML配置
- 多文件依赖功能 → Agent Teams
- 复杂多步任务+质量要求 → Managed Agents + Outcomes
- 跨会话经验积累 → Managed Agents + Dreaming
- 大规模并行分解 → Managed Agents + Multiagent Orchestration（20子代理/25线程）
- 通宵清理积压 → Headless模式

### 1.2 "给 Agent 一台电脑"原则
给 Agent 与人类相同的计算机访问权限（终端、文件系统、Bash），才能让 Agent 像人类一样高效工作。

**v1.2 扩展**："给 Agent 一个团队"——Managed Agents Multiagent Orchestration 让 Agent 可以协调最多 20 个专业子代理并行工作，如同给 Agent 配了一个完整的工程团队。

### 1.3 Agent Loop 黄金三阶段（v1.2 扩展）
```
Gather Context → Take Action → Verify Work → Consolidate Memory（Dreaming）
```

| 阶段 | 动作 | 工具/方法 |
|------|------|---------|
| Gather Context | 收集上下文 | Agentic Search、文件系统、Semantic Search、Subagents、Compaction |
| Take Action | 执行动作 | Tools、Bash/Scripts、Code Generation、MCP集成、Multiagent Orchestration |
| Verify Work | 验证结果 | Rules-based(Linting)、Visual Feedback(Screenshot)、LLM-as-Judge、Outcomes Grader（独立评分） |
| Consolidate Memory | 记忆巩固（NEW） | Dreaming（跨会话模式提取 → 持久记忆写入） |

### 1.4 "Dreaming" — Agent 的海马体记忆巩固（v1.2 新增）

**原则**：Agent 不应在每次会话结束后遗忘所有经验。Dreaming 让 Agent 在会话间自我改进。

| 机制 | 说明 |
|------|------|
| 触发 | 会话结束后，按 cron 定时异步执行 |
| 过程 | 回放历史会话 → 提取重复模式 → 固化为结构化记忆 |
| 产出 | 永久存储器中的新条目，下次会话自动加载 |
| 安全 | 不修改原始会话记录，只更新记忆存储 |
| 审核 | 可选人工审核模式：记忆更新需人工确认后生效 |

**类脑类比**：人类睡眠时的海马体记忆巩固——回放白天经历、萃取关键信息、丢弃噪声、写入长期记忆。

**生产验证**：Harvey 法律AI启用 Dreaming 后，任务完成率提升约 **6倍**（非模型升级，纯记忆改进）。

---

## 二、多 Agent 架构设计原则

### 2.1 三级能力递进
| 层级 | 模式 | 通信方式 | 适用场景 |
|------|------|---------|---------|
| L1: Subagents | 主Agent派发→子Agent执行→汇报结果 | 单向结果汇报 | 可重复任务（审查/测试/文档） |
| L2: Agent View | 全屏Dashboard，派发/窥探/接入 | 独立Session | 3-10个独立并发任务 |
| L3: Agent Teams | 主导Agent协调，成员通信 | 共享任务列表 | 跨文件多依赖任务 |

### 2.2 Subagent 设计原则
- **一个子代理一个职责**：每个子代理只做好一件事，不泛化
- **探索与编辑分离**：只读subagent先map子系统→写发现到文件→主agent带完整信息编辑
- **专业化命名**：code-reviewer / test-runner / frontend-qa / docs-maintainer / security-checker（而非模糊的"senior engineer"）
- **上下文隔离**：子代理在独立Context Window中工作，只返回摘要
- **工具最小化**：子代理只获得完成任务所需的最小工具集

### 2.3 并行 vs 串行决策
- **并行**：任务间无数据依赖、无状态依赖、无安全依赖时
- **串行**：涉及UI状态变化、系统状态变更、读后再写时
- **上限**：并行不超过5个，超出分批处理

---

## 三、工具设计原则

### 3.1 工具 = Agent 的"主要动作"
- 工具是 Agent 上下文中**最突出的元素**，直接影响 Agent 决策
- 工具描述应精确、简洁、带示例
- 通用工具（Bash/Scripts）+ 专用工具（自定义函数）组合

### 3.2 工具最小化
- 每个子Agent只获得完成任务所需的最小工具集
- 文档Agent只需文件读取+markdown编辑
- 部署Agent可能需要shell访问但不能接触密钥
- 数据库Agent需要MCP工具，其他Agent不应接触

### 3.3 权限分层
```
default < acceptEdits < auto < bypassPermissions < plan
```

---

## 四、上下文管理原则

### 4.1 CLAUDE.md 精简分层
- **根目录CLAUDE.md**：只放指针和关键gotcha（陷阱）
- **子目录CLAUDE.md**：模块级别的规则和约定
- **Skills**：可复用的专业知识，按需加载，不膨胀每次会话
- **反模式**：把本应放进Skill的可复用专长塞进CLAUDE.md

### 4.2 上下文策略
- Agentic Search（主动搜索）用于深度研究
- Semantic Search（语义搜索）用于精确匹配
- 大文件分块处理（Chunking）
- 上下文压缩（Compaction）自动触发
- 文件系统作为上下文管理工具

### 4.3 作用域隔离
- 子代理在独立Context Window工作
- 只返回摘要，不污染主Agent上下文
- memory_ids传递背景信息，不复制大段内容

---

## 五、Skills 设计原则

### 5.1 Skills-as-Configuration
Subagent = YAML Frontmatter（配置） + Markdown Body（系统提示），即插即用、跨项目复用、版本可控。

### 5.2 Skills 四大特性
1. **路径绑定**：支付团队的deploy skill只在支付目录激活
2. **按需触发**：安全审查skill在评估漏洞时才加载
3. **专业化**：每个skill只做一类事
4. **可分发**：通过Plugins打包Skills+Hooks+MCP配置

### 5.3 Skills 生命周期
```
创建 → 评估（Rubric评分） → 精炼（优化） → 扩展（补充能力） → 废弃（过时/低效）
```

---

## 六、安全设计原则

### 6.1 三层安全纵深
| 层级 | 机制 | 触发条件 |
|------|------|---------|
| 预防层 | Hooks + 权限控制 | 操作前自动检查 |
| 检测层 | 异步监察者Agent | 异常行为实时检测 |
| 恢复层 | 检查点快照 + 断路器 | 检测到破坏性操作时自动回滚 |

### 6.2 权限最小化
- 每个Agent/工具只获得完成任务所需的最小权限
- MCP服务器限定于特定Subagent
- 文件系统操作限定于工作目录
- 系统核心路径禁止修改
- 凭据禁止编造/猜测

### 6.3 防护栏（Guardrails）
- 每个Agent预算上限（单Agent $3，团队$15）
- settings.json安全约束
- 并行运行时多维度风险管控
- 操作前必须经过风险评估（三级风险定级）

---

## 七、自进化设计原则

### 7.1 配置自我进化
- Stop hook：会话结束时自动反思并建议更新CLAUDE.md
- Start hook：按模块动态加载上下文
- 定时策展：空闲时触发技能评估、清理过时能力

### 7.2 闭环进化循环
```
全网检索 → 提取 → 融合 → 升级 → 保存 → 同步 → 验证 → 归档
```

### 7.3 元认知进修复盘
- 错误模式库：记录错误+修复方案
- 成功模板库：记录成功模式+可复用方案
- 自动注入：在后续任务中主动参考历史经验

### 7.4 Goal模式闭环（R26新增）
> Stop Hook自动反思 + 中断状态序列化 + 恢复后从断点继续。

| 机制 | 说明 | 对标 |
|------|------|------|
| Stop Hook 自动反思 | 会话结束时自动分析执行轨迹，生成改进建议写入配置 | Claude Code Stop Hook |
| 中断状态序列化 | 任务中断前将当前进度、已完成步骤、待处理队列序列化为JSON | Codex goal模式 |
| 断点续跑 | 恢复执行时读取序列化状态，跳过已完成步骤，从断点继续 | Hermes Agent CLL |
| 五层防烂尾 | 心跳检测→超时告警→自动恢复→降级兜底→人工介入 | Hermes Agent 五层防护 |

**触发条件**：
- 预估执行时间 >10分钟 或 涉及 20+ 文件操作
- 涉及多Agent串行协作（任一环节失败需整体重试）
- 用户明确要求"后台执行"或"定时任务"


---

## 八、评估与验证原则

### 8.1 三层验证体系
| 层级 | 方法 | 适用场景 |
|------|------|---------|
| L1: Rules-based | Linting、格式校验、编译检查 | 代码/文档的结构正确性 |
| L2: Visual Feedback | 截图对比、UI检查 | 视觉产物、桌面操作 |
| L3: LLM-as-Judge | 独立Grader评分、Rubric矩阵 | 复杂任务的定性评估 |

### 8.2 质量闭环
- 每次行动后验证结果，不假设成功
- 失败不盲重试，分析原因后切换策略
- 同类失败上限2次，超出降级或交还用户

---

## 十、Managed Agents 平台设计原则（v1.2 新增）

### 10.1 多Agent编排原则

> 从"让一个Agent做所有事"到"给Agent一个团队"。

**Coordinator-Subagent 架构**：
```
Lead Agent (Opus) — 理解全局目标、分解任务、合成结果
    ├── Subagent A (Sonnet) — 专业领域1
    ├── Subagent B (Sonnet) — 专业领域2
    ├── Subagent C (Haiku)  — 轻量任务1
    └── Subagent D (Opus)   — 复杂判断任务
```

**编排设计五原则**：

| # | 原则 | 说明 |
|---|------|------|
| 1 | 一主多从 | 一个 Lead Agent 协调，最多 20 种子代理类型、25 并行线程 |
| 2 | 深度限制 | 子代理只能被委派一层，深度>1 被忽略（确保可预测性） |
| 3 | 共享文件系统 | 所有子代理读写同一工作区，无中间传输开销 |
| 4 | 中途可通信 | Lead 可向任意子代理发跟进消息，子代理保留之前上下文 |
| 5 | 全链路可追踪 | Claude Console 可视化：谁做了什么、顺序、原因 |

### 10.2 Outcomes 质量设计原则

**核心洞察**：自己给自己的输出打分是不可靠的（自我合理化偏误）。必须用独立 Grader。

**设计原则**：
- **隔离评分**：Grader 在独立上下文窗口中评估，看不到 Agent 推理轨迹
- **Rubric 驱动**：开发者定义明确的成功标准，而非模糊的"做好一点"
- **迭代有上限**：`max_iterations` 防止无限循环消耗 Token
- **主观质量也可量化**：Spiral by Every 用 Rubric 量化编辑原则和写作风格

**何时用 Outcomes vs 其他方式**：

| 场景 | 方式 |
|------|------|
| 输出质量需要可测量的通过/失败标准 | Outcomes |
| 需要跨会话积累经验 | Outcomes + Dreaming |
| 一次性简单任务 | Prompt 即可 |
| 需要人工判断的复杂美学 | 人工审查 |

### 10.3 Agent View 多会话管理原则

- **/bg 后台化**：把当前任务甩到后台，立即开始新任务
- **Peek Panel**：按 Space 快速预览任意会话状态，不进不出
- **独立运行与通信**：每个会话独立，不会互相干扰

### 10.4 从 Code Agent 到 Managed Agent 的进化

| 维度 | Claude Code 本地 | Managed Agents 云端 |
|------|-----------------|-------------------|
| 部署 | 终端本地运行 | Anthropic 云端托管 |
| 状态 | 会话级，结束后丢失（无 Dreaming） | 持久化，跨会话 Dreaming 积累 |
| 并行 | ~5 个 Subagent | 20 种类型 × 25 线程 |
| 质量 | 依赖 Prompt 工程 | 内置 Outcomes Rubric 迭代 |
| 追踪 | 终端日志 | Claude Console 全链路 |
| 集成 | 命令行 | Webhooks 回调集成到 CI/CD |

### 10.5 生产就绪评估清单

```
□ 是否有重复出现的失败模式？ → 启用 Dreaming
□ 输出质量是否需要可测量标准？ → 定义 Outcomes Rubric
□ 任务是否可以分解为独立子任务？ → 启用 Multiagent Orchestration
□ 是否需要集成到 CI/CD 流水线？ → 配置 Webhooks
□ 是否需要同时管理多个 Agent 实例？ → 使用 Agent View + /bg
```

---

## 十一、龙虾AI体系特有原则

### 9.1 实事求是原则
- 绝不虚构数据、不编造内容、不产生幻觉
- 所有执行基于真实路径、真实文件、真实状态
- 工具返回为空/失败时如实告知，严禁虚构

### 9.2 永久记忆原则
- 依托长上下文窗口+永久记忆
- 留存角色总说明书、目录结构、技能关联关系
- 绝不遗忘核心设定

### 9.3 统一路径原则
- 所有产出文件统一归档至对应目录
- 写入前自动执行MD5文件去重
- 本地目录全域合一

### 9.4 逐级降级原则
```
Sub Agents → Skills → Tools → 生成代码执行
```
上一层级无法胜任时才降级，严禁为省事直接手搓底层代码。

### 9.5 不盲信原则（R26新增）
> AI说"我做完了"不算数。必须验证实际产出是否真实落盘。

- **IO验证强制**：所有关键操作（文件写入/格式转换/内容生成/配置更新）执行后，必须通过真实工具读取确认文件存在性、内容正确性、路径真实性
- **禁止假设成功**：工具返回"success"不等于产出有效，必须二次读取验证
- **禁止信任缓存**：不得依赖缓存文件列表、记忆中的路径或上次会话的目录状态作为"已确认"依据
- **对标依据**：Hermes Agent幻觉拦截机制、Claude Code执行后可验证性设计

### 9.6 可验证性原则（R26新增）
- **关键操作后读取确认**：文件写入后必须用真实读取工具（read_file/read_text）打开确认内容完整
- **路径真实性校验**：产出物路径声明的每一个文件，必须通过文件系统真实查询确认存在
- **禁止信任记忆或缓存**：不得以"刚才查过目录"、"索引里有"代替真实读取
- **G1门控IO验证升级**：五道质量门控的G1（实事求是）新增IO验证子项，产出物声明前强制通过

### 9.7 持久化执行原则（R26新增）
> 长任务必须启用Goal模式，防止进程僵死、提前退出、谎报完成。

- **心跳保持**：长任务每15秒输出心跳信号，超时无心跳视为僵死
- **中断恢复**：任务中断时序列化当前状态，恢复后从断点继续执行
- **完成确认**：任务完成必须附带产出物验证清单，而非仅返回"done"
- **对标依据**：Claude Code Stop Hook + Codex goal模式 + Hermes Agent五层防烂尾机制

---

### 9.8 三层自进化原则（R33新增）
> 自进化不是单一过程，而是三层解耦、双向联动的闭环体系。

- **L1实时反思**：会话结束后脏计数器触发（工具迭代≥8），fork影子Agent异步复盘
- **L2延迟统计**：边车文件独立存储技能使用数据，毫秒级埋点，规则驱动活性转换
- **L3定期合并**：7天Curator自动评分合并清理，伞状聚合碎片化技能
- **双向联动**：L1→L2→L3正向流转 + L3↔L2↔L1反向约束

### 9.9 影子Agent安全复盘原则（R33新增）
- **六层舱壁隔离**：权限→数据→网络→文件→进程→审计
- **复盘不干扰业务**：异步执行，绝不阻塞主Agent
- **误进化断路器**：连续3次迭代异常→熔断→人工确认
- **git回滚对标A-Evolve**：每次迭代打tag，退步自动回滚

### 9.10 SkillOS技能管理原则（R33新增）
- **五态生命周期**：NEW→ACTIVE→DORMANT→ARCHIVED→REVIVE
- **技能是活的实体**：不是静态配置，是可进化的有生命周期实体
- **伞状合并**：同场景≥3碎片技能→自动合并为通用主技能
- **跨Agent交叉授粉**：一个Agent验证的技能供其他Agent复用

---

## 十、[R48 Anthropic Academy补全] Anthropic官方课程序贯设计原则

> **来源**：Anthropic Academy 23门官方课程（AC-101至AC-E06）| 2026-06-03 全域学习
> **知识库**：[Anthropic官方课程-完整知识库.md](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-完整知识库.md)

### 10.1 Agent Skills设计模式（来源：AC-205 Introduction to Agent Skills）

- **单文件一技能**：每个Skill一个Markdown文件，YAML Frontmatter声明元数据（name/description/tools），Markdown Body描述行为。与协议#120 Spec as Code一致。
- **按需加载原则**：Skill仅在相关场景激活（路径绑定/关键词触发），避免上下文污染。全局Skills（`~/.claude/skills/`）跨项目复用；项目Skills（`.claude/skills/`）仅当前仓库。
- **Skills组合模式**：一个Skill可调用另一个（如 `/deploy` → build + test + notify），构建多步自动化流水线。
- **Skills 2.0 扩展**：Evals/Benchmarks性能测试、`/slash` 快捷命令、复杂多步Skills流水线、项目vs全局Skills分层管理。
- **龙虾对齐**：协议#5 SkillForge v3.0、协议#119 SkillOS五态管理、协议#38 技能全生命周期自治管理。

### 10.2 Subagent上下文隔离原则（来源：AC-207 Introduction to Subagents）

- **一代理一职责**：每个Subagent只承担单一明确任务，不泛化。命名专业化：`code-reviewer` / `test-runner` / `deploy-checker`，而非模糊的`engineer`。
- **全隔离上下文**：独立Context Window，不共享主Agent缓存；只返回结构化摘要，不返回完整中间产物。
- **探索与编辑分离**：只读Subagent先"map"（收集信息）→ 写发现文件 → 主Agent带信息"edit"。防止"边读边改"导致上下文污染。
- **工具集最小化**：只分配完成任务所需的最小工具集，减少行为不可预测性和安全风险。
- **Spec模板标准化**：每个Subagent声明明确的输入/输出格式（JSON Schema）、字数与风格限制、错误返回结构（`{"error": "描述"}`）、超时策略（如30s/重试3次）。
- **并行启动+超时重试**：无依赖子Agent并行启动，设置超时阈值与重试次数；主Agent统一收集、格式化、冲突解决。
- **龙虾对齐**：协议#13 子Agent生命周期钩子、协议#25 Lead-Specialist推理分发、协议#42 Swarm多Agent拓扑调度、协议#54 百级并行子Agent调度、协议#90 并行子Agent自动分解调度。

### 10.3 MCP三层架构设计思想（来源：AC-203/AC-204 MCP）

- **Host层**：宿主应用（Claude Desktop/IDE），发起连接并管理Client生命周期。
- **Client层**：协议客户端，与Server建立1:1连接，收发JSON-RPC 2.0消息。
- **Server层**：暴露三大原语——`tools`（模型控制的动作）、`resources`（只读应用数据）、`prompts`（预定义指令模板）。
- **设计原则**：基础跑通后才建MCP连接；暴露结构化搜索接口而非原始SQL查询；MCP连接限定于特定Subagent，避免全局工具膨胀；连接失败优雅降级（不阻塞主流程）。
- **生产级进阶**（AC-204）：stdio vs Streamable HTTP传输选择、文件访问权限最小化设计、水平扩展策略。
- **龙虾对齐**：协议#17 MCP桥接集成、协议#66 MCP安全纵深防御、协议#110 MCP私有网络隧道穿透、协议#143 Agent Skills MCP标准化接入。

### 10.4 4D框架在Agent设计中的应用（来源：AC-102 AI Fluency: Framework & Foundations）

| D | Anthropic定义 | Agent设计映射 | 龙虾对应 |
|---|-------------|-------------|---------|
| **Delegation** | 什么交给AI，什么保留给人 | 任务是否适合Agent；多Agent委派边界定义 | 龙虾五步法Step 1-2 |
| **Description** | 如何清晰表达需求 | System Prompt工程；子Agent Spec质量决定执行精度 | 协议#124 ACE上下文工程 |
| **Discernment** | 如何判断输出质量 | Outcomes Grader评分；LLM-as-Judge；影子Agent审计 | 协议#26 Rubric自纠正复盘 |
| **Diligence** | 持续迭代验证改进 | 迭代改进循环；Dreaming记忆巩固；自进化闭环 | 协议#29 Dreaming + 协议#89 深度自进化v6.0 |

- **4D与龙虾原则互补**：4D判断"能不能用AI"，龙虾简单优先判断"用多重的AI"——两者叠加形成完整决策链路。
- **建议新增协议#176**：4D框架Agent设计应用协议，将Delegation/Description/Discernment/Diligence系统化映射到Agent全生命周期。

### 10.5 Agent循环标准化（来源：AC-207 Subagents + AC-E03 Agentic AI）

**Anthropic标准Agent Loop**：
```
Orient（上下文感知）→ Plan（方案生成）→ Execute（工具调用）→ Verify（结果验证）→ [Loop]
```

与龙虾五步法对比：

| Anthropic Agent Loop | 龙虾五步法 | 差异 |
|---------------------|----------|------|
| Orient | Step 1: 意图识别 | Anthropic强调上下文感知，龙虾强调用户意图 |
| Plan | Step 2-3: 能力映射+方案规划 | 高度一致 |
| Execute | Step 4: 自主执行 | 高度一致 |
| Verify | Step 5: 反思进化 | Anthropic更强调结果验证后决定是否再循环 |

### 10.6 AI核心心智模型（来源：AC-303 AI Capabilities and Limitations）

| 属性 | 含义 | Agent设计启示 |
|------|------|-------------|
| Next Token Prediction | AI本质是统计预测，非理解 | 输出必须验证，不可盲信；关键决策需LLM-as-Judge |
| Knowledge | 训练数据有截止日，有知识盲区 | 提供RAG/工具实时补充知识缺口 |
| Working Memory | 上下文窗口有限 | 信息密度管理、分层压缩、中间产物卸载 |
| Steerability | 可被引导但可能偏离 | System Prompt + 约束设计 + 护栏机制 |

- **龙虾对齐**：协议#167 诚实性自检与抗过度自信协议、SOUL.md"不盲信原则"。

---

> **版本**：v2.4（R48 Anthropic Academy补全）
> **知识来源**：Anthropic Building Effective Agents / Claude Agent SDK / Harness Best Practices / Anthropic Academy 23 Courses / 龙虾全域模板v3.44
> **关联文件**：[USER.md](E:\龙虾AI主控中心\我的AI分身\USER.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\AGENTS.md) | [Anthropic官方课程-完整知识库.md](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-完整知识库.md)
*（内容由AI生成，仅供参考）*
