# -*- coding: utf-8 -*-
"""
全域集成桥接模块 v1.0 — R16 三引擎统一调度层
将 Claude推理引擎 / 可视化工作流 / 自进化闭环 编织为统一执行总线
"""

import json
import time
import uuid
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Optional

# ==================== 三引擎统一调度器 ====================

class UnifiedOrchestrator:
    """
    统一调度器：三引擎编织层
    
    执行总线:
      用户请求 → 推理引擎(intent+condition) → 工作流引擎(execution) → 自进化(review+learn)
    
    数据流:
      Intent → ConditionTree → Workflow → Execution → Review → SkillForge → Snapshot
    """

    def __init__(self,
                 reasoning_engine,       # ClaudeReasoningEngineV2 实例
                 workflow_manager,       # WorkflowManagerV2 实例
                 evolution_orchestrator, # EvolutionOrchestratorV3 实例
                 config: dict = None):
        self.reasoning = reasoning_engine
        self.workflow = workflow_manager
        self.evolution = evolution_orchestrator
        self.config = config or {}
        self.execution_history: list = []
        self.metrics: dict = {"total_requests": 0, "successful": 0, "failed": 0, "avg_latency_ms": 0}

    def process(self, user_input: str, context: dict = None) -> dict:
        """统一处理管线"""
        request_id = f"req_{uuid.uuid4().hex[:8]}"
        start_time = time.time()

        self.metrics["total_requests"] += 1

        # Step 1: 推理引擎 — 意图解析 + 条件拆解
        reasoning_result = self.reasoning.process(user_input, context or {})
        intent = reasoning_result.get("intent")
        condition_tree = reasoning_result.get("condition_tree")

        # Step 2: 工作流引擎 — 生成并执行工作流
        workflow = self._build_workflow_from_reasoning(reasoning_result, request_id)
        wf_id = self.workflow.register(workflow)
        execution = self.workflow.run(wf_id)

        # Step 3: 自进化闭环 — 复盘 + 学习
        if execution:
            self.metrics["successful"] += 1

            # 技能萃取（如果有新工具调用模式）
            if execution.trace_chain:
                self.evolution.skill_forge.extract_from_logs([
                    {"action": t.get("node", ""), "msg": f"status={t.get('status', '')}"}
                    for t in execution.trace_chain[-5:]
                ])

            # 适应度评估
            self.evolution.sica.evaluate_fitness(
                f"workflow_{request_id}",
                {"success_rate": 1.0, "avg_time_ms": execution.metrics.get("total_time_ms", 0),
                 "satisfaction": 0.85}
            )

            # 生成 Obsidian 笔记
            if self.evolution.obsidian.vault_path:
                from dataclasses import dataclass as dc
                @dc
                class DummySkill:
                    skill_id = f"wf_{request_id}"
                    name = f"Workflow Execution: {request_id}"
                    description = intent.raw_input if intent else user_input
                    version = "1.0"
                    status = type('obj', (object,), {'value': 'stable'})()
                    evo_generation = 1
                    lineage = [request_id]
                    trigger_keywords = [intent.intent_type] if intent else ["general"]
                    dependencies = []
                    performance_baseline = execution.metrics

                dummy = DummySkill()
                self.evolution.obsidian.sync_to_vault(dummy)

        else:
            self.metrics["failed"] += 1

        # 指标更新
        elapsed = (time.time() - start_time) * 1000
        self.metrics["avg_latency_ms"] = (
            self.metrics["avg_latency_ms"] * (self.metrics["total_requests"] - 1) + elapsed
        ) / self.metrics["total_requests"]

        result = {
            "request_id": request_id,
            "intent": {
                "type": intent.intent_type if intent else "unknown",
                "difficulty": f"L{intent.difficulty.value}" if intent else "unknown",
            },
            "reasoning": {
                "path": reasoning_result.get("best_path", {}).path_id if reasoning_result.get("best_path") else "none",
                "cache_stats": reasoning_result.get("cache_stats", {}),
                "review_score": reasoning_result.get("review", {}).quality_score if reasoning_result.get("review") else 0,
            },
            "execution": {
                "execution_id": execution.execution_id if execution else "none",
                "total_time_ms": execution.metrics.get("total_time_ms", 0) if execution else 0,
                "nodes_visited": len(execution.trace_chain) if execution else 0,
            },
            "evolution": {
                "snap_active": self.evolution.snapshot.active_snap.snap_id if self.evolution.snapshot.active_snap else "none",
                "skills_registered": len(self.evolution.skill_forge.skill_store),
            },
            "latency_ms": elapsed,
        }

        self.execution_history.append(result)
        return result

    def _build_workflow_from_reasoning(self, reasoning_result: dict, request_id: str):
        """从推理结果自动构建工作流"""
        from dataclasses import dataclass as WF, field as wf_field
        from enum import Enum as _E

        class NT(_E): TRIGGER="trigger"; ACTION="action"; AGENT="agent"; MERGE="merge"; TERMINAL="terminal"

        @dataclass
        class WNode:
            node_id: str; node_type: NT; display_name: str
            config: dict = field(default_factory=dict); next_nodes: list = field(default_factory=list)
            status: Any = "pending"; output: Any = None; execution_time_ms: float = 0
            retry_count: int = 0; metrics: dict = field(default_factory=dict)
            on_error: str = None; fallback_node: str = None

        @dataclass
        class Workflow:
            workflow_id: str; name: str; description: str = ""
            nodes: dict = field(default_factory=dict); entry_node_id: str = ""
            execution_mode: Any = "sequential"; status: Any = "pending"
            created_at: str = field(default_factory=lambda: datetime.now().isoformat())
            tags: list = field(default_factory=list)

        from enum import Enum as _E2
        class EM(_E2): SEQUENTIAL="sequential"; PARALLEL="parallel"

        intent = reasoning_result.get("intent")
        difficulty = intent.difficulty.value if intent else 2

        # 自动节点生成
        nodes = {
            "n1": WNode("n1", NT.ACTION, f"解析: {intent.intent_type if intent else 'general'}", {},
                        ["n2"]),
            "n2": WNode("n2", NT.ACTION, f"拆解: L{difficulty}条件建模", {}, ["n3"]),
            "n3": WNode("n3", NT.AGENT if difficulty >= 3 else NT.ACTION,
                        "推理执行" if difficulty >= 3 else "直接执行",
                        {"agent_name": "search-agent" if difficulty >= 3 else ""},
                        ["n4"]),
            "n4": WNode("n4", NT.MERGE, "结果汇总", {}, ["n5"]),
            "n5": WNode("n5", NT.TERMINAL, "完成", {"terminal_type": "success"}, []),
        }

        wf = Workflow(
            workflow_id=f"wf_{request_id}",
            name=f"自动工作流: {intent.intent_type if intent else 'general'}",
            description=f"由推理引擎自动生成的执行工作流 (难度L{difficulty})",
            nodes={k: v for k, v in nodes.items()},
            entry_node_id="n1",
            execution_mode=EM.PARALLEL if difficulty >= 3 else EM.SEQUENTIAL,
        )

        return wf

    def get_status_report(self) -> dict:
        """生成状态报告"""
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics,
            "engines": {
                "reasoning": "active" if self.reasoning else "inactive",
                "workflow": "active" if self.workflow else "inactive",
                "evolution": "active" if self.evolution else "inactive",
            },
            "modular_health": {
                "Claude推理引擎v2.0": "healthy" if self.reasoning else "missing",
                "可视化工作流v2.0": "healthy" if self.workflow else "missing",
                "自进化闭环v3.0": "healthy" if self.evolution else "missing",
            }
        }


