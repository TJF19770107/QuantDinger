# 龙虾-Hermes Swarm多Agent协作协议 v1.0

> **协议编号**：63
> **对标来源**：Hermes v0.15.0 Kanban Swarm (104 PRs打造)
> **创建轮次**：R18
> **创建时间**：2026-06-01
> **状态**：ACTIVE

---

## 一、协议概述

本协议实现SQLite持久化任务看板的一键Swarm工作流，支持DAG拓扑自动分解、多Worker并行执行、独立校验节点、结果合成节点的完整多Agent协作链路。对标Hermes v0.15.0的`hermes kanban swarm`命令，将多Agent从"一次性通信"升级为"持久化工作队列"。

## 二、核心架构

### 2.1 Swarm拓扑结构

```
hermes kanban swarm → 一键创建完整Swarm拓扑：

  Root (Orchestrator/协调者)
    ├── Worker A (并行执行) ────┐
    ├── Worker B (并行执行) ────┤
    ├── Worker C (并行执行) ────┘
    ↓ (Gate: 所有Worker完成)
  Gated Verifier (独立校验节点)
    ↓ (Gate: 校验通过)
  Gated Synthesizer (结果合成节点)
    ↓
  Shared Blackboard (共享结果黑板 → 所有Agent可读写)
```

### 2.2 数据库驱动协调

整个Swarm以SQLite数据库为单一协调原语：
- 每个任务是一行数据库记录
- CAS（Compare-And-Swap）并发控制保证原子认领
- 任务状态持久化：Agent重启/机器重启，任务不丢失
- 跨会话持久化：昨天的任务今天接着做

## 三、关键机制

### 3.1 Triage自动分解

用户在Triage（分诊板）中输入一句话需求，Orchestrator自动：
1. **拆解**：大目标拆为子任务依赖树
2. **指派**：根据Agent画像描述匹配最合适的角色
3. **链接依赖**：识别并行任务和串行依赖

### 3.2 Agent画像描述

```
角色配置示例：
  researcher: "适合做文献调研、数据分析、竞品对比，擅长读取和总结大量文本"
  code-worker: "适合做代码编写、调试、测试，擅长工程实现"
  reviewer: "适合做代码审查、安全审计、性能分析"

Orchestrator读取画像后精准匹配任务→Agent
不再靠名字猜测，而是有评估依据
```

### 3.3 Per-Task模型覆盖

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 简单样板代码 | GPT-5 Nano / 本地模型 | Token少，速度快 |
| 复杂算法实现 | Claude Sonnet 4.6 / GPT-5 | 需要强推理 |
| 代码审查 | Claude Opus 4.6 | 需要深度理解 |
| 文档生成 | GPT-5 / Gemini 2.5 Pro | 长上下文 |

### 3.4 定时调度

- 支持per-task scheduled start times
- 可配置Claim TTL（超时回收）
- 重试指纹（retry fingerprinting）
- 过期任务自动检测（stale-task detection）
- Respawn guards（防止无限重启）

### 3.5 Workspace隔离策略

| 策略 | 适用场景 | 隔离级别 |
|------|---------|---------|
| Scratch | 轻量临时任务 | 共享目录+文件名前缀 |
| Dir | 需要独立文件的任务 | 独立子目录 |
| Worktree | 需要git分支隔离 | 独立git worktree |

## 四、任务状态机

```
triage → todo → in_progress → review → done
                    ↓              ↓
                  failed ←── rejected
                    ↓
                  retry → todo
```

## 五、交互入口

1. **CLI**：`hermes kanban swarm` 一键创建
2. **Web Dashboard**：实时查看每个任务状态/历史/Agent间对话
3. **Agent Tools**：`/workers/active`、`/runs/{id}`、`/inspect` API

## 六、一次性委托 vs Kanban持久化

| 维度 | 一次性委托 | Kanban持久化 |
|------|-----------|-------------|
| 主进程阻塞 | 会 | 不会 |
| 子Agent崩溃恢复 | 不能 | 能（自动重试） |
| 人类中途介入 | 不行 | 随时 /unblock |
| 审计记录 | 丢失 | 永久SQL库 |
| 跨角色接力 | 不支持 | 天然支持 |
| 跨会话持久化 | 不支持 | 支持 |

## 七、豆包Agent适配方案

1. **底层存储**：SQLite数据库作为Swarm任务看板
2. **自动分解**：主Agent内置Triage能力，接收一句话需求自动拆解
3. **画像系统**：为File/Computer/App/Browser/Search五大子Agent配置能力画像
4. **模型分层**：低价值任务走端侧模型，高难度任务走云端模型
5. **隔离策略**：File操作走Dir隔离，系统操作走Scratch，代码生成走Worktree