# Anthropic Academy 官方课程全集

> **来源**：Anthropic Academy (Skilljar)
> **采集时间**：2026-05-31
> **课程总数**：17 门（免费开放）
> **认证体系**：Claude Certified Architect, Foundations（需 Claude Partner Network 会员）

---

## 一、课程全景概览

Anthropic 于 2026 年 3 月 12 日正式推出 Claude Certified Architect 认证体系，伴随 100M 美元 Claude Partner Network 投资，Anthropic Academy 同步开放 17 门免费课程，覆盖从 AI 素养入门到 MCP 高级协议实现的完整知识体系。

---

## 二、课程分类与详情

### 2.1 AI 素养与基础（入门级·思维重构）

| # | 课程名称 | Skilljar 链接 | 时长 | 难度 | 证书 |
|---|---------|--------------|------|------|------|
| 1 | Claude 101 | [链接](https://anthropic.skilljar.com/claude-101) | ~1h | 初级 | 有 |
| 2 | AI Fluency: Framework & Foundations | [链接](https://anthropic.skilljar.com/ai-fluency-framework-and-foundations) | ~30min | 初级 | 有 |
| 3 | AI Capabilities and Limitations | [链接](https://anthropic.skilljar.com/ai-capabilities-and-limitations) | ~1h | 初级 | 有 |
| 4 | AI Fluency for Students | [链接](https://anthropic.skilljar.com/ai-fluency-for-students) | ~2h | 初级 | 有 |
| 5 | AI Fluency for Educators | [链接](https://anthropic.skilljar.com/ai-fluency-for-educators) | ~2h | 初级 | 有 |
| 6 | AI Fluency for Nonprofits | [链接](https://anthropic.skilljar.com/ai-fluency-for-nonprofits) | ~2h | 初级 | 有 |
| 7 | Teaching AI Fluency | [链接](https://anthropic.skilljar.com/teaching-ai-fluency) | ~1h | 初级 | 有 |

**核心框架：4D 框架**
- **Delegation（委托）**：将任务委派给 AI
- **Description（描述）**：清晰描述需求
- **Discernment（辨识）**：辨别 AI 输出质量
- **Diligence（勤勉）**：持续优化协作

---

### 2.2 开发者进阶（核心硬核区）

| # | 课程名称 | Skilljar 链接 | 时长 | 难度 | 证书 |
|---|---------|--------------|------|------|------|
| 8 | Claude Code 101 | [链接](https://anthropic.skilljar.com/claude-code-101) | ~1.5h | 中级 | 有 |
| 9 | Claude Code in Action | [链接](https://anthropic.skilljar.com/claude-code-in-action) | ~2h | 中级 | 有 |
| 10 | Building with the Claude API | [链接](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | ~3h | 高级 | 有 |
| 11 | Introduction to Model Context Protocol | [链接](https://anthropic.skilljar.com/introduction-to-mcp) | ~2h | 中级 | 有 |
| 12 | Model Context Protocol: Advanced Topics | [链接](https://anthropic.skilljar.com/mcp-advanced) | ~2h | 高级 | 有 |
| 13 | Introduction to Agent Skills | [链接](https://anthropic.skilljar.com/introduction-to-agent-skills) | ~2h | 中级 | 有 |
| 14 | Introduction to Subagents | [链接](https://anthropic.skilljar.com/introduction-to-subagents) | ~2h | 中级-高级 | 有 |

---

### 2.3 云平台部署（生态扩展区）

| # | 课程名称 | Skilljar 链接 | 时长 | 难度 | 证书 |
|---|---------|--------------|------|------|------|
| 15 | Claude with Amazon Bedrock | [链接](https://anthropic.skilljar.com/claude-with-amazon-bedrock) | ~2h | 高级 | 有 |
| 16 | Claude with Google Cloud's Vertex AI | [链接](https://anthropic.skilljar.com/claude-with-vertex-ai) | ~2h | 高级 | 有 |

---

### 2.4 团队与组织（协作扩展区）

| # | 课程名称 | Skilljar 链接 | 时长 | 难度 | 证书 |
|---|---------|--------------|------|------|------|
| 17 | Introduction to Claude Cowork | [链接](https://anthropic.skilljar.com/introduction-to-claude-cowork) | ~2h | 初级-中级 | 有 |

---

## 三、Claude Certified Architect 认证

### 3.1 考试概览

- **名称**：Claude Certified Architect, Foundations
- **形式**：60 题监考评估
- **五大知识域**：
  1. Agentic Architecture & Claude Code（最高权重）
  2. Context Management（上下文管理）
  3. API Design Patterns（API 设计模式）
  4. Security & Governance（安全与治理）
  5. Integration Architecture（集成架构）
- **准入条件**：Claude Partner Network 会员
- **2026 后续计划**：Seller 认证 / Developer 认证 / Advanced Architect 认证

### 3.2 备考路径

1. 完成 17 门 Skilljar 课程（免费）
2. 重点学习 Agent Skills + Subagents + MCP 系列
3. 通过 Partner Network 注册考试

---

## 四、核心技能提炼

### 4.1 子代理（Subagents）最佳实践

| 维度 | 最佳实践 |
|------|---------|
| 上下文隔离 | 每个 Subagent 拥有独立上下文窗口，避免污染主对话 |
| 任务委派 | 将复杂任务拆解为子任务，分配给专业化 Subagent |
| Skills 协同 | Subagent 可携带 Skills（Markdown 指令集），按需加载 |
| 工作流构建 | 串联多个 Subagent 形成自动化 Pipeline |
| 错误处理 | Subagent 失败时需优雅降级，主 Agent 接管兜底 |

### 4.2 多 Agent 协作（Multi-Agent）设计原则

| 原则 | 说明 |
|------|------|
| 职责单一 | 每个 Agent 只负责一类任务（File / System / App / Browser / Search） |
| 上下文隔离 | Agent 间不共享上下文，通过结构化输入/输出通信 |
| 调度中心 | 主 Agent 作为调度器（Orchestrator），决策路由 |
| 结果聚合 | 多 Agent 结果由主 Agent 统一加工呈现 |
| 降级策略 | 任一 Agent 失败不影响其他 Agent 执行 |

### 4.3 Claude Code 核心能力

| 能力 | 描述 |
|------|------|
| 代码生成 | 基于自然语言描述生成完整代码 |
| 代码修改 | 精确字符串替换编辑（diff-based） |
| 项目管理 | 理解项目结构、依赖关系 |
| 测试生成 | 自动生成单元测试和集成测试 |
| 文档编写 | 生成 API 文档、README、架构说明 |
| Shell 集成 | 执行命令、安装依赖、管理环境 |

### 4.4 MCP（Model Context Protocol）核心架构

```
┌──────────────┐     MCP Protocol     ┌──────────────────┐
│  MCP Client  │ ◄──────────────────► │   MCP Server     │
│  (Claude)    │   Tools/Resources/    │  (External Sys)  │
│              │       Prompts         │                  │
└──────────────┘                       └──────────────────┘
```

**三大核心原语**：
- **Tools**：Claude 可调用的外部函数
- **Resources**：Claude 可读取的外部数据源
- **Prompts**：预定义的提示词模板

**高级特性**：
- Sampling（采样）
- Notifications（通知）
- File System Access（文件系统访问）
- Transport Mechanisms（传输机制）

---

## 五、学习路径建议

### 开发者路径
```
Claude 101 → Claude Code 101 → Agent Skills → Subagents 
→ Claude API → MCP Intro → MCP Advanced → Claude Code in Action
```

### 架构师路径
```
全部课程 → 重点 MCP 系列 + Subagents + API 
→ Claude Certified Architect 备考 → 考试
```

### 产品/管理路径
```
Claude 101 → AI Fluency → AI Capabilities → Claude Cowork
```

---

## 六、与龙虾 AI 体系的映射

| Anthropic 概念 | 龙虾 AI 对应 |
|---------------|-------------|
| Subagents | 子 Agent（File/Computer/App/Browser/Search） |
| Agent Skills | 技能库（12 项官方技能） |
| Orchestrator | 主 Agent 调度 |
| MCP | 工具调用协议 |
| Skills (Markdown) | Skill Prompt（use_skill） |
| Context Window | 会话上下文 |
| Cowork | DesktopController |

---

## 七、关键洞察

1. **范式转移**：从"提示词工程"到"Agent 协作工程"
2. **Skills 即配置**：Markdown 格式的技能指令 = Agent 的可插拔能力模块
3. **Subagents = 专业化分工**：每个子代理专注单一领域，组合产生涌现能力
4. **MCP = 标准化接口**：解决 AI Agent 的"信息孤岛"问题
5. **认证生态**：Anthropic 正在构建与 AWS/Azure 认证相当的 AI 实施资质体系
6. **Cowork = 非开发者入口**：桌面自动化产品，降低 AI Agent 使用门槛

---

> **文档版本**：v1.0 | **下次更新**：待课程内容更新后自动同步