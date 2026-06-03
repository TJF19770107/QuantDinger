# Hermes Agent SWARM 架构解析

> 来源: 2026-05-31 迭代扫描
> 对标目标: 豆包Agent中枢调度 + 自进化闭环

---

## 一、SWARM架构核心组件

| 组件 | 功能 | 解决问题 |
|------|------|---------|
| Orchestrator Chat | 统一对话入口 | 避免多Agent上下文切换 |
| Multi-Agent Control Plane | 并行控制多Agent | 任务分解、资源分配、进度追踪 |
| Kanban TaskBoard | 看板式任务管理 | 可视化工作流，明确分工 |
| Reports + Inbox | 结果汇总与通知 | 聚合输出，减少信息碎片 |
| TUI View | 终端界面 | 开发者友好操作 |

## 二、Orchestrator工作流

```
用户输入 "我要做XXX"
  ↓
Orchestrator Chat 接收
  ↓
任务分解 (Multi-Agent Control Plane)
  ├─ Agent A: 调研收集
  ├─ Agent B: 执行编写
  ├─ Agent C: 审查测试
  └─ Agent D: 汇总发布
  ↓
Kanban看板追踪进度
  ↓
Reports + Inbox 聚合输出
```

## 三、自进化五步闭环

```
执行任务 → 自动评估结果 → 反思改进点
    ↓                          ↓
优化提升 ← 沉淀为技能(可复用) ← 提炼经验
```

## 四、黑板架构 (Blackboard Architecture)

多个Agent通过共享"黑板"异步协作，而非直接通信：
- 新增Agent只需适配黑板协议
- 大幅降低系统耦合度
- 支持动态扩展

## 五、分层记忆系统

| 记忆层 | 内容 | 生命周期 |
|--------|------|---------|
| 工作记忆 | 当前任务上下文 | 任务结束释放 |
| 情景记忆 | 任务执行经验 | 会话级持久 |
| 语义记忆 | 概念与知识 | 长期积累 |
| 程序记忆 | 技能与工作流 | 版本管理 |

## 六、对比同类框架

| 特性 | Hermes SWARM | CrewAI | LangGraph | AutoGen |
|------|-------------|--------|-----------|---------|
| Agent数量 | 无限 | 有限 | 有限 | 有限 |
| 编排方式 | 中央Orchestrator | 角色协作 | 图结构 | 对话式 |
| UI | TUI+Desktop | CLI | Python API | Python API |
| 学习曲线 | 低 | 中 | 高 | 高 |
| 任务管理 | 看板系统 | 内置 | 自定义 | 自定义 |

## 七、可融合要点

1. **Orchestrator Chat设计**：Marvis Main Agent即Orchestrator，强化任务分解与Agent调度
2. **自进化闭环**：每轮迭代自动触发评估→反思→沉淀→优化
3. **黑板模式**：Sub Agent间通过共享状态黑板通信，降低耦合
4. **分层记忆**：工作记忆(当前会话) → 情景记忆(偏好规则) → 语义记忆(技能库) → 程序记忆(工作流模板)
5. **Kanban可视化**：任务分解状态追踪

---

*归档时间: 2026-05-31*