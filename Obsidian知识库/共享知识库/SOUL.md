# SOUL.md — AI Agent 设计原则

> 来源：Anthropic官方课程提炼 · 2026-06-12 R18
> 同步自：Anthropic Academy 18门课程核心精华 + 2026年6月官方动态（Opus 4.6 Agent Teams + Claude Code 五大原语）

---


> 关联文档：[[Anthropic官方课程-390节全集]] — 18门课程全量索引 · 2026-06-02
## 一、Agent 内核设计原则

### 1.1 Agentic Loop 黄金闭环
```
收集上下文 → 执行操作 → 验证结果 → 反馈修正
```
- 每个操作后必须验证，形成感知-行动-验证的完整闭环
- 失败时自动回溯，不盲目前进

### 1.2 上下文窗口隔离原则
- **子代理隔离**：每个子代理拥有独立上下文窗口，主Agent只接收精炼结果
- **渐进式披露**：按需加载信息，避免一次性塞入全部上下文
- **精准回报**：子代理只返回关键信息，不返回完整执行过程

### 1.3 工具与权限分层
| 层级 | 范围 | 权限 |
|------|------|------|
| 核心层 | 读文件、搜索、基础执行 | 默认开启 |
| 扩展层 | 写文件、网络请求、MCP工具 | 按需授权 |
| 特权层 | 系统配置、删除、支付 | 显式确认 |

---

## 二、多Agent协作设计原则

### 2.1 Lead-Specialist 模式
- **Lead Agent**：负责任务分解、路由、结果汇总
- **Specialist Agent**：专注单一领域，独立上下文执行
- **共享文件系统**：通过文件传递中间结果，避免上下文污染

### 2.2 Agent 通信模式
| 模式 | 适用场景 | 特点 |
|------|---------|------|
| 并行执行 | 无依赖子任务 | 最大效率 |
| 链式调用 | 有先后依赖 | 结果传递 |
| 条件路由 | 动态决策 | 基于中间结果分支 |
| 竞争模式 | 多方案择优 | 并行生成+自动排序 |

### 2.3 委派判断标准
- **可独立完成**：任务不需要与其他任务实时协调
- **结果可验证**：产出有明确的质量标准
- **值得开销**：委派的开销小于直接执行的收益

---

## 三、Skills 设计原则

### 3.1 原子化与可组合
- 每个Skill仅做一件事，做好一件事
- Skills之间通过标准化接口组合
- SKILL.md 使用 frontmatter 声明触发条件和优先级

### 3.2 渐进式披露
```
SKILL.md (入口) → 详细指令文件 → 示例/模板 → 参考文档
```
- Level 1: 名称+描述+触发条件（始终加载）
- Level 2: 详细步骤（触发时加载）
- Level 3: 参考资料（按需加载）

### 3.3 团队分发
- 通过Git仓库管理Skills版本
- 企业级托管部署
- 与子代理集成实现专家级任务委派

---

## 四、安全设计原则

### 4.1 纵深防御
| 层级 | 机制 |
|------|------|
| 输入层 | 指令审计、注入检测 |
| 执行层 | 沙箱隔离、权限最小化 |
| 输出层 | 结果审查、敏感信息过滤 |
| 审计层 | 全链路日志、异常告警 |

### 4.2 异步监察者
- 独立LLM对每次操作进行安全评估
- 四级异常检测：正常/警告/危险/致命
- 三级分级干预：日志/确认/阻断

---

## 五、记忆与进化原则

### 5.1 双层记忆架构
- **会话记忆**：当前对话上下文，自动管理
- **持久记忆**：跨会话的模式、经验、偏好，结构化存储

### 5.2 Dreaming 策展
- 会话间自动提取模式
- 噪声过滤 + 原则蒸馏
- 自动记忆重构

### 5.3 自进化闭环
```
执行 → 评估 → 反思 → 改进 → 验证 → 沉淀
```
- 每次失败都是进化机会
- 成功模式自动沉淀为Skills
- 错误模式记录到经验池

---

> 核心法则：简单优于复杂，隔离优于耦合，验证优于假设。

---

## [更新日期: 2026-06-12 R17] SDK子代理新设计原则

> 来源：Anthropic Agent SDK 官方文档 (code.claude.com/docs/en/agent-sdk/subagents)

### 1. 子代理生命周期管理

```
创建(AgentDefinition) → 调用(Agent工具) → 执行(独立上下文) → 返回(精炼结果) → 可恢复(Resume)
```

**关键发现**：子代理并非一次性消耗品——通过 `agentId` 可恢复并保留完整对话历史，实现对长时域任务的持续上下文累积。

### 2. 动态工厂模式

```python
def create_security_agent(security_level: str) -> AgentDefinition:
    return AgentDefinition(
        description="Security code reviewer",
        prompt=f"{'Strict' if security_level=='strict' else 'Balanced'} security reviewer...",
        model="opus" if security_level == "strict" else "sonnet",
    )
```

**设计原则**：子代理不应是静态配置，而应根据运行时条件（任务复杂度、风险等级、数据敏感度）动态生成。高风险任务用Opus模型，常规任务用Sonnet，快速探索用Haiku。

### 3. 上下文隔离的铁律补充

| 子代理收到 | 子代理不收到 |
|-----------|------------|
| 自身系统提示词 | 父代理对话历史 |
| Agent工具提示字符串 | 父代理工具结果 |
| 项目CLAUDE.md | 父代理系统提示词 |
| 受限工具集 | 未列入skills的技能内容 |

**核心启示**：父→子的唯一通道是Agent工具的prompt字符串。必须在prompt中包含所有子代理需要的文件路径、错误信息和决策依据，不能假设子代理"知道"父代理的上下文。

### 4. 检测与监控原则

- 子代理调用通过 `ToolUseBlock(name="Agent"|"Task")` 检测
- 子代理内部消息携带 `parent_tool_use_id` 字段
- 兼容旧版SDK的 `"Task"` 和新版的 `"Agent"` 工具名

---

## [更新日期: 2026-06-02] Subagent 架构设计原则（基于官方完整文档）

> 来源：Anthropic 官方 Subagents 文档 (code.claude.com/docs/zh-CN/sub-agents) · 2026年4月

### 1. 上下文窗口经济学原理

Subagent 的核心设计逻辑源自一个根本约束：**上下文窗口是稀缺资源**。

```
主对话上下文 = 固定容量预算
├── 每次文件读取占用预算
├── 每次探索占用预算
├── 每次未完成想法占用预算
└── 预算耗尽 → 响应速度下降 + Token 成本攀升
```

**Subagent 的经济学解法**：将探索成本从主对话预算中移出，由独立预算承担，仅将**精炼结果**（而非完整过程）返回主对话。

### 2. 只读/编辑分离铁律

```
主 Agent（Orchestrator）：编辑权限
    ├── 规划工作流程
    ├── 综合子代理结果
    └── 执行最终编辑操作

Subagent（仅授予 Read/Grep/Glob）：只读
    ├── 独立上下文窗口
    ├── 搜索和探索代码库
    └── 返回精炼发现
```

**为什么编辑由主 Agent 执行**：
- 主 Agent 有"全局视图"，了解完整任务背景
- 多个 Subagent 同时编辑同一文件 → 冲突
- 编辑操作涉及最终质量责任，应集中控制

