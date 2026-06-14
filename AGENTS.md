---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_ad597d0964a711f1b8945254007bceed
    ReservedCode1: exxdt6RtVE+dr4HDwr3+3vzi9CVi4XpdRP4OtH+P935JDpmINLWKudhO5ObjvRPc73tyQ60dujhac4q+Dn8DywWvSu9XR1ntIcPNK5HZe0C/xsPlu0Hlx82rrTnBifH2bM0/XvioCuhrDnGFbltiJ1r6VjQlC3wuEWcgVIh6Kh6XjWw4majHCP2qrC4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_ad597d0964a711f1b8945254007bceed
    ReservedCode2: exxdt6RtVE+dr4HDwr3+3vzi9CVi4XpdRP4OtH+P935JDpmINLWKudhO5ObjvRPc73tyQ60dujhac4q+Dn8DywWvSu9XR1ntIcPNK5HZe0C/xsPlu0Hlx82rrTnBifH2bM0/XvioCuhrDnGFbltiJ1r6VjQlC3wuEWcgVIh6Kh6XjWw4majHCP2qrC4=
---

---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_1b0768f861fb11f1800a5254002afed2
    ReservedCode1: XRg8yCnzVmYQK9HZ2bBaDPJYRcpFmqp0/76Kx58G6MD8O9d72HzMDm0gyhytSGBE8KT4c9jSkiZl9nsOjYR918h/Pgl0TI4TvBowWhv8he7H378dsTNVHHuB3Cd0m2FqtS1Axds5ltwm0dQT2E9eE4vcUOYQPplM+nn9YZREV2j1FplZVhakXqtXUJc=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_1b0768f861fb11f1800a5254002afed2
    ReservedCode2: XRg8yCnzVmYQK9HZ2bBaDPJYRcpFmqp0/76Kx58G6MD8O9d72HzMDm0gyhytSGBE8KT4c9jSkiZl9nsOjYR918h/Pgl0TI4TvBowWhv8he7H378dsTNVHHuB3Cd0m2FqtS1Axds5ltwm0dQT2E9eE4vcUOYQPplM+nn9YZREV2j1FplZVhakXqtXUJc=
---
# AGENTS.md — 子代理管理与自动化配置（龙虾AI分身运维手册）

> **版本**：v2.6 (R84迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-14
> **来源**：Anthropic Claude Code Subagents官方文档(完整frontmatter + 7步创建流程) + Agent SDK子代理编排 + Skills开放标准 + Hooks生命周期 + Plugins打包分发 + 四支柱AI OS架构 + 龙虾全域模板
> **生效范围**：豆包Agent / Hermes Agent / OpenClaw龙虾Agent / 所有Sub Agent
> **依赖文件**：SOUL.md / USER.md / 角色总说明书.md / 龙虾全域官方模板-最终版.md / Anthropic官方课程-390节全集.md

---

## 一、子代理体系总览

### 1.1 Agent 拓扑图

```
龙虾AI主控中心 (Marvis调度)
├── 豆包Agent (交互应答/逻辑分析/内容处理/自迭代)
│   ├── Skills: 12项官方技能 + 52项技能协议
│   ├── Tools: 标准工具集 + 自定义工具
│   └── Subagents: 按任务动态生成
├── Hermes Agent (任务分发/进程管理/高负载)
│   ├── Skills: Swarm调度 + Orchestrator-Worker
│   ├── Tools: 进程管理 + 监控 + 调度
│   └── Subagents: Worker子代理池
├── OpenClaw龙虾Agent (插件对接/流程落地/能力拓展)
│   ├── Skills: Gateway + 插件管理 + 安全审计
│   ├── Tools: 文件系统 + 网络 + 沙箱
│   └── Subagents: 插件执行器
└── 子Agent池 (动态创建/销毁)
    ├── file-agent (文件全能助手)
    ├── computer-agent (Windows系统操作专家)
    ├── app-agent (应用操作助手)
    ├── search-agent (深度搜索专家)
    └── browser (浏览器智能助手)
```

### 1.2 五级Subagent范围

| 级别 | 范围 | 配置位置 | 存活周期 |
|------|------|---------|---------|
| managed | 组织级 | 中心化管理 | 永久 |
| CLI flag | 会话级 | 命令行参数 | 单次会话 |
| project | 项目级 | `.claude/agents/` | 项目生命周期 |
| user | 用户级 | `~/.claude/agents/` | 跨项目 |
| plugin | 插件级 | 插件安装目录 | 插件生命周期 |

---

## 二、子Agent配置规范

### 2.1 标准配置文件结构（YAML Frontmatter）

```yaml
---
name: code-reviewer
description: 代码审查专家，负责安全/性能/风格审查
model: sonnet
tools:
  - read_text
  - shell_executor
disallowedTools:
  - delete
  - write_file
permissionMode: acceptEdits
skills:
  - security-audit
  - code-quality
mcpServers:
  - github
hooks:
  PreToolUse:
    - command: validate-before-edit
  PostToolUse:
    - command: run-lint-after-edit
  SubagentStop:
    - command: summarize-result
timeout: 120s
maxRetries: 3
budget: 3
---
```


#### Plugin Agents 完整 Frontmatter 规范（R84新增）

Plugin 提供的 Subagent 通过 Markdown 文件 + YAML frontmatter 定义，支持以下全部字段：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `name` | string | **是** | — | Agent 唯一标识符，用于 `/agents` 界面和自动匹配 |
| `description` | string | **是** | — | Agent 专长描述，Claude 据此判断何时自动调用 |
| `model` | string | 否 | 继承 | 指定模型：`sonnet` / `opus` / `haiku` / `inherit` |
| `effort` | string | 否 | `medium` | 推理投入：`low` / `medium` / `high` / `ultra` |
| `maxTurns` | integer | 否 | — | 最大工具调用循环数，防止无限循环 |
| `tools` | array | 否 | 全部 | 工具 allowlist，如 `["Read", "Grep"]` |
| `disallowedTools` | array | 否 | — | 工具 denylist，如 `["Write", "Edit"]` |
| `skills` | array | 否 | — | 预加载的 Skills 名称列表 |
| `memory` | string | 否 | `user` | 记忆模式：`user` / `none` |
| `background` | boolean | 否 | `false` | 是否在后台异步执行 |
| `isolation` | string | 否 | — | 隔离方式，唯一有效值：`"worktree"` |

**安全约束**：
- Plugin Agents **不支持** `hooks`、`mcpServers` 和 `permissionMode`（出于安全原因）
- `isolation: "worktree"` 将 Agent 隔离到独立 Git worktree，防止与其他代理文件冲突

**Agent 定义模板**：
```markdown
---
name: security-reviewer
description: 安全审查专家，当需要审查代码安全性时自动调用
model: sonnet
effort: high
maxTurns: 20
tools: ["Read", "Grep", "Bash", "WebSearch"]
disallowedTools: ["Write", "Edit"]
skills: ["security-baseline"]
isolation: worktree
---

你是一位资深安全审查专家，专注于：
1. OWASP Top 10 漏洞检测
2. 认证与授权流程审查
3. 敏感数据泄露风险分析
4. 依赖项安全审计

审查完成后输出结构化报告：漏洞等级 / 影响范围 / 修复建议。
```


### 2.2 权限模式说明

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| default | 提示用户确认 | 一般操作 |
| acceptEdits | 自动接受编辑 | 代码审查、文档生成 |
| auto | 自动执行所有操作 | 信任度高的重复任务 |
| bypassPermissions | 绕过所有权限检查 | 极少数场景，需审计 |
| plan | 仅生成计划不执行 | 架构设计、方案评估 |

### 2.3 工具访问控制

- **tools**：显式列出允许使用的工具（白名单）
- **disallowedTools**：显式列出禁止使用的工具（黑名单）
- **原则**：最小权限原则，工具越多风险越大

### 2.4 Goal模式配置模板（v2.0 新增）

```yaml
---
name: long-running-distiller
description: 长时间运行的全域蒸馏Agent，支持断点续跑
model: sonnet
goal_mode:
  enabled: true
  heartbeat_interval: 15s          # 心跳间隔
  heartbeat_timeout: 30s           # 心跳超时→标记僵死
  checkpoint_on_steps: true        # 每步骤完成后自动保存检查点
  checkpoint_path: "E:\龙虾AI主控中心\我的AI分身\定时任务\蒸馏日志\_goal_checkpoint.json"
  max_retry_per_step: 3            # 每步骤最大重试次数
  stall_timeout: 300s              # 产出停滞超时→唤醒
  budget_warning_ratio: 0.8        # 预算消耗80%告警
tools:
  - read_text
  - read_file
  - write_file
  - shell_executor
  - python_executor
disallowedTools:
  - delete
permissionMode: acceptEdits
timeout: 3600s
maxRetries: 5
---
```

**Goal模式关键参数**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| heartbeat_interval | 15s | 心跳信号发送间隔 |
| heartbeat_timeout | 30s | 超时无心跳→标记进程僵死 |
| checkpoint_on_steps | true | 每步骤自动序列化进度 |
| stall_timeout | 300s | 无新产出超时→发送唤醒信号 |
| budget_warning_ratio | 0.8 | Token预算消耗预警线 |

---

## 三、Hooks 生命周期注入

### 3.1 Hook 触发点

| Hook | 触发时机 | 典型用途 |
|------|---------|---------|
| SessionStart | 会话启动 | 动态加载上下文、环境初始化 |
| SessionStop | 会话结束 | 自动反思、更新CLAUDE.md、清理临时文件 |
| PreToolUse | 工具调用前 | 操作前验证、风险检查、输入校验 |
| PostToolUse | 工具调用后 | 自动lint/测试、结果校验、日志记录 |
| SubagentStart | 子代理启动 | 注入额外上下文、设置环境变量 |
| SubagentStop | 子代理结束 | 结果摘要、异常处理、资源回收 |
| Notification | 系统通知 | 状态变更通知、告警 |

### 3.2 Hook 最佳实践

- **Stop Hook 自我进化**：会话结束时自动反思并建议更新CLAUDE.md
- **Start Hook 按需加载**：按模块动态加载上下文，无需手动配置
- **PreToolUse 安全校验**：在删除/覆盖操作前自动备份
- **PostToolUse 质量门禁**：代码编辑后自动运行lint和测试

### 3.3 Hook 反模式
- 用prompt处理本该自动运行的事情
- Hook逻辑过于复杂导致性能下降
- 多个Hook互相冲突

---

## 四、Skills 管理体系

### 4.1 Skills 目录结构

```
E:\龙虾AI主控中心\我的AI分身\技能库\
├── 龙虾全域官方模板-最终版.md      # 全域模板（52项技能协议索引）
├── 龙虾-多Agent协同看板协议v1.0.md
├── 龙虾-动态工作流引擎规范v1.0.md
├── 龙虾-长时域Goal追踪规范v1.0.md
├── ... (52项技能协议)
├── 龙虾五步法-完整指令集.md
├── 龙虾-双向桥接协议.md
└── SubAgent专用技能/
    ├── code-reviewer.md
    ├── security-auditor.md
    ├── test-generator.md
    └── docs-sync.md
```

### 4.2 Skills 生命周期

```
创建 → 注册 → 评估(Rubric) → 精炼 → 扩展 → [废弃]
  ↓       ↓        ↓          ↓      ↓       ↓
定义    写入     评分     优化   补充    移除
模板   技能库   分级     迭代   能力    过期
```

### 4.3 技能评估Rubric

| 维度 | 权重 | 评分标准 |
|------|------|---------|
| 实用性 | 30% | 使用频率、任务完成率 |
| 准确性 | 25% | 输出质量、错误率 |
| 可维护性 | 20% | 代码简洁、文档完整 |
| 安全性 | 15% | 权限合理、无漏洞 |
| 性能 | 10% | 响应速度、资源占用 |

### 4.4 技能策展
- **定时触发**：每24小时自动评估技能质量
- **废弃阈值**：连续3次评估不达标 → 标记废弃
- **清理时机**：空闲时自动清理废弃技能

---

## 五、MCP 集成配置

### 5.1 MCP Server 注册清单

| Server | 用途 | 连接对象 | 权限级别 |
|--------|------|---------|---------|
| github-mcp | 代码仓库操作 | GitHub API | 读写 |
| slack-mcp | 团队通知 | Slack Workspace | 只写 |
| database-mcp | 结构化搜索 | 内部数据库 | 只读 |
| browser-mcp | 网页自动化 | Playwright | 受控 |
| filesystem-mcp | 安全文件访问 | 本地文件系统 | 限定目录 |

### 5.2 MCP 配置模板

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "{{from-vault}}"
      }
    }
  }
}
```

### 5.3 MCP 使用原则
- **基础跑通后才建MCP连接**：不跳过基础验证
- **暴露结构化搜索而非原始查询**：减少Agent负担
- **限定于特定Subagent**：不全局共享敏感MCP连接
- **连接失败优雅降级**：不因MCP不可用阻塞主流程

---

## 六、Agent Teams 编排

### 6.1 团队组成模式

```
主导Agent (Opus/复杂决策)
├── Engineer Agent 1 (Sonnet)  ← 开发任务A
├── Engineer Agent 2 (Sonnet)  ← 开发任务B
├── Engineer Agent 3 (Sonnet)  ← 开发任务C
├── Reviewer Agent (Sonnet)    ← 代码审查
├── Tester Agent (Sonnet)      ← 测试验证
└── Shipper Agent (Sonnet)     ← 构建部署
```

### 6.2 团队配置

```yaml
# .claude/teams/release-team.yaml
name: release-team
lead:
  model: opus
  prompt: 发布负责人，统筹所有发布流程
