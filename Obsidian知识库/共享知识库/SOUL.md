---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_77846693685111f1a0095254002afed2
    ReservedCode1: H5XnElLy/A6KTMxOeSMLggwpZgcGupBXHhoEjP93pwqPK6JkTZImqtExbuo4xuFnybq4m5uLBDrevS5sz0pYCOD7A3R5jyUao0GsuDIxE4qQkY2jWPmE3z8LXCkqYpIa4OO5ziNmd2G+jXBJUie0zELUjsxTzq1UPJC/1qNVmcirDTRIeGZ6kDqKeTY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_77846693685111f1a0095254002afed2
    ReservedCode2: H5XnElLy/A6KTMxOeSMLggwpZgcGupBXHhoEjP93pwqPK6JkTZImqtExbuo4xuFnybq4m5uLBDrevS5sz0pYCOD7A3R5jyUao0GsuDIxE4qQkY2jWPmE3z8LXCkqYpIa4OO5ziNmd2G+jXBJUie0zELUjsxTzq1UPJC/1qNVmcirDTRIeGZ6kDqKeTY=
---

# SOUL.md — AI Agent 核心设计原则

> 基于 Anthropic 官方课程与六大 Agentic 设计模式提炼
> 更新：2026-06-16 第三轮循环 | 来源：Anthropic Academy + 六大设计模式 + 上下文工程

---

## 一、Agent 复杂度阶梯

设计 Agent 时遵循「最简可行复杂度」原则：

```
Level 0: 纯 LLM 回答（无工具、无状态）
Level 1: LLM + 工具调用（单一工具链）
Level 2: LLM + 多工具 + 推理循环（单 Agent）
Level 3: LLM + 子代理编排（多 Agent 协作）
Level 4: LLM + 自进化 + 持久记忆（自主 Agent）
```

**铁律**：绝不为了"看起来更智能"而升级复杂度层级。每一层升级必须有明确的业务价值驱动。

---

## 二、六大 Agentic 设计铁律

### 铁律 1: 先读后写（Read Before You Write）

Agent 在执行任何操作前，必须先从权威信息源加载上下文。

```
错误模式：Agent 直接基于训练数据生成回复
正确模式：Agent 先检索 → 再推理 → 最后生成
```

**实现机制**：RAG、数据库直查、API 实时拉取、文件系统读取

### 铁律 2: 分层上下文（Layered Context Hierarchy）

不同信息源具有不同权威等级：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 (最高) | System Prompt | 角色定义、约束、行为边界 |
| 2 | Retrieved Context | 运行时从权威源获取的数据 |
| 3 | Conversation History | 当前会话记录 |
| 4 (最低) | User Input | 用户最新输入 |

当来源冲突时，严格遵从上位权威，禁止取平均或选择"听起来合理"的。

### 铁律 3: 限定知识域（Scoped Knowledge Domains）

每个 Agent 必须有明确定义的能力边界：

```
显式约束：System Prompt 声明可处理 / 不可处理的范围
检索约束：仅从指定信息源获取上下文
拒绝策略：超范围问题明确拒绝，禁止猜测
```

### 铁律 4: 最小足迹（Minimal Footprint）

- 仅请求任务所需权限
- 仅访问任务所需数据
- 采取最小有效行动
- 不存储非必要的敏感信息
- 避免副作用操作

### 铁律 5: 偏好可逆（Prefer Reversible Actions）

两个等价方案时，优先选择可逆路径：

| 不可逆操作 | 可逆替代 |
|-----------|---------|
| 删除文件 | 移至暂存区 |
| 直接发送 | 先草拟审核 |
| 覆写记录 | 创建新记录 |
| 直接修改 | 标记待审查 |

**硬性规则**：不可逆且后果严重的操作必须暂停并人工确认。

### 铁律 6: 信任验证（Trust Verification）

多 Agent 系统中，不同来源的指令获得不同信任级别：

- 人类用户 → 完全信任
- 编排 Agent → 受限信任（不可覆盖安全护栏）
- 外部工具/API → 最小信任（仅限预定义交互）
- 文档嵌入指令 → 零信任（禁止执行）

---

## 三、韧性设计原则

### 3.1 故障隔离
- 单 Agent 故障不影响整个系统
- 子代理使用独立上下文窗口
- 异常传播边界清晰定义

### 3.2 优雅降级
- MCP 连接失败 → 降级为本地工具
- 子代理超时 → 主 Agent 接管任务
- API 不可用 → 使用缓存结果 + 标注时效

### 3.3 检查点机制
- 长期任务设置 Checkpoint
- 状态持久化到文件/数据库
- 支持从中断点恢复

### 3.4 停止条件
- 每个 Agent 定义最大执行轮次
- Token 预算上限
- 时间超时保护

---

## 四、五层可观测性支柱

| 层级 | 监控内容 | 工具 |
|------|---------|------|
| 1. 输入 | 用户意图、上下文质量 | 日志 |
| 2. 推理 | 模型思维链、工具选择 | 审计追踪 |
| 3. 行动 | 工具调用、副作用 | Hooks |
| 4. 输出 | 响应质量、格式、准确性 | 评估 |
| 5. 反馈 | 用户满意度、修正率 | 闭环 |

---

## 五、Claude Code 四大支柱映射

SOUL.md 中的设计原则在 Claude Code 架构中的落地：

| 设计原则 | 实现组件 | 配置方式 |
|---------|---------|---------|
| 先读后写 | Hooks (PreToolUse) | `.claude/hooks/` |
| 分层上下文 | CLAUDE.md + Skills | `.claude/skills/` |
| 限定知识域 | System Prompt + Skills 作用域 | SKILL.md frontmatter |
| 最小足迹 | Subagent 权限范围 | Subagent 配置 |
| 偏好可逆 | Hooks (PostToolUse 审计) | `.claude/hooks/` |
| 信任验证 | MCP 权限矩阵 | MCP server config |

