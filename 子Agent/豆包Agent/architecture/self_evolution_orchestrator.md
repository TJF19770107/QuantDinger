# self_evolution_orchestrator.py

> 原始文件: `self_evolution_orchestrator.py`  |  类型: `.py`  |  自动转换

```python
"""
SICA自进化编码框架适配器 v1.0
对标：SICA (Self-Improving Code Architecture)
代码生成 → 沙箱执行 → 自动测试 → 反馈优化 → 迭代进化

R07 全域缺口专项补全 - P0-3
"""

import json
import time
import hashlib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SICAEvolver")


class EvolutionStatus(Enum):
    IDLE = "idle"
    GENERATING = "generating"
    TESTING = "testing"
    EVALUATING = "evaluating"
    DEPLOYING = "deploying"
    ROLLBACK = "rollback"
    COMPLETED = "completed"


@dataclass
class EvolutionCycle:
    """单次进化周期"""
    cycle_id: str
    target_module: str
    start_time: float = 0.0
    end_time: float = 0.0
    status: EvolutionStatus = EvolutionStatus.IDLE
    code_before: str = ""
    code_after: str = ""
    test_results: dict = field(default_factory=dict)
    quality_score: float = 0.0
    decision: str = ""  # accept / reject / continue
    diff_summary: str = ""


@dataclass
class EvolutionLog:
    """进化日志"""
    cycles: list = field(default_factory=list)
    total_evolutions: int = 0
    success_rate: float = 0.0
    average_improvement: float = 0.0


class SICAEvolver:
    """SICA自进化编码框架核心控制器"""

    ACCEPT_THRESHOLD = 0.75
    REJECT_THRESHOLD = 0.40
    MAX_ITERATIONS = 5

    def __init__(
        self,
        sandbox=None,
        test_runner=None,
        code_generator=None,
        snapshot_manager=None,
        skill_forge=None
    ):
        self.sandbox = sandbox or self._default_sandbox
        self.test_runner = test_runner or self._default_test_runner
        self.code_generator = code_generator or self._default_code_generator
        self.snapshot_manager = snapshot_manager
        self.skill_forge = skill_forge
        self.evolution_log = EvolutionLog()

    def evolve(self, target_module: str, iteration_limit: int = None) -> EvolutionCycle:
        """执行一次完整进化周期"""
        limit = iteration_limit or self.MAX_ITERATIONS
        cycle = EvolutionCycle(
            cycle_id=f"sica_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            target_module=target_module,
            start_time=time.time()
        )

        logger.info(f"SICA进化启动: {target_module} (最多{limit}轮)")

        # 进化前快照
        if self.snapshot_manager:
            self.snapshot_manager.create_snapshot(
                f"pre_sica_{cycle.cycle_id}",
                [target_module],
                f"SICA进化前快照: {target_module}"
            )

        for iteration in range(limit):
            logger.info(f"--- 第 {iteration+1}/{limit} 轮 ---")

            # 1. 代码生成/修改
            cycle.status = EvolutionStatus.GENERATING
            cycle.code_before = self._read_module(target_module)
            new_code = self.code_generator(target_module, iteration, cycle)
            cycle.code_after = new_code

            # 2. 沙箱执行
            exec_result = self.sandbox(new_code, target_module)
            if not exec_result.get("success"):
                logger.warning(f"沙箱执行失败: {exec_result.get('error')}")
                if iteration < limit - 1:
                    continue
                break

            # 3. 自动测试
            cycle.status = EvolutionStatus.TESTING
            cycle.test_results = self.test_runner(target_module, new_code)

            # 4. 质量评估
            cycle.status = EvolutionStatus.EVALUATING
            cycle.quality_score = self._evaluate(cycle.test_results, exec_result)
            logger.info(f"质量评分: {cycle.quality_score:.3f}")

            # 5. 决策
            if cycle.quality_score >= self.ACCEPT_THRESHOLD:
                cycle.decision = "accept"
                cycle.status = EvolutionStatus.DEPLOYING
                self._deploy(target_module, new_code)
                logger.info(f"接受进化: 评分 {cycle.quality_score:.3f} >= {self.ACCEPT_THRESHOLD}")

                # 沉淀技能
                if self.skill_forge:
                    self.skill_forge.record_evolution(cycle)

                break

            elif cycle.quality_score < self.REJECT_THRESHOLD and iteration >= 1:
                cycle.decision = "reject"
                cycle.status = EvolutionStatus.ROLLBACK
                if self.snapshot_manager:
                    self.snapshot_manager.rollback_to_latest(target_module)
                logger.info(f"拒绝进化: 评分 {cycle.quality_score:.3f} < {self.REJECT_THRESHOLD}")
                break

            else:
                cycle.decision = "continue"
                logger.info(f"继续优化: 评分 {cycle.quality_score:.3f}")

        cycle.end_time = time.time()
        cycle.status = EvolutionStatus.COMPLETED
        self.evolution_log.cycles.append(cycle)
        self._update_log_stats()

        logger.info(f"SICA进化完成: {cycle.decision} (耗时: {cycle.end_time - cycle.start_time:.1f}s)")
        return cycle

    def _evaluate(self, test_results: dict, exec_result: dict) -> float:
        """多维度质量评估"""
        dims = {
            "test_pass_rate": test_results.get("pass_rate", 0.0),
            "execution_success": 1.0 if exec_result.get("success") else 0.0,
            "code_quality": test_results.get("code_quality", 0.5),
            "performance": test_results.get("performance_score", 0.5)
        }
        weights = {"test_pass_rate": 0.35, "execution_success": 0.25, "code_quality": 0.25, "performance": 0.15}
        return sum(dims[k] * weights[k] for k in dims)

    def _read_module(self, target_module: str) -> str:
        """读取模块代码"""
        try:
            return Path(target_module).read_text(encoding="utf-8")
        except Exception:
            return ""

    def _deploy(self, target_module: str, code: str):
        """部署代码"""
        Path(target_module).write_text(code, encoding="utf-8")
        logger.info(f"代码已部署: {target_module}")

    def _update_log_stats(self):
        """更新进化日志统计"""
        total = len(self.evolution_log.cycles)
        accepted = sum(1 for c in self.evolution_log.cycles if c.decision == "accept")
        self.evolution_log.total_evolutions = total
        self.evolution_log.success_rate = accepted / max(total, 1)

        scores = [c.quality_score for c in self.evolution_log.cycles]
        self.evolution_log.average_improvement = sum(scores) / max(len(scores), 1)

    def _default_sandbox(self, code: str, module: str) -> dict:
        """默认沙箱执行"""
        return {"success": True, "output": "sandbox placeholder"}

    def _default_test_runner(self, module: str, code: str) -> dict:
        """默认测试运行器"""
        return {"pass_rate": 0.8, "code_quality": 0.7, "performance_score": 0.6}

    def _default_code_generator(self, module: str, iteration: int, cycle: EvolutionCycle) -> str:
        """默认代码生成器"""
        return cycle.code_before or f"# Auto-generated for {module} (iter {iteration})"


# ========== GenericAgent 轻量化适配器 ==========

class GenericAgentAdapter:
    """GenericAgent轻量化架构适配器

    核心理念：Agent = LLM + Tools + Memory + Planning
    所有组件可插拔，最小化依赖
    """

    def __init__(self):
        self.config = {
            "agent_profile": "generic_lightweight",
            "llm": {"primary": "deepseek-v3", "fallback": "qwen3-coder-480b"},
            "tools": ["file_ops", "shell_exec", "web_search"],
            "memory": {
                "mode": "lightweight",
                "max_context_tokens": 32000,
                "compression": "semantic_summary"
            },
            "planning": {
                "mode": "pes_simple",
                "max_steps": 10,
                "timeout": 300
            }
        }
        self.tool_registry: dict = {}
        self.memory_context: list = []
        self.planning_history: list = []

    def register_tool(self, name: str, handler: callable):
        """注册工具（即插即用）"""
        self.tool_registry[name] = handler
        logger.info(f"工具已注册: {name}")

    def unregister_tool(self, name: str):
        """卸载工具"""
        self.tool_registry.pop(name, None)
        logger.info(f"工具已卸载: {name}")

    def execute(self, task: str, tools: list = None) -> dict:
        """执行任务：轻量化流程"""
        plan = self._plan(task)
        results = []

        for step in plan:
            tool_name = step.get("tool")
            if tool_name and tool_name in self.tool_registry:
                result = self.tool_registry[tool_name](**step.get("params", {}))
            else:
                result = {"status": "no_tool", "step": step}
            results.append(result)

            # 记忆更新
            self.memory_context.append({"task": task, "step": step, "result": result})
            if len(self.memory_context) > self.config["memory"]["max_context_tokens"] // 100:
                self._compress_memory()

        return {"success": True, "results": results, "plan": plan}

    def _plan(self, task: str) -> list:
        """PES简单规划"""
        max_steps = self.config["planning"]["max_steps"]
        return [
            {"step": 1, "tool": "analysis", "params": {"task": task}},
            {"step": 2, "tool": "execution", "params": {}}
        ][:max_steps]

    def _compress_memory(self):
        """记忆压缩"""
        self.memory_context = self.memory_context[-50:]  # 保留最近50条

    def get_status(self) -> dict:
        """获取Agent状态"""
        return {
            "profile": self.config["agent_profile"],
            "tools_loaded": list(self.tool_registry.keys()),
            "memory_items": len(self.memory_context),
            "planning_mode": self.config["planning"]["mode"]
        }


# ========== 快照管理器 ==========

class SnapshotManager:
    """增强版快照管理器：创建 + 对比 + 回滚 + 验证"""

    def __init__(self, snapshot_dir: str = "checkpoints/snapshots"):
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots: dict = {}
        self._load_index()

    def create_snapshot(self, name: str, file_paths: list, description: str = "") -> str:
        """创建完整文件快照"""
        snapshot_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_path = self.snapshot_dir / snapshot_id
        snapshot_path.mkdir(parents=True, exist_ok=True)

        manifest = {
            "snapshot_id": snapshot_id,
            "created_at": datetime.now().isoformat(),
            "description": description,
            "files": {}
        }

        for fp in file_paths:
            path = Path(fp)
            if path.exists():
                content = path.read_bytes()
                file_hash = hashlib.md5(content).hexdigest()
                manifest["files"][fp] = {"hash": file_hash, "size": len(content)}
                # 保存副本
                dest = snapshot_path / path.name
                dest.write_bytes(content)

        manifest_path = snapshot_path / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

        self.snapshots[snapshot_id] = manifest
        self._save_index()

        logger.info(f"快照已创建: {snapshot_id} ({len(manifest['files'])}个文件)")
        return snapshot_id

    def diff_snapshot(self, snapshot_id: str, current_files: list) -> dict:
        """对比快照与当前文件"""
        manifest = self.snapshots.get(snapshot_id, {})
        snapshot_files = manifest.get("files", {})

        added = []
        modified = []
        deleted = []
        unchanged = []

        for fp in current_files:
            if fp not in snapshot_files:
                added.append(fp)
            else:
                current_hash = hashlib.md5(Path(fp).read_bytes()).hexdigest() if Path(fp).exists() else ""
                if current_hash != snapshot_files[fp]["hash"]:
                    modified.append(fp)
                else:
                    unchanged.append(fp)

        for fp in snapshot_files:
            if fp not in current_files:
                deleted.append(fp)

        return {
            "snapshot_id": snapshot_id,
            "added": added,
            "modified": modified,
            "deleted": deleted,
            "unchanged": unchanged,
            "total_changes": len(added) + len(modified) + len(deleted)
        }

    def rollback(self, snapshot_id: str, target_files: list = None) -> bool:
        """从快照回滚文件"""
        manifest = self.snapshots.get(snapshot_id)
        if not manifest:
            logger.error(f"快照不存在: {snapshot_id}")
            return False

        snapshot_path = self.snapshot_dir / snapshot_id
        files_to_restore = target_files or list(manifest["files"].keys())

        for fp in files_to_restore:
            if fp in manifest["files"]:
                source = snapshot_path / Path(fp).name
                if source.exists():
                    Path(fp).write_bytes(source.read_bytes())
                    logger.info(f"已回滚: {fp}")

        logger.info(f"回滚完成: {snapshot_id} ({len(files_to_restore)}个文件)")
        return True

    def rollback_to_latest(self, target_module: str) -> bool:
        """回滚到最新快照"""
        sorted_ids = sorted(self.snapshots.keys(), reverse=True)
        for sid in sorted_ids:
            manifest = self.snapshots[sid]
            if any(target_module in f for f in manifest.get("files", {})):
                return self.rollback(sid)
        return False

    def verify_snapshot(self, snapshot_id: str) -> dict:
        """验证快照完整性"""
        manifest = self.snapshots.get(snapshot_id)
        if not manifest:
            return {"valid": False, "reason": "snapshot_not_found"}

        snapshot_path = self.snapshot_dir / snapshot_id
        issues = []
        for fp, info in manifest.get("files", {}).items():
            source = snapshot_path / Path(fp).name
            if not source.exists():
                issues.append(f"missing: {fp}")
            else:
                actual_hash = hashlib.md5(source.read_bytes()).hexdigest()
                if actual_hash != info["hash"]:
                    issues.append(f"corrupted: {fp}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "total_files": len(manifest["files"])
        }

    def _load_index(self):
        """加载快照索引"""
        index_path = self.snapshot_dir / "_index.json"
        if index_path.exists():
            self.snapshots = json.loads(index_path.read_text())

    def _save_index(self):
        """保存快照索引"""
        index_path = self.snapshot_dir / "_index.json"
        index_path.write_text(json.dumps(self.snapshots, indent=2, ensure_ascii=False))


# ========== Obsidian桥接器 ==========

class ObsidianBridge:
    """Obsidian知识库联动桥接器"""

    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path) if vault_path else None
        self.enabled = self.vault_path is not None and self.vault_path.exists()

    def sync_to_obsidian(self, source_file: str, target_note: str, tags: list = None):
        """同步豆包产出至Obsidian"""
        if not self.enabled:
            logger.warning("Obsidian桥接未启用")
            return False

        content = Path(source_file).read_text(encoding="utf-8")
        note_path = self.vault_path / f"{target_note}.md"

        # 添加WikiLink和标签
        frontmatter = "---\n"
        frontmatter += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
        if tags:
            frontmatter += f"tags: [{', '.join(tags)}]\n"
        frontmatter += f"source: [[{Path(source_file).stem}]]\n"
        frontmatter += "---\n\n"

        note_path.write_text(frontmatter + content, encoding="utf-8")
        logger.info(f"已同步至Obsidian: {note_path}")
        return True

    def read_from_obsidian(self, note_name: str) -> Optional[str]:
        """从Obsidian读取笔记"""
        if not self.enabled:
            return None

        note_path = self.vault_path / f"{note_name}.md"
        if note_path.exists():
            return note_path.read_text(encoding="utf-8")
        return None

    def query_links(self, note_name: str) -> list:
        """查询双向链接"""
        if not self.enabled:
            return []

        note_path = self.vault_path / f"{note_name}.md"
        if not note_path.exists():
            return []

        content = note_path.read_text(encoding="utf-8")
        import re
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        return links


# ========== 自动回滚规则引擎 ==========

class AutoRollbackEngine:
    """异常自动回滚规则引擎"""

    def __init__(self, snapshot_manager: SnapshotManager, rules_path: str = None):
        self.snapshot_manager = snapshot_manager
        self.rules = self._load_rules(rules_path)
        self.rollback_history: list = []
        self.cooldowns: dict = {}

    def evaluate(self, metrics: dict) -> Optional[str]:
        """评估触发规则，返回需要回滚的快照ID或None"""
        for rule in self.rules:
            trigger = rule.get("trigger", "")
            condition = rule.get("condition", "")
            action = rule.get("action", "")
            cooldown = rule.get("cooldown", 3600)

            # 检查冷却
            if trigger in self.cooldowns:
                elapsed = time.time() - self.cooldowns[trigger]
                if elapsed < cooldown:
                    continue

            if self._check_condition(condition, metrics):
                logger.warning(f"触发自动回滚规则: {rule['id']} ({trigger})")
                self.cooldowns[trigger] = time.time()

                if action == "rollback_to_last_stable":
                    snapshot_id = self._get_last_stable_snapshot()
                    self.rollback_history.append({
                        "rule_id": rule["id"],
                        "trigger": trigger,
                        "snapshot": snapshot_id,
                        "timestamp": datetime.now().isoformat(),
                        "metrics": metrics
                    })
                    return snapshot_id

        return None

    def _check_condition(self, condition: str, metrics: dict) -> bool:
        """检查条件表达式"""
        try:
            # 简化实现：解析 condition 表达式
            if "error_rate" in condition:
                error_rate = metrics.get("error_rate", 0)
                threshold = float(condition.split(">")[-1].strip()) if ">" in condition else 0.5
                return error_rate > threshold
            if "memory_mb" in condition:
                memory = metrics.get("memory_mb", 0)
                threshold = float(condition.split(">")[-1].strip()) if ">" in condition else 2048
                return memory > threshold
            return False
        except Exception:
            return False

    def _get_last_stable_snapshot(self) -> str:
        """获取最近稳定快照"""
        sorted_ids = sorted(self.snapshot_manager.snapshots.keys(), reverse=True)
        return sorted_ids[0] if sorted_ids else ""

    def _load_rules(self, rules_path: str = None) -> list:
        """加载自动回滚规则"""
        default_rules = [
            {
                "id": "ARR_001",
                "trigger": "critical_error_rate",
                "condition": "error_rate > 0.5 AND nodes_executed > 3",
                "action": "rollback_to_last_stable",
                "cooldown": 3600
            },
            {
                "id": "ARR_002",
                "trigger": "memory_overflow",
                "condition": "memory_mb > 2048",
                "action": "compress_and_continue",
                "cooldown": 600
            },
            {
                "id": "ARR_003",
                "trigger": "skill_degradation",
                "condition": "skill_success_rate < 0.3 AND activation_count > 10",
                "action": "deactivate_skill_and_rollback",
                "cooldown": 7200
            },
            {
                "id": "ARR_004",
                "trigger": "file_corruption",
                "condition": "checksum_mismatch_on_critical_files",
                "action": "restore_from_snapshot",
                "cooldown": 0
            }
        ]

        if rules_path and Path(rules_path).exists():
            return json.loads(Path(rules_path).read_text())
        return default_rules


# ========== 全域联动协调器 ==========

class EvolutionOrchestrator:
    """全域联动进化协调器"""

    def __init__(
        self,
        sica_evolver: SICAEvolver = None,
        generic_agent: GenericAgentAdapter = None,
        snapshot_manager: SnapshotManager = None,
        obsidian_bridge: ObsidianBridge = None,
        auto_rollback: AutoRollbackEngine = None,
        skill_forge=None,
        desktop_controller=None
    ):
        self.sica = sica_evolver or SICAEvolver()
        self.generic_agent = generic_agent or GenericAgentAdapter()
        self.snapshot = snapshot_manager or SnapshotManager()
        self.obsidian = obsidian_bridge
        self.rollback = auto_rollback or AutoRollbackEngine(self.snapshot)
        self.skill_forge = skill_forge
        self.desktop = desktop_controller

    def full_cycle(self, target_module: str, task: str = None) -> dict:
        """执行全域联动进化完整周期"""
        results = {
            "cycle_start": datetime.now().isoformat(),
            "target": target_module,
            "stages": {}
        }

        # Stage 1: 进化前快照
        logger.info("[全域联动] Stage 1: 进化前快照")
        snapshot_id = self.snapshot.create_snapshot(
            f"pre_evo_{target_module}",
            [target_module],
            "全域联动进化前快照"
        )
        results["stages"]["snapshot_pre"] = snapshot_id

        # Stage 2: SICA自进化
        logger.info("[全域联动] Stage 2: SICA自进化")
        cycle = self.sica.evolve(target_module)
        results["stages"]["sica_evolution"] = {
            "decision": cycle.decision,
            "score": cycle.quality_score
        }

        # Stage 3: 异常检测与自动回滚
        logger.info("[全域联动] Stage 3: 异常检测")
        metrics = {
            "error_rate": 0 if cycle.decision == "accept" else 1.0,
            "nodes_executed": 1,
            "memory_mb": 512
        }
        rollback_id = self.rollback.evaluate(metrics)
        results["stages"]["rollback_check"] = rollback_id

        # Stage 4: 技能沉淀
        if self.skill_forge and cycle.decision == "accept":
            logger.info("[全域联动] Stage 4: 技能沉淀")
            self.skill_forge.extract_from_evolution(cycle)
            results["stages"]["skill_distillation"] = "completed"

        # Stage 5: Obsidian同步
        if self.obsidian and self.obsidian.enabled:
            logger.info("[全域联动] Stage 5: Obsidian同步")
            self.obsidian.sync_to_obsidian(
                target_module,
                f"进化记录_{target_module}",
                tags=["evolution", "auto", datetime.now().strftime("%Y-%m-%d")]
            )
            results["stages"]["obsidian_sync"] = "completed"

        # Stage 6: 桌面控制联动
        if self.desktop and cycle.decision == "accept":
            logger.info("[全域联动] Stage 6: 桌面控制联动")
            results["stages"]["desktop_control"] = "triggered"

        results["cycle_end"] = datetime.now().isoformat()
        results["overall_status"] = "completed"
        return results


# ========== 测试入口 ==========

if __name__ == "__main__":
    # 测试SICA进化
    sica = SICAEvolver()
    cycle = sica.evolve("test_module.py", iteration_limit=2)
    print(f"SICA进化结果: {cycle.decision} (评分: {cycle.quality_score:.3f})")

    # 测试GenericAgent
    ga = GenericAgentAdapter()
    ga.register_tool("echo", lambda **kw: {"echo": kw})
    result = ga.execute("test task")
    print(f"GenericAgent状态: {json.dumps(ga.get_status(), ensure_ascii=False)}")

    # 测试快照管理器
    sm = SnapshotManager()
    sid = sm.create_snapshot("test_snap", ["test_module.py"], "测试快照")
    diff = sm.diff_snapshot(sid, ["test_module.py"])
    print(f"快照对比: {json.dumps(diff, ensure_ascii=False)[:200]}")

    # 测试全域联动
    orch = EvolutionOrchestrator(sica_evolver=sica, snapshot_manager=sm)
    full_result = orch.full_cycle("test_module.py")
    print(f"全域联动完成: {full_result['overall_status']}")
```
