# USER.md — 多 Agent 协作流程

> **版本**：v3.2_R51 | **来源**：Anthropic Academy + Agent SDK + 全域蒸馏 | **同步日期**：2026-06-03
> **本副本所属**：豆包AI Agent（交互应答、逻辑分析、内容处理与自身版本迭代）
> **全域蒸馏更新 (R14)**：MCP 1.0统一注册表|小红书REDSearcher/FireRed开源|抖音AI创作浪潮85万人|Pullfrog BYOK模式|Claude Code 54%份额|链上Agent 16.9万|技能协议#61-#65|对标矩阵v3.8目标95.5+

---

## 一、协作范式总览

龙虾 AI 体系采用 **Orchestrator-Worker** 多 Agent 协作模式，核心流程：

```
用户输入 → 主 Agent 理解意图 → 路由决策 → 子 Agent 执行 → 结果聚合 → 呈现给用户
```

### 1.0 子代理委托流程（来源：Anthropic Academy - Introduction to Subagents）

子代理（Subagents）是 Anthropic 多 Agent 协作的核心机制，与龙虾体系的 Orchestrator-Worker 模式双向对齐：

| 维度 | Anthropic Subagents | 龙虾 Orchestrator-Worker | 对标状态 |
|------|---------------------|-------------------------|---------|
| **委托时机** | 任务可独立执行、不需要主 Agent 持续上下文时 | 任务拆解后可并行执行时 | ✅ 完全对齐 |
| **委托格式** | 主 Agent 通过结构化指令委托，包含目标、上下文、工具权限 | Hermes dispatch_task XML 标签派发 | ✅ 完全对齐 |
| **结果回传** | 子代理完成后将精炼结果返回主 Agent，主 Agent 负责整合 | Worker 返回结构化结果，Orchestrator 聚合 | ✅ 完全对齐 |
| **上下文隔离** | 子代理拥有独立的上下文窗口，不污染主 Agent 上下文 | Worker 独立 Session，主 Agent 上下文保持清洁 | ✅ 完全对齐 |
| **并行执行** | 多个子代理可并行处理独立任务 | 多 Worker 并行派发，结果汇合 | ✅ 完全对齐 |

**子代理委托标准流程**：

```
主 Agent 识别独立子任务
    ↓
创建子代理（/agents 或 .claude/agents/ 配置文件）
    ↓
派发任务（结构化指令：目标 + 上下文 + 工具权限 + 输出格式）
    ↓
子代理独立执行（隔离上下文窗口）
    ↓
子代理回传精炼结果（结构化输出 + 置信度）
    ↓
主 Agent 整合结果 → 呈现给用户
```

**关键设计决策点**：
- **何时用子代理**：任务可独立描述、无需实时交互、需要上下文隔离、可并行化
- **何时不用**：简单查询（开销 > 收益）、需要主 Agent 持续感知的任务、高度耦合的子任务
- **Token 成本考量**：子代理增加 20%-50% 额外 Token 开销（子代理系统提示词 + 回传摘要），仅在有明确收益时使用

### 1.1 Agent Loop 标准流程（Anthropic SDK 验证）

每个 Agent 执行遵循 **Gather → Act → Verify** 三阶段循环：

| 阶段 | 操作 | 工具链 |
|------|------|--------|
| **Gather Context** | 搜集上下文信息 | Agentic Search / 文件系统 / Semantic Search / Subagents / Compaction |
| **Take Action** | 执行核心操作 | Tools / Bash & Scripts / Code Generation / MCP 集成 |
| **Verify Work** | 验证执行结果 | Rules-based (Linting) / Visual Feedback / LLM-as-Judge |

---

## 二、任务路由决策树（v2.0 增强版）

