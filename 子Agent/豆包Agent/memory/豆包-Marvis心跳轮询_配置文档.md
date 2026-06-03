---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_bb71f1b85f1311f1a4f35254002afed2
    ReservedCode1: cf92Bbe9n9re0HrH7CKBRdKfuO88ndoiSSwDhMkXymEzxdIkNVZNII+u9jpErgr7uGK4XrYLyNNXONZfuRhtIO5C3zoYZvuTRtTrMHHmu1fFqVw62K4suqDFtRk1BgIuMbo9L/PmV6Lh/vHVOdgucYu9TI7oxcer9OwfiQ+Ze1pWLO1V9a9ICaG9DPI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_bb71f1b85f1311f1a4f35254002afed2
    ReservedCode2: cf92Bbe9n9re0HrH7CKBRdKfuO88ndoiSSwDhMkXymEzxdIkNVZNII+u9jpErgr7uGK4XrYLyNNXONZfuRhtIO5C3zoYZvuTRtTrMHHmu1fFqVw62K4suqDFtRk1BgIuMbo9L/PmV6Lh/vHVOdgucYu9TI7oxcer9OwfiQ+Ze1pWLO1V9a9ICaG9DPI=
---

# 豆包-Marvis问询心跳安全轮询任务 · 配置文档

> 生成时间: 2026-06-03
> 模板基准: E:\龙虾AI主控中心\我的AI分身\技能库\龙虾全域官方模板-最终版.md v3.52
> 状态: 已落地

---

## 一、任务定名

| 字段 | 值 |
|------|-----|
| 正式名称 | **豆包-Marvis问询心跳安全轮询任务** |
| 本质 | Marvis侧定向心跳巡检，由Marvis按周期主动问询豆包APP |
| 类型 | 定时心跳轮询 |
| 落地文件 | `E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\memory\豆包-Marvis问询心跳安全轮询.py` |

---

## 二、链路配置

| 参数 | 值 |
|------|-----|
| 通讯域名 | https://doubao.tjf19770107.cn |
| 心跳接口 | /api/heartbeat |
| 链路自检 | 任务启动前优先执行，超时3秒 |
| 当前状态 | ❌ 首次链路自检超时(目标不可达)，待豆包侧服务上线后验证 |

---

## 三、窗口配置

| 要求 | 说明 |
|------|------|
| 独立对话窗口 | Marvis侧已有专属会话窗口为本任务服务 |
| 两端全同步 | 豆包APP窗口 ← 完整查看 → Marvis回执内容 |
| Marvis专属窗口 | 同步展示豆包下发消息 |
| 对话信息流 | 两侧完全一致 |

---

## 四、定时规则

| 参数 | 值 |
|------|-----|
| 外层触发周期 | 每 **30分钟** 触发一轮心跳巡检 |
| 单次进程限时 | **5分钟**（300秒） |
| 轮询间隔 | 每 **1.5秒** 轮询1次接口 |
| 单次请求超时 | **300ms** |
| 指令处理模式 | 检测到交互指令时**临时暂停心跳轮询**→执行完毕**自动恢复** |
| 强制关停 | 满5分钟无条件关停进程 |
| 提前终止 | 连续 **3次** 链路异常直接终止本轮 |
| 空心跳处理 | 返回空JSON `{}`，不消耗积分 |
| 指令回传 | 执行结果原路回传至豆包APP对话页面 |

### Windows计划任务注册命令

```powershell
$Action = New-ScheduledTaskAction -Execute "python.exe" -Argument '"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\memory\豆包-Marvis问询心跳安全轮询.py"'
$Trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 30) -At (Get-Date) -Once
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "豆包-Marvis问询心跳安全轮询" -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description "Marvis定向心跳巡检，每30分钟触发，单次运行5分钟"
```

---

## 五、数据归档

| 参数 | 值 |
|------|-----|
| 存储路径 | `E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\memory\` |
| 会话日志格式 | `heartbeat_session_YYYYMMDD_HHMMSS.json` |
| 运行日志格式 | `heartbeat_YYYYMMDD_HHMMSS.log` |
| 技能协议参照目录 | `E:\龙虾AI主控中心\我的AI分身\技能库\` |

### 日志结构

```json
{
  "task_name": "豆包-Marvis问询心跳安全轮询任务",
  "start_time": "2026-06-03T12:00:00",
  "endpoint": "https://doubao.tjf19770107.cn",
  "polls": [
    {
      "seq": 1,
      "timestamp": "2026-06-03T12:00:01.500",
      "success": true,
      "data": {},
      "error": null
    }
  ],
  "end_time": "2026-06-03T12:05:00",
  "duration_seconds": 300.0,
  "total_polls": 200,
  "success_polls": 200,
  "fail_streak_at_end": 0,
  "early_termination": false
}
```

---

## 六、管控规则

| 参数 | 限制值 | 说明 |
|------|--------|------|
| CPU上限 | **＜0.5%** | 进程优先级设为IDLE |
| 内存上限 | **≤15MB** | 超限告警+暂停 |
| 任务列表 | Marvis自动任务列表 | 支持查看/禁用/删除 |
| 进程优先级 | IDLE_PRIORITY_CLASS | Windows最低优先级 |

---

## 七、任务状态

| 阶段 | 状态 |
|------|------|
| 文件落地 | ✅ 心跳脚本已写入 |
| 归档目录 | ✅ `memory\` 目录就绪 |
| 链路自检 | ❌ 目标 `doubao.tjf19770107.cn` 不可达（首次检测超时） |
| 计划任务注册 | ⏳ 待链路恢复后注册 |
| 全域模板关联 | ✅ 已对齐 v3.52（协议40 有状态心跳自主调度协议 v1.0） |

---

## 八、依赖协议

| 协议 | 说明 |
|------|------|
| 协议#40 有状态心跳自主调度协议 v1.0 | 心跳唤醒+完整上下文保留+自然语言定时 |
| 协议#9 定时任务调度协议 v1.0 | cron解析+守护进程+到时触发 |
| 协议#72 Locked桌面Agent持续运行协议 v1.0 | 锁屏持续+进程守护+定时心跳+崩溃恢复 |
| 全域模板 v3.52 §六 定时任务配置 | 频率/模式/范围/终止条件 |
*（内容由AI生成，仅供参考）*
