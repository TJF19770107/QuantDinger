---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_788e0f77685111f1a99c5254007bceed
    ReservedCode1: thwF5kmfGlS3P4oIXA3x6Xi/zwAd4QN9G7odZHAXWB1nj/eZbaLOaIP7d+5+nt1mIWHCyHYsyAOsYL2uowkglCAbzq3OtkLGvNgcFGg9IZJz4LVIT6eWchitfMfUzL28a5idtbCzRXXKUBaHTmlGsIUnRFhFtno0/thMyHwFLNzASfDR/D3uzUU2v/I=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_788e0f77685111f1a99c5254007bceed
    ReservedCode2: thwF5kmfGlS3P4oIXA3x6Xi/zwAd4QN9G7odZHAXWB1nj/eZbaLOaIP7d+5+nt1mIWHCyHYsyAOsYL2uowkglCAbzq3OtkLGvNgcFGg9IZJz4LVIT6eWchitfMfUzL28a5idtbCzRXXKUBaHTmlGsIUnRFhFtno0/thMyHwFLNzASfDR/D3uzUU2v/I=
---

# AGENTS.md — 子代理管理与自动化配置

> 基于 Anthropic 官方课程（Subagents / Agent Skills / Claude Code）提炼
> 更新：2026-06-16 第三轮循环

---

## 一、子代理目录结构

```
项目根目录/
├── CLAUDE.md                    # 主配置：定义所有子代理
├── .claude/
│   ├── subagents/               # 子代理定义
│   │   ├── code-reviewer.md     # 代码审查子代理
│   │   ├── doc-writer.md        # 文档撰写子代理
│   │   ├── test-generator.md    # 测试生成子代理
│   │   └── security-auditor.md  # 安全审计子代理
│   ├── skills/                  # Skills 技能库
│   │   ├── code-review/SKILL.md
│   │   ├── api-design/SKILL.md
│   │   └── doc-writer/SKILL.md
│   ├── hooks/                   # Hooks 事件处理
│   │   ├── pre-commit.md
│   │   ├── security-check.md
│   │   └── session-init.md
│   └── mcp/                     # MCP 服务配置
│       └── mcp-config.json
```

---

## 二、子代理配置规范

### CLAUDE.md 子代理定义
```markdown
## Subagents

### code-reviewer
- **Purpose**: Review code changes for quality, security, and best practices
- **Trigger**: When code is modified or PR is submitted
- **Context**: Full diff of changed files
- **Output**: Review report with severity levels (critical/high/medium/low)
- **Constraints**: Read-only access to codebase, no file modifications

### doc-writer
- **Purpose**: Generate and update project documentation
- **Trigger**: When new features are implemented or API changes occur
- **Context**: Source code and existing docs
- **Output**: Updated documentation in markdown format
- **Constraints**: Write access limited to docs/ directory

### test-generator
- **Purpose**: Generate unit and integration tests
- **Trigger**: When new code is written
- **Context**: Source code and test framework config
- **Output**: Test files in tests/ directory
- **Constraints**: Write access limited to tests/ directory
```

### 子代理规范模板

每个子代理定义文件应包含：

```markdown
# [子代理名称]

## 角色
[一句话描述子代理职责]

## 触发条件
[何时创建此子代理]

## 上下文范围
[子代理可访问的文件/目录/数据范围]

## 工具权限
| 工具 | 权限 | 说明 |
|------|------|------|
| read_file | ✅ 允许 | 读取源代码 |
| write_file | ❌ 禁止 | 不可修改文件 |
| shell_executor | ⚠️ 受限 | 仅测试命令 |

## 输出规范
[子代理输出格式与位置]

## 故障处理
[超时/异常/错误时的行为]
```

---

## 三、权限矩阵

### 三级权限模型

| 级别 | 能力 | 适用子代理 |
|------|------|-----------|
| Observer | 只读（read/search/list） | code-reviewer, security-auditor |
| Contributor | 限定写（指定目录） | doc-writer, test-generator |
| Operator | 全权（需人工确认） | 部署代理、迁移代理 |

### 权限继承规则
- 子代理权限 ≤ 主 Agent 权限
- 子代理不可请求提升权限
- 子代理不可修改自身权限配置
- MCP 工具权限需显式声明

### 危险操作清单（子代理禁止）

| 操作 | 原因 |
|------|------|
| 修改 CLAUDE.md | 防止自修改 |
| 删除 .claude/ 目录 | 防止破坏配置 |
| 修改 MCP 配置 | 防止权限提升 |
| 网络请求（未授权域） | 防止数据泄露 |
| 读取 .env / .ssh | 防止凭据窃取 |
| 执行系统级命令 | 防止宿主机入侵 |

---

## 四、Hooks 自动化配置

### 推荐 Hooks 清单

```markdown
## Hooks

### PreToolUse: Security Check
**事件**: 任何写入/删除操作前
**行为**: 验证路径白名单、检查文件类型
**失败**: 阻止操作 + 通知用户

### PostToolUse: Audit Log
**事件**: 任何工具调用后
**行为**: 记录（工具名、参数、结果、时间戳）
**输出**: .claude/audit.log

### OnSessionStart: Context Init
**事件**: 会话开始时
**行为**: 加载项目 CLAUDE.md、检查更新
**失败**: 降级为最小上下文模式

### OnError: Graceful Degradation
**事件**: 任何异常发生时
**行为**: 记录错误 → 尝试降级 → 通知用户
**降级策略**: 子代理失败 → 主 Agent 接管 / API 失败 → 本地缓存
```

---

## 五、团队规模模板

### Solo 开发者（1人）
```
主 Agent (Claude Code)
├── Skills: 2-5 个（代码审查、文档、测试）
├── Hooks: 2-3 个（安全、格式化、提交前检查）
├── Subagents: 0-1 个（大规模重构时临时创建）
└── MCP: 1-2 个（数据库、文件系统）
```

### 小团队（2-5人）
```
主 Agent (Claude Code + CI 集成)
├── Skills: 5-10 个（多领域覆盖）
├── Hooks: 5-8 个（代码审查、CI 集成、部署检查）
├── Subagents: 2-3 个（code-reviewer / test-generator / doc-writer）
└── MCP: 3-5 个（数据库、文件系统、CI/CD、通知、监控）
```

### 中大型组织（10+人）
```
Agent 编排层 (Claude API + 自建平台)
├── Skills: 20+ 个（企业级模板库）
├── Hooks: 完整治理框架
├── Subagents: 按领域划分（前端/后端/数据/安全/运维）
├── MCP: 全集成（所有内部系统）
└── 认证：Claude Certified Architect + 企业治理
```

---

## 六、MCP 最小化原则

### 仅注册必要服务
```json
// ❌ 错误：过度注册
{"mcpServers": {"everything": {...}}}

// ✅ 正确：按需注册
{"mcpServers": {
  "project-db": {"command": "..."},
  "project-fs": {"command": "..."}
}}
```

### MCP 安全规则
- 每个 MCP Server 独立进程运行
- 网络隔离：仅允许预定义端点
- 敏感数据脱敏后再传递给 Claude
- 定期轮换认证凭证

