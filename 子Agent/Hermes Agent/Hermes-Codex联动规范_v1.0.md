# Hermes-Codex 联动规范 v1.0

> **版本**：v1.0 | **创建日期**：2026-06-01
> **生效范围**：全域 / 永久 / 永恒
> **关联文件**：AGENTS.md | 龙虾全域官方模板-最终版.md | Codex+飞书CLI自动化技能手册.md
> **依赖协议**：协议32（编排者-工作者结构化结果协议）/ 协议42（Swarm多Agent拓扑调度协议）/ 协议63（GEPA运行时自进化闭环协议）

---

## 一、联动架构总览

### 1.1 角色定位

| 角色 | 定位 | 核心职责 | 模型建议 |
|------|------|---------|---------|
| **Hermes** | 调度中枢 / Orchestrator | 任务分解、Agent 编排、结果汇总 | Opus（复杂决策）|
| **Codex** | 编码执行器 / Worker | 代码生成、文件操作、CLI 自动化 | Sonnet（高效执行）|
| **飞书 CLI** | 外部能力桥接 | 文档/Base/日历/消息 自动化 | — |

### 1.2 联动拓扑

```
用户请求
    ↓
Hermes (Orchestrator)
    ├── 任务理解 → 拆解子任务
    ├── 派遣 Codex Worker（编码/文件/CLI 任务）
    ├── 派遣 Search Agent（调研/检索任务）
    ├── 派遣 File Agent（文件整理/格式转换）
    └── 汇总结果 → 输出给用户
            ↑
Codex (Worker) 执行完成后返回结构化结果
```

---

## 二、Hermes 调用 Codex 完整流程

### 2.1 标准调用流程（六步法）

```
Step 1: 需求接收
    用户提出需求 → Hermes 解析意图 → 判断是否需要 Codex

Step 2: 任务拆解
    Hermes 将需求拆解为独立子任务
    每个子任务满足：自包含、结果导向、无依赖或依赖已明确

Step 3: 派遣指令生成
    Hermes 生成标准 dispatch_task 调用
    格式见第三节「标准调用指令格式」

Step 4: Codex 执行
    Codex 接收 task → 调用工具/技能执行
    执行过程中可调用飞书 CLI 完成自动化操作

Step 5: 结果返回
    Codex 返回结构化结果（JSON/Markdown/文件路径）
    格式见第四节「结果汇总输出范式」

Step 6: Hermes 汇总输出
    Hermes 收集所有 Worker 结果 → 去重/合并/格式化
    输出最终给用户
```

### 2.2 调用决策树

```
用户需求
    ├── 涉及编码/文件操作/CLI 自动化？
    │   └── 是 → 派遣 Codex Worker
    ├── 涉及网页搜索/深度调研？
    │   └── 是 → 派遣 Search Agent
    ├── 涉及文件整理/格式转换/搜索？
    │   └── 是 → 派遣 File Agent
    └── 涉及系统设置/进程管理？
        └── 是 → Hermes 自行处理或派遣 Computer Agent
```

---

## 三、标准调用指令格式

### 3.1 dispatch_task 标准模板

```python
dispatch_task(
    agent_name="codex-worker",
    task="""
<overall_goal>
{用户原始完整需求}
</overall_goal>

<current_task>
{本次委托具体任务描述（自包含、结果导向）}

【执行要求】
1. 输出格式：{指定输出格式}
2. 输出路径：{指定输出目录}
3. 依赖文件：{如有依赖文件，列出路径}
4. 飞书 CLI：{如需接入飞书，说明具体操作}
</current_task>
""",
    memory_ids=["{相关历史消息 memory_id}"],
    inherit_agent_id="{继承的 Agent ID 或留空}"
)
```

### 3.2 task 编写纪律

| 规则 | 说明 | 示例 |
|------|------|------|
| 自包含 | task 内部包含所有必要信息，不依赖外部状态 | ✅ "读取 E:\xxx\data.csv，生成分析报告" ❌ "处理那个文件" |
| 结果导向 | 描述目标状态，而非执行步骤 | ✅ "生成 Excel 报表并发送到飞书群" ❌ "先读文件，再处理，再生成" |
| 路径明确 | 所有文件路径使用绝对路径 | ✅ "E:\数据\report.xlsx" ❌ "当前目录下的文件" |
| 格式指定 | 明确指定输出格式 | ✅ "返回 Markdown 格式摘要" ❌ "返回结果" |

### 3.3 飞书 CLI 调用模板（在 Codex 中执行）

```bash
# 模板 1：生成内容并写入飞书文档
lark-cli docs create --title "{标题}" --content "$(cat output.md)"

# 模板 2：读取飞书 Base 并处理
lark-cli base record-list --app-token {TOKEN} --table-id {TABLE_ID} --filter "{条件}" | python process.py

# 模板 3：发送通知到飞书群
lark-cli im messages-send --receive-id {CHAT_ID} --content "{通知内容}"
```

---

## 四、分步执行规则

### 4.1 任务拆解原则

1. **原子性**：每个子任务尽量原子，独立完成一个明确功能
2. **无依赖优先**：无依赖的子任务优先执行
3. **并行化**：无数据依赖的子任务并行派遣
4. **失败隔离**：单个子任务失败不影响其他子任务

### 4.2 并行派遣规则

```
同轮并行上限：5 个 Agent
超出时：分批执行，每批 ≤ 5 个
依赖链：A → B → C 必须顺序执行，不得并行
```

### 4.3 超时与重试

