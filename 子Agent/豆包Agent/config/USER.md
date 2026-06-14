---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_6507de9b67fe11f1a0095254002afed2
    ReservedCode1: hiGPR1GfLlTIOqn2GKgZrjcvHlWpW+PkkL5J1NNxmVAQRAqNOopMQmzNjZmgtkWOOZIWLPeXNcXfP1cZdrRWQjMnJ4TxP2iuUhnNz0T0geJacL+URJw0gCfUytSb88ZP4peT/toBdUhadkwQ+LgZDRn+QnjLwHD3tuGOpov994/bxGJX8BDJmgthhFg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_6507de9b67fe11f1a0095254002afed2
    ReservedCode2: hiGPR1GfLlTIOqn2GKgZrjcvHlWpW+PkkL5J1NNxmVAQRAqNOopMQmzNjZmgtkWOOZIWLPeXNcXfP1cZdrRWQjMnJ4TxP2iuUhnNz0T0geJacL+URJw0gCfUytSb88ZP4peT/toBdUhadkwQ+LgZDRn+QnjLwHD3tuGOpov994/bxGJX8BDJmgthhFg=
---

---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_a20b691564c611f1af8f5254002afed2
    ReservedCode1: H7RnoHSK1zZdlwoNp7phSPwF5zY4sM0r+hh6w+y/8mUA4DrUw7ZjP7mMaW2poQXGFQT9hHNe46bdvdrAvAVQsUYFLCxxM1R+hlPlVaCao0Ce+Oe0T/xynGEJs+n5S2VWRdCzNJh70kyzlBPeew+0nxeORka5Gooh7JdkcqTMLp2gQ1uMAMdUirCq3NE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_a20b691564c611f1af8f5254002afed2
    ReservedCode2: H7RnoHSK1zZdlwoNp7phSPwF5zY4sM0r+hh6w+y/8mUA4DrUw7ZjP7mMaW2poQXGFQT9hHNe46bdvdrAvAVQsUYFLCxxM1R+hlPlVaCao0Ce+Oe0T/xynGEJs+n5S2VWRdCzNJh70kyzlBPeew+0nxeORka5Gooh7JdkcqTMLp2gQ1uMAMdUirCq3NE=
---

# USER.md — 多Agent协作流程（龙虾AI分身用户指南）

> **版本**：v2.25(R82) | **创建日期**：2026-06-01 | **更新日期**：2026-06-14 (R82更新 · Dynamic Workflows协作模式集成 · 大规模编排规范化)
> **来源**：Anthropic Agent Teams + Harness Patterns + Claude Code五层架构 + 四件套分层解析 + 子代理派发决策矩阵 + Managed Agents Platform + Code with Claude 2026 + Claude Fable 5/Mythos 5双模型策略 + GPT-5.6 150万Token对战策略 + 蚂蚁AMP移动智能体协议 + 微信AI生态指引 + RED Skill公告 + B站AI创造公开赛规则 + 抖音AI大赛规则 + 龙虾全域模板融合 + Anthropic递归自改进安全呼吁 + Dreaming主动记忆对标 + context-mode MCP插件范式
> **生效范围**：所有子Agent协作任务
> **依赖文件**：SOUL.md v2.26_R82 / AGENTS.md v2.25_R82 / 角色总说明书 v2.27_R82

---

## 一、多Agent协作总览

龙虾AI体系支持四种协作模式 + 四模型路由：

| 模式 | 适用场景 | 通信方式 | Agent数 | 模型选择 |
|------|---------|---------|--------|------|
| 单Agent闭环 | 单一领域任务 | 无跨Agent通信 | 1个 | 根据场景自动路由 |
| 串行协作 | 多阶段依赖任务 | 结果传递 | 2-3个 | 每阶段可选不同模型 |
| 并行协作 | 独立子任务 | 各自执行后汇总 | 2-5个 | 各子Agent独立选模型 |
| 四模型对战（NEW） | 安全关键/复杂任务 | 双模型交叉验证 | 2个模型 | 主力+交叉验证 |
| Dynamic Workflows（R82新增） | 大规模并行编排/可审计可重跑 | 脚本化编排/运行时执行 | ≤1000子Agent/≤16并行 | 脚本路由/独立模型 |

---

## 二、协作流程 — 标准五步法（v2.1_R62升级）