---

## 七、自动化派发规则

### 任务 → 子代理映射

| 任务类型 | 目标子代理 | 并行度 |
|---------|-----------|--------|
| 代码审查 | code-reviewer | 并行（按文件） |
| 文档更新 | doc-writer | 串行（避免冲突） |
| 测试生成 | test-generator | 并行（按模块） |
| 安全审计 | security-auditor | 串行（全量扫描） |
| 多语言翻译 | translator-N | 并行（按语言） |
| 数据迁移 | migration-agent | 串行（阶段依赖） |

### 派发决策算法
```
function dispatch(task):
    if task.type in PARALLEL_SAFE:
        create N subagents → parallel execute
    elif task.type has DEPENDENCIES:
        for each stage in dependency_order:
            create 1 subagent → execute → verify → next stage
    elif task.complexity <= SINGLE_FILE:
        handle directly（no subagent needed）
    else:
        create 1 subagent → execute → return result
```

---

> 管理哲学：子代理是工具，不是替代品。配置的目的不是让主 Agent 退位，而是让它在正确的层级上做正确的决策。
> 来源：Anthropic Academy Subagents/Agent Skills/Claude Code 课程 + 认证考试考试纲要
*（内容由AI生成，仅供参考）*

---

## 八、基于五种协调模式的派发决策优化（2026-06-15 第3轮更新）

> 来源：Anthropic 官方博客 Multi-agent coordination patterns (2026-04-10)

### 8.1 五种模式下的子代理配置差异

| 配置维度 | Orchestrator-Subagent | Agent Teams | Message Bus | Shared State |
|---------|----------------------|-------------|-------------|--------------|
| 子代理生命周期 | 单次任务→终止 | 跨多次任务存活 | 事件驱动存活 | 持续存活 |
| 上下文管理 | 每次重建 | 累积持久化 | 事件携带+自身 | 从存储自取 |
| 权限边界 | 编排器显式声明 | 队友自声明 | 订阅即权限 | 存储读写即权限 |
| 故障隔离 | 编排器不传播 | 队友间隔离 | 路由不传播 | 无隔离保障 |
| 发现机制 | 编排器预定义 | 协调器分配 | Pub/Sub 匹配 | 存储自检索 |
| 协调复杂度 | 低（集中式） | 中（队列式） | 高（事件式） | 最高（无协调） |

### 8.2 龙虾 dispatch_task 五模式扩展映射

```
dispatch_task 当前实现 → Orchestrator-Subagent (主要) + Agent Teams (继承模式)

扩展方向：
├── Generator-Verifier 模式
│   └── 派发验证子代理 + 反馈循环 + 最大迭代控制
│   └── 配置：verifier_agent + max_iterations + fallback_strategy
│
├── Agent Teams 增强
│   └── inherit_agent_id 实现队友持久化 + 任务队列认领
│   └── 配置：teammate_pool_size + task_queue + completion_signal
│
├── Message Bus（协议#251）
│   └── 事件发布/订阅 + Router 投递 + Agent 动态注册
│   └── 配置：event_topics + subscription_rules + router_config
│
└── Shared State（协议#247+#248）
    └── SQLite 持久化看板 + Agent 自检索 + 终止条件
    └── 配置：shared_store_path + termination_policy + write_conflict_resolution
```

### 8.3 按模式优化的自动化配置模板

#### Generator-Verifier 配置
```yaml
subagent:
  name: quality-verifier
  mode: generator-verifier
  max_iterations: 3
  fallback: escalate_to_user
  verify_criteria:
    - accuracy_check
    - tone_check
    - completeness_check
```

#### Agent Teams 配置
```yaml
team:
  name: migration-squad
  mode: agent-teams
  pool_size: 4
  task_queue: shared
  completion_signal: all_done
  conflict_resolution: locking
```

#### Message Bus 配置
```yaml
bus:
  name: event-bus
  mode: message-bus
  router: semantic_llm
  topics:
    - security.alerts
    - code.reviews
    - docs.updates
  agent_registry: dynamic
```

#### Shared State 配置
```yaml
shared_state:
  name: research-kb
  mode: shared-state
  store: sqlite
  termination:
    type: convergence
    threshold: 3_cycles_no_new_findings
  write_policy: append_only
  conflict: versioning
```

### 8.4 派发决策算法 v2.0（五种模式全覆盖）

```
function dispatch_v2(task):
    # 1. 质量验证模式判定
    if task.requires_quality_check AND has_explicit_criteria(task):
        return generator_verifier(task)

    # 2. 复杂度判定
    if task.complexity <= SINGLE_FILE:
        return handle_directly(task)

    # 3. 可分解性判定
    if has_clear_decomposition(task):
        if subtasks_short_and_independent(task):
            return orchestrator_subagent(task)  # 当前主线
        elif subtasks_benefit_from_context(task):
            return agent_teams(task)             # inherit_agent_id

    # 4. 松耦合生态判定
    if workflow_unpredictable(task) OR agent_ecosystem_growing(task):
        return message_bus(task)                 # 协议#251

    # 5. 协同构建判定
    if needs_mutual_discovery(task) OR eliminate_single_point(task):
        return shared_state(task)                # 协议#247+#248

    # 6. 兜底
    return orchestrator_subagent(task)
```

### 8.5 安全护栏：模式无关的通用约束

无论选择哪种协调模式，以下约束不可覆盖：

| 约束 | 所有模式强制 | 原因 |
|------|:---:|------|
| 子代理不可修改主配置 | ✅ | 防自修改攻击 |
| 子代理不可提升自身权限 | ✅ | 防权限蔓延 |
| MCP 权限需显式声明 | ✅ | 防影子依赖 |
| 危险操作路径白名单 | ✅ | 防越权访问 |
| Hooks 在所有模式生效 | ✅ | 统一安全层 |
| 敏感凭据不传递子代理 | ✅ | 防凭据泄漏 |

---

## 九、Dynamic Workflows 配置与派发（第4轮学习·R86新增）

> **来源**：Anthropic Claude Code Docs "Workflows" (2026)

### 9.1 Workflow 脚本配置模板

```yaml
# .claude/workflows/codebase-audit.yaml (项目级)
name: codebase-audit
description: "大规模代码审计——并行扫描所有API端点的认证检查"
trigger: "ultracode: audit every API endpoint"
phases:
  - name: enumerate_endpoints
    model: haiku_4.5         # 轻量模型扫描
    agents: 10
    task: "扫描 src/routes/ 下所有文件，列出每个API端点及其认证机制"
    
  - name: audit_parallel
    model: sonnet_4.5        # 审查用中等模型
    agents: 16               # 最大并发
    task: "逐端点检查: 是否有认证中间件? 是否有角色检查? 是否有输入验证?"
    
  - name: cross_verify
    model: opus_4.5          # 交叉验证用最强模型
    agents: 5
    task: "对比 audit_parallel 结果，驳斥至少一个其他Agent的发现，仅保留多源一致的漏洞"
    
  - name: synthesize_report
    model: opus_4.5
    agents: 1
    task: "汇总所有确认的漏洞，按严重性排序，生成修复建议"
```

