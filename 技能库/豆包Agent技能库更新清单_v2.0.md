# 豆包Agent — 技能库更新清单 v2.0
## 更新时间：2026-05-31 | 来源：第2轮全域迭代

---

## 🆕 新增技能模块

### 1. doubao-memory-system（长期记忆与Dreaming复盘）
- **对标**：Claude Managed Agents Memory + Dreaming
- **功能**：跨轮次记忆存储、自动摘要压缩、Dreaming模式复盘
- **存储路径**：E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\memory\
- **文件格式**：JSON 结构化记忆条目
- **状态**：P0 已规划

### 2. doubao-self-evolution（自改进闭环）
- **对标**：HyperAgents DGM-H
- **功能**：改进建议追踪、成功变体存档、改进过程自优化
- **存储路径**：E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\evolution\
- **状态**：P0 已规划

### 3. doubao-orchestrator（多Agent编排框架）
- **对标**：Hermes SWARM + Claude Orchestrator
- **功能**：任务看板、子Agent池管理、进程隔离、熔断机制
- **状态**：P1 规划中

### 4. doubao-skills-loader（Skills模块化系统）
- **对标**：Claude Skills
- **功能**：Skills注册/加载/组合、按需注入上下文
- **目录**：E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\skills\
- **状态**：P1 规划中

### 5. doubao-outcomes（任务契约与自评）
- **对标**：Claude Managed Agents Outcomes
- **功能**：成功标准rubric定义、执行后自评、未达标自动重试
- **状态**：P1 规划中

---

## 🔄 更新现有模块

### 6. doubao-context-engineering（上下文工程）
- **对标**：Claude CLAUDE.md + Skills + Compaction
- **更新内容**：增加上下文压缩策略、记忆注入规则
- **状态**：需更新

### 7. doubao-agent-benchmark（能力对标矩阵）
- **对标**：全域7大Agent
- **更新内容**：v2.0矩阵（10维度）、差距分析、优先级排序
- **状态**：v2.0 已更新

### 8. doubao-info-intake（全网情报采集模板）
- **对标**：全域
- **更新内容**：优化检索关键词、增加数据源列表
- **状态**：已更新

---

## 📊 技能库状态总览

| 状态 | 数量 | 模块 |
|------|------|------|
| 🆕 新增 | 5 | memory / evolution / orchestrator / skills-loader / outcomes |
| 🔄 更新 | 3 | context-engineering / benchmark / info-intake |
| ✅ 稳定 | 0 | — |
| 📦 总计 | 8 | — |
