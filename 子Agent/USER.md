---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_1a824c2861fb11f18f065254007bceed
    ReservedCode1: NpCpnwuwWwFJuD+KKSInA7gIjnOs4wW9SKQe1xCsTMXMi7EftQBbLKUVjtBrqb8L5Ra2jDLoS7hByYmS6UXAZrtRPRWmNi02/CVJPaOsfa5PdmiVbgxt6fcQWvhmLZ+RaqB9ORCEndaTxEwX2FoHTWmGDwg9rpG1aePbFxw+j7UlUcB/VMzOY9CI5tQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_1a824c2861fb11f18f065254007bceed
    ReservedCode2: NpCpnwuwWwFJuD+KKSInA7gIjnOs4wW9SKQe1xCsTMXMi7EftQBbLKUVjtBrqb8L5Ra2jDLoS7hByYmS6UXAZrtRPRWmNi02/CVJPaOsfa5PdmiVbgxt6fcQWvhmLZ+RaqB9ORCEndaTxEwX2FoHTWmGDwg9rpG1aePbFxw+j7UlUcB/VMzOY9CI5tQ=
---
# USER.md — 多Agent协作流程（龙虾AI分身用户指南）

> **版本**：v2.2(R80迭代) | **创建日期**：2026-06-01 | **更新日期**：2026-06-10
> **来源**：Anthropic Agent Teams + Harness Patterns + Managed Agents Platform + Code with Claude 2026 + 微信AI生态指引 + RED Skill公告 + B站AI创造公开赛规则 + 龙虾全域模板融合
> **生效范围**：所有子Agent协作任务
> **依赖文件**：SOUL.md / AGENTS.md / 角色总说明书.md

---

## 一、多Agent协作总览

龙虾AI体系支持三种协作模式，按复杂度和场景自动选择：

| 模式 | 适用场景 | 通信方式 | Agent数 | 示例 |
|------|---------|---------|--------|------|
| 单Agent闭环 | 单一领域任务 | 无跨Agent通信 | 1个 | 文件整理、系统设置、App操作 |
| 串行协作 | 多阶段依赖任务 | 结果传递 | 2-3个 | 搜索信息→写入文件→通知 |
| 并行协作 | 独立子任务 | 各自执行后汇总 | 2-5个 | 多维度分析、多文件处理 |

---

## 二、协作流程 — 标准五步法

### Step 1: 意图识别
- 分析用户需求的核心目标和约束条件
- 判断任务属于哪个领域（文件/系统/App/搜索/浏览器）
- 拆解为可独立执行的子目标

### Step 2: 能力映射
按逐级降级原则匹配执行者：
```
Sub Agents → Skills → Tools → 生成代码执行
```

**Agent路由规则**：

| 领域 | Agent | 关键词 |
|------|-------|--------|
| 文件 | file-agent | 文件、文档、PDF、图片、搜索、整理、转换 |
| 系统 | computer-agent | 系统设置、窗口、进程、桌面、注册表 |
| 应用 | app-agent | App、APK、小程序、Steam、安装、打开 |
| 搜索 | search-agent | 深度调研、对比分析、论文检索 |
| 浏览器 | browser | 登录、表单、多页交互 |

### Step 3: 方案规划
- 单Agent闭环：一次dispatch_task完成
- 串行协作：按阶段顺序派发，前一步完成后再派下一步
- 并行协作：无依赖的子任务同时派发

### Step 4: 自主执行
- 子Agent内部自主规划执行步骤
- 主Agent不干预子Agent内部流程
- 每次dispatch_task完成后验收结果

### Step 5: 反思进化
- 验目标：核对执行结果是否符合预期
- 验产物：确认文件/文档是否真实生成
- 补缺口：不完整时寻找其他Agent补全
- 沉淀经验：归档至知识库

---

## 三、三种协作模式详解

### 3.1 单Agent闭环模式

**流程**：
```
用户需求 → 匹配领域Agent → dispatch_task一次派发 → 验收结果 → 呈现
```

