---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_e804bb2f655f11f192bd5254007bceed
    ReservedCode1: vSFXJl9XJ3qdvlPkfTkM7HEPp9VvN0NMnhOLUb2jKN+CngYaWiLGmU40hySXgwMd/94gAt1MWGmENU3sVWrFVneAL33QjlkfCL5JCK26EztUEHCAaTS6dyODzo06/EtZhwjjP7dQ/ABSDk71fLmNUJKUkqcrt312a0z1r8nsHxkk/DtrJMOd3Fd/jL4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_e804bb2f655f11f192bd5254007bceed
    ReservedCode2: vSFXJl9XJ3qdvlPkfTkM7HEPp9VvN0NMnhOLUb2jKN+CngYaWiLGmU40hySXgwMd/94gAt1MWGmENU3sVWrFVneAL33QjlkfCL5JCK26EztUEHCAaTS6dyODzo06/EtZhwjjP7dQ/ABSDk71fLmNUJKUkqcrt312a0z1r8nsHxkk/DtrJMOd3Fd/jL4=
---

---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_accf548364a711f1b8945254007bceed
    ReservedCode1: nF/iNwSViL6BrmngH8f/N8znicgFwoWCVtXizC8eke7Zx8x4n+JongN1hGeogwNq/cAli0DaJtBCNI/6tHvCzZZEZemPXaucK2hXMkUQR9lAu77pmomiuLNcO8HsPCzYgdxK1vTLkry65e4YyWWn3rZg6wdf08dRbJBP3dtLdAVWrAbsx3siYRT5c1k=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_accf548364a711f1b8945254007bceed
    ReservedCode2: nF/iNwSViL6BrmngH8f/N8znicgFwoWCVtXizC8eke7Zx8x4n+JongN1hGeogwNq/cAli0DaJtBCNI/6tHvCzZZEZemPXaucK2hXMkUQR9lAu77pmomiuLNcO8HsPCzYgdxK1vTLkry65e4YyWWn3rZg6wdf08dRbJBP3dtLdAVWrAbsx3siYRT5c1k=
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

> **版本**：v2.7 (R84迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-14
> **来源**：Anthropic Agent Teams官方文档 + Agent SDK编排模式（Orchestrator/Pipeline/Mesh） + Plugins打包协作体系 + Claude Code Subagents + Skills九类分类法 + 四支柱AI OS架构 + 龙虾全域模板融合
> **生效范围**：所有子Agent协作任务
> **依赖文件**：SOUL.md / AGENTS.md / 角色总说明书.md / Anthropic官方课程-390节全集.md

---

## 一、多Agent协作总览

龙虾AI体系支持三种协作模式，按复杂度和场景自动选择：

| 模式 | 适用场景 | 通信方式 | Agent数 | 示例 |
|------|---------|---------|--------|------|
| 单Agent闭环 | 单一领域任务 | 无跨Agent通信 | 1个 | 文件整理、系统设置、App操作 |
| 串行协作 | 多阶段依赖任务 | 结果传递 | 2-3个 | 搜索信息→写入文件→通知 |
| 并行协作 | 独立子任务 | 各自执行后汇总 | 2-5个 | 多维度分析、多文件处理 |
| Managed Agents 云端托管 | 生产级Agent部署 | SSE 事件流 + API 驱动 | 不限 | 异步长任务、跨会话记忆、多用户服务 |

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

## 十一、Agent SDK 多Agent编排实战（R74新增）

### 11.1 并行子代理生成模式

基于 Agent SDK 0.2.82，主Agent可以同时派发多个子代理并行工作：

```python
# 三次并行调用，各自独立上下文
agents = {
    "code-reviewer": AgentDefinition(
        description="Python code quality and design review specialist",
        prompt="You're a Python senior engineer...",
        tools=["Read", "Grep"], model="sonnet", maxTurns=8,
    ),
    "security-scanner": AgentDefinition(
        description="Security vulnerability scanner",
        prompt="You're a security engineer. Find injection risks...",
        tools=["Read", "Grep", "Bash"], model="sonnet", maxTurns=6,
    ),
    "doc-writer": AgentDefinition(
        description="Docstring and README writer",
        prompt="You're a technical writer...",
        tools=["Read", "Write", "Edit"], model="haiku", maxTurns=5,
    ),
}
```

### 11.2 TaskBudget 双级成本控制

| 级别 | 机制 | 示例 | 作用 |
|------|------|------|------|
| L1 全局 | `TaskBudget(total=N)` | total=100000 tokens | 整个编排任务的Token硬上限 |
| L2 子代理 | `AgentDefinition.maxTurns=N` | maxTurns=6 | 单个子代理最大Agent循环数 |

**协作触发条件**（Anthropic明确的三类信号）：
1. **上下文被噪音淹没** → 子任务产生大量中间信息，主对话只需摘要
2. **搜索空间太大** → 竞品研究/事故根因，多子Agent并行扫不重叠方向
3. **工具太多打架** → 20+工具跨领域，按领域拆专家子Agent

### 11.3 Skills 在协作中的角色

> Anthropic 九类 Skill 分类中，"产品验证"类 Skill 回报最大。

多Agent协作中的Skills策略：
- **验证类Skill优先建设**：signup-flow-driver、checkout-verifier 等自动化测试能力
- **业务流程自动化Skill**：standup-post、weekly-recap 等重复工作流压缩
- **运维手册Skill**：oncall-runner、log-correlator 等标准化排障流程

### 11.4 Anthropic 内部方法论：从单Agent到多Agent的正确路径

1. **先把单Agent做到可控**：完成定义清晰、固定输出格式、10-30样本评估集
2. **出现信号再上多Agent**：只在上下文噪音/搜索空间大/工具冲突三类情况考虑
3. **按信息流切分，不按任务类型切分**
4. **把流程写成Skill，别写进Prompt**
5. **外部系统统一走MCP**
6. **最后再谈"聪明"**

### 11.5 Claude Certified Architect 对协作能力的启示

> Anthropic认证五大领域中的 Agentic Architecture & Claude Code 权重最高。

协作能力对标：
- **Subagents 配置**：五级作用域（managed/CLI/project/user/plugin），按优先级加载
- **Agent Teams**：子代理定义可供Agent Teams使用，spawn teammate时继承tools和model
- **Hooks 生命周期**：PreToolUse/PostToolUse/SubagentStart/SubagentStop 全程可控
- **Memory 跨会话**：user/project/local 三级记忆范围，支持Dreaming巩固

---

> **版本**：v2.2（R74更新）
> **知识来源**：Anthropic Agent SDK 0.2.82 / Claude Code Subagents官方文档 / Skills九类分类法 / kdnuggets完整指南 / 龙虾全域模板
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\AGENTS.md) | [Anthropic官方课程-390节全集](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-390节全集.md)
*（内容由AI生成，仅供参考）*


