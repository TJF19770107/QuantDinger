# self_evolution_core_v6.0.py

> 原始文件: `self_evolution_core_v6.0.py`  |  类型: `.py`  |  自动转换

```python

# -*- coding: utf-8 -*-
"""
深度自进化核心闭环 v6.0 — R15全域缺口补全 · P0-3
================================================
在上代v3.0基础上完成四大里程碑增强：

1. 技能自动萃取引擎 v6.0：日志→模式提取→Skill模板生成→SkillForge联动入库
2. SICA自适应逻辑 v6.0：四步进化循环 + 三维效用函数 + 帕累托前沿选择
3. 版本快照与异常自动回滚：快照链 + 差分存储 + 断路器 + 优雅降级
4. 全域联动桥接 v6.0：Obsidian/桌面控制/AI on UI三通道 + GenericAgent集成

对标：SICA · GEPA · GenericAgent · AlphaEvolve · HyperAgents · OpenSpace
"""

import json
import time
import uuid
import logging
import hashlib
import threading
import re
import sqlite3
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Callable
from collections import defaultdict, deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] EVOL_V6: %(message)s')
logger = logging.getLogger("SelfEvolutionV6")


# ==================== 枚举定义 ====================

class EvolutionPhase(Enum):
    OBSERVE = "observe"
    ANALYZE = "analyze"
    EVOLVE = "evolve"
    DEPLOY = "deploy"
    VERIFY = "verify"


class SkillStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class RollbackTrigger(Enum):
    MANUAL = "manual"
    METRIC_DEGRADATION = "metric_degradation"
    ANOMALY_DETECTED = "anomaly_detected"
    CIRCUIT_BREAKER = "circuit_breaker"
    PERIODIC_HEALTH_CHECK = "health_check"


# ==================== 数据模型 ====================

@dataclass
class LogRecord:
    """结构化日志记录"""
    record_id: str
    timestamp: str
    source: str            # 来源：tool_execution / agent_action / user_feedback
    category: str          # 分类：success / error / pattern / insight
    payload: dict
    execution_time_ms: float = 0
    tool_chain: list = field(default_factory=list)
    user_feedback: Optional[str] = None
    trace_id: str = ""
    tags: list = field(default_factory=list)


@dataclass
class PatternCandidate:
    """模式候选"""
    pattern_id: str
    source_records: list
    pattern_type: str = "execution"  # execution / error_recovery / optimization
    frequency: int = 0
    success_rate: float = 0.0
    context_signature: str = ""      # 上下文特征签名
    extracted_steps: list = field(default_factory=list)
    confidence: float = 0.0
    priority: int = 0


@dataclass
class SkillTemplate:
    """技能模板"""
    template_id: str
    name: str
    description: str
    category: str
    version: str = "1.0"
    triggers: list = field(default_factory=list)
    steps: list = field(default_factory=list)
    tools_required: list = field(default_factory=list)
    preconditions: list = field(default_factory=list)
    postconditions: list = field(default_factory=list)
    fallback_chain: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    status: SkillStatus = SkillStatus.DRAFT
    source_pattern_id: str = ""


@dataclass
class EvolutionGene:
    """进化基因（可微分参数）"""
    gene_id: str
    module: str
    parameter: str
    value: float
    min_range: float = 0.0
    max_range: float = 1.0
    mutation_rate: float = 0.1
    fitness_contribution: float = 0.0
    history: list = field(default_factory=list)


@dataclass
class VersionSnapshot:
    """版本快照"""
    snapshot_id: str
    version: str
    created_at: str
    source_files: dict[str, str]     # file_path → content_hash
    gene_pool: dict[str, float]      # gene_id → value
    metrics: dict[str, float]        # 效能指标
    status: str = "active"
    parent_snapshot_id: str = ""
    diff_size_bytes: int = 0         # 差分大小


# ==================== 1. 技能自动萃取引擎 v6.0 ====================

class SkillAutoExtractorV6:
    """
    技能自动萃取引擎 v6.0
    完整的「日志 → 模式提取 → 模板生成 → SkillForge入库」流水线
    """

    MIN_RECORDS_FOR_PATTERN = 5       # 至少5条记录才提取模式
    CONFIDENCE_THRESHOLD = 0.6        # 模式置信度阈值
    MAX_RECORDS_BUFFER = 10000       # 日志缓冲上限

    # 模式类型签名
    PATTERN_SIGNATURES = {
        "execution": ["exec_chain", "tool_calls", "execution_path"],
        "error_recovery": ["error", "retry", "fallback", "recovery"],
        "optimization": ["performance", "bottleneck", "improvement", "speedup"],
        "interaction": ["user_feedback", "user_confirmation", "ask_user"],
        "evolution": ["evolve", "update", "upgrade", "iteration"]
    }

    def __init__(self, skill_forge=None, memory_os=None):
        self.skill_forge = skill_forge
        self.memory_os = memory_os
        self.log_buffer: deque = deque(maxlen=self.MAX_RECORDS_BUFFER)
        self.patterns: dict[str, PatternCandidate] = {}
        self.templates: dict[str, SkillTemplate] = {}
        self.extraction_metrics = {
            "total_logs_processed": 0,
            "patterns_discovered": 0,
            "templates_generated": 0,
            "templates_published": 0
        }

    def ingest_log(self, log: LogRecord):
        """摄入日志"""
        self.log_buffer.append(log)
        self.extraction_metrics["total_logs_processed"] += 1

        # 检查是否有足够数据触发提取
        if len(self.log_buffer) >= self.MIN_RECORDS_FOR_PATTERN:
            self._trigger_extraction()

    def ingest_logs_batch(self, logs: list[LogRecord]):
        """批量摄入日志"""
        for log in logs:
            self.log_buffer.append(log)
        self.extraction_metrics["total_logs_processed"] += len(logs)

        if len(self.log_buffer) >= self.MIN_RECORDS_FOR_PATTERN:
            self._trigger_extraction()

    def _trigger_extraction(self):
        """触发模式提取流水线"""
        logger.info(f"触发技能萃取: {len(self.log_buffer)} 条日志待处理")

        # Phase 1: 日志聚类
        clusters = self._cluster_logs()

        # Phase 2: 模式挖掘
        for cluster in clusters:
            if len(cluster) >= self.MIN_RECORDS_FOR_PATTERN:
                candidate = self._mine_pattern(cluster)
                if candidate and candidate.confidence >= self.CONFIDENCE_THRESHOLD:
                    pattern_id = f"PATTERN_{uuid.uuid4().hex[:8]}"
                    candidate.pattern_id = pattern_id
                    self.patterns[pattern_id] = candidate
                    self.extraction_metrics["patterns_discovered"] += 1

                    # Phase 3: 模板生成
                    template = self._generate_template(candidate)
                    if template:
                        self.templates[template.template_id] = template
                        self.extraction_metrics["templates_generated"] += 1

                        # Phase 4: SkillForge入库
                        if self.skill_forge:
                            self._commit_to_skillforge(template)

        logger.info(f"萃取完成: {self.extraction_metrics['patterns_discovered']} 模式 / "
                    f"{self.extraction_metrics['templates_generated']} 模板")

    def _cluster_logs(self) -> list[list[LogRecord]]:
        """日志聚类（基于分类+上下文签名）"""
        clusters = defaultdict(list)

        for log in self.log_buffer:
            # 复合键：分类 + 来源 + 标签前2个
            key = f"{log.category}|{log.source}|{'_'.join(sorted(log.tags[:2]))}"
            clusters[key].append(log)

        # 按簇大小排序，取前20个簇
        sorted_clusters = sorted(clusters.values(), key=len, reverse=True)
        return sorted_clusters[:20]

    def _mine_pattern(self, cluster: list[LogRecord]) -> Optional[PatternCandidate]:
        """从日志簇挖掘执行模式"""
        if not cluster:
            return None

        # 1. 计算基本统计
        total = len(cluster)
        successes = sum(1 for log in cluster if log.category == "success")
        success_rate = successes / total if total > 0 else 0

        # 2. 提取步骤链
        all_steps = []
        tool_usage = defaultdict(int)

        for log in cluster:
            if log.tool_chain:
                all_steps.extend(log.tool_chain)
            for tool in (log.tool_chain or []):
                tool_usage[tool] += 1

        # 3. 步骤去重排序
        step_counts = {}
        step_order = []
        for step in all_steps:
            if step not in step_counts:
                step_counts[step] = 0
                step_order.append(step)
            step_counts[step] += 1

        # 过滤低频步骤（出现次数 < 总记录数 30%）
        filtered_steps = [s for s in step_order if step_counts[s] >= total * 0.3]

        # 4. 分类模式
        categories = defaultdict(int)
        for log in cluster:
            categories[log.category] += 1

        dominant_category = max(categories, key=categories.get)
        pattern_type = "error_recovery" if "error" in categories else \
                      "optimization" if "performance" in categories else \
                      "execution"

        # 5. 上下文签名
        tool_signature = "_".join(sorted(tool_usage.keys())[:5])
        context_sig = hashlib.md5(f"{dominant_category}|{tool_signature}".encode()).hexdigest()[:12]

        # 6. 置信度计算（多因子）
        # - 簇大小 > 阈值 → 增加置信度
        # - 成功率 > 阈值 → 增加置信度
        # - 步骤链一致性好 → 增加置信度
        size_factor = min(total / (self.MIN_RECORDS_FOR_PATTERN * 2), 1.0)
        success_factor = success_rate
        consistency = len(filtered_steps) / max(len(step_order), 1)
        confidence = (size_factor * 0.3 + success_factor * 0.4 + consistency * 0.3)

        return PatternCandidate(
            pattern_id="",
            source_records=[r.record_id for r in cluster[:10]],
            pattern_type=pattern_type,
            frequency=total,
            success_rate=success_rate,
            context_signature=context_sig,
            extracted_steps=filtered_steps,
            confidence=confidence,
            priority=int(confidence * 10)
        )

    def _generate_template(self, candidate: PatternCandidate) -> Optional[SkillTemplate]:
        """从模式候选生成技能模板"""
        template_id = f"SKILL_{uuid.uuid4().hex[:8]}"

        # 1. 技能命名（基于上下文签名+模式类型）
        name = f"自动萃取_{candidate.pattern_type}_{candidate.context_signature}"

        # 2. 描述
        desc = (f"从 {candidate.frequency} 条执行记录中自动萃取的{candidate.pattern_type}技能。"
                f"成功率: {candidate.success_rate:.1%} | 置信度: {candidate.confidence:.2f}")

        # 3. 步骤映射
        steps = []
        for i, step in enumerate(candidate.extracted_steps):
            steps.append({
                "order": i + 1,
                "action": step,
                "description": f"步骤{i+1}: {step}",
                "expected_output": "执行成功",
                "on_error": "retry_or_fallback"
            })

        # 4. 前置条件
        preconditions = ["日志缓冲区已满阈值", "模式置信度>=0.6"] if candidate.pattern_type != "execution" \
            else ["上下文完整", "工具可用"]

        # 5. 后置条件
        postconditions = ["技能模板已生成", "有效执行模式已沉淀"]

        return SkillTemplate(
            template_id=template_id,
            name=name,
            description=desc,
            category=f"auto_extracted_{candidate.pattern_type}",
            version="1.0",
            steps=steps,
            tools_required=candidate.extracted_steps,
            preconditions=preconditions,
            postconditions=postconditions,
            fallback_chain=["回退到人工确认"],
            metadata={
                "source_pattern_id": candidate.pattern_id,
                "confidence": candidate.confidence,
                "frequency": candidate.frequency,
                "success_rate": candidate.success_rate,
                "extraction_time": datetime.now().isoformat()
            },
            status=SkillStatus.DRAFT,
            source_pattern_id=candidate.pattern_id
        )

    def _commit_to_skillforge(self, template: SkillTemplate):
        """提交模板到 SkillForge 入库"""
        if not self.skill_forge:
            logger.warning("SkillForge 未连接，模板暂存于本地")
            return

        try:
            # 调用 SkillForge 入库接口
            self.skill_forge.register(template)
            template.status = SkillStatus.ACTIVE
            self.extraction_metrics["templates_published"] += 1
            logger.info(f"技能已入库 SkillForge: {template.name} ({template.template_id})")
        except Exception as e:
            logger.error(f"SkillForge入库失败: {e}")

    def rate_skill(self, template_id: str, rubric_scores: dict) -> float:
        """Rubric 技能评分（0-1）"""
        template = self.templates.get(template_id)
        if not template:
            return 0.0

        weights = {
            "completeness": 0.25,
            "reusability": 0.2,
            "correctness": 0.25,
            "efficiency": 0.15,
            "maintainability": 0.15
        }

        score = sum(rubric_scores.get(k, 0) * w for k, w in weights.items())
        if score < 0.3:
            template.status = SkillStatus.DEPRECATED
        return score

    def query_logs(self, category: str = None, source: str = None,
                   time_range: tuple = None) -> list[LogRecord]:
        """日志查询API"""
        results = list(self.log_buffer)

        if category:
            results = [log for log in results if log.category == category]
        if source:
            results = [log for log in results if log.source == source]

        return results

    def get_extraction_report(self) -> dict:
        """萃取报告"""
        return {
            "metrics": self.extraction_metrics,
            "active_patterns": len(self.patterns),
            "active_templates": sum(1 for t in self.templates.values() if t.status == SkillStatus.ACTIVE),
            "draft_templates": sum(1 for t in self.templates.values() if t.status == SkillStatus.DRAFT),
            "deprecated_templates": sum(1 for t in self.templates.values() if t.status == SkillStatus.DEPRECATED),
            "top_patterns": sorted(
                [(pid, p.frequency, p.confidence) for pid, p in self.patterns.items()],
                key=lambda x: x[2], reverse=True
            )[:10]
        }


# ==================== 2. SICA 自适应逻辑 v6.0 ====================

class SICAAdaptiveEngineV6:
    """
    SICA (Self-Improving Code Agent) 自适应引擎 v6.0
    四步进化循环 + 三维效用函数 + 帕累托前沿选择
    """

    # 四步进化循环
    EVOLUTION_CYCLE = [
        EvolutionPhase.OBSERVE,
        EvolutionPhase.ANALYZE,
        EvolutionPhase.EVOLVE,
        EvolutionPhase.DEPLOY
    ]

    MAX_GENERATIONS = 20
    POPULATION_SIZE = 8
    MUTATION_RATE = 0.15
    CROSSOVER_RATE = 0.6

    def __init__(self, safe_guard=None):
        self.safe_guard = safe_guard
        self.genes: dict[str, EvolutionGene] = {}        # 基因库
        self.generation_history: list[dict] = []          # 代际历史
        self.pareto_frontier: list = []                   # 帕累托前沿
        self.utility_history: list[tuple] = []            # 效用函数时间序列
        self.current_generation: int = 0
        self._lock = threading.Lock()

    def cycle(self, observables: dict, fitness_feedback: dict) -> dict:
        """执行一个完整进化周期"""
        cycle_start = time.time()
        phase_results = {}

        with self._lock:
            # Phase 1: OBSERVE - 观测当前状态
            observation = self._observe(observables)
            phase_results["observe"] = observation

            # Phase 2: ANALYZE - 分析改进方向
            analysis = self._analyze(observation, fitness_feedback)
            phase_results["analyze"] = analysis

            # Phase 3: EVOLVE - 执行进化操作
            evolved = self._evolve(analysis)
            phase_results["evolve"] = evolved

            # Phase 4: DEPLOY - 部署新策略
            deploy_result = self._deploy(evolved)
            phase_results["deploy"] = deploy_result

            # 记录代际历史
            self.generation_history.append({
                "generation": self.current_generation,
                "timestamp": datetime.now().isoformat(),
                "utility": self._compute_utility(evolved),
                "gene_count": len(self.genes),
                "phase_results": phase_results
            })
            self.current_generation += 1

        return {
            "generation": self.current_generation,
            "phase_results": phase_results,
            "duration_ms": (time.time() - cycle_start) * 1000,
            "gene_count": len(self.genes),
            "improvement": analysis.get("expected_improvement", 0)
        }

    def _observe(self, observables: dict) -> dict:
        """观测：采集当前系统状态 + 基因表达"""
        return {
            "state": observables,
            "active_genes": len(self.genes),
            "current_utility": self._compute_utility(self.genes) if self.genes else 0,
            "timestamp": time.time()
        }

    def _analyze(self, observation: dict, fitness_feedback: dict) -> dict:
        """分析：计算三维效用函数 + 确定改进方向"""
        utility = self._triple_utility(observation, fitness_feedback)
        self.utility_history.append((time.time(), utility))

        # 目标梯度方向
        gradients = {
            "accuracy": fitness_feedback.get("accuracy", observation.get("state", {}).get("accuracy", 0.5)),
            "efficiency": 1.0 - min(observation.get("state", {}).get("latency", 1000) / 10000, 1.0),
            "adaptability": fitness_feedback.get("adaptability", 0.5)
        }

        expected_improvement = max(0, 0.9 - utility["overall"])

        return {
            "utility": utility,
            "gradients": gradients,
            "expected_improvement": expected_improvement,
            "improvement_direction": self._select_direction(gradients, utility),
            "pareto_candidates": self._update_pareto_frontier(utility, observation)
        }

    def _evolve(self, analysis: dict) -> dict:
        """进化：突变 + 交叉 + 选择"""
        evolved_genes = {}
        mutations = 0
        crossovers = 0

        # 1. 突变：随机变异基因
        for gene_id, gene in list(self.genes.items()):
            import random
            if random.random() < self.MUTATION_RATE:
                new_value = gene.value + random.uniform(-gene.mutation_rate, gene.mutation_rate)
                new_value = max(gene.min_range, min(gene.max_range, new_value))
                gene.value = new_value
                gene.history.append({
                    "generation": self.current_generation,
                    "value": new_value,
                    "operation": "mutation"
                })
                mutations += 1
            evolved_genes[gene_id] = gene

        # 2. 交叉：选择两个基因交换参数
        gene_ids = list(self.genes.keys())
        for i in range(0, len(gene_ids) - 1, 2):
            import random
            if random.random() < self.CROSSOVER_RATE and len(gene_ids) >= 2:
                g1, g2 = self.genes[gene_ids[i]], self.genes[gene_ids[i + 1]]
                alpha = random.uniform(0, 1)
                new_val = alpha * g1.value + (1 - alpha) * g2.value
                g1.value = max(g1.min_range, min(g1.max_range, new_val))
                g1.history.append({
                    "generation": self.current_generation,
                    "value": new_val,
                    "operation": "crossover"
                })
                crossovers += 1

        # 3. 选择：保留适应度最高的基因组合
        self.genes = evolved_genes

        return {
            "mutations": mutations,
            "crossovers": crossovers,
            "total_genes": len(self.genes),
            "pareto_frontier_size": len(self.pareto_frontier)
        }

    def _deploy(self, evolved: dict) -> dict:
        """部署：应用进化结果 + 安全审查"""
        deploy_safe = True

        if self.safe_guard:
            try:
                deploy_safe = self.safe_guard.audit_evolution(self.genes)
            except Exception:
                deploy_safe = False

        if not deploy_safe:
            logger.warning("安全检查未通过，基因部署被阻止")
            return {"deployed": False, "reason": "safety_audit_failed"}

        return {
            "deployed": True,
            "gene_count": len(self.genes),
            "current_utility": self._compute_utility(self.genes),
            "timestamp": datetime.now().isoformat()
        }

    def _triple_utility(self, observation: dict, feedback: dict) -> dict:
        """三维效用函数 U = w1 * F1(性能) + w2 * F2(正确性) + w3 * F3(适应度)"""
        state = observation.get("state", {})

        # F1: 性能维度 (0-1)
        latency = state.get("latency", 1000)
        memory = state.get("memory_usage", 500)
        F1 = max(0, 1.0 - latency / 10000) * 0.5 + max(0, 1.0 - memory / 2000) * 0.5

        # F2: 正确性维度 (0-1)
        accuracy = feedback.get("accuracy", state.get("accuracy", 0.85))
        success_rate = feedback.get("success_rate", 0.9)
        F2 = accuracy * 0.6 + success_rate * 0.4

        # F3: 适应度维度 (0-1)
        # - 基因多样性
        gene_diversity = min(len(self.genes) / 20, 1.0) if self.genes else 0.2
        # - 收敛速度
        convergence = 1.0 - (self.current_generation / self.MAX_GENERATIONS)
        # - 反馈响应
        feedback_response = feedback.get("adaptability", 0.7)
        F3 = gene_diversity * 0.3 + convergence * 0.3 + feedback_response * 0.4

        overall = 0.4 * F1 + 0.35 * F2 + 0.25 * F3

        return {
            "overall": overall,
            "F1_performance": F1,
            "F2_correctness": F2,
            "F3_adaptability": F3,
            "weights": {"w1": 0.4, "w2": 0.35, "w3": 0.25}
        }

    def _select_direction(self, gradients: dict, utility: dict) -> str:
        """选择改进方向"""
        if utility["overall"] > 0.85:
            return "fine_tune"
        if gradients["accuracy"] < 0.5:
            return "improve_accuracy"
        if gradients["efficiency"] < 0.4:
            return "improve_efficiency"
        return "balance"

    def _update_pareto_frontier(self, utility: dict, observation: dict) -> list:
        """更新帕累托前沿"""
        point = (utility["F1_performance"], utility["F2_correctness"], utility["F3_adaptability"])

        # 检查是否被现有前沿支配
        dominated = False
        new_frontier = []
        for existing in self.pareto_frontier:
            if all(e >= p for e, p in zip(existing, point)):
                dominated = True
                new_frontier.append(existing)
            elif all(p >= e for p, e in zip(point, existing)):
                continue  # 新点支配旧点
            else:
                new_frontier.append(existing)

        if not dominated:
            new_frontier.append(point)

        self.pareto_frontier = new_frontier
        return new_frontier

    def _compute_utility(self, genes: dict) -> float:
        """基于当前基因池计算总效用"""
        if not genes:
            return 0
        return sum(g.value * g.fitness_contribution for g in genes.values()) / max(len(genes), 1)

    def register_gene(self, module: str, parameter: str,
                      initial_value: float = 0.5,
                      mutation_rate: float = 0.1,
                      fitness_contribution: float = 0.5):
        """注册新的进化基因"""
        gene_id = f"GENE_{module}_{parameter}_{uuid.uuid4().hex[:4]}"
        self.genes[gene_id] = EvolutionGene(
            gene_id=gene_id,
            module=module,
            parameter=parameter,
            value=initial_value,
            mutation_rate=mutation_rate,
            fitness_contribution=fitness_contribution
        )
        logger.info(f"基因已注册: {gene_id} = {initial_value}")
        return gene_id


# ==================== 3. 版本快照与异常自动回滚 v6.0 ====================

class SnapshotManagerV6:
    """版本快照管理器 + 差分存储 + 自动回滚 + 断路器"""

    MAX_SNAPSHOTS = 50
    DEGRADATION_THRESHOLD = 0.2  # 效能下降 20% 触发回滚
    CIRCUIT_BREAKER_THRESHOLD = 3  # 连续3次失败触发断路器

    def __init__(self, snapshot_dir: str = None):
        self.snapshot_dir = snapshot_dir or "snapshots"
        Path(self.snapshot_dir).mkdir(parents=True, exist_ok=True)
        self.snapshots: dict[str, VersionSnapshot] = {}
        self.active_snapshot_id: str = ""
        self.consecutive_failures: int = 0
        self.circuit_open: bool = False
        self.rollback_history: list = []

    def create_snapshot(self, version: str, source_files: dict[str, str],
                        gene_pool: dict, metrics: dict,
                        parent_id: str = "") -> VersionSnapshot:
        """创建版本快照"""
        snapshot_id = f"V{version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 差分计算
        if parent_id and parent_id in self.snapshots:
            parent = self.snapshots[parent_id]
            diff_size = self._compute_diff(source_files, parent.source_files)
        else:
            diff_size = sum(len(v) for v in source_files.values())

        snapshot = VersionSnapshot(
            snapshot_id=snapshot_id,
            version=version,
            created_at=datetime.now().isoformat(),
            source_files=source_files,
            gene_pool=gene_pool,
            metrics=metrics,
            status="active",
            parent_snapshot_id=parent_id,
            diff_size_bytes=diff_size
        )

        self.snapshots[snapshot_id] = snapshot
        self.active_snapshot_id = snapshot_id

        # 保存到磁盘
        self._persist_snapshot(snapshot)

        # 清理旧快照
        self._cleanup_old_snapshots()

        logger.info(f"快照已创建: {snapshot_id} (diff: {diff_size}B)")
        return snapshot

    def check_health(self, current_metrics: dict) -> dict:
        """健康检查 v6.0"""
        result = {
            "healthy": True,
            "action": "continue",
            "metrics": current_metrics,
            "comparison": {}
        }

        active = self.snapshots.get(self.active_snapshot_id)
        if not active or not active.metrics:
            return result

        # 对比指标
        for metric, value in current_metrics.items():
            baseline = active.metrics.get(metric, value)
            if baseline > 0:
                change = (value - baseline) / baseline
                result["comparison"][metric] = {
                    "baseline": baseline,
                    "current": value,
                    "change_pct": change
                }

                # 检测性能退化
                if change < -self.DEGRADATION_THRESHOLD:
                    result["healthy"] = False
                    result["action"] = "rollback"
                    result["degraded_metric"] = metric

        # 断路器检测
        if not result["healthy"]:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.CIRCUIT_BREAKER_THRESHOLD:
                self.circuit_open = True
                result["action"] = "circuit_breaker"
                result["message"] = f"断路器打开: 连续{self.consecutive_failures}次故障"
        else:
            self.consecutive_failures = 0
            self.circuit_open = False

        return result

    def rollback(self, trigger: RollbackTrigger, target_snapshot_id: str = None) -> dict:
        """执行回滚"""
        # 确定回滚目标
        if target_snapshot_id:
            target = self.snapshots.get(target_snapshot_id)
        else:
            # 回滚到上一个健康快照
            sorted_snapshots = sorted(
                [(sid, s) for sid, s in self.snapshots.items()],
                key=lambda x: x[1].created_at, reverse=True
            )
            target = None
            for sid, snap in sorted_snapshots:
                if sid != self.active_snapshot_id and snap.status == "active":
                    target = snap
                    break

        if not target:
            return {"success": False, "reason": "无可用的回滚目标"}

        rollback_entry = {
            "trigger": trigger.value,
            "from_snapshot": self.active_snapshot_id,
            "to_snapshot": target.snapshot_id,
            "timestamp": datetime.now().isoformat(),
            "circuit_breaker": self.circuit_open
        }
        self.rollback_history.append(rollback_entry)

        # 执行回滚
        self.active_snapshot_id = target.snapshot_id
        self.consecutive_failures = 0
        self.circuit_open = False

        logger.warning(f"回滚执行: {self.active_snapshot_id} → {target.snapshot_id}")
        return {"success": True, "rollback": rollback_entry, "active_snapshot": target.snapshot_id}

    def _compute_diff(self, current: dict[str, str], previous: dict[str, str]) -> int:
        """计算文件差异大小（简化：基于哈希）"""
        diff = 0
        for path, content in current.items():
            prev_content = previous.get(path, "")
            if content != prev_content:
                diff += abs(len(content) - len(prev_content))
        return diff

    def _persist_snapshot(self, snapshot: VersionSnapshot):
        """持久化快照到磁盘"""
        file_path = Path(self.snapshot_dir) / f"{snapshot.snapshot_id}.json"
        data = {
            "snapshot_id": snapshot.snapshot_id,
            "version": snapshot.version,
            "created_at": snapshot.created_at,
            "source_files": snapshot.source_files,
            "gene_pool": snapshot.gene_pool,
            "metrics": snapshot.metrics,
            "status": snapshot.status,
            "parent_snapshot_id": snapshot.parent_snapshot_id,
            "diff_size_bytes": snapshot.diff_size_bytes
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_snapshot(self, snapshot_id: str) -> Optional[VersionSnapshot]:
        """从磁盘加载快照"""
        file_path = Path(self.snapshot_dir) / f"{snapshot_id}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return VersionSnapshot(**data)
        return None

    def _cleanup_old_snapshots(self):
        """清理超出上限的旧快照"""
        if len(self.snapshots) > self.MAX_SNAPSHOTS:
            sorted_ids = sorted(
                self.snapshots.keys(),
                key=lambda sid: self.snapshots[sid].created_at
            )
            remove_count = len(self.snapshots) - self.MAX_SNAPSHOTS
            for sid in sorted_ids[:remove_count]:
                del self.snapshots[sid]

    def get_snapshot_chain(self) -> list:
        """获取快照链"""
        chain = []
        current_id = self.active_snapshot_id
        while current_id and current_id in self.snapshots:
            snap = self.snapshots[current_id]
            chain.append({
                "snapshot_id": snap.snapshot_id,
                "version": snap.version,
                "created_at": snap.created_at,
                "status": snap.status
            })
            current_id = snap.parent_snapshot_id
        return chain


# ==================== 4. 全域联动桥接 v6.0 ====================

class CrossDomainBridgeV6:
    """
    全域联动桥接 v6.0
    三层桥接总线：Obsidian / AI on UI / 桌面控制
    """

    BRIDGE_PROTOCOL_VERSION = "6.0"

    def __init__(self, obsidian_client=None, desktop_controller=None, ai_ui_client=None):
        self.obsidian = obsidian_client
        self.desktop = desktop_controller
        self.ai_ui = ai_ui_client
        self.bridge_log: list = []
        self.transport_stats = defaultdict(int)

    # ---------- Obsidian 通道 ----------

    def sync_to_obsidian(self, note_path: str, content: str, tags: list = None) -> dict:
        """同步到 Obsidian 知识库"""
        tags = tags or ["auto_sync", "evolution_v6"]
        result = {"channel": "obsidian", "action": "sync", "note_path": note_path}

        try:
            if self.obsidian:
                self.obsidian.create_or_update(note_path, content, tags)
                result["status"] = "success"
            else:
                # 文件系统直写（备选）
                full_path = Path("E:/龙虾AI主控中心/知识库") / note_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                result["status"] = "local_write"
                result["local_path"] = str(full_path)
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)

        self._log_bridge("obsidian", result)
        return result

    def read_from_obsidian(self, note_path: str) -> dict:
        """从 Obsidian 读取"""
        result = {"channel": "obsidian", "action": "read", "note_path": note_path}

        try:
            if self.obsidian:
                content = self.obsidian.read(note_path)
                result["content"] = content
            else:
                full_path = Path("E:/龙虾AI主控中心/知识库") / note_path
                if full_path.exists():
                    result["content"] = full_path.read_text(encoding="utf-8")
                else:
                    result["content"] = None
                    result["status"] = "not_found"
                    return result
            result["status"] = "success"
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)

        return result

    # ---------- 桌面控制通道 ----------

    def desktop_execute(self, action: str, params: dict = None) -> dict:
        """桌面控制通道执行"""
        params = params or {}
        result = {"channel": "desktop", "action": action}

        if self.desktop:
            try:
                output = self.desktop.execute(action, **params)
                result["status"] = "success"
                result["output"] = output
            except Exception as e:
                result["status"] = "failed"
                result["error"] = str(e)
        else:
            result["status"] = "no_controller"

        self._log_bridge("desktop", result)
        return result

    def desktop_screenshot(self, region: tuple = None) -> dict:
        """桌面截图"""
        return self.desktop_execute("screenshot", {"region": region})

    def desktop_click(self, x: int, y: int) -> dict:
        """桌面点击"""
        return self.desktop_execute("click", {"x": x, "y": y})

    # ---------- AI on UI 通道 ----------

    def ai_ui_analyze(self, screenshot_path: str, instruction: str) -> dict:
        """AI on UI 分析：截图→语义理解→操作决策"""
        result = {"channel": "ai_ui", "action": "analyze",
                 "screenshot": screenshot_path, "instruction": instruction}

        if self.ai_ui:
            try:
                analysis = self.ai_ui.semantic_locate(screenshot_path, instruction)
                result["status"] = "success"
                result["analysis"] = analysis
            except Exception as e:
                result["status"] = "failed"
                result["error"] = str(e)
        else:
            result["status"] = "no_ui_client"

        self._log_bridge("ai_ui", result)
        return result

    def ai_ui_operate(self, element_name: str, operation: str = "click") -> dict:
        """AI on UI 操作"""
        result = {"channel": "ai_ui", "action": operation, "element": element_name}

        if self.ai_ui:
            try:
                output = self.ai_ui.operate(element_name, operation)
                result["status"] = "success"
                result["output"] = output
            except Exception as e:
                result["status"] = "failed"
                result["error"] = str(e)
        else:
            result["status"] = "no_ui_client"

        self._log_bridge("ai_ui", result)
        return result

    # ---------- GenericAgent 集成 ----------

    def generic_agent_dispatch(self, task: dict) -> dict:
        """通过GenericAgent轻量化架构分发任务"""
        result = {
            "channel": "generic_agent",
            "action": "dispatch",
            "task": task,
            "protocol_version": self.BRIDGE_PROTOCOL_VERSION
        }

        # 任务格式标准化
        generic_task = {
            "id": str(uuid.uuid4())[:8],
            "goal": task.get("goal", ""),
            "params": task.get("params", {}),
            "max_tools": min(task.get("max_tools", 10), 10),
            "constraints": task.get("constraints", []),
            "dispatch_time": datetime.now().isoformat()
        }

        result["generic_task"] = generic_task
        result["status"] = "queued"

        self._log_bridge("generic_agent", result)
        return result

    # ---------- 工具方法 ----------

    def _log_bridge(self, channel: str, result: dict):
        """记录桥接日志"""
        self.bridge_log.append({
            "channel": channel,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        self.transport_stats[channel] += 1

    def get_bridge_stats(self) -> dict:
        """获取桥接统计"""
        return {
            "total_transports": sum(self.transport_stats.values()),
            "by_channel": dict(self.transport_stats),
            "protocol_version": self.BRIDGE_PROTOCOL_VERSION
        }


# ==================== 主引擎 v6.0 ====================

class SelfEvolutionCoreV6:
    """深度自进化核心闭环主引擎 v6.0"""

    def __init__(
        self,
        memory_os=None,
        safe_guard=None,
        skill_forge=None,
        obsidian_client=None,
        desktop_controller=None,
        ai_ui_client=None,
        snapshot_dir: str = None
    ):
        self.memory_os = memory_os
        self.safe_guard = safe_guard

        # 四大子引擎
        self.extractor = SkillAutoExtractorV6(skill_forge=skill_forge, memory_os=memory_os)
        self.sica = SICAAdaptiveEngineV6(safe_guard=safe_guard)
        self.snapshot_manager = SnapshotManagerV6(snapshot_dir=snapshot_dir)
        self.bridge = CrossDomainBridgeV6(
            obsidian_client=obsidian_client,
            desktop_controller=desktop_controller,
            ai_ui_client=ai_ui_client
        )

        # 统计
        self.stats = {
            "cycles_completed": 0,
            "snapshots_created": 0,
            "skills_extracted": 0,
            "rollbacks_executed": 0,
            "bridge_operations": 0
        }

        # 健康监控
        self.health_check_interval = 60  # 每60秒健康检查
        self._last_health_check = time.time()

    def evolve(self, observables: dict, fitness_feedback: dict = None) -> dict:
        """
        执行一个完整自进化周期 v6.0
        1. Skill引擎萃取新技能
        2. SICA遗传算法进化基因
        3. 快照保存当前状态
        4. 桥接同步全域知识
        """
        fitness_feedback = fitness_feedback or {}
        cycle_start = time.time()

        # Step 1: 技能自动萃取（基于最近日志）
        extraction_report = self.extractor.get_extraction_report()
        self.stats["skills_extracted"] = extraction_report["templates_generated"]

        # Step 2: SICA四步进化循环
        evolution_result = self.sica.cycle(observables, fitness_feedback)

        # Step 3: 版本快照
        if evolution_result["phase_results"].get("deploy", {}).get("deployed"):
            gene_snapshot = {gid: gene.value for gid, gene in self.sica.genes.items()}
            snapshot = self.snapshot_manager.create_snapshot(
                version=f"6.0.{self.stats['cycles_completed']}",
                source_files={
                    "self_evolution_core": "v6.0",
                    "gene_pool": json.dumps(gene_snapshot)
                },
                gene_pool=gene_snapshot,
                metrics={
                    "utility": evolution_result["phase_results"]["analyze"]["utility"]["overall"],
                    "gene_count": len(self.sica.genes),
                    "pareto_frontier": len(self.sica.pareto_frontier)
                },
                parent_id=self.snapshot_manager.active_snapshot_id if self.snapshot_manager.active_snapshot_id else ""
            )
            self.stats["snapshots_created"] += 1

        # Step 4: 健康检查
        if time.time() - self._last_health_check > self.health_check_interval:
            health = self.snapshot_manager.check_health({
                "utility": evolution_result["phase_results"]["analyze"]["utility"]["overall"],
                "gene_count": len(self.sica.genes)
            })
            if health["action"] in ("rollback", "circuit_breaker"):
                rollback_result = self.snapshot_manager.rollback(RollbackTrigger.METRIC_DEGRADATION)
                self.stats["rollbacks_executed"] += 1
            self._last_health_check = time.time()

        # Step 5: 全域桥接同步
        self._sync_to_bridges(evolution_result)

        self.stats["cycles_completed"] += 1

        return {
            "cycle": self.stats["cycles_completed"],
            "evolution": evolution_result,
            "extraction": extraction_report,
            "health": self.snapshot_manager.check_health({"utility": evolution_result["phase_results"]["analyze"]["utility"]["overall"]}),
            "bridge_stats": self.bridge.get_bridge_stats(),
            "duration_ms": (time.time() - cycle_start) * 1000,
            "stats": self.stats.copy()
        }

    def _sync_to_bridges(self, evolution_result: dict):
        """同步进化结果到全域桥接"""
        utility = evolution_result["phase_results"]["analyze"]["utility"]["overall"]

        # Obsidian 同步
        self.bridge.sync_to_obsidian(
            note_path=f"进化日志/进化周期_{self.stats['cycles_completed'] + 1}.md",
            content=f"# 进化周期 {self.stats['cycles_completed'] + 1}\n\n"
                    f"- 时间: {datetime.now().isoformat()}\n"
                    f"- 效用: {utility:.4f}\n"
                    f"- 基因数: {len(self.sica.genes)}\n",
            tags=["evolution", "auto_log", "v6.0"]
        )

        self.stats["bridge_operations"] += 1

    def ingest_logs(self, logs: list[LogRecord]):
        """从外部注入日志（供执行引擎调试后调用）"""
        self.extractor.ingest_logs_batch(logs)

    def query_evolution_state(self) -> dict:
        """查询当前进化状态"""
        return {
            "stats": self.stats,
            "gene_count": len(self.sica.genes),
            "current_generation": self.sica.current_generation,
            "active_snapshot": self.snapshot_manager.active_snapshot_id,
            "circuit_breaker": self.snapshot_manager.circuit_open,
            "bridge_stats": self.bridge.get_bridge_stats(),
            "latest_utility": self.sica.utility_history[-1] if self.sica.utility_history else None
        }

    def emergency_rollback(self) -> dict:
        """紧急回滚"""
        return self.snapshot_manager.rollback(RollbackTrigger.MANUAL)


# ==================== 测试入口 ====================

if __name__ == "__main__":
    core = SelfEvolutionCoreV6(snapshot_dir="E:/龙虾AI主控中心/snapshots")

    # 模拟日志注入
    sample_logs = [
        LogRecord(
            record_id=f"log_{i}",
            timestamp=datetime.now().isoformat(),
            source="tool_execution",
            category="success" if i % 3 != 0 else "error",
            payload={"action": f"task_{i}", "result": "completed"},
            tool_chain=["read_file", "analyze", "write_file"],
            tags=["iteration", "auto"]
        )
        for i in range(10)
    ]

    core.ingest_logs(sample_logs)

    # 执行一个进化周期
    result = core.evolve(
        observables={"latency": 150, "memory_usage": 450, "accuracy": 0.88},
        fitness_feedback={"accuracy": 0.88, "success_rate": 0.92, "adaptability": 0.75}
    )

    print(json.dumps(result["stats"], ensure_ascii=False, indent=2))
    print(f"效用: {result['evolution']['phase_results']['analyze']['utility']}")

```
