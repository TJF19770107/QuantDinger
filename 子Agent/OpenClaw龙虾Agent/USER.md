---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_e26f32d16a3711f1a99c5254007bceed
    ReservedCode1: mM+9U1yKv1N5ZBGvRaQxk28/UM8YUDVuMUs1iEnjtmL5Q5wXclUulIIjM0u6eB8DpZFW1pmoYed7BWA1LIHEyLtWwzTwYWM3wys399G4A7JTE2qU2nGwRoX4LEGnmQIB6QXTRMFb8BKEXUXqAp4Rp6q+owaKC+CQS9N0hcOEQ6jqo50ZtkxFO2aeJwA=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_e26f32d16a3711f1a99c5254007bceed
    ReservedCode2: mM+9U1yKv1N5ZBGvRaQxk28/UM8YUDVuMUs1iEnjtmL5Q5wXclUulIIjM0u6eB8DpZFW1pmoYed7BWA1LIHEyLtWwzTwYWM3wys399G4A7JTE2qU2nGwRoX4LEGnmQIB6QXTRMFb8BKEXUXqAp4Rp6q+owaKC+CQS9N0hcOEQ6jqo50ZtkxFO2aeJwA=
---

# USER.md — 多Agent协作流程

> 基于 Anthropic 官方课程（Subagents + Agent Skills）提炼 | 版本 v1.0 | 2026-06-14

---

## 一、多Agent协作总览

### 1.1 协作架构

```
用户需求
    │
    ▼
┌─────────────────────┐
│   Main Agent（指挥官） │
│   解析意图 + 任务拆解   │
│   选择匹配的 Skills    │
│   委派给 Subagents    │
│   合并结果 + 验证     │
└──────┬───┬───┬──────┘
       │   │   │
   ┌───┘   │   └───┐
   ▼       ▼       ▼
Subagent  Subagent  Subagent
(A)       (B)       (C)
独立上下  独立上下  独立上下
文+权限   文+权限   文+权限
   │       │       │
   └───────┼───────┘
           ▼
    结构化结果返回
```

### 1.2 协作三阶段

| 阶段 | 动作 | 工具/机制 |
|------|------|----------|
| 解析 | Main Agent 理解意图、拆解为子任务 | CLAUDE.md + 上下文分析 |
| 委派 | 匹配 Skills、创建 Subagents、分发任务 | SKILL.md匹配 + Subagent机制 |
| 合并 | 收集子任务结果、验证完整性、输出 | Execute and Judge Loop |

---

## 二、任务拆解规则

### 2.1 拆解判断矩阵

| 条件 | 是否拆解 | 委派方式 |
|------|---------|---------|
| 子任务间无数据依赖 | ✅ 拆解 | 并行派发（Parallel Dispatch） |
| 子任务间有数据依赖 | — | 顺序派发（Sequential） |
| 单一Agent可闭环 | ❌ 不拆解 | 直接执行 |
| 需要不同工具权限集 | ✅ 拆解 | 不同Subagent |
| 需要不同模型能力 | ✅ 拆解 | 不同模型选择（Haiku/Sonnet/Opus） |
| 跨领域（文件+网页+应用） | ✅ 拆解 | 分领域Subagent |

### 2.2 并行调度策略

- **零依赖检测**：使用零样本思维链推理确认子任务确实不依赖彼此输出
- **并发上限**：单轮并行不超过5个Subagent
- **模型选择**：简单任务→Haiku（快速低延迟）、中等任务→Sonnet（均衡）、深度任务→Opus（深度推理）

---

## 三、Subagent 管理协议

### 3.1 内置 Subagent 使用规则

| Subagent | 触发条件 | 用途 | 行为限制 |
|----------|---------|------|---------|
| **Explore** | 需要搜索代码库、发现文件、探索代码结构 | 只读搜索分析 | 不可修改文件、使用Haiku模型 |
| **Plan** | 处于计划模式、需要研究代码库 | 只读研究 | 继承自主对话、不可修改文件 |
| **General-purpose** | 复杂研究、多步骤操作、代码修改 | 全能操作 | 继承全部工具权限 |

### 3.2 自定义 Subagent 创建规范

```
基础配置：
  - 名称：简洁描述职责（如 code-reviewer、doc-writer）
  - 描述：用于Main Agent自动匹配的判断依据
  - 系统提示：定义行为边界和专业领域

权限配置（最小权限原则）：
  - 只读代理：allowTools = [read_text, web_search, web_fetch]
  - 文件代理：allowTools = [read_text, write_file, edit_file, delete]
  - 系统代理：allowTools = [shell_executor, python_executor]

模型选择：
  - 快速任务 → Haiku
  - 均衡任务 → Sonnet  
  - 深度任务 → Opus

Skills注入：
  - 通过 frontmatter 的 skills: 字段绑定
  - 每个Subagent可注入多个Skills
```

