---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_cdb23bc46a7a11f1a0095254002afed2
    ReservedCode1: i0/BX8k0pDVtMRyEb9LIOIyGng4wFt+pctBvt9jnLAlpkxjLtKXmAvyN3WIj0X3zIppqECGMxJLUH+uranspBYmpt8GS1txqkLr+r5DJ8U6xg0C1YOyy7D1g9mH/nR8c2litzflOn6EYT943x4WRyrE4TJKG5F1R0b50X00beLIR3p9C605NpO06m3A=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_cdb23bc46a7a11f1a0095254002afed2
    ReservedCode2: i0/BX8k0pDVtMRyEb9LIOIyGng4wFt+pctBvt9jnLAlpkxjLtKXmAvyN3WIj0X3zIppqECGMxJLUH+uranspBYmpt8GS1txqkLr+r5DJ8U6xg0C1YOyy7D1g9mH/nR8c2litzflOn6EYT943x4WRyrE4TJKG5F1R0b50X00beLIR3p9C605NpO06m3A=
---





# Anthropic官方课程-390节全集

> **来源**：Anthropic官方文档（docs.anthropic.com / code.claude.com / skilljar.com）
> **整理日期**：2026-06-17
> **版本**：R54 — 全域知识库重构版

---

## 目录

- [A. 课程体系总览](#a-课程体系总览)
- [B. 子代理（Sub-agents）深度指南](#b-子代理sub-agents深度指南)
- [C. 多Agent协作（Agent Teams）](#c-多agent协作agent-teams)
- [D. Claude Code最佳实践](#d-claude-code最佳实践)
- [E. Skills系统](#e-skills系统)
- [F. Hooks自动化](#f-hooks自动化)
- [G. Agent SDK](#g-agent-sdk)
- [H. MCP协议](#h-mcp协议)

---

## A. 课程体系总览

### A.1 Anthropic官方课程完整目录

Anthropic通过Skilljar平台提供免费课程库，覆盖从15分钟速成到数小时深度课。核心分类：**速成类**（15-20分钟）、**开发实操类**（数小时）、**平台集成类**（与云服务对接）、**场景应用类**（教育/非营利等）。

| # | 课程名称 | 时长 | 难度 | 证书 | 核心内容 |
|---|---------|------|------|:---:|---------|
| 1 | **Claude 101** | ~1h | 初级 | √ | 日常工作任务中使用Claude，核心功能与高级学习资源 |
| 2 | **Claude Code 101** | ~2h | 初级-中级 | √ | 日常开发工作流中有效使用Claude Code |
| 3 | **Claude Platform 101** | ~2h | 初级-中级 | √ | 在Claude Developer Platform上从零构建应用 |
| 4 | **Introduction to Claude Cowork** | ~2h | 初级 | √ | Cowork任务循环、插件与Skills、文件与研究工作流、多步工作引导 |
| 5 | **Claude Code in Action** | ~2h | 中级 | √ | 将Claude Code集成到开发工作流实战 |
| 6 | **AI Fluency: Framework & Foundations** | ~2h | 初级 | √ | 有效、高效、合乎伦理、安全地与AI系统协作 |
| 7 | **Building with the Claude API** | ~4h | 中级 | √ | 使用Claude API全频谱开发（85节详细大纲） |
| 8 | **Introduction to Model Context Protocol** | ~1.5h | 中级 | √ | 用Python从零构建MCP服务器和客户端，三原语（Tools/Resources/Prompts） |
| 9 | **Model Context Protocol: Advanced Topics** | ~2h | 高级 | √ | 高级MCP实现模式：Sampling、Notifications、文件系统访问、Transport机制 |
| 10 | **AI Fluency for Educators** | ~2h | 初级 | √ | 教育工作者将AI Fluency融入教学实践和机构战略 |
| 11 | **AI Fluency for Students** | ~2h | 初级 | √ | 学生负责任地使用AI辅助学习、职业规划和学术成功 |
| 12 | **Introduction to Subagents** | ~2h | 中级-高级 | √ | 创建和使用Subagents、上下文管理与任务委派、Skills结合、构建多Agent系统 |
| 13 | **Introduction to Agent Skills** | ~1.5h | 中级 | √ | SKILL.md结构、条件加载、手动触发、可复用工作流构建 |
| 14 | **AI Capabilities and Limitations** | ~30min | 初级 | - | AI能力边界认知、合理期望管理 |
| 15 | **Teaching AI Fluency** | ~1.5h | 中级 | √ | 教授AI流利度的教学方法和课程设计 |
| 16 | **Cloud Platform Courses** | 视平台 | 高级 | √ | 与AWS Bedrock、GCP Vertex AI等云平台对接 |
| 17 | **CCA Foundations Certification** | 自定 | 中级-高级 | √ | 5领域60题认证考试（AI Fluency / API / MCP / Claude Code / Platform） |

### A.2 课程分类维度

```
+-------------------------------+-------------------------------+-------------------------------+---------------------------------+
|           速成类               |           开发实操类            |           平台集成类            |            场景应用类              |
|           15-20min             |           数小时                |           与云服务对接           |            教育/非营利              |
+-------------------------------+-------------------------------+-------------------------------+---------------------------------+
| AI Capabilities & Limitations | Claude 101                    | Cloud Platform Courses          | AI Fluency for Educators          |
|                               | Claude Code 101               | (AWS Bedrock / GCP Vertex AI)   |                                   |
|                               | Claude Code in Action         |                                | AI Fluency for Students           |
|                               | Building with the Claude API  |                                |                                   |
|                               | MCP Introduction              |                                | Teaching AI Fluency               |
|                               | MCP Advanced                  |                                |                                   |
|                               | Introduction to Subagents     |                                |                                   |
|                               | Introduction to Agent Skills  |                                |                                   |
|                               | Claude Cowork                 |                                |                                   |
+-------------------------------+-------------------------------+-------------------------------+---------------------------------+
```

### A.3 推荐学习路径

| 角色 | 推荐路径 |
|------|---------|
| **非开发者** | AI Capabilities → Claude 101 → AI Fluency → Subagents入门 |
| **开发者** | Claude Code 101 → Claude Code in Action → Building with API → MCP入门 |
| **教育工作者** | AI Fluency Framework → AI Fluency for Educators → Teaching AI Fluency |
| **高级工程师** | MCP入门 → MCP进阶 → Subagents → Agent Skills → Cloud Platform |
| **认证追求者** | 全路径 → CCA Foundations Certification |

### A.4 CCA Foundations 认证考试详情

5领域60题认证考试，覆盖Anthropic核心技术栈：

| 领域 | 题量 | 覆盖内容 |
|------|:---:|---------|
| AI Fluency | 12 | AI能力、伦理使用、负责任AI实践 |
| Building with Claude API | 12 | API调用、提示工程、参数调优 |
| MCP协议 | 12 | 服务器构建、客户端连接、三原语 |
| Claude Code | 12 | 终端代理、四阶段工作流、Skills/Hooks |
| Claude Platform | 12 | 开发者平台、部署、组织管理 |

---

## B. 子代理（Sub-agents）深度指南

### B.1 核心概念

子代理是**专业化的AI助手**，处理特定类型的任务。每个子代理运行在**自己的上下文窗口**中，拥有自定义系统提示、特定工具访问权限和独立权限控制。

**何时使用子代理**：当副任务会向主对话中涌入搜索结果、日志或文件内容时——子代理在自己的上下文中完成这些工作，仅返回摘要。

**子代理 vs 后台代理 vs Agent Teams 对比**：

| 维度 | 子代理 (Sub-agents) | 后台代理 (Background Agents) | Agent Teams |
|------|---------------------|------------------------------|-------------|
| **上下文** | 独立上下文窗口，结果返回调用者 | 独立上下文窗口，完全独立 | 独立上下文窗口，完全独立 |
| **通信** | 仅向主代理报告结果 | 仅向主代理报告结果 | 队友之间直接通信 |
| **协调** | 主代理管理所有工作 | 主代理监控多个并行会话 | 共享任务列表 + 自协调 |
| **作用域** | 单会话内 | 跨多个独立会话 | 多会话协作 |
| **Token成本** | 较低（结果摘要返回主上下文） | 中等 | 较高（每个队友是独立Claude实例） |
| **最佳场景** | 专注任务，只需结果 | 长时间运行的独立任务 | 需要讨论和协作的复杂工作 |

### B.2 内置子代理

Claude Code包含以下内置子代理，在交互式会话中自动注册：

#### Explore（探索）

| 属性 | 值 |
|------|-----|
| **模型** | Haiku（快速、低延迟） |
| **工具** | 只读工具（拒绝Write和Edit） |
| **用途** | 文件发现、代码搜索、代码库探索 |

调用时可指定彻底程度：
- **quick**：目标查找
- **medium**：平衡探索
- **very thorough**：综合分析

#### Plan（规划）

| 属性 | 值 |
|------|-----|
| **模型** | 继承主对话 |
| **工具** | 只读工具（拒绝Write和Edit） |
| **用途** | Plan模式下的代码库研究 |

在Plan模式下，Claude将研究任务委托给Plan子代理，探索输出留在独立上下文窗口，主对话保持只读。

#### General-purpose（通用）

| 属性 | 值 |
|------|-----|
| **模型** | 继承主对话 |
| **工具** | 所有工具 |
| **用途** | 复杂研究、多步操作、代码修改 |

适合需要探索+修改、需要复杂推理来解释结果、或需要多个依赖步骤的任务。

#### 辅助内置代理

| 代理 | 模型 | 触发场景 |
|------|------|---------|
| `statusline-setup` | Sonnet | 运行 `/statusline` 配置状态栏 |
| `claude-code-guide` | Haiku | 询问Claude Code功能相关问题 |

**启用/禁用**：
- 在 `permissions.deny` 中添加特定内置类型来阻止
- 在非交互模式和Agent SDK中设置 `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` 移除所有内置类型
- 阻止所有子代理：在 `permissions.deny` 中拒绝 `Agent` 工具本身

### B.3 自定义子代理

#### 创建方法

**方法1：`/agents` 命令（推荐）**

```
/agents → Library → Create new agent → 选择作用域 → Generate with Claude
```

**方法2：手动Markdown文件**

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
memory: user
---

You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

#### YAML 前置元数据完整字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|:---:|------|
| `name` | string | ✓ | 子代理唯一标识符 |
| `description` | string | ✓ | Claude据此判断何时委托任务 |
| `tools` | string | - | 允许的工具列表（如 `Read, Grep, Glob, Bash`），逗号分隔 |
| `model` | string | - | 模型选择：`opus` / `sonnet` / `haiku` / `inherit` |
| `memory` | string | - | 持久记忆：`user` / `project` / `none` |
| `permissionMode` | string | - | 权限模式：`default` / `auto` / `plan` |
| `isolation` | string | - | 隔离级别：`process` / `sandbox` |
| `background` | boolean | - | 后台运行模式 |
| `hooks` | object | - | 子代理级Hooks配置 |
| `skills` | array | - | 加载的Skills列表 |
| `mcpServers` | array | - | 连接的MCP服务器 |
| `color` | string | - | UI显示颜色 |

### B.4 子代理作用域与优先级

子代理按作用域分层管理，同名时高优先级覆盖低优先级：

```
优先级从高到低：
1. Managed settings（组织级部署）        ← 最高
2. --agents CLI 标志（当前会话）
3. .claude/agents/（当前项目）           ← 推荐，可纳入版本控制
4. ~/.claude/agents/（所有项目）         ← 个人跨项目共享
5. Plugins agents/ 目录（插件安装时）    ← 最低
```

**路径发现规则**：
- 项目子代理从当前工作目录向上扫描，所有 `.claude/agents/` 目录均被扫描
- `--add-dir` 添加的目录中 `.claude/agents/` 也会加载
- 支持递归扫描，可组织子文件夹如 `agents/review/`、`agents/research/`
- 子文件夹路径不影响子代理身份标识，身份仅由 `name` frontmatter 决定

### B.5 工具权限控制

子代理的工具控制通过 `tools` 字段实现：

| 配置 | 效果 |
|------|------|
| `tools: ""` | 继承主会话全部工具（默认） |
| `tools: "Read, Grep"` | 显式白名单 |
| `tools: "!Write"` | 黑名单排除（禁止写入） |

支持 `@path限制` 语法约束工具操作范围。

### B.6 持久记忆（Memory）

子代理可配置持久记忆目录，累积跨会话洞察：

| 配置 | 存储位置 | 范围 |
|------|---------|------|
| `memory: user` | `~/.claude/agent-memory/` | 所有项目 |
| `memory: project` | `.claude/agent-memory/` | 当前项目 |
| `memory: none` | 不启用 | - |

### B.7 Hooks与Skills集成

子代理可配置独立的Hooks和Skills：

```yaml
---
name: ci-helper
description: CI pipeline troubleshooting and fix
tools: Read, Grep, Glob, Bash
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "npx prettier --write"
skills:
  - ci-workflows
  - error-patterns
---
```

### B.8 子代理设计原则

1. **单一职责**：每个子代理只处理一类明确任务
2. **独立上下文**：子代理在自己的上下文中运行，不污染主对话
3. **明确Spec**：
   - 输入字段格式
   - 输出格式（JSON / Markdown / 纯文本）
   - 错误返回结构：`{"error": "描述"}`
   - 超时策略与重试阈值
4. **短时任务优先**：子代理适合短时、明确输入输出的工作；主代理负责统筹与复杂逻辑
5. **模型路由优化**：读操作用Haiku（低成本快响应），写操作用Sonnet/Opus（高质量）

---

## C. 多Agent协作（Agent Teams）

### C.1 核心概念

Agent Teams是**实验性功能**（默认禁用），允许多个Claude Code实例协同工作。一个会话作为**Team Lead**，协调工作、分配任务、合成结果。队友独立工作（各有独立上下文窗口），彼此**直接通信**。

**启用方式**：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### C.2 Leader-Teammate 架构

```
                     +------------------+
                     |   Team Lead       |
                     |  (协调/分配/合成)  |
                     +--+-------+-------+
                        |       |       |
               +--------v+ +---v---+ +--v------+
               |Teammate1| |Tmate2 | |Teammate3 |
               | (UX分析) | |(技术)  | |(Devil's  |
               |          | |       | | Advocate)|
               +----------+ +-------+ +----------+
                        |       |       |
                        +---+---+-------+
                            |
                     +------v-------+
                     | 共享任务列表   |
                     | (文件锁竞争)   |
                     +--------------+
```

### C.3 共享任务列表与文件锁

任务状态：
- **pending**（待处理）
- **in progress**（进行中）
- **completed**（已完成）

任务可设置依赖关系：有未解决依赖的pending任务无法被认领。

**文件锁机制**：多个队友同时认领同一任务时，文件锁确保只有一个成功，防止竞态条件。

### C.4 直接通信

与子代理不同，Agent Teams中的队友可以**直接互相通信**，而非仅向主代理报告。

```
子代理通信拓扑（Star）：所有通信经过主代理
Agent Teams通信拓扑（Mesh）：队友之间可直接消息传递
```

### C.5 显示模式

| 模式 | 说明 |
|------|------|
| **in-process** | 所有队友在主终端内运行，Shift+Down循环切换队友 |
| **split panes** | 每个队友独立分屏，需要tmux或iTerm2 |

默认 `"auto"`：已在tmux会话或iTerm2中用split panes，否则用in-process。

```json
{
  "teammateMode": "in-process"
}
```

### C.6 质量门 Hooks

| Hook事件 | 触发时机 | 用途 |
|---------|---------|------|
| `TeammateIdle` | 队友即将空闲 | Exit code 2 发送反馈让队友继续工作 |
| `TaskCreated` | 任务创建时 | 验证任务完整性，Exit code 2 拒绝 |
| `TaskCompleted` | 任务完成时 | 运行验证检查 |

### C.7 适用场景与不适用场景

| 适用场景 | 不适用场景 |
|---------|-----------|
| **研究审查**：多队友从不同角度同时研究 | **顺序任务**：依赖链不适合并行 |
| **新模块/功能开发**：队友各负责独立模块 | **同文件编辑**：竞态冲突风险 |
| **竞争假设调试**：多队友并行测试不同理论 | **高依赖工作**：需要大量协调 |
| **跨层协调**：前端+后端+测试各由不同队友负责 | **简单任务**：协调开销 > 收益 |

### C.8 行业最佳实践案例

**案例1：研究审查**
```
"I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Spawn three teammates to explore this from different angles:
one on UX, one on technical architecture, one playing devil's advocate."
```

**案例2：多模块并行重构**
```
"Spawn 4 teammates to refactor these modules in parallel. Use Sonnet for
each teammate."
```

**案例3：Plan审批流程**
```
"Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes."
```

### C.9 子代理 vs Agent Teams 决策矩阵

| 决策因素 | 选子代理 | 选Agent Teams |
|---------|:------:|:-----------:|
| 任务可完全独立执行 | ✓ | ✓ |
| 需要队友间直接通信 | ✗ | ✓ |
| 需要共享发现、互相质疑 | ✗ | ✓ |
| 仅需结果返回主代理 | ✓ | ✗ |
| Token预算有限 | ✓ | ✗ |
| 实验性功能不可用 | ✓ | ✗ |
| 需要跨会话持久化 | ✗ | ✓（后台代理） |
| 单会话内快速委派 | ✓ | ✗ |
| 需要直接与每个worker交互 | ✗ | ✓ |

---

## D. Claude Code最佳实践

### D.1 上下文窗口管理（核心约束）

> **最重要的约束**：Claude的上下文窗口保存整个对话——每条消息、每个文件、每个命令输出。LLM性能随上下文填充而下降，快满时Claude会开始"遗忘"早期指令或犯错。

**管理策略**：

| 策略 | 实现方式 |
|------|---------|
| **分拆任务** | 大任务拆分为多个独立会话或子代理 |
| **子代理隔离** | 探索、研究等副任务委派给子代理，仅返回摘要 |
| **上下文监控** | 自定义状态栏（`/statusline`）跟踪上下文使用量 |
| **压缩后重注入** | SessionStart hook + compact matcher 在压缩后重新注入关键上下文 |
| **减少Token使用** | 使用Haiku做探索、压缩输出、精简CLAUDE.md |

### D.2 验证闭环

> 给Claude一个可以运行的检查：测试、构建、截图对比。这是"看着它做"和"放手让它做"的区别。

**四层验证策略**：

| 层级 | 方式 | 说明 |
|:---:|------|------|
| 1 | **同一Prompt** | 在同一消息中要求Claude运行检查并迭代 |
| 2 | **/goal 条件** | 独立评估器每轮后重新检查，直到条件满足 |
| 3 | **Stop Hook** | 确定性脚本门控，阻断Turn结束直到检查通过（最多8次连续阻断） |
| 4 | **验证子代理** | 用新鲜模型尝试反驳结果，做检查的Agent不做打分 |

**Prompt对比示例**：

| Before | After |
|--------|-------|
| "implement a function that validates email addresses" | "write a validateEmail function. example test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing" |
| "make the dashboard look better" | "[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them" |
| "the build is failing" | "the build fails with this error: [paste error]. fix it and verify the build succeeds. address the root cause, don't suppress the error" |

### D.3 探索→规划→编码→提交 四阶段工作流

```
Phase 1: Explore（探索）
+-------------------------------------------------------------------+
| Plan模式，只读。阅读文件和回答问题，不做修改。                       |
| 示例："read /src/auth and understand how we handle sessions and    |
| login. also look at how we manage environment variables."          |
+-------------------------------------------------------------------+
                              |
                              v
Phase 2: Plan（规划）
+-------------------------------------------------------------------+
| 要求Claude创建详细的实现计划。                                      |
| 示例："I want to add Google OAuth. What files need to change?      |
| What's the session flow? Create a plan."                           |
| 按 Ctrl+G 在文本编辑器中打开计划直接编辑。                           |
+-------------------------------------------------------------------+
                              |
                              v
Phase 3: Implement（实现）
+-------------------------------------------------------------------+
| 退出Plan模式，让Claude编码并对照计划验证。                           |
| 示例："implement the OAuth flow from your plan. write tests for    |
| the callback handler, run the test suite and fix any failures."    |
+-------------------------------------------------------------------+
                              |
                              v
Phase 4: Commit（提交）
+-------------------------------------------------------------------+
| 提交并创建PR。                                                     |
| 示例："commit with a descriptive message and open a PR"            |
+-------------------------------------------------------------------+
```

**何时跳过Plan模式**：范围明确的小修改（改typo、加日志、重命名变量）直接执行。如果修改能用一句话描述diff，跳过计划。

### D.4 精准Prompt技巧

| 策略 | Before | After |
|------|--------|-------|
| **限定范围** | "add tests for foo.py" | "write a test for foo.py covering the edge case where the user is logged out. avoid mocks." |
| **指向源码** | "why does ExecutionFactory have such a weird api?" | "look through ExecutionFactory's git history and summarize how its api came to be" |
| **参考已有模式** | "add a calendar widget" | "look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget" |
| **描述症状** | "fix the login bug" | "users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it" |

### D.5 提供富内容

| 方式 | 说明 |
|------|------|
| `@` 引用文件 | 直接引用文件路径，Claude在响应前读取 |
| 粘贴图片 | 直接复制粘贴或拖放图片到提示中 |
| URL引用 | 给文档和API参考链接 |
| 管道输入 | `cat error.log \| claude` 直接发送文件内容 |
| 让Claude自行获取 | 告诉Claude使用Bash命令、MCP工具或读文件自行拉取上下文 |

### D.6 CLI工具集成

Claude Code原生支持通过CLI工具与外部服务交互：

| 工具 | 用途 |
|------|------|
| `gh` | GitHub：创建Issue、开PR、读取评论 |
| `aws` | AWS CLI：云资源管理 |
| `gcloud` | Google Cloud：云服务操作 |
| `sentry-cli` | Sentry：错误追踪和监控 |

未预装CLI工具时：`"Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C."`

### D.7 CLAUDE.md 编写规范

**CLAUDE.md**是特殊文件，Claude在每个会话启动时读取。包含Bash命令、代码风格和工作流规则。

**Include / Exclude 对照表**：

| Include | Exclude |
|---------|---------|
| Claude无法推断的Bash命令 | 读代码就能知道的内容 |
| 与默认不同的代码风格规则 | 标准语言约定（Claude已知） |
| 测试指令和首选测试运行器 | 详细的API文档（链接文档即可） |
| 仓库规范（分支命名、PR约定） | 频繁变化的信息 |
| 项目特定的架构决策 | 长篇解释或教程 |
| 开发环境特殊要求（必需环境变量） | 代码库的文件级描述 |
| 常见陷阱和非明显行为 | 自我证明的实践（如"写干净的代码"） |

**放置位置**：

| 位置 | 作用域 |
|------|--------|
| `~/.claude/CLAUDE.md` | 所有Claude会话 |
| `./CLAUDE.md` | 项目根（纳入Git共享） |
| `./CLAUDE.local.md` | 个人项目笔记（.gitignore） |
| 父目录 | Monorepo自动拉取 |
| 子目录 | Claude读取该目录文件时按需拉取 |

**导入语法**：`@path/to/import`

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

**编写原则**：
- 保持简洁：每行自问"删除这行会导致Claude犯错吗？"不过则删
- 持续迭代：把它当代码维护——出问题时审查、定期修剪、测试变更
- 添加强调词（如"IMPORTANT"、"YOU MUST"）提高遵循度
- 纳入Git版本控制，让团队贡献，文件价值随时间复利增长

---

## E. Skills系统

### E.1 SKILL.md 文件结构

Skills通过 `.claude/skills/` 目录中的 `SKILL.md` 文件定义。支持YAML前置元数据 + Markdown正文。

**基础结构**：
```markdown
---
name: api-conventions
description: REST API design conventions for our services
---

# API Conventions

- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

### E.2 条件加载 vs 手动触发

**条件加载**（默认）：Claude在需要时自动加载匹配的Skill。

```yaml
---
name: api-conventions
description: REST API design conventions for our services
---
```

**手动触发**（带副作用的可重复工作流）：

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

触发方式：`/fix-issue 1234`

`disable-model-invocation: true` 用于有副作用的工作流，确保只有用户手动触发时才执行，Claude不会自动调用。

### E.3 Skills vs Hooks 决策指南

| 决策因素 | Skills | Hooks |
|---------|:------:|:-----:|
| 需要LLM推理判断 | ✓ | ✗ |
| 每次都必须执行，零例外 | ✗ | ✓ |
| 按需加载，避免占满上下文 | ✓ | ✗ |
| 确定性操作（格式化/通知/文件保护） | ✗ | ✓ |
| 提供领域知识和指令 | ✓ | ✗ |
| 需要跨会话复用 | ✓ | 部分 |

### E.4 实际Skills示例

#### api-conventions（条件加载，领域知识型）

```markdown
---
name: api-conventions
description: REST API design conventions for our services
---

# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

#### fix-issue（手动触发，工作流型）

```markdown
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

#### codebase-explorer（条件加载，工具型）

Skills也可包含可执行脚本，放在与 `SKILL.md` 同目录下。例如一个 codebase 树状图可视化工具，Claude在需要了解项目结构时自动加载。

---

## F. Hooks自动化

### F.1 Hook事件

Hooks是用户定义的Shell命令，在Claude Code生命周期的特定节点执行，提供**确定性控制**——确保某些动作始终发生，而非依赖LLM选择执行。

**四大核心事件**：

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `Notification` | Claude等待输入或权限时 | 桌面通知 |
| `PostToolUse` | 工具执行后 | 自动格式化、验证 |
| `PreToolUse` | 工具执行前 | 文件保护、命令拦截 |
| `SessionStart` | 会话开始时 | 上下文重注入 |

### F.2 桌面通知配置

**macOS**：
```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

**Linux**：
```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
      }]
    }]
  }
}
```

**Windows (PowerShell)**：
```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
      }]
    }]
  }
}
```

**Notification matcher 精确过滤**：

| Matcher | 触发条件 |
|---------|---------|
| `permission_prompt` | Claude需要批准工具使用 |
| `idle_prompt` | Claude完成工作等待下一指令 |
| `auth_success` | 认证完成 |
| `elicitation_dialog` | MCP服务器打开引出表单 |
| `elicitation_complete` | MCP引出表单提交或取消 |
| `elicitation_response` | MCP引出响应发回服务器 |
| `""`（空） | 所有通知类型 |

### F.3 自动格式化（PostToolUse）

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
      }]
    }]
  }
}
```

### F.4 文件保护（PreToolUse）

创建保护脚本 `.claude/hooks/protect-files.sh`：

```bash
#!/bin/bash
# protect-files.sh

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done

exit 0
```

注册Hook：
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
      }]
    }]
  }
}
```

### F.5 上下文重注入（SessionStart + compact）

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{
        "type": "command",
        "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
      }]
    }]
  }
}
```

可以替换为动态命令，如 `git log --oneline -5` 显示最近提交。

### F.6 三类Hook对比

| 类型 | 机制 | 适用场景 |
|------|------|---------|
| **确定性规则** | Shell命令，Exit code 控制 | 每次必须执行，零例外 |
| **Prompt-based Hooks** | LLM评估条件后决定执行 | 需要判断但可离线决策 |
| **Agent-based Hooks** | Agent评估复杂条件 | 需要深度推理的决策 |

### F.7 Hooks完整生命周期

```
SessionStart → [用户输入] →
  PreToolUse → ToolExecution → PostToolUse → ...
  (循环直到完成) →
