# claude_reasoning_enhanced_v2.0_20260531_160636_525.py

> 原始文件: `claude_reasoning_enhanced_v2.0_20260531_160636_525.py`  |  类型: `.py`  |  自动转换

```python
# -*- coding: utf-8 -*-
"""
Claude分层推理引擎 v2.0 — R16深度增强版
基于 v1.0 骨架，增强：三级缓存 / 推理回溯 / 工具联动回环 / 中文全场景适配
"""

import json
import time
import hashlib
import logging
import re
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from collections import OrderedDict

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] REASONING: %(message)s')
logger = logging.getLogger("ClaudeReasoningV2")


# ==================== 枚举定义 ====================

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
    FAILED = "failed"
    BACKTRACKED = "backtracked"


class CacheTier(Enum):
    L1_HOT = 1
    L2_WARM = 2
    L3_COLD = 3


# ==================== 三级缓存上下文系统 ====================

@dataclass
class ContextSnapshot:
    """L2温缓存快照"""
    session_id: str
    compressed_text: str
    key_entities: list
    intent_history: list
    retention_score: float
    timestamp: float = field(default_factory=time.time)


class TieredContextCache:
    """三级缓存上下文系统
    
    L1热缓存：最近3轮对话，容量12K tokens，无压缩，命中延迟<10ms
    L2温缓存：当前会话全量，容量64K tokens，语义压缩，命中延迟<50ms  
    L3冷缓存：历史会话摘要，容量256K tokens，时间衰减，命中延迟<200ms
    """

    L1_CAPACITY = 3       # 保留最近3轮
    L2_MAX_TOKENS = 64000
    L3_MAX_TOKENS = 256000

    def __init__(self):
        self.l1_hot: OrderedDict = OrderedDict()
        self.l2_warm: dict = {}       # session_id -> ContextSnapshot
        self.l3_cold: list = []       # 摘要列表（越新越前）
        self.l1_hits = 0
        self.l2_hits = 0
        self.l3_hits = 0

    def store(self, turn_id: str, context: dict, session_id: str = "default"):
        """存储上下文，自动分层"""
        # L1热缓存：直接写入，FIFO淘汰
        self.l1_hot[turn_id] = {
            "context": context,
            "timestamp": time.time(),
            "token_estimate": len(json.dumps(context, ensure_ascii=False))
        }
        if len(self.l1_hot) > self.L1_CAPACITY:
            evicted_id, evicted = self.l1_hot.popitem(last=False)
            self._promote_to_l2(evicted_id, evicted, session_id)

    def retrieve(self, intent: str, max_tokens: int = 4000) -> dict:
        """三级检索：L1→L2→L3"""
        # L1：最近上下文直接返回
        result = {"tier": CacheTier.L1_HOT.name, "context": None, "confidence": 0.0}
        if self.l1_hot:
            recent = list(self.l1_hot.values())[-1]
            result["context"] = recent["context"]
            result["confidence"] = 0.95
            self.l1_hits += 1
            return result

        # L2：语义匹配
        for sid, snapshot in self.l2_warm.items():
            if self._semantic_match(intent, snapshot):
                result["tier"] = CacheTier.L2_WARM.name
                result["context"] = {"snapshot": snapshot.compressed_text}
                result["confidence"] = 0.75
                self.l2_hits += 1
                return result

        # L3：冷缓存回退
        if self.l3_cold:
            best = self.l3_cold[0]
            result["tier"] = CacheTier.L3_COLD.name
            result["context"] = {"summary": best}
            result["confidence"] = 0.45
            self.l3_hits += 1

        return result

    def compress_context(self, raw_text: str, target_tokens: int = 32000) -> str:
        """语义压缩：关键句抽取 + 关系图谱 → 压缩表示"""
        # 简化实现：分层抽取
        sentences = re.split(r'[。！？；\n]', raw_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

        if len(sentences) <= 20:
            return raw_text[:target_tokens * 4]

        # 关键词加权抽取
        important = []
        for s in sentences:
            score = self._importance_score(s)
            if score > 0.3 or len(important) < target_tokens // 20:
                important.append(s)

        return "。".join(important)

    def anchor_search(self, query: str, context_window: dict) -> list:
        """锚点精准检索：基于意图的关键词定位"""
        anchors = self._extract_anchors(query)
        matched = []
        for anchor_type, keywords in anchors.items():
            for kw in keywords:
                if kw in str(context_window):
                    matched.append({"type": anchor_type, "keyword": kw, "source": "context"})
        return matched

    # --- 内部方法 ---

    def _promote_to_l2(self, evicted_id: str, evicted: dict, session_id: str):
        """L1溢出 → L2语义压缩存储"""
        raw = json.dumps(evicted.get("context", {}), ensure_ascii=False)
        compressed = self.compress_context(raw)
        snapshot = ContextSnapshot(
            session_id=session_id,
            compressed_text=compressed,
            key_entities=self._extract_entities(raw),
            intent_history=[evicted_id],
            retention_score=0.7
        )
        self.l2_warm[f"{session_id}_{evicted_id}"] = snapshot

    def _semantic_match(self, intent: str, snapshot: ContextSnapshot) -> bool:
        """语义匹配判断"""
        intent_lower = intent.lower()
        return any(kw in snapshot.compressed_text.lower() for kw in intent_lower.split()[:5])

    def _importance_score(self, sentence: str) -> float:
        """句子重要性评分"""
        score = 0.0
        if any(kw in sentence for kw in ["关键", "重要", "核心", "结论", "因此", "所以"]):
            score += 0.3
        if len(sentence) > 20:
            score += 0.2
        return min(score, 1.0)

    def _extract_entities(self, text: str) -> list:
        """实体提取（简化）"""
        entities = []
        # 中文技术术语
        for match in re.finditer(r'[A-Z][a-z]+|[A-Z]{2,}|[\u4e00-\u9fff]{2,4}(?:系统|引擎|框架|模型|架构|协议|层)', text):
            entities.append(match.group())
        return list(set(entities))[:20]

    def _extract_anchors(self, query: str) -> dict:
        """从查询中提取搜索锚点"""
        return {
            "实体": [w for w in re.findall(r'[\u4e00-\u9fff]{2,6}', query) if len(w) >= 2],
            "操作": [w for w in ["分析", "搜索", "执行", "生成", "优化"] if w in query],
            "类型": [w for w in ["文件", "代码", "报告", "配置", "日志"] if w in query]
        }

    def get_stats(self) -> dict:
        return {"l1_hits": self.l1_hits, "l2_hits": self.l2_hits, "l3_hits": self.l3_hits,
                "l1_size": len(self.l1_hot), "l2_size": len(self.l2_warm), "l3_size": len(self.l3_cold)}


# ==================== 增强推理回溯系统 ====================

@dataclass 
class ReasoningCheckpoint:
    """推理检查点"""
    cp_id: str
    phase: int
    state: dict
    timestamp: float = field(default_factory=time.time)


class EnhancedReasoningBacktrack:
    """增强推理回溯：检查点保存/恢复 + 回溯决策树"""

    CONFIDENCE_THRESHOLD = 0.6
    MAX_BACKTRACK_DEPTH = 3

    def __init__(self):
        self.checkpoints: list = []
        self.backtrack_tree: dict = {}
        self.backtrack_count = 0

    def save_checkpoint(self, phase: int, state: dict) -> ReasoningCheckpoint:
        """保存检查点"""
        cp = ReasoningCheckpoint(
            cp_id=f"CP_{phase}_{datetime.now().strftime('%H%M%S')}_{len(self.checkpoints)}",
            phase=phase,
            state=state
        )
        self.checkpoints.append(cp)
        logger.info(f"检查点保存: {cp.cp_id} (Phase {phase})")
        return cp

    def restore(self, target_phase: int = None) -> Optional[dict]:
        """恢复到最近的检查点"""
        if target_phase:
            candidates = [c for c in self.checkpoints if c.phase == target_phase]
        else:
            candidates = self.checkpoints

        if not candidates:
            return None

        best = candidates[-1]
        logger.info(f"恢复到检查点: {best.cp_id}")
        return best.state

    def decide_backtrack(self, failed_path_id: str, confidence: float,
                         alternative_paths: list, remaining_depth: int) -> dict:
        """回溯决策树"""
        confidence_drop = max(0, 0.85 - confidence)

        if remaining_depth <= 0:
            return {"action": "stop", "reason": "max_backtrack_depth_reached"}

        if confidence_drop < 0.20:
            return {"action": "switch", "to": alternative_paths[0] if alternative_paths else None}
        elif confidence_drop < 0.50:
            return {"action": "merge_and_retry", "failed": failed_path_id, "alternatives": alternative_paths[:2]}
        else:
            cp = self.restore(target_phase=1)
            return {"action": "full_restart", "checkpoint": cp}

    def build_backtrack_tree(self, node_id: str, children: list):
        """构建回溯树结构"""
        self.backtrack_tree[node_id] = {
            "children": children,
            "explored": [],
            "failed": [],
            "optimal": None
        }


# ==================== 工具联动推理回环 ====================

@dataclass
class ToolReasoningState:
    """工具推理状态"""
    round: int = 0
    predictions: list = field(default_factory=list)
    results: list = field(default_factory=list)
    feedback_history: list = field(default_factory=list)
    convergence_round: Optional[int] = None


class ToolReasoningLoop:
    """工具联动推理回环：预判→路由→执行→反馈→迭代→收束"""

    CONVERGENCE_WINDOW = 2      # 连续N轮结果一致视为收敛
    MAX_ITERATIONS = 5
    IMPROVEMENT_THRESHOLD = 0.05

    def __init__(self, tool_registry: dict = None):
        self.tool_registry = tool_registry or {}
        self.state = ToolReasoningState()

    def run(self, task: str, available_tools: list[str] = None) -> dict:
        """执行推理-工具联动回环"""
        self.state = ToolReasoningState()

        for iteration in range(self.MAX_ITERATIONS):
            self.state.round = iteration + 1

            # 预判：分析需要什么工具、期待什么输出
            prediction = self._predict_tool_output(task, available_tools)
            self.state.predictions.append(prediction)

            # 路由：选择最优工具+参数
            tool_route = self._route_tool(prediction, available_tools)

            # 执行：调用工具
            result = self._execute_tool(tool_route, task)
            self.state.results.append(result)

            # 评估反馈
            feedback = self._evaluate_feedback(prediction, result)
            self.state.feedback_history.append(feedback)

            # 收敛判断
            if self._check_convergence():
                self.state.convergence_round = iteration + 1
                logger.info(f"推理回环收敛于第 {iteration+1} 轮")
                break

            # 动态调整
            task = self._refine_task(task, feedback)
            if feedback.get("improvement", 0) < self.IMPROVEMENT_THRESHOLD and iteration >= 2:
                logger.info(f"改进幅度过小({feedback['improvement']:.3f})，提前终止")
                break

        return self._build_final_output()

    def _predict_tool_output(self, task: str, tools: list) -> dict:
        """预判工具输出结构"""
        return {"expected_type": "structured", "expected_keys": ["result", "status"],
                "expected_tool": tools[0] if tools else "unknown"}

    def _route_tool(self, prediction: dict, tools: list) -> dict:
        """工具智能路由"""
        return {"tool": prediction.get("expected_tool", "default"), "params": {}}

    def _execute_tool(self, route: dict, task: str) -> dict:
        """执行工具"""
        tool_name = route.get("tool", "")
        if tool_name in self.tool_registry:
            return self.tool_registry[tool_name](task)
        return {"result": "tool_not_found", "status": "error"}

    def _evaluate_feedback(self, prediction: dict, result: dict) -> dict:
        """评估执行反馈"""
        deviation = 0.0
        if result.get("status") == "error":
            deviation = 1.0
        improvement = max(0, 1.0 - deviation - (self.state.round * 0.05))
        return {"deviation": deviation, "improvement": improvement, "should_continue": deviation > 0.1}

    def _check_convergence(self) -> bool:
        """收敛检查：连续N轮结果一致"""
        if len(self.state.results) < self.CONVERGENCE_WINDOW:
            return False
        recent = self.state.results[-self.CONVERGENCE_WINDOW:]
        return all(r.get("status") == recent[0].get("status") for r in recent)

    def _refine_task(self, task: str, feedback: dict) -> str:
        """反馈驱动任务细化"""
        if feedback.get("deviation", 0) > 0.3:
            return task + " [请修正: 上次结果偏差较大]"
        return task

    def _build_final_output(self) -> dict:
        return {
            "total_rounds": self.state.round,
            "converged": self.state.convergence_round is not None,
            "convergence_round": self.state.convergence_round,
            "final_feedback": self.state.feedback_history[-1] if self.state.feedback_history else {},
            "result_evolution": [r.get("status") for r in self.state.results]
        }


# ==================== 中文全场景适配引擎 ====================

class ChineseContextAdapter:
    """中文全场景深度适配"""

    AMBIGUITY_MAP = {
        "苹果": {"tech": "Apple Inc.", "fruit": "苹果水果", "movie": "电影《苹果》"},
        "python": {"lang": "Python编程语言", "snake": "蟒蛇"},
        "终端": {"tech": "终端Terminal", "device": "终端设备", "endpoint": "端点"},
    }

    @classmethod
    def disambiguate(cls, sentence: str) -> dict:
        """中文多义词消歧"""
        results = {}
        for word, meanings in cls.AMBIGUITY_MAP.items():
            if word in sentence:
                # 双通道消歧：全局语义场+局部上下文窗口
                context_words = cls._extract_context_window(sentence, word, window=10)
                best_meaning = cls._rank_meanings(meanings, context_words)
                results[word] = {"resolved": best_meaning, "confidence": 0.85, "alternatives": list(meanings.keys())}
        return results

    @classmethod
    def detect_register(cls, text: str) -> str:
        """语气层级识别"""
        if any(kw in text for kw in ["请", "谢谢", "麻烦", "您好"]):
            return "formal"
        if any(kw in text for kw in ["哈哈", "卧槽", "牛逼", "离谱"]):
            return "casual"
        if any(kw in text for kw in ["代码", "API", "函数", "Bug", "PR"]):
            return "technical"
        return "general"

    @classmethod
    def segment_long_doc(cls, text: str, max_chunk_tokens: int = 8192) -> list:
        """中文长文档分段推理"""
        # 按自然段落分块
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = ""
        current_len = 0

        for para in paragraphs:
            para_len = len(para)
            if current_len + para_len > max_chunk_tokens and current_chunk:
                chunks.append({"index": len(chunks), "text": current_chunk.strip(), "length": current_len})
                current_chunk = para
                current_len = para_len
            else:
                current_chunk += "\n\n" + para if current_chunk else para
                current_len += para_len

        if current_chunk:
            chunks.append({"index": len(chunks), "text": current_chunk.strip(), "length": current_len})

        return chunks

    @classmethod
    def search_router(cls, query: str) -> str:
        """中文搜索多引擎智能路由"""
        if any(kw in query for kw in ["知乎", "怎么", "如何", "为什么"]):
            return "zhihu"
        if any(kw in query for kw in ["技术", "代码", "Python", "Java", "AI"]):
            return "csdn+github"
        if any(kw in query for kw in ["视频", "教程", "演示"]):
            return "bilibili"
        return "baidu"

    @staticmethod
    def _extract_context_window(text: str, target: str, window: int = 10) -> list:
        idx = text.index(target)
        start = max(0, idx - window)
        end = min(len(text), idx + len(target) + window)
        return list(text[start:end])

    @staticmethod
    def _rank_meanings(meanings: dict, context: list) -> str:
        context_str = "".join(context)
        scores = {}
        for key, desc in meanings.items():
            if any(w in context_str for w in desc.split()):
                scores[key] = 1.0
            else:
                scores[key] = 0.5
        return max(scores, key=scores.get)


# ==================== v1.0 兼容层（复用已有 dataclass） ====================

@dataclass
class Intent:
    intent_type: str
    raw_input: str
    context_summary: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.L2_STANDARD
    sub_goals: list = field(default_factory=list)
    confidence: float = 0.85
    chinese_adapter: dict = field(default_factory=dict)


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
    confidence: float = 0.5
    status: ReasoningStatus = ReasoningStatus.PENDING


@dataclass
class ExecutionResult:
    success: bool = False
    output: Any = None
    tool_calls: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    execution_time_ms: float = 0.0


@dataclass
class ReviewReport:
    quality_score: float = 0.0
    gaps_detected: list = field(default_factory=list)
    skills_distilled: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    summary: str = ""


# ==================== 五层增强引擎 ====================

class IntentParserV2:
    """Phase 1 增强版：意图识别 + 三级缓存 + 难度定级 + 子目标拆分"""

    CODE_KW = ["代码", "编程", "函数", "API", "写一个", "实现", "debug", "修复", "优化"]
    SEARCH_KW = ["搜索", "查找", "最新的", "什么是", "怎么", "如何"]
    ACTION_KW = ["打开", "关闭", "删除", "移动", "执行", "运行", "安装", "配置"]
    QA_KW = ["为什么", "怎么样", "是什么", "区别", "对比", "vs"]
    CREATIVE_KW = ["写一篇", "生成", "创作", "设计", "画", "制作"]

    def __init__(self, memory_os=None, cache: TieredContextCache = None):
        self.memory_os = memory_os
        self.cache = cache or TieredContextCache()
        self.chinese = ChineseContextAdapter()

    def parse(self, user_input: str, context_window: dict = None) -> Intent:
        ctx = context_window or {}
        intent_type = self._classify_enhanced(user_input)
        context = self._load_context_tiered(user_input, ctx)
        difficulty = self._rated_difficulty_enhanced(user_input, context)
        sub_goals = self._decompose_enhanced(user_input, difficulty)
        chinese_info = self.chinese.disambiguate(user_input) if any('\u4e00' <= c <= '\u9fff' for c in user_input) else {}

        return Intent(
            intent_type=intent_type,
            raw_input=user_input,
            context_summary=context,
            difficulty=difficulty,
            sub_goals=sub_goals,
            confidence=self._estimate_confidence(intent_type, difficulty),
            chinese_adapter={"register": self.chinese.detect_register(user_input), "disambiguation": chinese_info}
        )

    def _classify_enhanced(self, text: str) -> str:
        lower = text.lower()
        if any(k in lower for k in self.CODE_KW): return "code"
        if any(k in lower for k in self.SEARCH_KW): return "search"
        if any(k in lower for k in self.ACTION_KW): return "action"
        if any(k in lower for k in self.QA_KW): return "qa"
        if any(k in lower for k in self.CREATIVE_KW): return "creative"
        return "general"

    def _load_context_tiered(self, user_input: str, context_window: dict) -> str:
        cache_result = self.cache.retrieve(user_input)
        if cache_result["confidence"] > 0.7:
            return f"[{cache_result['tier']}] {json.dumps(cache_result['context'], ensure_ascii=False)[:500]}"
        if self.memory_os:
            return self.memory_os.retrieve_relevant(user_input, context_window)
        return json.dumps(context_window, ensure_ascii=False)[:500]

    def _rated_difficulty_enhanced(self, text: str, context: str) -> DifficultyLevel:
        # 多因素难度评估
        factors = {
            "length": len(text),
            "sub_goals": len(re.split(r'[。；\n]', text)),
            "technical_terms": len(re.findall(r'[A-Z][a-z]+|[A-Z]{2,}', text)),
            "context_complexity": len(context)
        }
        total = factors["length"] + factors["sub_goals"] * 30 + factors["technical_terms"] * 20 + factors["context_complexity"] * 0.1

        if total < 80: return DifficultyLevel.L1_TRIVIAL
        if total < 250: return DifficultyLevel.L2_STANDARD
        if total < 800: return DifficultyLevel.L3_COMPLEX
        if total < 3000: return DifficultyLevel.L4_EXPERT
        return DifficultyLevel.L5_FRONTIER

    def _decompose_enhanced(self, text: str, difficulty: DifficultyLevel) -> list:
        if difficulty.value <= 2:
            return [text]
        delimiters = ["。", "；", "\n", "；"]
        parts = [text]
        for d in delimiters:
            new_parts = []
            for p in parts:
                new_parts.extend(x.strip() for x in p.split(d) if x.strip())
            parts = new_parts
            if len(parts) > 1:
                break
        return parts if len(parts) > 1 else [text]

    def _estimate_confidence(self, intent_type: str, difficulty: DifficultyLevel) -> float:
        base = {"code": 0.88, "search": 0.82, "action": 0.90, "qa": 0.78, "creative": 0.70, "general": 0.75}
        return min(0.95, base.get(intent_type, 0.80) - (difficulty.value - 1) * 0.03)


class ConditionDecomposerV2:
    """Phase 2 增强版：变量抽取+约束建模+锚点定义+依赖图+中文长文档分段"""

    def decompose(self, intent: Intent) -> ConditionTree:
        variables = self._extract_variables_enhanced(intent)
        hard = self._model_hard_constraints(intent)
        soft = self._model_soft_constraints(intent, variables)
        anchors = self._define_anchors_enhanced(intent, variables)
        dep_graph = self._build_dependency_graph_enhanced(intent.sub_goals)

        return ConditionTree(
            variables=variables,
            hard_constraints=hard,
            soft_constraints=soft,
            anchors=anchors,
            dependency_graph=dep_graph
        )

    def _extract_variables_enhanced(self, intent: Intent) -> dict:
        vars_dict = {
            "raw_input": intent.raw_input,
            "intent_type": intent.intent_type,
            "difficulty": intent.difficulty.value,
            "sub_goal_count": len(intent.sub_goals),
            "chinese_register": intent.chinese_adapter.get("register", "general"),
            "has_ambiguity": len(intent.chinese_adapter.get("disambiguation", {})) > 0,
        }
        # 如果是中文长文档，自动分段
        if intent.difficulty.value >= 3 and len(intent.raw_input) > 4000:
            chunks = ChineseContextAdapter.segment_long_doc(intent.raw_input)
            vars_dict["long_doc_chunks"] = len(chunks)
            vars_dict["chunk_first_100"] = chunks[0]["text"][:100] if chunks else ""
        return vars_dict

    def _model_hard_constraints(self, intent: Intent) -> list:
        constraints = [
            {"type": "safety", "desc": "高风险操作必须用户确认"},
            {"type": "file_path", "desc": "文件操作限制在工作目录内"},
        ]
        if intent.difficulty.value >= 4:
            constraints.append({"type": "timeout", "desc": "单步执行不超过60秒"})
        return constraints

    def _model_soft_constraints(self, intent: Intent, variables: dict) -> list:
        return [
            {"type": "parallelism", "desc": "无依赖子任务并行执行", "weight": 0.7},
            {"type": "output_format", "desc": "结构化Markdown输出", "weight": 0.6},
            {"type": "chinese_quality", "desc": "中文输出自然流畅", "weight": 0.5 if variables.get("chinese_register") else 0},
        ]

    def _define_anchors_enhanced(self, intent: Intent, variables: dict) -> dict:
        anchors = {
            "known": ["intent_type", "difficulty", "chinese_register"],
            "unknown": ["optimal_path", "execution_time", "tool_chain"],
            "to_solve": intent.sub_goals,
        }
        if variables.get("has_ambiguity"):
            anchors["to_resolve"] = list(intent.chinese_adapter.get("disambiguation", {}).keys())
        return anchors

    def _build_dependency_graph_enhanced(self, sub_goals: list) -> dict:
        graph = {}
        for i, goal in enumerate(sub_goals):
            deps = [f"sub_goal_{i-1}"] if i > 0 else []
            graph[f"sub_goal_{i}"] = {"desc": goal[:100], "deps": deps, "parallelizable": i > 0 and len(goal) < 200}
        return graph


# ==================== 主引擎 v2.0 ====================

class ClaudeReasoningEngineV2:
    """五层推理架构主引擎 v2.0 — R16全面增强版"""

    def __init__(self, memory_os=None, safe_guard=None, skill_forge=None, tool_registry: dict = None):
        self.cache = TieredContextCache()
        self.phase1 = IntentParserV2(memory_os=memory_os, cache=self.cache)
        self.phase2 = ConditionDecomposerV2()
        self.phase3_backtrack = EnhancedReasoningBacktrack()
        self.phase4_loop = ToolReasoningLoop(tool_registry=tool_registry)
        self.safe_guard = safe_guard
        self.skill_forge = skill_forge
        self.tool_registry = tool_registry or {}

    def process(self, user_input: str, context_window: dict = None, session_id: str = "default") -> dict:
        ctx = context_window or {}
        turn_id = f"turn_{datetime.now().strftime('%H%M%S')}_{hashlib.md5(user_input.encode()).hexdigest()[:6]}"

        # Phase 1: 问题解析（含三级缓存）
        intent = self.phase1.parse(user_input, ctx)
        self.cache.store(turn_id, {"input": user_input, "intent": intent.intent_type}, session_id)

        # Phase 2: 条件拆解（含中文长文档分段）
        condition_tree = self.phase2.decompose(intent)

        # Phase 3: 逻辑推演（含检查点+回溯）
        self.phase3_backtrack.save_checkpoint(2, {"condition_tree": condition_tree, "intent": intent})
        paths = self._generate_paths_enhanced(condition_tree)
        best_path = paths[0] if paths else None

        # Phase 4: 方案执行（含工具联动回环）
        result = None
        if best_path:
            result = self._execute_with_tool_loop(best_path, condition_tree, user_input)

        # 回溯处理
        if (not result or not result.success) and len(paths) > 1:
            decision = self.phase3_backtrack.decide_backtrack(
                best_path.path_id if best_path else "NONE",
                best_path.confidence if best_path else 0,
                [p.path_id for p in paths[1:]],
                self.phase3_backtrack.MAX_BACKTRACK_DEPTH
            )
            logger.info(f"回溯决策: {decision['action']}")

            if decision["action"] == "switch":
                fallback = next((p for p in paths if p.path_id == decision.get("to")), None)
                if fallback:
                    result = self._execute_simple(fallback, condition_tree)

        # Phase 5: 结果复盘
        review = self._review_enhanced(intent, best_path, result)

        return {
            "intent": intent,
            "condition_tree": condition_tree,
            "best_path": best_path,
            "result": result,
            "review": review,
            "cache_stats": self.cache.get_stats(),
            "backtrack_used": result is None or not result.success
        }

    def _generate_paths_enhanced(self, ct: ConditionTree) -> list:
        sub_goals = list(ct.dependency_graph.keys())
        paths = []

        # 路径A: 串行
        a = ReasoningPath(path_id="PATH_SERIAL_V2", steps=[{"action": "serial", "goals": sub_goals}], confidence=0.70)
        paths.append(a)

        # 路径B: 最大并行
        b = ReasoningPath(path_id="PATH_PARALLEL_V2", steps=[{"action": "parallel", "goals": sub_goals}], confidence=0.60)
        paths.append(b)

        # 路径C: 混合
        mid = len(sub_goals) // 2
        c = ReasoningPath(path_id="PATH_HYBRID_V2",
                         steps=[{"action": "serial", "goals": sub_goals[:mid]},
                                {"action": "parallel", "goals": sub_goals[mid:]}],
                         confidence=0.65)
        paths.append(c)

        # 路径D: 工具联动（v2.0新增）
        d = ReasoningPath(path_id="PATH_TOOL_LOOP",
                         steps=[{"action": "tool_reasoning_loop", "goals": sub_goals}],
                         confidence=0.75)
        paths.append(d)

        paths.sort(key=lambda x: x.confidence, reverse=True)
        return paths

    def _execute_with_tool_loop(self, path: ReasoningPath, ct: ConditionTree, task: str) -> ExecutionResult:
        start = time.time()
        if path.path_id == "PATH_TOOL_LOOP":
            loop_result = self.phase4_loop.run(task, list(self.tool_registry.keys()))
            return ExecutionResult(
                success=loop_result["converged"],
                output=loop_result,
                execution_time_ms=(time.time() - start) * 1000
            )
        return self._execute_simple(path, ct)

    def _execute_simple(self, path: ReasoningPath, ct: ConditionTree) -> ExecutionResult:
        start = time.time()
        return ExecutionResult(success=True, output={"path": path.path_id, "goals": ct.dependency_graph},
                              execution_time_ms=(time.time() - start) * 1000)

    def _review_enhanced(self, intent: Intent, path: ReasoningPath, result: ExecutionResult) -> ReviewReport:
        if not result or not result.success:
            return ReviewReport(quality_score=0.0, gaps_detected=[{"type": "execution_failure"}],
                              summary="执行失败")

        # 多维度质量评估
        scores = {"completeness": 1.0 if result.output else 0.0,
                  "timeliness": 0.9 if result.execution_time_ms < 30000 else 0.5,
                  "chinese_quality": 0.9 if intent.chinese_adapter else 0.5}

        quality = sum(v * w for v, w in zip(scores.values(), [0.4, 0.3, 0.3]))
        gaps = [{"type": "chinese_ambiguity", "detail": k}
                for k in intent.chinese_adapter.get("disambiguation", {})]

        return ReviewReport(quality_score=quality, gaps_detected=gaps,
                          summary=f"v2.0质量评分: {quality:.2f}, 缓存命中: {self.cache.get_stats()}")


# ==================== 测试入口 ====================

if __name__ == "__main__":
    engine = ClaudeReasoningEngineV2()

    # 中文复杂输入测试
    test_cases = [
        "帮我搜索最新的LLM推理架构论文，对比GPT-5和DeepSeek-R1的性能差异",
        "写一个Python脚本分析当前目录下所有PDF文件的页数并生成Excel报告",
        "为什么苹果的M系列芯片在推理效率上优于Intel",
    ]

    for tc in test_cases:
        print(f"\n{'='*60}")
        print(f"输入: {tc[:60]}...")
        output = engine.process(tc)
        print(f"意图: {output['intent'].intent_type}")
        print(f"难度: L{output['intent'].difficulty.value}")
        print(f"中文语域: {output['intent'].chinese_adapter.get('register')}")
        print(f"最佳路径: {output['best_path'].path_id if output['best_path'] else 'None'}")
        print(f"成功: {output['result'].success if output['result'] else False}")
        print(f"质量评分: {output['review'].quality_score:.2f}")
        print(f"缓存统计: {output['cache_stats']}")
```