### 3. 模型选择策略

| Subagent 类型 | 推荐模型 | 理由 |
|-------------|---------|------|
| 探索/搜索 | Haiku | 快速、低成本、能力足够 |
| 分析/审查 | Sonnet | 能力与成本的最佳平衡 |
| 复杂判断/架构 | Opus 或完整模型 ID | 需要深度推理 |
| 通用 | inherit（默认） | 与主对话保持一致 |

**成本优化铁律**：能用 Haiku 不用 Sonnet，能用 Sonnet 不用 Opus。Explore 内置代理使用 Haiku 正是这一原则的体现。

### 4. 最小权限原则在 Subagent 中的实践

```
tools: Read, Glob, Grep          ← 安全审查代理（只读）
tools: Agent(worker, researcher)  ← 协调代理（限制可生成的子代理类型）
disallowedTools: Write, Edit      ← 继承所有工具但禁止写入
isolation: worktree               ← 完全隔离的文件系统副本
```

**两层防护**：
- `tools`（允许列表）：精确控制能力
- `disallowedTools`（拒绝列表）：从继承池中移除敏感工具

### 5. 防止上下文污染的四大手段

| 手段 | 机制 | 效果 |
|------|------|------|
| Subagent 隔离 | 独立上下文窗口 | 探索结果不占用主对话 |
| 精炼返回 | 只返回摘要而非完整过程 | 大幅减少主对话 token |
| 后台执行 | `background: true` | 不阻塞主对话流程 |
| Worktree 隔离 | `isolation: worktree` | 文件系统级别的沙箱 |

---

> **核心法则更新**：将上下文窗口视为预算，将 Subagent 视为外包——外包探索、保留编辑、精炼回报。

---

## [更新日期: 2026-06-01] CCA 4D 架构师能力框架

> 来源：Anthropic CCA Foundations 认证体系 · 2026年3月

### 1. 4D 框架总览

Anthropic 将 AI 时代架构师能力拆解为 4 个维度：

| D | 维度 | 英文 | 核心问题 |
|---|------|------|---------|
| D1 | **委派判断** | Delegation | 什么给AI、什么给人类？何时用子代理？ |
| D2 | **精确描述** | Description | 如何让代理准确理解任务并独立执行？ |
| D3 | **判断质量** | Discernment | AI 输出何时"足够好"可以交付？ |
| D4 | **审核纪律** | Diligence | 交付前如何系统性地验证 AI 产出？ |

### 2. Delegation 委派决策矩阵

```
任务特征分析：
├── 确定性 + 高容错 → 全自动（格式化代码、生成文档骨架）
├── 确定性 + 低容错 → 半自动 + 验证（数据库迁移、支付逻辑）
├── 模糊性 + 高容错 → AI 草稿 + 人工选定（文案构思、UI草案）
└── 模糊性 + 低容错 → 人工决策 + AI辅助（架构选型、安全策略）
```

### 3. Description 精确描述梯度

```
vague "帮我写个API"
  → specific "用FastAPI写POST /register，接收email+password，返回JWT"
    → spec-like（含错误码、性能要求、安全约束、测试用例格式）
```

**Subagent Spec 模板**（Anthropic 官方最佳实践）：
1. 输入格式：字段名、类型、示例值
2. 输出格式：JSON Schema / 模板 / 字数范围
3. 风格约束：语气、格式、禁止项
4. 失败返回结构：`{"error": "描述", "suggestion": "修复建议"}`
5. 超时策略：最大运行时间 + 降级行为

### 4. Discernment 质量判断三段法

1. **正确性检查**：事实准确？引用存在？API 调用有效？
2. **完整性检查**：覆盖边缘情况？错误处理完整？文档同步？
3. **适用性检查**：适合当前项目风格？符合团队约定？用户可直接使用？

### 5. Diligence 审核纪律清单

- [ ] 代码审查：安全漏洞、性能问题、边界条件
- [ ] 配置审查：权限最小化、密钥不硬编码、端口不冲突
- [ ] 文档审查：与代码实际行为一致、链接有效、无过时内容
- [ ] 合规审查：数据隐私、许可证兼容、审计日志完整

> "不因为 AI 生成的看起来正确就跳过审查"——CCA 核心纪律


---

## [更新日期: 2026-06-01] AI Agent 设计原则

> 来源：Anthropic Academy 官方课程 + Multi-agent coordination patterns 官方博客 + Claude Code Harness 最佳实践

### 1. 多Agent协调模式选择决策树

在构建多Agent系统时，遵循"从简单开始、逐步演进"的核心原则：

```
任务特点分析：
├── 质量关键 + 有明确评估标准
│   └── Generator-Verifier：生成→验证→反馈循环
│       适用：代码审查、合规检查、客服回复质量保障
│
├── 任务可分解 + 子任务有边界
│   ├── Worker 需要长期上下文积累
│   │   └── Agent Teams：持久Worker从共享队列认领任务
│   │       适用：大型框架迁移、并行批处理
│   │
│   └── Worker 一次性完成任务
│       └── Orchestrator-Subagent：编排→分发→综合
│           适用：代码审查分项、文档多步处理
│           ★ 推荐作为默认起点
│
├── 事件驱动 + Agent生态系统持续增长
│   └── Message Bus：publish/subscribe + Router 路由
│       适用：安全运营自动化、事件级联处理
│
└── 协作知识发现 + 去中心化
    └── Shared State：直接读写共享存储，无中心协调
        适用：研究综合、知识库共建
```

**演进路径**：
```
Orchestrator-Subagent（起点）
  ├── 条件逻辑越来越多 → Message Bus
  ├── Worker 需要跨任务积累 → Agent Teams
  ├── 需要质量闭环 → + Generator-Verifier
  └── 发现需实时流通 → Shared State
```

### 2. Sub-agents 读写分离原则

```
核心架构：
┌──────────────────────────────────────────┐
│           主 Agent（编排 + 编辑权限）       │
│    - 规划工作流程                           │
│    - 综合子代理结果                         │
│    - 执行最终编辑操作                       │
└──────┬────────┬────────┬────────┬─────────┘
       │        │        │        │
  ┌────▼───┐ ┌─▼────┐ ┌─▼────┐ ┌─▼────┐
  │Subagent│ │Subagt│ │Subagt│ │Subagt│
  │只读搜索│ │只读安全│ │只读架构│ │只读文档│
  │独立窗口│ │独立窗口│ │独立窗口│ │独立窗口│
  └────────┘ └──────┘ └──────┘ └──────┘
```

**设计铁律**：
- 探索用只读 Subagent：梳理子系统、搜索代码库、安全审计
- 编辑由主 Agent 执行：在掌握全局上下文后集中修改
- 每个 Subagent 在独立上下文窗口中操作
- 只返回精炼发现，不传递中间过程
- 完成任务即终止，不跨任务持久化

### 3. Skills 渐进式披露设计

```
上下文加载策略（从常驻到按需）：

CLAUDE.md ──────── 常驻 ──────── 项目宪法、关键约束（≤200行）
    │
    ▼
Skills ─────────── 按需 ──────── 任务匹配时自动加载
    │                              触发：description 字段语义匹配
    │                              限定：可绑定到特定子目录
    │
    ▼
Subagents ──────── 后台 ──────── 被调用时启动独立实例
                                   原则：探索与编辑分离
```