---

## 鍗佷簩銆佸Agent鍗忎綔娴佺▼锛?026-06-11澧為噺鏇存柊锛?
### 12.1 鍗旳gent闂幆 vs 澶欰gent鍗忎綔鐨勫喅绛栨祦绋?
鍐崇瓥鏍戯紙鑷笂鑰屼笅鍒ゆ柇锛屽懡涓嵆姝級锛?
```
鐢ㄦ埛浠诲姟
  鈫?鏄惁涓哄崟涓€棰嗗煙銆佹棤骞惰闇€姹傦紵
  鈹溾攢 鏄?鈫?鍗旳gent闂幆锛堝父瑙勪細璇濓級
  鈫?鍚?鏄惁鏈?+鐙珛瀛愪换鍔′笖浜掍笉渚濊禆锛?  鈹溾攢 鏄?鈫?澶氫釜Subagents骞惰澶勭悊
  鈫?鍚?鏄惁闇€瑕佹垚鍛橀棿閫氫俊涓庤嚜鍗忚皟锛?  鈹溾攢 鍚?鈫?Subagents锛堜富Agent缂栨帓锛?  鈫?鏄?鏄惁娑夊強澶у瀷浠ｇ爜搴?澶氭ā鍧?璺ㄥ眰锛?  鈹溾攢 鍚?鈫?Subagents锛堜覆琛?绠€鍗曞苟琛岋級
  鈫?鏄?棰勭畻鍏佽杈冮珮Token娑堣€楋紵
  鈹溾攢 鍚?鈫?Subagents锛堥檷绾ф柟妗堬級
  鈫?鏄?  鈹斺攢 Agent Teams锛堟垚鍛樼洿鎺ラ€氫俊銆佽嚜鍗忚皟銆佷氦鍙夐獙璇侊級
```

蹇€熷垽鏂彛璇€锛?- 銆屽幓鏌ヤ竴涓媂銆嶁啋 Subagent
- 銆屼綘浠竴璧峰垎鏋愶紝瀵逛簡浜掔浉楠岃瘉銆嶁啋 Agent Teams
- 銆屽府鎴戞敼涓€涓嬭繖涓€嶁啋 鍗曚細璇?
### 12.2 Agent Teams 鍚敤涓庨厤缃寚鍗?
**鍓嶆彁鏉′欢**锛?- Claude Code v2.1.32+
- Opus 4.6妯″瀷璁块棶鏉冮檺

**鍚敤鏂瑰紡**锛?
鏂瑰紡涓€锛歴ettings.json锛堟帹鑽愰」鐩骇鍒級
```json
// .claude/settings.json 鎴?~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "model": "sonnet"
}
```

鏂瑰紡浜岋細鐜鍙橀噺
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**瀹炶返閰嶇疆寤鸿**锛?
```json
// 鐢熶骇绾ф帹鑽愰厤缃?{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "model": "sonnet",
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash(git:*)"]
  }
}
```

