# mcp-tools_AI分身蒸馏_R25.json

> 原始文件: `mcp-tools_AI分身蒸馏_R25.json`  |  类型: `.json`  |  自动转换

```json
{
  "skill_id": "83",
  "name": "AI分身蒸馏专家",
  "version": "R25",
  "tools": [
    {
      "name": "distill_personality",
      "description": "步骤①：分析用户行为数据生成人格画像",
      "input": {
        "source_files": [
          "角色总说明书.md",
          "SOUL.md",
          "USER.md",
          "AGENTS.md"
        ]
      },
      "output": "知识库/用户人格画像_Rxx.md"
    },
    {
      "name": "distill_plan",
      "description": "步骤②：制定分阶段进化规划",
      "input": {
        "personality_report": "知识库/用户人格画像_Rxx.md"
      },
      "output": "知识库/AI分身进化规划_Rxx.md"
    },
    {
      "name": "distill_convert_files",
      "description": "步骤③：扫描并转换非MD文件",
      "input": {
        "base_path": "E:\\龙虾AI主控中心\\我的AI分身"
      },
      "output": "定时任务/蒸馏日志/文件转换日志_Rxx.md"
    },
    {
      "name": "distill_knowledge_base",
      "description": "步骤④：构建知识库索引",
      "input": {
        "source_dir": "E:\\龙虾AI主控中心\\我的AI分身\\知识库"
      },
      "output": "知识库/知识库索引_Rxx.md"
    },
    {
      "name": "distill_self_skill",
      "description": "步骤⑤：更新self-skill/MCP/Agent能力",
      "input": {
        "distillation_history": "定时任务/蒸馏日志/"
      },
      "output": "技能库/"
    },
    {
      "name": "distill_core_config",
      "description": "步骤⑥：更新SOUL/USER/AGENTS",
      "input": {
        "all_outputs": "全部蒸馏产物"
      },
      "output": "角色总说明书/SOUL.md USER.md AGENTS.md"
    },
    {
      "name": "sync_sub_agents",
      "description": "全域同步：将核心配置同步到三大子Agent",
      "input": {
        "core_config": [
          "SOUL.md",
          "USER.md",
          "AGENTS.md"
        ]
      },
      "output": "子Agent/*/config/"
    }
  ],
  "quality_gates": {
    "G1": "实事求是 — 所有数据必须可追溯至源文件",
    "G2": "MD5去重 — 写入前校验，禁止重复文件",
    "G3": "路径合规 — 所有产物归档至指定目录",
    "G4": "对标校验 — 版本号与对标矩阵一致",
    "G5": "全局一致性 — SOUL/USER/AGENTS/角色总说明书四文件交叉验证"
  }
}
```