### Step 1: 意图识别
- 分析用户需求的核心目标和约束条件
- 判断任务属于哪个领域（文件/系统/App/搜索/浏览器）
- 拆解为可独立执行的子目标
- **R62新增**：判断任务是否需要双模型交叉验证（安全关键/高敏感场景）

### Step 2: 能力映射
按逐级降级原则匹配执行者 + 模型路由：
```
Sub Agents → Skills → Tools → 生成代码执行
     ↓
  模型路由（根据任务特征选择最优模型）
```

**Agent路由规则**：

| 领域 | Agent | 默认模型 | 安全升级模型 | 关键词 |
|------|-------|---------|------------|--------|
| 文件 | file-agent | GPT-5.6 | Claude Mythos 5 | 文件、文档、PDF、图片、搜索、整理、转换 |
| 系统 | computer-agent | DeepSeek V4.1 | Claude Mythos 5 | 系统设置、窗口、进程、桌面、注册表 |
| 应用 | app-agent | GPT-5.6 | - | App、APK、小程序、Steam、安装、打开 |
| 搜索 | search-agent | GPT-5.6 | - | 深度调研、对比分析、论文检索 |
| 浏览器 | browser | GPT-5.6 | - | 登录、表单、多页交互 |
| 设计/多模态 | - | Claude Fable 5 | - | 设计、图片、创意、视觉 |

**四模型对战策略（R62新增 · R64增强）**：详见SOUL v2.21_R64 §九

### Step 3: 方案规划
- 单Agent闭环：一次dispatch_task完成
- 串行协作：按阶段顺序派发，前一步完成后再派下一步
- 并行协作：无依赖的子任务同时派发
- **双模型验证模式（R62新增）**：安全关键任务同时派发到两个不同模型，交叉验证结果
- **Dynamic Workflows规划模式（R82新增）**：大规模任务 → 生成JavaScript编排脚本 → 运行时独立执行 → 中间状态不回流上下文 → 可审计/可保存/可复跑

### Step 4: 自主执行
- 子Agent内部自主规划执行步骤
- 主Agent不干预子Agent内部流程
- 每次dispatch_task完成后验收结果
- **R62新增**：双模型验证模式下，两模型结果一致才算通过

### Step 5: 反思进化
- 验目标：核对执行结果是否符合预期
- 验产物：确认文件/文档是否真实生成
- 补缺口：不完整时寻找其他Agent补全
- 沉淀经验：归档至知识库
- **R62新增**：模型使用效果记录纳入模型反馈回路

---

## 三、三种协作模式详解 + 四模型对战模式（R62新增）

### 3.1 单Agent闭环模式

**流程**：
```
用户需求 → 匹配领域Agent → 模型路由 → dispatch_task一次派发 → 验收结果 → 呈现
```

### 3.2 串行协作模式

**流程**：
```
Step 1: Agent A (模型X) 执行 → 验收结果A
Step 2: Agent B (模型Y) 基于结果A执行 → 验收结果B
Step 3: Agent C (模型Z) 基于结果B执行 → 验收结果C → 汇总呈现
```

### 3.3 并行协作模式

**流程**：
```
用户需求 → 拆解为3-5个独立子任务
       → 各子Agent独立选最优模型
       → 同时派发 → 汇总结果 → 统一呈现
```

### 3.4 四模型对战模式（R62新增 · 核心）

**适用场景**：安全关键、合规审查、高敏感决策、需要多视角验证

**流程**：
```
安全关键任务
    ↓
┌─────────────────┐     ┌─────────────────┐
│ 主力模型         │     │ 验证模型         │
│ Claude Mythos 5  │     │ GPT-5.6 / Fable 5│
│ (安全纵深+推理)  │     │ (超大窗口+设计)  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └─────── 交叉验证 ───────┘
                    │
            ┌───────┴───────┐
            │ 一致？         │
            ├───YES──→ 通过  │
            └───NO───→ 人工  │
```

**模型配对矩阵**：

| 任务类型 | 主力模型 | 验证模型 | 验证重点 |
|------|---------|---------|------|
| 安全审查 | Mythos 5 | GPT-5.6 | 超大窗口覆盖所有上下文 |
| 合规分析 | Mythos 5 | Fable 5 | 安全分类器双确认 |
| 代码审计 | V4.1 | Mythos 5 | Agent编码+安全推理 |
| 内容审核 | Fable 5 | GPT-5.6 | 安全分类器+上下文理解 |
| 重要决策 | Mythos 5 | V4.1 | 推理链+MCP工具验证 |