---

## 四、Skills 协作协议

### 4.1 Skill 自动触发匹配

```
用户输入 → Main Agent 解析
              │
              ├── 匹配 Skill A (description 命中) → 注入知识
              │         │
              │         └── context: fork → 自动创建 Subagent
              │
              ├── 匹配 Skill B (description 命中) → 注入知识
              │         │
              │         └── 无 fork → 在当前上下文执行
              │
              └── 无匹配 → Main Agent 自行处理
```

### 4.2 Skill 优先级规则

- **项目级 Skills**（`.claude/skills/`）> **用户级 Skills**（`~/.claude/skills/`）> **全局 Skills**
- 多个匹配时，Claude 按 description 相似度排序选择最相关的一个
- `user-invocable: false` 的 Skills 仅自动触发，不会出现在 `/skills` 列表中

---

## 五、验证与质量控制

### 5.1 Execute and Judge Loop

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Subagent     │────▶│ 验证Agent     │────▶│ 通过 → 返回  │
│ 执行任务      │     │ 检查输出质量   │     │ 未通过 → 重试 │
└─────────────┘     └──────────────┘     └─────────────┘
```

### 5.2 质量检查维度
- 完整性：是否覆盖所有子任务
- 一致性：格式、命名、风格是否统一
- 准确性：关键数据和结论是否正确
- 安全性：是否触犯任何安全边界

---

## 六、故障处理流程

| 故障类型 | 处理策略 | 降级方案 |
|---------|---------|---------|
| Subagent 超时 | 切换更轻量模型重试 | Main Agent 自行处理 |
| Skill 匹配失败 | 检查 description 措辞 | 用户手动调用 |
| 上下文溢出 | 使用 Explore 子代理分段处理 | 分页读取 |
| 权限不足 | 检查 allowed-tools 配置 | 升级权限后重新委派 |
| 结果冲突 | 多个 Subagent 结果不一致时 | Main Agent 判定/请求用户裁决 |

---

*由 Marvis 基于 Anthropic 官方课程整理 | 2026-06-14 23:58 CST*

---

## 多Agent协调五大模式（Anthropic 2026年4月官方指南）

核心原则：按"需要什么上下文"分解任务，而非按"做什么类型的工作"。

| 模式 | 架构 | 适用场景 | 通信方式 |
|------|------|---------|---------|
| Sequential Pipeline | A→B→C链式 | 翻译→润色→排版 | 数据传递 |
| Parallel Fan-out | 中央→多Worker | 同时分析多文档 | 独立上下文 |
| Orchestrator-Worker | 主Agent调度子Agent | 复杂代码审查 | 结构化任务 |
| Agent Debate | 多Agent辩论收敛 | 高风险决策 | 对抗验证 |
| Swarm Autonomy | 自组织无中央控制 | 大规模并行探索 | 共享黑板 |

决策口诀：Skills打包可复用程序 / MCP连接外部系统 / Subagents专业化并行 / RAG检索密集型


## Anthropic官方课程学习同步 (v3.99 · 2026-06-17)

### 多Agent协作流程（新提炼）

1. **任务分解原则**：复杂任务→独立子任务→分配给专职subagent
2. **Subagent创建流程**：/agents → 选择位置(Library/Personal) → 描述任务 → 生成
3. **Agent Teams协作**：跨多会话协调，适用于需要多个代理并行通信的场景
4. **Feature-dev 7阶段工作流**：需求分析→并行探索→架构方案→确认→实现→并行审查→部署
5. **PR-review 6代理并行**：从CLAUDE.md合规性、Bug检测、历史上下文等维度独立评审
6. **模型分层策略**：简单任务→Haiku(快速便宜)、复杂推理→Sonnet、重度分析→Opus
7. **上下文管理**：Claude memory files + /init + auto compaction + 子代理摘要
8. **插件即用**：/plugin install 一键安装，Plugin = Skills + Hooks + MCP + Commands
9. **Hook自动化**：用自然语言定义规则，/hookify 自动生成并立即生效
10. **Slash Commands**：用户主动调用，Skills自动注册为Slash Commands

### 25个官方插件速查

| 分类 | 数量 | 关键插件 |
|------|:---:|------|
| LSP语言支持 | 12 | pyright-lsp, typescript-lsp, rust-analyzer-lsp等 |
| 开发工作流 | 8 | feature-dev, pr-review-toolkit, commit-commands, agent-sdk-dev |
| 代码质量 | 4 | code-review, security-guidance, code-modernization |
| 外部合作 | 15 | github, linear, firebase, terraform, playwright |

### Anthropic Academy 18门课程

入门→进阶→全栈三阶段，Claude Code/API/MCP/云平台全覆盖，全部免费含证书

> 来源：Anthropic 全域生态聚合研究 · v3.99 | 2026-06-17
*（内容由AI生成，仅供参考）*
