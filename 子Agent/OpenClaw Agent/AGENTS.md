---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_0303856967ad11f1a0095254002afed2
    ReservedCode1: TH0rhd7HkGmtVxBdTIlJXsDaLQuX9kdTkTNOr0HAWiryTXonHHZi2kGjDp6Z728caPueVNIZakEavTmRgIfPZ1fGIqQfOt7VVL4te3B9MVesO+Iz51zJIrnV6sneBQEtTHZgXMsa0atYz8EIgrHfx6ROOw+D7+7UEPcMC6dAy0t48j/89KTecVgH4A4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_0303856967ad11f1a0095254002afed2
    ReservedCode2: TH0rhd7HkGmtVxBdTIlJXsDaLQuX9kdTkTNOr0HAWiryTXonHHZi2kGjDp6Z728caPueVNIZakEavTmRgIfPZ1fGIqQfOt7VVL4te3B9MVesO+Iz51zJIrnV6sneBQEtTHZgXMsa0atYz8EIgrHfx6ROOw+D7+7UEPcMC6dAy0t48j/89KTecVgH4A4=
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

> **版本**：v2.1(R80迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-01
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

> **版本**：v2.1（R33更新）
> **知识来源**：Anthropic Advanced Subagents + Agent Teams + Harness + Managed Agents + 龙虾全域模板v3.26 + Hermes Curator v0.12.0
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [USER.md](E:\龙虾AI主控中心\我的AI分身\USER.md) | [角色总说明书.md](E:\龙虾AI主控中心\我的AI分身\角色总说明书\角色总说明书.md)


---



---

## 十三、Anthropic Academy 核心能力注入（R79 · 2026-06-14）

> **来源**：Anthropic Academy 子代理、MCP、Skills、Hooks 全课程体系（R79蒸馏同步至龙虾分身体系）。
> **版本**：v2.5 (R79) — 对应 Anthropic Academy 2026 春季学期结业课程内容。

---

### 13.1 子代理课程精华（三大模式 + 七步创建 + 僵死检测）

#### 13.1.1 三大子代理设计模式

| 模式 | Claude Code 原生机制 | 龙虾体系实现 | 关键要点 |
|------|------|------|------|
| **Structured Outputs** | `structured_output: {schema: ...}` | 子Agent返回JSON Schema强制校验 | 杜绝"自由发挥" → 下游解析零歧义 |
| **Blocker Reporting** | 子代理主动上报阻塞状态 | Hermes Goal僵死检测五维监控 | 不死等超时 → 30s心跳 + 产出变化检测 |
| **Tool Restriction** | `allowed_tools` / `disallowed_tools` 白名单 | 所有子Agent `disallowedTools` 机制 | 最小工具集原则 → 安全沙箱 |

**Structured Outputs 实现规范**：
```yaml
# 子代理输出 schema 定义（Claude Code 子代理配置）
subagents:
  invoice-parser:
    structured_output:
      schema:
        type: object
        required: [status, invoices]
        properties:
          status: { enum: [success, partial, empty] }
          invoices:
            type: array
            items:
              type: object
              required: [amount, date, vendor]
              properties:
                amount: { type: number }
                date: { type: string, format: date }
                vendor: { type: string }
                category: { type: string }
          errors: { type: array, items: { type: string } }
```

**Blocker Reporting 实现规范**：
```python
# 子代理阻塞上报（Claude Code 子代理配置）
blocker_reporting:
  heartbeat_interval: 30  # 秒
  auto_report_on:
    - tool_failure_count >= 2     # 连续2次同一工具失败
    - missing_context_detected     # 上下文不足
    - permission_denied            # 权限拒绝
    - timeout > 120               # 超时2分钟
  report_format:
    status: blocked
    blocker_type: <type>
    last_action: <description>
    suggestion: <提议的解决方案>
```

#### 13.1.2 子代理七步创建流程（Claude Code 标准）

```
Step 1: 定义职责边界（一句话描述子代理职责）
  → 输出：职责声明 + 输入/输出规格

Step 2: 设计工具集（最小工具集原则）
  → 输出：allowed_tools 清单 + disallowed_tools 清单

Step 3: 设计输出格式（Structured Outputs JSON Schema）
  → 输出：JSON Schema 定义文件

Step 4: 编写系统提示（System Prompt）
  → 输出：子代理 SOUL.md 或系统指令

Step 5: 配置 Blocker Reporting（阻塞上报策略）
  → 输出：heartbeat + report 配置

Step 6: 编写测试用例（验收标准）
  → 输出：测试 prompt + 预期输出

Step 7: 集成注册（注册到 Agent Router）
  → 输出：路由表条目更新
```

#### 13.1.3 Goal僵死检测机制（五维监控）

| 监控维度 | 检测方法 | 僵死判定 | 恢复动作 |
|---------|---------|---------|---------|
| **心跳信号** | 每30秒写入心跳时间戳 | >60秒无心跳 | 唤醒 + 注入当前状态 |
| **工具调用产出率** | 最近10次工具调用的成功率 | 成功率 <30% 持续2分钟 | 切换备用工具/降级策略 |
| **代币消耗速率** | 每秒token消耗速率 | 速率突降 >80% 持续1分钟 | 可能是死循环，强制注入新指令 |
| **上下文利用率** | 已用token/总预算 | >90% 且无产出 | 强制压缩上下文后继续 |
| **产出变化检测** | 连续3次输出内容cosine相似度 >0.95 | 判定为重复产出僵死 | 注入多样性提示/更换策略 |

---

### 13.2 Hooks 生命周期注入最佳实践（Anthropic Academy R79更新）

**五大注入点生命周期**：

| 注入点 | 触发时机 | 典型用途 | 安全级别 |
|------|---------|---------|---------|
| **PreToolUse** | 工具调用执行前 | 参数校验、敏感操作拦截、自动备份 | 中风险 |
| **PostToolUse** | 工具调用执行后 | 结果校验、自动格式化、操作日志 | 低风险 |
| **PreToolExtraction** | 工具结果提取前 | 结果预处理、自动摘要 | 低风险 |
| **PostToolExtraction** | 工具结果提取后 | 结果后处理、格式转换 | 低风险 |
| **Notification** | 特定事件触发 | 任务完成通知、错误告警 | 低风险 |

**Hooks 设计四条原则**（Anthropic Academy 最佳实践）：

1. **幂等性原则**：同一Hook多次执行结果一致，避免副作用累积
2. **快速返回原则**：Hook执行超时 <5秒，长时间操作应异步化
3. **故障透明原则**：Hook失败不应阻断主流程，降级为日志+继续执行
4. **最小权限原则**：Hook只能访问完成任务所需的最小范围

**龙虾体系 Hooks 映射表**：

| Claude Code Hook | 龙虾对标实现 | 状态 |
|------|------|------|
| PreToolUse 备份 | Agent执行前自动快照 | 已有 |
| PostToolUse Lint | 代码检查子Agent | 已有 |
| PreToolExtraction 摘要 | 上下文压缩模块 | 已有 |
| Notification 告警 | Hermes 任务状态推送 | 已有 |
| PostToolUse 日志 | 全域操作审计日志 | 已有 |

---

### 13.3 Skills 工程化（Anthropic Academy R79核心）

#### 13.3.1 Progressive Disclosure 目录结构

> **核心理念**：技能目录只在需要时加载，避免一次性塞入全部指令。

```
skills/
├── skill-name/
│   ├── SKILL.md              # 主入口：触发条件 + 简短说明 + 子文件索引
│   ├── reference.md          # 详细参考（仅在需要时加载）
│   ├── examples.md           # 使用示例（用户提问模式匹配触发）
│   ├── scripts/              # 可执行脚本
│   │   ├── main.py
│   │   └── utils.py
│   └── templates/            # 输出模板
│       └── report.md
```

**加载策略**：
| 层级 | 内容 | 加载时机 | 大小限制 |
|------|------|---------|---------|
| **层1: SKILL.md** | 触发条件 + 概述 + 子文件索引 | 技能激活时（必须加载） | ≤500 token |
| **层2: reference.md** | 详细规范、API文档 | 任务需深度参考时按需加载 | ≤2000 token |
| **层3: examples.md** | 典型用例 | 用户提问模式匹配时触发加载 | ≤1000 token |
| **层4: scripts/** | 可执行代码 | 任务需要计算/转换时执行 | 无限制（不在上下文中） |

#### 13.3.2 三级共享机制

| 级别 | 共享方式 | 适用场景 | 龙虾对标 |
|------|---------|---------|------|
| **Level 1: Commit to Repo** | 直接提交到项目仓库的 `.claude/skills/` | 项目专属技能（单仓库内共享） | 子Agent内部技能目录 |
| **Level 2: Plugin Publishing** | 打包发布为插件，跨仓库安装 | 团队/组织级技能（跨仓库共享） | 技能库统一管理 |
| **Level 3: Enterprise Deploy** | 企业平台统一部署，强制所有Agent加载 | 企业级标准技能（安全审计/合规审查） | 企微侧边栏企业部署 |

**选型指南**：
```
技能受众？
├── 仅当前项目 → Level 1: commit到 .claude/skills/
├── 团队内多项目 → Level 2: 打包发布为插件
└── 全企业强制 → Level 3: 平台统一部署
```

---

### 13.4 MCP 生产级部署（Anthropic Academy R79核心）

#### 13.4.1 Transport 选型：stdio vs HTTP SSE

| 维度 | stdio | HTTP SSE |
|------|------|------|
| **连接方式** | 本地进程 stdio 管道 | HTTP 长连接（SSE推送） |
| **网络要求** | 仅本地 | 需网络，支持远程 |
| **并发能力** | 单客户端 | 多客户端并发 |
| **部署复杂度** | 低（直接启动子进程） | 中（需HTTP服务器 + 证书管理） |
| **适用场景** | 本地开发、单Agent使用 | 团队共享、企业平台、多个Agent同时调用 |
| **安全** | 天然隔离（仅本地进程） | 需 Token 鉴权 + HTTPS |
| **龙虾对标** | 子Agent本地调用 | 豆包桥接（跨进程HTTP通信） |

**选型决策树**：
```
MCP Server需要被多个Agent同时调用？
├── 否 → stdio（简单、高效、天然安全）
└── 是 → HTTP SSE
    └── 是否有跨网络需求？
        ├── 否 → HTTP SSE（本地多Agent）
        └── 是 → HTTP SSE + HTTPS + Token鉴权
```

#### 13.4.2 生产级容错五机制

| 机制 | 实现 | 触发条件 | 行为 |
|------|------|---------|------|
| **指数退避重试** | `retry_with_backoff(base=1s, max=30s, factor=2)` | 网络错误/服务不可用 | 1s→2s→4s→8s→16s→30s... 最多5次 |
| **Token鉴权** | `Authorization: Bearer <token>` 请求头校验 | 每次HTTP请求 | 拒绝未授权请求，返回401 |
| **连接保活** | SSE heartbeat 每15秒发送 keepalive | SSE连接空闲 | 检测断开，自动重连 |
| **熔断器** | 连续5次失败 → 熔断30秒 → 半开探测 | 服务降级 | 保护下游服务不被雪崩 |
| **优雅降级** | 优先读缓存，限流时返回部分结果 | 压力过大/服务降级 | 返回 stale 结果 + 降级标记 |

---

### 13.5 认证考试五大领域对标（Anthropic Academy → 龙虾体系）

> **来源**：Anthropic Academy Claude Certified Architect 认证考试大纲。

| 考试领域 | 权重 | 龙虾体系对标 | 覆盖度 | 主要差距 |
|---------|:---:|------|:---:|------|
| **1. Agent Architecture Design** | 25% | SOUL.md 二章 + 子Agent架构 | 85% | 缺少 Formal Agentic Architecture 理论框架 |
| **2. Tool Integration & MCP** | 20% | MCP生产级部署 + 工具设计原则 | 20% | **最大短板**：未系统学习 MCP Server 开发与认证机制 |
| **3. Skills & Hooks Engineering** | 15% | AGENTS.md 13.3 + SOUL.md 2.7 | 70% | 缺少 Skills CI/CD 自动化流程 |
| **4. Sub-Agent Orchestration** | 20% | 子代理三大模式 + 上下文隔离 | 90% | 几乎全覆盖 |
| **5. Safety & Guardrails** | 20% | 六层安全纵深 + 工具白名单 | 80% | 缺少 Anthropic 官方安全评审标准 |
| **综合覆盖率** | 100% | — | **~73%** | — |

**R79 优先建设项（P0-P3）**：

| 优先级 | 建设项 | 原因 | 预期收益 |
|:---:|------|------|------|
| **P0** | MCP Server 开发与部署实操（stdio + HTTP SSE） | 认证考试覆盖率最大短板（20%→5%） | 认证覆盖率 +15% |
| **P1** | Formal Agent Architecture 理论学习 | 补齐架构设计理论缺口 | 认证覆盖率 +10% |
| **P2** | Skills CI/CD 自动化发布流程 | 完善团队级技能共享 | 团队效率提升 |
| **P3** | Anthropic 安全评审标准对标 | 满足认证考试安全领域要求 | 认证覆盖率 +5% |

---

> **版本更新记录**：v2.5 (R79) — 基于 Anthropic Academy 2026 春季学期全课程体系蒸馏。详细课程内容见 `Obsidian知识库/共享知识库/Anthropic官方课程-390节全集.md`。

*（内容由AI生成，仅供参考）*

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