Notification（等待输入/权限）
```

### F.8 Hooks配置位置

Hooks通过 `.claude/settings.json` 或 `~/.claude/settings.json` 配置。使用 `/hooks` 命令浏览已注册的hooks。每个事件类型是 `hooks` 对象中的一个键。

---

## G. Agent SDK

### G.1 Agent Loop 五阶段

Agent SDK的核心是Agent Loop——自主循环运行推理、工具选择、执行、观察、重复直到目标达成。

```
+----------------------------------------------------+
|                   Agent Loop                        |
|                                                     |
|  +--------+    +-------------+    +--------+        |
|  | Reason |--->| Select Tool |--->| Execute|        |
|  +--------+    +-------------+    +--------+        |
|       ^                                |            |
|       |                                |            |
|       +-------- Observe <-------------+            |
|                        |                            |
|                        v                            |
|                 Goal Complete?                      |
|                  /         \                        |
|                YES          NO                      |
|                 |            |                      |
|               退出       继续循环                    |
+----------------------------------------------------+
```

### G.2 query() 函数

```python
# Python SDK 基本用法
from claude_agent_sdk import ClaudeSDKClient

client = ClaudeSDKClient()

async for message in client.query("请分析这个项目的代码结构"):
    if message.is_tool_use():
        print(f"Tool call: {message.tool_name}")
    elif message.is_final():
        print(f"Final result: {message.content}")
