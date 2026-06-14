---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_e894944f655f11f1af8f5254002afed2
    ReservedCode1: GGbUlbC9AOozJXiJxKuI6H2Z2C/Hcmb7R9tZ3TiYt9bpH1v+0g9ZZM7nyDXzhmvHShdgLz3FWwNVLg9NdwfIN7PnQ17uJ/BxZIFVInU3gvcaG4PJQUuvSnT9rjwOXmo/KITMosEuwOguP4xpDqMBUDxfIfL3+oEWfEthx8UennfmrQHN5IZkhnrTl1k=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_e894944f655f11f1af8f5254002afed2
    ReservedCode2: GGbUlbC9AOozJXiJxKuI6H2Z2C/Hcmb7R9tZ3TiYt9bpH1v+0g9ZZM7nyDXzhmvHShdgLz3FWwNVLg9NdwfIN7PnQ17uJ/BxZIFVInU3gvcaG4PJQUuvSnT9rjwOXmo/KITMosEuwOguP4xpDqMBUDxfIfL3+oEWfEthx8UennfmrQHN5IZkhnrTl1k=
---

# AGENTS.md — 子代理管理与自动化配置

> 来源：Anthropic官方课程提炼 · 2026-06-12 R18
> 定位：子代理创建、管理、配置的完整手册

---


> 关联文档：[[Anthropic官方课程-390节全集]] — 18门课程全量索引 · 2026-06-02
## 一、子代理架构总览

### 1.1 子代理定义
子代理是拥有**独立上下文窗口**的专用AI助手，由主Agent创建和调度，执行隔离任务后仅返回精炼结果。

### 1.2 核心价值
| 价值 | 说明 |
|------|------|
| 上下文隔离 | 每个子代理独立上下文，避免主对话膨胀 |
| 并行执行 | 多个子代理可同时处理不同子任务 |
| 专注高效 | 每个子代理聚焦单一领域，质量更高 |
| 安全边界 | 子代理权限可独立控制，降低风险 |

### 1.3 何时使用子代理
- 任务可拆分为**独立可验证**的子任务
- 子任务执行过程**不需要**与主Agent实时交互
- 结果可**精炼汇总**，不需要完整执行日志
- 任务复杂度**值得**创建子代理的开销

---

## 二、子代理配置规范

### 2.1 创建子代理
```markdown
## 子代理：代码审查专家

### 触发条件
- 用户要求代码审查
- 提交PR前自动触发
- 代码变更超过50行

### 系统提示词
你是一个代码审查专家，专注于：
1. 代码质量和可读性
2. 潜在Bug和安全漏洞
3. 性能优化建议
4. 最佳实践遵循

### 权限
- 读取：当前项目所有文件
- 写入：仅审查报告文件
- 禁止：修改源代码、执行系统命令
```

### 2.2 子代理分类
| 类型 | 特点 | 示例 |
|------|------|------|
| 文件Agent | 文件系统操作 | 搜索、整理、转换 |
| 浏览器Agent | 网页交互 | 表单填写、数据提取 |
| 应用Agent | 应用操作 | 启动、安装、界面交互 |
| 系统Agent | 系统配置 | 设置、诊断、修复 |
| 搜索Agent | 深度检索 | 论文检索、对比分析 |

### 2.3 权限矩阵
| 权限 | 文件Agent | 浏览器Agent | 应用Agent | 系统Agent |
|------|----------|------------|----------|----------|
| 读文件 | ✅ | 按需 | 按需 | ✅ |
| 写文件 | ✅ | ❌ | ❌ | 受限 |
| 网络访问 | ❌ | ✅ | ❌ | ❌ |
| 系统设置 | ❌ | ❌ | ❌ | ✅ |
| 应用控制 | ❌ | ❌ | ✅ | ❌ |

---

## [更新日期: 2026-06-12 R17] Agent SDK 子代理程序化配置

> 来源：Anthropic Agent SDK 官方文档

### 2.4 程序化定义子代理（SDK推荐方式）

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Review the authentication module for security issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
                    prompt="You are a code review specialist with expertise in security, performance, and best practices.",
                    tools=["Read", "Grep", "Glob"],
                    model="sonnet",
                ),
                "test-runner": AgentDefinition(
                    description="Runs and analyzes test suites.",
                    prompt="You are a test execution specialist.",
                    tools=["Bash", "Read", "Grep"],
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)
```

### 2.5 文件系统定义子代理（.claude/agents/目录）

```markdown
---
name: debugger
description: Use immediately when errors occur. Find root cause + minimal fix + verification.
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---

You are a debugging specialist.

## Process
1. Capture exact error + repro steps
2. Locate failing area
3. Implement minimal safe fix
4. Verify with tests
```

**注意**：程序化定义的代理优先级高于同名的文件系统代理。

### 2.6 子代理工具安全约束

- 子代理**不能**生成自己的子代理（不要给子代理分配Agent工具）
- `tools`（允许列表）精确控制能力
- `disallowedTools`（拒绝列表）从继承池中移除敏感工具
- 最小权限：审查代理只给Read/Grep/Glob，不给Write/Edit

### 2.7 子代理检测代码

```python
for block in message.content:
    if isinstance(block, ToolUseBlock) and block.name in ("Task", "Agent"):
        print(f"Subagent invoked: {block.input.get('subagent_type')}")
    if hasattr(message, "parent_tool_use_id") and message.parent_tool_use_id:
        print("  (running inside subagent)")
```

**兼容性**：旧版SDK使用 `"Task"` 工具名，新版使用 `"Agent"`，检测时需同时匹配。

---

## 三、Skills 自动化配置

### 3.1 SKILL.md 模板
```markdown
---
name: 代码格式化
description: 按照项目规范自动格式化代码
trigger: 用户提到"格式化"或"format"
priority: 5
---

# 代码格式化 Skill

## 步骤
1. 检测文件语言和类型
2. 读取项目格式化配置（.prettierrc / .editorconfig）
3. 应用格式化规则
4. 验证格式化结果
5. 报告变更摘要

## 约束
- 不修改代码逻辑
- 保留原有注释
- 遵循项目已有风格
```

### 3.2 Skills 生命周期
```
创建 → 测试 → 评估 → 精炼 → 分发 → 废弃
```
- **创建**：编写SKILL.md和配套文件
- **测试**：在隔离环境中验证
- **评估**：Rubric评分，检查触发准确性
- **精炼**：根据评估结果优化
- **分发**：提交仓库或通过plugins分发
- **废弃**：过时或低效的Skills标记废弃

### 3.3 Skills 与 Subagents 集成
- Skills可注入到自定义子代理中
- 子代理通过Skills获得领域专家能力
- 实现"子代理隔离 + Skills专业化"的双层架构

---

## 四、Hooks 自动化配置

### 4.1 Hook 类型
| Hook | 触发时机 | 用途 |
|------|---------|------|
| PreToolUse | 工具调用前 | 权限检查、参数校验 |
| PostToolUse | 工具调用后 | 结果验证、日志记录 |
| PreMessage | 消息发送前 | 内容审查、格式标准化 |
| PostMessage | 消息接收后 | 自动处理、路由判断 |

### 4.2 配置示例
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "delete|rm|format",
        "action": "confirm",
        "message": "检测到高风险操作，需要确认"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "write_file",
        "action": "validate",
        "message": "验证文件写入完整性"
      }
    ]
  }
}
```

---

## 五、MCP Server 自动化配置

### 5.1 标准MCP Server注册
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/workspace"],
      "tools": ["read_file", "write_file", "list_directory"],
      "resources": ["file:///workspace/**"],
      "prompts": ["code_review", "refactor"]
    }
  }
}
```

### 5.2 工具权限声明
每个MCP Server必须声明：
- **tools**：可执行的函数列表
- **resources**：可访问的数据源
- **prompts**：预构建的指令模板

---

## 六、CLAUDE.md 项目记忆配置

### 6.1 标准结构
```markdown
# 项目名称

## 技术栈
- 前端：React 18 + TypeScript
- 后端：Python FastAPI
- 数据库：PostgreSQL

## 编码规范
- 使用2空格缩进
- 函数命名使用驼峰式
- 每个文件不超过300行

## 常用命令
- `npm run dev` 启动开发服务器
- `npm test` 运行测试
- `npm run build` 构建生产版本

## 注意事项
- API密钥存储在.env文件中，不提交到Git
- 数据库迁移使用Alembic
```

### 6.2 自动更新策略
- 项目结构变更时更新技术栈
- 新增约定时补充编码规范
- 每次迭代后更新注意事项

---

## 七、Agent 生命周期管理

### 7.1 状态机
```
IDLE → RUNNING → WAITING → COMPLETED / FAILED
                      ↑__________|
