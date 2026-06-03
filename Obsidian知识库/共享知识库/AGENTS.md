# AGENTS.md — 子代理管理与自动化配置

> 来源：Anthropic官方课程提炼 · 2026-06-01
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
