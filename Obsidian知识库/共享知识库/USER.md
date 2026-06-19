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

## 九、Dynamic Workflows：大规模并行协作模式

> 来源：Anthropic 2026-06-03 发布 | 面向 Max/Team plan 用户

### 9.1 模式定义

Dynamic Workflows 是多Agent协作的第五种模式——**自动规模化并行**：

```
模式 5: Dynamic Workflows（自动规模化并行）
适用场景：超大规模任务，可拆分为 10+ 独立并行子任务
触发方式：直接描述复杂任务，Claude 自动拆解
依赖要求：Max / Team plan
```

### 9.2 执行流程

```
用户：迁移项目从 Express 到 FastAPI
          │
          ▼
    ┌─────────────────────────┐
    │  Claude 主Agent（编排器）│
    │  自动拆解任务            │
    └───────┬─────────────────┘
            │
    ┌───────┼───────┬───────┬───────┐
    ▼       ▼       ▼       ▼       ▼
 [路由]  [控制器] [模型]  [测试]  [文档]
 Sub 1   Sub 2   Sub 3   Sub 5   Sub N
    │       │       │       │       │
    └───────┴───────┴───────┴───────┘
            │ 结果汇总
            ▼
    主Agent 审核关键决策 → 呈现最终结果
```

### 9.3 与现有四种模式的对比

| 维度 | Subagent委派 | Agent Teams | Workflow编排 | Skills+Hooks | Dynamic Workflows |
|------|:---:|:---:|:---:|:---:|:---:|
| 子代理数量 | 1-3 | 3-5 | 固定流程 | 0（自动触发） | **10-100+** |
| 任务拆分 | 手动 | 手动 | 预定义 | 不需要 | **自动** |
| 并行度 | 低 | 中 | 流程定义 | 事件驱动 | **极高** |
| 人工介入 | 每步可选 | 关键节点 | 检查点 | 自动 | **仅关键决策** |
| 适用规模 | 小任务 | 中型项目 | 固定流程 | 日常自动化 | **超大规模** |

### 9.4 最佳实践

**何时使用**：
- 代码跨语言/跨框架大规模迁移
- 全量API接口重构
- 多模块独立开发
- 批量测试用例生成

**何时避免**：
- 子任务间存在复杂依赖关系
- 需要频繁人工决策的创意性工作
- 小型任务（传统Subagent更高效）

### 9.5 人工介入策略

```
默认自动化执行 → 仅以下情况介入：
  1. 架构级决策（如技术选型变更）
  2. 安全敏感操作（如数据库迁移）
  3. 子代理执行失败需要重新规划
  4. 最终结果审核
```

---

## 十、Skills 链式编排与 Generator→Evaluator 循环

### 10.1 链式编排六步法

```
Step 1: 规划定义 → SPEC.md
Step 2: 技能选择 → 匹配技能列表
Step 3: 外部连接 → MCP/Proxy 配置
Step 4: Generator→Evaluator 验证循环 → 通过/失败日志
Step 5: 状态交接 → NOTES.md + Files API
Step 6: 链入下一步 → 迭代至完成
```

### 10.2 Generator→Evaluator 协作模式

这是 Anthropic 推荐的质量保证核心模式：

```
┌──────────┐    产物     ┌──────────┐
│ Generator │ ─────────→ │ Evaluator│
│  (生成器) │            │ (评估器) │
└──────────┘            └────┬─────┘
                             │
                    通过阈值？──→ 链入下一步
                    未通过？────→ 修复循环或人工介入
```

**关键约束**：
- Generator 和 Evaluator 使用**独立上下文窗口**
- Evaluator 从零重新推导检查条件（不继承 Generator 推理）
- 每次验证产生独立日志，支持可追溯审计

### 10.3 实操示例：内容生产流水线

```
brief → draft → SEO检查 → slides → exec summary PDF
  │       │        │         │          │
  │       │     Evaluator   │     Evaluator
  │    Evaluator 检查元数据  │     检查摘要准确性
  │    检查覆盖度            │
  └─────── 每个产出物经过独立验证 ──────┘
```

### 10.4 npx 技能安装协作流程

2026年新技能安装体系简化了团队协作配置：

