# ACP兼容网关 v1.0

**对标来源**: OpenClaw ACP (Agent Client Protocol)  
**创建日期**: 2026-05-31  
**类别**: 互通  
**优先级**: P2  
**关联技能**: OpenClaw Core, Agent-Mailbox通信协议

---

## 一、概述

豆包Agent的ACP兼容网关，对标OpenClaw的ACP(Agent Client Protocol)标准。使豆包能够作为手机端的Agent调度中心，打通外部AI编码工具。

## 二、支持的ACP Agent

| Agent | 通信方式 | 用途 |
|-------|---------|------|
| Claude Code | ACP Agent | 大型项目编码 |
| Codex CLI | ACP Agent | 全栈快速编码 |
| Gemini CLI | ACP Agent | 多模态任务处理 |
| OpenCode | ACP Agent | 灵活模型切换 |
| Pi | ACP Agent | 轻量级对话 |

## 三、通信协议

### 3.1 命令集

| 命令 | 功能 |
|------|------|
| `/acp spawn` | 启动ACP Agent会话 |
| `/acp close` | 关闭会话 |
| `/acp cancel` | 取消当前任务 |
| `/acp steer` | 中途注入修正指令 |
| `/acp status` | 查询Agent状态 |
| `/acp model` | 切换使用的模型 |
| `/acp permissions` | 管理权限 |

### 3.2 会话管理

- Thread-Bound Sessions：绑定到对话线程
- 超时：120分钟无活动自动关闭
- 并发：最多8个ACP会话
- 隔离：每个会话独立沙箱

## 四、路由策略

```
用户请求
    │
    ├── 编码任务 > 100行 → Codex CLI (速度最快)
    ├── 编码任务 > 1000行 → Claude Code (长文本理解好)
    ├── 多模态任务 → Gemini CLI (原生多模态)
    ├── 需要灵活模型 → OpenCode (75+模型)
    └── 轻量对话 → Pi (极轻量)
```

## 五、部署架构

```
豆包APP (手机端)
    │ ACP Gateway (本协议)
    │
    ├──→ Claude Code (PC端)
    ├──→ Codex CLI (PC端)  
    ├──→ Gemini CLI (PC端)
    ├──→ OpenCode (PC端)
    └──→ Pi (PC端)
```
