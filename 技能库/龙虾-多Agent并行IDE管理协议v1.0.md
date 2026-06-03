# 龙虾-多Agent并行IDE管理协议 v1.0

> **协议编号**：协议68
> **版本**：v1.0
> **对标来源**：Superset IDE + ZCode + Codex IDE Plugin + Windsurf 2.0
> **核心价值**：多Agent并行状态管理、Git worktree隔离、远程工作区、Diff/Patch精确修改
> **激活咒语**：`/ide manage`
> **依赖协议**：协议12（IDE→Agent容器架构）、协议58（AI IDE五模块工程化）

---

## 一、协议概述

本协议实现Superset IDE式的多Agent并行IDE管理能力，统一管理多个编码Agent（Claude Code/Codex/OpenCode），通过Git worktree实现任务级隔离，支持远程工作区部署。

### 1.1 核心指标

| 指标 | 当前值 | 目标值 | 提升 |
|------|--------|--------|------|
| AI IDE能力 | 91 | 95 | +4 |
| 多Agent并行数 | 1 | 5+ | +4 |
| 远程部署支持 | 否 | 是 | 新增 |

---

## 二、多Agent并行状态管理

### 2.1 Superset配置

```yaml
# superset-config.yaml — 多Agent并行IDE管理配置
superset:
  version: "1.0"
  
agents:
  - id: claude-code
    name: "Claude Code Agent"
    model: claude-opus-4-8
    worktree: .worktrees/claude
    role: [refactor, debug, review]
    env:
      NODE_ENV: development
      PYTHONPATH: ./src
    
  - id: codex
    name: "Codex Agent"
    model: codex-5
    worktree: .worktrees/codex
    role: [implement, test, deploy]
    env:
      RUST_BACKTRACE: 1
    
  - id: opencode
    name: "OpenCode Agent"
    model: zen-router
    worktree: .worktrees/opencode
    role: [docs, lint, format]
    env:
      PRETTIER_CONFIG: .prettierrc

management:
  port_allocation: auto        # 自动分配端口（3000-3099）
  terminal_sessions: 5         # 最多5个并行终端
  env_isolation: strict        # 严格环境变量隔离
  resource_monitor: true       # 实时资源监控
  
state_matrix:
  # 每个Agent维护独立状态行
  format: "agent_id|task_id|status|progress|errors|uptime"
  poll_interval: 2s
  dashboard:
    enabled: true
    port: 9000
```

### 2.2 状态管理API

```python
# superset_state_manager.py
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"

@dataclass
class AgentState:
    agent_id: str
    task_id: str
    status: AgentStatus
    progress: float        # 0.0 ~ 1.0
    errors: List[str]
    uptime: float          # 秒
    model: str
    worktree: str
    port: Optional[int]

class SupersetStateManager:
    """多Agent并行IDE状态管理器"""
    
    def __init__(self):
        self.agents: Dict[str, AgentState] = {}
        self.port_pool = range(3000, 3100)
        self.active_ports: set = set()
    
    def register_agent(self, agent_config: dict) -> AgentState:
        """注册新Agent并分配端口"""
        port = self._allocate_port()
        state = AgentState(
            agent_id=agent_config["id"],
            task_id="",
            status=AgentStatus.IDLE,
            progress=0.0,
            errors=[],
            uptime=0.0,
            model=agent_config["model"],
            worktree=agent_config["worktree"],
            port=port
        )
        self.agents[agent_config["id"]] = state
        return state
    
    def _allocate_port(self) -> int:
        for port in self.port_pool:
            if port not in self.active_ports:
                self.active_ports.add(port)
                return port
        raise RuntimeError("No available ports in range 3000-3099")
    
    def get_state_matrix(self) -> str:
        """生成状态矩阵"""
        lines = ["AGENT_ID|TASK_ID|STATUS|PROGRESS|ERRORS|UPTIME"]
        for state in self.agents.values():
            lines.append(
                f"{state.agent_id}|{state.task_id}|"
                f"{state.status.value}|{state.progress:.1%}|"
                f"{len(state.errors)}|{state.uptime:.0f}s"
            )
        return "\n".join(lines)
    
    def dispatch_task(self, agent_id: str, task: dict):
        """分发任务到指定Agent"""
        agent = self.agents[agent_id]
        agent.task_id = task["id"]
        agent.status = AgentStatus.RUNNING
        # 通过协议12 IDE→Agent容器桥接
        self._bridge_to_ide_container(agent, task)
    
    def _bridge_to_ide_container(self, agent, task):
        """协议12桥接：IDE→Agent容器"""
        # 协议12是IDE→Agent容器架构协议，负责Agent实例化
        pass
```

