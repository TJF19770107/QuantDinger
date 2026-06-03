# 豆包Agent 能力缺口追踪 (GAP BACKLOG)

> 最后更新: 2026-05-31 R∞ 全域深度迭代
> 对标目标: Codex · Claude · Hermes · OpenClaw · OpenCode · Gemini · Marvis Workbody · MUSE · SkillOpt · ANNEAL · MOSS

---

## 状态图例

- 📋 已识别，方案设计中
- 🔧 开发中
- ✅ 已修补，待验证
- ✔️ 已验证通过

---

## P0 - 关键缺口（阻塞核心能力）

| ID | 缺口描述 | 对标源 | 状态 | 识别轮次 | 最后修补 |
|----|----------|--------|------|----------|---------|
| GAP-001 | **Harness工程飞轮**：缺失 Traces→Evals→Diagnosis→自修复 闭环 | Codex CLI | ✅ | R001 | SICA进化器+自动回滚规则引擎落地 |
| GAP-002 | **Agent间直接通信**：子Agent间无直接通信通道 | OpenClaw | ✅ | R001 | 可视化工作流多Agent分发+Agent节点 |
| GAP-003 | **自动技能生成与进化**：技能需手动编写 | Hermes | ✔️ | R001→R07 | SkillForge v4.0+MUSE五阶段（R∞升级） |
| GAP-034 | **Layer7知识联动层全空白** | Obsidian生态 | 📋 | R09 | 待R∞+1设计 |
| GAP-035 | **AONP协议栈未对接** | AONP MWC 2026 | 📋 | R09 | 待R∞+2设计 |
| GAP-036 | **长周期任务持久化缺失** | Durable Task | 📋 | R09 | 待实现 |
| GAP-044 | **MOSS源码级自进化安全护栏** | MOSS | 📋 | R∞ | 待设计 |

## P1 - 重要缺口（影响效率与质量）

| ID | 缺口描述 | 对标源 | 状态 | 识别轮次 | 最后修补 |
|----|----------|--------|------|----------|---------|
| GAP-004 | **多层推理链**：无 thinking+content 双通道显式推理输出 | Claude | ✅ | R001 | Claude五层推理引擎完整落地 |
| GAP-005 | **技能渐进式匹配**：技能全量加载而非四层渐进式 | Hermes | ✅ | R001 | GenericAgent轻量化按需加载 |
| GAP-037 | **沙箱安全执行层空白** | Zylos Sandbox | 📋 | R09 | 待实现 |
| GAP-038 | **Obsidian-豆包双向同步未部署** | 全域模板§十二 | 📋 | R09 | 待部署 |
| GAP-042 | **MUSE五阶段技能生命周期完整实现** | MUSE-Autoskill | 📋 | R∞ | R∞设计完成，待代码实现 |
| GAP-043 | **SkillOpt文本空间梯度优化引擎** | Microsoft SkillOpt | 📋 | R∞ | R∞设计完成，待代码实现 |
| GAP-045 | **ANNEAL符号补丁生成与验证** | ANNEAL | 📋 | R∞ | R∞设计完成，待代码实现 |
| GAP-046 | **深度Agent桌面控制对标** | My Computer/Meta | 📋 | R∞ | 待对标分析 |

## P2 - 增强缺口（锦上添花）

| ID | 缺口描述 | 对标源 | 状态 | 识别轮次 |
|----|----------|--------|------|----------|
| GAP-006 | **子Agent独立人格文件**：无 SOUL.md 式独立人格定义 | OpenClaw | 📋 | R001 |
| GAP-007 | **工具权限精细控制**：无 rateLimit/requireConfirmation 粒度 | OpenClaw | 📋 | R001 |
| GAP-008 | **评估回归套件**：无 Promptfoo 等价自动化回归评估 | Codex CLI | 📋 | R001 |
| GAP-009 | **多模型路由调度**：无模型无关的任务-模型最优匹配 | Gemini Antigravity | 📋 | R001 |
| GAP-010 | **Token消耗优化**：目标降低至当前 1/4（Hermes 同等水平） | Hermes | 📋 | R001 |
| GAP-039 | **看板协作广度不足** | Hermes SWARM 9模式 | 📋 | R09 |
| GAP-040 | **MCP工具集未体系化** | Marvis Workbody | 📋 | R09 |
| GAP-041 | **能力注册中心未实现** | AONP AIDP | 📋 | R09 |

## P3 - 深度优化缺口

| ID | 缺口描述 | 对标源 | 状态 | 识别轮次 |
|----|----------|--------|------|----------|
| GAP-011 | **GEP完整6步循环实现** | Evolver GEP | 📋 | R07 |
| GAP-013 | **DGM-H元认知自修改** | HyperAgents | 📋 | R07 |
| GAP-015 | **Agent SDK化输出** | Claude SDK | 📋 | R07 |

---

## R∞闭合记录

| 缺口ID | 描述 | 闭合方式 |
|--------|------|---------|
| GAP-012 | Evolver守护进程 | ✔️ 融入EVOL-OBSERVE |
| GAP-014 | 跨域迁移能力 | ✔️ 融入EVOL-UPDATE |
| GAP-016 | 进化可视化EvoMap | ✔️ 融入EVOL-REFLECT |
| GAP-017 | Ralph Loop目标自闭环 | ✔️ 融入EVOL-INTEGRATE |

## R∞新增缺口

| 缺口ID | 描述 | 对标源 | 优先级 |
|--------|------|--------|--------|
| GAP-042 | MUSE五阶段技能生命周期完整实现 | MUSE-Autoskill | P1 |
| GAP-043 | SkillOpt文本空间梯度优化引擎 | Microsoft SkillOpt | P1 |
| GAP-044 | MOSS源码级自进化安全护栏 | MOSS | P0 |
| GAP-045 | ANNEAL符号补丁生成与验证 | ANNEAL | P1 |
| GAP-046 | 深度Agent桌面控制对标 | My Computer/Meta | P1 |

---

## 修补进度时间线

```
R001→R007 (05-25~05-31) ─── 17项缺口识别，7项闭合
     │
R009 (05-31) ─── 8项新缺口(GAP-034~041)，总缺口25项，修补率28%
     │
R∞ (05-31) ─── 5项新缺口(GAP-042~046)，4项闭合(GAP-012/014/016/017)
     │         总缺口30项，闭合11项，修补率36.7%
     │         核心突破: EVOL自进化层 + MUSE五阶段对标 + SkillOpt适配
     │         + ANNEAL集成方案 + MOSS安全护栏
     ...
```

---

## 缺口总览

| 指标 | 数值 |
|------|------|
| 总缺口数 | 30项 |
| 已闭合 | 11项 |
| 修补率 | 36.7% |
| P0未闭合 | 4项 (GAP-034/035/036/044) |
| P1未闭合 | 8项 |
| P2未闭合 | 8项 |
| P3未闭合 | 3项 |

---

*自动维护于豆包Agent自进化系统*