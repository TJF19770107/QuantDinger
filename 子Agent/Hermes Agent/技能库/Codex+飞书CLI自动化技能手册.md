---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_cf54d54c59baa0ada35a5ecb7c73a584_codex_feishu_v2
    ReservedCode1: a364dd92fb2b11468007b8a32e37d5ce0e9cde93942c7ef03d69b0dcc642881a
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_cf54d54c59baa0ada35a5ecb7c73a584_codex_feishu_v2
    ReservedCode2: a364dd92fb2b11468007b8a32e37d5ce0e9cde93942c7ef03d69b0dcc642881a
---

# Codex+飞书CLI自动化技能手册

> **版本**：v2.0 | **更新日期**：2026-06-18
> **模板基准**：龙虾全域官方模板-最终版 v3.99，SHA256=a364dd92
> **来源**：GitHub feishu-user-plugin、公众号文章《Codex对话接入飞书完整版》、@larksuite/cli官方文档、夜雨聆风实践
> **定位**：龙虾AI全域技能池 — Codex/飞书CLI自动化能力模块
> **本次更新**：新增公众号文章核心要点（飞书开放平台接入流程、权限配置避坑指南、5大自动化场景SOP），v1.0→v2.0

---

## 一、完整架构图（四层链路）

```
┌─────────────────────────────────────────────────────────┐
│                      Agent 层 (Codex / Claude / OpenClaw) │
│  自然语言指令 → "帮我在飞书创建一份周报文档"              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Skill 层 (Feishu-Skill)                │
│  ┌──────────────────────────────────────────────────┐   │
│  │ • 告诉 Agent 如何检查 feishu-tool 状态             │   │
│  │ • 判断三层鉴权状态（cookie / API / OAuth）         │   │
│  │ • 每个工具应传什么 JSON 参数                       │   │
│  │ • 文档/任务/成员 分别读哪份参数参考说明             │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  CLI 层 (feishu-tool / lark-cli)         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ • 标准化命令行接口                                  │   │
│  │ • npx feishu-user-plugin <command>                 │   │
│  │ • lark-cli <domain> <command>                     │   │
│  │ • 自动处理认证、重试、错误                           │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              飞书开放平台 API 层                          │
│  文档 / 多维表格 / 知识库 / 云空间 / 日历 / 任务 / OKR   │
│  消息 / 群聊 / 私聊 / 联系人 / 实时事件 / 审批 / 邮箱    │
└─────────────────────────────────────────────────────────┘
```

**链路优势**：Agent 无需直接理解飞书 API，边界清晰；Skill 层负责"教 Agent 怎么用"，CLI 层负责"执行"。

---

## 二、接入流程总图（含公众号文章最新要点）

### 2.1 飞书开放平台前置步骤

```
飞书开放平台 https://open.feishu.cn

步骤1：创建自建应用
  → 获取 App ID + App Secret

步骤2：开启机器人能力
  → 记录 Verification Token + Encrypt Key

步骤3：权限配置（关键！）
  → 获取与发送消息
  → 读取通讯录
  → 访问云文档
  → 多维表读写
  → 审批实例访问

步骤4：发布应用
  → 管理员审核通过
```

### 2.2 两套CLI方案对比

| 维度 | feishu-user-plugin (MCP) | @larksuite/cli (官方) |
|------|------------------------|---------------------|
| 安装 | `npm install -g feishu-user-plugin` | `npm install -g @larksuite/cli` |
| 鉴权 | Cookie + API + OAuth 三层 | OAuth 2.0 设备流 |
| 工具数 | 84个 | 200+ 命令 |
| Agent集成 | MCP stdio 协议 | CLI 命令行 |
| 配置复杂度 | 低（自动setup） | 中（需手动配置） |
| 适用场景 | 个人+企业 | 企业为主 |
| 多账号 | 内置多profile | 需自行管理 |

---

## 三、核心安装命令

### 3.1 feishu-user-plugin MCP（推荐个人/Codex使用）

