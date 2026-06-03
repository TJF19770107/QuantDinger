# 龙虾-Lead-Specialist多Agent推理分发协议 v1.0

> **对标来源**：Claude Managed Agents Multiagent Sessions (2026-05-06)
> **版本**：v1.0
> **状态**：ACTIVE
> **所属模块**：Claude推理引擎 → Phase 4 方案执行
> **创建**：2026-05-31 R07

---

## 一、协议目标

将Claude Managed Agents的Lead-Specialist架构融入豆包Agent推理引擎的"方案执行"阶段，实现多Agent并行推理分发，解决单Agent上下文窗口瓶颈和模型成本优化问题。

---

## 二、核心架构

```
用户请求
    │
    ▼
┌─────────────────────────────────────┐
│         Lead Agent (推理引擎)         │
│  ├─ 问题解析 + 条件拆解 + 逻辑推演    │
│  ├─ 任务分解 → Specialist分配决策     │
│  └─ 结果汇总 + 一致性检查             │
└──────┬──────────┬──────────┬────────┘
       │          │          │
   ┌───▼───┐  ┌──▼────┐  ┌──▼──────┐
   │Research│  │ Code  │  │ Review  │
   │  Specialist│ Specialist│ Specialist│
   │  (搜索) │  (编码) │  (审查)   │
   └───┬───┘  └──┬────┘  └──┬──────┘
       │          │          │
       └──────────┼──────────┘
                  ▼
        Shared Filesystem
        /mnt/shared/ (集成面)
                  │
        Persistent Event Log
        (可回溯、可审计)
```

---

## 三、Lead Agent决策规则

### 3.1 分发策略

| 策略 | 触发条件 | 行为 |
|------|---------|------|
| BROADCAST | 任务可并行无依赖 | 同时分发所有Specialist，结果汇总 |
| PIPELINE | 存在上下游依赖 | 串行分发，上游输出→下游输入 |
| COMPETE | 需要多方案对比 | 多Specialist并行执行同一任务，择优 |
| DELEGATE | 简单子任务 | 指定单一Specialist执行，Lead仅等待 |

### 3.2 模型混合调度

| 角色 | 推荐模型 | 理由 |
|------|---------|------|
| Lead Agent | 高性能模型 | 需要强推理+决策能力 |
| Research Specialist | 中等模型 | 搜索+摘要，Token消耗大 |
| Code Specialist | 高性能模型 | 代码生成需要精度 |
| Review Specialist | 轻量模型 | 审查只需比对+判断，成本敏感 |

### 3.3 Shared Filesystem路径约定

```
/mnt/shared/
├── research/     # Research Specialist 输出
├── code/         # Code Specialist 输出
├── review/       # Review Specialist 输出
├── artifacts/    # 中间产物
└── final/        # 最终交付物
```

---

## 四、Persistent Event Memory

### 4.1 事件记录格式

```json
{
  "event_id": "ls_20260531_214500_a1b2",
  "session_id": "sess_R07_003",
  "agent_role": "code_specialist",
  "action": "tool_call",
  "tool": "read_file",
  "input": { "path": "/mnt/shared/research/context.md" },
  "output_snippet": "前256字符...",
  "duration_ms": 340,
  "status": "success",
  "timestamp": "2026-05-31T21:45:00"
}
```

### 4.2 回溯能力

- Lead Agent可查询任意Specialist的完整执行历史
- 调试时按 `session_id` + `agent_role` 过滤
- Console展示完整Agent树（哪个Agent何时触发什么）

---

## 五、集成到推理引擎

### 5.1 增强Phase 4

原有Phase 4"方案执行"为单Agent线性执行。集成后：

```
Phase 3 逻辑推演结束
    │
    ▼
Lead Agent 任务分解 ──→ Specialist分配
    │                        │
    ├─ Research Specialist ──┤
    ├─ Code Specialist ──────┤  并行执行
    └─ Review Specialist ────┘
                    │
            Shared Filesystem 汇总
                    │
            Lead Agent 一致性检查
                    │
            Phase 5 结果复盘
```

### 5.2 触发条件

- 任务Token估算 > 单Agent上下文窗口的60%
- 任务包含明确可并行子任务（搜索+编码+审查）
- 用户明确要求多方案对比

---

## 六、性能指标

| 指标 | 单Agent模式 | Lead-Specialist模式 | 提升 |
|------|------------|-------------------|------|
| 复杂任务吞吐量 | 1x | 2.5-3.5x | 并行红利 |
| 上下文窗口利用率 | ~60% | ~90% | 分工减少浪费 |
| 模型成本 | 全量高性能 | 混合降本30-50% | 按需分配 |
| 失败恢复时间 | 全量重跑 | 单Specialist重跑 | 隔离失败 |

---

> 版本：v1.0 (R07)
> 下一版本：v2.0 增加Agent健康评分 + 动态权重调整
