# 龙虾-Gateway微内核中枢协议 v1.0

> **来源**：OpenClaw Gateway 源码级分析
> **提取轮次**：R04
> **创建时间**：2026-05-31
> **状态**：ACTIVE

---

## 一、协议目标

将豆包Agent的核心调度层升级为微内核中枢（Gateway），实现插件生命周期管理、RPC 方法注册、配置热加载和安全纵深防御的统一架构。

---

## 二、Gateway 五大角色

```
┌─────────────────────────────────────────────┐
│              Gateway 微内核中枢               │
│                                              │
│  ┌─────────────────────────────────────┐    │
│  │ 角色1：唯一长驻进程                    │    │
│  │ 角色2：RPC 方法注册中心（42+ handler） │    │
│  │ 角色3：插件生命周期管理器              │    │
│  │ 角色4：安全决策点（纵深防御）            │    │
│  │ 角色5：配置热加载引擎                  │    │
│  └─────────────────────────────────────┘    │
│                    ↕                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Channel  │  │  Agent   │  │  Plugin  │  │
│  │ 适配层   │  │  核心    │  │  系统    │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

---

## 三、RPC 方法注册体系

### 3.1 功能域分类

| 功能域 | RPC 方法 | 职责 |
|--------|---------|------|
| 聊天/消息 | sendMessage, getHistory, streamResponse | 消息收发与历史 |
| 会话管理 | createSession, closeSession, listSessions | 会话生命周期 |
| 配置管理 | getConfig, updateConfig, hotReload | 运行时配置 |
| 模型管理 | listModels, switchModel, modelStatus | LLM 模型调度 |
| 安全审批 | requestApproval, checkPermission | 安全决策 |
| 定时任务 | scheduleTask, cancelTask, listTasks | 定时任务管理 |
| 远程节点 | connectNode, disconnectNode, syncState | 跨设备协同 |
| 语音唤醒 | registerWake, processAudio, voiceStatus | 语音交互 |

### 3.2 方法授权流程

```
Client 请求 → 身份验证（Ed25519）
                ↓
           权限检查（ACL 白名单）
                ↓
           限流检查（Rate Limiter）
                ↓
           执行 RPC Handler
                ↓
           审计日志记录
```

---

## 四、插件生命周期管理

```
加载（Load）
  ↕
初始化（Init）← 注入配置
  ↕
激活（Activate）← 注册到 RPC 表
  ↕
运行（Running）
  ↕
挂起（Suspend）← 异常/超限
  ↕
停用（Deactivate）
  ↕
卸载（Unload）
```

---

## 五、安全纵深防御

```
第1层：网络 TLS + Device Identity
第2层：认证 Ed25519 Challenge-Response
第3层：授权 ACL 白名单 + 角色权限
第4层：审批 高危操作人工确认
第5层：沙箱 Docker/SSH/OpenShell 隔离
```

执行策略默认 `deny`：
- 所有 shell 命令需通过白名单或人工审批
- 插件安装时静态代码扫描，危险模式直接阻断
- 控制平面写操作限流

---

## 六、配置热加载

```json
{
  "agent": {
    "name": "doubao",
    "model": "claude-4-sonnet",
    "personality": "lobster"
  },
  "channels": ["marvis", "wechat", "telegram"],
  "security": {
    "execution_policy": "deny",
    "allowed_commands": ["ls", "cat", "echo"],
    "sandbox": "docker"
  }
}
```

配置文件变更后自动热重载，无需重启。

---

## 七、与龙虾现有协议的关系

| 现有协议 | 互补关系 |
|---------|---------|
| 龙虾-双向桥接协议 v2.0 | Gateway 是桥接协议的实现载体 |
| 龙虾-Gateway性能优化手册 v1.0 | 本协议定义架构，优化手册提供调参 |
| 龙虾-自进化协调器(SICA) v1.0 | SICA 作为 Gateway 的一个 RPC handler 注册 |

---

> 版本：v1.0
> 来源：OpenClaw Gateway 源码分析 | 龙虾自主融合
> 文件路径：E:\龙虾AI主控中心\我的AI分身\技能库\龙虾-Gateway微内核中枢协议v1.0.md