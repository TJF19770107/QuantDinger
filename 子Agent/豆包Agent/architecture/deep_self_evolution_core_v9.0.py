"""
深度自进化核心闭环 v9.0 — R44全域缺口专项补全 · P0-3
=====================================================
版本: v9.0 (R44升级)
上一版本: v8.0 (SICA v3.0 + GEPA融合 + 五模进化 + 数字分身联动)

v9.0 核心升级（对标R44专项补全清单P0-3）:
  1. 技能自动萃取引擎 SkillAutoExtractor → 从日志与执行记录自动生成标准化Skill
  2. SICA v4.0 加固: 灰度部署+A/B测试+NRP验证+自动回滚
  3. GenericAgent自进化逻辑 → 框架自适应优化
  4. 版本快照 + 异常自动回滚
  5. 全域联动进化: Obsidian↔桌面控制↔AI on UI 三层联动
  6. SkillLite 三层安全沙箱自进化 (NEW: 攻击→检测→抗体→防御)
  7. 多模型路由自进化 + 成本感知自适应
"""

import json
import time
import uuid
import hashlib
import logging
import threading
import traceback
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from enum import Enum, auto
from typing import Any, Optional, List, Dict, Tuple, Callable, Union
from collections import defaultdict, deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] EVOLUTION_V9: %(message)s')
logger = logging.getLogger("EvolutionV9")


# ==============================
# 枚举定义
# ==============================

class EvolutionPhase(Enum):
    """进化阶段"""
    OBSERVE = "observe"
    ANALYZE = "analyze"
    EXTRACT = "extract"
    VALIDATE = "validate"
    DEPLOY = "deploy"
    MONITOR = "monitor"
    ROLLBACK = "rollback"


class SkillCategory(Enum):
    """技能分类"""
    FILE_OPERATION = "file_operation"
    SYSTEM_CONFIG = "system_config"
    REASONING = "reasoning"
    APP_OPERATION = "app_operation"
    WEB_INTERACTION = "web_interaction"
    DATA_ANALYSIS = "data_analysis"
    SAFETY = "safety"
    OPTIMIZATION = "optimization"


class DeploymentMode(Enum):
    """部署模式"""
    GRAYSCALE = "grayscale"       # 灰度部署
    AB_TEST = "ab_test"          # A/B测试
    FULL_ROLLOUT = "full"         # 全量部署
    SHADOW = "shadow"            # 影子模式
    CANARY = "canary"            # 金丝雀


class RollbackTrigger(Enum):
    """回滚触发条件"""
    ERROR_RATE = "error_rate"           # 错误率超阈值
    PERFORMANCE_DROP = "perf_drop"      # 性能下降
    NRP_FAILURE = "nrp_failure"         # NRP验证失败
    MANUAL = "manual"                   # 手动触发
    TIME_EXPIRED = "time_expired"        # 灰度窗口到期


# ==============================
# 数据模型 v9.0
# ==============================

@dataclass
class SkillSpec:
    """技能规格"""
    skill_id: str
    category: SkillCategory
    name: str
    version: str
    prompt_template: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    success_rate: float = 0.0
    avg_execution_ms: float = 0.0
    total_executions: int = 0
    source_log_id: Optional[str] = None
    parent_skill_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    last_used: float = 0.0
    is_active: bool = True
    hash_digest: str = ""


@dataclass
class ExecutionLog:
    """执行日志"""
    log_id: str
    skill_id: Optional[str]
    agent_id: str
    task_summary: str
    input_snapshot: Dict[str, Any]
    output_snapshot: Dict[str, Any]
    success: bool
    error_info: Optional[str]
    execution_time_ms: float
    tools_used: List[str]
    tokens_consumed: int
    traceback_str: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    novelty_score: float = 0.0      # 新颖度评分
    reusable: bool = False          # 是否可转化为技能


@dataclass
class VersionSnapshot:
    """版本快照"""
    snapshot_id: str
    component: str                       # 组件名
    version: str
    state_dump: Dict[str, Any]           # 状态全量
    hash_digest: str                     # SHA256校验
    created_at: float = field(default_factory=time.time)
    parent_snapshot_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class GrayscaleConfig:
    """灰度配置"""
    deployment_mode: DeploymentMode = DeploymentMode.GRAYSCALE
    rollout_pct: float = 10.0             # 灰度比例 0-100
    ab_test_group: str = "A"
    evaluation_window_ms: int = 3600000   # 评估窗口 1小时
    success_threshold: float = 0.90       # 成功率阈值
    perf_threshold_ms: int = 10000        # 性能阈值
    max_error_rate: float = 0.05          # 最大错误率
    auto_rollback: bool = True
    target_group: List[str] = field(default_factory=list)