**使用场景**：
- 文件操作（搜索、读取、写入、整理、转换）
- 系统设置（配置、优化、排查）
- App操作（安装、打开、操作）
- 深度搜索调研

**任务派发规范**：
```
<overall_goal>用户原始完整需求</overall_goal>
<current_task>本次具体任务（所有实质性内容写在这里）</current_task>
```

**禁止行为**：不要指导子Agent具体步骤，描述最终目标即可。

### 3.2 串行协作模式

**流程**：
```
Step 1: Agent A 执行 → 验收结果A
Step 2: Agent B 基于结果A执行 → 验收结果B
Step 3: Agent C 基于结果B执行 → 验收结果C → 汇总呈现
```

**使用场景**：
- 信息搜集→文档生成（search-agent→file-agent）
- App启动→系统调整（app-agent→computer-agent）
- 网页操作→数据处理→写入文件（browser→python_executor→file-agent）

**memory_ids传递**：
- 上游Agent结果通过memory_ids传递给下游Agent
- 不在task中重复已通过memory_ids传递的内容

### 3.3 并行协作模式

**流程**：
```
用户需求 → 拆解为3-5个独立子任务
       → 同时派发各Agent
       → 汇总结果 → 统一呈现
```

### 3.4 Goal模式Task接力（v2.0 新增）

**流程**：
```
长任务 → 状态锁初始化 → 子Task 1执行 → 检查点保存
                                           ↓
                                    子Task 2执行 → 检查点保存
                                           ↓
                                    [如中断] → 序列化状态 → 恢复后从断点继续
                                           ↓
                                    子Task N执行 → IO验证 → 状态锁释放
```

**适用场景**：
- 六步蒸馏全流程（预估>30min）
- 全域文件转换（>100文件）
- 跨Agent长链路协作（搜索→分析→报告→同步→归档）

**使用场景**：
- 多维度搜索（同时搜索不同关键词/来源）
- 多文件处理（同时处理不同文件）
- 多平台查询（同时查不同数据源）

**使用场景**：
- 多维度搜索（同时搜索不同关键词/来源）
- 多文件处理（同时处理不同文件）
- 多平台查询（同时查不同数据源）

**并行条件**：
- 无数据依赖
- 无状态依赖
- 无安全依赖
- 单次最多5个并行

---

## 四、跨Agent通信协议

### 4.1 双向桥接协议（龙虾标准）

```json
{
  "source": "lobster_master",
  "target": "doubao_agent|hermes_agent|openclaw_agent",
  "action": "deploy|query|evolve|sync",
  "payload": {},
  "timestamp": "",
  "trace_id": ""
}
```

### 4.2 Agent间信息传递

| 传递方式 | 适用场景 | 工具 |
|---------|---------|------|
| memory_ids | 将上游Agent结果作为背景信息注入下游Agent | dispatch_task参数 |
| inherit_agent_id | 同一Agent的连续会话（延续任务） | dispatch_task参数 |
| 文件传递 | 通过磁盘文件传递中间/最终产物 | 中间产物目录(temp) |
| MCP协议 | Agent与外部系统通信 | MCP Server |

### 4.3 延续任务判断

当用户使用以下语言时，很可能是延续任务，需填写 `inherit_agent_id`：
- "不对" / "别..." / "不是这样"
- "恢复" / "撤销" / "改回"
- "再..." / "继续..." / "还有..."

---

## 五、协作安全机制

### 5.1 任务验收三问
每次dispatch_task完成后，必须回答：
1. 执行目标是否完全达成？
2. 是否有真实产物（文件/设置变更）？
3. 是否有未完成部分需要其他Agent补全？

### 5.2 降级兜底
- 同一工具/技能针对同一子目标失败上限2次
- 超出后必须降级到上一层能力或交还用户
- 严禁仅通过参数微调绕过上限

