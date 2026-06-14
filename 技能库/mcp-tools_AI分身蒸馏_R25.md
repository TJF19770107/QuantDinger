---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_4940d1eb61a611f18f065254007bceed
    ReservedCode1: NwU9wjCCsIXrjE8B3o1cv10+2MAoqITCphtcIrI6eiejWUivdyRQVhWuJ64UOqOk/NoE3byH4hnytU3lKdFJI1zfQJAuq7W4SCSM3f85hy/NyktISPg972O+NHqq3/ouX9pBVvFT4V3e++VKdTk1o/fvJ8iyX9TLn0YELMC+Saw6r2hfEZwMkLTD6dE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_4940d1eb61a611f18f065254007bceed
    ReservedCode2: NwU9wjCCsIXrjE8B3o1cv10+2MAoqITCphtcIrI6eiejWUivdyRQVhWuJ64UOqOk/NoE3byH4hnytU3lKdFJI1zfQJAuq7W4SCSM3f85hy/NyktISPg972O+NHqq3/ouX9pBVvFT4V3e++VKdTk1o/fvJ8iyX9TLn0YELMC+Saw6r2hfEZwMkLTD6dE=
---

# AI分身蒸馏专家

**版本**: R25

## 质量门控
- **G1**: 实事求是 — 所有数据必须可追溯至源文件
- **G2**: MD5去重 — 写入前校验，禁止重复文件
- **G3**: 路径合规 — 所有产物归档至指定目录
- **G4**: 对标校验 — 版本号与对标矩阵一致
- **G5**: 全局一致性 — SOUL/USER/AGENTS/角色总说明书四文件交叉验证

## 工具定义

### 1. distill_personality

步骤①：分析用户行为数据生成人格画像

**输出**: 知识库/用户人格画像_Rxx.md

### 2. distill_plan

步骤②：制定分阶段进化规划

**输出**: 知识库/AI分身进化规划_Rxx.md

### 3. distill_convert_files

步骤③：扫描并转换非MD文件

**输出**: 定时任务/蒸馏日志/文件转换日志_Rxx.md

### 4. distill_knowledge_base

步骤④：构建知识库索引

**输出**: 知识库/知识库索引_Rxx.md

### 5. distill_self_skill

步骤⑤：更新self-skill/MCP/Agent能力

**输出**: 技能库/

### 6. distill_core_config

步骤⑥：更新SOUL/USER/AGENTS

**输出**: 角色总说明书/SOUL.md USER.md AGENTS.md

### 7. sync_sub_agents

全域同步：将核心配置同步到三大子Agent

**输出**: 子Agent/*/config/

**输入**: 
- source_files: 角色总说明书.md, SOUL.md, USER.md, AGENTS.md

**输出**: 知识库/用户人格画像_Rxx.md

**输入**: 
- personality_report: 知识库/用户人格画像_Rxx.md

**输出**: 知识库/AI分身进化规划_Rxx.md

**输入**: 
- base_path: E:\龙虾AI主控中心\我的AI分身

**输出**: 定时任务/蒸馏日志/文件转换日志_Rxx.md

**输入**: 
- source_dir: E:\龙虾AI主控中心\我的AI分身\知识库

**输出**: 知识库/知识库索引_Rxx.md

**输入**: 
- distillation_history: 定时任务/蒸馏日志/

**输出**: 技能库/

**输入**: 
- all_outputs: 全部蒸馏产物

**输出**: 角色总说明书/SOUL.md USER.md AGENTS.md

**输入**: 
- core_config: SOUL.md, USER.md, AGENTS.md

**输出**: 子Agent/*/config/
*（内容由AI生成，仅供参考）*