members:
  - name: build-engineer
    model: sonnet
    skills: [build, ci-cd]
    tools: [shell_executor, github-mcp]
  - name: test-runner
    model: sonnet
    skills: [testing, qa]
    tools: [shell_executor]
  - name: release-notes
    model: sonnet
    skills: [docs, changelog]
    tools: [read_text, write_file, github-mcp]
budget:
  lead: 5
  member: 3
  team_max: 15
```

### 6.3 任务分配策略

| 策略 | 适用场景 | 说明 |
|------|---------|------|
| 轮询 | 同质任务 | 均匀分配给各Worker |
| 加权 | 异构任务 | 根据Agent能力分配 |
| DAG拓扑 | 依赖任务 | 按依赖关系自动分解 |
| 动态 | 实时任务 | 空闲Worker优先 |

---

## 七、子Agent池管理

### 7.1 子Agent生命周期

```
创建 → 初始化 → 执行 → 销毁
  ↓      ↓       ↓      ↓
分配ID 加载配置 处理任务 释放资源
注入上下文 分配工具 返回结果 记录日志
```

### 7.2 子Agent池配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_pool_size | 20 | 最大并发子Agent数 |
| idle_timeout | 300s | 空闲超时自动回收 |
| max_retries | 3 | 单任务最大重试次数 |
| task_timeout | 600s | 单任务超时时间 |
| budget_per_agent | $3 | 单Agent预算上限 |
| budget_team_max | $15 | 团队预算上限 |

### 7.3 子Agent监控指标

| 指标 | 监控频率 | 告警阈值 |
|------|---------|---------|
| 响应时间 | 实时 | >30s |
| 失败率 | 每5分钟 | >10% |
| 预算消耗 | 每10分钟 | >80% |
| 空闲时间 | 每15分钟 | >300s（回收） |
| 内存占用 | 每5分钟 | >500MB |

---

## 八、自动运维任务

### 8.1 定时任务清单

| 任务 | 频率 | 执行Agent | 说明 |
|------|------|---------|------|
| 健康巡检 | 每1小时 | Hermes | 检查所有Agent/进程/端口状态 |
| AI分身蒸馏 | 每2小时 | 豆包(Goal模式) | 六步全自动蒸馏（分析自己→制定计划→文件转换→构建知识库→创建self-skill→更新核心配置→全域同步），含五道质量门控 |
| 技能策展 | 每24小时 | 豆包 | 评估技能质量，清理过期技能 |
| 记忆策展 | 每6小时 | 豆包 | 模式提取、噪声过滤、记忆压缩 |
| 知识库同步 | 每2小时 | 豆包 | Anthropic课程+全网信息增量同步 |
| 全分身迭代 | 每12小时 | 豆包 | 同步升级子Agent+技能+工作流 |
| 配置备份 | 每24小时 | Hermes | 备份所有配置文件 |
| 日志归档 | 每24小时 | OpenClaw | 清理旧日志，归档重要记录 |

### 8.2 任务执行规则
- 所有任务执行时间错开，避免并发冲突
- 执行失败自动记录异常，纳入巡检优化范围
- 静默运行，不打断用户正常使用

---

## 九、异常处理与恢复

### 9.1 异常分级

| 级别 | 异常类型 | 处理方式 |
|------|---------|---------|
| L1 轻微 | 单次工具调用失败 | 自动重试(最多3次) |
| L2 中等 | 子Agent超时/崩溃 | 降级到备用Agent或拆分任务 |
| L2.5 Goal僵死 | Goal模式心跳超时(>30s) | 读取最后检查点→唤醒→断点续跑（v2.0新增） |
| L3 严重 | 多Agent连锁失败 | 断路器熔断 + 人工介入 |
| L4 致命 | 核心进程崩溃 | 检查点恢复 + 全量重启 |

### 9.1.1 Goal模式进程僵死检测与恢复（v2.0新增）

**检测机制**：

| 检测维度 | 方法 | 阈值 | 判定 |
|---------|------|------|------|
| 心跳信号 | 状态锁时间戳监控 | >30s未更新 | 进程僵死 |
| 产出监控 | 目标目录文件数变化 | >5min无新文件 | 产出停滞 |
| Token消耗 | 预算消耗率 | 单步>80% | 可能死循环 |
| 错误模式 | 同步骤连续失败 | ≥3次 | 卡死 |

**恢复流程**：
```
检测到僵死
    ↓