```bash
# 团队成员只需执行一条命令即可获得相同技能
npx skills add claudeception
npx skills add op7418/NanoBanana-PPT-Skills

# 无需手动管理文件，无需重启，全局生效
```


---

## 十一、Agent SDK 集成协作模式（第5轮学习·R92新增）

> 来源：platform.claude.com Agent SDK Python 参考

### 11.1 协作模式选型：query() vs ClaudeSDKClient

| 协作特征 | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| 一次任务·独立会话 | ✅ 天然匹配 | ❌ 生命周期开销 |
| 多轮对话·上下文累积 | ⚠️ 需 `resume` | ✅ 自动累积 |
| 大规模并行 | ✅ 无状态即并行 | ❌ 需管理多个客户端 |
| 长期项目·持续协作 | ❌ 每次重建上下文 | ✅ 会话复用 |
| 团队共享状态 | 需 Files API 中转 | 需外部持久化 |

**集成原则**：团队协作场景下，`query()` 用于独立可并行的微任务分发（如"每人审一个模块"），`ClaudeSDKClient` 用于需要累积上下文的长对话（如"本周需求迭代对话"）。

### 11.2 会话生命周期管理

```python
from claude import ClaudeSDKClient, SessionQuery

# 按项目过滤——多项目环境中精准定位协作会话
sessions = client.list_sessions(SessionQuery(directory="/project-A"))
for s in sessions:
    msgs = client.get_session_messages(s.id)
    # 分析协作轨迹：谁在何时做了何决策
```

**协作价值**：
- `list_sessions()` → 团队 Agent 协作审计（谁做了什么）
- `get_session_messages()` → Agent 执行历史回放（为什么这样做）
- `continue_conversation=True` → 跨会话任务延续（断点续传）

### 11.3 自定义 MCP 工具的团队共享

```python
@tool("query_database", "安全查询生产数据库（只读）", {"sql": str})
async def query_db(args):
    # 沙箱执行，仅允许 SELECT
    ...

server = create_sdk_mcp_server("team-db", tools=[query_db])
```

**设计原则**：
- MCP 工具即 API 合约——定义后团队成员调用同一接口
- `create_sdk_mcp_server()` 进程内服务器 → 零网络依赖的内联协作
- Vault credential 共享 → 所有 Agent 用同一凭据访问外部服务
> 更新：2026-06-16 第四轮循环
> 本轮新增：Dynamic Workflows 大规模并行协作模式（第5种协作模式、自动拆解-并行执行-关键决策审核）、Generator→Evaluator 验证循环协作模式、Skills 链式编排六步法、npx 技能安装协作流程


---

## 五、多Agent协调五大模式（Anthropic 2026年4月官方指南）

### 5.1 上下文中心分解方法论
多Agent系统的价值在于特定场景，而非默认选择。核心判断标准：
- **不要按"做什么工作"分解，要按"需要什么上下文"分解**
- 上下文重叠的子任务用一个Agent，上下文隔离的子任务用多个Agent

### 5.2 五大协调模式速查

| 模式 | 架构 | 适用场景 | 通信方式 |
|------|------|---------|---------|
| Sequential Pipeline | A→B→C 链式 | 文本翻译→润色→排版 | 数据传递 |
| Parallel Fan-out | 中央→多Worker并发 | 同时分析多个文档 | 独立上下文 |
| Orchestrator-Worker | 主Agent调度子Agent | 复杂代码审查 | 结构化任务 |
| Agent Debate | 多Agent辩论收敛 | 高风险决策 | 对抗验证 |
| Swarm Autonomy | 自组织、无中央控制 | 大规模并行探索 | 共享黑板 |

### 5.3 Skills / MCP / Subagents / RAG 决策口诀
- 打包可复用程序 → Agent Skills
- 连接外部系统 → MCP
- 需要专业化并行 → Subagents（注意协调成本）
- 检索密集型 → RAG

---

## 六、Agent Teams 实战操作手册（R89新增）

> 来源：Anthropic 官方 Agent Teams 文档 + Claude Code Best Practices
> 更新：2026-06-16 第四轮循环

### 6.1 启动 Agent Team

