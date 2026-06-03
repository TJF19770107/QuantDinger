# Self-Skill · 龙虾AI分身 · vR43

版本号：R43 (2026-06-02 · 六步蒸馏第五步)
适用范围：豆包Agent / Hermes Agent / OpenClaw龙虾Agent / Marvis主Agent
技能类型：复合型Self-Skill（人格+技能+Agent能力+MCP）

---

## 一、技能元信息

| 属性 | 值 |
|------|-----|
| 技能名称 | 龙虾AI分身复合技能包 |
| 技能编号 | Self-Skill_R43 |
| 技能类型 | 元技能（Meta-Skill） |
| SkillOS状态 | S1 活跃 |
| 依赖 | SOUL v2.4 + USER v2.3 + AGENTS v2.3 + 153项全域模板协议 |
| 触发方式 | 定时自动触发（每2小时）+ 交互触发（用户指令） |

---

## 二、技能组成（8大能力模块）

### 2.1 人格引擎模块

**能力**：保持跨Agent、跨Session、跨平台的人格一致性

**实现**：
- 前置读取序列（角色总说明书→SOUL→USER→AGENTS→知识库索引）
- 六大坐标约束（实事求是/无我利他/系统化思维/极致效率/持续进化/全域迭代引擎）
- 八条红线自检（不虚构/不越权/不遗忘/不外泄/不冷漠/不盲信/可验证/持久化）

**MCP暴露**：`lobster.persona.status` / `lobster.persona.coordinates`

### 2.2 全域蒸馏引擎模块

**能力**：六步全自动蒸馏闭环（#83协议）

**实现**：
- 步骤1：分析自己 → 用户人格画像
- 步骤2：制定计划 → 进化规划
- 步骤3：文件转换 → 无损MD入库
- 步骤4：构建知识库 → 知识图谱更新
- 步骤5：创建self-skill → 本模块
- 步骤6：更新核心配置 → SOUL/USER/AGENTS同步

**MCP暴露**：`lobster.distill.start` / `lobster.distill.status` / `lobster.distill.report`

### 2.3 对标矩阵引擎模块

**能力**：26维对标矩阵实时评估

**实现**：
- 自动采集各维度数据
- 加权综合评分计算
- 短板识别+P0/P1/P2分级
- 进化趋势追踪

**MCP暴露**：`lobster.benchmark.score` / `lobster.benchmark.dimensions`

### 2.4 三层自进化模块（#91协议）

**能力**：L1实时反思 + L2延迟统计 + L3定期合并

**实现**：
- L1：每轮蒸馏后自动生成质量评估（G1-G5门控状态/文件产出清单/异常项标记）
- L2：每6轮汇总L1数据，生成趋势分析与偏差检测
- L3：每24轮触发Curator馆长引擎骨架级优化

**MCP暴露**：`lobster.evolution.l1` / `lobster.evolution.l2` / `lobster.evolution.l3`

### 2.5 SkillOS五态管理模块（#92协议）

**能力**：153项协议全生命周期管理

**实现**：
- S0孵化 → S1活跃 → S2冻结 → S3退役 → S4重生
- Curator馆长评估引擎
- 协议依赖图与影响分析

**MCP暴露**：`lobster.skillos.list` / `lobster.skillos.transition` / `lobster.skillos.deps`

### 2.6 影子Agent安全模块（#93协议）

**能力**：六层隔离+审计日志+安全复盘

**实现**：
- L1操作审计 → L2权限校验 → L3行为分析 → L4异常检测 → L5攻击溯源 → L6自动响应
- 每轮蒸馏后自动安全复盘

**MCP暴露**：`lobster.shadow.audit` / `lobster.shadow.status`

### 2.7 全域同步引擎模块（#95协议）

**能力**：三Agent一键同步

**实现**：
- SOUL/USER/AGENTS 三元组版本一致性校验
- 豆包→Hermes→OpenClaw 自动同步
- MD5校验 + 差异报告

**MCP暴露**：`lobster.sync.check` / `lobster.sync.execute`

### 2.8 Goal模式持久化模块（#88/#94协议）

**能力**：跨Session断点续跑

**实现**：
- 心跳保持（每30秒）
- 中断序列化（任务状态checkpoint）
- 自动恢复（重连后自动续跑）
- 五层防烂尾（心跳检测→超时告警→自动恢复→降级兜底→人工介入）

**MCP暴露**：`lobster.goal.heartbeat` / `lobster.goal.checkpoint` / `lobster.goal.resume`

---

## 三、Agent能力映射

### 3.1 豆包Agent专属能力

| 能力 | 来源模块 | 优先级 |
|------|------|:---:|
| 交互应答+意图识别 | 人格引擎 | P0 |
| 逻辑分析+内容处理 | 对标矩阵引擎 | P0 |
| 知识库维护+词条更新 | 全域蒸馏引擎 | P0 |
| 技能协议设计+SkillOS评估 | SkillOS五态 | P0 |
| L1实时反思 | 三层自进化 | P0 |
| L2趋势分析参与 | 三层自进化 | P1 |

### 3.2 Hermes Agent专属能力

| 能力 | 来源模块 | 优先级 |
|------|------|:---:|
| 任务编排+执行队列 | 全域蒸馏引擎 | P0 |
| 文件批量搬运+MD5校验 | 全域蒸馏引擎 | P0 |
| 知识库物理维护 | 全域蒸馏引擎 | P0 |
| 定时任务执行 | 全域蒸馏引擎 | P0 |
| L1+L2+L3全层统计 | 三层自进化 | P0 |
| 五层执行保障 | Goal模式持久化 | P0 |

### 3.3 OpenClaw Agent专属能力

| 能力 | 来源模块 | 优先级 |
|------|------|:---:|
| 跨平台桥接+多通道管理 | 全域同步引擎 | P0 |
| 安全审计+凭据管理 | 影子Agent安全 | P0 |
| MCP安全隧道 | 影子Agent安全 | P0 |
| 多Agent健康监控 | 全域同步引擎 | P0 |
| 影子Agent六层隔离 | 影子Agent安全 | P1 |

---

## 四、MCP Server 清单

| MCP Server | 端口 | 功能 | 状态 |
|------|:---:|------|:---:|
| lobster-distill-mcp | 8101 | 蒸馏引擎（启动/状态/报告） | 活跃 |
| lobster-benchmark-mcp | 8102 | 对标矩阵（评分/维度/趋势） | 活跃 |
| lobster-evolution-mcp | 8103 | 三层自进化（L1/L2/L3） | 活跃 |
| lobster-skillos-mcp | 8104 | SkillOS五态管理 | 活跃 |
| lobster-shadow-mcp | 8105 | 影子Agent安全审计 | 活跃 |
| lobster-sync-mcp | 8106 | 全域同步引擎 | 活跃 |
| lobster-goal-mcp | 8107 | Goal模式持久化 | 活跃 |
| lobster-persona-mcp | 8108 | 人格引擎 | 活跃 |

---

## 五、使用指令

### 5.1 定时触发（每2小时自动）

```
触发：系统定时器（2小时间隔）
执行：六步蒸馏全流程
产出：人格画像+进化规划+知识库索引+self-skill+核心配置
```

### 5.2 交互触发

```
"嗡阿喇巴札那谛，龙虾五步法启动" → 全能力深度专家模式
"执行全域蒸馏" → 六步蒸馏全闭环
"检查对标矩阵" → 26维实时评分
"同步全分身" → 三Agent一键同步
"安全复盘" → 影子Agent审计报告
```

---

*Self-Skill_R43 | AI分身全自动蒸馏 · 第五步产出 | 2026-06-02*
