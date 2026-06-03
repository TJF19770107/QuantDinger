# Firecracker 豆包沙箱安全执行方案

> **对标**：AWS Firecracker microVM + gVisor
> **目标**：豆包代码执行层从无隔离升级为 microVM 级安全隔离
> **版本**：v1.0 Draft

---

## 一、安全需求分析

### 1.1 当前风险

| 执行场景 | 风险等级 | 所需隔离 |
|---------|---------|---------|
| 用户shell命令 | 🔴 高 | 必须隔离 |
| LLM生成代码执行 | 🔴 高 | 必须隔离 |
| Python脚本测试 | 🟡 中 | 推荐隔离 |
| 文件格式转换 | 🟡 中 | 可选隔离 |
| 系统配置查询 | 🟢 低 | 不需要 |

### 1.2 隔离方案对比

| 方案 | 隔离级别 | 启动速度 | 内存开销 | 兼容性 |
|------|---------|---------|---------|--------|
| 无隔离 | 无 | 即时 | 0 | 完全 |
| subprocess | 极低 | 即时 | 几MB | 完全 |
| Docker | 中（共享内核） | 秒级 | 几十MB | 高 |
| gVisor | 高（用户态内核） | 百毫秒 | 几十MB | 中 |
| Firecracker | 最高（独立内核） | 125ms | 5-10MB | 中 |
| QEMU/KVM | 最高（独立内核） | 秒级 | 数百MB | 高 |

**结论**：Firecracker 是"容器速度 + VM安全"的最优解。

## 二、沙箱架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户请求                               │
│          "帮我运行这段Python代码"                          │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              沙箱调度器 (Sandbox Scheduler)               │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. 风险评估 → 是否需要沙箱?                         │  │
│  │ 2. 资源评估 → 内存/CPU/网络需求                      │  │
│  │ 3. 沙箱分配 → 从预热池获取/新建 microVM              │  │
│  │ 4. 环境注入 → CoW镜像 + 代码 + 数据                 │  │
│  │ 5. 结果回传 → stdout + exit code + 文件              │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              Firecracker microVM Pool                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ microVM 1 │  │ microVM 2 │  │ microVM N │  ...        │
│  │ Kernel    │  │ Kernel    │  │ Kernel    │              │
│  │ CoW rootfs│  │ CoW rootfs│  │ CoW rootfs│              │
│  │ 128MB RAM │  │ 256MB RAM │  │ 512MB RAM │              │
│  │ No Network│  │ No Network│  │ No Network│              │
│  └──────────┘  └──────────┘  └──────────┘              │
│         ↑             ↑             ↑                    │
│         └─────────────┼─────────────┘                    │
│              virtio-vsock 通信                           │
└─────────────────────────────────────────────────────────┘
```

## 三、沙箱调度器实现骨架

```python
# sandbox_scheduler.py

import subprocess
import json
import uuid
import time
import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class RiskLevel(Enum):
    LOW = "low"        # 无需沙箱
    MEDIUM = "medium"  # 推荐沙箱
    HIGH = "high"      # 必须沙箱

@dataclass
class SandboxConfig:
    memory_mb: int = 128
    vcpu_count: int = 1
    timeout_seconds: int = 30
    allow_network: bool = False
    allow_filesystem_write: bool = True

