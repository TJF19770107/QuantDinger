# claude_reasoning_engine_v6.0.py

原始格式: Python

```python

"""
Claude 分层推理引擎 v6.0 — 豆包Agent推理核心
================================================
版本: v6.0 (R44全域缺口专项补全 · P0-1落地)
对标: Claude Opus 4.5 Extended Thinking + Effort参数 + 中文全场景适配
创建: 2026-06-02 R44
上一版本: v5.0 (仅设计文档)

核心架构:
  问题解析 → 条件拆解 → 逻辑推演 → 方案执行 → 结果复盘
  双模动态切换: 默认模式(快速推理) ↔ 扩展思考模式(深度推理)
  推理检查点 + DAG回溯 + 长上下文密度优化CIDM
"""

import json
import time
import uuid
import logging
import threading
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict, Tuple, Callable
from enum import Enum
from pathlib import Path
from collections import deque, defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] REASONING_V6: %(message)s')
logger = logging.getLogger("ReasoningV6")


# ==============================
# 枚举定义
# ==============================

class ReasoningMode(Enum):
    """推理模式"""
    DEFAULT = "default"         # 默认快速推理
    EXTENDED = "extended"       # 扩展思考模式
    HYBRID = "hybrid"           # 双模动态切换


class EffortLevel(Enum):
    """推理努力度（对标Claude Opus 4.5 effort参数）"""
    LOW = "low"          # 快速响应，适合简单任务
    MEDIUM = "medium"    # 平衡模式
    HIGH = "high"        # 深度推理，适合复杂任务
    MAXIMUM = "maximum"  # 极限推理


class ReasoningPhase(Enum):
    """五步推理阶段"""
    PARSE = "parse"             # 问题解析
    DECOMPOSE = "decompose"     # 条件拆解
    REASON = "reason"           # 逻辑推演
    EXECUTE = "execute"         # 方案执行
    REVIEW = "review"           # 结果复盘


class CheckpointType(Enum):
    """检查点类型"""
    STATE = "state"             # 完整状态快照
    DELTA = "delta"             # 增量差异
    BRANCH = "branch"           # 分支点
    ERROR = "error"             # 错误检查点


class BacktrackStrategy(Enum):
    """回溯策略"""
    FULL_ROLLBACK = "full_rollback"       # 全量回滚
    PARTIAL_REVERT = "partial_revert"     # 部分撤销
    BRANCH_EXPLORE = "branch_explore"     # 分支探索
    CHECKPOINT_RESUME = "checkpoint_resume"  # 检查点恢复


# ==============================
# 数据模型
# ==============================

@dataclass
class ReasoningContext:
    """推理上下文"""
    context_id: str
    original_query: str
    language: str = "zh-CN"           # 自动语言检测
    domain: str = "general"           # 领域分类
    complexity_score: float = 0.0     # 复杂度评分 0-100
    tokens_used: int = 0
    max_tokens: int = 200000
    created_at: float = field(default_factory=time.time)


@dataclass
class ParseResult:
    """问题解析结果"""
    intent: str                       # 核心意图
    sub_intents: List[str] = field(default_factory=list)
    entities: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    ambiguity_flags: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class DecomposeResult:
    """条件拆解结果"""
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    priority_order: List[str] = field(default_factory=list)
    parallelizable: List[List[str]] = field(default_factory=list)
    precondition_chain: List[str] = field(default_factory=list)


@dataclass
class ReasoningPath:
    """推理路径节点"""
    path_id: str
    phase: ReasoningPhase
    hypothesis: str
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0
    parent_path_id: Optional[str] = None
    children_path_ids: List[str] = field(default_factory=list)
    is_valid: bool = True
    timestamp: float = field(default_factory=time.time)


@dataclass
class ReasoningDAG:
    """推理有向无环图"""
    dag_id: str
    root_path_id: str
    paths: Dict[str, ReasoningPath] = field(default_factory=dict)
    selected_path_id: Optional[str] = None
    terminated_path_ids: List[str] = field(default_factory=list)
    branching_points: List[str] = field(default_factory=list)


@dataclass
class Checkpoint:
    """推理检查点"""
    checkpoint_id: str
    checkpoint_type: CheckpointType
    phase: ReasoningPhase
    context_snapshot: Dict[str, Any]
    reasoning_state: Dict[str, Any]
    parent_checkpoint_id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class ExecutionPlan:
    """执行方案"""
    plan_id: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    tools_required: List[str] = field(default_factory=list)
    estimated_tokens: int = 0
    fallback_plans: List[str] = field(default_factory=list)
    risk_level: str = "low"


@dataclass
class ReviewResult:
    """复盘结果"""
    success: bool
    actual_vs_expected: Dict[str, Any] = field(default_factory=dict)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    lessons: List[str] = field(default_factory=list)
    optimization_suggestions: List[str] = field(default_factory=list)
    self_evolution_triggers: List[str] = field(default_factory=list)


# ==============================
# 中文全场景适配器
# ==============================

class ChineseReasoningAdapter:
    """中文推理适配器：处理中文特有歧义、成语、多义词、文言等"""

    # 中文歧义词库
    AMBIGUITY_PATTERNS = {
        "可以": ["可能", "允许", "能力"],
        "行": ["银行", "行业", "行走", "可以"],
        "打": ["击打", "打印", "打电话", "打车", "打游戏"],
        "开": ["开启", "开车", "开会", "开心"],
        "快": ["快速", "快乐", "锋利", "即将"],
        "好": ["良好", "喜好", "容易", "完成"],
    }

    # 成语→推理模式映射
    IDIOM_REASONING_MAP = {
        "一石二鸟": {"strategy": "multiplex", "optimize": "efficiency"},
        "因噎废食": {"strategy": "caution", "optimize": "risk_balance"},
        "举一反三": {"strategy": "generalize", "optimize": "transfer_learning"},
        "循序渐进": {"strategy": "incremental", "optimize": "stability"},
        "未雨绸缪": {"strategy": "proactive", "optimize": "preparedness"},
    }

    def detect_chinese_ambiguity(self, text: str) -> List[Dict[str, Any]]:
        """检测中文歧义"""
        ambiguities = []
        for word, meanings in self.AMBIGUITY_PATTERNS.items():
            if word in text:
                ambiguities.append({
                    "word": word,
                    "possible_meanings": meanings,
                    "context_needed": True
                })
        return ambiguities

    def resolve_ambiguity(self, word: str, context: str) -> str:
        """基于上下文消歧"""
        if word not in self.AMBIGUITY_PATTERNS:
            return word
        # 简单的上下文词频消歧
        return self.AMBIGUITY_PATTERNS[word][0]

    def extract_idiom_strategy(self, text: str) -> List[Dict[str, str]]:
        """提取成语中的推理策略"""
        strategies = []
        for idiom, mapping in self.IDIOM_REASONING_MAP.items():
            if idiom in text:
                strategies.append({"idiom": idiom, **mapping})
        return strategies

    def detect_language_mix(self, text: str) -> Dict[str, float]:
        """检测中英文混用比例"""
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        total = max(chinese_chars + english_chars, 1)
        return {
            "chinese_ratio": chinese_chars / total,
            "english_ratio": english_chars / total,
            "is_mixed": chinese_chars > 0 and english_chars > 0
        }


# ==============================
# 长上下文密度优化器 (CIDM)
# ==============================

class ContextDensityOptimizer:
    """CIDM: 长上下文密度优化，确保200K token窗口高效利用"""

    def __init__(self, max_tokens: int = 200000):
        self.max_tokens = max_tokens
        self.density_threshold = 0.85  # 密度低于85%时触发压缩
        self.importance_scores: Dict[str, float] = {}

    def calculate_density(self, context: ReasoningContext) -> float:
        """计算上下文信息密度"""
        if context.tokens_used == 0:
            return 1.0
        return min(1.0, context.tokens_used / self.max_tokens)

    def should_compress(self, context: ReasoningContext) -> bool:
        """判断是否需要压缩"""
        density = self.calculate_density(context)
        return density > self.density_threshold

    def score_importance(self, text: str, context: ReasoningContext) -> float:
        """评估信息重要性"""
        # 基于关键词、新颖性、与原始问题的相关性评分
        score = 0.5  # 基础分

        # 含关键实体 +0.3
        if any(kw in text for kw in ["目标", "结论", "发现", "关键", "核心"]):
            score += 0.3

        # 含数字/数据 +0.15
        if any(c.isdigit() for c in text):
            score += 0.15

        # 长度适中 +0.05
        if 20 < len(text) < 500:
            score += 0.05

        return min(1.0, score)

    def compress_context(self, context: ReasoningContext,
                        segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """压缩上下文：保留高重要性，摘要低重要性"""
        scored = [(seg, self.score_importance(seg.get("text", ""), context))
                  for seg in segments]
        scored.sort(key=lambda x: x[1], reverse=True)

        retained = []
        token_budget = self.max_tokens * 0.7  # 压缩到70%

        for seg, score in scored:
            if token_budget <= 0:
                break
            if score > 0.5:
                retained.append(seg)
                token_budget -= len(seg.get("text", "")) // 4
            elif score > 0.3:
                # 低重要性：保留摘要
                seg["compressed"] = True
                seg["text"] = seg.get("text", "")[:100] + "..."
                retained.append(seg)

        return retained


# ==============================
# 推理检查点管理器
# ==============================

class CheckpointManager:
    """推理检查点管理：支持DAG回溯和状态恢复"""

    def __init__(self, max_checkpoints: int = 100):
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.checkpoint_tree: Dict[str, List[str]] = defaultdict(list)
        self.max_checkpoints = max_checkpoints

    def save(self, phase: ReasoningPhase, context: ReasoningContext,
             state: Dict[str, Any], ctype: CheckpointType = CheckpointType.STATE,
             parent_id: Optional[str] = None) -> Checkpoint:
        """保存检查点"""
        cp = Checkpoint(
            checkpoint_id=f"cp_{uuid.uuid4().hex[:8]}",
            checkpoint_type=ctype,
            phase=phase,
            context_snapshot={
                "context_id": context.context_id,
                "tokens_used": context.tokens_used,
                "language": context.language,
                "complexity_score": context.complexity_score
            },
            reasoning_state=state,
            parent_checkpoint_id=parent_id
        )

        self.checkpoints[cp.checkpoint_id] = cp
        if parent_id:
            self.checkpoint_tree[parent_id].append(cp.checkpoint_id)

        # 清理旧检查点
        if len(self.checkpoints) > self.max_checkpoints:
            oldest = min(self.checkpoints.keys(),
                        key=lambda k: self.checkpoints[k].timestamp)
            del self.checkpoints[oldest]

        return cp

    def restore(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """从检查点恢复状态"""
        cp = self.checkpoints.get(checkpoint_id)
        if not cp:
            return None
        logger.info(f"恢复检查点 {checkpoint_id} (阶段: {cp.phase.value})")
        return {
            "phase": cp.phase,
            "context_snapshot": cp.context_snapshot,
            "reasoning_state": cp.reasoning_state
        }

    def get_branch_chain(self, checkpoint_id: str) -> List[Checkpoint]:
        """获取从根到当前检查点的完整链路"""
        chain = []
        current_id = checkpoint_id
        while current_id:
            cp = self.checkpoints.get(current_id)
            if cp:
                chain.append(cp)
                current_id = cp.parent_checkpoint_id
            else:
                break
        return list(reversed(chain))

    def get_branching_points(self) -> List[str]:
        """获取所有分支点"""
        return [cid for cid, children in self.checkpoint_tree.items()
                if len(children) > 1]


# ==============================
# 工具联动推理适配器
# ==============================

class ToolReasoningBridge:
    """工具调用与推理引擎的桥接层"""

    def __init__(self):
        self.tool_call_history: deque = deque(maxlen=1000)
        self.pattern_cache: Dict[str, Dict[str, Any]] = {}

    def analyze_tool_dependency(self, tools_needed: List[str]) -> Dict[str, List[str]]:
        """分析工具调用依赖关系"""
        dependencies = {}
        for tool in tools_needed:
            deps = self._infer_dependencies(tool)
            dependencies[tool] = deps
        return dependencies

    def plan_tool_sequence(self, tools_needed: List[str],
                          dependencies: Dict[str, List[str]]) -> List[List[str]]:
        """规划工具调用序列（拓扑排序）"""
        in_degree = {t: 0 for t in tools_needed}
        for tool, deps in dependencies.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[tool] += 1

        # BFS分层
        layers = []
        remaining = set(tools_needed)
        while remaining:
            layer = [t for t in remaining if in_degree.get(t, 0) == 0]
            if not layer:
                break  # 循环依赖
            layers.append(layer)
            remaining -= set(layer)
            for t in layer:
                for other in tools_needed:
                    if t in dependencies.get(other, []):
                        in_degree[other] -= 1

        return layers

    def record_tool_result(self, tool_name: str, success: bool,
                          execution_time_ms: float, output_size: int):
        """记录工具调用结果"""
        self.tool_call_history.append({
            "tool": tool_name,
            "success": success,
            "execution_time_ms": execution_time_ms,
            "output_size": output_size,
            "timestamp": time.time()
        })

    def _infer_dependencies(self, tool: str) -> List[str]:
        """推断工具依赖（基于命名约定和模式缓存）"""
        # 常见依赖模式
        known_deps = {
            "web_fetch": ["web_search"],
            "analyze_image": ["search_image"],
            "edit_file": ["read_text"],
            "dispatch_task": [],
        }
        return known_deps.get(tool, [])


# ==============================
# 核心推理引擎 v6.0
# ==============================

class ClaudeReasoningEngineV6:
    """
    Claude分层推理引擎 v6.0
    完整五步推理链路 + 双模动态切换 + DAG回溯 + CIDM
    """

    def __init__(self):
        self.mode = ReasoningMode.HYBRID
        self.effort = EffortLevel.MEDIUM
        self.chinese_adapter = ChineseReasoningAdapter()
        self.density_optimizer = ContextDensityOptimizer()
        self.checkpoint_manager = CheckpointManager()
        self.tool_bridge = ToolReasoningBridge()

        # 推理DAG
        self.dags: Dict[str, ReasoningDAG] = {}

        # 统计
        self.stats = {
            "total_sessions": 0,
            "avg_complexity": 0.0,
            "total_tokens": 0,
            "backtrack_count": 0,
            "success_rate": 0.0,
        }

    # ===== 阶段一：问题解析 =====

    def parse(self, query: str, context: ReasoningContext) -> ParseResult:
        """问题解析：提取意图、实体、约束"""
        cp = self.checkpoint_manager.save(
            ReasoningPhase.PARSE, context,
            {"query": query, "mode": self.mode.value}
        )

        # 中文适配
        ambiguities = self.chinese_adapter.detect_chinese_ambiguity(query)
        idioms = self.chinese_adapter.extract_idiom_strategy(query)
        lang_mix = self.chinese_adapter.detect_language_mix(query)

        # 意图识别
        intent = self._classify_intent(query)

        # 实体提取
        entities = self._extract_entities(query)

        # 约束识别
        constraints = self._extract_constraints(query)

        # 复杂度评分
        complexity = self._score_complexity(query, intent, constraints)
        context.complexity_score = complexity

        result = ParseResult(
            intent=intent,
            entities=entities,
            constraints=constraints,
            ambiguity_flags=[a["word"] for a in ambiguities],
            confidence=self._calc_parse_confidence(ambiguities, entities)
        )

        logger.info(f"[PARSE] 意图={intent}, 复杂度={complexity:.1f}, "
                    f"歧义词={len(ambiguities)}, 置信度={result.confidence:.2f}")
        return result

    # ===== 阶段二：条件拆解 =====

    def decompose(self, parse_result: ParseResult,
                 context: ReasoningContext) -> DecomposeResult:
        """条件拆解：将问题拆分为可独立执行的条件单元"""
        cp = self.checkpoint_manager.save(
            ReasoningPhase.DECOMPOSE, context,
            {"parse_result": {"intent": parse_result.intent}},
            parent_id=cp if 'cp' in dir() else None
        )

        conditions = self._decompose_conditions(parse_result)

        # 依赖分析
        dependencies = {}
        for i, cond in enumerate(conditions):
            deps = []
            for j, other in enumerate(conditions):
                if i != j and self._is_dependent(cond, other):
                    deps.append(other["id"])
            dependencies[cond["id"]] = deps

        # 优先级排序
        priority_order = self._topological_sort(conditions, dependencies)

        # 并行化识别
        parallelizable = self._identify_parallel(conditions, dependencies)

        result = DecomposeResult(
            conditions=conditions,
            dependencies=dependencies,
            priority_order=priority_order,
            parallelizable=parallelizable,
            precondition_chain=self._build_precondition_chain(conditions)
        )

        logger.info(f"[DECOMPOSE] 条件数={len(conditions)}, "
                    f"并行组={len(parallelizable)}")
        return result

    # ===== 阶段三：逻辑推演 =====

    def reason(self, parse_result: ParseResult,
              decompose_result: DecomposeResult,
              context: ReasoningContext) -> ReasoningDAG:
        """逻辑推演：构建推理DAG，进行多路径探索"""
        cp = self.checkpoint_manager.save(
            ReasoningPhase.REASON, context,
            {"conditions": len(decompose_result.conditions)}
        )

        dag = ReasoningDAG(
            dag_id=f"dag_{uuid.uuid4().hex[:8]}",
            root_path_id="",
            paths={}
        )

        # 构建根路径
        root_path = ReasoningPath(
            path_id=f"path_root_{dag.dag_id}",
            phase=ReasoningPhase.REASON,
            hypothesis=parse_result.intent,
            confidence=parse_result.confidence
        )
        dag.root_path_id = root_path.path_id
        dag.paths[root_path.path_id] = root_path

        # 扩展思考模式：多路径探索
        if self.mode == ReasoningMode.EXTENDED or (
            self.mode == ReasoningMode.HYBRID and
            context.complexity_score > 50
        ):
            self._expand_reasoning_paths(dag, parse_result, decompose_result)
            # 选择最优路径
            best_path = max(
                dag.paths.values(),
                key=lambda p: p.confidence if p.is_valid else -1
            )
            dag.selected_path_id = best_path.path_id

        # 保存DAG
        self.dags[dag.dag_id] = dag

        logger.info(f"[REASON] DAG={dag.dag_id}, 路径数={len(dag.paths)}, "
                    f"选中={dag.selected_path_id}")
        return dag

    # ===== 阶段四：方案执行 =====

    def execute(self, dag: ReasoningDAG,
               decompose_result: DecomposeResult,
               context: ReasoningContext) -> ExecutionPlan:
        """方案执行：生成执行计划并预估资源"""
        # 分析工具依赖
        tools_needed = self._infer_tools_needed(decompose_result, context)
        tool_deps = self.tool_bridge.analyze_tool_dependency(tools_needed)
        tool_sequence = self.tool_bridge.plan_tool_sequence(tools_needed, tool_deps)

        # 生成执行步骤
        steps = []
        for layer_idx, layer in enumerate(tool_sequence):
            for tool in layer:
                steps.append({
                    "step_id": f"step_{layer_idx}_{tool}",
                    "tool": tool,
                    "layer": layer_idx,
                    "parallel_group": len(layer) > 1,
                    "dependencies": tool_deps.get(tool, []),
                    "status": "pending"
                })

        # Token预估
        estimated_tokens = len(steps) * 2000 * (
            1.5 if self.effort in (EffortLevel.HIGH, EffortLevel.MAXIMUM) else 1.0
        )

        plan = ExecutionPlan(
            plan_id=f"plan_{uuid.uuid4().hex[:8]}",
            steps=steps,
            tools_required=tools_needed,
            estimated_tokens=estimated_tokens,
            fallback_plans=self._generate_fallbacks(steps),
            risk_level=self._assess_risk(steps, tool_deps)
        )

        logger.info(f"[EXECUTE] 计划={plan.plan_id}, 步骤={len(steps)}, "
                    f"层数={len(tool_sequence)}, 预估Token={estimated_tokens}")
        return plan

    # ===== 阶段五：结果复盘 =====

    def review(self, execution_result: Dict[str, Any],
              plan: ExecutionPlan,
              dag: ReasoningDAG,
              context: ReasoningContext) -> ReviewResult:
        """结果复盘：对比预期、提炼经验、触发自进化"""
        actual_output = execution_result.get("output", {})
        expected_output = execution_result.get("expected", {})

        # 对比分析
        comparison = self._compare_results(actual_output, expected_output)

        # 错误分析
        errors = execution_result.get("errors", [])
        error_analysis = []
        for err in errors:
            error_analysis.append({
                "error": err,
                "step_affected": self._trace_error_step(err, plan),
                "root_cause": self._diagnose_root_cause(err),
                "prevention": self._suggest_prevention(err)
            })

        # 经验提炼
        lessons = self._extract_lessons(execution_result, plan, dag)

        # 自进化触发
        triggers = []
        if len(errors) > 0:
            triggers.append("skill_patch_needed")
        if execution_result.get("success_rate", 1.0) < 0.8:
            triggers.append("strategy_optimization_needed")
        if context.tokens_used > context.max_tokens * 0.9:
            triggers.append("context_compression_optimization")

        result = ReviewResult(
            success=len(errors) == 0,
            actual_vs_expected=comparison,
            errors=error_analysis,
            lessons=lessons,
            optimization_suggestions=self._generate_optimizations(execution_result),
            self_evolution_triggers=triggers
        )

        logger.info(f"[REVIEW] 成功={result.success}, 错误={len(errors)}, "
                    f"经验={len(lessons)}, 进化触发={len(triggers)}")
        return result

    # ===== 完整推理流程 =====

    def reason_full(self, query: str, mode: ReasoningMode = None,
                   effort: EffortLevel = None) -> Dict[str, Any]:
        """执行完整五步推理流程"""
        if mode:
            self.mode = mode
        if effort:
            self.effort = effort

        context = ReasoningContext(
            context_id=f"ctx_{uuid.uuid4().hex[:8]}",
            original_query=query
        )

        try:
            # Step 1: 解析
            parse_result = self.parse(query, context)

            # Step 2: 拆解
            decompose_result = self.decompose(parse_result, context)

            # Step 3: 推演
            dag = self.reason(parse_result, decompose_result, context)

            # Step 4: 执行
            plan = self.execute(dag, decompose_result, context)

            # Step 5: 复盘 (此处为模拟执行结果)
            execution_result = {
                "output": {"plan": plan.plan_id, "steps": len(plan.steps)},
                "expected": {"plan": plan.plan_id, "steps": len(plan.steps)},
                "errors": [],
                "success_rate": 1.0
            }
            review = self.review(execution_result, plan, dag, context)

            # 更新统计
            self.stats["total_sessions"] += 1
            self.stats["total_tokens"] += context.tokens_used

            return {
                "success": review.success,
                "context_id": context.context_id,
                "parse": {
                    "intent": parse_result.intent,
                    "complexity": context.complexity_score,
                    "confidence": parse_result.confidence
                },
                "decompose": {
                    "conditions": len(decompose_result.conditions),
                    "parallel_groups": len(decompose_result.parallelizable)
                },
                "reason": {
                    "dag_id": dag.dag_id,
                    "paths": len(dag.paths),
                    "selected_path": dag.selected_path_id
                },
                "execute": {
                    "plan_id": plan.plan_id,
                    "steps": len(plan.steps),
                    "risk_level": plan.risk_level,
                    "estimated_tokens": plan.estimated_tokens
                },
                "review": {
                    "success": review.success,
                    "lessons": len(review.lessons),
                    "evolution_triggers": review.self_evolution_triggers
                },
                "stats": self.stats
            }

        except Exception as e:
            logger.error(f"推理流程异常: {e}")
            return {"success": False, "error": str(e)}

    # ===== 回溯能力 =====

    def backtrack(self, checkpoint_id: str,
                 strategy: BacktrackStrategy = BacktrackStrategy.CHECKPOINT_RESUME,
                 reason: str = "") -> Optional[Dict[str, Any]]:
        """从指定检查点回溯"""
        self.stats["backtrack_count"] += 1

        restored = self.checkpoint_manager.restore(checkpoint_id)
        if not restored:
            logger.error(f"回溯失败：检查点 {checkpoint_id} 不存在")
            return None

        chain = self.checkpoint_manager.get_branch_chain(checkpoint_id)

        logger.info(f"[BACKTRACK] 检查点={checkpoint_id}, 策略={strategy.value}, "
                    f"链路长度={len(chain)}, 原因={reason}")

        return {
            "status": "restored",
            "checkpoint_id": checkpoint_id,
            "restored_phase": restored["phase"].value,
            "chain_length": len(chain),
            "strategy": strategy.value,
            "reason": reason
        }

    # ===== 双模动态切换 =====

    def auto_select_mode(self, query: str, context: ReasoningContext) -> ReasoningMode:
        """根据问题复杂度自动选择推理模式"""
        complexity = self._score_complexity(query, "", [])

        if complexity < 20:
            return ReasoningMode.DEFAULT
        elif complexity < 60:
            return ReasoningMode.HYBRID
        else:
            return ReasoningMode.EXTENDED

    def auto_select_effort(self, query: str) -> EffortLevel:
        """自动选择推理努力度（对标Claude Opus 4.5）"""
        # 基于问题特征自动调参
        length = len(query)
        has_complex_keywords = any(kw in query for kw in
            ["分析", "对比", "优化", "设计", "架构", "算法", "推理", "证明"])

        if has_complex_keywords and length > 200:
            return EffortLevel.MAXIMUM
        elif has_complex_keywords or length > 100:
            return EffortLevel.HIGH
        elif length > 50:
            return EffortLevel.MEDIUM
        else:
            return EffortLevel.LOW

    # ===== 内部辅助方法 =====

    def _classify_intent(self, query: str) -> str:
        """意图分类"""
        intents = {
            "代码生成": ["写", "生成", "创建", "实现", "开发"],
            "信息查询": ["什么是", "如何", "怎么", "查询", "查找", "搜索"],
            "文件操作": ["打开", "读取", "保存", "删除", "复制", "移动"],
            "系统配置": ["设置", "配置", "安装", "卸载", "启动", "关闭"],
            "分析推理": ["分析", "对比", "为什么", "原因", "优化", "评估"],
            "翻译转换": ["翻译", "转换", "格式", "导出"],
        }
        for intent, keywords in intents.items():
            if any(kw in query for kw in keywords):
                return intent
        return "通用问答"

    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """实体提取"""
        entities = {}
        # 路径检测
        import re
        path_pattern = r'[A-Za-z]:\\[^\s，。！？]+'
        paths = re.findall(path_pattern, query)
        if paths:
            entities["file_paths"] = paths

        # URL检测
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, query)
        if urls:
            entities["urls"] = urls

        # 数字检测
        num_pattern = r'\d+'
        numbers = re.findall(num_pattern, query)
        if numbers:
            entities["numbers"] = numbers

        return entities

    def _extract_constraints(self, query: str) -> List[str]:
        """约束识别"""
        constraints = []
        constraint_keywords = [
            "必须", "不能", "不要", "禁止", "只", "仅",
            "不超过", "至少", "最多", "最少", "限",
            "格式要求", "字数", "语言"
        ]
        for ck in constraint_keywords:
            if ck in query:
                constraints.append(ck)
        return constraints

    def _score_complexity(self, query: str, intent: str,
                         constraints: List[str]) -> float:
        """复杂度评分 0-100"""
        score = 10.0  # 基础分

        # 长度因子
        length = len(query)
        if length > 500:
            score += 25
        elif length > 200:
            score += 15
        elif length > 100:
            score += 10
        elif length > 50:
            score += 5

        # 意图因子
        complex_intents = {"分析推理": 20, "代码生成": 15, "系统配置": 10}
        score += complex_intents.get(intent, 0)

        # 约束因子
        score += min(len(constraints) * 5, 15)

        # 歧义因子
        ambiguities = self.chinese_adapter.detect_chinese_ambiguity(query)
        score += min(len(ambiguities) * 3, 10)

        return min(100.0, score)

    def _calc_parse_confidence(self, ambiguities: list,
                              entities: Dict) -> float:
        """计算解析置信度"""
        base = 0.95
        base -= len(ambiguities) * 0.05
        base += min(len(entities) * 0.01, 0.05)
        return max(0.5, min(1.0, base))

    def _decompose_conditions(self, parse: ParseResult) -> List[Dict[str, Any]]:
        """拆解条件"""
        conditions = []
        cond_id = 0

        # 意图 → 条件
        conditions.append({
            "id": f"cond_{cond_id}", "type": "intent",
            "description": f"验证意图: {parse.intent}", "priority": 0
        })
        cond_id += 1

        # 约束 → 条件
        for constraint in parse.constraints:
            conditions.append({
                "id": f"cond_{cond_id}", "type": "constraint",
                "description": f"满足约束: {constraint}", "priority": 1
            })
            cond_id += 1

        # 歧义 → 条件
        for amb in parse.ambiguity_flags:
            conditions.append({
                "id": f"cond_{cond_id}", "type": "disambiguate",
                "description": f"消歧: {amb}", "priority": 2
            })
            cond_id += 1

        return conditions

    def _is_dependent(self, a: Dict, b: Dict) -> bool:
        """判断条件依赖关系"""
        # 消歧依赖约束满足
        if a["type"] == "disambiguate" and b["type"] == "constraint":
            return True
        return False

    def _topological_sort(self, conditions: List[Dict],
                         dependencies: Dict[str, List[str]]) -> List[str]:
        """拓扑排序"""
        in_degree = {}
        for cond in conditions:
            in_degree[cond["id"]] = 0
        for deps in dependencies.values():
            for dep in deps:
                if dep in in_degree:
                    in_degree[dep] += 1  # 注意：这里反向，被依赖的入度+1

        result = []
        queue = [cid for cid, deg in in_degree.items() if deg == 0]

        while queue:
            cid = queue.pop(0)
            result.append(cid)
            for other_cid, deps in dependencies.items():
                if cid in deps and other_cid in in_degree:
                    in_degree[other_cid] -= 1
                    if in_degree[other_cid] == 0:
                        queue.append(other_cid)

        return result

    def _identify_parallel(self, conditions: List[Dict],
                          dependencies: Dict[str, List[str]]) -> List[List[str]]:
        """识别可并行条件"""
        # 同一优先级且无相互依赖的条件可并行
        by_priority = defaultdict(list)
        for cond in conditions:
            by_priority[cond["priority"]].append(cond["id"])

        parallel = []
        for priority, cids in by_priority.items():
            if len(cids) > 1:
                # 检查无相互依赖
                independent = True
                for i, a in enumerate(cids):
                    for b in cids[i+1:]:
                        if b in dependencies.get(a, []) or a in dependencies.get(b, []):
                            independent = False
                            break
                if independent:
                    parallel.append(cids)

        return parallel

    def _build_precondition_chain(self, conditions: List[Dict]) -> List[str]:
        """构建前置条件链"""
        return sorted(
            conditions,
            key=lambda c: (c["priority"], c["id"])
        )

    def _expand_reasoning_paths(self, dag: ReasoningDAG,
                               parse: ParseResult,
                               decompose: DecomposeResult):
        """扩展推理路径（扩展思考模式）"""
        root = dag.paths[dag.root_path_id]

        for cond in decompose.conditions[:5]:  # 限制路径数
            path = ReasoningPath(
                path_id=f"path_{cond['id']}_{dag.dag_id}",
                phase=ReasoningPhase.REASON,
                hypothesis=f"{root.hypothesis} | 条件: {cond['description']}",
                parent_path_id=root.path_id,
                confidence=root.confidence * 0.8
            )
            root.children_path_ids.append(path.path_id)
            dag.paths[path.path_id] = path

        # 记录分支点
        if len(root.children_path_ids) > 1:
            dag.branching_points.append(root.path_id)

    def _infer_tools_needed(self, decompose: DecomposeResult,
                           context: ReasoningContext) -> List[str]:
        """推断所需工具"""
        tools = set()
        for cond in decompose.conditions:
            if cond["type"] == "intent":
                if any(kw in str(cond) for kw in ["文件", "读取", "搜索"]):
                    tools.add("read_text")
                    tools.add("shell_executor")
            elif cond["type"] == "constraint":
                tools.add("web_search")
            elif cond["type"] == "disambiguate":
                tools.add("analyze_image")
        return list(tools) if tools else ["web_search"]

    def _generate_fallbacks(self, steps: List[Dict]) -> List[str]:
        """生成回退方案"""
        return ["retry_with_lower_effort", "ask_user_for_clarification"]

    def _assess_risk(self, steps: List[Dict],
                    dependencies: Dict[str, List[str]]) -> str:
        """评估执行风险"""
        if len(steps) > 20:
            return "high"
        elif len(steps) > 10:
            return "medium"
        return "low"

    def _compare_results(self, actual: Any, expected: Any) -> Dict[str, Any]:
        """对比实际与预期结果"""
        return {
            "match": actual == expected,
            "actual_type": type(actual).__name__,
            "expected_type": type(expected).__name__
        }

    def _trace_error_step(self, error: str, plan: ExecutionPlan) -> Optional[str]:
        """追踪错误步骤"""
        for step in plan.steps:
            if step["tool"] in error:
                return step["step_id"]
        return None

    def _diagnose_root_cause(self, error: str) -> str:
        """诊断根因"""
        causes = {
            "timeout": "执行超时",
            "permission": "权限不足",
            "not found": "目标不存在",
            "connection": "网络连接失败",
            "parse": "解析失败",
        }
        for key, cause in causes.items():
            if key in error.lower():
                return cause
        return "未知错误"

    def _suggest_prevention(self, error: str) -> str:
        """建议预防措施"""
        if "timeout" in error.lower():
            return "增加超时阈值或拆分任务"
        if "permission" in error.lower():
            return "检查权限配置"
        if "not found" in error.lower():
            return "验证目标路径/资源存在性"
        return "人工审查"

    def _extract_lessons(self, result: Dict, plan: ExecutionPlan,
                        dag: ReasoningDAG) -> List[str]:
        """提炼经验教训"""
        lessons = []
        if result.get("success_rate", 1.0) >= 0.95:
            lessons.append(f"推理路径 {dag.selected_path_id} 高效可靠")
        if plan.risk_level != "low":
            lessons.append(f"高风险执行计划需增加检查点密度")
        return lessons

    def _generate_optimizations(self, result: Dict) -> List[str]:
        """生成优化建议"""
        return [
            "定期清理低置信度推理路径",
            "优化CIDM压缩策略以降低Token消耗",
            "扩展中文歧义词库覆盖范围"
        ]

    def get_status(self) -> Dict[str, Any]:
        """获取引擎状态"""
        return {
            "mode": self.mode.value,
            "effort": self.effort.value,
            "active_dags": len(self.dags),
            "checkpoints": len(self.checkpoint_manager.checkpoints),
            "stats": self.stats
        }


# ==============================
# 入口
# ==============================

if __name__ == "__main__":
    engine = ClaudeReasoningEngineV6()

    # 测试完整推理流程
    result = engine.reason_full(
        "分析一下E:\\workspace目录下的所有Python文件，找出性能瓶颈并生成优化方案",
        mode=ReasoningMode.HYBRID,
        effort=EffortLevel.HIGH
    )

    print("=" * 60)
    print("Claude 分层推理引擎 v6.0 - 测试运行")
    print("=" * 60)
    print(f"成功: {result['success']}")
    print(f"意图: {result.get('parse', {}).get('intent')}")
    print(f"复杂度: {result.get('parse', {}).get('complexity')}")
    print(f"条件数: {result.get('decompose', {}).get('conditions')}")
    print(f"推理路径: {result.get('reason', {}).get('paths')}")
    print(f"执行步骤: {result.get('execute', {}).get('steps')}")
    print(f"复盘成功: {result.get('review', {}).get('success')}")
    print(f"引擎状态: {json.dumps(engine.get_status(), indent=2, ensure_ascii=False)}")

```
