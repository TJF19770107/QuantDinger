---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_73f692855ef011f1b5095254007bceed
    ReservedCode1: 3qZbMrQ+D1w5r/8j4le+j0e3thkvmjeFGOWkkEtzyYmE2wsFOeBPu3zwgrcoLVCo+FkMdJcFIKqXKprbSLXk1w9qMWDnvlhWWujNhjuukooUbDOVw2V6kgunREVyeTFUrU9ivN354xFdRSyEW611VRHRhDNeB3wOwlQ/yr7hq5SxSTCWMbM8IJVHtJI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_73f692855ef011f1b5095254007bceed
    ReservedCode2: 3qZbMrQ+D1w5r/8j4le+j0e3thkvmjeFGOWkkEtzyYmE2wsFOeBPu3zwgrcoLVCo+FkMdJcFIKqXKprbSLXk1w9qMWDnvlhWWujNhjuukooUbDOVw2V6kgunREVyeTFUrU9ivN354xFdRSyEW611VRHRhDNeB3wOwlQ/yr7hq5SxSTCWMbM8IJVHtJI=
---

# AGENTS.md — 子代理管理与自动化配置（龙虾AI分身运维手册）

> **版本**：v2.0 | **创建日期**：2026-06-01 | **更新日期**：2026-06-01
> **来源**：Anthropic Advanced Subagents + Agent Teams + Harness Patterns + Managed Agents Platform + Code with Claude 2026 + 龙虾全域模板
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

## 十二、Codex Worker 四大核心技能配置（R43新增）

> **版本**：v1.0 | **创建日期**：2026-06-02
> **参考**：[Hermes×Codex联动能力手册_v1.0.md](E:\龙虾AI主控中心\我的AI分身\知识库\Hermes×Codex联动能力手册_v1.0.md)

### 12.1 技能一：角色定义
- 定位：Codex编码执行器，隶属Hermes调度体系
- 行为：严格按task指令执行，绝对路径，结构化返回
- 输出：JSON格式 `{"status","data","files","summary","error"}`

### 12.2 技能二：项目约束
- 文件：绝对路径、禁止系统目录、统一输出目录
- 飞书CLI：执行前检查可用性、不硬编码凭证、指数退避重试
- 并行：上限5个、有依赖必须串行

### 12.3 技能三：输入示例
- AI调研→飞书文档：搜索+提炼+创建文档
- 批量CSV→飞书Base：读取+映射+批量写入
- 定时任务→自动汇报：数据采集+生成+发送

### 12.4 技能四：错误兜底
- L1（轻微）：网络超时/API限流→指数退避重试
- L2（中等）：Token过期/权限不足→自动刷新或返回错误
- L3（严重）：CLI未安装/配置缺失→终止并上报
- 禁止静默失败，任何错误返回结构化错误信息

### 12.5 自动检索规则（Codex启动时自动执行）
- 扫描目录：技能库/工作流库/Hermes Agent/OpenClaw Agent
- 加载优先级：全域模板→AGENTS→SOUL→USER→联动规范→技能手册→技能协议
- 校验：完整性检查、版本号比对、必填字段检查

---

## 十三、[R48 Anthropic Academy补全] 子代理管理与自动化深度配置

> **来源**：Anthropic Academy AC-207 Subagents + AC-201 Claude Code + AC-205 Agent Skills | 2026-06-03
> **知识库**：[Anthropic官方课程-完整知识库.md](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-完整知识库.md)

### 13.1 CLAUDE.md/Hook/Skill/Subagent/Plugin 五层配置（来源：AC-201 + AC-205 + AC-207）

**五层配置架构全览**：

| 层级 | 配置位置 | 作用域 | 加载时机 | 内容示例 |
|------|---------|--------|---------|---------|
| **CLAUDE.md** | 项目根 + 子目录 | 项目级/目录级 | 始终加载 | 项目规则、gotcha、约束、编码规范 |
| **Hook** | `.claude/hooks/` | 全局/项目级 | 生命周期事件触发 | Start/Stop/PreToolUse/PostToolUse |
| **Skill** | `~/.claude/skills/` 或 `.claude/skills/` | 按需触发 | 路径/关键词匹配时加载 | 安全审查、部署流水线、代码审查模板 |
| **Subagent** | `.claude/agents/` | 独立上下文 | 主Agent显式委派 | 代码审查员、测试运行器、文档生成器 |
| **Plugin** | 插件市场安装 | 打包分发 | 安装后生效 | Skills+Hooks+MCP配置的综合包 |

**五层协作规则**：
```
CLAUDE.md ──→ 定义"宪法"和全局约束，最高优先级
     ↓
Hook ──→ 生命周期注入，拦截关键操作（PreToolUse安全检查）
     ↓
Skill ──→ 按需加载专业知识，不常驻上下文
     ↓
Subagent ──→ 独立上下文执行专业任务，返回摘要
     ↓
Plugin ──→ 打包以上所有，社区分发
```

**配置最佳实践**（Anthropic官方推荐）：
- CLAUDE.md只放指针和gotcha，可复用专长放入Skills
- 每个Skill一个Markdown文件，不超过500行
- Subagent的CLAUDE.md独立配置，不与主Agent共享
- Hook仅在需要安全拦截或审计时使用，避免过度Hook化