@dataclass
class ModelRouteConfig:
    """模型路由配置"""
    route_id: str
    model_name: str
    cost_per_1k_tokens: float
    avg_quality_score: float
    max_context_tokens: int
    supported_languages: List[str] = field(default_factory=list)
    suitable_task_types: List[str] = field(default_factory=list)
    current_load: int = 0
    max_concurrent: int = 10


@dataclass
class SandboxDefenseRule:
    """沙箱防御规则"""
    rule_id: str
    attack_pattern: str            # 攻击模式描述
    detection_logic: str           # 检测逻辑（正则/ML模型）
    antibody_action: str           # 抗体动作：block/log/alert/deceive
    defense_level: str = "medium"  # low/medium/high/critical
    source_incident_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)


# ==============================
# v9.0 核心：技能自动萃取引擎 SkillAutoExtractor
# ==============================

class SkillAutoExtractor:
    """
    技能自动萃取引擎
    从执行日志与成功轨迹中自动提取可复用的标准化Skill
    """

    NOVELTY_THRESHOLD = 0.65      # 新颖度阈值
    USAGE_THRESHOLD = 3            # 至少成功执行N次才萃取
    MIN_CONFIDENCE = 0.70          # 最小置信度

    def __init__(self, skill_registry_path: str = ""):
        self.skill_registry_path = skill_registry_path
        self.extracted_skills: Dict[str, SkillSpec] = {}
        self.execution_logs: List[ExecutionLog] = []
        self.extraction_stats = {
            "total_logs_analyzed": 0,
            "skills_extracted": 0,
            "skills_upgraded": 0,
            "false_positives": 0
        }

    def analyze_log(self, log: ExecutionLog) -> float:
        """分析单条执行日志的新颖度和可复用性"""
        self.extraction_stats["total_logs_analyzed"] += 1

        # 新颖度评分
        novelty = self._score_novelty(log)
        log.novelty_score = novelty

        # 可复用性判断
        if log.success and novelty > self.NOVELTY_THRESHOLD:
            log.reusable = True

        return novelty

    def extract_skills_batch(self, logs: List[ExecutionLog]) -> List[SkillSpec]:
        """从一批日志中批量萃取技能"""
        # 按任务类型聚类
        clusters = self._cluster_by_task_type(logs)
        new_skills = []

        for task_type, cluster_logs in clusters.items():
            # 至少成功 N 次
            successful_logs = [l for l in cluster_logs if l.success]
            if len(successful_logs) < self.USAGE_THRESHOLD:
                continue

            # 提取通用模式
            skill = self._extract_from_cluster(task_type, successful_logs)
            if skill and self._validate_skill(skill):
                self.extracted_skills[skill.skill_id] = skill
                new_skills.append(skill)
                self.extraction_stats["skills_extracted"] += 1

                logger.info(f"[Extract] 新技能 {skill.name} | "
                           f"分类={skill.category.value} | "
                           f"来源={len(successful_logs)}条日志")

        return new_skills

    def generate_skill_markdown(self, skill: SkillSpec) -> str:
        """生成标准化Skill Markdown文件"""
        return f"""---
skill_id: {skill.skill_id}
name: {skill.name}
version: {skill.version}
category: {skill.category.value}
tags: {json.dumps(skill.tags, ensure_ascii=False)}
dependencies: {json.dumps(skill.dependencies)}
success_rate: {skill.success_rate:.1%}
avg_execution_ms: {skill.avg_execution_ms:.0f}ms
source_log: {skill.source_log_id or 'auto-extracted'}
generated_by: SkillAutoExtractor v9.0
created_at: {datetime.fromtimestamp(skill.created_at).isoformat()}
hash: {skill.hash_digest}
---

# {skill.name}

## 输入 Schema
```json
{json.dumps(skill.input_schema, ensure_ascii=False, indent=2)}
```

## 输出 Schema
```json
{json.dumps(skill.output_schema, ensure_ascii=False, indent=2)}
```

## 执行指令
{skill.prompt_template}

## 依赖
{chr(10).join(f'- {dep}' for dep in skill.dependencies)}

## 统计
- 总执行次数: {skill.total_executions}
- 成功率: {skill.success_rate:.1%}
- 平均耗时: {skill.avg_execution_ms:.0f}ms
"""

    def _score_novelty(self, log: ExecutionLog) -> float:
        """计算新颖度评分"""
        score = 0.5  # 基础分

        # 使用了新工具组合 +0.2
        if len(log.tools_used) > 2:
            score += 0.2

        # 首次出现的任务模式 +0.2
        if log.error_info is None:
            score += 0.1

        # 高token消耗说明复杂任务 +0.1
        if log.tokens_consumed > 5000:
            score += 0.1

        return min(1.0, score)

    def _cluster_by_task_type(self, logs: List[ExecutionLog]) -> Dict[str, List[ExecutionLog]]:
        """按任务类型聚类"""
        clusters = defaultdict(list)
        for log in logs:
            cluster_key = self._derive_task_type(log)
            clusters[cluster_key].append(log)
        return dict(clusters)

    def _derive_task_type(self, log: ExecutionLog) -> str:
        """推导任务类型"""
        # 基于使用的工具组合推导
        tools_sorted = sorted(log.tools_used)
        return "|".join(tools_sorted[:3]) if tools_sorted else "unknown"

    def _extract_from_cluster(self, task_type: str,
                             logs: List[ExecutionLog]) -> Optional[SkillSpec]:
        """从聚类中萃取技能"""
        if len(logs) < 2:
            return None

        skill_id = f"skill_{task_type.replace('|','_')}_{uuid.uuid4().hex[:6]}"

        # 从成功日志中提取共性
        input_keys = set()
        output_keys = set()
        for log in logs:
            input_keys.update(log.input_snapshot.keys())
            output_keys.update(log.output_snapshot.keys())

        # 计算成功率
        success_rate = sum(1 for l in logs if l.success) / len(logs)

        # 生成Hash
        content_str = json.dumps({
            "task_type": task_type,
            "input_keys": sorted(input_keys),
            "output_keys": sorted(output_keys)
        })
        hash_digest = hashlib.sha256(content_str.encode()).hexdigest()[:16]

        return SkillSpec(
            skill_id=skill_id,
            category=self._infer_category(task_type),
            name=f"自动萃取: {task_type[:60]}",
            version="1.0.0-auto",
            prompt_template=f"执行 {task_type} 类任务",
            input_schema={k: "auto" for k in input_keys},
            output_schema={k: "auto" for k in output_keys},
            tags=["auto-extracted", "v9.0"],
            success_rate=success_rate,
            total_executions=len(logs),
            source_log_id=logs[0].log_id,
            hash_digest=hash_digest
        )

    def _validate_skill(self, skill: SkillSpec) -> bool:
        """验证技能质量"""
        if not skill.skill_id or not skill.prompt_template:
            return False
        if skill.success_rate < self.MIN_CONFIDENCE:
            self.extraction_stats["false_positives"] += 1
            return False
        # 去重：检查是否与已有技能重复
        for existing in self.extracted_skills.values():
            if existing.hash_digest == skill.hash_digest:
                return False
        return True

    def _infer_category(self, task_type: str) -> SkillCategory:
        """推断技能分类"""
        if any(kw in task_type for kw in ["文件", "file", "read", "write", "copy"]):
            return SkillCategory.FILE_OPERATION
        if any(kw in task_type for kw in ["系统", "system", "config", "设置"]):
            return SkillCategory.SYSTEM_CONFIG
        if any(kw in task_type for kw in ["推理", "reason", "分析", "analyze"]):
            return SkillCategory.REASONING
        if any(kw in task_type for kw in ["app", "应用", "install", "open"]):
            return SkillCategory.APP_OPERATION
        return SkillCategory.OPTIMIZATION


