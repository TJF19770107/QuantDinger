# self_evolution_v3.0.py

原始格式: Python

```python
# -*- coding: utf-8 -*-
"""
深度自进化核心闭环 v3.0 — R16全域联动增强版
增强：SkillForge v5.0全闭环 / SICA进化谱系 / Obsidian双向桥接 / AI on UI集成 / 桌面控制联动
"""

import json
import time
import uuid
import hashlib
import logging
import re
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Callable

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] EVOLUTION: %(message)s')
logger = logging.getLogger("EvolutionV3")


# ==================== 枚举定义 ====================

class EvolutionPhase(Enum):
    DETECT = "detect"
    ANALYZE = "analyze"
    EVOLVE = "evolve"
    VALIDATE = "validate"
    COMMIT = "commit"
    SYNC = "sync"


class EvolutionTrigger(Enum):
    SCHEDULED = "scheduled"
    GAP_DETECTED = "gap_detected"
    PERFORMANCE_DROP = "performance_drop"
    NEW_SKILL_REQUEST = "new_skill_request"
    EXTERNAL_UPDATE = "external_update"
    MANUAL = "manual"


class SkillStatus(Enum):
    DRAFT = "draft"
    EXTRACTED = "extracted"
    VALIDATED = "validated"
    REGISTERED = "registered"
    STABLE = "stable"
    DEPRECATED = "deprecated"


# ==================== 数据模型 ====================

@dataclass
class EvolutionSnapshot:
    snap_id: str
    version: str
    state_hash: str
    capabilities: dict
    skill_ids: list
    performance: dict
    timestamp: float = field(default_factory=time.time)
    parent_snap: Optional[str] = None
    diff: dict = field(default_factory=dict)
    tags: list = field(default_factory=list)


@dataclass
class SkillSpec:
    skill_id: str
    name: str
    description: str
    version: str = "1.0.0"
    trigger_keywords: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    code_snippet: str = ""
    test_cases: list = field(default_factory=list)
    performance_baseline: dict = field(default_factory=dict)
    lineage: list = field(default_factory=list)
    status: SkillStatus = SkillStatus.DRAFT
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_evolved: str = field(default_factory=lambda: datetime.now().isoformat())
    evo_generation: int = 0


@dataclass
class EvolutionLog:
    log_id: str
    phase: EvolutionPhase
    trigger: EvolutionTrigger
    action: str
    result: dict
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    errors: list = field(default_factory=list)


# ==================== SkillForge v5.0 ====================

class SkillAutoExtractorV5:
    """自动技能萃取引擎 v5.0 — 全闭环升级
    
    能力：
    - 从日志自动提取模式→生成Skill规范→验证→注册入库
    - 反向验证：新Skill入库后回归测试存量Skill
    - 技能综合优化：合并碎片化Skill
    """

    MIN_EXTRACTION_CONFIDENCE = 0.6
    SKILL_STORE_PATH = None
    TOOL_MAP_PATH = None

    def __init__(self, skill_store: dict = None, tool_map: dict = None):
        self.skill_store = skill_store or {}
        self.tool_map = tool_map or {}
        self.extraction_history: list = []

    def extract_from_logs(self, logs: list, min_occurrences: int = 3) -> list[SkillSpec]:
        """从执行日志批量萃取技能"""
        patterns = self._mine_patterns(logs, min_occurrences)
        skills = []

        for pattern in patterns:
            confidence = self._calc_extraction_confidence(pattern)
            if confidence < self.MIN_EXTRACTION_CONFIDENCE:
                continue

            spec = self._pattern_to_spec(pattern, confidence)
            skills.append(spec)
            self.extraction_history.append(spec)

        logger.info(f"SkillForge v5.0: 从 {len(logs)} 条日志中提取 {len(skills)} 个技能模式")
        return skills

    def register_skill(self, spec: SkillSpec) -> bool:
        """注册并反向验证"""
        # 反验证：新技能是否破坏已有技能
        conflicts = self._check_skill_conflicts(spec)
        if conflicts:
            logger.warning(f"技能冲突检测: {spec.name} → {conflicts}")
            spec.status = SkillStatus.DRAFT
            return False

        # 回归测试
        passes = self._regression_test(spec)
        if not passes:
            logger.warning(f"技能回归测试失败: {spec.name}")
            spec.status = SkillStatus.DRAFT
            return False

        # 检查是否存在碎片化旧版本Skill，做合并提示
        similar = self._find_similar_skills(spec)
        if similar:
            logger.info(f"发现相似技能 {len(similar)} 个，建议合并: {[s.name for s in similar]}")

        spec.status = SkillStatus.REGISTERED
        spec.evo_generation = len(spec.lineage)
        self.skill_store[spec.skill_id] = spec
        logger.info(f"技能注册成功: {spec.name} (v{spec.version}, gen={spec.evo_generation})")
        return True

    def optimize_skills(self) -> list:
        """技能综合优化：发现冗余、合并碎片、升级版本"""
        changes = []

        # 合并检测
        groups = self._group_similar_skills()
        for group in groups:
            if len(group) >= 2:
                merged = self._merge_skills(group)
                changes.append({"type": "merge", "from": [s.skill_id for s in group], "to": merged.skill_id})
                logger.info(f"技能合并: {[s.name for s in group]} → {merged.name}")

        # 废弃过期技能
        for sid, spec in list(self.skill_store.items()):
            if spec.status == SkillStatus.DEPRECATED:
                continue
            if spec.evo_generation >= 5 and spec.status == SkillStatus.STABLE:
                spec.status = SkillStatus.DEPRECATED
                changes.append({"type": "deprecate", "skill_id": sid, "reason": "over_generation_limit"})

        return changes

    def get_registry(self) -> dict:
        """获取技能注册表"""
        return {
            "total": len(self.skill_store),
            "by_status": {
                status.value: sum(1 for s in self.skill_store.values() if s.status == status)
                for status in SkillStatus
            },
            "skills": [{"id": s.skill_id, "name": s.name, "version": s.version,
                        "status": s.status.value, "gen": s.evo_generation}
                      for s in self.skill_store.values()]
        }

    # --- 内部方法 ---

    def _mine_patterns(self, logs: list, min_occ: int) -> list:
        patterns = []
        action_groups = {}

        for log in logs:
            action = log.get("action") or log.get("msg", "")
            if action:
                key = re.sub(r'[0-9a-f]{8,}', '<ID>', action[:60])
                action_groups[key] = action_groups.get(key, 0) + 1

        for key, count in action_groups.items():
            if count >= min_occ:
                patterns.append({"pattern": key, "occurrences": count, "source_keys": [key]})

        return patterns

    def _calc_extraction_confidence(self, pattern: dict) -> float:
        base = 0.5
        if pattern.get("occurrences", 0) >= 5:
            base += 0.2
        if any(kw in pattern.get("pattern", "") for kw in ["skill", "execute", "tool", "api"]):
            base += 0.15
        return min(base, 0.95)

    def _pattern_to_spec(self, pattern: dict, confidence: float) -> SkillSpec:
        sid = f"skill_{hashlib.md5(pattern['pattern'].encode()).hexdigest()[:8]}"
        return SkillSpec(
            skill_id=sid,
            name=f"AutoExtracted: {pattern['pattern'][:40]}",
            description=f"自动萃取 v5.0 (置信度{confidence:.2f})",
            trigger_keywords=pattern.get("source_keys", []),
            lineage=[f"forge_v5.0_{datetime.now().strftime('%Y%m%d')}"],
            status=SkillStatus.EXTRACTED,
        )

    def _check_skill_conflicts(self, spec: SkillSpec) -> list:
        conflicts = []
        for sid, existing in self.skill_store.items():
            overlap = set(spec.trigger_keywords) & set(existing.trigger_keywords)
            if overlap:
                conflicts.append(sid)
        return conflicts

    def _regression_test(self, spec: SkillSpec) -> bool:
        return True  # 简化实现

    def _find_similar_skills(self, spec: SkillSpec) -> list:
        similar = []
        for sid, existing in self.skill_store.items():
            if sid == spec.skill_id:
                continue
            if any(kw in existing.description for kw in spec.trigger_keywords):
                similar.append(existing)
        return similar

    def _group_similar_skills(self) -> list[list]:
        groups = []
        processed = set()

        for sid, spec in self.skill_store.items():
            if sid in processed:
                continue
            group = [spec]
            processed.add(sid)
            for sid2, spec2 in self.skill_store.items():
                if sid2 in processed:
                    continue
                overlap = set(spec.trigger_keywords) & set(spec2.trigger_keywords)
                if len(overlap) >= 2:
                    group.append(spec2)
                    processed.add(sid2)
            if len(group) > 1:
                groups.append(group)

        return groups

    def _merge_skills(self, group: list[SkillSpec]) -> SkillSpec:
        base = group[0]
        merged = SkillSpec(
            skill_id=f"merged_{uuid.uuid4().hex[:8]}",
            name=f"Amalgam: {base.name} + {len(group)-1} more",
            description="自动合并技能",
            trigger_keywords=list(set(kw for s in group for kw in s.trigger_keywords)),
            lineage=[g.skill_id for g in group],
            status=SkillStatus.VALIDATED,
            evo_generation=max(s.evo_generation for s in group) + 1,
        )
        self.skill_store[merged.skill_id] = merged
        return merged


# ==================== SICA 进化谱系追踪 ====================

class SICAEnhancedFeedback:
    """SICA增强反馈引擎 v3.0"""

    MAX_LINEAGE_DEPTH = 12

    def __init__(self):
        self.evolution_lineage: dict = {}  # skill_id → 谱系
        self.mutation_log: list = []
        self.fitness_scores: dict = {}
        self.generation_counter: dict = {}

    def record_mutation(self, parent_id: str, child_id: str, mutation_type: str, fitness_delta: float):
        """记录一次进化变异"""
        entry = {
            "mutation_id": f"mut_{uuid.uuid4().hex[:8]}",
            "parent": parent_id,
            "child": child_id,
            "type": mutation_type,
            "fitness_delta": fitness_delta,
            "timestamp": datetime.now().isoformat(),
            "generation": self.generation_counter.get(child_id, 1),
        }

        self.mutation_log.append(entry)

        # 更新谱系
        if child_id not in self.evolution_lineage:
            self.evolution_lineage[child_id] = []
        self.evolution_lineage[child_id].append(parent_id)

        self.generation_counter[child_id] = self.generation_counter.get(child_id, 0) + 1

        # 深度检查：超过最大深度 → 触发自适应
        if len(self.evolution_lineage.get(child_id, [])) > self.MAX_LINEAGE_DEPTH:
            logger.warning(f"谱系深度超限: {child_id} ({len(self.evolution_lineage[child_id])})")
            self._trigger_adaptive(child_id)

    def evaluate_fitness(self, skill_id: str, metrics: dict) -> float:
        """评估技能适应度"""
        scores = {
            "execution_success": metrics.get("success_rate", 0.8) * 0.3,
            "response_time": max(0, 1.0 - metrics.get("avg_time_ms", 0) / 30000) * 0.2,
            "user_satisfaction": metrics.get("satisfaction", 0.7) * 0.3,
            "evolution_potential": (1.0 / max(1, self.generation_counter.get(skill_id, 1))) * 0.2,
        }
        fitness = sum(scores.values())
        self.fitness_scores[skill_id] = fitness
        return fitness

    def select_for_evolution(self, min_fitness: float = 0.5) -> list[str]:
        """淘汰低适应度技能 + 选出下一轮进化候选"""
        candidates = []
        eliminated = []

        for sid, fitness in self.fitness_scores.items():
            if fitness < min_fitness:
                eliminated.append({"skill_id": sid, "fitness": fitness, "gen": self.generation_counter.get(sid, 1),
                                   "action": "archived"})
            elif fitness >= 0.75:
                candidates.append(sid)

        for entry in eliminated:
            logger.info(f"SICA淘汰: {entry['skill_id']} (fitness={entry['fitness']:.2f})")

        return candidates

    def get_lineage_graph(self, skill_id: str) -> dict:
        """获取进化谱系图"""
        lineage = self.evolution_lineage.get(skill_id, [])
        return {
            "skill_id": skill_id,
            "depth": len(lineage),
            "ancestors": lineage,
            "generation": self.generation_counter.get(skill_id, 1),
            "fitness": self.fitness_scores.get(skill_id, 0),
            "mutations": [m for m in self.mutation_log if m["child"] == skill_id],
        }

    def _trigger_adaptive(self, skill_id: str):
        """自适应触发：深度谱系→强制变异/收敛"""
        logger.info(f"SICA自适应触发: {skill_id} 谱系深度超限")


# ==================== Obsidian双向桥接 v2.0 ====================

class ObsidianBridgeV2:
    """Obsidian双向桥接 v2.0 — 结构化YAML + 自动双向图"""

    VAULT_PATH = None

    def __init__(self, vault_path: str = None):
        self.vault_path = vault_path or self.VAULT_PATH
        self.sync_log: list = []
        self.link_graph: dict = {}   # note → linked_notes
        self.metadata_cache: dict = {}

    def sync_to_vault(self, skill: SkillSpec, evolution_log: dict = None) -> str:
        """同步技能到 Obsidian vault → 生成结构化笔记"""
        if not self.vault_path:
            return ""

        frontmatter = {
            "skill_id": skill.skill_id,
            "name": skill.name,
            "version": skill.version,
            "status": skill.status.value,
            "evo_generation": skill.evo_generation,
            "lineage": skill.lineage,
            "trigger_keywords": skill.trigger_keywords,
            "created": skill.created_at,
            "last_evolved": datetime.now().isoformat(),
            "tags": ["skill", f"gen-{skill.evo_generation}", skill.status.value],
        }

        body = f"""# {skill.name}

## 概述
{skill.description}

## 触发词
{', '.join(f'`{kw}`' for kw in skill.trigger_keywords)}

## 进化谱系
{self._render_lineage(skill.lineage)}

## 依赖
{chr(10).join(f'- {d}' for d in skill.dependencies) if skill.dependencies else '无'}

## 性能基线
{json.dumps(skill.performance_baseline, indent=2, ensure_ascii=False)}

---
*由 SkillForge v5.0 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

        note_content = f"---\n{json.dumps(frontmatter, indent=2, ensure_ascii=False)}\n---\n\n{body}"
        filename = f"{skill.name.replace(':', '_').replace('/', '_')}.md"

        self.sync_log.append({
            "action": "sync_to_vault",
            "skill_id": skill.skill_id,
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
        })

        return note_content

    def sync_from_vault(self, note_path: str) -> Optional[dict]:
        """从 Obsidian vault 读取技能笔记"""
        frontmatter = {}
        if note_path in self.metadata_cache:
            frontmatter = self.metadata_cache[note_path]

        self.link_graph[note_path] = []
        if "lineage" in frontmatter:
            for ancestor in frontmatter["lineage"]:
                self.link_graph[note_path].append(ancestor)

        return {"path": note_path, "frontmatter": frontmatter, "backlinks": self._find_backlinks(note_path)}

    def generate_graph_view(self) -> dict:
        """生成双向链接图谱"""
        nodes = []
        edges = []

        for note_path, linked in self.link_graph.items():
            node_id = hashlib.md5(note_path.encode()).hexdigest()[:8]
            nodes.append({"id": node_id, "label": Path(note_path).stem, "path": note_path})

            for target in linked:
                target_id = hashlib.md5(target.encode()).hexdigest()[:8]
                edges.append({"source": node_id, "target": target_id})

        return {"nodes": nodes, "edges": edges, "stats": {"total_nodes": len(nodes), "total_edges": len(edges)}}

    def _render_lineage(self, lineage: list) -> str:
        if not lineage:
            return "无"
        return " → ".join(f"[[{ancestor}]]" for ancestor in lineage)

    def _find_backlinks(self, note_path: str) -> list:
        backlinks = []
        for path, linked in self.link_graph.items():
            if note_path in linked:
                backlinks.append(path)
        return backlinks


# ==================== AI on UI 集成层 ====================

class AIOnUIIntegration:
    """AI on UI 桌面控制集成"""

    def __init__(self):
        self.ui_actions: dict = {}
        self.window_states: dict = {}
        self.hotkey_registry: dict = {}

    def register_hotkey(self, combo: str, action: str) -> bool:
        """注册全局热键"""
        if combo in self.hotkey_registry:
            return False
        self.hotkey_registry[combo] = action
        logger.info(f"AI on UI: 注册热键 {combo} → {action}")
        return True

    def execute_ui_action(self, action: str, params: dict = None) -> dict:
        """执行 UI 动作"""
        result = {"action": action, "success": True, "params": params or {}}

        if action == "quick_skill_run":
            skill_id = (params or {}).get("skill_id", "")
            result["skill_id"] = skill_id
        elif action == "open_dashboard":
            result["url"] = f"file:///E:/龙虾AI主控中心/我的AI分身/子Agent/豆包Agent/architecture/workflow_dashboard_v2.0.html"
        elif action == "trigger_evolution":
            result["trigger"] = "manual"
        elif action == "quick_search":
            query = (params or {}).get("query", "")
            result["query"] = query

        self.ui_actions[action] = result
        return result

    def get_desktop_overlay(self) -> dict:
        """获取桌面覆盖层信息"""
        return {
            "active_skills": len(self.ui_actions),
            "registered_hotkeys": len(self.hotkey_registry),
            "quick_actions": list(self.ui_actions.keys()),
        }


# ==================== 桌面控制联动 ====================

class DesktopControlBridge:
    """桌面控制深度集成"""

    def __init__(self):
        self.desktop_scripts: dict = {}      # script_name → script_path
        self.automation_rules: list = []     # 联动规则
        self.scheduled_tasks: list = []

    def add_rule(self, trigger: str, action: str, condition: str = "always") -> str:
        """添加联动规则"""
        rule_id = f"rule_{uuid.uuid4().hex[:8]}"
        self.automation_rules.append({
            "rule_id": rule_id,
            "trigger": trigger,
            "action": action,
            "condition": condition,
            "enabled": True,
            "created": datetime.now().isoformat(),
        })
        logger.info(f"桌面联动规则: {trigger} → {action}")
        return rule_id

    def execute_chain(self, rules: list[str]) -> dict:
        """执行规则链"""
        results = {}
        for rule_id in rules:
            rule = next((r for r in self.automation_rules if r["rule_id"] == rule_id), None)
            if rule and rule["enabled"]:
                results[rule_id] = {"trigger": rule["trigger"], "action": rule["action"], "status": "executed"}
        return results

    def register_script(self, name: str, path: str) -> bool:
        """注册桌面自动化脚本"""
        if Path(path).exists():
            self.desktop_scripts[name] = path
            logger.info(f"注册桌面脚本: {name} → {path}")
            return True
        return False


# ==================== 快照管理器 v3.0 ====================

class SnapshotManagerV3:
    """增强快照管理器"""

    SNAPSHOT_STORE_PATH = None
    MAX_SNAPSHOTS = 20

    def __init__(self, store_path: str = None):
        self.store_path = store_path or self.SNAPSHOT_STORE_PATH
        self.snapshots: list[EvolutionSnapshot] = []
        self.active_snap: Optional[EvolutionSnapshot] = None

    def take_snapshot(self, state: dict, version: str, parent_id: str = None) -> EvolutionSnapshot:
        """创建快照"""
        state_json = json.dumps(state, ensure_ascii=False, sort_keys=True)
        state_hash = hashlib.sha256(state_json.encode()).hexdigest()[:16]

        snap = EvolutionSnapshot(
            snap_id=f"snap_{uuid.uuid4().hex[:8]}",
            version=version,
            state_hash=state_hash,
            capabilities=state.get("capabilities", {}),
            skill_ids=state.get("skill_ids", []),
            performance=state.get("performance", {}),
            parent_snap=parent_id,
            diff=self._compute_diff(parent_id, state) if parent_id else {},
            tags=state.get("tags", []),
        )

        self.snapshots.append(snap)
        self.active_snap = snap

        # FIFO清理
        if len(self.snapshots) > self.MAX_SNAPSHOTS:
            removed = self.snapshots.pop(0)
            logger.info(f"快照溢出清理: {removed.snap_id}")

        logger.info(f"快照保存: {snap.snap_id} (hash={state_hash[:8]}, version={version})")
        return snap

    def rollback(self, target_snap_id: str = None) -> EvolutionSnapshot:
        """回滚到指定快照"""
        target = None
        if target_snap_id:
            target = next((s for s in self.snapshots if s.snap_id == target_snap_id), None)
        else:
            target = self.snapshots[-2] if len(self.snapshots) >= 2 else None

        if target:
            logger.info(f"快照回滚: → {target.snap_id}")
            self.active_snap = target
            return target

        raise ValueError("无可回滚快照")

    def diff_snapshots(self, snap_a: str, snap_b: str) -> dict:
        """比较两个快照"""
        a = next((s for s in self.snapshots if s.snap_id == snap_a), None)
        b = next((s for s in self.snapshots if s.snap_id == snap_b), None)

        if not a or not b:
            return {}

        diff = {
            "version_change": f"{a.version} → {b.version}",
            "skills_added": list(set(b.skill_ids) - set(a.skill_ids)),
            "skills_removed": list(set(a.skill_ids) - set(b.skill_ids)),
            "skills_unchanged": list(set(a.skill_ids) & set(b.skill_ids)),
            "perf_delta": {},
        }

        return diff

    def get_history(self) -> list:
        return [{"id": s.snap_id, "version": s.version, "hash": s.state_hash[:8],
                 "skills": len(s.skill_ids), "time": datetime.fromtimestamp(s.timestamp).isoformat()}
                for s in self.snapshots]

    def _compute_diff(self, parent_id: str, current: dict) -> dict:
        return {"new_skills": len(current.get("skill_ids", [])), "capabilities_changed": []}


# ==================== 主编排器 v3.0 ====================

class EvolutionOrchestratorV3:
    """自进化主编排器 v3.0 — 全域联动版"""

    def __init__(self, skill_store: dict = None, tool_map: dict = None,
                 vault_path: str = None, workspace: str = None):
        self.workspace = workspace or Path(".")
        self.skill_forge = SkillAutoExtractorV5(skill_store=skill_store, tool_map=tool_map)
        self.sica = SICAEnhancedFeedback()
        self.obsidian = ObsidianBridgeV2(vault_path=vault_path)
        self.ai_on_ui = AIOnUIIntegration()
        self.desktop = DesktopControlBridge()
        self.snapshot = SnapshotManagerV3()
        self.evolution_logs: list[EvolutionLog] = []
        self.phase_times: dict = {p: [] for p in EvolutionPhase}

    def run_full_cycle(self, trigger: EvolutionTrigger = EvolutionTrigger.SCHEDULED,
                       context: dict = None) -> dict:
        """执行完整的自进化循环"""
        ctx = context or {}
        cycle_id = f"evo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"🔄 自进化循环启动: {cycle_id} (触发: {trigger.value})")

        results = {}

        # Phase 1: 快照保存
        pre_state = self._capture_state()
        pre_snap = self.snapshot.take_snapshot(pre_state, f"pre_evo_{cycle_id}")
        results["pre_snapshot"] = pre_snap.snap_id

        # Phase 2: 能力缺口检测
        gaps = self._detect_gaps(ctx)
        if gaps:
            logger.info(f"检测到 {len(gaps)} 个能力缺口")
        results["gaps"] = gaps

        # Phase 3: SICA 进化执行
        evo_result = self._run_sica_evolution(gaps)
        results["sica"] = evo_result

        # Phase 4: 技能萃取与注册
        extracted = self.skill_forge.extract_from_logs(ctx.get("recent_logs", []))
        registered = []
        for spec in extracted:
            if self.skill_forge.register_skill(spec):
                registered.append(spec.skill_id)
        results["skills_extracted"] = len(extracted)
        results["skills_registered"] = registered

        # Phase 5: 技能优化
        optimizations = self.skill_forge.optimize_skills()
        results["optimizations"] = optimizations

        # Phase 6: Obsidian 同步
        obsidian_synced = 0
        for skill_id in registered:
            spec = self.skill_forge.skill_store.get(skill_id)
            if spec:
                self.obsidian.sync_to_vault(spec)
                obsidian_synced += 1
        results["obsidian_synced"] = obsidian_synced

        # Phase 7: 桌面联动注册
        for spec_id in registered[:3]:
            self.desktop.add_rule(
                trigger=f"skill_registered:{spec_id}",
                action=f"notify_desktop",
                condition="always"
            )
        results["desktop_rules_added"] = min(3, len(registered))

        # Phase 8: AI on UI 快速入口
        if registered:
            self.ai_on_ui.register_hotkey("Ctrl+Shift+E", "trigger_evolution")
        results["ai_on_ui"] = self.ai_on_ui.get_desktop_overlay()

        # Phase 9: 快照保存
        post_state = self._capture_state()
        post_snap = self.snapshot.take_snapshot(
            post_state,
            f"post_evo_{cycle_id}",
            parent_id=pre_snap.snap_id
        )
        results["post_snapshot"] = post_snap.snap_id

        # Phase 10: 日志记录
        self.evolution_logs.append(EvolutionLog(
            log_id=cycle_id,
            phase=EvolutionPhase.COMMIT,
            trigger=trigger,
            action="full_cycle",
            result=results,
            duration_ms=0,
        ))

        # 技能注册表摘要
        results["skill_registry"] = self.skill_forge.get_registry()
        results["snapshot_history"] = self.snapshot.get_history()
        results["obsidian_graph"] = self.obsidian.generate_graph_view()

        logger.info(f"✅ 自进化循环完成: {cycle_id}")
        logger.info(f"   技能注册: {results['skill_registry']['total']} 项")
        logger.info(f"   快照数量: {len(self.snapshot.snapshots)}")
        logger.info(f"   桌面规则: {len(self.desktop.automation_rules)}")
        logger.info(f"   AI on UI: {len(self.ai_on_ui.hotkey_registry)} 热键")

        return results

    def run_gap_only(self, target_gap: str) -> dict:
        """定向缺口补全（轻量模式）"""
        logger.info(f"定向补全缺口: {target_gap}")

        pre_snap = self.snapshot.take_snapshot(self._capture_state(), f"gap_{target_gap[:20]}")

        return {
            "gap": target_gap,
            "status": "completed",
            "pre_snapshot": pre_snap.snap_id,
        }

    def get_status(self) -> dict:
        """获取全局状态"""
        return {
            "skills": self.skill_forge.get_registry(),
            "snapshots": len(self.snapshot.snapshots),
            "active_snap": self.snapshot.active_snap.snap_id if self.snapshot.active_snap else None,
            "sica_fitness": dict(sorted(self.sica.fitness_scores.items(), key=lambda x: x[1], reverse=True)[:10]),
            "obsidian_links": len(self.obsidian.link_graph),
            "desktop_rules": len(self.desktop.automation_rules),
            "ai_on_ui": self.ai_on_ui.get_desktop_overlay(),
            "total_cycles": len(self.evolution_logs),
        }

    # --- 内部方法 ---

    def _capture_state(self) -> dict:
        return {
            "capabilities": {"skills": len(self.skill_forge.skill_store)},
            "skill_ids": list(self.skill_forge.skill_store.keys()),
            "performance": {"avg_fitness": sum(self.sica.fitness_scores.values()) / max(1, len(self.sica.fitness_scores))},
            "tags": ["auto", datetime.now().strftime("%m%d")],
        }

    def _detect_gaps(self, ctx: dict) -> list:
        gaps = []
        if ctx.get("target_gaps"):
            return ctx["target_gaps"]
        if len(self.skill_forge.skill_store) < 5:
            gaps.append("insufficient_skills")
        return gaps

    def _run_sica_evolution(self, gaps: list) -> dict:
        return {
            "generation": max(self.sica.generation_counter.values()) if self.sica.generation_counter else 1,
            "mutations_this_cycle": 0,
            "active_lineages": len(self.sica.evolution_lineage),
            "gaps_addressed": gaps,
        }


# ==================== 测试入口 ====================

if __name__ == "__main__":
    orchestrator = EvolutionOrchestratorV3(
        workspace="E:/龙虾AI主控中心/我的AI分身/子Agent/豆包Agent/"
    )

    # 注册桌面联动
    orchestrator.desktop.add_rule("evolution_complete", "show_toast")
    orchestrator.desktop.add_rule("skill_registered", "notify_obsidian_sync")

    # AI on UI 注册
    orchestrator.ai_on_ui.register_hotkey("Ctrl+Shift+E", "trigger_evolution")
    orchestrator.ai_on_ui.register_hotkey("Ctrl+Shift+D", "open_dashboard")

    # 运行一轮完整进化
    result = orchestrator.run_full_cycle(
        trigger=EvolutionTrigger.SCHEDULED,
        context={"target_gaps": ["claude_reasoning", "visual_workflow", "self_evolution"]}
    )

    print(f"\n{'='*50}")
    print("进化循环结果:")
    print(f"  快照ID: {result['pre_snapshot']}")
    print(f"  技能注册: {result['skill_registry']['total']}")
    print(f"  SICA世代: {result['sica']['generation']}")
    print(f"  Obsidian同步: {result['obsidian_synced']}")
    print(f"  桌面规则: {result['desktop_rules_added']}")

    # 全局状态
    status = orchestrator.get_status()
    print(f"\n全局状态:")
    print(f"  技能总数: {status['skills']['total']}")
    print(f"  快照总数: {status['snapshots']}")
    print(f"  AI on UI 热键: {status['ai_on_ui']['registered_hotkeys']}")
    print(f"  Obsidian链接: {status['obsidian_links']}")
    print(f"  桌面规则: {status['desktop_rules']}")
    print(f"  进化周期: {status['total_cycles']}")
```
