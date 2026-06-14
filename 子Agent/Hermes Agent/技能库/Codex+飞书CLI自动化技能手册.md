# Codex + 飞书CLI自动化技能手册

> 版本：v1.0 | 生成日期：2026-06-14 | 来源：公众号文章 + 全网开源项目调研

---

## 一、概述

飞书于2026年3月底正式开源CLI工具（lark-cli），覆盖即时通讯、云文档、多维表格、日历、会议、邮箱、任务、知识库等11大业务域，提供200+命令和19个Agent Skills。Codex CLI作为OpenAI推出的AI编程助手，可与飞书CLI深度集成，实现"一句话操作飞书全量数据"的自动化能力。

本手册系统梳理Codex+飞书CLI的集成方案、核心命令、权限配置与自动化场景，形成标准化SOP。

---

## 二、飞书CLI核心能力矩阵

### 2.1 11大业务域

| 业务域 | 核心能力 | 典型命令 |
|--------|---------|---------|
| 即时通讯 | 消息收发、群管理、机器人交互 | `lark im send` `lark im list` |
| 云文档 | 创建/编辑/搜索文档 | `lark doc create` `lark doc search` |
| 云空间 | 文件管理、知识库操作 | `lark drive upload` `lark drive list` |
| 电子表格 | 表格读写、公式计算 | `lark sheet read` `lark sheet write` |
| 多维表格 | 数据CRUD、视图管理 | `lark base query` `lark base insert` |
| 日历 | 日程查询、创建会议 | `lark calendar list` `lark calendar create` |
| 视频会议 | 创建/管理会议 | `lark meeting create` `lark meeting list` |
| 邮箱 | 邮件收发 | `lark mail send` `lark mail list` |
| 任务 | 任务创建/分配/跟踪 | `lark task create` `lark task list` |
| 知识库 | 知识管理、搜索 | `lark wiki search` `lark wiki create` |
| 通讯录 | 部门/用户查询 | `lark contact search` |

### 2.2 飞书CLI安装与配置

```bash
# 安装飞书CLI
git clone https://github.com/larksuite/cli.git
cd cli
npm install -g

# 验证安装
lark --version

# 配置凭证（需要飞书开放平台 App ID 和 App Secret）
lark config set appId cli_xxxxxxxxxxxxx
lark config set appSecret xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 三、Codex + 飞书集成方案

### 3.1 方案一：飞书CLI直接集成（推荐）

最直接的集成方式——通过飞书CLI让Codex直接操作飞书数据。

```bash
# 在Codex中直接使用飞书CLI命令
codex exec "用飞书CLI帮我查一下今天的日程"
codex exec "帮我在飞书创建一个明天下午3点的会议"
codex exec "读取飞书多维表格中的销售数据并生成汇总报告"
```

**Codex上下文注入方式**：
1. 将飞书CLI的GitHub README链接发给Codex，让其自动安装
2. 提供App ID和App Secret给Codex完成配置
3. Codex自动完成权限申请和授权流程

### 3.2 方案二：feishu-codex-bridge（长连接桥接）

通过飞书长连接实现双向通信，手机上即可操控本地Codex。

```bash
# 克隆仓库
git clone https://github.com/lutianding118-cmd/feishu-codex-bridge.git
cd feishu-codex-bridge
npm install

# 配置 .env
FEISHU_APP_ID=你的飞书App ID
FEISHU_APP_SECRET=你的飞书App Secret
FEISHU_VERIFICATION_TOKEN=
BRIDGE_PORT=3457
BRIDGE_AUTH_CODE=123456
DEFAULT_WORKSPACE_DIR=D:\workspace
CODEX_COMMAND=codex
TASK_HEARTBEAT_MS=60000
FEISHU_MESSAGE_MODE=direct

