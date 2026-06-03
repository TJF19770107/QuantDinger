# Hermes × Codex 联动能力规范

> **版本**：v2.0_R43 | **创建日期**：2026-06-02
> **模板基线**：龙虾全域官方模板-最终版.md v3.37
> **生效范围**：Hermes ↔ Codex 全量交互 / 全域 / 永久
> **依赖协议**：协议32（编排者-工作者结构化结果协议）/ 协议42（Swarm多Agent拓扑调度协议）/ 协议63（GEPA运行时自进化闭环协议）
> **关联文档**：龙虾全域官方模板-最终版.md | AGENTS.md | Codex+飞书CLI自动化技能手册.md

---

## 一、架构总览：Soul-Worker 双层架构

```
┌─────────────────────────────────────────────────┐
│                龙虾AI主控中心 (Soul)              │
│  五步法引擎 | 自进化闭环 | 记忆系统 | 安全护栏    │
└────────────┬────────────────────────────────────┘
             │ 双向桥接协议 (Bridge Protocol v2.1)
    ┌────────┴────────┐
    ▼                 ▼
┌───────────┐   ┌───────────┐
│  Hermes   │   │   Codex   │
│(Orchestra-│◄─►│ (Worker)  │
│  tor)     │   │           │
│ 调度/编排 │   │ 编码/沙箱 │
│ 自进化    │   │ AI IDE    │
└───────────┘   └───────────┘
```

### 1.1 Hermes 职责（Soul 层调度中枢）

| 职责域 | 核心能力 | 成熟度（对标矩阵） |
|--------|---------|-------------------|
| 多Agent协调 | Swarm拓扑调度、DAG分解、模型分层 | 96 |
| 任务编排 | 百级并行子Agent、双轮Review、断点续传 | 98 |
| 自进化引擎 | GEPA闭环、SkillForge、记忆策展 | 99 |
| 意图识别 | 用户需求拆解、能力模块匹配 | 97 |
| 反思进化 | Rubric自评分、经验沉淀、基因更新 | 98 |
| 安全策略 | 三级风险定级、凭据管理、路径审计 | 78 |

### 1.2 Codex 职责（Worker 层编码执行体）

| 职责域 | 核心能力 | 成熟度（对标矩阵） |
|--------|---------|-------------------|
| 编码执行 | Python/Shell/PS1/JS 代码生成与执行 | 97 |
| AI IDE | 代码生成/调试/重构/测试/部署五模块 | 98 |
| 任务编排 | 脚本化编排、多步骤流程 | 90 |
| 沙箱隔离 | 文件系统级隔离、受限进程 | 94 |
| 文件操作 | 读写/转换/批量处理 | 94 |
| 自愈回滚 | 错误自动修复+重试+降级 | 95 |
| 工具调用 | 外部工具链集成（lark-cli/git/npm/pip） | 90 |

### 1.3 分工边界（硬约束）

```
Hermes 负责                        Codex 负责
─────────────────────────────────────────────
意图识别与拆解        ──→          接收结构化task
能力映射与调度        ──→          执行编码任务
多Agent编排与协调     ──→          单任务专注执行
结果汇总与反思        ←──          返回结构化结果
自进化决策            ←──          提供执行反馈数据
安全策略制定          ──→          遵循安全约束执行
记忆沉淀与策展        ──→          本地文件操作
模型选择与路由        ──→          按指令使用指定工具/环境
```

### 1.4 对标矩阵（Hermes × Codex 能力分布）

| 维度 | Codex | Hermes | 分工说明 |
|------|-------|--------|---------|
| 编码能力 | **97** | 60 | Codex 主责编码执行 |
| 自主规划 | 72 | **90** | Hermes 主责规划编排 |
| 工具调用 | 90 | **78** | Codex 工具链更丰富 |
| 本地执行 | 80 | **90** | Hermes 桌面控制更强 |
| 自进化 | 50 | **95** | Hermes 主导进化决策 |
| AI IDE | **98** | 50 | Codex 核心优势 |
| 多Agent | 90 | **87** | 协同互补 |
| 安全机制 | 70 | **78** | 双层安全防护 |
| 长期记忆 | 40 | **90** | Hermes 记忆策展 |
| 沙箱隔离 | 75 | 55 | Codex 沙箱更强 |
| 任务编排 | 90 | **87** | Codex 脚本编排优势 |
| 自愈回滚 | 70 | **65** | Codex 自愈更完善 |
| 桌面控制 | 40 | **60** | Hermes 桌面操控 |