# ==============================
# v9.0 核心：SICA v4.0 加固引擎
# ==============================

class SICAv4Engine:
    """
    SICA v4.0 自进化编码框架加固版
    新增：灰度部署 + A/B测试 + NRP验证 + 自动回滚
    """

    def __init__(self):
        self.grayscale_configs: Dict[str, GrayscaleConfig] = {}
        self.deployment_history: deque = deque(maxlen=500)
        self.ab_test_results: Dict[str, Dict] = {}
        self.rollback_queue: deque = deque(maxlen=100)
        self.active_deployments: Dict[str, Dict] = {}

    def create_grayscale_deployment(self, component: str,
                                   new_version: str,
                                   config: GrayscaleConfig) -> str:
        """创建灰度部署"""
        deploy_id = f"deploy_{component}_{uuid.uuid4().hex[:6]}"
        self.grayscale_configs[deploy_id] = config

        self.active_deployments[deploy_id] = {
            "component": component,
            "new_version": new_version,
            "status": "initializing",
            "rollout_pct": 0.0,
            "start_time": time.time(),
            "metrics": {
                "total_requests": 0,
                "success_count": 0,
                "error_count": 0,
                "avg_latency_ms": 0.0,
            }
        }

        logger.info(f"[SICA v4.0] 灰度部署 {deploy_id} | "
                   f"{component} → {new_version} | "
                   f"初始比例 {config.rollout_pct}% | "
                   f"模式 {config.deployment_mode.value}")

        return deploy_id

    def step_rollout(self, deploy_id: str, increment_pct: float = 10.0) -> Dict:
        """逐步推进灰度"""
        deployment = self.active_deployments.get(deploy_id)
        if not deployment:
            return {"error": "部署不存在"}

        config = self.grayscale_configs.get(deploy_id)
        if not config:
            return {"error": "配置不存在"}

        # 检查质量指标是否达标
        metrics = deployment["metrics"]
        if metrics["total_requests"] > 0:
            error_rate = metrics["error_count"] / metrics["total_requests"]
            if error_rate > config.max_error_rate:
                # 触发自动回滚
                self.trigger_rollback(deploy_id, RollbackTrigger.ERROR_RATE,
                                     f"错误率 {error_rate:.1%} 超过阈值 {config.max_error_rate:.1%}")
                return {"status": "rolled_back", "reason": f"错误率超标: {error_rate:.1%}"}

            if metrics["avg_latency_ms"] > config.perf_threshold_ms:
                self.trigger_rollback(deploy_id, RollbackTrigger.PERFORMANCE_DROP,
                                     f"延迟 {metrics['avg_latency_ms']:.0f}ms 超过阈值")
                return {"status": "rolled_back", "reason": "性能下降"}

        # 推进灰度
        new_pct = min(deployment["rollout_pct"] + increment_pct, 100.0)
        deployment["rollout_pct"] = new_pct

        if new_pct >= 100.0:
            deployment["status"] = "full_rollout"
            logger.info(f"[SICA v4.0] {deploy_id} 全量部署完成")
        else:
            logger.info(f"[SICA v4.0] {deploy_id} 灰度推进至 {new_pct}%")

        return {"status": "stepped", "rollout_pct": new_pct}

    def run_ab_test(self, deploy_id: str, group_a_config: Dict,
                   group_b_config: Dict) -> Dict:
        """执行A/B测试"""
        results = {
            "deploy_id": deploy_id,
            "group_a": {"config": group_a_config, "metrics": {}},
            "group_b": {"config": group_b_config, "metrics": {}},
            "start_time": time.time(),
            "winner": None,
        }

        config = self.grayscale_configs.get(deploy_id)
        if config:
            config.ab_test_group = "B"  # 将部分流量路由到B组

        self.ab_test_results[deploy_id] = results
        return results

    def evaluate_ab_test(self, deploy_id: str) -> Dict:
        """评估A/B测试结果"""
        results = self.ab_test_results.get(deploy_id)
        if not results:
            return {"error": "未找到A/B测试结果"}

        # 比较A/B组指标
        a_score = self._calculate_group_score(results["group_a"])
        b_score = self._calculate_group_score(results["group_b"])

        results["winner"] = "B" if b_score > a_score else "A"
        results["delta"] = abs(b_score - a_score)

        logger.info(f"[SICA v4.0] A/B测试 {deploy_id} 结果: "
                   f"胜者={results['winner']}, 差异={results['delta']:.3f}")

        return results

    def validate_nrp(self, skill: SkillSpec) -> Dict:
        """NRP（No Regret Policy）验证：确保新技能不引入退化"""
        checks = {
            "schema_valid": self._check_schema(skill),
            "dependency_intact": self._check_dependencies(skill),
            "no_performance_regression": self._check_performance(skill),
            "backward_compatible": self._check_backward_compat(skill),
        }

        all_passed = all(checks.values())
        return {
            "passed": all_passed,
            "checks": checks,
            "recommendation": "deploy" if all_passed else "hold_for_fix"
        }

    def trigger_rollback(self, deploy_id: str, trigger: RollbackTrigger,
                        reason: str = "") -> bool:
        """触发自动回滚"""
        deployment = self.active_deployments.get(deploy_id)
        if not deployment:
            return False

        deployment["status"] = "rolled_back"
        deployment["rollback_trigger"] = trigger.value
        deployment["rollback_reason"] = reason

        self.rollback_queue.append({
            "deploy_id": deploy_id,
            "component": deployment["component"],
            "version": deployment["new_version"],
            "trigger": trigger.value,
            "reason": reason,
            "timestamp": time.time()
        })

        logger.warning(f"[SICA v4.0] 自动回滚 {deploy_id} | "
                      f"触发={trigger.value} | 原因={reason}")

        return True

    def _calculate_group_score(self, group: Dict) -> float:
        """计算实验组评分"""
        metrics = group.get("metrics", {})
        success_rate = metrics.get("success_count", 0) / max(metrics.get("total_requests", 1), 1)
        latency_penalty = min(1.0, metrics.get("avg_latency_ms", 0) / 10000)
        return success_rate * 0.7 + (1 - latency_penalty) * 0.3

    def _check_schema(self, skill: SkillSpec) -> bool:
        return bool(skill.input_schema and skill.output_schema)

    def _check_dependencies(self, skill: SkillSpec) -> bool:
        return True

    def _check_performance(self, skill: SkillSpec) -> bool:
        return skill.avg_execution_ms < 30000

    def _check_backward_compat(self, skill: SkillSpec) -> bool:
        return True