```
- **IDLE**：等待任务分配
- **RUNNING**：执行任务中
- **WAITING**：等待用户输入或依赖完成
- **COMPLETED**：任务成功完成
- **FAILED**：任务失败，需人工介入

### 7.2 失败处理
| 失败类型 | 处理策略 |
|---------|---------|
| 工具调用失败 | 分析原因→调整参数→重试（上限2次） |
| 超时 | 检查点恢复→断点续传 |
| 权限不足 | 降级到更低权限操作→提示用户 |
| 依赖失败 | 等待依赖完成→超时后降级 |

---

> 核心法则：隔离上下文、声明权限、自动化配置、优雅降级。


---

## [更新日期: 2026-06-01] 子代理管理与自动化配置

> 来源：Anthropic Academy Subagents 课程 + Claude Code Harness 最佳实践 + Cowork 定时任务

### 1. Subagent 生命周期管理

```
┌──────────────────────────────────────────────────┐
│              Subagent 生命周期                     │
├──────────┬──────────┬──────────┬─────────────────┤
│  创建     │   执行    │   完成    │     终止         │
│ CREATED  │ RUNNING  │ COMPLETED│  TERMINATED     │
├──────────┼──────────┼──────────┼─────────────────┤
│ 定义职责  │ 分发任务  │ 精炼结果  │ 释放上下文窗口    │
│ 配置权限  │ 等待返回  │ 综合报告  │ 清理临时文件      │
│ 限定工具  │ 超时监控  │ 或：失败   │ 回收 token 配额   │
└──────────┴──────────┴──────────┴─────────────────┘
```

**生命周期四阶段**：

| 阶段 | 操作 | 关键配置 | 失败处理 |
|------|------|---------|---------|
| **创建** | 定义 description / tools / permissions | `name`、`description`（触发条件）、`tools`列表、`permissions`（read-only / read-write） | N/A |
| **执行** | 分发子任务，等待结果 | `timeout`（建议≤300s）、`max_iterations`（建议≤10） | 超时→降级或重试；失败→记录原因 |
| **完成** | 接收精炼结果，综合到主任务 | 结构化结果对象（状态码 + 发现 + 置信度） | 结果为空→标记为无发现 |
| **终止** | 释放上下文窗口资源 | 自动清理 | N/A |

### 2. Claude Code Subagent 配置方法

**基础配置**（`.claude/settings.json`）：
```json
{
  "subagents": {
    "code-explorer": {
      "description": "Search and analyze large codebases to find relevant files and patterns",
      "tools": ["Read", "Glob", "Grep"],
      "permissions": "read-only",
      "timeout": 120
    },
    "security-auditor": {
      "description": "Audit code changes for security vulnerabilities and OWASP Top 10 patterns",
      "tools": ["Read", "Glob", "Grep"],
      "permissions": "read-only",
      "timeout": 180
    },
    "test-generator": {
      "description": "Generate unit tests for specified modules or functions",
      "tools": ["Read", "Write", "Bash"],
      "permissions": "read-write",
      "timeout": 300,
      "max_iterations": 10
    }
  }
}
```

**配置要点**：
- `description`：决定何时触发，需精确描述职责
- `tools`：最小权限原则，只授予必需的工具
- `permissions`：探索类用 `read-only`，编辑类用 `read-write`（慎用）
- `timeout`：防止单个 Subagent 无限运行
- 路径限定：避免 Subagent 访问无关目录

### 3. 子代理与主代理的职责边界

| 维度 | 主 Agent（Orchestrator） | Subagent（Worker） |
|------|------------------------|-------------------|
| **职责** | 全局规划、任务分解、结果综合、最终编辑 | 专注单项调查/分析任务 |
| **权限** | 完整读写权限 | 最小化权限（优先只读） |
| **上下文** | 保持全局视图、跨子任务连贯 | 独立上下文窗口、不污染主会话 |
| **生命周期** | 整个会话持续存在 | 一次性、完成即终止 |
| **输出** | 综合报告 + 执行编辑 | 精炼发现（非完整对话记录） |
| **数量** | 1个 | 可并行多个（建议≤5个） |

**职责分离铁律**：
- 主 Agent **绝不**在同一会话中既做大规模搜索又做代码编辑
- 搜索/调查/审计 → 分发给只读 Subagent
- 编辑/写入/修改 → 由主 Agent 在掌握全局后执行
- 每个 Subagent 只返回**精炼的发现**，不返回完整对话历史

### 4. 自动化调度配置

#### 4.1 Cowork `/schedule`（定时任务）

**创建方式**：
```
在 Cowork 任务中输入：/schedule
然后描述：每天上午9点汇总过去24小时的Slack消息和邮件
```

**调度配置**：
```yaml
# ~/.claude/scheduled-tasks/daily-brief/SKILL.md
name: daily-brief
schedule: "0 9 * * *"    # 每天上午9点
description: 每日简报 - 汇总Slack消息、邮件和日历事件
```

**特点**：
- 在 Claude Desktop App 打开期间运行
- 电脑休眠时跳过，唤醒后自动补执行一次
- 每次运行产生独立的 Cowork 会话
- 可查看历史记录和跳过的运行

#### 4.2 `/loop`（循环任务）

```yaml
# ~/.claude/scheduled-tasks/code-review-loop/SKILL.md
name: code-review-loop
loop: "*/30 * * * *"     # 每30分钟
description: 定时扫描代码库变更，自动运行代码审查
```

**本地 vs 云端对比**：

| 特性 | 本地 `/loop` | 云端 Scheduled Tasks |
|------|------------|---------------------|
| 运行位置 | 本地机器 | Anthropic 云服务器 |
| 在线要求 | Desktop App 打开 | 无需本地在线 |
| 持久性 | App关闭则停止 | 24/7 跨设备持久 |
| MCP | 本地 MCP Server | Web 账号 MCP |
| 适用 | 文件系统依赖任务 | 纯 API / Web 任务 |
| 远程控制 | 不支持 | 手机端 Claude App 可监控 |

#### 4.3 调度最佳实践

| 实践 | 说明 |
|------|------|
| 间隔合理 | 避免过于频繁（建议 ≥5分钟），减少 token 消耗 |
| 幂等设计 | 任务应可安全重复执行，不会重复创建/发送 |
| 错误通知 | 失败后自动通知用户，而非静默跳过 |
| 结果归档 | 每次运行结果保存为独立文件，便于回溯 |
| 资源限制 | 单任务设置超时上限，防止失控 |

### 5. 多Agent并行编排与冲突检测

#### 5.1 并行编排策略

```
主Agent
  ├── 并行批次1：同时启动
  │   ├── Subagent A：安全审查（120s超时）
  │   ├── Subagent B：测试覆盖率分析（120s超时）
  │   └── Subagent C：代码风格检查（60s超时）
  │
  ├── 等待批次1全部完成
  │
  ├── 并行批次2：基于批次1结果
  │   ├── Subagent D：深度架构分析（180s超时）
  │   └── Subagent E：依赖风险扫描（90s超时）
  │
  └── 综合所有结果 → 生成统一报告
```

#### 5.2 冲突检测机制

| 冲突类型 | 检测方式 | 处理策略 |
|---------|---------|---------|
| **文件编辑冲突** | 两 Subagent 返回的编辑涉及同一文件 | 主 Agent 串行化处理，后编辑基于前编辑结果 |
| **资源锁冲突** | 数据库/文件系统并发写入 | 使用文件锁或数据库事务，先到先得 |
| **循环依赖** | Subagent A 结果触发 Subagent B，B 结果又触发 A | 设置最大级联深度（≤3层） |
| **权限冲突** | Subagent 尝试访问未授权资源 | 预检查权限，拒绝时记录并降级 |
| **结果冲突** | 两 Subagent 对同一问题给出矛盾结论 | 主 Agent 评估置信度 + 必要时启动裁决 Subagent |

#### 5.3 并行限制与保护

```
并行约束：
├── 单批次最多 5 个 Subagent 同时运行
├── 批次间必须等待上一批次全部完成
├── 总 Subagent 调用上限：20 次/会话
│
保护机制：
├── 超时熔断：单个 Subagent 超时自动终止
├── Token 预算：每个 Subagent 独立 token 上限
├── 降级策略：Subagent 失败时主 Agent 自行处理或跳过
└── 审计日志：记录所有 Subagent 调用及结果
```

---

> **核心法则**：隔离上下文、声明权限、自动化配置、优雅降级。Subagent 是工具不是目的——只在任务受益于独立上下文和并行执行时才使用。

---

## [更新日期: 2026-06-02] Subagent 完整配置手册（基于官方完整文档）

> 来源：Anthropic 官方 Subagents 文档 (code.claude.com/docs/zh-CN/sub-agents) · 2026-06-02

### 6. Subagent Frontmatter 完整字段规范

仅 `name` 和 `description` 必填，其他字段均为可选：

```yaml
---
name: code-reviewer              # 必填：小写字母+连字符，全局唯一
description: >                   # 必填：Claude 决定何时委派的依据
  Reviews code for quality and best practices.
  Use proactively after code changes.
tools: Read, Glob, Grep          # 允许列表（省略=继承所有）
disallowedTools: Write, Edit     # 拒绝列表（从继承池移除）
model: sonnet                    # sonnet/opus/haiku/inherit/完整ID
permissionMode: default          # default/acceptEdits/auto/dontAsk/bypassPermissions/plan
maxTurns: 10                     # 最大代理轮数
skills: [deep-review]            # 启动时预加载的 Skills
mcpServers: ["slack"]            # 可用的 MCP Servers
hooks: []                        # 生命周期 Hooks
memory: project                  # user/project/local 持久记忆范围
background: false                # true=始终后台运行
effort: high                     # low/medium/high/xhigh/max
isolation: worktree              # 空白=无隔离 / worktree=git worktree
color: green                     # red/blue/green/yellow/purple/orange/pink/cyan
initialPrompt: ""                # 作为主代理运行时自动提交的首条消息
---
```

### 7. 内置 Subagent 能力矩阵

| 内置 Agent | Model | Tools | 用途 | 加载 CLAUDE.md? | 加载 Git Status? |
|-----------|-------|-------|------|----------------|-----------------|
| **Explore** | Haiku | 只读 (R/G/G) | 文件发现/代码搜索/库探索 | ❌ | ❌ |
| **Plan** | 继承 | 只读 (R/G/G) | Plan Mode 代码库研究 | ❌ | ❌ |
| **General-purpose** | 继承 | 全工具 | 复杂多步操作/代码修改 | ✅ | ✅ |
| **statusline-setup** | Sonnet | 专用 | `/statusline` 配置 | N/A | N/A |
| **claude-code-guide** | Haiku | 专用 | Claude Code 功能问答 | N/A | N/A |

**Explore 彻底程度级别**：
- `quick`：快速定位查找
- `medium`：平衡的探索
- `very thorough`：全面分析

### 8. 五级 Subagent 范围优先级

```
优先级1（最高）：托管设置（组织管理员部署）
  → 覆盖所有下级同名定义