# 启动
npm start
```

**核心特性**：
- 群=项目：每个群绑定一个本地目录
- 话题=会话：话题内连续Codex会话（自动resume）
- 流式卡片：推理/命令/文件改动实时刷新
- 免@对话：话题内直接说话

### 3.3 方案三：Agent Notifier（远程操控）

将Claude Code和Codex CLI的交互搬到飞书，手机上批准权限、选择方案。

```bash
git clone https://github.com/KaminDeng/agent_notifier.git
cd agent_notifier
# 按README配置飞书应用并启动
```

**核心特性**：
- 飞书卡片实时推送权限确认
- 方案选择交互式卡片
- 多终端并行路由，互不干扰
- 支持输入框自由回复

### 3.4 方案四：modelzen/feishu-codex-bridge（增强版）

功能最丰富的桥接方案。

```bash
git clone https://github.com/modelzen/feishu-codex-bridge.git
cd feishu-codex-bridge
npm install

# 配置 config.json
{
  "appId": "cli_xxxxx",
  "appSecret": "xxxxx",
  "webhookUrl": "https://open.feishu.cn/...",
  "allowedOpenIds": ["ou_xxxxx"],
  "codexCommand": "codex",
  "workingDir": "D:\\workspace",
  "mode": "tui",
  "outputSource": "session"
}

npm start
```

**增强特性**：
- 文档评论回复（飞书云文档评论@机器人直接驱动Codex）
- 私聊控制台（管理面板：新建项目/列表/设置/诊断）
- Codex用量统计（5小时/7天限额进度、热力图）
- 战绩分享卡（可转发到任意群）
- AES-256-GCM加密密钥库
- 跨平台后台服务（macOS lauchd / Windows登录自启 / Linux systemd）

---

## 四、飞书开放平台权限配置

### 4.1 创建飞书自建应用

```
1. 登录飞书开放平台 → 应用管理 → 创建应用 → 企业自建应用
2. 填写应用名称（如"Codex助手"）
3. 启用机器人能力
4. 记录 App ID 和 App Secret
```

### 4.2 权限配置清单

| 权限代码 | 权限说明 | 用途 |
|---------|---------|------|
| im:message | 获取与发送单聊、群聊消息 | 消息收发核心 |
| im:message:send_as_bot | 以应用身份发送消息 | 机器人主动推送 |
| im:resource | 获取消息中的资源文件 | 文件操作 |
| drive:drive | 访问云空间 | 文件管理 |
| doc:doc | 云文档读写 | 文档操作 |
| calendar:calendar | 日历读写 | 日程管理 |
| contact:contact | 通讯录访问 | 用户查询 |
| bitable:app | 多维表格操作 | 数据管理 |
| meeting:meeting | 会议管理 | 创建会议 |

### 4.3 事件订阅配置

| 事件 | 说明 |
|------|------|
| im.message.receive_v1 | 接收消息（核心事件） |
| im.message.reaction.created_v1 | 消息反应创建 |
| drive.file.read_v1 | 文件读取事件 |

**推荐使用长连接模式**：无需公网IP，本机直连飞书服务器。

---

## 五、自动化场景SOP

### 5.1 场景一：每日早报自动推送

```bash
# 通过Codex调用飞书CLI生成并推送每日早报
codex exec "用飞书CLI执行以下操作：
1. 查询我今天的所有日程
2. 读取团队多维表格中本周的任务列表
3. 查看未读重要消息
4. 将以上信息汇总成早报，发送到「每日早报」飞书群"
```

### 5.2 场景二：会议纪要自动生成

```bash
codex exec "用飞书CLI帮我：
1. 读取今天下午会议的相关飞书文档
2. 提取关键讨论点
3. 创建一份会议纪要文档
4. 发送链接到项目群"
```

### 5.3 场景三：数据报表自动处理

```bash
codex exec "用飞书CLI执行：
1. 读取多维表格「销售数据」本月所有记录
2. 按地区和产品线汇总
3. 生成分析报告并写入飞书文档
4. 发送汇总消息到「销售团队」群"
```

### 5.4 场景四：任务自动化分配

```bash
codex exec "用飞书CLI执行：
1. 读取多维表格「需求池」中未分配的需求
2. 根据成员工作负载自动分配
3. 为每个新任务设置截止日期
4. 飞书私聊通知相关人员"
```

### 5.5 场景五：知识库智能检索

```bash
codex exec "用飞书CLI搜索知识库中关于「微服务架构」的所有文档，提取关键设计模式和最佳实践，汇总成一份技术指南"
```

### 5.6 场景六：消息智能分流与自动回复

```bash
# 通过bridge监听飞书消息，Codex自动处理
# 在feishu-codex-bridge中配置自动回复规则
codex exec "监控飞书群消息，当检测到包含'bug'关键词的消息时，
自动在飞书多维表格创建issue记录，并回复处理进度卡片"
```

---

## 六、错误处理与故障排查

### 6.1 常见错误

| 错误现象 | 原因 | 解决方案 |
|---------|------|---------|
| "Connected to Feishu WebSocket" 不出现 | 飞书应用未发布/未安装 | 检查飞书开放平台应用状态 |
| 推送乱码/碎字符 | mode设置不当 | 使用 `mode: "tui"` + `outputSource: "session"` |
| Codex进程卡死 | 任务超时 | 配置watchdog自动终止（默认120s） |
| 长连接断开 | 网络波动 | bridge内置自动重连机制 |
| 权限不足 | 飞书应用权限未开通 | 检查权限管理页面补充授权 |
| 消息不推送 | 机器人未被添加进会话 | 将机器人拉入目标群聊/私聊 |

### 6.2 调试命令

```bash
# 检查飞书CLI状态
lark --version
lark config list