### 5.3 工具调用安全
- 🔴 高风险操作：必须确认
- 🟡 中风险操作：二次确认
- 🟢 低风险操作：直接执行
- 工具调用即警戒：涉及系统状态变更时必须评估风险

---

## 六、协作最佳实践

### 6.1 任务描述
- task中使用结果导向：描述目标而非步骤
- memory_ids传递背景信息，不在task中重复
- attachments块必须原样透传

### 6.2 结果验证
- Sub Agent返回特殊卡片时，用present_result原子转发
- 不手写/复制/改写Sub Agent的特殊卡片
- 多个Agent结果需汇总时，不调用present_result

### 6.3 上下文管理
- 子Agent通过memory_ids获取必要背景
- 大段文件内容优先通过memory_ids传递
- 避免在task中重复已传递的内容

### 6.4 失败处理
- 分析失败原因，明确失败节点
- 切换参数/路径/能力层级或交还用户
- 严禁重复完全相同的调用

---

## 七、全分身同步流程

### 7.1 同步触发条件
- 新技能协议生成
- Agent能力升级
- SOUL.md / USER.md / AGENTS.md 更新
- 全域模板迭代

### 7.2 同步目标
| 分身 | 同步内容 | 同步方式 | R26新增 |
|------|---------|---------|---------|
| 豆包Agent | 技能/工作流/记忆/设计原则/Goal模式配置 | 写入对应配置目录 | Goal模式状态锁 |
| Hermes Agent | 调度策略/协作流程/进程管理/心跳检测 | 更新调度配置 | 五层防烂尾对齐 |
| OpenClaw龙虾Agent | 插件/协议/底层能力/IO验证钩子 | 更新插件配置 | 执行可验证性协议 |

### 7.3 同步验证
- 同步后执行巡检（健康巡检技能）
- 检查所有子Agent运行状态
- 异常记录纳入下一轮优化

---

## 八、任务执行检查清单

```
□ Step 1: 意图识别完成？拆解是否合理？
□ Step 2: Agent/工具匹配正确？是否越级？
□ Step 3: 协作模式选择正确？串行/并行/单Agent/Goal模式？
□ Step 4: dispatch_task参数填写完整？task/agent_name/memory_ids/inherit_agent_id？
□ Step 5: 执行结果验收完成？目标/产物/缺口？
□ Goal模式检查（耗时>10min或20+文件操作时启用）：
  □ 心跳信号是否正常（15s间隔）？
  □ 中断状态是否已序列化？
  □ 断点续跑路径是否确认？
□ 最终回复：是否需要present_result？是否有yyb-product？
□ 是否有新技能/经验需要沉淀归档？
```

---

## 十、Managed Agents 编排工作流（v1.1 新增）

### 9.1 Multiagent Orchestration 工作流

**适用场景**：任务可分解为多个独立子任务，需要并行处理以提高效率。

**流程**：
```
用户需求
  ↓
Lead Agent (Opus) 分解任务
  ↓
┌──────────┬──────────┬──────────┬──────────┐
│ Subagent │ Subagent │ Subagent │ Subagent │  ← 并行执行（最多20种 × 25线程）
│    A     │    B     │    C     │    D     │
└──────────┴──────────┴──────────┴──────────┘
  ↓           ↓           ↓           ↓
Lead Agent 接收结果、中途可发跟进消息
  ↓
合成最终结果 → 呈现给用户
```

**典型工作流模式**：

| 模式 | 场景 | 子代理分工 |
|------|------|-----------|
| 研究-评估-生成 | 销售线索处理 | 研究子代理(并行拉取)→资格评估子代理→草拟子代理 |
| 多维度分析 | 事件根因分析 | 部署历史/错误日志/性能指标/客服工单 四路并行 |
| 数据聚合 | 季度报告 | 财务/销售/运营/HR 四路并行拉取→Lead合成 |
| 合规多路审查 | 合同审查 | 政策对照/法规比对/历史条款 三路并行 |
| 多版草稿 | 内容创作 | 多个写作子代理并行生成→Outcomes Grader评分→返回最佳版 |

