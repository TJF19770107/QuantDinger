# 龙虾-Agent运行时恢复保障协议 v1.0

> **协议编号**：69
> **对标来源**：OpenClaw v2026.5.28 Agent Runtime Recovery
> **创建时间**：2026-06-01（R19）
> **版本**：v1.0

---

## 一、协议概述

本协议提取自OpenClaw v2026.5.28对Agent和Codex运行时恢复机制的系统性加固，确保在复杂Agent编排、运行中断恢复、超时终止、共享状态重启等场景中状态管理可控、不崩溃扩散。

---

## 二、四层恢复保障机制

### 第1层：工作区隔离

```
subagent_cwd ≠ workspace_root
subagent_files ≠ parent_workspace
```

- spawned agent的cwd和workspace与父Agent严格分离
- 崩溃后仅清理自身工作区，不污染父级
- ACP spawn attachments正确转发

### 第2层：锁生命周期管理

```
on_timeout_abort → release_all_session_locks()
on_runtime_teardown → release_live_locks()
on_cleanup → SKIP if lock held by live OpenClaw instance
```

- timeout abort时自动释放session锁
- 运行时清理过程不误删仍由活跃OpenClaw持有的锁
- 避免使用陈旧的restart continuation

### 第3层：共享状态隔离

```
Codex app-server failure → does NOT crash shared runtime
Codex helper failure → does NOT crash shared runtime
hook context → prompt-local (不扩散到全局)
```

- 单个运行时组件失败不拖垮整个共享状态
- hook上下文保持prompt-local，不污染全局命名空间
- exec abort listeners正确清理

### 第4层：增量恢复

```
stream assistant deltas incrementally
avoid session event queue self-wait
forward partial results on reconnect
```

- 中断后增量流式恢复而非全量重放
- 避免事件队列自等待死锁
- 重连时转发部分已完成结果

---

## 三、恢复状态机

```
NORMAL → TIMEOUT → [释放锁] → ABORT
                  → [保留live锁] → SKIP_CLEANUP

NORMAL → CRASH → [隔离工作区] → CLEANUP_OWN
               → [不拖垮共享] → PARENT_CONTINUE

NORMAL → RESTART → [丢弃陈旧continuation] → FRESH_START
                 → [转发已完成的attachments] → RESUME
```

---

## 四、适用场景

- 多Agent并行编排（百级subagent）
- 长时间运行Agent的崩溃恢复
- 共享运行时环境的多租户隔离
- 定时自动化任务的断点续传

## 五、关键约束

- 清理操作前必须验证锁持有者身份
- 不得使用超过30秒的陈旧restart continuation
- hook上下文永远保持prompt-local
- 共享运行时状态修改必须原子化