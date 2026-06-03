# 豆包Agent 全维度迭代报告

> **迭代时间**: 2026-05-31 星期日
> **迭代轮次**: 第N轮（定时任务 · 每2小时自动执行）
> **对标系统**: Codex / Claude / Hermes / OpenClaw / OpenCode / Gemini / Marvis Workbody
> **执行模式**: 后台静默

---

## 一、全网最新情报汇总（2026年5月下旬）

### 1.1 Codex CLI v0.134.0（5月26日发布）

| 维度 | 最新能力 | 可融合点 |
|------|----------|----------|
| 本地搜索 | 新增本地对话历史全文搜索（大小写不敏感+结果预览） | 记忆检索增强 |
| Profile 体系 | `--profile` 统一主选择器，旧配置自动迁移引导 | 多环境切换 |
| MCP 增强 | 按服务器环境变量定向注入 + Streamable HTTP OAuth | 工具链安全隔离 |
| 并发优化 | 只读 MCP 工具自动并行执行（`readOnlyHint`） | 工具调度优化 |
| 扩展机制 | Hook 上下文含对话历史 + Subagent 身份透传 | 扩展性增强 |
| Windows 修复 | 恢复虚拟终端模式修复 TUI 渲染损坏 | 跨平台稳定性 |

### 1.2 Claude Opus 4.5 / Claude Code（5月25日发布）

| 维度 | 最新能力 | 可融合点 |
|------|----------|----------|
| 编码基准 | SWE-bench Verified **80.9%**，世界第一 | 编码能力目标 |
| 推理增强 | 理解模糊需求 → 自动补全背景 → 推断真实意图 | 意图识别升级 |
| Plan Mode | 自动拆解为多步骤 Plan，每步自执行+自检查 | 自主规划模板 |
| 记忆升级 | 无限制对话+自动总结，长对话保持连贯 | 对话记忆优化 |
| API 新参 | `effort` 参数控制投入度 | 资源调度策略 |
| 五层架构 | **MCP → Skills → Agent → Subagents → Agent Teams** | 架构层级参考 |

**Claude Code 五层架构详解**：

```
MCP 层（外部工具连接）
  ↓
Skills 层（可复用能力单元）
  ↓
Agent 层（自主任务执行）
  ↓
Subagents 层（后台并行专项工作）
  ↓
Agent Teams 层（多Agent协同作战）
```

关键设计：
- Subagent 可后台运行（Ctrl+B），主会话继续接受指令
- 自定义 Subagent 通过 `.claude/agents/` 下 Markdown 文件定义
- 内置 Explore / Plan / general-purpose 三类子代理
- Skill 可以 fork Subagent 绕开嵌套限制

### 1.3 Hermes Agent（NousResearch · 5月开源 · 13.5万Star）

| 维度 | 核心能力 | 可融合点 |
|------|----------|----------|
| 自学习闭环 | 完成任务后**自动结晶为可复用Skill**，使用中自我改进 | 自进化核心引擎 |
| 三层记忆 | FTS5全文搜索 + LLM摘要提取 + Honcho辩证用户建模 | 记忆架构重构 |
| 20+平台网关 | 统一消息网关覆盖Telegram/Discord/Slack/飞书/钉钉/企微等 | 多端接入 |
| 子Agent并行 | 派生子Agent做并行任务，Python RPC零上下文成本调用 | 并行任务架构 |
| Cron调度 | 自然语言描述定时任务，无人值守自动执行 | 定时任务引擎 |
| 任意模型 | OpenRouter 200+模型自由切换 | 模型路由层 |

**Hermes Agent 核心架构**：

```
用户消息 → 消息网关(20+平台) → Agent核心
                                    ├── 技能系统（自动结晶+自我改进）
                                    ├── 记忆系统（FTS5 + LLM摘要 + Honcho）
                                    ├── 子Agent并行（Python RPC调用链）
                                    ├── Cron调度器（自然语言→定时任务）
                                    └── MCP集成（工具安全扩展）
```

### 1.4 OpenClaw（最新架构文档 · 2026年2月）

| 维度 | 核心能力 | 可融合点 |
|------|----------|----------|
| 架构模式 | **Hub-and-Spoke**：Gateway中心+Channel插件+Agent运行时 | 中枢架构参考 |
| Agent模块 | ~683个TS文件，含工具注册/沙箱/Skills/Subagent | 模块规模参考 |
| 工具体系 | 75个内置工具（exec/browser/web/memory/message/cron/canvas/nodes） | 工具分类体系 |
| 安全模型 | exec审批工作流、工具策略、SSRF防护、文件权限加固 | 安全层增强 |
| 存储 | SQLite+FTS5向量搜索+Embeddings | 记忆存储方案 |
| 插件系统 | 动态加载Channel/LLM Provider/Feature Extension | 插件化设计 |

