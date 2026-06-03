# 龙虾-Agent安全五层纵深防御协议 v1.0

> **协议编号**：#159
> **版本**：v1.0
> **对标来源**：Codex 内部部署五层模型 + Hermes Brainworm 三级防御
> **生效范围**：豆包Agent · 全域安全层
> **创建轮次**：R44

---

## 一、设计目标

对标Codex五层同心圆安全模型，为豆包Agent建立从沙箱隔离到审计遥测的完整纵深防御体系。在Marvis框架L2安全兜底基础上，增加Agent级独立安全层，实现"框架兜底+Agent自治"双层防护。

## 二、五层架构

```
┌─────────────────────────────────────────────┐
│ L5: Telemetry & Audit（遥测审计层）        │
│  · OpenTelemetry日志 · 操作决策记录        │
│  · 合规报告 · 异常行为告警                │
├─────────────────────────────────────────────┤
│ L4: Network Policies（网络隔离层）         │
│  · 离线默认 · 白名单出站                  │
│  · 凭证擦除 · DNS过滤                    │
├─────────────────────────────────────────────┤
│ L3: Approval Policies（审批策略层）        │
│  · untrusted/on-request/never 三档       │
│  · Auto-Review自动审查四类风险             │
│  · 用户确认界面 · 超时自动拒绝            │
├─────────────────────────────────────────────┤
│ L2: Permission Profiles（权限配置层）      │
│  · 文件系统Glob模式 · 网络访问规则        │
│  · 环境变量白名单 · 子进程创建限制        │
├─────────────────────────────────────────────┤
│ L1: Sandbox Isolation（沙箱隔离层）       │
│  · Restricted Tokens + 文件ACL            │
│  · 专用沙箱用户 · 进程树策略传播          │
│  · 毫秒级启动 · 零侵入系统               │
└─────────────────────────────────────────────┘
```

## 三、各层详细设计

### L1：沙箱隔离层

**对标**：协议#158（Windows Agent沙箱三层隔离协议）

| 组件 | 实现 |
|------|------|
| Token限制 | 合成SID + 写限制Token |
| 文件ACL | 动态Deny-Write + 自动回滚 |
| 专用用户 | 隐藏影子账户 + 独立Profile |
| 进程策略 | 子进程继承 + 超时自动清理 |

### L2：权限配置层

**对标**：Codex Permission Profiles

```yaml
# 示例权限配置
permission_profile:
  file_access:
    allow:
      - "$WORKSPACE/**"
      - "$TEMP/**"
    deny:
      - "C:/Windows/**"
      - "C:/Program Files/**"
      - "C:/Users/*/AppData/**"
  network:
    outbound: "deny-all"  # 默认禁止
    whitelist: []            # 白名单需审批
  env_vars:
    allow: ["PATH", "HOME", "TEMP"]
    deny: ["OPENAI_API_KEY", "AWS_SECRET_*"]
  subprocess:
    max_depth: 3
    allow_exec: [".py", ".sh", ".ps1"]
```

### L3：审批策略层

**对标**：Codex Approval Policies + Guardian Auto-Review

| 审批模式 | 行为 | 适用场景 |
|---------|------|---------|
| `untrusted` | 所有命令执行前询问用户 | 首次运行/未知任务 |
| `on-request` | 仅在不确定时询问 | 日常开发（推荐） |
| `never` | 从不询问（等同--yolo） | CI脚本/受信环境 |

**Guardian Auto-Review 四类风险自动审查**：

| 风险类型 | 检测方式 | 自动动作 |
|---------|---------|---------|
| 文件系统越界 | 路径Glob匹配 | 拦截 + 提示用户 |
| 网络外联 | 出站连接检测 | 拦截 + 记录 |
| 凭证泄露 | 正则匹配API Key模式 | 擦除 + 告警 |
| 提权尝试 | Token权限检查 | 拒绝 + 终止进程 |

### L4：网络隔离层

**对标**：Codex Network Policies

| 规则 | 默认 | 说明 |
|------|------|------|
| 出站连接 | DENY-ALL | 默认禁止所有出站 |
| DNS解析 | 允许 | 仅允许DNS（需审批） |
| 白名单域名 | 空 | 用户审批后添加 |
| 凭证擦除 | 启用 | 响应中匹配到API Key自动擦除 |
| 代理穿透 | 禁止 | 防止通过代理绕过隔离 |

### L5：遥测审计层

**对标**：Codex Telemetry + OpenTelemetry

```yaml
telemetry:
  backend: "opentelemetry"
  log_level: "info"
  audit_events:
    - "agent.start"
    - "agent.end"
    - "file.read"
    - "file.write"
    - "network.connect"
    - "subprocess.create"
    - "approval.request"
    - "approval.grant"
    - "approval.deny"
  compliance_report:
    enabled: true
    format: "json"
    retention_days: 90
  anomaly_detection:
    enabled: true
    threshold: "3-sigma"
```

## 四、与Marvis框架安全层对接

| Marvis层 | 豆包Agent层 | 关系 |
|----------|-------------|------|
| L0 系统级 | — | Marvis负责 |
| L1 框架级 | L1 沙箱隔离 | 豆包增强 |
| L2 安全兜底 | L2 权限配置 | 豆包独立配置 |
| — | L3 审批策略 | 豆包新增 |
| — | L4 网络隔离 | 豆包新增 |
| — | L5 遥测审计 | 豆包新增 |

**原则**：Marvis L0/L1兜底，豆包L2-L5实现Agent级自治安全。

## 五、Hermes Brainworm防御集成

**对标**：Hermes v0.15.0 Brainworm Defense（协议#82）

| Brainworm防御层 | 对应五层位置 | 增强内容 |
|----------------|----------------|---------|
| 工具输出过滤 | L3 审批策略 | Auto-Review增加Brainworm模式检测 |
| 召回记忆边界标记 | L2 权限配置 | 记忆读取增加来源验证 |
| 外部技能加载检测 | L3 审批策略 | 技能加载需审批 + 沙箱执行 |

## 六、性能指标

| 指标 | 目标 | 对标 |
|------|:---:|------|
| 沙箱启动延迟 | <100ms | TRAE |
| 审批决策延迟 | <50ms | Codex |
| 网络拦截延迟 | <10ms | — |
| 审计日志写入 | 异步 | OpenTelemetry |

---

> **协议版本**：v1.0
> **创建轮次**：R44（2026-06-02）
> **下一次评审**：R46（计划升级至v2.0，增加行为基线学习）