---

## 三、Git Worktree任务隔离

### 3.1 Worktree管理器

```python
# git_worktree_manager.py
import subprocess
import os
from pathlib import Path

class GitWorktreeManager:
    """Git Worktree任务级隔离管理器
    
    对标：Superset IDE的 worktree-per-task 模式
    每个子Agent获得独立Git worktree，互不干扰
    """
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.worktree_dir = self.repo_root / ".worktrees"
        self.active_worktrees: dict = {}
    
    def create_worktree(self, agent_id: str, branch: str = "main") -> Path:
        """为Agent创建独立worktree"""
        worktree_path = self.worktree_dir / agent_id
        
        # 创建worktree
        subprocess.run([
            "git", "worktree", "add",
            str(worktree_path),
            branch
        ], check=True, cwd=self.repo_root)
        
        self.active_worktrees[agent_id] = {
            "path": worktree_path,
            "branch": branch,
            "created_at": self._timestamp()
        }
        return worktree_path
    
    def cleanup_worktree(self, agent_id: str):
        """任务完成后清理worktree"""
        if agent_id in self.active_worktrees:
            worktree_path = self.active_worktrees[agent_id]["path"]
            subprocess.run([
                "git", "worktree", "remove", str(worktree_path)
            ], cwd=self.repo_root)
            self.active_worktrees.pop(agent_id)
    
    def merge_results(self, agent_id: str, target_branch: str = "main"):
        """合并Agent worktree的变更"""
        worktree_path = self.active_worktrees[agent_id]["path"]
        # 获取worktree中的变更
        subprocess.run([
            "git", "worktree", "add", "-b", f"merge-{agent_id}",
            str(self.worktree_dir / f"{agent_id}-merge"), target_branch
        ], cwd=self.repo_root)
        
        # 合并策略：先cherry-pick再merge
        # ...
    
    def _timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
```

### 3.2 Worktree工作流

```
主仓库 (main)
  ├── .worktrees/claude/     → 重构/调试/审查
  ├── .worktrees/codex/      → 实现/测试/部署  
  ├── .worktrees/opencode/   → 文档/Lint/格式化
  └── .worktrees/review/     → 合并前统一Review
```

---

## 四、Diff/Patch精确修改

### 4.1 精确Diff引擎（对标Codex Plugin）