### 9.2 派发算法 v3.0：三阶梯选择

```
用户任务 → 规模评估
│
├─ TIER 1: <10 子代理，<30分钟 → dispatch_task (传统)
│   └─ 五模式选择决策树（第8节 v2.0 算法）
│     - 有效: memory_ids, inherit_agent_id, 并行≤5
│
├─ TIER 2: 10-100 子代理，小时级 → 生成 Workflow 脚本
│   └─ 运行: ultracode 关键词或 /effort ultracode
│     - 子代理: acceptEdits 模式，继承工具白名单
│     - 保存: 同会话可 /workflows 面板暂停/恢复
│
└─ TIER 3: 100-1000 子代理，天级 → 持久化 Workflow
    └─ 保存: `s` 键保存为 /command
      - .claude/workflows/ (项目级, 团队共享)
      - ~/.claude/workflows/ (个人级, 全局可用)
      - 入参: args 参数传递（如 /triage-issues 1024, 1025, 1030）
```

### 9.3 Workflow 安全护栏

| 规则 | 说明 |
|------|------|
| **子代理不可交互** | 运行中不接受用户输入（仅权限提示可暂停） |
| **子代理 = acceptEdits** | 强制，不受会话权限模式影响 |
| **工具白名单继承** | 子代理继承你的 allowlist，未列的工具会弹窗中断 |
| **无文件系统直访** | Workflow 脚本本身不能直接读/写文件或执行 Shell——由 Agent 执行 |
| **16 并发 / 1000 Agent 上限** | 运行时约束，防止资源耗尽 |
| **不跨会话恢复** | 退出 Claude Code 后运行不可恢复——重新开始时从头执行 |

### 9.4 与现有 AGENTS.md 配置的关系

| 现有能力 | Workflow 中的对应 |
|---------|----------------|
| dispatch_task (v2.0 五模式) | 脚本内多 Phase 并行派发 → TIER 2-3 |
| 子代理权限模型 (Observer/Contributor/Operator) | Workflow 子代理 = acceptEdits（等价 Contributor） |
| Hooks 审计 | PreToolUse/PostToolUse 在 Workflow 场景同样生效 |
| MCP 最小化原则 | Workflow 场景更严格——白名单预配置避免长时间运行中断 |
| 团队规模模板 | Solo(Skills) / 小团队(subagents) / 大型(Agent Teams) / **超大型(Workflows)** |

---

## Anthropic 子代理管理与自动化

> 来源：Claude Code Advanced Patterns (2026.06)
> 更新：2026-06-15

### 五大机制
| 机制 | 用途 | 绕过模型？ |
|------|------|-----------|
| CLAUDE.md | 硬性规则(≤200行) | 否 |
| Skills | 流程知识(≤500行) | 否 |
| Subagents | 委派工作 | 否 |
| Hooks | 确定性自动化 | **是** |
| MCP | 外部访问 | 否 |

### 目录结构
`.claude/agents/`(项目级) + `~/.claude/agents/`(用户级)

### 权限最小化
code-reviewer: read/grep/glob(Haiku) | test-runner: bash/read(Haiku) | debugger: read/bash/grep(Sonnet)

### Hooks关键用例
PostToolUse: 自动lint | PreToolUse: 拦截危险命令 | SessionStart: 注入进度

### 子代理上限
1-3(小型) → 3-5(中型) → 5-8(大型) | 最大并行≤12 | 深度≤2层


---

## 第八章：Plugin Agents 配置完整规范（第三轮新增）

> **数据来源**：code.claude.com/docs/zh-CN/plugins-reference + claudecode.xyz/articles/claude-code-subagent-agent
> **更新**：2026-06-16 第三轮循环

### 8.1 agents/ 目录结构

Plugin agents 位于插件根目录中的 `agents/` 目录：

```
my-plugin/
├── plugin.json
└── agents/
    ├── code-reviewer.md      # YAML frontmatter + Markdown body
    ├── security-auditor.md
    └── db-migration-helper.md
```

每个 agent 文件格式：
```markdown
---
name: agent-name
description: 该 agent 的专长以及 Claude 应何时调用它
model: sonnet
effort: medium
maxTurns: 20
tools:
  - Read
  - Grep
disallowedTools:
  - Write
skills:
  - my-skill
color: blue
---

详细的系统提示，描述 agent 的角色、专业知识和行为。
```

### 8.2 YAML Frontmatter 完整字段表

| 字段 | 类型 | 必填 | 说明 | 示例值 |
|------|------|:--:|------|--------|
| `name` | string | ✅ | 唯一标识符（小写+连字符） | `code-reviewer` |
| `description` | string | ✅ | 触发时机描述，Claude 据此自动调用 | `专家级代码审查员。写完代码后主动调用。检查质量、安全性和可维护性。` |
| `model` | string | ❌ | 模型选择 | `sonnet` / `opus` / `haiku` / `inherit` |
| `tools` | list | ❌ | 允许的工具白名单 | `[Read, Grep, Glob, Bash]` |
| `disallowedTools` | list | ❌ | 明确禁止的工具 | `[Write, Edit]` |
| `permission_mode` | string | ❌ | 权限模式 | `plan` / `default` / `acceptEdits` / `bypassPermissions` |
| `skills` | list | ❌ | 预加载的 Skills | `[my-skill, db-helper]` |
| `autoMemory` | boolean | ❌ | 跨会话持久记忆 | `true` |
| `env` | object | ❌ | 额外环境变量 | `{MY_VAR: value}` |
| `color` | string | ❌ | UI 显示颜色 | `blue` / `red` / `green` / `yellow` / `purple` |
| `effort` | string | ❌ | 思考深度（仅 Opus 4.6+） | `low` / `medium` / `high` / `max` |
| `maxTurns` | integer | ❌ | 最大 Agentic 轮次 | `10` / `20` |
| `memory` | string | ❌ | 记忆范围 | `user` / `project` / `local` |
| `background` | boolean | ❌ | 默认后台运行 | `true` / `false` |
| `isolation` | string | ❌ | 隔离模式 | `worktree` |
| `initialPrompt` | string | ❌ | 主 agent 运行时的初始消息 | `分析当前项目的安全漏洞` |

### 8.3 Plugin Agents 的安全限制

⚠️ **Plugin agents 与独立 agents 的能力差异**：

| 字段 | 独立 agents | Plugin agents |
|------|:----------:|:----------:|
| `hooks` | ✅ 支持 | ❌ 不支持（安全限制） |
| `mcpServers` | ✅ 支持 | ❌ 不支持（安全限制） |
| `permissionMode` | ✅ 支持 | ❌ 不支持（安全限制） |
| `name` / `description` / `model` | ✅ 支持 | ✅ 支持 |
| `tools` / `disallowedTools` | ✅ 支持 | ✅ 支持 |
| `maxTurns` / `skills` | ✅ 支持 | ✅ 支持 |
| `memory` / `background` | ✅ 支持 | ✅ 支持 |

Plugin agents 被限制不能设置 hooks、MCP servers 和 permissionMode，以防止恶意插件获得过高权限。

### 8.4 集成行为

