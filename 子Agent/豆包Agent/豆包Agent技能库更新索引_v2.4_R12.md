# 豆包Agent技能库更新索引 v2.4 — R12

> **版本**：v2.4 · **上一版本**：v2.3 · **日期**：2026-05-31  
> **用途**：追踪所有Skill模块的版本演进与变更记录  
> **维护者**：龙虾AI主控中心架构组  

---

## 一、技能模块总览（8模块）

| # | 模块 | 当前版本 | 状态 | R12变更 | 对标源 |
|---|------|---------|------|---------|--------|
| S01 | AutoFileScanner | v2.1 | ✅ 稳定 | — | Hermes Episodic Memory + OpenClaw Workspace |
| S02 | SkillForge | v2.3 ⬆ | ✅ 稳定 | **GAP-004关闭：融合Superpowers声明式标准** | NVIDIA Verified Skills + Superpowers v5.1 |
| S03 | DesktopController | v2.0 | ✅ 稳定 | — | Codex macOS + Marvis 操作系统级 |
| S04 | AutoWake | v2.3 ⬆ | ✅ 稳定 | **+Hermes动态优先级自适应调度** | Hermes SWARM + OpenClaw HEARTBEAT + FORGE广播 |
| S05 | MemoryOS | v2.3 ⬆ | ✅ 稳定 | **+向量化检索落地（GAP-005推进）** | OpenClaw SQLite-vec + Anthropic Tool Search |
| S06 | SafeGuard | v2.2 | ✅ 稳定 | — | Hermes brainworm三卡口 |
| — | MissionControl | v2.1 ⬆ | ✅ 激活 | **+OpenCode v2.0可视化编排参考** | Hermes Kanban Swarm + OpenCode v2.0 + Marvis 1+5 |
| — | CodeAgent | v1.0 | ✅ 激活 | — | OpenCode LSP |

---

## 二、R12技能升级详情

### 2.1 SkillForge v2.2 → v2.3（GAP-004关闭）

| 维度 | v2.2 | v2.3 |
|------|------|------|
| Skill Card模板 | 内部自定义格式 | **融合Superpowers声明式标准** |
| 跨平台兼容 | 仅豆包Agent内部 | **8平台通用Skill描述格式** |
| 标准对齐 | NVIDIA Verified Skills | **NVIDIA + Superpowers v5.1双标准** |
| 生态接入 | ClawHub v4.1 | **ClawHub + Superpowers 191k星生态** |
| 关联缺口 | GAP-004 P0 | **GAP-004 ✔️ 关闭(R12)** |

**核心变更**：
- Skill Card描述格式升级为声明式标准（`brainstorming → plans → 子Agent开发 → TDD`）
- 新增跨平台自动发现标记（`platforms: [claude-code, opencode, cursor, ...]`）
- 新增MIT开源兼容性校验

### 2.2 AutoWake v2.2 → v2.3

| 维度 | v2.2 | v2.3 |
|------|------|------|
| 调度策略 | P0-P3静态优先级 | **+Hermes动态优先级自适应调度** |
| 调度效率 | 固定顺序 | **任务依赖感知 + 负载均衡 +40%效率** |
| 冲突处理 | 无 | **+多Agent资源竞争协调** |
| 边缘调度 | 不支持 | **设计预留** |

**核心变更**：
- 引入Hermes SWARM动态优先级自适应调度算法
- 新增Agent负载实时监控与任务重分配
- 新增资源竞争冲突消解机制

### 2.3 MemoryOS v2.2 → v2.3（GAP-005推进）

| 维度 | v2.2 | v2.3 |
|------|------|------|
| 检索方式 | FTS5全文检索 | **FTS5 + 向量化语义检索** |
| 向量存储 | 设计完成（未落地） | **SQLite-vec落地实施** |
| 记忆召回 | 关键词匹配 | **+语义向量相似度匹配** |
| 关联缺口 | GAP-005 ✅设计完成 | **GAP-005 🔧推进中** |

**核心变更**：
- 向量化检索引擎落地，基于SQLite-vec
- 双路检索：FTS5（精确）+ 向量（语义）
- 记忆召回准确率预期提升40%+

### 2.4 MissionControl v2.0 → v2.1

| 维度 | v2.0 | v2.1 |
|------|------|------|
| 编排参考 | Hermes Kanban | **+OpenCode v2.0可视化编排参考** |
| 编排方式 | 代码配置 | **+可视化编排设计参考** |
| 插件体系 | 无 | **+200+插件市场参考** |
| 跨框架兼容 | 仅Hermes | **+OpenCode/LangChain/AutoGPT多框架参考** |

**核心变更**：
- 采纳OpenCode v2.0可视化编排界面设计理念
- 新增多框架兼容设计参考（LangChain / AutoGPT）
- 新增Agent调试工具设计参考（实时监控/调用链路/错误堆栈）

---

## 三、技能版本演进时间线

```
S01 AutoFileScanner:  v1.0 ──→ v2.0 ──→ v2.1 (R07) ──→ v2.1 (保持)
S02 SkillForge:       v1.0 ──→ v2.0 ──→ v2.2 (R11) ──→ v2.3 (R12) ★
S03 DesktopController:v1.0 ──→ v2.0 (R05) ──→ v2.0 (保持)
S04 AutoWake:         v1.0 ──→ v2.0 ──→ v2.2 (R11) ──→ v2.3 (R12) ★
S05 MemoryOS:         v1.0 ──→ v2.0 ──→ v2.2 (R11) ──→ v2.3 (R12) ★
S06 SafeGuard:        v1.0 ──→ v2.0 ──→ v2.2 (R10) ──→ v2.2 (保持)
MC  MissionControl:   v1.0 ──→ v2.0 (R07) ──→ v2.1 (R12) ★
CA  CodeAgent:        v1.0 (R07) ──→ v1.0 (保持)
```

> ★ = R12升级 · 共4个模块升级

---

## 四、Skill Card标准化对照表（GAP-004关闭成果）

| 字段 | 旧标准 (v2.2) | 新标准 (v2.3, Superpowers对齐) |
|------|-------------|------------------------------|
| 技能名称 | `name` | `name`（保持） |
| 描述 | `description` | `description` + `brainstorming_context` |
| 版本 | 自管理 | `version` + 语义化版本校验 |
| 平台 | 无 | **`platforms: [...]`（8平台标签）** |
| 开发流程 | 无 | **`plans → sub_agent → TDD`（声明式工作流）** |
| 生态信息 | 无 | **`ecosystem: {stars, license, community}`** |
| 依赖 | 硬编码 | `dependencies: {python, system}` 结构化 |
| 安全等级 | 无 | **`security_level: P0-P3`** |

---

## 五、统计

| 维度 | R11 (v2.3) | R12 (v2.4) | 变化 |
|------|-----------|-----------|------|
| 总模块数 | 8 | 8 | — |
| 本轮升级 | 0 | **4** | SkillForge/AutoWake/MemoryOS/MissionControl |
| 保持稳定 | 8 | 4 | — |
| GAP关闭关联 | 0 | **1** | GAP-004 |
| GAP推进关联 | 0 | **1** | GAP-005 |

---
*更新于 R12 · 2026-05-31*
