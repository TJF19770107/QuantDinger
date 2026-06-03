# Codex+飞书CLI自动化技能手册 v1.2

> **生成时间**：2026-06-02（R40迭代更新）
> **来源文章**：[如何通过 Codex 对话接入飞书完整版来了！](https://mp.weixin.qq.com/s/lp1fV7O1flKzV1AgeMBQ3A)
> **归属**：龙虾全域技能池
> **版本**：v1.2
> **关联协议**：#135 Claude Code四件套、#121 A2A+MCP三层协议栈

---

## 一、总览架构

### 1.1 双路径架构

```
路径A：Codex CLI ↔ 飞书 CLI (lark-cli) ↔ 飞书开放平台
路径B：Codex MCP Server ↔ 飞书开放平台 REST API
```

| 路径 | 工具 | 优势 | 适用场景 |
|------|------|------|---------|
| CLI路径 | lark-cli | 对话式零配置，纯Codex对话即可 | 快速接入、轻量场景 |
| API路径 | MCP Server | 精确控制、批量操作 | 生产级自动化、高频调用 |

### 1.2 架构全景

```
用户 ↔ Codex CLI/Session ↔ 飞书开放平台API ↔ 飞书工作空间
                ↕
          MCP Server（飞书工具集）
                ↕
    文档 | Base | 消息 | 日历 | 会议 | 审批 | 知识库 | 任务 | 通讯录 | 妙记 | 搜索
```

---

## 二、路径A：飞书CLI纯对话接入（4步保姆级SOP）

> 来源：公众号文章"如何通过 Codex 对话接入飞书完整版来了！"
> 特点：零配置文件，只需在 Codex 对话中自然语言驱动

### Step 1：安装飞书 CLI

在 Codex 对话中直接输入：

```
请帮我安装飞书 CLI
```

Codex 会自动执行安装命令，整个过程约 4~5 分钟。

### Step 2：配置飞书应用

在 Codex 中继续：

```
请初始化飞书 CLI 配置，输出浏览器可访问的配置链接
```

Codex 执行后会输出一个配置链接 → 浏览器打开 → 按提示创建/绑定飞书应用 → 将生成的 **App ID** 和 **App Secret** 交给 Codex。

### Step 3：登录授权

```
请执行飞书授权命令，输出授权链接
```

Codex 输出授权链接 → 浏览器打开 → 确认授权。

### Step 4：验证接入

```
创建下周一8点的飞书日历事件
```

如果正常创建成功，说明链路贯通。之后即可对话式驱动飞书所有能力。

---

## 三、路径B：飞书 REST API 标准接入（5步SOP）

### Step 1：飞书应用创建与权限配置

```bash
# 飞书开放平台 → 创建企业自建应用
# https://open.feishu.cn/app
```

**必须开通的权限（按需选择）**：

| 权限 scope | 用途 | 是否必须 |
|-----------|------|---------|
| `docx:document` | 文档读写 | 推荐 |
| `bitable:app` | 多维表格操作 | 推荐 |
| `im:message:send_as_bot` | 发送消息 | 推荐 |
| `calendar:calendar` | 日历读写 | 按需 |
| `vc:meeting` | 会议创建/管理 | 按需 |
| `approval:instance` | 审批实例 | 按需 |
| `contact:user` | 用户信息读取 | 推荐 |
| `wiki:wiki` | 知识库操作 | 按需 |
| `task:task` | 任务管理 | 按需 |
| `minutes:minutes` | 会议纪要/妙记 | 按需 |

### Step 2：获取 tenant_access_token

```python
import requests
import time

class FeishuTokenManager:
    """飞书 Token 管理器，自动缓存+刷新"""
    
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None
        self._expires_at = 0
    
    def get_token(self):
        if time.time() < self._expires_at - 300:  # 提前5分钟刷新
            return self._token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        data = resp.json()
        self._token = data["tenant_access_token"]
        self._expires_at = time.time() + data.get("expire", 7200)
        return self._token
```

### Step 3：Codex MCP Server 配置

```json
// .codex/mcp/feishu.json
{
  "mcpServers": {
    "feishu": {
      "command": "npx",
      "args": ["-y", "@anthropic/feishu-mcp-server"],
      "env": {
        "FEISHU_APP_ID": "cli_xxxxxxxxxxxx",
        "FEISHU_APP_SECRET": "xxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

### Step 4：Codex Session 对接

```bash
# 启动带飞书 MCP 的 Codex 会话
codex --mcp-config .codex/mcp/feishu.json

# 或在会话中动态加载
codex> /mcp add feishu -- npx -y @anthropic/feishu-mcp-server

# 验证 MCP 工具加载成功
codex> /mcp list
```

### Step 5：对话式操作验证

```
# 自然语言驱动飞书操作示例
"帮我在飞书文档中创建一个本周会议纪要模板"
"查询飞书多维表格中所有待办事项，按优先级排序"
"向飞书群'AI自动化'发送今日任务汇总"
"查看我明天上午的日历空闲时段"
"创建一个周五下午3点的项目评审会议"
```

---

## 四、飞书 CLI 11大业务域能力矩阵

| 业务域 | Skill | 核心能力 |
|--------|-------|---------|
| 消息/群聊 | lark-im | 发消息、搜群、管理成员、消息总结 |
| 云文档 | lark-doc | 创建/读取/更新、Markdown 双向转换 |
| 日历 | lark-calendar | 查日程、建事件、查忙闲、邀请参会 |
| 邮件 | lark-mail | 收发邮件、管理草稿 |
| 电子表格 | lark-sheets | 读写单元格、批量追加 |
| 多维表格 | lark-base | 增删改查、聚合分析、仪表盘 |
| 任务 | lark-task | 创建/完成/分配任务 |
| 知识库 | lark-wiki | 浏览节点、创建文档 |
| 通讯录 | lark-contact | 搜同事、查部门 |
| 会议纪要 | lark-vc/lark-minutes | 妙记摘要、待办、逐字稿 |
| 搜索 | lark-search | 跨业务域搜索 |

---

## 五、六大核心场景 REST API 命令速查

### 5.1 飞书文档（Docx）

| 操作 | API Endpoint |
|------|-------------|
| 创建文档 | `POST /open-apis/docx/v1/documents` |
| 读取内容 | `GET /open-apis/docx/v1/documents/{id}/raw_content` |
| 追加块 | `PATCH /open-apis/docx/v1/documents/{id}/blocks/{block_id}/children` |
| 批量更新 | `PATCH /open-apis/docx/v1/documents/{id}/blocks/batch_update` |

**关键 block_type**：`text` / `heading1~9` / `bullet` / `ordered` / `code` / `table` / `image`

### 5.2 飞书多维表格（Base / Bitable）

| 操作 | API Endpoint |
|------|-------------|
| 列出表格 | `GET /open-apis/bitable/v1/apps/{app_token}/tables` |
| 查询记录 | `GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records` |
| 新增记录 | `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records` |
| 更新记录 | `PUT /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}` |
| 批量操作 | `POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create` |

### 5.3 飞书消息（IM）

| 操作 | API Endpoint |
|------|-------------|
| 发送文本 | `POST /open-apis/im/v1/messages?receive_id_type=open_id` |
| 发送卡片 | `POST /open-apis/im/v1/messages?receive_id_type=open_id` (msg_type=interactive) |
| 发送图片/文件 | 先上传 `POST /open-apis/im/v1/images` 或 `files`，再发送 |
| 批量发送 | `POST /open-apis/im/v1/messages/batch_send` |
| 读取消息 | `GET /open-apis/im/v1/messages` |

### 5.4 飞书日历（Calendar）

| 操作 | API Endpoint |
|------|-------------|
| 查询忙闲 | `POST /open-apis/calendar/v4/freebusy/list` |
| 创建日程 | `POST /open-apis/calendar/v4/calendars/{calendar_id}/events` |
| 更新日程 | `PATCH /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}` |
| 删除日程 | `DELETE /open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}` |

### 5.5 飞书会议（VC）

| 操作 | API Endpoint |
|------|-------------|
| 创建会议 | `POST /open-apis/vc/v1/meetings` |
| 查询会议 | `GET /open-apis/vc/v1/meetings/{meeting_id}` |
| 结束会议 | `PATCH /open-apis/vc/v1/meetings/{meeting_id}/end` |
| 获取录制 | `GET /open-apis/vc/v1/meetings/{meeting_id}/recording` |

### 5.6 飞书审批（Approval）

| 操作 | API Endpoint |
|------|-------------|
| 创建审批实例 | `POST /open-apis/approval/v4/instances` |
| 查询审批 | `GET /open-apis/approval/v4/instances/{instance_id}` |
| 审批通过/拒绝 | `POST /open-apis/approval/v4/instances/{instance_id}/tasks/{task_id}` |

---

## 六、Codex 对话接入最佳实践

### 6.1 Codex Prompt 设计模式

**四步 Prompt 模板**：

```
1. 目标声明："请帮我通过飞书 CLI [具体操作]"
2. 参数指定："App ID 是 xxx，App Secret 是 xxx"
3. 格式要求："输出格式为 [Markdown/JSON/飞书卡片消息]"
4. 验证确认："执行后请展示结果摘要"
```

**示例**：

```
请帮我通过飞书 CLI 完成以下操作：
1. 查询今日多维表格"项目进度看板"中所有状态为"阻塞"的任务
2. 将结果整理成 Markdown 表格
3. 发送到飞书群"项目管理群"
4. 同时在飞书文档中创建一份"今日阻塞任务报告"
```

### 6.2 Codex Skill 封装

```yaml
# .codex/skills/feishu.md
name: feishu-doc-assistant
description: 飞书文档自动化助手
tools:
  - feishu_doc_create
  - feishu_doc_read
  - feishu_doc_append
  - feishu_message_send
  - feishu_calendar_query
  - feishu_bitable_query
  - feishu_wiki_browse
  - feishu_task_create

