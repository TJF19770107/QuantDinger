---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_780664b0685111f1a0095254002afed2
    ReservedCode1: DlI1ZWJZLB/Fmxtx178+OFhcpQ/McZZvtqsKVfHqs71v/0td36VzSJJXUkkrRi5S+yEGZzPDSE5oAvm/vDvWg+zhB70SpsHdaQtUSjXV+xToB5JhRBSPY5oXOY8nfILRj4YX0DqazbvzuUDVNZhk8G0+7DeipBszeWvkEIhrf95J8bZB6xT+8UgqiG4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_780664b0685111f1a0095254002afed2
    ReservedCode2: DlI1ZWJZLB/Fmxtx178+OFhcpQ/McZZvtqsKVfHqs71v/0td36VzSJJXUkkrRi5S+yEGZzPDSE5oAvm/vDvWg+zhB70SpsHdaQtUSjXV+xToB5JhRBSPY5oXOY8nfILRj4YX0DqazbvzuUDVNZhk8G0+7DeipBszeWvkEIhrf95J8bZB6xT+8UgqiG4=
---

# USER.md — 多 Agent 协作流程与任务拆解

> 基于 Anthropic 官方课程（Subagents / Agent Skills / Claude Cowork）提炼
> 更新：2026-06-16 第三轮循环

---

## 一、四模式协作架构

多 Agent 系统有四种协作模式，按复杂度递增：

```
Subagent 委派 → Agent Teams → Workflow 编排 → Skills + Hooks 自动化
     ↓                ↓              ↓                ↓
  简单任务分配    专业团队协作    流程引擎驱动    自适应触发
```

### 模式 1: Subagent 委派（基础模式）

**适用场景**：主 Agent 需要执行独立、可隔离的子任务

**配置方式**（CLAUDE.md）：
```markdown
## Subagents
- name: code-reviewer
- description: Reviews code changes for quality and security
- path: .claude/subagents/code-reviewer.md
```

**协作流程**：
```
用户请求 → 主 Agent 拆解 → 创建子 Agent 实例
         → 子 Agent 独立执行 → 结果汇总 → 主 Agent 呈现
```

**关键原则**：
- 子代理拥有独立上下文窗口（不污染主对话）
- 子代理不可修改主 Agent 的 System Prompt
- 子代理故障不影响主 Agent

### 模式 2: Agent Teams（团队协作）

**适用场景**：多专业领域并行协作

**团队结构**：
| 角色 | 职责 | 示例 |
|------|------|------|
| Orchestrator | 任务拆解与调度 | 主 Agent |
| Specialist A | 领域专精任务 | 前端代码生成 |
| Specialist B | 领域专精任务 | 后端 API 设计 |
| Reviewer | 质量审查 | 代码审查与安全审计 |

**协作协议**：
1. Orchestrator 接收用户请求
2. 拆解为并行子任务（无依赖 → 并行 / 有依赖 → 串行）
3. 分配子任务给对应 Specialist
4. Reviewer 检查所有子任务产物
5. Orchestrator 汇总并呈现最终结果

### 模式 3: Workflow 编排（流程引擎）

**适用场景**：固定流程的多步骤任务

**编排方式**：
```
                     ┌─────────────┐
用户输入 → [验证] →  │ Agent A     │ → [检查] → 终审 → 输出
                     │ Agent B     │
                     └─────────────┘
```

**Hooks 驱动的质量门控**：
```
PreToolUse  → 验证工具调用合法性
PostToolUse → 检查输出质量与一致性
OnError     → 触发降级或人工介入
```

### 模式 4: Skills + Hooks 自动化（自适应模式）

**适用场景**：根据任务上下文自动匹配能力

**配置结构**：
```
.claude/
├── CLAUDE.md          # 主配置（项目约定、Subagent 定义）
├── skills/
│   ├── code-review/SKILL.md     # 代码审查技能
│   ├── api-design/SKILL.md      # API 设计技能
│   └── doc-writer/SKILL.md      # 文档撰写技能
├── hooks/
│   ├── pre-commit.md            # 提交前钩子
│   └── security-check.md        # 安全检查钩子
└── mcp/
    └── mcp-config.json          # MCP 服务配置
```

