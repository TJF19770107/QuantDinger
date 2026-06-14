# USER.md — 多Agent协作流程

> 来源：Anthropic官方课程提炼 · 2026-06-12 R18
> 定位：面向用户和调度层的多Agent协作操作手册

---


> 关联文档：[[Anthropic官方课程-390节全集]] — 18门课程全量索引 · 2026-06-02
## 一、多Agent协作核心流程

### 1.1 任务接收与分解
```
用户需求 → 意图识别 → 领域匹配 → 子任务拆分 → Agent路由
```
1. **意图识别**：判断任务类型（文件/浏览器/应用/搜索/系统）
2. **领域匹配**：匹配最优Sub Agent（file-agent/browser/app-agent/computer-agent/search-agent）
3. **子任务拆分**：跨域任务按阶段分解，单域任务整体派发
4. **Agent路由**：明确先后依赖关系，确定执行顺序

### 1.2 单Agent闭环（推荐）
- 所有工作可合并在一次派发内完成时，**必须整包派发**
- Agent内部具备自主规划能力，无需外部指导步骤
- 正确：[派发File Agent] "找到周报并据此生成月报"
- 错误：先让File Agent找路径，再让其读取，最后再让其写文档

### 1.3 多Agent协作模式
| 场景 | 模式 | 示例 |
|------|------|------|
| 串行依赖 | A完成→B开始 | app-agent启动游戏→computer-agent调整配置 |
| 并行独立 | 同时派发 | 同时搜索多个来源 |
| 动态路由 | 基于结果决定 | 根据搜索结果决定下一步Agent |

---

## 二、Agent 调度标准

### 2.1 派发协议
```
<overall_goal> 用户原始完整需求 </overall_goal>
<current_task> 本次委托的具体任务 </current_task>
```
- `<overall_goal>` 始终保持用户原始完整需求不变
- `<current_task>` 仅写当前Agent需要完成的局部目标
- 结果导向：描述最终目标状态，不教导执行步骤

### 2.2 记忆传递机制
| 机制 | 用途 | 条件 |
|------|------|------|
| memory_ids | 传递历史工具结果 | 历史消息末尾有 `[memory_id: xxx]` 标记 |
| inherit_agent_id | 延续同名Agent对话 | 用户使用修正/回退类语言时 |

### 2.3 结果验收标准
- **验目标**：核对执行结果是否满足任务目标
- **验产物**：要求生成文件时，必须有真实文件路径
- **补缺口**：未完成目标时寻找其他Agent补全

---

## 三、Agent 协作最佳实践

### 3.1 上下文管理
- **精炼传递**：Agent间只传递必要结果，不传递完整执行过程
- **文件中介**：大批量数据通过文件系统传递，不占用上下文
- **记忆复用**：已获取的信息通过memory_ids传递，不重复获取

### 3.2 错误处理
- **失败不盲重试**：分析失败原因后再调整策略
- **同类失败上限2次**：超出后降级或交还用户
- **优雅降级**：Agent失败时自动降级到Skill/Tool层

### 3.3 并行调度
- 无依赖的多个Agent调用**必须并行发起**
- 每轮并行上限5个
- 有数据/状态/安全依赖的必须顺序执行

---

## 四、Claude Code 工作流集成

### 4.1 日常开发节奏
```
Explore → Plan → Code → Commit
```
- **Explore**：理解代码库、阅读相关文件
- **Plan**：生成执行计划，确认范围
- **Code**：编写/修改代码
- **Commit**：提交并记录变更

### 4.2 五大定制手段
| 手段 | 作用 | 粒度 |
|------|------|------|
| CLAUDE.md | 项目级记忆和约定 | 项目 |
| Subagents | 隔离上下文执行专项任务 | 任务 |
| Skills | 可复用指令模板 | 操作 |
| MCP Servers | 连接外部系统 | 集成 |
| Hooks | 确定性检查点 | 事件 |

---

## 五、MCP 集成流程

### 5.1 三层架构
```
Tools（执行）→ Resources（读取）→ Prompts（模板）
```
1. **Tools**：让Agent执行操作（函数调用、API请求）
2. **Resources**：让Agent直接访问数据（文件、数据库、API）
3. **Prompts**：预构建的指令模板，标准化交互

### 5.2 传输模式选择
| 模式 | 适用场景 |
|------|---------|
| STDIO | 本地开发、单机部署 |
| StreamableHTTP | 生产环境、远程服务 |

---

> 核心法则：专业的事交给专业的Agent，结果导向、记忆复用、失败降级。

---

## [更新日期: 2026-06-12 R17] Agent SDK 多Agent协作新模式

> 来源：Anthropic Agent SDK 官方文档 + code-smarter.com 实战指南

### 1. 自动匹配与显式调用的双模路由

| 模式 | 机制 | 适用场景 |
|------|------|---------|
| 自动匹配 | Claude根据description字段自动判断 | 常规任务，信任Agent判断 |
| 显式调用 | 在prompt中指名Agent | 明确知道用哪个Agent，或需要强制路由 |

**自动匹配写法范例**：
```
description: "Performance optimization specialist for query tuning"
→ 当prompt提到"优化查询"时自动触发
```

**显式调用写法范例**：
```
"Use the code-reviewer agent to check the authentication module"
→ 绕过自动匹配，直接调用
```

### 2. 并行化执行模型

多个子代理可同时执行，总耗时 = 最慢子代理的耗时（而非所有子代理耗时之和）。

```
传统串行：安全检查(2min) → 测试覆盖(3min) → 风格审查(2min) = 7min
并行执行：安全检查(2min) ‖ 测试覆盖(3min) ‖ 风格审查(2min) = 3min
```

**并行条件**：子任务之间无数据依赖、无状态依赖、无安全依赖。

### 3. Agent OS五层协作模型

```
记忆层(CLAUDE.md) → 能力层(Skills+Commands) → 委托层(Subagents)
    → 自动化层(Hooks) → 集成层(MCP)
```

**协作要点**：
- CLAUDE.md：两次纠正Claude同样问题 → 写入项目记忆
- Skills：通过frontmatter声明触发条件，allowed-tools限制工具
- Subagents：主线程编排，重活在子代理
- Hooks：格式化 + 安全规则是必须配置的两项
- MCP：构建领域专属MCP Server将AI从通用变为竞争优势

### 4. 子代理恢复机制（Resume）

- 子代理完成后返回 `agentId: <id>`
- 通过 `resume: sessionId` 恢复同一会话
- 子代理保留完整对话历史（工具调用/结果/推理）
- 内置Explore和Plan为一次性代理，不返回agentId
- 需恢复时使用custom agent或general-purpose


---

## [更新日期: 2026-06-01] 多Agent协作流程

> 来源：Anthropic 官方 Multi-agent coordination patterns + Claude Code Subagents 实战

### 1. Orchestrator-Subagent 工作流编排

**核心流程**：
```
用户任务 → Orchestrator（规划分配）
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
Subagent A  Subagent B  Subagent C
（安全检查）（测试覆盖）（代码风格）
    │           │           │
    └───────────┼───────────┘
                ▼
        Orchestrator（综合结果）
                │
                ▼
          统一审查报告
```

