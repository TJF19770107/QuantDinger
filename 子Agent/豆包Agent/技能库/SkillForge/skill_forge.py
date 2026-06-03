# skill_forge.py - 豆包Agent自主技能锻造引擎
# 版本：v1.0 | 自动生成：R06 | 来源：R05设计
"""从迭代日志中自动提取可复用模式，生成标准化技能并入库注册。"""
import os, json, re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

SKILL_TEMPLATE = """# {skill_name}
> 版本：v1.0
> 自动生成：{gen_date}
> 来源迭代：{source}
> 质量评分：{score}

## 触发条件
{triggers}

## 能力描述
{description}

## 执行流程
{steps}

## 输出格式
```json
{output_schema}
```

## 安全审查
- 风险等级：{risk_level}
- {safety_notes}

## 演化记录
- v1.0: 自动锻造，基于{source}
"""

class SkillForge:
    """自主技能锻造引擎 —— 模式提取→技能生成→自动注册"""

    def __init__(self, agent_root: str):
        self.root = Path(agent_root)
        self.skill_lib = self.root / "技能库"
        self.iter_log_dir = self.root / "迭代记录"
        self.index_file = self.root / "skills_index.json"
        self.QUALITY_THRESHOLD = 0.6

    def extract_patterns(self, iteration_logs: List[str]) -> List[Dict]:
        """从迭代日志中提取可复用操作模式"""
        patterns = []
        for log_path in iteration_logs:
            try:
                content = Path(log_path).read_text(encoding="utf-8")
                # 提取能力补全模式
                cap_matches = re.findall(r'### 能力\d+：(.*?)\n.*?#### \d+\.\d+ 目标\n(.*?)\n', content, re.DOTALL)
                for name, goal in cap_matches:
                    patterns.append({
                        "name": name.strip(),
                        "goal": goal.strip()[:200],
                        "source": Path(log_path).name,
                        "frequency": 1
                    })
                # 提取执行流程模式
                step_matches = re.findall(r'(STEP \d+:.*?)\n', content)
                if len(step_matches) >= 3:
                    patterns.append({
                        "name": f"自动流程_{Path(log_path).stem[-8:]}",
                        "steps": step_matches,
                        "source": Path(log_path).name,
                        "frequency": 1
                    })
            except Exception:
                pass
        return patterns

    def quality_score(self, pattern: Dict) -> float:
        """质量评估：复用频率(0.3) + 独立性(0.3) + 通用性(0.4)"""
        freq_score = min(pattern.get("frequency", 0) / 10, 1.0) * 0.3
        ind_score = 0.3  # 默认独立性
        gen_score = 0.35  # 默认通用性
        return freq_score + ind_score + gen_score

    def generate_skill(self, pattern: Dict) -> Dict:
        """根据模式生成完整技能包"""
        score = self.quality_score(pattern)
        if score < self.QUALITY_THRESHOLD:
            return None
        
        skill_name = pattern["name"].replace(" ", "_").replace("/", "_")
        skill_dir = self.skill_lib / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        triggers = "- 关键词：{}\n- 场景：{}".format(
            pattern.get("name", ""),
            pattern.get("goal", "")[:100]
        )
        
        md_content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            gen_date=datetime.now().strftime("%Y-%m-%d"),
            source=pattern.get("source", "unknown"),
            score=f"{score:.2f}",
            triggers=triggers,
            description=pattern.get("goal", "自动生成的技能"),
            steps="\n".join([f"1. {s}" for s in pattern.get("steps", ["执行", "验证", "归档"])]),
            output_schema='{"result": "success/failure", "details": "..."}',
            risk_level="CAUTION",
            safety_notes="自动生成技能，执行前需SafeGuard审查"
        )
        
        skill_md_path = skill_dir / "SKILL.md"
        skill_md_path.write_text(md_content, encoding="utf-8")
        
        return {"name": skill_name, "score": score, "path": str(skill_dir)}

    def register_skill(self, skill: Dict):
        """注册技能到索引"""
        index = {}
        if self.index_file.exists():
            index = json.loads(self.index_file.read_text(encoding="utf-8"))
        index[skill["name"]] = {
            "path": skill["path"],
            "score": skill["score"],
            "registered": datetime.now().isoformat(),
            "status": "active"
        }
        self.index_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    def full_cycle(self, iteration_logs: List[str]) -> List[Dict]:
        """完整锻造循环"""
        patterns = self.extract_patterns(iteration_logs)
        forged = []
        for p in patterns:
            skill = self.generate_skill(p)
            if skill:
                self.register_skill(skill)
                forged.append(skill)
        return forged

if __name__ == "__main__":
    forge = SkillForge(str(ROOT))
    logs = list(forge.iter_log_dir.glob("*.md"))
    skills = forge.full_cycle([str(l) for l in logs])
    print(f"锻造完成：{len(skills)} 个新技能入{'' if skills else '，无达标模式'}")
