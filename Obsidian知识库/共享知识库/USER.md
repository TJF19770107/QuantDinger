# USER.md — 多Agent协作流程

> 来源：Anthropic官方课程提炼 · 2026-06-01
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