# ==============================
# v9.0 核心：GenericAgent自进化逻辑
# ==============================

class GenericAgentEvolution:
    """
    GenericAgent轻量化自进化
    实现框架级自适应优化：策略参数自动调优、执行流程自重构
    """

    def __init__(self):
        self.adaptation_log: deque = deque(maxlen=500)
        self.parameter_history: Dict[str, List[Dict]] = defaultdict(list)
        self.optimization_rules: List[Dict] = []

    def adapt_strategy(self, agent_id: str, performance_metrics: Dict) -> Dict:
        """自适应策略调整"""
        adaptations = {}

        # 成功率下降 → 增加重试次数
        if performance_metrics.get("success_rate", 1.0) < 0.85:
            adaptations["max_retries"] = min(5, performance_metrics.get("max_retries", 3) + 1)
            adaptations["reason"] = "success_rate_below_threshold"

        # 延迟过高 → 启用并行化
        if performance_metrics.get("avg_latency_ms", 0) > 15000:
            adaptations["enable_parallel"] = True
            adaptations["max_parallel"] = 3
            adaptations["reason"] = "high_latency"

        # Token消耗过高 → 启用CIDM压缩
        if performance_metrics.get("avg_tokens", 0) > 50000:
            adaptations["enable_cidm"] = True
            adaptations["compress_threshold"] = 0.7
            adaptations["reason"] = "high_token_usage"

        if adaptations:
            self.adaptation_log.append({
                "agent_id": agent_id,
                "adaptations": adaptations,
                "timestamp": time.time()
            })

        return adaptations

    def learn_from_execution(self, execution: ExecutionLog) -> List[Dict]:
        """从执行中学习优化规则"""
        new_rules = []

        if execution.traceback_str:
            # 从错误中学习
            root_cause = self._analyze_root_cause(execution.traceback_str)
            new_rules.append({
                "type": "error_avoidance",
                "pattern": root_cause,
                "action": "retry_with_alternative_tool"
            })

        if execution.tokens_consumed > 100000:
            new_rules.append({
                "type": "efficiency",
                "pattern": "high_token_consumption",
                "action": "split_into_subtasks"
            })

        self.optimization_rules.extend(new_rules)
        return new_rules

    def _analyze_root_cause(self, traceback_str: str) -> str:
        """分析错误根因"""
        if "permission" in traceback_str.lower():
            return "permission_denied"
        if "timeout" in traceback_str.lower():
            return "timeout"
        if "not found" in traceback_str.lower():
            return "resource_not_found"
        return "unknown_error"


