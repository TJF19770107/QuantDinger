# AONP 豆包桥接协议 v3.0 设计方案

> **基于**：AONP 五协议框架 (MWC 2026 · 中国移动)
> **对标**：SRMP / M2TP / AIDP / SMIP / A2P + AGW
> **目标**：豆包Agent双向桥接协议从 JSON v2.0 升级为 AONP 简化兼容层
> **版本**：v3.0 Draft

---

## 一、协议栈总览

```
豆包桥接协议 v3.0 = AONP 简化兼容层

┌─────────────────────────────────────────────────────────┐
│                    应用层（用户/Marvis/其他Agent）        │
├─────────────────────────────────────────────────────────┤
│ SRMP层    │ 语义路由 + 意图解析 + 多Agent组播           │
│           │ 实现：Orchestrator Chat + delegate_task     │
├───────────┼─────────────────────────────────────────────┤
│ M2TP层    │ 多模态传输 + 分片 + 中继加速                 │
│           │ 实现：JSON → 分片 → QUIC/TCP自适应           │
├───────────┼─────────────────────────────────────────────┤
│ AIDP层    │ Agent/工具跨域发现 + 动态注册                │
│           │ 实现：能力注册中心 + DNS-SD                   │
├───────────┼─────────────────────────────────────────────┤
│ SMIP层    │ 会话管理 + 异步调用状态机                    │
│           │ 实现：Durable Task模式持久化会话              │
├───────────┼─────────────────────────────────────────────┤
│ A2P层     │ 授权访问 + 令牌缓存 + 细粒度权限              │
│           │ 实现：SafeGuard v3.0 + OAuth2.0              │
├───────────┼─────────────────────────────────────────────┤
│ AGW层     │ 网关核心 + 注册+认证+代理+管控               │
│           │ 实现：「1+4+N」模块架构                       │
└───────────┴─────────────────────────────────────────────┘
```

## 二、各层设计详案

### 2.1 SRMP 语义路由层

```json
{
  "SRMP": {
    "version": "1.0",
    "message_type": "task_delegation | multicast | route_query",
    "source": {
      "agent_id": "lobster_master",
      "capability_tags": ["orchestration", "task_decomposition"]
    },
    "target": {
      "intent": "file_operation | code_generation | web_search | app_control",
      "required_capabilities": ["file_read", "text_search"],
      "preferred_agent": "doubao_file_agent"
    },
    "routing": {
      "strategy": "capability_match | load_balance | least_latency",
      "fallback": ["doubao_generic_agent", "external_openclaw"],
      "timeout_ms": 30000
    },
    "payload": {},
    "trace": {
      "correlation_id": "uuid",
      "span_id": "uuid",
      "parent_span_id": null,
      "timestamp": "ISO8601"
    }
  }
}
```

### 2.2 M2TP 多模态传输层

| 特性 | 实现方案 | 对标AONP |
|------|---------|---------|
| 分片传输 | 大于1MB消息自动分片，每片64KB | M2TP分片机制 |
| 中继加速 | 共享内存 + Unix Socket（同机）/ QUIC（跨机） | 中继加速 |
| 协议转换 | JSON ↔ Protocol Buffers ↔ MessagePack | TCP/QUIC/MoQ转换 |
| 压缩 | zstd 压缩（文本3:1，二进制1.2:1） | 效率提升 |
| 重传 | 选择性重传 + FEC前向纠错 | 稳定性 |

```
M2TP消息格式：
┌────────────┬──────────┬──────────┬──────────────┐
│  Header    │ 分片索引  │  总数     │  Payload     │
│  16 bytes  │  4 bytes │  4 bytes │  最多64KB     │
│  msg_id    │  seq_no  │  total   │  zstd压缩     │
│  msg_type  │          │          │               │
│  timestamp │          │          │               │
└────────────┴──────────┴──────────┴──────────────┘
```

### 2.3 AIDP 跨域发现层

```
能力注册中心（对标 AIDP DNS扩展）

capability_registry/
├── agents/
│   ├── doubao_file_agent.json     # Agent能力描述
│   ├── doubao_computer_agent.json
│   └── ...
├── tools/
│   ├── web_search.json             # 工具能力描述
│   ├── python_executor.json
│   └── ...
└── discovery/
    ├── dns_records.json            # DNS-SD记录
    └── multicast_groups.json       # 组播组
```

