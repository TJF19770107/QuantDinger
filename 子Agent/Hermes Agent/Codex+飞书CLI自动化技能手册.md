# Codex+飞书CLI自动化技能手册

> 基于龙虾全域官方模板 v3.79 Final · 协议#188/#196/#240 知识提炼
> 生成日期：2026-06-18
> 版本：v5.0
> 来源：模板内部知识提炼（公众号文章微信反爬，不再重试）

---

## 一、概述

Codex+飞书CLI联合自动化是「思考(ChatGPT)+执行(Codex)」统一入口范式下的关键办公自动化能力。通过 Codex CLI 调度飞书 lark-cli，实现自然语言到飞书全系办公操作的零代码自动化闭环。

**三层架构**：
```
自然语言 → Codex CLI（思考翻译） → 飞书 lark-cli（执行层） → 飞书开放平台 API
```

**核心价值**：覆盖近10亿 Codex 用户的飞书全系办公能力，从对话直接驱动文档/表格/消息/日历/会议/邮件/审批等11大业务域。

---

## 二、Codex CLI 核心能力矩阵

### 2.1 Codex 超级应用架构

| 组件 | 说明 | 协议关联 |
|------|------|---------|
| ChatGPT（思考层） | 自然语言理解、任务规划、上下文推理 | #188 超级应用Agent融合 |
| Codex（执行层） | CLI调度、工具调用、沙箱执行、输出验证 | #240 超级Agent融合 |
| Agent Plugins | 6角色110技能 → 8角色146技能+80企业应用 | #196 超级应用合体 |
| Annotations | 人-Agent实时协作批注编辑 | #188 |
| Sites | 自然语言一键生成可交互Web应用 | #188 |

### 2.2 Codex CLI 核心命令

| 命令 | 功能 | 关键参数 |
|------|------|---------|
| `codex login` | OAuth登录认证 | — |
| `codex init` | 初始化项目上下文 | — |
| `codex session` | 管理会话 | `--resume` 恢复上次会话 |
| `codex task` | 执行单次任务 | `--json` JSON输出, `--output-schema` 结构化输出 |
| `codex submit` | 提交异步任务 | `--background` 后台执行 |
| `codex resume` | 恢复任务 | `--last` 最近一个任务 |
| `codex plugins` | 管理插件 | `list/install/uninstall` |
| `codex doctor` | 环境诊断 | — |
| `codex schema` | 查看输出结构 | — |

### 2.3 Codex 权限模式

| 模式 | 说明 | 风险等级 | 适用场景 |
|------|------|:---:|------|
| `suggest` | 仅建议，不执行 | 🟢 低 | 学习/探索 |
| `auto-edit` | 自动编辑文件 | 🟡 中 | 日常开发 |
| `full-auto` | 全自动执行 | 🟡 中 | CI/CD |
| `yolo` | 无需确认全自动 | 🔴 高 | 受控沙箱环境 |

### 2.4 Codex CI 非交互模式

```bash
# JSON结构化输出
codex task "分析飞书文档" --json --output-schema '{"summary":"string","actions":"array"}'

# 恢复最近会话
codex resume --last

# 指定模型
codex task "创建飞书多维表格" --model gpt-5.1-codex

# 指定权限模式
codex task "批量发送飞书消息" --permission-mode full-auto
```

---

## 三、飞书 CLI 自动化操作

### 3.1 安装与授权

```bash
# 零配置安装（推荐：直接把README丢给Codex）
npm install -g @larksuite/cli

# 国内镜像加速
npm install -g @larksuite/cli --registry=https://registry.npmmirror.com

# 添加Agent Skills
npx skills add larksuite/cli -y -g

# OAuth 2.0 设备流授权
lark-cli auth login --recommend
```

### 3.2 三种接入模式

