# 龙虾-端侧Agent全平台统一运行时协议 v2.0

> **协议编号**: #163
> **对标来源**: Hermes v0.15.0 Windows原生 + Coze 3.0三端协同 + OpenClaw移动端
> **上一版本**: v1.0 (协议#96, 2026-06-01)
> **版本**: v2.0
> **生效日期**: 2026-06-02
> **状态**: ✅ 已落地

---

## 一、协议概述

本协议升级自v1.0（协议#96），全面对标**Hermes v0.15.0 Windows原生支持**、**Coze 3.0三端协同**和**OpenClaw移动端焕新**，实现端侧Agent在Windows/macOS/Linux/iOS/Android/Web六端统一运行时，支持免WSL/Docker的纯原生运行、三端协同任务接力、移动端远程操控和计划任务开机自启。

**核心升级**：
- 新增Windows原生支持（免WSL/Docker）
- 新增三端协同架构（桌面端/移动端/Web端）
- 新增GitBash兼容层（解决Windows命令兼容）
- 新增计划任务开机自启（无管理员权限）
- 新增移动端远程操控协议

---

## 二、六端统一运行时架构

### 2.1 支持平台矩阵

| 平台 | 运行模式 | 依赖 | 状态 |
|------|---------|------|------|
| **Windows 10/11** | 原生 (PowerShell/GitBash) | GitBash (可选) | ✅ 已支持 |
| **macOS 12+** | 原生 (zsh/Bash) | 无 | ✅ 已支持 |
| **Linux (Ubuntu 20.04+)** | 原生 (Bash) | 无 | ✅ 已支持 |
| **iOS 15+** | 远程操控 (OpenClaw iOS) | OpenClaw App | ✅ 已支持 |
| **Android 10+** | 远程操控 (OpenClaw Android) | OpenClaw App | 🔄 开发中 |
| **Web (Chrome/Edge/Safari)** | 浏览器扩展 | OpenClaw Browser Extension | ✅ 已支持 |

### 2.2 统一运行时核心组件

```
端侧Agent统一运行时
├── 核心引擎 (Python/TypeScript)
│   ├── 任务调度器
│   ├── 工具调用引擎
│   ├── 记忆管理器
│   └── 安全沙箱
├── 平台适配层 (每个平台独立实现)
│   ├── Windows适配层 (PowerShell + GitBash)
│   ├── macOS适配层 (zsh + LaunchAgent)
│   ├── Linux适配层 (Bash + systemd)
│   ├── iOS适配层 (OpenClaw iOS App)
│   ├── Android适配层 (OpenClaw Android App)
│   └── Web适配层 (Browser Extension + WebSocket)
├── 通信层
│   ├── 本地IPC (命名管道/Unix Domain Socket)
│   ├── 远程RPC (WebSocket/HTTP)
│   └── 消息推送 (APNs/FCM/Web Push)
└── 存储层
    ├── 本地文件存储
    ├── SQLite (结构化数据)
    └── Vector DB (记忆检索)
```

---

## 三、Windows原生支持

### 3.1 免WSL/Docker运行

**之前**：Windows用户必须安装WSL2或Docker Desktop才能运行Hermes/OpenClaw

**现在**：纯Windows原生运行，零额外依赖

```powershell
# 安装（无需管理员权限）
Invoke-WebRequest -Uri "https://install.hermes.ai/windows.ps1" -OutFile "$env:TEMP\hermes_install.ps1"
powershell -ExecutionPolicy Bypass -File "$env:TEMP\hermes_install.ps1"

# 启动（前台）
hermes start

# 启动（后台，推荐）
Start-Process -WindowStyle Hidden -FilePath "hermes" -ArgumentList "start"

# 查看状态
hermes status
```

### 3.2 GitBash兼容层

**问题**：Windows PowerShell命令与Linux/macOS Bash不兼容（如`ls` vs `Get-ChildItem`）

**解决方案**：自动检测并使用GitBash执行Shell命令

```python
# 平台适配层 (Windows)
import subprocess
import os

def execute_shell_command(command: str) -> str:
    """执行Shell命令，自动选择PowerShell或GitBash"""
    
    # 检测GitBash
    gitbash_path = find_gitbash()
    
    if gitbash_path:
        # 使用GitBash执行（兼容Linux命令）
        result = subprocess.run(
            [gitbash_path, "-c", command],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
    else:
        # 降级到PowerShell
        result = subprocess.run(
            ["powershell", "-Command", convert_to_ps(command)],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
    
    return result.stdout

def find_gitbash() -> Optional[str]:
    """查找GitBash路径"""
    candidates = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\bin\bash.exe"),
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None
```

**轻量化PortableGit方案**（~45MB）：

```powershell
# 自动下载并配置PortableGit
if (-not (find_gitbash)) {
    Write-Host "未检测到GitBash，正在下载轻量版..."
    Invoke-WebRequest -Uri "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/PortableGit-2.45.0-64-bit.7z.exe" `
                      -OutFile "$env:TEMP\PortableGit.exe"
    Start-Process -Wait -FilePath "$env:TEMP\PortableGit.exe" -ArgumentList "-o`"$env:LOCALAPPDATA\hermes\git`" -y"
    # 添加到PATH
    $env:PATH += ";$env:LOCALAPPDATA\hermes\git\bin"
}
```

### 3.3 UTF-8字符集自动配置

**问题**：Windows控制台默认编码为GBK，导致UTF-8输出乱码

**解决方案**：自动切换控制台代码页至UTF-8 (CP_UTF8 = 65001)

```python
# Windows UTF-8自动配置
import sys
import ctypes

def enable_utf8_on_windows():
    """在Windows上启用UTF-8控制台输出"""
    if sys.platform == "win32":
        # 设置控制台代码页为UTF-8
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
        
        # 重构Python标准输入输出流
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
        sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)
        
        print("✅ Windows UTF-8编码已启用 (CP_UTF8=65001)")
```

---

## 四、三端协同架构

### 4.1 三端定义

| 端 | 定义 | 核心能力 | 协同角色 |
|----|------|---------|---------|
| **桌面端** | Windows/macOS/Linux原生应用 | 本地文件访问、系统级集成、高性能计算 | **主操作端**，处理复杂任务 |
| **移动端** | iOS/Android App | 任务查看、审批、轻量交互、远程操控 | **辅助端**，审批+监控 |
| **Web端** | Chrome/Edge/Safari浏览器扩展 | 跨平台访问、轻量级交互、快速配置 | **配置端**，快速设置 |

### 4.2 协同场景

```
场景1: 跨设备任务接力
  1. 用户在桌面端创建编程项目
  2. 离开电脑，在移动端继续查看进度
  3. 移动端收到"需要审批"通知
  4. 用户在移动端审批通过
  5. 桌面端自动继续任务

场景2: 移动端远程操控（锁屏模式）
  1. 用户离开电脑，电脑锁屏
  2. 在移动端打开OpenClaw App
  3. 选择"远程操控" → 选择电脑
  4. 发送指令: "帮我整理桌面文件"
  5. 电脑端Agent执行，结果推送到移动端

场景3: Web端快速配置
  1. 用户在朋友电脑上（无本地Agent）
  2. 打开 coze.cn 或 openclaw.ai
  3. 登录账号，自动同步配置和记忆
  4. 在Web端发送指令，云端Agent执行
```

### 4.3 协同协议

```json
// 三端协同消息格式
{
  "message_id": "msg_20260602_001",
  "type": "task_update",
  "task_id": "task_20260602_001",
  "source_device": {
    "device_id": "desktop_win_001",
    "device_type": "desktop",
    "platform": "windows"
  },
  "target_devices": ["mobile_ios_001", "web_chrome_001"],
  "payload": {
    "task_status": "awaiting_approval",
    "task_description": "删除文件: C:/Temp/*",
    "requires_approval": true,
    "approval_timeout_seconds": 300
  },
  "timestamp": "2026-06-02T15:30:00Z"
}
```

---

## 五、计划任务开机自启

### 5.1 Windows计划任务

**目标**：实现Agent开机自启，无需管理员权限

```powershell
# 创建计划任务（无需管理员权限）
$action = New-ScheduledTaskAction -Execute "hermes" -Argument "start --daemon"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$settings = New-ScheduledTaskSettings -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "HermesAgent" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
```

**关键设计**：
- 使用`-LogonType Interactive`（用户登录时触发），无需管理员权限
- 勾选"允许电池供电时运行"，避免笔记本合盖停止
- 勾选"即使电池供电也不停止"，确保移动场景持续运行

### 5.2 macOS LaunchAgent

```xml
<!-- ~/Library/LaunchAgents/com.hermes.agent.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hermes.agent</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/hermes</string>
        <string>start</string>
        <string>--daemon</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>~/Library/Logs/hermes.out.log</string>
    
    <key>StandardErrorPath</key>
    <string>~/Library/Logs/hermes.err.log</string>
</dict>
</plist>
```

加载：`launchctl load ~/Library/LaunchAgents/com.hermes.agent.plist`

### 5.3 Linux systemd

```ini
# ~/.config/systemd/user/hermes.service
[Unit]
Description=Hermes Agent
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/hermes start --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

启用：`systemctl --user enable hermes.service`

---

## 六、移动端远程操控

### 6.1 OpenClaw iOS Pro UI

**核心功能**：
- 实时查看Agent工作状态（任务列表/进度/日志）
- 发送语音指令（语音→文本→Agent执行）
- 审批敏感操作（删除文件/发送邮件/支付等）
- 接收推送通知（任务完成/需要审批/错误告警）

**通信协议**：

```swift
// iOS App → Agent (WebSocket)
{
  "type": "command",
  "command_id": "cmd_20260602_001",
  "command": "list_files",
  "args": {"path": "~/Desktop", "pattern": "*.pdf"},
  "timeout_seconds": 60
}

// Agent → iOS App (WebSocket)
{
  "command_id": "cmd_20260602_001",
  "status": "completed",
  "result": {
    "files": [
      {"name": "report.pdf", "size": 2048000, "modified": "2026-06-02T10:30:00Z"},
      {"name": "presentation.pdf", "size": 5120000, "modified": "2026-06-01T15:45:00Z"}
    ]
  }
}
```

### 6.2 锁屏远程操控

**场景**：电脑锁屏，但Agent仍需工作（如深夜跑训练任务）

**实现**：

```
1. 电脑端: Agent以"锁屏会话"模式运行（Windows: 使用WTSGetActiveConsoleSessionId检测锁屏）
2. 移动端: 通过WebSocket连接到电脑端Agent
3. 移动端发送指令: "检查训练进度"
4. 电脑端Agent: 读取训练日志，返回进度
5. 移动端: 显示进度条 + 可操作按钮（"继续" / "停止" / "调整超参数"）
```

**安全机制**：
- 锁屏模式下，禁止Agent访问敏感文件（如`~/.ssh/`, `~/.aws/`）
- 所有锁屏模式下的操作，均记录审计日志
- 用户可在移动端"紧急停止"按钮，立即终止Agent所有操作

---

## 七、与豆包Agent的集成

### 7.1 集成架构

```
豆包Agent
  └── 端侧统一运行时层（本协议）
        ├── Windows适配模块 (PowerShell + GitBash)
        ├── macOS适配模块 (zsh + LaunchAgent)
        ├── Linux适配模块 (Bash + systemd)
        ├── iOS远程操控模块 (OpenClaw iOS Protocol)
        ├── Android远程操控模块 (OpenClaw Android Protocol)
        ├── Web扩展模块 (Browser Extension)
        ├── 三端协同协调器
        └── 计划任务管理器
```

### 7.2 配置示例

```yaml
# 豆包Agent配置 (~/.lobster/config.yaml)
cross_platform_runtime:
  enable: true
  version: "v2.0"
  
  # 平台适配
  platforms:
    - type: "windows"
      enable: true
      shell_backend: "gitbash"  # 或 "powershell"
      utf8_auto_config: true
      portable_git:
        enable: true
        install_path: "$LOCALAPPDATA\\hermes\\git"
        
    - type: "macos"
      enable: true
      shell_backend: "zsh"
      launch_agent: true
      
    - type: "linux"
      enable: true
      shell_backend: "bash"
      systemd_user_service: true
      
    - type: "ios"
      enable: true
      connection_mode: "websocket"  # 或 "apns_push"
      
    - type: "android"
      enable: false  # 开发中
      connection_mode: "websocket"
      
    - type: "web"
      enable: true
      extension_id: "lobster-web-extension"
      
  # 三端协同
  cross_device_sync:
    enable: true
    sync_interval_seconds: 30
    conflict_resolution: "desktop_wins"  # desktop_wins / mobile_wins / manual
    
  # 计划任务
  scheduled_tasks:
    enable: true
    autostart: true
    tasks:
      - name: "每日晨报"
        schedule: "0 8 * * *"  # cron格式
        command: "生成今日工作计划"
        
      - name: "每周总结"
        schedule: "0 18 * * 5"
        command: "生成本周工作总结"
        
  # 移动端远程操控
  remote_control:
    enable: true
    require_approval_for_sensitive_ops: true
    sensitive_ops: ["delete_file", "send_email", "payment"]
```

### 7.3 使用方式

```bash
# Windows: 安装并启动
python -m lobster.install.windows --install-dir "$env:LOCALAPPDATA\lobster"
lobster start --daemon

# macOS/Linux: 安装并启动
python -m lobster.install.unix --install-dir ~/.local/share/lobster
lobster start --daemon

# iOS/Android: 连接
# 1. 在移动端安装OpenClaw App
# 2. 登录账号（与桌面端相同）
# 3. 自动发现局域网内的Agent实例
# 4. 点击连接 → 开始远程操控

# Web: 安装浏览器扩展
# 1. 打开 coze.cn 或 openclaw.ai
# 2. 安装浏览器扩展
# 3. 登录 → 自动同步配置和记忆
```

---

## 八、协议版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-01 | 初始版本（协议#96），CLI/Desktop/IDE/Chrome/Mobile五形态统一运行时 |
| **v2.0** | **2026-06-02** | **全面升级：Windows原生+三端协同+GitBash兼容+计划任务自启+移动端远程操控** |

---

> **协议状态**: ✅ 已落地
> **对标产品**: Hermes v0.15.0 (Windows原生) + Coze 3.0 (三端协同) + OpenClaw (移动端)
> **集成协议**: #96(五形态统一运行时v1) / #141(Coze3.0生态对接) / #160(去中心化自组织团队)
> **下一版本计划**: v3.0 支持ClawInstitute平台跨设备协同（协议#160对接）
