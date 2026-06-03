# SafeGuard - 三环安全护栏与自动回滚系统
> 版本：v1.0  
> 自动生成：2026-05-31 R05  
> 来源：豆包Agent 6大自主能力补全  
> 对标：self_evolve_agent SAFE/CAUTION/UNSAFE + autoresearch Git回滚

## 触发条件
- **自动触发**：任何代码/配置变更前强制审查
- **自动触发**：运行时异常指标触发监控告警
- **自动触发**：迭代后核心功能退化触发自动回滚
- **手动触发**：用户说"回滚"、"撤销上次变更"、"恢复到稳定版本"

## 能力描述
三环安全体系：外环执行前审查 → 中环运行时监控 → 内环自动回滚。基于检查点系统，任何异常均可自动恢复到上一个稳定版本。

## 三环体系

### 外环：执行前审查（Pre-execution Review）
审查清单（5项全部通过才放行）：
1. ☐ 是否包含危险操作？（eval/exec/os.system/rm -rf/del /f/format）
2. ☐ 是否操作系统核心路径？（C:\Windows\等）
3. ☐ 是否包含无限循环或深度递归？
4. ☐ 是否尝试修改安全相关配置？
5. ☐ 是否有恶意模式特征？（base64混淆/隐藏文件操作/异常网络请求）

判决矩阵：
- SAFE：5项全部通过 → 自动放行
- CAUTION：1-2项需确认 → 展示风险点，需用户确认
- UNSAFE：3项以上或命中高危关键词 → 自动拒绝并记录

### 中环：运行时监控（Runtime Monitor）
监控指标及阈值：
| 指标 | 正常范围 | 告警阈值 | 终止阈值 |
|------|---------|---------|---------|
| CPU使用率 | <60% | >80% | >90% |
| 内存使用率 | <70% | >85% | >95% |
| 执行时间 | 预期×1.0 | 预期×1.5 | 预期×2.0 |
| 文件操作数 | <100 | >300 | >500 |
| 网络连接数 | <5 | >10 | >20 |

### 内环：自动回滚（Auto Rollback）
回滚触发条件（满足任一）：
1. 迭代后回归测试失败
2. 核心功能成功率下降 > 10%
3. 新增bug数量 > 3
4. 系统崩溃/异常退出

回滚流程：
```
1. 检测异常 ✓
2. 定位 stable_checkpoint.json
3. 对比当前状态与检查点Diff
4. 确认回滚范围 → 用户确认（SAFE级别可自动确认）
5. 执行回滚：文件还原 / Git reset
6. 验证回滚后状态（冒烟测试）
7. 记录回滚日志
8. 更新 stable_checkpoint 指针
```

## 检查点系统

### 检查点格式 (checkpoint_R05_20260531_030000.json)
```json
{
  "checkpoint_id": "R05_20260531_030000",
  "status": "stable",
  "snapshot": {
    "技能库/AutoFileScanner/SKILL.md": "md5_hash_xxx",
    "技能库/SkillForge/SKILL.md": "md5_hash_xxx",
    "memory/long_term.db": "md5_hash_xxx"
  },
  "diff_summary": "新增6个技能模块SKILL.md",
  "validation": {
    "smoke_test": "passed",
    "core_functions": ["AutoFileScanner", "MemoryOS"],
    "error_rate": 0
  },
  "rollback_cmd": "copy checkpoints/checkpoint_R05.../* to 豆包Agent/",
  "created_at": "2026-05-31T03:00:00"
}
```

### 稳定版本指针 (stable_checkpoint.json)
```json
{
  "current_stable": "checkpoint_R05_20260531_030000",
  "last_rollback": null,
  "total_checkpoints": 5,
  "total_rollbacks": 0
}
```

## UNSAFE自动拒绝规则（不可绕过）
以下操作无需审查，直接拒绝：
- 删除系统文件（C:\Windows\等）
- 格式化磁盘操作
- 修改系统注册表（写入）
- 包含 eval("__import__('os').system(...)") 等绕过模式
- 连接到黑名单IP/域名
- 尝试修改本SafeGuard模块自身

## 输出格式
```json
{
  "review_result": "SAFE",
  "checkpoint_created": "checkpoint_R05_20260531_030000",
  "warnings": [],
  "monitor_status": "normal",
  "rollback_status": null
}
```

## 安全审查
- 风险等级：CAUTION（自身是安全模块，但回滚操作需谨慎）
- SafeGuard自身代码禁止被SkillForge修改
- 回滚操作记录到独立审计日志

## 演化记录
- v1.0: 初始创建，基于R05迭代设计