```bash
# 安装飞书用户插件 MCP 服务器 + CLI 工具
npm install -g feishu-user-plugin

# 验证安装
npx feishu-user-plugin --version

# 自动配置 Claude Code
npx feishu-user-plugin setup

# 自动配置 Codex
npx feishu-user-plugin setup --client codex

# 同时配置 Claude Code 和 Codex
npx feishu-user-plugin setup --client both
```

### 3.2 飞书官方CLI（@larksuite/cli）

```bash
# 安装飞书官方CLI
npm install -g @larksuite/cli

# 验证安装
lark-cli --version

# OAuth授权
lark-cli auth login --recommend
```

### 3.3 Scholar MCP（论文检索场景）

```bash
npm install -g scholar-mcp
```

---

## 四、Codex 配置示例

### 4.1 feishu-user-plugin MCP 配置

`~/.codex/config.toml`：

```toml
[mcp_servers.feishu-user-plugin]
command = "npx"
args = ["feishu-user-plugin", "--transport=stdio"]
startup_timeout_sec = 120

[mcp_servers.feishu-user-plugin.env]
# 自动从 ~/.feishu-user-plugin/credentials.json 读取多账号配置
```

### 4.2 飞书项目 MCP 配置

```toml
[mcp_servers.feishu-project]
command = "npx"
args = ["-y", "@feishu/project-mcp"]
startup_timeout_sec = 60
```

### 4.3 多账号配置

`~/.feishu-user-plugin/credentials.json`：

```json
{
  "default": {
    "cookie": "从浏览器复制",
    "app_id": "cli_xxx",
    "app_secret": "xxx"
  },
  "work": {
    "cookie": "工作账号cookie",
    "app_id": "cli_yyy",
    "app_secret": "yyy"
  }
}
```

---

## 五、权限配置要点（公众号文章避坑指南）

### 5.1 Token 类型选择

| Token 类型 | 适用场景 | 说明 |
|-----------|---------|------|
| `tenant_access_token` | CLI 自动化、服务端调用 | 应用级，无需用户授权，Codex CLI 推荐使用 |
| `user_access_token` | 用户相关操作 | 需要用户授权，有明确用户身份 |

### 5.2 三层鉴权体系

| 鉴权方式 | 适用场景 | 配置位置 | 说明 |
|---------|---------|---------|------|
| **Cookie鉴权** | 个人使用、CLI模式 | `~/.feishu-user-plugin/credentials.json` | 从浏览器DevTools复制，以本人身份操作 |
| **官方API** | 企业应用、服务端 | 飞书开放平台 → 创建应用 → App ID + Secret | 需配置应用权限范围（scope） |
| **OAuth 2.1** | 第三方授权、MCP安全 | 飞书开放平台 → OAuth配置 | 支持细粒度scope权限 |

### 5.3 鉴权状态检查

```bash
npx feishu-user-plugin status
# 预期输出：✅ cookie: valid / ✅ api: valid / ✅ oauth: valid
```

### 5.4 常见失败原因

| 错误码 | 现象 | 原因 | 解决 |
|-------|------|------|------|
| 403 | 请求被拒 | 权限未开通 | 飞书开放平台→权限管理→添加scope |
| 99991663 | 调用失败 | 应用未启用 | 发布应用并管理员审核 |
| 无 | 消息发不出 | 机器人未加入群 | 将机器人加入目标群聊 |
| 401 | Unauthorized | cookie过期 | 重新从浏览器复制cookie |
| 超时 | MCP connection timeout | 启动超时 | 增加`startup_timeout_sec`到120 |

### 5.5 安全建议

- 不要硬编码 App Secret，使用环境变量：`export FEISHU_APP_ID=xxx`
- `.env` 文件加入 `.gitignore`，避免凭证泄露
- 生产环境使用 OAuth 而非 cookie
- 定期轮换 App Secret
- MCP 连接建议开启 OAuth 2.1 细粒度权限

---

## 六、常用操作场景 SOP

### 场景1：创建飞书文档

