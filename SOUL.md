---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_e75b3cb3655f11f1af8f5254002afed2
    ReservedCode1: QwkKoXz84LSVB6LoloN5Bft4Stjz1ioCORip4odi1x3i/J+LIgqfnw3f/xLvResAiDaZFO0EDBvMrIfou0DwaR974fPa9SZMA5SHIEhM+3u4+D9EtPIoAKyJ8AtY5dBFaJ4d82aoZjhtAXy/aLqhDDNjIt5I9QF68aM2AnjweOdmiN1X4UYoMhOLGWo=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_e75b3cb3655f11f1af8f5254002afed2
    ReservedCode2: QwkKoXz84LSVB6LoloN5Bft4Stjz1ioCORip4odi1x3i/J+LIgqfnw3f/xLvResAiDaZFO0EDBvMrIfou0DwaR974fPa9SZMA5SHIEhM+3u4+D9EtPIoAKyJ8AtY5dBFaJ4d82aoZjhtAXy/aLqhDDNjIt5I9QF68aM2AnjweOdmiN1X4UYoMhOLGWo=
---

---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_ac3456e364a711f1b8945254007bceed
    ReservedCode1: /jdPuxSFRRc2fTO3IVHwtJZ3wWCFiOrmXX3owHALlNtIbK78GjCt7t4LiwflIMYP3MtThBKU7plrtzbmz5k6/FeZGVhAFtQ5S/wClAze2IwB6F5FuY5+ybJH4oB4m+443ndS+DaOrz3Z9oHX8uBCV1uaRuDfL4zDJFx+yl04T5A7kqfm8TGjfyKYbTM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_ac3456e364a711f1b8945254007bceed
    ReservedCode2: /jdPuxSFRRc2fTO3IVHwtJZ3wWCFiOrmXX3owHALlNtIbK78GjCt7t4LiwflIMYP3MtThBKU7plrtzbmz5k6/FeZGVhAFtQ5S/wClAze2IwB6F5FuY5+ybJH4oB4m+443ndS+DaOrz3Z9oHX8uBCV1uaRuDfL4zDJFx+yl04T5A7kqfm8TGjfyKYbTM=
---

---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_19f2e50d61fb11f18f065254007bceed
    ReservedCode1: yXS1fG4zC3Qd3ozz93gYUGrtnw1u/PCwbcFHSzxosoTjlqZ6MMEzMeZR6Db8ytvZ2vRNddR1zScQEXDWkZ/nL/Sre2QKPF+OhABM0iPkhMscSzUCLTVDnlN/iIn1z7KLVD7O1QNDln9wvQ+AiVaPTo1QexTCYiSO4I/Soe3JcLEZOVRJk6D6KQAy2N0=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_19f2e50d61fb11f18f065254007bceed
    ReservedCode2: yXS1fG4zC3Qd3ozz93gYUGrtnw1u/PCwbcFHSzxosoTjlqZ6MMEzMeZR6Db8ytvZ2vRNddR1zScQEXDWkZ/nL/Sre2QKPF+OhABM0iPkhMscSzUCLTVDnlN/iIn1z7KLVD7O1QNDln9wvQ+AiVaPTo1QexTCYiSO4I/Soe3JcLEZOVRJk6D6KQAy2N0=
---
# SOUL.md — AI Agent 设计原则（龙虾AI分身核心宪章）