### 9.2 Outcomes 质量工作流

**流程**：
```
Agent 产出 → 独立 Grader 评分（隔离上下文）
    │
    ├── 达标 → 返回用户
    │
    └── 未达标 → Grader 指出具体问题 → Agent 迭代修正 → 重新评分
                   ↑                                           │
                   └─────────────────── 循环 ──────────────────┘
                   （最多 max_iterations 次）
```

**集成到龙虾五步法**：

| 步骤 | 原有 | Outcomes 增强 |
|------|------|-------------|
| 意图识别 | 分析需求 | 同时定义 Outcomes Rubric |
| 能力映射 | 匹配 Agent | 匹配 Agent + Grader 模型 |
| 方案规划 | 串行/并行决策 | 加入 Outcomes 迭代预算 |
| 自主执行 | Agent 自主执行 | Agent 执行 → Grader 评估 → 迭代修正 |
| 反思进化 | 验收结果 | Rubric 评分 + Dreaming 模式沉淀 |

### 9.3 Webhooks 异步集成工作流

```
龙虾AI体系
  │
  ├── 触发 Managed Agent 任务
  │
  ├── 设置 webhook_url（CI/CD / 通知 / 下一步触发）
  │
  ├── Agent 异步执行（用户无需等待）
  │
  ├── Agent 完成后 POST 结果到 webhook_url
  │
  └── 下游系统自动处理结果
```

### 9.4 Agent View 并行管理工作流

```
Agent View Dashboard
├── 会话1：Code Review Agent ──── 运行中
├── 会话2：Test Runner Agent ──── 等待输入
├── 会话3：Docs Writer Agent ──── 已完成
├── 会话4：Security Audit Agent ── 运行中
└── 会话5：空闲（可启动新任务）
```

**快捷键**：
- `←` 打开 Agent View
- `Space` 查看选中会话详情（Peek Panel）
- `/bg` 后台化当前任务并返回 Agent View
- `→` 进入选中会话

---

## 十一、Managed Agents 协作最佳实践（v1.1 新增）

### 10.1 何时升级到 Managed Agents

| 当前状态 | 升级建议 |
|---------|---------|
| 单个 Agent 反复遇到相同失败 | → Managed Agents + Dreaming |
| 任务质量不稳定，手动迭代 Prompts | → Managed Agents + Outcomes |
| 串行 Agent 链耗时过长 | → Multiagent Orchestration 并行化 |
| 需要在 CI/CD 中集成 Agent | → Webhooks 回调 |
| 同时管理多个 Agent 实例 | → Agent View |

### 10.2 子代理设计清单

```
□ 每个子代理职责单一吗？（一个子代理做好一件事）
□ 子代理之间无数据依赖吗？（有依赖则不适合并行）
□ 子代理获得最小工具集吗？（权限最小化）
□ 子代理工作独立可验证吗？（可独立评分）
□ 总子代理数 ≤ 20 种类型吗？
□ Lead Agent 有能力合成所有结果吗？
```

### 10.3 Outcomes Rubric 撰写指南

**好 Rubric 的特征**：
- 可测量（"识别所有安全漏洞"而非"做好安全审查"）
- 有边界（"不超过 500 字"）
- 有优先级（"安全漏洞必须标注，代码风格只是建议"）
- 有具体的失败标准（"不标注安全漏洞 = 不通过"）

**坏 Rubric 的例子**：
- "写出好的代码"（太模糊）
- "做得更好一点"（无法测量）
- "全面检查"（没有边界）

### 10.4 影子Agent复盘安全协议（R33新增）

多Agent协作中的所有复盘操作必须遵循影子Agent六层隔离：

