# 多Agent协作架构参考

**版本**：v1.0
**创建日期**：2026-05-31（R∞迭代）
**上级约束**：角色总说明书 v1.0
**关联技能**：S09 多Agent协作协议 / 龙虾-多Agent协同看板协议v1.0
**参考来源**：疯狂的豇豆多Agent专题(06期) / Hermes Agent Profile机制 / Claude Agent Swarm模式 / CSDN MCP多Agent趋势 / AWS代理式AI演进

---

## 一、多Agent协作的核心问题

在构建多Agent系统时，所有实践者面临五个本质问题：

| 问题 | 描述 | 豇豆方案 | 龙虾方案 |
|------|------|---------|---------|
| **谁来做？** | 任务如何分配给正确的Agent | Profile隔离机制 | Marvis统一调度 + 30秒初筛 |
| **怎么做？** | Agent间如何通信与协作 | Kanban看板 + 原子认领 | 协作协议v2.4 + 看板协议v1.0 |
| **冲突怎么解决？** | 多Agent同时操作同一资源 | 原子认领（先到先得） | 任务级状态锁 |
| **进度怎么追踪？** | 任务可视化与状态同步 | Kanban看板 | 迭代日志 + SQLite看板 |
| **怎么持续优化？** | 协作模式随任务类型进化 | 社区驱动迭代 | 五步自主迭代闭环 |

---

## 二、多Agent适用边界（豇豆方法论）

### 2.1 4类必须用多Agent的人群

| 人群 | 场景 | 龙虾对标 |
|------|------|---------|
| **多角色协作者** | 一人身兼PM/Dev/Ops，需不同Agent扮演不同角色 | 豆包(Hermes(龙虾()))嵌套协作 |
| **复杂项目管理者** | 多依赖/多阶段项目，需要Agent追踪各链路 | 看板协议+状态锁 |
| **多平台运营者** | 小红书/抖音/公众号/YouTube多平台内容分发 | MCP跨平台发布技能 |
| **技术架构师** | 需要Agent分别负责架构设计/代码审查/部署运维 | 豆包(分析)+Hermes(调度)+龙虾(执行) |

### 2.2 5类必用多Agent的任务

| 任务类型 | 特征 | 推荐协作模式 |
|---------|------|------------|
| **跨域复杂项目** | 涉及多个独立知识域 | Pipeline（串行传递） |
| **多平台分发** | 同内容需适配不同平台 | Fan-Out（并行分发） |
| **并行独立子任务** | 子任务间无依赖 | Fan-Out（全并行） |
| **长周期分阶段** | 需状态保持与阶段切换 | Pipeline + 检查点 |
| **需隔离的安全任务** | 不同安全级别需沙箱隔离 | Profile隔离 + Voting（安全审查） |

### 2.3 30秒初筛（龙虾版）

```
问1：任务是否跨多个独立知识域？
    → 是：标记多Agent | 否：继续
问2：子任务能否完全并行执行？
    → 是：标记多Agent | 否：继续
问3：是否需要安全隔离（敏感数据/高风险操作）？
    → 是：标记多Agent | 否：继续
问4：是否是长周期（>1天）且分阶段的任务？
    → 是：标记多Agent | 否：单Agent执行
```

---

## 三、主流多Agent协作模式

### 3.1 Fan-Out（扇出模式）

```
         ┌→ Agent A（任务1）
调度器 ──┼→ Agent B（任务2）
         └→ Agent C（任务3）
              ↓ 结果汇总
           调度器合并输出
```

**适用**：并行独立子任务、多平台内容分发
**龙虾实现**：Hermes Agent分发 + 豆包Agent × N 并行执行

### 3.2 Pipeline（流水线模式）

```
Agent A（采集）→ Agent B（分析）→ Agent C（报告）→ Agent D（归档）
```

**适用**：跨域复杂项目、长周期分阶段任务
**龙虾实现**：豆包(情报采集) → 豆包(分析融合) → 豆包(报告生成) → 龙虾(归档)

### 3.3 Voting（投票模式）

```
同一任务 ─→ Agent A（方案1）
          → Agent B（方案2）→ 投票/融合 → 最优方案
          → Agent C（方案3）
```

**适用**：安全审查、高风险决策、多模型对比
**龙虾实现**：豆包Agent多轮推理交叉验证

### 3.4 Swarm（蜂群模式）

```
任务池 ──→ Agent A 认领任务1
         → Agent B 认领任务2  （动态认领，无需中央调度）
         → Agent C 认领任务3
```

**适用**：大量同类任务、不确定任务数量
**龙虾实现**：看板协议原子认领机制