class SandboxScheduler:
    def __init__(self, kernel_path: str, base_rootfs: str, pool_size: int = 5):
        self.kernel_path = kernel_path
        self.base_rootfs = base_rootfs
        self.pool_size = pool_size
        self.active_vms = {}
        self.warm_pool = []
    
    def assess_risk(self, code: str, context: dict) -> RiskLevel:
        """评估代码风险等级"""
        high_risk_patterns = [
            "os.system", "subprocess", "eval(", "exec(",
            "import shutil", "os.remove", "os.rmdir",
            "socket", "requests.post", "urllib",
            "ctypes", "__import__", "compile("
        ]
        
        medium_risk_patterns = [
            "open(", "write(", "read(",
            "os.path", "glob", "pathlib",
            "json.dump", "csv.writer", "pickle"
        ]
        
        for pattern in high_risk_patterns:
            if pattern in code:
                return RiskLevel.HIGH
        
        for pattern in medium_risk_patterns:
            if pattern in code:
                return RiskLevel.MEDIUM
        
        return RiskLevel.LOW
    
    def create_sandbox(self, config: SandboxConfig) -> str:
        """创建 Firecracker microVM"""
        vm_id = str(uuid.uuid4())[:8]
        
        # 创建 CoW 镜像
        cow_path = f"/tmp/sandbox-{vm_id}.ext4"
        subprocess.run([
            "qemu-img", "create", "-f", "qcow2",
            "-b", self.base_rootfs, "-F", "raw",
            cow_path
        ], check=True)
        
        # 启动 Firecracker
        fc_config = {
            "boot-source": {
                "kernel_image_path": self.kernel_path,
                "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
            },
            "drives": [{
                "drive_id": "rootfs",
                "path_on_host": cow_path,
                "is_root_device": True,
                "is_read_only": False
            }],
            "machine-config": {
                "vcpu_count": config.vcpu_count,
                "mem_size_mib": config.memory_mb
            },
            "network-interfaces": [] if not config.allow_network else [{
                "iface_id": "eth0",
                "host_dev_name": f"tap-{vm_id}"
            }]
        }
        
        # 通过 Firecracker API socket 启动
        fc_socket = f"/tmp/fc-{vm_id}.socket"
        # ... Firecracker API 调用 ...
        
        self.active_vms[vm_id] = {
            "config": config,
            "cow_path": cow_path,
            "fc_socket": fc_socket,
            "created_at": time.time(),
            "status": "running"
        }
        
        return vm_id
    
    def execute_in_sandbox(self, vm_id: str, code: str, timeout: int = 30) -> dict:
        """在沙箱中执行代码"""
        vm = self.active_vms.get(vm_id)
        if not vm:
            return {"error": "VM not found", "exit_code": -1}
        
        # 通过 vsock 发送代码
        # 在 microVM 内部运行: python3 -c "code"
        # 捕获 stdout/stderr/exit_code
        
        result = {
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
            "execution_time_ms": 0,
            "truncated": False
        }
        
        # ... vsock 通信 + 超时控制 ...
        
        return result
    
    def cleanup_sandbox(self, vm_id: str):
        """清理沙箱"""
        vm = self.active_vms.pop(vm_id, None)
        if vm:
            # 停止 Firecracker
            # 删除 CoW 镜像
            # 清理 socket
            pass
    
    def get_or_create_sandbox(self, code: str) -> str:
        """获取或创建沙箱（预热池优先）"""
        risk = self.assess_risk(code, {})
        
        if risk == RiskLevel.LOW:
            return None  # 无需沙箱
        
        config = SandboxConfig(
            memory_mb=128 if risk == RiskLevel.MEDIUM else 256,
            timeout_seconds=30 if risk == RiskLevel.MEDIUM else 60,
            allow_network=False
        )
        
        # 从预热池获取
        if self.warm_pool:
            vm_id = self.warm_pool.pop()
            return vm_id
        
        return self.create_sandbox(config)
```

## 四、资源限制矩阵

| 风险等级 | 内存 | CPU | 磁盘 | 网络 | 超时 | 最大并发 |
|---------|------|-----|------|------|------|---------|
| 🟢 低 | 无需沙箱 | 无需 | 无需 | 允许 | 无限制 | 无限制 |
| 🟡 中 | 128MB | 1 vCPU | 100MB CoW | 禁止 | 30s | 5 |
| 🔴 高 | 256MB | 1 vCPU | 200MB CoW | 禁止 | 60s | 3 |

## 五、实施路线

| 阶段 | 内容 | 耗时 |
|------|------|------|
| Phase 1 | Firecracker 安装 + 基础镜像制作 + 单VM启动测试 | R08 |
| Phase 2 | 沙箱调度器 + CoW镜像池 + vsock通信 | R09-R10 |
| Phase 3 | 风险评估引擎 + 预热池 + 资源限制 | R11 |
| Phase 4 | 监控面板 + 审计日志 + 告警 | R12 |

---

## 六、替代方案：Windows兼容路径

如果当前环境无法运行 Firecracker（需 Linux KVM），可采用渐进替代：

| 阶段 | 方案 | 隔离级别 |
|------|------|---------|
| 兜底 | subprocess + 临时目录 + 用户确认 | 极低 |
| 过渡 | Docker Desktop + --read-only + --network=none | 中 |
| 目标 | Firecracker (via WSL2 KVM) | 高 |

---

> 创建时间：2026-05-31 17:00
> 状态：设计完成 · Windows环境优先采用Docker过渡方案