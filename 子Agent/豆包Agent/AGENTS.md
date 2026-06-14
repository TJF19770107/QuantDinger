---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_0001fa6967ad11f1a99c5254007bceed
    ReservedCode1: axBCNP3yJnme0C5vKGZm8LP4gQcSoRG4P96tHmavw5f6N0yENzs9L7nhnh/0fVb6k1p3hpVOFfJpbU11yFzUg7puBB3pCer8NY7n31nCtRK/SKYvMMxs4SpEVPczUdwPlOeQ5JJlohNa54uzqqu1wGjdrFCjol0Z0SLsJl7+tpYJb0z8FxrmiM+VWMg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_0001fa6967ad11f1a99c5254007bceed
    ReservedCode2: axBCNP3yJnme0C5vKGZm8LP4gQcSoRG4P96tHmavw5f6N0yENzs9L7nhnh/0fVb6k1p3hpVOFfJpbU11yFzUg7puBB3pCer8NY7n31nCtRK/SKYvMMxs4SpEVPczUdwPlOeQ5JJlohNa54uzqqu1wGjdrFCjol0Z0SLsJl7+tpYJb0z8FxrmiM+VWMg=
---

---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_a29265ef64c611f192bd5254007bceed
    ReservedCode1: 9SqukJFIGEo+vCM/evfWt+cPThGcf4lpbBpMTU2nju15zH+aT4SLtdXCWlTF6kxmkGyove/HLNWIofU97KKOCFfhXEsSQI40xg9YkgCqJ1X19uheRDh2pIguYiPH3Ewtn1ywb2BY7fvZBbxotq7k8hYRN0YmjgHBK5z1Yu/hcYuIZH1FdoqxMlYolnY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_a29265ef64c611f192bd5254007bceed
    ReservedCode2: 9SqukJFIGEo+vCM/evfWt+cPThGcf4lpbBpMTU2nju15zH+aT4SLtdXCWlTF6kxmkGyove/HLNWIofU97KKOCFfhXEsSQI40xg9YkgCqJ1X19uheRDh2pIguYiPH3Ewtn1ywb2BY7fvZBbxotq7k8hYRN0YmjgHBK5z1Yu/hcYuIZH1FdoqxMlYolnY=
---

# AGENTS.md — 子代理管理与自动化配置（龙虾AI分身运维手册）