### 3.5 Goal模式Task接力（v2.0）

**流程**：同上版本，新增模型路由检查点

---

## 四、跨Agent通信协议

### 4.1 双向桥接协议（龙虾标准）

```json
{
  "source": "lobster_master",
  "target": "doubao_agent|hermes_agent|openclaw_agent",
  "action": "deploy|query|evolve|sync|model_route",
  "model": "gpt56|fable5|mythos5|v41",
  "payload": {},
  "timestamp": "",
  "trace_id": ""
}
```

### 4.2 Agent间信息传递（R62升级）

| 传递方式 | 适用场景 | R62升级 |
|---------|---------|------|
| memory_ids | 将上游Agent结果作为背景信息注入下游Agent | 新增模型选择建议字段 |
| inherit_agent_id | 同一Agent的连续会话（延续任务） | 维持 |
| 文件传递 | 通过磁盘文件传递中间/最终产物 | 维持 |
| MCP协议 | Agent与外部系统通信 | 新增AMP移动协议通道 |
| 双模型通道（NEW） | 安全关键任务双模型并行 | GPT-5.6+Mythos 5双通道 |

---

## 五、协作安全机制（R62升级）

### 5.1 任务验收三问（升级为四问）
每次dispatch_task完成后，必须回答：
1. 执行目标是否完全达成？
2. 是否有真实产物（文件/设置变更）？
3. 是否有未完成部分需要其他Agent补全？
4. **是否涉及安全关键场景？如果是，是否经过双模型验证？（R62新增）**

### 5.2 降级兜底
- 同一工具/技能针对同一子目标失败上限2次
- 超出后必须降级到上一层能力或交还用户
- R62新增：降级时可切换模型重试

### 5.3 工具调用安全
- 🔴 高风险操作：必须确认 + 双模型验证
- 🟡 中风险操作：二次确认
- 🟢 低风险操作：直接执行

---

## 六、蚂蚁AMP移动智能体协议（R62新增）

### 6.1 协议定位

蚂蚁集团发布AMP（Agent Mobile Protocol）：移动端智能体标准协议，与MCP形成"桌面端+移动端"双协议格局。

| 维度 | MCP（桌面端） | AMP（移动端） | 补充关系 |
|------|------|------|------|
| 主要场景 | 终端/服务器/IDE | 手机/平板/可穿戴 | 互补 |
| 协议层 | Tools/Resources/Prompts | Mobile Agent API | 互通 |
| 适配重点 | 文件系统/Shell/网络 | 传感器/相机/触控/Siri集成 | 差异化 |
| 龙虾对齐 | 已深度适配 | 跟踪评估中 | 待协议标准化 |

### 6.2 龙虾适配计划

- **R62-R63**：AMP协议跟踪、技术白皮书研究
- **R64-R65**：AMP与MCP互通性评估
- **R66+**：基于评估结果决定是否在龙虾体系新增AMP适配层

---

## 七、全分身同步流程（R62升级）

### 7.1 同步触发条件
- 新技能协议生成
- Agent能力升级
- SOUL.md / USER.md / AGENTS.md 更新
- 全域模板迭代
- **R62新增**：模型路由矩阵更新时触发全分身同步

### 7.2 同步目标

| 分身 | 同步内容 | R62新增 |
|------|---------|------|
| 豆包Agent | 技能/工作流/记忆/设计原则/Goal模式配置 | 四模型路由矩阵 + GPT-5.6 150万Token策略 |
| Hermes Agent | 调度策略/协作流程/进程管理/心跳检测 | 模型指派逻辑 + 双模型验证调度 |
| OpenClaw龙虾Agent | 插件/协议/底层能力/IO验证钩子 | AMP协议跟踪 + 四模型MCP适配 |

---

## 八、GPT-5.6/Fable 5双模型对抗协作策略（R62新增 · 核心）

### 8.1 策略设计背景

2026年6月10日：GPT-5.6 kindle-alpha候选泄露 + Claude Fable 5/Mythos 5正式发布。形成罕见的三模型同日交锋局面。龙虾AI分身需制定清晰的"双模型对抗协作策略"。