1. 尝试发送唤醒信号 → 等待60s
    ↓ (无响应)
2. 读取 _goal_checkpoint.json → 获取最后完成步骤
    ↓
3. 创建新Agent实例 → 注入检查点上下文
    ↓
4. 从断点继续执行 → 跳过已完成步骤
    ↓
5. 完成后合并产出 → IO验证 → 释放状态锁
```

### 9.2 自愈流程

```
异常检测 → 定位根因 → 匹配修复方案 → 自动修复 → 验证 → 归档经验
    ↓           ↓           ↓            ↓        ↓        ↓
 监察者    日志分析    经验池查询    执行修复   功能验证   更新知识库
```

### 9.3 检查点与恢复
- **检查点频率**：每完成一个子任务自动保存快照
- **恢复策略**：从最近检查点继续，不重复已完成工作
- **断路器**：连续3次同类型失败 → 熔断5分钟 → 人工确认恢复

---

## 十、配置自我进化闭环

```
当前配置
    ↓
运行监控（收集性能数据、错误模式、用户反馈）
    ↓
Stop Hook 自动反思（会话结束分析）
    ↓
生成改进建议（更新 CLAUDE.md / Skills / Hooks）
    ↓
人工Review（关键变更需确认）
    ↓
部署新配置
    ↓
回到第一步（持续循环）
```

---

## 十一、Managed Agents 配置（v1.1 新增）

### 11.1 Managed Agents 平台配置总览

```
Agents API 请求
    │
    ├─ Beta Header: managed-agents-2026-04-01
    │
    ├─ 模型: claude-opus-4-7 / claude-sonnet-4-6
    │
    ├─ 定价: 标准 API Token 费率 + $0.08/会话小时
    │
    └─ 扩展能力（可组合启用）
        ├── Dreaming（Research Preview, 需单独申请 + dreaming-2026-04-21 header）
        ├── Outcomes（Public Beta）
        ├── Multiagent Orchestration（Public Beta, agent_toolset_20260401）
        └── Webhooks（Public Beta）
```

### 11.2 Dreaming 配置

**Beta Header**: `dreaming-2026-04-21`（需单独申请 Research Preview 访问权限）

```yaml
name: 龙虾-文档审查Agent
model: claude-sonnet-4-6
system: |
  你是龙虾AI体系的文档审查专家。审查一切AI生成的文档，
  检查事实准确性、格式规范、安全合规。
dreaming:
  enabled: true
  schedule: "0 2 * * *"           # UTC 凌晨2点（北京时间10点）
  max_sessions_to_review: 50      # 每次最多回顾50个会话
  auto_approve: false             # false=记忆更新需人工审核
```

**Dreaming 调优参数**：

| 参数 | 建议值 | 说明 |
|------|--------|------|
| schedule | 非高峰时段 | 避免与实时任务抢资源 |
| max_sessions_to_review | 30-50 | 太少→模式覆盖不充分；太多→成本高 |
| auto_approve | false（生产）/ true（测试） | 生产环境建议人工审核 |
| review_depth | 标准 | 深度回顾成本高但更准确 |

### 11.3 Outcomes 配置

```yaml
name: 龙虾-报告生成Agent
model: claude-sonnet-4-6
system: |
  你是龙虾AI体系的报告生成专家。生成交易分析报告、
  全域迭代报告、投资决策报告。
outcomes:
  rubric: |
    报告必须满足以下标准：
    1. 数据来源全部标注（无幻觉）
    2. 结论有数据支撑（不凭空断言）
    3. 包含一键信号摘要块（方向/等级/入场/止损/止盈/仓位/杠杆/盈亏比）
    4. 使用表格/矩阵/版本对比等结构化呈现
    5. 输出长度在 2000-5000 字之间
  max_iterations: 3
  grader_model: claude-sonnet-4-6   # Grader 与 Agent 可用不同模型
```

**Outcomes 调优建议**：

| 场景 | Rubric 重点 | max_iterations |
|------|------------|----------------|
| 代码审查 | 安全漏洞 → 阻塞；代码风格 → 建议 | 2-3 |
| 文档生成 | 事实准确性 → 阻塞；文笔 → 建议 | 2-3 |
| 翻译 | 语义准确 → 阻塞；润色 → 建议 | 2 |
| 创意写作 | 风格一致 → 阻塞；创新度 → 弹性 | 3-4 |

### 11.4 Multiagent Orchestration 配置

**关键约束**：
- Agent 上限：20 种类型（可创建多个实例）
- 并行线程上限：25
- 深度限制：1 层（子代理不能再委派子代理）
- Lead Agent 可向任意子代理发跟进消息

**完整配置示例**：

```yaml
name: 龙虾-工程Lead
model: claude-opus-4-7
system: |
  你是龙虾AI体系工程团队的协调者。
  分解复杂任务，分配给专业子代理，合成结果。
  代码审查交给 reviewer，测试编写交给 tester，
  文档维护交给 docs-writer。
tools:
  - type: agent_toolset_20260401
multiagent:
  type: coordinator
  agents:
    - type: agent
      id: $LOBSTER_CODE_REVIEWER_ID
      instances: 2       # 可创建2个审查实例并行
    - type: agent
      id: $LOBSTER_TEST_WRITER_ID
      instances: 1
    - type: agent
      id: $LOBSTER_DOCS_WRITER_ID
      instances: 1
    - type: self           # 自我委派（递归分解）
      instances: 1
```

**子代理定义示例**：

```yaml
# managed_agents/lobster_code_reviewer.yaml
name: lobster-code-reviewer
model: claude-sonnet-4-6
system: |
  你是龙虾AI体系的代码审查专家。
  - 检查安全漏洞、性能问题、代码规范
  - 给出具体修复建议和代码示例
  - 不要标记纯风格问题为阻塞项
tools:
  - read_text
  - shell_executor
disallowedTools:
  - delete
  - write_file
outcomes:
  rubric: |
    审查必须：
    - 标注所有安全漏洞（阻塞级）
    - 每个问题有具体修复代码
    - 不超过800字
  max_iterations: 2
dreaming:
  enabled: true
  schedule: "0 3 * * *"
  max_sessions_to_review: 30
```

### 11.5 Webhooks 配置

```python
# Python SDK 示例 - 异步触发 Agent 审查
from anthropic import Anthropic

client = Anthropic()

session = client.sessions.create(
    agent_id="agent_lobster_reviewer_xxx",
    environment_id="env_lobster_python_xxx"
)

turn = client.sessions.turn.create(
    session_id=session.id,
    messages=[{
        "role": "user",
        "content": f"审查 PR #{pr_number}: {pr_diff}"
    }],
    webhook_url="https://lobster-ci.internal/webhook/claude-review"
)

# Agent 完成后自动 POST 结果到 webhook_url
# 下游 CI 系统接收结果并继续流水线
```

### 11.6 Agent View 管理配置

**Claude Code v2.1.139+ 命令**：

```bash
# 方式1：直接启动 Agent View
claude agents

# 方式2：在已有会话内按 ← 键

