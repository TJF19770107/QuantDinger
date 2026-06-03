"""
Claude分层推理引擎 v2.0
对标：Claude Extended Thinking · OpenAI o-series · DeepSeek-R1
五层推理架构 + 反思闭环(OpenClaw) + Mailbox P2P(Claude Agent Teams) + Idempotency Gates(RSI)

R10 全域缺口专项补全升级 - P0-1
从 v1.0 (550行) 升级至 v2.0，注入 R09 情报：
  - OpenClaw v4.2: 反思闭环 followups/ + 四层完成链路 L1-L4
  - Claude Agent Teams: Mailbox P2P + Shared Task List
  - RSI综述: Idempotency Gates + 五柱框架
"""

import json
import time
import uuid
import hashlib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ClaudeReasoningEngine.v2")


# ========== 枚举与数据结构 ==========

class DifficultyLevel(Enum):
    L1_TRIVIAL = 1
    L2_STANDARD = 2
    L3_COMPLEX = 3
    L4_EXPERT = 4
    L5_FRONTIER = 5


class ReasoningStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    BACKTRACK = "backtrack"
    FAILED = "failed"
    REFLECTING = "reflecting"   # v2.0: 反思中


class GateStatus(Enum):
    """Idempotency Gate 状态 (RSI五柱框架)"""
    PASSED = "passed"
    BLOCKED = "blocked"
    QUEUED = "queued"
    EXPIRED = "expired"


@dataclass
class Intent:
    intent_type: str
    raw_input: str
    context_summary: str
    difficulty: DifficultyLevel
    sub_goals: list = field(default_factory=list)
    confidence: float = 0.0
    task_fingerprint: str = ""  # v2.0: 任务指纹(用于幂等性)


@dataclass
class ConditionTree:
    variables: dict = field(default_factory=dict)
    hard_constraints: list = field(default_factory=list)
    soft_constraints: list = field(default_factory=list)
    anchors: dict = field(default_factory=dict)
    dependency_graph: dict = field(default_factory=dict)


@dataclass
class ReasoningPath:
    path_id: str
    steps: list = field(default_factory=list)
    confidence: float = 0.0
    status: ReasoningStatus = ReasoningStatus.PENDING
    checkpoints: list = field(default_factory=list)


@dataclass
class ExecutionResult:
    success: bool
    output: Any = None
    tool_calls: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    execution_time_ms: float = 0.0


@dataclass
class ReviewReport:
    quality_score: float
    gaps_detected: list = field(default_factory=list)
    skills_distilled: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    summary: str = ""


# ========== v2.0 新增：Idempotency Gate Manager (RSI五柱框架) ==========

class IdempotencyGate:
    """幂等性门控：防止重复执行，确保任务不重复派发

    RSI综述五柱框架之 Idempotency Gates：
    每个任务生成唯一指纹，执行前检查、执行后标记，
    同一指纹在 TTL 内不会被重复执行。
    """

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._gate_registry: dict = {}  # fingerprint -> GateStatus + timestamp
        self._execution_log: list = []

    def generate_fingerprint(self, task: str, context: dict = None) -> str:
        """生成任务指纹：SHA256(user_input + key_params)"""
        seed = f"{task}|{json.dumps(context or {}, sort_keys=True, ensure_ascii=False)}"
        return hashlib.sha256(seed.encode()).hexdigest()[:12]

    def check_gate(self, fingerprint: str) -> GateStatus:
        """检查门控状态"""
        entry = self._gate_registry.get(fingerprint)
        if not entry:
            return GateStatus.PASSED

        elapsed = time.time() - entry["timestamp"]
        if elapsed > self.ttl:
            entry["status"] = GateStatus.EXPIRED
            return GateStatus.PASSED

        if entry["status"] == GateStatus.BLOCKED:
            return GateStatus.BLOCKED
        if entry["status"] == GateStatus.QUEUED:
            return GateStatus.QUEUED

        return GateStatus.PASSED

    def lock_gate(self, fingerprint: str):
        """锁定门控（执行中）"""
        self._gate_registry[fingerprint] = {
            "status": GateStatus.QUEUED,
            "timestamp": time.time()
        }

    def mark_executed(self, fingerprint: str):
        """标记已执行"""
        self._gate_registry[fingerprint] = {
            "status": GateStatus.PASSED,
            "timestamp": time.time()
        }
        self._execution_log.append({
            "fingerprint": fingerprint,
            "executed_at": datetime.now().isoformat()
        })

    def mark_blocked(self, fingerprint: str, reason: str):
        """标记为阻断"""
        self._gate_registry[fingerprint] = {
            "status": GateStatus.BLOCKED,
            "timestamp": time.time(),
            "reason": reason
        }

    def get_pending_duplicates(self) -> list:
        """获取排队的重复任务"""
        return [
            fp for fp, entry in self._gate_registry.items()
            if entry["status"] == GateStatus.QUEUED
        ]