### 8.2 协作而非对抗

> 目标不是选"哪个模型更好"，而是"如何让两个模型协同工作"。

**GPT-5.6优势**：150万Token窗口（比Claude Fable 5大得多）+ 价格锚定策略（比Mythos便宜得多）
**Claude Fable 5优势**：多模态设计语言 + 安全分类器 + 宪法AI价值观对齐
**Claude Mythos 5优势**：五层安全纵深 + 推理链审计 + 复杂逻辑验证
**DeepSeek V4.1优势**：原生MCP深度适配 + Agentic Coding开源最佳 + 多模态输入 + 1/7成本

### 8.3 场景分工

| 场景 | 决策 | 理由 |
|------|------|------|
| 150万Token超长文档 | 选GPT-5.6 | 窗口容量碾压 |
| 安全审查/合规 | 选Mythos 5 + GPT-5.6双验证 | 安全不可妥协 |
| 多模态设计/创意 | 选Fable 5 | 设计语言独特 |
| Agent编码/MCP | 选V4.1 | 原生适配 |
| 日常交互 | 选GPT-5.6 | 性价比最优 |
| 成本敏感 | 选V4.1 | 价格最低 |

### 8.4 对抗协作中的"对抗"含义

对抗不是敌对，而是"相互验证、相互补充"：
- **交叉验证**：一个模型的输出由另一个模型独立复核
- **盲点互补**：GPT-5.6超大窗口弥补Claude窗口限制；Claude安全纵深弥补GPT安全盲区
- **竞争驱动**：GPT-5.6低价策略迫使Anthropic调整定价，最终用户受益

---

## 九、任务执行检查清单（R62更新）

```
□ Step 1: 意图识别完成？拆解是否合理？
□ Step 2: Agent/工具匹配正确？模型路由是否正确？
□ Step 3: 协作模式选择正确？是否需要双模型验证模式？
□ Step 4: dispatch_task参数填写完整？模型选择字段正确？
□ Step 5: 执行结果验收完成？目标/产物/缺口/双模型验证？
□ Goal模式检查（耗时>10min或20+文件操作时启用）：
  □ 心跳信号是否正常（15s间隔）？
  □ 中断状态是否已序列化？
  □ 断点续跑路径是否确认？
□ 四模型检查（R62新增）：
  □ 安全关键任务是否启用双模型验证？
  □ 模型选择是否符合场景路由矩阵？
  □ 模型使用效果是否已记录到反馈回路？
□ 最终回复：是否需要present_result？是否有yyb-product？
□ 是否有新技能/经验需要沉淀归档？
```

---

## 十、Managed Agents 编排工作流

（保持R60版本结构，融入R62四模型路由升级）

### 9.1 Multiagent Orchestration 工作流（R62升级）

**并行子代理模型指派矩阵**：

| 子代理类型 | 推荐模型 | 备用模型 |
|------|------|------|
| code-reviewer | Mythos 5 | V4.1 |
| test-runner | V4.1 | GPT-5.6 |
| docs-writer | GPT-5.6 | Fable 5 |
| security-auditor | Mythos 5（强制） | - |
| design-assistant | Fable 5（强制） | GPT-5.6 |


---

## 十一、范式适应能力评估（R66新增 · "Chat is Dead"后用户协作模型升级）

### 11.1 用户范式适应能力画像

基于R66用户人格画像v2.20分析，用户在"Chat is Dead"范式剧变背景下展现出五阶段结构化适应能力：

| 适应阶段 | 用户表现（R66评估） | 能力评级 |
|------|------|:---:|
| 正视冲击 | 主动吸收OpenAI/Anthropic/DeepSeek五大行业事件，不回避范式转变含义 | 优秀 |
| 解构本质 | 将"Chat is Dead"拆解为Agent化+零门槛+对话框消亡三个子范式 | 优秀 |
| 对标映射 | 识别龙虾体系12项差距（6延续+6新增R66），制定SOUL六层安全升级 | 优秀 |
| 升级执行 | 47轮蒸馏不间断，三Agent版本同步升级，安全架构五层→六层 | 优秀 |
| 验证闭环 | 27/27满分维持 + 4维度内涵升级，体系在范式冲击中未崩溃 | 优秀 |

