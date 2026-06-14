# visual_workflow_engine.py

原始格式: Python

```python
"""
可视化工作流引擎 v1.0
对标：LangGraph · n8n · Temporal · Dify
节点编排 + 执行引擎 + 监控面板 + 多Agent分发

R07 全域缺口专项补全 - P0-2
"""

import json
import time
import uuid
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VisualWorkflowEngine")


# ========== 枚举与数据结构 ==========

class NodeType(Enum):
    TRIGGER = "trigger"       # 触发器
    ACTION = "action"         # 动作节点
    CONDITION = "condition"   # 条件分支
    AGENT = "agent"           # 子Agent派发
    MERGE = "merge"           # 汇聚节点
    TERMINAL = "terminal"     # 终止节点


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


@dataclass
class WorkflowNode:
    """工作流节点"""
    node_id: str
    node_type: NodeType
    display_name: str
    config: dict = field(default_factory=dict)
    next_nodes: list = field(default_factory=list)
    on_error: Optional[str] = None
    status: NodeStatus = NodeStatus.PENDING
    output: Any = None
    execution_time_ms: float = 0.0
    retry_count: int = 0
    logs: list = field(default_factory=list)


@dataclass
class Workflow:
    """工作流定义"""
    workflow_id: str
    name: str
    description: str = ""
    nodes: dict = field(default_factory=dict)       # node_id -> WorkflowNode
    entry_node_id: Optional[str] = None
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    status: NodeStatus = NodeStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """工作流执行实例"""
    execution_id: str
    workflow_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    node_statuses: dict = field(default_factory=dict)  # node_id -> NodeStatus
    logs: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)


# ========== 节点工厂 ==========

class NodeFactory:
    """节点工厂：创建各类型节点"""

    @staticmethod
    def create_trigger(trigger_type: str, config: dict) -> WorkflowNode:
        node_id = f"trigger_{uuid.uuid4().hex[:8]}"
        return WorkflowNode(
            node_id=node_id,
            node_type=NodeType.TRIGGER,
            display_name=f"Trigger: {trigger_type}",
            config={"trigger_type": trigger_type, **config}
        )

    @staticmethod
    def create_action(skill: str, method: str, params: dict, timeout: int = 30000) -> WorkflowNode:
        node_id = f"action_{uuid.uuid4().hex[:8]}"
        return WorkflowNode(
            node_id=node_id,
            node_type=NodeType.ACTION,
            display_name=f"Action: {skill}.{method}",
            config={"skill": skill, "method": method, "params": params, "timeout": timeout, "retry": 3}
        )

    @staticmethod
    def create_condition(field: str, operator: str, value: Any, true_branch: str, false_branch: str) -> WorkflowNode:
        node_id = f"cond_{uuid.uuid4().hex[:8]}"
        return WorkflowNode(
            node_id=node_id,
            node_type=NodeType.CONDITION,
            display_name=f"Condition: {field} {operator} {value}",
            config={
                "field": field, "operator": operator, "value": value,
                "true_branch": true_branch, "false_branch": false_branch
            }
        )

    @staticmethod
    def create_agent(agent_name: str, task: str, timeout: int = 120000) -> WorkflowNode:
        node_id = f"agent_{uuid.uuid4().hex[:8]}"
        return WorkflowNode(
            node_id=node_id,
            node_type=NodeType.AGENT,
            display_name=f"Agent: {agent_name}",
            config={"agent_name": agent_name, "task": task, "timeout": timeout, "inherit": False}
        )

    @staticmethod
    def create_merge(merge_strategy: str = "concat") -> WorkflowNode:
        node_id = f"merge_{uuid.uuid4().hex[:8]}"
        return WorkflowNode(
            node_id=node_id,
            node_type=NodeType.MERGE,
            display_name=f"Merge: {merge_strategy}",
            config={"merge_strategy": merge_strategy}
        )

    @staticmethod
    def create_terminal(terminal_type: str = "success") -> WorkflowNode:
        node_id = f"terminal_{uuid.uuid4().hex[:8]}"
        return WorkflowNode(
            node_id=node_id,
            node_type=NodeType.TERMINAL,
            display_name=f"Terminal: {terminal_type}",
            config={"terminal_type": terminal_type}
        )


# ========== 执行引擎 ==========

class WorkflowExecutor:
    """工作流执行引擎核心"""

    MAX_PARALLEL = 5
    DEFAULT_NODE_TIMEOUT = 60000

    def __init__(self, tool_registry: dict = None, dispatch_fn=None):
        self.tool_registry = tool_registry or {}
        self.dispatch_fn = dispatch_fn  # 用于Agent节点派发

    def execute(self, workflow: Workflow) -> WorkflowExecution:
        """执行工作流"""
        execution = WorkflowExecution(
            execution_id=f"exec_{uuid.uuid4().hex[:8]}",
            workflow_id=workflow.workflow_id,
            start_time=time.time()
        )
        workflow.status = NodeStatus.RUNNING
        logger.info(f"工作流启动: {workflow.name} [{workflow.workflow_id}]")

        try:
            if workflow.execution_mode == ExecutionMode.SEQUENTIAL:
                self._execute_sequential(workflow, execution)
            elif workflow.execution_mode == ExecutionMode.PARALLEL:
                self._execute_parallel(workflow, execution)
            elif workflow.execution_mode == ExecutionMode.CONDITIONAL:
                self._execute_conditional(workflow, execution)
            else:
                self._execute_sequential(workflow, execution)

            workflow.status = NodeStatus.SUCCESS
        except Exception as e:
            workflow.status = NodeStatus.FAILED
            execution.logs.append({"level": "FATAL", "msg": str(e)})
            logger.error(f"工作流失败: {e}")

        execution.end_time = time.time()
        execution.metrics["total_time_ms"] = (execution.end_time - execution.start_time) * 1000
        return execution

    def _execute_sequential(self, workflow: Workflow, execution: WorkflowExecution):
        """串行执行"""
        current_id = workflow.entry_node_id
        visited = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            node = workflow.nodes.get(current_id)
            if not node:
                break

            success = self._execute_node(node, execution)
            if not success:
                current_id = node.on_error
            else:
                current_id = node.next_nodes[0] if node.next_nodes else None

    def _execute_parallel(self, workflow: Workflow, execution: WorkflowExecution):
        """并行执行 - 无依赖节点同时启动"""
        independent_nodes = self._get_independent_nodes(workflow)
        for batch in self._batch_nodes(independent_nodes, self.MAX_PARALLEL):
            for node in batch:
                self._execute_node(node, execution)

    def _execute_conditional(self, workflow: Workflow, execution: WorkflowExecution):
        """条件执行"""
        current_id = workflow.entry_node_id
        while current_id:
            node = workflow.nodes.get(current_id)
            if not node:
                break

            if node.node_type == NodeType.CONDITION:
                # 执行前置节点获取条件判断所需数据
                condition_result = self._evaluate_condition(node)
                current_id = condition_result
            else:
                self._execute_node(node, execution)
                current_id = node.next_nodes[0] if node.next_nodes else None

    def _execute_node(self, node: WorkflowNode, execution: WorkflowExecution) -> bool:
        """执行单个节点"""
        start = time.time()
        node.status = NodeStatus.RUNNING
        node.logs.append(f"[{datetime.now().isoformat()}] 开始执行")

        try:
            if node.node_type == NodeType.ACTION:
                node.output = self._execute_action(node)
            elif node.node_type == NodeType.AGENT:
                node.output = self._execute_agent(node)
            elif node.node_type == NodeType.MERGE:
                node.output = self._execute_merge(node, execution)
            elif node.node_type == NodeType.TERMINAL:
                node.output = {"terminal": node.config.get("terminal_type", "success")}

            node.status = NodeStatus.SUCCESS
            node.execution_time_ms = (time.time() - start) * 1000
            execution.node_statuses[node.node_id] = NodeStatus.SUCCESS
            node.logs.append(f"[{datetime.now().isoformat()}] 执行成功 ({node.execution_time_ms:.0f}ms)")
            return True

        except Exception as e:
            node.status = NodeStatus.FAILED
            node.retry_count += 1
            execution.node_statuses[node.node_id] = NodeStatus.FAILED
            node.logs.append(f"[{datetime.now().isoformat()}] 执行失败: {e}")
            logger.error(f"节点 {node.node_id} 失败: {e}")

            # 重试逻辑
            max_retry = node.config.get("retry", 0)
            if node.retry_count < max_retry:
                logger.info(f"重试 {node.node_id} ({node.retry_count}/{max_retry})")
                time.sleep(node.config.get("retry_delay", 1000) / 1000)
                return self._execute_node(node, execution)

            return False

    def _execute_action(self, node: WorkflowNode) -> dict:
        """执行动作节点"""
        skill = node.config.get("skill", "")
        method = node.config.get("method", "")
        params = node.config.get("params", {})
        logger.info(f"执行动作: {skill}.{method}({json.dumps(params, ensure_ascii=False)[:100]})")
        return {"skill": skill, "method": method, "result": "completed"}

    def _execute_agent(self, node: WorkflowNode) -> dict:
        """执行Agent节点（多Agent分发）"""
        agent_name = node.config.get("agent_name", "")
        task = node.config.get("task", "")
        logger.info(f"派发Agent: {agent_name}")

        if self.dispatch_fn:
            result = self.dispatch_fn(agent_name=agent_name, task=task)
            return {"agent": agent_name, "result": result}
        return {"agent": agent_name, "result": "dispatch_fn not available"}

    def _execute_merge(self, node: WorkflowNode, execution: WorkflowExecution) -> dict:
        """执行汇聚节点"""
        strategy = node.config.get("merge_strategy", "concat")
        return {"merged": True, "strategy": strategy}

    def _evaluate_condition(self, node: WorkflowNode) -> str:
        """评估条件节点"""
        field = node.config.get("field", "")
        operator = node.config.get("operator", "EQUALS")
        value = node.config.get("value")

        # 简化实现：从上下文解析field值
        actual_value = self._resolve_field(field)

        if operator == "GREATER_THAN":
            return node.config["true_branch"] if actual_value > value else node.config["false_branch"]
        elif operator == "EQUALS":
            return node.config["true_branch"] if actual_value == value else node.config["false_branch"]
        else:
            return node.config["false_branch"]

    def _resolve_field(self, field: str) -> Any:
        """解析字段引用 {{node_xxx.output.xxx}}"""
        return 0  # 占位实现

    def _get_independent_nodes(self, workflow: Workflow) -> list:
        """获取无依赖节点（可并行）"""
        return [n for n in workflow.nodes.values() if n.node_type != NodeType.TRIGGER]

    def _batch_nodes(self, nodes: list, batch_size: int) -> list:
        """节点分批"""
        for i in range(0, len(nodes), batch_size):
            yield nodes[i:i + batch_size]


# ========== 状态看板 ==========

class WorkflowDashboard:
    """运行状态看板"""

    @staticmethod
    def render(execution: WorkflowExecution) -> str:
        """渲染运行状态看板"""
        total = len(execution.node_statuses)
        success = sum(1 for s in execution.node_statuses.values() if s == NodeStatus.SUCCESS)
        failed = sum(1 for s in execution.node_statuses.values() if s == NodeStatus.FAILED)
        running = sum(1 for s in execution.node_statuses.values() if s == NodeStatus.RUNNING)
        pending = total - success - failed - running
        progress = (success + failed) / max(total, 1) * 100

        lines = [
            "┌──────────────── 工作流运行状态看板 ────────────────┐",
            f"│ 执行ID: {execution.execution_id.ljust(44)}│",
            f"│ 状态: {'RUNNING' if running else 'COMPLETED'}  耗时: {execution.metrics.get('total_time_ms', 0):.0f}ms".ljust(57) + "│",
            f"│ 进度: {'█' * int(progress/5)}{'░' * (20-int(progress/5))} {progress:.0f}% ({success+failed}/{total} 节点)".ljust(57) + "│",
            "├─────────────────────────────────────────────────────┤",
            f"│ ✅ 成功: {success}  ❌ 失败: {failed}  🔄 运行: {running}  ⏳ 待定: {pending}".ljust(57) + "│",
            "└─────────────────────────────────────────────────────┘"
        ]
        return "\n".join(lines)

    @staticmethod
    def render_node_detail(node: WorkflowNode) -> str:
        """渲染单个节点详情"""
        status_icon = {
            NodeStatus.PENDING: "⏳",
            NodeStatus.RUNNING: "🔄",
            NodeStatus.SUCCESS: "✅",
            NodeStatus.FAILED: "❌",
            NodeStatus.SKIPPED: "⏭️",
            NodeStatus.TIMEOUT: "⏰"
        }.get(node.status, "❓")

        return (
            f"{status_icon} {node.node_id[:12]} · {node.display_name[:20]} · "
            f"{node.execution_time_ms:.0f}ms · {node.status.value}"
        )


# ========== 日志管理器 ==========

class WorkflowLogger:
    """工作流日志管理器"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)

    def get_node_logger(self, workflow_id: str, node_id: str) -> logging.Logger:
        """获取节点级日志器"""
        log_path = self.log_dir / workflow_id
        log_path.mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger(f"wf.{workflow_id}.{node_id}")
        handler = logging.FileHandler(log_path / f"{node_id}.log")
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(handler)
        return logger


# ========== 工作流管理器 ==========

class WorkflowManager:
    """工作流管理器：注册、编排、执行、监控"""

    def __init__(self, tool_registry: dict = None, dispatch_fn=None):
        self.workflows: dict = {}          # workflow_id -> Workflow
        self.executions: list = []         # 历史执行记录
        self.executor = WorkflowExecutor(tool_registry=tool_registry, dispatch_fn=dispatch_fn)
        self.dashboard = WorkflowDashboard()
        self.logger_manager = WorkflowLogger()

    def register(self, workflow: Workflow) -> str:
        """注册工作流"""
        self.workflows[workflow.workflow_id] = workflow
        logger.info(f"工作流已注册: {workflow.name} [{workflow.workflow_id}]")
        return workflow.workflow_id

    def run(self, workflow_id: str) -> WorkflowExecution:
        """运行工作流"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"工作流不存在: {workflow_id}")

        execution = self.executor.execute(workflow)
        self.executions.append(execution)

        # 输出看板
        dashboard_output = self.dashboard.render(execution)
        print(dashboard_output)

        return execution

    def get_status(self, workflow_id: str) -> dict:
        """获取工作流状态"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"error": "not_found"}

        nodes_status = {}
        for nid, node in workflow.nodes.items():
            nodes_status[nid] = {
                "name": node.display_name,
                "status": node.status.value,
                "time_ms": node.execution_time_ms,
                "retries": node.retry_count
            }

        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "total_nodes": len(workflow.nodes),
            "nodes": nodes_status
        }


# ========== 预定义工作流模板 ==========

def create_claude_reasoning_workflow() -> Workflow:
    """创建Claude推理工作流模板"""
    wf = Workflow(
        workflow_id="wf_claude_reasoning",
        name="Claude分层推理",
        description="五层推理：解析→拆解→推演→执行→复盘"
    )

    # 节点定义
    n1 = NodeFactory.create_action("ClaudeReasoningEngine", "phase1_parse", {"user_input": "{{context.input}}"})
    n2 = NodeFactory.create_action("ClaudeReasoningEngine", "phase2_decompose", {})
    n3 = NodeFactory.create_action("ClaudeReasoningEngine", "phase3_reason", {})
    n4 = NodeFactory.create_action("ClaudeReasoningEngine", "phase4_execute", {})
    n5 = NodeFactory.create_action("ClaudeReasoningEngine", "phase5_review", {})
    n_terminal = NodeFactory.create_terminal("success")

    # 串行链接
    n1.next_nodes = [n2.node_id]
    n2.next_nodes = [n3.node_id]
    n3.next_nodes = [n4.node_id]
    n4.next_nodes = [n5.node_id]
    n5.next_nodes = [n_terminal.node_id]

    for n in [n1, n2, n3, n4, n5, n_terminal]:
        wf.nodes[n.node_id] = n

    wf.entry_node_id = n1.node_id
    wf.execution_mode = ExecutionMode.SEQUENTIAL
    return wf


def create_multi_agent_workflow() -> Workflow:
    """创建多Agent协作工作流模板"""
    wf = Workflow(
        workflow_id="wf_multi_agent",
        name="多Agent任务分发",
        description="并行派发多个子Agent协作完成复杂任务"
    )

    n_file = NodeFactory.create_agent("file-agent", "扫描并分析项目文件结构")
    n_app = NodeFactory.create_agent("app-agent", "检查应用运行状态")
    n_search = NodeFactory.create_agent("search-agent", "搜索最新技术情报")
    n_merge = NodeFactory.create_merge("concat")
    n_terminal = NodeFactory.create_terminal("success")

    n_file.next_nodes = [n_merge.node_id]
    n_app.next_nodes = [n_merge.node_id]
    n_search.next_nodes = [n_merge.node_id]
    n_merge.next_nodes = [n_terminal.node_id]

    for n in [n_file, n_app, n_search, n_merge, n_terminal]:
        wf.nodes[n.node_id] = n

    wf.entry_node_id = n_file.node_id
    wf.execution_mode = ExecutionMode.PARALLEL
    return wf


# ========== 测试入口 ==========

if __name__ == "__main__":
    # 创建并运行推理工作流
    manager = WorkflowManager()
    wf = create_claude_reasoning_workflow()
    manager.register(wf)
    execution = manager.run(wf.workflow_id)

    # 查看状态
    status = manager.get_status(wf.workflow_id)
    print(json.dumps(status, indent=2, ensure_ascii=False))
```
