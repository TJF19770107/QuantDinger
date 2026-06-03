# Hermes × Codex 联动能力归档文档

> **版本**：v3.14_R20 | **归档日期**：2026-06-01
> **模板基线**：龙虾全域官方模板-最终版.md v3.14
> **SHA256**：4147EBA891813A3790EA5BA127333E52FE3241361000FDDB4B0F0D139EC990AD
> **生效范围**：Hermes ↔ Codex 全量交互

---

## 一、架构总览：Soul-Worker 双层架构

```
┌─────────────────────────────────────────────────┐
│                龙虾AI主控中心 (Soul)              │
│  五步法引擎 | 自进化闭环 | 记忆系统 | 安全护栏    │
└────────────┬────────────────────────────────────┘
             │ 双向桥接协议 (Bridge Protocol)
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

| 职责域 | 核心能力 | 成熟度 |
|--------|---------|--------|
| 多Agent协调 | Swarm拓扑调度、DAG分解、模型分层 | 96 |
| 任务编排 | 百级并行子Agent、双轮Review、断点续传 | 98 |
| 自进化引擎 | GEPA闭环、SkillForge、记忆策展 | 99 |
| 意图识别 | 用户需求拆解、能力模块匹配 | 97 |
| 反思进化 | Rubric自评分、经验沉淀、基因更新 | 98 |

### 1.2 Codex 职责（Worker 层编码执行体）

| 职责域 | 核心能力 | 成熟度 |
|--------|---------|--------|
| 编码执行 | Python/Shell/PS1 代码生成与执行 | 97 |
| AI IDE | 代码生成/调试/重构/测试/部署五模块 | 98 |
| 任务编排 | 脚本化编排、多步骤流程 | 90 |
| 沙箱隔离 | 文件系统级隔离、受限进程 | 94 |
| 文件操作 | 读写/转换/批量处理 | 94 |
| 自愈回滚 | 错误自动修复+重试+降级 | 95 |

### 1.3 分工边界

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
```

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

### 2.2 桥接消息格式

```json
{
  "source": "hermes_orchestrator",
  "target": "codex_worker",
  "action": "deploy|query|evolve|sync",
  "payload": {
    "task_id": "R20_task_001",
    "task_type": "code_generation|file_operation|format_conversion|script_execution",
    "content": {},
    "constraints": {},
    "output_format": "json|markdown|file"
  },
  "timestamp": "2026-06-01T12:00:00+08:00",
  "trace_id": "trace_R20_20260601_120000_001"
}
```

### 2.3 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `source` | string | 发起方标识，固定 `hermes_orchestrator` |
| `target` | string | 接收方标识，固定 `codex_worker` |
| `action` | enum | 操作类型：`deploy`/`query`/`evolve`/`sync` |
| `payload.task_id` | string | 任务唯一标识 |
| `payload.task_type` | enum | 任务类型 |
| `payload.content` | object | 任务具体内容 |
| `payload.constraints` | object | 执行约束（路径/安全/超时等） |
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
    "task_id": "R20_task_001",
    "status": "success|partial|failed",
    "data": {},
    "files_created": [],
    "errors": [],
    "retry_count": 0,
    "execution_time_ms": 1234,
    "self_heal_log": []
  },
  "timestamp": "2026-06-01T12:00:10+08:00",
  "trace_id": "trace_R20_20260601_120000_001"
}
```

---

## 三、标准调用指令集

### 3.1 按 action 分类

#### 3.1.1 `deploy` — 任务部署

**用途**：Hermes 向 Codex 派发编码/文件操作任务。

```json
{
  "action": "deploy",
  "payload": {
    "task_id": "R20_deploy_001",
    "task_type": "code_generation",
    "content": {
      "overall_goal": "生成批量文件转换脚本",
      "current_task": "将 D:\\docs\\ 下所有 .docx 转为 PDF",
      "requirements": ["递归扫描", "跳过已有PDF", "输出转换报告"],
      "target_path": "D:\\docs\\"
    },
    "constraints": {
      "max_retry": 2,
      "timeout_seconds": 300,
      "output_dir": "E:\\龙虾AI主控中心\\我的AI分身\\output\\"
    },
    "output_format": "json"
  }
}
```

#### 3.1.2 `query` — 状态查询

**用途**：Hermes 查询 Codex 当前运行状态或任务进度。

```json
{
  "action": "query",
  "payload": {
    "task_id": "R20_deploy_001",
    "query_type": "status|progress|result"
  }
}
```

#### 3.1.3 `evolve` — 自进化触发

**用途**：Hermes 触发 Codex 执行自进化流程（经验沉淀、技能更新）。

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

**用途**：Hermes 指令 Codex 同步最新配置/技能/规则。

```json
{
  "action": "sync",
  "payload": {
    "sync_type": "skill_library|config|knowledge_base",
    "target_paths": [],
    "force_overwrite": false
  }
}
```

### 3.2 按 task_type 分类

| task_type | 说明 | 典型 action |
|-----------|------|------------|
| `code_generation` | 代码生成与执行 | deploy |
| `file_operation` | 文件读写/复制/移动 | deploy |
| `format_conversion` | 文件格式转换 | deploy |
| `script_execution` | 已有脚本执行 | deploy |
| `data_processing` | 数据分析处理 | deploy |
| `status_query` | 状态查询 | query |
| `skill_update` | 技能更新 | evolve |
| `config_sync` | 配置同步 | sync |

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
        ├── 加载技能库（AGENTS.md + 技能协议）
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
  └── 置信度评分（多Agent交叉验证）
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

---

## 五、结果汇总输出范式

### 5.1 成功结果

```json
{
  "status": "success",
  "task_id": "R20_deploy_001",
  "summary": "已将 15 个 .docx 文件转换为 PDF",
  "files_created": [
    "D:\\docs\\报告.pdf",
    "D:\\docs\\合同.pdf"
  ],
  "statistics": {
    "total": 15,
    "converted": 15,
    "skipped": 0,
    "failed": 0
  },
  "execution_time_ms": 45230,
  "retry_count": 0,
  "self_heal_events": []
}
```

### 5.2 部分成功结果

```json
{
  "status": "partial",
  "task_id": "R20_deploy_002",
  "summary": "15 个文件中成功转换 13 个，2 个失败",
  "files_created": ["..."],
  "statistics": {
    "total": 15,
    "converted": 13,
    "skipped": 0,
    "failed": 2
  },
  "errors": [
    {
      "file": "D:\\docs\\加密文件.docx",
      "error_type": "PermissionError",
      "error_message": "文件受密码保护无法读取",
      "fallback": "已跳过"
    }
  ],
  "execution_time_ms": 52100,
  "retry_count": 2
}
```

### 5.3 失败结果

```json
{
  "status": "failed",
  "task_id": "R20_deploy_003",
  "summary": "任务执行失败",
  "error_type": "DependencyMissing",
  "error_message": "lark-cli 未安装且安装失败",
  "retry_count": 2,
  "fallback_applied": "生成飞书CLI命令文本，需用户手动执行",
  "files_created": [],
  "execution_time_ms": 8900
}
```

---

## 六、自动化协作链路打通方案

### 6.1 定时触发链路

```
定时任务 (每2小时)
    │
    ▼
