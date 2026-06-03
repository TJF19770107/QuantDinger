# 龙虾-多Agent协同看板协议 v1.0

> **创建时间**：2026-05-31
> **对标来源**：Hermes Agent SWARM v2.1 + Kanban v0.12.0
> **适用场景**：豆包Agent多Sub-Agent任务编排

---

## 一、协议概述

本协议定义豆包Agent的多Agent协同看板系统，实现任务的原子认领、并行执行、失败熔断与结果汇总。

## 二、核心架构

### 2.1 看板数据模型（SQLite）

```sql
CREATE TABLE kanban_tasks (
    id TEXT PRIMARY KEY,
    parent_id TEXT,           -- 父任务ID（支持依赖）
    status TEXT DEFAULT 'pending',  -- pending/claimed/running/done/failed/locked
    role TEXT,                -- 专家角色：researcher/coder/reviewer/analyst
    agent_id TEXT,            -- 认领的Agent进程ID
    payload TEXT,             -- 任务描述JSON
    summary TEXT,             -- 执行摘要
    tool_trace TEXT,          -- 工具调用轨迹
    token_cost INTEGER,       -- Token消耗
    fail_count INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    claimed_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

### 2.2 原子认领协议

```sql
-- 原子认领：只有一个Agent能拿到任务
BEGIN TRANSACTION;
UPDATE kanban_tasks 
SET status='claimed', agent_id=?, claimed_at=CURRENT_TIMESTAMP
WHERE id=? AND status='pending';
COMMIT;
```

### 2.3 熔断机制

- 单个任务连续失败3次 → 状态变为 `locked`，等待人工介入
- Agent进程崩溃/超时 → 调度器检测进程存活，自动回收任务重新分配
- 调度器心跳间隔：30s

## 三、协作模式

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| Fan-Out | 一个父任务扇出N个并行子任务 | 批量文件处理、并行搜索 |
| Pipeline | 任务链式传递，上游输出→下游输入 | 数据处理流水线 |
| Voting | 多个Agent独立执行，投票仲裁 | 代码审查、方案评审 |
| Human-in-Loop | 关键节点暂停等待人工审批 | 支付、删除、安全操作 |
| Orchestrator+Worker | 主Agent拆任务+汇总，Worker执行 | 复杂多步骤任务 |
| Supervisor+Subagent | 主Agent审核，子Agent执行 | 质量把关场景 |
| Expert Roles | 不同Agent配置不同专业工具集 | 跨领域综合分析 |
| Parallel Research | 多个Research Agent并行检索 | 信息密集调研 |

## 四、Agent注册规范

```json
{
  "agent_id": "doubao-coder-01",
  "role": "coder",
  "capabilities": ["code_generation", "refactoring", "testing"],
  "tools": ["shell_executor", "python_executor", "read_text", "write_file"],
  "model": "default",
  "max_iterations": 50,
  "crash_recovery": true
}
```

## 五、豆包Sub-Agent池规划

| Agent | 角色 | 对标 | 优先级 |
|-------|------|------|--------|
| Code Agent | 编码/重构/测试 | Codex + OpenCode | P0 |
| File Agent | 文件搜索/转换/整理 | Marvis File Agent | P0 |
| Search Agent | 深度搜索/调研 | Marvis Search Agent | P1 |
| Memory Agent | 长期记忆/知识图谱 | Hermes Memory | P1 |
| Gateway Agent | 多渠道消息/API网关 | OpenClaw Gateway | P1 |
| Review Agent | 代码审查/质量把关 | Claude Reviewer | P1 |
| Orchestrator Agent | 任务拆解/编排/汇总 | Hermes SWARM Orch | P0 |
| Evolution Agent | Skill提取/自我优化 | HyperAgents Meta | P2 |

---

> 版本：v1.0 | 状态：待部署 | 下一版：集成Kanban SQLite实现