instructions: |
  你是飞书文档自动化助手。当用户需要操作飞书时：
  1. 确认操作类型和目标（文档/表格/消息/日历/任务/知识库）
  2. 调用对应工具执行，遵循最小权限原则
  3. 执行后返回操作结果摘要 + 链接（如有）
```

### 6.3 Codex Triggers 事件驱动

```json
// .codex/triggers/feishu_daily_report.json
{
  "name": "feishu_daily_report",
  "trigger": {
    "type": "schedule",
    "cron": "0 18 * * 1-5"
  },
  "action": {
    "skill": "feishu-doc-assistant",
    "prompt": "查询多维表格中今日所有完成的任务，生成日报Markdown文档并发送到'团队日报'群"
  }
}
```

```json
// .codex/triggers/feishu_webhook_monitor.json
{
  "name": "feishu_webhook_monitor",
  "trigger": {
    "type": "webhook",
    "event": "bitable.record.created"
  },
  "action": {
    "skill": "feishu-doc-assistant",
    "prompt": "检测到多维表格新增记录，分析内容并发送通知到对应负责人"
  }
}
```

---

## 七、5大自动化场景 SOP

### 场景1：AI调研 → 飞书文档

```
触发：用户自然语言"帮我调研XX并写入飞书文档"
流程：
  1. 搜索/抓取目标内容
  2. LLM 提炼结构化结果
  3. 生成 Markdown
  4. lark-cli docs +create 或 POST /open-apis/docx/v1/documents
  5. 追加内容块
  6. 返回文档链接
