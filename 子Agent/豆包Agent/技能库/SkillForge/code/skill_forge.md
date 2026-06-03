# skill_forge.py

> 原始文件: `skill_forge.py`  |  类型: `.py`  |  自动转换

```python
"""
SkillForge v2.0 - 自主技能锻造引擎 (DGM演化树)
路径: 豆包Agent/技能库/SkillForge/code/skill_forge.py
对标: Darwin Gödel Machine + LoongFlow PES + OpenClaw Skills
"""

import json
import re
import hashlib
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

logger = logging.getLogger("SkillForge")

class SkillStatus(Enum):
    ACTIVE = "active"
    DORMANT = "dormant"       # 连续10轮未使用
    DEPRECATED = "deprecated"  # 休眠超过50轮淘汰

@dataclass
class SkillNode:
    """演化树节点：一个技能版本"""
    id: str
    name: str
    version: str
    quality_score: float = 0.0
    parent_id: Optional[str] = None  # 父节点（来源技能）
    source_iteration: str = ""       # 来源迭代轮次
    triggers: List[str] = field(default_factory=list)
    status: SkillStatus = SkillStatus.ACTIVE
    usage_count: int = 0
    dormant_rounds: int = 0
    skill_path: str = ""

@dataclass
class SkillArchive:
    """DGM风格技能档案库"""
    nodes: Dict[str, SkillNode] = field(default_factory=dict)
    tree_edges: List[Tuple[str, str]] = field(default_factory=list)  # (parent_id, child_id)

class EvolutionTree:
    """DGM演化树管理器
    对标 Darwin Gödel Machine：档案库 + 采样 + 基准验证
    """

    def __init__(self, archive_path: Path):
        self.archive = SkillArchive()
        self.archive_path = archive_path
        self._load_archive()

    def sample(self, n: int = 5) -> List[SkillNode]:
        """采样：精英保留Top20% + 轮盘赌剩余80%"""
        active = [n for n in self.archive.nodes.values()
                  if n.status == SkillStatus.ACTIVE]
        active.sort(key=lambda n: n.quality_score, reverse=True)

        elite_count = max(1, int(len(active) * 0.2))
        elite = active[:elite_count]

        # 轮盘赌采样
        remaining = active[elite_count:]
        weights = [n.quality_score for n in remaining]
        total_w = sum(weights) or 1

        sampled = elite.copy()
        # TODO: R07 实际实现加权随机采样
        return sampled[:n]

    def mutate(self, node: SkillNode) -> SkillNode:
        """变异：20%概率引入新特性"""
        new_node = SkillNode(
            id=f"{node.id}_mut",
            name=node.name,
            version=f"{node.version}-mut",
            quality_score=node.quality_score * 0.9,  # 暂估：变异可能降低质量
            parent_id=node.id,
            triggers=node.triggers.copy(),
        )
        return new_node

    def crossover(self, parent_a: SkillNode, parent_b: SkillNode) -> SkillNode:
        """交叉：融合两个技能"""
        crossover_id = hashlib.md5(
            f"{parent_a.id}+{parent_b.id}".encode()
        ).hexdigest()[:12]
        return SkillNode(
            id=f"cross_{crossover_id}",
            name=f"{parent_a.name}×{parent_b.name}",
            version="v1.0-cross",
            quality_score=(parent_a.quality_score + parent_b.quality_score) / 2,
            triggers=list(set(parent_a.triggers + parent_b.triggers)),
        )

    def deprecate_stale(self, max_dormant: int = 50):
        """淘汰：休眠超过50轮 → 归档"""
        for node in self.archive.nodes.values():
            if node.dormant_rounds >= max_dormant:
                node.status = SkillStatus.DEPRECATED

    def _load_archive(self):
        """从磁盘加载技能档案库"""
        # TODO: R07 实现JSON序列化/反序列化
        pass

class PatternExtractor:
    """模式提取器：从迭代报告中识别可复用操作模式"""

    def __init__(self):
        self.min_frequency = 3  # 同一模式出现3次触发技能生成

    def extract(self, iteration_logs: List[str]) -> List[dict]:
        """从迭代日志中提取模式"""
        patterns = []
        # TODO: R07 实现LLM辅助模式提取或正则匹配
        return patterns

    def score_pattern(self, pattern: dict) -> float:
        """质量评分：复用频率(30%) + 成功率(30%) + 独立性(20%) + 通用性(20%)"""
        score = (
            pattern.get("frequency_score", 0) * 0.30 +
            pattern.get("success_score", 0) * 0.30 +
            pattern.get("independence_score", 0) * 0.20 +
            pattern.get("generality_score", 0) * 0.20
        )
        return score

class SkillForge:
    """技能锻造引擎主类"""

    ROOT_DIR = Path(r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent")
    SKILL_LIB = ROOT_DIR / "技能库"
    ITER_LOG_DIR = ROOT_DIR / "迭代记录"
    ARCHIVE_PATH = ROOT_DIR / "skill_archive.json"

    def __init__(self):
        self.extractor = PatternExtractor()
        self.evolution_tree = EvolutionTree(self.ARCHIVE_PATH)
        self.forge_count = 0

    def forge_from_logs(self, n_rounds: int = 5) -> dict:
        """从最近N轮迭代日志锻造新技能"""
        self.forge_count += 1
        logs = self._load_recent_logs(n_rounds)
        if not logs:
            return {"forged": 0, "message": "无可用日志"}

        # Step 1: 模式提取
        patterns = self.extractor.extract(logs)

        # Step 2: 质量评估 & 阈值过滤
        candidates = []
        for p in patterns:
            score = self.extractor.score_pattern(p)
            if score >= 0.6:
                candidates.append((p, score))

        # Step 3: 演化树操作
        forged = []
        for pattern, score in candidates:
            node = self._create_skill_node(pattern, score)
            self.evolution_tree.archive.nodes[node.id] = node
            forged.append({"name": node.name, "score": score})

        # Step 4: DGM变异 & 交叉
        # TODO: R07 实现完整演化循环

        return {"forged": len(forged), "skills": forged}

    def _load_recent_logs(self, n: int) -> List[str]:
        """加载最近N轮迭代日志"""
        if not self.ITER_LOG_DIR.exists():
            return []
        log_files = sorted(
            self.ITER_LOG_DIR.glob("*迭代*.md"),
            key=lambda p: p.stat().st_mtime, reverse=True
        )
        logs = []
        for f in log_files[:n]:
            try:
                logs.append(f.read_text(encoding='utf-8'))
            except Exception as e:
                logger.warning(f"读取日志失败: {f}, {e}")
        return logs

    def _create_skill_node(self, pattern: dict, score: float) -> SkillNode:
        """从模式创建演化树节点"""
        skill_id = hashlib.md5(
            json.dumps(pattern, sort_keys=True).encode()
        ).hexdigest()[:12]
        return SkillNode(
            id=f"skill_{skill_id}",
            name=pattern.get("name", f"auto_skill_{skill_id}"),
            version="v1.0",
            quality_score=score,
            source_iteration=pattern.get("source", "R06"),
            triggers=pattern.get("triggers", []),
        )

# 模块入口
if __name__ == "__main__":
    sf = SkillForge()
    result = sf.forge_from_logs(n_rounds=5)
    print(json.dumps(result, ensure_ascii=False))

```