**编排要点**：
- Orchestrator 保持全局视图，不陷入细节
- 子任务间独立性越高效果越好
- Subagent 一次性运行，完成即终止
- 结果综合阶段需去重和冲突解决
- 建议设置超时：单个 Subagent 不超过 5 分钟

**适用场景**：
- PR 代码审查（安全/测试/风格/架构分项审查）
- 文档多步骤处理（提取→翻译→格式化）
- 项目初始化（脚手架→依赖安装→配置→验证）

### 2. Agent Teams 长时域任务分配

**核心流程**：
```
Coordinator → 任务队列
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
  Worker A    Worker B     Worker C
  （服务1）    （服务2）     （服务3）
  迁移完成     迁移中        迁移完成
     │            │            │
     └────────────┼────────────┘
                  ▼
         Coordinator（收集 + 集成测试）
```

**分配策略**：
- Worker 从共享队列主动认领任务（非推送）
- Coordinator 只分配工作 + 收集结果，不重置 Worker
- Worker 持久存在，跨任务积累上下文 → 性能递增
- 独立性是核心要求：Worker 不能共享中间发现

**适用场景**：
- 大型代码库框架迁移（每个服务独立迁移）
- 批量数据处理（每个分区独立处理）
- 多仓库同步升级

### 3. Generator-Verifier 质量保障循环

**核心流程**：
```
任务 → Generator → 输出 → Verifier（评估）
                ↑                    │
                │    ┌───────────────┘
                │    ▼
                └── 反馈（具体问题）
                     
循环终止条件：Verifier 接受 OR 达到最大迭代次数
```

**质量保障要点**：
- 验证标准必须明确（不能说"检查好不好"）
- 生成和验证必须是可分离的技能
- 设置最大迭代次数（建议 3-5 次）
- 配合降级策略：超限后升级给人类 / 返回最佳尝试
- Verifier 的反馈必须具体（如"功能归属到错误的定价层级"）

**适用场景**：
- 客服邮件回复质量保障
- 代码生成的测试验证
- 事实核查和合规审查
- 基于量规的评分

### 4. Message Bus 事件驱动流水线

**核心流程**：
```
事件源 → [Router] → 订阅Agent
                       │
                ┌──────┼──────┐
                ▼      ▼      ▼
            调查A   调查B   调查C
                │      │      │
                └──────┼──────┘
                       ▼
                  [Router] → 响应协调
```

**流水线设计要点**：
- Agent 通过 publish/subscribe 松耦合交互
- Router 是系统核心：路由准确性决定系统可靠性
- 新增 Agent 无需重新布线现有连接
- 必须建立全链路日志关联机制
- LLM-based Router 提供语义灵活性但有自身失败模式

**适用场景**：
- 安全运营自动化（告警分类→专题调查→响应）
- CI/CD 事件驱动流水线
- 微服务事件编排

### 5. Shared State 协作式知识库

**核心流程**：
```
    ┌──────────┐
    │ Agent A  │（学术文献）
    │          │
    └────┬─────┘
         │ 写入发现
    ┌────▼─────────────────────┐
    │      Shared Store         │
    │  （数据库/文件系统/文档）   │
    └────┬─────────────────────┘
         │ 读取发现
    ┌────▼─────┐   ┌──────────┐
    │ Agent B  │   │ Agent C  │
    │（行业报告）│   │（新闻报道）│
    └──────────┘   └──────────┘
    
终止条件：时间预算 / 收敛阈值 / 指定Agent判定
```

**协作要点**：
- 无中心协调器，Agent 自主读写
- 发现实时流通，无需等待路由
- 必须设计终止条件：时间预算、收敛阈值（N周期无新发现）、或指定 Agent 判定
- 警惕反应式循环：A写→B读→B写→A读→A写...无限消耗 token

**适用场景**：
- 研究综合（多视角并行探索）
- 知识库共建
- 去中心化的协作分析

### 协作模式速查

| 任务特征 | 推荐模式 | 关键考量 |
|---------|---------|---------|
| 质量保障 + 明确标准 | Generator-Verifier | 验证标准必须具体 |
| 任务可分解为独立子任务 | Orchestrator-Subagent | 默认首选 |
| Worker需要跨任务积累经验 | Agent Teams | 独立性是硬要求 |
| 事件驱动 + 扩展性要求 | Message Bus | 路由准确性决定成败 |
| 发现需实时共享 + 去中心化 | Shared State | 必须设计终止条件 |

---

## [更新日期: 2026-06-02] Subagent 五触发模式 + 四工作模式

> 来源：Anthropic 官方 Subagents 文档 + IceYao 深度解析 · 2026-06-02

### 6. Subagent 五种触发方式速查

| 方式 | 触发机制 | 适用场景 | 持久性 |
|------|---------|---------|--------|
| **对话式调用** | 自然语言 "使用子代理探索..." | 临时探索、一次性审查 | 仅当次会话 |
| **自定义子代理** | 定义 Markdown 文件 + YAML Frontmatter | 重复性任务（安全审查、测试生成） | 跨会话可复用 |
| **CLAUDE.md 指令** | 项目级规则始终加载 | 团队一致性、项目约定 | 始终生效 |
| **Skills 技能** | 按需加载，description 匹配触发 | 复杂多步骤工作流 | 按需 |
| **Hooks 挂钩** | 生命周期事件自动触发 | 提交前审查、质量门 | 事件驱动 |

**从临时到自动化的演进路径**：
```
对话式调用（临时探索）
  → 识别重复模式
    → 自定义子代理（固化规则）
      → CLAUDE.md 指令（全局生效）
        → Skills 技能（按需组合）
          → Hooks 挂钩（100%自动执行）
```

### 7. 四大工作模式操作指南

#### 7.1 实施前研究模式

```markdown
使用场景：实现功能前需要了解现有代码库

触发指令模板：
"Before I implement [功能], use a subagent to research:
- How is [相关功能] currently handled?
- What patterns already exist?
- Where should new logic live based on current architecture?
Summarize findings, then we'll plan the implementation."

优势：主对话不被数十个文件的内容占满
```

#### 7.2 并行修改模式

```markdown
使用场景：多个文件独立应用相同的模式修改

触发指令模板：
"Use parallel subagents to update [操作] in these files:
- [文件A路径]
- [文件B路径]
- [文件C路径]
Each should follow the pattern in [参考文件路径].
Work on all simultaneously."

关键约束：必须确保文件之间无相互依赖
```

#### 7.3 独立审查模式

```markdown
使用场景：需要不受之前对话影响的客观审查

触发指令模板：
"Use a fresh subagent with read-only access to review [代码/文档].
It should NOT see our previous discussion. I want an unbiased review.
Check for: [安全检查项]. Be critical."

核心原理：消除 AI 对自己代码的确认偏误
```

#### 7.4 管道工作流模式

```markdown
使用场景：具有清晰交接的阶段化流程

触发指令模板：
"Build this as a pipeline:
1. First subagent: [设计] and write to [输出文件A]
2. Second subagent: [实现] based on that spec
3. Third subagent: [测试/验证] the implementation
Each stage completes before the next begins.
Use output files as the handoff mechanism."

交接机制：文件（非对话历史）作为阶段间的交接物
```

### 8. Subagent 协作防误用清单