# 检查Codex状态
codex --version

# 查看bridge日志（如开启debugLogs）
tail -f ~/.feishu-codex-bridge/logs/app.log

# 测试飞书连接
lark im send --receive_id ou_xxxxx --msg_type text --content '{"text":"测试连接"}'
```

---

## 七、安全最佳实践

### 7.1 凭证管理

```
- 飞书App Secret使用AES-256-GCM加密存储（~/.feishu-codex-bridge/）
- 不将凭证写入环境变量或代码仓库
- 定期轮换App Secret
```

### 7.2 访问控制

```
- allowedOpenIds白名单机制：仅授权用户可控制CLI
- 群隔离：每个群绑定独立工作目录
- 会话隔离：每个话题独立Codex进程
- 敏感操作二次确认（删除/修改核心数据）
```

### 7.3 数据保护

```
- 本地加密密钥库不入仓库
- 飞书消息传输使用TLS加密
- 调试日志默认关闭，生产环境禁用debugLogs
```

---

## 八、技能库扩充建议

### 8.1 需新增的Agent Skills

| 技能名称 | 功能 | 优先级 |
|---------|------|:---:|
| feishu-message-sender | 飞书消息发送 | 🔴 高 |
| feishu-doc-creator | 飞书文档创建与编辑 | 🔴 高 |
| feishu-calendar-manager | 飞书日程管理 | 🟡 中 |
| feishu-bitable-operator | 飞书多维表格CRUD | 🔴 高 |
| feishu-meeting-organizer | 飞书会议组织 | 🟡 中 |
| feishu-wiki-searcher | 飞书知识库检索 | 🟡 中 |
| codex-bridge-manager | Codex桥接管理 | 🔴 高 |

### 8.2 与龙虾全域模板的对接

```
- 飞书CLI操作 → 协议#127 桌面全平台操控
- Codex集成 → 协议#240 超级Agent融合
- 飞书桥接安全 → 协议#246 七维纵深防御
- 自动化执行 → 协议#238 自进化闭环v6.1
```

---

## 九、参考资源

| 资源 | 地址 |
|------|------|
| 飞书CLI官方仓库 | https://github.com/larksuite/cli |
| Codex CLI官方文档 | https://codexguide.ai |
| feishu-codex-bridge | https://github.com/lutianding118-cmd/feishu-codex-bridge |
| modelzen增强bridge | https://github.com/modelzen/feishu-codex-bridge |
| Agent Notifier | https://github.com/KaminDeng/agent_notifier |
| 飞书开放平台 | https://open.feishu.cn |
| Codex × 飞书CLI教程 | https://codexguide.ai/recipes/feishu-cli-codex.html |

---

*（内容由AI生成，基于公众号文章+全网开源项目调研，仅供参考）*