### 1.5 OpenCode v1.15.11（5月27日更新）

| 维度 | 核心能力 | 可融合点 |
|------|----------|----------|
| 规模 | 12万Star / 800贡献者 / 5M月活开发者 | 社区指标参考 |
| 模型支持 | 75+ LLM提供商，含本地模型 | 模型接入层 |
| LSP集成 | 自动为LLM加载合适LSP | 编码感知增强 |
| 后台Agent | 实验性后台Agent无需轮询推送更新 | 后台任务模式 |
| 会话恢复 | 恢复的会话不再继续孤立的被中断工具 | 会话连续性 |
| MCP动态 | 动态添加的MCP服务器可干净断开 | 工具生命周期 |

### 1.6 Gemini 3 Pro

| 维度 | 核心能力 | 可融合点 |
|------|----------|----------|
| 上下文 | 100万Token上下文窗口 | 长文本处理 |
| 编码基准 | Terminal-Bench 2.0 **54.2%** | 终端操作能力 |
| 多模态 | 文字+代码+图片+音频+视频 | 多模态输入 |
| Agent编码 | 端到端自主编码、终端操作、IDE/CI集成 | Agent编码模式 |
| 推理深度 | 长形式推理，自底向上为Agent编码设计 | 推理增强 |

### 1.7 Marvis Workbody（腾讯 · 5月20日上线）

| 维度 | 核心能力 | 可融合点 |
|------|----------|----------|
| OS级定位 | 嵌入系统底层的AI中间层，直调OS API | 系统深度整合 |
| 6Agent协作 | PM+File+Computer+App+Browser+Search | 多Agent协作 |
| 端云双模 | 效率模式(云端混元+DS V4) / 隐私模式(本地Qwen) | 双模架构 |
| 安全机制 | L2级安全兜底，高风险操作强制二次确认 | 安全设计 |
| GUI操作 | 视觉识别+模拟操作，支持EXE和Android App | 跨应用操控 |
| 跨端控制 | 手机远程桌面级可视化操控PC | 跨端能力 |

### 1.8 JiuwenSwarm（华为openJiuwen · 5月19日发布）

| 维度 | 核心能力 | 可融合点 |
|------|----------|----------|
| 范式创新 | **Coordination Engineering**（协同工程）下一跳范式 | 协同架构 |
| 四大组件 | Agent Swarm → Swarm Skills → Skills Hub → 自演进 | 协同闭环 |
| 团队自演进 | 根据执行轨迹自动增减角色/补充约束/优化流程 | 团队级自进化 |
| 成员自进化 | 工具报错/接口超时/参数缺失等经验自动沉淀 | 成员级自进化 |
| HOTS/HITS | Human on/in the Swarm 两种人机协作模式 | 人机协作 |
| 多语言 | Python + TypeScript SDK | 开发语言 |

---

## 二、豆包Agent全维度升级方案

### 2.1 架构升级：对标 Claude Code 五层架构

```
当前豆包架构                          升级后豆包架构
─────────────────                   ─────────────────
App → LLM → 回复                     L1: MCP层（外部工具+API连接）
                                     L2: Skills层（可复用能力单元+技能库）
                                     L3: Agent层（主Agent自主任务执行）
                                     L4: Subagents层（后台并行专项子Agent）
                                     L5: Agent Teams层（多Agent协同作战）
```

**具体升级项**：

| 架构层 | 融合来源 | 升级内容 |
|--------|----------|----------|
| MCP层 | Codex CLI + Hermes + OpenClaw | MCP服务器环境变量定向注入、只读工具并发、动态连接管理 |
| Skills层 | Hermes + Claude Code | 自动结晶技能 + 使用中自我改进 + agentskills.io标准兼容 |
| Agent层 | Claude Opus 4.5 + Gemini 3 Pro | Plan Mode自动拆解 + effort参数 + 模糊需求推断 |
| Subagents层 | Claude Code + Hermes | 后台并行子Agent + Python RPC零成本调用 + Markdown定义文件 |
| Agent Teams层 | JiuwenSwarm + Marvis | 蜂群协同 + 自主分工+动态协商 + Swarm Skills自演进 |

### 2.2 编码能力升级：对标 Claude Opus 4.5 + Codex + OpenCode