```

`query()` 创建新会话 → 发送第一条用户消息 → 流式返回助手消息 → 当Claude请求时执行工具调用 → 返回最终结果。

ResultMessage 字段包含 token count、cost、model choice 和 task usage metrics。

### G.3 会话持久化

```python
# 创建持久化会话
session = client.create_session(session_id="my-session-001")

# 后续调用使用同一会话
async for message in session.query("继续上一个任务"):
    ...
```

### G.4 工具权限配置

```python
client = ClaudeSDKClient(
    allowed_tools=["Read", "Write", "Edit", "Bash"],
    disallowed_tools=["WebSearch"]
)
```

内置工具集：Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, NotebookEdit, Monitor, Task管理工具, MCP资源工具。

### G.5 子代理架构在SDK中的应用

SDK原生支持子代理架构，Lead Agent可将专业任务委派给独立的子代理：

```python
client = ClaudeSDKClient(
    agents=[
        {
            "name": "code-reviewer",
            "description": "Reviews code for quality and security",
            "tools": "Read, Grep, Glob",
            "model": "sonnet"
        }
    ]
)
```

子代理在隔离的上下文中运行，协调并行工作流，防止上下文污染。

### G.6 SystemPromptPreset vs 自定义System Prompt

```python
# 使用预设
client = ClaudeSDKClient(
    system_prompt_preset="claude_code"  # 默认预设
)