鍥㈤槦鎴愬憳浣跨敤Sonnet锛堥潪Opus锛夊钩琛℃垚鏈笌鑳藉姏銆傞」鐩瓹LAUDE.md鑷姩琚?鎵€鏈夐槦鍙嬪姞杞斤紝鏃犻渶鍦ㄦ瘡涓槦鍙嬬殑鎻愮ず璇嶄腑閲嶅椤圭洰涓婁笅鏂囥€?
### 12.3 Skills/Hooks/MCP/Subagents 鍥涗欢濂楀崗鍚屽伐浣滄祦

鍗忓悓鍏崇郴鍏ㄦ櫙锛?
```
          璇锋眰杩涘叆
              鈫?        CLAUDE.md锛堝叏灞€鍩虹嚎濮嬬粓鍔犺浇锛?              鈫?        Skills娓愯繘寮忓姞杞斤紙鐩稿叧鏃惰嚜鍔ㄦ縺娲伙級
              鈫?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈫?       鈫?       鈫?  Hooks   Subagents  MCP
  (浜嬩欢    (骞惰     (澶栭儴
  瑙﹀彂)   闅旂)     杩炴帴)
```

鍥涗欢濂楀悇鑷殑瑙掕壊瀹氫綅锛?
| 缁勪欢 | 瑙掕壊 | 瑙﹀彂鏃舵満 | 鍏稿瀷鐢ㄦ硶 |
|------|------|---------|---------|
| CLAUDE.md | 瀹硶 | 濮嬬粓鍔犺浇 | 浣犳槸璋?鍋氫粈涔?涓嶅仛浠€涔?|
| Skills | 椋熻氨 | 浠诲姟鐩稿叧鏃?| 鏂囦欢鏁寸悊/鍙戠エ璇嗗埆/鏂囨。鍐欎綔 |
| Hooks | 闂ㄧ | 浜嬩欢瑙﹀彂 | PreToolUse鏍￠獙/PostToolUse鏃ュ織 |
| MCP | 璁惧 | 闇€瑕佸閮ㄦ暟鎹?| 杩炴帴Notion/Linear/鏁版嵁搴?|
| Subagents | 澶栧寘 | 骞惰浠诲姟 | 澶氭枃浠跺垎鏋?鐙珛瀛愪换鍔?|
| Agent Teams | 鍥㈤槦 | 澶嶆潅骞惰 | 澶氭ā鍧楀紑鍙?绔炰簤鍋囪璋冭瘯 |

鐪熷疄宸ヤ綔娴佺ず渚嬶紙鏂囦欢鏁寸悊鍦烘櫙锛夛細

1. CLAUDE.md 瀹氫箟鍏ㄥ眬琛屼负绾︽潫
2. User: "鏁寸悊妗岄潰鏂囦欢"
3. Skills 鑷姩婵€娲?file-organizer
4. Hooks(PreToolUse) 鏍￠獙鏂囦欢璺緞瀹夊叏鎬?5. Subagents 骞惰鎵弿涓嶅悓鐩綍
6. MCP 鏃犻渶姹傦紙绾湰鍦版搷浣滐級
7. 缁撴灉姹囨€?鈫?鏁寸悊钃濆浘 鈫?鐢ㄦ埛纭 鈫?鎵ц

### 12.4 璺ˋgent閫氫俊妯″紡

榫欒櫨AI浣撶郴鏀寔鍥涚璺ˋgent閫氫俊妯″紡锛?
**妯″紡涓€锛氬叡浜换鍔″垪琛紙Agent Teams鍘熺敓锛?*
```
Team Lead 鍒涘缓浠诲姟鍒楄〃 鈫?Teammates 璁ら浠诲姟
     鈫?鐘舵€佸悓姝ワ細寰呭鐞?杩涜涓?宸插畬鎴?     鈫?鑷姩渚濊禆瑙ｉ櫎闃诲锛欰瀹屾垚鍚嶣鑷姩瑙ｉ攣
```

**妯″紡浜岋細鐩存帴娑堟伅锛圓gent Teams鍘熺敓锛?*
```
鎴愬憳A鍙戠幇渚濊禆闂 鈫?鐩存帴閫氱煡鎴愬憳B
鎴愬憳B瀹屾垚 鈫?鎴愬憳C鍩轰簬B鐨勫伐浣滅户缁?鏃犻渶鎵€鏈夐€氫俊缁忚繃Team Lead
```

**妯″紡涓夛細涓籄gent姹囨€伙紙Subagents榛樿妯″紡锛?*
```
Subagent A 鈹€鈹€鈫?缁撴灉 鈹€鈹€鈹?Subagent B 鈹€鈹€鈫?缁撴灉 鈹€鈹€鈹も啋 涓籄gent姹囨€?鈫?缁煎悎杈撳嚭
Subagent C 鈹€鈹€鈫?缁撴灉 鈹€鈹€鈹?```