- 安装插件时自动发现 `agents/` 目录下的所有 agent 文件
- Claude 根据每个 agent 的 `description` 字段判断是否自动委派
- 同名 agent 遵循优先级链（独立配置 > Plugin agents）

---

## 第九章：Built-in Subagents 清单与用法（第三轮新增）

> **数据来源**：code.claude.com/docs/en/sub-agents + 4sapi.com/blog/claude-code-subagents-complete-guide
> **更新**：2026-06-16 第三轮循环

### 9.1 11 个内置 Subagent 完整清单

| # | Agent 名称 | 默认模型 | 工具权限 | 典型触发场景 | 是否可写 |
|:-:|-----------|---------|---------|------------|:---:|
| 1 | **Explore** | Haiku | Read/Grep/Glob（只读） | 代码库搜索、文件定位、架构探索 | ❌ |
| 2 | **Plan** | 继承主会话 | 只读 | Plan 模式下收集上下文 | ❌ |
| 3 | **general-purpose** | 继承主会话 | 全部工具 | 复杂的多步骤任务 | ✅ |
| 4 | **Bash** | 继承 | 终端命令 | 隔离上下文运行命令 | ✅ |
| 5 | **statusline-setup** | Sonnet | Read/Edit | 执行 /statusline 配置 | ✅ |
| 6 | **claude-code-guide** | Haiku | 只读 | 询问 Claude Code 自身功能 | ❌ |
| 7 | **code-reviewer** | Sonnet | Read/Grep/Glob | 代码质量审查、改进建议 | ❌ |
| 8 | **security-reviewer** | Sonnet | Read/Grep/Glob/Bash | 安全漏洞检测、修复建议 | ✅ |
| 9 | **test-creator** | Sonnet | Read/Write/Bash | 生成测试用例 | ✅ |
| 10 | **build-error-resolver** | Sonnet | Read/Bash | 修复构建错误 | ✅ |
| 11 | **doc-updater** | Sonnet | Read/Write | 更新文档 | ✅ |

### 9.2 Explore Agent 深入

- **模型**：Haiku（快速、低延迟、低成本）
- **Thoroughness Levels**：`quick`（定向查找）、`medium`（平衡探索）、`very thorough`（全面分析）
- **特殊优化**：跳过 CLAUDE.md 和 git status 加载（更快启动）
- **最佳触发**：需要读 3+ 文件了解代码库时自动触发

### 9.3 Plan Agent 深入

- **模型**：继承主会话模型
- **触发条件**：Plan 模式下需要理解代码库时
- **关键设计**：防止无限嵌套（subagent 不能再派生子代理），同时收集必要上下文

### 9.4 general-purpose Agent 深入

- **适用**：既需要探索又需要修改的复杂多步骤任务
- **继承**：主会话的所有工具和权限
- **典型场景**：复杂研究 → 代码修改 → 验证 → 迭代

### 9.5 辅助 Agent 清单

| Agent | 何时自动调用 |
|-------|------------|
| **Bash** | 需要在隔离上下文中运行终端命令 |
| **statusline-setup** | 运行 `/statusline` 命令时 |
| **claude-code-guide** | 用户询问 Claude Code 功能问题时 |

### 9.6 Subagent 运行时识别

```
Subagent 在跑：
├── Task: Explore codebase IN "分析项目结构..."
├──  Read config.py
├──  Grep "function"
└──  返回结果

主Agent 在跑：
├── Read config.py
├── Edit main.py
├── Bash npm install
└── ...
```

---

## 第十章：Subagent 作用域与优先级（第三轮新增）

> **数据来源**：claudecode.xyz + studynil.com + 4sapi.com 社区最佳实践汇总
> **更新**：2026-06-16 第三轮循环

### 10.1 四级覆盖链

```mermaid
graph TD
    A["--agents CLI Flag (最高优先级)"] --> B[".claude/agents/ (项目级)"]
    B --> C["~/.claude/agents/ (用户级)"]
    C --> D["Plugin agents/ (最低优先级)"]
```

| 级别 | 位置 | 作用域 | 优先级 | 持久性 |
|:---:|------|------|:---:|------|
| **1** | `--agents` CLI Flag | 当前会话 | **最高** | 会话结束即失效 |
| **2** | `.claude/agents/` | 当前项目 | 高 | Git 版本控制，团队共享 |
| **3** | `~/.claude/agents/` | 所有项目 | 中 | 跨项目持久，个人使用 |
| **4** | Plugin `agents/` 目录 | 插件启用的地方 | 最低 | 随插件安装/卸载 |

### 10.2 覆盖机制

- **同名 Agent**：高优先级覆盖低优先级（如 `.claude/agents/code-reviewer.md` 覆盖 Plugin 中的同名定义）
- **不同名 Agent**：不同级别的 agent 共存，不会互相覆盖
- **合并行为**：同一 agent 名在不同级别的多个定义中，仅最高优先级生效

### 10.3 CLI Flag 用法

```bash
# 临时会话定义 agent（JSON 格式）
claude --agents '{
  "code-reviewer": {
    "description": "代码审查员，代码修改后自动调用",
    "prompt": "你是资深代码审查员，关注质量、安全、测试和性能。",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  }
}'
```

**适用**：临时需要特定 agent、测试新 agent 配置、一次性任务

### 10.4 创建 Subagent 的三种方式

| 方式 | 命令/位置 | 适用场景 |
|------|---------|---------|
| `/agents` 命令 | 交互式 UI | 推荐：自然语言描述，自动生成配置 |
| 手写 Markdown | `.claude/agents/*.md` | 精确控制：手动编写 YAML + system prompt |
| `--agents` CLI Flag | 命令行参数 | 临时会话：一次性 agent 定义 |

---

## 第十一章：持久记忆 autoMemory 与后台运行 Ctrl+B（第三轮新增）

> **数据来源**：claudecode.xyz/articles/claude-code-subagent-agent + digitalapplied.com/blog
> **更新**：2026-06-16 第三轮循环

### 11.1 autoMemory 持久记忆机制

Subagent 可以拥有自己的 Auto Memory，跨会话保留学习内容：

```yaml
---
name: database-expert
description: 数据库查询专家，了解项目 Schema 后自动记住
autoMemory: true
---
```

**工作原理**：
1. Subagent 在任务执行中学习项目特定知识（Schema 布局、命名约定、常用查询模式）
2. 学习内容写入该 subagent 专属的 memory 存储
3. 下次该 subagent 被激活时自动加载之前的记忆
4. 跨会话持久化，不受主对话上下文清理影响

### 11.2 memory 字段的作用域

| 值 | 存储位置 | 共享范围 | 适用场景 |
|----|---------|---------|---------|
| `user` | `~/.claude/memory/` | 跨项目 | 通用知识（如编码风格偏好） |
| `project` | `.claude/memory/` | 团队共享（Git 控制） | 项目特定知识（如架构决策） |
| `local` | `.claude/memory.local/` | 仅本地（gitignored） | 个人调试笔记 |

### 11.3 前台运行模式

