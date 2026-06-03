
# DesktopController v2.0 — 桌面程序控制能力

> 技能ID：SKILL_DESKTOP_CONTROLLER_v2.0  
> 状态：ACTIVE  
> 创建：2026-05-31 R08（v1.0 升级至 v2.0）  
> 上一版本：v1.0 (R06)  
> 依赖：SafeGuard v3.0, AutoFileScanner v1.0  
> 被依赖：自进化闭环, AutoWake v2.0

---

## 一、技能定位

DesktopController 是豆包Agent对 Windows 桌面环境的控制层，负责安全地执行系统级操作——打开/关闭应用、文件管理、窗口操作、进程监控。所有操作通过 SafeGuard 安全审查，危险操作（删除/格式化/注册表修改）在调用时由 SafeGuard 的二级确认机制拦截。

```
用户 / 其他Skill请求
         │
    DesktopController v2.0
         │
    ┌────┼─────┬──────────┐
    ▼    ▼     ▼          ▼
  App   File  Window   Process
  操作   操作   操作     操作
         │
    SafeGuard v3.0 → 权限分级 / 操作审计
         │
    AutoFileScanner → 文件状态确认
```

---

## 二、核心能力（v2.0 增强项）

### 2.1 应用控制

| 操作 | 命令 | 风险等级 | 权限策略 |
|------|------|---------|---------|
| 打开应用 | `Start-Process` | 🟢 低 | 自动执行，记录日志 |
| 关闭应用 | `Stop-Process` | 🟡 中 | 确认后执行，记录日志 |
| 安装应用 | `winget/choco` | 🟡 中 | 需确认安装来源 |
| 卸载应用 | `winget uninstall` | 🟡 中 | 需确认，记录变更 |
| 系统设置 | `control / ms-settings` | 🟢 低 | 自动执行，只读操作 |

### 2.2 文件管理

| 操作 | 实现 | 风险等级 | 权限策略 |
|------|------|---------|---------|
| 创建文件/目录 | `New-Item` | 🟢 低 | 自动执行 |
| 复制/移动 | `Copy-Item` / `Move-Item` | 🟢 低 | 自动执行 |
| 重命名 | `Rename-Item` | 🟢 低 | 自动执行 |
| 删除到回收站 | `Remove-Item` (无 -Force) | 🟡 中 | 需确认，可恢复 |
| 永久删除 | `Remove-Item -Force` | 🔴 高 | 双重确认 + SafeGuard审查 |
| 磁盘格式化 | `Format-Volume` | 🔴 高 | 禁止执行 |

### 2.3 窗口管理

| 操作 | PowerShell实现 |
|------|---------------|
| 列出所有窗口 | `Get-Process \| Where-Object {$_.MainWindowTitle}` |
| 激活窗口 | 通过 Win32 API `SetForegroundWindow` |
| 最小化/最大化 | `ShowWindow` API |
| 获取前台窗口标题 | `GetForegroundWindow` + `GetWindowText` |

### 2.4 进程监控

```python
class ProcessMonitor:
    """进程监控器"""
    
    def list_processes(self, filter_name: str = None) -> List[ProcessInfo]:
        """列出运行中的进程，可按名称过滤"""
        ...
    
    def get_process_info(self, pid: int) -> ProcessInfo:
        """获取进程详细信息：内存/CPU/启动时间/命令行"""
        ...
    
    def wait_for_process(self, name: str, timeout: int = 30) -> bool:
        """等待进程启动（用于自动化流程同步）"""
        ...
```

---

## 三、三级权限分级体系

```
🟢 只读操作：自动执行
  ├── 列出进程 / 窗口 / 文件
  ├── 查询系统信息
  └── 启动应用（非安装类）

🟡 写入操作：需用户确认
  ├── 创建/修改/删除普通文件
  ├── 安装/卸载应用
  ├── 修改环境变量
  └── 停止非系统进程

🔴 高风险操作：双重确认 + SafeGuard拦截
  ├── 永久删除文件
  ├── 修改注册表
  ├── 停止系统服务
  ├── 格式化磁盘
  └── 修改系统目录
```

---

## 四、接口定义

### 4.1 Python 类接口