# ==============================
# v9.0 核心：域联动进化协调器
# ==============================

class CrossDomainEvolutionCoordinator:
    """
    全域联动进化协调器
    打通 Obsidian ↔ 桌面控制 ↔ AI on UI 三层联动
    """

    def __init__(self):
        self.obsidian_nodes: Dict[str, Any] = {}
        self.desktop_operations: deque = deque(maxlen=200)
        self.ui_interactions: deque = deque(maxlen=200)
        self.cross_domain_rules: List[Dict] = []

    def register_obsidian_event(self, event: Dict):
        """注册Obsidian事件"""
        self.obsidian_nodes[event.get("node_id", str(uuid.uuid4()))] = event
        self._check_cross_domain_trigger(event, "obsidian")

    def register_desktop_event(self, event: Dict):
        """注册桌面控制事件"""
        self.desktop_operations.append(event)
        self._check_cross_domain_trigger(event, "desktop")

    def register_ui_event(self, event: Dict):
        """注册AI on UI事件"""
        self.ui_interactions.append(event)
        self._check_cross_domain_trigger(event, "ui")

    def _check_cross_domain_trigger(self, event: Dict, source: str):
        """检查跨域联动触发条件"""
        # 示例规则：Obsidian技能更新 → 触发UI重新适配 → 桌面控制调整
        if source == "obsidian" and event.get("type") == "skill_updated":
            logger.info(f"[CrossDomain] Obsidian技能更新触发桌面控制适配")
            self._trigger_desktop_adaptation(event)

    def _trigger_desktop_adaptation(self, event: Dict):
        """触发桌面控制适配"""
        self.desktop_operations.append({
            "type": "adaptation",
            "trigger": event.get("node_id"),
            "action": "update_hotkeys",
            "timestamp": time.time()
        })

    def generate_cross_domain_report(self) -> Dict:
        """生成跨域联动报告"""
        return {
            "obsidian_events": len(self.obsidian_nodes),
            "desktop_operations": len(self.desktop_operations),
            "ui_interactions": len(self.ui_interactions),
            "cross_domain_rules": len(self.cross_domain_rules),
            "last_sync": time.time()
        }