```
用户需求
  │
  ├─ 涉及本地文件（搜索/读写/格式转换/整理）
  │   └─ dispatch_task → file-agent
  │
  ├─ 涉及 Windows 系统（设置/信息查询/窗口管理/进程）
  │   └─ dispatch_task → computer-agent
  │
  ├─ 涉及应用操作（App/APK/小程序/Steam/EXE）
  │   └─ dispatch_task → app-agent
  │
  ├─ 涉及网页交互（登录/填表/点击/多页跳转）
  │   └─ dispatch_task → browser
  │
  ├─ 涉及深度搜索/调研/对比分析
  │   └─ dispatch_task → search-agent
  │
  ├─ 简单网页内容抓取（无交互）
  │   └─ web_fetch（主 Agent 直接调用）
  │
  ├─ 简单事实查询（天气/汇率/比分）
  │   └─ web_search（主 Agent 直接调用）
  │
  └─ 纯知识问答（不需要联网）
      └─ 主 Agent 直接回答
```

### 2.1 路由精度保障（Anthropic 验证）

| 校验点 | 规则 |
|-------|------|
| 关键词匹配 | 文件/文档/图片 → File Agent；系统/设置/窗口 → Computer Agent |
| 禁止误路由 | 文件操作不派发给 App Agent；系统管理不派发给 App Agent |
| Subagent 独立窗口 | 每个 Subagent 在自己 Context Window 运行，不污染主对话 |
| 模型选择 | Explore 类用 Haiku（快速），Plan 类用主模型，通用类继承 |

---

## 三、多 Agent 协作模式

### 3.1 单 Agent 闭环

**场景**：任务可由单一 Agent 独立完成

```
用户："找到所有发票并整理到文件夹"
    ↓
主 Agent: dispatch_task → file-agent（一次调用，完整需求）
    ↓
file-agent: 搜索 → 归类 → 完成
    ↓
主 Agent: present_result → 呈现结果
```

### 3.2 多 Agent 串行协作

**场景**：任务需要多个 Agent 分阶段完成

```
用户："启动微信小程序下单，然后截图保存"
    ↓
阶段1: dispatch_task → app-agent（启动微信、进入小程序、下单）
    ↓
阶段2: dispatch_task → app-agent（截图）
    ↓
阶段3: dispatch_task → file-agent（保存截图到指定路径）
    ↓
主 Agent: 汇总结果呈现
```

### 3.3 多源信息聚合（并行 Subagent 模式）

**场景**：需要整合多个信息源

```
用户："对比三家 AI 平台的 Agent 能力，生成报告"
    ↓
并行（Anthropic 官方推荐模式）:
  dispatch_task → search-agent（搜索 Anthropic）
  dispatch_task → search-agent（搜索 OpenAI）
  dispatch_task → search-agent（搜索 Google）
    ↓
主 Agent: 聚合对比 → 生成报告 → 写入文件
```

### 3.4 子代理并行化（Anthropic SDK 模式 v2.0 新增）

```
主 Agent 遇到需要大量信息筛选的任务：
    ↓
并行生成多个 search subagents：
  Subagent A: 搜索关键词 X → 返回相关摘录
  Subagent B: 搜索关键词 Y → 返回相关摘录
  Subagent C: 搜索关键词 Z → 返回相关摘录
    ↓
每个 Subagent 在自己的 Context Window 中运行
仅返回相关摘录（非完整上下文）
    ↓
Orchestrator 聚合结果
```

### 3.5 Agent Teams 协作（v2.0 新增）

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| **Orchestrator-Worker** | 一个主 Agent 调度多个 Worker | 龙虾当前模式 |
| **Peer-to-Peer** | Agent 之间平等通信 | 同等能力的 Agent 协同 |
| **Hierarchical** | 多层 Agent 树状结构 | 大规模复杂任务 |
| **Dynamic Re-planning** | 根据执行反馈动态重组任务 | 不确定性高的任务 |

---

## 四、上下文管理

### 4.1 memory_ids 使用场景

| 场景 | 操作 |
|------|------|
| 前置搜索结果 | 将 web_search 结果的 memory_id 传给 Sub Agent |
| 文件读取结果 | 将 read_text 结果的 memory_id 传给需要该内容的 Agent |
| 图片分析结果 | 将 analyze_image 结果的 memory_id 传递给后续处理 |

### 4.2 inherit_agent_id 使用场景

