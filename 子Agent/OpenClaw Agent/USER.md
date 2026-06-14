---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_0286e2b767ad11f1a99c5254007bceed
    ReservedCode1: kbfVAlbPIEGPE0uBHejzxh7GFFLIMuxb+sumQDucAVxVbiwEA4LpXstNfXuTdvGcN+dl7jEp5Vonmev6eZrnFgHDCwM+I334CG3N9z/QKlQaG+CpxAwqXxtLQikC8v3hrnWDn/iE7sDWh6A6a9caiO5S3ZOzmQKBFngq+jhmVeG1+/8N75iCTrUNwwA=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_0286e2b767ad11f1a99c5254007bceed
    ReservedCode2: kbfVAlbPIEGPE0uBHejzxh7GFFLIMuxb+sumQDucAVxVbiwEA4LpXstNfXuTdvGcN+dl7jEp5Vonmev6eZrnFgHDCwM+I334CG3N9z/QKlQaG+CpxAwqXxtLQikC8v3hrnWDn/iE7sDWh6A6a9caiO5S3ZOzmQKBFngq+jhmVeG1+/8N75iCTrUNwwA=
---

---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_1a824c2861fb11f18f065254007bceed
    ReservedCode1: NpCpnwuwWwFJuD+KKSInA7gIjnOs4wW9SKQe1xCsTMXMi7EftQBbLKUVjtBrqb8L5Ra2jDLoS7hByYmS6UXAZrtRPRWmNi02/CVJPaOsfa5PdmiVbgxt6fcQWvhmLZ+RaqB9ORCEndaTxEwX2FoHTWmGDwg9rpG1aePbFxw+j7UlUcB/VMzOY9CI5tQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_1a824c2861fb11f18f065254007bceed
    ReservedCode2: NpCpnwuwWwFJuD+KKSInA7gIjnOs4wW9SKQe1xCsTMXMi7EftQBbLKUVjtBrqb8L5Ra2jDLoS7hByYmS6UXAZrtRPRWmNi02/CVJPaOsfa5PdmiVbgxt6fcQWvhmLZ+RaqB9ORCEndaTxEwX2FoHTWmGDwg9rpG1aePbFxw+j7UlUcB/VMzOY9CI5tQ=
---
# USER.md — 多Agent协作流程（龙虾AI分身用户指南）