---

## 二、双向桥接协议 v2.1

### 2.1 协议架构

```
Hermes (source)                     Codex (target)
     │                                    │
     │  dispatch_task / query / evolve    │
     ├───────────────────────────────────►│
     │                                    │
     │          result / ack / sync       │
     │◄───────────────────────────────────┤
     │                                    │
```

### 2.2 桥接消息格式（请求）

```json
{
  "source": "hermes_orchestrator",
  "target": "codex_worker",
  "action": "deploy|query|evolve|sync",
  "payload": {
    "task_id": "R43_task_001",
    "task_type": "code_generation|file_operation|format_conversion|script_execution|data_processing",
    "content": {},
    "constraints": {},
    "output_format": "json|markdown|file"
  },
  "timestamp": "2026-06-02T12:00:00+08:00",
  "trace_id": "trace_R43_20260602_120000_001"
}
```

### 2.3 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `source` | string | 发起方标识，固定 `hermes_orchestrator` |
| `target` | string | 接收方标识，固定 `codex_worker` |
| `action` | enum | 操作类型：`deploy`/`query`/`evolve`/`sync` |
| `payload.task_id` | string | 任务唯一标识 |
| `payload.task_type` | enum | 任务类型：`code_generation`/`file_operation`/`format_conversion`/`script_execution`/`data_processing` |
| `payload.content` | object | 任务具体内容（含 overall_goal + current_task） |
| `payload.constraints` | object | 执行约束（路径/安全/超时/重试等） |
| `payload.output_format` | string | 期望输出格式 |
| `timestamp` | ISO8601 | 消息时间戳 |
| `trace_id` | string | 全链路追踪ID |

### 2.4 返回消息格式

```json
{
  "source": "codex_worker",
  "target": "hermes_orchestrator",
  "action": "result",
  "payload": {
    "task_id": "R43_task_001",
    "status": "success|partial|failed",
    "data": {},
    "files_created": ["路径1", "路径2"],
    "errors": [],
    "statistics": {},
    "retry_count": 0,
    "execution_time_ms": 1234,
    "self_heal_log": []
  },
  "timestamp": "2026-06-02T12:00:10+08:00",
  "trace_id": "trace_R43_20260602_120000_001"
}
```

---

## 三、标准调用指令集

### 3.1 按 action 分类

#### 3.1.1 `deploy` — 任务部署（最常用）

**用途**：Hermes 向 Codex 派发编码/文件操作/自动化任务。

```json
{
  "action": "deploy",
  "payload": {
    "task_id": "R43_deploy_001",
    "task_type": "code_generation",
    "content": {
      "overall_goal": "生成批量文件转换脚本",
      "current_task": "将 D:\\docs\\ 下所有 .docx 转为 PDF\n\n【处理要求】\n1. 递归扫描子目录\n2. 跳过已有同名PDF的文件\n3. 输出转换报告\n\n【约束】\n- 超时：300s\n- 重试上限：2\n- 输出目录：E:\\output\\"
    },
    "constraints": {
      "max_retry": 2,
      "timeout_seconds": 300,
      "output_dir": "E:\\龙虾AI主控中心\\我的AI分身\\output\\",
      "risk_level": "🟢"
    },
    "output_format": "json"
  }
}
```

#### 3.1.2 `query` — 状态查询

```json
{
  "action": "query",
  "payload": {
    "task_id": "R43_deploy_001",
    "query_type": "status|progress|result"
  }
}
```

#### 3.1.3 `evolve` — 自进化触发

```json
{
  "action": "evolve",
  "payload": {
    "evolve_type": "skill_update|memory_curation|rule_refinement",
    "source_data": {},
    "target_skill": ""
  }
}
```