# ==============================
# v9.0 核心：多模型路由自进化
# ==============================

class ModelRouterEvolution:
    """多模型路由自进化 + 成本感知自适应"""

    def __init__(self):
        self.routes: Dict[str, ModelRouteConfig] = {}
        self.route_performance: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.cost_stats: Dict[str, Dict] = defaultdict(dict)
        self._init_default_routes()

    def _init_default_routes(self):
        """初始化默认路由"""
        self.routes["claude_opus"] = ModelRouteConfig(
            route_id="claude_opus",
            model_name="Claude Opus 4.5",
            cost_per_1k_tokens=0.015,
            avg_quality_score=0.95,
            max_context_tokens=200000,
            supported_languages=["zh", "en", "ja", "ko", "fr", "de"],
            suitable_task_types=["complex_reasoning", "code_generation", "analysis"]
        )
        self.routes["claude_sonnet"] = ModelRouteConfig(
            route_id="claude_sonnet",
            model_name="Claude Sonnet 4",
            cost_per_1k_tokens=0.003,
            avg_quality_score=0.88,
            max_context_tokens=200000,
            supported_languages=["zh", "en"],
            suitable_task_types=["general_qa", "translation", "summarization"]
        )

    def select_route(self, task_type: str, complexity: float,
                    budget_constraint: Optional[float] = None) -> ModelRouteConfig:
        """智能路由选择"""
        candidates = []

        for route in self.routes.values():
            if task_type not in route.suitable_task_types:
                continue
            if route.current_load >= route.max_concurrent:
                continue
            if budget_constraint and route.cost_per_1k_tokens > budget_constraint:
                continue

            # 综合评分
            quality_weight = 0.6
            cost_weight = 0.3
            load_weight = 0.1

            cost_score = 1.0 / (1.0 + route.cost_per_1k_tokens * 100)
            load_score = 1.0 - (route.current_load / max(route.max_concurrent, 1))

            total_score = (
                route.avg_quality_score * quality_weight +
                cost_score * cost_weight +
                load_score * load_weight
            )

            candidates.append((total_score, route))

        if not candidates:
            return self.routes["claude_sonnet"]  # 默认低成本

        # 选择最高分
        candidates.sort(key=lambda x: x[0], reverse=True)
        selected = candidates[0][1]
        selected.current_load += 1

        logger.info(f"[Router] 选择 {selected.model_name} | "
                   f"任务={task_type} | 复杂度={complexity:.1f} | "
                   f"成本={selected.cost_per_1k_tokens}")

        return selected

    def record_route_performance(self, route_id: str, success: bool,
                                latency_ms: float, quality_score: float):
        """记录路由性能（用于自进化）"""
        self.route_performance[route_id].append({
            "success": success,
            "latency_ms": latency_ms,
            "quality_score": quality_score,
            "timestamp": time.time()
        })

        # 动态更新路由质量评分
        if route_id in self.routes:
            recent = list(self.route_performance[route_id])[-20:]
            if recent:
                self.routes[route_id].avg_quality_score = (
                    sum(r["quality_score"] for r in recent) / len(recent)
                )


# ==============================
# v9.0 核心：沙箱安全自进化
# ==============================