**妯″紡鍥涳細memory_ids浼犻€掞紙榫欒櫨璺ㄤ細璇濓級**
```
Agent A 杈撳嚭 memory_ids 鈫?Agent B 璇诲彇璁板繂涓婁笅鏂?璺ㄤ細璇濅俊鎭紶閫掓満鍒讹紝閫傜敤浜庨暱浠诲姟娴佹按绾?```

閫氫俊妯″紡閫夋嫨鍐崇瓥锛?- 鎴愬憳闇€瑕佽嚜鍗忚皟 + 鐩存帴閫氫俊 鈫?妯″紡涓€/浜岋紙Agent Teams锛?- 浠诲姟鐙珛 + 鍙渶缁撴灉 鈫?妯″紡涓夛紙Subagents锛?- 璺ㄤ細璇?+ 闀夸换鍔℃祦姘寸嚎 鈫?妯″紡鍥涳紙memory_ids锛?


---

## 十三、Agent Teams 五大协作模式（v2.3 / R76更新）

> 来源：code.claude.com/docs/en/agent-teams v2.1.32 官方实战案例

### 13.1 模式一：并行代码审查（Parallel Code Review）

**场景**：PR审查需要安全/性能/测试三个视角同时进行
**配置**：
- 3个审查队友：security-reviewer / performance-reviewer / test-auditor
- 每个队友独立上下文，各自产出审查报告
- Team Lead合成最终审查意见

**提示词模板**：
```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
```

### 13.2 模式二：竞争假设调试（Competing Hypotheses Debugging）

**场景**：Bug原因不明，需要并行探索多个根因假设
**配置**：
- 5个队友各自探索不同的根因理论
- 队友间互相交流，用科学辩论模式排除错误假设
- 最快收敛到正确答案

**提示词模板**：
```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk
to each other to try to disprove each other's theories, like a scientific debate.
```

### 13.3 模式三：跨层协调开发（Cross-layer Coordination）

**场景**：修改横跨前端/后端/数据库/测试的功能
**配置**：
- 4个队友各自负责独立代码层：frontend / backend-api / database-migration / test-suite
- 每个队友拥有不同的文件集，避免文件冲突
- Lead负责跨层接口契约定义

**提示词模板**：
```
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### 13.4 模式四：新模块并行开发

**场景**：从零构建多模块功能
**配置**：
- 每个队友负责一个独立模块或组件
- 使用计划批准模式确保质量：复杂或高风险任务要求队友先规划后执行
- Lead在关键接口点介入协调

**提示词模板**：
```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

### 13.5 模式五：复用子代理定义作为队友

**场景**：项目中已有 .claude/agents/security-reviewer 子代理定义，直接复用为Agent Teams队友
**配置**：
- 子代理定义自动继承 tools/model/permissions
- 无需重复配置，开箱即用

**提示词模板**：
```
Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

### 13.6 Agent Teams 决策速查表

| 需求信号 | → 选择方案 | 规模 |
|----------|-----------|------|
| "去查一下X" | Subagent | 1个 |
| "你俩一起分析，互相验证" | Agent Teams | 2-3个 |
| "帮我改这个" | 单会话 | 0个 |
| "并行审查PR安全/性能/测试" | Agent Teams | 3个 |
| "5种假设各自验证" | Agent Teams | 5个 |
| "前端+后端+数据库+测试" | Agent Teams | 4个 |

---

> **知识来源**：Claude Code Agent Teams 官方文档 v2.1.32 / Anthropic Academy Subagents课程
*(内容由AI生成，仅供参考)*
*（内容由AI生成，仅供参考）*


---

## 十四、多Agent协作流程（Anthropic Academy课程补充）

[来源：Anthropic Academy课程·第R77轮学习 2026-06-11]

### 14.1 Agent / Subagent / Agent Teams 三模式决策框架

#### 一句话理解三种模式

| 模式 | 类比 | 通信方式 | 适用场景 |
|------|------|---------|---------|
| Agent | 单兵作战 | 你 ↔ AI | 简单-中等复杂度，一个会话能完成 |
| Subagent | 老板+员工 | 主AI → 子AI（单向汇报） | 多任务独立并行，不需要AI间对话 |
| Agent Teams | 项目组协作 | AI ↔ AI（双向对话） | 复杂任务需要AI互相辩论和协调 |

#### 实战决策树三问

**问题1：任务能否在一个会话中完成？**
- 能 → 用 Agent（常规会话）
- 不能（上下文会混乱 / 任务需并行 / 需要不同工具权限）→ 继续问题2

**问题2：子任务之间需要互相沟通吗？**
- 不需要（各干各的，各自独立）→ 用 Subagent
- 需要（要讨论、辩论、协调）→ 继续问题3

**问题3：这个任务值得花10倍Token吗？**
- 值得（关键项目、高价值交付）→ 用 Agent Teams
- 不值得 → 降级用 Subagent 或重新拆分任务为更简单单元

### 14.2 并行编排最佳实践

#### 并行条件判断

必须同时满足三个条件才可并行：
1. **无数据依赖**：任务A的输出不作为任务B的输入
2. **无状态依赖**：任务A不改变任务B需要读取的状态
3. **无安全依赖**：任务A的失败不影响任务B的安全性

#### Agent SDK 并行实现模式

```python
# 定义三个专业化子代理
code_reviewer = AgentDefinition(description="Python code quality review", ...)
security_scanner = AgentDefinition(description="Security vulnerability scan", ...)
doc_writer = AgentDefinition(description="Technical documentation", ...)