| 模式 | 授权方式 | 安全等级 | 说明 |
|------|---------|:---:|------|
| 不授权 | 无需飞书账号 | 🟢 低 | 仅查看公开文档 |
| 应用身份 | create_application OAuth | 🟡 中 | 生产环境推荐 |
| 用户身份 | request_user OAuth | 🟡 中 | 需用户授权 |

### 3.3 三层命令体系

飞书 lark-cli 提供三层抽象：

| 层级 | 说明 | 示例 |
|------|------|------|
| **快捷命令** | `+` 前缀，自然语言风格 | `lark-cli docs +create --title "周报"` |
| **API命令** | 直接映射飞书API | `lark-cli docs create --title "周报" --content file.md` |
| **通用API** | 调用任意飞书开放平台API | `lark-cli api /open-apis/docx/v1/documents` |

### 3.4 11大业务域命令速查

#### 3.4.1 云文档（lark-doc）

| 命令 | 说明 |
|------|------|
| `lark-cli docs +create` | 创建文档 |
| `lark-cli docs create --title "标题" --content file.md` | 从Markdown创建文档 |
| `lark-cli docs +read --id doc_id` | 读取文档内容 |
| `lark-cli docs +update --id doc_id --content file.md` | 更新文档 |
| `lark-cli docs +list` | 列出文档列表 |
| `lark-cli docs +search --keyword "关键词"` | 搜索文档 |

#### 3.4.2 多维表格（lark-base）

| 命令 | 说明 |
|------|------|
| `lark-cli base +query --app-token <token> --table-id <tid>` | 查询记录 |
| `lark-cli base record-create --app-token <token> --table-id <tid> --data records.json` | 批量创建记录 |
| `lark-cli base +add --app-token <token> --table-id <tid> --data '{...}'` | 添加单条记录 |
| `lark-cli base +update --app-token <token> --table-id <tid> --data '{...}'` | 更新记录 |
| `lark-cli base +table-list --app-token <token>` | 列出工作表 |

#### 3.4.3 消息与群组（lark-im）

| 命令 | 说明 |
|------|------|
| `lark-cli im +chat-search --keyword "群名"` | 搜索群组 |
| `lark-cli im +messages-send --chat-id <id> --content "消息"` | 发送消息 |
| `lark-cli im +messages-search --chat-id <id> --keyword "关键词"` | 搜索历史消息 |
| `lark-cli im +messages-list --chat-id <id>` | 获取消息列表 |
| `lark-cli im +chat-members --chat-id <id>` | 获取群成员 |
| `lark-cli im +chat-create --name "群名" --user-ids id1,id2` | 创建群组 |

#### 3.4.4 日历（lark-calendar）

| 命令 | 说明 |
|------|------|
| `lark-cli calendar +agenda` | 查看今日日程 |
| `lark-cli calendar +create --summary "主题" --start-time "..." --end-time "..."` | 创建日程 |
| `lark-cli calendar +freebusy --user-id <id>` | 查询忙闲 |
| `lark-cli calendar +suggestion --attendees id1,id2` | 推荐空闲时段 |
| `lark-cli calendar event-create --summary "项目评审" --start-time "2026-06-19T10:00:00+08:00" --end-time "2026-06-19T11:00:00+08:00" --attendees user_id1,user_id2` | 创建事件并邀请 |

#### 3.4.5 视频会议（lark-vc）

| 命令 | 说明 |
|------|------|
| `lark-cli vc +search --keyword "项目"` | 搜索会议 |
| `lark-cli vc +minutes --meeting-id <id>` | 获取会议纪要 |
| `lark-cli vc +create --topic "主题"` | 创建会议 |
| `lark-cli vc minutes-get --meeting-id <id>` | 提取会议详情 |

#### 3.4.6 邮件（lark-mail）

| 命令 | 说明 |
|------|------|
| `lark-cli mail +triage` | 邮件智能分类 |
| `lark-cli mail +send --to addr --subject "主题" --body "内容"` | 发送邮件 |
| `lark-cli mail +reply --message-id <id> --body "回复"` | 回复邮件 |
| `lark-cli mail messages-list --folder INBOX --unread` | 列出未读邮件 |