优先级2：--agents CLI 标志（仅当前会话）
优先级3：.claude/agents/（项目级，团队共享）
优先级4：~/.claude/agents/（用户级，个人所有项目）
优先级5（最低）：Plugin agents/ 目录
```

**命名冲突规则**：同名时高优先级覆盖低优先级，不警告。同范围同名时 Claude Code 保留一个丢弃另一个且无警告。

**Plugin 子代理特殊限制**（安全原因）：
- ❌ 不支持 `hooks` frontmatter
- ❌ 不支持 `mcpServers` frontmatter
- ❌ 不支持 `permissionMode` frontmatter
- 需要这些功能 → 复制到 `.claude/agents/` 或 `~/.claude/agents/`

### 9. Subagent 后台执行配置

| 场景 | 配置 | 效果 |
|------|------|------|
| 始终后台 | `background: true` | Subagent 始终在后台运行，不阻塞主对话 |
| 手动后台 | 运行时 `Ctrl+B` | 临时发送到后台 |
| 查看后台 | `/tasks` 命令 | 查看所有后台 Subagent 状态 |
| 默认前台 | `background: false` 或不设 | 等待完成后才继续 |

### 10. Worktree 隔离配置

```yaml
isolation: worktree  # Subagent 在临时 git worktree 中运行
```

**Worktree 行为**：
- 创建存储库的隔离副本
- 默认从 `default branch` 分支（非父会话 HEAD）
- Subagent 不进行任何更改时自动清理
- 适用于需要文件系统隔离的大规模重构

### 11. Subagent 记忆持久化

```yaml
memory: user     # ~/.claude/agent-memory/ 跨项目积累
memory: project  # 项目级持久记忆
memory: local    # 仅当前设备
```

**用途**：Subagent 在多次调用间积累见解（代码库模式、重复出现的问题），实现跨会话学习。

### 12. Subagent + Agent Teams 集成

Subagent 定义可作为 Agent Teams 的队友类型引用：

```
队友使用 Subagent 的 tools 和 model
定义的 body 作为额外指令附加到队友的系统提示
```

这实现了"配置一次，两处使用"：Subagent 既可被主对话直接委派，也可作为 Agent Teams 中的队友模板。

### 13. 工具限制的高级用法：限制可派生的 Subagent 类型

```yaml
# 协调代理：只能派发 worker 和 researcher 类型的子代理
tools: Agent(worker, researcher), Read, Bash

# 完全禁止派生子代理（不列出 Agent 工具）
tools: Read, Glob, Grep
```

`Agent(agent_type)` 语法限制主代理可以派发的子代理类型，防止代理链路失控。

---

## 新增第14节：Dynamic Workflows 子代理管理（2026-05-28）

### 14.1 动态工作流 vs 传统子代理对比
| 维度 | 传统子代理 | Dynamic Workflows |
|------|-----------|-------------------|
| 并发上限 | 个别（1-5个） | 16并发 / 1000总计 |
| 编排方式 | Prompt驱动 | JavaScript确定性脚本 |
| 可复用性 | 随对话消逝 | 脚本版本管理、跨项目复用 |
| 验证机制 | 手动审查 | 自动对抗验证循环 |
| Token消耗 | 正常 | 正常 × 3~50倍 |
| 状态持久 | 弱 | 断点恢复 |

### 14.2 编排脚本示例
```javascript
// Claude Dynamic Workflow 自动生成的编排脚本
const workflow = {
  name: "monorepo-migration",
  phases: [
    { name: "analyze", parallel: 10, task: "扫描模块依赖关系" },
    { name: "implement", parallel: 16, task: "按模块迁移代码" },
    { name: "verify", parallel: 16, mode: "adversarial", task: "对抗验证" },
    { name: "fix", parallel: 8, condition: "verify.failures > 0" }
  ]
};
```

### 14.3 子代理资源管理
- **并发限制**：默认 16 个并发，超出排队等待
- **运行上限**：单次工作流最多 1000 个子代理
- **独立上下文**：每个子代理拥有独立上下文窗口，互不干扰
- **结果聚合**：主编排器收集所有子代理结果，验证后合并输出

### 14.4 配置模式演进（结合 Harness 最佳实践）
```
阶段1：基础 CLAUDE.md（根目录放全局指针，子目录放局部约定）
阶段2：添加 Hooks（stop hook 自动反思 + start hook 动态加载上下文）
阶段3：Skills 按需加载（路径绑定，按子目录激活）
阶段4：LSP 集成（符号级导航，精确引用追踪）
阶段5：Plugins 打包分发（Skills+Hooks+MCP 统一安装）
阶段6：Dynamic Workflows（大规模并行子代理编排）
```

---

> **核心法则更新**：name 唯一、description 写触发条件、tools 最小权限、model 用 Haiku 省钱、background 不阻塞、isolation 保安全、workflow 编排脚本可复用。

---

## 十五、R45新增：子代理Skills工程化配置（2026-06-02）

> 来源：Anthropic内部数百Skills实践 + Claude Code Harness架构 2026

### 15.1 Skills九类分类体系

| # | 类型 | 典型应用 | 子代理适用 |
|---|------|---------|-----------|
| 1 | 库和API参考 | 内部库使用指南+边界情况 | ✅ 专项子代理 |
| 2 | 产品验证 | Playwright端到端测试 | ✅ 验证子代理 |
| 3 | 数据获取和分析 | 数据系统连接+监控 | ✅ 分析子代理 |
| 4 | 业务流程自动化 | 站会/工单/周报 | ✅ 自动化子代理 |
| 5 | 代码脚手架 | 按规范生成框架 | ✅ 脚手架子代理 |
| 6 | 代码质量和审查 | 对抗性审查+代码风格 | ✅ 审查子代理 |
| 7 | CI/CD和部署 | PR监控→构建→灰度→回滚 | ✅ 部署子代理 |
| 8 | Runbooks | 症状→多工具调查→报告 | ✅ 诊断子代理 |
| 9 | 基础设施运维 | 清理/审批/成本 | ✅ 运维子代理 |

### 15.2 子代理Skill配置规范

**Skill目录结构**：
```
.claude/skills/security-review/
├── SKILL.md          # 核心指令+YAML元数据
├── references/       # 按需加载的参考文档
│   ├── owasp.md
│   └── cve-patterns.md
├── scripts/          # 可执行脚本
│   └── scan.sh
└── assets/           # 模板文件
    └── report-template.md
```

**description字段规范**（决定子代理何时激活）：
- ✅ 好：`"Use when user requests security review of code changes or PR"`
- ❌ 差：`"A powerful skill that supercharges your security workflow"`

**Gotchas维护**：
- 记录Claude实际踩过的坑（非预测的坑）
- 每次遇到新edge case就补进去
- 信噪比最高的部分，优先维护

### 15.3 子代理工程化检查清单

| 检查项 | 标准 |
|-------|------|
| description | 写触发条件，不写功能摘要 |
| SKILL.md | 核心逻辑，不堆细节 |
| references/ | 有分层，细节按需加载 |
| Gotchas | 有实际踩坑记录 |
| 更新频率 | 跟得上模型迭代节奏 |
| 验证 | 7天内主动触发过 |

---

> 更新日期：2026-06-02 R45 | 新增：Skills九类分类+子代理配置规范+工程化检查清单

---

## 十六、R53新增：Claude Code 全栈自动化配置（2026-06-05）

> 来源：Anthropic 官方 Sub-Agents / Skills / Hooks / MCP / Agent Teams 完整文档 · 2026-06-05

### 16.1 Sub-Agent 定义格式（完整规范）

仅 `name` 和 `description` 必填，其他字段可选：

```yaml
---
name: security-reviewer             # 必填：小写字母+连字符，全局唯一
description: >                      # 必填：Claude 决定何时委派的依据
  Audits code changes for security vulnerabilities.
  Use proactively after code changes.
tools: Read, Glob, Grep             # 允许列表（省略=继承所有）
disallowedTools: Write, Edit        # 拒绝列表（从继承池移除）
model: sonnet                       # sonnet/opus/haiku/inherit/完整模型ID
permissionMode: default             # default/acceptEdits/auto/dontAsk/bypassPermissions/plan
maxTurns: 10                        # 最大代理轮数
skills: [deep-review]               # 启动时预加载的 Skills
mcpServers: ["slack"]               # 可用的 MCP Servers
hooks: []                           # 生命周期 Hooks
memory: project                     # user/project/local 持久记忆范围
background: false                   # true=始终后台运行
effort: high                        # low/medium/high/xhigh/max
isolation: worktree                 # 空白=无隔离 / worktree=git worktree
color: green                        # red/blue/green/yellow/purple/orange/pink/cyan
initialPrompt: ""                   # 作为主代理运行时自动提交的首条消息
---
Your system prompt body here.
```

**五级范围优先级**（高优先级覆盖低优先级）：
```
1. 托管设置（组织管理员部署）← 最高
2. --agents CLI 标志（仅当前会话）
3. .claude/agents/（项目级，团队共享）
4. ~/.claude/agents/（用户级，个人所有项目）
5. Plugin agents/ 目录 ← 最低
```

### 16.2 Skills 目录结构与 Frontmatter 字段

**目录结构**：

```
.claude/skills/
├── security-review/
│   ├── SKILL.md              # 核心指令 + YAML 元数据
│   ├── references/           # 按需加载的参考文档
│   │   ├── owasp.md
│   │   └── cve-patterns.md
│   ├── scripts/              # 可执行脚本
│   │   └── scan.sh
│   └── assets/               # 模板等资源文件
│       └── report-template.md
├── deploy/
│   └── SKILL.md
└── code-review/
    └── SKILL.md