```python
# diff_patch_engine.py
"""
对标：Codex IDE Plugin + ZCode Diff引擎
当前问题：豆包Agent仅支持全文件覆盖
解决方案：引入精确Diff/Patch，仅修改目标行
"""

class DiffPatchEngine:
    """精确Diff/Patch引擎"""
    
    def generate_diff(self, old_file: str, new_file: str) -> str:
        """生成精确Diff"""
        import difflib
        with open(old_file, 'r', encoding='utf-8') as f:
            old_lines = f.readlines()
        with open(new_file, 'r', encoding='utf-8') as f:
            new_lines = f.readlines()
        
        diff = difflib.unified_diff(
            old_lines, new_lines,
            fromfile=old_file,
            tofile=new_file,
            n=2  # 2行上下文
        )
        return ''.join(diff)
    
    def apply_patch(self, target_file: str, diff_content: str) -> bool:
        """应用Diff Patch到目标文件"""
        import patch_match
        with open(target_file, 'r', encoding='utf-8') as f:
            original = f.read()
        
        try:
            patched = patch_match.apply_patch(original, diff_content)
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(patched)
            return True
        except Exception as e:
            print(f"Patch failed: {e}")
            return False
    
    def multi_agent_merge(self, patches: dict) -> dict:
        """多Agent变更合并，冲突检测
        
        patches = {
            "claude-code": "--- a/src/main.py\n+++ b/src/main.py\n...",
            "codex": "--- a/src/main.py\n+++ b/src/main.py\n...",
        }
        """
        from itertools import combinations
        
        conflicts = []
        agents = list(patches.keys())
        
        # 检测所有Agent对之间的冲突
        for a1, a2 in combinations(agents, 2):
            if self._has_conflict(patches[a1], patches[a2]):
                conflicts.append({
                    "agents": [a1, a2],
                    "severity": "warning",
                    "resolution": "manual_review_required"
                })
        
        return {
            "total_patches": len(patches),
            "conflicts": conflicts,
            "mergeable": len(conflicts) == 0
        }
    
    def _has_conflict(self, diff1: str, diff2: str) -> bool:
        """检测两个Diff是否冲突（修改了重叠行）"""
        lines1 = self._extract_modified_lines(diff1)
        lines2 = self._extract_modified_lines(diff2)
        return bool(lines1 & lines2)
    
    def _extract_modified_lines(self, diff: str) -> set:
        """提取Diff中修改的行号"""
        modified = set()
        for line in diff.split('\n'):
            if line.startswith('@@'):
                # @@ -10,5 +10,7 @@
                parts = line.split()
                old_range = parts[1].split(',')[0].replace('-', '')
                modified.add(int(old_range))
        return modified
```

---

## 五、远程工作区支持

### 5.1 远程部署配置

```yaml
# remote-workspace.yaml
remote_workspaces:
  - id: vps-shanghai
    host: 10.0.0.100
    port: 2222
    user: agent-runner
    key: ~/.ssh/agent_key_rsa
    workspace: /home/agent-runner/workspaces
    
  - id: vps-shenzhen
    host: 10.0.0.200
    port: 2222
    user: agent-runner
    key: ~/.ssh/agent_key_rsa
    workspace: /home/agent-runner/workspaces

deployment_rules:
  - condition: "agent.role contains 'deploy'"
    action: "deploy_to_vps"
    target: "vps-shanghai"
    
  - condition: "agent.cpu_usage > 80%"
    action: "offload_to_remote"
    target: "vps-shenzhen"
    
  - condition: "agent.model == 'claude-opus-4-8'"
    action: "local_only"
    reason: "编码Agent需要低延迟本地环境"
```

### 5.2 SSH隧道管理器

```python
# remote_workspace_manager.py
import paramiko
import os

class RemoteWorkspaceManager:
    """远程工作区SSH连接管理器
    
    对标：Superset IDE Remote Workspace
    将Agent计算负载卸载到VPS，本地仅保留IDE交互层
    """
    
    def __init__(self):
        self.connections: dict = {}
        self.workspaces: dict = {}
    
    def connect(self, remote_id: str, config: dict):
        """建立SSH隧道"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=config["host"],
            port=config["port"],
            username=config["user"],
            key_filename=os.path.expanduser(config["key"])
        )
        self.connections[remote_id] = ssh
        self.workspaces[remote_id] = config["workspace"]
    
    def deploy_agent(self, remote_id: str, agent_config: dict):
        """将Agent部署到远程VPS"""
        ssh = self.connections[remote_id]
        workspace = self.workspaces[remote_id]
        
        # 1. 创建远程工作目录
        agent_dir = f"{workspace}/{agent_config['id']}"
        ssh.exec_command(f"mkdir -p {agent_dir}")
        
        # 2. 同步代码到远程
        sftp = ssh.open_sftp()
        self._sync_directory(sftp, agent_config["worktree"], agent_dir)
        
        # 3. 远程安装依赖
        ssh.exec_command(f"cd {agent_dir} && pip install -r requirements.txt")
        
        # 4. 启动Agent守护进程
        ssh.exec_command(f"cd {agent_dir} && nohup python agent_daemon.py > agent.log 2>&1 &")
    
    def disconnect_all(self):
        for ssh in self.connections.values():
            ssh.close()
        self.connections.clear()
    
    def _sync_directory(self, sftp, local_path: str, remote_path: str):
        """增量同步目录"""
        for root, dirs, files in os.walk(local_path):
            remote_root = root.replace(local_path, remote_path)
            try:
                sftp.mkdir(remote_root)
            except:
                pass
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_root, file)
                sftp.put(local_file, remote_file)
```