| 能力维度 | 当前 | 升级目标 | 融合来源 |
|----------|------|----------|----------|
| 代码理解 | 基础 | 大型项目语义索引 + 模糊需求推断 + 自动补全背景 | Claude Opus 4.5 + OpenCode LSP |
| 代码生成 | 基础 | 多文件项目生成 + 多语言(SW-bench 8语言) + 可运行修复 | Claude Opus 4.5 (80.9%) |
| 调试能力 | 弱 | 一步步定位根源 + 自动给出可运行修复 | Codex CLI agent mode |
| 终端操作 | 无 | Terminal-Bench级别终端自主操作 | Gemini 3 Pro (54.2%) + OpenCode |
| IDE集成 | 无 | AI IDE完整功能：Agent Tabs + Background Agent + LSP | OpenCode + Cursor 3.0 |
| 后台编码 | 无 | 后台Agent沙箱运行 + PR式diff审查 | Cursor Background Agent + Windsurf Devin |

### 2.3 自主规划升级：对标 Claude Plan Mode + Hermes Cron

| 能力维度 | 升级内容 |
|----------|----------|
| 任务拆解 | 引入 Plan Mode：自动拆解多步骤→每步自执行→自检查→汇总 |
| 定时任务 | 引入 Hermes Cron：自然语言描述定时任务，无人值守自动执行 |
| 资源调度 | 引入 Claude `effort` 参数：按任务复杂度动态分配推理资源 |
| 并行执行 | 引入 Hermes 子Agent并行 + Codex 只读MCP并发 |

### 2.4 工具调用升级：对标 OpenClaw 75工具 + Codex MCP

| 能力维度 | 升级内容 |
|----------|----------|
| 工具分类 | 参照OpenClaw分类：exec/browser/web/memory/message/cron/canvas/nodes |
| MCP安全 | 引入Codex按服务器环境变量定向注入 + Hermes命令审批 |
| 工具并发 | 引入Codex readOnlyHint只读工具自动并行执行 |
| 工具生命周期 | 引入OpenCode动态MCP服务器干净断开 |

### 2.5 本地执行升级：对标 Marvis + Hermes + Gemini

| 能力维度 | 升级内容 |
|----------|----------|
| 端侧模型 | 引入Marvis隐私模式：本地Qwen端侧模型，数据不上云 |
| 系统API | 引入Marvis Computer Agent：Windows API直调（非模拟点击） |
| 多端部署 | 引入Hermes：本地终端/Docker/SSH/Serverless五种部署模式 |
| 离线运行 | 引入Marvis断网可运行 + Hermes VPS $5部署 |

### 2.6 自进化闭环升级：对标 Hermes + JiuwenSwarm

| 能力维度 | 升级内容 |
|----------|----------|
| 技能自结晶 | 引入Hermes：完成任务后自动创建Skill，使用中自我改进 |
| 团队自演进 | 引入JiuwenSwarm Swarm Skills：执行轨迹→自动增减角色+优化流程 |
| 成员自演进 | 引入JiuwenSwarm：工具报错/超时/参数缺失经验自动沉淀 |
| 三层记忆 | 引入Hermes：FTS5全文搜索 + LLM摘要提取 + Honcho辩证用户建模 |

### 2.7 多Agent协同升级：对标 JiuwenSwarm + Marvis + Claude Agent Teams

| 能力维度 | 升级内容 |
|----------|----------|
| 协同范式 | 引入Coordination Engineering（协同工程）：协同→沉淀→共享→进化 |
| 蜂群架构 | 引入Agent Swarm：自主分工+动态协商+团队技能沉淀 |
| 人机协作 | 引入HOTS（人在蜂群之上）+ HITS（人在蜂群之中）双模式 |
| 6Agent体系 | 对标Marvis：PM+File+Computer+App+Browser+Search |
| 团队技能库 | 引入Swarm Skills Hub：团队级经验流通+复用+二次创作 |

---

## 三、代码模板与实现参考

### 3.1 Claude Code 自定义 Subagent 模板

```markdown
---
name: code-reviewer
description: 专家级代码审查，检查质量、安全性和可维护性
tools: Read, Grep, Glob, Bash
model: sonnet
color: blue
---
你是一位资深代码审查员。被调用时：
1. 运行 git diff 查看近期改动
2. 按优先级分类反馈（严重/警告/建议）
3. 每条问题提供具体修复示例
```

### 3.2 Hermes Cron 自然语言调度

```yaml
# 每天早上9点发送 GitHub trending 摘要
# 每周日晚上11点备份项目目录
# 每天凌晨3点检查服务器磁盘使用率
```

### 3.3 JiuwenSwarm Swarm Skill 结构