# 完全自定义
client = ClaudeSDKClient(
    system_prompt="You are a specialized code analyzer..."
)
```

SDK加载项目设置、附加指令、环境变量和发现的Skills定义。自定义System Prompt可能跳过Claude Code通常注入的动态文件系统上下文。

### G.7 ThinkingConfig和EffortLevel

```python
client = ClaudeSDKClient(
    thinking_config={
        "effort_level": "high",
        "budget_tokens": 16000
    }
)
```

EffortLevel控制推理深度、延迟和成本：

| 级别 | 说明 | 适用场景 |
|------|------|---------|
| **low** | 快速响应 | 简单问题、查找、格式化 |
| **medium** | 平衡推理 | 默认选择，大多数开发任务 |
| **high** | 深度推理 | 复杂分析、架构设计、多步规划 |

---

## H. MCP协议

### H.1 三原语（Core Primitives）

MCP（Model Context Protocol）的核心是三个原语：

```
+----------------------------------------------------+
|                  MCP Server                          |
|                                                      |
|  +-------------+  +-------------+  +-------------+  |
|  |    Tools    |  |  Resources  |  |   Prompts   |  |
|  |   (操作)     |  |   (数据)     |  |   (模板)     |  |
|  +------+------+  +------+------+  +------+------+  |
|         |                |                |           |
+---------+----------------+----------------+---------+
          |                |                |
     +----v----------------v----------------v--------+
     |              MCP Client                        |
     |      (Claude / Cursor / Agent Runtime)         |
     +------------------------------------------------+
```

| 原语 | 用途 | 示例 |
|------|------|------|
| **Tools** | 模型可调用的操作 | `get_weather`、`search_database`、`create_issue` |
| **Resources** | 暴露数据供模型读取 | 文件内容、数据库记录、API响应 |
| **Prompts** | 预定义提示模板 | 代码审查模板、翻译指令、格式化指南 |

### H.2 MCP服务器与客户端构建

**服务器端（Python）**：

```python
from mcp import Server, Tool

server = Server("my-service")

@server.tool()
def search_docs(query: str) -> str:
    """Search documentation for the given query."""
    results = doc_index.search(query)
    return format_results(results)

server.run()
```

**客户端连接**：

```bash
claude mcp add my-service -- python my_server.py
```

### H.3 高级主题

| 主题 | 说明 |
|------|------|
| **Sampling** | 服务器可请求客户端LLM进行采样（反向调用） |
| **Notifications** | 服务器主动推送更新通知客户端 |
| **Transport** | stdio / HTTP+SSE 两种传输机制 |
| **File System Access** | 安全暴露文件系统访问能力 |
| **Elicitation** | 交互式表单/确认流程 |

### H.4 生产部署模式

三种部署模式：

1. **Stdio Transport**：本地进程通信（开发/单机环境）
2. **HTTP+SSE Transport**：远程服务器连接（生产/分布式环境）
3. **混合模式**：本地工具 + 远程资源组合

### H.5 连接Claude到外部服务的实战模式

| 服务 | MCP集成模式 |
|------|-----------|
| **GitHub** | Issues/PRs/代码搜索、项目管理 |
| **Notion** | 文档读写、知识库管理 |
| **Figma** | 设计稿读取、UI对比验证 |
| **数据库** | SQL查询、数据分析、Schema管理 |
| **监控系统** | 日志分析、告警查询、性能追踪 |
| **文件系统** | 安全文件读写、项目上下文提供 |

### H.6 MCP生态现状

MCP在2026年已成为跨Claude、Cursor和大多数Agent运行时的**通用语言**（lingua franca）。MCP课程由DeepLearning.AI与Anthropic联合出品，约1.5小时，免费，是提示工程入门教程后的标准下一步。

---

## 附录A：Agent系统设计五大模式（Building Effective Agents）

**核心哲学**：成功的Agent实现不使用复杂框架或专用库，而是采用简单、可组合的模式。严格区分 **Workflows**（预定义代码路径编排）和 **Agents**（LLM动态自主决策）。

### 三大核心原则

| # | 原则 | 说明 |
|---|------|------|
| 1 | **Simplicity（简单设计优先）** | 从单次LLM调用开始，只在必要时增加复杂度 |
| 2 | **Transparency（显式规划步骤）** | 显式展示Agent规划步骤，人类可理解、可审计 |
| 3 | **ACI（Agent-Computer Interface）** | 精心设计工具文档和测试，通过MCP集成第三方工具生态 |

### 五工作流模式

```
模式1：Prompt Chaining（提示链）
输入 -> [LLM步骤1] -> Gate（门控） -> [LLM步骤2] -> Gate -> ... -> 输出
适用：任务可清晰分解为固定子步骤