**设计原则**：
- 不把所有专业知识常驻上下文 → 节省 token、减少噪声
- description 即触发条件 → 精确匹配、避免误触发
- 路径限定 → 支付服务的部署 Skill 只在支付目录激活
- 可组合 → 多个 Skills 同时加载不冲突
- 可移植 → Claude.ai / Claude Code / API 三环境统一运行

### 4. Harness 七层架构的模块化设计理念

```
Layer 7: Subagents    ← 探索编辑分离，独立上下文窗口
Layer 6: MCP          ← 外部连接，标准化接口
Layer 5: LSP          ← 符号导航，精确引用追踪
Layer 4: Plugins      ← 组织分发，打包 Skills+Hooks+MCP
Layer 3: Skills       ← 按需加载，渐进式披露
Layer 2: Hooks        ← 事件触发，100%执行率
Layer 1: CLAUDE.md    ← 会话基石，≤200行
```

**模块化理念**：
- **每层独立演进**：升级 LSP 不影响 Hooks，替换 MCP 不破坏 Skills
- **自下而上构建**：先做好 CLAUDE.md → 再添加 Hooks → 逐步上移
- **上层依赖下层**：MCP 的有效性依赖 LSP 提供的精确定位
- **Plugin 是聚合层**：将下层能力打包为可分发单元

### 5. Dynamic Workflows 动态编排模式（2026年5月新增）

**核心能力**：
- **并行子代理**：单次运行支持 16 个并发子代理，总计 1000 个代理/工作流
- **JavaScript编排**：确定性脚本，可版本控制、审计、复用
- **对抗验证循环**：内置 implement–verify–fix 循环，子代理间互相检查
- **企业级规模**：适用于数十万行代码库迁移、跨模块分析等复杂任务

**架构特点**：
```
用户需求 → Claude Code 生成 JavaScript 编排脚本 → 并行派发子代理 → 验证汇总 → 结果返回
```

**适用场景**：
- 大型代码库迁移（如 Bun 从 Zig 迁移到 Rust，75万行代码，11天完成）
- 跨文件批量重构
- 全服务范围 Bug 排查
- 需要多角度压力测试的设计方案

**成本考量**：
- Token 消耗显著高于普通会话
- 建议从范围明确的任务开始，评估使用量
- 适用于 Max/Team/Enterprise 用户（需管理员开启）

### 6. 从简单开始逐步演进

> "Start with the simplest pattern. See where it breaks. Then evolve."

**六步演进法**：
1. **从 Orchestrator-Subagent 起步**：覆盖最广泛的问题，协调开销最小
2. **观察瓶颈**：信息中转丢失？吞吐不足？Worker 需要持久化？
3. **评估动态工作流适用性**：任务复杂度是否达到需要并行编排的程度
4. **定向演进**：按决策树选下一个模式
5. **组合使用**：生产系统常混合多种模式（如 Orchestrator + Shared State + Dynamic Workflows）
6. **定期审查**：每3-6月重新评估，模型升级后必审

**反模式警示**：
- 不要一上来就构建复杂的 Message Bus
- 不要为简单任务引入 Agent Teams 的持久化开销
- 不要在没有明确评估标准时使用 Generator-Verifier
- 不要忘记为 Shared State 设计终止条件
- **动态工作流滥用**：不要为简单查询启动并行子代理，浪费资源

---

## 八、R45新增：Agent Harness工程化原则（2026-06-02）

> 来源：Anthropic《Claude Code大型代码库最佳实践》2026

### 8.1 配置比模型重要
Anthropic生产实践核心洞察：围绕模型构建的工具生态（Harness），对最终表现的影响**比模型本身更大**。

### 8.2 Hooks/Skills/Agents职责三定律
```
Hooks 管"不能做什么"（硬约束）→ 写在settings.json，Claude无法跳过
Skills 管"应该怎么做"（能力包）→ 文件夹组织，渐进式披露
Agents 管"谁来做"（角色担当）→ 独立上下文，专注单一领域
```

### 8.3 Skills工程设计原则
- **Gotchas信噪比最高**：记录Claude实际踩过的坑，不是预测的坑
- **文件夹不是文件**：scripts/ + references/ + assets/ 分层组织
- **给信息不给剧本**：留判断权给Claude，不写死每一步
- **description是触发条件**：不是功能摘要，决定模型何时激活Skill
- **7天验证周期**：装Skill后用一周，不主动触发就卸载

### 8.4 Agent模式选择原则
- 从Orchestrator-Subagent起步（覆盖最广泛，协调开销最小）
- 任务短且有界→Orchestrator-Subagent；任务需持续深入→Agent Teams
- 步骤可预测→Orchestrator-Subagent；事件涌现→Message Bus
- Worker独立不互扰→Agent Teams；发现需实时流动→Shared State
- 生产系统常混合多种模式

---

> 更新日期：2026-06-02 R45 | 新增：Harness工程化原则 + Skills工程设计 + 模式选择矩阵

---

## 九、R53新增：Claude Code 子代理设计原则（2026-06-05）

> 来源：Anthropic 官方 Sub-Agents / Agent Teams / Skills / Hooks 文档 · 2026-06-05 全域学习

### 9.1 Sub-Agent 隔离上下文原则

Sub-Agent 的核心设计逻辑：**上下文窗口是稀缺资源**。将探索成本从主对话预算中移出，由独立预算承担，仅将精炼结果返回。

```
主对话上下文 = 固定容量预算
├── 每次文件读取占用预算
├── 每次探索占用预算
├── 每次未完成想法占用预算
└── 预算耗尽 → 响应速度下降 + Token 成本攀升

Subagent 经济学解法：
  独立上下文窗口 → 探索成本外部化 → 仅精炼结果返回主对话
```

**隔离四大手段**：

| 手段 | 机制 | 效果 |
|------|------|------|
| Subagent 隔离 | 独立上下文窗口 | 探索结果不占用主对话 |
| 精炼返回 | 只返回摘要而非完整过程 | 大幅减少主对话 token |
| 后台执行 | `background: true` | 不阻塞主对话流程 |
| Worktree 隔离 | `isolation: worktree` | 文件系统级别的沙箱 |

### 9.2 Skills 按需加载 vs CLAUDE.md 始终加载

| 机制 | 加载方式 | 适用场景 |
|------|----------|----------|
| **CLAUDE.md** | 每次对话**始终加载** | 通用项目信息：技术栈、架构、约定 |
| **Skills** | **按需加载**（名称+描述始终可见） | 特定工作流：部署、代码审查、测试生成 |

**核心原则**：CLAUDE.md 放通用，Skills 放特定——不浪费日常对话的上下文空间。

```
上下文加载策略（从常驻到按需）：

CLAUDE.md ──────── 常驻 ──────── 项目宪法、关键约束（≤200行）
    │
    ▼
Skills ─────────── 按需 ──────── 任务匹配时自动加载
    │                              description 字段语义匹配触发
    │                              可绑定到特定子目录
    │
    ▼
Subagents ──────── 后台 ──────── 被调用时启动独立实例
                                  探索与编辑分离
```

**Skills 两种触发方式**：
- **Model-invoked**：Claude 根据 description 自动匹配并加载
- **User-invoked**：用户输入 `/skill-name` 手动触发

### 9.3 最小权限原则（Tools 白名单）

