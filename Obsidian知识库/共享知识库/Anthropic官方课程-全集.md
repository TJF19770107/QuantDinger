# Anthropic 官方课程全集

> 版本：v1.0 | 采集日期：2026-05-31
> 来源：Anthropic Academy (Skilljar) + DeepLearning.AI 合作课程
> 课程总数：20门（Skilljar 17门 + DeepLearning.AI 3门）
> 认证体系：Claude Certified Architect, Foundations
> 学习平台：https://anthropic.skilljar.com/

---

## 一、课程总览

### 1.1 课程分类矩阵

| # | 课程名称 | 平台 | 难度 | 时长 | 证书 | CCA关联 |
|---|---------|------|------|------|------|---------|
| 1 | Claude 101 | Skilljar | 初级 | ~45min | ✅ | 入门 |
| 2 | AI Capabilities and Limitations | Skilljar | 初级 | ~30min | ✅ | — |
| 3 | AI Fluency: Framework & Foundations | Skilljar | 初级 | ~30min | ✅ | — |
| 4 | AI Fluency for Students | Skilljar | 初级 | ~2h | ✅ | — |
| 5 | AI Fluency for Educators | Skilljar | 初级 | ~1h | ✅ | — |
| 6 | AI Fluency for Nonprofits | Skilljar | 初级 | ~1h | ✅ | — |
| 7 | Teaching AI Fluency | Skilljar | 初级 | ~1h | ✅ | — |
| 8 | Claude Code 101 | Skilljar | 中级 | ~2h | ✅ | Domain 3 |
| 9 | Claude Code in Action | Skilljar | 中级 | ~2h | ✅ | Domain 3 |
| 10 | Building with the Claude API | Skilljar | 中级 | ~2h | ✅ | Domain 1 |
| 11 | Introduction to Agent Skills | Skilljar | 中级 | ~1.5h | ✅ | Domain 4 |
| 12 | Introduction to Subagents | Skilljar | 中-高 | ~2h | ✅ | Domain 4 |
| 13 | Introduction to MCP | Skilljar | 中级 | ~2.5h | ✅ | Domain 2 |
| 14 | MCP: Advanced Topics | Skilljar | 高级 | ~2h | ✅ | Domain 2 |
| 15 | Introduction to Claude Cowork | Skilljar | 中级 | ~1.5h | ✅ | Domain 5 |
| 16 | Claude with Amazon Bedrock | Skilljar | 中级 | ~3h | ✅ | Domain 4 |
| 17 | Claude with Google Cloud Vertex AI | Skilljar | 中级 | ~3h | ✅ | Domain 4 |
| 18 | Agent Skills with Anthropic | DeepLearning.AI | 中级 | — | ✅ | Domain 4 |
| 19 | Claude Code: A Highly Agentic Coding Assistant | DeepLearning.AI | 中级 | — | ✅ | Domain 3 |
| 20 | Building Towards Computer Use | DeepLearning.AI | 高级 | — | ✅ | Domain 4 |

### 1.2 CCA 五大考试域

| 域 | 考试占比 | 核心课程 |
|---|---------|---------|
| Domain 1: API & Prompt Engineering | 中 | Claude API、Prompt Caching |
| Domain 2: MCP & Integration | 中 | MCP入门+高级 |
| Domain 3: Claude Code | 中 | Claude Code 101 + in Action |
| Domain 4: Agentic Architecture | 最高 | Agent Skills、Subagents、Computer Use |
| Domain 5: Safety & Governance | 中 | Claude Cowork、Enterprise |

---

## 二、核心课程深度解析

### 2.1 子代理（Subagents）—— 多Agent协作基石

**课程**：Introduction to Subagents
**时长**：约2小时 | **难度**：中级-高级 | **证书**：✅

**核心要点**：
- 子代理是把整体任务拆成能独立运行的小单元，适用于并行处理与上下文窗口受限的场景
- 主代理负责统筹与复杂逻辑，子代理适合短时、明确输入输出的工作
- 拆分好任务能显著降低主代理的上下文占用，提高稳定性
- 设计子代理规格（spec）时需明确：输入输出格式、字数/风格限制、错误返回结构、超时策略

**子代理 Spec 模板**：
```
输入字段：项目名、目标平台、字数上限
输出要求：JSON格式含 title、intro、install_steps
失败返回：{"error":"描述"}
超时：30s，最多重试3次
```