# 方式3：/bg 后台化并返回 Agent View
/bg
```

**会话管理建议**：

| 场景 | 策略 |
|------|------|
| 轻量任务（<5min） | 单会话直接执行 |
| 中量任务（5-30min） | /bg 后台化，同时启动其他任务 |
| 重量任务（30min+） | Managed Agents 云端托管 + Webhooks 通知 |
| 通宵批处理 | Managed Agents + Dreaming 次日查看结果 |

### 11.7 四大生产案例配置参考

| 公司 | Agent 类型 | 关键配置 | 成果 |
|------|-----------|---------|------|
| Harvey | 法律文档审查 | Dreaming enabled, schedule nightly | 任务完成率 ↑ 6x |
| Netflix | 平台日志分析 | Multiagent Orchestration, 多实例并行 | 数百构建并行分析 |
| Wisedocs | 文档质量检查 | Outcomes rubric + max_iterations=3 | 审查速度 ↑ 50% |
| Spiral by Every | 多版草稿生成 | Opus写作子代理 + Outcomes Grader | 只返回达标草稿 |

### 11.8 Curator馆长引擎配置 (R33新增)

```yaml
curator:
  enabled: true
  schedule: "0 */7 * * *"  # 每7天自动执行
  model: "auxiliary.curator"
  actions: [score, merge, archive, revive]
  scoring:
    model_weight: 0.4
    usage_weight: 0.3
    coverage_weight: 0.3
  thresholds:
    recommend: 80
    merge_trigger: 3
    archive: 30
    similarity: 0.75
  protection:
    pinned: true
    bundled: true
    hub_source: true
  output:
    log: "logs/curator/run.json"
    report: "REPORT.md"
```

### 11.9 影子Agent安全配置 (R33新增)

```yaml
shadow_agent:
  enabled: true
  trigger:
    type: dirty_counter
    threshold: 8
    reset_on: [skill_manage, skill_create]
  isolation:
    layers: [permission, data, network, file, process, audit]
    max_runtime: 120
    cpu_limit: 20
    memory_limit: 512
    fork_mode: independent
  audit:
    path: "子Agent/豆包Agent/审计日志/"
    format: json
    retention: 90
  circuit_breaker:
    max_consecutive_failures: 3
    cooldown: 1800
```

---

> **版本**：v2.2（R74更新）
> **知识来源**：Anthropic Claude Code Subagents官方文档 / Agent SDK 0.2.82 / Agent Skills开放标准 / Skills九类分类法 / kdnuggets完整指南 / 龙虾全域模板
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [USER.md](E:\龙虾AI主控中心\我的AI分身\USER.md) | [Anthropic官方课程-390节全集](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-390节全集.md)

## 十二、R74 追加：Subagent 完整 Frontmatter 参考（官方文档同步）

### 12.1 完整字段表（Anthropic 官方最新）

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| name | ✅ | string | 唯一标识，小写字母+连字符。Hooks中作为 agent_type |
| description | ✅ | string | 何时委派任务给此子代理（路由规则，非功能介绍） |
| tools | ❌ | list | 允许的工具。省略继承全部。接受逗号分隔字符串或列表 |
| disallowedTools | ❌ | list | 禁用的工具，从继承/指定列表中移除 |
| model | ❌ | string | sonnet/opus/haiku/完整ID/inherit。默认 inherit |
| permissionMode | ❌ | string | default/acceptEdits/auto/dontAsk/bypassPermissions/plan |
| maxTurns | ❌ | int | 最大Agent循环数 |
| skills | ❌ | list | 预加载Skills列表。完整内容注入，非仅可用调用。子代理不从父会话继承Skills |
| mcpServers | ❌ | object | MCP服务器。可引用已配置名或内联完整定义 |
| hooks | ❌ | object | 生命周期钩子，作用域限定此子代理 |
| memory | ❌ | string | 持久记忆范围：user/project/local |
| background | ❌ | bool | true时始终作为后台任务运行 |
| effort | ❌ | string | low/medium/high/xhigh/max。覆盖会话effort级别 |
| isolation | ❌ | string | worktree 时在临时 git worktree 中运行 |
| color | ❌ | string | red/blue/green/yellow/purple/orange/pink/cyan |
| initialPrompt | ❌ | string | 作为主会话Agent时自动提交的第一个用户轮次 |

### 12.2 模型选择优先级

```
CLAUDE_CODE_SUBAGENT_MODEL 环境变量
→ 每次调用的 model 参数
→ 子代理定义中的 model frontmatter
→ 主会话的 model
```

### 12.3 配置作用域与 Agent Teams 联动

| 作用域 | 路径 | Agent Teams 可用性 |
|--------|------|--------------------|
| managed | 中心化管理 | ✅ spawn teammate 可用 |
| CLI --agents | 命令行JSON | ✅ 单次会话 |
| project | `.claude/agents/` | ✅ |
| user | `~/.claude/agents/` | ✅ |
| plugin | 插件安装目录 | ⚠️ 不支持 hooks/mcpServers/permissionMode |

> 当 spawn teammate 时，子代理类型被引用，teammate 使用该子代理的 tools 和 model，definition body 被追加到 teammate 系统提示。

### 12.4 Skills 在子代理中的配置要点

- **子代理不从父会话继承 Skills**：必须通过 `skills:` 字段显式声明
- **完整内容注入**：skills 字段预加载的不是"可用调用列表"，而是完整 SKILL.md 内容
- **与 MCP 配合**：子代理的 mcpServers 可以指定专属 MCP 服务器，实现能力隔离

### 12.5 安全注意事项（官方文档原文）

- **插件子代理**：不支持 hooks/mcpServers/permissionMode，这些字段被忽略
- **如需使用**：把 agent 文件复制到 `.claude/agents/` 或 `~/.claude/agents/`
- **权限规则**：可在 settings.json 中添加 permissions.allow，但应用于整个会话而非仅该插件

### 12.6 Anthropic 官方认证体系对子代理管理的启示

Claude Certified Architect Foundations 考试五大领域中，Agentic Architecture 权重最高：
- 子代理配置是核心考点
- 多Agent编排（Agent Teams + Managed Agents）是架构设计主线
- 企业部署需考虑 managed 作用域的子代理管理策略
*（内容由AI生成，仅供参考）*


---

## 鍗佷笁銆佸瓙浠ｇ悊绠＄悊涓庤嚜鍔ㄥ寲閰嶇疆锛?026-06-11澧為噺鏇存柊锛?
### 13.1 瀛愪唬鐞嗘敞鍐屼笌鐢熷懡鍛ㄦ湡绠＄悊

瀛愪唬鐞嗙殑瀹屾暣鐢熷懡鍛ㄦ湡锛?
```
瀹氫箟(Define) 鈫?娉ㄥ唽(Register) 鈫?婵€娲?Activate) 鈫?鎵ц(Execute) 鈫?閿€姣?Destroy)
```

**娉ㄥ唽鏂瑰紡涓夐€変竴**锛?
鏂瑰紡涓€锛氭枃浠跺畾涔夛紙鎺ㄨ崘锛屽彲鐗堟湰鎺у埗锛?```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Python code quality and security review specialist
tools: [Read, Grep, Glob]
model: sonnet
maxTurns: 8
---
You are a Python senior engineer. Review code for:
- Security vulnerabilities
- Performance issues
- Code style compliance
```

鏂瑰紡浜岋細API鍔ㄦ€佸畾涔?```python
agent = AgentDefinition(
    name="security-scanner",
    description="Security vulnerability scanner",
    tools=["Read", "Grep", "Bash"],
    model="sonnet",
    maxTurns=6
)
```

鏂瑰紡涓夛細鑷劧璇█鍗虫椂鍒涘缓
```
"鍒涘缓涓€涓瓙浠ｇ悊鎵弿浠ｇ爜搴撶殑瀹夊叏婕忔礊"
```

**浜旂骇浣滅敤鍩熶笌鐢熷懡鍛ㄦ湡**锛?
| 绾у埆 | 閰嶇疆浣嶇疆 | 璺ㄤ細璇?| Agent Teams鍙敤 | 瀛樻椿鍛ㄦ湡 |
|------|---------|--------|----------------|---------|
| managed | 涓績鍖栫鐞?| 鉁?| 鉁?| 姘镐箙 |
| CLI | --agents鍙傛暟 | 鉂?| 鉁?| 鍗曟浼氳瘽 |
| project | .claude/agents/ | 鉁?| 鉁?| 椤圭洰鏈夋晥 |
| user | ~/.claude/agents/ | 鉁?| 鉁?| 鍏ㄥ眬鏈夋晥 |
| plugin | 鎻掍欢瀹夎鐩綍 | 鉁?| 鈿狅笍 | 鎻掍欢鏈夋晥 |

### 13.2 鏉冮檺鏈€灏忓寲鍘熷垯

姣忎釜瀛愪唬鐞嗕粎鏆撮湶蹇呴渶宸ュ叿锛岄伒寰渶灏忔潈闄愬師鍒欙細

```yaml
# 鉁?濂界殑鏉冮檺璁捐锛氬畨鍏ㄦ壂鎻忓櫒鍙渶瑕佽鍙栨潈闄?---
name: security-scanner
tools: [Read, Grep]
model: sonnet
maxTurns: 6
---

