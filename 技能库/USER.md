---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_fded353d67ac11f1a0095254002afed2
    ReservedCode1: nJ1P3aCw4GrGewYPK8l+Gx8rA10PgAlnYmE1qjWTSfRTie9aYAMa9t/m6IRvUjhGHiZov9ciEA4Y0k9KdXSrxmpC8AC3EafBuicYuSbuPzW4CIqXjBTTzUEwmPcvvcAaU3Xlj09CU1MspZ/GO/PjCp66sW2uU9PMbla2U+sUW5bwjq15DpmxiZiM8FE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_fded353d67ac11f1a0095254002afed2
    ReservedCode2: nJ1P3aCw4GrGewYPK8l+Gx8rA10PgAlnYmE1qjWTSfRTie9aYAMa9t/m6IRvUjhGHiZov9ciEA4Y0k9KdXSrxmpC8AC3EafBuicYuSbuPzW4CIqXjBTTzUEwmPcvvcAaU3Xlj09CU1MspZ/GO/PjCp66sW2uU9PMbla2U+sUW5bwjq15DpmxiZiM8FE=
---

# USER.md — 多 Agent 协作流程

> **版本**：v1.1(R80迭代)
> **来源**：Anthropic Academy 官方课程提炼
> **更新日期**：2026-05-31
> **适用范围**：龙虾 AI 体系用户配置

---

## 一、协作范式总览

龙虾 AI 体系采用 **Orchestrator-Worker** 多 Agent 协作模式，核心流程：

```
用户输入 → 主 Agent 理解意图 → 路由决策 → 子 Agent 执行 → 结果聚合 → 呈现给用户
```

---

## 二、任务路由决策树

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

### 3.3 多源信息聚合

**场景**：需要整合多个信息源

```
用户："对比三家 AI 平台的 Agent 能力，生成报告"
    ↓
并行:
  dispatch_task → search-agent（搜索 Anthropic）
  dispatch_task → search-agent（搜索 OpenAI）
  dispatch_task → search-agent（搜索 Google）
    ↓
主 Agent: 聚合对比 → 生成报告 → 写入文件
```

### 3.4 Agent SDK 编排者-工作者三步法（Anthropic Academy R79注入）

```
Step 1: 任务分析
    Orchestrator 评估任务复杂度 → 判断是否需拆解
    产物：任务复杂度判断 + 子目标列表

Step 2: 子目标分配
    为每个子目标创建 Worker Subagent
    传入：task + output_schema + allowed_tools
    原则：一个 Subagent 只做一类事

Step 3: 结果聚合
    收集所有 Subagent 返回 → 验证结构化输出 → 合并报告
    失败处理：单个失败不影响整体，标记 + 降级
```

### 3.5 Dynamic Workflows 六模式

| 模式 | 描述 | 龙虾适用场景 | 示例 |
|------|------|-------------|------|
| **Chain** | 线性链式执行 | 串行多步骤任务 | file-agent → computer-agent |
| **Parallel** | 并行执行 | 多源信息聚合 | 同时搜索多个平台 |
| **Router** | 条件路由 | 意图分发 | 路由决策树判断目标 Agent |
| **Handoff** | Agent 间传递控制权 | 跨域任务交接 | app-agent → browser-agent |
| **Map-Reduce** | 分发-汇聚 | 批量处理 | 多文件并发处理 |
| **Human-in-the-Loop** | 人工审批节点 | 高风险决策 | ask_user 确认卡片 |

### 3.6 上下文隔离机制详解

```
Subagent 执行模型（与主对话隔离）：
┌────────────────────────────────────┐
│  主对话 Context Window（干净）      │
│  ├── Subagent 启动 Prompt          │
│  └── Subagent 结果摘要（返回）      │
│  （中间过程全部不可见）              │
└──────────────┬─────────────────────┘
               │ 仅传递：task + schema
               ▼
┌────────────────────────────────────┐
│  Subagent Context Window（独立）    │
│  ├── 完整执行过程                   │
│  ├── 工具调用链路                   │
│  └── 中间推理步骤                   │
└────────────────────────────────────┘
```

> **核心原则**：Subagent 的中间推理和工具调用不污染主对话。仅 Prompt 和结果摘要进入主上下文。

### 3.7 Managed Agents 平台设计原则

| 原则 | 说明 | 龙虾实现状态 |
|------|------|-------------|
| **隔离性** | 每个 Agent 独立上下文，不相互污染 | ✅ 通过 dispatch_task 实现 |
| **可观测性** | 执行链路可追踪、可审计 | ✅ memory_ids 记录执行过程 |
| **可恢复性** | 失败后可从中断点恢复 | ⚠️ 部分实现（inherit_agent_id） |
| **权限最小化** | Agent 仅拥有完成任务的必要权限 | ✅ 安全分级约束 |
| **标准化接口** | 统一的 task XML 输入 / 结构化输出 | ✅ overall_goal + current_task |

### 3.8 Claude Cowork：Dispatch 与 Computer Use

#### Dispatch（远程任务分配）
```
手机端 → 发送自然语言指令 → 桌面 Claude Cowork 接收 → 自主执行 → 返回结果
```
- 无需在电脑前，通过手机远程触发桌面 Agent
- 适合长时间运行的任务（如批量文件处理、数据清洗）

#### Computer Use（桌面自主控制）
```
Claude 桌面端 → 直接操控鼠标/键盘 → 打开应用/点击/输入 → 完成多步骤任务
```
- 无需编写自动化脚本
- 像人类一样操作系统 GUI
- 适用于需要跨应用操作的场景（如：打开 Excel + 截图 + 粘贴到飞书）

> **龙虾体系借鉴**：Computer Use 能力由 Computer Agent 承载，Dispatch 概念可用于 Hermes 远程调度子 Agent。

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
| 共享知识库 | `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\` |

### 6.3 错峰执行

- 广度情报采集：每 2 小时
- 深度架构优化：每 3 小时
- 两条循环错峰运行

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

---

> **参考来源**：Anthropic Academy - Introduction to Subagents, Claude Code in Action, Introduction to Claude Cowork
*（内容由AI生成，仅供参考）*


---

## Anthropic官方课程R80同步：多Agent协作流程

### Dynamic Workflows 使用场景
1. 代码库级漏洞扫描
2. 大规模文件迁移（500+文件）
3. 交叉验证研究
4. 复杂规划

### 升级路径
单一子任务(<10min)→Subagents / 多代理协作+监督→Agent Teams / 大规模编排→Dynamic Workflows

### Claude Code 最佳实践
- /config 启用 Dynamic Workflows
- /deep-research 运行内置研究工作流
- JS脚本描述编排逻辑，存入项目仓库

> 同步自：Anthropic官方课程 R80 | 2026-06-14