| 场景 | 不要用 Subagent | 原因 | 替代方案 |
|------|----------------|------|---------|
| 简单单步任务 | 委派到 Subagent | 开销超过任务本身 | 主对话直接执行 |
| 需要实时交互 | 派到 Subagent | Subagent 不能调用 AskUserQuestion | 主对话处理 |
| 强依赖共享上下文 | 拆成多个 Subagent | 独立上下文导致信息割裂 | 保留在主对话 |
| 结果每次可预测 | 创建 Subagent | 隔离收益不大 | Skills 模板即可 |
| 跨代理状态持久 | 依赖 Subagent 记忆 | 完成后不保留状态 | 使用 Agent Teams + memory |

---

## 新增第六节：Dynamic Workflows 实战流程（2026-05-28 新特性）

### 6.1 动态工作流触发机制
| 触发方式 | 操作 | 说明 |
|---------|------|------|
| 手动命令 | "Create a workflow" | 显式创建编排脚本 |
| UltraCode模式 | 设置 effort=xhigh | Claude 自动决定何时启动工作流 |
| 自动模式 | 启用 auto mode | 推荐，让 Claude 自主判断任务规模 |

### 6.2 并行Agent调度实战
```
> 用户: "把这个50万行代码库从Vue2迁移到Vue3"
├─ Claude Code生成 JavaScript编排脚本
├─ 自动拆分为 N 个子任务
├─ 并行派发 16 个子代理（每代理处理独立模块）
│   ├─ sub-agent-01: components/ 目录迁移
│   ├─ sub-agent-02: views/ 目录迁移
│   ├─ ...
│   └─ sub-agent-16: 全局状态管理重写
├─ 对抗验证循环：实现→测试→修复→重测（自动循环直到通过）
└─ 所有子代理结果汇总反馈给用户
```

### 6.3 关键操作约束
- **范围定义**：从少范围任务开始，评估 Token 用量后再扩大
- **成本预警**：Dynamic Workflows Token 消耗 = 普通会话 × N 倍（N = 3~50）
- **脚本可复用**：生成的 JavaScript 编排脚本可版本管理、跨项目复用
- **断点恢复**：中断后从断点恢复，不需重跑整个工作流

### 6.4 Harness 配置维护原则（2026年5月更新）
- **每 3~6 个月审查一次配置**：旧模型时代的约束可能变成新模型的束缚
- **重大模型发布后立即审查**：Opus 4.7→4.8 后，部分"拆分单文件"类规则需要移除
- **Hooks 不只是安全门**：使用 stop hook 自动反思并建议更新 CLAUDE.md
- **Skills 路径绑定**：按子目录激活不同 Skills，避免全项目膨胀

---

## 七、R45新增：多Agent五模式协调流程（2026-06-02）

> 来源：Anthropic《Multi-agent coordination patterns》2026

### 7.1 五种模式速查

| 模式 | 何时使用 | 何时避免 |
|------|---------|---------|
| Generator-Verifier | 输出质量要求高+评估标准明确 | 评估标准模糊/主观判断 |
| Orchestrator-Subagent | 任务拆分明确+子任务有界 | 子任务需长时间持续 |
| Agent Teams | 并行独立工作负载 | 子任务互相依赖 |
| Message Bus | 事件驱动管道+Agent生态增长 | 简单线性工作流 |
| Shared State | 协作研究+去中心化 | 反应性循环风险高 |

### 7.2 模式演进判断

```
当前模式挣扎 → 判断瓶颈类型 → 按需演进

Orchestrator-Subagent 信息瓶颈 → Agent Teams（Worker持久化）
Orchestrator-Subagent 工作流不可预测 → Message Bus（事件驱动）
Agent Teams 需要共享发现 → Shared State（去中心化）
Message Bus 需要累积知识 → Shared State（共享存储）
```

### 7.3 Harness调度最佳实践

**CLAUDE.md 分层原则**：
- 根目录：项目是什么+框架+关键约定（克制！）
- 子目录：局部约定（自动叠加加载）
- 专业知识 → 放 Skills（按需加载，不放 CLAUDE.md）

**Hooks 自我进化**：
- Stop Hook：会话结束反思→提议更新 CLAUDE.md
- Start Hook：根据当前模块动态加载团队配置
- PreToolUse：拦截危险操作（.env触碰、force push）

---

> 更新日期：2026-06-02 R45 | 新增：五模式协调流程+Harness调度最佳实践

---

## 八、R53新增：Multi-Agent API 模式与协作深化（2026-06-05）

> 来源：Anthropic 官方 Multi-Agent API Patterns + Agent Teams + 企业部署文档 · 2026-06-05

### 8.1 四大 API 模式

#### Pattern 1：并行扇出 (Parallel Fan-Out)

同时处理 N 个独立项目。使用 Haiku 处理单项（便宜快速），Opus 做最终综合。

```
         ┌── Worker(Haiku) → 结果1 ──┐
任务 →  ──┼── Worker(Haiku) → 结果2 ──┼── Opus 综合 → 最终输出
         └── Worker(Haiku) → 结果N ──┘
```

**适用**：批量文档分类、多文件独立格式化、多源数据提取

#### Pattern 2：层次化编排 (Hierarchical Orchestration)

编排器分解任务 → 派生工作代理 → 收集并综合结果。每个子任务包含置信度评分。

```
Orchestrator (Opus)
  ├── 分解任务 → 子任务A + 子任务B + 子任务C
  ├── 派发 Sonnet Workers
  ├── 收集 {result + confidence_score}
  └── 综合 → 置信度加权最终输出
```

**适用**：复杂跨域任务、需要全局判断的综合分析

#### Pattern 3：检查/验证代理 (Checker-Verifier)

Agent A 生成 → Agent B 独立验证 → 反馈修正。最多尝试 N 次。

```
Generator → 输出 → Verifier → 通过 → 交付
                ↑        │
                │    ┌───┘
                └── 反馈（具体问题）
```

**适用**：代码生成验证、金融计算、合规审查。验证标准必须明确具体。

#### Pattern 4：共享上下文流水线 (Shared Context Pipeline)

顺序代理管道，每个代理构建在前一个代理的输出之上。

```
原始数据分析 → 趋势解读 → 执行摘要撰写 → 准确性审查
```

每个阶段维护共享历史 + 状态对象，阶段间通过文件交接。

### 8.2 四大模式速查

| 模式 | 何时使用 | 何时避免 | Token 成本 |
|------|---------|---------|-----------|
| Parallel Fan-Out | N 个完全独立子任务 | 子任务有依赖 | N × Haiku + 1 × Opus |
| Hierarchical Orchestration | 需要全局判断的复杂任务 | 简单线性任务 | 1 × Opus + N × Sonnet |
| Checker-Verifier | 输出质量要求高 + 标准明确 | 评估标准模糊 | (Gen+Ver) × max_attempts |
| Shared Context Pipeline | 阶段化顺序流程 | 阶段间可并行 | N × 模型成本 |

### 8.3 Agent Teams 使用场景与限制

**适用场景**：
- 研究与审查：多个队友同时调查不同方面，分享并挑战彼此的发现
- 新模块/功能：每个队友独立负责一个部分
- 竞争假设调试：队友并行测试不同理论，更快收敛
- 跨层协调：前端、后端、测试各由一个队友负责

