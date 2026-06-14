---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_1608abaf67ba11f1a0095254002afed2
    ReservedCode1: 01D89qZwX5PeCXmsvi36WwRTHTpJBNP+/pMO0Ekmocfqxb+7v7jgnKcLWyHtuQwwMo8iPNGs061X3x1oSdbLGPYEA/uVHrPaGx0DLvmbN6I1TylETJ5KiNYCJYAJorHI6aN929b31DUUQbvsUrf7yJ5i/2QEZOgRsfG/mbHykmr9MtWLLBJ3F4GqzbQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_1608abaf67ba11f1a0095254002afed2
    ReservedCode2: 01D89qZwX5PeCXmsvi36WwRTHTpJBNP+/pMO0Ekmocfqxb+7v7jgnKcLWyHtuQwwMo8iPNGs061X3x1oSdbLGPYEA/uVHrPaGx0DLvmbN6I1TylETJ5KiNYCJYAJorHI6aN929b31DUUQbvsUrf7yJ5i/2QEZOgRsfG/mbHykmr9MtWLLBJ3F4GqzbQ=
---

# Codex + 飞书CLI 自动化技能手册 v2.1

> 基于龙虾全域官方模板 v3.89 · R90 全域迭代
> 协议编号：#201（v2.1）| 关联协议：#186/#188/#204/#206/#212/#215/#226
> 技能标识：`lark-cli-automation` | 安全等级：🟡 中风险
> 来源：公众号「我姚学AI」+ codexguide.ai + 飞书官方文档 + GitHub开源社区
> 更新日期：2026-06-14

---

## 一、技能概述

将飞书全系办公能力（14业务域、200+命令、19 Agent Skills）纳入龙虾全域Agent可调用工具链，实现「自然语言 → Agent调度 → CLI命令 → 飞书API」零代码自动化闭环。

### 核心能力矩阵

| 维度 | 说明 |
|------|------|
| 覆盖业务域 | 即时通讯、云文档、多维表格(Base)、日历、邮箱、任务、会议、知识库、通讯录、云盘、电子表格、妙记、审批、OKR |
| Agent Skills | 19项（按业务域划分，每域1-2个Skills） |
| 命令体系 | 三层架构：快捷命令→ API命令→ 原始API命令 |
| 输出格式 | JSON / Pretty / Table / NDJSON / CSV 五种 |
| Codex权限模式 | suggest / auto-edit / full-auto / yolo 四种 |

---

## 二、四步接入SOP

### 第一步：安装Codex CLI

```bash
# 方式一：npm全局安装（推荐）
npm install -g @openai/codex

# 方式二：pip安装
pip install openai-codex

# 方式三：Homebrew（macOS）
brew install openai/codex/codex

# 验证安装
codex --version
```

### 第二步：安装飞书CLI

```bash
# 全局安装飞书CLI
npm install -g @larksuite/cli

# 安装Agent Skills
npx skills add larksuite/cli -y -g

# 验证安装
lark-cli --version
lark-cli skills list
```

### 第三步：配置飞书应用