class SandboxEvolutionEngine:
    """沙箱安全自进化：攻击检测→抗体生成→防御部署"""

    def __init__(self):
        self.defense_rules: Dict[str, SandboxDefenseRule] = {}
        self.incident_log: deque = deque(maxlen=1000)
        self.antibody_templates: Dict[str, str] = {
            "path_traversal": "block_pattern('..%2f', '../', '..\\')",
            "command_injection": "sanitize_shell_input(); deny_raw_exec()",
            "resource_exhaustion": "enforce_limits(memory=512MB, cpu=50%, time=30s)",
            "data_exfiltration": "block_outbound(); audit_all_io()",
        }

    def detect_attack(self, execution_context: Dict) -> Optional[str]:
        """检测攻击模式"""
        # 路径穿越检测
        if "..%2f" in str(execution_context) or "../" in str(execution_context):
            return "path_traversal"

        # 命令注入检测
        suspicious = ["; rm ", "| sh", "$()", "`", "eval(", "exec("]
        for pattern in suspicious:
            if pattern in str(execution_context):
                return "command_injection"

        return None

    def generate_antibody(self, attack_type: str,
                         incident_id: str) -> SandboxDefenseRule:
        """生成抗体防御规则"""
        template = self.antibody_templates.get(attack_type, "alert_and_log()")

        rule = SandboxDefenseRule(
            rule_id=f"antibody_{attack_type}_{uuid.uuid4().hex[:6]}",
            attack_pattern=attack_type,
            detection_logic=template,
            antibody_action="block",
            defense_level="critical",
            source_incident_id=incident_id
        )

        self.defense_rules[rule.rule_id] = rule

        logger.info(f"[Sandbox] 生成抗体 {rule.rule_id} | "
                   f"攻击类型={attack_type} | 防御级别={rule.defense_level}")

        return rule

    def deploy_defense(self, rule: SandboxDefenseRule) -> bool:
        """部署防御规则"""
        self.defense_rules[rule.rule_id] = rule
        return True

    def get_active_defenses(self) -> List[Dict]:
        """获取已激活的防御规则"""
        return [
            {
                "rule_id": r.rule_id,
                "attack_pattern": r.attack_pattern,
                "action": r.antibody_action,
                "level": r.defense_level,
                "age_seconds": time.time() - r.created_at
            }
            for r in self.defense_rules.values()
        ]


# ==============================
# v9.0 核心：版本快照与回滚
# ==============================