# 注册到编排器
opts = ClaudeAgentOptions(
    system_prompt="You're a PR review orchestrator. Run the three agents in parallel.",
    agents={"code-reviewer": code_reviewer, "security-scanner": security_scanner, "doc-writer": doc_writer},
    task_budget=TaskBudget(total=100000),  # 全局100K Token硬上限
)
```

关键要点：编排器在一次消息中调用多个 Agent Tool，SDK 自动并行执行。

#### 上下文隔离机制

- 每个子代理的上下文窗口从零开始
- 父到子的唯一通道：Agent Tool 提示词字符串
- 子代理看不到其他子代理的推理过程
- 主Agent只看到最终结果，不看到中间推理

### 14.3 常见误区与避坑指南

**误区1：「复杂任务就用Agent Teams」**
- 错误：任务稍微复杂就无脑开Agent Teams
- 正确：先问"AI之间需要对话吗？"如果只是任务多但各自独立，用Subagent就够了
- 案例：修复10个独立bug → 用Subagent，不需要Agent Teams

**误区2：「Subagent一定比Agent Teams便宜」**
- 陷阱：召唤10个子AI的总成本可能超过3个AI的Agent Teams
- 原则：成本 = AI数量 × 每个AI的工作量 × 协调开销

**误区3：「单Agent只能做简单任务」**
- 反例：复杂代码重构可用单Agent完成，前提是任务清晰、上下文管理得当
- 技巧：用计划模式让Agent先梳理思路再执行

**误区4：「Agent Teams会自动协调，不需要管理」**
- 风险：放任讨论可能跑偏或陷入无休止辩论
- 最佳实践：定期检查进度、关键决策点人工介入、设定讨论时限

### 14.4 选择速查表

| 需求信号 | 选择方案 | 规模 |
|----------|---------|------|
| "去查一下X" | Subagent | 1个 |
| "帮我改这个" | 单会话Agent | 0个 |
| "你俩一起分析，互相验证" | Agent Teams | 2-3个 |
| "并行审查PR安全/性能/测试" | Agent Teams | 3个 |
| "5种假设各自验证" | Agent Teams | 5个 |
| "前端+后端+数据库+测试" | Agent Teams | 4个 |

### 14.5 从单Agent到多Agent的正确路径

1. 先把单Agent做到可控：清晰定义、固定输出格式、10-30样本评估集
2. 出现信号再上多Agent：上下文噪音 / 搜索空间大 / 工具冲突
3. 按信息流切分，不按任务类型切分
4. 把流程写成Skill，别写进Prompt
5. 外部系统统一走MCP
6. 最后再谈"聪明"

### 九、Agent Teams Delegate Mode 操作流程（v2.1.45）

```
启动 Agent Teams → Shift+Tab 开启 Delegate Mode → Lead 仅协调不实现
    │
    ├── Spawn Teammate 1 (Default Mode)：实现任务 A → 5-6个子任务 → 逐个报告进度
    ├── Spawn Teammate 2 (Default Mode)：实现任务 B → 独立文件集 → 不冲突
    ├── Spawn Teammate 3 (Plan Mode)：架构审查 → 只读分析 → 输出审查报告
    │
    └── 定期 Ctrl+T 监控 → 发现阻塞立即转向 → 完成后汇总