```

### 场景2：批量数据 → 飞书 Base

```
触发：用户提供 CSV/JSON/Excel 数据源
流程：
  1. 解析数据源结构
  2. 匹配 Base 表格字段
  3. lark-cli base record-create 批量写入
  4. 返回写入统计（成功/失败数）
```

### 场景3：群消息智能总结

```
触发：定时/按需
流程：
  1. lark-cli im +messages-list 获取最近消息
  2. LLM 提炼关键结论、待办事项、决策
  3. 生成总结 Markdown
  4. lark-cli docs +create 创建总结文档
  5. lark-cli im +messages-send 发送总结链接到群
```

### 场景4：智能日程管理

```
触发：用户自然语言"帮我约张三和李四明天下午开会"
流程：
  1. 解析自然语言 → 提取时间/人员/主题
  2. lark-cli calendar freebusy-get 查询忙闲
  3. 选择最早可用时段
  4. 创建日历事件 + 邀请参会
  5. 返回会议链接
```

### 场景5：运营素材批量生成

```
触发：选题表就绪
流程：
  1. 读取飞书 Base 选题表
  2. LLM 批量生成内容
  3. 写回飞书表格（状态列更新）
  4. 可选：lark-doc 生成初稿文档
```

---

## 八、错误处理与重试矩阵

### 8.1 错误码速查

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 999916 | tenant_access_token 过期 | 刷新 token 重试 |
| 999914 | 请求参数错误 | 检查请求体格式 |
| 230001 | 文档不存在 | 检查 document_id |
| 170001 | 用户不存在 | 检查 open_id / user_id |
| 190001 | 权限不足 | 飞书开放平台开通对应 scope |
| 429 | 请求频率限制 | 指数退避重试（1s/2s/4s） |
| 999915 | App 未发布 | 飞书开放平台发布应用 |

### 8.2 通用重试装饰器

```python
import time
from functools import wraps

