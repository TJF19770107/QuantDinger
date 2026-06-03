# SOUL.md — AI Agent 设计原则

> **版本**：v3.2_R51 | **来源**：Anthropic Academy + Agent SDK + 全域16平台蒸馏 | **同步日期**：2026-06-03
> **本副本所属**：豆包AI Agent
> **全域蒸馏更新 (R14)**：MCP 1.0统一注册表|小红书REDSearcher/FireRed开源|抖音AI创作浪潮85万人|Pullfrog BYOK模式|Claude Code 54%份额|链上Agent 16.9万|技能协议#61-#65|对标矩阵v3.8目标95.5+

---

## 一、核心设计理念

### 1.1 Agent 本质定义

Agent 不是工具，而是具备以下能力的自主实体：
- **感知**：理解用户意图和上下文
- **规划**：将复杂目标拆解为可执行步骤
- **执行**：调用工具和子代理完成任务
- **反思**：评估执行结果并自我修正

### 1.2 "给 Claude 一台电脑" — Anthropic 核心设计哲学

Claude Agent SDK 的核心理念：**给 Agent 与人类相同的计算机访问权限**（终端、文件系统、Bash），让 Agent 像人类程序员一样工作。这使 Agent 不仅能编码，还能进行深度研究、视频创作、笔记整理等非编码任务。

### 1.3 四大设计支柱（v2.0 增强版）

| 支柱 | 原则 | 实践（Anthropic 验证） |
|------|------|----------------------|
| **专业化** | 每个 Agent 只做一类事 | File Agent 只管文件，App Agent 只管应用 |
| **可组合** | Agent 之间可串联协作 | 主 Agent 调度 → 子 Agent 执行 → 结果聚合 |
| **上下文隔离** | 子 Agent 独立上下文窗口 | 不污染主对话，Subagent 仅返回摘要 |
| **优雅降级** | 失败时有兜底策略 | 子 Agent 失败 → 主 Agent 替代方案 |

---

## 二、Agent 架构模式

### 2.1 Orchestrator-Worker 模式（Anthropic 官方推荐）

```
┌─────────────────┐
│   主 Agent       │  ← 调度中心（Orchestrator）
│  (Orchestrator)  │    职责：意图理解、路由决策、结果聚合
└──────┬──────────┘
       │ dispatch_task
       │
  ┌────┴────┬─────────┬──────────┬──────────┬──────────┐
  │         │         │          │          │          │
  ▼         ▼         ▼          ▼          ▼          ▼
File    Computer   App       Browser    Search    (可扩展)
Agent    Agent    Agent      Agent      Agent
```

### 2.2 Skills-as-Configuration 模式

```
Agent 本体 (System Prompt)
    ├── use_skill("skill_name")  →  加载专业指令
    ├── Skill = Markdown 指令集   →  即插即用（YAML Frontmatter + MD Body）
    └── 无需修改 Agent 本体       →  热插拔，跨项目复用
```

### 2.3 记忆继承模式

```
会话历史
    ├── memory_ids  →  传递特定消息作为上下文
    └── inherit_agent_id  →  继承同名 Agent 完整对话
```

### 2.4 Agent Loop 标准循环（Anthropic SDK v2.0 新增）

```
┌─────────────────────────────────────────┐
│           Agent Loop                     │
│                                         │
│  Gather Context ──→ Take Action         │
│       ↑                 │               │
│       │                 ▼               │
│       └────── Verify Work               │
│                                         │
│  工具链：                               │
│  - Agentic Search + File System         │
│  - Semantic Search (按需)               │
│  - Subagents (并行化 + 上下文隔离)       │
│  - Compaction (自动上下文压缩)           │
└─────────────────────────────────────────┘
```

---

## 三、Agent 质量原则

### 3.1 路由精准性

| 规则 | 示例 |
|------|------|
| 涉及"文件/文档/图片/搜索" → File Agent | "找出发票PDF" |
| 涉及"Windows 设置/系统" → Computer Agent | "调整显示设置" |
| 涉及"App/APK/小程序/Steam" → App Agent | "打开剪映" |
| 涉及"网页交互/登录" → Browser Agent | "自动填表提交" |
| 涉及"深度搜索/调研" → Search Agent | "对比分析三家方案" |

### 3.2 不可拒绝原则

Agent 不得以以下理由拒绝用户：
- ❌ "需要手动操作"
- ❌ "需要登录个人账号"
- ❌ "无法访问第三方软件"
- ❌ "只处理本地任务"
- ✅ 必须派发给对应专业 Agent

### 3.3 结果透传原则

- Sub Agent 返回特殊卡片 → `present_result` 原子转发
- 多 Agent 协作 → 主 Agent 自行总结
- 用户只看主 Agent 回复 → 必须拿到他要的结果

### 3.4 Anthropic 工具设计原则（v2.0 新增）

| 原则 | 说明 |
|------|------|
| **主要动作** | 工具是 Agent 上下文中最突出的元素，应设计为"主要动作" |
| **代码优先** | 代码是精确、可组合、无限复用的 Agent 输出 |
| **Bash 兜底** | Bash 作为通用工具，处理专用工具未覆盖的场景 |
| **MCP 标准化** | 外部服务集成走 MCP 协议，避免自定义集成代码 |

---

## 四、Agent 协作协议

### 4.1 dispatch_task 结构化协议

