---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_d18573385eff11f1b5095254007bceed
    ReservedCode1: NdEvd97MTMdAGDAELjglFuRmloY4QvgqYG62630gZgl2wXwkqQmPVZTf2tVJw3K3tdU+5QbLT5NlZUvPLImbuTFQK/VYw+EgvvSxGheCq5CJDB0ILQtxwaUbYXcYfUiLiGJlnVw0GcebumNBtUr9yRp3xWMn5OZSOWLGmN8gxA046R73JmEYAZVHL9g=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_d18573385eff11f1b5095254007bceed
    ReservedCode2: NdEvd97MTMdAGDAELjglFuRmloY4QvgqYG62630gZgl2wXwkqQmPVZTf2tVJw3K3tdU+5QbLT5NlZUvPLImbuTFQK/VYw+EgvvSxGheCq5CJDB0ILQtxwaUbYXcYfUiLiGJlnVw0GcebumNBtUr9yRp3xWMn5OZSOWLGmN8gxA046R73JmEYAZVHL9g=
---

# 龙虾-桌面Agent全感官操控协议 v1.0

> **来源**: R50内生迭代 · 协议#172+#127+#45+#53+#180 五协议交叉融合
> **对标**: Codex Windows Computer Use v26.527 + Marvis 6Agent桌面级能力
> **状态**: ACTIVE · 桌面控制维度 99→100 核心突破协议

---

## 一、协议定义

桌面Agent全感官操控协议定义了Agent对桌面环境的完整感知-执行-调度能力体系。在原协议#172（视觉操控v3.0）、#127（桌面全接管v2.0）、#45（感知行动语义桌面）、#53（Windows视觉操控）、#180（全天候自主运行）的基础上，实现五感闭环的统一架构。

---

## 二、五层架构

### L1 视觉感知层

```
┌─────────────────────────────────────┐
│           L1 视觉感知层              │
├─────────────────────────────────────┤
│ 1. UIA元素树遍历                     │
│    - MSAA / UI Automation /          │
│      Accessibility API               │
│    - 获取窗口/按钮/菜单/文本框/列表    │
│    - 获取元素属性(name/type/rect/...)  │
│                                     │
│ 2. OCR文本识别                       │
│    - 截图→文本提取                    │
│    - 支持中英混合/多语言               │
│    - 文本坐标映射                     │
│                                     │
│ 3. 截屏帧差检测                       │
│    - 前后帧对比                        │
│    - 变化区域定位                       │
│    - 动画/进度条/加载状态感知            │
│                                     │
│ 4. 语义定位（核心突破）                │
│    - "点击发送按钮"→自动定位            │
│    - "输入用户名"→自动定位文本框         │
│    - 不依赖像素坐标                     │
│    - 对标 Codex Win CU v26.527        │
└─────────────────────────────────────┘
```

### L2 听觉交互层

```
┌─────────────────────────────────────┐
│           L2 听觉交互层              │
├─────────────────────────────────────┤
│ 1. 语音输入                          │
│    - 麦克风语音→文本转写               │
│    - 意图解析→动作执行                 │
│                                     │
│ 2. 系统音频输出监听                    │
│    - 通知/警报/播报声音                │
│    - 结合截屏上下文理解                 │
│                                     │
│ 3. 多模态输入融合                     │
│    - 语音+截屏 同步上下文              │
│    - "这个按钮"→截屏标注+语音          │
└─────────────────────────────────────┘
```

### L3 触觉执行层

```
┌─────────────────────────────────────┐
│           L3 触觉执行层              │
├─────────────────────────────────────┤
│ 1. 键鼠模拟                          │
│    - SendInput / 低级键盘钩子         │
│    - 点击/双击/右键/拖拽              │
│    - 键盘输入/快捷键/组合键            │
│                                     │
│ 2. 多点触控手势                       │
│    - Pinch/Zoom/Swipe/Rotate         │
│    - 触摸屏支持                       │
│                                     │
│ 3. 剪贴板读写                         │
│    - 文本/文件/图片/富文本             │
│    - 格式保持                        │
│    - 跨应用传递                       │
│                                     │
│ 4. 双重定位                          │
│    - 精确坐标（像素级）                │
│    - 语义定位（元素级）                │
│    - 自动降级：语义→坐标              │
└─────────────────────────────────────┘
```

### L4 语义上下文层

```
┌─────────────────────────────────────┐
│           L4 语义上下文层            │
├─────────────────────────────────────┤
│ 1. 活动应用感知                       │
│    - 前台窗口/进程标识                 │
│    - URL/文件路径/应用内页面            │
│                                     │
│ 2. 用户意图预测                       │
│    - 行为模式提取                     │
│    - 时间规律学习                     │
│    - 上下文触发关联                    │
│    - 预执行准备                       │
│    （独立协议#184细化）               │
│                                     │
│ 3. 跨应用工作流衔接                    │
│    - Excel取数据→PPT贴图表            │
│    - 浏览器填表→邮件发送              │
│    - 数据搬运/格式转换/流程接力         │
│                                     │
│ 4. 应用内状态感知                     │
│    - 表单字段内容/光标位置             │
│    - 列表选中项/页面滚动位置            │
│    - 弹窗/对话框/菜单打开状态           │
│    - 状态变更事件监听                  │
└─────────────────────────────────────┘
```

