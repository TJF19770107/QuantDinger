# Codex + 飞书 CLI 自动化技能手册 v1.2

> **版本**：v1.2（R28迭代 · 2026-06-01）
> **来源**：公众号「我姚学AI」《如何通过 Codex 对话接入飞书完整版来了！》
> **作者**：姚路行
> **生效范围**：全域 / 永久 / 永恒
> **关联模板**：龙虾全域官方模板-最终版.md v3.20

---

## 一、概述

Codex 通过飞书 CLI 可以接入飞书全生态能力，实现：创建/更新文档、读写 Base、查日历、发消息、管任务、邮箱、知识库、会议纪要等。本文档提供标准化接入流程与自动化场景 SOP。

---

## 二、接入四步流程（保姆级）

### 第 1 步：安装飞书 CLI

在 Codex 对话中直接描述需求，Codex 自动生成安装命令：

```
用户 → Codex：「帮我安装飞书 CLI」
Codex → 自动执行 npm/brew 安装命令
```

**预计耗时**：4～5分钟

**安装完成后验证**：
```
lark-cli --version
```

### 第 2 步：配置飞书应用

让 Codex 输出配置链接，在浏览器中完成应用创建：

```
用户 → Codex：「帮我初始化飞书 CLI 配置，输出浏览器可访问的配置链接」
```

操作流程：
1. 打开 Codex 输出的配置链接
2. 按页面提示创建飞书应用（或绑定已有应用）
3. 获取 **App ID** 和 **App Secret**
4. 将凭据交回 Codex 完成配置

**关键配置项**：
| 参数 | 说明 | 获取方式 |
|------|------|---------|
| App ID | 飞书应用唯一标识 | 飞书开放平台 → 应用详情 |
| App Secret | 飞书应用密钥 | 飞书开放平台 → 应用详情 → 凭证与基础信息 |

### 第 3 步：登录授权

完成用户 OAuth 授权：

```
用户 → Codex：「帮我完成飞书用户授权，输出浏览器可访问的授权链接」
```

操作流程：
1. 打开 Codex 输出的授权链接
2. 浏览器中确认授权
3. 授权完成，飞书 CLI 与 Codex 链路打通

**权限范围建议**（按需勾选）：
- 日历读写
- 文档创建与编辑
- Base 读写
- 消息发送
- 通讯录读取

### 第 4 步：验证接入

执行低风险验证命令，确认链路通畅：

```
用户 → Codex：「在飞书日历中创建一个下周一 8:00 的事件，标题为"测试接入"」
```

验证标准：
- 日历中能看到该事件 → 权限和链路正常
- 出现权限错误 → 回到第 3 步，检查应用权限配置
- 出现网络错误 → 检查 CLI 版本和网络连通性

---

## 三、飞书 CLI 核心命令体系

### 3.1 命令总览（11 大业务域）

| 业务域 | CLI 前缀 | 核心能力 |
|--------|---------|---------|
| 即时通讯 | `lark-cli im` | 发消息、搜群、管理成员、消息总结 |
| 云文档 | `lark-cli docs` | 创建/读取/更新文档、Markdown 双向转换 |
| 日历 | `lark-cli calendar` | 查日程、建事件、查忙闲、邀请参会 |
| 邮件 | `lark-cli mail` | 收发邮件、管理草稿 |
| 电子表格 | `lark-cli sheets` | 读写单元格、批量追加 |
| 多维表格 | `lark-cli base` | 增删改查、聚合分析、仪表盘 |
| 任务 | `lark-cli task` | 创建/完成/分配任务 |
| 知识库 | `lark-cli wiki` | 浏览节点、创建文档 |
| 通讯录 | `lark-cli contact` | 搜同事、查部门 |
| 会议纪要 | `lark-cli vc` | 妙记摘要、待办、逐字稿 |
| 搜索 | `lark-cli search` | 跨业务域搜索 |

### 3.2 常用命令示例

#### 文档操作
```bash
# 创建飞书文档
lark-cli docs +create --title "周报-2026年第22周" --content "# 本周工作总结\n..."

# 读取飞书文档
lark-cli docs +view --doc-id <文档ID>

# 更新飞书文档
lark-cli docs +update --doc-id <文档ID> --content "更新后的内容"
```

#### Base 多维表格操作
```bash
# 创建记录
lark-cli base record-create --app-token <Base Token> --table-id <表ID> --fields '{"名称":"项目A","状态":"进行中"}'

# 查询记录
lark-cli base record-list --app-token <Base Token> --table-id <表ID> --filter "状态=进行中"

# 更新记录
lark-cli base record-update --app-token <Base Token> --table-id <表ID> --record-id <记录ID> --fields '{"状态":"已完成"}'
```

#### 日历操作
```bash
# 创建日程
lark-cli calendar event-create --summary "项目评审" --start "2026-06-01T14:00:00+08:00" --end "2026-06-01T15:00:00+08:00"

# 查忙闲
lark-cli calendar freebusy --start "2026-06-01T09:00:00+08:00" --end "2026-06-01T18:00:00+08:00"
```