```
用户 → 主Agent → 委派 Subagent
                     ↓
               Subagent 工作...
               (主Agent 等待)
                     ↓
               Subagent 完成
                     ↓
          主Agent 获得摘要 → 继续对话
```

**适用**：需要 subagent 结果才能继续的关键路径任务

### 11.4 后台运行模式（Ctrl+B）

```
用户 → 主Agent → 委派 Subagent (后台)
      主Agent 继续与用户对话...
                     ↓ (Subagent 在后台工作)
               Subagent 完成 → 自动汇报给主Agent
```

**适用**：
- 非关键路径的探索任务（代码搜索、文档扫描）
- 并行处理多个独立任务
- 用户不想等待的耗时操作

**配置**：在 frontmatter 中设置 `background: true` 让 subagent 默认后台运行

### 11.5 并行 vs 顺序 Subagent 调用

| 模式 | 方式 | Token 成本 | 适用场景 |
|------|------|:---:|------|
| **顺序** | 逐个调用 | 正常（N×1） | 有依赖关系、成本敏感 |
| **并行** | 同时启动多个 | ~N×（每个 re-read system prompt+context） | 时间关键、独立子任务 |

**优化策略**：
- 审查和探索类任务 → 并行（code-reviewer + security-reviewer 同时运行）
- 构建和测试类任务 → 顺序（先 build-error-resolver 再 test-creator）
- 成本考虑 → 用 Haiku 模型的 Explore agent 做初步探索，再用 Sonnet agent 做深度分析

### 11.6 隔离高流量操作模式

```
用 Explore Agent 分析代码库 → 返回精简摘要
↓
用 Plan Agent 制定重构计划 → 返回结构化步骤
↓
主Agent 按计划执行修改（上下文保持干净）
```

这个模式确保大量代码阅读和搜索的"噪音"被隔离在 subagent 的独立上下文中，主 Agent 只看到处理后的干净结果。

---

## 十二、Dynamic Workflows：自动子代理生成与管理

> 来源：Anthropic 2026-06-03 发布

### 12.1 从手动配置到自动生成

传统子代理管理模式 vs Dynamic Workflows 模式：

| 维度 | 传统手动配置 | Dynamic Workflows |
|------|------------|-------------------|
| 子代理定义 | 手动编写 `.md` 文件 | Claude 自动生成 |
| 任务分配 | 主Agent手动调度 | 自动拆解+分配 |
| 并行控制 | 开发者手动规划 | 自动并行优化 |
| 规模上限 | 通常 3-5 个 | 可达 100+ 个 |
| 上下文管理 | 开发者手动控制 | 自动隔离 |

### 12.2 自动生成子代理的生命周期

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 任务分析  │ → │ 自动拆分  │ → │ 生成N个   │ → │ 并行执行  │
│          │    │          │    │ Subagent  │    │          │
└──────────┘    └──────────┘    └──────────┘    └─────┬────┘
                                                      │
                                              ┌───────▼────────┐
                                              │ 结果汇总+归档   │
                                              │ Subagent 自动销毁│
                                              └────────────────┘
```

### 12.3 与传统 Subagent 配置的共存策略

```
项目根目录/
├── CLAUDE.md                         # 保持不变：手动定义常驻子代理
├── .claude/
│   ├── subagents/                    # 手动定义（code-reviewer等）
│   │   ├── code-reviewer.md
│   │   ├── security-auditor.md
│   │   └── doc-writer.md
│   └── skills/                       # Skills 技能库
│       └── ...
│
│ Dynamic Workflows 自动生成的子代理：
│ → 临时创建，任务完成后自动销毁
│ → 不污染 .claude/subagents/ 目录
│ → 仅存在于会话生命周期内
```

**共存原则**：
- 常驻子代理（code-reviewer、security-auditor）→ 手动定义在 `.claude/subagents/`
- 大规模一次性任务 → 交给 Dynamic Workflows 自动生成
- 两者互不干扰，根据任务规模自动选择

### 12.4 触发条件配置

```markdown
# CLAUDE.md 中添加

## Dynamic Workflows Policy
- 当任务可拆分为 5+ 独立并行子任务时，优先使用 Dynamic Workflows
- 当任务需要保持人工逐步骤审核时，退回手动 Subagent 模式
- 安全敏感操作（数据库迁移、生产部署）必须人工审核
```

---

## 十三、Skills 版本锁定与企业治理配置

### 13.1 Skills Registry 配置

```yaml
# .claude/skills/registry.yaml
skills:
  - name: code-review
    owner: dev-team
    version: 2.1.0          # 生产环境锁定版本
    eval_suite: review-evals-v3
    rollback: 2.0.5
    sandbox: true
    approval: required
    
  - name: security-audit
    owner: security-team
    version: 1.4.2
    eval_suite: sec-evals-v2
    rollback: 1.4.0
    sandbox: true
    approval: required
    
  - name: doc-generator
    owner: docs-team
    version: 1.0.0
    eval_suite: doc-evals-v1
    rollback: 0.9.8
    sandbox: false
    approval: optional
```

### 13.2 企业治理检查清单

| 控制领域 | 标准要求 | 配置物 |
|---------|---------|--------|
| 可发现性 | 小型可组合技能 + 清晰触发器和元数据 | SKILL.md + tags |
| 质量门槛 | Generator→Evaluator 循环 + 阈值 | TESTS.md + eval_log |
| 版本控制 | 锁定生产版本 + 回滚计划 | REGISTRY.md + CHANGELOG |
| 安全 | 沙箱执行 + 凭据存保险库 + 审计I/O | THREAT.md + audit_log |
| 监控 | 使用量指标 + 定期重评 + 负责人 | RUNBOOK.md |

### 13.3 Skills 常见错误与修正配置

| 错误模式 | 修正配置 |
|---------|---------|
| 单体"超级技能" | 拆分为窄领域技能，配独立 SKILL.md |
| 缺失验证 | 添加 Evaluator 技能，配通过/失败阈值 |
| 凭据内嵌 | 迁移至 Vault，使用 MCP/Proxy 访问 |
| 无回滚 | 锁定版本号，保留 `rollback` 字段 |
| 状态丢失 | 持久化产物到 Files API，记录 NOTES.md |

### 13.4 新技能生态集成配置

2026年6月社区技能的一键安装与配置：

```bash
# 自动沉淀工作流
npx skills add claudeception

# 版本管理（防覆盖）
npx skills add xiaoerzhan/skill-vision-control

# 文档转视频PPT
npx skills add op7418/NanoBanana-PPT-Skills

# 需求预判
npx skills add humanplane/homunculus
```

安装后无需额外配置，自动生效。Skill Vision Control 会在更新时自动保留本地修改并提供 Diff 对比。


---

## 十四、Agent SDK 自动化配置（第5轮学习·R92新增）

> 来源：platform.claude.com Agent SDK Python + code.claude.com/docs/en/sub-agents

### 14.1 SDK 会话自动化配置

```python
from claude import ClaudeAgentOptions, MCPTool, ClaudeSDKClient

options = ClaudeAgentOptions(
    max_turns=20,                       # 轮次上限（防无限循环）
    model="claude-sonnet-4-5",
    mcp_servers={
        "filesystem": mcp_filesystem,   # 内联 MCP
        "database": mcp_database,       # 多 MCP 混合
    },
    system_prompt="你是自动化运维Agent..."
)