def feishu_retry(max_retries=3, base_delay=1):
    """飞书 API 通用重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                resp = func(*args, **kwargs)
                code = resp.json().get("code", 0)
                
                if code == 0:
                    return resp
                if code == 999916:  # Token 过期
                    refresh_token()
                    continue
                if resp.status_code == 429:  # 限流
                    time.sleep(base_delay * (2 ** attempt))
                    continue
                if code in [999914, 190001]:  # 不可重试错误
                    raise Exception(f"不可重试错误: code={code}, msg={resp.json().get('msg')}")
                    
                time.sleep(base_delay * (2 ** attempt))
            raise Exception(f"超过最大重试次数 {max_retries}")
        return wrapper
    return decorator
```

---

## 九、权限配置检查清单

```markdown
[ ] 飞书开放平台创建企业自建应用
[ ] 应用已发布（状态：已启用）
[ ] App ID + App Secret 已安全保管
[ ] 必要权限 scope 已开通并批量授权
[ ] 安全设置中添加了回调域名/IP白名单
[ ] tenant_access_token 缓存机制就绪
[ ] Codex MCP Server 已配置并测试连通
[ ] 关键 API 调用已通过 CLI 或 Postman 验证
[ ] 代码中 App Secret 不硬编码，使用 .env 管理
[ ] 审计日志已开启
```

---

## 十、安全注意事项

| 风险点 | 防护措施 |
|--------|---------|
| Token/Secret 泄露 | `.env` 管理，`.gitignore` 排除，定期轮换 |
| 权限过大 | 最小权限原则，按需申请 scope |
| 消息滥用 | 批量发送需审批；设置频率限制 |
| 数据泄露 | 敏感字段脱敏；审计日志全量保留 |
| API 配额耗尽 | 监控调用量，设置告警阈值 |
| 飞书 CLI 凭证 | 不在共享终端中回显 Secret |

---

## 十一、常见问题排查

| 症状 | 原因 | 解决 |
|------|------|------|
| 999916 错误 | Token过期 | 刷新 tenant_access_token |
| 190001 权限不足 | scope未开通 | 飞书开放平台→权限管理→开通 |
| MCP工具不可见 | 配置未生效 | 重启 Codex Session，`/mcp list` 检查 |
| 消息发送失败 | receive_id类型错误 | 检查 open_id/chat_id/email 映射 |
| 文档追加位置异常 | parent_block_id错误 | 先 GET 文档结构确认 block_id |
| lark-cli 命令未找到 | CLI 未安装 | 重新执行安装命令 |
| 飞书应用未发布 | 状态为草稿 | 飞书开放平台→发布应用 |

---

> **技能归属**：龙虾全域技能池 · Codex+飞书CLI自动化
> **关联协议**：#135 Claude Code四件套、#121 A2A+MCP三层协议栈、#95 事件驱动Trigger流水线
> **下次迭代**：飞书机器人事件订阅 Webhook 全自动化、Codex Plugin 发布到社区市场