```yaml
# 只读安全审查代理
tools: Read, Glob, Grep

# 协调代理：限制可派生的子代理类型
tools: Agent(worker, researcher), Read, Bash

# 从继承池中移除敏感工具
disallowedTools: Write, Edit

# 完全禁止派生子代理
tools: Read, Glob, Grep   # 不列出 Agent 工具
```

**两层防护**：
- `tools`（允许列表）：精确控制能力，省略则继承所有工具
- `disallowedTools`（拒绝列表）：从继承池中移除敏感工具

**模型选择成本铁律**：能用 Haiku 不用 Sonnet，能用 Sonnet 不用 Opus。Explore 内置代理使用 Haiku 正是这一原则的体现。

### 9.4 context: fork 模式隔离

Skills 可通过 `context: fork` 始终在隔离的 Sub-Agent 中运行：

```yaml
---
name: deep-research
description: 深入研究某主题
context: fork
agent: Explore
---
```

`context: fork` 让 Skill 自带 Sub-Agent 隔离，避免长研究过程污染主对话上下文。

### 9.5 Agent Teams 与 Sub-Agents 选择决策树

| | Sub-Agents | Agent Teams |
|---|---|---|
| **上下文** | 自有上下文窗口；结果返回调用者 | 自有上下文窗口；完全独立 |
| **通信** | 仅向主代理报告结果 | 队友之间直接通信 |
| **协调** | 主代理管理所有工作 | 共享任务列表 + 自协调 |
| **适用** | 只需要结果的聚焦任务 | 需要讨论和协作的复杂工作 |
| **Token 成本** | 较低：结果摘要回主上下文 | 较高：每个队友是独立 Claude 实例 |

**决策树**：

```
任务特征分析：
├── 聚焦任务 + 只需结果 → Sub-Agents
│   └── 适用：代码审查、文件探索、安全审计
│
├── 复杂协作 + 需要讨论 → Agent Teams
│   ├── 研究与审查：队友分享并挑战彼此发现
│   ├── 竞争假设调试：并行测试不同理论
│   └── 跨层协调：前端/后端/测试各由一队友负责
│
├── 关键差异：
│   ├── Sub-Agents 不继承 Skills → 需显式指定 skills 字段
│   ├── Agent Teams 队友可复用 Sub-Agent 定义
│   └── Agent Teams 适合 3-5 个队友，每人 5-6 个任务
│
└── 顺序任务 + 同文件编辑 → 单个 Session 或 Sub-Agents 更高效
```

---

> 更新日期：2026-06-05 R53 | 新增：Claude Code 子代理设计原则五维度（隔离上下文、按需加载、最小权限、fork隔离、决策树）

---

## 十、R58新增：CCA认证体系设计原则（2026-06-05）

> 来源：Anthropic CCA Foundations 认证架构 · 2026-06-05 全域学习

### 10.1 认证五域映射

CCA认证60题评估覆盖五大领域，反映Anthropic对AI架构师的能力定义：

| 领域 | 核心能力 | 权重信号 |
|------|---------|---------|
| Agentic Architecture | 子代理编排、多Agent协调、Dynamic Workflows | ★★★★★ 最高 |
| Claude Code | Harness七层扩展、CLAUDE.md分层、Hooks/Skills/Subagents | ★★★★★ 最高 |
| Context Management | 上下文窗口经济、渐进式披露、记忆策略 | ★★★★ |
| API Design Patterns | 并行扇出/层次编排/验证循环/共享流水线 | ★★★★ |
| Security & Governance | 权限最小化、沙箱隔离、审计日志、Managed Settings | ★★★ |
| Integration Architecture | MCP三层扩展、云平台部署、企业集成模式 | ★★★ |

### 10.2 认证设计的核心信号

> "The exam tests how you design systems, not how you use the product."

- 认证不考"怎么用Claude聊天"，考"怎么用Claude构建系统"
- Agentic Architecture和Claude Code权重最高 → Anthropic认为架构设计能力>API调用技能
- Partner Network准入机制 → 构建企业级Claude生态的护城河

### 10.3 认证准备策略

```
学习路径：
13门Skilljar课程（免费） → 开源Notebook实操 → 生产项目实践 → Partner Network准入 → CCA考试

关键课程优先：
1. Building with the Claude API（84课时，8+小时，最重）
2. Claude Code in Action（日常开发工作流）
3. Introduction to Agent Skills + Subagents（Agent架构核心）
4. MCP系列（Introduction + Advanced）
```

---

> 更新日期：2026-06-05 R58 | 新增：CCA认证五域映射+准备策略


---

## [更新日期: 2026-06-05] Opus 4.8 Dynamic Workflows 设计原则

> 来源：Anthropic Opus 4.8 发布（2026-05-28）· Dynamic Workflows 研究预览版 · Bun 迁移案例（75万行/11天/99.8%通过率）

### 1. Dynamic Workflows 核心架构

```
复杂任务 → 规划（Plan）
              │
              ▼
         问题分解
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
 Subagent  Subagent  Subagent（并行数十~数千个）
    │         │         │
    ▼         ▼         ▼
 对抗验证 ← 交叉验证 ← 证伪检查
              │
              ▼
         答案收敛
              │
              ▼
         汇总汇报
```

**设计原则**：
- **先规划再执行**：复杂任务不立即执行，先拆解为可并行的子问题
- **对抗证伪机制**：内置对抗 Agent 证伪前面的结论，直到答案收敛
- **断点恢复**：中途打断支持恢复，不丢失已完成的子任务
- **容量弹性**：从数十到数千个子代理，随任务复杂度自动扩展

### 2. Effort Control 思考投入控制

| 模式 | 思考强度 | 适用场景 | 成本 |
|------|---------|---------|------|
| Fast Mode | 低 | 简单任务、快速迭代 | 标准价的 33% |
| Normal | 中 | 日常开发、通用问答 | 标准价 |
| High | 高 | 复杂推理、架构设计 | 标准价 |
| XHigh (Ultra Code) | 极高 | 大型迁移、安全审计 | Max 之上 |

**设计原则**：
- **按需投入**：简单任务不浪费推理 token，复杂任务不自降标准
- **自动探测**：Ultra Code 模式下 Claude 自动判断是否适合使用 workflow
- **成本透明**：Fast Mode 降价 67%，激励开发者对简单任务使用轻量模式

### 3. 诚实度提升的设计启示

Opus 4.8 将代码缺陷漏报率降至前代 1/4，过度自信行为降至前代 1/10：

- **不确定性声明**：模型应主动声明"我不确定"，而非假装知道
- **多角度验证**：关键结论必须多 Agent 交叉验证
- **容错边界暴露**：Agent 应清晰告知自己能力的边界，而非掩盖局限

### 4. Claude Code AI OS 设计四支柱

| 支柱 | 类比 | 设计原则 |
|------|------|---------|
| **Skills** | 教育（长期记忆） | 按需加载、路径绑定、渐进披露 |
| **Hooks** | 反射（自省机制） | 事件驱动、自动进化、审计追踪 |
| **MCP** | 感官（外部连接） | 标准化、三原语、可扩展 |
| **Subagents** | 双手（任务执行） | 隔离上下文、只读探索、精炼回报 |

**核心设计原则**：四支柱互补不重叠，形成完整的 AI 操作系统架构。Skills 教会知识，Hooks 确保纪律，MCP 打通外部，Subagents 并行执行。