### 13.2 子Agent生命周期管理（来源：AC-207 Subagents + AC-E03 Agentic AI）

**完整生命周期状态机**：

```
CREATED → DISPATCHED → RUNNING → COMPLETED
                  ↓         ↓
              CANCELLED   FAILED → RETRYING → COMPLETED/FAILED_FINAL
                  ↓
              TIMED_OUT → RETRYING → COMPLETED/FAILED_FINAL
```

**各阶段Hook注入点**（对应协议#13）：

| Hook点 | 触发时机 | 典型用途 |
|--------|---------|---------|
| `on_create` | Subagent Spec生成后 | 注入全局约束、安全策略 |
| `on_dispatch` | 派发到独立上下文前 | 工具集审查、资源配额分配 |
| `on_start` | 子Agent开始执行 | 上下文初始化、计时启动 |
| `on_iteration` | 每轮工具调用后 | 行为监控、脏计数更新 |
| `on_complete` | 正常完成 | 结果校验、摘要提取 |
| `on_fail` | 异常失败 | 错误分类、自动重试决策 |
| `on_timeout` | 超时终止 | 资源回收、部分结果保存 |

**生命周期管理参数**：
```yaml
lifecycle:
  max_runtime_seconds: 300      # 最大运行时间
  max_iterations: 50            # 最大工具调用轮数
  max_retries: 3                # 最大重试次数
  retry_backoff: exponential    # 重试退避策略
  cooldown_seconds: 10          # 同类型Subagent冷却时间
  max_concurrent_same_type: 5   # 同类型最大并发数
```

### 13.3 自动化工作流触发规则（来源：AC-201 Claude Code + AC-205 Agent Skills）

**三大触发机制**：

**A. 文件类型触发**：
```yaml
file_type_triggers:
  - patterns: ["*.py", "*.js", "*.ts"]
    agent: "code-reviewer"
    skill: "code-review"
  - patterns: ["Dockerfile", "docker-compose*.yml"]
    agent: "devops"
    skill: "container-check"
  - patterns: ["*.md"]
    agent: "doc-writer"
    skill: "format-markdown"
  - patterns: ["package.json", "Cargo.toml", "go.mod"]
    agent: "dependency-checker"
    skill: "audit-deps"
```

**B. 关键词触发**：
```yaml
keyword_triggers:
  - keywords: ["deploy", "发布", "上线"]
    skill: "deploy-checklist"
    hook: "pre_deploy_audit"
  - keywords: ["security", "安全", "漏洞"]
    skill: "security-review"
    agent: "security-auditor"
  - keywords: ["test", "测试", "验证"]
    skill: "run-tests"
```

**C. 复杂度触发**：
```yaml
complexity_triggers:
  - condition: "predicted_tokens > 5000"
    action: "split_into_subagents"
  - condition: "file_count > 20"
    action: "parallel_batch_processing"
  - condition: "dependency_depth > 5"
    action: "sequential_pipeline"
```

### 13.4 Subagent与Skills的协同配置（来源：AC-207 + AC-205）

**Skills绑定Subagent的标准模式**：
```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: 代码审查子代理，检查安全性、性能和代码规范
tools:
  - Read
  - Grep
  - Glob
skills:
  - security-review    # 安全审查Skill
  - style-check        # 代码风格Skill
  - perf-analyze       # 性能分析Skill
max_iterations: 30
timeout_seconds: 180
---

你是一个代码审查子代理。请按照绑定的Skills执行检查。
```

**Skills发现与匹配规则**：
1. 主Agent解析任务 → 提取关键词
2. 在Skills目录中按名称/描述/标签匹配
3. 匹配到的Skill绑定到Subagent的工具列表
4. Subagent启动时自动加载绑定的Skills到其独立上下文

### 13.5 自动化运维触发规则（来源：AC-201 + AC-207）

**定时任务与事件驱动对照表**：

| 触发类型 | 机制 | 适用场景 | 龙虾实现 |
|---------|------|---------|---------|
| 定时触发 | Cron/计划任务 | 知识库更新、定期审计 | AutoWake v2.0 + 协议#40 有状态心跳自主调度 |
| 文件变更 | Watch/Filesystem Event | 代码审查、格式检查 | 协议#95 事件驱动Trigger自动化 |
| API事件 | Webhook | CI/CD流水线、部署通知 | 协议#13 事件驱动自动化流水线 |
| 复杂度阈值 | Token/步骤计数 | 自动拆分Subagent | 协议#90 并行子Agent自动分解调度 |
| 异常检测 | 错误率/超时率 | 自动熔断、降级 | 协议#24 自愈回滚检查点 |

---

> **版本**：v2.3（R48 Anthropic Academy补全）
> **知识来源**：Anthropic Advanced Subagents + Agent Teams + Harness + Managed Agents + Anthropic Academy 23 Courses + 龙虾全域模板v3.44
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [USER.md](E:\龙虾AI主控中心\我的AI分身\USER.md) | [Anthropic官方课程-完整知识库.md](E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\Anthropic官方课程-完整知识库.md)
*（内容由AI生成，仅供参考）*