```bash
# 自然语言描述即可，Claude 自动创建团队
"I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles:
one teammate on UX, one on technical architecture, one playing devil's advocate."
```

### 6.2 四种协作流程

#### 流程 A：探索-计划-编码-提交（最佳实践标准流）

```
Explore (Plan Mode) → Plan (生成蓝图) → Implement (Edit Mode) → Commit (PR)
```

每阶段产出物：研究摘要 → 实现计划 → 代码+测试 → PR描述

#### 流程 B：并行研究审查

```
Team Lead 创建研究任务
  ├── Teammate A: 调查方案X的可行性
  ├── Teammate B: 调查方案Y的可行性
  └── Teammate C: 对抗验证（Devil's Advocate）
         ↓
    三方向步执行，结果自动汇总至 Lead
         ↓
    Lead 合成最终报告
```

#### 流程 C：竞合调试

```
复现间歇性Bug（每50次挂1次）
  ├── Teammate A: 假设A→复现→验证
  ├── Teammate B: 假设B→复现→验证
  └── Teammate C: 假设C→复现→验证
         ↓
    某假设成立前不停止（Loop until done 模式）
```

#### 流程 D：跨层协调开发

```
Lead: 新增OAuth登录功能
  ├── Teammate Frontend: 登录页面 + Token管理
  ├── Teammate Backend: OAuth回调 + Session管理
  └── Teammate Test: 端到端测试用例
         ↓
    各自独立 worktree，完成后 Lead 合并审查
```

### 6.3 上下文管理铁律

Claude 的上下文窗口是最宝贵的资源，性能随填充率线性下降。

| 策略 | 操作 | 效果 |
|------|------|------|
| **/context** | 查看当前 Token 使用量 | 知情决策 |
| **/compact** | 高密度压缩对话历史 | 延长有效对话长度 |
| **/clear** | 完全清空对话记忆 | 切换到全新任务 |
| **Subagent 委派** | 繁重检索交给子代理独立上下文 | 主对话保持精简 |

### 6.4 验证闭环设计

给 Claude 一个可运行的检查是"监督"和"放手"的分界线：

```
Prompt 级： "run the tests after implementing"
/gool 级： 设定目标条件，每轮自动检测
Hook 级：  Stop hook 运行检查脚本，不通过不结束
对抗验证级：独立 Agent 验证主 Agent 输出
```

**关键原则**：让 Claude 展示证据（测试输出、命令结果、截图对比），而非仅声明"已完成"。

---

## 2026-06-16 更新：多 Agent 协作流程进阶

### 一、Subagent 委派流程

```
主 Agent 识别任务 → 匹配 Subagent 描述 → 委托执行 → 独立上下文工作 → 结果摘要回传
```

**详细步骤**：
1. **任务识别**：主 Agent 分析用户需求，判断是否可委派
2. **描述匹配**：扫描 `~/.claude/agents/` 和 `.claude/agents/`，匹配 Subagent 的 `description` 字段
3. **委托执行**：将任务 + 上下文摘要发送给匹配的 Subagent
4. **独立工作**：Subagent 在自己的上下文窗口中执行（可使用受限工具集）
5. **结果回传**：Subagent 完成后返回结果摘要，主会话接收并整合

**委派时机判断**：
- ✅ 委派：专注型任务（只读探索、安全审查、代码分析）、上下文可能被污染的繁重检索
- ❌ 不委派：需要主会话全程参与的多步骤协调任务、需要即时反馈的交互任务

### 二、Agent Teams 并行协作流程

```
Lead 分配任务 → Teammates 独立执行 → Mailbox 通信 → 自我协调 → Lead 汇总
```

**Lead 职责**：
1. 分解上层目标为可独立执行的子任务
2. 将子任务写入共享任务列表
3. 监控进度（非微观管理，信任 Teammate 自主完成）
4. 汇总各 Teammate 输出，消除冲突
5. 执行团队清理

**Teammate 职责**：
1. 从共享任务列表中认领任务
2. 独立在自身上下文中执行
3. 遇到阻塞时通过 Mailbox 求助其他 Teammate
4. 完成后更新任务状态 + 通知 Lead