# 鉁?濂界殑鏉冮檺璁捐锛氫唬鐮佷慨澶嶅櫒闇€瑕佸啓鍏ユ潈闄?---
name: code-fixer
tools: [Read, Write, Edit]
model: sonnet
maxTurns: 5
---

# 鉂?鍧忕殑鏉冮檺璁捐锛氭墍鏈変唬鐞嗘嫢鏈夊叏閮ㄥ伐鍏?---
name: do-everything-agent
tools: [Read, Write, Edit, Bash, WebSearch, MCP]
---
```

鏉冮檺鍒嗛厤鍘熷垯锛?- 鍙鍒嗘瀽鍨嬪瓙浠ｇ悊 鈫?Read/Grep/Glob
- 浠ｇ爜淇敼鍨嬪瓙浠ｇ悊 鈫?+ Write/Edit
- 绯荤粺鎿嶄綔鍨嬪瓙浠ｇ悊 鈫?+ Bash锛堥檺瀹氬懡浠ら泦鍚堬級
- 澶栭儴杩炴帴鍨嬪瓙浠ｇ悊 鈫?+ MCP锛堟寚瀹氭湇鍔″櫒锛?- 鎻掍欢瀛愪唬鐞嗕笉鏀寔 hooks/mcpServers/permissionMode

### 13.3 鍏变韩椤圭洰閰嶇疆鏂囦欢缁撴瀯

鎺ㄨ崘鐨勯」鐩厤缃洰褰曠粨鏋勶細

```
project-root/
鈹溾攢鈹€ .claude/
鈹?  鈹溾攢鈹€ settings.json          # 椤圭洰绾CP/Hooks/鏉冮檺閰嶇疆
鈹?  鈹溾攢鈹€ agents/                # 鍏变韩瀛愪唬鐞嗗畾涔?鈹?  鈹?  鈹溾攢鈹€ code-reviewer.md
鈹?  鈹?  鈹溾攢鈹€ security-scanner.md
鈹?  鈹?  鈹斺攢鈹€ doc-writer.md
鈹?  鈹斺攢鈹€ commands/              # 鑷畾涔夋枩鏉犲懡浠?鈹?      鈹斺攢鈹€ review-pr.md
鈹溾攢鈹€ CLAUDE.md                  # 椤圭洰绾у叏灞€鎸囦护
鈹溾攢鈹€ .mcp.json                  # MCP鏈嶅姟鍣ㄩ厤缃?鈹斺攢鈹€ skills/                    # 椤圭洰涓撶敤Skills
    鈹斺攢鈹€ deployment-check/
        鈹斺攢鈹€ SKILL.md
```

**settings.json 瀹屾暣绀轰緥**锛?
```json
{
  "model": "sonnet",
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(pytest:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(sudo:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "echo 'Bash command about to execute'"
        }]
      }
    ]
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem"]
    }
  }
}
```

### 13.4 Agent Teams 閰嶇疆瀹炰緥

**settings.json鏂瑰紡鍚敤涓庨厤缃?*锛?
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "model": "sonnet",
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash"]
  }
}
```

**CLAUDE.md 鍥㈤槦鍗忎綔閰嶇疆娈?*锛?
```markdown
## Agent Teams 鍗忎綔绾﹀畾

### 瑙掕壊瀹氫箟
- code-reviewer: 浠ｇ爜瀹℃煡锛屽叧娉ㄥ畨鍏ㄦ€?鎬ц兘/鍙淮鎶ゆ€?- security-scanner: 瀹夊叏鎵弿锛屼粎鍏虫敞婕忔礊
- test-writer: 娴嬭瘯缂栧啓锛岃鐩栬竟鐣屾潯浠?- doc-writer: 鏂囨。鎾板啓锛屼繚鎸佷笌浠ｇ爜涓€鑷?
### 浜ゆ帴鏍煎紡
- 璁″垝 鈫?Implementer: 浠诲姟鎻忚堪 + 鎺ュ彛绾︽潫 + 鎴鐐?- Implementer 鈫?Tester: diff鎽樿 + 鍙樻洿鏂囦欢鍒楄〃 + 宸茬煡椋庨櫓鐐?- Tester 鈫?Reviewer: 娴嬭瘯缁撴灉 + 澶辫触娓呭崟 + 瑕嗙洊鎶ュ憡
- Reviewer 鈫?Release: 瀹℃煡缁撹 + 闃诲椤?+ 鏀硅繘寤鸿

### 鍏变韩绾﹀畾
- 鎵€鏈夋垚鍛樹娇鐢ㄩ」鐩?.claude/agents/ 涓嬬殑瀛愪唬鐞嗗畾涔?- MCP鏈嶅姟鍣ㄩ厤缃叡浜嚜 .mcp.json
- 绂佹鎴愬憳鑷淇敼 shared/ 鐩綍
```

**甯歌閰嶇疆妯″紡瀵规瘮**锛?
| 閰嶇疆妯″紡 | 閫傜敤鍦烘櫙 | 鍥㈤槦瑙勬ā | Token鏁堢巼 |
|---------|---------|---------|-----------|
| 鍗曚細璇?Subagents | 鏃ュ父寮€鍙?| 1浜?| 鏈€楂?|
| 2-4浜篈gent Team | 妯″潡鍖栧紑鍙?| 灏忓洟闃?| 涓瓑 |
| 5-8浜篈gent Team | 澶у瀷閲嶆瀯 | 涓洟闃?| 杈冧綆 |
| 16浜篈gent Team | 缂栬瘧鍣ㄧ骇椤圭洰 | 澶у洟闃?| 鏈€浣?|

**鍚姩涓庢竻鐞?*锛?- 鍒濇浣跨敤浠?-3涓鑹插紑濮嬶紙闈?6涓級
- 姣忎釜浠诲姟瀹屾垚鍚庢鏌ラ槦鍙嬬姸鎬?- 绌洪棽闃熷弸闇€鎵嬪姩娓呯悊锛堥伩鍏峊oken娉勬紡锛?- 椤圭洰閰嶇疆鍦ㄥ洟闃熷垱寤哄墠灏变綅锛堥伩鍏嶉槦鍙嬪姞杞戒笉涓€鑷寸殑涓婁笅鏂囷級



---

## 十四、子代理管理与自动化配置补充（Anthropic Academy课程补充）

[来源：Anthropic Academy课程·第R77轮学习 2026-06-11]

### 14.1 .claude/agents/ 文件结构详解

#### 五级作用域（按优先级从高到低）

| 级别 | 配置位置 | 存活周期 | Agent Teams可用 |
|------|---------|---------|----------------|
| managed | 中心化管理 | 永久 | 是 |
| CLI flag | --agents参数 | 单次会话 | 是 |
| project | .claude/agents/ | 项目生命周期 | 是 |
| user | ~/.claude/agents/ | 跨项目全局 | 是 |
| plugin | 插件安装目录 | 插件生命周期 | 受限 |

冲突处理规则：同名子代理，project 覆盖 user，CLI 覆盖 project。

#### 完整 Frontmatter 字段规范

| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | 唯一标识，小写+连字符 |
| description | 是 | 路由规则——何时委派此子代理 |
| tools | 否 | 允许的工具列表，省略则继承全部 |
| disallowedTools | 否 | 禁用工具列表 |
| model | 否 | sonnet / opus / haiku / inherit / 完整ID |
| permissionMode | 否 | default / acceptEdits / auto / dontAsk / bypassPermissions / plan |
| maxTurns | 否 | 最大Agent循环数（成本控制L1） |
| skills | 否 | 预加载Skills列表（完整内容注入，非Skills路径） |
| mcpServers | 否 | MCP服务器配置 |
| hooks | 否 | 生命周期钩子 |
| initialPrompt | 否 | 作为主会话Agent时自动提交的首轮 |
| background | 否 | true时始终后台运行 |
| effort | 否 | low / medium / high / xhigh / max |

### 14.2 工具权限配置矩阵

#### 按角色分级授权