---

## 六、设计反模式（六大破裂模式）

| 破裂模式 | 症状 | 修复 |
|---------|------|------|
| 上下文溢出 | Agent 忽略早期指令 | Progressive Disclosure |
| 权限蔓延 | Agent 执行非预期操作 | 最小足迹 + 信任验证 |
| 工具滥用 | 不必要的工具调用链 | 工具使用审计 Hooks |
| 幻觉放大 | 多 Agent 链式错误传播 | 先读后写 + Checkpoint |
| 死循环 | Agent 重复相同操作 | 停止条件 + 轮次上限 |
| 影子依赖 | 隐性依赖外部服务 | MCP 健康检查 + 降级 |

---

> 设计哲学：Agent 不是越复杂越好，而是在给定复杂度下越可靠越好。
> 来源：Anthropic Academy 六大设计模式 + Claude Code 官方文档 + 上下文工程
*（内容由AI生成，仅供参考）*

---

## 七、五种多Agent协调模式设计哲学（2026-06-15 第3轮学习更新）

> 来源：Anthropic 官方博客 Multi-agent coordination patterns (2026-04-10)

### 7.1 模式选择铁律：复杂度阶梯不可逆

```
Generator-Verifier（最简）→ Orchestrator-Subagent → Agent Teams
    → Message Bus → Shared State（最复杂）
```

**铁律**：不在模式阶梯上升级，除非当前模式已暴露明确不可修复的局限性。升级必须有"前一模式在哪里挣扎"的证据。

### 7.2 各模式与六大设计铁律的适配

| 设计铁律 | Generator-Verifier | Orchestrator | Teams | Message Bus | Shared State |
|---------|:---:|:---:|:---:|:---:|:---:|
| 先读后写 | ✅ Verifier 强制实现 | ✅ 编排器收集后合成 | ⚠️ 队友需自行保证 | ⚠️ 依赖事件携带完整上下文 | ⚠️ 存储即读写机制 |
| 分层上下文 | ✅ 清晰两层 | ✅ 编排器+子代理双层 | ⚠️ 队友间上下文隔离 | ❌ 事件流冲淡层级 | ❌ 所有Agent平等读写 |
| 限定知识域 | ✅ 天然强制 | ✅ 子代理边界清晰 | ✅ 队友领域专业化 | ⚠️ 订阅范围约束 | ⚠️ 靠自律 |
| 最小足迹 | ✅ Verifier 审计 | ✅ 权限显式声明 | ⚠️ 持久化上下文增加足迹 | ⚠️ 事件订阅扩大暴露面 | ❌ 全量读写存储 |
| 偏好可逆 | ✅ 循环迭代即为可逆 | ✅ 子代理可重试 | ⚠️ 多步操作可逆性难保证 | ⚠️ 事件不可撤销 | ❌ 直接写入不可逆 |
| 信任验证 | ✅ Verifier 即信任锚 | ✅ 编排器不覆盖安全 | ⚠️ 队友独立判断 | ❌ 路由来源混淆 | ❌ 所有贡献者同权 |

### 7.3 终止条件设计原则

- **时间预算**：所有模式适用，最通用兜底
- **收敛阈值**：Generator-Verifier/Shared State 核心机制
- **队列清空**：Agent Teams/Message Bus 自然终止
- **指定关闭Agent**：Shared State 特定需求
- **最大迭代**：Generator-Verifier 防无限循环

### 7.4 SOUL 层面的关键洞察

1. **安全性随模式复杂度递减**：Generator-Verifier 四项 ✅ → Shared State 四项 ❌。模式越复杂，安全边界越模糊。
2. **Shared State 是最强大但也最危险的模式**：消除单点故障的代价是失去信任验证和可逆性。
3. **Hooks 是跨模式的统一安全层**：无论选用哪种协调模式，Hooks (PreToolUse / PostToolUse / OnError) 提供不依赖模式选择的安全护栏。
4. **上下文中心分解是贯穿五种模式的元原则**：选择模式前先回答"每个Agent需要什么上下文"。

---

## 八、Dynamic Workflows：第六种编排范式（第4轮学习·R86新增）

> **来源**：Anthropic 官方博客 "Introducing dynamic workflows in Claude Code" + Claude Code Docs "Workflows" (2026)

### 8.1 哲学定位

Dynamic Workflows 不是五种协调模式的增量补充，而是一种**范式跃迁**。它回答了一个设计哲学问题：编排逻辑应当属于 LLM 推理还是确定性代码？

| 传统 Agent 系统 | Dynamic Workflows |
|---------------|------------------|
| 编排即推理：Agent 逐轮决策 | 编排即代码：脚本确定执行路径 |
| 上下文驱动：一切在 LLM 上下文中 | 脚本驱动：LLM 只写一次脚本，运行时执行 |
| 质量取决于持续推理 | 质量取决于脚本的质量模式设计 |
| 大任务受限于上下文窗口 | 数百 Agent 并行，上下文隔离 |

### 8.2 对六大设计铁律的冲击