**核心限制**：
- 需要 Claude Code v2.1.32+，需启用 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- Token 成本显著高于单会话（每个队友是独立 Claude 实例）
- 队友不继承 Leader 的对话历史，需在 spawn prompt 中包含任务细节
- `skills` 和 `mcpServers` frontmatter 在 Agent Teams 中不生效（从项目/用户设置加载）
- 不适合顺序任务、同文件编辑、强依赖的工作

**团队规模建议**：
- 3-5 个队友是最佳平衡点
- 每个队友 5-6 个任务避免上下文切换过度
- 从研究型任务入手，再逐步扩展到实现型任务

### 8.4 错误恢复与韧性设计

多智能体工作流比单次调用更容易失败，需要分层错误处理：

| 错误类型 | 处理策略 | 重试上限 |
|---------|---------|---------|
| RateLimitError | 指数退避重试 | 3次 |
| 529 Overloaded | 自动降级到备用模型 | 1次降级 |
| 工具调用失败 | 分析原因 → 调整参数 → 重试 | 2次 |
| 超时 | 检查点恢复 → 断点续传 | N/A |
| 不可重试错误 | 记录原因 → 人工介入 | 0次 |

**区分可重试与不可重试**：
- 可重试：RateLimitError、529 Overloaded、临时网络故障
- 不可重试：权限不足、认证失败、模型不存在、参数错误

**降级策略**：
```
主模型过载 → 自动降级到备用模型
Subagent 失败 → 主 Agent 自行处理或跳过
Worker 卡住 → 超时熔断 + 任务重新分配
```

### 8.5 成本估算方法

**模型定价参考**：

| 模型 | 输入/百万tokens | 输出/百万tokens |
|------|----------------|-----------------|
| claude-opus-4-6 | $15.0 | $75.0 |
| claude-sonnet-4-6 | $3.0 | $15.0 |
| claude-haiku-4-5 | $1.0 | $5.0 |

**成本估算公式**：

```
单次运行成本 = Σ(每个Agent的输入token × 输入价格 + 输出token × 输出价格)

预估步骤：
1. 列出所有 Agent 及各自模型
2. 估算每 Agent 的输入/输出 token 数
3. 乘以并行度
4. 加上编排器综合成本
```

**省钱铁律**：
- 编排器/综合器用 Opus（推理最强）
- 一般工作代理用 Sonnet（性价比最佳）
- 大量并行用 Haiku（~15x 更便宜）
- Explore 内置代理已默认使用 Haiku

---

> 更新日期：2026-06-05 R53 | 新增：四大API模式 + Agent Teams 场景限制 + 错误恢复 + 成本估算

---

## 九、R58新增：Claude Cowork 操作流程（2026-06-05）

> 来源：Anthropic Academy · Introduction to Claude Cowork 课程 · 2026-06-05

### 9.1 Cowork vs Chat 本质区别

| 维度 | Chat | Cowork |
|------|------|--------|
| 本质 | 对话 | 工作会话 |
| 操作对象 | 文本 | 本地文件、文件夹、应用 |
| 执行方式 | 问答 | 读取→计划→执行→产出 |
| 用户角色 | 提问者 | 指导者（steer） |
| 产出物 | 文字回答 | 真实文件（代码/文档/数据） |

### 9.2 Cowork 任务循环

```
用户描述任务 → Claude制定计划 → Claude执行操作 → 用户途中指导 → 产出最终文件
```

### 9.3 Cowork 核心能力

- **Plugin系统**：安装插件扩展Claude的工具集
- **Skills集成**：在Cowork会话中调用Skills完成专项任务
- **文件工作流**：读取→编辑→创建→组织本地文件
- **多步任务引导**：长任务过程中的steering机制
- **定时任务**：/schedule和/loop实现自动化

### 9.4 Cowork 适用场景

| 场景 | 示例 |
|------|------|
| 文档批量处理 | 格式化100个Markdown文件、生成索引 |
| 数据整理 | 从CSV提取分析、生成Excel报告 |
| 项目管理 | 自动生成周报、整理会议记录 |
| 定时自动化 | 每日数据汇总、定期代码审查 |

---

> 更新日期：2026-06-05 R58 | 新增：Claude Cowork操作流程


---

## [更新日期: 2026-06-05] Dynamic Workflows 多Agent协作（基于 Opus 4.8）

> 来源：Anthropic Opus 4.8 发布（2026-05-28）· Bun 迁移实战案例 · Dynamic Workflows 研究预览版

### 6. Dynamic Workflows 编排模式

#### 6.1 规划→拆解→并行→验证 四步法

```
用户任务 → Claude 规划（Plan）
              │
         任务拆解（Decompose）
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
 Agent A   Agent B   Agent C（并行执行，数十~数千个）
    │         │         │
    └─────────┼─────────┘
              ▼
        交叉验证（Cross-validate）
              │
        对抗证伪（Adversarial Verify）
              │
         答案收敛（Converge）
              │
         用户汇报（Report）
```

#### 6.2 与传统多Agent协作对比

| 维度 | 传统模式 | Dynamic Workflows |
|------|---------|-----------------|
| Agent 数量 | 固定（2~5个） | 弹性（数十~数千个） |
| 规划方式 | 主 Agent 即时拆解 | Claude 先规划再分发 |
| 验证机制 | 结果验收 | 内置对抗证伪 + 交叉验证 |
| 断点恢复 | 不支持 | 支持中途打断恢复 |
| 适用规模 | 单文件/单模块 | 全代码库/多仓库 |
| 典型耗时 | 分钟级 | 分钟~天数级 |

#### 6.3 适用场景判断

**适合使用 Dynamic Workflows**：
- 全服务范围 Bug 查找（各服务独立审计）
- 性能优化审计（各模块独立基准测试）
- 安全审计（各组件独立漏洞扫描）
- 大型代码库迁移（各模块独立迁移）
- 框架替换（逐个文件独立替换）
- API 废弃迁移（逐个调用点独立替换）
- 语言移植（逐个模块独立移植）
- 多角度方案验证（多个方案独立探索）

**不适合使用 Dynamic Workflows**：
- 简单问答
- 单文件修改
- 需要强上下文关联的改动
- Agent 间需要实时协调的任务

### 7. Bun 迁移案例的协作启示

Jarred Sumner（Bun 创始人）使用 Dynamic Workflows 将 Bun 从 Zig 完整移植到 Rust：

**数据**：
- 代码量：约 75 万行
- 耗时：11 天（从第一次测试到最终合并）
- 测试通过率：99.8%
- Agent 模式：先规划→并行分发数百个子代理→交叉验证→收敛

**协作启示**：
- **模块独立性是并行化的前提**：Bun 的模块间耦合度低，适合大规模并行
- **长时间运行 Agent 需要持久 Worker**：Worker 持久存在，跨任务积累上下文
- **集成测试不可省略**：即使每个模块独立验证通过，仍需全局集成测试
- **断点恢复降低风险**：中途可中止和恢复，避免长时间运行失败后全盘重来

### 8. Generator-Verifier 循环升级版

Opus 4.8 引入的对抗验证可视为 Generator-Verifier 循环的升级：

