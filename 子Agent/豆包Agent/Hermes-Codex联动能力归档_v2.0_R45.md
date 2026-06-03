# Hermes-Codex 联动能力归档 v2.0

> **版本**：v2.0 | **迭代轮次**：R45 | **日期**：2026-06-02
> **来源**：Hermes 官方文档 (hermes-doc.aigc.green) + Codex CLI 0.130.0
> **关联协议**：#141 Coze3.0三Agent协同、#142 Hermes架构对齐
> **状态**：✅ 已完成

---

## 一、架构总览

Hermes 将 `openai/*` 和 `openai-codex/*` 轮次交给 Codex CLI app-server 处理，自身成为外围壳层：

- **Hermes 壳层职责**：会话数据库、斜杠命令、网关、记忆和技能审查
- **Codex 核心职责**：终端命令、文件编辑、沙箱和 MCP 工具调用
- **认证方式**：通过 ChatGPT 订阅认证（无需 API 密钥）

### 三层工具来源

| 层级 | 来源 | 说明 |
|------|------|------|
| L1 | Codex 内置工具集（5个） | shell / apply_patch / update_plan / view_image / web_search |
| L2 | 原生 Codex 插件 | Linear / GitHub / Gmail / Calendar / Canva 等 |
| L3 | Hermes MCP 回调 | web_search / browser_* / vision_analyze / image_generate / skill_* / tts |

### ASCII 架构图

```
Hermes shell (CLI / TUI / gateway)
    │
    ▼
AIAgent.run_conversation()
    │ api_mode == codex_app_server
    ▼
CodexAppServerSession ─── JSON-RPC over stdio ───→ codex app-server (子进程)
                                                        │
                                                        ├── shell + apply_patch + update_plan
                                                        ├── view_image + sandbox
                                                        └── MCP 客户端
                                                             ├── 用户 MCP 服务器
                                                             ├── 原生插件 (linear, github, gmail, …)
                                                             └── hermes_tools_mcp_server (回调)
                                                                   └── web_search, browser_*, vision, …
```

---

## 二、Codex 内置工具集（5个）

| 工具 | 功能 | 说明 |
|------|------|------|
| `shell` | 沙箱内运行任意 shell 命令 | 读/写/搜索/查找/运行，seatbelt/landlock 沙箱保护 |
| `apply_patch` | Codex 补丁格式结构化多文件编辑 | 非平凡代码编辑（添加函数、跨文件重构），单次写入可走 shell heredocs |
| `update_plan` | 内部待办/计划跟踪器 | 相当于 Hermes 的 `todo` 工具，完全在 Codex 运行时内管理 |
| `view_image` | 本地图像文件加载 | 将图像加载到对话中供模型查看 |
| `web_search` | 内置网络搜索 | Codex 自带搜索，与 Hermes 回调版（Firecrawl）并存，模型自行选择 |

---

## 三、原生 Codex 插件迁移

通过 `plugin/list` RPC 自动发现已安装插件，自动写入 `[plugins."<name>@openai-curated"]` 配置。

### 已迁移插件清单

| 插件 | 功能 | 迁移方式 |
|------|------|---------|
| Linear | 查找/更新 issue | 自动 |
| GitHub | 搜索代码、查看 PR、评论 | 自动 |
| Gmail | 读取/发送邮件 | 自动 |
| Google Calendar | 创建/查找事件 | 自动 |
| Outlook 日历/邮件 | 通过 Microsoft 连接器 | 自动 |
| Canva | 设计生成 | 自动 |

### 不迁移的情况

- 尚未安装的插件（需先在 Codex 中安装）
- `availability != AVAILABLE` 的插件（安装损坏、OAuth 过期等）
- ChatGPT 应用市场条目（`app/list`，已通过账户认证在 Codex 中启用）

---

## 四、Hermes MCP 回调工具

注册为 `hermes-tools` MCP 服务器，通过 stdio 通信。当 Codex 需要其内置工具之外的能力时，生成 `hermes_tools_mcp_server` 子进程回调。

### 可用工具

| 工具 | 功能 |
|------|------|
| `web_search` / `web_extract` | 基于 Firecrawl 的网络搜索与内容提取 |
| `browser_navigate` / `browser_click` / `browser_type` / `browser_press` | 浏览器自动化操作 |
| `browser_snapshot` / `browser_scroll` / `browser_back` | 浏览器状态管理 |
| `browser_get_images` / `browser_console` / `browser_vision` | 浏览器高级功能 |
| `vision_analyze` | 调用视觉模型检查图像 |
| `image_generate` | 通过 Hermes image_gen 插件链生成图像 |
| `skill_view` / `skills_list` | 读取 Hermes 技能库 |
| `text_to_speech` | TTS 文本转语音 |

