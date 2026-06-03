# visual_workflow_engine_v2.0.py

> 原始文件: `visual_workflow_engine_v2.0.py`  |  类型: `.py`  |  自动转换

```python
# -*- coding: utf-8 -*-
"""
可视化工作流引擎 v2.0 — R16深度增强版
增强：超时熔断降级 / 节点全维度监控 / 多Agent分发策略 / HTML暗色看板绑定
"""

import json
import time
import uuid
import logging
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Callable

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] WORKFLOW: %(message)s')
logger = logging.getLogger("WorkflowV2")


# ==================== 枚举定义 ====================

class NodeType(Enum):
    TRIGGER = "trigger"
    ACTION = "action"
    CONDITION = "condition"
    AGENT = "agent"
    MERGE = "merge"
    TERMINAL = "terminal"
    SUB_WORKFLOW = "sub_workflow"
    DYNAMIC = "dynamic"
    WAIT = "wait"
    NOTIFY = "notify"


class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    SUB_WORKFLOW = "sub_workflow"


class NodeStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    DEGRADED = "degraded"


class DispatchStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    CAPACITY_AWARE = "capacity_aware"
    AFFINITY = "affinity"
    BROADCAST = "broadcast"


# ==================== 数据模型 ====================

@dataclass
class WorkflowNode:
    node_id: str
    node_type: NodeType
    display_name: str
    config: dict = field(default_factory=dict)
    next_nodes: list[str] = field(default_factory=list)
    status: NodeStatus = NodeStatus.PENDING
    output: Any = None
    execution_time_ms: float = 0
    retry_count: int = 0
    logs: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    on_error: Optional[str] = None
    fallback_node: Optional[str] = None


@dataclass
class Workflow:
    workflow_id: str
    name: str
    description: str = ""
    nodes: dict = field(default_factory=dict)
    entry_node_id: str = ""
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    status: NodeStatus = NodeStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: list = field(default_factory=list)


@dataclass
class WorkflowExecution:
    execution_id: str
    workflow_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    node_statuses: dict = field(default_factory=dict)
    node_metrics: dict = field(default_factory=dict)
    logs: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    trace_chain: list = field(default_factory=list)


# ==================== 节点工厂 v2.0 ====================

class NodeFactoryV2:
    """增强节点工厂"""

    @staticmethod
    def create_trigger(trigger_type: str, config: dict) -> WorkflowNode:
        return WorkflowNode(
            node_id=f"trigger_{uuid.uuid4().hex[:8]}",
            node_type=NodeType.TRIGGER,
            display_name=f"Trigger: {trigger_type}",
            config={"trigger_type": trigger_type, **config}
        )

    @staticmethod
    def create_action(skill: str, method: str, params: dict,
                      timeout: int = 30000, retry: int = 3, fallback: str = None) -> WorkflowNode:
        return WorkflowNode(
            node_id=f"action_{uuid.uuid4().hex[:8]}",
            node_type=NodeType.ACTION,
            display_name=f"Action: {skill}.{method}",
            config={"skill": skill, "method": method, "params": params,
                    "timeout": timeout, "retry": retry},
            fallback_node=fallback
        )

    @staticmethod
    def create_condition(field: str, operator: str, value: Any,
                         true_branch: str, false_branch: str, compound: str = None) -> WorkflowNode:
        return WorkflowNode(
            node_id=f"cond_{uuid.uuid4().hex[:8]}",
            node_type=NodeType.CONDITION,
            display_name=f"Condition: {field} {operator} {value}",
            config={"field": field, "operator": operator, "value": value,
                    "true_branch": true_branch, "false_branch": false_branch,
                    "compound": compound}
        )

    @staticmethod
    def create_agent(agent_name: str, task: str, timeout: int = 120000,
                     strategy: DispatchStrategy = DispatchStrategy.CAPACITY_AWARE) -> WorkflowNode:
        return WorkflowNode(
            node_id=f"agent_{uuid.uuid4().hex[:8]}",
            node_type=NodeType.AGENT,
            display_name=f"Agent: {agent_name}",
            config={"agent_name": agent_name, "task": task, "timeout": timeout,
                    "dispatch_strategy": strategy.value}
        )

    @staticmethod
    def create_sub_workflow(workflow_id: str, name: str, timeout: int = 300000) -> WorkflowNode:
        return WorkflowNode(
            node_id=f"subwf_{uuid.uuid4().hex[:8]}",
            node_type=NodeType.SUB_WORKFLOW,
            display_name=f"SubWF: {name}",
            config={"workflow_id": workflow_id, "timeout": timeout}
        )


# ==================== 超时熔断与降级引擎 ====================

class CircuitBreaker:
    """超时熔断控制器"""

    YELLOW_TIMEOUT_MS = 30000
    RED_TIMEOUT_MS = 60000
    MAX_RETRIES = 3

    def __init__(self):
        self.breaker_state: dict = {}  # node_id -> {"tripped": bool, "failures": int, "last_trip": float}

    def execute_with_protection(self, node: WorkflowNode, executor: Callable) -> Any:
        """带熔断保护的节点执行"""
        start = time.time()
        retries = 0

        while retries <= self.MAX_RETRIES:
            try:
                result = executor()
                elapsed = (time.time() - start) * 1000

                # 黄色告警
                if elapsed > self.YELLOW_TIMEOUT_MS:
                    logger.warning(f"⏰ 黄色告警: {node.display_name} 耗时 {elapsed:.0f}ms > {self.YELLOW_TIMEOUT_MS}ms")
                    node.metrics["performance"] = "degraded"

                return result

            except Exception as e:
                elapsed = (time.time() - start) * 1000
                retries += 1

                if elapsed > self.RED_TIMEOUT_MS:
                    logger.error(f"🔴 熔断触发: {node.display_name} 超时 {elapsed:.0f}ms")
                    self._trip(node.node_id)
                    return self._degraded_result(node, e)

                if retries >= self.MAX_RETRIES:
                    logger.error(f"❌ 重试耗尽: {node.display_name} ({retries}次)")
                    return self._degraded_result(node, e)

                logger.info(f"重试 {node.display_name} ({retries}/{self.MAX_RETRIES})")
                time.sleep(1)

        return self._degraded_result(node, Exception("max_retries_exceeded"))

    def _trip(self, node_id: str):
        self.breaker_state[node_id] = {"tripped": True, "failures": 1, "last_trip": time.time()}

    def _degraded_result(self, node: WorkflowNode, error: Exception) -> dict:
        """降级结果"""
        node.status = NodeStatus.DEGRADED
        default_value = node.config.get("default_value")
        return {"status": "degraded", "error": str(error), "default": default_value,
                "fallback_used": node.fallback_node is not None}

    def is_tripped(self, node_id: str) -> bool:
        state = self.breaker_state.get(node_id, {})
        if state.get("tripped"):
            elapsed = time.time() - state.get("last_trip", 0)
            if elapsed > 300:  # 5分钟自动恢复
                self.breaker_state.pop(node_id, None)
                return False
            return True
        return False


# ==================== 节点全维度监控 ====================

class NodeMonitor:
    """节点级全维度监控"""

    def __init__(self):
        self.metrics_store: dict = {}  # node_id -> 历史指标列表

    def capture(self, node: WorkflowNode, start_time: float) -> dict:
        """捕获单次执行指标"""
        elapsed = (time.time() - start_time) * 1000
        output_size = len(json.dumps(node.output, ensure_ascii=False)) if node.output else 0

        metrics = {
            "execution_time_ms": elapsed,
            "retry_count": node.retry_count,
            "status": node.status.value,
            "output_size": output_size,
            "timestamp": datetime.now().isoformat(),
            "node_type": node.node_type.value,
        }

        if node.node_id not in self.metrics_store:
            self.metrics_store[node.node_id] = []

        self.metrics_store[node.node_id].append(metrics)
        node.metrics = metrics
        return metrics

    def get_baseline(self, node_id: str) -> dict:
        """获取性能基线"""
        history = self.metrics_store.get(node_id, [])
        if not history:
            return {}

        times = sorted([m["execution_time_ms"] for m in history])
        n = len(times)

        return {
            "p50": times[n // 2],
            "p95": times[int(n * 0.95)],
            "p99": times[int(n * 0.99)],
            "avg": sum(times) / n,
            "min": times[0],
            "max": times[-1],
            "total_executions": n,
            "error_rate": sum(1 for m in history if m["status"] == "failed") / n,
        }

    def detect_anomaly(self, node_id: str, current_time_ms: float) -> Optional[str]:
        """异常检测"""
        baseline = self.get_baseline(node_id)
        if not baseline or baseline["total_executions"] < 5:
            return None

        p95 = baseline["p95"]
        if current_time_ms > p95 * 3:
            return "CRITICAL_SLOWDOWN"
        if current_time_ms > p95 * 2:
            return "WARNING_SLOWDOWN"
        return None

    def get_summary(self) -> dict:
        """全量指标摘要"""
        total = sum(len(v) for v in self.metrics_store.values())
        failures = sum(1 for v in self.metrics_store.values()
                      for m in v if m.get("status") in ("failed", "timeout"))

        return {
            "total_executions": total,
            "failure_rate": failures / max(total, 1),
            "monitored_nodes": len(self.metrics_store),
            "anomalies_active": 0,
        }


# ==================== 多Agent分发调度器 ====================

class MultiAgentDispatcher:
    """多Agent智能分发调度器"""

    def __init__(self, dispatch_fn=None):
        self.dispatch_fn = dispatch_fn
        self.agent_load: dict = {}       # agent_name -> {"queue_depth": int, "last_active": float}
        self.affinity_map: dict = {}     # task_type -> agent_name
        self.dispatch_stats: dict = {}   # strategy -> {"sent": int, "success": int}

    def dispatch(self, agent_name: str, task: str, strategy: DispatchStrategy) -> dict:
        """按策略派发"""
        if strategy == DispatchStrategy.CAPACITY_AWARE:
            return self._capacity_aware_dispatch(agent_name, task)
        elif strategy == DispatchStrategy.ROUND_ROBIN:
            return self._round_robin_dispatch(agent_name, task)
        elif strategy == DispatchStrategy.AFFINITY:
            return self._affinity_dispatch(task)
        elif strategy == DispatchStrategy.BROADCAST:
            return self._broadcast_dispatch(task)
        else:
            return self._simple_dispatch(agent_name, task)

    def health_check(self, agent_name: str) -> dict:
        """Agent健康检查"""
        load_info = self.agent_load.get(agent_name, {})
        last_active = load_info.get("last_active", 0)
        is_healthy = (time.time() - last_active) < 30  # 30秒内心跳

        return {
            "agent": agent_name,
            "healthy": is_healthy,
            "queue_depth": load_info.get("queue_depth", 0),
            "last_active_ago": time.time() - last_active if last_active else float("inf"),
        }

    def select_best_agent(self, task_type: str, candidates: list[str]) -> str:
        """选择最优Agent"""
        best = None
        best_score = -1

        for agent in candidates:
            health = self.health_check(agent)
            affinity_bonus = 10 if self.affinity_map.get(task_type) == agent else 0
            health_score = 20 if health["healthy"] else 0
            load_penalty = health["queue_depth"] * (-3)

            score = health_score + affinity_bonus + load_penalty
            if score > best_score:
                best_score = score
                best = agent

        return best or (candidates[0] if candidates else "")

    # --- 内部方法 ---

    def _simple_dispatch(self, agent_name: str, task: str) -> dict:
        if self.dispatch_fn:
            return self.dispatch_fn(agent_name=agent_name, task=task)
        return {"agent": agent_name, "status": "dispatched"}

    def _capacity_aware_dispatch(self, agent_name: str, task: str) -> dict:
        health = self.health_check(agent_name)
        if not health["healthy"]:
            logger.warning(f"Agent {agent_name} 不健康，降级为直接派发")
        return self._simple_dispatch(agent_name, task)

    def _round_robin_dispatch(self, agent_name: str, task: str) -> dict:
        return self._simple_dispatch(agent_name, task)

    def _affinity_dispatch(self, task: str) -> dict:
        best = self.select_best_agent("default", list(self.agent_load.keys()))
        return self._simple_dispatch(best, task)

    def _broadcast_dispatch(self, task: str) -> dict:
        results = {}
        for agent_name in self.agent_load:
            results[agent_name] = self._simple_dispatch(agent_name, task)
        return {"broadcast": results, "agent_count": len(results)}


# ==================== 增强版执行引擎 ====================

class WorkflowExecutorV2:
    """工作流执行引擎 v2.0 — 超时熔断+监控+分发增强"""

    MAX_PARALLEL = 5
    LOOP_MAX_ITERATIONS = 10

    def __init__(self, tool_registry: dict = None, dispatch_fn=None):
        self.tool_registry = tool_registry or {}
        self.dispatcher = MultiAgentDispatcher(dispatch_fn=dispatch_fn)
        self.circuit_breaker = CircuitBreaker()
        self.monitor = NodeMonitor()

    def execute(self, workflow: Workflow) -> WorkflowExecution:
        execution = WorkflowExecution(
            execution_id=f"exec_{uuid.uuid4().hex[:8]}",
            workflow_id=workflow.workflow_id,
            start_time=time.time()
        )
        workflow.status = NodeStatus.RUNNING
        logger.info(f"🚀 工作流启动: {workflow.name} [{workflow.workflow_id}]")

        try:
            mode = workflow.execution_mode

            if mode == ExecutionMode.SEQUENTIAL:
                self._execute_sequential_v2(workflow, execution)
            elif mode == ExecutionMode.PARALLEL:
                self._execute_parallel_v2(workflow, execution)
            elif mode == ExecutionMode.CONDITIONAL:
                self._execute_conditional_v2(workflow, execution)
            elif mode == ExecutionMode.LOOP:
                self._execute_loop_v2(workflow, execution)
            else:
                self._execute_sequential_v2(workflow, execution)

            workflow.status = NodeStatus.SUCCESS
        except Exception as e:
            workflow.status = NodeStatus.FAILED
            execution.logs.append({"level": "FATAL", "msg": str(e)})

        execution.end_time = time.time()
        execution.metrics["total_time_ms"] = (execution.end_time - execution.start_time) * 1000
        execution.metrics["monitor_summary"] = self.monitor.get_summary()

        return execution

    def _execute_node_v2(self, node: WorkflowNode, execution: WorkflowExecution) -> bool:
        """执行单个节点 — 熔断+监控"""
        start = time.time()
        node.status = NodeStatus.RUNNING

        # 熔断检查
        if self.circuit_breaker.is_tripped(node.node_id):
            node.status = NodeStatus.SKIPPED
            logger.warning(f"节点已熔断跳过: {node.display_name}")
            return False

        def _execute():
            if node.node_type == NodeType.ACTION:
                node.output = self._execute_action(node)
            elif node.node_type == NodeType.AGENT:
                node.output = self._execute_agent_enhanced(node)
            elif node.node_type == NodeType.MERGE:
                node.output = {"merged": True}
            elif node.node_type == NodeType.TERMINAL:
                node.output = {"terminal": node.config.get("terminal_type", "success")}
            return node.output

        result = self.circuit_breaker.execute_with_protection(node, _execute)

        if node.status in (NodeStatus.DEGRADED, NodeStatus.FAILED):
            execution.node_statuses[node.node_id] = node.status
            execution.trace_chain.append({"node": node.node_id, "status": node.status.value, "time_ms": (time.time() - start) * 1000})
            return False

        node.status = NodeStatus.SUCCESS
        node.execution_time_ms = (time.time() - start) * 1000
        execution.node_statuses[node.node_id] = NodeStatus.SUCCESS
        execution.trace_chain.append({"node": node.node_id, "status": "success", "time_ms": node.execution_time_ms})

        # 指标采集
        self.monitor.capture(node, start)

        # 异常检测
        anomaly = self.monitor.detect_anomaly(node.node_id, node.execution_time_ms)
        if anomaly:
            logger.warning(f"异常检测 [{node.node_id}]: {anomaly}")

        return True

    def _execute_sequential_v2(self, workflow: Workflow, execution: WorkflowExecution):
        current_id = workflow.entry_node_id
        visited = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            node = workflow.nodes.get(current_id)
            if not node:
                break

            success = self._execute_node_v2(node, execution)
            if not success and node.fallback_node:
                current_id = node.fallback_node
                continue
            elif not success:
                current_id = node.on_error
            else:
                current_id = node.next_nodes[0] if node.next_nodes else None

        execution.logs.append({"level": "INFO", "msg": f"串行执行完成: {len(visited)}个节点"})

    def _execute_parallel_v2(self, workflow: Workflow, execution: WorkflowExecution):
        """并行执行（增强版）"""
        independent = [n for n in workflow.nodes.values() if n.node_type != NodeType.TRIGGER]

        batch_size = self.MAX_PARALLEL
        for i in range(0, len(independent), batch_size):
            batch = independent[i:i + batch_size]
            for node in batch:
                self._execute_node_v2(node, execution)

    def _execute_conditional_v2(self, workflow: Workflow, execution: WorkflowExecution):
        current_id = workflow.entry_node_id
        while current_id:
            node = workflow.nodes.get(current_id)
            if not node:
                break

            if node.node_type == NodeType.CONDITION:
                condition_result = self._evaluate_condition_enhanced(node)
                current_id = condition_result
            else:
                self._execute_node_v2(node, execution)
                current_id = node.next_nodes[0] if node.next_nodes else None

    def _execute_loop_v2(self, workflow: Workflow, execution: WorkflowExecution):
        """循环迭代执行"""
        max_iter = workflow.nodes.get("loop_config", {}).get("max_iterations", self.LOOP_MAX_ITERATIONS)

        for i in range(max_iter):
            logger.info(f"循环迭代 {i+1}/{max_iter}")
            current_id = workflow.entry_node_id
            while current_id:
                node = workflow.nodes.get(current_id)
                if not node:
                    break
                self._execute_node_v2(node, execution)
                current_id = node.next_nodes[0] if node.next_nodes else None

            # 收敛检查
            if i >= 2:
                recent = execution.trace_chain[-3:]
                if all(t.get("status") == "success" for t in recent):
                    logger.info(f"循环收敛于第 {i+1} 轮")
                    break

    def _execute_agent_enhanced(self, node: WorkflowNode) -> dict:
        """增强Agent执行：策略派发+健康检查"""
        agent_name = node.config.get("agent_name", "")
        task = node.config.get("task", "")
        strategy = DispatchStrategy(node.config.get("dispatch_strategy", "capacity_aware"))

        # 健康检查
        health = self.dispatcher.health_check(agent_name)
        logger.info(f"Agent健康: {agent_name} → {health['healthy']}")

        return self.dispatcher.dispatch(agent_name, task, strategy)

    def _execute_action(self, node: WorkflowNode) -> dict:
        skill = node.config.get("skill", "")
        method = node.config.get("method", "")
        return {"skill": skill, "method": method, "status": "completed"}

    def _evaluate_condition_enhanced(self, node: WorkflowNode) -> str:
        """增强条件评估 — 支持复合条件"""
        compound = node.config.get("compound")
        if compound:
            rules = node.config.get("rules", [])
            results = [self._eval_single_rule(r, node) for r in rules]

            if compound == "AND":
                passed = all(results)
            elif compound == "OR":
                passed = any(results)
            else:
                passed = results[0] if results else False
        else:
            passed = self._eval_single_rule(node.config, node)

        return node.config["true_branch"] if passed else node.config["false_branch"]

    def _eval_single_rule(self, rule: dict, node: WorkflowNode) -> bool:
        field = rule.get("field", "")
        operator = rule.get("operator", "EQUALS")
        value = rule.get("value")
        actual = self._resolve_field(field)
        try:
            if operator == "GREATER_THAN": return float(actual) > float(value)
            if operator == "EQUALS": return str(actual) == str(value)
            if operator == "CONTAINS": return str(value) in str(actual)
        except Exception:
            return False
        return False

    def _resolve_field(self, field: str) -> Any:
        return 0


# ==================== 工作流管理器 v2.0 ====================

class WorkflowManagerV2:
    """工作流管理器 v2.0"""

    def __init__(self, tool_registry: dict = None, dispatch_fn=None):
        self.workflows: dict = {}
        self.executions: list = []
        self.executor = WorkflowExecutorV2(tool_registry=tool_registry, dispatch_fn=dispatch_fn)
        self.monitor = NodeMonitor()

    def register(self, workflow: Workflow) -> str:
        self.workflows[workflow.workflow_id] = workflow
        return workflow.workflow_id

    def run(self, workflow_id: str) -> WorkflowExecution:
        wf = self.workflows.get(workflow_id)
        if not wf:
            raise ValueError(f"工作流不存在: {workflow_id}")

        execution = self.executor.execute(wf)
        self.executions.append(execution)
        return execution

    def get_status(self, workflow_id: str) -> dict:
        wf = self.workflows.get(workflow_id)
        if not wf:
            return {"error": "not_found"}

        nodes = {}
        for nid, node in wf.nodes.items():
            nodes[nid] = {
                "name": node.display_name,
                "status": node.status.value,
                "time_ms": node.execution_time_ms,
                "retries": node.retry_count,
                "metrics": node.metrics,
            }

        return {"workflow_id": workflow_id, "name": wf.name,
                "status": wf.status.value, "total_nodes": len(wf.nodes), "nodes": nodes}

    def get_dashboard_data(self, execution_id: str) -> dict:
        """获取看板数据"""
        for ex in self.executions:
            if ex.execution_id == execution_id:
                return {
                    "execution_id": ex.execution_id,
                    "start_time": ex.start_time,
                    "end_time": ex.end_time,
                    "metrics": ex.metrics,
                    "trace_chain": ex.trace_chain,
                    "node_statuses": {k: v.value for k, v in ex.node_statuses.items()},
                }
        return {}

    def get_node_baselines(self) -> dict:
        """获取所有节点性能基线"""
        result = {}
        for node_id in self.monitor.metrics_store:
            result[node_id] = self.monitor.get_baseline(node_id)
        return result


# ==================== 预定义工作流模板 v2.0 ====================

def create_claude_reasoning_v2() -> Workflow:
    wf = Workflow(workflow_id="wf_claude_v2", name="Claude推理v2.0",
                  description="五层推理+三级缓存+回溯", execution_mode=ExecutionMode.SEQUENTIAL)

    nodes = [
        NodeFactoryV2.create_action("ReasoningV2", "phase1_parse", {"input": "{{context.input}}"}, timeout=60000),
        NodeFactoryV2.create_action("ReasoningV2", "phase2_decompose", {}, timeout=30000),
        NodeFactoryV2.create_action("ReasoningV2", "phase3_reason", {}, timeout=60000),
        NodeFactoryV2.create_action("ReasoningV2", "phase4_execute", {}, timeout=120000, retry=2),
        NodeFactoryV2.create_action("ReasoningV2", "phase5_review", {}, timeout=30000),
    ]

    for i, n in enumerate(nodes):
        n.next_nodes = [nodes[i + 1].node_id] if i + 1 < len(nodes) else []
        wf.nodes[n.node_id] = n

    wf.entry_node_id = nodes[0].node_id
    return wf


def create_self_evolution_v2() -> Workflow:
    wf = Workflow(workflow_id="wf_evolution_v2", name="自进化v3.0循环",
                  description="SICA进化→快照→检测→沉淀→同步", execution_mode=ExecutionMode.SEQUENTIAL)

    n1 = NodeFactoryV2.create_action("Evolution", "pre_snapshot", {})
    n2 = NodeFactoryV2.create_action("Evolution", "sica_evolve", {}, timeout=300000, retry=1,
                                     fallback="rollback_from_snapshot")
    n3 = NodeFactoryV2.create_condition("{{n2.output.score}}", "GREATER_THAN", 0.7,
                                        true_branch="skill_forge", false_branch="rollback")
    n4 = NodeFactoryV2.create_action("SkillForge", "extract_and_register", {})
    n5 = NodeFactoryV2.create_action("Obsidian", "sync_to_vault", {})

    n1.next_nodes = [n2.node_id]
    n2.next_nodes = [n3.node_id]
    n3.next_nodes = []  # conditional branching

    for n in [n1, n2, n3, n4, n5]:
        wf.nodes[n.node_id] = n

    wf.nodes["rollback"] = NodeFactoryV2.create_action("Snapshot", "rollback", {})
    wf.nodes["skill_forge"] = n4
    wf.nodes["obsidian_sync"] = n5

    n4.next_nodes = [n5.node_id]
    wf.nodes["rollback"].next_nodes = []

    wf.entry_node_id = n1.node_id
    return wf


if __name__ == "__main__":
    manager = WorkflowManagerV2()
    wf = create_claude_reasoning_v2()
    manager.register(wf)
    execution = manager.run(wf.workflow_id)

    print(f"\n执行ID: {execution.execution_id}")
    print(f"总耗时: {execution.metrics.get('total_time_ms', 0):.0f}ms")
    print(f"追踪链: {json.dumps(execution.trace_chain, indent=2, ensure_ascii=False)}")
```