| 层级 | 控制项 | 策略 |
|------|--------|------|
| 权限隔离 | 影子Agent最小只读权限 | 禁止写文件/系统命令/网络访问 |
| 数据隔离 | 仅注入摘要，非原始数据 | 独立上下文，不污染主Agent缓存 |
| 网络隔离 | 全部阻断外网 | 仅本地回环 |
| 文件隔离 | 仅读写技能库 | 禁止系统路径 |
| 进程隔离 | fork独立子进程 | 120秒超时→强制终止 |
| 审计隔离 | 独立日志文件 | 90天滚动归档 |

**脏计数触发**：工具迭代≥8次/会话自动触发复盘。Agent主动操作技能时重置。

---

### 10.5 R56全域蒸馏协作更新（R56新增）

**微信AI Agent生态接入协作**：
- 豆包Agent新增"微信AI Agent生态监控"技能，每轮蒸馏自动拉取最新进展
- Hermes Agent新增"Skill标准化对齐"模块，确保mcp.json + SKILL.md格式与微信AI生态兼容
- OpenClaw龙虾Agent新增"RED Skill + B站BuildinPublic双平台监测"技能

**跨Agent通信协议升级**：
- memory_ids传递内容新增"平台Agent生态情报"类别
- 微信AI Agent相关情报必须通过官方公告/财报/主流媒体三重验证
- Skill分发情报（RED Skill周榜 / B站AI创造公开赛入围）纳入全域学习报告

**任务执行检查清单更新**：
- Goal模式检查项新增："微信AI Agent生态情报是否已验证？"
- 失败处理新增："涉及微信AI Agent生态的情报失败，必须切换信源重试"

---

> **版本**：v2.1_R56（R33+R56更新）
> **知识来源**：Anthropic Agent Teams + Harness + Managed Agents + 微信AI生态指引 + RED Skill公告 + B站AI创造公开赛规则 + 龙虾全域模板v3.26
> **关联文件**：[SOUL.md](E:\龙虾AI主控中心\我的AI分身\SOUL.md) | [AGENTS.md](E:\龙虾AI主控中心\我的AI分身\AGENTS.md) | [全域学习报告_20260610.md](E:\龙虾AI主控中心\我的AI分身\知识库\全域学习报告_20260610.md)


---

## 鍗佷簩銆佸Agent鍗忎綔娴佺▼锛?026-06-11澧為噺鏇存柊锛?
### 12.1 鍗旳gent闂幆 vs 澶欰gent鍗忎綔鐨勫喅绛栨祦绋?
鍐崇瓥鏍戯紙鑷笂鑰屼笅鍒ゆ柇锛屽懡涓嵆姝級锛?
```
鐢ㄦ埛浠诲姟
  鈫?鏄惁涓哄崟涓€棰嗗煙銆佹棤骞惰闇€姹傦紵
  鈹溾攢 鏄?鈫?鍗旳gent闂幆锛堝父瑙勪細璇濓級
  鈫?鍚?鏄惁鏈?+鐙珛瀛愪换鍔′笖浜掍笉渚濊禆锛?  鈹溾攢 鏄?鈫?澶氫釜Subagents骞惰澶勭悊
  鈫?鍚?鏄惁闇€瑕佹垚鍛橀棿閫氫俊涓庤嚜鍗忚皟锛?  鈹溾攢 鍚?鈫?Subagents锛堜富Agent缂栨帓锛?  鈫?鏄?鏄惁娑夊強澶у瀷浠ｇ爜搴?澶氭ā鍧?璺ㄥ眰锛?  鈹溾攢 鍚?鈫?Subagents锛堜覆琛?绠€鍗曞苟琛岋級
  鈫?鏄?棰勭畻鍏佽杈冮珮Token娑堣€楋紵
  鈹溾攢 鍚?鈫?Subagents锛堥檷绾ф柟妗堬級
  鈫?鏄?  鈹斺攢 Agent Teams锛堟垚鍛樼洿鎺ラ€氫俊銆佽嚜鍗忚皟銆佷氦鍙夐獙璇侊級
```

