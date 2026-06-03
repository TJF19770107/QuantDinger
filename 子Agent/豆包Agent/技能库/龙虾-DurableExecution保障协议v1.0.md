# 龙虾-DurableExecution保障协议 v1.0

> **对标来源**：Temporal Durable Workflow Engine
> **版本**：v1.0
> **状态**：ACTIVE
> **所属模块**：可视化工作流引擎 → 执行引擎增强
> **创建**：2026-05-31 R07

---

## 一、协议目标

将Temporal的Durable Execution模型融入可视化工作流引擎v2.0，补全"进程级容错"缺口。从应用层超时熔断升级为系统级持久化保障，确保长时间运行的工作流在进程崩溃/重启后精确恢复。

---

## 二、核心概念

### 2.1 Durable Execution vs 普通执行

| 维度 | 普通执行 | Durable Execution |
|------|---------|-------------------|
| 进程崩溃 | 任务丢失，需从头重跑 | 从最近Checkpoint恢复 |
| 执行保证 | Best-effort | Exactly-Once（精确一次） |
| 状态持久化 | 无 | 每次节点执行前后自动Checkpoint |
| 运行时长 | 分钟级 | 小时/天级 |
| 恢复时间 | 全量重跑 | <1s 恢复至断点 |

### 2.2 Exactly-Once语义

工作流中每个节点的执行保证精确一次完成——即使进程在执行中途崩溃，恢复后也不会重复执行已完成节点，也不会遗漏未执行节点。

---

## 三、Checkpoint机制

### 3.1 Checkpoint触发时机

```
节点N开始 → [Checkpoint: N_START] → 节点N执行 → [Checkpoint: N_END] → 节点N+1开始
```

### 3.2 Checkpoint内容

```json
{
  "checkpoint_id": "cp_wf_R07_003_node_004",
  "workflow_id": "wf_R07_003",
  "node_id": "action_generate_report",
  "phase": "END",
  "timestamp": "2026-05-31T21:45:00",
  "state_snapshot": {
    "variables": { "report_dir": "/output/R07/", "template": "standard" },
    "node_output_hash": "sha256:a1b2c3...",
    "downstream_queue": ["node_005", "node_006"]
  },
  "position": { "node_index": 4, "total_nodes": 7 }
}
```

### 3.3 Checkpoint存储

| 层级 | 位置 | 持久化方式 | 延迟 |
|------|------|-----------|------|
| 本地 | 工作目录/checkpoints/ | 文件系统 | <5ms |
| 持久化 | SQLite/JSON | 磁盘确认写入 | <20ms |

---

## 四、恢复流程

```
进程崩溃/重启
    │
    ▼
工作流引擎启动 → 扫描checkpoints/目录
    │
    ▼
定位最近有效Checkpoint (按workflow_id + timestamp排序)
    │
    ├─ 找到 N_END checkpoint → 从 N+1 开始
    ├─ 找到 N_START checkpoint → 重新执行 N（可能未完成）
    └─ 未找到 → 从头开始
    │
    ▼
加载state_snapshot → 恢复变量 → 继续执行
```

---

## 五、重试策略DSL

### 5.1 定义

```yaml
retry_policy:
  node_id: "action_api_call"
  max_attempts: 5
  backoff:
    type: exponential       # exponential | fixed | linear
    initial_interval: 1s
    max_interval: 60s
    multiplier: 2.0
  non_retryable_errors:     # 不可重试的错误类型
    - "AUTH_FAILED"
    - "INVALID_INPUT"
    - "RESOURCE_NOT_FOUND"
  timeout_per_attempt: 30s
```

### 5.2 重试决策树

```
节点失败
  ├─ 错误类型 ∈ non_retryable → 直接标记FAILED，不重试
  ├─ 重试次数 ≥ max_attempts → 标记FAILED，触发降级
  └─ 其他 → 等待backoff间隔 → 重试
```

---

## 六、与现有v2.0引擎融合

### 6.1 分层容错体系

```
┌─────────────────────────────────────────┐
│         应用层：超时熔断 + 降级 (v2.0)     │  ← 已有
├─────────────────────────────────────────┤
│         系统层：Durable Execution (R07)   │  ← 新增
│   Checkpoint持久化 + Exactly-Once + 恢复  │
└─────────────────────────────────────────┘
```

### 6.2 融合后执行流程

```
节点开始
  │
  ├─ [新增] 写 Checkpoint (START)
  │
  ├─ 执行节点逻辑
  │   ├─ 正常完成 → [新增] 写 Checkpoint (END)
  │   ├─ 超时 → [v2.0] 重试(最多3次)
  │   │   └─ 重试失败 → [v2.0] 降级策略
  │   └─ 进程崩溃 → [新增] 下次启动自动恢复
  │
  └─ 结果传递
```

---

## 七、适用场景

| 场景 | 是否启用 | 理由 |
|------|---------|------|
| 长时间数据迁移 | ✅ 必须 | 小时级运行，崩溃不可接受 |
| 批量文件处理 | ✅ 强烈建议 | 部分完成可恢复 |
| 多Agent复杂编排 | ✅ 建议 | Agent调用不稳定 |
| API聚合查询 | ⚠️ 可选 | 秒级完成，Checkpoint开销大于重跑 |
| 实时对话推理 | ❌ 不适用 | 毫秒级，无需持久化 |

---

> 版本：v1.0 (R07)
> 下一版本：v2.0 分布式Checkpoint + 多引擎协同恢复