#### 3.1.4 `sync` — 配置同步

```json
{
  "action": "sync",
  "payload": {
    "sync_type": "skill_library|config|knowledge_base",
    "target_paths": ["E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\Hermes Agent\\", "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent\\", "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\OpenClaw\\"],
    "force_overwrite": false
  }
}
```

### 3.2 dispatch_task 标准模板（XML格式）

```xml
<overall_goal>
{用户原始完整需求}
</overall_goal>

<current_task>
{本次委托具体任务描述（自包含、结果导向）}

【处理要求】
1. {具体要求1}
2. {具体要求2}

【约束】
- 超时：{秒}
- 重试上限：{次数}
- 输出目录：{路径}
- 安全级别：{🟢/🟡/🔴}

【输出格式】{json|markdown|file|table}
</current_task>
```

### 3.3 task 编写纪律

| 规则 | 说明 | 正确示例 | 错误示例 |
|------|------|---------|---------|
| 自包含 | task 内部包含所有必要信息 | "读取 E:\data.csv，生成分析报告" | "处理那个文件" |
| 结果导向 | 描述目标状态，而非执行步骤 | "生成 Excel 报表并发送到飞书群" | "先读文件，再处理，再生成" |
| 路径明确 | 所有文件路径使用绝对路径 | "E:\数据\report.xlsx" | "当前目录下的文件" |
| 格式指定 | 明确指定输出格式 | "返回 Markdown 格式摘要" | "返回结果" |
| 无歧义 | 用词精确，不含模糊描述 | "筛选2026年6月订单" | "筛选最近的订单" |

### 3.4 按 task_type 分类速查

| task_type | 说明 | 典型工具链 | 适用场景 |
|-----------|------|-----------|---------|
| `code_generation` | 代码生成与执行 | python_executor / shell_executor | 脚本开发、自动化处理 |
| `file_operation` | 文件读写/复制/移动/删除 | read_file / write_file / delete / edit_file | 文件管理、同步分发 |
| `format_conversion` | 文件格式转换 | convert_file | PDF/Word/Excel/图片互转 |
| `script_execution` | 已有脚本执行 | python_executor / shell_executor | 预置脚本运行 |
| `data_processing` | 数据分析处理 | read_file + python_executor | CSV/Excel数据分析 |

---

## 四、分步执行规则（龙虾五步法映射）

### Step 1：意图识别 + 匹配 Codex 能力

```
用户输入 / 定时任务触发
        │
        ▼
Hermes 五步法引擎解析意图
        │
        ├── 判断是否需要编码执行 ──→ 否 ──→ 由 Hermes 直接处理
        │
        ▼ 是
匹配 Codex 能力矩阵：
  ├── 编码生成 (97) ──→ task_type: code_generation
  ├── 文件操作 (94) ──→ task_type: file_operation
  ├── 格式转换      ──→ task_type: format_conversion
  ├── 脚本执行      ──→ task_type: script_execution
  └── 数据处理      ──→ task_type: data_processing
```

### Step 2：桥接 Payload 封装

```
Step 1 确定 task_type
        │
        ▼
封装桥接消息：
  ├── 生成 trace_id（链路追踪）
  ├── 构造 content（任务内容 + 要求 + 约束）
  ├── 设定 output_format（期望输出格式）
  ├── 注入 constraints（超时/重试/路径/安全）
  └── 添加 session 上下文（SOUL/USER/AGENTS 引用）
```

### Step 3：调用 Codex 执行

```
Hermes dispatch_task(codex_worker, bridge_message)
        │
        ▼
Codex 接收 task
        │
        ├── 解析 task XML 标签
        ├── 加载 AGENTS.md + 技能库（自动扫描规则）
        ├── 执行任务（工具/脚本）
        ├── 自愈循环（失败→修复→重试）
        └── 封装结构化结果
```

### Step 4：结果校验

```
Codex 返回结构化结果
        │
        ▼
Hermes 结果校验：
  ├── 状态码检查（success/partial/failed）
  ├── 产出物完整性验证
  ├── 输出格式合规检查
  ├── 错误日志审查
  └── 置信度评分（多Agent交叉验证 — 协议61）
```