AutoWake v2.0 心跳唤醒
    │
    ▼
Hermes 五步法引擎启动
    │
    ├── Step 1: 扫描待处理队列
    ├── Step 2: 匹配 Codex 能力
    ├── Step 3: 封装 bridge_message
    │
    ▼
Codex Worker 接收 dispatch_task
    │
    ├── 加载 AGENTS.md + 技能库
    ├── 执行任务
    ├── 自愈循环
    └── 返回结构化结果
    │
    ▼
Hermes 结果校验 + 反思进化
    │
    ├── 写入迭代日志
    ├── 更新知识库
    ├── 同步至全部分身
    └── 记忆沉淀
```

### 6.2 事件驱动链路

```
事件触发 (文件变化/Git push/用户指令)
    │
    ▼
事件驱动自动化流水线 (协议13)
    │
    ▼
Hermes 识别事件类型
    │
    ├── 文件变化 → Codex 文件处理
    ├── Git push → Codex 代码审查
    ├── 用户指令 → 意图识别后路由
    └── 系统告警 → 自愈响应
```

### 6.3 链路保障机制

| 保障层 | 机制 | 协议来源 |
|--------|------|---------|
| 幂等性 | Exactly-Once 语义 | 协议27 DurableExecution |
| 断点续传 | Checkpoint 持久化 | 协议27 + 龙虾五步法 |
| 熔断保护 | 连续失败3次终止 | 协议1 多Agent协同看板 |
| 超时控制 | 单任务60秒超时 | AGENTS.md |
| 结果校验 | 多Agent置信度验收 | 协议61 |
| 审计追溯 | trace_id 全链路追踪 | 双向桥接协议 v2.1 |

---

## 七、能力矩阵参考（对标融合矩阵摘录）

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

---

## 八、安全协同机制

### 8.1 双重安全护栏

```
Hermes 安全层 (策略制定)         Codex 安全层 (执行约束)
─────────────────────────────────────────────────
三级风险定级 (🔴/🟡/🟢)    →    操作前风险校验
系统核心路径禁止             →    路径白名单检查
凭据禁造原则                 →    {{from-vault}} 标记
安全验证不绕过               →    超权限操作拒绝
信息保护最高优先级           →    敏感信息脱敏
```

### 8.2 协作安全规则

| 规则 | Hermes 职责 | Codex 职责 |
|------|-----------|-----------|
| 风险定级 | 任务分发时标记风险级别 | 执行前再次校验 |
| 路径审计 | 指定安全输出目录 | 禁止写入系统路径 |
| 凭据管理 | 从 Vault 注入 | 标记 `{{from-vault}}` |
| 操作日志 | 记录调度决策 | 记录执行详情 |
| 回滚策略 | 制定回滚方案 | 执行回滚操作 |

---

> **文档版本**：v3.14_R20
> **归档时间**：2026-06-01 12:00
> **下次审查**：R21 迭代
> **关联文档**：龙虾全域官方模板-最终版.md | AGENTS.md | 72项技能协议
