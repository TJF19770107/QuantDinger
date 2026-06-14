# task_queue.json

原始格式: JSON

```json
{
  "tasks": [
    {
      "id": "iter_global",
      "priority": "P1",
      "type": "iteration",
      "description": "每3小时全域闭环迭代（P0专项补全+技能锻造+情报采集+工程落地）",
      "status": "pending",
      "created_at": "2026-05-31 03:46:27",
      "timeout": 900,
      "retry_count": 0,
      "max_retries": 3
    },
    {
      "id": "scan_files",
      "priority": "P2",
      "type": "auto_scan",
      "description": "AutoFileScanner 扫描目录变化并注册能力",
      "status": "pending",
      "trigger": "wake",
      "timeout": 120,
      "retry_count": 0
    },
    {
      "id": "skill_forge",
      "priority": "P2",
      "type": "skill_forge",
      "description": "SkillForge 从迭代日志自动锻造新技能",
      "status": "pending",
      "trigger": "post_iteration",
      "timeout": 300,
      "retry_count": 0
    },
    {
      "id": "memory_compress",
      "priority": "P3",
      "type": "maintenance",
      "description": "MemoryOS 压缩长期记忆、清理过期条目",
      "status": "pending",
      "trigger": "wake",
      "timeout": 180,
      "retry_count": 0
    },
    {
      "id": "health_check",
      "priority": "P2",
      "type": "health",
      "description": "SafeGuard 系统健康检查 + 检查点验证",
      "status": "pending",
      "trigger": "wake",
      "timeout": 120,
      "retry_count": 0
    },
    {
      "id": "p0_claude_reasoning",
      "priority": "P0",
      "type": "architecture",
      "description": "落地Claude分层推理架构：问题解析→条件拆解→逻辑推演→方案执行→结果复盘",
      "status": "pending",
      "created_at": "2026-05-31 03:46:27",
      "timeout": 600,
      "retry_count": 0
    },
    {
      "id": "p0_workflow_viz",
      "priority": "P0",
      "type": "architecture",
      "description": "搭建可视化工作流体系：功能节点+串行/并行/条件跳转+状态看板+节点监控",
      "status": "pending",
      "created_at": "2026-05-31 03:46:27",
      "timeout": 600,
      "retry_count": 0
    },
    {
      "id": "p0_self_evolve",
      "priority": "P0",
      "type": "architecture",
      "description": "强化深度自进化核心闭环：SICA+GenericAgent+Obsidian+桌面联动+技能自动萃取",
      "status": "pending",
      "created_at": "2026-05-31 03:46:27",
      "timeout": 600,
      "retry_count": 0
    }
  ],
  "updated": "2026-05-31 03:46:27"
}
```