模式2：Routing（路由分发）
输入 -> [分类器] -> 路由A/B/C -> [专用处理模块] -> 输出
适用：不同类别输入需不同处理逻辑

模式3：Parallelization（并行化）
输入 -> 分发器 -> [Section A] [Section B] [Voting C] -> 聚合器 -> 输出
适用：可独立并行处理的子任务或需多视角验证

模式4：Orchestrator-Workers（编排器-工作者）
输入 -> [Orchestrator] -> 动态分解 -> [W1] [W2] [W3]... -> 合成 -> 输出
适用：无法预知子任务数量和内容

模式5：Evaluator-Optimizer（评估器-优化器）
输入 -> [Generator] -> [Evaluator] -> 反馈循环 -> 优化输出
适用：有明确评估标准且迭代能带来可衡量提升
```

---

## 附录B：能力成熟度模型

### Anthropic官方推荐的能力进阶路径

```
Level 1: AI Fluency（AI流利度）
  +-- 理解AI能力边界，负责任使用

Level 2: Claude日常使用（Claude 101 / Cowork）
  +-- 工作流集成，文件操作，多步引导

Level 3: Claude Code开发（Code 101 / Code in Action）
  +-- 终端代理，四阶段开发工作流

Level 4: API与MCP（Building with API / MCP入门）
  +-- 编程调用，构建MCP服务器和客户端

Level 5: 高级Agent（MCP进阶 / Subagents / Agent Skills）
  +-- 多Agent系统，上下文隔离，专业工作流

Level 6: 企业部署（Cloud Platform / CCA认证）
  +-- 云平台对接，生产部署，组织级管理
```

### 四件套能力矩阵

| 组件 | 目的 | 部署位置 | 触发方式 |
|------|------|---------|---------|
| **CLAUDE.md** | 持久化项目上下文 | 项目根 | 每次会话自动加载 |
| **Skills** | 领域知识+可复用工作流 | `.claude/skills/` | 按需/手动触发 |
| **Hooks** | 确定性自动化 | `.claude/settings.json` | 生命周期事件触发 |
| **Sub-agents** | 上下文隔离+任务委派 | `.claude/agents/` | 主Agent按需委派 |
| **MCP Servers** | 外部服务连接 | 本地/远程 | 工具调用 |

---

## 附录C：权限模式三种方案

| 模式 | 机制 | 最佳场景 |
|------|------|---------|
| **Auto模式** | 独立分类器模型审查命令，仅阻止高风险操作（作用域升级/未知基础设施/恶意内容驱动） | 信任任务方向但不想逐步点击 |
| **权限白名单** | 通过 `/permissions` 允许列表特定安全工具（如 `npm run lint`、`git commit`） | 已知安全的重复操作 |
| **沙箱** | OS级隔离，限制文件系统和网络访问，Claude在定义边界内自由工作 | 不可信代码执行或探索性任务 |

---

> **R54 全域知识库重构** | 2026-06-17 | 基于Anthropic官方文档（docs.anthropic.com / code.claude.com / skilljar.com）完整重构 | 覆盖8大核心模块+3个附录 | 下次同步：跟随Anthropic 2026 H2新课程/文档发布

---

## 附录D：Anthropic 2026 多Agent系统演进前瞻 (R55 · 2026-06-18)

> 来源：Anthropic官方工程博客 + 行业多Agent系统最佳实践综合研究

### D.1 Conductor-Specialist 架构（模块化单体）

2026年多Agent系统的核心范式从"上帝Agent"转向 **Conductor-Specialist架构**：

```
用户需求 → Conductor（Orchestrator，Opus级高推理）
                │  不写代码，仅负责任务分解和分配
    ┌───────────┼───────────┐
    ▼           ▼           ▼
Frontend    Backend     QA Agent
Agent       Agent       (Haiku，低成本)
(Sonnet)    (Sonnet)
    │           │           │
仅触碰UI组件  仅触碰API/DB   仅运行测试
```

**关键设计原则**：
- Specialist Agent 严格限定文件操作范围（目录级隔离）
- Conductor 输出结构化 tickets，而非自然语言模糊描述
- 每个 Specialist 使用 `.gitignore` 逻辑或文件锁提示强制执行边界

### D.2 上下文窗口"滑动窗口"策略

| 策略 | 实现 |
|------|------|
| **结构化摘要交接** | Agent A → Agent B 传递结构化摘要（任务名/状态/依赖/函数签名/测试结果），而非原始代码/日志 |
| **RAG 知识图谱集成** | Agent 连接持久化向量数据库（Knowledge Graph），按需检索参考文档而非全部加载到上下文 |
| **反上下文中毒** | 避免向Agent喂入 500K+ token 无关历史——每轮交接必须压缩 |

**错误 vs 正确交接示例**：

| 错误 | 正确 |
|------|------|
| "这是我写的500行代码..." | "Task: Auth Module. Status: Complete. Dependencies: Postgres, Bcrypt. Function Signatures: `create_user()`, `verify_user()`. Tests: Passing." |

### D.3 Message Bus 模式（Agent间通信标准化）

不使用自然语言做 Agent-to-Agent 通信（噪声过大），改用结构化输出：

```json
{"agent_id": "backend", "task_id": "123", "status": "blocked", "reason": "Missing API key in .env"}
```

**Shared Blackboard 模式**：使用共享文件（`TASKS.md` 或数据库）作为"真实源"——Agent 从 Blackboard 读取待办任务，而非等待 Conductor 分配。

### D.4 三击法则（3-Strike Rule）

Agent 失败处理的核心弹性机制：
- Agent 修复编译错误/测试失败尝试 **最多3次**
- 3次后必须停止 → 升级到 Conductor 或 "Senior Developer" Agent
- 无限调试循环是多Agent系统的 #1 成本黑洞

### D.5 快照回滚机制

Agent 执行高风险操作（重构）前：
1. 系统自动拍摄快照（commit hash 或 checkpoint）
2. 若 Agent 方案引入的 bug > 修复的 bug → 自动回滚
3. 与 3-Strike Rule 组合形成安全的失败边界

### D.6 对抗性审查（Adversarial Review）

不再信任 Agent 自己写的代码，"自我修正"被"对抗审查"取代：

```
Coder Agent 写代码 → Red Team Agent 专门审查安全漏洞（SQL注入/XSS/Prompt注入）
Architect Agent 出方案 → Devil's Advocate Agent 专门寻找方案缺陷
```

### D.7 Docker 沙盒隔离（Agent as Service）

每个 Sub-agent 任务：
1. 启动全新 Docker 容器
2. 仅授予该任务所需的最小权限
3. 任务完成后立即销毁容器
4. 防止幻觉临时文件和冲突环境变量残留

### D.8 MCP 2.0 预测方向

| 维度 | 当前 (MCP 1.x) | 预测方向 (2026 H2+) |
|------|---------------|-------------------|
| **操作方向** | 偏读取（拉取数据） | **双向 Action MCP**：Agent 可通过签名提示执行操作（创建 Jira ticket、预订会议、部署到 AWS） |
| **服务发现** | 手动配置 | **动态 MCP 发现**：Agent 浏览"注册表"自动安装所需连接器 |
| **凭据管理** | 直接暴露 | **安全凭据保险库**：协议层处理 OAuth/API Keys，Agent 永远不接触原始密钥 |
| **触发方式** | 用户提示驱动 | **事件驱动**：Webhook/System Hook 自动触发 Agent（如新合同上传→Legal Agent 自动审阅） |

### D.9 跨Agent协商（Cross-Agent Negotiation）

两个独立 Claude Agent 通过 MCP 接口协商：
- "Buyer" Agent vs "Seller" Agent → 自动达成合同
- 需结构化谈判 Schema + HITL 审批门控

### D.10 Agent 可观测性

类比 Datadog 对服务器的监控，Agent 可观测性工具：
- 追踪 Agent 决策 token-by-token
- 解释 Agent 为什么做出某个决策
- 可视化多Agent系统整体 Token 消耗分布

### D.11 总结：2026 工作流全景

```
1. 输入：人类描述功能需求
2. Conductor：拆解为 5 个 tickets
3. Spawner：启动 5 个隔离 Docker 容器（每个 Agent 一个）
4. 执行：Agent 并行工作，从共享知识库（Vector DB）读取参考
5. 审查：Merge Agent 审查 Workers 生成的 PR
6. 清理：销毁容器，状态持久化到 Postgres/Vector DB
```

---

> **R55 演进前瞻补充** | 2026-06-18 | 基于 Anthropic 2026 多Agent系统工程实践 + 行业趋势综合研究 | 新增附录D（11项2026演进方向）
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5c88af2466d07566d86b2b33cd54a234
    ReservedCode1: 43797b2246fe877f017ef1ab3a1a5e2b05e3b76826f3fe8890c122309a793d63==
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5c88af2466d07566d86b2b33cd54a234
    ReservedCode2: 43797b2246fe877f017ef1ab3a1a5e2b05e3b76826f3fe8890c122309a793d63==
---


# Anthropic官方课程-390节全集 — v1.30 增量更新

> **版本**：v1.30（R98稳态 · 2026-06-18 定时循环）
> **来源**：5路web_search综合提炼（Anthropic Academy课程体系/多Agent架构/Claude Code四件套/Dynamic Workflows/Agent SDK & Managed Agents）
> **关联迭代**：R98 · 全域模板v3.100

---

## I. 多Agent架构深度解读（Orchestrator-Subagent模式）

### I.1 核心原则：单Agent优先

Anthropic官方核心结论：**单Agent能解决的场景，绝不盲目上多Agent**。仅在以下3类明确场景下，多Agent架构能带来可量化收益，其余场景的协调开销远超收益。

### I.2 三大适用场景

| 场景 | 核心痛点 | 解决方案 | 典型实例 |
|------|---------|---------|---------|
| **上下文保护** (Context Protection) | 上下文窗口有限，内容增加导致推理质量显著下降 | 子Agent独立上下文执行专项任务，结果摘要回传主Agent | 安全审查/文档撰写/定价建模各自独立子Agent |
| **专业化** (Specialization) | 通才模型在多领域切换上下文降低所有任务质量 | 每个子Agent配备专属system prompt + 限定工具集 | 安全审查员/文档撰写员/定价建模师 |
| **模型升级** (Model Upgrade) | 大部分工作简单但某些子任务极难 | 协调员用Haiku路由排序，昂贵Opus仅用于专家子Agent | Every公司：Haiku协调员+Opus写作子Agent |

### I.3 编排器-子Agent模式架构

```
Lead Agent (Orchestrator) → 规划/分配/综合
    ├── Subagent A (部署历史分析) → 独立上下文+限定工具
    ├── Subagent B (错误日志分析) → 独立上下文+限定工具
    ├── Subagent C (指标分析)       → 独立上下文+限定工具
    └── Subagent D (支持工单分析)   → 独立上下文+限定工具
