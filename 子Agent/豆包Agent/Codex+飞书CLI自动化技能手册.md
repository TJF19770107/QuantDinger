# Codex + 飞书 CLI 自动化技能手册 v1.0

> 来源：龙虾全域官方模板 v3.94 · 公众号文章《如何通过 Codex 对话接入飞书完整版来了！》
> 生成日期：2026-06-15
> 协议映射：模板 254 项协议中与 Codex/飞书 相关 12 项

---

## 一、核心架构概览

```
用户 ↔ Codex CLI (本地) ↔ 飞书开放平台 API
         │                      │
         ├─ 代码生成/自动化      ├─ 文档（飞书文档）
         ├─ 事件驱动流水线      ├─ Base（多维表格）
         ├─ 桌面视觉操控        ├─ 消息（机器人/群聊）
         ├─ 锁屏无人值守        ├─ 日历（日程管理）
         └─ 长时域Goal推进      └─ 会议（视频会议）
```

### 对标协议映射

| 编号 | 协议名称 | 涉及领域 | 版本 |
|:---:|------|------|:---:|
| #13 | 事件驱动自动化流水线协议 | Codex Triggers + 飞书 Webhook | v1.0 |
| #40 | 有状态心跳自主调度协议 | Codex Thread Automations + 飞书定时消息 | v1.0 |
| #53 | Windows桌面视觉操控协议 | Codex Win CU + 飞书桌面端操控 | v1.0 |
| #78 | 长时域Goal任务推进协议 | Codex /goal + 飞书OKR同步 | v1.0 |
| #79 | Appshots上下文快照注入协议 | Codex Appshots + 飞书截图分享 | v1.0 |
| #93 | 锁屏远程移动Agent操控协议 | Codex Mobile + 飞书移动端审批 | v1.0 |
| #95 | 事件驱动Trigger自动化流水线协议 | Codex Triggers + 飞书事件通知 | v1.0 |
| #123 | 多渠道Gateway桥接协议 | 飞书/微信/钉钉/Telegram统一路由 | v1.0 |
| #172 | 桌面全平台视觉操控协议 v3.0 | Codex Win CU v26.527 + 飞书桌面 | v3.0 |
| #188 | 超级应用Agent融合协议 | Codex+ChatGPT合体 + 飞书生态 | v1.0 |
| #218 | 豆包专业版六大领域能力对齐协议 | Codex 6角色 + 飞书企业协作 | v1.0 |
| #223 | 腾讯效率智能体工具集全链路工业化对齐协议 | CodeBuddy + 飞书企业平台 | v1.0 |

---

## 二、Codex CLI 接入飞书完整流程

### 2.1 前置准备

```bash
# 1. 确认 Codex CLI 版本 (≥ v0.135.0, 87K+ Stars)
codex --version

# 2. 飞书开放平台创建应用
# 访问 https://open.feishu.cn/app 创建企业自建应用
# 获取: App ID / App Secret

# 3. 配置飞书应用权限
# 权限清单:
# - im:message:send_as_bot      (机器人发送消息)
# - im:message:read              (读取消息)
# - drive:drive:readonly        (云文档只读)
# - bitable:app:readonly        (多维表格只读)
# - calendar:calendar:readonly  (日历只读)
# - meeting:meeting:readonly    (会议只读)
# - approval:instance:readonly  (审批只读)
```

### 2.2 Codex 环境变量配置

```bash
# ~/.bashrc 或 ~/.zshrc
export FEISHU_APP_ID="cli_xxxxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export FEISHU_BASE_URL="https://open.feishu.cn/open-apis"

# 飞书租户访问令牌自动刷新 (TTL 2小时)
alias feishu-token='curl -s -X POST "${FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}" | jq -r ".tenant_access_token"'
```

### 2.3 Codex 对话方式操控飞书

```
# Codex 对话中自然语言指令示例:
用户: "帮我在飞书的项目看板里添加一条新任务：Codex 接入测试，截止明天"
Codex: [执行 feishu-cli 命令操作多维表格]

用户: "给飞书群 '技术团队' 发送今日代码提交汇总"
Codex: [拉取 git log → 格式化 → 飞书消息发送]

用户: "在飞书日历上创建明天下午3点的 Code Review 会议"
Codex: [调用飞书日历 API 创建日程]

用户: "检查飞书审批里待处理的请假申请并汇总"
Codex: [调用审批 API → 汇总 → 展示]
```