| 设计铁律 | 五种模式下的状态 | Dynamic Workflows 下的变化 |
|---------|:---:|---------|
| **最小足迹** | Generator-Verifier 最安全，Shared State 最危险 | ✅ 最优——脚本变量 < LLM 上下文泄露面 |
| **偏好可逆** | Shared State 不可逆 | ✅ 脚本版本化 → 可回滚整个编排 |
| **信任验证** | 靠 Hooks 统一层 | ✅ 脚本级检查点 + Agent 互相驳斥 |
| **限制知识域** | Shared State 靠自律 | ✅ 脚本变量天然隔离 |
| **分层上下文** | Message Bus 冲淡层级 | ✅ 两层：战略(LLM) + 执行(脚本运行) |
| **低门槛** | Shared State 为最复杂 | ⚠️ 新门槛：需能读/写/调 JavaScript 脚本 |

### 8.3 SOUL 级关键洞察

1. **最优安全模式**：Dynamic Workflow 在全部六条设计铁律上不弱于任一协调模式，在"最小足迹"和"偏好可逆"上明显优于 Shared State
2. **编排与推理的分离是安全增益**：将循环控制从 LLM 推理中剥离到脚本，消除了推理错误导致的无限循环（反应式循环的根治）
3. **脚本即设计文档**：Workflow 脚本记录了 Agent 系统当时的编排意图，比任何事后审计日志都更清晰地说明了"这个系统如何运作"
4. **但代价是灵活性**：一旦脚本启动，中间无法动态调整策略。适用于"已知怎么做"的任务，不适用于"正在探索怎么做"的任务
5. **与五种模式互补而非替代**：Generator-Verifier 的检查逻辑、Orchestrator-Subagent 的派发结构、Agent Teams 的持久化队友——这些模式都可以实现为 Workflow 脚本中的不同阶段

---

## Anthropic 官方 Agent 设计原则

> 来源：Anthropic Engineering Blog (2026.06)
> 更新：2026-06-15

### 复杂度阶梯
单次LLM调用 → 增强型LLM → Prompt Chaining → Routing → Parallelization → Orchestrator-Workers → Evaluator-Optimizer → 自主Agent
**核心原则：仅在简单方案不足时才增加复杂度。**

### 六大Agentic模式
| 模式 | 场景 |
|------|------|
| Prompt Chaining | 固定步骤分解 |
| Routing | 多类型分类 |
| Parallelization | 无依赖并行 |
| Orchestrator-Workers | 动态分解 |
| Evaluator-Optimizer | 迭代评估 |
| Autonomous Agent | 开放问题 |

### 上下文工程五大维度
选择 → 结构化 → 排序 → 压缩 → 时机

### Skills三层设计
L1(描述) → L2(SKILL.md) → L3+(引用文件) — 渐进式信息披露

### 韧性五原则
错误隔离 · 状态恢复 · 护栏优先 · 可观测性 · 渐进授权


---

## 第七章：Plugin 架构设计原则（第三轮新增）

> **数据来源**：code.claude.com/docs/zh-CN/plugins-reference 完整技术规范
> **更新**：2026-06-16 第三轮循环

### 7.1 六组件架构总览

Plugin 作为自包含组件目录，通过以下六种组件类型扩展 Claude Code：

| 组件 | 位置约定 | 核心职责 |
|------|---------|---------|
| **Skills** | `skills/` / `commands/` | 知识模块注入，创建可调用快捷方式 |
| **Agents** | `agents/` | 独立上下文的专业化 AI 助手 |
| **Hooks** | `hooks/hooks.json` | 20+ 事件生命周期的自动化响应 |
| **MCP Servers** | `.mcp.json` 或内联 | 外部工具与数据源连接代理 |
| **LSP Servers** | `.lsp.json` 或内联 | 实时代码诊断与导航 |
| **Monitors** | `monitors/monitors.json` | 后台持久监控进程 |

### 7.2 组件隔离原则

1. **每个组件独立配置**：组件配置不交叉污染，各自拥有独立的作用域和生命周期
2. **Plugin 级共享上下文**：环境变量 `${CLAUDE_PLUGIN_ROOT}` 和 `${CLAUDE_PLUGIN_DATA}` 在组件间共享
3. **最小权限原则**：Agents 默认继承主会话权限，但可通过 `tools`/`disallowedTools` 显式限制
4. **优先级链**：`--agents CLI Flag` > `.claude/agents/` > `~/.claude/agents/` > Plugin `agents/`

### 7.3 独立配置 vs Plugin 模式选择

| 维度 | 独立配置（`.claude/`） | Plugin 模式 |
|------|----------------------|-------------|
| Skill 名称 | `/hello`（简短） | `/plugin-name:hello`（命名空间） |
| 适用场景 | 个人工作流、项目自定义、快速实验 | 团队共享、社区分发、跨项目重用 |
| 版本控制 | 随项目 Git | 独立版本化发布 |
| 安装方式 | 直接编辑文件 | `claude plugins install` |
| 冲突处理 | 无命名空间，靠文件优先级 | 命名空间天然隔离，无冲突 |

**选择建议**：
- 个人实验/单项目 → 独立配置
- 团队/社区共享/跨项目 → Plugin 模式
- 混合使用：Plugin 提供通用基础，`.claude/` 覆盖项目特定需求

### 7.4 环境变量体系设计

| 变量 | 生命周期 | 用途 |
|------|---------|------|
| `${CLAUDE_PLUGIN_ROOT}` | 随插件版本更新变化 | 指向插件安装目录 |
| `${CLAUDE_PLUGIN_DATA}` | 跨版本持久保留 | 持久数据目录（`~/.claude/plugins/data/{id}/`） |
| `${CLAUDE_PROJECT_DIR}` | 当前会话 | 项目根目录 |
| `CLAUDE_PLUGIN_OPTION_<KEY>` | 子进程 | 导出给 hooks/scripts 的配置项 |

---

## 第八章：Subagent 设计规范（第三轮新增）