```

### I.4 四种生产级编排模式

| 模式 | 适用场景 | 延迟特征 | 主要失败模式 |
|------|---------|---------|------------|
| **Parallel Fan-Out** | 独立子任务+共享截止时间 | 受最慢节点限制 | 任务粒度不够细导致统一瓶颈 |
| **Sequential Review Chains** | Reviewer与Producer需要不同视角 | 串行累加 | 审查循环过度迭代 |
| **Adversarial Dual-Analysis** | 证据模糊的诊断问题 | 双路并行后合并 | 对抗方过于激进 |
| **Hierarchical Planner-Executor** | Planner分解→Executor执行→Synthesizer整合 | 三层串行 | Planner分解错误级联 |

### I.5 五大协调模式演进路径

Anthropic建议大多数场景从**Orchestrator-Subagent**开始，按需演进：
1. **Generator-Verifier** → 最简单的多Agent模式，生产部署最多
2. **Orchestrator-Subagent** → 最通用的起点，层级化架构
3. **Agent Teams** → 子任务需持续工作时，Worker持久化
4. **Message Bus** → Agent数量多、交互模式复杂时引入共享通信层
5. **Shared State** → 去中心化终极形态，共享存储协调

### I.6 关键设计原则

- **更少更精准的专家胜过许多模糊的专家**：如果两个角色重叠，合并它们
- **按角色混合模型层级**：协调员用快速廉价模型（Haiku），昂贵模型仅用于专家
- **严格限定每个专家的工具集**：安全审查员不给Write权限
- **写代码前先在纸上画团队草图**：协调员+一组每个只做一件明确工作的专家
- **Incident-Response参考模式**：主Agent调查，4个子Agent并行展开到不同数据源

---

## J. Claude Code四件套详解

### J.1 Skills（技能系统）

**核心机制**：SKILL.md文件 + YAML frontmatter配置 + Markdown指令体

| 特性 | 说明 |
|------|------|
| **位置** | Personal: `~/.claude/skills/` / Project: `.claude/skills/` / Plugin: `/skills/` |
| **自动检测** | 基于description语义匹配，Claude自动在相关任务时加载 |
| **动态上下文注入** | `!`前缀命令在加载前执行，结果注入SKILL.md |
| **Live Change Detection** | 文件变更实时生效，无需重启 |
| **嵌套发现** | 从启动目录到repo root的所有`.claude/skills/`自动发现 |
| **命名空间** | Plugin Skills使用`plugin-name:skill-name`格式 |
| **优先级** | Enterprise > Personal > Project |

**SKILL.md结构**：
```yaml
---
name: skill-name
description: When Claude should use this skill
disable-model-invocation: true/false
---
# Skill instructions (Markdown body)
```

### J.2 Hooks（事件钩子系统）

**完整生命周期事件（22个）**：

| 阶段 | 事件 | 触发时机 |
|------|------|---------|
| **会话** | SessionStart | 会话开始/恢复 |
| | Setup | `--init-only`或`--init`/`--maintenance`模式 |
| | SessionEnd | 会话终止 |
| **提示** | UserPromptSubmit | 用户提交提示前 |
| | UserPromptExpansion | 用户命令展开为提示时（可阻止） |
| **工具** | PreToolUse | 工具调用执行前（可阻止） |
| | PermissionRequest | 权限对话框出现时 |
| | PermissionDenied | 工具调用被auto模式拒绝时（可返回{retry:true}） |
| | PostToolUse | 工具调用成功后 |
| | PostToolUseFailure | 工具调用失败后 |
| | PostToolBatch | 并行工具批次完成后 |
| **Agent** | SubagentStart | 子Agent生成时 |
| | SubagentStop | 子Agent完成时 |
| | TaskCreated/TaskCompleted | 任务创建/完成时 |
| **上下文** | PreCompact | 上下文压缩前 |
| | PostCompact | 上下文压缩完成后 |
| | InstructionsLoaded | CLAUDE.md加载到上下文时 |
| | ConfigChange | 配置文件变更时 |
| | CwdChanged | 工作目录变更时 |
| | FileChanged | 监控文件变更时 |
| **其他** | Notification/Elicitation/ElicitationResult/Stop/StopFailure/TeammateIdle | 辅助事件 |

**Hook类型**：
- `command`：执行Shell命令或脚本
- `http`：POST JSON到URL
- `mcp_tool`：调用MCP Server工具
- `prompt`：LLM评估（使用`$ARGUMENTS`占位符）
- `agent`：运行Agentic验证器

### J.3 Subagents（子代理）

**Plugin Agent配置字段**：

| 字段 | 说明 |
|------|------|
| `name` | Agent标识符 |
| `description` | 描述，用于自动调用匹配 |
| `model` | 模型选择（sonnet/opus/haiku） |
| `effort` | 努力级别（low/medium/high） |
| `maxTurns` | 最大轮次限制 |
| `tools` | 允许的工具列表 |
| `disallowedTools` | 禁止的工具列表 |
| `skills` | 绑定的技能列表 |
| `memory` | 持久记忆配置 |
| `background` | 后台运行配置 |
| `isolation` | 隔离模式（唯一有效值：`"worktree"`） |

**安全约束**：Plugin agents不支持`hooks`/`mcpServers`/`permissionMode`。

### J.4 Plugins（插件系统）

**插件目录结构**：
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 插件清单（必须）
├── skills/                  # Agent Skills
│   └── skill-name/
│       └── SKILL.md
├── agents/                  # 自定义Agent定义
├── hooks/
│   └── hooks.json           # Hook事件处理器
├── .mcp.json                # MCP服务器配置
├── .lsp.json                # LSP服务器配置
└── settings.json            # 插件默认设置
```