```bash
# 自然语言指令
"帮我在飞书知识库「团队文档」下创建一份周报，标题为「2026年第25周周报」"

# CLI 操作
npx feishu-user-plugin doc create --title "2026年第25周周报" --folder "团队文档"
```

### 场景2：更新多维表格

```bash
# 自然语言指令
"把这份数据追加到飞书多维表格「销售数据」的最后一行"

# 批量操作（500条/次）
npx feishu-user-plugin table append --name "销售数据" --data ./data.json
```

### 场景3：搜索知识库

```bash
# 自然语言指令
"在飞书知识库搜索关于「Q2 OKR总结」的文档"

# CLI 操作
npx feishu-user-plugin wiki search --query "Q2 OKR总结"
npx feishu-user-plugin doc read_markdown --id <doc_id>
```

### 场景4：发送消息（含卡片消息）

```bash
# 以本人身份发送文本消息
npx feishu-user-plugin message send --chat "产品群" --content "今天下午3点评审会，请大家准时参加"

# 发送卡片消息（含交互元素）
lark-cli im message-send --chat-id oc_xxx --msg-type interactive --card card.json
```

**card.json 示例**：
```json
{
  "config": { "wide_screen_mode": true },
  "elements": [
    {
      "tag": "div",
      "text": {
        "content": "Codex 已生成报告，请查阅",
        "tag": "lark_md"
      }
    }
  ]
}
```

### 场景5：管理日历

```bash
# 创建日程
npx feishu-user-plugin calendar create --title "迭代复盘会议" \
  --start "2026-06-18T14:00:00" --end "2026-06-18T15:00:00" \
  --members "张三,李四"
```

### 场景6：论文精读（双语飞书文档）

```bash
# 自然语言指令
"搜索本周关于AI Agent的论文，生成双语精读文档存到飞书知识库"

# 链路：Scholar MCP检索 → 全文解析 → 飞书CLI创建文档
```

### 场景7：飞书项目管理工单

```bash
# 自然语言指令
"帮我在飞书项目里创建一个'数据同步优化'的需求工单，指派给 @王五"

# 先命中本地业务上下文缓存，再调MCP
```

### 场景8：多维表批量写入

```bash
# 用飞书官方CLI写多维表
lark-cli bitable append \
  --app-token bascnxxx \
  --table-id tblxxx \
  --record '{"字段1":"值A","字段2":"值B"}'
```

---

## 七、飞书文档操作省 Token 策略

### 7.1 `read_doc_markdown` 节省 ~60% token

| 读取方式 | Token 消耗 | 说明 |
|---------|-----------|------|
| `doc read`（默认） | 100%（基准） | 返回完整文档 JSON 结构 |
| `doc read_markdown` | ~40% | 仅返回 Markdown 纯文本 |

### 7.2 推荐实践

```bash
# ❌ 避免：默认读取（浪费token）
npx feishu-user-plugin doc read --id <id>

# ✅ 推荐：Markdown读取（省token）
npx feishu-user-plugin doc read_markdown --id <id>
```

### 7.3 其他省 Token 策略

- 批量操作：多维表格追加使用 500 条/批
- 缓存搜索结果：wiki search 结果缓存本地
- 切片读取：大文档分段读取
- MCP Prompts：优先使用预置 slash command

---

## 八、工具清单速览

### 8.1 feishu-user-plugin 工具分类（84个工具）

| 大类 | 工具数量 | 典型工具 |
|------|---------|---------|
| 消息与群聊 | 17 | send_message, read_group_messages, merge_forward |
| 文档生态 | 27 | doc_create, doc_read_markdown, doc_search, doc_append_blocks |
| 多维表格 | ✅ | table_read, table_append, table_search |
| 知识库 | ✅ | wiki_search, wiki_create_doc, wiki_read |
| 云空间 | ✅ | drive_list, drive_create_folder |
| 协作工具 | 21 | calendar_create, task_create, okr_read, contact_search |
| 实时事件 | 2 | ws_listen |
| 诊断多账号 | 4 | status, profile_switch |