### Step 5：反思进化

```
校验通过的结果
        │
        ▼
Hermes 反思引擎：
  ├── Rubric 自评分
  ├── 提取成功模式 → 经验池
  ├── 提取失败模式 → 错误模式库
  ├── 更新能力矩阵数值
  ├── 生成迭代日志
  └── 触发记忆策展（Dreaming协议）
```

### 4.1 任务拆解原则

1. **原子性**：每个子任务尽量原子，独立完成一个明确功能
2. **无依赖优先**：无依赖的子任务优先执行
3. **并行化**：无数据依赖的子任务并行派遣（同轮上限5个）
4. **失败隔离**：单个子任务失败不影响其他子任务

### 4.2 超时与重试

| 场景 | 超时时间 | 重试次数 | 降级策略 |
|------|---------|---------|---------|
| 代码生成 | 300s | 2 | 返回部分结果 |
| 文件操作 | 60s | 3 | 切换 Python 实现 |
| 飞书 CLI | 30s | 2 | 提示用户手动操作 |
| 数据搜索 | 120s | 1 | 扩大搜索范围 |
| 格式转换 | 180s | 2 | 返回源文件路径 |

### 4.3 并行派遣规则

- 同轮并行上限：5 个 Agent
- 超出时：分批执行，每批 ≤5 个
- 依赖链（A→B→C）：必须顺序执行，不得并行

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
```

### 5.2 结构化结果对象（协议32兼容）

```json
{
  "task_id": "R43_task_001",
  "overall_status": "success|partial|failed",
  "subtasks": [
    {
      "subtask_id": "R43_task_001-1",
      "agent": "codex-worker",
      "status": "success",
      "outputs": {"files": ["E:\\output\\report.xlsx"], "data": {}},
      "summary": "已生成报表"
    }
  ],
  "final_output": {"files": ["..."], "summary": "..."},
  "execution_log": []
}
```

### 5.3 Codex 返回结果格式（必须包含字段）

```json
{
  "status": "success|partial|failed",
  "task_id": "R43_task_001",
  "summary": "人类可读摘要",
  "files_created": ["E:\\output\\file1.pdf"],
  "statistics": {
    "total": 15,
    "converted": 13,
    "skipped": 0,
    "failed": 2
  },
  "errors": [
    {
      "file": "E:\\docs\\加密文件.docx",
      "error_type": "PermissionError",
      "error_message": "文件受密码保护无法读取",
      "fallback": "已跳过"
    }
  ],
  "execution_time_ms": 45230,
  "retry_count": 0,
  "self_heal_events": []
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

### 6.3 飞书 CLI 调用模板

```bash
# 模板 1：生成内容并写入飞书文档
lark-cli docs create --title "{标题}" --content "$(cat output.md)"

# 模板 2：读取飞书 Base 并处理
lark-cli base record-list --app-token {TOKEN} --table-id {TABLE_ID} --filter "{条件}" | python process.py

# 模板 3：发送通知到飞书群
lark-cli im messages-send --receive-id {CHAT_ID} --content "{通知内容}"
```

### 6.4 安全约束

| 操作 | 风险级别 | 确认要求 |
|------|---------|---------|
| 删除文件 | 🔴 高风险 | 必须用户确认 |
| 覆盖文件 | 🟡 中风险 | 提示影响，用户主动要求时执行 |
| 发送飞书消息 | 🟡 中风险 | 内容超过200字时提示用户确认 |
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
  1. 注册定时任务（每2小时）
  2. 触发时：派遣 Codex 执行数据采集
  3. Codex 完成后：调用 lark-cli im messages-send 发送汇报
  4. 静默执行，仅在失败时通知用户
```

### 场景 4：文件同步分发

```
Hermes:
  1. 接收同步指令（源文件 + 目标目录列表）
  2. 派遣 Codex 执行文件复制分发
  3. Codex 返回同步状态表格
  4. Hermes 汇总展示
```

---

## 八、自动化协作链路

### 8.1 定时触发链路

```
定时任务 (每2小时)
    │
    ▼
AutoWake v2.0 心跳唤醒
    │
    ▼
Hermes 五步法引擎启动
    ├── Step 1: 扫描待处理队列
    ├── Step 2: 匹配 Codex 能力
    ├── Step 3: 封装 bridge_message
    │
    ▼
Codex Worker 接收 dispatch_task
    ├── 加载 AGENTS.md + 技能库
    ├── 执行任务
    ├── 自愈循环
    └── 返回结构化结果
    │
    ▼
Hermes 结果校验 + 反思进化
    ├── 写入迭代日志
    ├── 同步至全部分身
    └── 记忆沉淀
```

### 8.2 事件驱动链路

```
事件触发 (文件变化/Git push/用户指令)
    │
    ▼
事件驱动自动化流水线 (协议13)
    │
    ▼
Hermes 识别事件类型
    ├── 文件变化 → Codex 文件处理
    ├── Git push → Codex 代码审查
    ├── 用户指令 → 意图识别后路由
    └── 系统告警 → 自愈响应
```

### 8.3 链路保障机制

| 保障层 | 机制 | 协议来源 |
|--------|------|---------|
| 幂等性 | Exactly-Once 语义 | 协议27 DurableExecution |
| 断点续传 | Checkpoint 持久化 | 协议27 + 龙虾五步法 |
| 熔断保护 | 连续失败3次终止 | 协议1 多Agent协同看板 |
| 超时控制 | 单任务300s超时 | AGENTS.md |
| 结果校验 | 多Agent置信度验收 | 协议61 |
| 审计追溯 | trace_id 全链路追踪 | 双向桥接协议 v2.1 |

---

## 九、双重安全协同

### 9.1 安全分工

```
Hermes 安全层 (策略制定)         Codex 安全层 (执行约束)
─────────────────────────────────────────────────
三级风险定级 (🔴/🟡/🟢)    →    操作前风险校验
系统核心路径禁止             →    路径白名单检查
凭据禁造原则                 →    {{from-vault}} 标记
安全验证不绕过               →    超权限操作拒绝
信息保护最高优先级           →    敏感信息脱敏
```

### 9.2 协作安全规则

| 规则 | Hermes 职责 | Codex 职责 |
|------|-----------|-----------|
| 风险定级 | 任务分发时标记风险级别 | 执行前再次校验 |
| 路径审计 | 指定安全输出目录 | 禁止写入系统路径 |
| 凭据管理 | 从 Vault 注入 | 标记 `{{from-vault}}` |
| 操作日志 | 记录调度决策 | 记录执行详情 |
| 回滚策略 | 制定回滚方案 | 执行回滚操作 |

---

## 十、故障排查

| 故障现象 | 根因 | 解决方案 |
|---------|------|---------|
| Codex 无响应 | 超时/进程崩溃 | 检查超时配置，查看 Hermes 执行日志 |
| 飞书 CLI 报错 `unauthorized` | App Secret 错误/过期 | 重新生成 App Secret，更新配置 |
| 结果格式不正确 | Codex 未按规范返回 | 在 task 中强化输出格式要求 |
| 并行任务结果缺失 | 某 Agent 静默失败 | 为每个子任务加入状态校验 |
| 飞书权限错误 | 应用未申请对应权限 | 开放平台添加权限，管理员审核 |
| 编码错误 `UnicodeEncodeError` | strftime 中文格式 | 改用 f-string 拼接日期 |

---

## 十一、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-06-01 | 初始版本，定义 Hermes-Codex 联动完整规范 |
| v2.0_R43 | 2026-06-02 | R43迭代：合并归档文档 + 升级桥接协议 v2.1 + 增强五步法映射 + 补全链路保障 + 全域模板对齐 |

---

> **文件位置**：`E:\龙虾AI主控中心\我的AI分身\知识库\Hermes_Codex联动能力规范.md`
> **同步目标**：Hermes Agent / OpenClaw / 豆包Agent
> **关联协议**：32（编排者-工作者）/ 42（Swarm拓扑调度）/ 63（GEPA闭环）/ 27（DurableExecution）/ 61（置信度验收）