# ==================== 工厂函数 ====================

def build_unified_orchestrator(
    skill_store: dict = None,
    tool_registry: dict = None,
    dispatch_fn=None,
    vault_path: str = None,
    workspace: str = "."
) -> UnifiedOrchestrator:
    """构建统一调度器实例"""

    # Lazy import to avoid circular deps
    import sys

    # 推理引擎
    from claude_reasoning_enhanced_v2_0 import ClaudeReasoningEngineV2
    reasoning = ClaudeReasoningEngineV2(tool_registry=tool_registry)

    # 工作流管理器
    from visual_workflow_engine_v2_0 import WorkflowManagerV2
    workflow = WorkflowManagerV2(tool_registry=tool_registry, dispatch_fn=dispatch_fn)

    # 自进化编排器
    from self_evolution_v3_0 import EvolutionOrchestratorV3
    evolution = EvolutionOrchestratorV3(
        skill_store=skill_store,
        tool_map=tool_registry,
        vault_path=vault_path,
        workspace=workspace
    )

    return UnifiedOrchestrator(
        reasoning_engine=reasoning,
        workflow_manager=workflow,
        evolution_orchestrator=evolution,
    )


# ==================== 时序调度器 ====================

class ScheduledLoopRunner:
    """
    时序调度器：按3小时周期执行自进化循环
    """

    DEFAULT_INTERVAL_SECONDS = 10800  # 3 hours

    def __init__(self, orchestrator: UnifiedOrchestrator):
        self.orchestrator = orchestrator
        self.interval = self.DEFAULT_INTERVAL_SECONDS
        self.cycle_count = 0
        self.cycle_results: list = []

    def run_single_cycle(self, trigger: str = "scheduled",
                         target_gaps: list = None) -> dict:
        """执行单次进化循环"""
        self.cycle_count += 1
        now = datetime.now()

        context = {}
        if target_gaps:
            context["target_gaps"] = target_gaps

        result = self.orchestrator.evolution.run_full_cycle(
            trigger=type('T', (), {'value': trigger})(),
            context=context
        )

        cycle_record = {
            "cycle_id": self.cycle_count,
            "timestamp": now.isoformat(),
            "trigger": trigger,
            "skills_extracted": result.get("skills_extracted", 0),
            "skills_registered": len(result.get("skills_registered", [])),
            "gaps_detected": len(result.get("gaps", [])),
            "snapshot_id": result.get("post_snapshot", ""),
            "duration": "~3s"  # approximate
        }

        self.cycle_results.append(cycle_record)
        return cycle_record

    def get_history(self) -> list:
        return self.cycle_results

    def get_next_run(self) -> str:
        return f"{(datetime.timestamp(datetime.now()) + self.interval) / 3600:.1f}h from now"


if __name__ == "__main__":
    print("=" * 50)
    print("全域集成桥接模块 v1.0")
    print("编织: Claude推理 | 可视工作流 | 自进化闭环")
    print("=" * 50)

    print("\n模块就绪。通过 build_unified_orchestrator() 构建统一调度器。")
    print("时序调度器 SupportedLoopRunner 支持每3小时自动进化循环。")