#### 3.4.7 知识库（lark-wiki）

| 命令 | 说明 |
|------|------|
| `lark-cli wiki +create-node --space-id <id> --title "标题"` | 创建知识库节点 |
| `lark-cli wiki +search --keyword "关键词"` | 搜索知识库 |
| `lark-cli wiki +list` | 列出知识库 |

#### 3.4.8 云盘（lark-drive）

| 命令 | 说明 |
|------|------|
| `lark-cli drive +list` | 列出云盘文件 |
| `lark-cli drive +upload --file path/to/file` | 上传文件 |
| `lark-cli drive +download --file-token <token>` | 下载文件 |

#### 3.4.9 任务（lark-task）

| 命令 | 说明 |
|------|------|
| `lark-cli task +create --summary "任务" --due-date "2026-06-20"` | 创建任务 |
| `lark-cli task +get-my-tasks` | 获取我的任务 |
| `lark-cli task +complete --task-id <id>` | 完成任务 |

#### 3.4.10 审批（lark-approval）

| 命令 | 说明 |
|------|------|
| `lark-cli approval +create --type "请假"` | 创建审批 |
| `lark-cli approval +search --status pending` | 搜索待审批项 |

#### 3.4.11 辅助命令

| 命令 | 说明 |
|------|------|
| `lark-cli doctor` | 诊断环境配置 |
| `lark-cli --dry-run` | 预览操作（不实际执行） |
| `lark-cli schema` | 查看数据结构 |
| `lark-cli auth status` | 查看授权状态 |
| `lark-cli auth logout` | 登出 |

### 3.5 19个 Agent Skills 全景

飞书CLI内置19个Agent Skills，对应各业务域：

| # | Skill名称 | 业务域 | 核心能力 |
|---|---------|------|---------|
| 1 | lark-doc | 云文档 | 创建/读取/更新/搜索文档 |
| 2 | lark-sheets | 电子表格 | 读写电子表格数据 |
| 3 | lark-base | 多维表格 | Base增删改查 |
| 4 | lark-im | 消息 | 群聊/私聊/消息搜索 |
| 5 | lark-calendar | 日历 | 日程/忙闲/推荐 |
| 6 | lark-vc | 视频会议 | 会议创建/纪要 |
| 7 | lark-mins | 妙记 | 录制转文字 |
| 8 | lark-mail | 邮箱 | 收发/分类 |
| 9 | lark-wiki | 知识库 | 节点/空间管理 |
| 10 | lark-drive | 云盘 | 文件上传/下载 |
| 11 | lark-task | 任务 | 创建/完成/列表 |
| 12 | lark-approval | 审批 | 申请/查询 |
| 13 | lark-event | 事件订阅 | WebSocket推送 |
| 14 | lark-whiteboard | 白板 | 协作白板 |
| 15 | lark-search | 统一搜索 | 跨域内容搜索 |
| 16 | lark-shared | 共享 | 文件共享管理 |
| 17 | lark-okr | OKR | 目标管理 |
| 18 | lark-attendance | 考勤 | 打卡/统计 |
| 19 | lark-contact | 通讯录 | 用户/部门管理 |

### 3.6 权限 Scope 清单

| 域 | Scope | 用途 |
|------|------|------|
| 云文档 | `docx:document` | 文档读写 |
| 多维表格 | `bitable:app` | Base操作 |
| 消息 | `im:message` | 收发消息 |
| 日历 | `calendar:calendar` | 日历管理 |
| 视频会议 | `vc:meeting` | 会议管理 |
| 邮箱 | `mail:mail` | 邮件收发 |
| 知识库 | `wiki:wiki` | 知识库操作 |
| 云盘 | `drive:drive` | 文件管理 |
| 任务 | `task:task` | 任务管理 |
| 审批 | `approval:approval` | 审批流程 |
| 通讯录 | `contact:contact` | 用户信息 |
| 妙记 | `mins:mins` | 会议转写 |
| OKR | `okr:okr` | 目标管理 |
| 考勤 | `attendance:attendance` | 考勤数据 |