```

**SKILL.md Frontmatter 完整字段**：

| 字段 | 说明 | 必填 |
|------|------|------|
| `name` | Skill 名称 | 是 |
| `description` | 描述（决定自动匹配触发） | 是 |
| `allowed-tools` | 预批准的工具列表 | 否 |
| `model` | 指定使用的模型 | 否 |
| `disable-model-invocation` | 禁止模型自动触发 | 否 |
| `user-invocable` | 是否允许用户手动 `/` 触发 | 否 |
| `argument-hint` | 参数提示 | 否 |
| `context` | `fork` 表示在 Subagent 中运行 | 否 |
| `agent` | 指定运行的 Subagent 类型 | 否 |

**三个存放位置**（启动时自动扫描）：
- 项目级：`.claude/skills/`
- 用户级：`~/.claude/skills/`
- 插件级：Plugin 内的 `skills/`

### 16.3 Hooks 配置与生命周期事件

**Hook 类型**：

| 类型 | 配置 | 说明 |
|------|------|------|
| **Command** | `type: "command"` | 执行 shell 命令，stdin/stdout 通信 |
| **HTTP** | `type: "http"` | HTTP POST 请求 |
| **MCP Tool** | `type: "mcp_tool"` | 调用已连接 MCP 服务器的工具 |
| **Prompt** | `type: "prompt"` | Claude 模型单轮评估，返回 yes/no |
| **Agent** | `type: "agent"` | 派生子代理验证条件（实验性） |

**完整生命周期事件**：

| 事件 | 触发时机 | Matcher |
|------|---------|---------|
| `SessionStart` | 会话开始或恢复 | `startup`/`resume`/`clear`/`compact` |
| `UserPromptSubmit` | 用户提交提示 | 不支持 |
| `PreToolUse` | 工具调用前 | 工具名/正则 |
| `PostToolUse` | 工具调用成功后 | 工具名/正则 |
| `PostToolUseFailure` | 工具调用失败后 | 工具名/正则 |
| `PostToolBatch` | 并行工具批次完成后 | 不支持 |
| `Stop` | Claude 完成响应时 | 不支持 |
| `SubagentStart` | 子代理派生时 | agent type |
| `SubagentStop` | 子代理完成时 | agent type |
| `SessionEnd` | 会话终止时 | `clear`/`resume`/`logout`/`other` |
| `TeammateIdle` | Agent Team 队友空闲时 | 不支持 |
| `TaskCreated` | 任务被创建时 | 不支持 |
| `TaskCompleted` | 任务完成时 | 不支持 |

**Hook 存放位置**：

| 位置 | 范围 | 可共享 |
|------|------|--------|
| `~/.claude/settings.json` | 所有项目 | 否 |
| `.claude/settings.json` | 单项目 | 是（可提交） |
| `.claude/settings.local.json` | 单项目 | 否（gitignored） |
| 管理策略设置 | 组织范围 | 管理员控制 |
| Plugin `hooks/hooks.json` | 插件启用时 | 是 |
| Skill/Agent frontmatter | 组件活跃时 | 是 |

### 16.4 MCP 三层扩展模型

| 层 | 配置者 | 分发方式 | 配置键 |
|----|--------|----------|--------|
| **Managed** | 管理员 | 组织策略推送 | `managedMcpServers` |
| **Org** | 管理员 | 系统目录分发 | `orgMcpServers` |
| **User** | 最终用户 | 应用内 UI | `mcpServers` |

**管理控制键**：

| 键 | 效果 |
|----|------|
| `isLocalDevMcpEnabled: false` | 禁止用户添加本地 MCP 服务器 |
| `isDesktopExtensionEnabled: false` | 禁止安装本地 `.mcpb` 桌面扩展 |
| `isDesktopExtensionSignatureRequired: true` | 拒绝未签名的 `.mcpb` 扩展 |
| `allowManagedHooksOnly: true` | 阻止用户/项目/插件 hooks |

**MCP 安全模型**：
- OAuth 和 headers-helper 认证
- 工具策略锁：`allow` / `ask` / `blocked`
- 插件签名验证

### 16.5 Agent Teams 配置与任务管理

**启用方式**：设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

**团队架构**：

| 组件 | 角色 |
|------|------|
| **Team Lead** | 创建团队、派生队友、协调工作 |
| **Teammates** | 独立 Claude Code 实例，各自处理任务 |
| **Task List** | 共享工作项，队友认领并完成 |
| **Mailbox** | 智能体间消息通信 |

**显示模式**：
- `in-process`：所有队友在主终端内，Shift+Down 切换
- `split-panes`：每个队友独立窗格（需 tmux 或 iTerm2）
- 默认 `auto`：tmux 会话中自动 split-panes，否则 in-process

**任务管理**：
- 任务三态：pending → in progress → completed
- 支持任务依赖：未解决的依赖阻塞认领
- 文件锁防竞争：多队友同时认领同一任务时安全处理

**质量门 Hooks**：
- `TeammateIdle`：队友即将空闲时运行，exit code 2 发送反馈
- `TaskCreated`：任务创建时运行，exit code 2 阻止创建
- `TaskCompleted`：任务完成时运行，exit code 2 阻止完成

### 16.6 项目目录结构最佳实践

```
项目根/
├── CLAUDE.md                    # 始终加载：技术栈、架构、约定
├── .claude/
│   ├── settings.json            # 项目级配置
│   ├── settings.local.json      # 本地覆盖（gitignored）
│   ├── agents/                  # 自定义 Sub-Agents
│   │   ├── security-reviewer.md
│   │   ├── code-explorer.md
│   │   └── test-generator.md
│   ├── skills/                  # 项目级 Skills
│   │   ├── deploy/
│   │   │   └── SKILL.md
│   │   ├── code-review/
│   │   │   ├── SKILL.md
│   │   │   ├── references/
│   │   │   │   └── style-guide.md
│   │   │   └── scripts/
│   │   │       └── check.sh
│   │   └── migrate/
│   │       └── SKILL.md
│   └── hooks/                   # Hook 脚本
│       ├── block-rm.sh
│       └── lint-check.sh
├── .mcp.json                    # MCP 服务器配置
└── .gitignore
```

**构建演进路径**：

```
阶段1：CLAUDE.md（项目宪法 + 关键约束）
  → 阶段2：Hooks（stop hook 反思 + start hook 加载上下文）
    → 阶段3：Skills 按需加载（路径绑定，按子目录激活）
      → 阶段4：LSP 集成（符号级导航，精确引用追踪）
        → 阶段5：Plugins 打包分发（Skills+Hooks+MCP 统一安装）
          → 阶段6：Dynamic Workflows（大规模并行子代理编排）
```

---

> 更新日期：2026-06-05 R53 | 新增：Sub-Agent 完整定义格式 + Skills 目录结构 + Hooks 生命周期 + MCP 三层模型 + Agent Teams 配置 + 项目目录最佳实践

---

## 十七、R58新增：CCA认证与子代理能力对标（2026-06-05）

> 来源：Anthropic CCA Foundations 认证体系 · 2026-06-05

### 17.1 认证五大领域与子代理配置对标

| CCA 领域 | 对应子代理配置重点 | AGENTS.md 已覆盖章节 |
|----------|-------------------|---------------------|
| Agentic Architecture | Subagent定义格式、Agent Teams配置、Dynamic Workflows | §1-2, §5-6, §16 |
| Claude Code | 七层Harness架构、项目目录结构 | §14-16 |
| Context Management | 上下文窗口隔离原则、渐进式披露 | §1-2, §9 |
| API Design Patterns | 四大API模式、多Agent协调流程 | USER.md §8 |
| Security & Governance | 最小权限原则、tools白名单、MCP安全模型 | §2-3, §13, §16.4 |

### 17.2 认证级子代理配置检查清单

- [ ] 所有子代理有精确的 `description`（写触发条件，非功能摘要）
- [ ] `tools` 使用最小权限（探索类只读，编辑类限定范围）
- [ ] 高风险子代理配置 `disallowedTools` 显式拒绝
- [ ] Subagent模型选择遵循成本铁律（Haiku→Sonnet→Opus梯度）
- [ ] Skills 目录结构规范（references/scripts/assets分层）
- [ ] Hooks 覆盖关键生命周期事件（PreToolUse拦截危险操作）
- [ ] MCP Server 权限声明完整（tools/resources/prompts三层）
- [ ] 项目根目录 CLAUDE.md ≤200行，专业知识外移到Skills

---

> 更新日期：2026-06-05 R58 | 新增：CCA认证与子代理配置对标+检查清单


---

## [更新日期: 2026-06-05] Dynamic Workflows 大规模子代理（基于 Opus 4.8）

> 来源：Anthropic Opus 4.8 Dynamic Workflows · Claude Code Harness 最佳实践 · 2026年

### 8. Dynamic Workflows 子代理编排

#### 8.1 大规模并行执行模型

```
Coordinator Agent（规划 + 分配）
    │
    ├── Worker Agent 1（模块A独立处理）
    ├── Worker Agent 2（模块B独立处理）
    ├── Worker Agent 3（模块C独立处理）
    ├── ...（可扩展至数千个）
    │
    ▼