**实战步骤（20分钟速成）**：
1. 注册Skilljar并打开课程（2分钟）
2. 观看4个短视频并记录spec模板（15分钟）
3. 定义任务拆分（每个子代理负责单一维度）
4. 并行启动子代理，设置超时与重试阈值
5. 主代理收集结果，统一格式并解决冲突，一致性校验

**常见问题**：
- 空响应 → 增加重试并检查输入格式
- 输出格式错位 → spec强制JSON模式+示例
- 并行结果冲突 → 主代理以优先级规则/合并模板调和

---

### 2.2 Claude Agent 三级架构

**来源**：Anthropic 官方教程"7步构建Claude Agent战队"

| 层级 | 名称 | 能力 | 通信 | 适用场景 | 比喻 |
|------|------|------|------|---------|------|
| Level 1 | Subagents | 当前session运行，汇报结果 | 彼此不可通信 | 可重复任务（审查/测试/文档） | 承包商 |
| Level 2 | Agent View | 全屏dashboard，派发/窥探/接入 | 独立session | 3-10个独立任务 | 任务看板 |
| Level 3 | Agent Teams | 主导Agent协调，成员通信 | 共享任务列表 | 跨文件相互依赖任务 | 工程团队 |

**Level 3 启用方式**：
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**模型路由优化**：
- 主导Agent：复杂工作用Opus
- 团队成员：自动使用Sonnet（成本仅1/5）

**决策框架**：
- 单次prompt/单文件修复 → 常规Claude Code session
- 3个独立任务无依赖 → Agent View
- 可重复工作流 → Subagents + YAML配置
- 多文件依赖功能 → Agent Teams
- 通宵清理积压 → Headless模式 + --max-budget-usd

**防护栏（Guardrails）**：
- 每个Agent预算$3，团队上限$15
- settings.json安全约束
- 并行运行时多维度风险管控

---

### 2.3 Agent Skills —— 可复用能力封装

**课程**：Introduction to Agent Skills
**时长**：约1.5小时 | **难度**：中级

**核心要点**：
- Agent Skills 是Agent的"能力集"，将特定任务逻辑封装成可复用的技能
- 让Claude不再是简单的对话模型，而是能执行特定操作的"数字员工"
- 通过Markdown指令构建Skills，Claude跨任务上下文应用
- 这是从"提示词工程"到"Agent协作工程"的关键一步

**Skill构建范式**：
```markdown
# Skill名: 代码审查专家
## 触发条件: 当用户请求代码审查时
## 输入: 代码文件路径或代码片段
## 输出: 结构化审查报告
## 规则:
1. 检查安全漏洞
2. 评估代码质量
3. 提供优化建议
4. 格式: JSON
```

---

### 2.4 MCP (Model Context Protocol) —— Agent神经系统

**课程**：Introduction to MCP + MCP Advanced Topics
**总时长**：约4.5小时 | **难度**：中级→高级

**MCP 入门核心**：
- 三原语：Tools（工具）、Resources（资源）、Prompts（提示词）
- Python从零构建MCP服务器和客户端
- JSON-RPC协议通信
- 解决AI"信息孤岛"问题，标准化Agent间上下文共享

**MCP 高级主题**：
- Sampling（采样）、Notifications（通知）
- 文件系统访问
- 传输机制（Transport）
- 生产环境部署优化

**与龙虾AI体系对照**：
- MCP ≈ 龙虾双向桥接协议 + MCP桥接集成协议v1.0
- Agent间通信标准化 → 龙虾Swarm多Agent拓扑调度协议v1.0

---

### 2.5 Claude API 构建

**课程**：Building with the Claude API
**时长**：约2小时 | **难度**：中级

**核心覆盖**：
- 函数调用（Function Calling）
- 工具使用（Tool Use）
- 流式传输（Streaming）
- SDK使用
- 生产模式部署

API是Agent的"手脚"，使Claude与外部系统交互，是构建Agentic应用的基石。

---

### 2.6 Claude Cowork —— 桌面Agent工作区

**课程**：Introduction to Claude Cowork
**时长**：约1.5小时 | **难度**：中级

**核心覆盖**：
- Cowork任务循环
- 插件系统
- 文件工作流
- 多步骤工作负责任引导
- 面向非开发者的桌面自动化

对标龙虾：桌面Agent工作区隔离协议v1.0 + 感知行动语义桌面协议v1.0

---

### 2.7 AI Fluency 4D框架

**课程**：AI Fluency: Framework & Foundations
**时长**：约30分钟 | **难度**：初级