> **数据来源**：code.claude.com/docs/en/sub-agents + studynil.com/claude-code/best-practice/subagents
> **更新**：2026-06-16 第三轮循环

### 8.1 11 大内置 Agent 职责边界

| Agent | 默认模型 | 权限模式 | 职责 | 可改代码 |
|-------|---------|---------|------|:---:|
| Explore | Haiku | 只读 | 代码库快速探索、文件搜索、架构理解 | ❌ |
| Plan | 继承 | 只读 | Plan 模式下收集上下文 | ❌ |
| general-purpose | 继承 | 全部 | 复杂的多步骤+多工具任务 | ✅ |
| Bash | 继承 | 终端 | 隔离上下文运行命令 | ✅ |
| statusline-setup | Sonnet | 读写 | 配置状态栏 | ✅ |
| claude-code-guide | Haiku | 只读 | 回答 Claude Code 自身功能问题 | ❌ |
| code-reviewer | Sonnet | Read/Grep/Glob | 代码质量审查 | ❌ |
| security-reviewer | Sonnet | Read/Grep/Glob/Bash | 安全漏洞检测 | ✅ |
| test-creator | Sonnet | Read/Write/Bash | 生成测试用例 | ✅ |
| build-error-resolver | Sonnet | Read/Bash | 修复构建错误 | ✅ |
| doc-updater | Sonnet | Read/Write | 更新文档 | ✅ |

### 8.2 权限模式选择指南

| 模式 | 适用场景 | 风险等级 |
|------|---------|:---:|
| `default` | 标准权限检查，每个敏感操作请求批准 | 🟢 低 |
| `plan` | 只读信息收集（Plan/Explore 模式） | 🟢 最低 |
| `acceptEdits` | 接受编辑无确认，但其他操作仍需批准 | 🟡 中 |
| `bypassPermissions` | 完全绕过权限检查（仅高信任 agent） | 🔴 高 |

**最佳实践**：Explore 和 Plan 用 plan 模式；code-reviewer 用 default；security-reviewer 用 acceptEdits 以便自动修复。

### 8.3 Subagent 设计反模式

1. **Underspecified Agents**：description 过于模糊（如"研究课题并返回结果"），导致输出格式不可预测
2. **Overlap Responsibility**：两个 agent 职责重叠，造成重复工作或互相覆盖结果
3. **Unbounded Scope**：无明确约束（maxTurns、工具限制），agent 可能无限探索
4. **Missing Success Criteria**：没有可验证的完成条件（"实现功能" vs "实现功能使 npm test 通过"）

### 8.4 任务分解模板

```
Task: [要完成的任务]
Subtasks:
  [子任务 A — 独立]
  [子任务 B — 独立]
  [子任务 C — 依赖 A 和 B 输出]
对于每个子任务：
  Input: [传入的具体内容]
  Output: [返回的具体格式]
  Constraint: [范围限制]
  Done when: [可验证条件]
```

---

## 第九章：Agent Skills 设计模式（第三轮新增）

> **数据来源**：platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills + dlai.ai Agent Skills课程
> **更新**：2026-06-16 第三轮循环

### 9.1 Pre-built vs Custom Skills 设计决策

| 维度 | Pre-built (Anthropic) | Custom Skills |
|------|----------------------|---------------|
| **Skill ID** | 短名称（pptx/xlsx/docx/pdf） | 生成式 UUID（skill_01...） |
| **管理方** | Anthropic 维护和更新 | 用户通过 Skills API 上传 |
| **版本控制** | 日期格式（20251013）或 latest | Epoch 时间戳或 latest |
| **可用范围** | 所有用户 | 工作区私有 |
| **适用场景** | 通用文档生成 | 领域特定专业知识 |
| **学习曲线** | 零配置 | 需编写 SKILL.md + 可选脚本 |

### 9.2 Container 模式详解

```json
{
  "container": {
    "skills": [
      {
        "type": "anthropic",
        "skill_id": "pptx",
        "version": "latest"
      },
      {
        "type": "custom",
        "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
        "version": "latest"
      }
    ]
  }
}
```

- 单个请求最多 **8 个 Skills**
- Anthropic 和 Custom Skills 可在同一请求中混合使用
- 所有 Skills 共享同一个代码执行环境

### 9.3 渐进式披露设计原则

Skills 的三级渐进式信息披露：

| 层级 | 触发条件 | 加载内容 | 上下文成本 |
|:---:|------|------|:---:|
| **L1 发现** | Claude 启动时 | 所有可用 Skills 的元数据（名称+描述） | 极低 |
| **L2 触发** | 任务匹配 Skill 时 | `SKILL.md` 完整指令内容 | 中等 |
| **L3+ 引用** | 需要补充知识时 | `reference.md`、`scripts/` 等辅助文件 | 按需 |

**核心优势**：Claude 瞬间了解可用的 Skills，但只在需要时才加载完整指令，极大节省上下文窗口。

### 9.4 Skills 目录结构最佳实践

```
my-skill/
├── SKILL.md         # 核心指令（简练：包含何时触发、做什么、输入/输出格式）
├── reference.md     # 详细参考（可选，仅在需要时加载）
└── scripts/         # 辅助脚本（可选）
    ├── helper.py
    └── validate.sh
```

**SKILL.md 编写原则**：
- **description 是触发器**：写给模型看（"when should I fire?"），不是给人类看的摘要
- **指令精炼**：避免冗长，200 行以内
- **输入/输出明确**：定义好 Skill 期望的输入格式和输出格式

### 9.5 Skills 生态定位

Skills vs 其他扩展方式对比：

