# 龙虾-Gateway性能优化手册 v1.0

> **创建时间**：2026-05-31
> **对标来源**：OpenClaw Gateway v2026.5.22 — /v1/models 接口 20s → 5ms (4100x)
> **适用场景**：豆包Agent的Sub-Agent池、工具Schema、模型列表的性能优化

---

## 一、OpenClaw Gateway优化拆解

### 1.1 4100x 性能飞跃的三大技术

| 技术 | 优化前 | 优化后 | 倍数 |
|------|--------|--------|------|
| Provider Auth-State预热 | 每次调用全量发现providers (~20s) | 启动时预缓存映射表 (~5ms) | **4100x** |
| 增量内存索引 | 全量扫描文件系统索引 | 仅索引变更文件 | **3-5x** |
| 启动成本归因 | 黑盒启动，无法定位瓶颈 | benchmark工具逐段计时 | **调试效率10x** |

### 1.2 预热机制详解

```
启动阶段（一次性）：
  1. 遍历所有provider插件的auth-state
  2. 构建 provider_id → capabilities 映射表
  3. 缓存到进程内存

运行时（每次请求）：
  /v1/models → 直接读内存映射表 → 返回
  (不再触发provider发现 + CLI调用)
```

## 二、豆包Agent可借鉴优化

### 2.1 Sub-Agent池预热

```
启动时：
  ┌──────────────────────────────────┐
  │ 预创建一个Sub-Agent池（热备）      │
  │                                  │
  │ Code-Agent    → idle, ready      │
  │ File-Agent    → idle, ready      │
  │ Search-Agent  → idle, ready      │
  │ Memory-Agent  → idle, ready      │
  │ Review-Agent  → idle, ready      │
  └──────────────────────────────────┘

运行时：
  任务派发 → 直接取热备Agent → 执行
  (跳过创建耗时，首响应降低 80%+)
```

### 2.2 工具Schema缓存

```
首次加载 → 全量工具Schema → 缓存到内存
后续调用 → 直接读缓存 → 不再重复解析

多轮对话中：
  只发送增量Schema（新增工具）
  而不是每次都发送全部Schema
```

### 2.3 MCP/插件发现结果缓存

```
启动时：
  - 扫描所有MCP server → 缓存server列表 + 工具列表
  - 扫描所有Skill → 缓存Skill注册表

运行时：
  - 工具列表查询 → 直接读缓存
  - 新增MCP server → 增量更新缓存（不触发全量扫描）
```

### 2.4 模型列表/Provider列表预热

```
豆包当前：每次请求 → 发现可用模型 → 延迟 ~N秒

优化后：启动时预缓存模型列表 → 请求时直接返回 → 延迟 ~ms
```

## 三、性能优化清单

| # | 优化项 | 预期提升 | 实现难度 | 优先级 |
|---|--------|---------|---------|--------|
| 1 | Sub-Agent池预热 | 首响应 -80% | 中 | P0 |
| 2 | 工具Schema缓存 | 对话Token -30% | 低 | P0 |
| 3 | MCP服务发现缓存 | 工具列表查询 -95% | 低 | P1 |
| 4 | 模型列表预热 | 模型查询 -95% | 低 | P1 |
| 5 | Skill库增量索引 | 启动时间 -60% | 中 | P2 |
| 6 | 上下文分层记忆 | 对话Token -40% | 高 | P1 |
| 7 | 并行工具调用优化 | 工具执行 -50% | 中 | P2 |

## 四、性能基准与监控

### 4.1 关键指标

| 指标 | 当前基线 | 优化目标 |
|------|---------|---------|
| Sub-Agent创建延迟 | ~2s | ~200ms |
| 工具列表查询延迟 | ~1s | ~5ms |
| 模型列表查询延迟 | ~1s | ~5ms |
| 启动首响应时间 | ~5s | ~1s |
| 多轮对话Token浪费率 | ~35% | ~10% |
| Skill库加载时间 | ~3s | ~1s |

### 4.2 监控埋点

```python
# 启动阶段计时
startup_timeline = {
    "agent_pool_warmup": 0,
    "tool_schema_cache": 0,
    "mcp_discovery": 0,
    "model_list_cache": 0,
    "skill_index": 0
}

# 运行时延迟采样
runtime_latency = {
    "dispatch_task": [],     # p50/p95/p99
    "tool_execute": [],
    "skill_trigger": [],
    "memory_query": []
}
```

## 五、OpenClaw 其他可借鉴特性

| 特性 | OpenClaw实现 | 豆包可借鉴 |
|------|-------------|-----------|
| Per-Sender Tool Policies | 按用户/群组限制工具 | 按Sub-Agent角色限制工具集 |
| Plugin SDK统一目录 | text/image/video/music四类provider | Skill统一注册表 |
| Cron Inspection API | 单任务查看/调试 | Goal进度查看/调试 |
| 明文密钥告警 | openclaw doctor检测 | 配置文件安全检查 |
| WebSocket实时推送 | Dashboard实时事件 | Sub-Agent执行日志实时推送 |

---

> 版本：v1.0 | 状态：规范定义 | 实现优先级：P0项近期投入 (Sub-Agent池预热 + Schema缓存)