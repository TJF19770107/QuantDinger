# OpenClaw龙虾Agent 迭代配置 · 2026-05-31

**版本号**：R07
**所属子Agent**：OpenClaw龙虾Agent（底层能力支撑、插件联动、全流程落地执行）
**同步基准**：MCP协议最新标准 + OpenAI Agents SDK + OpenClaw v2026.5.28

---

## 一、MCP 最新协议对接方案

### 1.1 MCP 协议标准化路线图

| 协议阶段 | 状态 | OpenClaw对接方案 |
|----------|------|-----------------|
| Streamable HTTP 传输 | 已标准化 | 替换现有JSON-RPC over stdio为HTTP，支持无状态部署 |
| OAuth 2.1 认证 | 已标准化 | 接入OAuth 2.1，支持跨应用SSO |
| Skills over MCP | 已标准化 | 龙虾技能库通过skills/list和skills/get端点暴露 |
| Server自动发现 | 已标准化 | 创建.well-known/mcp-server-card/server.json |
| SDK v2.0 | 即将发布 | TS/Python双语言SDK适配 |

### 1.2 OpenClaw MCP Server 注册中心设计

```
E:\龙虾AI主控中心\我的AI分身\子Agent\OpenClaw龙虾Agent\mcp-registry\
    ├── server-card.json          # 龙虾MCP Server自描述
    ├── tools-registry.json       # 工具注册表（FastAPI-MCP自动生成）
    ├── skills-endpoint.json      # Skills over MCP端点清单
    └── auth-config.json          # OAuth 2.1客户端配置
```

### 1.3 FastAPI-MCP 集成

将现有龙虾技能中的 Python 服务暴露为 MCP 工具：

| 现有技能 | FastAPI-MCP暴露方案 |
|----------|-------------------|
| auto_file_scanner.py | → MCP Tool: file_scan |
| memory_os.py | → MCP Tool: memory_search / memory_store |
| desktop_controller.py | → MCP Tool: desktop_action (受限暴露) |
| safe_guard.py | → MCP Guardrail: safety_check |
| skill_forge.py | → MCP Tool: skill_generate |

**实现路径**：
```python
# 示例：将auto_file_scanner暴露为MCP工具
from fastapi_mcp import FastApiMCP

app = FastAPI()
mcp = FastApiMCP(app)

@mcp.tool("file_scan")
async def scan_directory(path: str, pattern: str = "*"):
    return auto_file_scanner.scan(path, pattern)
```

---

## 二、OpenAI Agents SDK 集成

### 2.1 三大原语映射

| OpenAI Agents SDK 原语 | OpenClaw龙虾Agent 对应能力 |
|------------------------|--------------------------|
| **Handoff** | dispatch_task → 子Agent任务转移 |
| **Guardrail** | SafeGuard技能 → 输入/输出安全检查 |
| **Tracing** | execution_log + 可视化工作流 |

### 2.2 Handoff 增强方案

参考 OpenAI Agents SDK 的 Handoff 机制优化多Agent调度：

```
当前：Hermes Agent → dispatch_task → 目标Agent
优化后：
    主调度器(Orchestrator)
    ├── Handoff: agent_name + context + expected_output
    ├── Guardrail: 输入验证 → 输出验证
    └── Tracing: trace_id贯穿全链路
```

### 2.3 多Agent编排优化

借鉴 OpenAI Agents SDK 的设计理念：

| 编排模式 | 适用场景 | OpenClaw实现 |
|----------|----------|-------------|
| 串行链 | 文件处理流水线 | 扫描→分析→归档 |
| 并行扇出 | 多源情报采集 | 同时查询GitHub/B站/抖音/小红书 |
| 路由分发 | 任务类型匹配Agent | 文件→FileAgent, 系统→ComputerAgent |
| 循环迭代 | 自进化闭环 | R01→R02→...→R07 |

---

## 三、OpenClaw v2026.5.28 新特性对接

### 3.1 子智能体物理隔离

| OpenClaw特性 | 龙虾体系实现 |
|-------------|-------------|
| 运行路径隔离 | 每个子Agent独立运行目录 |
| 工作空间隔离 | 豆包/Hermes/OpenClaw各自独立目录 |
| 沙箱防污染 | SafeGuard + Firecracker沙箱方案 |

**当前状态**：豆包Agent、Hermes Agent、OpenClaw龙虾Agent已实现目录级隔离，沙箱方案已有架构设计（Firecracker_豆包沙箱方案.md），待实施。

### 3.2 Codex 弹性恢复机制

| OpenClaw特性 | OpenClaw龙虾Agent应用 |
|-------------|---------------------|
| 任务中断恢复 | checkpoint机制 → stable_checkpoint.json |
| 状态持久化 | 迭代日志目录 + memory/long_term.db |
| 断点续传 | task_queue.json + 任务状态追踪 |

**当前状态**：豆包Agent已有checkpoints目录和stable_checkpoint机制，需扩展到Hermes Agent和OpenClaw龙虾Agent。

### 3.3 移动端Pro UI

| OpenClaw特性 | 意义 |
|-------------|------|
| WKWebView渲染 | 移动端可直接查看迭代报告、知识库 |
| 实时语音双向播放 | 可对接豆包AI播客功能 |
| 移动端监控 | 巡检报告、告警推送 |

---

## 四、底层能力拓展

### 4.1 新工具/协议接入优先级

| 优先级 | 工具/协议 | 说明 |
|--------|----------|------|
| P0 | MCP Server注册中心 | 统一管理所有龙虾体系MCP工具 |
| P0 | FastAPI-MCP适配层 | 将Python技能暴露为MCP工具 |
| P1 | OpenAI Agents SDK Handoff | 多Agent调度优化 |
| P1 | OAuth 2.1认证 | 企业级安全标准 |
| P2 | Letta .af格式 | 子Agent打包与迁移标准 |
| P2 | Skills over MCP | 技能库标准化暴露 |

### 4.2 沙箱安全增强

| 层级 | 当前状态 | R07建议 |
|------|----------|---------|
| 文件系统 | 目录隔离 | 增加文件操作审计日志 |
| 网络 | 无限制 | 按子Agent配置网络白名单 |
| 进程 | 共享进程空间 | 子Agent独立进程/线程池 |
| 权限 | 管理员权限 | 最小权限原则，按需提权 |

### 4.3 可观测性增强

| 维度 | 工具 | 方案 |
|------|------|------|
| 日志 | iteration_log.md | 统一日志格式、按子Agent分文件 |
| 指标 | 扣子罗盘 | 接入扣子罗盘监控 |
| 追踪 | Tracing原语 | trace_id贯穿全链路 |
| 告警 | SafeGuard | 异常行为自动告警 |

---

## 五、版本迭代记录

| 轮次 | 日期 | 核心更新 |
|------|------|----------|
| R01-R06 | 2026-05-31 | 目录建立、SOUL/USER/AGENTS初版、执行技能 |
| **R07** | **2026-05-31** | **MCP标准化对接、OpenAI Agents SDK集成、v2026.5.28特性、沙箱增强** |

---

> **关联文件**：SOUL.md v1.0、AGENTS.md v3.0、execution-skills.md、同步情报_20260531_2200.md