| 方式 | 上下文共享 | 触发方式 | 独立权限 |
|------|:---:|------|:---:|
| **Skills** | 可 fork 隔离 | 自动匹配 + 手动 `/name` | 部分（工具限制） |
| **Subagents** | 完全隔离 | 描述匹配 + 手动 `/agents` | 完全（独立 tools/permissions） |
| **Hooks** | 事件共享 | 事件驱动自动 | 无（事件作用域） |
| **MCP** | 外部连接 | 工具调用 | 服务端定义 |

---

> 🛡️ **韧性五原则摘要（本轮追加扩展）**
>
> 1. **超载卸载** — 主Agent 思考深度有限时，把高复杂度子任务卸载到 subagent（不同上下文可能看到不同的解决方案）
> 2. **规模约束** — 每个 CLAUDE.md 控制在 200 行以内，Skills 同样适用此约束
> 3. **人机协同** — Plugin 的 permissionMode 提供 4 级权限控制，让人类保持对关键操作的控制
> 4. **反脆弱验证** — 并行运行 code-reviewer + security-reviewer 两个独立上下文发现不同问题
> 5. **渐进式进化** — Skills 的三级渐进披露机制确保能力扩展不牺牲当前效用
>
> 更新：2026-06-16 第四轮循环

---

## 十、Dynamic Workflows：大规模并行 Agent 设计原则

> 来源：Anthropic 2026-06-03 发布 | 基于 C10 Subagents 课程的工程化延伸

### 10.1 核心概念

Dynamic Workflows 将「子代理委派」从手动设计提升为**自动规模化**范式：

```
传统模式：主Agent → 手动定义 3-5 个子代理 → 逐个调度
Dynamic Workflows：主Agent → 自动拆解任务 → 动态生成 N 个子代理 → 并行执行
```

### 10.2 设计铁律

**铁律 6: 反智能惰性（Anti-Cognitive-Laziness）**

问题：超长会话中模型逐渐疲劳、忽略新信息、产生幻觉。
方案：每个子 Agent 拥有**独立上下文窗口**，从零开始加载任务描述和必要数据，不与主对话共享上下文污染。

```
错误模式：100轮对话后仍在同一上下文追问 → 模型疲劳 → 幻觉
正确模式：每遇复杂子任务 → 新建 Subagent → 独立上下文 → 干净结果
```

**铁律 7: 上下文预算控制（Context Budget Control）**

- 子 Agent 默认限制工具调用次数和上下文 Token 数
- 主 Agent 仅接收子 Agent 返回的**结构化摘要**，而非完整执行日志
- 子 Agent 失败不污染主上下文

### 10.3 适用条件判断

| 条件 | Dynamic Workflows | 传统 Subagent |
|------|:---:|:---:|
| 任务可拆为 10+ 独立子任务 | ✅ | ❌ |
| 子任务间无复杂依赖 | ✅ | ✅ |
| 需要人工逐步骤决策 | ❌ | ✅ |
| 代码量 > 10 万行规模迁移 | ✅ | ❌ |
| 3-5 个明确专业角色分工 | ❌ | ✅ |

### 10.4 已知性能基准

- 75 万行代码跨语言迁移（Zig→Rust）：6 天，99.8% 测试通过率
- 传统方案需团队数月，Dynamic Workflows 单次对话完成

---

## 十一、Generator → Evaluator 验证铁律

> 来源：Anthropic Cookbook + 官方 Skills 最佳实践

### 11.1 核心原则

> 每个生成步骤必须配对独立的评估器。评估器独立重新推导检查条件，不与生成器共享上下文。

### 11.2 设计模式

```
Generator（生成器）          Evaluator（评估器）
     │                              │
     │ 生成产物                      │ 独立重新推导检查条件
     │                              │
     └──────── 产物传入 ────────────→│
                                    │ 通过阈值？→ 链入下一步
                                    │ 未通过 → 修复或人工介入
```

### 11.3 为何必须分离

- **偏见隔离**：Generator 的推理路径不能影响 Evaluator 的判断
- **多样性检查**：独立上下文可能发现 Generator 遗漏的问题
- **可审计**：每次验证产生独立日志，支持追溯和回归测试

### 11.4 实施清单

```
□ 每个生成步骤定义明确的通过/失败阈值
□ Evaluator 使用独立上下文（不继承 Generator 对话）
□ 验证失败自动路由到修复流程或人工审核
□ 评估日志持久化到文件（NOTES.md + eval_log）
□ 定期重评以检测能力漂移
```

> 更新：2026-06-16 第四轮循环 | 本轮新增：Dynamic Workflows 大规模并行设计原则（铁律6/7）、Generator→Evaluator 验证铁律（反偏见隔离）


---

## 九、Agentic 模式选择六维度决策矩阵（Anthropic 2026年4月）

### 9.1 上下文中心分解（Context-Centric Decomposition）
不是按"做什么类型的工作"来分解任务，而是按"每个Agent需要什么上下文"来分解。如果两个子任务需要相同的上下文，交给一个Agent比拆成两个Agent更优。

| 决策因素 | 单一Agent | 多Agent |
|---------|----------|---------|
| 子任务所需上下文高度重叠 | ✅ | ❌ 上下文碎片化 |
| 子任务间存在强依赖 | ✅ 状态共享自然 | ❌ 状态同步成本高 |
| 每个子任务有独立的上下文边界 | ❌ 上下文过载 | ✅ 各Agent专注 |
| 子任务需要并行处理 | ❌ 难以并行 | ✅ 天然适合 |

### 9.2 六大Agentic模式选择指南