蹇€熷垽鏂彛璇€锛?- 銆屽幓鏌ヤ竴涓媂銆嶁啋 Subagent
- 銆屼綘浠竴璧峰垎鏋愶紝瀵逛簡浜掔浉楠岃瘉銆嶁啋 Agent Teams
- 銆屽府鎴戞敼涓€涓嬭繖涓€嶁啋 鍗曚細璇?
### 12.2 Agent Teams 鍚敤涓庨厤缃寚鍗?
**鍓嶆彁鏉′欢**锛?- Claude Code v2.1.32+
- Opus 4.6妯″瀷璁块棶鏉冮檺

**鍚敤鏂瑰紡**锛?
鏂瑰紡涓€锛歴ettings.json锛堟帹鑽愰」鐩骇鍒級
```json
// .claude/settings.json 鎴?~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "model": "sonnet"
}
```

鏂瑰紡浜岋細鐜鍙橀噺
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**瀹炶返閰嶇疆寤鸿**锛?
```json
// 鐢熶骇绾ф帹鑽愰厤缃?{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "model": "sonnet",
  "permissions": {
    "allow": ["Read", "Write", "Edit", "Bash(git:*)"]
  }
}
```

鍥㈤槦鎴愬憳浣跨敤Sonnet锛堥潪Opus锛夊钩琛℃垚鏈笌鑳藉姏銆傞」鐩瓹LAUDE.md鑷姩琚?鎵€鏈夐槦鍙嬪姞杞斤紝鏃犻渶鍦ㄦ瘡涓槦鍙嬬殑鎻愮ず璇嶄腑閲嶅椤圭洰涓婁笅鏂囥€?
### 12.3 Skills/Hooks/MCP/Subagents 鍥涗欢濂楀崗鍚屽伐浣滄祦

鍗忓悓鍏崇郴鍏ㄦ櫙锛?
```
          璇锋眰杩涘叆
              鈫?        CLAUDE.md锛堝叏灞€鍩虹嚎濮嬬粓鍔犺浇锛?              鈫?        Skills娓愯繘寮忓姞杞斤紙鐩稿叧鏃惰嚜鍔ㄦ縺娲伙級
              鈫?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈫?       鈫?       鈫?  Hooks   Subagents  MCP
  (浜嬩欢    (骞惰     (澶栭儴
  瑙﹀彂)   闅旂)     杩炴帴)
```

鍥涗欢濂楀悇鑷殑瑙掕壊瀹氫綅锛?
| 缁勪欢 | 瑙掕壊 | 瑙﹀彂鏃舵満 | 鍏稿瀷鐢ㄦ硶 |
|------|------|---------|---------|
| CLAUDE.md | 瀹硶 | 濮嬬粓鍔犺浇 | 浣犳槸璋?鍋氫粈涔?涓嶅仛浠€涔?|
| Skills | 椋熻氨 | 浠诲姟鐩稿叧鏃?| 鏂囦欢鏁寸悊/鍙戠エ璇嗗埆/鏂囨。鍐欎綔 |
| Hooks | 闂ㄧ | 浜嬩欢瑙﹀彂 | PreToolUse鏍￠獙/PostToolUse鏃ュ織 |
| MCP | 璁惧 | 闇€瑕佸閮ㄦ暟鎹?| 杩炴帴Notion/Linear/鏁版嵁搴?|
| Subagents | 澶栧寘 | 骞惰浠诲姟 | 澶氭枃浠跺垎鏋?鐙珛瀛愪换鍔?|
| Agent Teams | 鍥㈤槦 | 澶嶆潅骞惰 | 澶氭ā鍧楀紑鍙?绔炰簤鍋囪璋冭瘯 |

鐪熷疄宸ヤ綔娴佺ず渚嬶紙鏂囦欢鏁寸悊鍦烘櫙锛夛細

