# 龙虾全域官方模板 - 最终版

> **版本**：v3.0 Final  
> **适用范围**：龙虾AI主控中心全域所有Agent迭代任务  
> **最后更新**：2026-05-31  
> **维护者**：龙虾AI主控中心架构组  

---

## 一、模板概述

本模板定义了龙虾AI主控中心所有Agent迭代任务的标准执行规范，采用**龙虾五步法**为骨架，确保每次迭代产出结构化、可执行、可追溯。

### 五步法核心

```
情报采集(Intelligence) → 架构升级(Architecture) → 能力迭代(Capability) → 缺口分析(Gap) → 可执行代码产出(Code)
```

每一步均有明确的**输入约束**、**执行规范**、**质量门禁**和**产物清单**。

---

## 二、步骤详细规范

### Step 1：情报采集 (Intelligence Collection)

| 维度 | 规范 |
|------|------|
| **输入** | 竞品动态、技术白皮书、社区实践、内部回顾、用户反馈 |
| **输出** | 结构化情报摘要（含来源、可信度评级、关键提取点） |
| **质量门禁** | 至少覆盖3个维度来源；每条情报标注时间戳和URL |
| **产物** | `情报采集摘要.md` / `intelligence_brief.json` |

**执行要求**：
- 情报必须分类：A类（核心对标系统）、B类（技术栈趋势）、C类（用户侧需求）
- 每条情报提炼为 ≤200字的摘要 + 3个关键洞察
- 标注与当前架构的关联度（高/中/低）

### Step 2：架构升级 (Architecture Upgrade)

| 维度 | 规范 |
|------|------|
| **输入** | 情报采集摘要 + 当前架构文档 |
| **输出** | 新架构全景图 + 分层设计 + 组件交互时序图 |
| **质量门禁** | 架构图至少5层；每层标注对标系统；关键路径有备选方案 |
| **产物** | `架构升级方案_v{x.y}.md` + `architecture_diagram.mermaid` |

**执行要求**：
- 架构分层自上而下：思考层 → 规划层 → 执行层 → 工具层 → 基础设施层
- 每层必须标注对标系统（如"思考层对标Claude Agent SDK + Gemini 2.5"）
- 所有数据流和调用链路必须用 Mermaid sequence diagram 描述
- 关键路径必须有降级策略（Plan B）

### Step 3：能力迭代 (Capability Iteration)

| 维度 | 规范 |
|------|------|
| **输入** | 架构升级方案 + 现有能力矩阵 |
| **输出** | 更新后的能力矩阵 + 新增/废弃/升级能力清单 |
| **质量门禁** | 每个能力有唯一编号、对标系统、实现状态、代码模板路径 |
| **产物** | `能力矩阵_v{x.y}.json` + `技能库更新索引.md` |

**执行要求**：
- 能力矩阵使用 JSON Schema 严格校验
- 能力编号格式：`{层级}-{领域}-{序号}`（如 `THINK-LLM-001`）
- 实现状态：`PLANNED` / `IN_PROGRESS` / `IMPLEMENTED` / `VERIFIED` / `DEPRECATED`
- 每个新增能力必须有对应的代码模板引用路径

### Step 4：缺口分析 (Gap Analysis)

| 维度 | 规范 |
|------|------|
| **输入** | 新能力矩阵 + 对标系统能力清单 |
| **输出** | 差距热力图 + 优先级排序的补缺路线图 |
| **质量门禁** | 每个缺口有优先级（P0-P3）、预估工时、前置依赖 |
| **产物** | `缺口分析报告.md` + `补缺路线图.md` |

**执行要求**：
- 缺口按影响面分 P0（核心功能缺失）/ P1（关键体验断层）/ P2（竞争力短板）/ P3（锦上添花）
- P0 缺口必须有应急替代方案
- 补缺路线图以时间轴展示（短期/中期/长期）

### Step 5：可执行代码产出 (Executable Code)

| 维度 | 规范 |
|------|------|
| **输入** | 补缺路线图 + 能力矩阵中 `PLANNED` 项 |
| **输出** | 可直接部署的代码 + 单元测试 + 集成测试 + 部署文档 |
| **质量门禁** | 代码通过 linting；测试覆盖率 ≥ 80%；有完整的 API 文档 |
| **产物** | `src/` 目录 + `tests/` 目录 + `deploy/` 目录 + `README.md` |

**执行要求**：
- 代码语言根据能力层级自动选择（思考层→Python、工具层→Go/Rust、前端→TypeScript）
- 每个模块必须有 `__init__` 或等效入口
- 测试框架统一：Python用pytest、JS用vitest
- 产物路径必须写入迭代日志

---

## 三、质量门禁总览