### 不可用工具（需 AIAgent 上下文）

| 工具 | 原因 |
|------|------|
| `delegate_task` | 需要 Agent 循环上下文派发子 Agent |
| `memory` | 需要 AIAgent 中间循环状态 |
| `session_search` | 需要 AIAgent 上下文 |
| `todo` | 需要 AIAgent 上下文（Codex `update_plan` 是运行时内等价功能） |

---

## 五、工作流功能

### /goal（Ralph 循环）

- **可用**，`state_meta` 以会话 ID 为键持久化
- 续写提示通过 `run_conversation()` 作为普通用户消息反馈
- 注意：每次续写是全新 Codex 回合，审批策略从头评估
- 建议设置 `default_permissions = ":workspace"` 减少审批提示

### 看板（多 Agent 工作树分发）

- **可用**，通过 `HERMES_KANBAN_TASK` 环境变量传递
- 工作进程作为独立 `hermes chat -q` 子进程启动
- 看板工具（`kanban_complete` / `kanban_block` / `kanban_comment` 等）通过 MCP 回调暴露
- 沙箱配置：保留 `workspace-write`，额外添加看板数据库目录为可写根目录

### 定时任务

- 未专门测试，配置中设置 `openai_runtime: codex_app_server` 即生效
- 定时任务通过 `cronjob → AIAgent.run_conversation` 运行
- 依赖 `delegate_task` / `memory` / `session_search` / `todo` 的定时任务需限定使用默认运行时

---

## 六、审批机制

Codex 执行前请求批准，转为 Hermes"危险命令"提示：

```
╭───────────────────────────────────────╮
│ 危险命令                              │
│ /bin/bash -lc 'echo hello > foo.txt'  │
│ ❯ 1. 允许一次                         │
│   2. 本次会话内允许                    │
│   3. 拒绝                             │
╰───────────────────────────────────────╯
```

### 三种权限配置文件

| 配置文件 | 行为 |
|---------|------|
| `:read-only` | 不允许写入，每个 shell 命令都需要审批 |
| `:workspace` | 允许当前工作区内写入，无需提示（启用运行时后 Hermes 默认） |
| `:danger-no-sandbox` | 完全无沙箱（除非理解其含义，否则不要使用） |

- `apply_patch` 审批：Hermes 显示更改摘要（如 `1 add, 1 update: /tmp/new.py, /tmp/old.py`）

---

## 七、自我改进循环

记忆和技能提示在 Codex 运行时上持续生效：

- **计数触发**：每 10 条用户提示 → 记忆审查；每 10 次工具迭代 → 技能审查
- **事件映射**：Codex 的 `commandExecution` / `fileChange` / `mcpToolCall` / `dynamicToolCall` 投射为合成的 `assistant tool_call` + `tool` 结果消息
- **Review 降级**：当父 Agent 运行在 `codex_app_server` 时，review 分支降级为 `codex_responses`（直接与 OpenAI Responses API 通信），确保 `memory` / `skill_manage` 等 Agent 循环工具正常工作

---

## 八、启用方式

```
/codex-runtime codex_app_server
```

**前提条件**：
1. Codex CLI 已安装：`npm i -g @openai/codex`
2. `codex login` 已完成（OAuth 认证）
3. （可选）安装 Codex 插件：`codex plugin marketplace add openai-curated`

**执行动作**：
- 验证 `codex` CLI 已安装
- 将 `model.openai_runtime: codex_app_server` 持久化到 config.yaml
- 用户 MCP 服务器从 `~/.hermes/config.yaml` 迁移到 `~/.codex/config.toml`
- 发现并迁移已安装的原生 Codex 插件
- 将 Hermes 工具注册为 MCP 服务器
- 写入 `default_permissions = ":workspace"`

---

## 九、MCP 服务器迁移

Hermes `config.yaml` → Codex `config.toml` 自动转换：

| Hermes 字段 | Codex 字段 |
|------------|-----------|
| `command` + `args` + `env` | stdio 传输 |
| `url` + `headers` | streamable_http 传输 |
| `timeout` | `tool_timeout_sec` |
| `connect_timeout` | `startup_timeout_sec` |
| `enabled: false` | `enabled = false` |

不迁移：Hermes 特有的 `sampling` 键（Codex MCP 客户端无对应项，丢弃并警告）。

---

## 十、安全编辑 ~/.codex/config.toml

受管理内容包裹在两个标记注释之间：

```toml
# ═══════════════════════════════════════════
# managed by hermes-agent — do not edit below
# ═══════════════════════════════════════════
default_permissions = ":workspace"
[mcp_servers.filesystem]
...
[plugins."github@openai-curated"]
...
# ═══════════════════════════════════════════
# end managed by hermes-agent
# ═══════════════════════════════════════════
```