```

**核心操作清单**：
- [ ] Shift+Tab 开启 Delegate Mode
- [ ] 每个Teammate 5-6个独立可交付任务
- [ ] 明确定义文件边界（`src/api/users/` vs `src/api/billing/`）
- [ ] Spawn Prompt 包含：做什么、在哪里做、关注什么、输出格式
- [ ] Plan Mode 队友仅用于审查/设计，不写代码
- [ ] 每完成1个任务上报进度，避免无检查点的巨量任务
- [ ] 3-5人团队为最优，超过5人分阶段运行

### 15. Dynamic Workflows 六模式详解（R67新增 · 2026-06-12）

> Dynamic Workflows 是 Claude Code 的最新能力：Claude 根据任务动态生成 JavaScript 工作流，协调多个子 Agent 并行处理、交叉验证、迭代汇总。

#### 15.1 六种模式速查

| 模式 | 英文名 | 流程 | 适用场景 | 龙虾对标 |
|------|------|------|----------|----------|
| 分类-行动 | Classify-and-act | 分类Agent判断类型→路由到对应Agent | 工单分类（Bug/反馈/咨询） | 任务意图识别→dispatch_task路由 |
| 扇出-合成 | Fanout-and-synthesize | 任务拆成小步骤→并行执行→汇总 | 80条技术说法逐一核查 | 并行工具调用（每轮≤5） |
| 对抗式验证 | Adversarial verification | 产出Agent生成→验证Agent检查→反驳Agent复核 | 代码审查/安全分析/事实核查 | LLM-as-Judge Grader |
| 生成-筛选 | Generate-and-filter | 批量生成候选→评分/去重/筛选 | 命名/方案/架构候选项 | — |
| 锦标赛 | Tournament | 多Agent不同思路→两两比较→评审选出胜者 | CLI工具命名/产品方案选择 | — |
| 循环至完成 | Loop until done | 持续启动Agent直到停止条件满足 | 调试/根因分析/持续分拣 | 定时任务每2小时循环 |

#### 15.2 三大单Agent缺陷及工作流解法

| 缺陷 | 表现 | 工作流解法 |
|------|------|------------|
| Agentic Laziness（惰性早停） | 50项审查只处理35项就宣布完成 | 拆给多个子Agent，各自独立验证 |
| Self-preferential Bias（自我偏好） | 自己验证自己输出时倾向认可自我 | 独立验证Agent进行对抗式检查 |
| Goal Drift（目标漂移） | 长任务中逐渐偏离原始目标 | 子Agent拥有独立上下文和更聚焦目标 |

#### 15.3 六大使用场景

1. **大规模迁移与重构**：项目级字段改名/代码迁移，子Agent在独立worktree中修改
2. **深度研究**：并行搜索→抓取→对抗验证→合成报告（`/deep-research` skill已用上）
3. **深度验证**：抽取待核查声明→逐条验证→检查来源质量
4. **大规模排序**：1000行数据→两两比较/先分桶再排序
5. **记忆与规则遵守**：每条规则配一个verifier agent，从历史纠错中沉淀回CLAUDE.md
6. **根因分析**：不同Agent从不同证据提假设→验证+反驳分别检查

#### 15.4 动态工作流启动方式

```
方法一：明确要求 Claude 创建工作流
方法二：启用 ultracode 设置 → Claude 自动判断何时启用
方法三：/goal + /loop 结合使用
```

每工作流支持：16个并发子Agent、1000个总Agent、中断后从中断位置继续。

### 16. Agent SDK 编排者-工作者三步法（R67新增）

```
步骤1：编排者获取任务 → 生成 task.md（含子任务列表）
步骤2：循环委托工作者 → 每个工作者执行一个子任务 → 返回结构化结果
步骤3：编排者收集所有结果 → 合成最终产出 → 标记任务完成
```

**关键参数速查**：

| 参数 | 建议值 | 说明 |
|------|--------|------|
| max_turns | 15-30 | 单Agent最大轮次，防止无限循环 |
| max_budget_usd | $3-5 | 单Agent美元预算上限 |
| temperature | 0-0.3（确定性）/ 0.7-1.0（创意） | 创造性控制 |
| permission_mode | acceptEdits → auto → plan | 权限递增，风险递增 |

**成本提醒**：Dynamic Workflows Token消耗为单Agent聊天的~15倍，建议从小规模、范围明确的任务开始。改一个函数/补一个测试→普通单Agent足够，不需要上工作流。

> 本文件由 Marvis 龙虾 Agent 每2小时自动更新 | 版本: v2.4_R77 | 最后更新: 2026-06-12 09:00


---

## 十七、Anthropic 官方课程协作流程提炼（R77新增 · 2026-06-12）

> 来源：Anthropic Academy Building with Claude API § Agent Architectures + Claude Code in Action 七大模块

### 17.1 Building with Claude API 中的 Agent 架构模式

Anthropic 在 API 课程 Agent 章节（11讲）中定义了四种核心架构模式：

| 模式 | 说明 | 龙虾对标 | 推荐场景 |
|------|------|---------|---------|
| **Parallelization** | 无依赖任务同时执行 | 并行 dispatch_task（上限5个） | 多文件分析/多维度评估 |
| **Operation Chaining** | 前一步输出作为后一步输入 | 串行协作（search→file→present） | 信息搜集→文档生成 |
| **Conditional Routing** | 根据中间结果决定下一步 | memory_ids 传递上下文 | 动态任务分流 |
| **Agent vs Workflow** | 灵活 vs 确定性的区分 | dispatch_task vs 定时任务 | 开放任务 vs 固定流程 |

### 17.2 Claude Code 七大模块 → 龙虾协作流程对标

| Claude Code 模块 | 龙虾现有实现 | 升级方向 |
|-----------------|-------------|---------|
| 上下文管理 | memory_ids + inherit_agent_id | 增强项目级上下文持久化 |
| Thinking & Planning | 任务分级 + 逐级降级 | 显式 Planning 模式 |
| GitHub 集成 | — | 接入 git 操作自动化 |
| MCP 服务器扩展 | shell_executor 兜底 | 建设 MCP Server 层 |
| Custom Commands | Skills + 定时任务 | 增强可复用指令库 |
| Hooks | 定时任务每2小时循环 | PreToolUse/PostToolUse 钩子 |
| Claude Code SDK | Agent SDK (dispatch_task) | 编程化 Agent 编排 |

### 17.3 课程推荐的学习路径 → 对应协作成熟度

| 学习阶段 | 推荐课程 | 对应龙虾协作能力 |
|---------|---------|----------------|
| 入门 | Claude 101 + AI Fluency | 单Agent闭环 |
| 进阶 | Building with Claude API（Tool Use + RAG） | 串行协作 |
| 开发 | API全部 + MCP ×2 + Claude Code | 并行协作 + MCP连接 |
| 生产 | Agent Skills + Subagents + Cowork | 多Agent全模式 |

### 17.4 Agent SDK 三种编排模式（R78新增）

Anthropic 2026年发布 Claude Agent SDK，提供三大编排架构：

**模式一：Orchestrator 架构（调度器模式）**
```
Orchestrator（Opus，任务拆解+委派+合并）
  ├── SearchAgent（搜索研究，Haiku/快）
  ├── WriterAgent（撰写生成，Sonnet/质量）
  ├── ReviewerAgent（审校验证，Haiku/校验）
  └── GeneralAgent（通用任务，Sonnet）
