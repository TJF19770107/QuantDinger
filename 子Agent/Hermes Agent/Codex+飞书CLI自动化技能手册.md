# Codex + 飞书CLI自动化技能手册 v1.0

> 生成时间：2026-06-14 14:00 CST
> 来源：飞书官方CLI开源文档 + Codex CLI对接实操 + 龙虾全域模板迭代沉淀
> 协议编号：技能池SOP-007

---

## 一、概述

飞书于2026年4月1日正式开源CLI工具 `lark-cli`，将飞书11大业务域、200+命令、19个Agent Skills全面向AI Agent开放。这使得Codex、Claude Code、Cursor、OpenClaw等AI工具可以直接通过命令行操控飞书：发消息、创建会议、写文档、更新多维表格、管理日历、发送邮件、处理任务——全程无需人工复制粘贴。

本手册提炼标准化操作步骤（SOP），覆盖安装配置、核心命令、权限管理、自动化场景、错误处理与安全边界。

---

## 二、环境准备

### 2.1 前置依赖

| 依赖 | 要求 | 检查命令 |
|------|------|---------|
| Node.js | >= 16.x | `node --version` |
| npm | >= 8.x | `npm --version` |
| Codex CLI | 已安装 | `codex --version` |
| 飞书账号 | 个人或企业均可 | — |

### 2.2 安装飞书CLI

```bash
# 全局安装飞书CLI
npm install -g @larksuite/cli

# 安装Agent Skills（必需）
npx skills add larksuite/cli -y -g
```

### 2.3 配置与授权

```bash
# 初始化配置并创建新应用（跳过交互菜单）
lark-cli config init --new

# 用户登录（推荐权限模式，自动审批无需管理员审核）
lark-cli auth login --recommend
```

授权流程：
1. `config init --new` 输出授权链接
2. 浏览器打开链接 → 飞书扫码登录 → 点击「同意授权」
3. `auth login --recommend` 仅申请推荐权限，不触发管理员审核

### 2.4 验证安装

```bash
lark-cli --version          # 查看版本号
lark-cli auth status         # 查看登录状态
```

---

## 三、三层命令架构

飞书CLI设计了三层命令架构，日常使用只需第一层：

### 3.1 第一层：Shortcuts（带 + 前缀）

高频操作封装，带智能默认值、风险验证、格式化输出。

```bash
# 日程
lark-cli calendar +agenda                  # 查看今日日程
lark-cli calendar +meeting-create ...      # 创建会议

# 消息
lark-cli im +messages-send ...             # 发送消息
lark-cli im +messages-search ...           # 搜索消息

# 文档
lark-cli docs +create ...                  # 创建文档
lark-cli docs +update ...                  # 更新文档
```

### 3.2 第二层：API Commands

与飞书开放平台API端点一一对应，自动从平台元数据生成。

```bash
lark-cli api im.message.list               # 获取消息列表
lark-cli api calendar.event.list            # 获取日历事件列表
```

### 3.3 第三层：Raw API Access

完整暴露飞书2500+ API端点。

```bash
lark-cli raw POST /open-apis/im/v1/messages
```

---

## 四、11大业务域能力矩阵

| 域 | 模块名 | 核心能力 | Shortcut示例 |
|---|--------|---------|-------------|
| 即时通讯 | `lark-im` | 消息发送/回复、群聊管理、消息搜索、文件发送 | `+messages-send` |
| 云文档 | `lark-doc` | 文档创建/读取/更新、Markdown支持、评论协作 | `+docs-create` |
| 多维表格 | `lark-base` | 字段/记录/视图/仪表盘操作 | `+base-records-query` |
| 日历 | `lark-calendar` | 日程查询、会议创建、闲忙查询、时间推荐 | `+agenda` |
| 邮件 | `lark-mail` | 邮件读取/发送/回复/归档 | `+mail-send` |
| 任务 | `lark-task` | 任务创建/更新/子任务管理 | `+task-create` |
| 会议 | `lark-meeting` | 会议创建/参会人管理/录制 | `+meeting-create` |
| 知识库 | `lark-wiki` | 知识空间/页面节点管理 | `+wiki-create` |
| 云空间 | `lark-drive` | 文件上传/下载/管理 | `+drive-upload` |
| 审批 | `lark-approval` | 审批实例查询/创建 | `+approval-query` |
| OKR | `lark-okr` | 目标/关键结果管理 | `+okr-query` |

