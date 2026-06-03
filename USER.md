---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_737aeca25ef011f1b5095254007bceed
    ReservedCode1: Oza8K8cAsySK9GNe36Wqjy9V4u4JsTlNn93jG3vUG6P9aq5tIyh7c4vwCd2192d9MZ2/cKQTNtyqc1MyC3R0iwWXe4rFYUxIWBa4OAqG01QDoXoAJ7vOr5WGCFg6/INUasca2RjnFahfMao3rmkNUbM3NhJmrgcUb9mqWpmpRxhaOhmDqI+74A779S0=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_737aeca25ef011f1b5095254007bceed
    ReservedCode2: Oza8K8cAsySK9GNe36Wqjy9V4u4JsTlNn93jG3vUG6P9aq5tIyh7c4vwCd2192d9MZ2/cKQTNtyqc1MyC3R0iwWXe4rFYUxIWBa4OAqG01QDoXoAJ7vOr5WGCFg6/INUasca2RjnFahfMao3rmkNUbM3NhJmrgcUb9mqWpmpRxhaOhmDqI+74A779S0=
---

# USER.md — 多Agent协作流程（龙虾AI分身用户指南）

> **版本**：v2.0 | **创建日期**：2026-06-01 | **更新日期**：2026-06-01
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

## 十二、[R48 Anthropic Academy补全] 多Agent协作深度最佳实践

> **来源**：Anthropic Academy AC-207 Subagents + AC-E03 Agentic AI + AC-202 Claude API | 2026-06-03
> **知识库**：[Anthropic官方课程-完整知识库.md](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-完整知识库.md)

### 12.1 Subagent任务委派规范（来源：AC-207 Introduction to Subagents）

**委派决策矩阵**：

| 任务特征 | 主Agent处理 | Subagent处理 | 理由 |
|---------|-----------|-------------|------|
| 多步复杂逻辑 | ✅ | ❌ | 需全局视野和协调 |
| 单一明确目标 | ❌ | ✅ | 独立上下文效率更高 |
| 需要跨文件关联 | ✅ | ❌ | 需全局文件感知 |
| 独立文件/模块操作 | ❌ | ✅ | 并行加速 |
| 决策需综合判断 | ✅ | ❌ | 需要汇总多方信息 |
| 机械重复检查 | ❌ | ✅ | Subagent适合标准化任务 |

**委派流程**：
```
主Agent判断任务特征 → 匹配委派决策矩阵 → 
  适合Subagent → 生成Spec（输入/输出/工具/超时）→ 并行/串行派发 → 收集摘要
  适合主Agent → 直接处理
```

### 12.2 并行子Agent编排模式（来源：AC-207 Subagents + AC-202 Claude API）

**四种标准编排模式**：

| 模式 | 结构 | 适用场景 | 实例 |
|------|------|---------|------|
| **扇出-收集** | N路并行→主Agent聚合 | 无依赖独立任务 | 多平台文档生成、多维度代码审查 |
| **流水线** | A→B→C 串行 | 有严格数据依赖 | 数据提取→清洗→分析→报告 |
| **路由** | 主Agent→按条件分发→指定Subagent | 任务类型不同 | 按文件类型路由到不同专业Subagent |
| **对抗验证** | 生成Agent + 审查Agent 并行 | 质量关键任务 | 代码生成+安全审查+风格检查并行，取交集 |

**并行启动参数标准**：
```yaml
parallel_launch:
  max_concurrent: 由协议#54/90动态计算
  timeout_per_agent: 120s
  retry_max: 3
  retry_backoff: exponential
  result_format: JSON # 统一聚合格式
```

### 12.3 主Agent-Subagent通信协议（来源：AC-207 + AC-E03）

**通信接口标准**：

```
主Agent → Subagent（请求）:
{
  "task_id": "uuid",
  "spec": {
    "goal": "单一明确目标",
    "input": { ... },
    "output_schema": { ... },
    "tools": ["工具白名单"],
    "max_tokens": 预算,
    "timeout_seconds": 超时
  }
}

Subagent → 主Agent（响应）:
{
  "task_id": "uuid",
  "status": "success | partial | failed",
  "summary": "结构化摘要（非原始数据）",
  "result": { ... },
  "confidence": 0.0-1.0,
  "errors": ["如有"]
}
```

**通信原则**：
- **只返回摘要**：Subagent不返回完整中间产物，仅返回结构化摘要和结论
- **置信度必带**：所有Subagent响应必须附带置信度评分，低于0.7需主Agent交叉验证
- **错误不静默**：任何失败返回结构化错误信息，不得返回空响应
- **龙虾对齐**：协议#61 多Agent置信度验收协议、协议#32 编排者-工作者结构化结果协议

### 12.4 Skills标准化流程（来源：AC-205 Agent Skills + AC-207 Subagents）

**Skill标准化五步法**：

| 步骤 | 动作 | 产出物 |
|------|------|--------|
| 1. 需求识别 | 识别可标准化的重复工作流 | 工作流清单 |
| 2. 边界定义 | 明确Skill的触发条件、输入输出、工具范围 | Skill Spec |
| 3. 编写测试 | 编写Evals/Benchmarks验证Skill行为 | 测试用例集 |
| 4. 团队验证 | 团队内Review + Rubric评分 | Review记录 |
| 5. 发布维护 | 发布到Skills目录 + 定期Curator评估 | 版本化Skill文件 |

**Skill命名规范**（Anthropic官方推荐）：
- `动词-对象` 格式：`review-security`、`deploy-staging`、`generate-report`
- 避免模糊词：不使用 `helper`、`utils`、`misc`
- 与Subagent一致：Skill名称与其服务的Subagent名称保持对应

### 12.5 Claude Code多Agent协作模式（来源：AC-201 Claude Code in Action）

**五层协作架构**：

```
CLAUDE.md（项目宪法 + 规则）
   ↓
Hook层（生命周期注入：Start/Stop/PreToolUse/PostToolUse）
   ↓
Skill层（按需加载的专业知识：~/.claude/skills/）
   ↓
Subagent层（独立上下文子代理：.claude/agents/）
   ↓
Plugin层（Skills+Hooks+MCP配置打包分发）
```

**协作触发规则**：
- **文件类型触发**：`.py` → `python-expert` Subagent；`Dockerfile` → `devops` Subagent
- **关键词触发**：`deploy` → 加载 `deploy` Skill；`security` → 加载 `security-review` Skill
- **复杂度触发**：任务token消耗预测 > 阈值 → 自动拆分为Subagent
- **龙虾对齐**：协议#111 Agent技能四件套生态分发、协议#135 Claude Code四件套扩展体系适配

### 12.6 Agent Team协作模式（来源：AC-E03 Agentic AI + Coze 3.0）

**三种Team结构**：

| 结构 | 通信方式 | 适用场景 |
|------|---------|---------|
| 层级式 | 主Agent → 领域Agent → 执行Agent | 大型项目、明确分工 |
| 对等式 | Agent间直接通信、共享任务板 | 探索性任务、去中心化 |
| 混合式 | 层级调度 + 对等协作 | 复杂多变任务 |

**龙虾对齐**：协议#160 去中心化自组织Agent团队、协议#141 Coze3.0三Agent接入协同

---

> **版本**：v2.2（R48 Anthropic Academy补全）
> **知识来源**：Anthropic Agent Teams + Harness + Managed Agents + Anthropic Academy 23 Courses + 龙虾全域模板v3.44
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\AGENTS.md) | [Anthropic官方课程-完整知识库.md](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-完整知识库.md)
*（内容由AI生成，仅供参考）*