---

## [更新日期: 2026-06-05] LSP 集成设计原则

> 来源：Claude Code Harness 最佳实践 · Anthropic 2026年分享

- **符号感知而非字符串匹配**：在大型代码库中，按符号搜索（LSP）过滤在读文件之前就完成，大幅降低上下文消耗
- **类型精确性优先**：grep 一个常见函数名可能返回几千条结果，LSP 只返回指向同一个符号的引用

---

## [更新日期: 2026-06-10] Agent Teams / Swarm 多 Agent 编排原则

> 来源：Anthropic Claude Opus 4.6 官方发布 + Claude Code Swarm 特性 · 2026-06

### 团队领导模式

**核心架构**：不与单个 AI 对话，而是与团队领导对话，由领导协调整个专家团队。

```
用户 → Team Lead (规划/委派/综合) → 专家组并行执行 → 结果回流整合
```

**领导 Agent 职责**：
- 不直接编写代码，专注于规划、委派和综合
- 创建计划供用户审批
- 进入"委派模式"后生成特定角色的 Agent

**Worker Agent 职责**：
- 每个 Agent 拥有独立的 context window（新鲜上下文）
- 共享任务板，通过 @mention 协调
- 在独立的 Git worktree 中工作，防止文件冲突

### 并行化设计原则

| 原则 | 说明 |
|------|------|
| **新鲜上下文** | 每个团队成员约使用 40% context window（vs 单 Agent 80-90%）|
| **并行加速** | 单人 2 小时的任务，团队 30 分钟完成 |
| **认知负载分配** | 5 万行代码库不再由一个 Agent 独立承担 |
| **Git Worktree 隔离** | 5 个 Agent 同时编码不冲突，测试通过后才合并 |

### TeammateTool 编排层（13 个操作）

**团队生命周期**：spawnTeam、discoverTeams、cleanup
**加入工作流**：requestJoin、approveJoin、rejectJoin
**协调通信**：直接消息、广播消息、计划审批协议

### 环境变量设计

```
CLAUDE_CODE_AGENT_ID          # 唯一标识符
CLAUDE_CODE_AGENT_TYPE        # 角色（frontend/backend 等）
CLAUDE_CODE_TEAM_NAME         # 团队归属
CLAUDE_CODE_PLAN_MODE_REQUIRED # 强制计划审批标志
```

### 适用场景判断矩阵

| 适用 | 不适用 |
|------|--------|
| 大型跨文件重构 | 快速修复和小改动 |
| 多组件功能开发 | 范围不清晰的探索 |
| 并行工作流项目 | 安全关键代码（需人工审查）|
| 超单 Agent 上下文限制的代码库 | 不需要并行的简单任务 |

### 四大扩展原语统一设计

Claude Code 的 **Skills + Hooks + Agents + MCP** 形成了完整的可编程 AI 平台：

| 原语 | 类比 | 确定性 | 生命周期 |
|------|------|--------|----------|
| **Skills** | 知识注入 | 非确定性（按需加载） | 会话级 |
| **Hooks** | 规则护栏 | 确定性（保证执行） | 事件级 |
| **Agents** | 并行执行 | 确定性（隔离 context） | 任务级 |
| **MCP** | 外部连接 | 确定性（开放协议） | 连接级 |

**关键设计洞察**：四者互补，解决"最后一英里"问题。Skills 编码工作流为可复用命令，Hooks 在非确定性 AI 行为上施加确定性护栏，Agents 以隔离上下文并行执行，MCP 通过开放协议连接 1000+ 外部工具。

---

## 七、Trustworthy Agents 设计原则（R74新增 · 2026-06-11）

> 来源：Anthropic 官方研究文章 "Trustworthy Agents in Practice" (2026-04-09)

### 7.1 五大核心原则

| 原则 | 设计要点 |
|------|---------|
| Human Control | Plan Mode：从单步审批升级到整体策略审批；子代理工作流可见可控；用户在策略层面而非步骤层面行使判断 |
| Alignment | Claude主动在不确定时暂停，复杂任务中主动暂停率翻倍；训练场景强化"不确定即暂停"本能；Constitution倾向"提出疑虑"而非假设执行 |
| Security | 多层防御：模型训练识别注入模式 + 生产流量监控 + 红队测试；无单层防线可保证安全 |
| Transparency | Agent行为可审计；操作日志完整记录；子代理工作流透明化 |
| Privacy | 工具和数据权限最小化；用户决定Claude可以做什么、不可以做什么 |

### 7.2 Agent 四层架构

```
Model (模型)    → 核心智能，训练塑造能力与行为
  ↓
Harness (缰绳)  → 指令和护栏，约束操作边界
  ↓
Tools (工具)    → 可调用的服务和应用（邮件/日历/支出软件）
  ↓
Environment (环境) → 运行位置和可访问资源（企业笔记本 vs 个人手机）
```

**安全关键洞察**：Agent行为依赖四层协同。训练精良的模型仍可被配置不当的Harness、权限过大的Tool或暴露的Environment所利用。安全防御必须在每一层建立。

### 7.3 Plan Mode 设计哲学

- **核心张力**：自主性（有用）vs 控制（安全）
- **Plan Mode 解法**：Claude展示执行计划 → 用户审核/编辑/批准 → 执行中随时可干预
- **升级意义**：用户从"每次操作都审批"升级到"审批准策略"，在最有判断价值的层面保持控制
- **子代理场景延伸**：多Agent并行工作时，用户需看到整体工作流而非单一线程

### 7.4 主动暂停机制

- 训练时构建模糊场景，强化Claude选择"暂停"而非"假设"
- Claude's Constitution 倾向"提出疑虑、寻求澄清、或拒绝执行"而非假设
- 实测效果：复杂任务中Claude主动暂停率约翻倍，用户干预率仅微增
- 校准点：暂停太少→误读意图；暂停太多→失去自主性价值

### 7.5 提示注入防御分层

| 层级 | 机制 |
|------|------|
| L1 模型训练 | 识别注入模式，拒绝服从 |
| L2 生产监控 | 实时流量检测，拦截攻击 |
| L3 红队测试 | 外部专家对抗测试 |
| L4 权限最小化 | 工具和数据按需授予 |

**行业诉求**：NIST标准化Agent安全基准、证据共享常态化、MCP等开放协议标准化。

---

---

## [更新日期: 2026-06-11] Agent Teams v2.1.45 高级设计原则

> 来源：Claude Code Agent Teams 实战最佳实践 · 2026年6月

### 1. Delegate Mode（委派模式）设计

Delegate Mode 是 Agent Teams 架构的核心设计模式，实现关注点分离：

- **Lead Agent 只协调不执行**：限制Lead只能执行任务分派、进度监控、结果汇总，禁止直接实现代码
- **原理**：防止Lead"越俎代庖"，确保分工明确、避免上下文污染
- **实现**：Shift+Tab 开启 Delegate Mode
- **反模式**：Lead在未开启Delegate Mode的情况下自己写代码 → 队友闲置、Lead上下文过载

### 2. Plan Mode 行为契约