# 自动化生命周期：open → run → close
client = ClaudeSDKClient()
async with client.connect(options) as session:
    result = await session.query("检查今天的错误日志")
    # session 自动管理连接、上下文、清理
```

### 14.2 会话检索自动化

```python
# 按目录过滤当前项目所有协作会话
active_sessions = client.list_sessions(
    SessionQuery(directory="/team-project", status="active")
)
# 按时间排序，获取最近修改的文件和变更摘要
for s in active_sessions:
    history = client.get_session_messages(s.id)
```

**自动化场景**：
- 每日自动审计前一天的所有 Agent 决策
- CI/CD 中验证没有 Agent 执行非法操作
- 多项目环境下按项目维度统计 Agent 使用量

### 14.3 MCP 工具注册自动化

```python
@tool(
    name="deploy_preview",
    description="部署预览环境到 Vercel",
    input_schema={"branch": str, "commit": str},
    annotations=ToolAnnotations(readOnlyHint=False, openWorldHint=True)
)
async def deploy(args): ...

# 工具注册即配置——零额外 JSON 文件
server = create_sdk_mcp_server("ci-cd", tools=[deploy])
```

**设计哲学**：代码即配置。`@tool` 装饰器同时完成函数定义、类型声明、MCP 协议注册——消除配置漂移，确保"代码中的就是运行时的"。

### 14.4 子代理配置字段更新（官方最新）

| 新增/更新字段 | 类型 | 说明 |
|-------------|------|------|
| `autoMemory` | boolean | 跨会话持久记忆（无需主 Agent 手动维护） |
| `memory` | `user`/`project`/`local` | 记忆存储作用域 |
| `background` | boolean | 默认后台运行（不阻塞主会话） |
| `isolation` | `worktree` | 隔离模式（独立工作树） |
| `initialPrompt` | string | 主 Agent 派发时的初始消息 |
| `effort` | `low`/`medium`/`high`/`max` | Opus 4.6+ 思考深度控制 |

---

> **版本更新声明**
> 更新：2026-06-16 第四轮循环
> 本轮新增：Dynamic Workflows 自动子代理生成与管理（生命周期、与传统配置共存策略、触发条件配置）、Skills 版本锁定与企业治理（Registry配置、检查清单、错误修正）、新技能生态集成配置（npx 一键安装）


---

## 六、Claude Code 六种扩展机制速查（2026年5月）

| 机制 | 文件位置 | 用途 | 触发方式 |
|------|---------|------|---------|
| CLAUDE.md | 项目根目录 | 持久化上下文、项目规则 | 自动加载 |
| Skills | .claude/skills/*/SKILL.md | 可复用程序化知识 | 元数据自动匹配 |
| Hooks | .claude/hooks/ | 事件触发处理器 | 事件驱动 |
| Subagents | 内建 | 独立上下文任务委派 | 主Agent调度 |
| MCP | 独立服务 | 外部工具/数据连接 | 工具调用 |
| Dynamic Workflows | 内建（Max/Team） | 大规模并行任务拆分 | 自动触发 |

### 6.1 Skills 六步标准工作流

| 步骤 | 名称 | 操作 | 关键输出 |
|------|------|------|---------|
| Step 1 | 规划定义 | 明确任务、输入、输出、约束 | SPEC.md |
| Step 2 | 技能选择 | 清晰触发器和元数据 | 技能匹配列表 |
| Step 3 | 外部连接 | MCP Server 或程序化工具调用 | MCP配置 |
| Step 4 | 验证循环 | Generator→Evaluator成对运行 | 验证日志 |
| Step 5 | 状态交接 | Files API持久化输出物 | NOTES.md |
| Step 6 | 迭代交付 | 验证通过链入下一步 | 最终产物 |

### 6.2 Skills 企业治理矩阵

| 控制领域 | 标准要求 | 证明产物 |
|---------|---------|---------|
| 可发现性 | 小型可组合技能，清晰触发器 | SKILL.md + tags |
| 质量门槛 | Generator→Evaluator循环 | TESTS.md + 评估日志 |
| 版本控制 | 锁定生产版本 + 回滚计划 | REGISTRY.md + CHANGELOG |
| 安全 | 沙箱执行、凭据存保险库 | THREAT.md + 审计日志 |
| 监控 | 使用量指标、定期重评 | RUNBOOK.md + 仪表盘 |

---

## 七、Agent Teams 子代理编排进阶（R89新增）

> 来源：Anthropic 官方 Agent Teams + Hooks + Best Practices 文档
> 更新：2026-06-16 第四轮循环

### 7.1 Subagent 定义复用为 Teammate

子代理定义可以在两种模式间复用：

```bash
# 作为 Subagent 委派（单会话内）
"Use the security-reviewer agent to audit the auth module"

# 作为 Agent Team Teammate（多会话协作）
"Spawn a teammate using the security-reviewer agent type to audit the auth module"
```

**复用规则**：
- `tools` 和 `model` 字段被 Teammate 沿用
- 定义正文追加到 Teammate 的系统提示（不替换）
- `skills` 和 `mcpServers` 在 Teammate 模式下从项目/用户设置加载
- 团队协调工具（SendMessage、任务管理）始终可用

### 7.2 Teammate 权限与模型

| 配置项 | 行为 |
|--------|------|
| 权限继承 | Teammates 继承 Lead 的权限设置 |
| 模型选择 | 默认不继承 Lead 的 `/model`，需显式指定 |
| 计划审批 | 可要求 Teammate 先规划再执行 |
| 直接交互 | Shift+Down 循环切换 / 分屏模式点击 |

### 7.3 Hooks 事件完整生命周期

```
SessionStart → UserPromptSubmit → PreToolUse → PostToolUse →
  ├── SubagentStart → SubagentStop
  ├── TaskCreated → TaskCompleted
  ├── TeammateIdle
  ├── PreCompact → PostCompact
  └── Stop → SessionEnd
```

**关键 Hooks 配置示例**：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "if": "Bash(rm *)",
        "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh"
      }]
    }],
    "TeammateIdle": [{
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/quality-check.py"
      }]
    }]
  }
}
```

### 7.4 Hook 决策输出标准

| 输出 | 效果 |
|------|------|
| `exit 0`（无 JSON 输出） | 无决策，走正常权限流程 |
| `{"permissionDecision": "allow"}` | 明确放行 |
| `{"permissionDecision": "deny", "permissionDecisionReason": "..."}` | 阻止并说明原因 |
| `exit 2`（TeammateIdle/TaskCreated/TaskCompleted） | 发送反馈并保持工作/阻止操作 |

### 7.5 Claude Code 环境配置 Checklist