- 管理块之外的内容属于用户，重新迁移时保留
- 可添加自定义 MCP 服务器、覆盖 `default_permissions`、配置 Codex 专属选项

---

## 十一、标准调用指令

| 指令 | 功能 | 说明 |
|------|------|------|
| `/codex-runtime codex_app_server` | 启用 Codex 运行时 | 下次会话生效 |
| `/codex-runtime auto` | 禁用，切回默认运行时 | 下次会话生效 |
| `/codex-runtime` | 查询当前状态 | 无参数，仅查询 |

也可在 `~/.hermes/config.yaml` 中手动设置：
```yaml
model:
  openai_runtime: codex_app_server
```

---

## 十二、结果输出范式

### 标准 JSON 格式

```json
{
  "status": "success|error|needs_params|handoff",
  "result": {},
  "metadata": {
    "task_id": "xxx",
    "trace_id": "xxx",
    "timestamp": "2026-06-02T00:00:00+08:00"
  }
}
```

### 任务派发 XML 格式

```xml
<overall_goal>
{Hermes 层面的任务总目标}
</overall_goal>

<current_task>
{Codex 需要执行的具体任务描述}
</current_task>
```

### 错误返回

```json
{
  "status": "error",
  "error_type": "unauthorized|timeout|missing_params|execution_failed",
  "error_message": "...",
  "retry_count": 0,
  "fallback": "..."
}
```

---

## 功能对比速查表

| 功能 | Hermes 默认运行时 | Codex app-server |
|------|:---:|:---:|
| `delegate_task` 子 Agent | ✅ | ❌ |
| `memory` / `session_search` / `todo` | ✅ | ❌ |
| `web_search` / `web_extract` | ✅ | ✅（MCP 回调） |
| 浏览器自动化（Camofox/Browserbase） | ✅ | ✅（MCP 回调） |
| `vision_analyze` / `image_generate` | ✅ | ✅（MCP 回调） |
| `skill_view` / `skills_list` | ✅ | ✅（MCP 回调） |
| `text_to_speech` | ✅ | ✅（MCP 回调） |
| Codex `shell`（终端/读/写/搜索） | — | ✅（内置） |
| Codex `apply_patch`（结构化编辑） | — | ✅（内置） |
| Codex `update_plan`（运行时待办） | — | ✅（内置） |
| Codex `view_image`（图像加载） | — | ✅（内置） |
| Codex 沙箱（seatbelt/landlock） | — | ✅（内置） |
| ChatGPT 订阅认证 | — | ✅ |
| 原生 Codex 插件（Linear/GitHub/…） | — | ✅（自动迁移） |
| 用户 MCP 服务器 | ✅ | ✅（自动迁移） |
| 记忆 + 技能回顾（后台） | ✅ | ✅（项目投影） |
| `/goal`（Ralph 循环） | ✅ | ✅ |
| 看板工作者调度 | ✅ | ✅（回调） |
| 看板编排工具 | ✅ | ✅（回调） |

---

## 版本信息

| 字段 | 值 |
|------|-----|
| 版本 | v2.0 |
| 迭代轮次 | R45 |
| 日期 | 2026-06-02 |
| 来源 | Hermes 官方文档 (hermes-doc.aigc.green) |
| 状态 | ✅ 完成 |

## 关联文档索引

| 文档 | 路径 |
|------|------|
| AGENTS.md（Codex 配置） | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\技能库\AGENTS.md) |
| 龙虾全域官方模板 | [龙虾全域官方模板-最终版.md](E:\龙虾AI主控中心\我的AI分身\技能库\龙虾全域官方模板-最终版.md) |
| 协议 #141 Coze3.0三Agent协同 | 龙虾-Coze3.0三Agent接入协同协议 v1.0 |
| 协议 #142 Hermes架构对齐 | 龙虾-Hermes v0.15架构对齐协议 v1.0 |
| R45 迭代日志 | [20260602_R45_Hermes-Codex联动迭代日志.md](E:\龙虾AI主控中心\我的AI分身\迭代报告归档\20260602_R45_Hermes-Codex联动迭代日志.md) |

## 下一步优化方向

1. **双运行时智能路由**：根据任务特征自动选择 Hermes 默认运行时或 Codex 运行时，无需手动 `/codex-runtime` 切换
2. **Agent 循环工具桥接**：探索 `delegate_task` / `memory` / `session_search` 在 Codex 运行时上的 MCP 回调可行性
3. **定时任务 Codex 运行时验证**：完整测试 cron 任务在 Codex 运行时上的稳定性与工具可用性
4. **认证统一**：调研 Hermes 与 Codex OAuth 会话共享方案，消除双认证痛点
5. **性能基准测试**：对比默认运行时与 Codex 运行时的任务完成速度、Token 消耗、成功率
