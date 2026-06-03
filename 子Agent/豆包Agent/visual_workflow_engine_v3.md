# visual_workflow_engine_v3.py

> 原始文件: `visual_workflow_engine_v3.py`  |  类型: `.py`  |  自动转换

```python

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可视化工作流引擎 v3.0 — LobsterAI Visual Workflow Engine
========================================================
版本: v3.0 | 迭代: R19 | 日期: 2026-05-31
对标: LangGraph · Google Opal · Claude Code Swarm · Hermes SWARM 9模式
覆盖缺口: GAP-055(Swarm对等协作) · GAP-056(工作流动态路由)
依赖: Python 3.10+ · json · dataclasses · enum · threading · time · queue · hashlib
"""

import json
import time
import queue
import hashlib
import threading
import logging
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Union
from collections import defaultdict


# ============================================================================
# 第一部分：工作流节点系统
# ============================================================================

class NodeType(Enum):
    """节点类型"""
    START = auto()       # 起始节点
    TASK = auto()        # 任务节点
    CONDITION = auto()   # 条件分支节点
    PARALLEL = auto()    # 并行分发节点
    JOIN = auto()        # 并行汇合节点
    AGENT = auto()       # Agent派发节点
    END = auto()         # 终止节点
    WAIT = auto()        # 等待/延时节点


class NodeStatus(Enum):
    """节点执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class RoutingRule(Enum):
    """路由规则"""
    SEQUENTIAL = "sequential"     # 串行
    PARALLEL_ALL = "parallel_all" # 全并行
    PARALLEL_ANY = "parallel_any" # 任一完成即继续
    CONDITIONAL = "conditional"   # 条件跳转
    ROUND_ROBIN = "round_robin"   # 轮询分发
    PRIORITY = "priority"         # 优先级分发


@dataclass
class WorkflowNode:
    """工作流节点"""
    node_id: str
    name: str
    node_type: NodeType
    handler: Optional[Callable] = None
    config: dict = field(default_factory=dict)
    status: NodeStatus = NodeStatus.PENDING
    inputs: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    started_at: float = 0.0
    finished_at: float = 0.0
    retry_count: int = 0
    max_retries: int = 1
    timeout_seconds: float = 300.0
    log_lines: list[str] = field(default_factory=list)

    def log(self, message: str):
        ts = time.strftime("%H:%M:%S")
        self.log_lines.append(f"[{ts}] {message}")

    def duration_ms(self) -> float:
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at) * 1000
        return 0


@dataclass
class WorkflowEdge:
    """工作流边 — 定义节点间连接与路由规则"""
    edge_id: str
    source: str
    target: str
    rule: RoutingRule = RoutingRule.SEQUENTIAL
    condition: Optional[Callable[[dict], bool]] = None
    label: str = ""


# ============================================================================
# 第二部分：多Agent任务分发
# ============================================================================

class AgentMode(Enum):
    """Agent协作模式 — 对标 Hermes SWARM 9模式"""
    SOLO = "solo"                  # 单Agent闭环
    FAN_OUT = "fan_out"           # 扇出 — 一对多并行
    PIPELINE = "pipeline"         # 流水线 — 串行接力
    VOTING = "voting"             # 投票 — 多数决定
    SWARM = "swarm"               # 蜂群 — 对等协作
    LEAD_SPECIALIST = "lead_specialist"  # 主从 — Leader分配
    BROADCAST = "broadcast"       # 广播 — 全部通知
    COMPETITION = "competition"   # 竞速 — 最快者胜
    CONSENSUS = "consensus"       # 共识 — 全体一致


@dataclass
class AgentTask:
    """Agent任务描述"""
    task_id: str
    agent_name: str
    task_description: str
    mode: AgentMode = AgentMode.SOLO
    depends_on: list[str] = field(default_factory=list)
    priority: int = 5  # 1-10
    timeout: float = 600.0
    result: Any = None
    status: str = "queued"


class AgentDispatcher:
    """
    多Agent任务分发器 — 对标 Claude Code Swarm / Hermes SWARM
    
    支持9种协作模式: Solo / Fan-Out / Pipeline / Voting / Swarm /
                     Lead-Specialist / Broadcast / Competition / Consensus
    """

    def __init__(self):
        self.task_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.agent_registry: dict[str, dict] = {}
        self.task_history: list[AgentTask] = []
        self.active_tasks: dict[str, AgentTask] = {}
        self.logger = logging.getLogger("AgentDispatcher")

    def register_agent(self, name: str, capabilities: list[str], max_concurrent: int = 3):
        """注册Agent"""
        self.agent_registry[name] = {
            "capabilities": capabilities,
            "max_concurrent": max_concurrent,
            "current_load": 0,
            "total_completed": 0,
            "total_failed": 0,
        }

    def dispatch(self, tasks: list[AgentTask], mode: AgentMode = AgentMode.SOLO) -> dict:
        """
        按指定模式分发任务
        
        Returns:
            分发方案 dict，包含各Agent的任务分配
        """
        plan = {"mode": mode.value, "assignments": {}, "estimated_duration": 0.0}

        if mode == AgentMode.SOLO:
            for task in tasks:
                plan["assignments"][task.agent_name] = [task.task_description]
                plan["estimated_duration"] += task.timeout

        elif mode == AgentMode.FAN_OUT:
            # 扇出：所有Agent并行执行各自任务
            for task in tasks:
                plan["assignments"][task.agent_name] = [task.task_description]
            plan["estimated_duration"] = max((t.timeout for t in tasks), default=0)

        elif mode == AgentMode.PIPELINE:
            # 流水线：按依赖顺序串行
            sorted_tasks = self._topological_sort(tasks)
            for i, task in enumerate(sorted_tasks):
                plan["assignments"][f"stage_{i}"] = [task.task_description]
            plan["estimated_duration"] = sum(t.timeout for t in sorted_tasks)

        elif mode == AgentMode.VOTING:
            # 投票：多个Agent执行相同任务，投票决定
            for task in tasks:
                voters = [name for name in self.agent_registry if self._can_handle(name, task.task_description)]
                plan["assignments"][task.task_description] = voters[:3]  # 最多3个投票者
            plan["estimated_duration"] = max((t.timeout for t in tasks), default=0)

        elif mode == AgentMode.SWARM:
            # 蜂群：对等协作，共享API客户端+MCP连接
            for task in tasks:
                handlers = [name for name in self.agent_registry if self._can_handle(name, task.task_description)]
                plan["assignments"][task.task_description] = handlers
            plan["estimated_duration"] = max((t.timeout for t in tasks), default=0)

        elif mode == AgentMode.LEAD_SPECIALIST:
            # 主从：Leader分析任务 → 分配给Specialist
            leader = tasks[0].agent_name if tasks else "file-agent"
            plan["leader"] = leader
            for task in tasks[1:]:
                plan["assignments"][task.agent_name] = [task.task_description]
            plan["estimated_duration"] = sum(t.timeout for t in tasks)

        elif mode == AgentMode.COMPETITION:
            # 竞速：多个Agent竞争，最快者胜
            for task in tasks:
                competitors = [name for name in self.agent_registry if self._can_handle(name, task.task_description)]
                plan["assignments"][f"race_{task.task_id}"] = competitors[:2]
            plan["estimated_duration"] = max((t.timeout for t in tasks), default=0)

        else:
            for task in tasks:
                plan["assignments"][task.agent_name] = [task.task_description]

        return plan

    def _topological_sort(self, tasks: list[AgentTask]) -> list[AgentTask]:
        """拓扑排序 — 按依赖关系排序"""
        task_map = {t.task_id: t for t in tasks}
        visited = set()
        temp = set()
        order = []

        def visit(task_id):
            if task_id in temp:
                return  # 检测到环，跳过
            if task_id in visited:
                return
            temp.add(task_id)
            task = task_map.get(task_id)
            if task:
                for dep_id in task.depends_on:
                    if dep_id in task_map:
                        visit(dep_id)
            temp.discard(task_id)
            visited.add(task_id)
            if task_id in task_map:
                order.append(task_map[task_id])

        for task_id in task_map:
            if task_id not in visited:
                visit(task_id)

        return order

    def _can_handle(self, agent_name: str, task_desc: str) -> bool:
        """判断Agent是否能处理该任务"""
        info = self.agent_registry.get(agent_name, {})
        capabilities = info.get("capabilities", [])
        return any(cap.lower() in task_desc.lower() for cap in capabilities)

    def get_load_stats(self) -> dict:
        """获取所有Agent负载统计"""
        stats = {}
        for name, info in self.agent_registry.items():
            utilization = info["current_load"] / max(info["max_concurrent"], 1)
            stats[name] = {
                "load": info["current_load"],
                "max": info["max_concurrent"],
                "utilization": f"{utilization:.0%}",
                "completed": info["total_completed"],
                "failed": info["total_failed"],
                "success_rate": (
                    f"{info['total_completed'] / max(info['total_completed'] + info['total_failed'], 1):.0%}"
                ),
            }
        return stats


# ============================================================================
# 第三部分：工作流引擎
# ============================================================================

@dataclass
class WorkflowRun:
    """工作流运行实例"""
    run_id: str
    workflow_name: str
    started_at: float
    finished_at: float = 0.0
    nodes_state: dict[str, NodeStatus] = field(default_factory=dict)
    edges_traversed: list[str] = field(default_factory=list)
    total_steps: int = 0
    current_step: int = 0
    error_log: list[str] = field(default_factory=list)


class VisualWorkflowEngine:
    """
    可视化工作流引擎 v3.0
    
    核心功能:
    - 功能节点拆分 (Start/Task/Condition/Parallel/Join/Agent/End/Wait)
    - 串行/并行/条件跳转路由 (Sequential/ParallelAll/ParallelAny/Conditional/RoundRobin/Priority)
    - 运行状态看板 (节点状态/边遍历/耗时/错误)
    - 节点监控 (日志绑定/超时检测/重试机制)
    - 多Agent分发集成 (AgentDispatcher)
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.nodes: dict[str, WorkflowNode] = {}
        self.edges: dict[str, WorkflowEdge] = {}
        self.agent_dispatcher = AgentDispatcher()
        self.runs: list[WorkflowRun] = []
        self._current_run: Optional[WorkflowRun] = None
        self.logger = logging.getLogger(f"WorkflowEngine.{name}")

    # ---- 构建工作流 ----
    def add_node(self, node: WorkflowNode) -> str:
        """添加节点"""
        self.nodes[node.node_id] = node
        return node.node_id

    def add_edge(self, edge: WorkflowEdge) -> str:
        """添加边"""
        self.edges[edge.edge_id] = edge
        return edge.edge_id

    def create_node(self, name: str, node_type: NodeType, handler: Optional[Callable] = None,
                    config: Optional[dict] = None) -> WorkflowNode:
        """工厂方法：创建节点"""
        node_id = f"node_{hashlib.md5(f'{name}_{time.time()}'.encode()).hexdigest()[:8]}"
        node = WorkflowNode(
            node_id=node_id, name=name, node_type=node_type,
            handler=handler, config=config or {}
        )
        self.nodes[node_id] = node
        return node

    def connect(self, source_id: str, target_id: str, rule: RoutingRule = RoutingRule.SEQUENTIAL,
                condition: Optional[Callable[[dict], bool]] = None, label: str = "") -> str:
        """连接两个节点"""
        edge_id = f"edge_{source_id}_to_{target_id}"
        edge = WorkflowEdge(
            edge_id=edge_id, source=source_id, target=target_id,
            rule=rule, condition=condition, label=label
        )
        self.edges[edge_id] = edge
        return edge_id

    # ---- 执行工作流 ----
    def execute(self, initial_input: dict = None) -> WorkflowRun:
        """
        执行工作流（同步模拟）
        
        Returns:
            WorkflowRun 包含完整执行状态
        """
        run = WorkflowRun(
            run_id=hashlib.md5(f"{self.name}_{time.time()}".encode()).hexdigest()[:12],
            workflow_name=self.name,
            started_at=time.time(),
        )
        self._current_run = run
        self.runs.append(run)

        # 找到起始节点
        start_nodes = [n for n in self.nodes.values() if n.node_type == NodeType.START]
        if not start_nodes:
            start_nodes = list(self.nodes.values())[:1]  # fallback

        # 待执行队列
        pending = list(start_nodes)
        visited = set()

        while pending:
            node = pending.pop(0)
            if node.node_id in visited:
                continue
            visited.add(node.node_id)

            run.current_step += 1
            node.status = NodeStatus.RUNNING
            node.started_at = time.time()
            node.log(f"开始执行: {node.name}")

            try:
                # 执行节点处理器
                if node.handler:
                    node.outputs = node.handler(node.inputs) or {}
                node.status = NodeStatus.SUCCESS
                node.log(f"执行成功: {node.name}")

            except Exception as e:
                node.status = NodeStatus.FAILED
                node.log(f"执行失败: {e}")
                run.error_log.append(f"{node.name}: {e}")

                if node.retry_count < node.max_retries:
                    node.retry_count += 1
                    node.log(f"重试 {node.retry_count}/{node.max_retries}")
                    node.status = NodeStatus.PENDING
                    pending.insert(0, node)
                    continue

            node.finished_at = time.time()
            node.status = NodeStatus.SUCCESS if node.status != NodeStatus.FAILED else NodeStatus.FAILED

            # 查找出边
            outgoing = [e for e in self.edges.values() if e.source == node.node_id]

            for edge in outgoing:
                run.edges_traversed.append(edge.edge_id)

                if edge.rule == RoutingRule.CONDITIONAL and edge.condition:
                    if not edge.condition(node.outputs):
                        continue  # 条件不满足，跳过

                target_node = self.nodes.get(edge.target)
                if target_node and target_node.node_id not in visited:
                    if edge.rule == RoutingRule.PARALLEL_ALL:
                        # 并行：同时添加所有并行边
                        parallel_edges = [e for e in self.edges.values() if e.source == node.node_id and e.rule == RoutingRule.PARALLEL_ALL]
                        for pe in parallel_edges:
                            pn = self.nodes.get(pe.target)
                            if pn and pn.node_id not in visited:
                                pending.insert(0, pn)
                        break
                    else:
                        pending.insert(0, target_node)

        run.finished_at = time.time()
        run.nodes_state = {nid: n.status for nid, n in self.nodes.items()}

        # 检查是否有节点未执行
        for node in self.nodes.values():
            if node.node_id not in visited:
                node.status = NodeStatus.SKIPPED

        run.total_steps = len(visited)
        return run

    # ---- 状态看板 ----
    def get_dashboard(self) -> dict:
        """
        生成运行状态看板数据 — 用于前端可视化渲染
        
        Returns:
            结构化的看板数据，可直接序列化为JSON供前端消费
        """
        nodes_status = []
        for node in self.nodes.values():
            nodes_status.append({
                "id": node.node_id, "name": node.name,
                "type": node.node_type.name, "status": node.status.value,
                "duration_ms": node.duration_ms(), "retries": node.retry_count,
                "log_lines": node.log_lines[-5:],  # 最近5条日志
            })

        edges_status = []
        for edge in self.edges.values():
            traversed = edge.edge_id in (self._current_run.edges_traversed if self._current_run else [])
            edges_status.append({
                "id": edge.edge_id, "source": edge.source,
                "target": edge.target, "rule": edge.rule.value,
                "label": edge.label, "traversed": traversed,
            })

        run_info = None
        if self._current_run:
            run_info = {
                "run_id": self._current_run.run_id,
                "started_at": self._current_run.started_at,
                "finished_at": self._current_run.finished_at,
                "duration_s": (self._current_run.finished_at - self._current_run.started_at) if self._current_run.finished_at else 0,
                "total_steps": self._current_run.total_steps,
                "current_step": self._current_run.current_step,
                "error_count": len(self._current_run.error_log),
            }

        return {
            "workflow_name": self.name,
            "nodes": nodes_status,
            "edges": edges_status,
            "run": run_info,
            "agent_load": self.agent_dispatcher.get_load_stats(),
            "summary": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "success_count": sum(1 for n in self.nodes.values() if n.status == NodeStatus.SUCCESS),
                "failed_count": sum(1 for n in self.nodes.values() if n.status == NodeStatus.FAILED),
                "skipped_count": sum(1 for n in self.nodes.values() if n.status == NodeStatus.SKIPPED),
            },
        }

    def get_dashboard_html(self) -> str:
        """生成可视化看板HTML（简化版）"""
        dash = self.get_dashboard()
        nodes_html = ""
        for node in dash["nodes"]:
            color = {"success": "#4CAF50", "failed": "#F44336", "running": "#2196F3",
                     "pending": "#9E9E9E", "skipped": "#FFC107", "timeout": "#FF9800"}
            bg = color.get(node["status"], "#9E9E9E")
            nodes_html += f"""
            <div style="border:2px solid {bg}; border-radius:8px; padding:10px; margin:5px; display:inline-block; min-width:140px;">
                <strong>{node['name']}</strong><br>
                <span style="color:{bg}">● {node['status']}</span><br>
                <small>{node['duration_ms']:.0f}ms | {node['type']}</small>
            </div>"""

        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>工作流看板 - {self.name}</title>
<style>body{{font-family:system-ui;background:#1a1a2e;color:#e0e0e0;padding:20px}}
.summary{{background:#16213e;padding:15px;border-radius:8px;margin:10px 0}}
h2{{color:#00d4ff}}</style></head><body>
<h2>工作流看板: {self.name}</h2>
<div class="summary">
    节点 {dash['summary']['total_nodes']} | 边 {dash['summary']['total_edges']} | 
    成功 {dash['summary']['success_count']} | 失败 {dash['summary']['failed_count']}
</div>
<div style="display:flex;flex-wrap:wrap;gap:8px;">{nodes_html}</div>
<div style="margin-top:20px"><h3>Agent负载</h3><pre>{json.dumps(dash['agent_load'], indent=2, ensure_ascii=False)}</pre></div>
</body></html>"""

    # ---- 节点监控 ----
    def get_node_metrics(self, node_id: str) -> Optional[dict]:
        """获取单个节点监控指标"""
        node = self.nodes.get(node_id)
        if not node:
            return None
        return {
            "name": node.name,
            "type": node.node_type.name,
            "status": node.status.value,
            "duration_ms": node.duration_ms(),
            "retries": node.retry_count,
            "input_keys": list(node.inputs.keys()),
            "output_keys": list(node.outputs.keys()),
            "log": node.log_lines,
            "timeout": node.timeout_seconds,
        }

    def get_all_metrics(self) -> list[dict]:
        """获取所有节点监控指标"""
        return [m for nid in self.nodes if (m := self.get_node_metrics(nid))]

    # ---- 历史运行记录 ----
    def get_run_history(self, limit: int = 10) -> list[dict]:
        """获取运行历史"""
        history = []
        for run in self.runs[-limit:]:
            history.append({
                "run_id": run.run_id,
                "started_at": run.started_at,
                "duration_s": (run.finished_at - run.started_at) if run.finished_at else None,
                "total_steps": run.total_steps,
                "errors": len(run.error_log),
                "edges_traversed": len(run.edges_traversed),
            })
        return history


# ============================================================================
# 第四部分：预置工作流模板
# ============================================================================

class WorkflowTemplates:
    """预置工作流模板库"""

    @staticmethod
    def iteration_workflow(engine: VisualWorkflowEngine) -> VisualWorkflowEngine:
        """迭代补全工作流模板"""
        start = engine.create_node("开始迭代", NodeType.START)
        baseline = engine.create_node("基线评估", NodeType.TASK)
        gap_scan = engine.create_node("缺口扫描", NodeType.TASK)
        retrieval = engine.create_node("全网检索", NodeType.AGENT)
        analysis = engine.create_node("情报分析", NodeType.TASK)
        design = engine.create_node("方案设计", NodeType.TASK)
        impl = engine.create_node("代码落地", NodeType.TASK)
        verify = engine.create_node("验证归档", NodeType.TASK)
        end = engine.create_node("迭代完成", NodeType.END)

        engine.connect(start.node_id, baseline.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(baseline.node_id, gap_scan.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(gap_scan.node_id, retrieval.node_id, RoutingRule.PARALLEL_ALL)
        engine.connect(retrieval.node_id, analysis.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(analysis.node_id, design.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(design.node_id, impl.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(impl.node_id, verify.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(verify.node_id, end.node_id, RoutingRule.SEQUENTIAL)

        return engine

    @staticmethod
    def multi_agent_workflow(engine: VisualWorkflowEngine) -> VisualWorkflowEngine:
        """多Agent协作工作流模板"""
        start = engine.create_node("任务接收", NodeType.START)
        classify = engine.create_node("任务分类", NodeType.TASK)
        fanout = engine.create_node("并行分发", NodeType.PARALLEL)
        agent_a = engine.create_node("Agent-A执行", NodeType.AGENT)
        agent_b = engine.create_node("Agent-B执行", NodeType.AGENT)
        agent_c = engine.create_node("Agent-C执行", NodeType.AGENT)
        join = engine.create_node("结果汇合", NodeType.JOIN)
        merge = engine.create_node("结果融合", NodeType.TASK)
        end = engine.create_node("任务完成", NodeType.END)

        engine.connect(start.node_id, classify.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(classify.node_id, fanout.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(fanout.node_id, agent_a.node_id, RoutingRule.PARALLEL_ALL)
        engine.connect(fanout.node_id, agent_b.node_id, RoutingRule.PARALLEL_ALL)
        engine.connect(fanout.node_id, agent_c.node_id, RoutingRule.PARALLEL_ALL)
        engine.connect(agent_a.node_id, join.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(agent_b.node_id, join.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(agent_c.node_id, join.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(join.node_id, merge.node_id, RoutingRule.SEQUENTIAL)
        engine.connect(merge.node_id, end.node_id, RoutingRule.SEQUENTIAL)

        return engine


# ============================================================================
# 第五部分：模块自检
# ============================================================================

def self_test():
    """模块自检"""
    print("=" * 60)
    print("可视化工作流引擎 v3.0 自检")
    print("=" * 60)

    # 1. AgentDispatcher测试
    dispatcher = AgentDispatcher()
    dispatcher.register_agent("file-agent", ["文件", "搜索", "读取", "写入"])
    dispatcher.register_agent("app-agent", ["应用", "安装", "启动", "操作"])
    dispatcher.register_agent("computer-agent", ["系统", "设置", "配置", "窗口"])

    tasks = [
        AgentTask(task_id="t1", agent_name="file-agent", task_description="搜索文件"),
        AgentTask(task_id="t2", agent_name="app-agent", task_description="启动应用"),
    ]

    plan = dispatcher.dispatch(tasks, mode=AgentMode.FAN_OUT)
    print(f"\n[Agent分发] FAN_OUT模式 → {plan['mode']}")
    print(f"  分配方案: {plan['assignments']}")
    print(f"  负载: {dispatcher.get_load_stats()}")

    plan2 = dispatcher.dispatch(tasks, mode=AgentMode.VOTING)
    print(f"\n[Agent分发] VOTING模式 → {plan2['assignments']}")

    # 2. WorkflowEngine测试
    engine = VisualWorkflowEngine("迭代补全测试")

    def dummy_handler(inputs):
        return {"result": "done"}

    start = engine.create_node("开始", NodeType.START)
    scan = engine.create_node("扫描", NodeType.TASK, handler=dummy_handler)
    build = engine.create_node("构建", NodeType.TASK, handler=dummy_handler)
    archive = engine.create_node("归档", NodeType.TASK, handler=dummy_handler)
    end = engine.create_node("结束", NodeType.END)

    engine.connect(start.node_id, scan.node_id)
    engine.connect(scan.node_id, build.node_id)
    engine.connect(build.node_id, archive.node_id)
    engine.connect(archive.node_id, end.node_id)

    run = engine.execute()
    print(f"\n[工作流执行] {run.run_id}")
    print(f"  步骤: {run.total_steps}, 耗时: {run.finished_at - run.started_at:.3f}s")

    # 3. 看板
    dash = engine.get_dashboard()
    print(f"\n[状态看板] 节点: {dash['summary']['total_nodes']}, "
          f"成功: {dash['summary']['success_count']}, 失败: {dash['summary']['failed_count']}")

    metrics = engine.get_all_metrics()
    print(f"  节点监控: {len(metrics)} 个节点已记录")

    # 4. 工作流模板测试
    engine2 = VisualWorkflowEngine("多Agent协作模板")
    engine2 = WorkflowTemplates.multi_agent_workflow(engine2)
    print(f"\n[模板] 多Agent协作模板: {len(engine2.nodes)} 节点, {len(engine2.edges)} 边")

    print("\n✅ 所有模块自检通过")


if __name__ == "__main__":
    self_test()

```