```
Generator → 输出 → Verifier（初级评估）
                     │ 通过？→ 接受
                     │ 不通过？
                     ▼
                Adversarial Agent（对抗证伪）
                     │ 发现漏洞 → 反馈 Generator
                     │ 无法证伪 → 交叉验证
                                    │
                                    ▼
                               多 Agent 投票 → 收敛
```

**升级要点**：
- 引入对抗式验证而非简单式的"检查"
- 多层验证流水线：初级 → 对抗 → 交叉
- 投票机制解决争议，非单一 Agent 裁决

---

## [更新日期: 2026-06-05] Claude Code Harness 集成流程

> 来源：Anthropic Claude Code Harness 最新最佳实践 · 2026年

### 9. 企业级五大集成手段升级

| 手段 | 升级要点 | 效果 |
|------|---------|------|
| CLAUDE.md | 精简原则——只放广泛适用内容 | 每次会话不膨胀 |
| Subagents | Dynamic Workflows 大规模并行 | 数千 Agent 协同 |
| Skills | 路径绑定 + 企业级托管分发 | 团队标准化 |
| MCP | LSP 符号级集成 | 上下文命中率提升 |
| Hooks | 自我进化（Stop Hook 自动反思更新 CLAUDE.md） | 配置自愈 |

### 10. 大规模迁移协作工作流

```
1. Coordinator Agent（规划）
   → 分析代码库结构，确定迁移范围
   → 拆分为独立模块清单
   → 设定迁移标准和验收条件

2. Worker Agents（批量 > 并行）
   → 每个 Worker 认领一个模块
   → 独立上下文执行迁移
   → 报告迁移结果和测试状态

3. Verifier Agent（验证）
   → 对每个 Worker 结果进行代码审查
   → 运行单元测试和集成测试
   → 标记失败模块供人工审查

4. Integrator Agent（集成）
   → 合并所有成功模块的变更
   → 运行全局测试套件
   → 生成最终迁移报告
```

---

## [更新日期: 2026-06-10] Claude Code Agent Teams 协作模式

> 来源：Claude Opus 4.6 + Swarm 模式 · Anthropic 2026-06

### Swarm 协作工作流

```
用户: "构建包含 OAuth、测试和文档的用户认证系统"

[Team Lead] 分析需求 → 创建计划 → 审批后进入委派模式

├── auth-backend: 实现 OAuth 提供者集成（独立 worktree）
├── auth-frontend: 构建登录/登出 UI 组件（独立 worktree）
├── test-agent: 编写认证流程集成测试（独立 worktree）
└── docs-agent: 记录 API 端点和用法（独立 worktree）

[并行执行] 所有 Agent 同时工作，通过任务板协调

[Synthesis] Team Lead 整合所有成果："认证系统完成，各专家交付如下..."
```

### 任务板协调机制

共享任务列表位于 `~/.claude/tasks/{team-name}/`：

```
{
  "id": "1",
  "subject": "实现 OAuth 回调处理器",
  "status": "in_progress",
  "owner": "auth-backend",
  "blocks": ["2", "3"],
  "description": "处理 OAuth 重定向和 token 交换..."
}
```

**自组织规则**：
1. 检查 TaskList 寻找可用工作
2. 认领未分配、未阻塞的任务
3. 完成后标记状态
4. 发现额外工作时创建新任务

### Writer/Reviewer 对抗模式（增强版）

使用 Agent Teams 的自动化版本：

| 角色 | 职责 | 上下文 |
|------|------|--------|
| **Writer Agent** | 实现功能 | 项目完整 context |
| **Reviewer Agent** | 审查差异 | 新鲜 context，只看 diff + 标准 |
| **Test Agent** | 运行验证 | 隔离环境，只运行测试 |
| **Lead Agent** | 协调流程 | 接收缺陷报告，委派修复 |

**关键原则**：Reviewer 只看到差异和标准，看不到实现推理过程，因此按自己的条件评估结果。

### 扇出并行模式（Agent Teams 版）

适用于批量迁移、大规模重构：

```
Step 1: Lead Agent 分析代码库，生成任务清单
Step 2: Lead Agent 创建专家团队，分配任务
Step 3: 各 Worker Agent 并行处理分配的文件
Step 4: 任务板自动追踪进度和依赖
Step 5: Lead Agent 综合结果，生成报告
```

### 上下文效率对比

| 指标 | 单 Agent | Agent Teams |
|------|---------|-------------|
| 平均 context 使用率 | 80-90% | ~40% |
| 大型代码库 (>5万行) | 往往超出容量 | 认知负载分散 |
| Token 膨胀 | 单次会话持续膨胀 | 每次委派刷新上下文 |
| 并行能力 | 无（串行） | 天然支持并行 |

### 对抗性审查配置

```
使用子代理根据 PLAN.md 审查速率限制器差异。
检查每个要求是否已实现、列出的边界情况是否有测试，
以及任务范围之外是否有任何更改。
报告缺陷，而不是风格偏好。
```

审查者只标记影响正确性或陈述要求的缺陷，其余视为可选建议，避免过度工程化。

---

## 八、Claude Code Advanced Patterns（R74新增 · 2026-06-11）

> 来源：Anthropic 官方 Webinar "Claude Code Advanced Patterns: Subagents, MCP, and Scaling to Real Codebases" (2026-03-24)
> 讲师：Lizzie Alvarado Ford / Alon Krifcher / Kacie Jenkins

### 8.1 四大进阶模式

| # | 模式 | 核心内容 |
|---|------|---------|
| 1 | Subagents + Hooks 编排 | 子代理并行任务、Hooks强制护栏、工具链式调用，无需人工监督每一步 |
| 2 | MCP 内部工具集成 | 将Claude Code连接到内部服务；判断何时值得构建自定义工具 vs 简单脚本 |
| 3 | 大型仓库上下文策略 | monorepos的CLAUDE.md结构设计；数十万行代码中的上下文窗口管理；保持Claude聚焦当前任务 |
| 4 | CI/CD 流水线集成 | 自动PR审查、测试生成、在人工发现前捕获回归的模式 |

### 8.2 上下文工程演进

| 阶段 | 策略 | 适用场景 |
|------|------|---------|
| 入门 | 手动提供上下文 | 小项目/单文件任务 |
| 进阶 | CLAUDE.md 持久记忆 | 团队项目/重复任务 |
| 高阶 | 动态上下文加载（Start Hook按模块加载） | monorepos/大型代码库 |
| 专家 | 子代理上下文隔离 + 精炼回报 | 百级并行任务 |

### 8.3 CI/CD 流水线 Agent 模式

```
PR创建 → Claude Code自动审查 → 生成测试 → 运行回归 → 报告结果
         ↑                    ↑
    Hooks检查护栏        MCP调用内部测试服务
```

**关键原则**：Claude Code 不应只是开发者手中的工具，而应嵌入SDLC全流程——从特性调研到CI/CD。

---

## 九、Agent Teams 扩展协作模式（R74新增）

> 来源：Anthropic 官方文档 code.claude.com/docs/en/agent-teams (2026-05)

### 9.1 三种协作模式深度

