# AGENTS.md — 子代理管理与自动化配置

> 基于 Anthropic 官方课程（Agent Skills + Subagents） | 版本 v1.1 | 2026-06-14

---

## 一、子代理配置总览

### 1.1 已注册子代理

| 代理ID | 名称 | 模型 | 工具权限 | 用途 | 状态 |
|--------|------|------|---------|------|------|
| file-agent | File Agent | Sonnet | read/write/delete/edit | 文件全生命周期管理 | 活跃 |
| computer-agent | Computer Agent | Sonnet | shell/process/system | Windows系统操作 | 活跃 |
| app-agent | App Agent | Sonnet | app操控/截图/UI分析 | 应用操作与推荐 | 活跃 |
| browser | Browser Agent | Sonnet | 浏览器/网页交互 | 登录认证/多步表单 | 活跃 |
| search-agent | Search Agent | Sonnet | 多轮搜索+总结 | 深度调研 | 活跃 |

### 1.2 内置 Subagent（Claude Code 原生）

| 子代理 | 模型 | 工具权限 | 自动触发条件 |
|--------|------|---------|-------------|
| **Explore** | Haiku（快速） | 只读 | 代码搜索、文件发现、代码库探索 |
| **Plan** | 继承自主对话 | 只读 | 计划模式下的代码库研究 |
| **General-purpose** | 继承自主对话 | 全部 | 复杂研究、多步骤操作 |

---

## 二、自动化派发规则

### 2.1 派发决策树

```
用户需求
    │
    ├─ 涉及文件/文档/图片/搜索/整理 → file-agent
    │
    ├─ 涉及Windows系统设置/窗口管理/进程 → computer-agent
    │
    ├─ 涉及App/软件/小程序/Steam/APK → app-agent
    │
    ├─ 涉及网页登录/表单/多步交互 → browser
    │
    ├─ 涉及深度信息调研/论文检索 → search-agent
    │
    └─ 多领域交叉 → 多Agent协作（顺序派发）
```

### 2.2 派发参数模板

```
dispatch_task(
  agent_name="file-agent|computer-agent|app-agent|browser|search-agent",
  task="<overall_goal>用户原始需求</overall_goal>
        <current_task>本次具体任务（自包含、可独立执行）</current_task>",
  memory_ids=[相关历史消息ID列表],
  inherit_agent_id="上次同名Agent的sa-xxx（延续任务时填写）"
)
```

### 2.3 继承规则

- **continuation 检测关键词**："不对"、"别..."、"不是这样"、"恢复"、"撤销"、"改回"
- 检测到 continuation 时，填写 `inherit_agent_id` 继承上次同名 Agent 记忆
- `agent_name` 必须与 `inherit_agent_id` 对应的历史 Agent 完全一致，否则系统自动降级创建新 Agent

---

## 三、Skills 自动化配置

### 3.1 可用 Skills 清单

| Skill名称 | 触发场景 | 自动/手动 |
|-----------|---------|----------|
| anthropic-courses-sync | 定时学习Anthropic课程 | 自动（定时任务） |
| lobster-methodology | 龙虾五步法分析 | 自动（分析类任务） |
| lobster-template | 全域模板输出 | 自动（产出报告） |

### 3.2 Skill Frontmatter 配置模板

```yaml
---
name: skill-name
description: |
  当用户提到XXX/需要XXX/涉及XXX时自动触发。
  精确描述触发场景以提高匹配准确率。
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - read_text
  - write_file
  - web_search
context: fork    # 在独立子代理中运行
---
```

---

## 四、Hooks 自动化触发

### 4.1 预定义 Hooks

| Hook类型 | 触发时机 | 执行动作 |
|----------|---------|---------|
| PreToolUse | dispatch_task调用前 | 检查memory_ids是否正确提取 |
| PostToolUse | dispatch_task返回后 | 验产物、补缺口、决定下一步 |
| Notification | 任务完成 | 报告执行结果 |
| Stop | 安全风险检测 | 暂停并请求用户确认 |

### 4.2 安全防护 Hooks

- 所有 `delete` / `shell_executor` / `python_executor` 调用 → 触发三级风险定级
- 路径含 `../` 跳转 → 解析最终路径并确认
- 写入系统核心路径 → 直接拦截

---

## 五、上下文管理规则

### 5.1 Memory ID 使用规范

- 历史消息末尾带 `[memory_id: memory_xxx]` 的，若与当前任务相关 → 提取到 `memory_ids` 参数
- `memory_ids` 与 `<current_task>` 不重复传递信息
- 一次最多 20 条 memory_id

### 5.2 上下文隔离原则

- 子代理结果通过结构化摘要返回，不携带冗长的中间推理
- Explore 子代理的搜索结果不污染主对话上下文
- 每次派发使用独立上下文窗口

---

## 六、24小时自动化闭环

### 6.1 定时任务配置

| 任务 | 周期 | 动作 |
|------|------|------|
| Anthropic课程学习 | 每2小时 | 检索最新课程→更新知识库→同步配置文件→全域迭代 |

### 6.2 闭环验证清单

- [ ] 知识库文件是否更新（18门课程内容）
- [ ] SOUL.md 是否包含最新设计原则
- [ ] USER.md 是否包含最新协作流程
- [ ] AGENTS.md 是否包含最新自动化配置
- [ ] 新内容是否已同步至豆包/Hermes/OpenClaw Agent

---

## 七、故障自愈策略

| 故障 | 检测方式 | 自愈动作 |
|------|---------|---------|
| Skilljar 直连失败 | web_fetch ERR_CONNECTION_CLOSED | 切换到中文技术源（web_search + web_fetch 备选源） |
| web_search 结果为空 | total:0 | 更换关键词重试 1 次 |
| 配置文件写入失败 | 目录不存在 | 自动创建目录 |
| 子代理执行超时 | dispatch_task 无返回 | 切换更轻量模型降级重试 |

---

*由 Marvis 维护 | 2026-06-14 23:58 CST* | 基于 Anthropic Introduction to Agent Skills + Introduction to Subagents

---

## R53 同步：Managed Agents 企业部署与自动化评估（2026-06-17）

### 新增部署参数

| 参数 | 推荐值 | 说明 |
|------|:---:|------|
| KV-cache 监控 | 持续 | 缓存命中率是生产环境 #1 指标 |
| 凭据模式 | proxy_injection | Git tokens在沙盒初始化时注入 |
| 评估管道 | 自动化 | 功能+安全+性能+质量四维测试 |

### 故障自愈策略扩展

| 故障 | 检测方式 | 自愈动作 |
|------|---------|---------|
| KV-cache 命中率 < 50% | 性能监控告警 | 检查缓存配置，调整 prompt 结构 |
| Subagent 凭据泄露风险 | Hook 审计异常 | 立即隔离会话，轮换凭据 |
| 评估评分下降 > 10% | 自动化测试报告 | 自动回滚到上一个稳定版本 |

### 安全扩展

1. 凭据代理注入 — Agent 代码永不可直接访问 API Key/Token
2. Plugin subagent 的 hooks/mcpServers/permissionMode 被忽略
3. 安全规则必须用 Hooks（无条件触发）而非 Skills（依赖自主决策）

> R53同步完成 | 2026-06-17