---

## 三、核心命令速查

### 3.1 飞书消息操作

```bash
# 发送文本消息到群聊
curl -X POST "${FEISHU_BASE_URL}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "oc_xxxxxxxxxxxx",
    "msg_type": "text",
    "content": "{\"text\":\"Codex 自动化测试消息\"}"
  }'

# 发送富文本卡片消息
curl -X POST "${FEISHU_BASE_URL}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "oc_xxxxxxxxxxxx",
    "msg_type": "interactive",
    "content": "{\"config\":{\"wide_screen_mode\":true},\"elements\":[{\"tag\":\"markdown\",\"content\":\"**Codex 任务报告**\"}]}"
  }'
```

### 3.2 飞书文档操作

```bash
# 创建飞书文档
curl -X POST "${FEISHU_BASE_URL}/docx/v1/documents" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title":"Codex 自动生成报告 - 2026-06-15"}'

# 追加文档内容
curl -X POST "${FEISHU_BASE_URL}/docx/v1/documents/${DOC_ID}/blocks/${BLOCK_ID}/children" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"children":[{"block_type":2,"text":{"elements":[{"text_run":{"content":"Codex自动写入内容"}}]}}]}'

# 获取文档内容
curl -X GET "${FEISHU_BASE_URL}/docx/v1/documents/${DOC_ID}/raw_content" \
  -H "Authorization: Bearer ${TOKEN}"
```

### 3.3 飞书多维表格 (Base) 操作

```bash
# 列出所有 Base
curl -X GET "${FEISHU_BASE_URL}/bitable/v1/apps" \
  -H "Authorization: Bearer ${TOKEN}"

# 列出 Base 中的表格
curl -X GET "${FEISHU_BASE_URL}/bitable/v1/apps/${APP_TOKEN}/tables" \
  -H "Authorization: Bearer ${TOKEN}"

# 批量新增记录
curl -X POST "${FEISHU_BASE_URL}/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records/batch_create" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "records":[
      {"fields":{"任务名称":"Codex接入测试","负责人":"Marvis","状态":"进行中"}},
      {"fields":{"任务名称":"飞书消息自动化","负责人":"Codex","状态":"待开始"}}
    ]
  }'

# 搜索记录 (筛选)
curl -X POST "${FEISHU_BASE_URL}/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records/search" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"filter":{"conjunction":"and","conditions":[{"field_name":"状态","operator":"is","value":["待开始"]}]}}'
```

### 3.4 飞书日历操作

```bash
# 创建日程
curl -X POST "${FEISHU_BASE_URL}/calendar/v4/calendars/${CALENDAR_ID}/events" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Codex 自动化 Code Review",
    "start_time": {"timestamp":"1718438400"},
    "end_time": {"timestamp":"1718442000"},
    "attendee_ability":"can_see_others"
  }'

# 查询日程
curl -X GET "${FEISHU_BASE_URL}/calendar/v4/calendars/${CALENDAR_ID}/events?start_time=1718438400&end_time=1718524800" \
  -H "Authorization: Bearer ${TOKEN}"
```

### 3.5 飞书会议操作

```bash
# 创建会议
curl -X POST "${FEISHU_BASE_URL}/vc/v1/meetings" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"topic":"Codex+飞书自动化方案讨论"}'

# 获取会议列表
curl -X GET "${FEISHU_BASE_URL}/vc/v1/meetings?page_size=20" \
  -H "Authorization: Bearer ${TOKEN}"

# 获取会议录制
curl -X GET "${FEISHU_BASE_URL}/vc/v1/meetings/${MEETING_ID}/recording" \
  -H "Authorization: Bearer ${TOKEN}"
```

---

## 四、自动化场景 SOP

### 4.1 场景一：GitHub 事件 → 飞书群通知

```
触发条件: GitHub Push / PR / Issue
执行流程:
  1. Codex Trigger 监听 GitHub Webhook
  2. 解析事件类型和内容
  3. Codex 生成格式化摘要
  4. 调用飞书消息 API 发送到指定群聊
  5. 记录执行日志到飞书文档

错误处理:
  - 飞书 API 超时 (5s): 重试 3 次, 指数退避
  - Token 过期: 自动刷新 Tenant Access Token
  - 频率限制 (10 QPS): 使用队列削峰

关联协议: #13事件驱动 + #95Trigger流水线 + #40状态心跳
```