| 模式 | 机制 | 适用 | 上下文效率 |
|------|------|------|-----------|
| 并行独立 | 各子代理处理不同文件/模块，无依赖 | 多模块重构、批量分析 | 最高 |
| 串行依赖 | A输出文件→B读取→继续处理 | 管道式工作流 | 中等 |
| 对抗验证 | 两个子代理独立解决同一问题，交叉比对结果 | 安全关键代码、复杂算法 | 最低（但可靠性高） |

### 9.2 上下文效率实测

| 指标 | 单Agent | Agent Teams |
|------|---------|-------------|
| 平均上下文使用率 | 80-90% | ~40% |
| 大型代码库 (>5万行) | 往往超出容量 | 认知负载分散 |
| Token膨胀 | 单次会话持续膨胀 | 每次委派刷新上下文 |
| 并行能力 | 无（串行） | 天然支持并行 |

### 9.3 对抗审查子代理配置

```
使用子代理根据 PLAN.md 审查速率限制器差异。
检查每个要求是否已实现、列出的边界情况是否有测试，
以及任务范围之外是否有任何更改。
报告缺陷，而不是风格偏好。
```

审查者只标记影响正确性或陈述要求的缺陷，其余视为可选建议。

---

---

## 十、Agent Teams Delegate Mode 协调流程（R75新增）

> 来源：Claude Code Agent Teams v2.1.45 · 2026年6月

### 10.1 Delegate Mode 操作规范

| 操作 | 快捷键/命令 | 效果 |
|------|-----------|------|
| 开启 Delegate Mode | Shift+Tab | Lead 仅能协调，禁止直接实现代码 |
| 自然语言生成队友 | `Spawn a teammate using the xxx agent type` | 基于已有 agent 定义创建队友 |
| 要求计划批准 | `Require plan approval before they make changes` | 队友先规划后执行 |
| 指定模型 | `Use Sonnet for each teammate` | 统一或差异化模型分配 |

### 10.2 团队规模与成本平衡

| 团队规模 | 适用场景 | 协调成本 | Token消耗 |
|----------|---------|---------|-----------|
| 2-3人 | 简单审查、小范围重构 | 低 | 可控 |
| 3-5人（甜点区） | 日常开发、多模块并行 | 适中 | 合理 |
| 5-8人 | 大型项目、跨层协调 | 高（指数增长） | 显著 |
| 8人以上 | 建议分阶段运行（Phase 1: 3人 → Phase 2: 3人） | 极高 | 不推荐 |

### 10.3 Vague Prompt 反模式与正确写法

| 反模式 | 问题 | 正确写法 |
|--------|------|----------|
| `review the auth module` | 队友浪费Token探索代码库 | `Review src/auth/ for security vulnerabilities. Focus on token handling, session management, input validation. JWT stored in httpOnly cookies. Report issues with severity ratings.` |
| `fix the bugs` | 无明确边界 | `Fix crash on login page when email field is empty. File: src/pages/Login.tsx. Expected: show validation error instead of crash.` |
| `improve performance` | 无具体指标 | `Profile src/api/users.ts and identify endpoints taking >200ms. Optimize top 3 slowest. Target: reduce p95 latency by 30%.` |

### 10.4 Troubleshooting 速查

| 症状 | 根因 | 修复 |
|------|------|------|
| 队友在文件上互相覆盖 | 共享文件无隔离 | 明确定义文件边界 |
| Lead 在执行而非协调 | Delegate Mode 未开启 | Shift+Tab 开启 |
| 任务永远"In Progress" | 任务过大无check-in点 | 拆分为5-6个小任务 |
| Token燃烧无结果 | Prompt太模糊 | 加入具体路径+验收标准+约束 |
| Plan Mode队友不写代码 | 模式固定不可切换 | Spawn新Default Mode队友 |

---

## 十一、插件生态集成指南（R75新增）

> 来源：yeyulingfeng.com · Claude Code 插件生态 2026年4月

### 11.1 三套推荐配置

| 级别 | 插件 | MCP | Hooks | 目标 |
|------|------|-----|-------|------|
| 轻量级 | context7 | GitHub | 无 | 让Claude不再幻觉API，能操作GitHub |
| 标准级 | superpowers + context7 + code-review | GitHub + Playwright | auto-lint | 结构化开发 + 实时文档 + 代码审查 + 自动测试 + 自动格式化 |
| 极客级 | 标准级 + claude-mem + claude-hud + playwright | 标准级 + PostgreSQL + Figma | auto-lint + safety-guard + inject-context | 全栈自动化 + 安全护栏 + 跨会话记忆 + 实时监控 |

### 11.2 社区智慧

> "大部分人只需要一个好的 CLAUDE.md，不需要整个生态系统。"

一个深度配置的 CLAUDE.md + 3个精选插件，胜过盲目安装20个插件后的一片混乱。

---

> 版本：v1.5 · R80迭代更新 · 2026-06-14
> 关联：[[Anthropic官方课程-390节全集]] v12.0

---

## Anthropic官方课程知识同步（2026-06-12更新）

> 来源：Anthropic Academy 学习路径 + Claude Code 管理实践

### 十二、推荐进阶路径（从零到专家）

```
第1周：Skills 入门
  ├── 目标：理解按需加载机制
  ├── 实践：创建3个自定义Skill
  ├── 验证：7天内每个Skill至少被自动触发1次
  └── 产出：个人常用工作流的Skills集合

第2周：Hooks 护栏
  ├── 目标：建立确定性检查点
  ├── 实践：配置 PreToolUse 拦截危险操作
  ├── 配置 SessionStart 动态注入上下文
  ├── 配置 PostToolUse 自动格式化/验证
  └── 产出：覆盖关键生命周期的Hooks配置

第3周：MCP 外部连接
  ├── 目标：打通外部工具和数据源
  ├── 实践：安装2-3个核心MCP Server
  ├── 配置分层（user/org/managed）
  ├── 测试不同传输方式
  └── 产出：生产可用的MCP连接配置

第4周：Subagents 并行执行
  ├── 目标：掌握上下文隔离 + 并行编排
  ├── 实践：创建3个自定义子代理定义
  ├── 实践 Orchestrator-Subagent 模式
  ├── 理解只读/编辑分离铁律
  └── 产出：项目级 .claude/agents/ 配置

第2个月：Agent Teams 团队协作
  ├── 目标：多Agent并行复杂项目
  ├── 实践：3-5人团队完成一个模块化任务
  ├── 掌握 Delegate Mode、任务板、Mailbox
  ├── 成本控制与规模平衡
  └── 产出：可复用的Agent Teams配置模板

第3个月：Dynamic Workflows 大规模编排
  ├── 目标：数十~数百Agent并行
  ├── 实践：大型代码库迁移或审计
  ├── 掌握对抗验证 + 断点恢复
  └── 产出：版本化的编排脚本
```

**关键原则**：不要跳级。每个阶段熟练掌握后再进阶。Hooks未稳定前不要引入Subagents——护栏未建好就放行子代理是危险的。