---

## 五、19个内置Agent Skills

| # | Skill名称 | 功能描述 |
|---|----------|---------|
| 1 | `feishu-send-message` | 发送飞书消息 |
| 2 | `feishu-send-file` | 发送文件（非纯文本） |
| 3 | `feishu-create-doc` | 创建飞书云文档 |
| 4 | `feishu-update-doc` | 更新飞书云文档内容 |
| 5 | `feishu-read-doc` | 读取飞书云文档 |
| 6 | `feishu-create-meeting` | 创建飞书会议 |
| 7 | `feishu-query-calendar` | 查询飞书日历 |
| 8 | `feishu-send-mail` | 发送飞书邮件 |
| 9 | `feishu-create-task` | 创建飞书任务 |
| 10 | `feishu-query-base` | 查询多维表格 |
| 11 | `feishu-update-base` | 更新多维表格记录 |
| 12 | `feishu-search-messages` | 搜索飞书消息 |
| 13 | `feishu-upload-file` | 上传文件到飞书云空间 |
| 14 | `feishu-create-wiki` | 创建知识库页面 |
| 15 | `feishu-query-approval` | 查询审批实例 |
| 16 | `feishu-create-approval` | 发起审批 |
| 17 | `feishu-read-mail` | 读取邮件 |
| 18 | `feishu-meeting-record` | 妙记录制转文字 |
| 19 | `feishu-okr-report` | OKR进度报告 |

---

## 六、Codex CLI对接SOP（标准操作流程）

### 6.1 一键安装脚本（Codex内执行）

在Codex终端中粘贴以下内容，Codex将自动执行完整安装流程：

```
请立刻帮我安装飞书官方CLI (lark-cli)，让我可以直接操作飞书和飞书文档。
请严格按顺序执行以下步骤：
1. 运行命令：npm install -g @larksuite/cli
2. 运行命令：npx skills add larksuite/cli -y -g
3. 运行命令：lark-cli config init --new （这一步会输出授权链接，请把链接发给我，我会在浏览器里完成飞书授权）
4. 运行命令：lark-cli auth login --recommend （同样会输出授权链接，请发给我授权）
安装完成后，告诉我"安装完成"，并显示 lark-cli --version 和 lark-cli auth status 的结果。
```

### 6.2 授权关键点

- **安全确认**：授权必须由人手动在浏览器中扫码确认
- **最小权限**：`--recommend` 仅申请推荐权限（自动审批），避免权限过大
- **身份模式**：用户身份模式可访问日历、私信等个人数据，不授权模式仅执行基础操作

### 6.3 典型工作流示例

**场景1：每日SEO/GEO检查提醒**

```bash
# 1. 查询今日日程
lark-cli calendar +agenda

# 2. 检查是否有空闲时段
lark-cli calendar +freebusy --start "2026-06-14T09:00" --end "2026-06-14T18:00"

# 3. 发送提醒消息
lark-cli im +messages-send --content "每日SEO/GEO检查提醒：请检查主博客的搜索引擎优化状态" --type text
```

**场景2：会议纪要自动生成与分发**

```bash
# 1. 读取妙记录制内容
lark-cli meeting +record-transcript --meeting-id "xxx"

# 2. 提取关键待办项
# （LLM处理）

# 3. 创建会议纪要文档
lark-cli docs +create --title "周例会纪要-20260614" --content "# 周例会纪要\n\n..."

# 4. 分配任务
lark-cli task +create --title "跟进客户需求" --assignee "张三"
```

**场景3：多维表格自动化数据分析**

```bash
# 1. 查询表格数据
lark-cli base +records-query --table-id "xxx" --filter "状态=待处理"

# 2. 批量更新记录
lark-cli base +records-update --table-id "xxx" --data '[{"record_id":"x","fields":{"状态":"已完成"}}]'
```

---

## 七、输出格式与参数

### 7.1 输出格式

