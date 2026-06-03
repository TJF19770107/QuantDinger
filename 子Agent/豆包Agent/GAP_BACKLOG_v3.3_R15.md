# 豆包Agent 全域缺口积压清单 v3.3-R15

> 更新: 2026-05-31 R15
> 上一版: v3.2_R14 → 本版新增GAP-024~028（5项）
> 对标源: 14系统 + Brightlume + BayesianPersuasion

---

## 缺口全览（22项，按优先级排列）

### 🔴 P0级（5项 — 阻断级，必须立即解决）

| # | 缺口名称 | 来源 | 对标源 | 当前状态 |
|---|----------|------|--------|---------|
| GAP-007 | Plan模式缺失 | R13 | Claude Code/Codex CLI/Gemini CLI/Cursor | 📋 R13激活 → R15 AGP Planning Agent参考 |
| GAP-012 | MCP Gateway架构缺失 | R14 | Apigene + OpenClaw MCP Host v2026.3.25 | 📋 R14激活 → R15 OpenClaw MCP集成对齐 |
| GAP-015 | 自进化缺乏形式化协议 | R14 | Autogenesis AGP + HyperAgents Archive | 📋 R14激活 → R15 Archive+SEPL双保障设计 |
| **GAP-024** | **长任务调度架构缺失** | **R02/R15** | **Brightlume三层架构** | **📋 R15新激活** |
| **GAP-025** | **事件驱动触发器缺失** | **R02/R15** | **Brightlume事件+定时混合** | **📋 R15新激活** |

### 🟡 P1级（12项 — 重要但可延后）

| # | 缺口名称 | 来源 | 对标源 | 缺口描述 |
|---|----------|------|--------|----------|
| GAP-009 | 上下文工程未结构化 | R13 | Anthropic CE + Hermes四层 + OpenClaw上下文窗口管理器 | 上下文偏全量塞入，缺结构化组织+按需展开 |
| GAP-010 | 技能标准化未覆盖agentskills.io | R13 | agentskills.io (20+工具兼容) + ClawHub 5,400+ | 技能生成未遵循跨平台标准 |
| GAP-011 | 回滚缺乏原子化保障 | R13 | Autogenesis SEPL | Merkle树回滚缺提议-评估-提交形式化保障 |
| GAP-013 | A2A Agent Card未发布 | R14 | Google A2A v1.0 (150+组织) | Agent无法被外部发现和协作 |
| GAP-014 | Firecracker沙箱未集成 | R14 | E2B/Firecracker/Google Sandbox | 代码执行仅容器隔离 |
| GAP-016 | 并行执行引擎偏弱(D07=3) | R14 | Marvis原生并行 + OpenClaw maxConcurrent 8 | 多Agent并行调度效率待提升 |
| GAP-018 | 经验库自蒸馏未实现 | R14 | EvolveR (ICML 2026) | 记忆系统缺策略原则自动提炼 |
| GAP-019 | 多Provider路由缺失 | R14 | OpenClaw delegateTo (30+ Provider) | 不同任务无法自动路由到最优Provider |
| GAP-020 | 进程内MCP未实现 | R14 | Claude Agent SDK | 自定义工具需独立进程，有IPC开销 |
| GAP-022 | A2A OAuth 2.0认证缺失 | R14 | A2A认证规范 | 缺乏跨组织Agent协作的标准认证机制 |
| **GAP-026** | **幂等工具调用未实现** | **R02/R15** | **Brightlume Layer 2 + Stripe/AWS** | **📋 R15新激活 — 缺乏关键操作去重保障** |
| **GAP-027** | **熔断器模式未实现** | **R02/R15** | **Circuit Breaker Pattern** | **📋 R15新激活 — 连续失败无自动熔断** |

### 🟢 P2级（5项 — 前瞻规划）

| # | 缺口名称 | 来源 | 对标源 | 缺口描述 |
|---|----------|------|--------|----------|
| GAP-008 | 事件驱动触发缺失 | R13 | Codex CLI Triggers | 无GitHub/webhook/文件变更事件自动触发 |
| GAP-017 | 端云双模缺失 | R14 | Marvis效率/隐私双模 | 缺云端推理+本地执行混合模式 |
| GAP-021 | 能力市场接口未规划 | R14 | Workfoz/ClawHub | 豆包Agent技能无法对外发布和交易 |
| GAP-023 | GPU沙箱预留接口缺失 | R14 | Modal | AI推理/训练场景需要GPU沙箱 |
| **GAP-028** | **死信队列未建立** | **R02/R15** | **Brightlume DLQ+Replay** | **📋 R15新激活 — 失败任务无归档追溯** |

---

## 缺口来源演进

| 版本 | 新增缺口 | 总数 | 重点变化 |
|------|---------|------|----------|
| R13 | GAP-007~011 (5项) | 11 | Plan模式+上下文+标准+回滚 |
| R14 | GAP-012~023 (12项) | 17→合并 | MCP Gateway+自进化协议+沙箱+A2A+并行+Provider |
| R15 | GAP-024~028 (5项) | 22 | 长任务调度+事件驱动+幂等+熔断+死信队列 |

---

## R15→R16 优先补缺路线图

```
R16（预计2026-06-01 03:00）
├─ 🔴 GAP-024: 长任务调度架构方案（检查点+熔断+死信队列）
│   ├─ 检查点状态管理设计（执行状态/工具结果/Agent记忆/时间戳）
│   ├─ 指数退避熔断器设计（1s/2s/4s/8s/16s, 3次→Open, 30s冷却）
│   └─ 死信队列归档方案（checkpoints/dead_letter/）
├─ 🔴 GAP-012: MCP Gateway架构方案初稿
│   ├─ OpenClaw MCP Host v2026.3.25 实践对齐
│   └─ 认证/路由/压缩/观测四层设计
├─ 🔴 GAP-015: 自进化协议正式化
│   ├─ HyperAgents Archive种群多样性机制
│   └─ Staged Eval分阶段评估门禁
├─ 🟡 GAP-026: 幂等工具调用设计（UUID幂等键+状态验证）
├─ 🟡 GAP-027: 熔断器原型（Closed→Open→Half-Open）
└─ 🟡 GAP-025: Watchdog文件监听+Webhook触发器接口设计

R17（预计2026-06-01 06:00）
├─ 🟡 GAP-028: 死信队列建立（归档+修复机制+手动重放）
├─ 🟡 GAP-018: EvolveR经验库自蒸馏设计
├─ 🟡 GAP-011: SEPL原子回滚融入现有回滚体系
└─ 🟡 GAP-009: 上下文工程结构化方案（五层记忆对齐OpenClaw）
```

---

## 关键指标

| 指标 | R14 | R15 | 新增 |
|------|-----|-----|------|
| 总缺口 | 17 | 22 | +5（长调度/事件驱动/幂等/熔断/死信） |
| 🔴 P0 | 3 | 5 | +2（长调度/事件驱动） |
| 🟡 P1 | 10 | 12 | +2（幂等/熔断器） |
| 🟢 P2 | 4 | 5 | +1（死信队列） |
| 能力数 | 42 | 47 | +5 |
| 对标系统 | 14 | 14 | Brightlume/BayesianPersuasion深度情报注入 |

---

> **缺口清单版本**: v3.3-R15
> **更新日期**: 2026-05-31
> **归档路径**: E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\GAP_BACKLOG_v3.3_R15.md