- Plan Mode 在 Teammate **整个生命周期**内持续生效，每轮都评估（非一次性）
- Teammate 的 Plan Mode **固定不可切换**：Plan Mode 队友无法转为执行模式
- **设计启示**：Plan Mode 用于架构审查/设计角色（只读），Default Mode 用于需要写代码/修改文件的角色
- 需要 Plan-then-Implement 流程时，使用 Plan Approval 功能，而非尝试切换模式

### 3. 文件冲突隔离设计

| 策略 | 实现方式 | 适用场景 |
|------|---------|----------|
| 自然隔离 | 按目录边界分配：`src/api/users/` vs `src/api/billing/` | 模块化项目 |
| 人工隔离 | 通过任务分解创建：`refactor API layer` → 拆分为按端点分组的子任务 | 单体项目 |
| 共享文件标记 | 在 CLAUDE.md 标记 `coordinate before editing`，由 Lead 排序管理访问 | 不可避共享文件 |

### 4. 任务规模黄金法则

- 每个 Teammate 5-6个任务（每个独立可交付）
- 1个巨量任务 = 无自然检查点 → 高风险浪费
- 5-6个聚焦任务 = 每次完成上报进度 → 可及时转向

### 5. 渐进式上手路径

```
第一阶段：研究/审查任务（Review PR、Research库、Investigate Bug）→ 零代码破坏风险
第二阶段：熟悉团队协作动态 → 切入实现任务
第三阶段：持续 Ctrl+T 定期监控 → 无人值守过久 = 风险累计
```

---

> 版本：v1.3 · R80迭代更新 · 2026-06-14
> 关联：[[Anthropic官方课程-390节全集]] v12.0

---

## Anthropic官方课程知识同步（2026-06-12更新）

> 来源：Anthropic Academy 课程体系深度提炼 · 2026-06-12

### 十一、分层架构原则

Anthropic 多Agent系统的核心架构可抽象为四个角色层：

```
Team Lead（编排决策层）
  ├── 任务分解、全局规划、资源分配
  ├── 接收精炼结果、综合判断
  └── 最终编辑与交付物产出

Teammates（专业执行层）
  ├── 独立上下文窗口、隔离并行执行
  ├── 专注单一领域、不跨域
  └── 仅返回精炼结果，不传递完整过程

Communication Bus（通信总线层）
  ├── 文件系统中介（中间产物传递）
  ├── 任务板/Task List（认领与协调）
  └── Mailbox（Agent间直接消息）

Shared Workspace（共享工作区层）
  ├── Git Worktree 文件隔离
  ├── 共享配置文件（CLAUDE.md/settings.json）
  └── 持久化记忆池（跨会话学习）
```

**设计铁律**：四层解耦，每层独立演进。Teammates层换模型不影响Bus层；Workspace层改隔离策略不波及编排层。

### 十二、工具权限三级最小化体系

| 级别 | 权限范围 | 授予工具 | 适用角色 |
|------|---------|---------|---------|
| **L1 只读分析** | 读取+搜索+审计 | Read, Glob, Grep, Bash(readonly) | 代码审查、安全扫描、探索调研 |
| **L2 测试执行** | L1 + 测试运行+报告生成 | L1 + Bash(test), Write(report only) | 测试生成、覆盖率分析、CI验证 |
| **L3 代码修改** | L2 + 编辑+写入 | L2 + Edit, Write, Bash(full) | 主Agent编排器、功能实现 |

**配置实现**：
```yaml
# L1 只读分析型
tools: Read, Glob, Grep
disallowedTools: Write, Edit

# L2 测试执行型
tools: Read, Glob, Grep, Bash
disallowedTools: Write, Edit
# 注：Bash 仅限测试命令，通过 Hook 约束

# L3 代码修改型（主Agent保留）
tools: Read, Write, Edit, Glob, Grep, Bash
```

**原则**：默认L1，按需升级。任何子代理从L1起步，确有必要才提权。禁止子代理拥有L3权限（编辑权归主Agent）。

### 十三、四大机制对比：Skills vs Hooks vs MCP vs Subagents