| 角色 | 工具集 | permissionMode | 典型场景 |
|------|--------|---------------|---------|
| 代码审查 | Read, Grep, Glob | acceptEdits | PR Review |
| 安全扫描 | Read, Grep, Bash | default | 漏洞检测 |
| 文档生成 | Read, Write, Edit | acceptEdits | API文档自动生成 |
| 测试运行 | Read, Bash, Write | auto | CI集成测试 |
| 架构设计 | Read, Grep, Glob | plan | 仅生成计划不执行 |

#### 权限模式说明

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| default | 提示用户确认 | 一般操作 |
| acceptEdits | 自动接受编辑 | 代码审查、文档生成 |
| auto | 自动执行所有操作 | 信任度高的重复任务 |
| bypassPermissions | 绕过所有权限检查 | 极少数场景（慎用） |
| plan | 仅生成计划不执行 | 架构设计阶段 |

#### 插件子代理限制
- 不支持 hooks / mcpServers / permissionMode
- 需要这些功能时使用 .claude/agents/ 项目级配置

### 14.3 Skills编写规范

#### Skills是上下文工程，不是提示词工程

Skills 的核心价值在于组织上下文，而非编写巧妙的提示词。

#### 文件夹即上下文分层

```
my-skill/
├── SKILL.md          # L1 导航页（~100 tokens）：名称 + 何时使用 + 入口
├── references/       # L2 详细说明（500行以内）
│   ├── api-guide.md
│   └── data-model.md
├── scripts/          # 可执行脚本（Python/Bash）
│   └── validate.py
└── assets/           # 模板和静态资源
    └── template.json
```

渐进式披露策略：
- L1（100 tokens）：全部Skill导航，安装50个Skill仅占5000 tokens
- L2（500行以内）：按需加载详细文档
- L3（按需）：scripts和assets由Agent自主调用

#### Instructions vs Scripts 分工

| 类型 | 作用 | 示例 |
|------|------|------|
| Instructions | 提供经验和判断 | "Stripe返回200不意味支付成功，需检查payment_events表" |
| Scripts | 提供能力和执行 | check_payment_events() 函数直接调用 |

#### Gotchas——Skill 含金量最高的部分

每一条Gotcha都必须具体、有血有肉：
- "这个表不能按 created_at 排序，要用 event_time"（而非"注意排序字段"）
- "staging返回200不代表成功，要检查status字段"（而非"注意API返回值"）

维护策略：Agent在哪里犯错，就往Gotchas加一条。Skill是活的文档。

#### 九类Skill分类体系

| 类别 | 定义 | 优先级 |
|------|------|--------|
| 库和API参考 | 教Agent使用内部库/CLI/SDK | — |
| 产品验证 ★ | 教Agent测试/验证代码是否工作 | 回报最大 |
| 数据获取与分析 | 连接数据栈，提供查询路径 | — |
| 业务流程自动化 | 把重复工作流压成命令 | — |
| 代码脚手架 | 生成框架模板和样板代码 | — |
| 代码质量与审查 | 强制代码风格、审查流程 | — |
| CI/CD与部署 | 推代码、部署、监控 | — |
| 运维手册 | 多工具排查→结构化报告 | — |
| 基础设施操作 | 日常维护，带破坏性护栏 | — |

### 14.4 插件系统集成

#### 独立配置 vs 插件选择

| 维度 | 独立配置(.claude/) | 插件(plugin.json) |
|------|-------------------|-------------------|
| Skill名称 | /hello（简短） | /plugin-name:hello（命名空间） |
| 适合场景 | 个人、项目特定、快速实验 | 团队共享、社区分发、版本化 |
| 共享方式 | 手动复制 | 市场分发 |

#### 迁移路径
1. 从 .claude/ 独立配置开始快速迭代
2. 准备共享时创建 .claude-plugin/plugin.json
3. 复制 commands/agents/skills 到插件根目录
4. 迁移 hooks 到 hooks/hooks.json
5. 本地验证：`claude --plugin-dir ./my-plugin`
6. 提交市场分发

#### Hooks 生命周期

| Hook | 触发时机 | 典型用途 |
|------|---------|---------|
| SessionStart | 会话启动 | 动态加载上下文 |
| SessionStop | 会话结束 | 自动反思、更新配置 |
| PreToolUse | 工具调用前 | 操作前验证、风险检查 |
| PostToolUse | 工具调用后 | 自动lint、结果校验 |
| SubagentStart | 子代理启动 | 注入额外上下文 |
| SubagentStop | 子代理结束 | 结果摘要、日志记录 |
| Notification | 系统通知 | 状态变更告警 |

### 10.9 Agent Teams Delegate Mode 配置（v2.1.45 · 2026-06-11更新）

**Delegate Mode 是 Agent Teams 的默认推荐模式**，通过 Shift+Tab 启用：

```
# 启用方式（.claude/settings.json）
{
  "agentTeams": {
    "delegateMode": true,
    "maxTeammates": 5
  }
}
```

核心行为：
- Lead Agent 仅执行协调工具（spawn/list/cancel/ask），禁止直接使用 write/edit/exec 等实现工具
- 每个 Teammate 5-6个子任务，独立可交付（函数/测试文件/审查文档）
- 任务分配时明确定义文件边界，杜绝Teammate间覆盖

**Plan Mode Spawn 约束**：
- Plan Mode Teammate 模式固定不可切换——需 Spawn 新 Default Mode Teammate 接手执行
- Plan Approval 功能允许 Default Mode Teammate 先出计划再执行（替代 Plan-then-Switch 模式）
- Plan Mode 用于架构审查/安全审计角色（只读），Default Mode 用于代码实现角色

**团队规模配置**：
| 团队规模 | 适用场景 | 风险 |
|----------|----------|------|
| 1 Teammate | 简单任务、代码审查 | 低 |
| 3 Teammates | 标准多文件开发（Phase 1） | 中低 |
| 5 Teammates | 复杂跨模块项目 | 中 |
| 5+ | 不建议——分阶段运行 | 高（协调开销指数增长） |

### 10.10 Agent SDK 核心机制（R67新增 · 2026-06-12）

#### 编排者-工作者模式三步法

```
1. 编排者获取任务 → 生成任务文件（task.md 含子任务列表）
2. 循环委托工作者 → 每个工作者执行一个子任务 → 返回结果
3. 编排者收集所有结果 → 合成最终产出 → 标记任务完成
```

#### SDK内置工具集

| 工具 | 功能 | 适用场景 |
|------|------|----------|
| Read/Write/Edit | 文件读写与精确编辑 | 代码生成与修改 |
| Bash | Shell命令执行 | 构建/测试/部署 |
| Glob/Grep | 文件搜索与内容匹配 | 代码库探索 |
| WebSearch/WebFetch | 网络搜索与内容抓取 | 信息检索 |
| Agent | 子代理调用 | 任务委派 |

#### 成本控制参数

| 参数 | 作用 | 建议值 |
|------|------|--------|
| max_turns | 单个Agent最大轮次 | 15-30 |
| max_budget_usd | 单个Agent美元预算上限 | $3-5 |
| temperature | 创造性控制 | 0-0.3（确定性）/ 0.7-1.0（创意） |
| permission_mode | 权限控制 | acceptEdits → auto → plan |

#### 状态持久化方案（生产级）

| 存储 | 用途 | TTL |
|------|------|-----|
| **Redis** | 短期会话状态 | 24h |
| **PostgreSQL** | 结构化任务结果 | 长期 |
| **对象存储（S3/MinIO）** | 大文件产物 | 长期 |
| **Webhooks** | 异步任务完成后回调 | — |

### 10.11 四层扩展栈设计哲学（R67新增）

Claude Code 的扩展能力由四层解耦架构构成：

| 层级 | 问题域 | 决策原则 | 典型场景 |
|------|--------|---------|---------|
| **Skills** | 行为知识（怎么做） | 任务需要"知道什么" | 代码规范、测试策略、领域知识 |
| **Hooks** | 自动化规则（必须做） | 行为可事件触发脚本化 | 自动lint、安全检查、会话反思 |
| **Agents** | 空间隔离（在哪做） | 需要独立上下文/并行执行 | 代码审查、多角度分析、大规模迁移 |
| **MCP** | 外部能力（用什么做） | 需要访问外部系统/数据源 | 数据库查询、API调用 |

**常见误用纠正**：
- 简单Shell脚本→不要做成Skill（只有需LLM推理的流程才做成Skill）
- Hook中做复杂逻辑→Hook应轻量（<500ms），重逻辑交给Agent
- 给Agent全部MCP工具→按需分配（测试Agent只需database-mcp）
- 为单次任务创建Agent→Agent适合复用场景，单次任务用子代理

