# DesktopController - 桌面程序控制模块
> 版本：v1.0  
> 自动生成：2026-05-31 R05  
> 来源：豆包Agent 6大自主能力补全  
> 对标：Microsoft Copilot Actions + Fara-7B + UI-TARS

## 触发条件
- 用户说"打开XX"、"关闭XX"、"运行XX"、"创建文件夹"、"整理文件"
- 涉及Windows系统操作、桌面软件控制

## 能力描述
三层安全控制体系，支持文件操作、进程管理、窗口控制、脚本执行，在严格安全护栏内模拟正常用户操作。

## 三层控制体系

### Layer A: Shell层（轻量/安全）
- 文件操作：创建/复制/移动/删除（回收站）
- 进程管理：启动/查询/终止用户应用
- 快捷方式：创建/删除桌面快捷方式
- 目录操作：创建/列出/清理文件夹
- 实现：PowerShell + Python subprocess

### Layer B: API层（中量/确认）
- 窗口管理：最大化/最小化/置顶/排列/切换
- 剪贴板：读写操作
- 屏幕信息：分辨率/DPI/缩放
- 注册表：只读查询（写入绝对禁止）
- 实现：pywin32 / ctypes

### Layer C: 自动化层（高级/授权）
- UI自动化：pywinauto控制应用界面
- 键盘鼠标：SendKeys模拟（需授权）
- 应用内操作：点击按钮/输入文字/截图
- 实现：pywinauto + pyautogui

## 安全白名单

### 允许路径
- E:\龙虾AI主控中心\ （所有子目录）
- 用户桌面（%USERPROFILE%\Desktop）
- 用户文档（%USERPROFILE%\Documents）
- 用户下载（%USERPROFILE%\Downloads）

### 禁止路径（绝对不可操作）
- C:\Windows\ （及所有子目录）
- C:\Program Files\ 
- C:\Program Files (x86)\
- C:\ProgramData\
- 系统注册表（写入）

### 操作确认矩阵
| 操作 | 允许 | 需确认 | 禁止 |
|------|------|--------|------|
| 打开应用 | ✅ | - | 系统工具 |
| 关闭应用 | ✅ | 系统进程 | 关键服务 |
| 创建文件 | ✅ | - | C:\Windows\ |
| 删除文件 | 回收站 | 永久删除 | 系统文件 |
| 执行脚本 | ✅ | .exe/.bat | 未知来源 |
| 窗口管理 | ✅ | - | - |
| 关机/重启 | - | ✅ | - |

## 输出格式
```json
{
  "operation": "open_app",
  "target": "notepad.exe",
  "result": "success",
  "layer": "A",
  "timestamp": "2026-05-31T03:00:00"
}
```

## 安全审查
- 风险等级：CAUTION
- 所有操作记录完整日志
- 系统路径操作自动拒绝
- 高风险操作二次确认

## 演化记录
- v1.0: 初始创建，基于R05迭代设计