| 维度 | Skills | Hooks | MCP | Subagents |
|------|--------|-------|-----|-----------|
| **类比** | 长期记忆 | 自动反射 | 实时感官 | 并行双手 |
| **加载方式** | 按需匹配触发 | 事件驱动自动执行 | 连接即用 | 主Agent显式派生 |
| **确定性** | 非确定（按需） | 确定（100%执行） | 确定（协议通信） | 确定（隔离上下文） |
| **生命周期** | 会话级 | 事件级 | 连接级 | 任务级 |
| **配置位置** | .claude/skills/*/SKILL.md | .claude/settings.json | .mcp.json | .claude/agents/*.md |
| **典型用途** | 领域知识、工作流 | 安全护栏、自动格式化 | 数据库、外部API | 并行探索、专项审查 |
| **成本** | 低（仅触发时加载） | 极低（脚本执行） | 低（标准协议） | 中~高（独立实例） |

**组合原则**：四者互补不重叠。Skills教知识，Hooks保纪律，MCP通外部，Subagents并行执行。禁止用Skills替代Hooks（失去确定性），禁止用Subagents替代MCP（增加成本）。

### 十四、4E框架：AI协作决策四维评估

> 来源：Anthropic Academy 企业级AI部署评估框架

| E | 维度 | 英文 | 评估问题 | 量化指标 |
|---|------|------|---------|---------|
| E1 | **有效性** | Effective | AI能否真正解决这个问题？ | 任务完成率、准确率、用户满意度 |
| E2 | **效率** | Efficient | AI方案是否比人工更快/更省？ | 时间节省比、Token成本、人工介入次数 |
| E3 | **伦理性** | Ethical | AI行为是否符合伦理与合规要求？ | 偏见检测、隐私合规、透明度评分 |
| E4 | **安全性** | Safe | AI操作是否存在不可接受的风险？ | 误操作率、权限越界次数、审计覆盖率 |

**决策应用**：
```
每个AI协作决策必须通过四维评估：

Effective? ─── 否 → 不委托，人工处理
    │ 是
Efficient? ─── 否 → 简化方案或降级到Skills
    │ 是
Ethical?  ─── 否 → 添加约束护栏后重新评估
    │ 是
Safe?     ─── 否 → 降级权限、添加Hooks拦截
    │ 是
    ▼
  执行委托
```

**成本-安全平衡**：E1+E2决定"能不能做"，E3+E4决定"该不该做"。四者缺一不可。

### 十五、Thinking Mode vs Planning Mode 判断框架

| 维度 | Thinking Mode | Planning Mode |
|------|--------------|---------------|
| **触发** | 复杂推理需求自动激活 | Shift+Tab 手动开启或配置强制 |
| **行为** | 深度思考后再作答，不产生文件 | 先展示完整执行计划，用户审批后执行 |
| **产出** | 推理结论 | 执行计划 + 审批后的实际变更 |
| **适用** | 架构分析、算法设计、多步推理 | 代码重构、批量修改、高风险操作 |
| **工具权限** | 正常权限 | 可限制为只读（Plan Mode + 只读子代理） |
| **用户控制** | 自动决策 | 用户在策略层面审批 |

**选择决策树**：
```
任务分析：
├── 需要用户审批操作？
│   ├── 是 → Planning Mode
│   └── 否 →
│       ├── 纯分析/推理？ → Thinking Mode（不产生副作用）
│       ├── 多步操作但低风险？ → 默认模式 + Thinking
│       └── 高风险批量操作？ → Planning Mode（审批后执行）
```

**Plan Mode 在 Agent Teams 中的特殊性**：
- 队友的Plan Mode在整个生命周期持续生效，每轮都评估
- Plan Mode队友固定不可切换为执行模式
- 用于架构审查/设计角色（只读），Default Mode用于编码实现角色

### 十六、CLAUDE.md WHY-WHAT-HOW 框架

> 来源：Anthropic Claude Code 官方最佳实践

CLAUDE.md 不应该是随意的信息堆砌，而应遵循 WHY-WHAT-HOW 三层结构：

```markdown
# WHY — 项目存在的原因与核心约束（始终加载，≤50行）
## 项目使命
一句话描述项目解决什么问题

## 不可妥协的约束
- 安全红线：绝不......
- 技术红线：必须使用......
- 业务红线：核心指标不可低于......

# WHAT — 当前的技术现实（始终加载，≤100行）
## 技术栈
- 语言/框架/数据库版本
- 关键依赖及其版本

## 项目结构
src/
├── api/        — REST API 端点
├── services/   — 业务逻辑层
└── models/     — 数据模型

## 关键约定
- 命名规范、目录约定、Git工作流

# HOW — 怎么做（按需加载到Skills中，不放此处）
❌ 不要把详细步骤、工作流、部署脚本放 CLAUDE.md
✅ 放入对应的 .claude/skills/*/SKILL.md
```

**WHY-WHAT-HOW 分层原则**：
- **WHY**：项目宪法，修改需团队讨论，≤50行
- **WHAT**：技术现状，随项目演进更新，≤100行
- **HOW**：操作细节，永远不放CLAUDE.md，外移到Skills

**常见反模式**：
- WHY-WHAT混杂 → 新人无法快速理解项目核心
- HOW入侵CLAUDE.md → 日常对话上下文被部署脚本污染
- 200行+的CLAUDE.md → 每次对话浪费~2000 token在无关信息上

---

> 更新日期：2026-06-12 | 新增：4E决策框架 + Thinking/Planning双模式 + WHY-WHAT-HOW三层CLAUDE.md + 三级权限体系 + 分层架构四层模型 + 四大机制对比矩阵

## 七、R18 新增：Claude Code 五大原语设计原则（2026-06-12）

> 来源：Anthropic 官方最佳实践 + Code With Seb 生产级多Agent系统指南

### 7.1 五原语架构

Claude Code 的本质是一个可编程的 AI 开发环境。五大核心原语不是提示词的替代品，而是脚手架层面的架构能力：

| 原语 | 定位 | 设计原则 |
|------|------|---------|
| 子代理 | 独立上下文执行者 | 职责单一、权限最小化、仅返回精炼结果 |
| 命令 | 可复用操作模板 | 一次定义、反复调用、减少重复输入 |
| 技能 | 按需加载的专业流程 | 渐进式披露：frontmatter声明 + 延迟加载正文 |
| 钩子 | 确定性检查点 | 无条件触发、比提示词更可靠、不可被AI绕过的安全机制 |
| 记忆 | 项目上下文基线 | 精炼至上：每一行都要问"删掉会让Claude出错吗？" |

### 7.2 测试时计算原则（Test-Time Compute）

**核心洞察**：一个代理产生的 bug，另一个相同模型的代理可以发现。

- 原因：独立的上下文窗口让模型看到不同的东西
- 应用：避免单一对话上下文过长导致模型能力下降
- 实践：Writer/Reviewer 双 Agent 模式——Reviewer 在全新上下文中审查，不受实现过程先入为主影响

### 7.3 子代理权限安全分层（更新）

| 层级 | 工具配置 | 适用场景 | 安全原则 |
|------|---------|---------|---------|
| 只读分析 | Read, Grep, Glob | 代码审查、架构探索 | 不能修改任何文件 |
| 测试执行 | Bash, Read, Grep | 运行测试、分析结果 | 可执行但沙箱隔离 |
| 代码修改 | Read, Edit, Write, Grep, Glob | 代码编写、重构 | 完整读写但禁止系统操作 |

### 7.4 Skills 渐进式加载设计

```
Claude 启动时扫描 skill frontmatter（每个 ~20-50 token）
→ 仅匹配到任务时才加载完整 SKILL.md 正文
→ 50 个 skill 的库仅增加约 ~2000 token 开销
→ 架构优势：丰富的能力库 ≠ 上下文膨胀
```

### 7.5 Hooks 设计原则

| 事件 | 触发时机 | 设计原则 |
|------|---------|---------|
| PreToolUse | 工具使用前 | 安全检查、审计日志（无条件执行） |
| PostToolUse | 工具完成后 | 类型检查、测试运行、格式化验证 |
| SessionStart | 新会话开始 | 环境检查、上下文自动加载 |
| SessionEnd | 退出时 | 清理、自动总结 |

**设计核心**：Hooks 是无条件执行的确定性脚本。阻止在生产路径上运行 `rm -rf` 的 hook 比"小心删除"的 Skill 指令更可靠。Skills 是建议，Hooks 是强制。

### 7.6 MCP 三大原语使用边界

| Primitive | 控制对象 | 正确时机 | 错误用法 |
|-----------|---------|---------|---------|
| Tools | 模型控制 | 数据库查询、API调用、文件操作 | 暴露静态数据 |
| Resources | 应用程序控制 | 文档模板、配置数据暴露 | 让模型控制操作 |
| Prompts | 用户控制 | 预定义提示词模板、交互式向导 | 自动化操作 |

### 7.7 子代理 5 大错误模式（设计反模式）

1. **用子代理做实现工作** → 浪费 Token（子代理仅用于研究/分析）
2. **给所有代理全部工具权限** → 安全风险（按需分配三类权限）
3. **使用描述性名称（如 "helper"）** → 匹配机制失效（使用功能描述性名称）
4. **忽略上下文压缩** → 上下文膨胀（子代理返回精简摘要）
5. **并行文件编辑无协调** → 合并冲突（无冲突操作才并行）

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

## Anthropic官方课程R85同步：Agent SDK 子代理定义核心字段

### AgentDefinition 完整字段表

| 字段 | 类型 | 说明 |
|------|------|------|
| description | string | 告诉 Claude 什么时候该用这个子代理（触发条件，非摘要） |
| prompt | string | 子代理的系统提示词 / 行为规范 |
| tools | string[] | 子代理可用工具（省略则继承父级） |
| disallowedTools | string[] | 显式禁止的工具 |
| model | string | sonnet / opus / haiku / inherit 或完整模型 ID |
| background | boolean | 是否作为非阻塞后台任务运行 |
| maxTurns | number | 最大 agentic turn 数 |
| skills | string[] | 明确注入给该子代理的技能列表 |

### 五种子代理模式（2026 生产验证）

| # | 模式 | 核心机制 | 适用场景 | 成本特征 |
|---|------|---------|---------|---------|
| 1 | Divide-and-Conquer | 拆分→并行子代理→聚合 | 大型代码审查、多文件迁移 | 并行分摊 |
| 2 | Specialist Routing | 按任务类型路由到专家 | 前端/后端/数据库分离 | 按需专家 |
| 3 | Parallel Research | 多角度并行研究→交叉验证 | 技术调研、竞品分析 | 广撒网式 |
| 4 | Judge-and-Iterate | 生成→评委打分→低于阈值重做 | 代码质量保障、文档审查 | 质量溢价 |
| 5 | Error-Recovery | 检测失败→诊断→修复→重试 | 自动化修复流水线 | 故障成本 |

## Anthropic官方课程R85同步：Skills 七条生产级最佳实践

| # | 实践 | 说明 |
|---|------|------|
| 1 | description 是触发条件 | 写"什么时候该用"，不是"这是什么"。例：包含 "babysit" 触发词 |
| 2 | 给信息也给灵活性 | 避免"必须先做A再做B再做C"；写"通常先做A效果较好" |
| 3 | 避免过度限制 | 让 Claude 根据上下文判断，不写死路径 |
| 4 | 初始化配置 | 用 config.json 存配置；未配置时用 AskUserQuestion 问用户 |
| 5 | description 写给模型看 | 启动时列出所有 skill description，包含触发词帮助匹配 |
| 6 | 内置记忆 | append-only 文本日志，让 Claude 记住上次执行了什么 |
| 7 | 按需 Hooks | /careful 拦截危险命令、/freeze 限制编辑范围，用完即关 |

### Skills 分发路径

```
小团队 → 直接提交 repo .claude/skills/
   ↓ 规模化