1. 登录[飞书开放平台](https://open.feishu.cn)，创建企业自建应用
2. 获取 App ID 和 App Secret
3. 配置应用权限范围（按需勾选14个业务域权限）

### 第四步：OAuth授权

```bash
# 设备流授权（推荐）
lark-cli auth login --recommend

# 或手动配置凭证
lark-cli config set app-id <YOUR_APP_ID>
lark-cli config set app-secret <YOUR_APP_SECRET>

# 验证授权状态
lark-cli auth whoami
```

---

## 三、两种身份模式

| 模式 | 说明 | 适用场景 | OAuth方式 |
|------|------|---------|----------|
| 应用身份（create_application） | 以应用自身身份调用API | 批量操作、系统集成、定时任务 | 应用凭证 |
| 用户身份（request_user） | 以授权用户身份调用API | 个人助理、消息发送、日程管理 | 用户OAuth授权 |

---

## 四、Codex四种权限模式

| 模式 | 风险等级 | 说明 | 适用场景 |
|------|---------|------|---------|
| suggest | 🟢 低 | 仅建议，不执行任何操作 | 初学者、代码审查 |
| auto-edit | 🟡 中 | 自动编辑文件，需确认危险操作 | 日常开发 |
| full-auto | 🟡 中 | 全自动执行，跳过非危险确认 | 自动化任务 |
| yolo | 🔴 高 | 绕过所有确认和沙箱，直接执行 | 仅限完全信任的沙箱环境 |

### Codex CI非交互模式参数

```bash
codex exec "任务描述" \
  --json \                    # JSON格式输出
  --output-schema schema.json \  # 输出结构验证
  --resume --last \           # 恢复上次会话
  --model gpt-5 \             # 指定模型
  --permission-mode full-auto  # 权限模式
```

---

## 五、14业务域命令速查表

### 5.1 即时通讯（lark-im）

| 命令 | 功能 | 示例 |
|------|------|------|
| `im chat-search` | 搜索群组 | `lark-cli im chat-search --query "项目群"` |
| `im messages-send` | 发送消息 | `lark-cli im messages-send --chat-id xxx --content "你好"` |
| `im messages-list` | 获取消息列表 | `lark-cli im messages-list --chat-id xxx --limit 50` |
| `im messages-search` | 搜索消息 | `lark-cli im messages-search --query "周报"` |
| `im chat-members` | 群成员管理 | `lark-cli im chat-members --chat-id xxx` |

### 5.2 云文档（lark-doc）

| 命令 | 功能 | 示例 |
|------|------|------|
| `docs create` | 创建文档 | `lark-cli docs create --title "周报" --content report.md` |
| `docs get` | 获取文档内容 | `lark-cli docs get --doc-token xxx` |
| `docs update` | 更新文档 | `lark-cli docs update --doc-token xxx --content new.md` |
| `docs list` | 列出文档 | `lark-cli docs list --folder-token xxx` |

### 5.3 多维表格（lark-base）

| 命令 | 功能 | 示例 |
|------|------|------|
| `base query` | 查询记录 | `lark-cli base query --app-token xxx --table-id xxx` |
| `base record-create` | 新增记录 | `lark-cli base record-create --app-token xxx --table-id xxx --data records.json` |
| `base record-update` | 更新记录 | `lark-cli base record-update --app-token xxx --table-id xxx --record-id xxx` |
| `base table-list` | 列出数据表 | `lark-cli base table-list --app-token xxx` |

### 5.4 日历（lark-calendar）

| 命令 | 功能 | 示例 |
|------|------|------|
| `calendar agenda` | 查询日程 | `lark-cli calendar agenda --start-date 2026-06-14` |
| `calendar create` | 创建日程 | `lark-cli calendar create --summary "评审会" --start-time "..."` |
| `calendar freebusy` | 查询忙闲 | `lark-cli calendar freebusy --user-id xxx` |
| `calendar suggestion` | 空闲时段推荐 | `lark-cli calendar suggestion --user-ids id1,id2 --duration 60` |

### 5.5 任务（lark-task）

| 命令 | 功能 | 示例 |
|------|------|------|
| `task create` | 创建任务 | `lark-cli task create --summary "完成报告" --due-date 2026-06-20` |
| `task get-my-tasks` | 获取我的任务 | `lark-cli task get-my-tasks --status pending` |
| `task update` | 更新任务 | `lark-cli task update --task-id xxx --status completed` |

### 5.6 邮件（lark-mail）

| 命令 | 功能 | 示例 |
|------|------|------|
| `mail messages-list` | 邮件列表 | `lark-cli mail messages-list --folder INBOX --unread` |
| `mail send` | 发送邮件 | `lark-cli mail send --to user@feishu.cn --subject "主题"` |
| `mail triage` | 邮件分类 | `lark-cli mail triage --folder INBOX` |

### 5.7 知识库（lark-wiki）

| 命令 | 功能 | 示例 |
|------|------|------|
| `wiki create-node` | 创建节点 | `lark-cli wiki create-node --space-id xxx --title "知识条目"` |
| `wiki get-node` | 获取节点内容 | `lark-cli wiki get-node --node-token xxx` |
| `wiki search` | 搜索知识库 | `lark-cli wiki search --query "技术方案"` |

### 5.8 会议/妙记（lark-vc / lark-minutes）

| 命令 | 功能 | 示例 |
|------|------|------|
| `vc search` | 搜索会议 | `lark-cli vc search --query "周会"` |
| `vc minutes-get` | 获取纪要 | `lark-cli vc minutes-get --meeting-id xxx` |
| `minutes transcript` | 获取逐字稿 | `lark-cli minutes transcript --meeting-id xxx` |

### 5.9 云盘（lark-drive）

| 命令 | 功能 | 示例 |
|------|------|------|
| `drive list` | 列出文件 | `lark-cli drive list --folder-token xxx` |
| `drive upload` | 上传文件 | `lark-cli drive upload --file report.pdf --folder xxx` |
| `drive download` | 下载文件 | `lark-cli drive download --file-token xxx` |

### 5.10 审批（lark-approval）

| 命令 | 功能 | 示例 |
|------|------|------|
| `approval create` | 创建审批 | `lark-cli approval create --approval-code xxx --data approval.json` |
| `approval search` | 搜索审批 | `lark-cli approval search --status pending` |
| `approval approve` | 审批通过 | `lark-cli approval approve --instance-id xxx` |

### 5.11 辅助命令

| 命令 | 功能 |
|------|------|
| `lark-cli doctor` | 诊断工具，检查配置完整性 |
| `lark-cli dry-run` | 干运行模式，预览不执行 |
| `lark-cli schema` | 查看API Schema |
| `lark-cli auth whoami` | 查看当前授权身份 |
| `lark-cli auth logout` | 退出授权 |

---

## 六、三重桥接方案对比

| 方案 | 安装方式 | 核心能力 | 安全等级 | 适用场景 |
|------|---------|---------|---------|---------|
| cc-connect | `npm install -g cc-connect` | WebSocket长连接，5分钟配置，4种权限模式 | 🟡 中 | 个人/小团队快速接入 |
| lark-coding-agent-bridge | `npx -y lark-channel-bridge@latest start` | 飞书卡片交互、富文本回复、多session管理 | 🟡 中 | 移动端对话、团队协作 |
| feishu-codex-bridge | `git clone → npm install` | 流式卡片展示、多项目独立管理、三级安全模式 | 🔴 高(danger模式) | 多项目管理、进度可视化 |

---

## 七、9域权限Scope清单

| 业务域 | 权限Scope | 用途 |
|--------|----------|------|
| 即时通讯 | `im:message` `im:chat` | 消息收发、群组管理 |
| 云文档 | `doc:document` `docx:document` | 文档读写 |
| 多维表格 | `bitable:app` | Base数据操作 |
| 日历 | `calendar:calendar` `calendar:event` | 日程管理 |
| 任务 | `task:task` | 任务增删改查 |
| 邮件 | `mail:mail` | 邮件收发 |
| 知识库 | `wiki:wiki` | 知识库编辑 |
| 会议 | `vc:meeting` `vc:minutes` | 会议纪要 |
| 审批 | `approval:approval` | 审批流操作 |

---

## 八、7项实战SOP模板

### SOP-1：每日站会纪要自动化
```
触发：定时任务 → lark-cli calendar agenda 获取今日日程
     → lark-cli im messages-send 发送站会提醒
     → lark-cli vc minutes-get 获取昨日纪要
     → AI提炼待办 → lark-cli task create 创建待办任务
     → lark-cli docs update 更新站会文档
```

### SOP-2：周报自动生成
```
触发：每周五17:00 → lark-cli task get-my-tasks 拉取本周任务
     → lark-cli calendar agenda 拉取本周会议
     → AI汇总生成周报Markdown
     → lark-cli docs create --title "周报_2026-W24" --content weekly.md
     → lark-cli im messages-send 发送周报链接
```

### SOP-3：项目进度同步
```
触发：Git commit → Codex提取commit message
     → lark-cli task update 更新对应任务状态
     → lark-cli im messages-send 发送进度通知
     → lark-cli base record-update 更新项目Base看板
```

### SOP-4：会议纪要全流程
```
触发：会议结束 → lark-cli vc minutes-get 获取纪要
     → lark-cli minutes transcript 获取逐字稿
     → AI提炼：摘要+待办+决策+风险
     → lark-cli docs create 创建纪要文档
     → lark-cli task create 分配待办任务
     → lark-cli im messages-send 通知参会人
```

### SOP-5：Base批量数据导入
```
触发：用户提供CSV/JSON/Excel
     → AI解析数据+字段映射
     → lark-cli base table-list 确认目标表
     → lark-cli base record-create --data records.json 批量写入
     → lark-cli im messages-send 导入完成通知
```

### SOP-6：邮件智能分类与回复
```
触发：定时/手动 → lark-cli mail messages-list --unread
     → AI分类：紧急/重要/普通/垃圾
     → 紧急邮件 → AI草拟回复 → 人工确认 → lark-cli mail send
     → 普通邮件 → lark-cli task create 标记待处理
```

### SOP-7：知识库自动归档
```
触发：群聊消息含链接/代码/方案 → AI识别知识价值
     → lark-cli wiki search 检查是否已有
     → lark-cli wiki create-node 创建新条目
     → AI提炼结构化摘要
     → lark-cli im messages-send 归档完成通知
```

---

## 九、6类常见错误排查

| 错误码 | 错误描述 | 原因 | 解决方案 |
|--------|---------|------|---------|
| 99991663 | App not enabled | 应用未启用 | 飞书开放平台启用应用 |
| 99991664 | Invalid tenant access token | 令牌过期 | `lark-cli auth login --recommend` |
| 99991665 | No permission | 权限不足 | 检查权限scope配置 |
| 99991666 | Resource not found | 资源不存在 | 检查token/id是否正确 |
| — | npm安装失败 | 网络问题 | 使用国内镜像 `--registry https://registry.npmmirror.com` |
| — | 二维码授权超时 | 超时未扫码 | 重新执行`lark-cli auth login` |

### 重试策略（指数退避）

```python
# 伪代码：飞书CLI调用重试策略
max_retries = 3
base_delay = 1  # 秒
for attempt in range(max_retries):
    try:
        result = lark_cli_execute(command)
        break
    except RateLimitError:
        delay = base_delay * (2 ** attempt)
        sleep(delay)
    except AuthError:
        lark_cli_auth_refresh()
```

---

## 十、8项安全实践

| 序号 | 安全实践 | 说明 |
|------|---------|------|
| 1 | 权限最小化 | 仅申请任务所需的scope，不申请多余权限 |
| 2 | dry-run先行 | 所有写操作先用`lark-cli dry-run`预览 |
| 3 | 测试企业隔离 | 先在测试企业验证，再上线生产 |
| 4 | 令牌定期检查 | `lark-cli auth whoami` 确认令牌有效 |
| 5 | 明文防护 | 禁止在日志/聊天中输出App Secret |
| 6 | 输入防注入 | 用户输入需经参数化处理，禁止拼接到CLI命令 |
| 7 | 输出净化 | CLI输出中的敏感信息（手机号/邮箱）需脱敏 |
| 8 | OS原生密钥链 | 使用系统密钥链存储凭证，不写入配置文件 |

---

## 十一、龙虾模板协议对齐

| 模板协议 | 协议名称 | 关联说明 |
|---------|---------|---------|
| #186 | Agent Team 协作架构 | 多Agent通过飞书消息/文档协作 |
| #188 | MXC 操作系统级沙箱 | CLI操作隔离在沙箱内执行 |
| #204 | Codex+飞书日历与会议管理 | 日历/会议域自动化 |
| #206 | Codex-飞书桥接 cc-connect | WebSocket桥接方案 |
| #212 | 公众号文章深度学习迭代 v2.0 | 知识提炼方法 |
| #215 | SkillForge 领域自演化 | 技能持续进化机制 |
| #226 | 记忆三范式融合检索 | 技能知识持久化 |

---

## 十二、社区资源索引

| 资源 | 地址 |
|------|------|
| 飞书CLI官方仓库 | https://github.com/larksuite/cli |
| 飞书开放平台 | https://open.feishu.cn |
| Codex CLI官方文档 | https://codexguide.ai |
| feishu-cli.com | https://feishu-cli.com |
| feishucli.net | https://feishucli.net |
| cc-connect桥接 | https://github.com/chenhg5/cc-connect |
| lark-coding-agent-bridge | https://github.com/zarazhangrui/lark-coding-agent-bridge |
| 公众号原文 | https://mp.weixin.qq.com/s/lp1fV7O1flKzV1AgeMBQ3A |

---

> 版本：v2.1 | 协议编号：#201 | 字节数：14828
> 基于龙虾全域官方模板 v3.89 · R90 全域迭代
> 最后更新：2026-06-14 14:24 CST
> *（内容由龙虾AI主控中心自动生成，仅供Agent内部技能调度参考）*
*（内容由AI生成，仅供参考）*