**Worktree隔离机制**：每个子Agent在独立Git worktree中工作，互不干扰，最终由Lead统一审查合并。

### 10.12 子代理五层嵌套限制（v2.1.172更新）

v2.1.172突破此前"深度>1被忽略"的限制：

- **五层嵌套**：主Agent → 管理型Sub-agent → 工兵型子智能体（写测试/查语法/跑部署）
- **最高5层**（5 levels deep）
- 修复了嵌套子代理父级挂起Bug
- 修复了Agent列表视图错误显示忙碌雪花30秒

### 10.13 Claudeception自动沉淀（2026-06新增）

Claudeception是Anthropic本月最火的自动进化类能力：
- 自动监测用户重复操作
- 重复3次以上→自动总结为专属Skill
- 下次同类任务自动调用，无需手动描述需求
- 安装：`npx skills add claudeception`

### 10.14 Opus 4.8 定价（2026-06更新）

| 模式 | 输入（百万token） | 输出（百万token） |
|------|-------------------|-------------------|
| 标准 | $5 | $25 |
| Fast | $10 | $50 |
| 历史对比（Opus 4.7 Fast） | $30 | $150 |

Fast模式降价约3倍。截至2026年4月，Claude Code已占据AI编程市场54%（Menlo Ventures数据）。

### 10.15 Ultracode 动态工作流触发（v2.1.160~v2.1.166）

- 原触发词 `/workflow` 已重命名为 `ultracode`
- 结合 `/goal` + `/loop` 使用
- 每工作流支持最多16个并发子Agent、1000个总Agent
- 支持中断恢复（长期运行不丢进度）
- 工作流可保存到 `~/.claude/workflows`，通过skill分发

> 本文件由 Marvis 龙虾 Agent 每2小时自动更新 | 版本: v2.3_R77 | 最后更新: 2026-06-12 09:00


---

## 十一、Anthropic 官方课程子代理管理最佳实践（R77新增 · 2026-06-12）

> 来源：Introduction to Subagents 课程 + Introduction to Agent Skills + Claude Code in Action

### 11.1 Subagent 设计六原则（Anthropic 官方课程提炼）

| 原则 | 说明 | 龙虾实现 |
|------|------|---------|
| **单一职责** | 每个子代理只做好一件事 | 5个专业 Agent（file/computer/app/search/browser） |
| **探索编辑分离** | 只读子代理先 map → 写发现到文件 → 主Agent带完整信息编辑 | 部分实现（search-agent 只读） |
| **专业化命名** | code-reviewer / test-runner / frontend-qa（非"senior engineer"） | Agent 名称已专业化 |
| **上下文隔离** | 子代理独立 Context Window，只返回摘要 | dispatch_task 独立会话 |
| **工具最小化** | 只给予完成任务所需的最小工具集 | tools/disallowedTools 控制 |
| **可复用 Skills** | Subagent 通过加载 Skills 获取领域知识 | use_skill + 全域技能库 |

### 11.2 Agent Skills 集成到 Subagent 的方式

Anthropic 课程明确了 Skills 和 Subagents 的协同模型：

```
Subagent (独立Context Window)
  ├── 自动加载匹配的 Skills（Markdown指令）
  ├── 执行专项任务
  └── 返回摘要给主 Agent
```

**关键配置**：
- Subagent YAML 中 `skills:` 字段列出可用 Skills
- Skills 本质是可复用 Markdown 指令，Claude 自动判断何时加载
- 创建 Skill 的最小化起点：从最简单的重复任务开始

### 11.3 子代理通信协议的三个层级

| 层级 | 通信方式 | 信息量 | 适用场景 |
|------|---------|--------|---------|
| L1: 结果摘要 | 子代理只返回自然语言摘要 | 最小 | 简单查询/检查 |
| L2: 结构化文件 | 子代理将发现写入文件，主Agent读取 | 中等 | 复杂分析/多文件 |
| L3: 完整记忆 | inherit_agent_id 继承上次会话全部记忆 | 最大 | 延续任务/迭代修改 |

### 11.4 从课程看子代理的生命周期管理

| 阶段 | Anthropic 课程指导 | 龙虾实践 |
|------|-------------------|---------|
| **创建** | 定义 name、description、tools、skills | YAML Frontmatter（§二 2.1） |
| **派发** | 主Agent委托任务 + 定义边界 | dispatch_task(task=结构化) |
| **监控** | heartbeat 心跳 + 超时检测 | Goal模式（§二 2.4） |
| **验收** | 验目标 + 验产物 + 补缺口 | dispatch_task 结果验收（§Main Agent 1.5） |
| **沉淀** | Dreaming 跨会话记忆巩固 | 经验记忆 + 知识库归档 |

### 11.5 Claude Partner Network Learning Path — 子代理编排四件套

Anthropic 将合作伙伴培训拆为4门模组化课程，本身就示范了子代理的编排哲学：

| 模组 | 课程 | 编排角色 |
|------|------|---------|
| 模块1 | Agent Skills | **知识注入层** |
| 模块2 | Building with Claude API | **能力执行层** |
| 模块3 | Introduction to MCP | **外部连接层** |
| 模块4 | Claude Code in Action | **工作流集成层** |

> 这四层映射到龙虾的：Skills → Tools → MCP → Agents 四层扩展栈。

### 11.6 Anthropic 子代理 7 步创建流程（R78新增）

来源：Claude Code 官方文档 `/agents` 交互式创建 + 手动 Markdown 配置 + `/agents generate` 一句话生成

**标准 7 步流程**：

| 步骤 | 操作 | 关键决策 |
|------|------|---------|
| 1. 打开界面 | `/agents` → Library → Create new agent → Personal/Project | Personal: `~/.claude/agents/`；Project: `.claude/agents/` |
| 2. 生成定义 | 选中 Generate with Claude，一句话描述 | Claude 自动生成 identifier/description/system_prompt |
| 3. 选择工具 | 从全量工具集中勾选 | 只读子代理：仅选 Read-only tools；全功能：继承所有工具 |
| 4. 选择模型 | sonnet / opus / haiku / inherit | Haiku：快速搜索/格式校验；Sonnet：分析/代码审查；Opus：复杂决策/规划 |
| 5. 选择颜色 | 背景色标识 | UI 视觉区分：探索子代理 vs 审查子代理 vs 构建子代理 |
| 6. 配置内存 | User scope / None | User scope：持久记忆目录 `~/.claude/agent-memory/`，跨会话学习 |
| 7. 保存测试 | 按 s/Enter 保存，立即可用 | 示例：`Use the code-improver agent to suggest improvements in this project` |

**子代理发现优先级**（高→低）：
1. Managed settings（组织级部署，最高优先级）
2. `--agents` CLI 标志（当前会话，不存磁盘）
3. `.claude/agents/`（项目级，可纳入版本控制）
4. `~/.claude/agents/`（用户级，跨项目共享）
5. Plugin `agents/` 目录（随插件安装，最低优先级）

**子代理 YAML frontmatter 完整参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 子代理标识符，用于委派和引用 |
| `description` | 是 | Claude 据此匹配何时调用该子代理，须描述清楚适用任务特征 |
| `tools` | 否 | 工具 allowlist/denylist，不填则继承主对话所有工具 |
| `model` | 否 | sonnet/opus/haiku/inherit，默认 inherit |
| `skills` | 否 | 预加载的 Skills 列表，子代理启动时自动注入 |
| `memory` | 否 | user/none，与 `/agents` 界面第6步对应 |
| `color` | 否 | 背景色，UI 中标识不同子代理 |
| `permissionMode` | 否 | 权限模式：default/plan/acceptEdits/bypassPermissions |
| `hooks` | 否 | 子代理专用的 Hooks 配置 |

**分叉子代理（Fork Subagent）**：
- 场景：需要对比不同方案时，从子代理分叉出分支继续探索
- 用法：`/fork` 或 `--fork-session` 从 CLI
- 机制：创建子代理会话的独立副本，不影响原会话

### 11.7 子代理自动化运维检查清单（R78新增）

**每日检查**：
- [ ] 所有子代理 YAML frontmatter 格式是否有效
- [ ] Tools allowlist 是否最小化（无多余权限）
- [ ] 子代理内存（agent-memory）是否正常累积
- [ ] 过期的临时子代理是否已清理