```bash
# 1. CLAUDE.md —— 项目持久上下文（/init 自动生成）
# 2. 权限配置 —— /permissions 白名单 + Auto Mode
# 3. MCP 服务 —— claude mcp add 连接外部工具
# 4. Hooks —— 事件驱动的确定性操作
# 5. Skills —— .claude/skills/*/SKILL.md 领域知识
# 6. Subagents —— .claude/agents/ 任务委派
# 7. Agent Teams —— 启用 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**CLAUDE.md 编写铁律**：
- ✅ 包含：Bash 命令、代码风格偏离项、测试指令、架构决策、环境怪癖、常见陷阱
- ❌ 排除：能从代码推断的内容、标准语言约定、详细 API 文档、长篇解释、自明实践
- 每个条目自问："删除它会导致 Claude 犯错吗？"——不删就保留，删了就砍掉

---

## 2026-06-16 更新：子代理管理进阶

### 一、Subagent 定义格式（YAML Frontmatter + Markdown）

Subagent 是带 YAML frontmatter 的 Markdown 文件，完整格式如下：

```markdown
---
name: security-reviewer
description: 审查代码安全漏洞，专注认证、注入、权限三类风险
tools: Read, Grep, Glob
model: sonnet
memory: project
---

你是资深安全审计工程师。每次审查时：
1. 先读取内存目录中的历史审计记录
2. 再扫描目标代码
3. 最后按严重程度（Critical / High / Medium / Low）分类输出
```

**字段说明**：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | Subagent 唯一标识名称 |
| `description` | ✅ | 一句话描述，用于主 Agent 自动匹配 |
| `tools` | ✅ | 工具白名单（Read/Grep/Glob/Bash/Write/WebSearch/WebFetch/MCP 工具） |
| `model` | ❌ | 指定模型（sonnet/haiku/opus），不指定则继承主会话 |
| `memory` | ❌ | 持久记忆：project（项目级）或 user（用户级） |

### 二、目录结构规范

```
~/.claude/agents/          # 用户级 Subagent（所有项目可用）
  security-reviewer.md
  doc-writer.md

.claude/agents/            # 项目级 Subagent（仅当前项目）
  code-reviewer.md
  test-generator.md
```

**优先级规则**：
- 项目级定义覆盖用户级同名 Subagent
- Managed Settings 定义优先级最高，不可被用户/项目覆盖

### 三、权限矩阵

Subagent 的 `tools` 字段定义其可用工具白名单：

| 工具 | 能力 | 风险等级 | 典型用途 |
|------|------|---------|---------|
| Read | 读取文件 | 🟢 低 | 代码审查、文档检查 |
| Grep | 正则搜索 | 🟢 低 | 模式匹配、代码搜索 |
| Glob | 文件名匹配 | 🟢 低 | 文件发现、目录遍历 |
| Bash | 执行命令 | 🟡 中 | 运行测试、Git 操作 |
| Write | 创建文件 | 🟡 中 | 生成代码、写报告 |
| Edit | 编辑文件 | 🟡 中 | 修改代码、重构 |
| WebSearch | 联网搜索 | 🟡 中 | 查文档、搜资料 |
| WebFetch | 抓取网页 | 🟡 中 | 分析在线文档 |
| MCP 工具 | 外部服务 | 🟡-🔴 中高 | 数据库查询、API 调用 |

**权限最小化示例**：
- 只读审查代理：`tools: Read, Grep, Glob`
- 代码生成代理：`tools: Read, Write, Edit, Bash`
- 研究代理：`tools: Read, WebSearch, WebFetch`

**六档权限模式**（`permissionMode`）：
| 模式 | 说明 |
|------|------|
| `plan` | 只读探索，不允许任何修改 |
| `default` | 高风险操作需要手动确认 |
| `acceptEdits` | 自动批准文件编辑 |
| `auto` | 自动批准大多数操作 |
| `bypassPermissions` | 跳过所有确认（危险） |

### 四、Managed Settings 企业部署

**managed-settings.json 路径**：
- macOS: `~/Library/Application Support/ClaudeCode/managed-settings.json`
- Windows: `C:\Program Files\ClaudeCode\managed-settings.json`（v2.1.75+）
- Windows 注册表（GPO）: `HKLM\Software\Policies\Anthropic\ClaudeCode`

**下发方式**：
| 方式 | 平台 | 说明 |
|------|------|------|
| managed-settings.json | 全平台 | 直接部署到指定路径 |
| MDM（Jamf/Kandji） | macOS | 通过设备管理系统推送 |
| Windows 组策略（GPO） | Windows | 写入注册表策略 |
| Anthropic 管理后台 | 全平台 | Web 控制台统一管理 |

**锁定策略示例**：
```json
{
  "permissions": {
    "allow": ["Agent(security-reviewer)", "Agent(doc-writer)"],
    "deny": ["Agent(general-purpose)"]
  },
  "allowManagedPermissionRulesOnly": true
}
```

设置 `allowManagedPermissionRulesOnly: true` 后，用户和项目级别的权限规则完全禁止修改。

### 五、Hooks 配置示例（settings.json）

完整的 Hooks 配置结构：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "npx your-tool init"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/validate-bash.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/log-tool-call.sh"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/slack-notify.sh"
          }
        ]
      }
    ]
  }
}
```

**事件类型详解**：
| 事件 | 触发时机 | 控制能力 | 典型脚本 |
|------|---------|---------|---------|
| `SessionStart` | 会话启动 | 注入上下文 | `npx your-tool init` |
| `PreToolUse` | 工具调用前 | Exit code 2 = 阻止 | `validate-bash.sh` |
| `PostToolUse` | 工具调用后 | 记录 + 通知 | `log-tool-call.sh` |
| `Notification` | 自定义事件 | 转发到外部 | `slack-notify.sh` |

**关键约束**：
- PreToolUse 脚本退出码 2 阻止工具执行
- PostToolUse 脚本结果不影响工具执行（仅记录）
- Hooks 是确定性代码，不依赖 LLM 判断

### 六、MCP 最小化原则

**按需配置，逐步接入**：

1. **只添加实际使用的服务器**："tool names are cheap, tool output is not"——工具名不占上下文，但工具返回占用
2. **密钥不提交**：Token 通过 `${ENV_VAR}` 形式引用环境变量，`.mcp.json` 中不写明文密钥
3. **Scope 分层**：
   - Project scope：团队标准工具和安全本地服务器 → 提交到仓库
   - User scope：个人工具、私人 Token、实验性工具 → 不提交
   - Local scope：测试新服务器 → 避免提交
4. **逐步接入**：安装一个 → 确认 Claude 正确使用 → 再添加下一个。不要一次连 20 个。

**从低风险到高风险的接入顺序**：
```
只读型 MCP → 低风险写入 → 高风险写入（需人工确认 + 审计）
```

**安全检查清单**：
- [ ] `.mcp.json` 中没有明文 Token
- [ ] 所有密钥通过环境变量引用
- [ ] 服务器按 scope 正确分层
- [ ] 写操作 MCP 有 PreToolUse Hook 门禁
- [ ] 高风险 MCP 有审计日志

### 七、Agent Teams 团队规模模板

| 规模 | Teammate 数 | 典型配置 | 适用场景 |
|------|------------|---------|---------|
| **小型** | 2-3 | Lead + 2 Teammates | 简单代码审查、双视角验证、小功能开发 |
| **中型** | 4-7 | Lead + 4-6 Teammates | 多模块并行开发、全栈项目、中型代码迁移 |
| **大型** | 8-15 | Lead + 8-14 Teammates | 大型代码库迁移、跨服务重构、深度交叉验证 |

