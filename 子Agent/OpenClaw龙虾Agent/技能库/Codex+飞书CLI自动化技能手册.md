# Codex + 飞书CLI 自动化技能手册 v1.0

> **创建日期**：2026-05-31
> **对标来源**：飞书官方 CLI (larksuite/cli) + Codex CLI + 多源技术文章提炼
> **归属**：龙虾全域技能池
> **状态**：ACTIVE

---

## 一、飞书 CLI 核心架构

### 1.1 三层命令架构

| 层级 | 前缀/模式 | 适用对象 | 说明 |
|------|----------|---------|------|
| Shortcuts 层 | `+` 前缀 | 日常用户 / AI Agent 默认 | 高频操作封装，智能默认值，风险验证 |
| API Commands 层 | 无前缀 | AI Agent 精细操作 | 100+ 命令，与飞书开放 API 一一对应 |
| Raw API 层 | 直接调用 | 高级开发 | 覆盖飞书全部 2500+ OpenAPI |

### 1.2 11 大业务域 + 19 个 AI Skill

| 业务域 | Skill 前缀 | 能力 |
|--------|-----------|------|
| 消息/群聊 | `lark-im` | 发消息、搜群聊、管理群成员、消息历史 |
| 文档 | `lark-doc` | 创建/读取/更新文档，Markdown 双向转换 |
| 日历 | `lark-calendar` | 查日程、建事件、查忙闲、邀请参会人 |
| 邮件 | `lark-mail` | 收发邮件、管理草稿、订阅新邮件事件 |
| 电子表格 | `lark-sheets` | 读写单元格、批量追加、条件查找 |
| 多维表格 | `lark-base` | 增删改查记录、聚合分析、生成仪表盘 |
| 任务 | `lark-task` | 创建/完成/分配任务，设置子任务和提醒 |
| 知识库 | `lark-wiki` | 浏览节点、创建文档、管理结构 |
| 通讯录 | `lark-contact` | 搜同事、查部门架构 |
| 会议纪要 | `lark-vc/lark-minutes` | 提取妙记摘要、待办、逐字稿 |
| 搜索 | `lark-search` | 跨业务域搜消息、文档、应用 |

---

## 二、安装与接入流程

### 2.1 飞书 CLI 安装（3步闭环）

```bash
# Step 1: 安装 CLI
npm install -g @larksuite/cli

# Step 2: 安装 AI Skills
npx skills add larksuite/cli -y -g

# Step 3: 初始化配置
lark-cli config init --new
```

配置完成后**重启 AI 工具**（Codex / Claude Code / Cursor / OpenClaw）使 Skills 生效。

### 2.2 用户授权（两种模式）

| 模式 | 命令 | 能力 |
|------|------|------|
| 不授权模式 | 无需操作 | 基础操作：发消息、创建文档 |
| 用户身份模式 | `lark-cli auth login` | 访问日历、私信、邮箱等个人数据 |

### 2.3 飞书 MCP 配置（适用于 Codex）

**飞书开发者后台配置：**