**4D框架**：
| D | 英文 | 中文 | 含义 |
|---|------|------|------|
| D1 | Delegation | 委托 | 识别可委托给AI的任务 |
| D2 | Description | 描述 | 清晰描述任务要求和预期输出 |
| D3 | Discernment | 辨别 | 批判性评估AI输出质量 |
| D4 | Diligence | 勤勉 | 持续迭代优化协作流程 |

---

## 三、学习路径建议

### 3.1 开发者路径（Agent架构师）

```
Step 1: Claude 101 → AI Capabilities
Step 2: Building with the Claude API
Step 3: Introduction to MCP → MCP Advanced
Step 4: Claude Code 101 → Claude Code in Action
Step 5: Introduction to Agent Skills → Introduction to Subagents
Step 6: Claude Cowork
Step 7: CCA认证考试
```

### 3.2 多Agent系统专家路径

```
Step 1: Agent Skills → Subagents
Step 2: Agent View → Agent Teams (Level 1→2→3)
Step 3: MCP 入门+高级
Step 4: Agent Skills with Anthropic (DeepLearning.AI)
Step 5: Building Towards Computer Use
Step 6: 实战Agent Teams项目
```

### 3.3 非技术用户路径

```
Step 1: AI Fluency: Framework & Foundations
Step 2: AI Capabilities and Limitations
Step 3: Claude 101
Step 4: Introduction to Claude Cowork
Step 5: 按角色选择垂直课程（教育/学生/非营利）
```

---

## 四、认证体系

### 4.1 Claude Certified Architect, Foundations

- **考试形式**：60题监考评估，5大领域
- **核心权重**：Agentic Architecture + Claude Code（最高权重）
- **目标人群**：方案架构师/高级工程师
- **准入条件**：需加入Claude Partner Network（免费）
- **前5000名员工可获优先访问**

### 4.2 2026下半年扩展计划

| 认证层级 | 目标人群 | 预计时间 |
|---------|---------|---------|
| Seller认证 | 销售工程师/AE/方案顾问 | 2026 H2 |
| Developer认证 | 实施工程师 | 2026 H2 |
| Advanced Architect | 复杂系统设计师 | 2026 H2 |

---

## 五、与龙虾AI体系融合映射

| Anthropic课程 | 龙虾对标协议 | 融合价值 |
|-------------|------------|---------|
| Introduction to Subagents | 协议25 Lead-Specialist多Agent推理分发 | 子代理分发与并行推理 |
| Agent Teams (Level 3) | 协议42 Swarm多Agent拓扑调度 | DAG拓扑+模型分层 |
| Agent Skills | 协议38 技能全生命周期自治管理 | 技能创建→评估→精炼→废弃 |
| MCP | 协议17 MCP桥接集成协议 | 标准化跨Agent通信 |
| Claude Cowork | 协议23 桌面Agent工作区隔离 + 协议45 语义桌面 | 桌面操控+审计 |
| Claude Code | 协议35 Spec驱动编码 + 协议14 多Agent并行隔离开发 | 规约生成+隔离开发 |
| AI Fluency 4D | 协议37 Dreaming跨会话元学习 | 模式提取+原则蒸馏 |
| Claude API + Tool Use | 协议20 工具容错与降级协议 | 备用链+并行引擎 |
| CCA Domain 5 (Safety) | 协议30 异步监察者安全协议 | 异常检测+分级干预 |
| Agent View | 协议40 有状态心跳自主调度 | 心跳唤醒+上下文保留 |

---

## 六、关键洞察

### 6.1 范式转移：从提示词工程到Agent协作工程

Anthropic课程传递的核心信号：AI学习已从"如何写更好的Prompt"转向"如何构建和管理自主完成任务的AI Agent"。重点已转移到：Agent设计原则、技能构建、工具集成、多Agent协作模式。

### 6.2 三层Agent能力递进

Subagents（可重复任务）→ Agent View（独立并发）→ Agent Teams（协作依赖），每一层对应不同的复杂度和协作需求。大多数人停在Level 1，真正的价值在Level 3。

### 6.3 MCP作为Agent基础设施

MCP正在成为AI Agent间的标准通信协议，相当于Agent世界的HTTP。理解并掌握MCP，是构建多Agent系统的前提。

### 6.4 Cowork的桌面自动化价值

Claude Cowork面向非开发者的桌面自动化，与龙虾的桌面控制能力高度契合，可互为补充。

---

> 最后更新：2026-05-31
> 数据来源：Anthropic Academy、Curaate、ZDNET、ClaudeImplementation.com、博客园、搜狐、网易
> 龙虾全域模板版本：v3.4 Final