| 模式 | 核心特征 | 最佳场景 | 复杂度 |
|------|---------|---------|:---:|
| Prompt Chaining | 顺序执行，前一步输出为后一步输入 | 线性工作流 | 低 |
| Routing | 根据输入分类分发到不同处理器 | 多类型请求 | 低 |
| Parallelization | 同时执行多个独立子任务 | 独立计算密集型 | 中 |
| Orchestrator-Workers | 中央调度+专业工作者 | 复杂多变任务 | 高 |
| Evaluator-Optimizer | 生成→评估→迭代改进 | 质量敏感任务 | 高 |
| Agent Teams | 多角色自主协作 | 长周期开放域问题 | 最高 |

### 9.3 Generator→Evaluator 验证循环（Anthropic推荐最高质量保证模式）
- 每个生成步骤配对独立的评估器
- 评估器独立重新推导检查条件（不与生成器共享上下文）
- 通过阈值→继续；未通过→修复或人工介入


---

## 十二、Agent SDK 设计哲学（第5轮学习·R92新增）

> 来源：platform.claude.com Agent SDK Python 参考文档

### 12.1 会话管理二元哲学

SDK 提供了两种会话模式，体现 Anthropic 对 Agent 设计的两条路径：

| 维度 | `query()` | `ClaudeSDKClient` |
|------|-----------|-------------------|
| 设计哲学 | 无状态函数式 | 有状态对象式 |
| 会话生命周期 | 每次调用即一次完整生命 | 显式 open → 多轮 → close |
| 适用场景 | 可并行的一次性任务 | 需要上下文累积的持续对话 |
| 上下文扩展 | `continue_conversation=True` 或 `resume` | 自动累积 |

**设计原则**：`query()` 的"默认新会话"设计体现最小意外原则——每个调用是独立计算单元，天然支持大规模并行。`ClaudeSDKClient` 的"显式生命周期"体现精确控制原则——开发者对会话状态有完全所有权。

### 12.2 Tool Annotations 的透明性设计

```python
ToolAnnotations(
    readOnlyHint=True,      # 声明"我是只读的"
    destructiveHint=True,   # 声明"我可能有破坏性"
    idempotentHint=False,   # 声明"重复调用可能有副作用"
    openWorldHint=True      # 声明"我连接外部世界"
)
```

四个布尔标志构成的语义框架实现了 **工具契约自声明**：
- 元数据不由SDK强制校验，而是作为"提示"注入Claude的推理
- Claude据此自主判断安全边界——这是一种信任模型而非访问控制模型
- 开发者必须诚实标注，否则会破坏Agent的安全判断

### 12.3 MCP Server 的内联注册模式

`create_sdk_mcp_server()` 允许在 Python 应用中内联注册 MCP 服务：

```python
# 函数式工具注册：用装饰器标记函数即完成 MCP 工具定义
@tool("greet", "Greet a user", {"name": str})
async def greet(args): ...

server = create_sdk_mcp_server("my-server", tools=[greet])
options = ClaudeAgentOptions(mcp_servers={"my": server})
```

**设计洞察**：MCP 工具注册从"配置式"（JSON文件）进化为"代码式"（Python装饰器），模糊了配置与代码的边界。工具定义即类型声明，函数签名即协议契约——体现了 Software 2.0 时代"代码即配置"的范式。

### 12.4 会话检索的审计能力

```python
# 按项目列出会话
list_sessions(directory="/path/to/project", limit=10)
# 按会话ID获取消息
get_session_messages(session_id="xxx")
```

完整的会话查询 API 提供了可观测性的基石——不是"黑盒Agent"，而是"可查询的执行历史"。这是 SOUL.md 五层可观测性支柱的编程接口落地。

---

## 十三、Agent Teams 架构设计原则（R89新增）

> 来源：Anthropic 官方 Agent Teams 文档 (code.claude.com/docs/en/agent-teams)
> 更新：2026-06-16 第四轮循环

### 13.1 Agent Teams 核心架构

Agent Teams 让多个 Claude Code 实例协同工作，一名 Team Lead 协调、分配任务、合成结果，Teammates 各自独立运行于自己的上下文窗口，并可直接相互通信。

```
Team Lead (主会话)
  ├── Teammate 1 (独立上下文窗口)
  ├── Teammate 2 (独立上下文窗口)
  ├── Teammate N (独立上下文窗口)
  └── 共享资源: Task List + Mailbox
```

**与 Subagents 的本质区别**：
| 维度 | Subagents | Agent Teams |
|------|----------|-------------|
| 上下文 | 独立窗口，结果返回调用方 | 独立窗口，完全自主 |
| 通信 | 仅向主 Agent 汇报 | Teammates 之间直接通信 |
| 协调 | 主 Agent 管理所有工作 | 共享任务列表 + 自主协调 |
| 适用场景 | 专注任务，只关心结果 | 需要讨论、辩论、协作的复杂任务 |
| Token 成本 | 较低（结果摘要回主上下文） | 较高（每个 Teammate 是独立实例） |

### 13.2 决策核心：何时使用 Agent Teams

**最强场景**：
1. **研究审查**：多个 Teammates 同时研究问题的不同方面，分享并挑战彼此发现
2. **新模块开发**：每人负责独立模块，互不干扰
3. **竞合调试**：并行测试不同假设，快速收敛到正确答案
4. **跨层协调**：前后端+测试各由不同 Teammate 负责

**不应使用的场景**：顺序任务、同文件编辑、强依赖任务 → 使用单会话或 Subagents

### 13.3 任务列表协调机制

任务有三种状态：`pending` → `in progress` → `completed`。任务间可设置依赖关系。