**自动匹配流程**：
```
用户请求 → Claude 分析上下文 → 匹配相关 Skills
         → 加载匹配的 SKILL.md → 注入领域指令 → 执行
         → Hooks 在关键节点自动触发 → 审计/验证
```

---

## 二、任务拆解矩阵

### 拆解决策树

```
收到用户请求
│
├─ 单领域、单文件？
│   └─ 直接执行（无需子代理）
│
├─ 单领域、多文件？
│   └─ 创建 1 个子代理并行处理
│
├─ 多领域、可并行？
│   └─ 创建 N 个子代理并行执行
│
├─ 多领域、有依赖？
│   └─ 串行编排：Agent A → Agent B → Agent C
│
└─ 跨系统集成？
    └─ MCP + Subagents 混合模式
```

### 并行调度规则

| 条件 | 策略 | 原因 |
|------|------|------|
| 无数据依赖 | 并行 | 效率最大化 |
| 无状态依赖 | 并行 | 独立上下文窗口 |
| 无安全依赖 | 并行 | 互不影响 |
| 有 UI 状态变化 | 串行 | 避免竞态 |
| 有文件写入冲突 | 串行 | 保证一致性 |
| 有级联风险 | 串行 | 故障隔离 |

### 上下文传递协议

子代理间传递信息时遵循：
1. **最小必要原则**：仅传递任务所需信息
2. **结构化格式**：使用 Markdown 结构化字段
3. **来源标注**：标记信息权威等级
4. **不覆盖安全规则**：禁止传递越权指令

---

## 三、Claude Cowork 协作循环

### Task Loop（任务循环）

```
1. UNDERSTAND → 分析用户意图与上下文
2. PLAN       → 制定执行计划
3. EXECUTE    → 调用工具执行
4. VERIFY     → 验证执行结果
5. REPORT     → 向用户呈现
6. LEARN      → 更新知识/记忆
```

### 多步工作引导原则

- **显式确认**：高风险操作前暂停
- **渐进式执行**：先试点 → 验证 → 全量
- **回滚路径**：每次变更记录回滚方案
- **状态透明**：用户可追踪当前进度

---

## 四、Skills 配置模板

### 基础 Skill 结构
```markdown
---
name: task-name
description: When to use this skill
triggers:
  - keyword-1
  - pattern-*
scope: project|global
priority: high|medium|low
---

# Skill Title

## Instructions
...

## Tools
...

## Examples
...
```

### Hooks 事件类型
| 事件 | 触发时机 | 用途 |
|------|---------|------|
| PreToolUse | 工具调用前 | 权限验证、参数校验 |
| PostToolUse | 工具调用后 | 结果审计、副作用检查 |
| OnSessionStart | 会话开始时 | 上下文初始化 |
| OnSessionEnd | 会话结束时 | 清理、摘要生成 |
| OnError | 异常发生时 | 降级、通知 |

---

## 五、MCP 集成规范

### 服务注册
```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["-m", "mcp_server_db"],
      "env": {"DB_URL": "..."}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem"]
    }
  }
}
```

### 工具使用协议
- Tool → 执行操作（write/deploy/send）
- Resource → 读取数据（read/query/list）
- Prompt → 模板提示（format/template）

---

> 设计哲学：多 Agent 不是简单地把任务分给多个 LLM，而是精心设计的协作协议、故障隔离和信任边界。
> 来源：Anthropic Academy Subagents/Agent Skills/Claude Cowork 课程 + Claude Code 官方文档
*（内容由AI生成，仅供参考）*

---

## 六、五种协调模式选择决策树（2026-06-15 第3轮更新）

> 来源：Anthropic 官方博客 Multi-agent coordination patterns (2026-04-10)

### 6.1 模式与任务特征映射矩阵

| 任务特征 | Generator-Verifier | Orchestrator-Subagent | Agent Teams | Message Bus | Shared State |
|---------|:---:|:---:|:---:|:---:|:---:|
| 输出质量>速度 | ✅ 核心场景 | — | — | — | — |
| 有明确评估标准 | ✅ 必须 | — | — | — | — |
| 任务分解清晰 | — | ✅ 前提 | ✅ 要求独立 | — | — |
| 子任务短且无依赖 | — | ✅ 最佳 | — | — | — |
| 需要持久化上下文 | — | ❌ 每次重置 | ✅ 核心优势 | — | ✅ 共享存储 |
| 多步自主执行 | — | ⚠️ | ✅ | — | ✅ |
| 工作流不可预知 | — | ❌ 需预定义 | — | ✅ 核心场景 | — |
| Agent生态增长 | — | ⚠️ | ✅ | ✅ 天然支持 | ✅ |
| 需相互发现构建 | — | ❌ 编排器瓶颈 | ❌ 队友隔离 | ⚠️ | ✅ 核心场景 |
| 消除单点故障 | — | ❌ 编排器即单点 | ⚠️ | ❌ 路由即单点 | ✅ 核心优势 |