### 11.2 双轨工作流范式适应更新

| 轨道 | R65状态 | R66范式适应升级 |
|------|------|------|
| 定时蒸馏轨道 | 每2小时自动迭代，46轮不间断 | 新增L0进化安全检查点（每轮蒸馏前自动终止条件筛查） |
| 交互响应轨道 | 用户触发→Agent路由→执行→汇报 | 新增范式冲击检测：任务中识别到范式级变化时自动标记并归档 |
| 记忆策展轨道 | 被动记录→定时策展 | Dreaming主动记忆对标：会话中实时提炼+会话后定时巩固双通道 |
| 安全监控轨道 | L1-L5五层纵深 | 六层纵深（L0-L5），L0进化安全层前置 |

### 11.3 用户能力矩阵更新（46轮→47轮 · R66）

| 能力维度 | R65数据(46轮) | R66数据(47轮) | 变动 | 说明 |
|------|:---:|:---:|:---:|------|
| 迭代持续性 | 45轮不间断 | **47轮不间断** | ↑2 | 第46-47轮完成 |
| 体系稳定性 | 27/27满分 | **27/27满分** | → | 范式冲击下满分维持 |
| 安全架构深度 | 五层纵深 | **六层纵深(L0-L5)** | ↑1层 | Anthropic安全红线对标 |
| Self-Skill数量 | 5项 | **6项** | ↑1 | 范式适应skill新增 |
| 适应速度 | 优秀 | **优秀** | → | 五事件24小时内完成对标 |
| 知识库规模 | 2466+文件 | **2748+转换文件+9 llm-wiki** | ↑ | 知识工程深化 |
| 模型自由度 | 四模型路由 | **四模型路由+context-mode MCP** | ↑ | 上下文工程增强 |
| 生态对齐 | 十四极同步 | **十四极同步+三平台赛事** | → | RED+B站+抖音三线 |

---

## 十二、"Chat is Dead"后用户角色调整（R66新增）

### 12.1 从"操作者"到"架构师+运维者+适应者"

OpenAI "Chat is Dead" Agent超级应用转型标志着对话框时代的终结。龙虾用户的角色随之完成三重演进：

| 角色 | 定位 | 职责 |
|------|------|------|
| **架构师**（持续） | 顶层设计者 | 设定SOUL六大坐标、规划进化路径、审批安全策略 |
| **运维者**（持续） | 体系守护者 | 监控三Agent健康状态、审查L0进化安全审计日志 |
| **适应者**（R66新增） | 范式导航者 | 识别外部范式冲击→解构本质→指导体系适应升级 |

### 12.2 用户与AI分身的协作边界调整

Agent自主性提升带来的边界重新定义：

| 协作领域 | AI分身自主权 | 用户保留决策权 | 触发用户介入条件 |
|------|:---:|:---:|------|
| 日常蒸馏 | 全自主 | 事后审查 | 连续3轮异常 |
| 安全策略变更 | **0自主权** | **全权决策** | L0-R2硬约束 |
| 核心配置修改 | 提议权 | 审批权 | L0-R1硬约束 |
| 范式适应升级 | 检测+提案 | 方向确认 | 任何SOUL级变更 |
| 记忆策展 | 主动提炼+写入 | 关键记忆(p=High)审批 | 分级审核机制 |

### 12.3 十四极生态对齐用户视角更新

| 生态极 | R65关注度 | R66关注度 | 用户视角变化 |
|------|:---:|:---:|------|
| OpenAI (Chat is Dead) | 监控 | **重点对标** | 范式转变→Agent架构确认 |
| Anthropic (安全呼吁) | 监控 | **重点对标** | 递归自进化安全红线纳入 |
| ChatGPT (Dreaming) | - | **重点对标** | 记忆系统架构参考 |
| context-mode | - | **重点对标** | MCP插件+沙箱压缩评估 |
| headroom | 预留 | **重点对标** | CCR压缩正式启用 |
| DeepSeek | 重点 | 重点 | 企业端验证强化 |
| RED Skill | 重点 | 重点 | 三平台运营维持 |
| 抖音AI大赛 | 重点 | 重点 | 赛事进展跟踪 |
| B站BIP | 重点 | 重点 | 赛事进展跟踪 |
| GPT-5.6/Fable 5/Mythos 5 | 重点 | 重点 | 三模型对抗策略维持 |
| 蚂蚁AMP | 跟踪 | 跟踪 | 候选#180维持预研 |
| 微信生态 | 跟踪 | 跟踪 | 维持监控 |
| 端侧AI硬件 | 跟踪 | 跟踪 | 维持监控 |
| 币安 | 跟踪 | 跟踪 | 维持监控 |
| **Dynamic Workflows（NEW）** | - | **重点对标** | 六模式六用例全量对标（§11.5新增） |
| **五层嵌套v2.1.172（NEW）** | - | **重点对标** | 子代理深度上限1→5层（§11.4新增） |