```python
class DesktopController:
    """Windows桌面程序控制器 v2.0"""

    def __init__(
        self,
        safe_guard=None,           # SafeGuard实例
        auto_file_scanner=None,    # AutoFileScanner实例
        audit_log_path: str = None # 操作审计日志路径
    ):
        self.safe_guard = safe_guard
        self.scanner = auto_file_scanner
        self.audit_log = Path(audit_log_path) if audit_log_path else None
        self.process_monitor = ProcessMonitor()

    # ========== 应用控制 ==========

    def open_app(self, app_path: str, args: str = None) -> ActionResult:
        """打开应用程序。
        
        Args:
            app_path: 应用路径或可执行文件名
            args: 命令行参数
        
        Returns:
            ActionResult: {success, message, pid}
        """
        ...

    def close_app(self, app_name: str, force: bool = False) -> ActionResult:
        """关闭应用程序。
        
        Args:
            app_name: 进程名称（不含 .exe）
            force: 是否强制终止
        
        风险等级：🟡 → 需要确认
        """
        ...

    def install_app(self, package_name: str, source: str = "winget") -> ActionResult:
        """通过包管理器安装应用。
        
        风险等级：🟡 → 需要确认安装来源
        """
        ...

    # ========== 文件管理 ==========

    def create_folder(self, path: str) -> ActionResult:
        """创建目录（自动创建中间目录）。"""
        ...

    def copy_file(self, source: str, dest: str, overwrite: bool = False) -> ActionResult:
        """复制文件或目录。"""
        ...

    def move_file(self, source: str, dest: str) -> ActionResult:
        """移动文件或目录。"""
        ...

    def delete_file(self, path: str, permanent: bool = False) -> ActionResult:
        """删除文件（默认移入回收站）。
        
        Args:
            path: 文件路径
            permanent: True=永久删除（🔴 高风险，需双重确认）
        """
        if permanent:
            return self._high_risk_delete(path)
        return self._safe_delete(path)

    def _high_risk_delete(self, path: str) -> ActionResult:
        """高风险删除流程：
        1. SafeGuard 三级定级审查
        2. 检查是否系统关键路径
        3. 询问用户是否备份
        4. 双重确认
        5. 执行 + 审计日志
        """
        ...

    # ========== 窗口管理 ==========

    def list_windows(self) -> List[WindowInfo]:
        """列出所有可见窗口。"""
        ...

    def activate_window(self, title_substring: str) -> ActionResult:
        """按标题子串激活窗口。"""
        ...

    def get_active_window(self) -> WindowInfo:
        """获取当前活动窗口信息。"""
        ...

    # ========== 系统信息 ==========

    def get_system_info(self) -> SystemInfo:
        """获取系统信息：OS版本/CPU/内存/磁盘。"""
        ...

    def get_disk_usage(self, drive: str = "C:") -> DiskUsage:
        """获取磁盘使用情况。"""
        ...

    # ========== 审计日志 ==========

    def log_action(self, action: str, level: str, result: ActionResult) -> None:
        """记录操作到审计日志。
        
        日志格式：
        {
            "timestamp": "ISO8601",
            "action": "open_app",
            "level": "LOW",
            "params": {...},
            "result": "success",
            "elapsed_ms": 1234
        }
        """
        ...

    def get_audit_trail(self, hours: int = 24) -> List[dict]:
        """查询指定时间范围内的操作审计记录。"""
        ...
```

### 4.2 数据结构

```python
@dataclass
class ActionResult:
    success: bool
    message: str
    data: dict = field(default_factory=dict)
    pid: int = 0
    elapsed_ms: float = 0.0

@dataclass
class WindowInfo:
    title: str
    process_name: str
    pid: int
    hwnd: int
    is_visible: bool

@dataclass
class ProcessInfo:
    pid: int
    name: str
    memory_mb: float
    cpu_percent: float
    start_time: str
    command_line: str

@dataclass
class SystemInfo:
    os_version: str
    cpu_count: int
    total_memory_gb: float
    available_memory_gb: float

@dataclass
class DiskUsage:
    drive: str
    total_gb: float
    used_gb: float
    free_gb: float
    percent_used: float
```

---

## 五、使用方式

### 5.1 基本使用

```python
from desktop_controller import DesktopController

dc = DesktopController(safe_guard=sg, auto_file_scanner=scanner)

# 打开记事本（🟢 自动执行）
result = dc.open_app("notepad.exe")
print(result.message)

# 创建目录（🟢 自动执行）
dc.create_folder("D:/NewProject/output")

# 删除文件（🟡 需要确认）
dc.delete_file("D:/temp/old_file.txt")  # → 移入回收站

# 永久删除（🔴 双重确认 + SafeGuard）
dc.delete_file("D:/temp/sensitive.txt", permanent=True)
```

### 5.2 与其他Skill联动

```python
# AutoWake 定时任务 → 清理临时文件
def nightly_cleanup():
    report = dc.scanner.full_scan()
    temp_files = [f for f in report.files if "temp" in f.path]
    for f in temp_files:
        dc.delete_file(f.path)  # 🟡 每次需确认

# SafeGuard 异常检测 → 回滚时移动文件
def rollback_restore(backup_path: str, target_path: str):
    dc.move_file(backup_path, target_path)
```

---

## 六、安全约束

1. **系统路径禁区**：禁止修改 `C:\Windows`, `C:\Program Files`, `C:\Program Files (x86)`, `C:\ProgramData`, `C:\Users\Default`
2. **敏感文件保护**：禁止修改 `.env`, `.git-credentials`, `*.pem`, `*.key`, 注册表系统键
3. **操作可逆优先**：删除默认走回收站；修改前自动备份（如 SafeGuard 要求）
4. **命令审计**：所有通过 DesktopController 执行的 PowerShell 命令都记录到审计日志
5. **禁止指令**：严禁执行 `Format-Volume`, `Clear-RecycleBin -Force`, `Remove-Item -Recurse -Force C:\*`

---

## 七、与其他技能的接口契约

| 调用方 | 接口 | 数据流向 |
|--------|------|---------|
| SafeGuard | 所有操作前调用 `review_action()` | 操作请求 → 安全检查结果 |
| AutoFileScanner | `list_files()` / `scan()` | 文件清单 → DesktopController |
| AutoWake | `open_app()`, `close_app()` | 定时任务 → 桌面自动化 |
| MemoryOS | `log_action()` | 操作记录 → 记忆存储 |
| 自进化闭环 | `execute_workflow_node()` | 工作流节点 → 桌面执行 |

---

## 八、操作审计日志示例

```json
{
  "audit_entries": [
    {
      "timestamp": "2026-05-31T14:30:00",
      "action": "open_app",
      "params": {"app": "notepad.exe"},
      "risk_level": "LOW",
      "result": "success",
      "pid": 12345,
      "elapsed_ms": 234
    },
    {
      "timestamp": "2026-05-31T14:31:00",
      "action": "delete_file",
      "params": {"path": "D:/temp/test.txt", "permanent": false},
      "risk_level": "MEDIUM",
      "result": "success",
      "confirmation": "user_approved",
      "elapsed_ms": 1567
    }
  ]
}
```

---

## 九、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | R06 | 初始版本：基础应用控制+文件操作 |
| v2.0 | R08 | 增强：三级权限分级体系、SafeGuard联动、操作审计日志、窗口管理、进程监控 |
