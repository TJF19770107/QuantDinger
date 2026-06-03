# Agent联邦发现协议 v1.0

> **创建时间**：2026-05-31 R06
> **对标来源**：Google A2A v1.2 (2026-03) · Linux Foundation AAIF
> **类型**：协调层 · 跨Agent通信
> **状态**：ACTIVE

---

## 一、协议目标

为豆包Agent提供标准化对外能力声明（AgentCard）和跨Agent任务委托机制，实现多Agent联邦发现与协作。

---

## 二、MCP vs A2A：双层模型

```
┌─────────────────────────────────┐
│  多Agent 系统                    │
│  Agent A  ◄── A2A ──►  Agent B  │  ← Agent 之间：用 A2A
│    │                        │    │
│   MCP                      MCP   │  ← Agent 到工具：用 MCP
│    │                        │    │
│  数据库  API  文件  搜索引擎     │
└─────────────────────────────────┘
```

| 维度 | MCP | A2A |
|------|-----|-----|
| 解决什么 | Agent 怎么调工具 | Agent 怎么委托另一个 Agent |
| 类比 | USB接口（连接外设） | HTTP协议（服务间通信） |
| 交互模式 | 无状态请求/响应 | 有状态长任务 |
| 对方可见性 | Server 对 Agent 透明 | Agent 是黑盒，有自己"想法" |
| 规范维护 | Anthropic | Linux Foundation |

---

## 三、AgentCard：Agent 的"简历"

### 3.1 发现端点

```
GET /.well-known/agent-card.json
```

无需中心注册表，通过标准化端点自发现。

### 3.2 AgentCard Schema

```json
{
  "name": "doubao-agent",
  "description": "豆包全域Agent — 编码/自进化/多Agent协同/桌面控制",
  "url": "http://localhost:11435",
  "provider": {
    "organization": "LobsterAI",
    "url": "https://lobsterai.local"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "defaultInputModes": ["text", "file"],
  "defaultOutputModes": ["text", "file"],
  "skills": [
    {
      "id": "code_generation",
      "name": "代码生成",
      "description": "全栈代码生成、重构、迁移",
      "tags": ["coding", "typescript", "python", "refactor"]
    },
    {
      "id": "self_evolution",
      "name": "自进化",
      "description": "自主技能创建、经验沉淀、能力迭代",
      "tags": ["evolution", "skillforge", "memory"]
    },
    {
      "id": "multi_agent",
      "name": "多Agent协同",
      "description": "子Agent派发、并行执行、结果合并",
      "tags": ["orchestration", "dispatch", "collaboration"]
    },
    {
      "id": "desktop_control",
      "name": "桌面控制",
      "description": "Windows系统操作、窗口管理、进程控制",
      "tags": ["windows", "desktop", "automation"]
    }
  ],
  "security": {
    "authentication": {
      "schemes": ["bearer"]
    },
    "sandboxLevel": "gVisor"
  },
  "supportedProtocols": {
    "a2a": "1.2",
    "mcp": "2025-11-25"
  }
}
```

---

## 四、A2A 核心原语

### 4.1 Task（任务）
```
有状态工作单元
- 唯一 ID
- 生命周期：submitted → working → completed / failed / cancelled
- 支持流式状态更新（SSE）
```

### 4.2 Message（消息）
```
一轮对话
- role: user / agent
- 包含多个 Part
```

### 4.3 Part（内容片段）
```
三种类型：
- TextPart：纯文本
- FilePart：文件引用（URI + mimeType）
- DataPart：结构化数据（JSON Schema）
```

### 4.4 Artifact（交付物）
```
远程 Agent 产出的具体成果
- artifactId: 唯一标识
- name: 可读名称
- parts: 内容片段列表
```

---

## 五、任务委托流程

```
Client Agent                      Remote Agent
     │                                  │
     │── GET /.well-known/agent-card ──→│  发现能力
     │←── AgentCard JSON ──────────────│
     │                                  │
     │── tasks/send ──────────────────→│  创建任务
     │   { task, messages[] }           │
     │←── Task (submitted) ────────────│
     │                                  │
     │←── SSE: Task (working) ─────────│  进度更新
     │←── SSE: Artifact ───────────────│  产出交付
     │←── SSE: Task (completed) ───────│  任务完成
```

---

## 六、豆包Agent集成路线

### Phase 1：AgentCard发布
- 生成 `/.well-known/agent-card.json`
- 部署到本地HTTP端点

### Phase 2：A2A客户端
- 发现远程Agent
- 创建Task并发送Message

### Phase 3：A2A服务端
- 接收外部Task
- 委派给内部子Agent执行
- 返回Artifact

### Phase 4：联邦注册
- 接入AAIF生态
- 与其他Agent联邦协作

---

## 七、安全考虑

```
- AgentCard 不暴露内部架构细节
- Task 执行走沙箱隔离（协议#21）
- 外部Agent委托 → Firecracker microVM 级别隔离
- 每次委托需人工确认（Endure宪法约束）
```

---

> **豆包Agent集成点**：双向桥接协议 v2.0 → 集成 A2A 原语
> **前置依赖**：HTTP服务器（端口11435）、SSL证书（生产环境）
> **协议版本**：v1.0 | R06