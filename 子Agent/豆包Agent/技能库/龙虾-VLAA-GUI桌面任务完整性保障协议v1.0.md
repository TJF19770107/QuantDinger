# 龙虾-VLAA-GUI桌面任务完整性保障协议 v1.0

> **对标来源**：UCSC/CMU/Salesforce VLAA-GUI (arXiv:2604.21375, 2026.04)
> **里程碑**：OSWorld 77.5% 首次超越人类基准 72.4%
> **类型**：操作层 · 可靠性保障
> **状态**：ACTIVE

---

## 一、协议概述

VLAA-GUI协议解决桌面AI Agent在复杂多步任务中的两大顽固问题：
1. **任务未完成即提前宣布成功**（遗漏子步骤）
2. **陷入重复失败动作的死循环**（无法自我突破）

协议提供三层可靠性保障机制，将桌面Agent从"不可靠的自动操作"提升为"可信任的自主执行者"。

---

## 二、三层保障机制

### 2.1 完整性核查员（Completion Verifier）

每次Agent声明"任务完成"时，强制通过以下核查清单：

```
[ ] 用户原始指令中的所有子目标是否已完成？
[ ] 每个子目标是否有可验证的产出物？
[ ] 产出物内容是否与预期一致？
[ ] 是否有遗漏的步骤（对比任务规划）？
```

**任一项目未通过 → 拒绝"完成"声明 → 生成补救步骤 → 继续执行**

### 2.2 三层循环破除器（Loop Breaker）

当检测到Agent连续执行相同/相似操作≥3次且无进展时，逐级升级：

| 级别 | 触发条件 | 策略 |
|------|---------|------|
| L1 参数微调 | 同一操作失败2次 | 微调坐标/等待时间/输入方式 |
| L2 策略切换 | L1无效 | 更换操作方式（如从点击改为键盘快捷键） |
| L3 任务重规划 | L2无效 | 完全重规划剩余步骤，寻找替代路径 |

**L3失败 → 标记为阻塞 → 请求用户介入**

### 2.3 联网自救援Agent（Web Rescue Agent）

遇到陌生UI元素或无法识别的操作时：
1. 截取当前屏幕
2. 自动联网搜索该应用/界面的操作教程
3. 提取操作步骤
4. 尝试执行
5. 成功则将经验写入技能库

---

## 三、豆包Agent集成方案

### 3.1 与SafeGuard协议#9的协作

- SafeGuard负责安全边界（不删系统文件、不越权）
- VLAA-GUI负责任务完整性（不遗漏、不死循环）
- 两者互补：SafeGuard防破坏，VLAA-GUI防失败

### 3.2 与DesktopController协议#6的协作

- DesktopController执行具体桌面操作
- VLAA-GUI作为"监理层"监督每次操作的合理性和进度

### 3.3 与自愈回滚协议#24的协作

- 循环破除器L2/L3触发时，先尝试自愈修复
- 自愈失败 → 回滚到上一检查点 → 重新规划

---

## 四、配置参数

```json
{
  "completion_verifier": {
    "enabled": true,
    "check_subgoals": true,
    "check_artifacts": true,
    "max_retries": 2
  },
  "loop_breaker": {
    "enabled": true,
    "similarity_threshold": 0.85,
    "max_repeats_per_level": 3,
    "l3_strategy": "replan_with_alternative_path"
  },
  "web_rescue": {
    "enabled": true,
    "search_sources": ["web_search", "tutorial_sites"],
    "max_search_attempts": 3,
    "cache_tutorial": true
  }
}
```

---

> **版本**：v1.0 | **创建**：2026-05-31 R08 | **状态**：ACTIVE
