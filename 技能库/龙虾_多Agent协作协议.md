# 龙虾_多Agent协作协议 v2.4

> **版本**：v2.4（R06升级）
> **来源**：Marvis Workbody + Hermes SWARM
> **类型**：核心升级 · 多Agent协作
> **升级日期**：2026-05-31（R06）

---

## 一、v2.3 → v2.4 变更摘要

| 维度 | v2.3 | v2.4 |
|------|------|------|
| 协作模式 | 固定分工 | 弹性编排+确定性分工 |
| Agent数量 | 6个 | 无限（按需创建） |
| 任务管理 | 隐式 | 看板式 (借鉴Hermes Kanban) |
| 记忆共享 | 无 | 三层记忆系统 |
| 异常处理 | 基础 | 自动重试+降级+人工介入 |

## 二、v2.4 协作模式

### 模式1：确定性分工（Marvis哲学）

```
PM Agent ──→ File Agent    (所有文件操作)
        ──→ Computer Agent (所有系统操作)
        ──→ App Agent      (所有应用操作)
        ──→ Browser Agent  (所有网页操作)
        ──→ Search Agent   (所有搜索操作)
```

优点：职责清晰，不会出现Agent冲突。

### 模式2：弹性编排（Hermes哲学）

```
PM Agent ──→ Worker-1 (临时创建：处理发票整理)
        ──→ Worker-2 (临时创建：处理合同审查)
        ──→ Worker-3 (临时创建：处理数据报表)
```

优点：灵活扩展，复杂任务自动拆解。

### 模式3：混合模式（R07目标）

```
PM Agent ──→ 确定性Agent (File/Computer/App/Browser/Search)
        ──→ 弹性Worker   (按需创建，处理专业子任务)
        ──→ 审查Agent    (质量检查+异常处理)
```

## 三、Agent生命周期

```
创建 ──→ 初始化 ──→ 执行 ──→ 完成
  │        │         │         │
  │        │         │         └──→ 结果摘要返回PM
  │        │         │
  │        │         └──→ 异常 ──→ 重试(最多3次) ──→ 降级 ──→ 人工介入
  │        │
  │        └──→ 超时(5分钟) ──→ 强制终止 + 部分结果返回
  │
  └──→ 资源不足 ──→ 排队等待 + 通知PM
```

## 四、通信协议

### PM → Worker (任务派发)

```json
{
  "task_id": "uuid",
  "task_type": "file_operation | system_config | web_scrape | code_gen | search",
  "task_description": "目标导向描述",
  "context": {
    "relevant_files": [],
    "relevant_memory": [],
    "constraints": ["不修改系统配置", "只读操作"]
  },
  "budget": {
    "max_iterations": 10,
    "max_tokens": 50000,
    "timeout_seconds": 300
  }
}
```

### Worker → PM (结果返回)

```json
{
  "task_id": "uuid",
  "status": "success | partial | failed | timeout",
  "summary": "一句话摘要",
  "result": {},
  "usage": {
    "iterations": 3,
    "tokens": 12000,
    "duration_seconds": 45
  },
  "tool_trace": ["read_file", "analyze", "write_file"],
  "artifacts": ["path/to/output/file"]
}
```

## 五、并行调度规则

| 条件 | 行为 |
|------|------|
| 子任务无依赖 | 并行派发（最多5个） |
| 子任务有依赖(A→B) | 先执行A，A完成后执行B |
| 子任务不确定 | 最保守串行执行 |
| Worker超时 | 取部分结果，通知用户 |
| Worker异常 | 自动重试1次，仍失败则降级 |

---

> 版本历史：v1.0 (R01) → v2.0 (R03) → v2.3 (R05) → **v2.4 (R06)**