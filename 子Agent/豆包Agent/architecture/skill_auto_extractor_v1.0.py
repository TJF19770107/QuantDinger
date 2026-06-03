"""
技能自动萃取引擎 · SkillAutoExtractor v1.0
==========================================
从执行日志、推理路径、工具调用记录中自动：
 1. 模式识别 → 发现高频/高成功率操作模式
 2. 质量评分 → 多维度评估模式成熟度
 3. Skill模板生成 → 自动生成标准化Skill JSON
 4. 入库审查 → 安全/质量/去重三重检查
 5. 迭代优化 → 基于新执行数据持续优化已有Skill

R13 全域缺口专项补全 · P0-3 技能自动萃取落地
"""

import json
import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SkillAutoExtractor")


# ====================================================================
# 数据结构
# ====================================================================

@dataclass
class ExecutionPattern:
    """执行模式：从日志中提取的重复操作模式"""
    pattern_id: str
    pattern_type: str                # action_sequence / tool_chain / reasoning_path
    steps: list                      # 步骤列表
    frequency: int = 0               # 出现次数
    success_rate: float = 0.0        # 成功率
    avg_execution_time_ms: float = 0.0
    tools_used: list = field(default_factory=list)
    preconditions: list = field(default_factory=list)
    postconditions: list = field(default_factory=list)
    first_seen: str = ""
    last_seen: str = ""

    def maturity_score(self) -> float:
        """模式成熟度评分"""
        freq_score = min(1.0, self.frequency / 10)
        success_score = self.success_rate
        stability_score = 1.0 if self.frequency >= 3 else 0.5
        return (freq_score * 0.3 + success_score * 0.5 + stability_score * 0.2)


@dataclass
class SkillCandidate:
    """技能候选：准备入库的技能"""
    candidate_id: str
    name: str
    description: str
    category: str                   # file_ops / search / reasoning / system / creative
    trigger_words: list             # 触发词
    execution_pattern: dict         # 执行模板
    tools_chain: list               # 工具调用链
    quality_score: float = 0.0
    generated_at: str = ""
    source_pattern_id: str = ""


# ====================================================================
# 模式识别引擎
# ====================================================================