**plugin.json字段**：name（唯一标识符+命名空间前缀）、description、version（SemVer）、author、homepage、repository、license。

**集成点**：Agents出现在`/agents`界面；Claude可基于任务上下文自动调用；用户可手动调用；Plugin agents与内置agents共存。

---

## K. Dynamic Workflows核心技术

### K.1 概述

Dynamic Workflows随**Claude Opus 4.8**（2026-05-28）发布，是目前处于研究预览阶段的动态工作流功能。核心能力：Claude根据具体任务自动编写**JavaScript编排脚本**，动态创建并调度数十至数百个并行子Agent协同工作，通过内建**对抗验证机制**确保结果质量。

### K.2 技术架构

```
用户Prompt → Claude生成JS编排脚本 → 脚本创建/协调子Agent
    ├── Subagent 1 (独立worktree) → 模型选择+上下文隔离
    ├── Subagent 2 (独立worktree) → ...
    ├── ... (可扩展到数百个)
    └── Subagent N → 对抗验证Agent证伪结果
    ↓
收敛结果 → 单一协调答案返回用户
```

### K.3 关键能力

| 能力 | 说明 |
|------|------|
| **动态编排脚本** | JS脚本替代对话上下文中的规划逻辑，支持大规模并行 |
| **百级并行** | 单Session数百并行子Agent |
| **模型分层** | 工作流可决定每个子Agent使用哪个模型 |
| **Worktree隔离** | 子Agent在独立worktree中运行 |
| **对抗验证** | 独立Agent从不同角度覆盖问题，其他Agent尝试证伪，持续迭代直至收敛 |
| **断点续传** | 可编排、可恢复的执行框架 |

### K.4 实战验证：Bun代码库迁移

- **任务**：75万行代码从Zig迁移至Rust
- **周期**：11天
- **结果**：通过99.8%现有测试
- **规模**：数百并行子Agent协同

### K.5 典型应用场景

| 场景 | 提示示例 |
|------|---------|
| **对抗性测试** | "这个测试可能每50次运行失败一次。设置工作流重复运行测试，形成假设并在worktree中对抗性验证" |
| **会话分析挖掘** | "回顾最近50次会话，挖掘反复犯的错误，生成CLAUDE.md规则" |
| **多角度拆解** | "拿我的商业计划，让不同Agent从投资者、客户和竞争对手角度拆解" |
| **批量排名** | "80份简历的文件夹，排名选出最佳候选，对前10名复核" |
| **代码审查** | "验证每一项技术声明是否符合代码库" |
| **大规模迁移** | "将User模型重命名为Account" |

### K.6 Opus 4.8核心提升

- **诚实性**：缺陷漏报降4倍，0%盲信错误结果，过度自信降10倍
- **编码**：ScienceQA登顶96.7%
- **速度**：Fast Mode 2.5×速度，成本降3倍
- **Agent能力**：Super-Agent benchmark唯一端到端完成所有用例的模型

---

## L. Agent SDK & Managed Agents双轨策略

### L.1 双轨定位

| 维度 | Agent SDK | Managed Agents |
|------|----------|---------------|
| **目标用户** | 平台构建者/基础设施团队 | 应用构建者/产品团队 |
| **托管方式** | 自托管 | Anthropic托管 |
| **状态持久化** | 开发者自行负责 | 内置（Sessions+Checkpointing） |
| **多Agent** | Subagent工具（内置） | 后续发布 |
| **核心哲学** | "给Claude一台电脑" | "分离指令与执行" |
| **定价** | API Token成本 | $0.08/session-hour + Token成本 |

### L.2 Agent SDK四层架构

```
应用层(Application) → 用户意图/任务定义/UI对接
    ↓
Agent层(Agent) → 规划/工具选择/对话管理
    ↓
运行时(Runtime) → 执行循环/重试/超时/熔断
    ↓
服务层(Service) → 模型API/工具实现/持久化
```

SDK并非API包装器，而是启动Claude Code CLI子进程，通过stdin/stdout JSON流协议通信。
- **TypeScript版**：`@anthropic-ai/claude-agent-sdk`（npm，闭源）
- **Python版**：`claude-agent-sdk`（PyPI，开源）

### L.3 Managed Agents三组件架构

```
Brain (Claude + Harness) → 决策路由
Hands (Disposable Linux Containers) → 代码执行（凭据从不进入沙箱）
Session (Durable Event Log) → 崩溃恢复的事件日志
```

**安全设计**：凭据从不进入沙箱。Git Token在初始化时注入并留在外部。OAuth Token存储在Vault中，通过Agent无法访问的代理获取。

**性能提升**：Brain立即开始推理，需要时启动容器 → 中位首Token时间降60%。

### L.4 Three-Agent Harness（生产验证模式）

```
Planner Agent → 结构和目标（结构化制品传递而非共享上下文）
    ↓
Generator Agent → 执行（5-15轮critique-and-refine循环）
    ↓
Evaluator Agent → 独立质量评估（消除自评通胀）
```

**关键洞察**：将评估分离为专用Agent消除了生成器对自身输出评分过高的问题。

### L.5 Managed Agents高级功能

| 功能 | 说明 |
|------|------|
| **Dreaming** | 跨会话记忆学习，会话间记住filetype workarounds/tool-specific patterns |
| **Outcomes** | 定义结果标准，Agent自行验证直到达标，无需人工审查每次尝试 |
| **Multiagent** | Lead Agent分解任务，子Agent并行执行，共享文件系统+持久事件记忆 |
| **Webhook通知** | Outcomes任务完成后webhook通知 |

**实测效果**：
- Outcomes：任务成功率+10个百分点（最难问题增益最大）
- 文件生成质量：docx +8.4%，pptx +10.1%
- Harvey法律团队：Dreaming使完成率提升约6倍
- 早期采用者：Notion/Rakuten/Sentry/Asana/Netflix

---

## M. 最佳实践提炼

### M.1 多Agent设计

1. **从单Agent开始**：先优化到极致，仅当遇到不可突破的硬约束时升级
2. **单Agent → Orchestrator-Subagent → Agent Teams**：按需渐进演进
3. **模型分层是最大杠杆**：协调员用Haiku（快/便宜），专家用Opus（贵/强）
4. **上下文隔离**：每个子Agent独立上下文，结果摘要回传
5. **Token成本意识**：多Agent系统Token消耗约为聊天对话的15倍

### M.2 Claude Code工程化

1. **Skills优先于CLAUDE.md**：Skills按需加载，长期参考资料零成本
2. **Hooks自动化质量门**：PostToolUse Hook自动格式化/检查
3. **Plugins团队标准化**：打包Skills+Agents+Hooks+MCP为可版本化、可市场分发的单元
4. **Subagent上下文分流**：大型任务拆分为子Agent独立上下文

### M.3 Dynamic Workflows使用决策

| 条件 | 是否使用Dynamic Workflows |
|------|--------------------------|
| 可高度并行化 | 是 |
| 需要对抗验证 | 是 |
| 大规模代码库操作（万行+） | 是 |
| 简单单文件任务 | 否（单Agent更高效） |
| 强串行依赖 | 否 |

### M.4 安全纵深防御

1. **凭据隔离**：凭据不入沙箱（Managed Agents模式）
2. **MCP安全**：OAuth 2.1 + 恶意检测扫描 + 凭证轮换
3. **权限最小化**：每个专家Agent只给必要工具
4. **审计追踪**：Managed Agents Console中完整事件日志

---

## N. 附录

### N.1 课程平台信息

- **平台**：Skilljar (anthropic.skilljar.com)
- **注册**：独立Skilljar账号（与claude.ai账号分离）
- **证书**：课程结业证书（区别于CCA Claude Certified Architect专业认证）
- **CCA认证**：2026-03-12宣布CCA Foundations，面向解决方案架构师与合作夥伴
- **课程入口**：anthropic.com/learn

### N.2 18门课程速查（2026-06-18完整列表）