| 场景 | 超时时间 | 重试次数 | 降级策略 |
|------|---------|---------|---------|
| 代码生成 | 300s | 2 | 返回部分结果 |
| 文件操作 | 60s | 3 | 切换 Python 实现 |
| 飞书 CLI | 30s | 2 | 提示用户手动操作 |
| 搜索任务 | 120s | 1 | 扩大搜索范围 |

### 4.4 结果校验

```python
# Codex Worker 返回结果必须包含：
{
    "status": "success" | "partial" | "failed",
    "data": { ... },          # 主要结果数据
    "files": ["path1", ...],  # 生成的文件路径列表
    "summary": "..."          # 人类可读摘要
    "error": "..."            # 如失败，错误信息
}
```

---

## 五、结果汇总输出范式

### 5.1 Hermes 汇总格式模板

```markdown
## 任务执行结果

**任务**：{用户原始需求}
**执行时间**：{开始时间} - {结束时间}
**执行状态**：✅ 全部完成 / ⚠️ 部分完成 / ❌ 失败

### 子任务执行情况

| 子任务 | 执行 Agent | 状态 | 输出 |
|--------|-----------|------|------|
| {子任务1} | Codex | ✅ | [输出文件](path) |
| {子任务2} | Search Agent | ✅ | 摘要文本 |
| {子任务3} | File Agent | ⚠️ | 部分完成 |

### 最终产出

{汇总后的最终结果，包含文件链接、关键数据、结论}

### 执行日志

- {时间戳} {Agent} {动作} {结果}
- ...
```

### 5.2 结构化结果对象（协议32）

```json
{
  "task_id": "xxx",
  "overall_status": "success|partial|failed",
  "subtasks": [
    {
      "subtask_id": "xxx-1",
      "agent": "codex-worker",
      "status": "success",
      "outputs": {"files": [...], "data": {...}},
      "summary": "..."
    }
  ],
  "final_output": {"files": [...], "summary": "..."},
  "execution_log": [...]
}
```

---

## 六、交互规范

### 6.1 Hermes ↔ Codex 通信规范

1. **指令传递**：通过 `dispatch_task` 的 `task` 参数传递，使用 XML 标签结构化
2. **进度反馈**：Codex 执行超过 30s 时，输出一句自然语言说明当前进展
3. **结果返回**：严格按第五节格式返回，不得自由发挥
4. **异常处理**：捕获异常 → 记录错误 → 返回错误状态，不得静默失败

### 6.2 飞书 CLI 集成规范

```
Codex 执行飞书 CLI 前的检查清单：
□ lark-cli --version 可执行（CLI 已安装）
□ 飞书应用已授权（App ID / App Secret 已配置）
□ 所需权限已申请（如 doc:create / base:read）
□ 网络可达（能访问飞书 API）

任一条件不满足 → 返回错误状态 → Hermes 提示用户处理
```

### 6.3 安全约束

| 操作 | 风险级别 | 确认要求 |
|------|---------|---------|
| 删除文件 | 🔴 高风险 | 必须用户确认 |
| 覆盖文件 | 🟡 中风险 | 提示影响，用户主动要求时执行 |
| 发送飞书消息 | 🟡 中风险 | 内容超过 200 字时提示用户确认 |
| 创建飞书文档 | 🟢 低风险 | 直接执行 |
| 读取文件 | 🟢 低风险 | 直接执行 |

---

## 七、典型场景 SOP

### 场景 1：AI 调研 → 飞书文档

```
Hermes:
  1. 拆解：Search Agent（调研）+ Codex（写文档）
  2. 派遣 Search Agent → 返回调研 Markdown
  3. 派遣 Codex → 接收 Markdown → 调用 lark-cli docs create
  4. 汇总：返回飞书文档链接

Codex 执行指令：
  lark-cli docs create --title "调研报告-{日期}" --content "{调研Markdown内容}"
```

### 场景 2：批量数据处理 → 飞书 Base

```
Hermes:
  1. 拆解：Codex（读文件）+ Codex（写 Base）
  2. 派遣 Codex → 读取本地 CSV/Excel
  3. 派遣 Codex → 调用 lark-cli base record-create 批量写入
  4. 汇总：返回 Base 表格链接

Codex 执行指令：
  python process.py input.csv | lark-cli base record-create --app-token {TOKEN} --table-id {TABLE_ID} --fields -
```

### 场景 3：定时任务 → 自动汇报

```
Hermes:
  1. 注册定时任务（每 2 小时）
  2. 触发时：派遣 Codex 执行数据采集
  3. Codex 完成后：调用 lark-cli im messages-send 发送汇报
  4. 静默执行，仅在失败时通知用户
```

---

## 八、故障排查

| 故障现象 | 根因 | 解决方案 |
|---------|------|---------|
| Codex 无响应 | 超时/进程崩溃 | 检查超时配置，查看 Hermes 执行日志 |
| 飞书 CLI 报错 `unauthorized` | App Secret 错误/过期 | 重新生成 App Secret，更新配置 |
| 结果格式不正确 | Codex 未按规范返回 | 在 task 中强化输出格式要求 |
| 并行任务结果缺失 | 某 Agent 静默失败 | 为每个子任务加入状态校验 |
| 飞书权限错误 | 应用未申请对应权限 | 开放平台添加权限，管理员审核 |

---

## 九、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-06-01 | 初始版本，定义 Hermes-Codex 联动完整规范 |

---

> **文件位置**：`E:\龙虾AI主控中心\我的AI分身\知识库\Hermes-Codex联动规范_v1.0.md`
> **同步状态**：待同步至 Hermes Agent / OpenClaw / 豆包Agent
> **关联协议**：协议32（编排者-工作者结构化结果协议）/ 协议42（Swarm多Agent拓扑调度协议）