1. CLAUDE.md 瀹氫箟鍏ㄥ眬琛屼负绾︽潫
2. User: "鏁寸悊妗岄潰鏂囦欢"
3. Skills 鑷姩婵€娲?file-organizer
4. Hooks(PreToolUse) 鏍￠獙鏂囦欢璺緞瀹夊叏鎬?5. Subagents 骞惰鎵弿涓嶅悓鐩綍
6. MCP 鏃犻渶姹傦紙绾湰鍦版搷浣滐級
7. 缁撴灉姹囨€?鈫?鏁寸悊钃濆浘 鈫?鐢ㄦ埛纭 鈫?鎵ц

### 12.4 璺ˋgent閫氫俊妯″紡

榫欒櫨AI浣撶郴鏀寔鍥涚璺ˋgent閫氫俊妯″紡锛?
**妯″紡涓€锛氬叡浜换鍔″垪琛紙Agent Teams鍘熺敓锛?*
```
Team Lead 鍒涘缓浠诲姟鍒楄〃 鈫?Teammates 璁ら浠诲姟
     鈫?鐘舵€佸悓姝ワ細寰呭鐞?杩涜涓?宸插畬鎴?     鈫?鑷姩渚濊禆瑙ｉ櫎闃诲锛欰瀹屾垚鍚嶣鑷姩瑙ｉ攣
```

**妯″紡浜岋細鐩存帴娑堟伅锛圓gent Teams鍘熺敓锛?*
```
鎴愬憳A鍙戠幇渚濊禆闂 鈫?鐩存帴閫氱煡鎴愬憳B
鎴愬憳B瀹屾垚 鈫?鎴愬憳C鍩轰簬B鐨勫伐浣滅户缁?鏃犻渶鎵€鏈夐€氫俊缁忚繃Team Lead
```

**妯″紡涓夛細涓籄gent姹囨€伙紙Subagents榛樿妯″紡锛?*
```
Subagent A 鈹€鈹€鈫?缁撴灉 鈹€鈹€鈹?Subagent B 鈹€鈹€鈫?缁撴灉 鈹€鈹€鈹も啋 涓籄gent姹囨€?鈫?缁煎悎杈撳嚭
Subagent C 鈹€鈹€鈫?缁撴灉 鈹€鈹€鈹?```

**妯″紡鍥涳細memory_ids浼犻€掞紙榫欒櫨璺ㄤ細璇濓級**
```
Agent A 杈撳嚭 memory_ids 鈫?Agent B 璇诲彇璁板繂涓婁笅鏂?璺ㄤ細璇濅俊鎭紶閫掓満鍒讹紝閫傜敤浜庨暱浠诲姟娴佹按绾?```

閫氫俊妯″紡閫夋嫨鍐崇瓥锛?- 鎴愬憳闇€瑕佽嚜鍗忚皟 + 鐩存帴閫氫俊 鈫?妯″紡涓€/浜岋紙Agent Teams锛?- 浠诲姟鐙珛 + 鍙渶缁撴灉 鈫?妯″紡涓夛紙Subagents锛?- 璺ㄤ細璇?+ 闀夸换鍔℃祦姘寸嚎 鈫?妯″紡鍥涳紙memory_ids锛?
## Anthropic课程同步：多Agent协作决策框架（2026-06-14）

### 三级架构选择
| 层级 | 名称 | 通信方式 | 适用场景 |
|------|------|----------|----------|
| Level 1 | Subagents | 仅汇报 | 可重复独立任务 |
| Level 2 | Agent View | 派发/窥探 | 3-10个独立任务 |
| Level 3 | Agent Teams | 成员间通信 | 跨文件依赖任务 |

### 决策准则
- 单文件修复 → 常规会话
- 无依赖独立任务 → Agent View
- 可重复工作流 → Subagents + YAML
- 跨文件依赖开发 → Agent Teams
- 通宵批处理 → Headless + 预算上限

### 成本优化
- 主控 Opus + 成员 Sonnet（1/5成本）
- 独立预算上限：$3 × N Agent = 团队上限

---

## Anthropic官方课程R80同步：多Agent协作流程

