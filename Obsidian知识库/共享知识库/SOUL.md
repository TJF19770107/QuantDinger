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
> 更新：2026-06-16 第三轮循环