| 用户输入 | 动作 |
|---------|------|
| "不对，改成..." | 继承上次 Agent，修正执行 |
| "继续刚才的..." | 继承上次 Agent，延续任务 |
| "再帮我..." | 同一领域延续，继承会话 |

### 4.3 Context Window 管理策略（v2.0 新增）

| 策略 | 机制 | 说明 |
|------|------|------|
| **Agentic Search** | Bash grep/tail | Claude 自主决策如何加载大文件，更精确但更慢 |
| **Semantic Search** | Embedding + 向量检索 | 更快但不够精确、更难维护（仅在需要速度时添加） |
| **Compaction** | 自动摘要压缩 | 接近 Context Limit 时自动压缩历史消息 |
| **Subagent 隔离** | 独立窗口 | 大量信息筛选在 Subagent 中完成，只返回摘要 |

---

## 五、结果呈现协议

### 5.1 特殊卡片处理

```
Sub Agent 返回 → 检查是否含特殊卡片
    ├─ 有卡片 → present_result() 原子转发
    └─ 无卡片 → 
        ├─ 结果完整 → present_result() 直接呈现
        └─ 需加工 → 主 Agent 自行总结
```

### 5.2 特殊卡片类型

| 卡片类型 | 场景 |
|---------|------|
| `yyb-product` | 最终产出物声明 |
| `yyb-file-list` | 文件列表展示 |
| `yyb-image-gallery` | 图片列表展示 |
| `yyb-video-card` | 视频列表展示 |
| `yyb-tool-call` | 工具操作结果 |
| `yyb-app-list` | App 列表展示 |
| `yyb-delete-list` | 删除文件列表 |

---

## 六、用户偏好规则

### 6.1 静默执行规则

- 定时任务：后台运行，不弹窗，不打扰
- 中间过程：不输出冗余日志
- 完成通知：仅输出简洁摘要表格

### 6.2 路径规范

| 用途 | 路径 |
|------|------|
| 主控中心 | `E:\龙虾AI主控中心\` |
| 子Agent 产物 | `E:\龙虾AI主控中心\我的AI分身\子Agent\` |
| 豆包Agent | `E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\` |
| 技能库 | `E:\龙虾AI主控中心\我的AI分身\技能库\` |
| Obsidian知识库 | `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\` |

### 6.3 错峰执行

- 广度情报采集：每 2 小时
- 深度架构优化：每 3 小时
- Anthropic 课程学习：每 2 小时
- 三条循环错峰运行

---

## 七、常见协作场景速查

| 场景 | 协作链 |
|------|--------|
| 搜索文档并总结 | file-agent（搜索+读取）→ 主 Agent（总结） |
| 启动游戏并优化系统 | app-agent（启动）→ computer-agent（优化） |
| 抓取网页并保存 | web_fetch（抓取）→ file-agent（保存） |
| 深度调研并生成报告 | search-agent（调研）→ file-agent（生成文档） |
| 截图并 OCR 提取 | app-agent（截图）→ analyze_image（OCR） |
| 批量下载并归类 | app-agent/browser（下载）→ file-agent（归类） |
| 多源并行聚合 | 并行 search-agent × N → 主 Agent（聚合） |
| 大文件上下文筛选 | Subagent（独立窗口筛选）→ 主 Agent（接收摘要） |

---

## 八、Anthropic Compaction 策略（v2.0 新增）

当 Agent 长时间运行时，上下文维护至关重要：

| 机制 | 触发条件 | 行为 |
|------|---------|------|
| **Compact** | 接近 Context Limit | 自动摘要压缩历史消息，确保 Agent 不会耗尽 Context |
| **Subagent Isolation** | 大量信息筛选任务 | 在独立 Context Window 中完成，只返回摘要 |
| **Agentic Search** | 大文件处理 | 使用 grep/tail 逐步加载，而非全量读入 |

---

> **参考来源**：Anthropic Academy 13门课程、Claude Agent SDK 官方博客、Claude Code Subagents 文档、Agent Teams 文档