### Dynamic Workflows 使用场景
1. **代码库级漏洞扫描**：对全仓库进行系统性安全检查
2. **大规模文件迁移**：500+文件的批量重构
3. **交叉验证研究**：从多个独立角度研究同一问题，交叉对比结论
4. **复杂规划**：在提交执行前从多个独立角度起草方案

### 从 Subagents → Agent Teams → Dynamic Workflows 的升级路径
- 单一子任务（<10分钟）→ Subagents
- 多代理协作需人工监督 → Agent Teams  
- 大规模编排需可审计可重跑 → Dynamic Workflows

### Claude Code 最佳实践（R80更新）
- /config 中启用 Dynamic Workflows
- /deep-research 运行内置研究工作流
- 使用 JS 脚本描述编排逻辑，存入项目仓库

> 同步自：Anthropic官方课程390节全集 R80 | 2026-06-14

---

## Anthropic官方课程R88同步：多Agent协作流程（2026-06-16）

### 决策框架：单会话 → 子代理 → Agent Teams

```
用户任务
    ↓
是单一领域、无并行需求？
├─ 是 → 单会话（常规对话，成本1x）
└─ 否 → 有2+独立子任务且互不依赖？
    ├─ 是 → 多个Subagents并行处理（成本1.5-2x）
    └─ 否 → 需要成员间通信与自协调？
        ├─ 否 → Subagents（主Agent编排）
        └─ 是 → Agent Teams（队友直接通信、自协调、交叉验证，成本3-4x）
```

**快速判断口诀**：
- "去查一下X" → Subagent
- "你们一起分析，对了互相验证" → Agent Teams
- "帮我改一下这个" → 单会话

### 任务设计原则

**清晰的所有权边界**：最具影响力的实践是确保每个队友拥有一组不同的文件或目录。当两个队友同时修改同一文件时会产生合并冲突。如果某文件确实需要多个队友更改，指定一个队友为所有者，其他人通过消息传达需求。

**适中的任务粒度**：单个Agent需要10-30分钟专注工作的任务是黄金大小。太大→一个队友成为瓶颈；太小→过度协调开销。

**依赖关系强制排序**：任务列表支持 `blockedBy` 关系。当依赖任务完成时，阻塞任务自动解除，下一个可用队友自认领。这比Team Lead逐一分配更高效。

### 成本控制

| 模式 | Token成本 | 适用场景 |
|------|----------|---------|
| 单会话 | 1x（基准） | 快速修复、同文件编辑 |
| 子代理 | 1.5-2x | 独立并行任务 |
| Agent Teams | 3-4x | 需要协调的跨领域变更 |

**ROI视角**：
- 小型项目（2队友/30分钟）：约$3.75 vs 单会话$1.50（2.5x），但并行调查将实际时间缩短近一半
- 中型项目（3队友/1小时）：约$10.25 vs 单会话$3.50（3x），串行2-3小时的工作在1小时内完成
- 时薪$100的开发者通过Agent Teams节省2小时 → 节省$200，Token成本仅$10-25

**成本优化策略**：
- 仅在任务确实需要并行协调时使用Agent Teams
- 独立并行任务优先用子代理（1.5-2x而非3-4x）
- 主控Opus + 成员Sonnet（1/5成本）
- 利用Prompt Caching降低缓存输入成本至$0.50/MTok

### 渐进扩展模式

> **从2-3个队友开始，仅在需要时扩展。**

Anthropic C编译器项目使用了16个Agent，但那是为期两周、$2万token成本、10万行代码的极端案例。对于大多数开发任务：

| 团队规模 | 适用场景 | Token效率 |
|---------|---------|-----------|
| 1人（单会话+Subagents） | 日常开发 | 最高 |
| 2-3人Agent Team | 模块化开发 | 中等 |
| 5-8人Agent Team | 大型重构 | 较低 |
| 16人Agent Team | 编译器级项目 | 最低 |

**每增加一个队友都会增加Token成本和通信表面积。先建Skills，再建Agent。**

> 同步自：Anthropic官方课程390节全集 R88 | 2026-06-16