**每周检查**：
- [ ] description 字段是否仍匹配实际调用场景
- [ ] 模型路由策略是否需要调整（基于实际性能数据）
- [ ] .claude/agents/ 目录是否已纳入版本控制（项目子代理）
- [ ] Plugin 子代理是否与主配置冲突

**版本升级时检查**：
- [ ] Claude Code 升级后子代理兼容性验证
- [ ] 新版本特性（如 Fork/Agent Teams）是否应纳入配置
- [ ] 过期子代理的弃用/归档



Anthropic 将合作伙伴培训拆为4门模组化课程，本身就示范了子代理的编排哲学：

| 模组 | 课程 | 编排角色 |
|------|------|---------|
| 模块1 | Agent Skills | **知识注入层** |
| 模块2 | Building with Claude API | **能力执行层** |
| 模块3 | Introduction to MCP | **外部连接层** |
| 模块4 | Claude Code in Action | **工作流集成层** |

> 这四层映射到龙虾的：Skills → Tools → MCP → Agents 四层扩展栈。

---

> 本次更新: v2.4_R78 · Anthropic 子代理7步创建流程 + 自动化运维检查清单


---

## 来自 Anthropic 官方课程的自动化配置补充（2026-06-14）

### Hooks 完整生命周期事件体系（30个事件，R84更新）

Claude Code Hooks 支持在 Agent 生命周期的关键节点插入自定义逻辑：

**会话级 Hook 事件**：
| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| UserPromptSubmit | 用户提交提示前 | 注入上下文、修改 Prompt |
| PreToolUse | 工具调用前 | 权限校验、参数拦截 |
| PostToolUse | 工具调用后 | 结果审计、日志记录 |
| Notification | 通知事件 | 进度提醒、状态同步 |
| Stop | Agent 停止时 | 清理资源、生成摘要 |

**子代理级 Hook 事件**：
| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| SubagentStart | 子代理启动时 | 环境初始化、上下文注入 |
| SubagentStop | 子代理停止时 | 结果收集、资源清理 |

**Hook 配置方式**：
1. **子代理 Frontmatter 中定义**：只在特定子代理活动时执行，子代理停止时自动清理
2. **settings.json 全局定义**：在主工作会话中全局执行
3. **Windows PowerShell 适配**：需在 Hook 条目中添加 `shell: powershell` 字段


**23种生命周期事件完整清单（R84更新）**：

| 事件 | 触发时机 | 分类 |
|------|----------|------|
| `SessionStart` | 会话开始或恢复 | 会话级 |
| `Setup` | `--init-only` 或 CI 模式启动 | 会话级 |
| `UserPromptSubmit` | 用户提交提示前 | 交互级 |
| `UserPromptExpansion` | 命令展开为提示前（可阻止） | 交互级 |
| `PreToolUse` | 工具调用前（可阻止） | 工具级 |
| `PermissionRequest` | 权限对话框出现时 | 工具级 |
| `PermissionDenied` | 工具被自动模式分类器拒绝 | 工具级 |
| `PostToolUse` | 工具调用成功后 | 工具级 |
| `PostToolUseFailure` | 工具调用失败后 | 工具级 |
| `PostToolBatch` | 并行工具批次完成后 | 工具级 |
| `Notification` | Claude Code 发送通知时 | 通知级 |
| `MessageDisplay` | 助手消息文本显示时 | 通知级 |
| `SubagentStart` | 子代理生成时 | 子代理级 |
| `SubagentStop` | 子代理完成时 | 子代理级 |
| `TaskCreated` | 通过 TaskCreate 创建任务时 | 团队级 |
| `TaskCompleted` | 任务标记完成时 | 团队级 |
| `Stop` | Claude 完成响应时 | 会话级 |
| `StopFailure` | API 错误导致轮次结束时 | 会话级 |
| `TeammateIdle` | Agent Team 队友即将空闲时 | 团队级 |
| `InstructionsLoaded` | CLAUDE.md / rules 加载时 | 配置级 |
| `ConfigChange` | 配置文件在会话中变更时 | 配置级 |
| `CwdChanged` | 工作目录变更时 | 配置级 |
| `FileChanged` | 被监视文件在磁盘变更时 | 配置级 |
| `WorktreeCreate` | 通过 `--worktree` 创建 worktree 时 | Git级 |
| `WorktreeRemove` | Worktree 被移除时 | Git级 |
| `PreCompact` | 上下文压缩前 | 上下文级 |
| `PostCompact` | 上下文压缩完成后 | 上下文级 |
| `Elicitation` | MCP 服务器请求用户输入时 | MCP级 |
| `ElicitationResult` | 用户回复 MCP elicitation 后 | MCP级 |
| `SessionEnd` | 会话终止时 | 会话级 |

**五种 Hook 类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| `command` | 执行 shell 命令或脚本 | PostToolUse 后自动格式化代码 |
| `http` | 将事件 JSON POST 到 URL | 任务完成时通知 Webhook |
| `mcp_tool` | 调用配置的 MCP Server 工具 | 触发企业微信消息 |
| `prompt` | 使用 LLM 评估提示 | 判断工具调用结果是否安全 |
| `agent` | 运行 agentic 验证器 | 复杂验证任务 |


### Subagents 安全约束配置

**禁止特定子代理**：
```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

**CLI 禁用**：
```bash
claude --disallowedTools "Agent(Explore)"
```

**SQL 注入防护 Hook 示例**：
```bash
# PreToolUse Hook：阻止非 SELECT 的 SQL 执行
#!/bin/bash
if echo "$CLAUDE_TOOL_INPUT" | grep -qiE "(drop|delete|truncate|alter|insert|update)"; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi
exit 0
```

### Managed Agents 平台能力集成

**Memory 存储**：
- 工作区级别的文本文档集合
- 挂载到 Agent 容器内 /mnt/memory/ 目录
- Agent 使用标准文件工具（Bash、grep）读写
- 跨会话持久化，Session 结束时状态不丢失

**Dreaming 反思机制**：
- Agent 空闲时自动触发
- 分析过往会话的错误模式和成功经验
- 自动更新 CLAUDE.md 和 Skills
- 类似人类"睡后学习"效果

**Outcomes 结果追踪**：
- 任务完成后自动生成结构化摘要
- 记录关键决策、完成项、未完成项
- 支持多 Session 持续追踪

**Multiagent Orchestration**：
- 主导 Agent 动态创建和管理子 Agent
- 共享任务列表（待处理/进行中/已完成状态）
- 自动依赖管理，被阻塞任务等待前置完成后自动触发

### Agent Teams 配置模板

**团队 Prompt 模板**：
```
你是一个项目的主导 Agent。你的团队包含以下成员：
- architect: 架构师，负责系统设计和接口定义
- coder: 编码员，负责功能实现
- reviewer: 审查员，负责代码审查和测试覆盖检查
- docs: 文档员，负责更新文档和 CHANGELOG

当前项目：[项目描述]
任务目标：[具体任务]

请将任务拆解并分派给合适的团队成员，协调他们的工作，确保最终交付物完整且质量达标。
```

**安全约束配置（settings.json）**：
```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(pytest:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(sudo:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Edit(/**/*.env)",
      "Edit(/**/*.pem)",
      "Edit(/**/*.key)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[HOOK] Bash executed at $(date)' >> /tmp/claude-audit.log"
          }
        ]
      }
    ]
  }
}
```


### Monitors 配置规范（R84新增）

**位置**：Plugin 根目录 `monitors/monitors.json`，或在 `plugin.json` 中通过 `experimental.monitors` 内联

**必需字段**：
| 字段 | 说明 |
|------|------|
| `name` | Plugin 内唯一标识符，防止重载时重复进程 |
| `command` | 会话工作目录中持久后台运行的 shell 命令 |

**可选字段**：
| 字段 | 说明 |
|------|------|
| `description` | 监视器用途描述 |
| `when` | 触发条件，如 `"on-skill-invoke:debug"` |

**配置示例**：
```json
[
  {
    "name": "deploy-status",
    "command": "${CLAUDE_PLUGIN_ROOT}/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

**运行约束**：
- 需要 Claude Code v2.1.105+
- 仅在交互式 CLI 会话中运行
- 与 Hooks 同信任级别，无沙箱
- Monitor tool 不可用的主机上自动跳过
- stdout 每行作为通知传递给 Claude

> Monitors 是实验性组件，遵循后台观察者模式——不主动干预 Agent 决策，而是持续将外部状态变化注入为通知。



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

> 同步自：Anthropic官方课程390节全集 R80 | 2026-06-14