### 6.2 龙虾 Agent 体系对应

| Anthropic 模式 | 龙虾已实现 | 实现方式 |
|---------------|:---:|---------|
| Generator-Verifier | ✅ | SafeGuard v5.0 验证钩子 (PreToolUse/PostToolUse 双重审计) |
| Orchestrator-Subagent | ✅ 主要模式 | dispatch_task + 线性派发 + 结果验收 |
| Agent Teams | ✅ 部分 | 并行 dispatch_task（同轮无依赖多Sub Agent） |
| Message Bus | ⚠️ 规划中 | 协议#251 Orchestrator编排 + 未来事件总线 |
| Shared State | ⚠️ 规划中 | 协议#247 持久化任务看板 + 协议#248 记忆宫殿索引 |

### 6.3 龙虾系统协作模式选择决策树

```
用户请求
│
├─ 需要质量验证？ → Generator-Verifier（SafeGuard审计+反馈循环）
│
├─ 单Agent可完成？ → 直接执行（Level 0-2）
│
├─ 多子任务清晰可分解？
│   ├─ 短任务+无依赖 → Orchestrator-Subagent（dispatch_task 并行）
│   └─ 需持久化上下文 → Agent Teams（inherit_agent_id 延续）
│
├─ 多个Agent生态需松耦合？ → Message Bus（未来协议#251扩展）
│
└─ 需Agent互相发现+共同构建？ → Shared State（协议#247+#248支撑）
```

### 6.4 反应式循环防护

Shared State 模式的核心风险——反应式循环防护清单：

1. **时间预算**：每个写作/研究循环设置硬性时间上限
2. **收敛阈值**：N轮无新发现自动终止
3. **写入差异度**：新写入内容与已有内容相似度>阈值则抑制
4. **全局窗口**：设置全局最大Token/轮次上限
5. **关闭Agent**：指定一个"仲裁Agent"判定存储是否已包含足够答案

---

## 七、Dynamic Workflows 工作流模式（第4轮学习·R86新增）

> **来源**：Anthropic 官方 Claude Code Docs "Workflows" (2026) + 官方博客

### 7.1 何时使用 Workflow 而非传统派发

| 判断维度 | 使用 dispatch_task (传统) | 使用 Dynamic Workflow |
|---------|------------------------|---------------------|
| 任务规模 | 1-10 个子代理 | 数十至数百个代理 |
| 执行时长 | 分钟级 | 小时至天级 |
| 可重复性 | 单次执行 | 需保存为可复用命令 |
| 质量要求 | 基本正确 | 需交叉验证+反驳收敛 |
| 编排确定性 | LLM 推理逐轮调整 | 脚本确定性执行 |

### 7.2 Workflow 触发方式

| 方式 | 命令 | 适用场景 |
|------|------|---------|
| 关键词触发 | `ultracode: <任务描述>` | 单次大型任务 |
| 模式切换 | `/effort ultracode` | 全会话所有任务自动 Workflow |
| 内置命令 | `/deep-research <问题>` | 交叉验证研究 |
| 已保存命令 | `/<command-name>` | 复用已验证的编排脚本 |

### 7.3 Workflow 最佳实践（七条）

| # | 实践 | 说明 |
|---|------|------|
| 1 | **小范围试跑再全量** | 先跑一个目录/窄问题，确认脚本质量和成本 |
| 2 | **工具白名单预配置** | 避免长运行中因权限提示中断 |
| 3 | **模型分层选择** | 编排阶段用最强模型，执行阶段用经济模型 |
| 4 | **脚本版本化** | 保存到 `.claude/workflows/`（项目级）或 `~/.claude/workflows/`（个人级） |
| 5 | **监控 `/workflows` 面板** | 实时查看 Agent 计数、Token 消耗、阶段耗时 |
| 6 | **暂停再恢复** | 运行中可按 `p` 暂停，同会话可恢复（已完成 Agent 结果缓存） |
| 7 | **脚本审计** | 运行时脚本写入 `~/.claude/projects/`，可阅读/编辑/对比 |