class PatternRecognitionEngine:
    """从执行日志中识别重复操作模式"""

    MIN_FREQUENCY = 2               # 最少出现次数才算模式
    MIN_SUCCESS_RATE = 0.5          # 最低成功率
    PATTERN_SIMILARITY_THRESHOLD = 0.7  # 模式相似度阈值（合并用）

    def __init__(self):
        self.raw_logs: list = []
        self.found_patterns: list[ExecutionPattern] = []

    def analyze_logs(self, log_entries: list[dict]) -> list[ExecutionPattern]:
        """分析执行日志，提取操作模式"""
        self.raw_logs = log_entries

        # Step 1: 按工具调用链分组
        chains = self._group_by_tool_chain(log_entries)

        # Step 2: 识别高频操作序列
        patterns = []
        for chain_key, entries in chains.items():
            if len(entries) < self.MIN_FREQUENCY:
                continue

            success_count = sum(1 for e in entries if e.get("success", False))
            success_rate = success_count / len(entries)

            if success_rate < self.MIN_SUCCESS_RATE:
                continue

            # 提取步骤模板
            steps = self._extract_step_template(entries)
            tools = self._extract_tools(entries)
            preconditions = self._infer_preconditions(entries)
            postconditions = self._infer_postconditions(entries)

            times = [e.get("execution_time_ms", 0) for e in entries if e.get("execution_time_ms")]
            avg_time = sum(times) / len(times) if times else 0

            pattern = ExecutionPattern(
                pattern_id=f"pat_{hashlib.md5(chain_key.encode()).hexdigest()[:12]}",
                pattern_type=self._classify_pattern_type(steps, tools),
                steps=steps,
                frequency=len(entries),
                success_rate=success_rate,
                avg_execution_time_ms=avg_time,
                tools_used=tools,
                preconditions=preconditions,
                postconditions=postconditions,
                first_seen=min(e.get("timestamp", "") for e in entries),
                last_seen=max(e.get("timestamp", "") for e in entries)
            )
            patterns.append(pattern)

        # Step 3: 合并相似模式
        merged = self._merge_similar_patterns(patterns)
        self.found_patterns = merged
        return merged

    def _group_by_tool_chain(self, logs: list) -> dict:
        """按工具调用链分组（抽象路径签名）"""
        groups = defaultdict(list)
        for entry in logs:
            tools = entry.get("tools_used", [])
            if not tools:
                continue
            # 生成工具链签名
            signature = "→".join(tools[:5])  # 取前5个工具
            groups[signature].append(entry)
        return dict(groups)

    def _extract_step_template(self, entries: list) -> list:
        """从多条目中提取步骤模板"""
        # 取最常见的步骤序列
        step_counter = Counter()
        for entry in entries:
            steps = tuple(entry.get("steps", [])[:3])  # 取前3步
            if steps:
                step_counter[steps] += 1

        if step_counter:
            most_common_steps = step_counter.most_common(1)[0][0]
            return list(most_common_steps)
        return []

    def _extract_tools(self, entries: list) -> list:
        """提取工具清单"""
        tool_counter = Counter()
        for entry in entries:
            for tool in entry.get("tools_used", []):
                tool_counter[tool] += 1
        return [t for t, _ in tool_counter.most_common(8)]

    def _infer_preconditions(self, entries: list) -> list:
        """推断前置条件"""
        preconditions = []
        first_entry = entries[0] if entries else {}

        if first_entry.get("requires_file"):
            preconditions.append("file_exists")
        if first_entry.get("requires_network"):
            preconditions.append("network_available")
        if first_entry.get("requires_auth"):
            preconditions.append("authenticated")

        return preconditions

    def _infer_postconditions(self, entries: list) -> list:
        """推断后置条件"""
        postconditions = []
        for entry in entries:
            if entry.get("success") and entry.get("output_type") == "file":
                postconditions.append("file_created")
            if entry.get("success") and entry.get("output_type") == "report":
                postconditions.append("report_generated")
        return list(set(postconditions))

    def _classify_pattern_type(self, steps: list, tools: list) -> str:
        """分类模式类型"""
        tool_set = set(tools)

        if any("file_" in t for t in tool_set) or any("move" in t for t in tool_set):
            return "file_ops"
        if any("search" in t for t in tool_set):
            return "search"
        if any("reason" in t for t in tool_set) or any("analyze" in t for t in tool_set):
            return "reasoning"
        if any("execute" in t for t in tool_set) or any("shell" in t for t in tool_set):
            return "system"
        if any("generate" in t for t in tool_set) or any("write" in t for t in tool_set):
            return "creative"

        return "general"

    def _merge_similar_patterns(self, patterns: list) -> list:
        """合并相似模式"""
        if len(patterns) <= 1:
            return patterns

        merged = []
        used = set()

        for i, p1 in enumerate(patterns):
            if i in used:
                continue
            group = [p1]
            used.add(i)

            for j, p2 in enumerate(patterns):
                if j in used:
                    continue
                if self._similarity(p1, p2) >= self.PATTERN_SIMILARITY_THRESHOLD:
                    group.append(p2)
                    used.add(j)

            if len(group) == 1:
                merged.append(p1)
            else:
                merged.append(self._merge_group(group))

        return merged

    def _similarity(self, p1: ExecutionPattern, p2: ExecutionPattern) -> float:
        """计算模式相似度"""
        score = 0.0
        weights = {"tools": 0.4, "steps": 0.3, "type": 0.3}

        # 工具重合度
        tools1 = set(p1.tools_used)
        tools2 = set(p2.tools_used)
        if tools1 and tools2:
            score += weights["tools"] * len(tools1 & tools2) / max(len(tools1 | tools2), 1)

        # 步骤重合度
        steps1 = set(str(s) for s in p1.steps)
        steps2 = set(str(s) for s in p2.steps)
        if steps1 and steps2:
            score += weights["steps"] * len(steps1 & steps2) / max(len(steps1 | steps2), 1)

        # 类型相同
        if p1.pattern_type == p2.pattern_type:
            score += weights["type"]

        return score

    def _merge_group(self, group: list) -> ExecutionPattern:
        """合并一组相似模式"""
        base = group[0]
        total_freq = sum(p.frequency for p in group)
        avg_sr = sum(p.success_rate * p.frequency for p in group) / max(total_freq, 1)
        avg_time = sum(p.avg_execution_time_ms for p in group) / len(group)
        all_tools = list(set(t for p in group for t in p.tools_used))

        return ExecutionPattern(
            pattern_id=base.pattern_id,
            pattern_type=base.pattern_type,
            steps=base.steps,
            frequency=total_freq,
            success_rate=avg_sr,
            avg_execution_time_ms=avg_time,
            tools_used=all_tools,
            preconditions=list(set(c for p in group for c in p.preconditions)),
            postconditions=list(set(c for p in group for c in p.postconditions)),
            first_seen=min(p.first_seen for p in group),
            last_seen=max(p.last_seen for p in group)
        )