Adversarial Agent（对抗证伪）
    │
    ▼
Cross-validator Agent（交叉验证）
    │
    ▼
Coordinator（结果汇总 + 集成测试）
```

**设计原则**：
- Worker 从队列主动认领任务（pull 而非 push）
- Worker 持久运行，跨任务积累上下文
- 各 Worker 独立执行，不共享中间发现
- 对抗验证 + 交叉验证形成双重保底

#### 8.2 超大规模作业的关键约束

| 约束 | 说明 |
|------|------|
| **模块独立** | 子任务间不能有运行时依赖或共享状态 |
| **结果可验证** | 每个子任务产出有明确的验收标准 |
| **冲突隔离** | 多个 Worker 不会编辑同一文件 |
| **成本可控** | Haiku 用于探索，Sonnet 用于分析，Opus 仅用于关键判断 |
| **超时保护** | 单个 Worker 设置超时上限，超时后降级标记 |

#### 8.3 Agent 类型与选型

| Agent 角色 | 推荐模型 | 核心能力 | 上下文策略 |
|-----------|---------|---------|----------|
| Coordinator | Opus 4.8 | 规划、分配、收束 | 全局视图，精炼接收 |
| Worker | Haiku/Sonnet | 独立执行子任务 | 独立上下文，隔离 |
| Adversarial | Sonnet/Opus | 证伪、挑错 | 读取 Worker 输出，对抗思考 |
| Cross-validator | Sonnet | 交叉对比、一致性检查 | 多 Worker 结果对比 |
| Integrator | Opus 4.8 | 合并、集成测试、报告 | 全量汇总 |

### 9. Plugins 打包分发机制

#### 9.1 Plugin 结构定义

```
plugin-name/
├── skills/           # Skills 集合
│   ├── skill-1/SKILL.md
│   └── skill-2/SKILL.md
├── hooks/            # Hooks 配置
│   ├── start-hook.sh
│   └── stop-hook.sh
├── mcp.json          # MCP Server 配置
├── CLAUDE.md         # 项目记忆
└── README.md         # 安装说明
```

#### 9.2 Plugin 价值

- **标准化分发**：新工程师第一天安装即拥有完整能力
- **部落知识显性化**：团队积累的最佳实践打包为可安装组件
- **环境一致性**：所有开发者使用相同的 Skills/Hooks/MCP 配置

### 10. LSP 集成子代理

#### 10.1 LSP 优势

在大型代码库中，传统 grep 搜索常见函数名可能返回几千条结果，Claude 需要逐个打开文件判断——LSP 只返回指向同一个符号的引用，过滤在读文件之前完成。

#### 10.2 LSP 子代理配置

```json
{
  "name": "lsp-explorer",
  "model": "haiku",
  "tools": ["Read", "Grep"],
  "mcpServers": [{
    "name": "typescript-lsp",
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-lsp", "--language", "typescript"]
  }]
}
```

### 11. Skills 路径绑定高级配置

#### 11.1 路径绑定语法

```markdown
---
name: payment-deploy
description: 支付团队部署流程
paths: ["src/payment/**", "deploy/payment/**"]
allowed-tools: ["Read", "Write", "Bash"]
---
```

**效果**：支付团队的安全审查 Skill 只在支付目录下激活，不会跑到别处干扰。

#### 11.2 Skills 优先级管理

| 优先级 | 使用场景 | 加载策略 |
|--------|---------|---------|
| 0~3 | 通用/低优先级 | 仅在明确匹配时加载 |
| 4~6 | 标准/中优先级 | 正常触发加载 |
| 7~9 | 关键/高优先级 | 强制加载（即使开销大） |
| 10 | 系统级 | 始终加载（谨慎使用） |

### 12. Hooks 自我进化配置

#### 12.1 Stop Hook 自动反思

**原理**：会话结束时，Stop Hook 自动捕获本次会话中暴露出的新模式/约定，建议更新 CLAUDE.md：

```bash
# .claude/hooks/stop/update-claudemd.sh
# 分析本次会话中新增的配置、模式、约定
# 自动生成 CLAUDE.md 更新建议
# 经人工确认后写入
```

#### 12.2 Start Hook 动态加载

**原理**：会话开始时，Start Hook 根据当前工作目录/项目类型，自动加载匹配的上下文模块，无需开发者手动配置：

```bash
# .claude/hooks/start/dynamic-context.sh
# 检测当前项目类型（React/Python/Go...）
# 自动加载对应项目的 CLAUDE.md 和 Skills
# 动态注入环境变量和路径映射
```

---

## [更新日期: 2026-06-10] Agent SDK 子代理 SDK 编程与四件套配置

> 来源：Anthropic 官方 Agent SDK 文档 · 2026-06

### Agent SDK 子代理编程方式（Python）

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs. Fix any issues.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
            agents={
                "reviewer": {
                    "description": "Reviews code for bugs and style issues",
                    "tools": ["Read", "Grep"]
                }
            }
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

### SDK 快速安装

```
# TypeScript
npm install @anthropic-ai/claude-agent-sdk

# Python
pip install claude-agent-sdk

# 环境变量
ANTHROPIC_API_KEY=your-api-key
# 或使用第三方提供商:
# Amazon Bedrock: CLAUDE_CODE_USE_BEDROCK=1
# Google Vertex AI: CLAUDE_CODE_USE_VERTEX=1
# Microsoft Azure:  CLAUDE_CODE_USE_FOUNDRY=1
```

### 四件套扩展栈配置速查

| 扩展方式 | 配置路径 | 触发方式 | 典型用途 |
|---------|---------|---------|---------|
| **Skills** | `.claude/skills/{name}/SKILL.md` | 自动匹配或 `/skill-name` | 领域知识、可重用工作流 |
| **Hooks** | `.claude/settings.json` 或 `hooks.json` | 事件触发（9种事件） | lint、安全验证、环境设置 |
| **Subagents** | `.claude/agents/{name}.md` 或 SDK `agents` 参数 | Agent 工具调用 | 隔离调查、代码审查、测试 |
| **MCP** | `.mcp.json` 或 `claude mcp add` | 工具调用 | 数据库、Figma、Notion 等外部服务 |
| **Plugins** | `/plugin install` | 安装后自动生效 | 社区和官方的打包功能 |
| **CLAUDE.md** | 项目根目录 `CLAUDE.md` | 每次对话启动加载 | 持久化全局指令和代码规范 |

### Skills 渐进式披露配置

```
skills/
  api-conventions/
    SKILL.md          # 第1层：启动时加载触发条件（YAML frontmatter）
    references/       # 第2层：激活时加载 SKILL.md 主体
      deep-dive.md    # 第3层：需要详细信息时加载
    examples/
      example.md      # 工作代码示例
```

**SKILL.md 模板**：
```yaml
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
```

### Hooks 九种事件类型

| 事件 | 触发时机 | 执行级别 |
|------|---------|---------|
| PreToolUse | 工具使用前 | block/suggest/warn |
| PostToolUse | 工具使用后 | suggest |
| SessionStart | 会话开始时 | 自动 |
| SessionEnd | 会话结束时 | 自动 |
| UserPromptSubmit | 用户提交提示时 | suggest |
| PreCompact | 压缩前 | 自动 |
| Notification | 显示通知时 | suggest |
| Stop | 用户停止时 | 自动 |
| SubagentStop | 子代理结束时 | 自动 |

### 子代理权限最小化模板

```yaml
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash     # 最小权限：只读 + 搜索
model: opus                       # 安全审查用最强模型
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling
Provide specific line references and suggested fixes.
```

### MCP 生产部署清单

| # | 最佳实践 | 说明 |
|---|---------|------|
| 1 | 有界上下文 | 每个 MCP 服务器围绕单一微服务域 |
| 2 | 无状态幂等 | 接受请求 ID，确定性输出 |
| 3 | 正确传输 | stdio（兼容性）+ 可流式 HTTP（网络部署），SSE 已弃用 |
| 4 | OAuth 2.1 | 自 2025-03 起 HTTP 传输强制要求 |
| 5 | 结构化输出 | LLM 可解析 + 人类可读 |
| 6 | 生产级检测 | 结构化日志、相关 ID、延迟、令牌成本 |
| 7 | 语义版本控制 | 重大变更时递增版本号 |
| 8 | 容器化交付 | 最小运行时镜像 + README + 示例

---

## 九、Agent Teams 团队协作深度（R76更新 · 2026-06-11）

> 来源：Anthropic 官方文档 code.claude.com/docs/en/agent-teams + Advanced Patterns Webinar

### 9.1 Agent Teams 架构

多个Claude子代理在共享文件系统上并行工作，主Agent作为编排器统一调度。每个子代理拥有独立上下文窗口，通过文件系统交换中间结果。

```
主Agent (Orchestrator)
  ├── 子代理A → 文件A → 精炼结果A
  ├── 子代理B → 文件B → 精炼结果B
  ├── 子代理C → 文件C → 精炼结果C
  └── 汇总 → 交叉验证 → 最终输出
