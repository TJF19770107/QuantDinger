# 龙虾-Codex可观测性生命周期协议 v1.0

> **协议编号**：65
> **对标来源**：Codex CLI v0.133 Extension Lifecycle Events
> **创建轮次**：R18
> **创建时间**：2026-06-01
> **状态**：ACTIVE

---

## 一、协议概述

本协议建立完整的Agent生命周期可观测性模型，通过11个标准事件覆盖从会话启动到子Agent生成的完整链路。区分观测事件（Observation，只读通知不阻塞Agent循环）与拦截事件（Interception，可修改行为或阻止操作），支持插件化的成本追踪、性能监控和治理门禁。

## 二、11事件模型

### 2.1 观测事件（Observation Events）

观测事件在操作提交后异步触发，不引入Agent循环延迟，不产生多Agent死锁。

| 事件 | 触发时机 | 关键负载 | 用途 |
|------|---------|---------|------|
| **SubagentStart** | 子Agent启动时 | agent_name, model, service_tier, permission_profile, parent_agent, spawn_depth | 成本追踪起点、权限校验 |
| **SubagentStop** | 子Agent完成/失败时 | input_tokens, output_tokens, reasoning_tokens, duration_ms, exit_reason | 成本结算、性能分析 |
| **ToolExecution** | 任何工具执行后 | tool_name, tool_input, tool_output_summary, duration_ms, mcp_source | 工具使用统计、延迟监控 |
| **TurnMetadata** | 每轮对话结束后 | turn_id, tokens_consumed, tools_called, wall_clock_ms | 轮次级别性能跟踪 |
| **AsyncApproval** | 异步审批事件 | approval_id, requested_action, status, timestamp | 审计追踪 |

### 2.2 拦截事件（Interception Events）

拦截事件在操作提交前触发，可修改行为参数或完全阻止操作。

| 事件 | 触发时机 | 可修改 | 用途 |
|------|---------|--------|------|
| **SessionStart** | 新会话启动 | config, system_prompt | 动态注入配置 |
| **PreToolUse** | 工具调用前 | tool_input, allow/deny | 参数审查、权限控制 |
| **PostToolUse** | 工具调用后 | tool_output_presentation | 输出格式化、敏感信息脱敏 |
| **PermissionRequest** | 权限请求 | approval_decision | 自定义审批逻辑 |
| **UserPromptSubmit** | 用户提交消息 | prompt_modifications | 输入预处理 |
| **Stop** | Agent停止 | stop_reason, cleanup_actions | 优雅关闭 |

## 三、插件架构

### 3.1 成本追踪插件

```
配对 SubagentStart + SubagentStop 事件：

SubagentStart: 记录 agent_name + model + service_tier
SubagentStop:  记录 tokens_consumed + duration_ms + exit_reason

输出：
  - Per-agent 成本分解
  - Per-task 总成本
  - 模型选择效率分析（廉价vs昂贵模型的实际效果对比）
```

### 3.2 治理门禁插件

```
拦截 SubagentStart 事件：

检查 permission_profile：
  - file_access: ["read_only", "read_write", "system"]
  - network_access: ["none", "whitelist", "full"]
  - shell_access: ["none", "sandbox", "full"]
  - spawn_depth_limit: 3 (防止无限递归)
  
  越权 → deny + 记录治理违规
  合规 → 继续执行
```

### 3.3 性能监控插件

```
监听 ToolExecution 事件：

统计维度：
  - Per-tool 平均延迟 (P50/P95/P99)
  - Per-tool 成功率
  - Per-model 工具调用效率
  - 异常检测：P99超过阈值自动告警
```

## 四、插件开发规范

### 4.1 插件接口

```python
class LifecyclePlugin:
    """Codex生命周期事件插件基类"""
    
    def on_subagent_start(self, event: SubagentStartEvent) -> None:
        """子Agent启动时触发"""
        pass
    
    def on_subagent_stop(self, event: SubagentStopEvent) -> None:
        """子Agent停止时触发"""
        pass
    
    def on_tool_execution(self, event: ToolExecutionEvent) -> None:
        """工具执行后触发"""
        pass
    
    def on_turn_metadata(self, event: TurnMetadataEvent) -> None:
        """轮次结束后触发"""
        pass
```

### 4.2 架构约束

- 观测事件处理器不得抛出异常（异常会被静默捕获并记录）
- 观测事件处理器执行时间不得超过100ms（超时自动终止）
- 拦截事件处理器必须在500ms内返回决策
- 所有事件处理器不得修改事件对象以外的Agent状态

## 五、豆包Agent适配方案

1. **事件总线**：在主Agent中建立事件总线，5个子Agent的启动/停止/工具调用均发布标准事件
2. **成本追踪**：SubagentStart+SubagentStop配对追踪File/Computer/App/Browser/Search各自Token消耗
3. **治理门禁**：SubagentStart时校验permission_profile，File Agent不能越权访问系统路径
4. **性能面板**：ToolExecution事件聚合后输出到可视化工作流引擎的性能面板
5. **异步审批**：AsyncApproval事件接入SafeGuard安全层，敏感操作触发用户确认