### 十三、常用管理命令速查表

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `/agents` | 列出所有子代理定义 | 检查当前可用子代理 |
| `/agents create` | 交互式创建子代理 | 快速定义新子代理 |
| `/tasks` | 查看后台子代理状态 | 监控并行任务进度 |
| `/status` | 当前会话上下文使用情况 | 判断是否需要compact |
| `/compact` | 压缩上下文窗口 | 上下文接近上限时 |
| `/schedule` | 创建定时任务 | 自动化例行工作 |
| `/loop` | 创建循环任务 | 持续监控类任务 |
| `/plugin install` | 安装插件 | 扩展能力 |
| `/plugin list` | 列出已安装插件 | 审计当前配置 |
| `Ctrl+B` | 发送子代理到后台 | 不阻塞主对话 |
| `Shift+Tab` | 切换 Delegate Mode | Agent Teams 中启用纯协调模式 |
| `claude mcp add` | 添加MCP服务器 | 连接外部工具 |
| `claude mcp list` | 列出MCP服务器 | 审计外部连接 |

**Claude Code CLI 管理命令**：
```bash
# 更新Claude Code
claude update

# 管理MCP服务器
claude mcp add <name> <command> [args...]
claude mcp remove <name>
claude mcp list

# 管理插件
claude plugin install <name>
claude plugin uninstall <name>

# 配置管理
claude config set <key> <value>
claude config get <key>
```

### 十四、子代理模式决策树（面向用户）

```
你需要委派任务。先判断：

1. 任务能否被清晰描述为一个独立问题？
   ├── 否 → 保留在主对话中，边做边调整
   └── 是 → 继续

2. 执行过程是否需要我（用户）实时交互审批？
   ├── 是 → 保留在主对话中（子代理不支持 AskUserQuestion）
   └── 否 → 继续

3. 产出是否需要多个专业角度？
   ├── 是 + 角度间独立 → 并行多个只读子代理
   │   示例：安全审查 + 性能审查 + 风格审查 同时进行
   │
   ├── 是 + 角度间需要交叉验证 → Agent Teams（3-5人对抗讨论）
   │   示例：竞争假设调试、多方案择优
   │
   └── 否 → 单个子代理即可

4. 任务规模多大？
   ├── 单文件/小范围 → 主对话直接处理
   ├── 多文件/单模块 → 1个子代理（Orchestrator-Subagent）
   ├── 多模块/跨层 → Agent Teams（3-5人）
   └── 全代码库/多仓库 → Dynamic Workflows（数十~数百子代理）
```

**快速判断口诀**：
- "看一看告诉我" → 只读子代理
- "检查并报告问题" → 只读子代理 + 结构化输出
- "修复这几个独立的文件" → 并行子代理（各自独立修改不同文件）
- "帮我设计并实现一个功能" → Agent Teams（设计+前端+后端+测试）

### 十五、云平台部署选择：AWS Bedrock vs GCP Vertex AI

| 维度 | AWS Bedrock | GCP Vertex AI |
|------|-----------|---------------|
| **模型可用性** | Claude全系列（Opus/Sonnet/Haiku） | Claude全系列 |
| **吞吐上限** | 按需扩展，需申请配额 | 按需扩展，需申请配额 |
| **数据驻留** | 选择AWS区域 | 选择GCP区域 |
| **VPC/网络隔离** | AWS PrivateLink | VPC Service Controls |
| **IAM集成** | AWS IAM + SCP策略 | GCP IAM + Organization Policy |
| **审计日志** | CloudTrail | Cloud Audit Logs |
| **成本模型** | 按token计费（与Anthropic API相同） | 按token计费（与Anthropic API相同） |
| **SDK集成** | boto3 / Claude Agent SDK | google-cloud-aiplatform / Claude Agent SDK |
| **Claude Code配置** | `CLAUDE_CODE_USE_BEDROCK=1` | `CLAUDE_CODE_USE_VERTEX=1` |

**选择建议**：
- 已有AWS生态 → Bedrock（IAM统一管理、VPC已有布局）
- 已有GCP生态 → Vertex AI（GCS数据湖集成、BigQuery分析）
- 多云架构 → 通过Claude Agent SDK统一抽象，底层切换
- 合规优先 → 选择已有合规认证的云平台（SOC2/ISO27001/HIPAA）

**Claude Agent SDK 云平台切换**：
```python
# AWS Bedrock
os.environ["CLAUDE_CODE_USE_BEDROCK"] = "1"

# GCP Vertex AI
os.environ["CLAUDE_CODE_USE_VERTEX"] = "1"

# Azure AI Foundry
os.environ["CLAUDE_CODE_USE_FOUNDRY"] = "1"

# SDK 初始化时自动检测环境变量，无需改代码
```

---

> 更新日期：2026-06-12 | 新增：4周→3个月进阶路径 + 管理命令速查 + 子代理决策树 + 云平台选型对比

## 九、R18 新增：生产级多Agent协作模式（2026-06-12）

> 来源：Claude Code 子代理实战模式 + 官方最佳实践

### 9.1 五大生产级协作模式

**模式1：并行调研扇出**
```
场景：需要回答多个独立代码库问题
方案：同时派出 N 个 Explore 子代理，每个在独立沙箱执行
优势：父代理收到精简报告，上下文保持清洁
信号：看到 "in parallel using separate subagents" 时触发
```

**模式2：Worktree 隔离编辑**
```
场景：高风险重构或配置变更
方案：子代理在独立 git worktree 中执行，主代理在原 worktree 继续工作
优势：互不干扰，子代理完成后主代理审查变更并合并
```

**模式3：Writer/Reviewer 双 Agent**
```
会话 A（Writer）：实现功能 X
会话 B（Reviewer）：全新上下文中审查，查找边界情况
优势：新鲜上下文审查更客观——无实现过程先入为主影响
```

**模式4：Orchestrator-Worker 编排**
```
Orchestrator（编排者）→ 任务分解 → Workers（执行者）
编排者用强大模型（Opus），Worker 用性价比模型（Sonnet/Haiku）
性能：比单 Agent 模式高 90.2%（Anthropic 内部测试）
```

**模式5：竞争择优模式**
```
多个子代理并行生成方案 → 主代理自动排序择优
适用场景：代码生成方案对比、技术选型评估
```

### 9.2 子代理调度量化指标

| 指标 | 推荐值 | 说明 |
|------|--------|------|
| 最佳子代理数量 | 3~8 个 | 超过 8 个协调成本 > 并行收益 |
| 最大并行数 | 15 个 | 硬上限 |
| 单次派发最大 agent | 5 个（主 Agent 约束） | 超出时分批 |
| MCP Server 最佳数量 | 3 个 | 超过 5 个开始拖慢响应 |
| Skills 库开销 | ~2000 token/50 个 | 仅扫描 frontmatter 不加载正文 |

### 9.3 上下文管理实战

**5 个高频命令**：
| 命令 | 作用 | 使用时机 |
|------|------|---------|
| `/compact` | 压缩上下文释放 Token | 对话超过 20 轮后 |
| `/clear` | 清空当前会话 | 全新任务开始前 |
| `/context` | 查看上下文状态 | 确认当前 Token 使用量 |
| `/mcp` | 查看 MCP 连接状态 | 排查外部工具连接问题 |
| `/hooks` | 查看已配置的 hooks | 检查自动化规则 |

**上下文管理决策树**：
```
任务是否与上次会话相关？
  是 → claude --continue 继续
  否 → /clear 清空后开始

同一问题是否已纠正两次以上？
  是 → /clear + 重写更精准的 prompt

是否需要探索大量文件？
  是 → 使用 Explore 子代理（不污染主上下文）
```