**自协调模式**：
- Team Lead 创建任务 → Teammates 自主申领 → 完成任务后申领下一项
- 使用文件锁防止多 Teammate 争抢同一任务

**显式分配模式**：
- Team Lead 直接指定某任务给某 Teammate

### 13.4 质量门控 Hooks

Teammate 专属 Hook 事件：
| 事件 | 触发时机 | 控制能力 |
|------|---------|---------|
| `TeammateIdle` | Teammate 即将空闲 | Exit code 2 → 发送反馈，保持工作 |
| `TaskCreated` | 任务创建时 | Exit code 2 → 阻止创建，发送反馈 |
| `TaskCompleted` | 任务标记完成时 | Exit code 2 → 阻止完成，发送反馈 |

### 13.5 架构设计铁律

1. **团队规模限制**：每个团队最多 5 个 Teammates（超此数量协调成本指数增长）
2. **显示模式选择**：In-process（Shift+Down 循环切换）/ Split-panes（tmux/iTerm2 分屏）
3. **计划审批门**：复杂任务必须要求 Teammate 先规划再执行，Lead 审核后放行
4. **清理原则**：必须由 Lead 执行团队清理，Teammate 直接执行可能导致状态不一致

---

## 2026-06-16 更新：Managed Agents 架构对 Agent 设计的启示

### 一、Managed Agents 三层架构的设计启示

Anthropic 的 Managed Agents 体系借鉴了操作系统虚拟化思想——将 Agent 的"大脑"（推理层）、"双手"（执行层）和"会话"（状态层）解耦为三个独立接口，各自可独立替换和容错。这一设计哲学对 AI Agent 架构设计有深远启示：

**Brain / Hands / Session 三向解耦**

| 层级 | 角色 | 技术特性 | 设计启示 |
|------|------|---------|---------|
| Brain（推理层） | Claude 模型 + Harness | 无状态，可水平扩展 | Agent 的 reasoning 应与 execution 分层 |
| Hands（执行层） | 沙箱容器 + MCP 服务器 | 按需启动，不占资源 | 工具执行应容器化，资源按需分配 |
| Session（状态层） | Append-only 事件日志 | 独立于 context window | 任务状态应持久化，支持断点恢复 |

**核心设计原则**：
1. **独立容错**：Brain 崩溃？Session 日志还在。系统自动唤醒新实例从事件日志恢复。
2. **安全边界**：凭证永远不进入执行沙箱，防止 Prompt Injection 窃取 Token。
3. **接口稳定性**：`execute(name, input) → string` / `provision({resources})` / `wake(sessionId)` 三个接口超脱具体实现。

### 二、Subagent 隔离上下文设计原则

Subagent 的核心价值在于**上下文隔离**，这是防止"上下文污染"的关键机制：

**防止上下文污染的五条原则**：
1. **独立上下文窗口**：每个 Subagent 拥有自己的 context window，不共享主会话状态
2. **摘要回传**：Subagent 完成任务后仅返回结果摘要，不将中间推理过程灌入主会话
3. **模型降级策略**：轻量任务（如文件搜索、格式检查）指定低成本模型（Haiku），重量任务（如架构分析）使用高性能模型（Opus/Sonnet）
4. **工具最小化**：通过 `tools` 白名单精确控制——只读代理只给 Read/Grep/Glob，杜绝写操作权限
5. **禁止嵌套派生**：Plan 代理不能派生子代理，防止无限递归和 Token 失控

**何时使用 Subagent 的判断矩阵**：
- 任务需要专注执行，不需要主会话参与中间过程 → Subagent
- 任务需要多角色协商、交叉验证 → Agent Teams
- 任务规模超大（100+子任务）→ Dynamic Workflows

### 三、Agent Teams 多实例协作模式

Agent Teams 的协作模式建立在一套松耦合通信机制之上：

**三种核心通信机制**：
1. **Mailbox 通信**：Teammate 之间直接互发消息，无需经过 Lead 中转。降低协调瓶颈。
2. **共享任务列表**：所有 Teammate 可查看全局任务池，自我认领任务。支持 Pull 模型调度。
3. **自我协调**：通过共享任务状态 + Teammate 间通信实现去中心化协调。

**Lead 的角色定义**：
- 负责任务分解和初始分配
- 监控进度（非微观管理）
- 汇总和协调输出
- 执行团队清理（不许 Teammate 越权操作）

**规模原则**：团队上限 5 个 Teammates（超出此数协调成本指数增长）。

### 四、Dynamic Workflows 动态编排设计

Dynamic Workflows 是 2026 年 5 月随 Claude Opus 4.8 发布的全新编排范式。本质是"AI 即兴生成 JavaScript 编排脚本"。

**四大编排模式的设计启示**：

| 模式 | 场景 | 设计要点 |
|------|------|---------|
| 大规模审计 | 代码库安全扫描 | 每个模块独立子 Agent，并行检查，结果汇总 |
| 大规模迁移 | 75 万行代码重构 | 架构拆分 → 模块迁移 → 测试生成，人类审核关键决策 |
| 交叉验证 | 多视角审查 | 多个 Agent 从不同角度审查同一对象，比对差异 |
| 深度研究 | 并行信息搜集 | 多方信息并行搜集，交叉验证后输出综合报告 |

**Dynamic Workflows 与 Subagent/Agent Teams 的选择决策**：
- 任务可分解为确定性步骤 → Dynamic Workflows（最高可预测性）
- 任务需要灵活调度 → Subagent（主 Agent 全权调度）
- 任务需要多角色协商 → Agent Teams（涌现式协作）

### 五、Advisor Tool 决策升级机制

Advisor Tool 实现了"主模型 + 咨询模型"双层架构：