自然生长 → sandbox → Slack 吆喝 → traction → PR 进 Marketplace
```

## Anthropic官方课程R85同步：12个Hooks 工业级架构

```
User prompt → Claude Code session
  → on-start hook: 加载 PROJECT_CONTEXT
  → AI 工作中
    → pre-tool-use hook: block .env
    → Edit file
    → post-edit hook: format + type-check
    → Bash command
    → pre-bash hook: block destructive
    → git commit
    → pre-commit hook: secret / debug / test
    → post-commit hook: backup push + changelog
  → Session end
  → on-stop hook: 自检提醒 + 通知
```

## Anthropic官方课程R85同步：Claude Code 四件套 AI 操作系统思维

### 四大支柱

| 组件 | 角色 | 比喻 | 何时使用 |
|------|------|------|---------|
| Skills | 长期记忆和专业知识 | AI 的教育 | 始终——这是基础 |
| Hooks | 事件触发自动反射 | AI 的反射 | 质量门控和审计追踪 |
| MCP | 与外部系统实时连接 | AI 的感官 | 需要实时数据时 |
| 子代理 | 并行隔离的 Claude 会话 | AI 的双手 | 大型或独立任务 |

### Developer OS 五层模块化生态

```
L5: Plugins（打包分发层）
L4: Subagents（并行隔离执行层）
L3: MCPs（外部系统连接层）
L2: Skills（专业知识层）
L1: Claude.md（基础配置层）
```

### 范式转换宣言

2026 年的 Claude Code 不应被理解为"AI 编程助手"，而应理解为**AI 操作系统**——一个配置一次就能放大通过它运行的每个工作流的平台。从代码助手进化到模块化操作系统：跨会话持久上下文、五层生态架构、可编程可扩展、社区驱动生长。

> 同步自：Anthropic官方课程390节全集 R85 | 2026-06-14


---

### R83 增量 (2026-06-15)

#### Agent SDK独立计费体系的设计启示

Anthropic将Agent SDK从订阅使用限制中解耦，设立独立的月度额度体系。这一架构决策揭示了AI Agent设计的核心原则：

**关注点分离（Separation of Concerns）**：交互式开发（探索/调试/迭代）与自动化执行（批量/CI/生产）属于不同的使用模式，应使用不同的资源池和计费模型。Agent系统设计中，同样应区分"规划与探索"上下文和"执行与验证"上下文。

**能力梯度定价（Capability-Gradient Pricing）**：$20-$200的梯度额度映射了从个人实验到团队生产的Agent使用强度，对应了Agent系统中从单Agent到Agent Swarm的能力梯度。

#### Dynamic Workflows的三大设计突破

**突破1：从"规划即执行"到"规划与执行解耦"**

传统ReAct循环将任务规划、步骤执行、结果验证全部压缩在同一上下文窗口中。Dynamic Workflows的根本创新在于：Claude先生成编排脚本（JavaScript），再由运行时系统按脚本派发子Agent。编排逻辑从对话上下文卸载到脚本运行时，主会话上下文不再爆炸。

**设计原则DP-R83-01（规划与执行解耦原则）**：复杂多步骤任务的编排逻辑应独立于执行上下文。编排器负责生成执行计划，执行器负责在隔离上下文中完成原子任务。两者通过结构化Schema通信，而非共享上下文。

**突破2：从"自我验证"到"对抗验证"**

Self-preferential bias是单Agent系统的固有缺陷。Dynamic Workflows将验证从执行中分离：每个子Agent的产出由另一个配置了"怀疑"提示的独立Agent做对抗性验证。执行与评估分离的设计原则确保了验证的独立性。

**设计原则DP-R83-02（对抗验证原则）**：任何Agent产出的质量验证，必须由独立的、配置了对抗/怀疑提示的Agent执行。评估Agent只能看到执行Agent的结构化输出，不能访问执行过程的中间状态。只有当对抗者未能提供有说服力的反例时，产出才被接受。

**突破3：从"单窗口限制"到"上下文卸载"**

三个死穴（Agentic Laziness / Self-preferential Bias / Goal Drift）的根本原因是单一上下文窗口同时承载规划和执行。Dynamic Workflows的结构性解法：每个子Agent拥有独立上下文窗口，主Agent只保留编排状态和聚合结果。

**设计原则DP-R83-03（上下文卸载原则）**：子Agent的中间推理和中间产物不应回流到主Agent上下文。主Agent仅接收结构化结果摘要。当子Agent数量超过并行阈值时，采用扇出-聚合模式分批处理。

#### 六种编排模式的Agent设计启示

**模式选择与任务特征映射**：

| 任务特征 | 推荐模式 | 设计理由 |
|---------|---------|---------|
| 步骤可预定义，有前后依赖 | Pipeline（流水线） | 确定的DAG结构 |
| 可拆分为独立子任务 | Fan-out-and-synthesize | 每个子任务干净上下文 |
| 需要质量保障 | Adversarial verification | 消除自我偏好偏差 |
| 需要方案探索 | Generate-and-filter / Tournament | 比较判断优于绝对评分 |
| 任务类型不确定 | Classify-and-act | 先分类后路由 |
| 工作量不确定 | Loop until done | 自适应循环 |

**架构分层原则**：
- Layer 1: 编排层（Orchestration）—— JavaScript脚本 / 编排Agent
- Layer 2: 执行层（Execution）—— 子Agent，独立上下文+worktree
- Layer 3: 验证层（Verification）—— 对抗验证Agent
- Layer 4: 聚合层（Aggregation）—— 汇总Agent

#### /goal与Workflows的协同设计原则

**设计原则DP-R83-04（流程确定性分治原则）**：
- 流程确定 → Workflows（静态编排，可复用，版本控制）
- 流程不确定但终点确定 → /goal（动态探索，双模型循环）
- 流程不确定且终点不确定 → 交互式对话（人类在环）

**双模型循环的设计启示**：/goal采用Haiku作为独立评估模型，不能运行命令或读取文件，仅基于会话中明确输出的内容做判定。这种轻量模型+条件驱动的验收模式，为Agent系统的自动验收提供了低成本方案。