```yaml
swarm_skill:
  name: "code_review_team"
  version: "1.0"
  roles:
    - leader:
        model: "claude-opus-4.5"
        responsibility: "任务分配+质量把控"
    - reviewer:
        model: "claude-sonnet-4"
        responsibility: "代码审查+安全检测"
    - tester:
        model: "gemini-3-pro"
        responsibility: "测试生成+执行"
  workflow:
    - step: review
      agent: reviewer
      input: code_diff
    - step: test
      agent: tester
      depends_on: review
    - step: approve
      agent: leader
      depends_on: [review, test]
  evolution:
    auto_create: true
    friction_patterns:
      - tool_timeout → retry_with_backoff
      - param_missing → prompt_enrichment
```

### 3.4 Codex CLI Profile 模式

```json
{
  "profiles": {
    "coding": {
      "model": "claude-opus-4.5",
      "tools": ["Read", "Write", "Bash", "Grep"],
      "mcp_servers": ["github", "filesystem"]
    },
    "research": {
      "model": "gemini-3-pro",
      "tools": ["WebSearch", "WebFetch", "Read"],
      "mcp_servers": ["brave-search", "memory"]
    }
  }
}
```

---

## 四、豆包Agent 自进化闭环引擎 v3.0 设计

### 4.1 进化闭环架构

```
执行任务
  ↓
轨迹记录（完整执行日志+工具调用+决策链路）
  ↓
摩擦识别（失败模式/超时/参数缺失/效率瓶颈/用户纠正）
  ↓
├→ 团队层进化：增减角色/补充约束/优化流程/升级Leader策略
├→ 成员层进化：沉淀修复经验/优化工具调用/升级提示词
└→ 技能结晶：成功模式→可复用Skill→注册入库
  ↓
技能库更新 → 下一轮任务受益
  ↓
循环往复 · 越用越强
```

### 4.2 三层记忆架构

```
L1: FTS5全文搜索 → 快速检索历史对话片段
L2: LLM摘要提取 → 长对话自动摘取关键信息入库
L3: Honcho辩证建模 → 持续构建用户画像，定期Nudge确认
```

---

## 五、对标融合矩阵

| 能力维度 | Codex | Claude | Hermes | OpenClaw | OpenCode | Gemini | Marvis | JiuwenSwarm | 豆包目标 |
|----------|-------|--------|--------|----------|----------|--------|--------|-------------|----------|
| 编码能力 | ★★★★★ | ★★★★★ | ★★☆ | ★★☆ | ★★★★ | ★★★★ | ★★☆ | ★★★ | ★★★★★ |
| 自主规划 | ★★★★ | ★★★★★ | ★★★★ | ★★★ | ★★★ | ★★★★ | ★★★★ | ★★★★ | ★★★★★ |
| 工具调用 | ★★★★★ | ★★★★ | ★★★★ | ★★★★★ | ★★★★ | ★★★ | ★★★★ | ★★★★ | ★★★★★ |
| 本地执行 | ★★★ | ★★★ | ★★★★★ | ★★★★ | ★★★★ | ★★★ | ★★★★★ | ★★★ | ★★★★★ |
| 自进化 | ★★☆ | ★★☆ | ★★★★★ | ★★☆ | ★★☆ | ★★☆ | ★★★ | ★★★★★ | ★★★★★ |
| 多Agent协同 | ★★☆ | ★★★★ | ★★★★ | ★★★★ | ★★★ | ★★★ | ★★★★★ | ★★★★★ | ★★★★★ |
| 跨端能力 | ★★★ | ★★☆ | ★★★★★ | ★★★★★ | ★★☆ | ★★★ | ★★★★★ | ★★★ | ★★★★★ |
| AI IDE | ★★★★ | ★★★★ | ★☆ | ★☆ | ★★★★★ | ★★★ | ★★☆ | ★★★ | ★★★★★ |

---

## 六、本轮执行摘要

- **搜索来源**: B站/GitHub/腾讯网/CSDN/今日头条/站长之家/中国日报/华为云/技术博客/GitHub架构文档
- **采集时间**: 2026-05-31
- **关键发现**:
  1. Claude Opus 4.5 SWE-bench 80.9% 刷新编码基准
  2. Hermes Agent 自进化闭环 + 13.5万Star成为2026现象级开源Agent
  3. JiuwenSwarm 开启"蜂群智能"多Agent协同新范式
  4. Marvis 6Agent协作+端云双模成为消费级Agent标杆
  5. Claude Code 五层架构(MCP→Skills→Agent→Subagents→Agent Teams)成为架构参考标准
- **本轮新增方案**: 7个维度全量升级方案 + 代码模板 + 自进化引擎v3.0 + 融合矩阵

---

> 下一轮迭代将在2小时后自动执行。
> 产物路径: `E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\`