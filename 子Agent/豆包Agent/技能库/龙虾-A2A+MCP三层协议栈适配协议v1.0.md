# 龙虾-A2A+MCP三层协议栈适配协议 v1.0

> 协议编号: 121 | 版本: v1.0 | 来源: 2026年代理协议栈标准（Linux Foundation AAIF治理）
> 生效范围: 全域Agent通信与工具连接 | 依赖: OpenClaw Core + HermesAgent

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
| JSON-RPC 2.0 | 工具调用协议 | ⬜ 待标准化 |
| MCP Server注册表 | 无 | ⚡ R34新增 |

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
| Agent Card | dispatch_task 参数schema | ⬜ 待标准化 |
| Agent发现 | Main Agent调度表 | ✅ 已有 |
| 任务委派 | dispatch_task | ✅ 已有 |
| 工作流协调 | Sub Agent协作 | ✅ 已有 |
| Agent Card自动发现 | 无 | ⚡ R34新增 |

## 四、治理与安全（跨层）

### 三层防线设计（对标Workforce安全架构）

| 防线 | 功能 | 龙虾对应 |
|------|------|---------|
| L1: Policy Engine | 策略引擎：定义Agent能做什么/不能做什么 | 安全约束体系 |
| L2: Sentinel Scanning | 哨兵扫描：检测异常行为 | ECCFramework |
| L3: Integrity Verification | 完整性校验：确保输出可信 | MD5去重+校验 |

## 五、R34行动清单

| 动作 | 说明 | 优先级 |
|------|------|--------|
| MCP Server注册表 | 标准化工具schema为MCP JSON-RPC 2.0格式 | 🟡 P1 |
| Agent Card标准化 | dispatch_task参数升级为Agent Card格式 | 🟡 P1 |
| Agent发现机制 | 实现Agent Card自动发现端点 | 🟢 P2 |
| 协议合规检查 | MCP+A2A标准合规审计 | 🟢 P3 |