Agent能力描述：
```json
{
  "agent": {
    "id": "doubao_file_agent",
    "type": "file",
    "capabilities": ["read", "write", "search", "convert", "organize"],
    "supported_formats": ["txt", "md", "pdf", "docx", "xlsx", "png", "jpg"],
    "max_file_size_mb": 500,
    "endpoints": {
      "task": "doubao://local/file/task",
      "status": "doubao://local/file/status",
      "health": "doubao://local/file/health"
    },
    "cost": {
      "read": 0.001,
      "write": 0.002,
      "search": 0.005
    },
    "ttl_seconds": 3600
  }
}
```

### 2.4 SMIP 会话管理层

```
会话状态机（对标 SMIP 异步调用）

States:
  CREATED → QUEUED → DISPATCHED → RUNNING → 
    ├─ COMPLETED
    ├─ FAILED → RETRYING → RUNNING
    ├─ WAITING_HUMAN → CONFIRMED → RUNNING
    └─ TIMEOUT → FAILED

Transitions:
  CREATED: 任务创建，入队
  QUEUED: 等待调度
  DISPATCHED: 已分配给Agent
  RUNNING: Agent正在执行
  COMPLETED: 成功完成
  FAILED: 执行失败（可重试）
  RETRYING: 正在重试（最多3次）
  WAITING_HUMAN: 等待用户确认
  CONFIRMED: 用户已确认
  TIMEOUT: 超时未完成
```

### 2.5 A2P 授权访问层

对标A2P的令牌管理，在 SafeGuard v3.0 基础上增加：

| 特性 | 实现 | 对标A2P |
|------|------|---------|
| 令牌缓存 | Redis/LRU内存缓存，TTL 15分钟 | 令牌缓存 |
| 批量授权 | 单次请求最多10个权限，原子授权 | 批量请求 |
| 细粒度权限 | r/w/x 三级，按Agent+工具细分 | 细粒度权限 |
| 令牌刷新 | Refresh Token + 滑动窗口 | 客户端解耦 |
| 审计日志 | 每次授权操作写入审计日志 | 安全防线 |

### 2.6 AGW 网关层

```
豆包AGW = 「1+4+N」模块（对标 AONP AGW）

┌────────────────────────────────────────────┐
│           1 网关核心交互入口                  │
│   ┌──────────────────────────────────┐    │
│   │  REST API / WebSocket / gRPC     │    │
│   │  统一认证 + 限流 + 负载均衡        │    │
│   └──────────────────────────────────┘    │
├────────────────────────────────────────────┤
│           4 大管控模块                       │
│   ┌──────────┬──────────┬──────────┬────┐ │
│   │注册管理   │认证授权   │消息代理   │行为│ │
│   │          │          │          │管控│ │
│   │Agent注册 │OAuth2.0  │Pub/Sub   │规则│ │
│   │工具注册   │JWT/TLS   │消息队列   │引擎│ │
│   │心跳检测   │RBAC      │死信队列   │审计│ │
│   │健康检查   │API Key   │消息持久化 │限流│ │
│   └──────────┴──────────┴──────────┴────┘ │
├────────────────────────────────────────────┤
│           N 个分布式AGW转发组件               │
│   跨机转发 · 协议转换 · 负载均衡 · 缓存      │
└────────────────────────────────────────────┘
```

---

## 三、实施路线

| 阶段 | 范围 | 产出 | 耗时 |
|------|------|------|------|
| v3.0-alpha | SRMP路由 + SMIP会话 | 核心通信 + 状态管理 | R08-R09 |
| v3.0-beta | AIDP发现 + A2P授权 | 动态发现 + 安全管理 | R10-R11 |
| v3.0-rc | M2TP传输 + AGW网关 | 完整传输 + 网关 | R12-R13 |
| v3.0-stable | 全协议联调 + 压测 | 生产就绪 | R14 |

---

> 创建时间：2026-05-31 17:00
> 状态：设计完成 · 待编码实现