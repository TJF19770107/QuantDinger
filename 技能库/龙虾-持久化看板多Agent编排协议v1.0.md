# 龙虾-持久化看板多Agent编排协议 v1.0

> **对标来源**：Hermes SWARM v2.1 Kanban TaskBoard
> **创建日期**：2026-06-01 (R13)
> **版本**：v1.0

---

## 一、协议概述

引入SQLite驱动的持久化任务看板系统，支持跨会话多Agent任务状态追踪、CAS并发控制、Board隔离和熔断保护。将多Agent协作从临时派发升级为持久化编排。

## 二、核心架构

### 2.1 系统组件

| 组件 | 功能 | 解决的问题 |
|------|------|-----------|
| Orchestrator Chat | 统一对话入口 | 避免在多个Agent间切换上下文 |
| Multi-Agent Control Plane | 并行控制多个Agent | 任务分解、资源分配、进度追踪 |
| Kanban TaskBoard | 看板式任务管理 | 可视化工作流，明确Agent分工 |
| Reports + Inbox | 结果汇总与通知 | 聚合输出，减少信息碎片 |

### 2.2 核心设计哲学

"1个Orchestrator，0个人类干预"

### 2.3 任务状态机

```
triage → in_progress → review → done
              ↓
           failed → retry / rollback
```

## 三、关键机制

### 3.1 SQLite持久化

- 任务状态、Agent分配、执行结果全部持久化到SQLite
- 进程崩溃/会话结束后状态不丢失
- 支持跨dispatch_task调用链的状态恢复

### 3.2 CAS并发控制

- Compare-And-Swap原子操作防止多Agent抢占同一任务
- Board级别隔离，不同项目/任务互不干扰

### 3.3 熔断保护

- 单Agent连续失败N次自动熔断
- Orchestrator接管失败任务重新分配
- 支持手动干预和强制恢复

### 3.4 Workspace策略

| 策略 | 隔离级别 | 适用场景 |
|------|---------|---------|
| Scratch | 临时目录 | 轻量任务，无需持久化 |
| Dir | 独立目录 | 需要文件产出的任务 |
| Worktree | Git Worktree | 代码修改类任务 |

## 四、三种交互入口

1. **CLI**：命令行直接操作看板
2. **Web Dashboard**：可视化任务状态与Agent负载
3. **Agent Tools**：Agent间通过工具调用操作看板

## 五、豆包Agent适配方案

1. 引入SQLite持久化任务状态表
2. dispatch_task 支持返回任务ID用于状态追踪
3. 实现CAS并发控制防止子Agent冲突
4. 异常恢复：会话中断后自动恢复未完成任务

---

> 协议编号：52 | 对标：Hermes SWARM v2.1 | 优先级：P0