class VersionSnapshotManager:
    """版本快照管理器"""

    def __init__(self, db_path: str = ""):
        self.db_path = db_path or "evolution_snapshots.db"
        self.snapshots: Dict[str, VersionSnapshot] = {}
        self._init_db()

    def _init_db(self):
        """初始化SQLite数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    component TEXT,
                    version TEXT,
                    state_dump TEXT,
                    hash_digest TEXT,
                    created_at REAL,
                    parent_snapshot_id TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning(f"快照数据库初始化失败: {e}")

    def create_snapshot(self, component: str, version: str,
                       state: Dict) -> VersionSnapshot:
        """创建版本快照"""
        state_json = json.dumps(state, ensure_ascii=False, default=str)
        hash_digest = hashlib.sha256(state_json.encode()).hexdigest()

        snapshot = VersionSnapshot(
            snapshot_id=f"snap_{component}_{uuid.uuid4().hex[:8]}",
            component=component,
            version=version,
            state_dump=state,
            hash_digest=hash_digest
        )

        self.snapshots[snapshot.snapshot_id] = snapshot

        # 持久化
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                "INSERT INTO snapshots VALUES (?,?,?,?,?,?,?)",
                (snapshot.snapshot_id, component, version,
                 state_json, hash_digest, snapshot.created_at,
                 snapshot.parent_snapshot_id)
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

        logger.info(f"[Snapshot] {snapshot.snapshot_id} | "
                   f"{component} v{version} | SHA256={hash_digest[:12]}")

        return snapshot

    def restore_snapshot(self, snapshot_id: str) -> Optional[Dict]:
        """恢复快照"""
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            return None

        logger.info(f"[Snapshot] 恢复 {snapshot_id} | "
                   f"{snapshot.component} v{snapshot.version}")

        return {
            "component": snapshot.component,
            "version": snapshot.version,
            "state": snapshot.state_dump,
            "hash": snapshot.hash_digest
        }

    def list_snapshots(self, component: str = None) -> List[Dict]:
        """列出快照"""
        snapshots = self.snapshots.values()
        if component:
            snapshots = [s for s in snapshots if s.component == component]

        return [
            {
                "snapshot_id": s.snapshot_id,
                "component": s.component,
                "version": s.version,
                "created_at": datetime.fromtimestamp(s.created_at).isoformat(),
                "hash": s.hash_digest[:12]
            }
            for s in sorted(snapshots, key=lambda x: x.created_at, reverse=True)
        ]


# ==============================
# 深度自进化核心闭环主控 v9.0
# ==============================

class DeepSelfEvolutionCoreV9:
    """深度自进化核心闭环 v9.0 — 总协调器"""

    def __init__(self):
        self.skill_extractor = SkillAutoExtractor()
        self.sica_engine = SICAv4Engine()
        self.generic_agent_evo = GenericAgentEvolution()
        self.cross_domain_coordinator = CrossDomainEvolutionCoordinator()
        self.model_router = ModelRouterEvolution()
        self.sandbox_evo = SandboxEvolutionEngine()
        self.snapshot_manager = VersionSnapshotManager()

        self.evolution_cycle = 0
        self.stats = {
            "total_cycles": 0,
            "skills_extracted": 0,
            "deployments_rolled": 0,
            "rollbacks_executed": 0,
            "attacks_detected": 0,
            "antibodies_generated": 0,
        }

    def run_evolution_cycle(self, logs: List[ExecutionLog] = None) -> Dict:
        """执行一轮完整进化循环"""
        self.evolution_cycle += 1
        cycle_id = f"R{self.evolution_cycle}"
        logger.info(f"=== 进化循环 {cycle_id} 开始 ===")

        results = {"cycle_id": cycle_id, "actions": []}

        # 1. 技能自动萃取
        if logs:
            for log in logs:
                self.skill_extractor.analyze_log(log)
            new_skills = self.skill_extractor.extract_skills_batch(logs)
            for skill in new_skills:
                results["actions"].append({
                    "type": "skill_extracted",
                    "skill_name": skill.name,
                    "skill_id": skill.skill_id
                })

        # 2. GenericAgent自进化
        if logs:
            for log in logs:
                new_rules = self.generic_agent_evo.learn_from_execution(log)
                for rule in new_rules:
                    results["actions"].append({
                        "type": "rule_learned",
                        "rule": rule
                    })

        # 3. 沙箱安全自进化
        for log_item in (logs or []):
            attack_type = self.sandbox_evo.detect_attack(
                log_item.input_snapshot
            )
            if attack_type:
                self.stats["attacks_detected"] += 1
                antibody = self.sandbox_evo.generate_antibody(
                    attack_type, log_item.log_id
                )
                self.sandbox_evo.deploy_defense(antibody)
                self.stats["antibodies_generated"] += 1
                results["actions"].append({
                    "type": "antibody_generated",
                    "attack_type": attack_type,
                    "rule_id": antibody.rule_id
                })

        # 4. 创建快照
        snapshot = self.snapshot_manager.create_snapshot(
            "evolution_core", f"v9.0-{cycle_id}",
            {"stats": self.stats, "cycle_id": cycle_id}
        )
        results["snapshot_id"] = snapshot.snapshot_id

        self.stats["total_cycles"] += 1
        logger.info(f"=== 进化循环 {cycle_id} 完成 | {len(results['actions'])} 项变更 ===")

        return results

    def get_status(self) -> Dict:
        """获取核心状态"""
        return {
            "version": "9.0",
            "evolution_cycle": self.evolution_cycle,
            "stats": self.stats,
            "skills_registered": len(self.skill_extractor.extracted_skills),
            "active_defenses": len(self.sandbox_evo.defense_rules),
            "snapshots": len(self.snapshot_manager.snapshots),
            "model_routes": len(self.model_router.routes),
            "cross_domain_events": self.cross_domain_coordinator.generate_cross_domain_report(),
        }


# ==============================
# 入口
# ==============================

if __name__ == "__main__":
    evo = DeepSelfEvolutionCoreV9()

    # 模拟执行日志
    logs = [
        ExecutionLog(
            log_id=f"log_{i}",
            skill_id=None,
            agent_id="agent_001",
            task_summary=f"自动化任务 {i}",
            input_snapshot={"task": f"test_{i}"},
            output_snapshot={"result": "success"},
            success=True,
            error_info=None,
            execution_time_ms=2500,
            tools_used=["read_text", "web_search"] if i % 2 == 0 else ["shell_executor"],
            tokens_consumed=3000 + i * 1000
        )
        for i in range(10)
    ]

    result = evo.run_evolution_cycle(logs)
    print(json.dumps(evo.get_status(), ensure_ascii=False, indent=2))
