# 豆包Agent 全域缺口积压清单 v3.2-R14

> 更新: 2026-05-31 R14
> 上一版: v3.1_R17 → 本版统一编号至GAP-023
> 对标源: 14系统覆盖

---

## 缺口全览（17项，按优先级排列）

### 🔴 P0级（3项 — 当前最高优先级）

| # | 缺口名称 | 来源 | 对标源 | 当前状态 | 缺口描述 |
|---|----------|------|--------|---------|----------|
| GAP-007 | Plan模式缺失 | R13 | Claude Code/Codex CLI/Gemini CLI/Cursor | 📋 R13激活 → R14 AGP Planning Agent参考 | 豆包无显式任务分解→子Agent派发→执行验证闭环 |
| GAP-012 | MCP Gateway架构缺失 | R14 | Apigene MCP Gateway (2026) | 📋 R14新激活 | 工具管理分散，无统一网关(认证/路由/压缩/观测) |
| GAP-015 | 自进化缺乏形式化协议 | R14 | Autogenesis AGP (NTU/Stanford/Princeton) | 📋 R14新激活 | 自进化偏经验驱动，缺RSPL资源注册+SEPL原子操作 |

### 🟡 P1级（10项 — 重要但非阻断）

| # | 缺口名称 | 来源 | 对标源 | 缺口描述 |
|---|----------|------|--------|----------|
| GAP-009 | 上下文工程未结构化 | R13 | Anthropic CE + Hermes四层加载 | 上下文偏全量塞入，缺结构化组织+按需展开+容量限制 |
| GAP-010 | 技能标准化未覆盖agentskills.io | R13 | agentskills.io (20+工具兼容) | 技能生成未遵循跨平台标准，影响互操作 |
| GAP-011 | 回滚缺乏原子化保障 | R13 | Autogenesis SEPL | Merkle树回滚缺提议-评估-提交形式化保障 |
| GAP-013 | A2A Agent Card未发布 | R14 | Google A2A v1.0 (150+组织) | Agent无法被外部发现和协作 |
| GAP-014 | Firecracker沙箱未集成 | R14 | E2B/Firecracker/Google Sandbox | 代码执行仅容器隔离，缺MicroVM硬件隔离 |
| GAP-016 | 并行执行引擎偏弱(D07=3) | R14 | Marvis原生并行调度 | 多Agent并行调度效率待提升 |
| GAP-018 | 经验库自蒸馏未实现 | R14 | EvolveR (ICML 2026) | 记忆系统缺从经验中自动提炼策略原则的能力 |
| GAP-019 | 多Provider路由缺失 | R14 | OpenClaw delegateTo | 不同任务无法自动路由到最优LLM Provider |
| GAP-020 | 进程内MCP未实现 | R14 | Claude Agent SDK | 自定义工具需独立进程，存在IPC开销 |
| GAP-022 | A2A OAuth 2.0认证缺失 | R14 | A2A认证规范 | 缺乏跨组织Agent协作的标准认证机制 |

### 🟢 P2级（4项 — 前瞻规划）

| # | 缺口名称 | 来源 | 对标源 | 缺口描述 |
|---|----------|------|--------|----------|
| GAP-008 | 事件驱动触发缺失 | R13 | Codex CLI Triggers | 无GitHub/webhook/文件变更事件自动触发 |
| GAP-017 | 端云双模缺失 | R14 | Marvis效率/隐私双模 | 缺云端推理+本地执行混合模式 |
| GAP-021 | 能力市场接口未规划 | R14 | Workfoz/ClawHub | 豆包Agent技能无法对外发布和交易 |
| GAP-023 | GPU沙箱预留接口缺失 | R14 | Modal | AI推理/训练场景需要GPU沙箱 |

---

## 缺口来源演进

| 版本 | 新增缺口 | 总数 | 重点变化 |
|------|---------|------|----------|
| R13 | GAP-007,008,009,010,011 (5项) | 11 | Plan模式+上下文+标准+回滚 |
| R14 | GAP-012~023 (12项) | 23→合并→17 | MCP Gateway+自进化协议+沙箱+A2A+并行+Provider |

---

## R14→R15 优先补缺路线图

```
R15（预计2026-06-01 00:00）
├─ 🔴 GAP-015: AGP双层协议(RSPL+SEPL)设计文档 → 完成形式化定义
├─ 🔴 GAP-012: MCP Gateway架构方案初稿 → 统一工具管理层
├─ 🔴 GAP-007: Plan模式引擎(含AGP Planning Agent参考) → 补齐四大CLI标配
├─ 🟡 GAP-014: Firecracker沙箱集成方案 → 代码执行安全升级
└─ 🟡 GAP-013: A2A Agent Card发布设计 → Agent生态可发现性

R16（预计2026-06-01 03:00）
├─ 🟡 GAP-018: EvolveR经验库自蒸馏设计
├─ 🟡 GAP-011: SEPL原子回滚融入现有回滚体系
└─ 🟡 GAP-009: 上下文工程结构化方案

R17（预计2026-06-01 06:00）
├─ 🟡 GAP-010: agentskills.io技能标准化适配
└─ 🟡 GAP-016: 并行执行引擎强化方案
```

---

## 关键指标

| 指标 | R13 | R14 | 变化 |
|------|-----|-----|------|
| 总缺口 | 11 | 17 | +6（协议/沙箱/并行/Provider/双模/市场） |
| 🔴 P0 | 2 | 3 | +1（MCP Gateway） |
| 🟡 P1 | 4 | 10 | +6（沙箱/A2A/并行/蒸馏/Provider/进程内MCP） |
| 🟢 P2 | 1 | 4 | +3（双模/市场/GPU沙箱） |
| 能力数 | 39 | 42 | +3（Gateway/A2A/双模） |
| 对标系统 | 11 | 14 | +Autogenesis/EvolveR/Workfoz |