1. 登录 [飞书开发者后台](https://open.feishu.cn/app) → 创建企业自建应用
2. 保存 APP ID 和 APP Secret
3. 添加应用能力（如机器人）
4. 配置权限（开通所需用户权限）
5. 安全设置 → 重定向 URL：`http://localhost:3000/callback`
6. 创建版本并发布

**本地 MCP 登录：**

```powershell
npx -y @larksuiteoapi/lark-mcp login -a <APP_ID> -s <APP_SECRET>
```

弹出浏览器窗口后点击授权。

**Codex config.toml 配置：**

```toml
# C:\Users\<用户名>\.codex\config.toml
[mcp_servers.feishu]
command = "npx.cmd"
args = [
  "-y",
  "@larksuiteoapi/lark-mcp",
  "mcp",
  "-a", "<APP_ID>",
  "-s", "<APP_SECRET>",
  "--oauth"
]
env = { SystemRoot="C:\\Windows", PROGRAMFILES="C:\\Program Files" }
startup_timeout_ms = 60_000
```

**验证：** 在 Codex 中输入 `/MCP` 查看飞书 MCP 是否已加载。

---

## 三、核心操作命令速查

### 3.1 文档操作

| 操作 | Shortcut 命令 | API 命令 |
|------|-------------|---------|
| 创建文档 | `lark-cli docs +create` | `lark-cli doc create --title "标题" --content "内容"` |
| 读取文档 | `lark-cli docs +read --url <链接>` | `lark-cli doc get --doc_token <token>` |
| 更新文档 | `lark-cli docs +update` | `lark-cli doc update --doc_token <token> --content "新内容"` |
| Markdown→飞书 | `lark-cli docs +import-md` | `lark-cli doc import --format markdown --file <路径>` |
| 飞书→Markdown | `lark-cli docs +export-md` | `lark-cli doc export --format markdown` |

### 3.2 消息与群聊

| 操作 | Shortcut 命令 |
|------|-------------|
| 发送消息 | `lark-cli im +messages-send --receive_id <id> --content "消息"` |
| 搜索群聊 | `lark-cli im +chat-search --keyword <关键词>` |
| 群消息总结 | `lark-cli im +messages-summary --chat_id <群ID>` |

### 3.3 日历操作

| 操作 | Shortcut 命令 |
|------|-------------|
| 查看今日日程 | `lark-cli calendar +agenda` |
| 创建日程 | `lark-cli calendar +event-create --summary "标题" --start_time <时间>` |
| 查忙闲 | `lark-cli calendar +freebusy --user_id <用户ID>` |

### 3.4 多维表格 (Base)

| 操作 | 命令 |
|------|------|
| 新增记录 | `lark-cli base record-create --app_token <token> --table_id <id> --fields '{"项目":"Codex接入"}'` |
| 查询记录 | `lark-cli base record-list --app_token <token> --table_id <id>` |
| 更新记录 | `lark-cli base record-update --app_token <token> --table_id <id> --record_id <id>` |

### 3.5 邮件操作

| 操作 | 命令 |
|------|------|
| 发送邮件 | `lark-cli mail +send --to <邮箱> --subject "主题" --body "内容"` |
| 查收邮件 | `lark-cli mail +list` |

---

## 四、Codex + 飞书 自动化场景 SOP

### 4.1 场景一：AI 调研 → 飞书文档自动生成

```
1. Codex 接收调研任务 → 执行 web_search / web_fetch 收集资料
2. Codex 整理内容为结构化 Markdown
3. Codex 调用 lark-cli docs +create --title "调研报告" --content "<Markdown正文>"
4. 飞书自动创建文档，返回链接
5. Codex 将链接交付用户
```

### 4.2 场景二：批量数据 → 飞书多维表格

```
1. 用户提供 CSV / Excel / Markdown 表格数据
2. Codex 解析数据结构
3. Codex 调用 lark-cli base record-create 逐条写入飞书 Base
4. 完成后返回飞书表格链接
```

### 4.3 场景三：群消息自动总结

```
1. Codex 定时或触发式调用 lark-cli im +messages-summary
2. 获取群消息内容
3. Codex LLM 提炼关键信息（待办/决策/讨论要点）
4. 通过 lark-cli im +messages-send 发送总结到群内
5. 或通过 lark-cli docs +create 生成会议纪要文档
```

### 4.4 场景四：日程智能管理

```
1. 用户：「帮我看看下周哪天有空，安排一个2小时的 Codex 评审会」
2. Codex 调用 lark-cli calendar +freebusy 查询忙闲
3. 找到可用时段后调用 lark-cli calendar +event-create 创建日程
4. 自动邀请参会人
5. 发送日程确认消息
```

### 4.5 场景五：运营素材批量生成 → 飞书表格

```
1. Codex 维护选题表
2. 批量生成标题/副标题/CTA/模板类型
3. 写入飞书多维表格
4. 导出 CSV → Canva Bulk Create 批量生成素材图
```

---

## 五、错误处理与权限配置

### 5.1 常见错误与修复

| 错误信息 | 原因 | 修复方案 |
|---------|------|---------|
| `permission denied` | 未开通对应权限 | 飞书开发者后台 → 权限管理 → 开通用户权限 → 重新发布 |
| `token expired` | 授权过期 | 执行 `lark-cli auth login` 重新授权 |
| `MCP server not found` | Codex 未正确加载 MCP | 检查 config.toml 配置，确认 `startup_timeout_ms = 60_000` |
| `npx.cmd not found` | Windows 上 npx 路径问题 | 将 `npx` 替换为 `npx.cmd` |
| `app not published` | 应用未发布 | 飞书开发者后台 → 创建版本 → 发布 |

### 5.2 权限最小化原则

- 日常操作推荐 `--recommend` 参数：`lark-cli auth login --recommend`
- 仅申请推荐权限，自动审批，不触发管理员审核
- 按需扩展权限，避免一次性全开

---

## 六、Codex 特有配置要点

### 6.1 工作流集成

Codex 原生支持 Tools 机制，飞书 CLI 作为外部工具可通过以下方式集成：

1. **MCP 方式**：在 config.toml 中配置 feishu MCP server（推荐）
2. **Shell 方式**：通过 `shell_executor` 直接调用 `lark-cli` 命令
3. **Agent Skills 方式**：安装 `npx skills add larksuite/cli -y -g` 后，Codex 自动识别 19 个 Skill

### 6.2 上下文优化

- 给 Codex 清晰上下文和目标描述
- 使用 Codex 的 `/goal` 进行跨会话持久化任务追踪
- 关键操作前让 Codex 先 `dry-run` 预览效果

---

## 七、技能迭代记录

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-05-31 | v1.0 | 初始版本，涵盖飞书 CLI 11 大业务域、Codex 接入配置、5 大自动化场景 SOP |

---

> **关联技能**：龙虾-多Agent协同看板协议 v1.0 / 龙虾-动态工作流引擎规范 v1.0 / 龙虾-长时域Goal追踪规范 v1.0
> **文件路径**：E:\龙虾AI主控中心\技能库\Codex+飞书CLI自动化技能手册.md
