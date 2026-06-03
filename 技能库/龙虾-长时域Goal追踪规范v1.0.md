# 龙虾-长时域Goal追踪规范 v1.0

> **创建时间**：2026-05-31
> **对标来源**：OpenAI Codex /goal (CLI 0.128.0+, 2026-05)
> **核心能力**：跨会话、跨中断、跨预算的持久化目标追踪
> **适用场景**：马拉松式开发任务、多日项目、无人值守全自动Agent

---

## 一、/goal 机制原理

### 1.1 Codex原始设计

```
/goal 命令 → 目标存入数据库（持久化记录）
     ↓
Agent 持续追踪该目标
     ↓
支持生命周期管理：
  create → running → pause → resume → complete
                              ↓
                          budget exhausted → 软停止
                          session terminated → 下次自动恢复
```

### 1.2 关键特性

| 特性 | 说明 |
|------|------|
| 跨会话存活 | 关闭终端再打开，目标继续执行 |
| 跨中断恢复 | 网络断连/进程崩溃后自动恢复 |
| 预算软停止 | Token预算耗尽时暂停，预算恢复后继续 |
| 进度持久化 | 已完成/未完成子任务全部记录 |
| TUI控制面板 | /goal pause / resume / clear / list |

### 1.3 真实验证案例

```
用户："把 backlog.md 里的 18 个特性全干完"
↓
Codex 自动：
  1. 解析 backlog.md → 18个任务
  2. 逐个执行
  3. 完成14/18（78%完成率）
  4. 自动开PR + 自审代码 + 跑通CI
  5. 用户第二天醒来看到结果
```

## 二、豆包Goal实现方案

### 2.1 数据模型

```sql
CREATE TABLE goals (
    id TEXT PRIMARY KEY,
    user_prompt TEXT,           -- 用户原始目标
    parsed_tasks TEXT,          -- 拆解后的子任务JSON
    status TEXT DEFAULT 'created',  -- created/running/paused/completed/failed
    progress JSON,              -- {total:18, done:14, current:15}
    total_budget INTEGER,       -- 总Token预算
    used_budget INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    session_id TEXT             -- 绑定会话（支持跨会话恢复）
);

CREATE TABLE goal_checkpoints (
    id TEXT PRIMARY KEY,
    goal_id TEXT,
    snapshot TEXT,              -- 当前状态快照（文件diff、完成列表等）
    created_at TIMESTAMP
);
```

### 2.2 生命周期状态机

```
                    ┌─────────┐
           create → │ created │
                    └────┬────┘
                         │ start
                    ┌────▼────┐
              ┌─────│ running │─────┐
              │     └────┬────┘     │
              │ pause    │          │ budget exhaust
         ┌────▼───┐     │     ┌────▼──────┐
         │ paused │     │     │ soft_stop  │
         └────┬───┘     │     └─────┬──────┘
              │ resume   │          │ budget restored
              └────┐     │     ┌────▼───┐
                   │     │     │ running │ (resume)
                   │     │     └─────────┘
                   │  complete
              ┌────▼─────┐
              │ completed │
              └──────────┘
```

### 2.3 豆包./goal 命令设计

```
./goal <目标描述>
    创建并启动一个持久化目标

./goal pause
    暂停当前目标

./goal resume [goal_id]
    恢复指定目标（默认恢复最近目标）

./goal list
    列出所有目标及状态

./goal status [goal_id]
    查看目标详细进度

./goal clear [goal_id]
    清除已完成/已放弃的目标
```

### 2.4 自动恢复机制

```
1. Agent 启动时检查 goals 表
2. 如果有 status=running 或 paused 的目标
3. 自动加载最近checkpoint
4. 提示用户是否继续执行
5. 用户确认后自动恢复
```

---

> 版本：v1.0 | 状态：规范定义 | 实现优先级：Phase 1 | 实现周期：1-2天