### 7.4 龙虾体系路由决策更新

```
任务到达
│
├─ 规模 ≤ 10 子代理，分钟级 → dispatch_task（传统派发）
│   └─ 模式选择见第六节决策树
│
├─ 规模 10-100+ 子代理，小时级 → Dynamic Workflow
│   ├─ 需交叉验证 → /deep-research
│   ├─ 需代码审查/迁移 → ultracode: <任务>
│   └─ 全会话 → /effort ultracode
│
└─ 规模 100-1000 子代理，天级 → 持久化 Workflow
    └─ 保存为 /command，配合 resume
```

---

## Anthropic 多Agent协作流程

> 来源：Anthropic Agent SDK + 5 Subagent Patterns (2026.06)
> 更新：2026-06-15

### 五大子代理模式
1. **分而治之** — 父拆解→N子并行→汇总（20文件摘要成本节省86%）
2. **专家路由** — 分类→专项子代理（各有独立Prompt+工具列表）
3. **并行研究** — 多角度同时调查→合成报告
4. **评判-迭代** — Writer→Judge→修订（最多3轮）
5. **错误恢复** — 捕获错误→Debugger子代理→隔离调试

### 硬约束
- 最大并行: 8-12 | 最大深度: 2层 | 模型: Haiku轻/Sonnet核/Opus慎
- 工具最小化: 摘要器不给bash，翻译器不给web_search
- 返回格式: `{result, citations?, confidence}`

### 长期运行驾驭
初始化Agent(feature_list+init.sh) → 编码Agent(每次会话一个功能+git+progress)


---

## 第六章：Managed Agents 多Agent会话流程（第三轮新增）

> **数据来源**：docs.anthropic.com/en/docs/managed-agents/multi-agent + platform.claude.com/cookbook
> **更新**：2026-06-16 第三轮循环

### 6.1 Coordinator-Thread 模型详解

Multiagent sessions 的核心是 **Coordinator-Thread** 架构：

```
┌─────────────────────────────────────┐
│         Primary Thread              │
│   (Session-level Event Stream)     │
│                                     │
│  Coordinator Agent                 │
│  ┌─────┐  ┌─────┐  ┌─────┐        │
│  │ T1  │  │ T2  │  │ T3  │  ...   │
│  └─────┘  └─────┘  └─────┘        │
│     ↑        ↑        ↑            │
│  Agent1   Agent2   Agent3          │
│  (独立线程)(独立线程)(独立线程)      │
└─────────────────────────────────────┘
```

**关键机制**：
- **Primary Thread**：协调者汇报活动的主线程，浓缩显示所有子线程的事件
- **Sub-Threads**：每个 agent 运行在自己的 session thread 中，拥有独立对话历史
- **Thread Persistence**：协调者可向之前调用的 agent 发送跟进消息，agent 保留所有之前轮次的记忆

### 6.2 Shared Sandbox 机制

所有 agent 共享以下资源：

| 共享资源 | 说明 |
|---------|------|
| **Sandbox** | 共享代码执行环境和文件系统 |
| **Filesystem** | 所有 agent 可读写同一文件系统 |
| **Vault Credentials** | Session 创建时的 vault_ids 适用于所有 threads |

**不共享的资源**：
| 隔离资源 | 说明 |
|---------|------|
| **Tools** | 每个 agent 使用自己定义的工具集 |
| **MCP Servers** | Agent-scoped，每个 agent 声明自己的服务器 |
| **Context** | 独立上下文窗口，不共享对话历史 |
| **Model** | 每个 agent 独立配置模型和系统提示 |

### 6.3 Vault Credential 共享机制

- Vault credentials 在 session 创建时通过 `vault_ids` 指定
- 所有 threads 共享同一套 vault credentials（session-scoped）
- Redis、Snowflake 等外部服务凭据一键接入所有 agent
- 安全边界：credentials 不跨 session 泄露

### 6.4 三模式编排实战操作