**最小权限原则**：按场景仅授权所需 Scope，禁止申请全部权限。

---

## 四、Codex Agent Plugins（6角色110技能）

### 4.1 角色矩阵

| 角色 | 技能数 | 核心能力 |
|------|:---:|------|
| Developer | 25 | 代码生成、调试、重构、Code Review |
| Data Analyst | 18 | SQL查询、可视化、统计建模 |
| DevOps | 15 | CI/CD、容器编排、监控告警 |
| Technical Writer | 12 | 文档生成、翻译、API文档 |
| Product Manager | 22 | PRD撰写、竞品分析、路线图 |
| Security Engineer | 18 | 漏洞扫描、合规检查、渗透测试 |

> 注：截至R73数据，Agent Plugins已扩展至**8角色146技能+80企业应用**。

### 4.2 企业应用集成

- 62→80+企业应用覆盖（GitHub、Jira、Slack、飞书、钉钉、Notion等）
- Annotations人-Agent实时协作批注编辑
- Sites自然语言一键生成可交互Web应用（日均12万站点）

---

## 五、自动化场景 SOP 模板

### SOP-1：每日站会纪要自动化

**触发**：定时任务执行

**流程**：
1. 获取参会人员当日日历 → `lark-cli calendar +agenda`
2. 拉取昨日任务完成情况 → `lark-cli task +get-my-tasks`
3. LLM生成站会报告
4. 发送到指定飞书群 → `lark-cli im +messages-send --chat-id <id>`

### SOP-2：周报自动生成

**触发**：每周五 17:00

**流程**：
1. 拉取本周所有任务 → `lark-cli task +get-my-tasks`
2. 汇总飞书文档修改记录 → `lark-cli docs +list`
3. 提取会议纪要关键结论 → `lark-cli vc +minutes`
4. LLM生成结构化周报
5. 写入飞书文档 → `lark-cli docs create --title "周报"`

### SOP-3：会议纪要全流程

**触发**：会议结束后

**流程**：
1. 获取飞书妙记转写 → `lark-cli mins +get --meeting-id <id>`
2. LLM提炼要点/待办/决策
3. 创建飞书文档归档 → `lark-cli docs create`
4. 将待办事项写入飞书任务 → `lark-cli task +create`
5. 在对应群发送纪要链接 → `lark-cli im +messages-send`

### SOP-4：Base批量数据导入

**触发**：用户提供数据文件

**流程**：
1. 解析CSV/JSON/Excel源数据
2. 映射字段到飞书Base列
3. 批量写入 → `lark-cli base record-create --data records.json`
4. 返回导入统计（成功/失败行数）

### SOP-5：审批流自动跟踪

**触发**：定时检查

**流程**：
1. 查询待审批项 → `lark-cli approval +search --status pending`
2. 检查超时审批（超过24h）
3. 发送提醒消息 → `lark-cli im +messages-send`
4. 生成审批状态日报

### SOP-6：知识库自动归档

**触发**：群聊中有重要决策/文档

**流程**：
1. 监听群聊关键词（"请归档"/"确认方案"）
2. LLM提取关键信息
3. 创建知识库节点 → `lark-cli wiki +create-node`
4. 回复归档链接到群聊

### SOP-7：客户通知自动化

**触发**：Base状态变更

**流程**：
1. 检测Base中客户状态变化
2. 匹配通知模板
3. 发送飞书消息通知相关负责人
4. 记录通知日志到Base

---

## 六、错误处理与边界条件

### 6.1 常见错误码速查