### 8.2 9个 MCP Prompts（Slash Commands）

| Prompt | 功能 |
|--------|------|
| `/send` | 以用户身份发消息 |
| `/reply` | 读最近消息然后回复 |
| `/digest` | 群/P2P最近消息总结 |
| `/search` | 搜联系人/群 |
| `/doc` | 搜/读/建文档 |
| `/table` | 操作多维表格 |
| `/wiki` | 搜知识库 |
| `/drive` | 列云空间/建文件夹 |
| `/status` | 检查三层鉴权状态 |

---

## 九、接入方式对比表

| 客户端 | 配置文件 | 顶层键 | setup命令 |
|--------|---------|--------|-----------|
| **Claude Code** | `~/.claude.json` / `.mcp.json` | `mcpServers.feishu-user-plugin` | `npx feishu-user-plugin setup` |
| **Codex** | `~/.codex/config.toml` | `[mcp_servers.feishu-user-plugin]` | `npx feishu-user-plugin setup --client codex` |
| **Cursor** | `.cursor/mcp.json` | `mcpServers.feishu` | 手动添加 |
| **VS Code Copilot** | `.vscode/mcp.json` | `servers.feishu` | 手动添加 |
| **OpenClaw** | `~/.openclaw/openclaw.json` | `mcp.servers.feishu-user-plugin` | 手动添加 |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | `mcpServers.feishu` | 手动添加 |

---

## 十、公众号文章核心自动化场景（v2.0新增）

### 场景A：Codex执行任务 → 飞书通知

```
Codex 完成代码分析
→ CLI 发送飞书群消息
→ @相关责任人
```

### 场景B：飞书消息触发 Codex

```
用户在飞书发指令
→ 飞书事件回调 → Webhook
→ 调用 Codex CLI → 返回结果
```

### 场景C：自动写飞书文档

```
Codex 生成总结
→ CLI 调用文档 API
→ 自动写入飞书文档
```

### 场景D：日报/周报自动化

```
定时任务
→ Codex 汇总数据
→ 写入多维表
→ 发送飞书卡片
```

### 场景E：智能日程协调

```
用户说"帮我和张三约个下周的会"
→ 查双方忙闲 → 找空档
→ 创建日程 → 邀请参会
→ 发消息通知
```

---

## 十一、推荐架构（可扩展）

```
飞书
 ↑↓
飞书 OpenAPI
 ↑↓
CLI 工具 (feishu-user-plugin / lark-cli)
 ↑↓
Codex / Claude / OpenClaw (LLM Agent)
 ↑↓
用户 (自然语言指令)
```

---

## 十二、龙虾 AI 全域技能池集成

### 12.1 技能注册

| 协议编号 | 技能名称 | 版本 | 状态 | 手册路径 |
|---------|---------|------|------|---------|
| #201 | 飞书 CLI Agent 自动化技能 | v4.1 | ✅ 激活 | 本手册 |
| #202 | Codex+飞书CLI自动化 | v1.1 | ✅ 激活 | 本手册 |
| #203 | Codex+飞书CLI消息与群组管理 | v1.1 | ✅ 激活 | 本手册 |
| #204 | Codex+飞书CLI日历与会议管理 | v1.1 | ✅ 激活 | 本手册 |
| #205 | Codex+飞书CLI综合办公自动化 | v1.1 | ✅ 激活 | 本手册 |

### 12.2 前置依赖

- 协议#178（Agent Team 协作架构）
- 协议#187（MXC 操作系统级沙箱）
- 协议#193（记忆三范式融合检索）
- 龙虾五步法 v2.0

---

## 十三、技能更新日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-18 | v2.0 | 公众号文章深度学习融合：飞书开放平台接入流程、权限配置避坑指南、5大自动化场景SOP、两套CLI方案对比、卡片消息模板、多维表批量写入命令 |
| 2026-06-17 | v1.0 | 初始创建，基于5大材料源提取核心知识 |
*（内容由AI生成，仅供参考）*