> **版本**：v2.1(R80迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-01
> **来源**：Anthropic Agent Teams + Harness Patterns + Managed Agents Platform + Code with Claude 2026 + 龙虾全域模板融合
> **生效范围**：所有子Agent协作任务
> **依赖文件**：SOUL.md / AGENTS.md / 角色总说明书.md

---

## 一、多Agent协作总览

龙虾AI体系支持三种协作模式，按复杂度和场景自动选择：

| 模式 | 适用场景 | 通信方式 | Agent数 | 示例 |
|------|---------|---------|--------|------|
| 单Agent闭环 | 单一领域任务 | 无跨Agent通信 | 1个 | 文件整理、系统设置、App操作 |
| 串行协作 | 多阶段依赖任务 | 结果传递 | 2-3个 | 搜索信息→写入文件→通知 |
| 并行协作 | 独立子任务 | 各自执行后汇总 | 2-5个 | 多维度分析、多文件处理 |

---

## 二、协作流程 — 标准五步法

### Step 1: 意图识别
- 分析用户需求的核心目标和约束条件
- 判断任务属于哪个领域（文件/系统/App/搜索/浏览器）
- 拆解为可独立执行的子目标

### Step 2: 能力映射
按逐级降级原则匹配执行者：
```
Sub Agents → Skills → Tools → 生成代码执行
```

**Agent路由规则**：

| 领域 | Agent | 关键词 |
|------|-------|--------|
| 文件 | file-agent | 文件、文档、PDF、图片、搜索、整理、转换 |
| 系统 | computer-agent | 系统设置、窗口、进程、桌面、注册表 |
| 应用 | app-agent | App、APK、小程序、Steam、安装、打开 |
| 搜索 | search-agent | 深度调研、对比分析、论文检索 |
| 浏览器 | browser | 登录、表单、多页交互 |

### Step 3: 方案规划
- 单Agent闭环：一次dispatch_task完成
- 串行协作：按阶段顺序派发，前一步完成后再派下一步
- 并行协作：无依赖的子任务同时派发

### Step 4: 自主执行
- 子Agent内部自主规划执行步骤
- 主Agent不干预子Agent内部流程
- 每次dispatch_task完成后验收结果

### Step 5: 反思进化
- 验目标：核对执行结果是否符合预期
- 验产物：确认文件/文档是否真实生成
- 补缺口：不完整时寻找其他Agent补全
- 沉淀经验：归档至知识库

---

## 三、三种协作模式详解

### 3.1 单Agent闭环模式

**流程**：
```
用户需求 → 匹配领域Agent → dispatch_task一次派发 → 验收结果 → 呈现
```

**使用场景**：
- 文件操作（搜索、读取、写入、整理、转换）
- 系统设置（配置、优化、排查）
- App操作（安装、打开、操作）
- 深度搜索调研

**任务派发规范**：
```
<overall_goal>用户原始完整需求</overall_goal>
<current_task>本次具体任务（所有实质性内容写在这里）</current_task>
```

**禁止行为**：不要指导子Agent具体步骤，描述最终目标即可。

### 3.2 串行协作模式

**流程**：
```
Step 1: Agent A 执行 → 验收结果A
Step 2: Agent B 基于结果A执行 → 验收结果B
Step 3: Agent C 基于结果B执行 → 验收结果C → 汇总呈现
```

**使用场景**：
- 信息搜集→文档生成（search-agent→file-agent）
- App启动→系统调整（app-agent→computer-agent）
- 网页操作→数据处理→写入文件（browser→python_executor→file-agent）

**memory_ids传递**：
- 上游Agent结果通过memory_ids传递给下游Agent
- 不在task中重复已通过memory_ids传递的内容

### 3.3 并行协作模式

**流程**：
```
用户需求 → 拆解为3-5个独立子任务
       → 同时派发各Agent
       → 汇总结果 → 统一呈现
```

### 3.4 Goal模式Task接力（v2.0 新增）

**流程**：
```
长任务 → 状态锁初始化 → 子Task 1执行 → 检查点保存
                                           ↓
                                    子Task 2执行 → 检查点保存
                                           ↓
                                    [如中断] → 序列化状态 → 恢复后从断点继续
                                           ↓
                                    子Task N执行 → IO验证 → 状态锁释放
```

**适用场景**：
- 六步蒸馏全流程（预估>30min）
- 全域文件转换（>100文件）
- 跨Agent长链路协作（搜索→分析→报告→同步→归档）

**使用场景**：
- 多维度搜索（同时搜索不同关键词/来源）
- 多文件处理（同时处理不同文件）
- 多平台查询（同时查不同数据源）

**使用场景**：
- 多维度搜索（同时搜索不同关键词/来源）
- 多文件处理（同时处理不同文件）
- 多平台查询（同时查不同数据源）

**并行条件**：
- 无数据依赖
- 无状态依赖
- 无安全依赖
- 单次最多5个并行

---


### 3.4 Agent SDK 编排者-工作者三步法（Anthropic Academy R79注入）

> **来源**：Anthropic Academy 多Agent编排课程。Agent SDK 推荐的标准化协作模式。

**三步法全景**：

| 步骤 | 名称 | 动作 | 工具 | 产出 |
|------|------|------|------|------|
| Step 1 | **Decompose（分解）** | 将用户任务拆分为独立可并行的子任务 | LLM推理 + 任务依赖图 | 子任务清单（带依赖关系） |
| Step 2 | **Dispatch（派发）** | 将子任务路由到合适的子Agent | Agent Router / Claude Cowork Dispatch | 子Agent执行会话 |
| Step 3 | **Synthesize（合成）** | 收集子Agent结果，合并为统一答案 | 结果聚合器 + LLM总结 | 最终用户回复 |

**分解原则（Decompose）**：
```
1. 独立性检验：子任务之间能否独立执行？
   ├── 无数据依赖 → 并行派发（节省时间）
   └── 有数据依赖 → 串行派发（先产生中间结果）
2. 粒度标准：
   ├── 太粗 → 子Agent无法在单上下文窗口内完成
   ├── 太细 → 编排开销 > 执行收益
   └── 最优：子Agent单次执行 30-120s，输出 500-3000 token
3. 安全边界：每个子任务的操作范围有明确边界
```

**派发策略（Dispatch）**：

| 派发模式 | 适用场景 | 优点 | 缺点 |
|---------|---------|------|------|
| **并行派发** | 独立子任务（无依赖） | 速度最快，总耗时=max(各子任务) | 上下文预算消耗大 |
| **串行派发** | 有依赖子任务 | 上下文可控，结果精准 | 总耗时=sum(各子任务) |
| **流水线派发** | 部分依赖，可分批 | 平衡速度与控制 | 编排复杂度高 |
| **竞速派发** | 同一任务多策略并行 | 取最优结果 | 资源消耗大 |

**合成策略（Synthesize）**：
```
1. 结构化合并：各子Agent返回JSON Schema → 直接合并
2. 对比择优：多策略竞速 → LLM选出最佳
3. 增量构建：流水线模式 → 逐层构建最终答案
4. 摘要回传：子Agent结果过长 → 仅摘要入主上下文
```

---

### 3.5 上下文隔离机制详解（Anthropic Academy R79注入）

> **来源**：Anthropic Academy 子代理上下文管理课程。

**核心原理**：子代理仅将 **prompt + 结果摘要** 回传主对话，中间推理过程不污染主上下文。

**隔离架构**：
```
主对话上下文 (Managed Agent)
├── [用户消息 + 系统提示]  ← 基础开销
├── [子代理A prompt + 结果摘要]  ← 只传这点（约200-500 token）
├── [子代理B prompt + 结果摘要]  
├── [子代理C prompt + 结果摘要]
└── [合成 + 最终回复]

子代理A 独立上下文 (隔离)
├── [子代理系统提示]
├── [任务 prompt]
├── [工具调用 × N]  ← 这些不会污染主上下文！
├── [中间推理 × N]  ← 这些也不会！
└── [输出结果 → 压缩为摘要回传]
```

**上下文预算分配模型**：

| 预算科目 | 占比 | 内容 |
|---------|------|------|
| 系统提示 + Agent指令 | 15-25% | SOUL.md / USER.md 知识注入 |
| 用户消息与历史 | 10-20% | 对话历史、上下文窗口滑动 |
| 子代理摘要区 | 30-50% | 所有子代理的 prompt + 结果摘要 |
| 合成与回复区 | 10-20% | 编排者合成、最终回复 |
| 安全缓冲 | 5-10% | 防止溢出 |

**何时不走子代理隔离**：
| 场景 | 原因 | 替代方案 |
|------|------|---------|
| 子任务 <500 token | 派发成本 > 收益 | 主Agent内直接执行 |
| 需要全上下文引用 | 隔离后无法引用前文 | 将必要前文注入子Agent prompt |
| 实时交互任务 | 隔离阻断用户交互 | 保留在主对话中 |

---

### 3.6 Claude Cowork：Dispatch 与 Computer Use（Anthropic Academy R79注入）

> **来源**：Anthropic Academy Claude Cowork 课程。

**Dispatch（远程任务分配）**：
- Claude Cowork 支持将任务远程派发到其他 Claude 实例或 MCP Server
- 类似 "Agent-to-Agent 远程调用"
- 适用场景：
  - 跨机器任务分配（CI/CD 触发审查）
  - 代码仓库自动化（PR审查机器人）
  - 企业内部 Agent 网格

**Computer Use（桌面自主控制）**：
| 能力 | 描述 | 安全级别 |
|------|------|---------|
| 屏幕理解 | 截图分析当前桌面状态 | 低风险（只读） |
| 鼠标操作 | 点击、拖拽、滚动 | 中风险（需确认） |
| 键盘输入 | 文本输入、快捷键 | 中风险（需确认） |
| 应用控制 | 打开/关闭应用、操作UI | 高风险（需审批） |
| 文件拖放 | 跨应用文件操作 | 高风险（需审批） |

**龙虾体系映射**：
| Claude Cowork 能力 | 龙虾对标实现 | 状态 |
|------|------|------|
| Dispatch 远程派发 | Hermes 任务队列 + 子Agent路由 | 已有 |
| Computer Use 桌面控制 | 暂未实现（OpenClaw 桌面能力预留） | 规划中 |
| Agent网格协作 | 豆包/Hermes/OpenClaw 三Agent体系 | 已有 |
| PR审查自动化 | code-reviewer子Agent | 已有 |


## 四、跨Agent通信协议

### 4.1 双向桥接协议（龙虾标准）

```json
{
  "source": "lobster_master",
  "target": "doubao_agent|hermes_agent|openclaw_agent",
  "action": "deploy|query|evolve|sync",
  "payload": {},
  "timestamp": "",
  "trace_id": ""
}
```

### 4.2 Agent间信息传递

| 传递方式 | 适用场景 | 工具 |
|---------|---------|------|
| memory_ids | 将上游Agent结果作为背景信息注入下游Agent | dispatch_task参数 |
| inherit_agent_id | 同一Agent的连续会话（延续任务） | dispatch_task参数 |
| 文件传递 | 通过磁盘文件传递中间/最终产物 | 中间产物目录(temp) |
| MCP协议 | Agent与外部系统通信 | MCP Server |

### 4.3 延续任务判断

当用户使用以下语言时，很可能是延续任务，需填写 `inherit_agent_id`：
- "不对" / "别..." / "不是这样"
- "恢复" / "撤销" / "改回"
- "再..." / "继续..." / "还有..."

---

## 五、协作安全机制

### 5.1 任务验收三问
每次dispatch_task完成后，必须回答：
1. 执行目标是否完全达成？
2. 是否有真实产物（文件/设置变更）？
3. 是否有未完成部分需要其他Agent补全？

### 5.2 降级兜底
- 同一工具/技能针对同一子目标失败上限2次
- 超出后必须降级到上一层能力或交还用户
- 严禁仅通过参数微调绕过上限

### 5.3 工具调用安全
- 🔴 高风险操作：必须确认
- 🟡 中风险操作：二次确认
- 🟢 低风险操作：直接执行
- 工具调用即警戒：涉及系统状态变更时必须评估风险

---

## 六、协作最佳实践

### 6.1 任务描述
- task中使用结果导向：描述目标而非步骤
- memory_ids传递背景信息，不在task中重复
- attachments块必须原样透传

### 6.2 结果验证
- Sub Agent返回特殊卡片时，用present_result原子转发
- 不手写/复制/改写Sub Agent的特殊卡片
- 多个Agent结果需汇总时，不调用present_result

### 6.3 上下文管理
- 子Agent通过memory_ids获取必要背景
- 大段文件内容优先通过memory_ids传递
- 避免在task中重复已传递的内容

### 6.4 失败处理
- 分析失败原因，明确失败节点
- 切换参数/路径/能力层级或交还用户
- 严禁重复完全相同的调用

---

## 七、全分身同步流程

### 7.1 同步触发条件
- 新技能协议生成
- Agent能力升级
- SOUL.md / USER.md / AGENTS.md 更新
- 全域模板迭代

### 7.2 同步目标
| 分身 | 同步内容 | 同步方式 | R26新增 |
|------|---------|---------|---------|
| 豆包Agent | 技能/工作流/记忆/设计原则/Goal模式配置 | 写入对应配置目录 | Goal模式状态锁 |
| Hermes Agent | 调度策略/协作流程/进程管理/心跳检测 | 更新调度配置 | 五层防烂尾对齐 |
| OpenClaw龙虾Agent | 插件/协议/底层能力/IO验证钩子 | 更新插件配置 | 执行可验证性协议 |

### 7.3 同步验证
- 同步后执行巡检（健康巡检技能）
- 检查所有子Agent运行状态
- 异常记录纳入下一轮优化

---

## 八、任务执行检查清单

```
□ Step 1: 意图识别完成？拆解是否合理？
□ Step 2: Agent/工具匹配正确？是否越级？
□ Step 3: 协作模式选择正确？串行/并行/单Agent/Goal模式？
□ Step 4: dispatch_task参数填写完整？task/agent_name/memory_ids/inherit_agent_id？
□ Step 5: 执行结果验收完成？目标/产物/缺口？
□ Goal模式检查（耗时>10min或20+文件操作时启用）：
  □ 心跳信号是否正常（15s间隔）？
  □ 中断状态是否已序列化？
  □ 断点续跑路径是否确认？
□ 最终回复：是否需要present_result？是否有yyb-product？
□ 是否有新技能/经验需要沉淀归档？
```

---

## 十、Managed Agents 编排工作流（v1.1 新增）

### 9.1 Multiagent Orchestration 工作流

**适用场景**：任务可分解为多个独立子任务，需要并行处理以提高效率。

**流程**：
```
用户需求
  ↓
Lead Agent (Opus) 分解任务
  ↓
┌──────────┬──────────┬──────────┬──────────┐
│ Subagent │ Subagent │ Subagent │ Subagent │  ← 并行执行（最多20种 × 25线程）
│    A     │    B     │    C     │    D     │
└──────────┴──────────┴──────────┴──────────┘
  ↓           ↓           ↓           ↓
Lead Agent 接收结果、中途可发跟进消息
  ↓
合成最终结果 → 呈现给用户
```

**典型工作流模式**：

| 模式 | 场景 | 子代理分工 |
|------|------|-----------|
| 研究-评估-生成 | 销售线索处理 | 研究子代理(并行拉取)→资格评估子代理→草拟子代理 |
| 多维度分析 | 事件根因分析 | 部署历史/错误日志/性能指标/客服工单 四路并行 |
| 数据聚合 | 季度报告 | 财务/销售/运营/HR 四路并行拉取→Lead合成 |
| 合规多路审查 | 合同审查 | 政策对照/法规比对/历史条款 三路并行 |
| 多版草稿 | 内容创作 | 多个写作子代理并行生成→Outcomes Grader评分→返回最佳版 |

### 9.2 Outcomes 质量工作流

**流程**：
```
Agent 产出 → 独立 Grader 评分（隔离上下文）
    │
    ├── 达标 → 返回用户
    │
    └── 未达标 → Grader 指出具体问题 → Agent 迭代修正 → 重新评分
                   ↑                                           │
                   └─────────────────── 循环 ──────────────────┘
                   （最多 max_iterations 次）
```

**集成到龙虾五步法**：

| 步骤 | 原有 | Outcomes 增强 |
|------|------|-------------|
| 意图识别 | 分析需求 | 同时定义 Outcomes Rubric |
| 能力映射 | 匹配 Agent | 匹配 Agent + Grader 模型 |
| 方案规划 | 串行/并行决策 | 加入 Outcomes 迭代预算 |
| 自主执行 | Agent 自主执行 | Agent 执行 → Grader 评估 → 迭代修正 |
| 反思进化 | 验收结果 | Rubric 评分 + Dreaming 模式沉淀 |

### 9.3 Webhooks 异步集成工作流

```
龙虾AI体系
  │
  ├── 触发 Managed Agent 任务
  │
  ├── 设置 webhook_url（CI/CD / 通知 / 下一步触发）
  │
  ├── Agent 异步执行（用户无需等待）
  │
  ├── Agent 完成后 POST 结果到 webhook_url
  │
  └── 下游系统自动处理结果
```

### 9.4 Agent View 并行管理工作流

```
Agent View Dashboard
├── 会话1：Code Review Agent ──── 运行中
├── 会话2：Test Runner Agent ──── 等待输入
├── 会话3：Docs Writer Agent ──── 已完成
├── 会话4：Security Audit Agent ── 运行中
└── 会话5：空闲（可启动新任务）
```

**快捷键**：
- `←` 打开 Agent View
- `Space` 查看选中会话详情（Peek Panel）
- `/bg` 后台化当前任务并返回 Agent View
- `→` 进入选中会话

---

## 十一、Managed Agents 协作最佳实践（v1.1 新增）

### 10.1 何时升级到 Managed Agents

| 当前状态 | 升级建议 |
|---------|---------|
| 单个 Agent 反复遇到相同失败 | → Managed Agents + Dreaming |
| 任务质量不稳定，手动迭代 Prompts | → Managed Agents + Outcomes |
| 串行 Agent 链耗时过长 | → Multiagent Orchestration 并行化 |
| 需要在 CI/CD 中集成 Agent | → Webhooks 回调 |
| 同时管理多个 Agent 实例 | → Agent View |

### 10.2 子代理设计清单

```
□ 每个子代理职责单一吗？（一个子代理做好一件事）
□ 子代理之间无数据依赖吗？（有依赖则不适合并行）
□ 子代理获得最小工具集吗？（权限最小化）
□ 子代理工作独立可验证吗？（可独立评分）
□ 总子代理数 ≤ 20 种类型吗？
□ Lead Agent 有能力合成所有结果吗？
```

### 10.3 Outcomes Rubric 撰写指南

**好 Rubric 的特征**：
- 可测量（"识别所有安全漏洞"而非"做好安全审查"）
- 有边界（"不超过 500 字"）
- 有优先级（"安全漏洞必须标注，代码风格只是建议"）
- 有具体的失败标准（"不标注安全漏洞 = 不通过"）

**坏 Rubric 的例子**：
- "写出好的代码"（太模糊）
- "做得更好一点"（无法测量）
- "全面检查"（没有边界）

### 10.4 影子Agent复盘安全协议（R33新增）

多Agent协作中的所有复盘操作必须遵循影子Agent六层隔离：

| 层级 | 控制项 | 策略 |
|------|--------|------|
| 权限隔离 | 影子Agent最小只读权限 | 禁止写文件/系统命令/网络访问 |
| 数据隔离 | 仅注入摘要，非原始数据 | 独立上下文，不污染主Agent缓存 |
| 网络隔离 | 全部阻断外网 | 仅本地回环 |
| 文件隔离 | 仅读写技能库 | 禁止系统路径 |
| 进程隔离 | fork独立子进程 | 120秒超时→强制终止 |
| 审计隔离 | 独立日志文件 | 90天滚动归档 |

**脏计数触发**：工具迭代≥8次/会话自动触发复盘。Agent主动操作技能时重置。

---

> **版本**：v2.1（R33更新）
> **知识来源**：Anthropic Agent Teams + Harness + Managed Agents + 龙虾全域模板v3.26 + Hermes Curator v0.12.0
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\AGENTS.md)
*（内容由AI生成，仅供参考）*

---

## Anthropic官方课程R80同步：多Agent协作流程

### Dynamic Workflows 使用场景
1. **代码库级漏洞扫描**：对全仓库进行系统性安全检查
2. **大规模文件迁移**：500+文件的批量重构
3. **交叉验证研究**：从多个独立角度研究同一问题，交叉对比结论
4. **复杂规划**：在提交执行前从多个独立角度起草方案

### 从 Subagents → Agent Teams → Dynamic Workflows 的升级路径
- 单一子任务（<10分钟）→ Subagents
- 多代理协作需人工监督 → Agent Teams  
- 大规模编排需可审计可重跑 → Dynamic Workflows

### Claude Code 最佳实践（R80更新）
- /config 中启用 Dynamic Workflows
- /deep-research 运行内置研究工作流
- 使用 JS 脚本描述编排逻辑，存入项目仓库

> 同步自：Anthropic官方课程390节全集 R80 | 2026-06-14