| 错误码 | 原因 | 处理方案 |
|--------|------|---------|
| 99991663 | Token过期 | `lark-cli auth login --recommend` 重新授权 |
| 99991664 | 权限不足 | 检查Scope清单，补充所需权限 |
| 99991665 | 频率限制 | 指数退避重试（1s→2s→4s→8s） |
| 99991666 | 参数错误 | `lark-cli --dry-run` 预览检查参数 |
| npm ERR! | npm安装失败 | 使用国内镜像 `--registry=https://registry.npmmirror.com` |
| 二维码过期 | OAuth设备流超时 | 重新执行登录命令 |

### 6.2 指数退避重试策略

```python
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait)
```

### 6.3 边界条件

- **批量操作上限**：单次Base写入 ≤ 5000行
- **消息频率**：同一群每分钟 ≤ 20条
- **文档大小**：单文档 ≤ 50MB（Markdown转换）
- **日历查询**：时间范围 ≤ 365天
- **会话超时**：Codex会话默认30分钟无操作超时

### 6.4 诊断命令

```bash
lark-cli doctor              # 全面诊断
lark-cli auth status         # 授权状态
lark-cli --dry-run <命令>    # 安全预览
```

---

## 七、安全权限配置规范

### 7.1 安全红线

1. **凭据管理**：禁止硬编码 App Secret，使用环境变量或 OS 原生密钥链
2. **`--dry-run` 强制**：所有写操作前必须执行 `--dry-run` 预览
3. **输入防注入**：对用户输入做语义过滤，禁止在自然语言中嵌入命令
4. **输出净化**：终端输出前检查，杜绝凭据/令牌泄露
5. **会话超时清理**：30分钟无操作的飞书CLI会话自动登出
6. **风险分级**：写操作（🟡中风险）→ 批量发送（🔴高风险+二次确认）→ 操作审计日志全量记录
7. **协议对齐**：遵循龙虾协议#187（MXC沙箱）、#204（供应链纵深防御）、#206（运行时全栈安全）、#226（桌面审计链）、#235（安全合规认证）

### 7.2 权限配置检查清单

- [ ] 飞书应用已创建（开放平台 → 企业自建应用）
- [ ] 应用权限已按需配置（最小权限原则，逐域审核）
- [ ] OAuth 2.0 授权已完成
- [ ] `lark-cli doctor` 诊断通过
- [ ] `lark-cli --dry-run` 预览验证通过
- [ ] Codex 权限模式已设置（生产环境推荐 `auto-edit`）
- [ ] 飞书测试企业环境已验证
- [ ] 审计日志功能已启用

### 7.3 环境变量凭据管理

```bash
# .env（加入 .gitignore）
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
CODEX_PERMISSION_MODE=auto-edit
```

### 7.4 三种桥接方案安全对比

| 方案 | 连接方式 | 安全等级 | 风险 |
|------|---------|:---:|------|
| cc-connect | WebSocket长连接 | 🟡 中 | 需飞书OAuth授权 |
| lark-coding-agent-bridge | npx一键启动 | 🟡 中 | 卡片交互+多session |
| feishu-codex-bridge | WebSocket+流式卡片 | 🔴 高 | danger模式绕过所有确认 |
| larksuite/cli（直连） | CLI直接调用 | 🟡 中 | 官方方案，安全兜底最完善 |

---

## 八、接入架构图（文字描述）

```
┌─────────────────────────────────────────────────────┐
│                    用户自然语言                        │
│         "帮我把今天的会议纪要做成飞书文档"              │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│              Codex CLI (思考+翻译层)                   │
│  · 协议#188 超级应用Agent融合                          │
│  · 协议#240 ChatGPT+Codex合体                         │
│  · 意图解析 → 任务拆解 → CLI命令生成                    │
│  · 权限模式：suggest/auto-edit/full-auto/yolo         │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│          飞书 lark-cli (执行层)                        │
│  · 三层命令体系（快捷/API/通用API）                      │
│  · 11大业务域 + 19 Agent Skills                       │
│  · OAuth 2.0 设备流授权                                │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│           飞书开放平台 API                             │
│  文档 · Base · 消息 · 日历 · 会议 · 邮件               │
│  知识库 · 云盘 · 任务 · 审批 · 通讯录 · 妙记 · OKR     │
└─────────────────────────────────────────────────────┘
```