#### 消息发送
```bash
# 发送文本消息
lark-cli im +messages-send --receive-id <群ID/用户ID> --content "自动化通知：任务已完成"

# 发送富文本卡片消息
lark-cli im +messages-send --receive-id <群ID> --msg-type interactive --card '{"header":{"title":"日报汇总"},"elements":[{"tag":"markdown","content":"## 今日完成\n- 任务1\n- 任务2"}]}'
```

#### 会议纪要
```bash
# 获取妙记摘要
lark-cli vc +minutes-summary --meeting-id <会议ID>

# 获取会议待办
lark-cli vc +minutes-todo --meeting-id <会议ID>
```

---

## 四、权限配置指南

### 4.1 最小权限原则

| 场景 | 所需权限 | 权限范围 |
|------|---------|---------|
| 自动发通知 | 消息发送 | `im:message:send` |
| 生成日报 | 文档创建、消息发送 | `doc:create` + `im:message:send` |
| 数据报表 | Base 读写 | `base:read` + `base:write` |
| 智能日程 | 日历读写、忙闲查询 | `calendar:read` + `calendar:write` |
| 会议助理 | 会议信息、妙记 | `vc:read` + `minutes:read` |

### 4.2 权限申请流程

```
飞书开放平台 → 我的应用 → [选择应用] → 权限管理 → 添加权限 → 提交审核 → 管理员通过 → 生效
```

---

## 五、5 大自动化场景 SOP

### 场景 1：AI 调研 → 飞书文档

```
触发：用户指定调研主题
流程：
  1. Codex 执行 web_search / 浏览器检索
  2. LLM 提炼关键信息 → 生成 Markdown 结构
  3. lark-cli docs +create 创建飞书文档
  4. 返回文档链接
适用：竞品分析、技术调研、行业报告
```

### 场景 2：批量数据 → 飞书 Base

```
触发：CSV/JSON/Excel 数据文件
流程：
  1. 解析数据文件结构
  2. 映射到 Base 字段
  3. 批量 lark-cli base record-create
  4. 返回表格链接
适用：客户名单导入、票据整理、项目跟踪
```

### 场景 3：群消息智能总结

```
触发：指定群聊 + 时间范围
流程：
  1. lark-cli im +messages-history 获取消息
  2. LLM 提炼主题/结论/待办
  3. 生成总结 → 发送回群 / 创建文档
适用：长群聊总结、会议回顾、信息归档
```

### 场景 4：日程智能管理

```
触发：指定参会者 + 时间范围
流程：
  1. lark-cli calendar freebusy 查忙闲
  2. 找到共同空闲时段
  3. lark-cli calendar event-create 创建日程
  4. 发送日历邀请
适用：多方会议排期、面试安排、项目里程碑
```

### 场景 5：运营素材批量生成

```
触发：选题表（飞书Base）
流程：
  1. lark-cli base record-list 读取选题
  2. LLM 批量生成文案
  3. 回写飞书 Base 表格
  4. 可选：对接 Canva API 导出图片
适用：公众号排期、社媒运营、电商详情页
```

---

## 六、错误处理与故障排查

| 错误类型 | 原因 | 解决方案 |
|---------|------|---------|
| `unauthorized` | App Secret 过期或错误 | 重新生成 App Secret 并更新配置 |
| `permission denied` | 应用未申请对应权限 | 开放平台添加权限 → 管理员审核 |
| `rate limit` | API 调用频率超限 | 降低调用频率，增加间隔 |
| `token expired` | 授权 Token 过期 | 重新执行登录授权流程 |
| `network error` | CLI 网络不通 | 检查代理/防火墙，确认飞书 API 可达 |
| `invalid params` | 参数格式不正确 | 检查参数 JSON 格式和必填字段 |

---

## 七、Codex 对话模板

### 模板 1：日常总结
```
「帮我总结今天飞书群 [群名] 里的讨论要点，创建为飞书文档并发送到群里」
```

### 模板 2：数据报表
```
「读取 [Base表URL] 中本周数据，生成分析报告，创建为飞书文档并发送给 [同事名]」
```

### 模板 3：智能排期
```
「帮我找一个下周三 [同事A] 和 [同事B] 都有空的时间，创建 1 小时的项目评审会议」
```

---

## 八、安全注意事项

- App Secret 不得明文存储在公开仓库
- 生产环境建议使用飞书应用商店发布的应用
- 定期轮换 App Secret
- 遵循「最小权限原则」配置应用权限
- 敏感操作（删除文档、踢出群成员）需二次确认
- 自动化脚本需加入人工审核节点

---

## 九、R28 新增：Codex Triggers + 飞书自动化增强

### 9.1 Codex Triggers 事件驱动

```
GitHub Issue → Codex Triggers → 自动分析 → 开PR修复 → 飞书通知
```

### 9.2 飞书 CLI 与 Codex Mobile 联动

```
Codex Mobile（锁屏Mac）→ Appshots 截图注入 → AI分析 → 飞书消息推送
```

### 9.3 Codex Developer OS 集成模式

```
Claude.md 持久上下文 → Skills模块 → Subagents → 飞书 CLI 插件 → 全链路自动化
```

---

> **版本**：v1.2
> **最后更新**：2026-06-01 R28
> **来源文章**：https://mp.weixin.qq.com/s/lp1fV7O1flKzV1AgeMBQ3A
> **关联模板**：龙虾全域官方模板-最终版.md v3.20
