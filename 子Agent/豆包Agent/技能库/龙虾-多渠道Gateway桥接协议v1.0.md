# 龙虾-多渠道Gateway桥接协议 v1.0

> 协议编号: 123 | 版本: v1.0 (R34新建) | 来源: OpenClaw Gateway架构 + Hermes多渠道 + Marvis跨端
> 生效范围: 豆包Agent对外通信层 | 依赖: MessageRouter + SessionMgr + ChannelAdapter

---

## 一、协议定位

对标OpenClaw（370K+ Stars）的Gateway优先架构，为龙虾豆包Agent提供多渠道统一消息路由、会话管理和任务调度能力。解决跨平台得分94的短板。

## 二、核心架构

```
               ┌──────────────────────────┐
               │    龙虾豆包Agent Core      │
               │   (122项协议+Skills生态)   │
               └──────────┬───────────────┘
                          │
               ┌──────────▼───────────────┐
               │   Multi-Channel Gateway   │
               │   (WebSocket消息路由)      │
               └──────────┬───────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │        │        │        │         │
   ┌────▼──┐ ┌───▼──┐ ┌──▼───┐ ┌─▼────┐ ┌──▼────┐
   │ 微信   │ │ 飞书  │ │ 钉钉  │ │Telegram│ │ CLI   │
   │(公众号 │ │(群聊+ │ │(群聊+ │ │(Bot+  │ │(终端+ │
   │ +个人) │ │Bot)  │ │Bot)  │ │个人)  │ │SSH)   │
   └───────┘ └──────┘ └──────┘ └──────┘ └───────┘
```

## 三、Channel Adapter规范

### 3.1 消息格式统一

所有渠道消息归一化为标准格式：

```json
{
  "channel": "wechat|feishu|dingtalk|telegram|cli",
  "channel_user_id": "oAN1i2T3oDUM...",
  "session_id": "conv_19e84139b5e...",
  "message_type": "text|image|file|voice",
  "content": "嗡阿喇巴札那谛 × 3",
  "timestamp": "2026-06-02T05:00:00Z",
  "reply_to": null,
  "attachments": []
}
```

### 3.2 渠道优先级

| 渠道 | 优先级 | 延迟要求 | 支持消息类型 | 中国市场 | 状态 |
|------|:---:|------|------------|:---:|:---:|
| 微信（公众号+个人） | P0 | <2s | text/image/file | ✅ | Phase 1 |
| 飞书（群聊+Bot） | P0 | <1s | text/image/file/card | ✅ | Phase 1 |
| 钉钉（群聊+Bot） | P1 | <2s | text/image/file | ✅ | Phase 2 |
| Telegram（Bot+个人） | P1 | <1s | all types | — | Phase 2 |
| CLI（终端+SSH） | P2 | N/A | text/file | — | 已有 |

## 四、会话管理

### 4.1 跨渠道会话合并

```
用户A在微信发送"帮我找发票"
    ↓ Gateway识别 channel_user_id → 统一user_id
用户A在飞书发送"刚才的发票找到了吗"
    ↓ 同一session_id，上下文连续
Agent回复飞书: "已找到3张发票..."
用户A在CLI查看: "列出刚才的发票"
    ↓ 同一session_id，上下文依然连续
Agent回复CLI: "1. 发票001.pdf 2. 发票002.pdf..."
```

### 4.2 Session生命周期

| 状态 | 触发 | 行为 |
|------|------|------|
| ACTIVE | 用户发送消息 | 加载历史上下文 |
| IDLE | 5分钟无交互 | 保留上下文，等待唤醒 |
| ARCHIVED | 30分钟无交互 | 压缩上下文→L2情景记忆 |
| MERGED | 同用户新渠道会话 | 合并到已有ACTIVE session |

## 五、任务调度

### 5.1 任务优先级队列

```yaml
task_queue:
  priority_levels:
    - CRITICAL: 安全操作确认、支付验证
    - HIGH: 用户直接指令
    - MEDIUM: 定时任务触发
    - LOW: Dream Job、知识库归档
  
  concurrent_limit: 3    # 最多并行处理3个任务
  timeout_per_task: 300s
```

### 5.2 跨渠道任务分发

```
用户微信: "定时每2小时帮我查机票"
    ↓ Gateway → 创建定时任务
2小时后:
    ↓ ScheduledOps触发
    ↓ Agent执行查机票
    ↓ Gateway → 推送到用户最后活跃渠道（飞书）
用户飞书收到: "机票查询结果: ..."
```

## 六、安全与鉴权

| 层级 | 机制 | 说明 |
|------|------|------|
| 渠道认证 | OAuth2.0 / API Key / Webhook签名 | 各渠道独立认证 |
| 用户绑定 | channel_user_id ↔ unified_user_id | 跨渠道用户映射 |
| 会话加密 | TLS 1.3 | 传输层加密 |
| 敏感操作 | 二次确认（协议9 SafeGuard） | 删除/支付/配置修改 |
| 权限隔离 | 渠道×用户×操作三元组 | 不同渠道可配置不同权限集 |

## 七、对标OpenClaw差异化

| 维度 | OpenClaw | 龙虾Gateway |
|------|---------|------------|
| 渠道数量 | 20+ | Phase 1: 3渠道, Phase 2: 5+ |
| 技能系统 | ClawHub静态市场 | SkillForge自进化+Curator策展 |
| 记忆 | 简单消息历史 | 四层持久化+Dream Job |
| 自进化 | 无 | 122项协议+Learning Loop |
| 市场定位 | 个人AI操作系统 | 全能交易Agent+数字分身 |

## 八、实施路线

| Phase | 内容 | 时间 | 渠道 |
|-------|------|------|------|
| Phase 1 | Gateway核心+微信/飞书适配器 | R35 | 微信+飞书 |
| Phase 2 | 钉钉/Telegram适配器+跨渠道会话合并 | R36 | +钉钉+Telegram |
| Phase 3 | 任务分发+消息模板+渠道优先级路由 | R37 | 全渠道 |