### 3.5 Kanban（看板模式·豇豆实践）

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│  Todo   │→│ Doing   │→│  Done   │
│         │  │ Agent A │  │         │
│ Task1   │  │ Agent B │  │ Task1   │
│ Task2   │  │         │  │ Task3   │
│ Task3   │  │         │  │         │
└─────────┘  └─────────┘  └─────────┘
```

**核心机制**：
- **Profile隔离**：每个Agent拥有独立的配置/记忆/工具空间
- **原子认领**：Agent认领任务时锁定，避免多Agent冲突
- **可视化追踪**：Kanban列展示任务流转状态

**龙虾对标**：龙虾多Agent协同看板协议v1.0已实现上述机制，需优化Profile隔离粒度（参考Hermes v0.13.0）。

---

## 四、Hermes Agent多Agent实践要点

### 4.1 Profile机制

Hermes Agent v0.13.0通过Profile实现多Agent：
```
~/.hermes/
├── profiles/
│   ├── researcher/    # 研究Agent配置
│   ├── writer/        # 写作Agent配置
│   └── reviewer/      # 审查Agent配置
└── shared/
    └── knowledge/     # 共享知识库
```

**对龙虾的启示**：豆包Agent/Hermes Agent/龙虾Agent的隔离应参考Profile机制，而非简单的目录分离。

### 4.2 Kanban实战流程

1. **创建Kanban Board**：定义列（Todo/In Progress/Review/Done）
2. **Agent认领任务**：Agent主动扫描Todo列并认领（原子操作）
3. **执行与状态更新**：Agent完成任务后移动卡片到下一列
4. **Review与合并**：Review列的卡片由主Agent审核后移入Done

### 4.3 通信协议

Hermes Agent间通信基于：
- **任务卡片**：JSON结构化任务描述
- **共享状态**：SQLite数据库存储Kanban状态
- **事件通知**：文件系统watch触发状态变更通知

---

## 五、行业最新实践（2026年5月）

### 5.1 Claude Agent SDK Swarm模式

```python
# mcp-agent框架的Swarm实现（模型无关）
from mcp_agent.workflows.swarm import Swarm

swarm = Swarm(
    agents=[researcher, writer, reviewer],
    mode="orchestrated"  # or "autonomous"
)
```

### 5.2 腾讯混元Multi-Agent模式

- 多个Agent像真实团队分工协作
- 配合Coze平台可视化编排
- 支持知识库/数据库/文件系统共享

### 5.3 Google Gen AI Toolbox多Agent数据库访问

- MCP协议桥接AI Agent与数据库
- 多Agent共享同一数据库连接池
- OAuth 2.1安全认证确保隔离

### 5.4 CSDN趋势：多模型+多Agent+多Server

```
LLM推理模型 ─┐
LLM检索模型 ─┼→ Agent统一调度 ─→ MCP统一标准
LLM生成模型 ─┘                      ↓
                           Server集群（金融/医疗/政务）
```

---

## 六、龙虾AI主控中心多Agent协作方案

### 6.1 架构总览

```
┌──────────────────────────────────────────────┐
│              Marvis 统一调度层                  │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│    │豆包Agent│  │ Hermes  │  │龙虾Agent│     │
│    │ L3+     │  │ Agent   │  │         │     │
│    └────┬────┘  └────┬────┘  └────┬────┘     │
│         └────────────┼────────────┘          │
│              ┌───────┴───────┐               │
│              │  协作协议v2.4  │               │
│              │  看板协议v1.0  │               │
│              └───────────────┘               │
└──────────────────────────────────────────────┘
```

### 6.2 协作模式映射

| 任务场景 | 龙虾协作模式 | 参与Agent |
|---------|------------|----------|
| 全域情报采集与分析 | Pipeline | 豆包(采集)→豆包(分析)→豆包(报告) |
| 三子Agent同步迭代 | Fan-Out | 豆包/ Hermes / 龙虾并行迭代 |
| 高风险操作确认 | Voting | 豆包×3 交叉验证 |
| 日常任务分发 | Kanban | Hermes分发 + 豆包认领执行 |
| 定时任务批量处理 | Swarm | 豆包×N动态认领定时任务 |

### 6.3 待优化项

| 优先级 | 优化项 | 参考 |
|--------|-------|------|
| P0 | Profile隔离粒度提升 | Hermes v0.13.0 Profile机制 |
| P0 | 30秒初筛自动化集成 | 豇豆多Agent适用边界 |
| P1 | 可视化Kanban看板 | 豇豆Kanban教程 |
| P1 | 原子认领冲突解决增强 | 龙虾看板协议v1.0 |
| P2 | 事件驱动的状态变更通知 | Hermes文件系统watch |
| P2 | 跨Agent共享知识库 | Hermes shared/knowledge |

---

## 七、参考资源

| 资源 | 链接 | 说明 |
|------|------|------|
| 疯狂的豇豆·多Agent专题 | https://www.crazyowen.cn/129.html | 4类人群+5类任务 |
| 疯狂的豇豆·Kanban教程 | https://www.crazyowen.cn/107.html | v0.13.0实战 |
| mcp-agent Swarm模式 | https://github.com/lastmile-ai/mcp-agent | Python多Agent框架 |
| 微软开放智能体网络 | Build2025 | MCP+A2A双协议 |
| AWS代理式AI五大阶段 | AWS Docs | 行业全景 |

---

**多Agent协作架构参考 · v1.0 · 龙虾AI主控中心永久版**