### 9.4 委派判断更新

| 维度 | 子代理 | 主 Agent |
|------|--------|---------|
| 代码探索/搜索 | Explore 子代理（只读、快速） | 简单查找 |
| 方案设计 | Plan 子代理（先探索再规划） | 简单修改 |
| 代码实现 | **主 Agent**（子代理做实现浪费 Token） | 主 Agent |
| 代码审查 | 专用子代理（全新上下文更客观） | 简单审查 |
| 测试执行 | Bash 子代理（独立 sandbox） | 手动验证 |
| 高风险变更 | Worktree 隔离子代理 | 低风险变更 |

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

### 从 Subagents → Agent Teams → Dynamic Workflows 的升级路径
- 单一子任务（<10分钟）→ Subagents
- 多代理协作需人工监督 → Agent Teams  
- 大规模编排需可审计可重跑 → Dynamic Workflows

### Claude Code 最佳实践（R80更新）
- /config 中启用 Dynamic Workflows
- /deep-research 运行内置研究工作流
- 使用 JS 脚本描述编排逻辑，存入项目仓库
- 工作流脚本可被团队成员复用和审计

### Anthropic官方课程R85同步：多Agent协作五种生产模式

| # | 模式 | 核心机制 | Agent SDK 实现 | 适用场景 |
|---|------|---------|---------------|---------|
| 1 | Divide-and-Conquer | 拆分→并行子代理→聚合 | 主Agent 同时 dispatch 多个子代理 | 大型代码审查、多文件迁移 |
| 2 | Specialist Routing | 按任务类型路由到专家 | 根据 task 内容匹配 AgentDefinition | 前端/后端/数据库分离 |
| 3 | Parallel Research | 多角度并行研究→交叉验证 | 同时派发不同角度的研究子代理 | 技术调研、竞品分析 |
| 4 | Judge-and-Iterate | 生成→评委打分→低于阈值重做 | 生成子代理 + 评委子代理循环 | 代码质量保障、文档审查 |
| 5 | Error-Recovery | 检测失败→诊断→修复→重试 | 错误检测子代理 + 修复子代理链 | 自动化修复流水线 |

### Orchestrator-Worker 八步建造法

1. **定义数据契约**：子代理输入=自包含子问题+上下文；输出=结构化对象（发现+置信度+来源）
2. **任务分解**：主代理将复杂问题拆分为独立子问题
3. **并行派发**：所有子代理同时启动，独立上下文
4. **紧凑交接**：子代理只返回结构化结果，不返回冗长推理
5. **合成阶段**：主代理评估每个子代理结果质量
6. **循环决策**：判断是否需要补充研究或重新派发
7. **引用纪律**：严格标注信息来源
8. **终止条件**：所有证据冲突已解决或达到最大迭代次数

### 从 Subagents → Agent Teams → Dynamic Workflows 升级决策矩阵

| 维度 | Subagents | Agent Teams | Dynamic Workflows |
|------|-----------|------------|-------------------|
| 子代理数量 | 1-10 | 3-10 | 100-1000+ |
| 人工监督 | 无需 | 关键节点介入 | 脚本审计 |
| 可重跑性 | 依赖对话 | 依赖上下文 | 脚本重跑 |
| 执行模式 | 回合制 | 回合制 | 后台非阻塞 |
| 编排者 | 主 Agent | 领导 Agent | JS 脚本 |
| 升级信号 | 子任务>10 或需协调 | 需人工介入 | 规模>50 或需审计 |

> 同步自：Anthropic官方课程390节全集 R85 | 2026-06-14


---

### R83 增量 (2026-06-15)

#### Claude Code多Agent编排实战：Workflows vs /goal 选择指南

**一句话核心区别**：Workflows解决"流程确定但需要多人协作"的问题，/goal解决"终点确定但路径不定"的问题。分界线是流程确定性，不是任务难度。

#### 何时用Dynamic Workflows

**适用信号**：
- 能提前画出流程图（PR审查、批量迁移、深度研究）
- 结果可被编译/测试/规则验证
- 需要多人（多Agent）并行协作
- 流程值得复用（存入~/.claude/workflows/或纳入版本控制）

**不适用信号**：
- 一个对话窗口能可靠完成的小任务（改一两个文件）
- 流程高度不确定且需要频繁人工拍板
- Token成本敏感的简单任务

**实操流程**：
1. 描述任务 → Claude生成JavaScript编排脚本
2. 脚本派发子Agent → 每个子Agent独立上下文+隔离worktree
3. 子Agent产出 → 对抗验证Agent核验
4. 汇聚结果 → 主Agent接收结构化摘要

**可重复工作流配合/loop使用**：
```
/loop "每小时运行一次" "用分类工作流处理支持队列"
/goal "所有bug已分类并标记优先级，npm test通过"
```

#### 何时用/goal

**适用信号**：
- 知道终点但不知路径（所有lint错误已修复、所有测试通过）
- 需要多次试错迭代
- 执行与评估需要分离（防止自我偏好偏差）

**条件编写三原则**：
1. 单一可衡量的最终状态：`eslint src/ --max-warnings 0`
2. 明确的验证方式：`npm test` 退出码为0
3. 关键约束条件：`仅修改 test/auth 目录下的文件`

**限制**：条件≤4000字符，单会话仅1个激活目标

#### 四步快速判断法

```
任务能拆成独立单元？
├── 不能 → 直接对话 或 /goal
└── 能 → 结果能被验证？
    ├── 不能 → /goal
    └── 能 → 需要逐步收敛？
        ├── 需要 → Workflows Loop 或 /goal
        └── 不需要 → 值得复用？
            ├── 值得 → Dynamic Workflows（脚本持久化）
            └── 不值得 → /goal（更轻量）
```

#### 三种协同组合

**组合一：Workflows + 内部/goal循环**
阶段1（Parallel）: 多个子Agent扫描问题 → 阶段2（Loop）: /goal循环修复直到达标 → 阶段3: 生成报告

**组合二：/goal触发Workflows**
设定大目标，让Claude自己决定在执行过程中调用哪个Workflow

**组合三：Auto mode处理审批**
在长任务中开启Auto mode减少人工审批频率（注意：Auto mode不启动新轮次，只自动审批工具调用）

#### 上下文管理实战心法

- CLAUDE.md ≤150行（太长反而抓不住重点）
- 上下文50%左右就该compact（别等满了再压缩）
- 不相关的工作流分开项目（避免上下文污染）
- 完成一个任务就立刻commit（别攒着）
- Workflows单次最多1000个Agent，跨会话不可恢复

#### Agent SDK编程实战

**子代理定义**：
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="用code-reviewer审查代码库",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="代码质量和安全审查专家",
                    prompt="分析代码质量并提供改进建议",
                    tools=["Read", "Glob", "Grep"],
                )
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)
```

**成本管理**：
- Agent SDK月度额度独立于交互使用限制（2026-06-15起）
- Pro=$20/月, Max 5x=$100/月, Max 20x=$200/月
- 高吞吐生产环境用API密钥按量付费
- 每个子Agent可设置token预算上限