| # | 课程名称 | 讲座数 | 视频时长 | 测验 | 类别 |
|---|---------|:---:|:---:|:---:|------|
| 1 | Claude 101 | - | ~1h | - | 入门 |
| 2 | Claude Code 101 | - | ~2h | - | 开发 |
| 3 | Claude Platform 101 | - | ~2h | - | 开发 |
| 4 | Introduction to Claude Cowork | - | ~2h | - | 协作 |
| 5 | Claude Code in Action | 15 | 1h | 1 | 开发 |
| 6 | AI Fluency: Framework & Foundations | - | ~2h | - | 素养 |
| 7 | Building with the Claude API | 84 | 8.1h | 10 | 开发 |
| 8 | Introduction to MCP | 16 | 1h | 1 | MCP |
| 9 | MCP: Advanced Topics | 15 | 1.1h | 2 | MCP |
| 10 | Introduction to Agent Skills | - | - | - | Agent |
| 11 | Introduction to Subagents | - | - | - | Agent |
| 12 | Claude with Amazon Bedrock | 85 | 8h | 10 | 云平台 |
| 13 | Claude with Google Vertex AI | 85 | 8h | 10 | 云平台 |
| 14 | AI Fluency for Educators | 5 | 30min | - | 教育 |
| 15 | AI Fluency for Students | 5 | 30min | - | 教育 |
| 16 | Teaching AI Fluency | 7 | 36min | 1 | 教育 |
| 17 | AI Fluency for Nonprofits | - | - | - | 公益 |
| 18 | AI Fluency for Small Businesses | - | - | - | 商业 |

### N.3 开发者完整学习路径

```
Claude Code 101 (2h)
    ↓
Claude Code in Action (1h)
    ↓
Building with the Claude API (8.1h, 84 lectures)
    ↓
Introduction to MCP (1h, 16 lectures)
    ↓
MCP: Advanced Topics (1.1h, 15 lectures)
    ↓
Introduction to Agent Skills
    ↓
Introduction to Subagents
    ↓
Claude with Amazon Bedrock / Google Vertex AI (各8h)
    ↓
→ CCA认证准备
```

---

## O. Claude Code 2026年6月重要更新（v2.1.169–v2.1.173）

> 来源：Claude Code Release Notes（releasebot.io） + code.claude.com/docs 官方文档
> 增量日期：2026-06-18

### O.1 版本更新时间线

| 版本 | 日期 | 核心变更 |
|------|------|---------|
| **2.1.173** | 2026-06-12 | 修复 Fable 5 模型名称规范化（移除 [1m] 后缀）、移除 Windows 沙箱启动警告 |
| **2.1.172** | 2026-06-11 | **嵌套子代理（Nested Sub-agents）正式支持**、智能模型与区域处理、新插件搜索、Chrome/VSCode/终端工作流优化 |
| **2.1.170** | 2026-06-09 | **Claude Fable 5 模型发布**、修复 VS Code 终端 transcript 保存 |
| **2.1.169** | 2026-06-09 | **Post-Session Hook 新增**、Safe Mode 故障排查模式 |

### O.2 嵌套子代理（Nested Sub-agents）— v2.1.172

**重大变更**：Claude Code 2.1.172 正式支持嵌套子代理。此前子代理不能派生新子代理（R89规则），现在**子代理可在其上下文中创建和委托给其他子代理**。

**使用规范**：
- 实际最多 2 层嵌套（编排器 → 工作者 → 子工作者）
- 每层子代理独立上下文窗口，各自拥有工具白名单和权限模式
- Plan Mode 下仍防止无限嵌套：Plan 子代理不能派生子代理
- 适用于复杂多步骤任务需要进一步分解的场景

**配置示例**：
```yaml
---
name: orchestrator
description: 分解复杂任务并委派给子工作者
tools: Read, Write, Edit, Bash, Agent
model: sonnet
permissionMode: acceptEdits
maxTurns: 50
---
```

**注意事项**：
- 嵌套增加 Token 消耗（每层 ~4K 系统提示 + CLAUDE.md）
- 仅在单层子代理无法满足需求时才使用嵌套
- 总并发 Agent 数不应超过 12 个

### O.3 Claude Fable 5 模型 — v2.1.170

**模型定位**：Mythos-class 模型，Anthropic 有史以来向公众开放的最强模型。Fable 5 默认包含 1M 上下文窗口。

**关键特性**：
- 能力超越此前所有公开可用的 Claude 模型
- 1M Token 上下文窗口（默认）
- 模型名称中的 [1m] 后缀在 v2.1.173 中自动规范化
- 通过 `claude --model fable-5` 或设置中指定使用

**版本要求**：Claude Code ≥ v2.1.170

### O.4 Post-Session Hook — v2.1.169

**全新 Hook 事件**：在现有 17 个生命周期事件基础上新增 **SessionEnd 后置钩子**，在会话完全结束（所有子代理完成、文件写入落盘）后触发。

**使用场景**：
- 会话结束后的通知推送（Slack/邮件）
- 自动生成会话摘要报告
- 清理临时文件和 Worktree
- 触发 CI/CD 后续流水线

**配置示例**：
```json
{
  "hooks": {
    "PostSession": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./hooks/session-summary.sh",
        "async": true
      }]
    }]
  }
}
```

与 SessionEnd Hook 的区别：
| Hook | 触发时机 | 用途 |
|------|---------|------|
| **SessionEnd** | 会话即将结束前 | 收尾操作、状态保存 |
| **PostSession** | 会话完全结束后 | 通知、报告、清理（新增） |

### O.5 Safe Mode — v2.1.169

新增安全故障排查模式，可在 Claude Code 启动时通过 `--safe` 标志进入，跳过所有自定义配置（CLAUDE.md、Skills、Hooks、MCP），仅保留内置基础功能，用于排查配置问题导致的异常。

### O.6 自定义子代理完整配置速查（基于官方文档 2026-06-18）

**YAML Frontmatter 完整字段**：

| 字段 | 类型 | 必需 | 说明 |
|------|------|:---:|------|
| `name` | string | ✅ | 小写+连字符唯一ID |
| `description` | string | ✅ | 触发条件描述 |
| `tools` | string[] | - | 工具白名单（支持 Agent(type) 语法） |
| `disallowedTools` | string[] | - | 工具黑名单 |
| `model` | string | - | sonnet / opus / haiku / fable-5 / inherit |
| `permissionMode` | string | - | plan / default / acceptEdits / auto / bypass |
| `skills` | string[] | - | 启动时预加载的技能列表 |
| `mcpServers` | object | - | 内联 MCP 服务器定义 |
| `hooks` | object | - | 限定于此代理的生命周期 hooks |
| `memory` | string | - | user / project / none |
| `background` | boolean | - | true 时始终后台运行 |
| `effort` | string | - | low / medium / high / xhigh / max |
| `isolation` | string | - | worktree 隔离模式 |
| `color` | string | - | UI 显示颜色 |
| `initialPrompt` | string | - | 主会话代理的首个自动提示 |
| `maxTurns` | int | - | 最大回合数限制 |

**五级存储位置优先级**：
1. Managed Settings (`managed-settings.d/`) — 企业不可覆盖
2. `--agents` CLI 标志 — 会话级临时定义
3. `.claude/agents/` — 项目级（Git 版本控制）
4. `~/.claude/agents/` — 用户级（跨项目共享）
5. Plugin `agents/` 目录 — 插件分发

### O.7 子代理内置类型更新

**8 种内置/可定义子代理完整矩阵（更新至 v2.1.172）**：

| 类型 | 模型 | 工具 | 权限 | maxTurns | 嵌套能力 |
|------|------|------|------|:---:|:---:|
| Explore | haiku | Read, Grep, Glob | plan | 15 | 否 |
| Plan | 继承主会话 | Read-only | plan | 20 | 否（防无限嵌套） |
| General-purpose | 继承主会话 | 所有工具 | acceptEdits | 40 | ✅（v2.1.172） |
| Code-reviewer | sonnet | Read, Grep, Glob | plan | 25 | 否 |
| Security-auditor | sonnet | Read, Grep, Glob | plan | 30 | 否 |
| Test-runner | haiku | Read, Bash, Grep | acceptEdits | 30 | 否 |
| Debugger | sonnet | Read, Bash, Grep, Glob | acceptEdits | 35 | ✅ |
| Refactor-assistant | sonnet | Read, Write, Edit, Bash | acceptEdits | 40 | ✅ |

---

> **END v1.31** | R99 增量迭代 | 2026-06-18 | 新增：嵌套子代理 / Fable 5 / Post-Session Hook / Safe Mode