| 步骤 | 门禁项 | 检查方式 | 阻断级别 |
|------|--------|----------|----------|
| Step 1 | 情报覆盖 ≥3个维度 | 人工 Review | Warning |
| Step 1 | 每条情报有时间戳 | 自动校验 | Error |
| Step 2 | 架构图 ≥5层 | 自动计数 | Error |
| Step 2 | 关键路径有降级方案 | 人工 Review | Warning |
| Step 3 | 能力矩阵 JSON Schema 校验通过 | 自动校验 | Error |
| Step 3 | 每个能力有代码模板引用 | 自动校验 | Warning |
| Step 4 | P0 缺口有应急方案 | 人工 Review | Error |
| Step 4 | 补缺路线图有时间轴 | 自动校验 | Warning |
| Step 5 | 代码 Linting 通过 | CI 自动 | Error |
| Step 5 | 测试覆盖率 ≥80% | CI 自动 | Error |

---

## 四、产物清单总览

每次全维度迭代必须产出的文件清单：

```
{Agent目录}/
├── 龙虾全域官方模板-最终版.md          # 本模板
├── {Agent名}架构升级方案_v{x.y}.md     # Step 2 产物
├── {Agent名}能力矩阵_v{x.y}.json       # Step 3 产物
├── {Agent名}技能库更新索引_v{x.y}.md   # Step 3 产物
├── {Agent名}缺口分析报告.md             # Step 4 产物
├── {Agent名}补缺路线图.md               # Step 4 产物
├── {Agent名}迭代日志_{date}_v{x.y}.md  # 迭代日志
├── src/                                 # Step 5 产物
│   ├── think/      # 思考层代码
│   ├── plan/       # 规划层代码
│   ├── execute/    # 执行层代码
│   ├── tool/       # 工具层代码
│   └── infra/      # 基础设施层代码
├── tests/                               # Step 5 产物
└── deploy/                              # Step 5 产物
```

---

## 五、迭代日志格式规范

每次迭代日志必须包含以下章节：

```markdown
# {Agent名}迭代日志_{YYYY-MM-DD}_v{x.y}

## 1. 迭代摘要
<!-- ≤500字概括本次迭代目标与核心变更 -->

## 2. 情报输入
<!-- 列出本次迭代使用的全部情报源及关键提取 -->

## 3. 架构变更
<!-- 版本号变更说明 + 架构图Diff -->

## 4. 能力变更
<!-- 新增/升级/废弃的能力清单表 -->

## 5. 缺口关闭情况
<!-- 已关闭的缺口 + 新增缺口 -->

## 6. 代码产出
<!-- 所有新增/修改的源码文件路径清单 -->

## 7. 测试结果
<!-- 测试覆盖率 + 关键测试用例结果 -->

## 8. 下一步计划
<!-- 下一次迭代的方向和优先级 -->
```

---

## 六、版本号规范

采用语义化版本（SemVer）：`主版本.次版本.修订号`

| 变更类型 | 版本号变化 | 示例 |
|----------|-----------|------|
| 架构层重构（新增/删除AI层） | 主版本 +1 | v2.0 → v3.0 |
| 能力矩阵新增 ≥3 项核心能力 | 次版本 +1 | v2.2 → v2.3 |
| 单个能力优化/Bug修复 | 修订号 +1 | v2.3.0 → v2.3.1 |

---

## 七、附录

### A. 对标系统速查表

| 系统 | 核心定位 | 关键技术点 | 对标层级 |
|------|----------|-----------|----------|
| Codex CLI | Agentic Shell | 512K Context, Hierarchical Agent, Checkpoint | 编码层 + 规划层 |
| Claude Agent SDK | Agent SDK | Central Orchestrator, Memory Bank, Agent Graph | 思考层 + 规划层 |
| Hermes | Agent Framework | Tool Registry, Multi-model Scheduling | 工具层 + 规划层 |
| OpenClaw | Agent Gateway | Message Routing, Auth/Quota, Dynamic Composition | 基础设施层 |
| Gemini 2.5 | Foundation Model | 1M+ Context, CoT, Long-Context Cache | 思考层 |
| Marvis Workbody | Local Agent | 本地优先, 文件+Shell+模型三合一, Sandbox | 执行层 + 基础设施层 |
| OpenCode | Coding Agent | Multi-Agent Coding, Autonomous PR | 编码层 |

### B. 能力编号体系

| 层级代码 | 层级名 | 领域代码示例 |
|----------|--------|-------------|
| THINK | 思考层 | LLM, MEM, CTX |
| PLAN | 规划层 | REACT, REFLEX, PLANEXEC |
| EXEC | 执行层 | CODE, FILE, SHELL |
| TOOL | 工具层 | REGISTRY, GATEWAY, PLUGIN |
| INFRA | 基础设施层 | LOCAL, DEPLOY, SANDBOX |
| EVOL | 自进化层 | OBSERVE, REFLECT, UPDATE |

---

> **模板使用声明**：本模板为龙虾AI主控中心全域标准，所有子Agent迭代任务必须严格遵循。未经架构组批准，不得修改步骤流程和质量门禁标准。