### 4.2 场景二：Codex 自动生成周报 → 飞书文档

```
触发条件: 每周五 17:00 (Cron)
执行流程:
  1. Codex 拉取本周 Git 提交记录
  2. Codex 拉取 Jira/GitHub Issues 完成情况
  3. AI 生成周报内容 (Markdown)
  4. 调用飞书文档 API 创建/更新周报
  5. 发送飞书消息通知团队

关联协议: #40定时调度 + #78长时域Goal + #123多渠道网关
```

### 4.3 场景三：飞书审批 → Codex 自动处理

```
触发条件: 飞书审批单状态变更 Webhook
执行流程:
  1. 飞书审批 → Webhook 推送到 Codex
  2. Codex 解析审批内容 (请假/报销/采购)
  3. 根据规则自动审批或拒绝 (金额阈值判断)
  4. 调用飞书审批 API 提交结果
  5. 大额审批 → Codex 生成分析报告 → 飞书消息通知管理者

安全约束:
  - 自动审批上限: ¥500/单
  - 敏感审批 (离职/权限变更): 强制人工
  - 完整审计日志写入飞书文档

关联协议: #95事件驱动 + #93锁屏远程审批 + #206运行时全栈安全
```

### 4.4 场景四：锁屏无人值守 → 飞书远程指令

```
触发条件: 用户通过飞书发送指令到机器人
执行流程:
  1. 飞书机器人接收指令 (自然语言)
  2. 飞书 → OpenClaw Gateway (协议#123) → Codex
  3. Codex 在锁屏状态下执行桌面操作
  4. 完成 → 飞书消息返回结果 (含 Appshots 截图)
  5. 失败 → 飞书消息通知 + 等待远程指令重试

支持指令:
  - "帮我重启 VNPY 量化程序"
  - "检查 Codex 策略进程是否运行"
  - "更新 E 盘技能库文件"
  - "截图当前桌面发送给我"

关联协议: #93锁屏远程操控 + #79Appshots注入 + #172桌面视觉操控v3
```

### 4.5 场景五：Codex 定时巡检 → 飞书多维表格

```
触发条件: 每 2 小时 (Cron)
执行流程:
  1. Codex 执行系统巡检 (进程/磁盘/网络/服务)
  2. 检查关键服务: VNPY / Memos / Hermes / OpenClaw
  3. 异常 → 飞书消息紧急通知
  4. 正常 → 飞书多维表格追加巡检记录
  5. 每周汇总 → 飞书文档生成运维周报

关联协议: #40状态心跳 + #223腾讯效率工具集 + #211状态漂移自检
```

---

## 五、权限配置与安全

### 5.1 飞书应用权限最小化原则

```
必需权限 (P0):
  - im:message:send_as_bot        机器人消息发送
  - im:message.p2p:send_as_bot   机器人私聊

可选权限 (按需):
  - drive:drive:readonly         文档只读
  - bitable:app:readonly         Base 只读
  - calendar:calendar:readonly   日历只读
  - approval:instance:readonly   审批只读
  - meeting:meeting:readonly     会议只读

禁止权限:
  - contact:contact:write        通讯录写入
  - admin:admin:write            管理后台写入
  - 任何带有 delete 的权限
```

### 5.2 Token 安全管理

```bash
# 1. Token 保存到环境变量 (不要硬编码!)
export FEISHU_TOKEN=$(feishu-token)

# 2. Token 自动刷新脚本 (crontab)
# 每 90 分钟刷新一次 (TTL 120分钟)
*/90 * * * * /usr/local/bin/feishu-token-refresh.sh

# 3. 敏感信息加密存储
# 使用 .env 文件, 加入 .gitignore
echo ".env" >> .gitignore
echo ".feishu_token" >> .gitignore

# 4. 凭证隔离 (协议#208 MCP供应链纵深防御)
# 飞书凭证与 Codex 其他凭证物理隔离
```

### 5.3 MCP 安全纵深

```
关联协议:
  #208 MCP工具供应链纵深防御 v1.0
  #227 MCP生态供应链纵深防御与配置完整性 v1.0
  #237 后量子MCP安全抗性 v1.0

Codex ↔ 飞书 安全通道:
  L1: Token 签名校验 (HMAC-SHA256)
  L2: IP 白名单 (飞书开放平台配置)
  L3: 请求频率限制 (10 QPS)
  L4: 行为审计日志 (全量记录)
  L5: 异常熔断 (连续 5 次失败自动停用)
```