# ====================================================================
# 技能生成引擎
# ====================================================================

class SkillGenerator:
    """从执行模式生成标准化Skill JSON"""

    SKILL_TEMPLATE = {
        "schema_version": "2.0",
        "skill_id": "",
        "name": "",
        "description": "",
        "category": "",
        "trigger_words": [],
        "tools_chain": [],
        "execution_flow": {"sequential": [], "parallel": [], "conditional": []},
        "preconditions": [],
        "postconditions": [],
        "quality_metrics": {
            "success_rate": 0.0,
            "avg_time_ms": 0,
            "maturity": "alpha",
            "iteration_count": 0
        },
        "changelog": []
    }

    def __init__(self, skill_output_dir: str = ""):
        self.skill_output_dir = Path(skill_output_dir) if skill_output_dir else Path("技能库")
        self.skill_output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, pattern: ExecutionPattern) -> SkillCandidate:
        """从模式生成Skill候选"""
        maturity = pattern.maturity_score()
        maturity_label = "beta" if maturity > 0.7 else "alpha"

        # 生成触发词
        trigger_words = self._generate_trigger_words(pattern)

        # 生成技能名称
        name = self._generate_skill_name(pattern)

        # 生成描述
        description = self._generate_description(pattern)

        candidate = SkillCandidate(
            candidate_id=f"skill_{hashlib.md5(pattern.pattern_id.encode()).hexdigest()[:12]}",
            name=name,
            description=description,
            category=pattern.pattern_type,
            trigger_words=trigger_words,
            execution_pattern={
                "steps": pattern.steps,
                "tools": pattern.tools_used
            },
            tools_chain=pattern.tools_used,
            quality_score=maturity,
            generated_at=datetime.now().isoformat(),
            source_pattern_id=pattern.pattern_id
        )

        return candidate

    def to_skill_file(self, candidate: SkillCandidate) -> dict:
        """将候选转换为完整Skill JSON"""
        skill = json.loads(json.dumps(self.SKILL_TEMPLATE))
        skill["skill_id"] = candidate.candidate_id
        skill["name"] = candidate.name
        skill["description"] = candidate.description
        skill["category"] = candidate.category
        skill["trigger_words"] = candidate.trigger_words
        skill["tools_chain"] = candidate.tools_chain
        skill["execution_flow"]["sequential"] = candidate.execution_pattern.get("steps", [])
        skill["quality_metrics"]["success_rate"] = candidate.quality_score
        skill["quality_metrics"]["maturity"] = "beta" if candidate.quality_score > 0.7 else "alpha"
        skill["changelog"].append({
            "version": "1.0",
            "date": candidate.generated_at,
            "changes": "自动萃取生成",
            "source": candidate.source_pattern_id
        })

        return skill

    def write_skill(self, candidate: SkillCandidate) -> str:
        """写入Skill文件"""
        skill = self.to_skill_file(candidate)
        filename = f"{candidate.candidate_id}.json"
        filepath = self.skill_output_dir / filename
        filepath.write_text(json.dumps(skill, indent=2, ensure_ascii=False))
        logger.info(f"技能已生成: {filepath}")
        return str(filepath)

    def _generate_trigger_words(self, pattern: ExecutionPattern) -> list:
        """生成触发词"""
        trigger_map = {
            "file_ops": ["查找文件", "文件搜索", "整理文件", "移动文件", "扫描", "列表"],
            "search": ["搜索", "查找", "调研", "检索", "查资料", "搜集信息"],
            "reasoning": ["分析", "推理", "推导", "评估", "为什么", "根因"],
            "system": ["执行", "运行", "启动", "配置", "系统"],
            "creative": ["生成", "创建", "制作", "写一个", "画一个"],
        }

        words = trigger_map.get(pattern.pattern_type, ["处理", "执行"])
        # 从步骤中提取关键词
        for step in pattern.steps:
            step_str = str(step)[:50]
            chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', step_str)
            words.extend(chinese_words[:3])

        # 从工具名称提取
        for tool in pattern.tools_used[:3]:
            tool_name = tool.replace("_", " ").strip()
            if tool_name:
                words.append(tool_name)

        return list(set(words))[:10]

    def _generate_skill_name(self, pattern: ExecutionPattern) -> str:
        """生成技能名称"""
        category_prefix = {
            "file_ops": "文件",
            "search": "搜索",
            "reasoning": "推理",
            "system": "系统",
            "creative": "创作",
            "general": "通用"
        }

        prefix = category_prefix.get(pattern.pattern_type, "通用")
        # 使用步骤中第一个中文关键词作为操作描述
        for step in pattern.steps[:1]:
            step_str = str(step)
            words = re.findall(r'[\u4e00-\u9fff]{2,4}', step_str)
            if words:
                return f"{prefix}{words[0]}自动化"

        return f"{prefix}操作自动化"

    def _generate_description(self, pattern: ExecutionPattern) -> str:
        """生成技能描述"""
        tool_list = " → ".join(pattern.tools_used[:4])
        return (
            f"自动识别并执行{pattern.pattern_type}类操作。"
            f"工具链: {tool_list}。"
            f"成功率: {pattern.success_rate:.0%}，"
            f"已执行{pattern.frequency}次。"
            f"R13自动萃取。"
        )


