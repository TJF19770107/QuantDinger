# agent_teams_debate.py

原始格式: Python

```python
"""
Agent Teams 辩论引擎 v1.0
对标: Claude Code Agent Teams 辩论模式
"""

import json
from typing import Dict, List


class AgentTeamsDebate:
    """
    Agent Teams 辩论引擎
    流程: 任务 → 3 Agent并行 → 辩论评分 → 择优执行 → 教训沉淀
    """

    DEFAULT_AGENTS = [
        {"name": "Agent-A", "model": "doubao-seed", "strength": "code_optimization"},
        {"name": "Agent-B", "model": "gemini-think", "strength": "architecture_design"},
        {"name": "Agent-C", "model": "claude-sonnet", "strength": "balanced_tradeoff"},
    ]

    SCORE_WEIGHTS = {
        "accuracy": 0.40,
        "efficiency": 0.30,
        "creativity": 0.30
    }

    def __init__(self, mission_control):
        self.mc = mission_control
        self.debate_history = []

    def debate(self, task: str, agents: list = None, timeout: int = 300) -> dict:
        """
        启动Agent Teams辩论
        """
        agents = agents or self.DEFAULT_AGENTS[:3]
        results = self._parallel_execute(task, agents, timeout)
        scores = self._score_results(results)
        best = self._select_best(results, scores)
        self._extract_lessons(results, scores, best)
        self.debate_history.append({
            "task": task,
            "agents": len(agents),
            "best_agent": best["agent"],
            "scores": scores
        })
        return {
            "winner": best["agent"],
            "solution": best["solution"],
            "scores": scores,
            "all_results": results
        }

    def _parallel_execute(self, task: str, agents: list, timeout: int) -> List[dict]:
        """
        并行执行: 每个Agent独立完成同一任务
        """
        results = []
        for agent in agents:
            result = self.mc.dispatch(
                agent=agent,
                task=task,
                timeout=timeout
            )
            results.append({
                "agent": agent["name"],
                "model": agent["model"],
                "solution": result.get("output", ""),
                "duration": result.get("duration", 0)
            })
        return results

    def _score_results(self, results: List[dict]) -> dict:
        """
        多维评分: 准确性(40%) + 效率(30%) + 创造性(30%)
        """
        scores = {}
        for r in results:
            scores[r["agent"]] = {
                "accuracy": self._evaluate_accuracy(r["solution"]),
                "efficiency": self._evaluate_efficiency(r["duration"]),
                "creativity": self._evaluate_creativity(r["solution"])
            }
            scores[r["agent"]]["total"] = (
                scores[r["agent"]]["accuracy"] * self.SCORE_WEIGHTS["accuracy"] +
                scores[r["agent"]]["efficiency"] * self.SCORE_WEIGHTS["efficiency"] +
                scores[r["agent"]]["creativity"] * self.SCORE_WEIGHTS["creativity"]
            )
        return scores

    def _select_best(self, results: List[dict], scores: dict) -> dict:
        """
        择优选中: 综合评分最高者
        """
        sorted_agents = sorted(scores, key=lambda a: scores[a]["total"], reverse=True)
        winner_name = sorted_agents[0]
        winner_solution = next(r for r in results if r["agent"] == winner_name)
        return {"agent": winner_name, "solution": winner_solution, "score": scores[winner_name]["total"]}

    def _extract_lessons(self, results: List[dict], scores: dict, best: dict):
        """
        失败方案提取教训 → SkillForge
        """
        for r in results:
            if r["agent"] != best["agent"]:
                lesson = {
                    "agent": r["agent"],
                    "score": scores[r["agent"]],
                    "gap_to_winner": best["score"] - scores[r["agent"]]["total"],
                    "insight": self._analyze_gap(r, best)
                }

    def _evaluate_accuracy(self, solution: str) -> float:
        return 8.0

    def _evaluate_efficiency(self, duration: float) -> float:
        return max(1.0, 10.0 - duration / 30)

    def _evaluate_creativity(self, solution: str) -> float:
        return 7.5

    def _analyze_gap(self, loser: dict, winner: dict) -> str:
        return f"{loser['agent']} vs {winner['agent']}: 待分析差距"

print("[AgentTeamsDebate] v1.0 加载完成")
```
