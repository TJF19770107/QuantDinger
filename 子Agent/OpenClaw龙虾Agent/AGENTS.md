# AGENTS.md — 子代理管理与自动化配置

> **版本**：v3.1_R14 | **来源**：Anthropic Academy + Claude Code Subagents + 全域蒸馏 | **同步日期**：2026-05-31 20:00
> **本副本所属**：OpenClaw龙虾Agent（底层执行子Agent）
> **全域蒸馏更新 (R14)**：OpenClaw 37.5万⭐ v2026.5.26|MCP 1.0 Windows 11原生集成|小红书Red Skill内容创作协议|链上Agent经济协议#65|AI视频创作工业化协议#63|Pullfrog式GitHub Actions Agent#61

---

## 一、Sub Agent 清单

| Agent ID | Agent Name | 职责域 | 状态 | 路由关键词 |
|----------|-----------|--------|------|-----------|
| file-agent | File Agent | 文件搜索/读写/格式转换/归类 | ACTIVE | 文件/文档/图片/PDF/搜索/整理 |
| computer-agent | Computer Agent | Windows系统/设置/窗口/进程 | ACTIVE | 系统/设置/窗口/桌面/进程/性能 |
| app-agent | App Agent | 应用操作/APK/小程序/Steam | ACTIVE | App/APK/应用/软件/小程序/Steam/EXE |
| browser | Browser Agent | 网页交互/登录/填表 | ACTIVE | 登录/填表/网页操作 |
| search-agent | Search Agent | 深度搜索/调研/对比 | ACTIVE | 调研/对比/论文/深度搜索 |

---

## 二、dispatch_task 规范化模板

### 2.1 标准调用格式

```
dispatch_task(
    agent_name="<目标Agent>",
    task="
<overall_goal>
用户原始完整需求（直接复述或等价压缩）
</overall_goal>
<current_task>
本次委托具体任务（自包含、可独立执行、结果导向）
</current_task>
",
    memory_ids=["<相关历史消息memory_id>"],
    inherit_agent_id="<继承的历史Agent ID或留空>"
)
```

### 2.2 task 编写纪律

| 规则 | 正确示例 | 错误示例 |
|------|---------|---------|
| 附件透传 | `<attachments>...</attachments>` 原样拼入 current_task | 忽略附件或改写路径 |
| 精简性 | 仅写目标+路径+约束 | 复制大段历史内容到 task |
| 结果导向 | "将照片按年份归类到子文件夹" | "先列目录，再读EXIF..." |

---

## 三、Sub Agent 能力边界

### 3.1 File Agent
**能做**：搜索/读写/格式转换/归类/上传
**不能做**：系统设置、应用操作、网页交互

### 3.2 Computer Agent
**能做**：系统设置/信息查询/窗口管理/进程管理
**不能做**：第三方应用操作、文件搜索

### 3.3 App Agent
**能做**：App操作/APK管理/小程序/Steam/应用推荐
**不能做**：系统管理工具、纯文件操作

### 3.4 Browser Agent
**能做**：网页交互/登录/填表
**不能做**：纯网页内容读取（应用 web_fetch）

### 3.5 Search Agent
**能做**：深度搜索/调研/对比分析
**不能做**：本地请求、简单事实查询

---

## 四、自动化配置

### 4.1 定时任务规则

```
定时任务 → 主 Agent 直接执行
    ├─ 提醒类 → 直接输出提醒文本
    ├─ 生成类 → 调用工具生成产物
    └─ 操作类 → 调用工具完成操作

禁止：创建/修改定时任务、追问时间频率
```

### 4.2 静默执行配置

| 配置项 | 值 |
|--------|-----|
| 中间日志 | 不输出 |
| 弹窗确认 | 禁止（除非高危操作） |
| 完成通知 | 简洁摘要表格 |
| 运行模式 | 后台静默 |

---

## 五、异常处理

| 异常 | 处理策略 |
|------|---------|
| Sub Agent 超时 | 主 Agent 降级执行或告知用户 |
| Sub Agent 结果不完整 | 寻找其他 Agent 补缺口 |
| 路由错误 | 重新派发给正确 Agent |
| 权限不足 | 告知用户，提供替代方案 |
| 依赖缺失 | 自动安装依赖后重试 |

---

> **参考来源**：Anthropic Academy - Introduction to Subagents, Introduction to Agent Skills, Claude Code in Action, MCP Introduction & Advanced