# ====================================================================
# 入库审查器
# ====================================================================

class SkillReviewer:
    """技能入库三重审查：安全 → 质量 → 去重"""

    MIN_QUALITY_SCORE = 0.4
    MIN_FREQUENCY = 2
    MAX_SIMILARITY_FOR_DUPLICATE = 0.8

    def __init__(self, existing_skills_dir: str = None):
        self.existing_skills: dict = {}
        if existing_skills_dir:
            self._load_existing(Path(existing_skills_dir))

    def review(self, candidate: SkillCandidate, pattern: ExecutionPattern) -> dict:
        """三重审查"""
        result = {
            "candidate_id": candidate.candidate_id,
            "passed": False,
            "checks": {
                "safety": {"passed": True, "issues": []},
                "quality": {"passed": False, "score": candidate.quality_score},
                "duplicate": {"passed": True, "similar_to": None}
            },
            "action": "reject"
        }

        # 审查1：安全检查
        safety = self._safety_check(candidate, pattern)
        result["checks"]["safety"] = safety
        if not safety["passed"]:
            result["action"] = "reject_security"
            return result

        # 审查2：质量检查
        quality = self._quality_check(candidate, pattern)
        result["checks"]["quality"] = quality
        if not quality["passed"]:
            result["action"] = "reject_quality"
            return result

        # 审查3：去重检查
        duplicate = self._duplicate_check(candidate)
        result["checks"]["duplicate"] = duplicate
        if not duplicate["passed"]:
            result["action"] = "skip_duplicate"
            return result

        # 全部通过
        result["passed"] = True
        result["action"] = "accept"

        # 将技能加入已存在列表（防后续重复）
        self.existing_skills[candidate.candidate_id] = candidate

        return result

    def _safety_check(self, candidate: SkillCandidate, pattern: ExecutionPattern) -> dict:
        """安全检查"""
        issues = []
        dangerous_tools = ["delete", "rm", "format", "kill", "uninstall", "clear"]
        dangerous_operations = ["删除", "格式化", "清空", "卸载", "重置"]

        # 检查危险工具
        for tool in pattern.tools_used:
            if any(dt in tool.lower() for dt in dangerous_tools):
                issues.append(f"包含危险工具: {tool}")

        # 检查危险操作描述
        for step in pattern.steps:
            step_str = str(step)
            if any(dop in step_str for dop in dangerous_operations):
                issues.append(f"包含危险操作: {step_str[:60]}")

        return {"passed": len(issues) == 0, "issues": issues}

    def _quality_check(self, candidate: SkillCandidate, pattern: ExecutionPattern) -> dict:
        """质量检查"""
        passed = (
            candidate.quality_score >= self.MIN_QUALITY_SCORE
            and pattern.frequency >= self.MIN_FREQUENCY
            and pattern.success_rate >= 0.5
        )

        return {
            "passed": passed,
            "score": candidate.quality_score,
            "frequency": pattern.frequency,
            "success_rate": pattern.success_rate
        }

    def _duplicate_check(self, candidate: SkillCandidate) -> dict:
        """去重检查"""
        for existing_id, existing in self.existing_skills.items():
            similarity = self._skill_similarity(candidate, existing)
            if similarity >= self.MAX_SIMILARITY_FOR_DUPLICATE:
                return {"passed": False, "similar_to": existing_id}

        return {"passed": True, "similar_to": None}

    def _skill_similarity(self, a: SkillCandidate, b: SkillCandidate) -> float:
        """技能相似度计算"""
        score = 0.0
        # 类别相同
        if a.category == b.category:
            score += 0.3
        # 工具链重合
        tools_a = set(a.tools_chain)
        tools_b = set(b.tools_chain)
        if tools_a and tools_b:
            score += 0.4 * len(tools_a & tools_b) / max(len(tools_a | tools_b), 1)
        # 触发词重合
        words_a = set(a.trigger_words)
        words_b = set(b.trigger_words)
        if words_a and words_b:
            score += 0.3 * len(words_a & words_b) / max(len(words_a | words_b), 1)
        return score

    def _load_existing(self, skills_dir: Path):
        """加载已有技能"""
        if not skills_dir.exists():
            return
        for f in skills_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                self.existing_skills[data.get("skill_id", f.stem)] = data
            except Exception:
                pass