**双Agent生态协作**（Claude Code ↔ Codex）：
- 共享层：`~/.agent-ecosystem/`（feishu-ops.md / 多维表格任务追踪 / 交接文档）
- 异步交接：Codex 完成任务后写入交接文档 → Claude Code 读取后继续
- 任务追踪：多维表格面板统一管理

---

## 九、Codex+飞书联合自动化技能

### 9.1 技能注册信息

| 字段 | 值 |
|------|-----|
| 技能名称 | Codex+飞书CLI联合自动化 |
| 技能标识 | `codex-feishu-automation` |
| 版本 | v5.0 |
| 技术栈 | Codex CLI / lark-cli (@larksuite/cli) / 飞书开放平台 |
| 安全等级 | 🟡 中风险（需飞书OAuth授权） |
| 关联协议 | #188 超级应用Agent融合 / #196 Codex+ChatGPT合体 / #240 超级Agent融合 / #201 飞书CLI自动化 / #187 MXC沙箱 / #204 供应链纵深防御 / #206 运行时全栈安全 / #226 桌面审计链 |

### 9.2 核心能力清单

| 能力 | 说明 |
|------|------|
| 自然语言操控飞书 | 通过Codex对话直接执行飞书全系操作 |
| 11域命令全覆盖 | 文档/Base/消息/日历/会议/邮件/知识库/云盘/任务/审批/通讯录 |
| 19 Agent Skills | 飞书CLI内置19个业务技能 |
| 自动化SOP | 7项标准化操作流程模板 |
| 安全四层防护 | 输入防注入+输出净化+--dry-run+操作审计 |
| 最小权限原则 | 14项Scope按需授权 |
| 错误自愈 | 指数退避重试+错误码速查+诊断命令 |
| 多模式接入 | 不授权/应用身份/用户身份三种模式 |

---

## 十、快速参考

### 10.1 安装检查清单

```bash
# 1. 安装飞书CLI
npm install -g @larksuite/cli --registry=https://registry.npmmirror.com

# 2. 添加Agent Skills
npx skills add larksuite/cli -y -g

# 3. 授权
lark-cli auth login --recommend

# 4. 诊断
lark-cli doctor

# 5. 安全预览测试
lark-cli --dry-run docs +create --title "测试"
```

### 10.2 自然语言速查模板

| 场景 | 自然语言指令 |
|------|------------|
| 创建文档 | "帮我在飞书创建一份标题为'Q2复盘报告'的文档" |
| 查日程 | "今天飞书上有什么会议" |
| 发消息 | "在飞书'产品群'发送'原型已更新，请查收'" |
| 创建Base记录 | "把这份CSV导入飞书多维表格" |
| 创建日程 | "帮我和张三约下周二下午2点的会议" |
| 提取纪要 | "把刚才会议的纪要做成飞书文档" |

### 10.3 社区资源

| 资源 | 地址 |
|------|------|
| 飞书CLI官方仓库 | https://github.com/larksuite/cli |
| 飞书开放平台 | https://open.feishu.cn |
| Codex官方文档 | https://codex.openai.com/docs |
| Codex×飞书指南 | https://codexguide.ai |
| 飞书CLI社区站点 | https://feishu-cli.com |
| feishucli.net | https://feishucli.net |

---

> **模板基准**：龙虾全域官方模板 v3.79 Final · 协议累计238项
> **来源声明**：基于模板v3.79内部知识提炼（协议#188/#196/#240 + R54-R73各轮迭代报告中的Codex/飞书知识）
> **生成日期**：2026-06-18
> **安全声明**：本手册所有操作均需 `--dry-run` 预览后方可执行，高风险操作需二次确认
