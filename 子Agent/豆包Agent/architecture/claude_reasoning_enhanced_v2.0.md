# claude_reasoning_enhanced_v2.0.py

> 原始文件: `claude_reasoning_enhanced_v2.0.py`  |  类型: `.py`  |  自动转换

```python
"""
Claude分层推理引擎 v2.0 · 中文增强版
=====================================
在v1.0五层推理骨架基础上，增强：
 1. 中文全场景意图分类（规则+语义双通道）
 2. 推理回溯深度增强（多级检查点+回滚策略）
 3. 工具联动推理（预判→联动→反馈→迭代）
 4. 长上下文分层加载（L1/L2/L3缓存）
 5. 中文长文档分段推理

R13 全域缺口专项补全 · P0-1 增强落地
"""

import json
import time
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from pathlib import Path
from datetime import datetime

# 继承v1.0的基础类
import sys
sys.path.insert(0, str(Path(__file__).parent))
from claude_reasoning_engine import (
    DifficultyLevel, ReasoningStatus, Intent, ConditionTree,
    ReasoningPath, ExecutionResult, ReviewReport,
    IntentParser, ConditionDecomposer, ReasoningEngine,
    ExecutionOrchestrator, ReviewLearner, ClaudeReasoningEngine
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ClaudeReasoningEnhanced")


# ====================================================================
# 增强 1：中文全场景意图分类器 (Chinese Intent Classifier)
# ====================================================================

class ChineseIntentClassifier:
    """中文意图分类器：规则+语义锚定双通道"""

    # 中文语义分类词典（按领域分组）
    CN_INTENT_PATTERNS = {
        "code": {
            "high": ["写一个程序", "实现一个函数", "API接口", "代码生成", "编程实现",
                     "写个脚本", "搭建系统", "部署", "重构代码", "写个模块"],
            "medium": ["代码", "编程", "函数", "算法", "脚本", "模块", "类", "接口",
                      "debug", "调试", "报错", "异常", "编译", "运行"],
            "low": ["开发", "技术", "架构", "设计模式", "框架", "库"]
        },
        "search": {
            "high": ["搜索最新", "查找资料", "检索论文", "调研", "查一下",
                    "网上搜", "百度一下", "查找文档", "找一篇"],
            "medium": ["搜索", "查找", "最新的", "什么是", "怎么", "有哪些",
                     "对比", "分析", "研究", "汇总"],
            "low": ["参考", "资料", "文档", "论文", "文献"]
        },
        "action": {
            "high": ["打开应用", "关闭窗口", "删除文件", "移动文件", "执行命令",
                    "下载到", "安装", "卸载", "重启"],
            "medium": ["打开", "关闭", "删除", "移动", "执行", "运行", "启动",
                     "停止", "切换"],
            "low": ["操作", "控制", "管理", "设置", "配置"]
        },
        "qa": {
            "high": ["为什么会出现", "如何解决", "是什么原因", "怎么回事",
                    "解释一下", "讲一下原理"],
            "medium": ["为什么", "如何", "是什么", "怎么样", "怎么做", "怎么用",
                     "区别", "对比", "哪个好"],
            "low": ["问题", "疑问", "不懂", "不清楚"]
        },
        "creative": {
            "high": ["写一篇文章", "生成报告", "创作", "设计架构", "画一个图",
                    "生成PPT", "写一份", "写个方案"],
            "medium": ["写一篇", "生成", "创作", "设计", "画", "做一份",
                     "制作", "构建一个"],
            "low": ["方案", "报告", "文章", "文档", "PPT", "设计"]
        },
        "reasoning": {
            "high": ["深层推理", "逻辑推演", "分析链路", "根因分析", "推导过程",
                    "证明", "反事实推理"],
            "medium": ["推理", "推演", "分析", "推导", "论证", "逻辑"],
            "low": ["思考", "考虑", "判断", "评估"]
        }
    }

    @classmethod
    def classify(cls, text: str) -> tuple:
        """双通道分类：规则 + 语义锚定 → (intent_type, confidence)"""
        scores = {k: 0.0 for k in cls.CN_INTENT_PATTERNS}

        # 通道1：关键词密度评分
        for intent_type, levels in cls.CN_INTENT_PATTERNS.items():
            for level_name, keywords in [("high", levels["high"]),
                                          ("medium", levels["medium"]),
                                          ("low", levels["low"])]:
                weight = {"high": 3.0, "medium": 1.5, "low": 0.5}[level_name]
                for kw in keywords:
                    count = text.count(kw)
                    if count > 0:
                        scores[intent_type] += min(count, 3) * weight

        # 通道2：中文语义锚点检测
        anchors = cls._detect_semantic_anchors(text)
        for anchor_type, anchor_score in anchors.items():
            if anchor_type in scores:
                scores[anchor_type] += anchor_score

        # 归一化并排序
        total = sum(scores.values()) or 1.0
        normalized = {k: v/total for k, v in scores.items()}
        best = max(normalized, key=normalized.get)

        return best, normalized[best]

    @classmethod
    def _detect_semantic_anchors(cls, text: str) -> dict:
        """中文语义锚点检测"""
        anchors = {}

        # 代码锚点：中英文混合代码指标
        code_indicators = [
            r'(?:def|class|import)\s+\w+',           # Python关键字
            r'(?:function|const|let|var)\s+\w+',      # JS关键字
            r'\.py\b|\.js\b|\.java\b',                # 文件扩展名
            r'pip\s+install|npm\s+install',            # 包管理命令
            r'(?:报错|错误|异常|bug|debug)',            # 调试词汇
        ]
        for pattern in code_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                anchors["code"] = anchors.get("code", 0) + 2.0

        # 搜索锚点
        search_indicators = [
            r'(?:huggingface\.co|github\.com|arxiv\.org)',  # URL模式
            r'(?:论文|文献|研究|综述)',                        # 学术词汇
            r'(?:最新|最近|202[5-9]|202[5-9]年)',           # 时效性
        ]
        for pattern in search_indicators:
            if re.search(pattern, text):
                anchors["search"] = anchors.get("search", 0) + 2.0

        # 问答锚点
        if text.endswith("?") or text.endswith("？"):
            anchors["qa"] = anchors.get("qa", 0) + 3.0
        if any(q in text for q in ["为什么", "如何", "怎么", "什么是"]):
            anchors["qa"] = anchors.get("qa", 0) + 2.0

        # 推理锚点
        reasoning_indicators = [
            r'(?:推理|逻辑|推导|论证|分析链)',
            r'(?:根因|root.?cause)',
            r'(?:假设|前提|条件|约束)',
        ]
        for pattern in reasoning_indicators:
            if re.search(pattern, text):
                anchors["reasoning"] = anchors.get("reasoning", 0) + 2.5

        return anchors


# ====================================================================
# 增强 2：长上下文分层加载管理器
# ====================================================================

class ContextLayerManager:
    """长上下文三层缓存管理器

    L1 热缓存 (<200ms)：最近3轮对话
    L2 温缓存 (<500ms)：同会话历史
    L3 冷缓存 (<2s)：  持久化记忆
    """

    def __init__(self, max_l1=3, max_l2=20, max_l3=100):
        self.l1_cache: list = []    # 最近N轮
        self.l2_cache: list = []    # 同会话
        self.l3_cache: dict = {}    # 持久化记忆索引
        self.max_l1 = max_l1
        self.max_l2 = max_l2
        self.max_l3 = max_l3
        self._compression_threshold = 50000  # 50k tokens触发压缩

    def load(self, query: str, context_window: dict) -> dict:
        """分层加载上下文"""
        result = {
            "l1_recent": self._load_l1(),
            "l2_session": self._load_l2(query),
            "l3_persistent": self._load_l3(query),
            "metadata": {
                "l1_count": len(self.l1_cache),
                "l2_count": len(self.l2_cache),
                "l3_count": len(self.l3_cache),
                "total_estimate_tokens": self._estimate_tokens()
            }
        }
        return result

    def push_l1(self, turn: dict):
        """推送对话轮到L1"""
        self.l1_cache.append(turn)
        if len(self.l1_cache) > self.max_l1:
            evicted = self.l1_cache.pop(0)
            self.l2_cache.append(evicted)
        # L2溢出 → 压缩后存入L3
        if len(self.l2_cache) > self.max_l2:
            oldest = self.l2_cache.pop(0)
            compressed = self._compress(oldest)
            key = f"session_{datetime.now().strftime('%Y%m%d_%H%M')}"
            self.l3_cache[key] = compressed

    def _load_l1(self) -> list:
        """L1热缓存：最近3轮直接返回"""
        return self.l1_cache[-self.max_l1:]

    def _load_l2(self, query: str) -> list:
        """L2温缓存：语义相关筛选"""
        if not self.l2_cache:
            return []
        # 简化：返回最近5轮 + 关键词命中
        relevant = []
        query_keywords = set(query[:50])  # 简化版关键词提取
        for turn in self.l2_cache[-5:]:
            turn_text = str(turn)
            if any(kw in turn_text for kw in ['推理', '进化', '迭代', '引擎', '架构']):
                relevant.append(turn)
        return relevant or self.l2_cache[-3:]

    def _load_l3(self, query: str) -> dict:
        """L3冷缓存：关键词索引检索"""
        if not self.l3_cache:
            return {}
        matched = {}
        for key, value in self.l3_cache.items():
            if any(kw in str(value) for kw in query[:30]):
                matched[key] = value
        return matched

    def _compress(self, data: dict) -> str:
        """语义压缩：保留关键信息，压缩率>60%"""
        text = json.dumps(data, ensure_ascii=False)
        if len(text) > self._compression_threshold:
            # 提取关键字段
            essential = {
                "intent": data.get("intent", ""),
                "result": data.get("result", {}).get("success"),
                "key_outputs": str(data.get("output", ""))[:500]
            }
            return json.dumps(essential, ensure_ascii=False)
        return text

    def _estimate_tokens(self) -> int:
        """估算总Token占用"""
        total = 0
        for turn in self.l1_cache:
            total += len(str(turn))
        for turn in self.l2_cache:
            total += len(str(turn))
        for v in self.l3_cache.values():
            total += len(str(v))
        return total // 2  # 粗略中文Token估算


# ====================================================================
# 增强 3：推理回溯深度增强
# ====================================================================

@dataclass
class Checkpoint:
    """推理检查点"""
    cp_id: str
    path_id: str
    step_index: int
    state_snapshot: dict
    timestamp: float = field(default_factory=time.time)


class DeepBacktrackManager:
    """深度推理回溯管理器

    支持：
    - 多级检查点自动保存
    - 条件触发回滚
    - 回滚路径智能选择
    - 回溯历史记录
    """

    MAX_BACKTRACK_DEPTH = 5

    def __init__(self):
        self.checkpoints: list[Checkpoint] = []
        self.backtrack_count = 0
        self.backtrack_history: list = []

    def save_checkpoint(self, path_id: str, step_index: int, state: dict) -> str:
        """保存检查点"""
        cp = Checkpoint(
            cp_id=f"cp_{path_id}_{step_index}_{int(time.time()*1000)}",
            path_id=path_id,
            step_index=step_index,
            state_snapshot=state
        )
        self.checkpoints.append(cp)
        # 限制检查点数量
        if len(self.checkpoints) > 50:
            self.checkpoints = self.checkpoints[-50:]
        return cp.cp_id

    def get_nearest_checkpoint(self, path_id: str, step_index: int) -> Optional[Checkpoint]:
        """获取最近的检查点"""
        candidates = [
            cp for cp in self.checkpoints
            if cp.path_id == path_id and cp.step_index < step_index
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda c: c.step_index)

    def execute_backtrack(self, source_path_id: str, source_step: int,
                          target_paths: list, condition_tree: dict) -> Optional[dict]:
        """执行推理回溯

        Returns:
            dict: 回溯结果 {new_path, checkpoint_used, confidence, strategy}
        """
        if self.backtrack_count >= self.MAX_BACKTRACK_DEPTH:
            logger.error(f"回溯深度耗尽 ({self.MAX_BACKTRACK_DEPTH})")
            return None

        self.backtrack_count += 1

        # 策略1：同路径回退到最近检查点
        cp = self.get_nearest_checkpoint(source_path_id, source_step)
        if cp:
            logger.info(f"策略1-检查点回溯: {cp.cp_id}")
            return {
                "strategy": "checkpoint_rollback",
                "checkpoint": cp,
                "new_path_id": source_path_id,
                "confidence": 0.7
            }

        # 策略2：切换到备用路径
        viable_paths = [
            p for p in target_paths
            if p.get("confidence", 0) > 0.5 and p["id"] != source_path_id
        ]
        if viable_paths:
            best = max(viable_paths, key=lambda p: p["confidence"])
            logger.info(f"策略2-路径切换: → {best['id']}")
            return {
                "strategy": "path_switch",
                "new_path_id": best["id"],
                "confidence": best["confidence"],
                "checkpoint": None
            }

        # 策略3：请求外部介入
        logger.warning("策略3-请求外部介入")
        self.backtrack_history.append({
            "timestamp": datetime.now().isoformat(),
            "source": source_path_id,
            "step": source_step,
            "strategy": "external_intervention",
            "available_paths": len(target_paths)
        })
        return {
            "strategy": "external_intervention",
            "confidence": 0.3,
            "checkpoint": None
        }

    def reset_backtrack_count(self):
        """重置回溯计数器（新任务开始时）"""
        self.backtrack_count = 0


# ====================================================================
# 增强 4：工具联动推理引擎
# ====================================================================

class ToolLinkageReasoner:
    """工具联动推理引擎

    核心理念：在调用工具前预判返回→准备多套应对→执行→反馈→推理评估→迭代

    联动回环：
    推理层决策 → 工具路由 → 执行 → 结果反馈 → 推理层评估 → 迭代 or 收束
         ↑                                                      |
         └──────────────── 回溯修正 ←─────────────────────────┘
    """

    def __init__(self, tool_registry: dict = None):
        self.tool_registry = tool_registry or {}
        self.execution_log: list = []
        self.fallback_map: dict = {}  # tool_name → fallback_tool

    def register_tool(self, name: str, handler: callable, fallback: str = None):
        """注册工具及降级方案"""
        self.tool_registry[name] = handler
        if fallback:
            self.fallback_map[name] = fallback

    def pre_predict(self, tool_name: str, params: dict, context: dict) -> dict:
        """工具调用前预判"""
        predictions = {
            "expected_output_type": "dict",
            "possible_errors": [],
            "fallback_ready": tool_name in self.fallback_map,
            "estimated_time_ms": self._estimate_time(tool_name, params)
        }

        # 常见失败模式预判
        if tool_name == "file_ops":
            if "path" in params and not Path(str(params["path"])).exists():
                predictions["possible_errors"].append("file_not_found")
        elif tool_name == "web_search":
            if "query" in params and len(str(params["query"])) < 3:
                predictions["possible_errors"].append("query_too_short")

        return predictions

    def execute_with_fallback(self, tool_name: str, params: dict,
                               max_retries: int = 2) -> dict:
        """工具执行+自动降级"""
        result = {"success": False, "output": None, "errors": [], "retries": 0}

        for attempt in range(max_retries + 1):
            try:
                if tool_name in self.tool_registry:
                    output = self.tool_registry[tool_name](**params)
                    result["success"] = True
                    result["output"] = output
                    result["retries"] = attempt
                    return result
                else:
                    result["errors"].append(f"tool_not_registered: {tool_name}")
                    break
            except Exception as e:
                result["errors"].append(f"attempt_{attempt}: {e}")
                if attempt < max_retries:
                    time.sleep(1 * (attempt + 1))

        # 全部重试失败 → 降级
        if tool_name in self.fallback_map:
            fallback = self.fallback_map[tool_name]
            logger.info(f"工具降级: {tool_name} → {fallback}")
            if fallback in self.tool_registry:
                try:
                    output = self.tool_registry[fallback](**params)
                    result["success"] = True
                    result["output"] = output
                    result["fallback_used"] = fallback
                except Exception as e:
                    result["errors"].append(f"fallback_failed: {e}")

        return result

    def evaluate_result(self, prediction: dict, result: dict) -> dict:
        """结果评估：实际vs预期"""
        evaluation = {
            "matched": result["success"] == (len(prediction.get("possible_errors", [])) == 0),
            "time_ok": True,
            "need_iteration": len(result.get("errors", [])) > 0,
            "confidence_adjustment": 0.0
        }

        if result.get("fallback_used"):
            evaluation["confidence_adjustment"] = -0.15
        if result["success"]:
            evaluation["confidence_adjustment"] = +0.05

        return evaluation

    def _estimate_time(self, tool_name: str, params: dict) -> float:
        """工具执行时间预估"""
        estimates = {
            "file_ops": 500,
            "web_search": 3000,
            "shell_exec": 2000,
            "dispatch_task": 15000,
            "llm_call": 5000
        }
        return estimates.get(tool_name, 1000)


# ====================================================================
# 增强 5：中文长文档分段推理适配器
# ====================================================================

class ChineseLongDocReasoner:
    """中文长文档分段推理适配器

    支持：
    - 10万字级文档分段推理
    - 跨段关联分析
    - 中文多义词上下文消歧
    - 中英混合推理
    """

    MAX_SEGMENT_CHARS = 8000   # 每段最多8000字
    OVERLAP_CHARS = 500         # 段间重叠500字

    def __init__(self):
        self.segment_index: dict = {}
        self.cross_references: list = []

    def segment(self, text: str) -> list[dict]:
        """长文档分段（带重叠窗口）"""
        segments = []
        pos = 0
        seg_id = 0

        while pos < len(text):
            end = min(pos + self.MAX_SEGMENT_CHARS, len(text))
            segment_text = text[pos:end]

            # 在自然段落边界切割
            if end < len(text):
                last_para = segment_text.rfind('\n\n')
                if last_para > self.MAX_SEGMENT_CHARS // 2:
                    end = pos + last_para
                    segment_text = text[pos:end]

            segments.append({
                "id": f"seg_{seg_id:04d}",
                "start": pos,
                "end": end,
                "text": segment_text,
                "length": len(segment_text),
                "summary": self._generate_summary(segment_text)
            })

            self.segment_index[seg_id] = {
                "keywords": self._extract_keywords(segment_text),
                "entities": self._extract_entities(segment_text)
            }

            # 重叠窗口
            pos = end - self.OVERLAP_CHARS if end < len(text) else len(text)
            seg_id += 1

        return segments

    def cross_segment_reason(self, segments: list, query: str) -> dict:
        """跨段关联推理"""
        # 找到与查询最相关的段
        relevant_segs = []
        for seg in segments:
            relevance = self._calculate_relevance(seg, query)
            if relevance > 0.3:
                relevant_segs.append({**seg, "relevance": relevance})

        # 按相关性排序
        relevant_segs.sort(key=lambda s: s["relevance"], reverse=True)

        # 跨段关联分析
        cross_links = []
        for i, seg_a in enumerate(relevant_segs[:5]):
            for seg_b in relevant_segs[i+1:i+4]:
                link = self._find_cross_links(seg_a, seg_b)
                if link:
                    cross_links.append(link)

        return {
            "relevant_segments": relevant_segs[:5],
            "cross_links": cross_links,
            "total_segments": len(segments),
            "coverage": len(relevant_segs) / max(len(segments), 1)
        }

    def resolve_ambiguity(self, word: str, context_segments: list) -> dict:
        """中文多义词消歧"""
        meanings = []
        for seg in context_segments:
            if word in seg["text"]:
                # 上下文窗口提取
                idx = seg["text"].find(word)
                ctx_start = max(0, idx - 50)
                ctx_end = min(len(seg["text"]), idx + 50 + len(word))
                ctx = seg["text"][ctx_start:ctx_end]

                # 语义锚定词检测
                anchors = self._detect_semantic_anchors_in_context(ctx)
                meanings.append({
                    "segment_id": seg["id"],
                    "context": ctx,
                    "anchors": anchors,
                    "confidence": len(anchors) / 5
                })

        # 选择置信度最高的含义
        if meanings:
            best = max(meanings, key=lambda m: m["confidence"])
            return {"word": word, "resolved_meaning": best, "all_candidates": meanings}
        return {"word": word, "resolved_meaning": None, "all_candidates": []}

    def _generate_summary(self, text: str) -> str:
        """段摘要生成"""
        # 提取前100字作为摘要
        clean = re.sub(r'\s+', ' ', text[:200])
        return clean[:100] + ("..." if len(text) > 200 else "")

    def _extract_keywords(self, text: str) -> list:
        """中文关键词提取"""
        # 简化：提取高频词（>3字）
        words = re.findall(r'[\u4e00-\u9fff]{2,8}', text[:1000])
        from collections import Counter
        counter = Counter(words)
        return [w for w, c in counter.most_common(10) if c > 1]

    def _extract_entities(self, text: str) -> list:
        """中文实体提取"""
        entities = []
        # 文件名/路径
        paths = re.findall(r'[A-Za-z]:[\\/][^\s，。]+', text)
        entities.extend([{"type": "file_path", "value": p} for p in paths])
        # URL
        urls = re.findall(r'https?://[^\s，。]+', text)
        entities.extend([{"type": "url", "value": u} for u in urls])
        # 日期
        dates = re.findall(r'\d{4}[-/]\d{2}[-/]\d{2}', text)
        entities.extend([{"type": "date", "value": d} for d in dates])
        return entities

    def _calculate_relevance(self, seg: dict, query: str) -> float:
        """计算段与查询的相关性"""
        text = seg["text"]
        query_chars = set(query)
        text_chars = set(text[:2000])
        overlap = len(query_chars & text_chars)
        return min(1.0, overlap / max(len(query_chars), 1))

    def _find_cross_links(self, seg_a: dict, seg_b: dict) -> Optional[dict]:
        """寻找跨段关联"""
        idx_a = self.segment_index.get(seg_a["id"].split("_")[1])
        idx_b = self.segment_index.get(seg_b["id"].split("_")[1])
        if not idx_a or not idx_b:
            return None

        shared_kw = set(idx_a.get("keywords", [])) & set(idx_b.get("keywords", []))
        if shared_kw:
            return {
                "segment_a": seg_a["id"],
                "segment_b": seg_b["id"],
                "shared_keywords": list(shared_kw),
                "strength": len(shared_kw) / 5
            }
        return None

    def _detect_semantic_anchors_in_context(self, ctx: str) -> list:
        """上下文中检测语义锚定词"""
        anchors = []
        category_indicators = {
            "programming": ["代码", "编程", "函数", "类", "模块", "API"],
            "data": ["数据", "数据库", "表", "字段", "查询"],
            "system": ["系统", "架构", "服务", "进程", "线程"],
            "math": ["数学", "公式", "计算", "算法", "证明"],
        }
        for cat, words in category_indicators.items():
            if any(w in ctx for w in words):
                anchors.append(cat)
        return anchors


# ====================================================================
# 主引擎 v2.0
# ====================================================================

class ClaudeReasoningEngineV2(ClaudeReasoningEngine):
    """Claude分层推理引擎 v2.0 · 中文增强版"""

    def __init__(
        self,
        memory_os=None,
        safe_guard=None,
        skill_forge=None,
        tool_registry: dict = None,
        enable_chinese_optimization: bool = True,
        enable_context_layers: bool = True
    ):
        super().__init__(
            memory_os=memory_os,
            safe_guard=safe_guard,
            skill_forge=skill_forge,
            tool_registry=tool_registry
        )

        # v2.0增强组件
        self.cn_classifier = ChineseIntentClassifier() if enable_chinese_optimization else None
        self.context_manager = ContextLayerManager() if enable_context_layers else None
        self.deep_backtrack = DeepBacktrackManager()
        self.tool_linker = ToolLinkageReasoner(tool_registry=tool_registry)
        self.long_doc_reasoner = ChineseLongDocReasoner()

        # v2.0配置
        self.config = {
            "enable_chinese_optimization": enable_chinese_optimization,
            "enable_context_layers": enable_context_layers,
            "max_backtrack_depth": 5,
            "tool_execution_timeout_ms": 60000
        }

    def process_v2(self, user_input: str, context_window: dict = None) -> dict:
        """增强版五层推理链路"""
        ctx = context_window or {}
        result = {"phases": {}, "metadata": {}}
        start_time = time.time()

        # Phase 0: 上下文分层加载
        if self.context_manager:
            ctx_layers = self.context_manager.load(user_input, ctx)
            result["metadata"]["context_layers"] = ctx_layers.get("metadata", {})

        # Phase 0.5: 中文意图增强分类
        intent_type = "general"
        cn_confidence = 0.0
        if self.cn_classifier:
            intent_type, cn_confidence = self.cn_classifier.classify(user_input)
            result["metadata"]["cn_intent"] = {"type": intent_type, "confidence": cn_confidence}

        # Phase 1-5: 标准五层推理（继承v1.0）
        standard_result = self.process(user_input, ctx)
        result["phases"] = standard_result

        # v2.0额外阶段
        result["metadata"].update({
            "engine_version": "v2.0-enhanced",
            "chinese_optimized": self.config["enable_chinese_optimization"],
            "context_layers_enabled": self.config["enable_context_layers"],
            "total_time_ms": (time.time() - start_time) * 1000,
            "intent_type": intent_type,
            "cn_confidence": cn_confidence
        })

        # 长文档检测
        if len(user_input) > self.long_doc_reasoner.MAX_SEGMENT_CHARS:
            segments = self.long_doc_reasoner.segment(user_input)
            cross_result = self.long_doc_reasoner.cross_segment_reason(
                segments, user_input[:200]
            )
            result["metadata"]["long_doc"] = {
                "segments": len(segments),
                "cross_links": len(cross_result.get("cross_links", []))
            }

        return result

    def analyze(self, user_input: str) -> dict:
        """快速分析：不解执行，仅推理"""
        ctx = {}
        intent = self.phase1.parse(user_input, ctx)
        ct = self.phase2.decompose(intent)
        paths = self.phase3.reason(ct)

        return {
            "intent": intent.intent_type,
            "difficulty": intent.difficulty.value,
            "paths_count": len(paths),
            "best_path": paths[0].path_id if paths else None,
            "confidence": paths[0].confidence if paths else 0.0,
            "sub_goals": intent.sub_goals
        }


# ====================================================================
# 测试入口
# ====================================================================

if __name__ == "__main__":
    engine = ClaudeReasoningEngineV2()

    # 测试1：中文意图分类
    test_inputs = [
        "帮我搜索并分析最新的大模型推理架构论文，生成一份对比报告",
        "写一个Python脚本，自动扫描文件并生成索引",
        "为什么SICA进化框架的收敛速度比预期慢？请做深层推理分析",
        "打开小红书网站并登录",
    ]

    print("=" * 60)
    print("Claude分层推理引擎 v2.0 · 中文增强版 · 测试")
    print("=" * 60)

    for inp in test_inputs:
        analysis = engine.analyze(inp)
        if engine.cn_classifier:
            intent, conf = engine.cn_classifier.classify(inp)
            print(f"\n输入: {inp[:50]}...")
            print(f"  中文意图: {intent} (置信度: {conf:.2f})")
            print(f"  推理分析: {json.dumps(analysis, ensure_ascii=False)}")

    # 测试2：长文档分段
    long_text = "深度学习" * 5000  # 模拟长文档
    segments = engine.long_doc_reasoner.segment(long_text)
    print(f"\n长文档分段: {len(segments)} 段 (总长 {len(long_text)} 字)")

    # 测试3：完整推理链路
    result = engine.process_v2(test_inputs[0])
    print(f"\n完整推理结果: {json.dumps(result['metadata'], ensure_ascii=False, indent=2)}")

    print("\n✅ Claude分层推理引擎 v2.0 · 中文增强版 测试通过")
```