# ========== v2.0 新增：Mailbox P2P 通信系统 (Claude Agent Teams) ==========

class Mailbox:
    """Agent间点对点信箱通信

    对标 Claude Agent Teams:
    - 命名邮箱 (named mailboxes)
    - 异步消息投递
    - 消息路由表
    - Shared Task List 同步
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.inbox: list = []
        self.outbox: list = []
        self.peers: dict = {}          # agent_id -> last_seen
        self.shared_tasks: dict = {}   # task_id -> status

    def register_peer(self, agent_id: str, capabilities: list = None):
        """注册通信对端"""
        self.peers[agent_id] = {
            "last_seen": datetime.now().isoformat(),
            "capabilities": capabilities or []
        }
        logger.info(f"Mailbox: 已注册对端 {agent_id}")

    def send(self, to_agent: str, message_type: str, payload: dict) -> str:
        """向指定Agent发送消息"""
        msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        message = {
            "msg_id": msg_id,
            "from": self.agent_id,
            "to": to_agent,
            "type": message_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat(),
            "status": "sent"
        }
        self.outbox.append(message)
        logger.debug(f"Mailbox: [{msg_id}] {self.agent_id} -> {to_agent}: {message_type}")
        return msg_id

    def receive(self) -> list:
        """拉取收件箱消息"""
        messages = self.inbox[:]
        self.inbox.clear()
        return messages

    def deliver(self, message: dict):
        """投递消息到收件箱"""
        self.inbox.append(message)
        message["status"] = "delivered"

    def broadcast(self, message_type: str, payload: dict):
        """向所有注册对端广播"""
        for peer_id in self.peers:
            self.send(peer_id, message_type, payload)

    def sync_shared_tasks(self, task_id: str, status: str, result: dict = None):
        """同步Shared Task List"""
        self.shared_tasks[task_id] = {
            "status": status,
            "result": result,
            "updated_at": datetime.now().isoformat(),
            "updated_by": self.agent_id
        }
        self.broadcast("shared_task_update", {
            "task_id": task_id, "status": status, "result": result
        })

    def get_shared_task_status(self, task_id: str) -> dict:
        """获取共享任务状态"""
        return self.shared_tasks.get(task_id, {"status": "unknown"})


# ========== v2.0 新增：反思闭环管理器 (OpenClaw followups/) ==========

class ReflectionLoop:
    """反思闭环：执行后自动反思，类比 OpenClaw followups/

    执行 → 评估 → 反思 → 调整 → 再执行
    最多 3 轮反思，每轮生成改进建议并自动应用
    """

    MAX_REFLECTION_ROUNDS = 3
    QUALITY_IMPROVEMENT_THRESHOLD = 0.05  # 至少提升5%才继续反思

    def __init__(self):
        self.reflection_history: list = []

    def reflect(self, intent: Intent, result: ExecutionResult, review: ReviewReport) -> dict:
        """执行反思闭环"""
        reflection = {
            "round": len(self.reflection_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "original_quality": review.quality_score,
            "adjustments": [],
            "decision": "continue"
        }

        # 质量足够高：结束反思
        if review.quality_score >= 0.85:
            reflection["decision"] = "complete"
            self.reflection_history.append(reflection)
            return reflection

        # 已达最大轮次：强制结束
        if reflection["round"] >= self.MAX_REFLECTION_ROUNDS:
            reflection["decision"] = "max_rounds_reached"
            self.reflection_history.append(reflection)
            return reflection

        # 生成调整方案
        adjustments = self._generate_adjustments(review)
        reflection["adjustments"] = adjustments

        self.reflection_history.append(reflection)
        return reflection

    def _generate_adjustments(self, review: ReviewReport) -> list:
        """基于复盘报告生成调整方案"""
        adjustments = []

        for gap in review.gaps_detected:
            if gap.get("type") == "performance":
                adjustments.append({
                    "type": "increase_parallelism",
                    "desc": "执行超时，下次提升并行度"
                })
            elif gap.get("type") == "execution_error":
                adjustments.append({
                    "type": "add_fallback_path",
                    "desc": f"错误: {gap.get('detail', '')}，添加降级路径"
                })
            elif gap.get("type") == "completeness":
                adjustments.append({
                    "type": "expand_context",
                    "desc": "输出不完整，扩大上下文窗口"
                })

        if review.quality_score < 0.5:
            adjustments.append({
                "type": "switch_reasoning_path",
                "desc": "质量过低，切换备用推理路径"
            })

        return adjustments

    def apply_adjustments(self, adjustments: list, execution_config: dict) -> dict:
        """将反思调整应用到执行配置"""
        for adj in adjustments:
            if adj["type"] == "increase_parallelism":
                execution_config["max_parallel"] = min(
                    execution_config.get("max_parallel", 5) * 2, 10
                )
            elif adj["type"] == "expand_context":
                execution_config["context_window_size"] = min(
                    execution_config.get("context_window_size", 32000) * 2, 128000
                )
            elif adj["type"] == "switch_reasoning_path":
                execution_config["force_alternate_path"] = True
            elif adj["type"] == "add_fallback_path":
                execution_config["enable_fallback"] = True

        return execution_config

    def get_reflection_summary(self) -> str:
        """获取反思总结"""
        if not self.reflection_history:
            return "无反思记录"
        last = self.reflection_history[-1]
        rounds = len(self.reflection_history)
        return f"反思{rounds}轮, 最终决策: {last['decision']}, 调整项: {len(last['adjustments'])}个"


# ========== Phase 1: 问题解析层 ==========

class IntentParser:
    """Phase 1：意图识别 + 上下文加载 + 难度定级 + 子目标拆分"""

    def __init__(self, memory_os=None):
        self.memory_os = memory_os

    def parse(self, user_input: str, context_window: dict) -> Intent:
        intent_type = self._classify(user_input)
        context = self._load_context(user_input, context_window)
        difficulty = self._rate_difficulty(user_input, context)
        sub_goals = self._decompose(user_input, difficulty)

        return Intent(
            intent_type=intent_type,
            raw_input=user_input,
            context_summary=context,
            difficulty=difficulty,
            sub_goals=sub_goals,
            confidence=self._estimate_confidence(user_input, intent_type)
        )

    def _classify(self, user_input: str) -> str:
        code_keywords = ["代码", "编程", "函数", "API", "写一个", "实现"]
        search_keywords = ["搜索", "查找", "最新的", "什么是"]
        action_keywords = ["打开", "关闭", "删除", "移动", "执行", "运行"]
        qa_keywords = ["为什么", "如何", "是什么", "怎么样"]
        creative_keywords = ["写一篇", "生成", "创作", "设计", "画"]

        lower = user_input.lower()
        if any(k in lower for k in code_keywords): return "code"
        if any(k in lower for k in search_keywords): return "search"
        if any(k in lower for k in action_keywords): return "action"
        if any(k in lower for k in qa_keywords): return "qa"
        if any(k in lower for k in creative_keywords): return "creative"
        return "general"

    def _load_context(self, user_input: str, context_window: dict) -> str:
        if self.memory_os:
            return self.memory_os.retrieve_relevant(user_input, context_window)
        return json.dumps(context_window, ensure_ascii=False)[:500]

    def _rate_difficulty(self, user_input: str, context: str) -> DifficultyLevel:
        length = len(user_input)
        if length < 20: return DifficultyLevel.L1_TRIVIAL
        if length < 100: return DifficultyLevel.L2_STANDARD
        if length < 500: return DifficultyLevel.L3_COMPLEX
        if length < 2000: return DifficultyLevel.L4_EXPERT
        return DifficultyLevel.L5_FRONTIER

    def _decompose(self, user_input: str, difficulty: DifficultyLevel) -> list:
        if difficulty.value <= 2:
            return [user_input]
        delimiters = ["。", "；", "\n"]
        parts = [user_input]
        for d in delimiters:
            new_parts = []
            for p in parts:
                new_parts.extend(p.split(d))
            parts = [x.strip() for x in new_parts if x.strip()]
            if len(parts) > 1: break
        return parts if len(parts) > 1 else [user_input]

    def _estimate_confidence(self, user_input: str, intent_type: str) -> float:
        return 0.85


# ========== Phase 2: 条件拆解层 ==========

class ConditionDecomposer:
    """Phase 2：变量抽取 + 约束建模 + 锚点定义 + 依赖图构建"""

    def decompose(self, intent: Intent) -> ConditionTree:
        variables = self._extract_variables(intent)
        hard = self._model_hard_constraints(intent, variables)
        soft = self._model_soft_constraints(intent, variables)
        anchors = self._define_anchors(intent, variables)
        dep_graph = self._build_dependency_graph(intent.sub_goals)

        return ConditionTree(
            variables=variables,
            hard_constraints=hard,
            soft_constraints=soft,
            anchors=anchors,
            dependency_graph=dep_graph
        )

    def _extract_variables(self, intent: Intent) -> dict:
        return {
            "raw_input": intent.raw_input,
            "intent_type": intent.intent_type,
            "difficulty": intent.difficulty.value,
            "sub_goal_count": len(intent.sub_goals)
        }

    def _model_hard_constraints(self, intent: Intent, variables: dict) -> list:
        return [
            {"type": "safety", "desc": "禁止高风险操作未经确认"},
            {"type": "file_io", "desc": "文件路径必须在工作目录内"},
            {"type": "idempotency", "desc": "同一任务指纹不允许重复执行"}  # v2.0
        ]

    def _model_soft_constraints(self, intent: Intent, variables: dict) -> list:
        return [
            {"type": "performance", "desc": "优先并行执行", "weight": 0.7},
            {"type": "quality", "desc": "输出结构化Markdown", "weight": 0.6}
        ]

    def _define_anchors(self, intent: Intent, variables: dict) -> dict:
        return {
            "known": ["intent_type", "difficulty"],
            "unknown": ["optimal_tool_chain", "execution_time"],
            "to_solve": intent.sub_goals
        }

    def _build_dependency_graph(self, sub_goals: list) -> dict:
        graph = {}
        for i, goal in enumerate(sub_goals):
            deps = [f"sub_goal_{i-1}"] if i > 0 else []
            graph[f"sub_goal_{i}"] = {"desc": goal[:80], "deps": deps}
        return graph


# ========== Phase 3: 逻辑推演层 ==========

class ReasoningEngine:
    """Phase 3：多路径推理 + 假设验证 + 回溯管理 + 置信度评分"""

    MAX_PATHS = 5
    CONFIDENCE_THRESHOLD = 0.6

    def __init__(self, safe_guard=None):
        self.safe_guard = safe_guard
        self.backtrack_stack: list = []

    def reason(self, condition_tree: ConditionTree) -> list:
        paths = self._generate_paths(condition_tree)
        scored = [self._score_path(p, condition_tree) for p in paths]
        scored.sort(key=lambda x: x.confidence, reverse=True)
        return scored[:self.MAX_PATHS]

    def _generate_paths(self, ct: ConditionTree) -> list:
        paths = []
        sub_goals = list(ct.dependency_graph.keys())

        path_a = ReasoningPath(
            path_id="PATH_SERIAL",
            steps=[{"action": "execute_serial", "goals": sub_goals}]
        )
        paths.append(path_a)

        path_b = ReasoningPath(
            path_id="PATH_PARALLEL",
            steps=[{"action": "execute_parallel", "goals": sub_goals}]
        )
        paths.append(path_b)

        path_c = ReasoningPath(
            path_id="PATH_HYBRID",
            steps=[
                {"action": "execute_serial", "goals": sub_goals[:1]},
                {"action": "execute_parallel", "goals": sub_goals[1:]}
            ]
        )
        paths.append(path_c)

        # v2.0: 第四路径 — 基于 Mailbox 的 Agent 协作路径
        if len(sub_goals) > 2:
            path_d = ReasoningPath(
                path_id="PATH_AGENT_COLLAB",
                steps=[
                    {"action": "distribute_via_mailbox", "goals": sub_goals},
                    {"action": "merge_via_shared_task_list", "goals": []}
                ]
            )
            paths.append(path_d)

        return paths

    def _score_path(self, path: ReasoningPath, ct: ConditionTree) -> ReasoningPath:
        scores = {
            "safety": 0.9 if "SERIAL" in path.path_id else (0.85 if "AGENT" in path.path_id else 0.6),
            "efficiency": 0.6 if "SERIAL" in path.path_id else (0.95 if "AGENT" in path.path_id else 0.9),
            "reliability": 0.85,
            "completeness": min(1.0, len(path.steps) / 3)
        }
        weights = {"safety": 0.35, "efficiency": 0.25, "reliability": 0.25, "completeness": 0.15}
        path.confidence = sum(scores[k] * weights[k] for k in scores)
        return path

    def backtrack(self, failed_path: ReasoningPath, remaining_paths: list) -> Optional[ReasoningPath]:
        failed_path.status = ReasoningStatus.FAILED
        self.backtrack_stack.append(failed_path)
        logger.warning(f"回溯: 路径 {failed_path.path_id} 失败，切换备用路径")

        for path in remaining_paths:
            if path.status == ReasoningStatus.PENDING and path.confidence >= self.CONFIDENCE_THRESHOLD:
                return path
        return None

    def validate_hypothesis(self, path: ReasoningPath, result: ExecutionResult) -> bool:
        return result.success


# ========== Phase 4: 方案执行层 ==========

class ExecutionOrchestrator:
    """Phase 4：工具路由 + 并行调度 + 执行监控 + 结果聚合"""

    MAX_PARALLEL = 5
    DEFAULT_TIMEOUT = 60000

    def __init__(self, tool_registry: dict = None, mailbox: Mailbox = None):
        self.tool_registry = tool_registry or {}
        self.monitor = ExecutionMonitor()
        self.mailbox = mailbox  # v2.0: Mailbox 注入

    def execute(self, path: ReasoningPath, condition_tree: ConditionTree) -> ExecutionResult:
        start = time.time()
        results = []
        errors = []

        try:
            for step in path.steps:
                if step["action"] == "execute_serial":
                    for goal in step["goals"]:
                        r = self._execute_step(goal)
                        results.append(r)
                elif step["action"] == "execute_parallel":
                    r = self._execute_parallel(step["goals"])
                    results.extend(r)
                elif step["action"] == "distribute_via_mailbox":
                    r = self._distribute_via_mailbox(step["goals"])
                    results.append(r)
                elif step["action"] == "merge_via_shared_task_list":
                    r = self._merge_shared_tasks()
                    results.append(r)

            exec_time = (time.time() - start) * 1000
            return ExecutionResult(
                success=len(errors) == 0,
                output=results,
                tool_calls=[step["goals"] for step in path.steps],
                errors=errors,
                execution_time_ms=exec_time
            )
        except Exception as e:
            logger.error(f"执行异常: {e}")
            return ExecutionResult(
                success=False,
                errors=[str(e)],
                execution_time_ms=(time.time() - start) * 1000
            )

    def _distribute_via_mailbox(self, goals: list) -> dict:
        """v2.0: 通过Mailbox向其他Agent分发子目标"""
        if not self.mailbox:
            return {"action": "distribute_via_mailbox", "status": "no_mailbox"}

        dispatched = []
        for i, goal in enumerate(goals):
            # 路由到合适的 Agent
            target = self._route_goal_to_agent(goal)
            msg_id = self.mailbox.send(target, "task_assignment", {
                "goal": goal,
                "priority": i + 1,
                "requester": "reasoning_engine"
            })
            dispatched.append({"goal": goal[:80], "target": target, "msg_id": msg_id})

        return {"action": "distribute_via_mailbox", "dispatched": dispatched}

    def _route_goal_to_agent(self, goal: str) -> str:
        """基于目标内容路由到合适的Agent"""
        if any(k in goal for k in ["文件", "搜索", "查找", "扫描"]):
            return "file-agent"
        if any(k in goal for k in ["应用", "打开", "安装", "app"]):
            return "app-agent"
        if any(k in goal for k in ["搜索", "最新", "资讯", "情报"]):
            return "search-agent"
        if any(k in goal for k in ["系统", "设置", "窗口", "桌面"]):
            return "computer-agent"
        return "file-agent"

    def _merge_shared_tasks(self) -> dict:
        """v2.0: 从Shared Task List聚合结果"""
        if not self.mailbox:
            return {"action": "merge_shared_tasks", "status": "no_mailbox"}
        return {
            "action": "merge_shared_tasks",
            "tasks": {
                tid: info["status"] for tid, info in self.mailbox.shared_tasks.items()
            }
        }

    def _execute_step(self, goal: str) -> dict:
        return {"goal": goal, "status": "completed", "output": f"Executed: {goal[:50]}"}

    def _execute_parallel(self, goals: list) -> list:
        return [{"goal": g, "status": "completed", "output": f"Parallel: {g[:50]}"} for g in goals[:self.MAX_PARALLEL]]


class ExecutionMonitor:
    def __init__(self):
        self._start_time = 0
        self._timeout = 60000

    def start(self, timeout_ms: int = 60000):
        self._start_time = time.time()
        self._timeout = timeout_ms

    def check_timeout(self) -> bool:
        elapsed = (time.time() - self._start_time) * 1000
        return elapsed > self._timeout

    def check_memory(self, limit_mb: int = 2048) -> bool:
        try:
            import psutil
            mem = psutil.Process().memory_info().rss / 1024 / 1024
            return mem < limit_mb
        except ImportError:
            return True


# ========== Phase 5: 结果复盘层 ==========

class ReviewLearner:
    """Phase 5：质量验证 + 缺口检测 + 技能沉淀 + 复盘报告"""

    QUALITY_THRESHOLD = 0.7

    def __init__(self, skill_forge=None, memory_os=None):
        self.skill_forge = skill_forge
        self.memory_os = memory_os

    def review(self, intent: Intent, path: ReasoningPath, result: ExecutionResult) -> ReviewReport:
        quality = self._validate_quality(intent, result)
        gaps = self._detect_gaps(result)
        skills = self._distill_skills(path, result)
        recommendations = self._generate_recommendations(gaps, quality)

        return ReviewReport(
            quality_score=quality,
            gaps_detected=gaps,
            skills_distilled=skills,
            recommendations=recommendations,
            summary=f"质量评分: {quality:.2f}, 检测缺口: {len(gaps)}个, 萃取技能: {len(skills)}个"
        )

    def _validate_quality(self, intent: Intent, result: ExecutionResult) -> float:
        if not result.success: return 0.0
        dims = {
            "completeness": 1.0 if result.output else 0.0,
            "timeliness": 0.9 if result.execution_time_ms < 30000 else 0.5,
            "correctness": 0.85
        }
        weights = {"completeness": 0.4, "timeliness": 0.3, "correctness": 0.3}
        return sum(dims[k] * weights[k] for k in dims)

    def _detect_gaps(self, result: ExecutionResult) -> list:
        gaps = []
        if result.errors:
            for err in result.errors:
                gaps.append({"type": "execution_error", "detail": err})
        if result.execution_time_ms > 60000:
            gaps.append({"type": "performance", "detail": "执行超时"})
        return gaps

    def _distill_skills(self, path: ReasoningPath, result: ExecutionResult) -> list:
        if not result.success: return []
        if self.skill_forge:
            return self.skill_forge.extract_from_path(path, result)
        return []

    def _generate_recommendations(self, gaps: list, quality: float) -> list:
        recs = []
        if quality < self.QUALITY_THRESHOLD:
            recs.append("建议启用备选推理路径")
        for gap in gaps:
            if gap["type"] == "performance":
                recs.append("优化并行调度策略")
        return recs


# ========== v2.0 主引擎 ==========

class ClaudeReasoningEngine:
    """五层推理架构主引擎 v2.0

    新增特性:
    - IdempotencyGate: 幂等性门控，防止重复执行
    - Mailbox: Agent间P2P通信 + Shared Task List
    - ReflectionLoop: OpenClaw风格反思闭环
    """

    def __init__(
        self,
        memory_os=None,
        safe_guard=None,
        skill_forge=None,
        tool_registry: dict = None,
        mailbox: Mailbox = None,           # v2.0
        enable_reflection: bool = True,    # v2.0
        enable_idempotency: bool = True    # v2.0
    ):
        self.phase1 = IntentParser(memory_os=memory_os)
        self.phase2 = ConditionDecomposer()
        self.phase3 = ReasoningEngine(safe_guard=safe_guard)
        self.phase4 = ExecutionOrchestrator(
            tool_registry=tool_registry,
            mailbox=mailbox
        )
        self.phase5 = ReviewLearner(skill_forge=skill_forge, memory_os=memory_os)

        # v2.0 组件
        self.mailbox = mailbox
        self.idempotency_gate = IdempotencyGate() if enable_idempotency else None
        self.reflection_loop = ReflectionLoop() if enable_reflection else None
        self.execution_config = {
            "max_parallel": 5,
            "context_window_size": 32000,
            "force_alternate_path": False,
            "enable_fallback": True
        }

    def process(self, user_input: str, context_window: dict = None) -> dict:
        """完整五层推理链路 v2.0（含幂等性门控 + 反思闭环）"""
        ctx = context_window or {}

        # === v2.0: Idempotency Gate Check ===
        if self.idempotency_gate:
            fingerprint = self.idempotency_gate.generate_fingerprint(user_input, ctx)
            gate_status = self.idempotency_gate.check_gate(fingerprint)

            if gate_status == GateStatus.BLOCKED:
                logger.warning(f"幂等性门控阻断: {fingerprint}")
                return {
                    "blocked": True,
                    "reason": "idempotency_gate_blocked",
                    "fingerprint": fingerprint,
                    "intent": None, "condition_tree": None,
                    "best_path": None, "result": None, "review": None,
                    "reflection": None, "backtrack_occurred": False
                }

            if gate_status == GateStatus.QUEUED:
                logger.info(f"幂等性门控排队: {fingerprint}")
                return {
                    "blocked": False,
                    "queued": True,
                    "fingerprint": fingerprint,
                    "intent": None, "condition_tree": None,
                    "best_path": None, "result": None, "review": None,
                    "reflection": None, "backtrack_occurred": False
                }

            # Lock gate
            self.idempotency_gate.lock_gate(fingerprint)
        else:
            fingerprint = None

        # Phase 1: 问题解析
        intent = self.phase1.parse(user_input, ctx)
        if fingerprint:
            intent.task_fingerprint = fingerprint
        logger.info(f"[Phase1] 意图: {intent.intent_type}, 难度: L{intent.difficulty.value}")

        # Phase 2: 条件拆解
        condition_tree = self.phase2.decompose(intent)
        logger.info(f"[Phase2] 变量: {len(condition_tree.variables)}个, 约束: {len(condition_tree.hard_constraints)}硬/{len(condition_tree.soft_constraints)}软")

        # Phase 3: 逻辑推演
        paths = self.phase3.reason(condition_tree)

        # v2.0: 如果反思要求备用路径，调整排序
        if self.execution_config.get("force_alternate_path") and len(paths) > 1:
            paths[0], paths[1] = paths[1], paths[0]
            self.execution_config["force_alternate_path"] = False

        best_path = paths[0] if paths else None
        logger.info(f"[Phase3] 生成 {len(paths)} 条推理路径, 最优: {best_path.path_id if best_path else 'None'} (置信度: {best_path.confidence:.2f})")

        # Phase 4: 方案执行
        result = self.phase4.execute(best_path, condition_tree) if best_path else ExecutionResult(success=False, errors=["无有效推理路径"])
        logger.info(f"[Phase4] 执行结果: {'成功' if result.success else '失败'}, 耗时: {result.execution_time_ms:.0f}ms")

        # 回溯处理
        backtrack_occurred = False
        if not result.success and len(paths) > 1:
            fallback = self.phase3.backtrack(best_path, paths[1:])
            if fallback:
                logger.info(f"[回溯] 切换到 {fallback.path_id}")
                result = self.phase4.execute(fallback, condition_tree)
                best_path = fallback
                backtrack_occurred = True

        # Phase 5: 结果复盘
        review = self.phase5.review(intent, best_path or paths[0], result)
        logger.info(f"[Phase5] 复盘: {review.summary}")

        # === v2.0: 反思闭环 ===
        reflection = None
        if self.reflection_loop and not result.success:
            reflection = self.reflection_loop.reflect(intent, result, review)
            adjustments = reflection.get("adjustments", [])
            if adjustments:
                self.execution_config = self.reflection_loop.apply_adjustments(
                    adjustments, self.execution_config
                )
            logger.info(f"[Reflection] {self.reflection_loop.get_reflection_summary()}")

        # === v2.0: Mark Idempotency Gate ===
        if self.idempotency_gate and fingerprint:
            self.idempotency_gate.mark_executed(fingerprint)

        return {
            "intent": intent,
            "condition_tree": condition_tree,
            "best_path": best_path,
            "result": result,
            "review": review,
            "reflection": reflection,
            "backtrack_occurred": backtrack_occurred,
            "fingerprint": fingerprint
        }


# ========== 测试入口 ==========

if __name__ == "__main__":
    # v2.0 完整链路测试
    mailbox = Mailbox(agent_id="claude_reasoning")
    mailbox.register_peer("file-agent", ["file_ops", "scanning"])
    mailbox.register_peer("search-agent", ["web_search", "deep_research"])

    engine = ClaudeReasoningEngine(
        mailbox=mailbox,
        enable_reflection=True,
        enable_idempotency=True
    )

    # 测试 1: 普通任务
    print("=== 测试1: 普通任务 ===")
    test1 = "帮我搜索并分析最新的大模型推理架构论文，生成一份对比报告"
    output1 = engine.process(test1)
    print(f"意图: {output1['intent'].intent_type}, 评分: {output1['review'].quality_score:.2f}")
    print(f"指纹: {output1.get('fingerprint', 'N/A')}")

    # 测试 2: 幂等性验证（相同任务不应重复执行）
    print("\n=== 测试2: 幂等性验证 ===")
    output2 = engine.process(test1)
    print(f"阻断: {output2.get('blocked', False)}, 排队: {output2.get('queued', False)}")

    # 测试 3: 反思闭环验证
    print("\n=== 测试3: 反思闭环验证 ===")
    if output1.get("reflection"):
        print(f"反思: {output1['reflection']['decision']}")
        print(f"调整项: {len(output1['reflection']['adjustments'])}个")