#### Parallelization（并行化）

```
Coordinator:
  ├─ Agent A: 搜索 arXiv 论文
  ├─ Agent B: 搜索 GitHub 代码库
  └─ Agent C: 搜索行业报告
  → 综合三个来源的结果 → 输出统一报告
```

**适用**：独立数据源搜索、多个独立文件分析、代码+安全并行审查

#### Specialization（专业化）

```
Coordinator:
  ├─ Security Agent: 安全审计（OWASP top 10）
  ├─ Documentation Agent: 生成 API 文档
  └─ Test Agent: 生成边界测试用例
  → 每个 agent 只做自己最擅长的事
```

**适用**：多角色协作、领域专家路由、不同质量视角独立检验

#### Escalation（升级）

```
Coordinator (Haiku):
  └─ 遇到复杂架构决策 → Escalate to Opus Agent
  → Opus Agent 深度推理 → 返回决策建议
```

**适用**：差异化模型成本控制、子问题复杂度分级、按需使用昂贵模型

### 6.5 配置 Checklist

```
□ 所有 agent 需要 managed-agents-2026-04-01 beta header
□ Coordinator 需要 agent_toolset_20260401 工具类型
□ multiagent.agents 列表最多 20 个唯一 agent
□ 每个 agent 的 tools 按角色限定（最小权限）
□ vault_ids 在 session 创建时指定
□ MCP server 按 agent 独立配置
□ 验证子 agent 的 tools 白名单不会越权
```

---

## 第七章：Plugin 安装与分发工作流（第三轮新增）

> **数据来源**：code.claude.com/docs/zh-CN/plugins + docs.anthropic.com/zh-CN/docs/claude-code/plugins-reference
> **更新**：2026-06-16 第三轮循环

### 7.1 独立配置 vs Plugin 模式选择矩阵

| 需求 | 推荐方案 | 原因 |
|------|---------|------|
| 单项目快速定制 | 独立配置（`.claude/`） | 零开销、即时生效 |
| 个人跨项目复用 | 用户级 Plugin | 一次安装全局可用 |
| 团队标准化 | 项目级 Plugin + Git 版本控制 | 统一版本、自动同步 |
| 社区公开分享 | Plugin Marketplace 发布 | 标准化分发渠道 |
| 企业管控 | Managed Plugin（只读） | 管理员控制版本和安全 |

### 7.2 `/plugin-name:skill` 命名空间机制

```
独立配置：
  /hello          → 简短直接，仅当前项目可用

Plugin 模式：
  /my-plugin:hello  → 命名空间隔离，跨项目不冲突
  /pdf-tools:merge  → 多插件共存，各管各的命名空间
```

**命名空间规则**：
- Plugin 安装时，所有 `/name` 被自动映射为 `/plugin-name:name`
- 防止不同插件间的 skill/command 名称冲突
- 用户可在 `settings.json` 中为常用插件配置简短别名

### 7.3 创建插件完整工作流

```bash
# 1. 初始化插件目录
mkdir my-plugin
cd my-plugin

# 2. 创建 plugin.json 清单
cat > plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My custom plugin",
  "skills": "./skills/",
  "agents": "./agents/"
}
EOF

# 3. 添加 Skill
mkdir -p skills/hello
cat > skills/hello/SKILL.md << 'EOF'
---
name: hello
description: Greet the user with a friendly message
---
Say hello to the user in a friendly manner.
EOF

# 4. 本地测试
claude --plugin-dir ./my-plugin

# 5. 发布到 Marketplace（可选）
claude plugins publish ./my-plugin
```

### 7.4 Plugin 安装范围

| 范围 | 命令 | 配置文件 | 用例 |
|------|------|---------|------|
| User | `claude plugins install <plugin> --scope user` | `~/.claude/settings.json` | 个人全局 |
| Project | `claude plugins install <plugin> --scope project` | `.claude/settings.json` | 团队 Git 控制 |
| Local | `claude plugins install <plugin> --scope local` | `.claude/settings.local.json` | 个人项目特定 |
| Managed | 管理员推送 | Managed settings | 企业管控（只读） |

### 7.5 依赖管理

Plugin 可声明对其他插件的依赖：
```json
{
  "dependencies": [
    "helper-lib",
    {"name": "secrets-vault", "version": "~2.1.0"}
  ]
}
```