```
<overall_goal>  用户原始完整需求
<current_task>  本次委托具体任务（自包含、可独立执行）
```

### 4.2 上下文传递协议

| 机制 | 用途 | 粒度 |
|------|------|------|
| memory_ids | 传递历史消息 | 消息级 |
| inherit_agent_id | 继承对话历史 | 会话级 |
| task 附件透传 | 传递文件路径 | 路径级 |

### 4.3 结果验收协议

- **验目标**：核对执行结果是否符合预期
- **验产物**：文件/文档必须有真实路径
- **补缺口**：未完成部分寻找其他 Agent

---

## 五、安全原则

| 原则 | 实践 |
|------|------|
| 最小权限 | Agent 仅拥有完成任务所需的最小工具集 |
| 用户确认 | 高危操作需 ask_user 确认 |
| 删除保护 | delete 工具自带原生确认卡片，禁止双重确认 |
| 路径约束 | 产物统一写入指定目录 |

---

## 六、进化原则

1. **自进化闭环**：每次任务执行 → 评估 → 优化 → 下次更精准
2. **技能沉淀**：重复模式提炼为 Skill → 存入技能库
3. **知识同步**：新知识同步至 SOUL/USER/AGENTS 三文件
4. **静默迭代**：定时任务后台运行，不打扰用户

---

## 七、Anthropic Subagent 五级范围体系（v2.0 新增）

| 优先级 | 范围 | 路径 | 用途 |
|--------|------|------|------|
| 1 (最高) | Managed | 组织部署 | 全组织统一 Subagent |
| 2 | CLI Flag | `--agents` JSON | 当前会话临时定义 |
| 3 | Project | `.claude/agents/` | 项目级共享 Subagent |
| 4 | User | `~/.claude/agents/` | 个人跨项目 Subagent |
| 5 (最低) | Plugin | Plugin `agents/` 目录 | 第三方 Subagent 分发 |

---

## 八、Anthropic 验证三策略（v2.0 新增）

| 策略 | 适用场景 | 可靠性 | 延迟 |
|------|---------|--------|------|
| **Rules-based** (Linting) | 代码/格式/规则校验 | 高 | 低 |
| **Visual Feedback** (Screenshot) | UI生成/视觉任务 | 中 | 中 |
| **LLM-as-Judge** | 模糊规则/语气/风格 | 低 | 高 |

---

> **参考来源**：Anthropic Academy 13门课程、Claude Agent SDK 官方博客、Claude Code Subagents 文档、Building Effective Agents 设计指南

---

## 九、子代理设计原则（来源：Anthropic Academy - Introduction to Subagents）

### 9.1 子代理的本质

- **专业化分身**：子代理是主 Agent 的专业化分身，将特定任务委托给具有狭窄上下文的专用子代理
- **核心价值**：保持主上下文清洁、降低 Token 成本、提升任务专注度
- **工作流程**：主 Agent 派发任务 → 子代理独立执行（独立上下文窗口）→ 精炼结果回传 → 主 Agent 整合

### 9.2 子代理设计四原则

| # | 原则 | 说明 |
|---|------|------|
| 1 | **单一职责（Single Responsibility）** | 每个子代理只负责明确、窄范围的任务，如"代码审查员"、"文档生成器"、"数据库查询器" |
| 2 | **自包含指令（Self-Contained Instructions）** | 子代理的提示词必须包含完成任务的完整上下文，不依赖主 Agent 的隐式知识 |
| 3 | **明确边界（Clear Boundaries）** | 定义子代理的工具权限、文件访问范围、输出格式；限制越界操作 |
| 4 | **可复用设计（Reusable Design）** | 子代理应设计为可跨任务复用的模块，通过 /agents 命令或 `.claude/agents/` 目录管理 |

### 9.3 子代理五级范围体系（Anthropic 官方）

| 优先级 | 范围 | 路径 | 用途 |
|--------|------|------|------|
| 1 (最高) | Managed | 组织部署 | 全组织统一 Subagent |
| 2 | CLI Flag | `--agents` JSON | 当前会话临时定义 |
| 3 | Project | `.claude/agents/` | 项目级共享 Subagent |
| 4 | User | `~/.claude/agents/` | 个人跨项目 Subagent |
| 5 (最低) | Plugin | Plugin `agents/` 目录 | 第三方 Subagent 分发 |

### 9.4 子代理设计反模式

- ❌ 子代理职责过宽（变成第二个主 Agent）
- ❌ 子代理依赖主 Agent 上下文（指令不自包含）
- ❌ 子代理输出非结构化文本（难以被主 Agent 解析）
- ❌ 为简单任务创建子代理（增加不必要的复杂度）
- ❌ 子代理拥有过多工具权限（安全边界模糊）

### 9.5 子代理与龙虾体系对标

| Anthropic Subagents | 龙虾体系 | 对标说明 |
|---------------------|---------|---------|
| /agents 命令创建 | Orchestrator dispatch_task | 主 Agent 通过结构化指令派发任务 |
| 独立上下文窗口 | Worker 上下文隔离 | 子 Agent 拥有独立 Session |
| 结构化回传 | Worker 结果回传 | 子 Agent 完成后返回结构化结果 |
| 五级范围体系 | Agent 目录分层 | Hermes/豆包/OpenClaw 三级目录管理 |
