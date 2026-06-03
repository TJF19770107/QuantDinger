# 龙虾-Windows桌面视觉操控协议 v1.0

> **协议编号**：53
> **对标来源**：Codex Windows Computer Use + Locked Computer Use + AppShots
> **生成轮次**：R15
> **生效日期**：2026-06-01

---

## 一、协议概述

将桌面视觉操控能力从单一平台（macOS）扩展至 Windows 全生态，支持锁屏后台运行、截图上下文快照注入、键鼠语义模拟。使豆包 Agent 具备跨平台的完整桌面控制闭环。

## 二、三层桌面操控架构

```
Layer 1: 前景视觉操控（Foreground Computer Use）
  └─ Screenshot → Perceive → Reason → Act 循环
  └─ 语义定位替代坐标定位
  └─ 活动桌面独占模式（Windows限制）

Layer 2: 锁屏后台操控（Locked Computer Use）
  └─ 锁屏后 Agent 仍可运行
  └─ 仅限活跃可信回合解锁
  └─ 检测本地输入自动重锁
  └─ 手机远程查看进度/批准操作

Layer 3: 快照注入（AppShots）
  └─ 快捷键捕获应用窗口截图
  └─ 全文上下文注入（包含屏幕外隐藏内容）
  └─ 免手动复制粘贴
```

## 三、Windows 平台适配

| 组件 | 适配方案 |
|------|---------|
| Shell | PowerShell 5.1+ / WSL2 |
| 沙箱 | Windows Sandbox / Docker Desktop |
| 截图 | Windows.Graphics.Capture API |
| 键鼠 | SendInput API / UI Automation |
| 远程 | ChatGPT App iOS/Android ↔ Windows Codex App |

## 四、安全边界

- 锁屏解锁仅限活跃 Computer Use 回合，窗口外拒绝解锁
- 检测本地键盘/鼠标输入自动重锁
- 解锁前验证：活跃回合 + 可信来源
- 操作审计链：每次视觉操作记录截图+动作日志

## 五、适用场景

- 打开桌面 App 测试流程
- 检查 GUI bug（无 API/MCP 的传统系统）
- 远程控制 Windows 开发机
- 跨平台自动化工作流

---

> **协议状态**：ACTIVE
> **依赖**：协议33 视觉桌面操控协议 / 协议23 桌面Agent工作区隔离协议