**通信规则**：
- Teammate ↔ Teammate：Mailbox 直接通信，无需经 Lead 中转
- Teammate → Lead：任务完成通知 + 结果输出
- Lead → Teammate：任务分配 + 全局调度指令

### 三、Skills 触发机制

Skills 通过 **SKILL.md 的 YAML frontmatter 自动匹配触发**：

**触发流程**：
1. Claude 接收用户输入
2. 扫描已加载的 Skills 列表
3. 用 Skill 的 `name` 和 `description` 与用户意图做语义匹配
4. 匹配成功 → 将 Skill 的指令注入当前上下文
5. 按 Skill 指令执行任务

**SKILL.md 结构**：
```yaml
---
name: skill-name           # 唯一标识
description: 一句话说明     # 用于自动匹配触发
---
# Skill 正文（Markdown）
```

**渐进式加载**：Skill 正文中的示例和模板应拆分到独立文件，仅在需要时加载，避免上下文膨胀。

### 四、Hooks 事件驱动流程

Hooks 是**确定性脚本**——不需要 LLM 推理判断，在特定事件触发时自动执行。

**四大事件类型和处理流程**：

| 事件类型 | 触发时机 | 流程 | 用途 |
|---------|---------|------|------|
| `SessionStart` | 会话开始时 | 执行脚本 → 注入上下文 | 初始化环境、加载项目配置 |
| `PreToolUse` | 工具调用前 | 执行校验脚本 → Exit 0 放行 / Exit 2 阻止 | 安全门禁、危险命令拦截 |
| `PostToolUse` | 工具调用后 | 执行日志脚本 | 审计日志、通知推送 |
| `Notification` | 自定义事件 | 转发到外部系统 | Slack 通知、状态同步 |

**配置位置**：`settings.json` 中的 `hooks` 字段。支持项目级、用户级。

**关键原则**：
- Hooks 是确定性代码，不依赖 LLM 判断
- PreToolUse 用 Exit code 2 阻止危险操作
- PostToolUse 用于记录和通知，不应阻塞流程

### 五、MCP 工具集成流程

```
mcp.json 配置 → 服务启动 → 工具发现 → 标准化调用 → 结果返回
```

**详细步骤**：
1. **配置**：在 `.mcp.json`（项目级）或 `~/.claude/.mcp.json`（用户级）定义 MCP 服务器
2. **启动**：Claude Code 按配置启动 MCP 服务器进程（stdio 本地或 HTTP/SSE 远程）
3. **工具发现**：Claude 通过 MCP 协议发现服务器暴露的工具列表
4. **标准化调用**：使用完全限定名 `ServerName:tool_name` 调用
5. **结果返回**：MCP 服务器执行操作，返回结构化结果

**三作用域配置示例**：
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**凭证管理原则**：密钥只用环境变量引用（如 `${GITHUB_TOKEN}`），绝不硬编码。

### 六、四模式协作决策树

```
                  ┌─ 任务是否可拆为确定性步骤？
                  │
         是 ──────┼────── 否
         │                 │
   规模 > 100 子任务？    任务需要多角色协商？
    │          │           │
   是          否     是 ──┼── 否
    │          │      │         │
Dynamic   Subagent  Agent    单 Agent
Workflows  委派     Teams    直接处理
```

**决策规则**：
1. 简单任务（单步、无依赖）→ 单 Agent 直接处理
2. 可委派的专注任务 → Subagent 委派（上下文隔离 + 成本最低）
3. 需要多角色协商/交叉验证 → Agent Teams（实验性，Token 成本高）
4. 超大规模确定性并行任务（100+ 子任务）→ Dynamic Workflows

---

## R91 增量：多Agent 5层嵌套协作流程 & Agent SDK 新定价（2026-06-17）

> 来源：Claude Code v2.1.172 + Agent SDK 2026-06-15 新定价

### 一、5层嵌套协作流程

```
用户请求 → 主Agent 拆解为顶层子任务
  ├── Layer 1 子代理 A: 整体架构分析
  │     ├── Layer 2 子代理 A1: 安全审计
  │     │     └── Layer 3 子代理 A1a: SQL注入检测
  │     └── Layer 2 子代理 A2: 性能分析
  ├── Layer 1 子代理 B: 模块重构
  │     └── Layer 2 子代理 B1: 单元测试生成
  └── Layer 1 子代理 C: 文档更新

所有结果逐层汇总 → 主Agent 综合呈现
```