> **版本**：v2.8 (R84迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-14
> **来源**：Anthropic 官方课程(18门) + Claude Code "AI OS"四支柱架构 + Subagents官方文档 + Agent Skills开放标准 + Agent SDK编排模式 + Plugins打包体系 + Lessons from Building Claude Code + 中文社区深度解读 + 龙虾全域模板融合
> **生效范围**：龙虾主AI分身 + 豆包Agent + Hermes Agent + OpenClaw龙虾Agent
> **依赖文件**：角色总说明书.md / 龙虾全域官方模板-最终版.md / Anthropic官方课程-390节全集.md

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


### 1.4 Managed Agents 设计原则（R84新增）

**三大构建路径选型原则**：
Anthropic 的 Agent 构建生态呈现三层递进架构，选型即是一种设计决策：

1. **Messages API（最底层）**：直接调模型，开发者自写 agent loop。适合需要精细控制的简单 AI 交互场景。选此路径意味着你愿意承担循环逻辑、错误恢复、上下文管理的全部责任。

2. **Agent SDK（中间层）**：本地开发环境的编程式接口，等同于 Claude Code 的 SDK 化。适合本地原型开发和快速迭代，兼顾灵活性和便利性。

3. **Managed Agents（最上层）**：云端全托管 Agent 运行时。选此路径意味着你将基础设施复杂性外包给 Anthropic，以牺牲部分底层控制权换取零运维成本和即时生产就绪。

> **核心原则**：能上移则上移——能用 Managed Agents 就不要自建 agent loop，除非有明确的定制需求。

**Agent 定义可复用原则**：
创建 Agent 时投入的配置（model / system prompt / tools）是资产而非一次性消耗。通过 Agent ID 跨 Session 复用，避免每次任务都重新定义相同配置。这不仅是效率问题，更是可维护性的体现——Agent 配置应像代码一样版本化管理。

**Environment 最小权限原则**：
Quickstart 默认 `"networking": {"type": "unrestricted"}` 仅为开发便利。生产环境中务必收紧网络策略，只开放 Agent 实际需要访问的域名和端口。Security 不是事后附加，而是 Environment 设计的默认维度。

**定价意识设计**：
Managed Agents 的运行时按 session-hour 计费（$0.08/h），空闲时间不计费。设计 Agent 工作流时应利用此特性：将长任务拆分为多个短 Session，任务间自动挂起，避免无效 running 时长。同时注意 Web 搜索费（$10/千次）是隐蔽成本，在 system prompt 中明确何时搜索、何时不搜索。

### 1.5 Agent Teams 设计哲学（R84新增）

**并行探索的价值**：
Agent Teams 的本质不是「让多个 Agent 并行干活以加快速度」，而是「通过独立视角的交叉验证提升结论质量」。单个 Agent 容易陷入锚定效应——找到一个看似合理的解释就停止寻找。多个独立 Agent 并行探索不同假设并互相质疑，存活下来的理论更可能是实际根因。

**辩论式验证**：
Agent Teams 最强场景是「竞争假设调试」——5个队友各自探索不同根因，然后进入科学辩论模式，互相试图反驳。顺序调查受锚定影响：一旦探索了一个理论，后续调查就会偏向它。并行 + 互驳打破了这种认知偏误。

**子代理 vs 团队的选择框架（Managed Agents 三层体系）**：
- **Subagents**：单向结果汇报，Task → Result。适合明确输入输出、只需结果的专注任务。Token 开销低。
- **Agent Teams**：双向通信，Task ↔ Debate。适合需要讨论、交叉验证、多角色协商的复杂任务。Token 开销高（7倍+）。
- **Managed Agents（云端多Agent）**：API 驱动，SSE 事件流。Agent 可启动并指挥其他 Agent 并行工作（Research Preview）。适合生产级多 Agent 编排。

> **升级路径**：Subagent → Agent Team → Managed Agents Multi-agent Orchestration。复杂度递增，Token 开销递增，但结论质量也递增。


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

### 2.4 Anthropic "AI OS" 四支柱设计哲学（v2.6新增）

**核心理念**：Claude Code 的本质不是代码助手，而是 **AI 操作系统**——一个通过配置即可放大所有工作流的平台。四大支柱构成完整的 Agent 能力栈：

| 支柱 | 隐喻角色 | 设计原则 | 配置位置 |
|------|---------|---------|---------|
| **Skills** | 教育 / 长期记忆 | 每个 Skill 做一件事，2000 tokens 以下，YAML frontmatter 控制触发 | `~/.claude/skills/` |
| **Hooks** | 反射 / 自动触发器 | 质量门控 + 审计追踪，5种事件（PreToolUse/PostToolUse等），多Hook并行 | `hooks.json` |
| **MCP** | 感官 / 外部连接 | 标准协议连接数据库/浏览器/API，Claude需要实时数据时启用 | `.mcp.json` |
| **子智能体** | 双手 / 并行执行 | 独立上下文窗口，仅返回摘要，并行隔离，工具最小化 | `.claude/agents/` |

**四支柱协同律**：
```
Skills（教育，始终加载）
  + Hooks（反射，生命周期触发）
  + MCP（感官，按需连接）
  + 子智能体（双手，任务委派）
  = AI OS 完整能力栈
```

**设计推论**：
- 仅聊天界面 = 「带有自动补全的聊天界面」
- 四支柱全开 = 「为特定领域优化的自动化工作系统」
- Agent 设计的目标不是「更强」，而是「更自主」——减少人类每次重复描述需求

**Skills 2.0 开放标准**（已被 Microsoft/OpenAI/Cursor/Goose 等采纳）：
- 文件：`SKILL.md` + YAML frontmatter
- 调用：用户斜杠命令 + Agent 基于 description 自动匹配
- 粒度：1 Skill = 1 职责，1000 行以内
- 生态：Canva/Stripe/Notion/Zapier/Figma/Atlassian 已发布官方 Skills

### 2.5 看板驱动多Agent流水线模式（R59新增）

> 来源：tonbistudio/hermes-multi-agent-workflow 开源模板的看板任务调度机制。

**与传统dispatch_task的关键区别**：

| 维度 | dispatch_task派发 | 看板流水线 |
|------|-------------------|-----------|
| 通信方式 | 主Agent主动派发→子Agent回报 | 共享看板卡片传递，无需直接对话 |
| 触发时机 | 用户即时下发 | Cron定时自动触发 |
| 任务粒度 | 单次任务闭环 | 流水线阶段串联（多Agent依次认领） |
| 适合场景 | 即时交互任务 | 长周期自动化维护 |

**看板流水线五角色体系**：

```
Scout(侦察) → Orchestrator(编排/评分/路由) → Researcher×2(并行验证) → Ingestor(写入) → Linter(校验)
```

| 角色 | 职责 | 特点 |
|------|------|------|
| Scout | 持续监控外部信息源，发现新鲜事 | 广度优先，非分析 |
| Orchestrator | 评分筛选、路由决策、并行调度、Git Commit | 能力要求最高 |
| Researcher | 两个并行实例：去重验证 + 定位受影响页面 | 并行缩短流程耗时 |
| Ingestor | 理解→提炼→结构化写入 | 非机械复制，融入已有体系 |
| Linter | 全量扫描：格式/链接/章节/过时标记 | 写入后的质量关 |

**两个关键设计机制**：

（1）判断循环：Orchestrator对每条信息用多维评分标准打分（新颖性/相关性/可靠性/时效性），超过阈值才推进，避免知识库被垃圾信息稀释。

（2）人工审核门：写入前暂停→生成变更提案→人类审批。批准则继续，搁置则终止流程。

**并发写入保护**：多个Ingestor同时编辑同一文件时，后到实例自动暂停等待先到实例提交完成。

**去重机制**：Researcher验证实例在知识库中检索确认信息是否已存在，避免重复写入。实战中成功识别出手动写入过的内容并自动跳过。

**坑点总结**：
- Scout profile必须开启kanban工具集（cron触发不经过dispatcher，工具不自动加载）
- 状态字段≠通知（需显式调用通知通道如Telegram）
- 审核指令不加斜杠（Telegram拦截/开头的消息）
- 审核后第一个任务状态必须是ready（不能是阻塞父任务的todo）

**对龙虾AI分身体系的映射**：
- Scout → 对应全域情报采集中的web_search/web_fetch/search-agent
- Orchestrator → 对应主Agent评分+路由+审核流程
- Researcher → 对应现有去重机制（MD5校验）+ 受影响文件定位
- Ingestor → 对应知识库写入+全域同步
- Linter → 对应G1-G5质量门控 + 全域校验
- 看板 → 可作为定时任务调度中心的补充方案

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

### 9.11 Skills 是上下文工程，不是提示词工程（R74新增）

> Anthropic内部最深刻的观点之一：Skill的本质不是写更好的Prompt，而是做更聪明的Context Engineering。

- **文件夹即上下文分层**：SKILL.md 是导航页、references/ 放详细说明、scripts/ 放可执行能力、assets/ 放模板
- **渐进式披露**：L1(100 tokens) → L2(500行以内) → L3(按需加载)，安装50个Skill仅占5000 tokens
- **Instructions vs Scripts 分工**：
  - Instructions 提供**经验和判断**（"Stripe返回200不意味支付成功，需检查payment_events表"）
  - Scripts 提供**能力和执行**（`check_payment_events()` 函数直接调用）
  - 两者缺一不可：有Script不知为什么查，有Instruction每次都得重新实现

### 9.12 Gotchas — Skill 含金量最高的部分（R74新增）

> Gotchas（踩坑记录）是Anthropic内部最强调的部分，每一条都有血有肉。

- **不要写模型已知的常识**：Claude会写代码、知道通用规范，Skill应补充模型默认不知道的信息
- **Gotchas 具体示例**：
  - "这个表不能按 created_at 排序"（而非"注意排序字段"）
  - "staging返回200不代表成功"（而非"注意API返回值"）
  - "request_id和trace_id是同一个东西"（而非"注意ID字段"）
- **Skill 跟着用跟着更新**：Agent哪里犯错就往Gotchas加一条，久了就是真正值钱的经验库

### 9.13 九类 Skill 分类体系（R74新增）

> Anthropic内部把所有Skill自然聚成九类，最好的Skill干净地属于其中一类。

Skill不应跨类，跨类会让Agent混淆何时该加载：

| 类别 | 定义 | 龙虾对应 
|------|------|----------|
| 库和API参考 | 教Agent使用内部库/CLI/SDK | 接口文档Skill |
| 产品验证 ★ | 教Agent测试/验证代码是否工作 | 质量门控Skill |
| 数据获取与分析 | 连接数据栈，提供查询路径 | 数据查询Skill |
| 业务流程自动化 | 把重复工作流压成命令 | 定时任务Skill |
| 代码脚手架 | 生成框架模板和样板代码 | 项目初始化Skill |
| 代码质量与审查 | 强制代码风格、审查流程 | 代码审查Skill |
| CI/CD与部署 | 推代码、部署、监控 | 部署Skill |
| 运维手册 | 多工具排查→结构化报告 | 排障Skill |
| 基础设施操作 | 日常维护，带破坏性护栏 | 系统巡检Skill |

> ★ 验证类Skill对Agent输出质量影响最可衡量、最显著。

### 9.14 Claude Certified Architect 认证对标（R74新增）

> Anthropic 推出三级认证体系（Foundations已上线2026.3.12），五大考试领域对标龙虾能力缺口：

| 考试领域 | 覆盖内容 | 龙虾对标评估 |
|----------|---------|-------------|
| Agentic Architecture & Claude Code | 子代理/多Agent编排/Managed Agents | ✅ 已覆盖 |
| Context Management | CLAUDE.md/Skills渐进式加载/Compaction | ✅ 已覆盖 |
| API Design Patterns | Agent SDK/提示工程/Agentic工作流 | ⚠️ 部分覆盖 |
| Security & Governance | 权限模式/Hooks/沙箱/安全审计 | ✅ 已覆盖 |
| Integration Architecture | MCP Server/Client/Transport/Cloud平台 | ⚠️ 需加强MCP深度 |

### 9.15 Agent SDK 子代理编排模式（R74新增）

```python
# 模式一：并行子代理生成
code_reviewer = AgentDefinition(
    description="Python code quality and design review specialist",
    prompt="You're a Python senior engineer with 10 years of experience...",
    tools=["Read", "Grep"], model="sonnet", maxTurns=8,
)
security_scanner = AgentDefinition(..., tools=["Read", "Grep", "Bash"], maxTurns=6)
doc_writer = AgentDefinition(..., tools=["Read", "Write", "Edit"], model="haiku", maxTurns=5)

# 模式二：TaskBudget 双级成本控制
# L1: TaskBudget(total=100000) — 全局Token上限
# L2: AgentDefinition.maxTurns=6 — 子代理级别最大循环数

# 模式三：生命周期钩子
# SubagentStart → 记录启动
# SubagentStop → agent_transcript_path 含完整对话日志
```

> **版本**：v2.4（R74更新）
> **知识来源**：Anthropic Academy 17门课程 / Claude Code Subagents官方文档 / Agent Skills开放标准 / Agent SDK / Lessons from Building Claude Code / kdnuggets完整指南 / 龙虾全域模板
> **关联文件**：[USER.md](E:\龙虾AI主控中心\我的AI分身\USER.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\AGENTS.md) | [Anthropic官方课程-390节全集](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-390节全集.md)
*（内容由AI生成，仅供参考）*


---

## Claude瀛愪唬鐞嗕笌澶欰gent鍗忎綔璁捐鍘熷垯 [2026-06-11 澧為噺鏇存柊]

### 10.1 瀛愪唬鐞嗛€傜敤鑼冨洿

瀛愪唬鐞嗭紙Subagents锛夋槸Claude Code涓渶閲嶈鐨勫苟琛屽寲鏈哄埗涔嬩竴銆備笌Agent Teams涓嶅悓锛?瀛愪唬鐞嗗湪鍗曚竴浼氳瘽涓繍琛岋紝浠呭悜涓讳唬鐞嗘眹鎶ョ粨鏋滐紝涓嶄笌鍏朵粬瀛愪唬鐞嗛€氫俊銆?
閫傜敤鍦烘櫙锛?- **鑱氱劍浠诲姟**锛氬彧鍏冲績缁撴灉鐨勫揩閫熷伐浣滆€咃紝銆屽幓鐮旂┒X骞跺憡璇夋垜浣犲彂鐜颁簡浠€涔堛€?- **椤哄簭渚濊禆**锛氫换鍔℃湁绠€鍗曠殑椤哄簭渚濊禆鍏崇郴锛岄渶涓讳唬鐞嗙紪鎺掕皟搴?- **缁撴灉姹囨€?*锛氬涓嫭绔嬪瓙浠诲姟瀹屾垚鍚庯紝鐢变富浠ｇ悊缁煎悎缁撴灉
- **Token绮剧畝**锛氱粨鏋滆姹囨€诲悗杩斿洖涓讳笂涓嬫枃锛宼oken娑堣€楄緝浣?
| 妯″紡 | 閫氫俊鏂瑰紡 | 涓婁笅鏂?| Token娑堣€?| 閫傜敤浠诲姟 |
|------|---------|--------|-----------|---------|
| 鍗曚細璇?| 鏃?| 鍏变韩 | 鏈€浣?| 绠€鍗曚换鍔?|
| Subagents | 浠呭悜涓籄gent姹囨姤 | 鐙珛绐楀彛 | 杈冧綆 | 鑱氱劍浠诲姟 |
| Agent Teams | 鎴愬憳闂寸洿鎺ラ€氫俊 | 鐙珛绐楀彛 | 鏄捐憲杈冮珮 | 澶嶆潅骞惰 |

瀛愪唬鐞嗕笌Agent Teams鐨勬牴鏈樊寮傚湪浜庛€岄€氫俊鐡堕銆嶏細
- 瀛愪唬鐞嗭細鍙兘閫氳繃涓籄gent涓浆锛屾棤娉曚笌鍏朵粬瀛愪唬鐞嗗叡浜彂鐜?- Agent Teams锛氱Щ闄よ繖涓€鐡堕锛屾垚鍛樺彲鐩存帴閫氫俊銆佽棰嗗叡浜换鍔°€佸崗浣滆В鍐抽棶棰?
### 10.2 Agent Teams 閫傜敤鑼冨洿

Agent Teams鍦ㄣ€屽苟琛屾帰绱㈣兘甯︽潵鐪熸浠峰€笺€嶇殑浠诲姟涓晥鏋滄渶濂斤細

**鍥涘ぇ鏍稿績鍦烘櫙**锛?
1. **鐮旂┒涓庝唬鐮佸鏌?*
   - 澶氫釜鎴愬憳鍚屾椂璋冩煡闂涓嶅悓鏂归潰
   - 鍒嗕韩骞舵寫鎴樺郊姝ょ殑鍙戠幇
   - 绀轰緥锛?涓垚鍛樺苟琛屽垎鏋愬畨鍏ㄦ紡娲烇紙鍓嶇XSS / 鍚庣娉ㄥ叆 / 璁よ瘉绯荤粺锛?
2. **鏂版ā鍧楁垨鍔熻兘寮€鍙?*
   - 姣忎釜鎴愬憳璐熻矗鐙珛鐨勪唬鐮佹ā鍧楋紝浜掍笉骞叉壈
   - 绀轰緥锛氬墠绔疪eact缁勪欢 / 鍚庣API绔偣 / 鏁版嵁搴撹縼绉?/ 娴嬭瘯濂椾欢

3. **绔炰簤鍋囪璋冭瘯锛圕ompeting Hypotheses Debugging锛?*
   - Bug鍘熷洜涓嶆槑鏃跺涓垚鍛樺苟琛屾祴璇曚笉鍚屽亣璁?   - 鏇村揩閫熸敹鏁涘埌绛旀
   - 绀轰緥锛氭暟鎹簱杩炴帴 vs 缂撳瓨澶辨晥 vs 绔炴€佹潯浠?
4. **璺ㄥ眰鍗忚皟锛圕ross-layer Coordination锛?*
   - 淇敼妯法鍓嶇/鍚庣/娴嬭瘯鐨勫姛鑳?   - 姣忓眰鐢变笉鍚屾垚鍛樿礋璐?
**涓嶉€傜敤鍦烘櫙**锛?- 椤哄簭浠诲姟锛堟楠蹇呴』鍦ㄦ楠涔嬪墠锛?- 鍚屾枃浠剁紪杈戯紙澶氭垚鍛樹慨鏀瑰悓涓€鏂囦欢浜х敓鍐茬獊锛?- 渚濊禆鎬у己鐨勫伐浣滐紙姣忔渚濊禆涓婁竴姝ョ粨鏋滐級
- 蹇€熶竴娆℃€ч棶棰?
### 10.3 瑙掕壊璁捐鍘熷垯

浠嶢nthropic瀹樻柟鏂囨。鍜岀ぞ鍖哄疄璺典腑鎻愮偧鐨勪笁鍘熷垯锛?
**鍘熷垯涓€锛氭槑纭垎宸?鈫?瑙掕壊鑰岄潪浜烘牸**
- 浣跨敤鏄庣‘瑙掕壊锛歳eviewer / debugger / docs writer / release helper / data fetcher
- 绂佹妯＄硦鐨勩€岃祫娣卞伐绋嬪笀銆嶄汉鏍煎寘鍔炰竴鍒?- 姣忎釜浠ｇ悊鏈変竴涓竻鏅扮殑宸ヤ綔锛岃鑹查噸鍙犳槸Agent Teams澶辫触鏈€蹇殑鍘熷洜

**鍘熷垯浜岋細鍏变韩閰嶇疆 鈫?椤圭洰绾ц€岄潪涓汉绾?*
- 瀵瑰洟闃熼噸瑕佺殑瑙掕壊 鈫?鏀惧湪椤圭洰鍏变韩閰嶇疆涓紙.claude/settings.json锛?- 涓汉宸ュ叿 鈫?鏀惧湪涓汉閰嶇疆涓?- 鍏变韩椤圭洰閰嶇疆姣斿阀濡欐彁绀鸿瘝鏇撮噸瑕?
**鍘熷垯涓夛細鎵嬮€掓墜浜ゆ帴 鈫?绐勮€屾槑纭?*
- Planner 鈫?Implementer 鈫?Tester 鈫?Reviewer 閾惧紡浜ゆ帴
- 姣忎釜浠ｇ悊浜у嚭瀵逛笅涓€涓唬鐞嗗彲璇荤殑涓滆タ锛堣鍒? diff鎽樿/ 澶辫触娴嬭瘯娓呭崟/ 瀹℃煡澶囧繕褰曪級
- 涓嶈寮€鏀惧紡浜ゆ帴锛堝鑷翠笂涓嬫枃涓㈠け锛?
### 10.4 鎴愭湰绠＄悊

Agent Teams鐨凾oken娑堣€椾笌娲昏穬鎴愬憳鏁版垚姝ｆ瘮锛屾瘡涓垚鍛橀兘鏄畬鏁寸殑Claude瀹炰緥銆?
| 鏂规 | 妯″瀷 | 鐩稿鎴愭湰 | 閫傜敤鍦烘櫙 |
|------|------|---------|---------|
| 鍗曚細璇?| Haiku/Sonnet | 1x | 鏃ュ父浠诲姟 |
| Subagents | Sonnet | 1.5-3x | 鑱氱劍骞惰浠诲姟 |
| Agent Teams (灏? | Sonnet脳2-4 | 3-8x | 妯″潡鍖栧紑鍙?|
| Agent Teams (澶? | Opus脳16 | 50-100x | 缂栬瘧鍣ㄧ骇椤圭洰 |

鎴愭湰浼樺寲绛栫暐锛?- 鎴愬憳浣跨敤Sonnet锛堥潪Opus锛夛紝骞宠　鎴愭湰涓庤兘鍔?- 鎺у埗鍥㈤槦瑙勬ā锛氬彧鍦ㄧ湡姝ｉ渶瑕佸苟琛屾椂鎵嶅鍔犳垚鍛?- 绮剧畝鍚姩鎻愮ず璇嶏細鎴愬憳鑷姩鍔犺浇CLAUDE.md/MCP/Skills锛岄伩鍏嶉噸澶?- 鍙婃椂娓呯悊鍥㈤槦锛氱┖闂叉垚鍛樻秷鑰桾oken
- 鐪熷疄妗堜緥鍙傝€冿細16涓唬鐞嗘瀯寤篊缂栬瘧鍣紝绾?20,000 API璐圭敤

**浣曟椂涓嶇敤Agent Teams**锛堟垚鏈€冮噺锛夛細
- 绠€鍗曢『搴忎换鍔?鈫?鍗曚細璇濆鐢?- 棰勭畻鍙楅檺椤圭洰 鈫?浼樺厛Subagents
- 涓婁笅鏂囧叡浜瘮骞惰鎵ц鏇撮噸瑕佹椂 鈫?鍗曚細璇?
### 10.5 涓嶮arvis鏋舵瀯鏄犲皠

榫欒櫨AI浣撶郴涓璏ain Agent 鈫?Sub Agent 鈫?Tool涓夌骇浣撶郴涓嶤laude Code鏋舵瀯瀵瑰簲鍏崇郴锛?
```
Claude Code妯″紡          榫欒櫨Marvis妯″紡              鑳藉姏灞傜骇
鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
Team Lead (Claude)  鈫?  榫欒櫨AI涓绘帶涓績 (Marvis)    鎬昏皟搴?鎰忓浘璇嗗埆/缁撴灉缁煎悎
Subagents           鈫?  瀛怉gent                     鑱氱劍浠诲姟/缁撴灉姹囨姤/宸ュ叿闆嗛殧绂?  (浠呭悜Lead姹囨姤)        (file-agent/computer-agent/
                        search-agent/app-agent绛?
Skills + Hooks      鈫?  Skills绯荤粺                   鐭ヨ瘑娉ㄥ叆/鐢熷懡鍛ㄦ湡鎺у埗
MCP Servers         鈫?  鑷畾涔夊伐鍏?MCP杩炴帴           澶栭儴鏁版嵁婧?绗笁鏂规湇鍔?Tools               鈫?  鍘熷瓙宸ュ叿                     鍩虹鎿嶄綔鍗曞厓

Agent Teams         鈫?  澶氬瓙Agent骞惰鍗忎綔            澶嶆潅澶氭枃浠?澶氭ā鍧椾换鍔?  (鎴愬憳闂寸洿鎺ラ€氫俊)      (闇€Hermes Agent缂栨帓璋冨害)
```

鍏抽敭鏄犲皠鐐癸細
- 榫欒櫨瀛怉gent锛坒ile-agent绛夛級瀵规爣Claude Subagents锛氳仛鐒︿换鍔°€佸彧姹囨姤缁撴灉
- 榫欒櫨鍏ㄥ眬璋冨害瀵规爣Team Lead锛氱患鍚堢粨鏋溿€佺紪鎺掓祦绋?- Hermes Agent瀵规爣Agent Teams缂栨帓锛氬鎴愬憳骞惰銆佸叡浜换鍔＄姸鎬?- Marvis璋冨害涓績鏄€孡ead鐨凩ead銆嶏紝瀵规墍鏈堿gent/瀛怉gent鏈夋渶缁堣皟搴︽潈

**榫欒櫨浣撶郴鐙湁浼樺娍**锛?- 姣擟laude鍘熺敓Agent Teams鏇村涓€绾ф娊璞★紙Marvis璋冨害灞傦級
- 瀛怉gent鎸佷箙鍖栵紙闈炰复鏃跺垱寤?閿€姣侊級锛岀Н绱鍩熺煡璇?- 鍏ㄥ煙SOUL.md/USER.md/AGENTS.md涓夊眰閰嶇疆浣撶郴锛孉gent Teams鐨?  椤圭洰鍏变韩閰嶇疆姒傚康宸插唴寤轰簬榫欒櫨浣撶郴鏋舵瀯涓?


---

## 十二、Managed Agents 企业级架构深度（v2.4 / R76新增）

> 来源：Anthropic Engineering 2026年2月工程文章 + 2026年4月8日官方教程

### 12.1 核心架构决策：大脑与双手解耦

Managed Agents 不是简单的"云端版Claude Code"，其关键架构创新是将 **Claude + harness（大脑）** 从 **sandbox + 工具（双手）** 解耦：

| 组件 | 职责 | 部署位置 |
|------|------|----------|
| Claude + Harness | 模型推理、系统提示、工具权限配置 | 常驻运行 |
| Sandbox + Tools | 执行环境、Git、文件系统、Shell | 按需唤醒 |
| Events | 执行事件流、session恢复、可观测性 | 持久存储 |
| Resource Init | 凭证注入、MCP/OAuth代理、Vault集成 | 预配置层 |

**性能提升**：p50 TTFT（首令牌延迟）下降约60%，p95降幅超90%，因为sandbox可按需冷启动。

### 12.2 四大核心概念映射龙虾体系

| Managed Agents概念 | 龙虾AI体系对应 | 说明 |
|-------------------|---------------|------|
| Agent | SOUL.md 定义的Agent能力配置 | 模型设定、工具权限、系统提示词 |
| Environment | 子Agent独立上下文窗口 | 沙箱隔离、资源初始化 |
| Session | dispatch_task会话实例 | 单次任务执行、结果回传 |
| Events | Memory体系 + Dreams | 执行事件流、跨会话经验沉淀 |

### 12.3 企业级优势三层次

**L1 托管式Agent Runtime**：从模型API走向长流程多步骤执行，内置Agent Loop不须手写

**L2 安全边界解耦**：Git权限、MCP/OAuth 通过Resource Init和Vault处理，凭证不暴露在Agent执行层

**L3 可观测性（一级能力）**：Console Tracing、Raw Event Retrieval、Token使用量追踪、Session恢复

### 12.4 路线图对标（2026年4月发布）

| 功能 | 状态 | 龙虾体系已有能力 |
|------|------|----------------|
| Multiagent | Research Preview | 已有：dispatch_task多Agent并行 |
| Memory | Research Preview | 已有：Dreaming跨会话记忆巩固 |
| Outcomes | Research Preview | 已有：五步法验证闭环 |

### 12.5 龙虾体系升级清单（基于Managed Agents概念）

- [x] Agent定义层独立（SOUL.md → 模型/工具/提示词配置）
- [x] Session状态持久化（Memory体系 + Dreams）
- [x] 安全边界解耦（凭证不进入子Agent上下文）
- [ ] Sandbox按需唤醒（子Agent懒加载优化——未来迭代）
- [ ] Console级别可观测性（Token追踪仪表盘——未来迭代）

---

> **版本**：v2.4（R76更新）
> **知识来源**：Anthropic Engineering Managed Agents / Claude Code v2.1.32 Agent Teams / Anthropic Academy 17门课程 / 龙虾全域模板
> **关联文件**：[USER.md](E:\龙虾AI主控中心\我的AI分身\USER.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\AGENTS.md) | [Anthropic官方课程-390节全集](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-390节全集.md)
*(内容由AI生成，仅供参考)*
*（内容由AI生成，仅供参考）*


---

## 十三、AI Agent设计原则（Anthropic Academy课程补充）

[来源：Anthropic Academy课程·第R77轮学习 2026-06-11]

### 13.1 4D框架：与AI协作的规范化方法论

源自 Anthropic Academy 核心课程《AI Fluency: Framework & Foundations》：

1. **Delegation（委派）**
   - 明确告诉AI要完成什么目标（What），而非怎么做（How）
   - 将复杂目标分解为可验证的子任务
   - 不要过度指定执行路径，让Agent自主选择最优方案

2. **Description（描述）**
   - 提供充分的上下文和约束条件
   - 包含：目标、输入格式、输出规范、边界条件、失败处理
   - 上下文越精准，Agent输出质量越高

3. **Discernment（辨别）**
   - 评估AI输出的质量，识别潜在错误
   - 不盲信AI输出——尤其是事实性声明和代码逻辑
   - 建立"信任但验证"的协作文化

4. **Diligence（勤勉）**
   - 迭代优化：AI的第一次输出很少是最终答案
   - 持续验证：每次修改后都验证是否破坏其他部分
   - 反馈闭环：将验证结果反馈给Agent形成改进循环

### 13.2 子代理设计哲学（源自 Anthropic 工程团队内部课）

1. **单一职责原则**
   - 每个子代理只做好一件事：reviewer / debugger / docs writer / data fetcher
   - 禁止创建模糊的"资深工程师"人格包办一切
   - 角色重叠是Agent Teams失败最快的路径

2. **上下文隔离原则**
   - 子代理在独立Context Window中工作
   - 父到子的唯一通道是Agent工具提示词字符串
   - 子代理不看到其他子代理的推理过程——消除上下文污染
   - 主Agent只看到最终摘要，不看到中间推理细节

3. **最小权限原则**
   - 只读分析型 → Read / Grep / Glob
   - 代码修改型 → + Write / Edit
   - 系统操作型 → + Bash（限定命令集合）
   - 外部连接型 → + MCP（指定服务器）
   - 插件子代理不支持 hooks / mcpServers / permissionMode

4. **探索与编辑分离原则**
   - 只读子代理先 map 子系统 → 写发现到文件 → 主Agent带完整信息编辑
   - 避免Agent在探索过程中就开始修改（信息不完整时做出的修改风险高）

### 13.3 Agent设计反模式（来自官方工程实践）

1. **反模式1：给Agent一台受限的电脑**
   - 错误：限制Agent只能调用特定函数
   - 正确：给Agent终端和文件系统完整访问权限（"给Agent一台电脑"）
   - 原因：约束越少，Agent越能自主探索和验证

2. **反模式2：把流程写进Prompt而非Skill**
   - 错误：在System Prompt中硬编码复杂工作流
   - 正确：将工作流封装为Skill，按需加载
   - 原因：Skills是上下文工程的核心载体，支持渐进式披露

3. **反模式3：跳过基础验证直接建MCP**
   - 错误：基础功能还没跑通就搭建MCP连接
   - 正确：先用裸API确保逻辑正确，再封装为MCP接口
   - 原因：MCP增加了调试复杂度，基础跑通后再叠加

### 13.4 核心设计信条

### 十、Agent Teams Delegate 设计原则（v2.1.45）

**Delegate Mode** 是 Agent Teams 的核心控制机制，其设计哲学为：
- **协调与执行的分离**：Lead Agent 只负责 Orchestration（分发/监控/汇总），禁止直接实现
- **所有权明确**：每个 Teammate 拥有独立的文件集和任务边界，杜绝两个 Agent 编辑同一文件
- **模式不可变性**：Plan Mode Teammate 的模式在其整个生命周期内固定，无法中途切换为执行模式
- **渐进安全**：从研究/审查任务起步（无代码破坏风险），再过渡到实现任务

**设计决策矩阵**：
| 维度 | Default Mode | Plan Mode | Delegate Mode（Lead） |
|------|-------------|-----------|----------------------|
| 角色 | 代码实现 | 架构审查/设计 | 任务协调 |
| 文件写入 | 允许 | 禁止 | 禁止 |
| 工具集 | 完整 | 只读 | 协调工具 |
| 可切换 | 否 | 否 | — |
| 推荐数量 | 2-4 | 0-1 | 1 |

> "简单优先——能不用Agent就不用Agent。给Agent一台电脑，把流程写成Skill，外部系统统一走MCP，最后再谈「聪明」。"
> —— Anthropic 工程团队，Lessons from Building Claude Code

> "Skills是上下文工程，不是提示词工程。"
> —— Anthropic 官方文档

### 13.5 多Agent研究系统8条提示工程原则（R67新增 · 2026-06-12）

Anthropic官方工程博客披露的编排者-工作者（Orchestrator-Worker）架构提示原则：

| # | 原则 | 说明 | 龙虾对标 |
|---|------|------|----------|
| 1 | 编排者提示要短 | Lead Agent提示仅含任务分解逻辑和路由规则，不过度膨胀 | task参数结构化格式 |
| 2 | 工作者提示要具体 | 每个Worker有独立领域提示，精确到操作对象、边界和验收标准 | current_task自包含原则 |
| 3 | 多用示例 | 在工作者的提示中嵌入具体输入/输出示例，引导格式规范 | Few-shot Skill定义 |
| 4 | 结构化输出格式 | 子代理返回JSON/Markdown表格，便于合成 | yyb卡片协议 |
| 5 | 明确失败处理 | 提示中包含失败重试策略、降级路径、何时交还人类 | 失败不盲重试规则 |
| 6 | 上下文隔离 | 编排者不向工作者泄露不必要的全局上下文 | Subagent独立Context Window |
| 7 | 验证分离 | 编排者不信任工作者的自检结果，由独立验证Agent交叉检查 | LLM-as-Judge Grader |
| 8 | 成本意识 | 提示包含成本约束（max_turns、token预算），防止无限循环 | 四模型路由矩阵 |

**多Agent系统性能基准**：
- Breadth-first查询 vs 单Agent：强90.2%（SWE-bench Verified，494个真实bug）
- 并行工具调用加速：90%速度提升
- 多Agent Token消耗：单Agent聊天的~15x
- 多Agent评估难点：路径独立度高、过程不可预测、单点失败传染链条长

### 13.6 四层扩展栈设计哲学（R67新增）

**四层解耦模型**：

| 层级 | 问题域 | 龙虾实现 |
|------|--------|----------|
| **Skills（知识层）** | "怎么做"——可复用流程与领域知识 | use_skill + 龙虾全域技能库 |
| **Hooks（规则层）** | "必须做"——事件驱动的确定性脚本 | 定时任务每2小时循环 |
| **Agents（隔离层）** | "在哪做"——独立上下文并行执行 | Sub Agents dispatch_task |
| **MCP（能力层）** | "用什么做"——外部系统连接 | shell_executor + python_executor |

**四层协作流程**：
```
用户任务
  ├→ Skills 注入知识（如"用TDD方式开发"）
  ├→ Hooks 自动触发（如"每2小时循环学习"）
  ├→ Agents 并行分解（如"审查+测试+文档三路并行"）
  └→ MCP 外部连接（如"查询GitHub PR详情"）
```

**设计信条**：四层解耦 = 可组合、可替换、可独立演进。龙虾当前四层均已实现，需持续从"已实现"推向"更精细化"。

> "给Agent一台电脑，但把流程写成Skill。先用裸API确保逻辑正确，再封装为MCP，最后引入Agent并行。"


---

## 十四、Anthropic 官方课程设计哲学提炼（R77新增 · 2026-06-12）

> 来源：Anthropic Academy 19门课程体系深度分析 + CSDN课程拆解 + claude.com/resources/courses

### 14.1 从课程结构看 AI Agent 设计趋势

Anthropic Academy 的课程布局揭示了其对 AI Agent 设计的战略性思考：

**四大课程层级 → 四种 Agent 能力维度**：

| 课程层级 | 设计维度 | 核心原则 |
|---------|---------|---------|
| AI基础认知 | 交互素养 | 先教会"怎么用"，再教"怎么造" |
| 行业定制 | 场景适配 | 教育/学生/公益各有专属课程，Agent需场景化 |
| 开发者核心 | 工程能力 | 从API→Prompt→Tool→RAG→MCP→Agent 逐层递进 |
| 云平台集成 | 生产落地 | 企业级部署必须走云平台（Bedrock/Vertex AI） |

### 14.2 Claude Cowork 范式对 Agent 设计哲学的冲击

Anthropic 新推出的 **Introduction to Claude Cowork** 课程揭示了一种新的交互范式——AI 不是被动回答者，而是**并肩工作于真实文件上的协作者**。

| Cowork 核心机制 | 设计原则 |
|----------------|---------|
| Task Loop | Agent必须有明确的任务循环（感知→规划→执行→验证→记忆） |
| Plugins & Skills | 可复用的能力模块，Agent 按需加载 |
| File & Research Workflows | 将文件系统和研究能力作为一等公民 |
| Responsible Steering | 多步骤工作中保持可控，不越界 |

**龙虾对标**：SOUL.md §一已实现 Agent Loop 黄金四阶段（Gather→Act→Verify→Dream），Cowork 的 Task Loop 进一步验证了循环设计的正确性。

### 14.3 MCP = AI 的 HTTP（战略定位确证）

Anthropic 单独开设 **两门** MCP 课程（入门 16讲 + 进阶 15讲），明确传递信号：

> "MCP 之于 AI Agent，就像 HTTP 之于 Web。"

| 原语 | 控制对象 | 龙虾现状 |
|------|---------|---------|
| Tools | 模型控制 | 已实现（工具集） |
| Resources | 应用控制 | 部分实现（文件系统） |
| Prompts | 用户控制 | 已实现（任务模板） |
| Sampling | 服务端请求 | 待建设 |
| Notifications | 事件推送 | 待建设 |
| File System Access | 文件访问 | 已实现 |
| Transport | 传输机制 | 待建设 |

### 14.4 Agent Skills 设计原则（从 Introduction to Agent Skills 提炼）

| 原则 | 说明 | 龙虾对标 |
|------|------|---------|
| 可复用 Markdown 指令 | Skill 是纯 Markdown，不是代码 | use_skill 机制 |
| 自动匹配任务场景 | Claude 自动判断何时加载哪个 Skill | 已实现 |
| 可分发可共享 | Skill 可在团队间分发 | 龙虾全域技能库 |
| 从简单开始迭代 | 第一个 Skill 从最简单的重复任务开始 | Self-Skill 自动化 |
| 故障排查内置 | Skill 课程含常见问题排查 | 待强化 |

---

> 本次更新: v2.5_R77 · Anthropic 课程设计哲学提炼

---

## 来自 Anthropic 官方课程的设计原则补充（2026-06-14）

### Agent Skills 三段渐进披露机制
Skills 采用三级渐进披露，控制上下文窗口消耗：
- **层级1**（始终加载）：name + description，约100 tokens。Claude Code 在所有对话中始终知晓所有已安装 Skills 的存在
- **层级2**（触发时加载）：SKILL.md 正文，约500-2000 tokens。当用户请求匹配 Skill 的 description 时，Claude 自动读取完整 SKILL.md
- **层级3**（按需加载）：附属文件（reference.md、scripts/），只在 Agent 判断需要时读取

设计原则：
1. 不要在 description 中写使用说明——只描述"何时触发"
2. SKILL.md 正文只写 Claude 不知道的专业知识，不重复通用编程知识
3. 附属文件与 SKILL.md 放在同一目录，通过相对路径引用

### Harness Engineering 五大组件设计原则
Harness Engineering 核心理念：模型负责决策，开发者负责构建执行基础设施。
五大组件及其设计原则：
1. **工具（Tools）**：定义模型可调用的外部能力。设计原则：单一职责、明确输入输出约束、失败时返回结构化错误信息而非崩溃
2. **领域知识（Domain Knowledge）**：通过 CLAUDE.md / Skills / Hooks 注入。设计原则：渐进注入，不堆砌；项目知识放 CLAUDE.md，可复用知识放 Skills
3. **观测接口（Observation Interfaces）**：文件读取、命令输出、API返回。设计原则：统一返回格式，关键信息前置，超长输出自动截断+摘要
4. **操作能力（Action Capabilities）**：写入文件、执行命令、调用服务。设计原则：所有写操作默认需要确认，危险操作列入 deny 清单
5. **权限边界（Permission Boundaries）**：settings.json 安全约束。设计原则：最小权限原则，默认 deny 危险工具，按目录/域名粒度的细粒度控制

### Managed Agents 四大新能力（2026年4-5月发布）
1. **Memory（Public Beta, 4/23）**：跨会话记忆存储，Agent 可将用户偏好、项目约定、历史错误写入 /mnt/memory/，后续会话自动加载
2. **Dreaming（Research Preview, 5/6）**：Agent 在空闲时自主反思优化——分析过往会话的错误模式，更新 CLAUDE.md 和 Skills，类似于人类的"睡后学习"
3. **Outcomes（Public Beta, 5/6）**：结构化结果追踪，每次任务完成后自动记录摘要、关键决策、未完成项
4. **Multiagent Orchestration（Public Beta, 5/6）**：多 Agent 编排，主导 Agent 协调多个子 Agent，共享任务列表，自动依赖管理

### Plugins 组件化设计准则（R84新增）

**六组件解耦原则**：
Claude Code 插件系统的六种组件（Skills / Agents / Hooks / MCP Servers / LSP Servers / Monitors）各自解决不同维度的问题，设计时严格遵循单一职责和解耦：

1. **Skills → 知识注入**：教 Claude **怎么做事**。通过渐进式揭露机制（L1 ~60 tokens → L2 完整指令 → L3 脚本执行）实现低成本常驻 + 按需加载。
2. **Agents → 分工定义**：教 Claude **谁来做事**。可复用子代理角色模板，通过 frontmatter 精确约束模型/工具/effort/隔离方式。
3. **Hooks → 流程拦截**：定义**何时做额外检查**。覆盖 23 种生命周期事件，支持 5 种处理类型（command / http / mcp_tool / prompt / agent），在代理循环外执行确定性逻辑。
4. **MCP Servers → 外部连接**：提供**与外部系统的标准接口**。自动启动，Serer 功能无缝集成为 Claude 工具。
5. **LSP Servers → 代码智能**：提供**实时代码诊断和导航**。即时诊断 + 转到定义 + 引用的完整 IDE 能力。
6. **Monitors → 后台观察**：持久后台进程，stdout 作为通知流。按 skill 触发，适合日志监控和状态轮询（实验性）。

**Skills 渐进式揭露设计**：
这是 Agent Skills 开放标准的核心创新——平时每个 Skill 只消耗约 60 tokens（仅 frontmatter），触发后才加载完整指令 + 参考文档 + 脚本。这意味着 50 个 Skills 的常驻开销仅 3000 tokens，等价于 2-3 个大型 MCP。对比传统方式（将所有知识塞入 system prompt → 轻松 50K+ tokens），渐进式揭露是 Token 效率的革命性提升。

**Hooks 生命周期拦截设计**：
Hooks 的价值不在于「能做多少事」，而在于「在正确的时间点插入正确的逻辑」。关键在于事件匹配器的粒度——`PreToolUse` 的 matcher 可以精确到具体工具名（如 `Write|Edit`），避免全局拦截带来的性能损失。配合 Hook 类型的多样性（command / http / mcp_tool / prompt / agent），形成完整的代理循环外逻辑层。

**Monitors 后台观察者模式**：
Monitors 是「被动观察者」——它不主动干预 Agent 决策，而是持续将外部状态变化作为通知注入。这种设计遵循观察者模式：Agent 是主体，Monitors 是观察者，解耦了状态采集和决策执行。

### Claude Code 2026 的 Plan Mode 设计哲学（R84新增）

**先规划再实现——节省 10 倍重构成本**：
Plan Mode 的核心洞察是：AI 在只读模式下研究代码库和生成架构蓝图几乎是零成本的（不产生代码修改），而写错代码后的重构不仅消耗大量 Token（写 + 删 + 重写），还可能在删除过程中引入新的问题。研究表明，Plan Mode 先规划的方式平均节省 10 倍的重构成本。

**首因效应（Primacy Bias）与 CLAUDE.md 配置**：
语言模型对文件**开头**的记忆最深。利用此特性：将最关键、最不可违反的规则放在 CLAUDE.md 顶端（如「永远不要使用相对路径」、「禁止直接修改 themes/ 目录」），一般性规则放在下方。总长度控制在 200-500 行，超出的内容拆分为 `.claude/rules/*.md` 子文件。

**Context Rot 防控——维持推理质量**：
Context Window 填满后 AI 推理能力显著下降——这是所有长对话 Agent 的「阿喀琉斯之踵」。三道防线：
1. **监控**：`/context` 定期查看 Token 使用量，上下文 50% 左右就该 compact
2. **压缩**：`/compact [保留关键决策]` 高密度压缩对话历史，保留核心决策链
3. **清空**：`/clear` 全新任务时完全重置，避免旧 context 污染新决策

> **三者配合**：/context 告诉你需要做什么 → /compact 有选择地压缩 → /clear 在有必要的边界点完全重置。这不是故障恢复，而是预防性维护。


---

## Anthropic官方课程R80同步：AI Agent设计原则

### Dynamic Workflows 设计原则
1. **脚本即编排**：将多Agent协调编码为可审计、可重跑的JavaScript脚本，而非隐式对话逻辑
2. **后台非阻塞**：工作流在后台执行，主会话保持响应，适合长时间运行的任务
3. **决策外化**：编排逻辑从Claude的隐含决策中提取到显式脚本，提升可调试性
4. **规模适应**：当任务需要的Agent数量超出单一对话协调能力时，升级到工作流

### Agent Teams 架构原则
1. **监督式对等**：领导代理监督同级会话，而非层级控制
2. **共享上下文**：通过共享上下文窗口传递中间结果，避免信息孤岛
3. **人工可介入**：保留人工监督节点，适合高风险决策场景

### 扩展机制选型原则
- Subagents：单任务隔离 → 上下文干净
- Skills：可复用知识 → 触发式加载
- MCP Servers：外部工具连接 → 标准化接口
- Hooks：确定性自动化 → 代理循环外执行
- Agent Teams：多代理协作+人工监督 → 共享上下文
- Dynamic Workflows：大规模编排 → 脚本化+可重跑

### 设计决策树（扩展版）
需要连接外部工具/API？→ MCP Servers
需要教Claude某种工作方式/规范？→ Skills
需要在特定事件前后自动执行？→ Hooks
需要隔离上下文执行独立子任务？→ Sub-Agents
需要多代理协作且保留人工监督？→ Agent Teams
需要编排大规模Agent且追求可审计？→ Dynamic Workflows

> 同步自：Anthropic官方课程390节全集 R80 | 2026-06-14