**团队规模选择原则**：
- 从 2-3 人小型团队起步，验证协作模式可行后再扩展
- 超过 5 个 Teammates 协调成本指数增长
- 大型团队（8+）仅用于已有成功经验 + 任务天然可高度并行化的场景

**实验性功能声明**：Agent Teams 在 2026 年初为实验性功能，需手动设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 启用。生产环境建议等待正式发布后再大规模使用。

---

## R91 增量：子代理嵌套配置 & 权限规则参数匹配（2026-06-17）

> 来源：Claude Code v2.1.172-v2.1.178 + Havoptic Changelog

### 一、子代理5层嵌套配置

**CLAUDE.md 配置示例**（主代理定义可嵌套的子代理）：

```markdown
## Subagents

### codebase-auditor
- Purpose: 大型代码库分层审查
- Max Depth: 3
- Tools: Read, Glob, Grep, Agent
- Agent(model:sonnet)

### deep-analyzer
- Purpose: 深度分析（可递归分解）
- Max Depth: 5
- Tools: Read, Glob, Grep, Agent, Bash
```

**嵌套权限控制**：
- 子代理的 `Agent` 工具即为其嵌套能力
- 每层子代理的工具白名单独立配置
- 深层子代理默认继承父级的工具限制并只能更严格

### 二、权限规则参数匹配（v2.1.178）

**`Tool(param:value)` 语法**：允许权限规则匹配工具的具体入参。

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(npm:*)",
      "Agent(model:sonnet)",
      "Agent(model:haiku)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(sudo:*)",
      "Agent(model:opus)"
    ]
  }
}
```

**应用场景**：

| 规则 | 效果 |
|------|------|
| `Agent(model:sonnet)` | 仅允许 Sonnet 模型的子代理 |
| `Agent(model:opus)` deny | 禁止 Opus 子代理（控制成本） |
| `Bash(rm:*)` deny | 全局禁止删除命令 |
| `Bash(git:*)` allow | 允许所有 git 操作 |
| `Write(path:src/*)` allow | 仅允许写入 src 目录 |

### 三、Managed Settings 安全增强

| 设置项 | 版本 | 功能 |
|--------|------|------|
| `enforceAvailableModels` | v2.1.175 | availableModels 白名单强制约束 Default 模型 |
| `--safe-mode` / `CLAUDECODESAFEMODE` | v2.1.169 | 启动时禁用所有自定义配置 |
| `requiredMinimumVersion` | v2.1.163 | Claude Code 版本下限强制管控 |
| `requiredMaximumVersion` | v2.1.163 | Claude Code 版本上限强制管控 |
| `fallbackModel` | v2.1.166 | 最多3个备用模型（主模型不可用时自动切换） |

### 四、Agent Teams 规模限制更新

鉴于子代理现在可嵌套5层，团队规模模板需增加深度维度：

| 维度 | 推荐值 | 最大值 | 风险 |
|------|--------|--------|------|
| 广度（并行 Teammates） | 3-5 | 15 | 协调成本指数增长 |
| 深度（嵌套层数） | 1-2 | 5 | Token 成本指数增长 |
| 总子代理数（广度×深度） | 5-10 | 理论无限 | 超过 20 个几乎不可调试 |

**组合约束**：广度 × 深度 ≤ 20 作为硬性上限。例如 4 个并行 Teammates 各嵌套 2 层（4×2=8）是合理的；5 个 Teammates 各嵌套 5 层（5×5=25）超限。

---

## R92 增量：Routines 配置、Managed Agents Vault 与 Security Scanning（2026-06-17）

> 来源：Code with Claude Tokyo (June 10-11, 2026)

### 一、Routines 配置规范

Routines 是云端托管的 Agent 执行环境，通过事件驱动触发。

**配置结构**：
```yaml
routines:
  - name: nightly-security-scan
    trigger:
      type: cron
      schedule: "0 2 * * *"        # 每天凌晨2点
    agent:
      prompt: "扫描项目安全漏洞并自动修复"
      auto_mode: true
      vault: "security-creds"      # 引用 Managed Agents Vault
    notify:
      on_success: slack:#security
      on_failure: slack:#oncall + email:admin@team.com

  - name: pr-test-runner
    trigger:
      type: github
      event: pull_request.merged
      branch: main
    agent:
      prompt: "运行全量回归测试，失败时自动回滚"
      auto_mode: false             # 回滚需人工确认
      vault: "ci-creds"

  - name: issue-triage
    trigger:
      type: github
      event: issues.opened
    agent:
      prompt: "自动分类 Issue 并分派到对应负责人"
      auto_mode: true
```

### 二、Managed Agents Vault 配置

Vault 为 Routines 提供安全的凭据和环境变量存储：

```yaml
vaults:
  - name: security-creds
    variables:
      - SNYK_API_KEY: "encrypted:****"
      - GITHUB_TOKEN: "encrypted:****"
    scoped_routines: [nightly-security-scan]

  - name: ci-creds
    variables:
      - DOCKER_REGISTRY_PASS: "encrypted:****"
      - AWS_ACCESS_KEY: "encrypted:****"
    scoped_routines: [pr-test-runner, deploy-routine]
```

**Vault 安全铁律**：
1. 每个 Routine 只访问其专属 Vault，不允许跨 Routine 共享
2. 凭据写入后不可明文读取，仅 Routine 执行时注入环境变量
3. Vault 凭据变更需额外 MFA 验证

### 三、Security Scanning 配置

Security Scanning 作为"第一个 Routine"的标准模板：

```yaml
routines:
  - name: nightly-security-scan
    trigger:
      type: cron
      schedule: "0 2 * * *"
    agent:
      prompt: |
        执行以下安全检查：
        1. 依赖漏洞扫描（npm audit / pip audit）
        2. 代码安全模式检测（SQL注入/CSRF/XSS）
        3. 许可证合规审查
        4. 敏感信息泄露检查（API Key / 密码硬编码）
        对每个发现问题自动创建修复 PR。
      auto_mode: true
      subagents:
        - name: dep-scanner
          tools: [Bash(npm:*), Bash(pip:*)]
        - name: code-scanner
          tools: [Read, Glob, Grep]
        - name: license-checker
          tools: [Read, Glob]
    notify:
      on_complete: slack:#security-daily
      on_critical: slack:#oncall
```

### 四、全栈 Agent 平台管理矩阵

| 管理维度 | CLI 配置 | Desktop 可视化管理 | Routines 云端配置 |
|---------|---------|-------------------|------------------|
| 子代理定义 | CLAUDE.md | 可视化编辑 | YAML 声明 |
| 权限控制 | permissions JSON | 图形化权限面板 | Vault 隔离 |
| 触发器 | 不支持 | 不支持 | Cron/API/GitHub |
| 密钥管理 | 环境变量 | 系统钥匙串 | Managed Vault |
| 任务监控 | 终端输出 | Desktop 面板 | Remote Control |