```
- 龙虾对标：主 Agent dispatch_task → 多 file-agent/computer-agent/app-agent 并行
- 最佳场景：多维度分析、跨域任务、需中央决策的复杂任务

**模式二：Pipeline 架构（管道模式）**
```
搜索(Research) → 撰写(Writer) → 编辑(Editor) → 格式化(Formatter) → 输出
```
- 龙虾对标：串行协作（search → file → present）
- 模型混合策略：Research用Haiku（便宜快速）、Writer用Sonnet（质量优先）、Editor用Haiku（格式校验）
- 最佳场景：文档生成、数据分析流水线、有严格依赖关系的序列任务

**模式三：Mesh 架构（网状模式）**
- 多Agent直接通信，无中央调度器
- Agent Teams实验功能即Mesh模式雏形
- 适用：需跨层协调的复杂系统、竞争假设调试、并行研究+新模块开发

**编排决策表**：

| 维度 | Orchestrator | Pipeline | Mesh |
|------|-------------|----------|------|
| 中央控制 | 有（Orchestrator） | 无（数据流驱动） | 无（分布式通信） |
| 并行能力 | 高（子Agent可并行） | 低（依赖串行） | 最高（全去中心化） |
| 可调试性 | 中（需追踪委派链） | 高（线性单向） | 低（网状路由复杂） |
| 龙虾对标 | dispatch_task并行 | 串行循环 | 未来Agent Teams |
| 推荐优先度 | ★★★★★ | ★★★★☆ | ★★★☆☆ (实验阶段) |

### 17.5 Plugins 多Agent协作打包体系（R78新增）

**核心理念**：Skills + Agents + Hooks + MCP 打包为一个可安装、可分享的协作单元。

**标准插件结构**：
```
my-plugin/
  .claude-plugin/plugin.json   # 清单：名称/描述/版本
  skills/                      # Agent Skills（自动调用）
  agents/                      # 自定义子代理（任务委派）
  hooks/                       # 事件钩子（生命周期触发）
  .mcp.json                    # MCP服务器定义
