# Agent-Mailbox通信协议 v1.0

**对标来源**: Claude Agent Teams (Anthropic 2026)  
**创建日期**: 2026-05-31  
**类别**: Agent协同  
**优先级**: P0  
**关联技能**: AgentIter, HermesAgent

---

## 一、协议概述

Agent-Mailbox是豆包Agent内部的多Agent消息队列通信协议，对标Claude Code的Agent Teams Mailbox机制。用于在Lead Agent与子Agent之间、以及子Agent之间建立异步消息通道。

## 二、核心概念

### 2.1 角色定义

| 角色 | 职责 |
|------|------|
| **Lead Agent** | 全局任务分解、调度、监控、结果汇总 |
| **Worker Agent** | 执行具体子任务，通过Mailbox接收任务、回传结果 |
| **Mailbox** | 消息中枢，管理所有Agent间的消息队列 |

### 2.2 消息类型

| 类型 | 方向 | 说明 |
|------|------|------|
| `task_dispatch` | Lead → Worker | 任务派发 |
| `task_result` | Worker → Lead | 任务结果回传 |
| `task_status` | Worker → Lead | 状态更新 (进度/阻塞) |
| `dependency_notify` | Worker → Worker | 依赖就绪通知 |
| `broadcast` | Any → All | 全局广播 |
| `heartbeat` | Worker → Lead | 心跳保活 |

## 三、消息格式

```json
{
  "protocol": "doubao-mailbox-v1",
  "message_id": "msg_{uuid}",
  "timestamp": "ISO8601",
  "from": "agent_id",
  "to": "agent_id | broadcast",
  "type": "task_dispatch | task_result | ...",
  "priority": "high | medium | low",
  "dependency": ["msg_id_1", "msg_id_2"],
  "ttl": 300,
  "payload": {},
  "callback_topic": "mailbox://{agent_id}/response"
}
```

## 四、通信流程

### 4.1 任务派发

```
Lead Agent
    │ task_dispatch → Mailbox
    │                    │
    │                    └→ Worker Agent Queue
    │                          │
    │   ← task_result ────────┘
```

### 4.2 依赖通知

```
Worker A (完成)
    │ dependency_notify → Mailbox
    │                        │
    │                        └→ Worker B Queue (等待中)
    │                              │
    │                              └→ 开始执行
```

## 五、实现要点

1. **异步队列**: 使用asyncio.Queue，非阻塞通信
2. **超时机制**: 消息30秒超时，超时触发重试或降级
3. **持久化**: 关键消息写入SQLite，Agent重启不丢失
4. **优先级**: 支持高/中/低三级优先级调度
5. **去重**: 基于message_id去重