### L5 时间调度层

```
┌─────────────────────────────────────┐
│           L5 时间调度层              │
├─────────────────────────────────────┤
│ 1. 事件驱动触发器                     │
│    - 文件变更→自动处理                │
│    - 窗口切换→上下文更新              │
│    - 通知到达→响应动作                │
│                                     │
│ 2. 定时心跳巡检                       │
│    - 多桌面/多显示器状态              │
│    - 窗口布局变化检测                 │
│    - 进程存活检查                     │
│                                     │
│ 3. 锁屏持续运行                       │
│    - 进程守护（不被挂起）              │
│    - 崩溃自动恢复                     │
│    - 任务队列持久化                   │
│    （继承协议#53 Locked CU）          │
│                                     │
│ 4. 空闲时段预加载                     │
│    - 用户习惯预测                     │
│    - 提前启动应用                     │
│    - 环境预热（加载数据/构建上下文）     │
│    （独立协议#184细化）               │
└─────────────────────────────────────┘
```

---

## 三、协议接口定义

```yaml
desktop_pentasensory:
  L1_visual:
    uia_tree:
      api: [MSAA, UI_Automation, Accessibility]
      output: element_tree{name, type, rect, value, state}
      refresh: on_window_change | on_polling(500ms)
    ocr:
      engine: [Tesseract, PaddleOCR, Windows OCR]
      support: [zh, en, ja, ko]
      mapping: text_to_coordinate
    frame_diff:
      method: pixel_compare
      threshold: 5%
      output: change_regions[]
    semantic_position:
      input: natural_language_target
      output: {element, coordinate, confidence}
      fallback: coordinate_mouse

  L2_audio:
    voice_input:
      stt: Whisper | Azure STT | Windows STT
      output: text + intent
    system_audio:
      monitor: audio_output_device
      event_types: [notification, alarm, announcement]
      context_fusion: screenshot_sync
    multimodal:
      input: [voice, screenshot, pointer]
      sync: timestamp_alignment

  L3_tactile:
    keymouse:
      api: SendInput | keybd_event | mouse_event
      actions: [click, dblclick, right_click, drag, scroll, key, hotkey]
    touch:
      gestures: [pinch, zoom, swipe, rotate, long_press]
      platform: [touchscreen, touchpad]
    clipboard:
      formats: [text, html, image, file_list]
      maintain: format_preservation
    dual_positioning:
      primary: semantic
      fallback: coordinate
      degrade_condition: semantic_confidence < 0.7

  L4_semantic:
    active_app:
      detect: [foreground_window, process_name, url, file_path]
      update: on_window_change
    intent_prediction:
      protocol_ref: 协议#184
      output: predicted_actions[]
      confidence: float 0-1
    cross_app_workflow:
      context_carry: [data, format, selection, cursor]
      transfer: clipboard | drag_drop | automation
    state_aware:
      form: {field_values, cursor_position}
      list: {selected_items, scroll_offset}
      dialog: {open, type, action_buttons}

  L5_temporal:
    event_driven:
      triggers: [file_change, window_change, notification, schedule]
      action: handler_chain
    heartbeat:
      interval: 30s
      check: [desktop_state, process_health, task_queue]
    locked_runtime:
      keep_alive: process_guard
      recovery: crash_restart
      queue: persistent_task_queue
    idle_preload:
      protocol_ref: 协议#184
      trigger: idle_time > 60s
      actions: [pre_launch_apps, preload_data, pre_build_env]
```

---

## 四、融合溯源

| 融合协议 | 贡献层 | 贡献能力 |
|---------|:---:|---------|
| #172 桌面全平台视觉操控 v3.0 | L1, L3 | UIA/OCR/语义定位/键鼠/多平台 |
| #127 Windows桌面全接管 v2.0 | L3, L4 | 窗口/进程/会话/剪贴板/快捷键 |
| #45 感知行动语义桌面 v1.0 | L1, L4 | Screenshot→Perceive→Reason→Act |
| #53 Windows桌面视觉操控 v1.0 | L1, L5 | Locked锁屏/AppShots/跨平台 |
| #180 全天候自主运行 v1.0 | L2, L5 | 事件驱动/定时心跳/多端协同 |
| Codex Win CU v26.527 | L1 | 语义定位/锁屏后台/手机远程 |
| Marvis 6Agent | L4, L5 | 操作系统级/多Agent桌面协同 |

---

> **版本**: v1.0  
> **创建**: 2026-06-03 R50  
> **融合协议数**: 5+  
> **关联协议**: #183(跨会话延续) / #184(意图预测)
*（内容由AI生成，仅供参考）*
