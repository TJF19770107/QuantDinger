# AGENTS.md — 子代理管理与自动化配置

> **版本**：v2.0 | **来源**：Anthropic Academy + Claude Code Subagents 文档 | **同步日期**：2026-05-31
> **本副本所属**：豆包AI Agent / Hermes Agent / OpenClaw Agent

---

## 一、Sub Agent 清单

| Agent ID | Agent Name | 职责域 | 状态 | 路由关键词 |
|----------|-----------|--------|------|-----------|
| file-agent | File Agent | 文件搜索/读写/格式转换/归类 | ACTIVE | 文件/文档/图片/PDF/搜索/整理 |
| computer-agent | Computer Agent | Windows系统/设置/窗口/进程 | ACTIVE | 系统/设置/窗口/桌面/进程/性能 |
| app-agent | App Agent | 应用操作/APK/小程序/Steam | ACTIVE | App/APK/应用/软件/小程序/Steam/EXE |
| browser | Browser Agent | 网页交互/登录/填表 | ACTIVE | 登录/填表/网页操作 |
| search-agent | Search Agent | 深度搜索/调研/对比 | ACTIVE | 调研/对比/论文/深度搜索 |

---

## 二、dispatch_task 规范化模板

### 2.1 标准调用格式

```
dispatch_task(
    agent_name="<目标Agent>",
    task="
<overall_goal>
用户原始完整需求（直接复述或等价压缩）
</overall_goal>
<current_task>
本次委托具体任务（自包含、可独立执行、结果导向）
</current_task>
",
    memory_ids=["<相关历史消息memory_id>"],
    inherit_agent_id="<继承的历史Agent ID或留空>"
)
```

### 2.2 task 编写纪律

| 规则 | 正确示例 | 错误示例 |
|------|---------|---------|
| 附件透传 | `<attachments>...</attachments>` 原样拼入 current_task | 忽略附件或改写路径 |
| 精简性 | 仅写目标+路径+约束 | 复制大段历史内容到 task |
| 结果导向 | "将照片按年份归类到子文件夹" | "先列目录，再读EXIF..." |

---

## 三、Sub Agent 能力边界

### 3.1 File Agent
**能做**：搜索/读写/格式转换/归类/上传
**不能做**：系统设置、应用操作、网页交互

### 3.2 Computer Agent
**能做**：系统设置/信息查询/窗口管理/进程管理
**不能做**：第三方应用操作、文件搜索

### 3.3 App Agent
**能做**：App操作/APK管理/小程序/Steam/应用推荐
**不能做**：系统管理工具、纯文件操作

### 3.4 Browser Agent
**能做**：网页交互/登录/填表
**不能做**：纯网页内容读取（应用 web_fetch）

### 3.5 Search Agent
**能做**：深度搜索/调研/对比分析
**不能做**：本地请求、简单事实查询

---

## 四、自动化配置

### 4.1 定时任务规则

```
定时任务 → 主 Agent 直接执行
    ├─ 提醒类 → 直接输出提醒文本
    ├─ 生成类 → 调用工具生成产物
    └─ 操作类 → 调用工具完成操作

禁止：创建/修改定时任务、追问时间频率
```

### 4.2 静默执行配置

| 配置项 | 值 |
|--------|-----|
| 中间日志 | 不输出 |
| 弹窗确认 | 禁止（除非高危操作） |
| 完成通知 | 简洁摘要表格 |
| 运行模式 | 后台静默 |

---

## 五、Anthropic Subagent 配置体系（v2.0 新增）

### 5.1 Subagent 定义格式

每个 Subagent 使用 **YAML Frontmatter + Markdown Body** 格式：

