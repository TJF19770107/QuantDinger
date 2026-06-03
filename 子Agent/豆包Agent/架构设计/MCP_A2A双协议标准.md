# MCP + A2A 双协议标准对比 — Agent通信基础设施
## 来源：DevTk.AI + 官方规范 2026-05

---

## 一、两大协议定位

```
MCP = AI的USB-C接口（Agent ↔ 工具，垂直连接）
A2A = AI Agent的HTTP协议（Agent ↔ Agent，水平协作）

两者互补，非竞争关系。
```

---

## 二、MCP（Model Context Protocol）

### 基本信息

| 维度 | 详情 |
|------|------|
| 创建者 | Anthropic（2024年11月） |
| 治理 | Linux基金会（2025年12月捐赠） |
| 传输 | JSON-RPC over stdio / Streamable HTTP |
| 生态 | 8,000+社区服务器 |

### 四个核心原语

| 原语 | 控制方 | 用途 |
|------|--------|------|
| Tools | 模型控制 | AI可调用的函数 |
| Resources | 应用控制 | AI可读取的数据 |
| Prompts | 用户控制 | 预置提示词模板 |
| Tasks | 模型控制 | 长时间异步操作（2025.11新增） |

### 2026年关键更新

- **MCP Apps (SEP-1865)**：工具返回交互式UI组件（仪表板/表单/可视化）
- 支持客户端：Claude、GPT、Gemini、Cursor、Windsurf等

---

## 三、A2A（Agent-to-Agent Protocol）

### 基本信息

| 维度 | 详情 |
|------|------|
| 创建者 | Google（2025年4月） |
| 治理 | Linux基金会 |
| 传输 | JSON-RPC over HTTP(S) / gRPC |
| 合作伙伴 | 100+（Salesforce/SAP/ServiceNow/LangChain/PayPal等） |

### Agent Card 发现机制

每个Agent在 `/.well-known/agent.json` 发布元数据：
- 身份描述、技能列表
- 支持的输入输出模式
- 流式推送支持
- 安全认证方式

### 任务生命周期状态机

```
queued → running → input-required/ auth-required → completed
                 → canceled / rejected / failed
```

| 状态 | 是否终态 | 描述 |
|------|:---:|------|
| queued | 否 | 已接收，等待处理 |
| running | 否 | 正在处理中 |
| input-required | 否 | 需要额外用户输入 |
| auth-required | 否 | 需要认证凭据 |
| completed | 是 | 成功完成 |
| canceled | 是 | 被取消 |
| rejected | 是 | Agent拒绝请求 |
| failed | 是 | 处理出错 |

---

## 四、MCP vs A2A 逐项对比

| 维度 | MCP | A2A |
|------|-----|-----|
| 用途 | Agent ↔ 工具（垂直） | Agent ↔ Agent（水平） |
| 架构 | 客户端-服务器 | 点对点 |
| 发现 | 宿主暴露工具 | Agent Card well-known URL |
| 状态 | 无状态函数调用 | 有状态任务生命周期 |
| 通信 | 请求→响应 | 多轮对话+任务跟踪 |
| 长任务 | Tasks原语 | 一等公民 |
| 文件 | 通过工具实现 | 内置FilePart |
| 认证 | 自定义 | OAuth2/Bearer/API Key/mTLS |
| 多Agent | 非设计目标 | 核心设计目标 |
| 人机协作 | 不内置 | input-required状态 |

---

## 五、共存架构

```
┌──────────────────────────────────────────┐
│        Agent 编排器（A2A发现）            │
├────────────┬────────────┬────────────────┤
│  Agent A   │  Agent B   │   Agent C      │
│  (MCP内部)  │  (MCP内部)  │   (MCP内部)    │
│  ├数据库    │  ├API      │   ├文件        │
│  ├搜索      │  ├邮件     │   ├GitHub     │
│  └计算      │  └CRM      │   └Slack      │
└────────────┴────────────┴────────────────┘
      ↕ A2A（Agent间通信）
      ↕ MCP（Agent内工具调用）
```

---

## 六、协议发展时间线

| 时间 | 事件 |
|------|------|
| 2024.11 | Anthropic发布MCP |
| 2025.03 | OpenAI支持MCP |
| 2025.04 | Google发布A2A（50+合作伙伴） |
| 2025.07 | A2A v0.3 — gRPC + 签名安全卡 |
| 2025.11 | MCP新增Tasks原语 + Streamable HTTP |
| 2025.12 | MCP捐赠Linux基金会 |
| 2026.01 | MCP Apps — AI客户端内交互式UI |
| 2026 | 两协议共存为行业标准 |

---

## 七、豆包对接建议

1. **内部工具调用**：采用MCP协议，Agent通过JSON-RPC调用本地工具
2. **子Agent通信**：采用A2A协议，每个子Agent发布Agent Card，主Agent通过A2A发现和调度
3. **外部Agent互通**：通过A2A Agent Card暴露豆包能力，接入外部Agent生态
4. **长任务处理**：A2A任务生命周期管理后台批量任务