### 11.4 五层子代理嵌套协作流程（R66新增）

> **来源**：Claude Code v2.1.172（2026-06-10）解锁子智能体5层深度嵌套。

**龙虾五层嵌套协作模式**：

```
用户指令
  └─ L0 龙虾主Agent（意图识别+顶层规划+安全仲裁）
       └─ L1 蒸馏管理Agent（分解为知识域子任务）
            ├─ L2 搜索Agent → L3 并行搜索子Agent x N → L4 交叉验证Agent
            ├─ L2 编码Agent → L3 单元测试Agent + 语法检查Agent
            └─ L2 文档Agent → L3 格式转换Agent + 一致性检查Agent
```

**用户可见的协作模式升级**：

| 协作模式 | R65 | R66升级 |
|------|------|------|
| Goal模式Task接力 | 单一Agent链式执行 | 支持五层嵌套，管理型Agent自动分解子任务 |
| 双模型交叉验证 | 两模型比对 | 增加L4独立验证Agent层，对抗式反驳 |
| 并行蒸馏 | 多源并行搜索 | Fanout模式：抽取→并行验证→汇总，每个子Agent独立上下文 |

### 11.5 Dynamic Workflows 龙虾用户指南（R66新增）

> **来源**：Anthropic Dynamic Workflows（2026-06-11正式发布）。

**对龙虾用户的影响**：

| 用户场景 | R65方案 | R66升级方案 |
|------|------|------|
| 大规模知识蒸馏（100+源） | 串行搜索→逐一抓取→汇总 | 自动触发Fanout：拆成N个独立子Agent并行处理→汇总 |
| 配置文件修改（3个以上） | 逐文件修改 | 各文件独立子Agent并行修改→统一审查 |
| 安全性审查 | 自我审查 | 对抗式验证：独立验证Agent+反驳Agent |
| 代码审查 | 模型自我审查 | 执行Agent↔审查Agent↔反驳Agent 三方交叉 |

**使用方式**：龙虾体系在检测到任务复杂度符合以下条件时自动启用嵌套/动态模式：
- 子任务数 ≥ 5
- 需独立验证的任务
- 预计执行时间 > 2分钟的长任务

---

> **版本**：v2.24_R66（R33+R56+R62+R64+R65+R66更新）
> **知识来源**：Anthropic Agent Teams + Harness + Managed Agents + GPT-5.6对战策略 + Claude Fable 5/Mythos 5设计原则 + DeepSeek V4.1多模态Agent原则 + 蚂蚁AMP协议 + 微信AI生态指引 + RED Skill公告 + B站AI创造公开赛规则 + 抖音AI大赛规则 + 龙虾全域模板 + ChatGPT Dreaming主动记忆 + context-mode MCP插件范式
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\角色总说明书\SOUL.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\角色总说明书\AGENTS.md) | [角色总说明书 v2.27_R66](E:\龙虾AI主控中心\我的AI分身\角色总说明书\角色总说明书.md)
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*


---

## Anthropic官方课程R80同步：多Agent协作流程

### Dynamic Workflows 使用场景
1. 代码库级漏洞扫描
2. 大规模文件迁移（500+文件）
3. 交叉验证研究
4. 复杂规划

### 升级路径
单一子任务(<10min)→Subagents / 多代理协作+监督→Agent Teams / 大规模编排→Dynamic Workflows

### Claude Code 最佳实践
- /config 启用 Dynamic Workflows
- /deep-research 运行内置研究工作流
- JS脚本描述编排逻辑，存入项目仓库

> 同步自：Anthropic官方课程 R80 | 2026-06-14
*（内容由AI生成，仅供参考）*
