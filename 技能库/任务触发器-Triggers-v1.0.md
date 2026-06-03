# 任务触发器-Triggers v1.0

**对标来源**: Codex CLI Triggers  
**创建日期**: 2026-05-31  
**类别**: 自动化  
**优先级**: P1  
**关联技能**: ScheduledOps, AgentIter

---

## 一、概述

豆包Agent的自动触发器系统，对标Codex CLI的Triggers机制。使Agent能够响应外部事件自动执行任务。

## 二、触发器类型

### 2.1 文件变更触发器

| 触发条件 | 动作 | 示例 |
|---------|------|------|
| 文件修改 | 自动代码审查 | `.py` 文件变更 → 自动pylint + 代码审查 |
| 新文件创建 | 自动格式化 | 新 `.md` 文件 → 自动格式化 |
| 文件删除 | 备份提醒 | 关键文件删除 → 确认+备份 |

### 2.2 时间触发器

| 触发条件 | 动作 | 示例 |
|---------|------|------|
| 定时 | 定期巡检 | 每2小时全维度迭代 |
| 间隔 | 健康检查 | 每30分钟进程/Agent巡检 |
| Cron | 每日报告 | 每天09:00生成日报 |

### 2.3 事件触发器

| 触发条件 | 动作 | 示例 |
|---------|------|------|
| Webhook | 外部事件响应 | GitHub Issue → 自动分析+回复 |
| Agent消息 | Agent间事件 | 子Agent完成 → 通知Lead Agent |
| 系统事件 | 系统状态变化 | 磁盘空间不足 → 自动清理 |

### 2.4 条件触发器

| 触发条件 | 动作 | 示例 |
|---------|------|------|
| 阈值触发 | 指标超限 | 错误率>5% → 自动排查 |
| 状态变化 | 状态切换 | Agent异常 → 自动重启 |
| 模式匹配 | 关键词匹配 | 用户说"紧急" → 提升优先级 |

## 三、触发器配置

```yaml
triggers:
  - name: auto-code-review
    type: file_change
    watch_paths: ["src/**/*.py"]
    action:
      skill: code-review-automation
      params:
        max_files: 5
    cooldown: 300  # 5分钟内不重复触发
  
  - name: health-check
    type: interval
    interval: 1800  # 30分钟
    action:
      skill: HealthCheck
      mode: quick
  
  - name: github-issue
    type: webhook
    endpoint: "/webhook/github"
    action:
      agent: coder-agent
      task: "分析新Issue并生成回复"
```

## 四、安全约束

1. 任何触发器的动作必须经过安全沙箱审查
2. 触发频率限制：同一触发器每分钟最多1次
3. 触发的任务默认低风险模式
4. 所有触发记录写入日志
