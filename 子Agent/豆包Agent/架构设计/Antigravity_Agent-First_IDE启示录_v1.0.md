# Google Antigravity Agent-First IDE 启示录 v1.0

> 生成日期：2026-05-31 | 来源：Google Antigravity v1.20.6 完整指南

---

## 一、Antigravity 核心范式

### 1.1 什么是 Agent-First？

```
传统 IDE（Code-First）：
开发者写代码 → IDE辅助（补全/提示/检错）

Agent-First IDE：
开发者描述目标 → Agent规划方案 → Agent自主执行 → 开发者审查结果
```

Antigravity 是 Google 在 VS Code 分支上构建的 Agent-First IDE：

| 属性 | 值 |
|------|-----|
| 基础 | VS Code Fork（不是插件，是独立IDE） |
| 模型 | Gemini 3.1 Pro为主，支持6种模型 |
| 上下文 | 1M+ token |
| 定价 | 免费版 ~20次Agent请求/天 |
| SWE-bench | 76.2% |
| MCP | 支持（GitHub/数据库/API） |

### 1.2 双界面设计

```
Editor View（编辑器界面）          Manager View（管理器界面）
┌──────────────────────┐    ┌──────────────────────────┐
│ 代码编辑 + Agent对话  │    │ Mission Control面板       │
│                      │    │ ├── 任务列表+进度         │
│  ┌────────────────┐  │    │ ├── 并行Agent管理         │
│  │ Agent Panel     │  │    │ ├── 代码Diff审查          │
│  │ (自然语言交互)  │  │    │ ├── 截图/录制回放        │
│  └────────────────┘  │    │ └── Artifact历史         │
│                      │    │                          │
│  左侧：文件树+搜索   │    │  右侧：Agent状态+日志     │
└──────────────────────┘    └──────────────────────────┘
```

---

## 二、Agent 工作流

### 2.1 Agent 执行四阶段

```
1. 接收目标（Goal Input）
   ↓ 开发者用自然语言描述任务
2. 自主规划（Autonomous Planning）
   ↓ Agent分析代码库→生成步骤→评估风险
3. 自主执行（Autonomous Execution）
   ↓ Agent创建文件/修改代码/运行测试/验证结果
4. 人工审查（Human Review）
   ↓ 开发者审查Diff→确认/驳回/调整
```

### 2.2 规划示例

```
用户输入："给这个Python项目添加类型注解"

Agent规划：
  Step 1: 扫描项目结构，识别所有 .py 文件
  Step 2: 分析现有类型使用情况
  Step 3: 生成类型注解建议（函数签名+变量）
  Step 4: 逐文件应用变更
  Step 5: 运行 mypy 验证
  Step 6: 如有错误，自动修复
  Step 7: 生成 Diff 供审查
```

### 2.3 并行 Agent

Antigravity 支持同时运行多个并行 Agent 处理同一代码库的不同任务：

```
任务A：给 API 层添加类型注解  → Agent 1
任务B：重构数据库查询层       → Agent 2
任务C：更新单元测试            → Agent 3
         ↓
    Manager View 统一管理进度
```

---

## 三、关键启示（豆包Agent可借鉴）

### 3.1 启示1：Agent-First 不是未来，是现在

Antigravity 证明了"描述→执行→审查"范式已进入生产级产品。豆包Agent的龙虾五步法本质上也是Agent-First范式，但缺少：

- 可运行的IDE界面
- 可视化Artifact系统
- 并行Agent管理

### 3.2 启示2：Artifact 透明化是信任的基础

| Artifact类型 | 作用 | 豆包Agent对标 |
|-------------|------|-------------|
| 任务列表+进度 | 让用户知道Agent在做什么 | AutoWake 任务队列 |
| 代码Diff | 精确展示将要修改的内容 | 无 |
| 截图/录制 | 操作结果可视化 | 无 |
| 日志 | 完整执行记录 | 迭代报告 |

### 3.3 启示3：MCP 正在成为 Agent 标准协议

Antigravity 通过 MCP 连接 GitHub / 数据库 / API。豆包Agent当前无MCP支持，R11应规划MCP调研和实现。

### 3.4 启示4：AGENTS.md 规则文件是必备基础设施

Antigravity 的 AGENTS.md 等同于豆包Agent的全域模板。两类文件对比：

| 维度 | AGENTS.md | 龙虾全域官方模板 |
|------|-----------|----------------|
| 作用 | 项目级Agent行为约束 | 全域Agent行为约束 |
| 格式 | Markdown | Markdown |
| 生效范围 | 单项目 | 全域所有子Agent |
| 动态性 | 静态 | 每轮迭代更新 |

### 3.5 启示5：多模型不是奢侈品

Antigravity 支持6种模型切换：

| 模型 | 用途 |
|------|------|
| Gemini 3.1 Pro | 日常任务（默认） |
| Gemini 3.1 Flash | 快速响应 |
| Claude Opus 4.6 | 复杂推理 |
| Claude Sonnet 4.6 | 平衡速度和质量 |
| GPT-OSS-120B | 开源替代 |
| Gemini 2.5 Pro | 长上下文任务 |

豆包Agent应建立模型抽象层，支持动态切换：

```
模型适配器接口：
  - baidu_doubao_2_0_pro    → 复杂任务规划
  - baidu_doubao_2_0_code   → 编码生成
  - baidu_doubao_2_0_lite   → 日常对话
  - claude_opus_4           → 深度推理
  - openai_gpt_o4           → 多模态任务
```

---

## 四、豆包Agent AI IDE 路线图

### 4.1 阶段规划

| 阶段 | 轮次 | 目标 | 产物 |
|------|------|------|------|
| Phase 1 | R10 | Agent-First 界面设计 | UI原型 + 交互流程 |
| Phase 2 | R11 | Artifact 可视化系统 | Diff视图 + 任务面板 |
| Phase 3 | R12 | 并行Agent管理 | Manager View |
| Phase 4 | R13 | MCP 协议集成 | GitHub/数据库插件 |

### 4.2 核心技术选型

| 组件 | 方案A | 方案B | 推荐 |
|------|------|------|------|
| 编辑器基础 | VS Code Extension | 自建IDE | VS Code Extension(快速起量) |
| Agent对话 | VS Code Chat API | 自建终端 | Chat API |
| Artifact渲染 | React组件 | HTML/Markdown | React组件 |
| 并行管理 | Web Worker | Python多进程 | Python多进程(本地) |

---

> 生成时间：2026-05-31 | 版本：v1.0