# ====================================================================
# 萃取流水线
# ====================================================================

class SkillAutoExtractionPipeline:
    """技能自动萃取完整流水线

    流程: 日志输入 → 模式识别 → 候选生成 → 审查 → 入库 → 迭代优化
    """

    def __init__(self, skill_output_dir: str, existing_skills_dir: str = None):
        self.pattern_engine = PatternRecognitionEngine()
        self.skill_generator = SkillGenerator(skill_output_dir)
        self.reviewer = SkillReviewer(existing_skills_dir)
        self.history: list = []

    def run(self, log_entries: list[dict]) -> dict:
        """执行完整萃取流水线"""
        pipeline_id = f"extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        result = {
            "pipeline_id": pipeline_id,
            "started_at": datetime.now().isoformat(),
            "stages": {},
            "summary": {}
        }

        # Stage 1: 模式识别
        logger.info(f"[{pipeline_id}] Stage 1: 模式识别")
        patterns = self.pattern_engine.analyze_logs(log_entries)
        result["stages"]["pattern_recognition"] = {
            "patterns_found": len(patterns),
            "pattern_types": [p.pattern_type for p in patterns]
        }

        # Stage 2: 候选生成
        logger.info(f"[{pipeline_id}] Stage 2: 候选生成 ({len(patterns)}个模式)")
        candidates = []
        for pattern in patterns:
            candidate = self.skill_generator.generate(pattern)
            candidates.append(candidate)
            result["stages"][f"candidate_{candidate.candidate_id}"] = {
                "quality_score": candidate.quality_score,
                "category": candidate.category
            }

        # Stage 3: 审查入库
        logger.info(f"[{pipeline_id}] Stage 3: 审查入库 ({len(candidates)}个候选)")
        accepted = 0
        rejected = 0
        written_files = []

        for candidate in candidates:
            pattern = next((p for p in patterns if p.pattern_id == candidate.source_pattern_id), None)
            if not pattern:
                continue

            review = self.reviewer.review(candidate, pattern)
            if review["passed"]:
                filepath = self.skill_generator.write_skill(candidate)
                written_files.append(filepath)
                accepted += 1
            else:
                rejected += 1

            result["stages"][f"review_{candidate.candidate_id}"] = review

        # Stage 4: 汇总
        result["summary"] = {
            "total_patterns": len(patterns),
            "total_candidates": len(candidates),
            "accepted": accepted,
            "rejected": rejected,
            "written_files": written_files,
            "completed_at": datetime.now().isoformat()
        }

        # 保存管道历史
        self.history.append(result)

        logger.info(
            f"[{pipeline_id}] 萃取完成: "
            f"{len(patterns)}模式 → {len(candidates)}候选 → "
            f"{accepted}入库 / {rejected}拒绝"
        )

        return result

    def get_history_summary(self) -> dict:
        """获取萃取历史摘要"""
        if not self.history:
            return {"runs": 0, "total_accepted": 0}

        total_accepted = sum(
            h.get("summary", {}).get("accepted", 0) for h in self.history
        )
        return {
            "runs": len(self.history),
            "total_accepted": total_accepted,
            "last_run": self.history[-1]["pipeline_id"],
            "last_accepted": self.history[-1].get("summary", {}).get("accepted", 0)
        }


# ====================================================================
# 演进优化器
# ====================================================================