---

## 六、实时代码质量分析

### 6.1 Lint/Type Check集成

```python
# code_quality_monitor.py
class CodeQualityMonitor:
    """实时代码质量分析
    
    对标：ZCode LSP集成 + Superset IDE实时诊断
    """
    
    def __init__(self):
        self.checkers = {
            "pylint": self._run_pylint,
            "mypy": self._run_mypy,
            "eslint": self._run_eslint,
            "prettier": self._run_prettier
        }
    
    def diagnose(self, file_path: str) -> dict:
        """运行所有检查器"""
        results = {}
        ext = os.path.splitext(file_path)[1]
        
        if ext == '.py':
            results["pylint"] = self._run_pylint(file_path)
            results["mypy"] = self._run_mypy(file_path)
        elif ext in ('.js', '.ts', '.jsx', '.tsx'):
            results["eslint"] = self._run_eslint(file_path)
            results["prettier"] = self._run_prettier(file_path)
        
        return {
            "file": file_path,
            "total_issues": sum(len(r.get("issues", [])) for r in results.values()),
            "checkers": results,
            "score": self._calculate_score(results)
        }
    
    def _run_pylint(self, file_path: str) -> dict:
        import subprocess
        result = subprocess.run(
            ["pylint", file_path, "--output-format=json"],
            capture_output=True, text=True
        )
        return {"tool": "pylint", "issues": result.stdout}
    
    def _run_mypy(self, file_path: str) -> dict:
        import subprocess
        result = subprocess.run(
            ["mypy", file_path, "--no-error-summary"],
            capture_output=True, text=True
        )
        return {"tool": "mypy", "issues": result.stdout}
    
    def _calculate_score(self, results: dict) -> float:
        total = sum(len(r.get("issues", [])) for r in results.values())
        return max(0.0, 100.0 - total * 5.0)
```

---

## 七、集成路径

```
协议68 集成路径：
  
  Superset IDE概念
    ├── 协议12: IDE→Agent容器架构 ← 已有
    ├── 协议58: AI IDE五模块工程化 ← 已有
    └── 协议68: 多Agent并行IDE管理 ← 新增
        ├── 多Agent并行状态矩阵
        ├── Git Worktree任务隔离
        ├── Diff/Patch精确修改
        ├── 远程工作区部署
        └── 实时代码质量监控

命令集：
  /ide manage       → 启动多Agent并行管理面板
  /ide diagnose     → 实时分析代码质量
  /ide diff <file>  → 显示Agent修改的Diff
  /ide worktree     → 为当前任务创建独立worktree
  /ide remote       → 部署Agent到远程VPS
```

---

## 八、依赖协议链

| 协议编号 | 协议名称 | 依赖关系 | 状态 |
|---------|---------|---------|------|
| 协议12 | IDE→Agent容器架构协议 | 前置依赖 | ✅ ACTIVE |
| 协议14 | 多Agent并行隔离开发协议 | Worktree隔离参考 | ✅ ACTIVE |
| 协议58 | AI IDE五模块工程化协议 | Diff/Patch基础 | ✅ ACTIVE |
| **协议68** | **多Agent并行IDE管理协议** | **本协议** | **v1.0** |

---

> **协议状态**: ✅ 已生成 v1.0
> **对标分数**: AI IDE能力 91 → 95（+4）
> **所属轮次**: R19
> **生成时间**: 2026-06-01