```

**龙虾对标**：
- 技能库 `E:\龙虾AI主控中心\我的AI分身\技能库\` 对应 Skills 目录
- 子Agent配置 对应 Agents 目录
- 定时任务每2小时循环 对应 Hooks 周期触发
- shell_executor 兜底 对应 MCP 外部连接

**插件协作生命周期**：
1. 安装 → `/plugin install` 一键注册所有组件
2. 启用 → 组件自动注入到 Agent 上下文
3. 任务触发 → Skills 自动匹配 / Agents 被委派 / Hooks 事件响应
4. 禁用 → `/plugin disable` 释放上下文资源
5. 更新 → 插件升级覆盖旧版配置

---

> 本次更新: v2.5_R78 · Anthropic Agent SDK编排模式 + Plugins协作体系

---

## 来自 Anthropic 官方课程的多Agent协作补充（2026-06-14）

### Agent 三级架构选择决策树
Claude Code 提供三种 Agent 协作层级，根据任务复杂度选择：

| 层级 | 名称 | 通信方式 | 上下文 | 适用场景 | 决策准则 |
|------|------|----------|--------|----------|----------|
| Level 1 | Subagents | 仅向主Agent汇报 | 独立会话 | 可重复独立任务 | 单文件修复、代码审查、测试生成 |
| Level 2 | Agent View | 主Agent派发/窥探 | 持久化会话 | 3-10个独立任务 | 批量清理、多模块独立开发 |
| Level 3 | Agent Teams | 成员间直接通信 | 独立会话+共享任务列表 | 跨文件相互依赖任务 | 多模块功能开发、代码库审查 |

### Agent Teams 决策框架
什么时候用什么：
- **单个 prompt / 单文件修复** → 常规 Claude Code 会话，无需 Agent
- **3个独立任务，无依赖** → Agent View，同时派发3个任务，完成后检查
- **可重复工作流（审查/测试/文档）** → 带 YAML 配置的 Subagents，每次一致
- **有依赖关系的多文件功能开发** → Agent Teams，主导Agent协调，成员协作
- **通宵清理积压任务** → 带 --max-budget-usd 上限的 Headless 模式

### 成本优化原则
1. 主导 Agent 用 Opus 处理复杂协调任务
2. 所有团队成员默认用 Sonnet，成本仅为 Opus 的 1/5
3. 为每个 Agent 设置独立预算上限（如每个 $3 × 5 Agent = 团队上限 $15）
4. 独立任务不需要 Agent Teams 的协调开销，有依赖关系的任务不应该在隔离的 Agent View 中运行

### Agent Teams 七步构建流程
1. 理解三级架构（Subagents → Agent View → Agent Teams）
2. 启用 Agent Teams：export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
3. 编写团队 Prompt：描述完整项目，让主导 Agent 拆解和分配角色
4. 路由 Model 节省成本：主导 Opus + 成员 Sonnet
5. 使用 Agent View Dashboard 管理：dispatch / peek / attach
6. 建立决策框架：按复杂度选择正确协作模式
7. 添加 Guardrails：权限 deny 清单 + 每个 Agent 独立预算上限

### 多 Agent 协作安全约束
```
{
  "permissions": {
    "deny": [
      "Bash(rm:*)", "Bash(sudo:*)", "Bash(chmod:*)",
      "Edit(/**/*.env)", "Edit(/**/*.pem)"
    ]
  },
  "maxBudgetUsd": 15
}
```

---

## Anthropic官方课程R80同步：多Agent协作流程

### Dynamic Workflows 使用场景
1. **代码库级漏洞扫描**：对全仓库进行系统性安全检查
2. **大规模文件迁移**：500+文件的批量重构
3. **交叉验证研究**：从多个独立角度研究同一问题，交叉对比结论
4. **复杂规划**：在提交执行前从多个独立角度起草方案

### Agent Teams 协作流程
1. 领导代理接收总体任务
2. 领导代理将任务分解给多个同级代理
3. 各代理独立执行，中间结果存入共享上下文
4. 领导代理汇总结果并决策
5. 适时请求人工介入确认


### Git Worktrees 实践（R84新增）

Agent Teams 中多个队友可能同时修改同一仓库的不同文件。Git Worktrees 是防止文件冲突的标准解决方案：

**每队友独立 Worktree 分支**：
```bash
# 为每个队友创建独立工作区
git worktree add ../project-reviewer-a feature/security-review
git worktree add ../project-reviewer-b feature/perf-review
git worktree add ../project-reviewer-c feature/test-coverage

# 各队友在独立 worktree 中工作，互不干扰
```

**合并最佳版本**：
队友完成后，人工选择最优质的分支合并到主分支：
```bash
git merge feature/perf-review  # 选择性能审查的最佳结果
git worktree remove ../project-reviewer-a  # 清理不需要的 worktree
```

**防文件冲突原理**：
每个 worktree 有独立的 `.git` 索引和工作区文件副本。队友 A 修改 `src/auth.ts` 不会与队友 B 对同一文件的修改冲突——它们在各自分支上独立演进，直到 merge 阶段才需要解决冲突。

### Token 成本对比表（R84新增）

| 模式 | Token 开销 | 计费单位 | 典型场景成本 |
|------|-----------|---------|------------|
| **Subagent** | 低 | 子代理独立 context + 结果摘要回传 | 代码审查：~5K tokens |
| **Agent Teams** | 高（7倍+） | 每个队友独立 Claude 实例 | 5队友竞争调试：~50K+ tokens |
| **Managed Agents** | 按 session-hour | Token费 + $0.08/h 运行时 + Web搜索费 | 1h Opus session：~$1.95 |

**成本优化决策树**：
- 专注任务只需结果 → Subagent（最低成本）
- 需要讨论和协作 → Agent Teams（接受 7 倍+ Token 开销）
- 需要生产部署 + 多用户 → Managed Agents（接受 API 计费模式）

> **核心原则**：Token 成本随协作复杂度指数增长。能用 Subagent 解决的绝不用 Agent Teams，能用单 Agent 调用解决的绝不用多 Agent 编排。



### 从 Subagents → Agent Teams → Dynamic Workflows 的升级路径
- 单一子任务（<10分钟）→ Subagents
- 多代理协作需人工监督 → Agent Teams  
- 大规模编排需可审计可重跑 → Dynamic Workflows

### Claude Code 最佳实践（R80更新）
- /config 中启用 Dynamic Workflows
- /deep-research 运行内置研究工作流
- 使用 JS 脚本描述编排逻辑，存入项目仓库
- 工作流脚本可被团队成员复用和审计

> 同步自：Anthropic官方课程390节全集 R80 | 2026-06-14