class SkillIterationOptimizer:
    """技能迭代优化器：基于新执行数据更新已有Skill"""

    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)

    def optimize(self, skill_id: str, new_execution_data: dict) -> dict:
        """基于新的执行数据优化技能"""
        skill_path = self.skills_dir / f"{skill_id}.json"
        if not skill_path.exists():
            return {"error": "skill_not_found", "skill_id": skill_id}

        skill = json.loads(skill_path.read_text())

        # 更新质量指标
        metrics = skill.get("quality_metrics", {})
        old_sr = metrics.get("success_rate", 0)
        old_count = metrics.get("iteration_count", 0)
        new_success = new_execution_data.get("success", False)

        # 加权更新成功率
        metrics["success_rate"] = (old_sr * old_count + (1 if new_success else 0)) / (old_count + 1)
        metrics["iteration_count"] = old_count + 1

        # 更新成熟度
        if metrics["iteration_count"] >= 20 and metrics["success_rate"] > 0.9:
            metrics["maturity"] = "stable"
        elif metrics["iteration_count"] >= 5 and metrics["success_rate"] > 0.7:
            metrics["maturity"] = "beta"

        # 更新变更记录
        skill.setdefault("changelog", []).append({
            "version": f"1.{metrics['iteration_count']}",
            "date": datetime.now().isoformat(),
            "changes": f"自动迭代优化: 成功率 {old_sr:.2f}→{metrics['success_rate']:.2f}",
            "execution_data": {
                "success": new_success,
                "time_ms": new_execution_data.get("execution_time_ms", 0)
            }
        })

        skill_path.write_text(json.dumps(skill, indent=2, ensure_ascii=False))
        return {"optimized": True, "skill_id": skill_id, "new_success_rate": metrics["success_rate"]}


# ====================================================================
# 测试入口
# ====================================================================

if __name__ == "__main__":
    # 模拟执行日志
    sample_logs = [
        {
            "timestamp": "2026-05-31T14:30:01",
            "tools_used": ["search_files", "analyze_content", "generate_report"],
            "steps": ["扫描目录", "读取文件", "生成报告"],
            "success": True,
            "execution_time_ms": 2500,
            "output_type": "report",
            "requires_file": True
        },
        {
            "timestamp": "2026-05-31T14:35:10",
            "tools_used": ["search_files", "analyze_content", "generate_report"],
            "steps": ["扫描目录", "读取文件", "生成报告"],
            "success": True,
            "execution_time_ms": 1800,
            "output_type": "report",
            "requires_file": True
        },
        {
            "timestamp": "2026-05-31T14:40:22",
            "tools_used": ["search_files", "analyze_content", "generate_report"],
            "steps": ["扫描目录", "读取文件", "生成报告"],
            "success": True,
            "execution_time_ms": 2100,
            "output_type": "report",
            "requires_file": True
        },
        {
            "timestamp": "2026-05-31T15:00:05",
            "tools_used": ["web_search", "web_fetch", "summarize"],
            "steps": ["联网搜索", "抓取内容", "摘要总结"],
            "success": True,
            "execution_time_ms": 5000,
            "output_type": "summary",
            "requires_network": True
        },
        {
            "timestamp": "2026-05-31T15:10:33",
            "tools_used": ["shell_exec", "python_exec", "write_file"],
            "steps": ["执行命令", "脚本处理", "写入结果"],
            "success": False,
            "execution_time_ms": 800,
            "output_type": "file",
            "requires_file": True
        },
    ]

    # 创建输出目录
    output_dir = Path(__file__).parent.parent / "技能库" / "auto_extracted"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 运行萃取流水线
    pipeline = SkillAutoExtractionPipeline(
        skill_output_dir=str(output_dir)
    )

    result = pipeline.run(sample_logs)

    print("=" * 60)
    print("技能自动萃取引擎 v1.0 · 测试")
    print("=" * 60)
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))

    # 展示生成的文件
    if result["summary"]["written_files"]:
        print(f"\n生成技能文件:")
        for f in result["summary"]["written_files"]:
            print(f"  → {f}")
            content = Path(f).read_text()
            print(f"    内容预览: {content[:200]}...")

    print(f"\n✅ 技能自动萃取引擎 v1.0 测试通过")
    print(f"   发现模式: {result['summary']['total_patterns']}")
    print(f"   生成候选: {result['summary']['total_candidates']}")
    print(f"   审查通过: {result['summary']['accepted']}")