---

## 六、错误处理与容错

### 6.1 常见错误码

| 错误码 | 含义 | 处理方式 |
|:---:|------|------|
| 99991663 | Tenant Access Token 过期 | 自动刷新 Token |
| 99991664 | 频率限制 | 队列排队 + 指数退避 |
| 99991668 | App 未开通对应权限 | 提示用户授权 |
| 99991672 | 消息内容超长 | 分段发送或上传为文档 |
| 99991673 | 群聊未添加机器人 | 提示先加机器人进群 |
| 10003 | 网络超时 | 重试 3 次, 间隔 1s/3s/5s |

### 6.2 容错策略

```
1. Token 缓存: 本地缓存 + 过期前 5 分钟自动刷新
2. 重试机制: 指数退避 (1s → 3s → 5s → 放弃)
3. 降级策略: 消息发送失败 → 内容暂存本地 → 下次成功补发
4. 熔断机制: 连续 5 次失败 → 暂停 5 分钟 → 自动恢复
5. 审计日志: 所有操作记录到本地 + 飞书文档双备份

关联协议:
  #24 自愈回滚检查点 v1.0
  #211 Agent长时间运行状态漂移自检 v1.0
  #212 跨会话任务中断恢复 v1.0
```

---

## 七、部署检查清单

```
[ ] Codex CLI 版本 ≥ v0.135.0
[ ] 飞书开放平台 App 创建完成
[ ] App ID / App Secret 已获取
[ ] 必需权限已授权 (im:message:send_as_bot)
[ ] Token 自动刷新脚本已配置
[ ] .env 文件已加入 .gitignore
[ ] 飞书机器人已添加到目标群聊
[ ] Webhook URL 已配置到飞书开放平台
[ ] 本地 crontab 定时任务已设定
[ ] 审计日志路径已配置
[ ] 异常熔断阈值已设定
[ ] Codex /goal 长时域任务已创建
[ ] 桌面锁屏持续运行已配置 (Codex Locked CU)
```

---

## 八、关联模板协议总览

| # | 协议 | 在本技能手册的关联 |
|:---:|------|------|
| #13 | 事件驱动自动化流水线 v1.0 | 飞书 Webhook → Codex Trigger |
| #24 | 自愈回滚检查点 v1.0 | 飞书 API 调用失败自动恢复 |
| #40 | 有状态心跳自主调度 v1.0 | Codex 定时巡检 → 飞书通知 |
| #53 | Windows桌面视觉操控 v1.0 | Codex 操控飞书桌面端 |
| #78 | 长时域Goal任务推进 v1.0 | 代码仓库 → 飞书 OKR 同步 |
| #79 | Appshots上下文快照注入 v1.0 | 飞书收截图 → Codex 分析 |
| #93 | 锁屏远程移动Agent操控 v1.0 | 手机飞书 → Codex 远程执行 |
| #95 | 事件驱动Trigger自动化 v1.0 | Codex Trigger → 飞书通知 |
| #123 | 多渠道Gateway桥接 v1.0 | 飞书/微信/钉钉统一路由 |
| #172 | 桌面全平台视觉操控 v3.0 | Codex Win CU + 飞书桌面 |
| #188 | 超级应用Agent融合 v1.0 | Codex+ChatGPT + 飞书生态 |
| #206 | Agent运行时全栈纵深防御 v1.0 | 飞书API五层安全防线 |
| #208 | MCP工具供应链纵深防御 v1.0 | 飞书凭证隔离 |
| #211 | 状态漂移自检 v1.0 | 飞书巡检异常检测 |
| #212 | 跨会话中断恢复 v1.0 | 飞书任务断点续传 |
| #223 | 腾讯效率智能体工具集 v1.0 | 飞书企业平台对标 |
| #227 | MCP配置完整性校验 v1.0 | Token/凭证完整性 |
| #237 | 后量子MCP安全抗性 v1.0 | 飞书通信加密升级 |

---

> 版本: v1.0 | 模板版本: v3.94 | 协议覆盖: 18/254 项
> 作者: 龙虾全域自进化系统 | 生成: 2026-06-15 定时任务
