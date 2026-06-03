# 龙虾-A2A+MCP三层协议栈适配协议 v1.1

> 协议编号: 121 | 版本: v1.1 (R34升级) | 来源: 2026年代理协议栈标准（Linux Foundation AAIF治理）
> 生效范围: 全域Agent通信与工具连接 | 依赖: OpenClaw Core + HermesAgent + Gateway协议123

---

## 一、2026年三层代理协议栈

```
A2A — Agent-to-Agent          (L3)
Agents发现彼此、委派任务、协调工作流

MCP — Model Context Protocol  (L2)
Agents连接工具、API和数据源

LLM Foundation Layer           (L1)
Claude、GPT、Gemini、Llama
─── GOVERNANCE & SECURITY ───（跨层治理）
```

> 由Linux Foundation的AAIF（Agentic AI Foundation）治理
> 100+企业加入支持者名单
> 被比作代理时代的TCP/IP和HTTP

## 二、MCP层（Agent ↔ Tool）

### 概述
MCP标准化了AI Agent如何连接外部工具、数据源和服务。
类比：MCP = AI世界的USB-C，通用端口让任何Agent连接任何工具。

### 关键数据
- 9700万+/月 SDK下载量（Python+TypeScript合计）
- 5800+ MCP服务器
- 五大厂商全面支持（Anthropic/OpenAI/Google/Microsoft/Amazon）
- 技术实现：JSON-RPC 2.0线格式，客户端-服务器架构

### 龙虾适配
| MCP概念 | Marvis对应 | 状态 |
|---------|-----------|------|
| MCP Client | Agent工具调用层 | ✅ 已有 |
| MCP Server | Tool schemas注册 | ✅ 已有 |
| 工具发现 | 自动schema发现 | ✅ 已有 |
| JSON-RPC 2.0 | 工具调用协议 | ✅ R34标准化 |
| MCP Server注册表 | Gateway协议123绑定 | 🆕 R34新增 |

## 三、A2A层（Agent ↔ Agent）

### 概述
A2A解决Agent之间如何发现彼此、委派任务、协调工作流的问题。
使用"Agent Cards"——结构化元数据文件，描述每个Agent的能力、输入输出格式和安全要求。

### 关键事件
- 2025年4月：Google开发A2A
- 2025年8月：IBM ACP并入A2A
- 2026年2月：100+企业加入AAIF

### 龙虾适配

| A2A概念 | Marvis对应 | 状态 |
|---------|-----------|------|
| Agent Card | dispatch_task标准化Agent Card | ✅ R34标准化 |
| Agent发现 | Main Agent调度表 + Card动态发现 | ✅ R34增强 |
| 任务委派 | dispatch_task | ✅ 已有 |
| 工作流协调 | Sub Agent协作 | ✅ 已有 |
| Agent Card自动发现 | Agent Card注册端点 | 🆕 R34新增 |

### Agent Card标准化格式（R34）

```json
{
  "agent_card": {
    "name": "doubao-agent",
    "version": "12.1",
    "capabilities": {
      "coding": 98,
      "planning": 98,
      "tools": 98,
      "memory": 99,
      "evolution": 99
    },
    "protocols": ["A2A", "MCP", "Gateway"],
    "endpoints": {
      "a2a": "a2a://doubao.lobster.ai/tasks",
      "mcp": "mcp://doubao.lobster.ai/tools",
      "gateway": "ws://gateway.lobster.ai/channels"
    },
    "input_formats": ["text", "image", "file"],
    "output_formats": ["text", "file", "card", "structured"],
    "security": {
      "auth": "OAuth2.0",
      "sandbox": "enabled",
      "max_concurrent": 3
    }
  }
}
```

## 四、R34 Agent Card动态发现机制

### 4.1 发现流程

```
Agent启动
    ↓
注册Agent Card到Discovery Registry
    ↓
其他Agent通过Discovery查询可用Agent
    ↓
匹配能力 → 建立A2A连接 → 委派任务
```

### 4.2 龙虾Agent Card注册表

| Agent | Card ID | 能力标签 | A2A端点 | 状态 |
|-------|---------|---------|---------|------|
| 豆包Agent | doubao-v12.1 | coding/planning/memory/evolution | a2a://doubao | ACTIVE |
| File Agent | file-v1.0 | file-search/file-ops/format-convert | a2a://file | ACTIVE |
| Computer Agent | computer-v1.0 | system-config/hardware/window-mgmt | a2a://computer | ACTIVE |
| App Agent | app-v1.0 | app-install/app-control/ui-interact | a2a://app | ACTIVE |
| Search Agent | search-v1.0 | deep-search/research-synthesis | a2a://search | ACTIVE |
| Browser Agent | browser-v1.0 | web-interact/form-fill/data-extract | a2a://browser | ACTIVE |

## 五、Gateway绑定（协议121↔协议123）

```
A2A层（协议121）
    ↓ Agent Card发现
Multi-Channel Gateway（协议123）
    ↓ 消息路由+会话管理
MCP层（协议121）
    ↓ 工具调用
外部渠道（微信/飞书/Telegram/CLI）
```

## 六、治理与安全（跨层）

### 三层防线设计（对标Workforce安全架构）

| 防线 | 功能 | 龙虾对应 |
|------|------|---------|
| L1: Policy Engine | 策略引擎：定义Agent能做什么/不能做什么 | 安全约束体系 |
| L2: Sentinel Scanning | 哨兵扫描：检测异常行为 | ECCFramework |
| L3: Integrity Verification | 完整性校验：确保输出可信 | MD5去重+校验 |

## 七、升级记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-06-01 | 初始版本：三层协议栈架构+MCP/A2A适配 |
| v1.1 | 2026-06-02 | R34升级：Agent Card标准化格式+动态发现机制+Gateway协议123绑定 |