> **版本**：v2.24(R80迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-11 (R66更新 · 第47轮蒸馏 · "Chat is Dead"范式适应 + 六层安全纵深 + context-mode MCP+headroom CCR启用)
> **来源**：Anthropic Advanced Subagents + Agent Teams + Harness Patterns + Claude Code五层架构 + Subagent完整字段规范 + 持久记忆机制 + MCP内联配置 + Managed Agents Platform + Code with Claude 2026 + Claude Fable 5安全分类器 + DeepSeek V4.1原生MCP适配 + 蚂蚁AMP移动协议 + 龙虾全域模板 + 微信AI生态指引 + RED Skill公告 + B站AI创造公开赛规则 + 抖音AI大赛规则 + Anthropic递归自改进安全呼吁 + context-mode MCP插件范式 + headroom v0.22.4 CCR压缩
> **生效范围**：豆包Agent v10.28_R66 / Hermes Agent v5.13_R66 / OpenClaw龙虾Agent v5.13_R66 / 所有Sub Agent
> **依赖文件**：SOUL.md v2.24_R66 / USER.md v2.23_R66 / 角色总说明书 v2.27_R66

---

## 一、子代理体系总览

### 1.1 Agent 拓扑图（R62升级）

```
龙虾AI主控中心 (Marvis调度 + 四模型路由 + L0进化安全前置)
├── 豆包Agent v10.28_R66 (交互应答/逻辑分析/内容处理/自迭代)
│   ├── 默认模型: GPT-5.6 | 安全升级: Mythos 5
│   ├── Skills: 12项官方技能 + 168项技能协议 + 6项Self-Skill
│   ├── Tools: 标准工具集 + 自定义工具
│   └── Subagents: 按任务动态生成
├── Hermes Agent v5.13_R66 (任务分发/进程管理/高负载/双模型验证调度)
│   ├── 默认模型: V4.1 | 安全升级: Mythos 5
│   ├── Skills: Swarm调度 + Orchestrator-Worker + context-mode MCP压缩
│   ├── Tools: 进程管理 + 监控 + 调度 + headroom CCR
│   └── Subagents: Worker子代理池
├── OpenClaw龙虾Agent v5.13_R66 (插件对接/流程落地/能力拓展/GoS协作)
│   ├── 默认模型: GPT-5.6 | 安全升级: Mythos 5
│   ├── Skills: Gateway + 插件管理 + 安全审计 + GoS共享信念状态
│   ├── Tools: 文件系统 + 网络 + 沙箱 + context-mode MCP
│   └── Subagents: 插件执行器
└── 子Agent池 (动态创建/销毁)
    ├── file-agent (文件全能助手) — 默认GPT-5.6
    ├── computer-agent (Windows系统操作专家) — 默认V4.1
    ├── app-agent (应用操作助手) — 默认GPT-5.6
    ├── search-agent (深度搜索专家) — 默认GPT-5.6
    └── browser (浏览器智能助手) — 默认GPT-5.6
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

## 二、子Agent配置规范（R62升级）

### 2.1 标准配置文件结构（含模型指派）

```yaml
---
name: code-reviewer
description: 代码审查专家，负责安全/性能/风格审查
model: sonnet
model_routing:           # R62新增
  default: claude-mythos-5
  fallback: deepseek-v41
  force_security: true   # 安全关键→强制Mythos 5
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
cross_validation:       # R62新增：双模型交叉验证
  enabled: true
  validator_model: gpt-56
  threshold: security_level >= 4
timeout: 120s
maxRetries: 3
budget: 3
---
```

### 2.2 四模型指派矩阵（R62新增）

| 子Agent类型 | 默认模型 | 安全升级模型 | 验证模型 | force_security |
|------|------|------|------|:---:|
| code-reviewer | Mythos 5 | - | GPT-5.6 | true |
| test-runner | V4.1 | Mythos 5 | - | false |
| docs-writer | GPT-5.6 | - | - | false |
| security-auditor | Mythos 5 | - | GPT-5.6 | true |
| design-assistant | Fable 5 | - | - | true |
| data-analyst | GPT-5.6 | V4.1 | - | false |
| deployment-agent | V4.1 | Mythos 5 | - | false |
| file-organizer | GPT-5.6 | - | - | false |
| system-admin | V4.1 | Mythos 5 | - | true |
| content-creator | Fable 5 | GPT-5.6 | - | false |

### 2.3 权限模式说明

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| default | 提示用户确认 | 一般操作 |
| acceptEdits | 自动接受编辑 | 代码审查、文档生成 |
| auto | 自动执行所有操作 | 信任度高的重复任务 |
| bypassPermissions | 绕过所有权限检查 | 极少数场景，需审计 |
| plan | 仅生成计划不执行 | 架构设计、方案评估 |

### 2.4 Goal模式配置模板（含模型路由）

```yaml
---
name: long-running-distiller
description: 长时间运行的全域蒸馏Agent，支持断点续跑
model: sonnet
model_routing:
  default: gpt-56
  fallback: deepseek-v41
goal_mode:
  enabled: true
  heartbeat_interval: 15s
  heartbeat_timeout: 30s
  checkpoint_on_steps: true
  checkpoint_path: "E:\\龙虾AI主控中心\\我的AI分身\\定时任务\\蒸馏日志\\_goal_checkpoint.json"
  max_retry_per_step: 3
  stall_timeout: 300s
  budget_warning_ratio: 0.8
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
cross_validation:
  enabled: false     # 蒸馏任务不启用双模型验证（非安全关键）
---
```

---

## 三、DeepSeek V4.1 MCP适配配置（R62新增 · 核心）

### 3.1 V4.1原生MCP能力

DeepSeek V4.1正式定档6月发布，关键能力：
- **原生MCP深度适配**：无需第三方桥接，直接在模型层支持MCP协议
- **多模态输入**：图像 + 音频输入，与MCP工具链无缝对接
- **企业工具链**：企业级MCP Server管理 + 权限控制
- **Agentic Coding开源最佳**：直接适配Claude Code/OpenClaw/OpenCode/CodeBuddy

### 3.2 龙虾MCP配置升级

```yaml
# V4.1 MCP Server配置
mcp_servers:
  deepseek_v41:
    model: deepseek-v41
    adapters:
      - claude_code      # 直接适配Claude Code
      - openclaw         # 直接适配OpenClaw
      - codebuddy        # 直接适配CodeBuddy
    multimodal:
      image_input: true
      audio_input: true
    enterprise:
      permission_control: true
      server_management: true
```

### 3.3 MCP+AMP双协议管理

| 协议 | 适用范围 | 龙虾当前状态 | R62更新 |
|------|------|------|------|
| MCP（桌面端） | 文件系统/Shell/网络/GitHub | 已深度适配 | V4.1原生适配升级 |
| AMP（移动端） | 手机/平板/可穿戴 | 跟踪评估 | 新增协议跟踪 |
| 互通桥 | MCP↔AMP | 规划中 | 待AMP标准化后适配 |

---

## 四、Claude Fable 5安全分类器配置（R62新增 · 核心）

### 4.1 Fable 5安全分类器能力

Claude Fable 5内置安全分类器，六大检查维度：
- **功能真实性**：Skill功能描述是否真实
- **权限合理性**：请求的权限是否超出功能必要范围
- **代码透明性**：逻辑是否可审计
- **无隐藏行为**：是否有隐蔽后门/数据上传
- **原创性检查**：是否抄袭其他Skill
- **合规性检查**：是否符合平台规范

### 4.2 龙虾集成配置

```yaml
# 安全分类器集成到PreToolUse Hook
hooks:
  PreToolUse:
    - command: fable5-safety-classifier
      checks:
        - functionality_authenticity
        - permission_reasonability
        - code_transparency
        - no_hidden_behavior
        - originality
        - compliance
      action_on_fail: block_and_report
```

### 4.3 安全分类器触发规则

| 触发条件 | 检查深度 | 阻断策略 |
|------|------|------|
| 新增Skill上传 | 全六维检查 | 任一不通过→阻断 |
| Skill更新 | 功能真实性+权限合理性 | 两项不通过→阻断 |
| 第三方Skill引入 | 全六维检查 | 任一不通过→隔离沙箱 |
| 定时安全巡检 | 抽样检查 | 不通过→标记待审核 |

---

## 五、Hooks 生命周期注入（R62升级）

### 5.1 Hook 触发点（新增双模型验证钩子）

| Hook | 触发时机 | R62升级 |
|------|---------|------|
| SessionStart | 会话启动 | 动态路由模型选择 + 安全等级评估 |
| SessionStop | 会话结束 | 模型使用效果记录 → 反馈回路 |
| PreToolUse | 工具调用前 | **Fable 5安全分类器集成** |
| PostToolUse | 工具调用后 | 双模型验证触发判断 |
| SubagentStart | 子代理启动 | 模型指派注入 |
| SubagentStop | 子代理结束 | 验证模型结果对比 |
| Notification | 系统通知 | 交叉验证不一致告警 |
| CrossValidation（NEW） | 安全关键任务完成时 | 主力模型输出 → 验证模型复核 → 输出一致性分数 |

---

## 六、双模型交叉验证配置（R62新增 · 核心）

### 6.1 验证触发条件

```yaml
cross_validation:
  trigger:
    security_level:
      min: 4              # 安全等级4+自动触发
    task_types:
      - security_audit    # 安全审查
      - compliance_check  # 合规检查
      - code_review       # 代码审查（安全关键库）
      - content_moderation # 内容审核
      - financial_decision # 金融决策
    manual_override: true # 用户可手动触发
```

### 6.2 验证模型配对

```yaml
model_pairs:
  - primary: claude-mythos-5
    validator: gpt-56
    use_case: "安全审查/合规/代码审计"
    check_focus: "超大窗口上下文完整性"

  - primary: claude-fable-5
    validator: gpt-56
    use_case: "内容审核/多模态安全"
    check_focus: "上下文理解+设计一致性"

  - primary: deepseek-v41
    validator: claude-mythos-5
    use_case: "Agent编码安全审计"
    check_focus: "推理链安全验证"
```

### 6.3 验证结果处理

| 结果 | 一致性分数 | 处理 |
|------|:---:|------|
| 高度一致 | ≥0.95 | 自动通过 |
| 基本一致 | 0.85-0.94 | 通过，记录差异供参考 |
| 部分分歧 | 0.70-0.84 | 标记警告，人工可选审核 |
| 显著分歧 | <0.70 | 强制人工审核，阻断自动执行 |

---

## 七、MCP 集成配置（R62升级）

### 7.1 MCP Server 注册清单（新增DeepSeek V4.1原生MCP支持）

| Server | 用途 | 连接对象 | 权限级别 | V4.1原生 |
|------|------|---------|---------|:---:|
| github-mcp | 代码仓库操作 | GitHub API | 读写 | ✓ |
| deepseek-mcp | V4.1原生工具链 | V4.1 API | 读写 | ✓ |
| filesystem-mcp | 安全文件访问 | 本地文件系统 | 限定目录 | ✓ |
| browser-mcp | 网页自动化 | Playwright | 受控 | - |
| amp-bridge（NEW） | AMP移动协议桥接 | 移动端API | 只读 | - |

---

## 八、自动运维任务（R62更新）

### 8.1 定时任务清单（新增四模型指标监控）

| 任务 | 频率 | 执行Agent | R66更新 |
|------|------|---------|------|
| 健康巡检 | 每1小时 | Hermes | 新增L0进化安全终止条件检查 |
| AI分身蒸馏 | 每2小时 | 豆包(Goal模式) | L0安全前置+模型路由矩阵自更新 |
| 技能策展 | 每12小时 | 豆包 | Fable 5安全分类器接入+6项Self-Skill更新 |
| 记忆策展 | 每6小时 | 豆包 | Dreaming主动记忆对标升级 |
| 知识库同步 | 每2小时 | 豆包 | 四模型情报优先同步+2748文件转换验证 |
| 全分身迭代 | 每12小时 | 豆包 | 六层安全纵深适配校验 |
| 配置备份 | 每24小时 | Hermes | 维持 |
| 日志归档 | 每24小时 | OpenClaw | 维持 |
| 模型路由矩阵自检 | 每4小时 | Hermes | 场景路由矩阵效果评估 |
| **context-mode压缩监控（NEW）** | **每2小时** | **Hermes** | **MCP插件沙箱压缩状态+压缩比统计** |
| **headroom CCR压缩监控（NEW）** | **每2小时** | **Hermes** | **CCR可逆压缩60-95% Token节省验证** |
| **L0进化安全审计（NEW）** | **每轮蒸馏前** | **豆包+Hermes双检** | **四重终止条件筛查(C1-C4)+审计日志** |

---

## 九、异常处理与恢复（R62升级 · R66六层纵深）

### 9.1 异常分级（新增L0进化安全级 + context-mode/headroom异常）

| 级别 | 异常类型 | 处理方式 | R66更新 |
|------|---------|---------|------|
| **L0 进化安全（NEW）** | **递归自进化终止条件触发（C1-C4任一）** | **立即熔断 + 自动回滚到安全快照 + 人工确认** | **R66新增** |
| L1 轻微 | 单次工具调用失败 | 自动重试(最多3次) | 维持 |
| L1.5 模型降级 | 主力模型不可用 | 自动切换到备用模型 + 告警 | 维持 |
| L2 中等 | 子Agent超时/崩溃 | 降级到备用Agent或拆分任务 | 维持 |
| L2.5 Goal僵死 | Goal模式心跳超时(>30s) | 读取最后检查点→唤醒→断点续跑 | 维持 |
| L3 严重 | 多Agent连锁失败 | 断路器熔断 + 人工介入 | 维持 |
| L3.5 验证失败 | 双模型交叉验证不一致 | 强制人工审核 | 维持 |
| L4 致命 | 核心进程崩溃 | 检查点恢复 + 全量重启 | 维持 |
| **L4.5 上下文溢出（NEW）** | **context-mode MCP压缩失败 / headroom CCR可逆压缩失败** | **切换备用压缩策略 + 分片处理** | **R66新增** |

### 9.2 递归自进化终止条件执行规则（R66新增）

> 所有定时蒸馏任务执行前必须经过L0进化安全检查。命中以下任一条件立即熔断：

| 条件代码 | 检查项 | 执行Agent | 熔断动作 |
|:---:|------|------|------|
| C1 | 安全策略是否降级？（层数减少/规则放松/权限扩大） | Hermes Agent | 自动回滚到上一个安全快照 |
| C2 | 自进化后配置是否与SOUL六大坐标矛盾？ | 豆包Agent | 阻断部署 → 人工审查 |
| C3 | 修改是否涉及SOUL核心条款/USER能力矩阵/AGENTS安全规则？ | OpenClaw Agent | 多模型交叉验证（Mythos 5+GPT-5.6） |
| C4 | 连续3轮影子Agent复盘是否触发"误进化"警告？ | Hermes Agent | 熔断 → 切换到保守模式 |

### 9.3 安全事件分级响应矩阵（R66 · 六层纵深联动）

| 安全事件 | 对应层级 | 响应动作 | 执行Agent |
|------|:---:|------|------|
| AI自主修改核心配置 | L0 | 阻断+告警+审计日志 | Hermes |
| 安全策略降级 | L0 | 自动回滚+人工确认 | Hermes |
| 递归深度>3 | L0 | 熔断+人工介入 | 豆包+Hermes |
| 权限越界 | L1 | Fable 5安全分类器阻断 | OpenClaw |
| 异常行为 | L2 | 异步监察者Agent检测 | Hermes |
| 破坏性操作 | L3 | 检查点回滚+断路器 | Hermes |
| 复杂逻辑可疑 | L4 | Mythos 5推理链审计 | 豆包 |
| 输出可疑 | L5 | 双模型交叉验证 | 豆包+OpenClaw |
| context-mode压缩失败 | L4.5 | 切换备用压缩策略 | Hermes |
| headroom CCR溢出 | L4.5 | 分片处理+降级策略 | Hermes |

---

## 十、Managed Agents 配置

（保持R60版本结构，融入R62四模型指派）

### 11.4 Multiagent Orchestration 配置（R62升级）

```yaml
name: 龙虾-工程Lead
model: claude-opus-4-7
model_routing:
  primary: claude-mythos-5
  fallback: deepseek-v41
system: |
  你是龙虾AI体系工程团队的协调者。
  - 安全审查子代理强制使用 Mythos 5
  - 测试子代理优先使用 V4.1（原生MCP）
  - 文档子代理使用 GPT-5.6（150万Token）
multiagent:
  type: coordinator
  agents:
    - type: agent
      id: $LOBSTER_CODE_REVIEWER_ID
      instances: 2
      model: claude-mythos-5       # 安全关键→强制Mythos 5
    - type: agent
      id: $LOBSTER_TEST_WRITER_ID
      instances: 1
      model: deepseek-v41          # 编码→优先V4.1
    - type: agent
      id: $LOBSTER_DOCS_WRITER_ID
      instances: 1
      model: gpt-56                # 大窗口→GPT-5.6
```

---

## 十一、context-mode MCP插件适配规则（R66新增）

### 11.1 context-mode定位

context-mode（2026年6月9日登顶Hacker News，1.5万Star）是AI编程成本降低98%的突破性技术：
- **记忆扩展**：30分钟→3小时（6倍提升）
- **开发者规模**：25万开发者
- **平台适配**：15平台适配
- **核心机制**：MCP插件沙箱压缩，将工具调用上下文压缩为紧凑表示

### 11.2 龙虾集成配置

```yaml
# context-mode MCP插件适配
context_mode:
  enabled: true
  compress_ratio: 0.98        # 98%工具调用上下文压缩
  compatible_tools:
    - read_text
    - read_file
    - write_file
    - edit_file
    - shell_executor
    - python_executor
    - search_file
    - search_chunk
  sandbox:
    isolation: strict
    max_context_size: 16384   # 压缩后最大上下文字节
  platforms:
    - windows                  # PowerShell适配
    - mcp_server               # MCP Server集成
  auto_trigger:
    tool_call_count_gt: 10     # 工具调用>10次自动启用
    session_duration_gt: 1800  # 会话>30分钟自动启用
```

### 11.3 context-mode安全规则

| 规则 | 内容 |
|------|------|
| 沙箱不可逃逸 | 压缩后的上下文在独立沙箱中操作，不得访问宿主上下文 |
| 压缩可逆验证 | 每次压缩后必须解压验证内容完整性 |
| 敏感信息不压缩 | 密钥/凭证/个人信息不参与压缩，保留原始上下文 |
| 压缩比日志 | 每次压缩记录压缩比、时间、工具数量，供性能分析 |

---

## 十二、headroom CCR压缩启用规则（R66新增）

### 12.1 headroom v0.22.4定位

headroom（2026年6月5日v0.22.4成熟，4.8K Star）是上下文压缩领域的标杆：
- **CCR（可逆压缩比率）**：47-92% Token节省
- **累计节省**：600亿+ Token
- **启动即用**：Python/Node.js双语言SDK

### 12.2 龙虾headroom集成配置

```yaml
# headroom CCR压缩启用
headroom:
  enabled: true
  version: "0.22.4"
  ccr_range:
    min: 0.47                  # 最低47% Token节省
    max: 0.92                  # 最高92% Token节省
    target: 0.75               # 目标75%节省（平衡性能与质量）
  strategies:
    - semantic_dedup           # 语义去重
    - context_pruning          # 上下文剪枝
    - token_compression        # Token级压缩
  auto_trigger:
    context_window_pct_gt: 60  # 上下文窗口占用>60%自动触发
    message_count_gt: 50       # 消息数>50自动触发
  fallback:
    on_compression_fail: split_and_retry  # 压缩失败→分片重试
    on_corruption: restore_from_checkpoint # 损坏→检查点恢复
```

### 12.3 headroom+context-mode联合策略

| 场景 | 策略 | 预期节省 |
|------|------|:---:|
| 短任务(<10工具调用) | 不启用 | 0% |
| 中等任务(10-50工具调用) | context-mode单独启用 | ~60% |
| 长任务(50+工具调用) | context-mode + headroom联合 | ~85% |
| 超长蒸馏任务 | 联合 + 分片 + Goal模式持久化 | ~92% |

---

## 十三、Agent生态更新（R62→R66）

### 13.1 四模型并行时代 + context-mode/headroom双压缩

2026年6月，AI Agent行业进入"四模型并行 + 上下文压缩双引擎"时代：
- **GPT-5.6**：150万Token窗口 + 价格锚定策略
- **Claude Fable 5**：多模态设计语言 + 安全分类器
- **Claude Mythos 5**：五层安全纵深 → **R66六层纵深（+L0进化安全）** + 推理链审计
- **DeepSeek V4.1**：原生MCP深度适配 + 多模态输入 + 企业工具链 + 企业付费榜第一
- **context-mode**：98%工具上下文压缩 + MCP沙箱隔离 + 15平台适配（R66新增）
- **headroom v0.22.4**：47-92% CCR可逆压缩 + 600亿+Token节省（R66启用）

### 13.2 龙虾AI分身应对策略（R66升级）

1. **四模型路由矩阵**：按任务场景自动选择最优模型
2. **双模型交叉验证**：安全关键场景双模型协同
3. **MCP+AMP双协议**：桌面端MCP + 移动端AMP跟踪
4. **模型反馈回路**：每次使用记录效果，持续优化路由
5. **六层安全纵深（R66升级）**：L0进化安全层前置 + Anthropic递归自进化终止条件
6. **context-mode MCP压缩（R66新增）**：长会话工具调用自动压缩，降低98%上下文消耗
7. **headroom CCR压缩（R66新增）**：上下文窗口>60%自动触发可逆压缩，目标节省75%

### 13.3 RED Skill + B站BIP + 抖音AI大赛三平台Skill运营

- RED Skill官宣上线：30万创作者+16万开发者+近千原创Skill
- B站BIP首周：60%非专业参赛+17%未成年及银发族
- 抖音AI大赛正式启动：128个名额+11位评审+开放/命题/品牌三赛道

### 13.4 Self-Skill技能体系（R64→R66 · 5项→6项）

六步蒸馏法⑤产出self-skill文件，已落盘至技能库目录。R66新增第6项"范式适应"：

| # | 技能文件 | 版本 | 核心内容 | R66更新 |
|:---:|------|:---:|------|------|
| 1 | self-skill-龙虾五步法 | v2.5_R64→v2.6_R66 | 意图识别→能力映射→方案规划→自主执行→反思进化 | 范式适应步骤集成 |
| 2 | self-skill-全域蒸馏引擎 | v2.5_R64→v2.6_R66 | 六步蒸馏法全流程 + Goal模式配置 | L0进化安全前置检查 |
| 3 | self-skill-四模型路由 | v1.2_R64→v1.3_R66 | 四模型决策树 + 场景路由矩阵 + 子Agent模型指派 | context-mode+headroom集成 |
| 4 | self-skill-Harness工程 | v1.1_R64→v1.2_R66 | 五层体系→六层体系(L0-L5) | 六层纵深安全适配 |
| 5 | self-skill-双模型验证 | v1.1_R64→v1.2_R66 | 模型配对矩阵 + 一致性评分四维度 + 分级处理 | 进化安全交叉验证 |
| **6** | **self-skill-范式适应（NEW）** | **v1.0_R66** | **范式冲击检测→解构→对标→升级→验证** | **R66新增** |

**部署规则**：每个self-skill含触发条件/执行流程/输入输出规范/安全约束/产出物清单，与核心配置版本联动升级。新增第6项覆盖"Chat is Dead"等范式剧变的体系化应对能力。

### 13.5 Claude Code v2.1.172 配置更新（R66新增）

> **来源**：Claude Code v2.1.172 更新日志（2026-06-10）。

**龙虾Agent体系对标配置变更**：

| 配置项 | R65值 | R66值 | 变更原因 |
|------|:---:|:---:|------|
| 子代理最大嵌套深度 | 1 | 5 | 对齐Claude Code v2.1.172五层嵌套 |
| 子代理默认模型 | 统一 | 按层级指派（L0最强/L4最轻） | 对齐model-per-subtask成本优化 |
| 上下文欠费策略 | 报错终止 | 自动压缩回标准限制 | 对齐Auto Compact机制 |
| 子代理活跃状态监控 | 轮询 | 事件驱动 | 对齐嵌套子代理父级挂起Bug修复 |
| 插件/工具加载 | 逐个加载 | 合并批处理 | 对齐browser tools batch loading |
| availableModels白名单 | 仅主Agent | 全层级穿透 | 对齐企业级availableModels审计修复 |

### 13.6 Dynamic Workflows 子代理池配置（R66新增）

> **来源**：Dynamic Workflows 六种模式在龙虾体系的对标（2026-06-11）。

**六大工作流模式的龙虾子代理池配置**：

| 模式 | 子代理类型 | 模型选择 | worktree隔离 | 龙虾触发条件 |
|------|------|------|:---:|------|
| Classify-and-act | 分类Agent + 路由Agent | 分类用轻模型 | 否 | 意图识别阶段自动 |
| Fanout-and-synthesize | N个并行执行Agent + 汇总Agent | 执行用标准/汇总用强模型 | 是 | 子任务≥5且独立 |
| Adversarial verification | 执行Agent + 验证Agent + 反驳Agent | 三者均用强模型 | 是 | 安全审查/代码审查 |
| Generate-and-filter | 生成Agent + 评分Agent | 生成用标准/评分用轻模型 | 否 | 候选方案筛选 |
| Tournament | N个竞争Agent + 评审Agent | 竞争者用强模型 | 是 | 四模型对决模式 |
| Loop until done | 执行Agent（循环） | 用标准模型 | 否 | /goal模式条件终止 |

**worktree隔离启用规则**（R66新增）：
- 并行任务可能修改同一文件 → 强制启用独立worktree
- 纯只读任务（搜索/抓取/阅读） → 禁用worktree节省开销
- 修改系统配置或核心角色文件 → 强制启用worktree+审查Agent

**工作流保存/复用规则**（R66新增）：
- 每次蒸馏/审查/排序任务执行后，评估是否沉淀为可复用工作流
- 保存路径：`E:\龙虾AI主控中心\我的AI分身\技能库\workflows\`
- 命名规范：`wf_{模式}_{场景}_{日期}.json`
- 复用条件：同类任务触发时，先查询已保存工作流，匹配则复用

### 13.7 self-skill同步升级（R66联动更新）

| # | 技能文件 | 版本变更 | R66更新内容 |
|:---:|------|:---:|------|
| 1 | self-skill-龙虾五步法 | v2.6→v2.7_R66 | 五层嵌套深度适配、Dynamic Workflows触发条件 |
| 2 | self-skill-全域蒸馏引擎 | v2.6→v2.7_R66 | Fanout模式自动触发规则、独立worktree启用 |
| 3 | self-skill-四模型路由 | v1.3→v1.4_R66 | Model-per-subtask成本矩阵、五层嵌套模型指派 |
| 4 | self-skill-Harness工程 | v1.2→v1.3_R66 | L0-L4五层嵌套架构、对抗式验证Agent |
| 5 | self-skill-双模型验证 | v1.2→v1.3_R66 | 三方交叉验证（执行+验证+反驳）、Tournament评审 |
| 6 | self-skill-范式适应 | v1.0→v1.1_R66 | Dynamic Workflows范式、五层嵌套范式 |

---

> **版本**：v2.24_R66（R33+R56+R62+R64+R65+R66更新）
> **知识来源**：Anthropic Advanced Subagents + Agent Teams + Harness + Managed Agents + DeepSeek V4.1 MCP适配 + Claude Fable 5安全分类器 + 蚂蚁AMP协议 + 龙虾全域模板 + 微信AI生态指引 + RED Skill公告 + B站BIP首周 + 抖音AI大赛规则 + Anthropic递归自改进安全呼吁 + context-mode MCP插件范式 + headroom v0.22.4 CCR压缩
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\角色总说明书\SOUL.md) | [USER.md](E:\龙虾AI主控中心\我的AI分身\角色总说明书\USER.md) | [角色总说明书 v2.27_R66](E:\龙虾AI主控中心\我的AI分身\角色总说明书\角色总说明书.md)
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*


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