```bash
lark-cli --output json       # JSON输出
lark-cli --output ndjson     # NDJSON输出
lark-cli --output table      # 表格输出
lark-cli --output csv        # CSV输出
lark-cli --output pretty     # 美化输出（默认）
```

### 7.2 分页处理

```bash
lark-cli --page-all          # 自动获取全量数据
lark-cli --page-size 50      # 自定义页大小
```

### 7.3 安全预览

```bash
lark-cli --dry-run           # 预览操作，不实际执行（破坏性操作建议先dry-run）
```

---

## 八、安全边界与权限模型

### 8.1 凭证存储

飞书CLI使用操作系统原生Keychain存储凭证，不将Token写入文件系统明文。

### 8.2 注入防护

- 输入注入保护：CLI自动过滤特殊字符/命令注入
- 终端输出脱敏：敏感信息（Token/私钥）不会在终端显示
- `--dry-run` 预览：所有破坏性操作支持预览模式

### 8.3 权限分级

| 模式 | 权限范围 | 适用场景 |
|------|---------|---------|
| 不授权模式 | 基础操作（公开信息） | 简单查询、公开文档读取 |
| 用户推荐权限（--recommend） | 个人数据（日历/消息/文档） | 个人办公自动化 |
| 管理员权限 | 企业全量数据 | 企业级自动化、批量管理 |

### 8.4 龙虾全域模板安全对齐

- 权限最小化原则 → 对应龙虾协议#246（七维纵深防御）
- 凭据禁造原则 → 对应龙虾协议#201
- `--dry-run` 安全预览 → 对应龙虾协议#247（操作前验证）
- 注入防护 → 对应龙虾协议#235（MCP安全）

---

## 九、错误处理与故障排查

### 9.1 常见错误

| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| `AUTH_EXPIRED` | Token过期 | `lark-cli auth login --recommend` 重新登录 |
| `PERMISSION_DENIED` | 权限不足 | 检查当前权限模式，必要时升级为管理员权限 |
| `RATE_LIMITED` | 触发频率限制 | 添加延迟重试，使用 `--page-size` 减少单次请求量 |
| `NETWORK_ERROR` | 网络连接失败 | 检查网络，确认飞书服务状态 |
| `INVALID_PARAM` | 参数错误 | 使用 `lark-cli <command> --help` 查看正确参数格式 |
| `CONFIG_MISSING` | 配置未初始化 | `lark-cli config init --new` 重新初始化 |

### 9.2 调试模式

```bash
lark-cli --debug           # 开启调试日志
lark-cli --verbose         # 详细输出
```

---

## 十、龙虾全域技能池注册

本技能手册已纳入龙虾全域技能池，注册信息如下：

| 字段 | 值 |
|------|-----|
| 技能编号 | SOP-007 |
| 技能名称 | Codex + 飞书CLI自动化 |
| 所属域 | 桌面自动化 / 办公协作 |
| 覆盖协议 | #238(自进化闭环) / #246(纵深防御) / #247(任务持久化) |
| 依赖工具 | Node.js >= 16 / npm / @larksuite/cli |
| 安全定级 | 🟡 中风险（涉及个人数据访问和消息发送） |
| 跨平台 | Windows / macOS / Linux |
| 更新频率 | 随飞书CLI版本同步更新 |

---

## 十一、自动化场景扩展模板

| 场景 | 触发条件 | CLI命令组合 | 产出 |
|------|---------|-----------|------|
| 每日站会纪要 | 定时触发 | `+agenda` → LLM提炼 → `+docs-create` → `+messages-send` | 飞书文档+消息推送 |
| 客户需求跟进 | 新消息含"需求"关键词 | `+messages-search` → LLM分析 → `+task-create` | 飞书任务分配 |
| 周报自动生成 | 每周五18:00 | `+base-records-query` → LLM汇总 → `+docs-create` → `+mail-send` | 邮件发送周报 |
| 会议语音转文字 | 会议结束 | `+record-transcript` → LLM总结 → `+docs-create` | 会议纪要文档 |
| 审批流程跟踪 | 定时扫描 | `+approval-query` → 滞期提醒 → `+messages-send` | 消息催办 |

---

*（内容由AI生成，基于飞书官方CLI文档及Codex实操记录）*