```yaml
---
name: code-reviewer           # 唯一标识符（小写字母+连字符）
description: Reviews code     # Claude 何时委托给此 Subagent
tools: Read, Glob, Grep       # 允许的工具列表（省略=继承全部）
disallowedTools: Write, Edit  # 禁止的工具列表
model: sonnet                 # 模型：sonnet/opus/haiku/inherit
permissionMode: acceptEdits   # 权限模式
maxTurns: 20                  # 最大代理轮数
skills:                       # 预加载的 Skills
  - api-conventions
mcpServers:                   # MCP 服务器限定
  - github
hooks:                        # 生命周期 Hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
memory: project               # 持久内存：user/project/local
background: false             # 是否始终后台运行
effort: high                  # 努力级别
isolation: ""                 # isolation: worktree 隔离模式
color: blue                   # 显示颜色
---
```

### 5.2 Subagent 五级范围

| 优先级 | 范围 | 存储位置 | 管理方式 |
|--------|------|---------|---------|
| 1 (最高) | Managed | 组织部署 | 管理员统一分发 |
| 2 | CLI Flag | `--agents` JSON | 当前会话临时定义 |
| 3 | Project | `.claude/agents/` | Git 版本控制、团队共享 |
| 4 | User | `~/.claude/agents/` | 个人跨项目复用 |
| 5 (最低) | Plugin | Plugin `agents/` | 第三方分发 |

### 5.3 内置 Subagent 类型

| 类型 | 模型 | 工具 | 用途 |
|------|------|------|------|
| **Explore** | Haiku (快速) | 只读 | 代码搜索/文件发现/代码库探索 |
| **Plan** | 继承主对话 | 只读 | Plan Mode 下收集上下文 |
| **General-purpose** | 继承主对话 | 全部 | 复杂多步任务/代码修改 |

### 5.4 权限模式

| 模式 | 行为 |
|------|------|
| `default` | 标准权限检查 |
| `acceptEdits` | 自动接受工作目录的文件编辑 |
| `auto` | 后台分类器审查命令 |
| `dontAsk` | 自动拒绝权限提示 |
| `bypassPermissions` | 跳过权限检查（谨慎使用） |
| `plan` | 只读探索模式 |

### 5.5 龙虾体系 Subagent 类型映射

| Anthropic 类型 | 龙虾对应 | 说明 |
|---------------|---------|------|
| Explore | file-agent (搜索模式) | 只读快速搜索 |
| Plan | search-agent | 规划前收集上下文 |
| General-purpose | file-agent (读写模式) | 复杂文件操作 |
| Custom (User) | app-agent / browser | 用户自定义专业 Subagent |
| Custom (Project) | computer-agent | 项目级系统操作 Agent |

---

## 六、Anthropic Hooks 生命周期（v2.0 新增）

### 6.1 Subagent 生命周期事件

| 事件 | 匹配器 | 触发时机 |
|------|--------|---------|
| `SubagentStart` | Agent type name | Subagent 开始执行 |
| `PreToolUse` | Tool name | Subagent 使用工具前 |
| `PostToolUse` | Tool name | Subagent 使用工具后 |
| `SubagentStop` | Agent type name | Subagent 完成执行 |

### 6.2 Hooks 注入位置

```
Subagent 生命周期
    │
    ├── SubagentStart Hook (settings.json 中定义)
    │
    ├── PreToolUse Hook (Subagent frontmatter 中定义)
    │   └── 验证命令/阻止危险操作
    │
    ├── [Agent 执行核心任务]
    │
    ├── PostToolUse Hook (Subagent frontmatter 中定义)
    │   └── Lint/格式化/后处理
    │
    └── SubagentStop Hook (settings.json 中定义)
        └── 清理/日志/通知
```

---

## 七、异常处理

| 异常 | 处理策略 |
|------|---------|
| Sub Agent 超时 | 主 Agent 降级执行或告知用户 |
| Sub Agent 结果不完整 | 寻找其他 Agent 补缺口 |
| 路由错误 | 重新派发给正确 Agent |
| 权限不足 | 告知用户，提供替代方案 |
| 依赖缺失 | 自动安装依赖后重试 |

---

> **参考来源**：Anthropic Academy 13门课程、Claude Code Subagents 文档（Frontmatter/Hooks/权限/五级范围）、Agent Teams 文档