- 安装主插件时自动解析并安装依赖
- 版本约束遵循 SemVer（`~2.1.0` = `>=2.1.0 <2.2.0`）
- 循环依赖检测自动报错

---

## 第八章：Claude Cowork 项目协作完整流程（第三轮新增）

> **数据来源**：anthropic.com/learn/courses（Introduction to Claude Cowork 课程）
> **更新**：2026-06-16 第三轮循环

### 8.1 Cowork 任务循环

Claude Cowork 是 Anthropic 的协作式工作任务循环课程，覆盖：

| 模块 | 内容 |
|------|------|
| **Task Loop** | 理解任务 → 探索代码库 → 执行变更 → 验证结果 → 迭代改进 |
| **Plugins & Skills** | 用插件和 Skills 扩展能力，实现标准化工作流 |
| **File Workflows** | 大规模文件处理、批量操作、格式转换 |
| **Research Workflows** | 代码库探索、文档分析、多源信息综合 |
| **Steering Multi-step Work** | 安全引导多步骤工作、人机协同决策点 |

### 8.2 文件夹组织最佳实践

```
project/
├── .claude/
│   ├── settings.json          # 项目设置
│   ├── agents/                 # Subagent 定义
│   │   ├── code-reviewer.md
│   │   └── test-creator.md
│   ├── commands/               # 自定义命令模板
│   │   ├── prd.md
│   │   └── deploy.md
│   ├── skills/                 # 项目 Skills
│   │   └── db-migration/
│   │       └── SKILL.md
│   └── hooks/                  # 自动化钩子
│       └── hooks.json
├── CLAUDE.md                   # 项目上下文
├── CLAUDE.local.md             # 个人笔记（.gitignore）
└── src/                        # 源代码
```

### 8.3 API 集成标准化流程

```
1. 确定外部服务 → 选择 CLI 工具（gh/aws/gcloud）
2. 安装 CLI → 验证认证 → 测试基本命令
3. 在 CLAUDE.md 中声明可用 CLI 工具
4. 设置 MCP Server（如需复杂集成）
5. 创建 Skill 封装常用 API 操作模式
6. 在 Hooks 中添加自动化检查（PreCommit lint）
```

### 8.4 MCP 协议标准化

MCP (Model Context Protocol) 三大原语：

| 原语 | 说明 | 示例 |
|------|------|------|
| **Tools** | 模型控制的动作 | 查询数据库、发送 API 请求 |
| **Resources** | 应用控制的只读数据 | 配置文件、文档库 |
| **Prompts** | 预定义指令模板 | "审查这段代码"、"生成测试" |

Claude Code 中 MCP 集成步骤：
```bash
# 添加 MCP server
claude mcp add <server-name> <command>

# 列出已配置的服务器
claude mcp list

# 测试连接
# 在 Claude 会话中直接使用 MCP 工具
```

### 8.5 Hooks 自动化流水线

**核心事件节点**：

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `SessionStart` | 会话启动 | 加载项目上下文、检查依赖 |
| `UserPromptSubmit` | 用户提交提示 | 输入验证、敏感信息过滤 |
| `PreToolUse` | 工具调用前 | 权限检查、参数校验 |
| `PostToolUse` | 工具调用后 | 结果验证、自动格式化 |
| `PreCommit` | Git 提交前 | lint 检查、测试运行 |
| `PostCompact` | 上下文压缩后 | 关键信息保留验证 |
| `SessionEnd` | 会话结束 | 清理临时文件、生成摘要 |

**四种钩子类型**：
- `command`：执行 Shell 脚本
- `http`：发送 Webhook 通知
- `prompt`：LLM 评估
- `agent`：运行 agentic 验证器

---

> **版本更新声明**
> 更新：2026-06-16 第三轮循环
> 本轮新增：Managed Agents 多Agent会话流程（Coordinator-Thread模型、Shared Sandbox、Vault凭证共享、三模式编排）、Plugin 安装与分发工作流（命名空间机制、创建-测试-发布全流程）、Claude Cowork 项目协作完整流程（文件夹组织、API集成、MCP标准化、Hooks自动化）
> 情报来源：docs.anthropic.com/managed-agents + code.claude.com/plugins + anthropic.com/learn/courses
