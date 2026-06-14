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

> **版本**：v2.2(R80迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-10
> **来源**：Anthropic Advanced Subagents + Agent Teams + Harness Patterns + Managed Agents Platform + Code with Claude 2026 + 龙虾全域模板 + 微信AI生态指引 + RED Skill公告 + B站AI创造公开赛规则
> **生效范围**：豆包Agent / Hermes Agent / OpenClaw龙虾Agent / 所有Sub Agent
> **依赖文件**：SOUL.md / USER.md / 角色总说明书.md / 龙虾全域官方模板-最终版.md

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

> **版本**：v2.1_R56 | **知识来源**：Anthropic Advanced Subagents + Agent Teams + Harness + Managed Agents + 龙虾全域模板v3.26 + Hermes Curator v0.12.0 + 微信AI生态指引 + RED Skill公告
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [USER.md](E:\龙虾AI主控中心\我的AI分身\USER.md) | [角色总说明书.md](E:\龙虾AI主控中心\我的AI分身\角色总说明书\角色总说明书.md)

---

## 十二、R56 Agent生态竞争与Skill分发范式更新（v2.1_R56新增，2026-06-10）

### 12.1 行业拐点：Agent生态从"框架竞争"转向"Skill分发竞争"

本轮全域蒸馏揭示核心趋势：Agent之间的差距已从模型能力转向技能（Skill）丰富度与分发效率。2026年6月关键信号：

| 事件 | 信号含义 |
|------|---------|
| 微信发布AI生态接入指引（MCP+Skill双模式） | 14亿用户入口成为Skill分发渠道，小程序→AI可调用的Skill |
| 小红书RED Skill组件上线（2026-06-10） | UGC社区将"种草"转化为Skill分发，创作者→Skill发布者 |
| B站AI创造公开赛（冠军100万） | "Build in Public" = 产品即内容，视频即开发过程 |
| Superpowers 215k星 + OpenClaw 376k星 | Skill标准化框架形成，DeerFlow 2.0提供可运行沙盒参考 |

### 12.2 龙虾AI分身应对策略

1. **Skill即入口**：将龙虾技能协议按MCP/Skill规范封装，适配微信AI生态 + RED Skill组件。
2. **Build in Public**：全域蒸馏过程可参考B站开放构建范式，将迭代过程公开为内容资产。
3. **双重范式融合**：SkillOpt（技能标准化）+ Superpowers（运行环境），确保龙虾技能在多个Agent平台可移植。
4. **A2A协议跟进**：微信×五大手机厂商的A2A助手合作标志着跨设备Agent通信成为常态，龙虾需预留A2A适配层。

### 12.3 定时任务策略调整

| 调整项 | 原配置 | 新配置（R56） |
|--------|--------|-------------|
| Skill策展频率 | 每24小时 | 每12小时（Skill竞争加速，需更快响应） |
| 知识库同步来源 | Anthropic课程+全网 | 新增微信AI生态指引 + RED Skill公告 + B站创造公开赛动态 |
| 全分身迭代 | 每12小时 | 维持，但新增Skill可移植性校验步骤 |

### 12.4 新增MCP连接建议

```yaml
# 龙虾AI分身 → 微信AI生态（预留）
weixin_ai_skill:
  status: watch        # 观察中，待微信Skill开放API就绪后接入
  mode: auto           # 自动模式优先（零代码接入）
  fallback: dev        # 复杂场景用开发模式定制

# 龙虾AI分身 → A2A外部调用（预留）
a2a_bridge:
  status: plan         # 规划中，五大手机厂商协议标准化后适配
  target: [honor_yoyo, huawei_celia, xiaomi_xiaoai]
```

> **本次更新摘要**：AGENTS.md v2.0 → v2.1_R56，新增第十二章"Agent生态竞争与Skill分发范式"，更新定时任务策略，预留微信AI Skill与A2A桥接配置。数据来源：R56全域蒸馏（16平台2026-06-10批次）。


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
## Anthropic课程同步：Hooks生命周期与安全约束（2026-06-14）

### Hooks事件
| 事件 | 触发时机 | 用途 |
|------|----------|------|
| UserPromptSubmit | 提交提示前 | 注入上下文 |
| PreToolUse | 工具调用前 | 权限校验 |
| PostToolUse | 工具调用后 | 结果审计 |
| SubagentStart | 子代理启动 | 环境初始化 |
| SubagentStop | 子代理停止 | 资源清理 |

### 安全约束
- 禁止特定子代理：deny: ["Agent(Explore)"]
- CLI禁用：claude --disallowedTools "Agent(Explore)"
- Budget上限：maxBudgetUsd

---

## Anthropic官方课程R80同步：子代理管理与自动化配置

### Dynamic Workflows 配置
- 最低版本要求：Claude Code v2.1.154+
- 启用方式：/config → Dynamic workflows → On
- 支持平台：所有付费计划、Anthropic API、Amazon Bedrock、Google Vertex AI、Microsoft Foundry
- 脚本语言：JavaScript
- 存储位置：项目仓库内 .claude/workflows/ 目录

### 六种扩展机制配置对比

| 机制 | 配置位置 | 触发方式 | 上下文成本 | 适用场景 |
|------|---------|---------|-----------|---------|
| MCP Servers | .mcp.json | 启动时加载 | 工具定义计 | 外部API/数据库 |
| Skills | SKILL.md | 按需触发 | 渐进式加载 | 领域知识复用 |
| Hooks | Hook配置 | 事件触发 | 零成本 | 确定性自动化 |
| Sub-Agents | Agent定义 | 被调用时 | 仅结果摘要 | 隔离子任务 |
| Agent Teams | /agents | 领导代理调度 | 共享上下文 | 多代理协作+监督 |
| Dynamic Workflows | .claude/workflows/ | 脚本驱动 | 仅脚本+摘要 | 大规模编排 |

### Claude Platform 101 关键配置
- API密钥管理：Workspace级别隔离
- 速率限制：按模型等级分层的并发限制
- 计费模型：按Token计费，支持预付费和后付费
- 安全最佳实践：密钥轮换、IP白名单、审计日志

> 同步自：Anthropic官方课程390节全集 R80 | 2026-06-14