**协作流程要点**：

1. **分层责任**：每层子代理只对自己层的任务负责，不越界
2. **摘要回传**：深层子代理返回结构化摘要（JSON/Markdown），不返回原始上下文
3. **失败隔离**：任一层子代理失败，不影响兄弟节点，只上报给父级
4. **成本模型**：深度 N 的嵌套≈ Token 消耗 ≈ 2^N × 单层成本（指数增长）

### 二、Agent SDK 新定价（2026年6月15日起）

**独立 credit 体系**：Agent SDK 调用从独立的月度 Agent SDK credit 中扣除，与交互式对话额度分离。

影响：
- 批量 Agent 编排不再消耗对话额度，适合 CI/CD 流水线集成
- 需要建立 Agent SDK 调用成本监控
- 大规模多 Agent 系统需考虑 credit 预算

**Python SDK 快速接入**：
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for msg in query(
    prompt="审查整个代码库的安全性",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Agent"],
        agents={
            "security-scanner": AgentDefinition(
                description="安全漏洞扫描专家",
                tools=["Read", "Glob", "Grep"],
            ),
            "compliance-checker": AgentDefinition(
                description="合规性检查专家",
                tools=["Read", "Glob"],
            ),
        },
    ),
):
    # 处理多层嵌套返回的结构化结果
    pass
```

### 三、协作模式升级

原四模式协作架构增加深度维度：

```
Subagent 委派 → Agent Teams → 嵌套 Agent 树 → Workflow 编排
     ↓              ↓              ↓                ↓
  简单任务分配    专业团队协作    分层递归分解    流程引擎驱动
  深度=1         深度=1        深度≤5          深度=动态
```

**选择升级路径**：
- 单 Agent 足够 → Subagent 委派（深度=1）
- 多角色并行 → Agent Teams（深度=1，广度≤5）
- 复杂分层任务 → 嵌套 Agent 树（深度≤3 推荐，≤5 上限）
- 超大规模确定任务 → Dynamic Workflows（深度动态，广度可达100+）
- 定时/事件驱动长期任务 → Routines（云端异步，Remote Control 监控）← NEW

---

## R92 增量：Routines 与异步 Agent 协作流程（2026-06-17）

> 来源：Code with Claude Tokyo (June 10-11, 2026)

### 一、Routines 协作模式

Routines 为多 Agent 系统引入了"异步协作"维度——任务不再需要开发者在场。

```
同步协作（传统）：
用户 → 主Agent → Subagents → 结果 → 用户审查

异步协作（Routines）：
触发器 → Routine Agent → Subagents → 自动PR/通知 → 用户异步审查
```

### 二、Routines 触发类型与协作场景

| 触发方式 | 协作场景 | 典型 Routine |
|---------|---------|-------------|
| **Cron 定时** | 周期性任务 | 每日凌晨2点代码安全扫描 → 自动修复PR |
| **Webhook/API** | 外部系统事件 | PR合并后全量回归测试 → 失败自动回滚 |
| **GitHub Events** | 代码仓库事件 | Issue创建 → 自动分类 → 分派到对应Agent |

### 三、Routines + Agent Teams 组合

```
Routine 触发器
  ├── 启动 Agent Team（安全审查组）
  │     ├── security-scanner: SQL注入/CSRF/权限检查
  │     ├── dependency-checker: 依赖版本漏洞扫描
  │     └── license-auditor: 许可证合规审查
  └── 汇总结果 → 自动创建修复 PR → Slack 通知
```

### 四、异步协作铁律

1. **结果可审计**：每个 Routine 执行生成完整日志，失败时保留现场
2. **Remote Control 兜底**：关键 Routine 开启 Remote Control，手机上可随时介入
3. **Vault 隔离**：不同 Routine 使用独立 Vault 凭据，互不污染
4. **告警优先**：Routine 异常 > 自动通知 > 人工介入（而非静默失败）