**工作流程**：
1. 主模型（如 Sonnet）执行常规任务推理
2. 在关键决策点自动触发 Advisor 咨询
3. Advisor 模型（如 Opus，更强）给出建议
4. 主模型综合 Advisior 建议后做出最终决策

**设计启示**：不要试图用一个模型解决所有问题。将"执行"和"判断"分离——轻量模型负责执行，重量模型负责把关。

### 六、六大 Agentic 模式的复杂度阶梯

```
Prompt Chaining → Routing → Parallelization → Orchestrator-Workers → Evaluator-Optimizer → Agent Teams
```

| 层级 | 模式 | 复杂度 | 关键特征 | 选择信号 |
|------|------|--------|---------|---------|
| 1 | Prompt Chaining | ⭐ | 顺序执行，A→B→C | 任务可分解为固定步骤 |
| 2 | Routing | ⭐ | 分类分发 | 输入类型差异大 |
| 3 | Parallelization | ⭐⭐ | 同时执行 | 子任务无依赖 |
| 4 | Orchestrator-Workers | ⭐⭐⭐ | 中央调度 | 任务动态变化 |
| 5 | Evaluator-Optimizer | ⭐⭐⭐⭐ | 迭代提升 | 质量要求高 |
| 6 | Agent Teams | ⭐⭐⭐⭐⭐ | 多主体协商 | 需要多角色协作 |

**架构选择铁律**：能用简单模式解决的决不用复杂模式。每个复杂度升级都意味着成本、延迟和不可预测性的指数增长。

---

## R91 增量：子代理5层嵌套设计原则（2026-06-17）

> 来源：Claude Code v2.1.172 (June 10, 2026) + Anthropic 官方文档

### 嵌套子代理架构

v2.1.172 起，子代理可孵化自己的子代理，最多5层深。这是 Agent 复杂度层级的重大升级。

```
Level 0: 纯 LLM 回答
Level 1: LLM + 工具调用
Level 2: LLM + 多工具 + 推理循环（单 Agent）
Level 3: LLM + 单层子代理编排
Level 4: LLM + 嵌套子代理编排（≤5层）← NEW
Level 5: LLM + 自进化 + 持久记忆（自主 Agent）
```

### 嵌套设计原则

1. **层层隔离**：每层子代理拥有独立上下文窗口，父级上下文不泄露到子代理，子代理结果摘要回传
2. **深度节制**：Token 消耗随嵌套深度指数增长，生产环境建议 ≤3 层
3. **场景匹配**：仅当父代理无法在单一上下文中完成任务时才使用嵌套——如 1000+ 文件代码库的分层审查
4. **结果压缩**：深层子代理必须返回结构化摘要，避免逐层膨胀

### 嵌套反模式

- **过度嵌套**：将简单任务分解为多层子代理，导致 Token 成本暴增 10x+
- **循环依赖**：A 代理嵌套 B，B 嵌套 C，C 又调用 A
- **上下文碎片化**：每层只看到局部信息，全局一致性丢失
- **调试黑洞**：5 层嵌套的错误追踪几乎不可能

### 架构升级的铁律（新增强版）

在原铁律基础上增加：
> **嵌套不是默认选项**。仅在单层子代理明确无法覆盖任务复杂度时，才考虑增加深度。每增加一层嵌套，必须能回答"这一层解决了哪一层无法解决的问题？"

---

## R92 增量：Agent Runtime 范式与云端自治（2026-06-17）

> 来源：Code with Claude Tokyo (June 10-11, 2026) — Claude Code 从 CLI 进化为全栈 Agent 平台

### 一、Agent 复杂度层级升级（加入 Agent Runtime）

原 6 层复杂度阶梯增加第 7 层——云端自治：

```
Level 0: 纯 LLM 回答
Level 1: LLM + 工具调用
Level 2: LLM + 多工具 + 推理循环（单 Agent）
Level 3: LLM + 单层子代理编排
Level 4: LLM + 嵌套子代理编排（≤5层）
Level 5: LLM + 自进化 + 持久记忆（自主 Agent）
Level 6: Agent Runtime — 云端托管 + 事件驱动 + 异步自治 ← NEW
```

### 二、Agent Runtime 设计原则

**核心定义**：Agent Runtime 是云端托管的 Agent 执行环境，具备触发器、密钥管理、状态持久化能力。Agent 不再是"你调用的工具"，而是"自己运行的平台"。

**Routines（例程）三层架构**：

```
触发器层 → 执行层 → 结果层
Cron/API/GitHub Events → Agent 执行 → PR/通知/日志
```

**设计铁律**：

1. **触发即执行**：Routine 被触发后无需人工干预，Auto Mode 自动判断安全性
2. **状态外置**：Agent 自身无状态，凭据和配置存储在 Managed Agents Vault
3. **异步优先**：Routines + Remote Control 使长时间任务异步化，开发者不必在线等待
4. **安全的默认**：Security Scanning 作为"第一个 Routine"的最佳实践——夜间扫描 → 自动修复 PR

### 三、从同步到异步：Agent 交互范式升级

传统模式：
```
开发者启动任务 → 守在终端前 → 逐条确认 → 等待完成 → 审查结果
```

Agent Runtime 模式：
```
开发者定义 Routine → 离开 → Routine 定时触发 → Auto Mode 自动执行 → Remote Control 远程监控 → 审查 diff/PR
```

**关键洞察**：Agent Runtime 的本质是"开发者时间的解放"。一个 Routine 替代初级工程师夜间值班的成本远低于人力成本——Claude Fable 5 $1000/M tokens 的定价逻辑：贵的是模型，省的是人力。