```

### 9.2 子代理设计模式（官方课程提炼）

| 模式 | 说明 | 示例 |
|------|------|------|
| 结构化输出 | 强制子代理按指定JSON Schema返回结果 | 代码审查报告 |
| 障碍报告 | 子代理卡住时主动上报，不傻等 | 依赖缺失、权限不足 |
| 工具限制 | 限制子代理只能使用特定工具 | 安全审查只读 |
| 上下文精炼 | 子代理只返回关键信息，不返回完整执行日志 | 摘要而非过程 |
| 超时熔断 | 子代理超时自动终止，防止资源泄漏 | 长时间任务 |

### 9.3 /agents 命令完整配置

```yaml
---
name: code-reviewer
description: Reviews code for bugs, security issues, and style
tools: Read, Grep, Glob        # 最小权限
model: sonnet                  # 审查用性价比模型
skills:
  - security-audit             # 注入安全审查技能
---
You are a senior code reviewer. Report:
1. Bugs and logic errors (critical)
2. Security vulnerabilities (critical)
3. Style issues (optional)
Provide file paths and line numbers.
```

### 9.4 子代理生命周期管理

| 阶段 | Hook事件 | 动作 |
|------|---------|------|
| 创建 | PreToolUse | 权限检查 + 上下文预算分配 |
| 执行 | 持续监控 | 超时检测 + 障碍报告接收 |
| 完成 | SubagentStop | 结果校验 + 摘要提取 + 资源释放 |
| 异常 | SubagentStop(失败) | 日志记录 + 可选重试 |

### 9.5 子代理反模式（避免）

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| 过度拆分 | 子代理比任务本身还简单 | 合并小任务 |
| 全权委托 | 不给子代理足够约束 | 结构化输出+工具限制 |
| 忽略结果验证 | 盲目信任子代理输出 | 对抗验证+交叉检查 |
| 无限上下文 | 子代理塞入过多信息 | 渐进式披露+路径绑定 |
| 无超时机制 | 子代理卡死拖垮主流程 | 30秒/5分钟分级超时 |

### 9.6 MCP + 子代理组合模式

```
Claude Code 主 Agent
  ├── 子代理A（研究）：MCP连接文档库 + 网页搜索
  ├── 子代理B（编码）：Skills加载专业规范 + 文件系统读写
  ├── 子代理C（审查）：只读+安全Skills + 结构化输出
  └── 子代理D（测试）：MCP连接CI服务 + 测试框架
