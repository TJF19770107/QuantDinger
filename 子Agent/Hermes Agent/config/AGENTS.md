---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_31783c4f64db11f1af8f5254002afed2
    ReservedCode1: 57bculI0ku3cFEUhfdIlIo2AjbiYzxDfBUfzHrZ6dU1XCnA4N3yUPAbPTpQnhs8R199Jjh/5WMx1ynIWOMAtodoWsxDhSEkaECYvuI0DEKEqV+L+xJ0h0uS6px4BSs+BEe3WLjGccucak3eeKS3AR4r8zgIGmWtYhtzpovKd/dvNYyXFnSDqQ3rsK+o=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_31783c4f64db11f1af8f5254002afed2
    ReservedCode2: 57bculI0ku3cFEUhfdIlIo2AjbiYzxDfBUfzHrZ6dU1XCnA4N3yUPAbPTpQnhs8R199Jjh/5WMx1ynIWOMAtodoWsxDhSEkaECYvuI0DEKEqV+L+xJ0h0uS6px4BSs+BEe3WLjGccucak3eeKS3AR4r8zgIGmWtYhtzpovKd/dvNYyXFnSDqQ3rsK+o=
---

# AGENTS.md   子代理管理与自动化配置

> 来源：Anthropic 官方 Agent SDK 文档 · 同步日期：2026-06-10
> 同步自：Claude Opus 4.6 Swarm + Agent SDK + MCP

---

## 子代理架构总览

### 子代理定义
子代理是拥有**独立上下文窗口**的专用AI助手，由主Agent创建和调度，执行隔离任务后仅返回精炼结果。

### 核心价值

| 价值 | 说明 |
|------|------|
| 上下文隔离 | 每个子代理独立上下文，避免主对话膨胀 |
| 并行执行 | 多个子代理可同时处理不同子任务 |
| 专注高效 | 每个子代理聚焦单一领域，质量更高 |
| 安全边界 | 子代理权限可独立控制，降低风险 |

### 何时使用子代理
- 任务可拆分为**独立可验证**的子任务
- 子任务执行过程**不需要**与主Agent实时交互
- 结果可**精炼汇总**，不需要完整执行日志
- 任务复杂度**值得**创建子代理的开销

---

## Agent SDK 子代理编程（Python）

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs. Fix any issues.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
            agents={
                "reviewer": {
                    "description": "Reviews code for bugs and style issues",
                    "tools": ["Read", "Grep"]
                }
            }
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

---

## 四件套扩展栈配置速查

| 扩展方式 | 配置路径 | 触发方式 | 典型用途 |
|---------|---------|---------|---------|
| **Skills** | .claude/skills/{name}/SKILL.md | 自动匹配或 /skill-name | 领域知识、可重用工作流 |
| **Hooks** | .claude/settings.json 或 hooks.json | 事件触发（9种事件） | lint、安全验证、环境设置 |
| **Subagents** | .claude/agents/{name}.md | Agent 工具调用 | 隔离调查、代码审查、测试 |
| **MCP** | .mcp.json 或 claude mcp add | 工具调用 | 数据库、Figma 等外部服务 |

## 子代理权限最小化模板

```yaml
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash     # 最小权限：只读 + 搜索
model: opus                       # 安全审查用最强模型
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
```

## Hooks 事件类型

| 事件 | 触发时机 | 执行级别 |
|------|---------|---------|
| PreToolUse | 工具使用前 | block/suggest/warn |
| PostToolUse | 工具使用后 | suggest |
| SessionStart | 会话开始时 | 自动 |
| PreCompact | 压缩前 | 自动 |
| UserPromptSubmit | 用户提交提示时 | suggest |
| SubagentStop | 子代理结束时 | 自动 |

## MCP 生产部署要点

| # | 最佳实践 | 说明 |
|---|---------|------|
| 1 | 有界上下文 | 每个 MCP 服务器围绕单一微服务域 |
| 2 | 无状态幂等 | 接受请求 ID，确定性输出 |
| 3 | 正确传输 | stdio（兼容性）+ 可流式 HTTP（网络部署）|
| 4 | OAuth 2.1 | HTTP 传输强制要求 |
| 5 | 结构化输出 | LLM 可解析 + 人类可读 |

## TeammateTool 编排层（13 个操作）

**团队生命周期**：spawnTeam、discoverTeams、cleanup
**加入工作流**：requestJoin、approveJoin、rejectJoin
**协调通信**：直接消息、广播消息、计划审批协议

## 环境变量标准

```
CLAUDE_CODE_AGENT_ID          # 每个 agent 的唯一标识
CLAUDE_CODE_AGENT_TYPE        # 角色分类
CLAUDE_CODE_TEAM_NAME         # 团队归属
CLAUDE_CODE_PLAN_MODE_REQUIRED # 强制计划审批标志
```
*（内容由AI生成，仅供参考）*
