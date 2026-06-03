# capabilities_R14.json

> 原始文件: `capabilities_R14.json`  |  类型: `.json`  |  自动转换

```json
{
  "version": "v14.0",
  "date": "2026-05-31",
  "total": 40,
  "new_in_r14": ["#37 增量索引引擎", "#38 AI文件标注", "#39 技能失败分析器", "#40 时间知识图谱"],
  "capabilities": {
    "perception_layer": {
      "#1 目录递归扫描": {"status": "STABLE", "version": "v2.0", "r14_note": "升级到增量索引"},
      "#2 内容解析引擎": {"status": "STABLE", "version": "v2.0", "r14_note": "新增PDF/DOCX/XLSX/PPTX"},
      "#37 增量索引引擎": {"status": "ACTIVE", "version": "v1.0", "r14_note": "基于mtime+MD5的增量更新"},
      "#38 AI文件标注": {"status": "ACTIVE", "version": "v1.0", "r14_note": "7AI provider自动文件树标注"}
    },
    "generation_layer": {
      "#3 自动技能生成": {"status": "ACTIVE", "version": "v4.0", "r14_note": "融合阿里云SkillForge三阶段闭环"},
      "#4 Skill Card标准": {"status": "STABLE", "version": "v2.0", "r14_note": "已关闭GAP-004"},
      "#39 技能失败分析器": {"status": "ACTIVE", "version": "v1.0", "r14_note": "SkillForge Failure Analyzer"},
      "#5 技能去重合并": {"status": "ACTIVE", "version": "v2.0", "r14_note": "Hermes Curator周期合并"}
    },
    "operation_layer": {
      "#6 Windows桌面控制": {"status": "ACTIVE", "version": "v3.0", "r14_note": "融合Windows UI Automation"},
      "#7 应用管理": {"status": "STABLE", "version": "v2.0"},
      "#8 进程管理": {"status": "STABLE", "version": "v2.0"},
      "#9 多模型协作": {"status": "DESIGNED", "version": "v1.0", "r14_note": "小模型决策+大模型规划"}
    },
    "drive_layer": {
      "#10 定时自主唤醒": {"status": "ACTIVE", "version": "v3.0", "r14_note": "融合TMT+TRIM+时间KG"},
      "#11 优先级矩阵": {"status": "STABLE", "version": "v2.0"},
      "#12 任务队列": {"status": "STABLE", "version": "v2.0"},
      "#13 多Agent协调": {"status": "ACTIVE", "version": "v2.0", "r14_note": "8种协调模式"}
    },
    "memory_layer": {
      "#14 短期记忆": {"status": "STABLE", "version": "v2.0"},
      "#15 长期记忆": {"status": "ACTIVE", "version": "v3.0", "r14_note": "融合Mem0压缩引擎"},
      "#16 情景记忆": {"status": "STABLE", "version": "v2.0"},
      "#40 时间知识图谱": {"status": "ACTIVE", "version": "v1.0", "r14_note": "Zep Temporal KG事件时间因果链"},
      "#17 向量检索": {"status": "DESIGNED", "version": "v1.0", "r14_note": "Mem0语义相似度匹配"}
    },
    "safety_layer": {
      "#18 事前审查": {"status": "STABLE", "version": "v3.0"},
      "#19 事中监控": {"status": "STABLE", "version": "v3.0"},
      "#20 事后恢复": {"status": "ACTIVE", "version": "v4.0", "r14_note": "State Rollback完整机制"},
      "#21 State Rollback": {"status": "ACTIVE", "version": "v1.0", "r14_note": "JumpCloud checkpoint序列化+hotl"},
      "#22 脑虫防御": {"status": "STABLE", "version": "v2.0"}
    },
    "reasoning_layer": {
      "#23 Claude推理引擎": {"status": "ACTIVE", "version": "v2.0", "r14_note": "800行增强版"},
      "#24 多模型热切换": {"status": "STABLE", "version": "v1.0"},
      "#25 Plan Mode": {"status": "STABLE", "version": "v1.0"}
    },
    "orchestration_layer": {
      "#26 可视化工作流": {"status": "ACTIVE", "version": "v2.0", "r14_note": "530行HTML暗色看板"},
      "#27 技能自动萃取": {"status": "ACTIVE", "version": "v1.0", "r14_note": "730行四阶段管道"},
      "#28 全域集成编排": {"status": "ACTIVE", "version": "v1.0", "r14_note": "440行推理→编排→进化"}
    },
    "coordination_layer": {
      "#29 自进化协调器": {"status": "ACTIVE", "version": "v1.0", "r14_note": "688行六阶段闭环"},
      "#30 端云路由引擎": {"status": "STABLE", "version": "v1.0"},
      "#31 专家门徒调度": {"status": "STABLE", "version": "v1.0"},
      "#32 检查点管理": {"status": "ACTIVE", "version": "v2.0", "r14_note": "State Rollback checkpoint序列化"}
    },
    "extended": {
      "#33 3D可视化": {"status": "DESIGNED", "version": "v1.0"},
      "#34 AI on UI": {"status": "DESIGNED", "version": "v1.0"},
      "#35 Llama推理": {"status": "DESIGNED", "version": "v1.0"},
      "#36 沙箱虚拟桌面": {"status": "DESIGNED", "version": "v1.0", "r14_note": "Windows CU沙箱标准"}
    }
  },
  "distribution": {
    "STABLE": 8,
    "ACTIVE": 16,
    "COMPLETED": 7,
    "DESIGNED": 8,
    "PLANNED": 1,
    "CLOSED": 0
  }
}
```