```

---

> 版本：v1.4 · R80迭代更新 · 2026-06-14
> 关联：[[Anthropic官方课程-390节全集]] v3.0


---

## 十、Agent Teams 管理与配置最佳实践（R76更新 · 2026-06-11）

> 来源：Claude Code v2.1.32 Agent Teams 官方文档 + Anthropic Academy Subagents 课程 + 社区实战

### 10.1 Agent Teams 启用方式

**方式一：settings.json（推荐，项目级共享）**
```json
{
  "experimentalAgentTeams": true
}
```

**方式二：环境变量（全局）**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**前置条件**：Claude Code v2.1.32+ / Opus 4.6 模型访问权限 / macOS 用户需 tmux 或 iTerm2

### 10.2 两种显示模式

| 模式 | 特点 | 适用场景 |
|------|------|----------|
| In-process | 队友嵌入当前终端，无并发显示 | 简单并行任务、不需要监控队友进度 |
| Split panes | 每个队友独立 tmux/iTerm2 面板 | 需要同时监控所有队友进度、快速介入 |

### 10.3 Agent Teams 黄金规模原则

**3-5个队友最优**：平衡并行收益与协调开销。超过5个队友协调成本指数增长，Token消耗线性翻倍。

**每个队友5-6个任务**：自包含的任务单元，产出清晰可交付成果。过多任务导致队友上下文爆炸，过少浪费实例资源。

### 10.4 成本管理速查

| 方案 | 模型 | 相对成本 | 典型场景 |
|------|------|---------|---------|
| 单会话 | Haiku/Sonnet | 1x | 日常任务 |
| Subagents | Sonnet | 1.5-3x | 聚焦并行任务 |
| Agent Teams (小) | Sonnet×2-4 | 3-8x | 模块化开发 |
| Agent Teams (大) | Opus×16 | 50-100x | 编译器级项目 |

**成本优化策略**：
1. 队友使用 Sonnet 而非 Opus（平衡成本与能力）
2. 控制团队规模：只在真正需要并行时增加队友
3. 精简启动提示词：队友自动加载 CLAUDE.md/MCP/Skills，避免重复
4. 及时清理团队：空闲队友消耗 Token
5. 参考：16个代理构建C编译器，约20,000 API费用

### 10.5 文件冲突避免策略

每个队友拥有不同的文件集，绝不多人同时编辑同一文件：

```
文件分区示例：
├── teammate-1: src/frontend/* (React组件)
├── teammate-2: src/backend/* (API端点)
├── teammate-3: src/database/* (迁移脚本)
└── teammate-4: tests/* (测试套件)
```

### 10.6 Hooks 质量门

在 settings.json 配置 hooks，在队友完成任务后强制执行规则：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "prettier --check ${CLAUDE_FILE_PATH} && eslint ${CLAUDE_FILE_PATH}"
        }]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [{
          "type": "command",
          "command": "python scripts/validate_output.py"
        }]
      }
    ],
    "Notification": [
      {
        "matcher": "Start|Stop",
        "hooks": [{
          "type": "command",
          "command": "osascript -e 'display notification "${CLAUDE_SUBAGENT_NAME} ${CLAUDE_HOOK_EVENT_TYPE}"'"
        }]
      }
    ]
  }
}
```

### 10.7 已知限制（v2.1.32）

| 限制 | 影响 | 建议 |
|------|------|------|
| In-process无会话恢复 | /resume和/rewind不恢复 | 关键任务用Split panes模式 |
| 任务状态滞后 | 队友进度显示延迟 | 手动检查队友输出 |
| 关闭缓慢 | 多队友清理耗时 | 耐心等待 |
| 每会话一个团队 | 不能嵌套Agent Teams | 复杂分解用Subagents做底层 |
| Lead不可转移 | 负责人固定 | 设计时明确Lead角色 |

### 10.8 龙虾体系Agent Teams配置模板

```json
// .claude/settings.json
{
  "experimentalAgentTeams": true,
  "agents": {
    "code-reviewer": {
      "description": "代码质量与安全审查专家",
      "tools": ["Read", "Grep", "Bash"],
      "model": "sonnet",
      "maxTurns": 8
    },
    "security-scanner": {
      "description": "安全漏洞扫描专用代理",
      "tools": ["Read", "Grep", "Bash"],
      "model": "sonnet",
      "maxTurns": 6
    },
    "test-auditor": {
      "description": "测试覆盖率与质量审计",
      "tools": ["Read", "Grep", "Bash"],
      "model": "haiku",
      "maxTurns": 5
    }
  }
}
```

---

---

## 十一、Hooks 25个生命周期事件全览（R75新增）

> 来源：yeyulingfeng.com · Claude Code 插件生态 2026年4月

### 11.1 四大类25个事件

| 类别 | 事件 | 触发时机 |
|------|------|----------|
| **Tool** | PreToolUse | 工具执行前拦截，可修改输入或阻止 |
| **Tool** | PostToolUse | 工具执行后自动验证/格式化 |
| **Tool** | PostToolUseFailure | 工具执行失败后处理 |
| **Session** | SessionStart | 会话开始时注入上下文（最近Issue/PR） |
| **Session** | SessionEnd | 会话结束时清理/归档 |
| **Session** | Stop | /exit 或 /quit 前触发 |
| **Session** | SubagentStart | 子代理创建时注入环境变量 |
| **Session** | SubagentStop | 子代理结束时验证产出 |
| **User** | UserPromptSubmit | 用户发送消息前预处理 |
| **User** | PreMessage | 消息发送前内容审查/格式标准化 |
| **User** | PostMessage | 消息接收后自动处理/路由判断 |
| **Notification** | Notification | 系统通知事件处理 |
| **Permission** | PrePermission | 权限请求前提醒 |
| **Permission** | PostPermission | 权限请求后跟踪 |
| **Lifecycle** | Checkpoint | 检查点自动备份时触发 |
| **Lifecycle** | PreCompact | /compact 执行前预处理 |
| **Lifecycle** | PostCompact | /compact 执行后注入摘要 |
| **Evolved** | EvolvedMessage | 消息演化事件 |
| **Evolved** | EvolvedUserTurn | 用户轮次演化事件 |
| **Evolved** | EvolvedAssistantTurn | 助手轮次演化事件 |
| **Agent** | AgentPreTask | 子代理执行任务前 |
| **Agent** | AgentPostTask | 子代理执行任务后 |
| **Agent** | AgentTaskPreAnnounce | 子代理任务公告前 |
| **Agent** | AgentTaskPostAnnounce | 子代理任务公告后 |
| **Agent** | AgentTeamsMailboxSend | Agent Team队友发送消息时 |

### 11.2 推荐Hook组合

| 场景 | Hook配置 |
|------|---------|
| 日常开发 | PostToolUse（auto-lint） + SessionStart（inject-context） |
| 安全关键项目 | PreToolUse（safety-guard） + PostToolUse（validate） + Checkpoint |
| CI/CD自动化 | SessionStart + PreToolUse + PostToolUseFailure + SessionEnd |

---

## 十二、插件生态管理（R75新增）

> 来源：yeyulingfeng.com · Anthropic 官方插件仓库

### 12.1 生态核心数据

| 指标 | 数据 |
|------|------|
| 官方市场插件 | 300个（含 Anthropic Verified 徽章） |
| 总安装量 | 446万次 |
| 增长周期 | 6个月从0到446万 |
| Top 1 插件 | frontend-design（50.7万安装） |
| Top MCP | Context7（24.8万安装，5.2万 Stars） |

### 12.2 Top 5 必装插件速查

| 排名 | 插件 | 安装量 | 一句话价值 |
|------|------|--------|-----------|
| 1 | frontend-design | 50.7万 | 告别"能跑但丑" |
| 2 | Superpowers | 41万 | 结构化开发全流程 |
| 3 | Context7 | 24.8万 | 实时框架文档，杜绝API幻觉 |
| 4 | code-review | 23.2万 | 自动安全/性能/风格审查 |
| 5 | github | 18.5万 | GitHub深度集成 |

### 12.3 插件安装命令

```bash
# 官方插件
/plugin install context7
/plugin install superpowers
/plugin install code-review

# MCP服务器
claude mcp add github --transport http
claude mcp add playwright --transport http
```

---

> **知识来源**：Claude Code 插件生态 v2026.04 / Anthropic Academy 课程体系 / 龙虾全域模板
> 版本：R75迭代更新 · 2026-06-11 20:30
> 关联：[[Anthropic官方课程-390节全集]] v12.0
*(内容由AI生成，仅供参考)*
*（内容由AI生成，仅供参考）*

---

## Anthropic官方课程知识同步（2026-06-12更新）

> 来源：Anthropic Academy 高级配置实践

### 十八、工具权限三级统一范式

已有子代理工具权限配置虽然提供了 `tools` 和 `disallowedTools` 字段，但在实践中应统一遵循三级权限范式：

| 级别 | 配置模板 | 角色类型 | 实例 |
|------|---------|---------|------|
| **L1 只读分析** | `tools: Read, Glob, Grep` | explorer, reviewer, auditor | security-reviewer, code-explorer |
| **L2 测试执行** | `tools: Read, Glob, Grep, Bash` + `disallowedTools: Write, Edit` | tester, analyzer | test-generator, coverage-analyzer |
| **L3 代码修改** | 继承全工具 | 主Agent编排器 | 仅主Agent拥有 |

**跨文件统一声明**（`.claude/settings.json`）：
```json
{
  "agentDefaults": {
    "L1_readonly": {
      "tools": ["Read", "Glob", "Grep"],
      "disallowedTools": ["Write", "Edit"],
      "model": "haiku"
    },
    "L2_testing": {
      "tools": ["Read", "Glob", "Grep", "Bash"],
      "disallowedTools": ["Write", "Edit"],
      "model": "sonnet"
    }
  }
}
```

**原则**：所有自定义子代理默认L1，按需提权。禁止任何子代理配置L3权限——编辑权归主Agent，这是只读/编辑分离铁律在配置层的体现。

### 十九、SDK定义 vs 文件系统定义 决策树

```
创建新子代理时的定义方式选择：

1. 该子代理是否仅用于当前项目？
   ├── 是 → 文件系统定义（.claude/agents/*.md）
   │   优势：团队共享、版本控制、code review
   │
   └── 否 → 继续

2. 该子代理是否需要在运行时动态配置？
   ├── 是 → SDK编程定义（agents参数）
   │   示例：根据用户输入动态调整子代理工具集
   │
   └── 否 → 继续

3. 该子代理是否需要跨项目复用？
   ├── 是 + 仅个人使用 → ~/.claude/agents/*.md（用户级）
   ├── 是 + 组织共享 → 托管设置推送
   └── 否 → .claude/agents/*.md（项目级）

4. 该子代理是否需要Plugin分发？
   ├── 是 → Plugin agents/ 目录
   │   注意：Plugin子代理不支持hooks/mcpServers/permissionMode
   └── 否 → 已覆盖
```

**对比总结**：

| 定义方式 | 适用场景 | 动态性 | 共享性 | 限制 |
|---------|---------|--------|--------|------|
| SDK `agents` 参数 | 运行时动态配置 | 高 | 低（代码内） | 需要编程能力 |
| `.claude/agents/*.md` | 项目级固定配置 | 低 | 高（Git管理） | 静态定义 |
| `~/.claude/agents/*.md` | 个人跨项目复用 | 低 | 低（个人） | 不团队共享 |
| Plugin `agents/` | 社区分发 | 低 | 高（市场分发） | 不支持hooks/MCP |

### 二十、MCP安全审计清单

| # | 检查项 | 风险等级 | 审计方法 |
|---|--------|---------|---------|
| 1 | MCP Server 是否有网络出站权限？ | 高 | 检查 args 中的网络相关参数 |
| 2 | 是否使用了 `npx -y` 自动安装？ | 中 | 审查 command 字段 |
| 3 | 工具策略是否配置了 `blocked` 列表？ | 高 | 检查 settings.json 的 mcpToolPolicy |
| 4 | OAuth 认证是否正确配置？ | 高 | HTTPS传输必须配置OAuth |
| 5 | 敏感数据是否可能通过MCP泄露？ | 高 | 审查 resources 配置的数据源范围 |
| 6 | MCP Server 是否来自信任源？ | 中 | 来源审查（官方/社区/内部） |
| 7 | 是否使用已弃用的SSE传输？ | 中 | 检查 transport 类型 |
| 8 | 管理端是否禁用了本地MCP？ | 组织级 | `isLocalDevMcpEnabled: false` |
| 9 | 桌面扩展是否要求签名？ | 高 | `isDesktopExtensionSignatureRequired: true` |
| 10 | 是否限制了用户自行添加MCP？ | 组织级 | managedMcpServers 覆盖 |

**分层安全策略**：
```json
{
  "managedMcpServers": { /* 组织级：管理员强制配置 */ },
  "orgMcpServers": { /* 部门级：推荐使用 */ },
  "mcpServers": { /* 用户级：个人选择 */ },
  
  "mcpToolPolicy": {
    "filesystem": {
      "delete_file": "blocked",
      "write_file": "ask",
      "read_file": "allow"
    }
  },
  
  "isLocalDevMcpEnabled": false,
  "isDesktopExtensionSignatureRequired": true
}
```

---

> 更新日期：2026-06-12 | 新增：三级权限统一范式 + SDK vs 文件系统定义决策树 + MCP 10项安全审计清单

## 十一、R18 新增：子代理全量配置手册（2026-06-12）

> 来源：Anthropic 官方 Agent SDK 文档 + Code With Seb 性能优化指南

### 11.1 子代理三种创建方式（更新）

| 方式 | 配置文件 | 适用场景 |
|------|---------|---------|
| 程序化 (agents 参数) | SDK 代码中 `AgentDefinition` | SDK 应用推荐，动态可调 |
| 文件系统 | `.claude/agents/*.md`（项目级）/ `~/.claude/agents/*.md`（用户级） | Claude Code 项目，团队共享 |
| 内置通用型 | Explore / Plan 自动触发 | 快速探索任务，无需定义 |

### 11.2 AgentDefinition 完整配置字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| description | string | **是** | 自然语言描述何时使用此代理（用于自动匹配） |
| prompt | string | **是** | 子代理的系统提示词 |
| tools | string[] | 否 | 允许的工具列表，省略则继承全部 |
| disallowedTools | string[] | 否 | 从继承工具中移除的工具 |
| model | string | 否 | 模型覆盖（sonnet/opus/haiku/inherit） |
| skills | string[] | 否 | 预加载的技能列表 |
| memory | string | 否 | 记忆来源（user/project/local） |
| mcpServers | array | 否 | MCP 服务器配置 |
| maxTurns | number | 否 | 最大轮次限制 |
| background | boolean | 否 | 是否作为非阻塞后台任务运行 |
| effort | string/number | 否 | 推理力度（low/medium/high/xhigh/max） |
| permissionMode | PermissionMode | 否 | 工具执行权限模式 |

### 11.3 子代理继承规则

**子代理收到**：
- 自己的系统提示词 (AgentDefinition.prompt)
- Agent 工具的提示字符串
- 项目级 CLAUDE.md（通过 settingSources 加载）
- 工具定义（继承自父代理或限制子集）

**子代理不收到**：
- 父代理的对话历史或工具结果
- 未在 skills 列表中列出的预加载技能内容
- 父代理的系统提示词

### 11.4 模型选择策略——节省 70% 成本

| Agent 角色 | 推荐模型 | 成本 | 原因 |
|-----------|---------|------|------|
| 编排者 (Orchestrator) | Opus | 高 | 需要最强的推理能力做任务分解 |
| 代码审查 (Reviewer) | Sonnet | 中 | 需要平衡分析能力和成本 |
| 探索搜索 (Explorer) | Haiku | 低 | 只读搜索，快速轻量 |
| 常规 Worker | Sonnet | 中 | 日常开发任务首选 |

**实际成本对比**：
- 全 Opus 方案：基准成本 100%
- 编排者 Opus + Worker Sonnet：约 30-40%（节省 60-70%）
- 编排者 Sonnet + Worker Haiku：约 15-20%（节省 80-85%）

### 11.5 内置子代理类型（更新）

| 类型 | 工具权限 | 模型 | 适用场景 |
|------|---------|------|---------|
| Explore 代理 | Glob/Grep/Read（只读） | Haiku | 代码库探索、架构分析 |
| Plan 代理 | 全部只读工具 | Sonnet | 方案设计、技术选型 |
| Bash 代理 | Bash/Read/Grep | Sonnet | 命令执行、测试运行 |
| Code 代理 | Edit/Write/Read/Grep/Glob | Sonnet | 代码编写与修改 |

### 11.6 子代理恢复机制

- 子代理完成后，Agent 工具结果包含 `agentId: <id>`
- 可通过 agentId 恢复子代理，保留完整对话历史
- Explore 和 Plan 为一次性代理，不返回 agentId
- 恢复时必须使用相同的 session（通过 resume 参数）

### 11.7 调试子代理失败

**启用调试模式**：
```json
{ "debug": true }
```

**常见失败模式与恢复**：
| 失败模式 | 原因 | 恢复策略 |
|---------|------|---------|
| 结果不完整 | 上下文被截断 | 减少输入数据量，分步处理 |
| 权限被拒 | 工具限制过严 | 检查 tools 配置，放宽必要权限 |
| 输出格式异常 | 系统提示词模糊 | 明确指定输出 schema 和格式要求 |
| 超时 | 任务过于复杂或模型太弱 | 拆分任务或升级模型 |

### 11.8 生产检查清单

**Agent 配置**：
- [ ] description 字段使用功能描述性名称
- [ ] prompt 包含明确的输入输出格式要求
- [ ] tools 权限最小化（按需分配，非全继承）
- [ ] 设置合理的 maxTurns 防止死循环

**成本控制**：
- [ ] Orchestrator 用 Opus，Worker 用 Sonnet/Haiku
- [ ] Explore 代理使用 Haiku 模型
- [ ] 无并行依赖的子任务同时派发

**错误处理**：
- [ ] 子代理 prompt 中包含异常处理与降级机制
- [ ] 配置 maxTurns 限制防止死循环
- [ ] 关键操作在 worktree 中隔离执行

**测试**：
- [ ] 子代理输出格式通过 schema 验证
- [ ] 权限配置在实际任务中验证有效
- [ ] 成本在预期范围内

---

## Anthropic官方课程R80同步：子代理管理与自动化配置

### Dynamic Workflows 配置
- 最低版本要求：Claude Code v2.1.154+
- 启用方式：/config → Dynamic workflows → On
- 支持平台：所有付费计划、Anthropic API、Amazon Bedrock、Google Vertex AI、Microsoft Foundry
- 脚本语言：JavaScript
- 存储位置：项目仓库内 .claude/workflows/ 目录

### Agent Teams 管理
- 创建命令：/agents create <name> --role <role>
- 监督命令：/agents supervise
- 上下文共享：通过共享文件或共享上下文窗口
- 人工介入点：在关键决策节点设置确认断点

### 六种扩展机制配置对比

| 机制 | 配置位置 | 触发方式 | 上下文成本 | 适用场景 |
|------|---------|---------|-----------|---------|
| MCP Servers | .mcp.json | 启动时加载 | 工具定义计 | 外部API/数据库 |
| Skills | SKILL.md | 按需触发 | 渐进式加载 | 领域知识复用 |
| Hooks | Hook配置 | 事件触发 | 零成本 | 确定性自动化 |
| Sub-Agents | Agent定义 | 被调用时 | 仅结果摘要 | 隔离子任务 |
| Agent Teams | /agents | 领导代理调度 | 共享上下文 | 多代理协作+监督 |
| Dynamic Workflows | .claude/workflows/ | 脚本驱动 | 仅脚本+摘要 | 大规模编排 |

### Claude Platform 101 关键配置（R80新增）
- API密钥管理：Workspace级别隔离
- 速率限制：按模型等级分层的并发限制
- 计费模型：按Token计费，支持预付费和后付费
- 模型选择策略：按任务复杂度匹配模型能力
- 安全最佳实践：密钥轮换、IP白名单、审计日志

### Anthropic官方课程R85同步：Agent SDK 子代理定义完整字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| description | string | 是 | 告诉 Claude 什么时候该用（触发条件，非摘要） |
| prompt | string | 是 | 系统提示词 / 行为规范 |
| tools | string[] | 否 | 可用工具（省略=继承父级） |
| disallowedTools | string[] | 否 | 显式禁用的工具 |
| model | string | 否 | sonnet / opus / haiku / inherit / 完整模型ID |
| background | boolean | 否 | 非阻塞后台任务 |
| maxTurns | number | 否 | 最大 agentic turn 数 |
| skills | string[] | 否 | 明确注入的技能列表 |

### 五种常用子代理类型（内置预设）

| 类型 | 用途 | 推荐模型 | 可用工具 |
|------|------|---------|---------|
| Explore | 快速搜索代码库（速度最快） | Haiku | Read、Grep、Glob |
| Bash | 执行终端命令、git 操作 | Sonnet | Bash |
| code-reviewer | 代码审查 | Sonnet | Read、Grep、Glob、Bash |
| general-purpose | 通用多步骤任务 | Sonnet | 全部工具 |
| Plan | 设计实现方案（不含写入） | Opus | 全部（不含写入） |

### 子代理上下文注入三种方式对比

| 方式 | 机制 | 何时使用 | 关键配置 |
|------|------|---------|---------|
| Skills 注入 | 在定义中指定 skills 字段 | 专用技能传递 | agent.skills = ["skill-name"] |
| Memory 持久化 | 子代理拥有持久记忆目录 | 长期经验积累 | 配置 memoryDir |
| 工具访问控制 | tools/disallowedTools 精细控制 | 安全隔离 | 最小权限原则 |

### Plugins 打包与市场分发

**Plugin 打包单元**：Skills + Hooks + MCP 配置 + Subagents 定义 → 一个可分发的 `.claude-plugin` 包

**分发路径**：
```
小团队 → 提交 repo .claude/skills/
规模化 → 内部 Plugin Marketplace
社区 → sandbox（自然生长）→ traction → 官方 Marketplace
```

### 全局与项目级配置标准

```
~/.claude/
  ├── settings.json       # 全局配置
  ├── skills/             # 全局技能
  ├── hooks/              # 全局钩子
  ├── agents/             # 全局子代理定义
  └── mcp.json            # 全局 MCP 配置

项目/.claude/
  ├── settings.json       # 项目配置（覆盖全局）
  ├── skills/             # 项目特定技能
  └── agents/             # 项目特定子代理
```

> 同步自：Anthropic官方课程390节全集 R85 | 2026-06-14


---

### R83 增量 (2026-06-15)

#### Agent SDK订阅额度配置

自2026年6月15日起，Agent SDK使用独立月度额度，需在Claude账户中一次性选择加入：

| 计划 | 月度SDK额度 | 适用场景 |
|------|-----------|---------|
| Pro | $20 | 个人实验与小规模自动化 |
| Max 5x | $100 | 中强度Agent工作负载 |
| Max 20x | $200 | 高强度多Agent编排 |
| Team标准 | $20/席位 | 团队协作基础 |
| Team高级 | $100/席位 | 团队级Agent自动化 |
| Enterprise | $20-$200/席位 | 企业级部署 |

**配置注意**：
- 额度按用户隔离，不可共享
- 每月刷新，不结转
- 超出后转入额外使用（需先启用）
- 大规模生产自动化仍建议用API密钥按量付费

#### Dynamic Workflows配置规范

**环境变量**：
```bash
# 方式一
export ANTHROPIC_WORKFLOW=1

# 方式二
export CLAUDE_CODE_ENABLE_WORKFLOW=true
```

**版本要求**：
- 基础Workflow：Claude Code V2.1.47+
- Dynamic Workflows完整功能：V2.1.154+
- 触发关键词：`ultra work`

**脚本持久化配置**：
```bash
# 持久化目录（默认临时目录仅3天生命周期）
~/.claude/workflows/

# 纳入版本控制
git add ~/.claude/workflows/my-workflow.js
```

**Skill分发配置**：
在Skill文件夹中包含JavaScript工作流文件，在SKILL.MD中引用：
```markdown
## Workflows
- `workflows/triage.js` — 自动分类和路由工作流
```

提示Claude将Skill中的工作流当作模板而非逐字执行的脚本，以获得更好的灵活性。

#### 六种编排模式配置速查

```javascript
// 流水线（Pipeline）
stages: [
  { id: "step1", agents: [...] },
  { id: "step2", dependsOn: ["step1"], agents: [...] }
]

// 扇出聚合（Fan-out）
stages: [{ id: "fanout", parallel: true, agents: [...] }]

// 对抗验证（Adversarial）
agents: [
  { id: "executor", prompt: "执行任务..." },
  { id: "verifier", prompt: "用怀疑态度验证executor的输出..." }
]

// 锦标赛（Tournament）
// N个agent两两比较，决出胜者

// 循环直到完成（Loop）
// while (!done) { spawn agent; check stop condition; }
```

#### 子代理权限与安全配置 (R83强化)

**隔离级别**：
- `worktree`：独立Git worktree，操作互不污染（推荐用于代码修改）
- `session`：共享会话但独立上下文
- `managed`：托管模式，主Agent完全控制

**工具权限粒度**：
```
子Agent可配置的工具集示例：
- 代码审查Agent: ["Read", "Glob", "Grep"]（只读 + 搜索）
- 代码修复Agent: ["Read", "Write", "Edit", "Bash"]（读写 + 执行）
- 分类Agent: ["Read", "Glob"]（只读）
```

**对抗验证安全原则**：
1. 验证Agent的提示必须配置为"怀疑模式"
2. 验证Agent不能读写执行Agent的工作区
3. 验证失败时自动触发重新执行或人工介入

#### 部署清单 (R83)

- [ ] Agent SDK月度额度已申领（如适用）
- [ ] ANTHROPIC_WORKFLOW环境变量已设置
- [ ] Claude Code版本≥V2.1.154
- [ ] 可复用Workflow脚本已迁移至~/.claude/workflows/
- [ ] Workflow脚本已纳入版本控制
- [ ] 每个子Agent已配置独立的工具权限和token预算
- [ ] 对抗验证Agent已配置怀疑模式提示
- [ ] 循环工作流已设置明确的停止条件

