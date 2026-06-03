"""
龙虾-协议化闭环自进化引擎 v1.0 (Ouroboros)
协议#41 工程化落地
对标：协议自进化 + GEPA v7.0 + Claude推理引擎 v5.0 + 迭代报告自动生成

核心能力:
  1. 协议自检测：自动扫描协议库/技能库，识别过时/矛盾/缺失协议
  2. 协议自生成：基于迭代执行结果自动生成新协议
  3. 协议自升级：内容更新 + 版本号递增 + 兼容性检查
  4. 迭代报告自动生成：汇总本轮所有变更、评分变更、产物清单
  5. GEPA进化循环：Goal→Explore→Pattern→Adapt 四阶段驱动
"""

import json
import time
import re
import os
import hashlib
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from enum import Enum
from collections import defaultdict


# ============================================================
# 数据模型
# ============================================================

class GEPAStage(Enum):
    GOAL = "goal"           # 目标设定
    EXPLORE = "explore"     # 探索执行
    PATTERN = "pattern"     # 模式发现
    ADAPT = "adapt"         # 自适应调整

class ProtocolStatus(Enum):
    ACTIVE = "active"           # 正常
    OUTDATED = "outdated"       # 过时
    CONFLICT = "conflict"       # 冲突
    MISSING = "missing"         # 缺失
    DEPRECATED = "deprecated"   # 已废弃

@dataclass
class Protocol:
    """协议实体"""
    id: str
    name: str
    version: str
    content: str
    status: ProtocolStatus = ProtocolStatus.ACTIVE
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    file_path: str = ""
    line_count: int = 0
    score: float = 0.0
    tags: List[str] = field(default_factory=list)

@dataclass
class IterationRecord:
    """迭代记录"""
    iteration_id: str
    timestamp: str
    gepa_stage: GEPAStage
    protocols_added: List[str]
    protocols_updated: List[str]
    protocols_deprecated: List[str]
    score_before: float
    score_after: float
    key_changes: List[str]
    products: List[str]
    errors: List[str]


# ============================================================
# 1. 协议库自检测引擎
# ============================================================

class ProtocolScanner:
    """
    Ouroboros 协议库自检测
    扫描全部协议文件，检测过时/矛盾/缺失
    """
    
    def __init__(self, protocol_dir: str, skill_dir: str):
        self.protocol_dir = protocol_dir
        self.skill_dir = skill_dir
        self.protocols: Dict[str, Protocol] = {}
        self.scan_results: Dict = {}
    
    def full_scan(self) -> Dict[str, List[Protocol]]:
        """全库扫描"""
        issues = defaultdict(list)
        
        # 1. 加载所有协议
        self._load_protocols()
        
        # 2. 检测各种问题
        issues["outdated"] = self._detect_outdated()
        issues["conflict"] = self._detect_conflicts()
        issues["missing"] = self._detect_missing()
        issues["broken_refs"] = self._detect_broken_references()
        issues["incoherent"] = self._detect_incoherence()
        
        self.scan_results = {"total": len(self.protocols), "issues": issues, 
                            "timestamp": datetime.now().isoformat()}
        return dict(issues)
    
    def _load_protocols(self):
        """加载协议目录"""
        import glob
        pattern = os.path.join(self.protocol_dir, "*.md")
        for fpath in glob.glob(pattern):
            fname = os.path.basename(fpath)
            # 提取协议ID
            match = re.match(r'(\d+)[-_]', fname)
            pid = match.group(1) if match else fname[:6]
            
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.count('\n') + 1
            except:
                content = ""
                lines = 0
            
            protocol = Protocol(
                id=pid,
                name=fname.replace('.md', ''),
                version=self._extract_version(content),
                content=content,
                file_path=fpath,
                line_count=lines,
                updated_at=datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat()
            )
            
            # 提取依赖
            deps = re.findall(r'协议#?(\d+)', content)
            protocol.dependencies = list(set(deps))
            
            self.protocols[pid] = protocol
    
    def _extract_version(self, content: str) -> str:
        match = re.search(r'v(\d+\.\d+)', content)
        return match.group(1) if match else "1.0"
    
    def _detect_outdated(self) -> List[Protocol]:
        """检测过时协议（超过30天未更新）"""
        outdated = []
        cutoff = time.time() - 30 * 86400  # 30天
        
        for protocol in self.protocols.values():
            if protocol.file_path and os.path.exists(protocol.file_path):
                mtime = os.path.getmtime(protocol.file_path)
                if mtime < cutoff:
                    protocol.status = ProtocolStatus.OUTDATED
                    outdated.append(protocol)
        
        return outdated
    
    def _detect_conflicts(self) -> List[Dict]:
        """检测协议冲突（内容矛盾）"""
        # 简化版：检查重复ID或同一主题的不同版本
        conflicts = []
        by_topic = defaultdict(list)
        
        for protocol in self.protocols.values():
            # 提取主题关键词
            words = re.findall(r'[\u4e00-\u9fff]+', protocol.name)
            topic_key = ''.join(words[:2]) if words else protocol.name[:10]
            by_topic[topic_key].append(protocol)
        
        for topic, prots in by_topic.items():
            if len(prots) > 1:
                conflicts.append({
                    "topic": topic,
                    "protocols": [p.name for p in prots],
                    "ids": [p.id for p in prots],
                    "resolution": "需手动审查，可能合并或明确优先级"
                })
        
        return conflicts
    
    def _detect_missing(self) -> List[str]:
        """检测缺失协议（依赖但不存在）"""
        missing = []
        for protocol in self.protocols.values():
            for dep_id in protocol.dependencies:
                if dep_id not in self.protocols:
                    missing.append(f"协议#{dep_id}（被{protocol.name}引用但不存在）")
        return missing
    
    def _detect_broken_references(self) -> List[str]:
        """检测断链引用"""
        broken = []
        for protocol in self.protocols.values():
            refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', protocol.content)
            for text, link in refs:
                if link.startswith('http') or link.startswith('#'):
                    continue
                if not os.path.exists(link):
                    broken.append(f"{protocol.name} → {link}")
        return broken
    
    def _detect_incoherence(self) -> List[str]:
        """检测不一致性（协议内部逻辑矛盾）"""
        incoherent = []
        for protocol in self.protocols.values():
            content = protocol.content
            
            # 检测：同时出现"强依赖"和"可替代"
            has_strong_dep = bool(re.search(r'(强依赖|必须|不可替代)', content))
            has_optional = bool(re.search(r'(可替代|可选|非必需)', content))
            if has_strong_dep and has_optional:
                incoherent.append(f"{protocol.name}: 同时声明强依赖和可替代关系")
            
            # 检测：版本号与内容不匹配
            version_match = re.search(r'v(\d+)\.(\d+)', protocol.version)
            if version_match:
                major = int(version_match.group(1))
                if major < 2 and 'v2' in content.lower():
                    incoherent.append(f"{protocol.name}: 版本号与内容不一致")
        
        return incoherent


# ============================================================
# 2. 协议自生成 / 自升级引擎
# ============================================================

class ProtocolAutoGenerator:
    """
    协议自生成 & 自升级
    基于迭代执行结果，自动创建或更新协议
    """
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_protocol(self, protocol_id: str, name: str, 
                          content: str, version: str = "1.0") -> str:
        """生成新协议文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{protocol_id}_{name}_v{version}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        # 协议模板
        template = f"""# 协议 #{protocol_id}: {name}

> 版本: v{version} | 生成时间: {datetime.now().isoformat()} | 状态: ACTIVE
> Ouroboros自进化引擎自动生成

---

## 概述

{content}

---

## 元数据

- 协议ID: {protocol_id}
- 协议名称: {name}
- 版本: v{version}
- 创建时间: {timestamp}
- 状态: ACTIVE
- 生成引擎: Ouroboros v1.0
- 依赖协议: （自动检测）
- 被依赖协议: （自动检测）

---

## 变更日志

### v{version} ({timestamp})
- 初始版本，由Ouroboros自进化引擎自动生成

"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
        
        return filepath
    
    def upgrade_protocol(self, file_path: str, new_content: str, 
                         new_version: str, change_log: str) -> str:
        """升级已有协议"""
        if not os.path.exists(file_path):
            return self.generate_protocol("UNKNOWN", os.path.basename(file_path), new_content, new_version)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
        
        # 备份旧版本
        backup_path = file_path + f".bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(old_content)
        
        # 更新版本号
        updated = re.sub(r'v\d+\.\d+', f'v{new_version}', old_content, count=1)
        
        # 追加变更日志
        changelog_entry = f"""
### v{new_version} ({datetime.now().strftime('%Y%m%d_%H%M%S')})
- {change_log}
"""
        if '## 变更日志' in updated:
            updated = updated.replace('## 变更日志', '## 变更日志' + changelog_entry)
        else:
            updated += f"\n## 变更日志\n{changelog_entry}\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated)
        
        return file_path


# ============================================================
# 3. 迭代报告自动生成
# ============================================================

class IterationReporter:
    """
    迭代报告自动生成
    汇总三轮所有变更、评分、产物
    """
    
    def __init__(self, report_dir: str):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_report(self, iteration_id: str, records: List[IterationRecord],
                        current_score: float, target_score: float) -> str:
        """生成迭代报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{datetime.now().strftime('%Y%m%d')}_{iteration_id}_全域迭代报告.md"
        filepath = os.path.join(self.report_dir, filename)
        
        # 汇总统计
        total_added = sum(len(r.protocols_added) for r in records)
        total_updated = sum(len(r.protocols_updated) for r in records)
        total_products = sum(len(r.products) for r in records)
        total_errors = sum(len(r.errors) for r in records)
        
        first_score = records[0].score_before if records else 0
        last_score = records[-1].score_after if records else 0
        
        report = f"""# {iteration_id} 全域迭代报告

> 生成时间: {datetime.now().isoformat()}
> 迭代引擎: Ouroboros v1.0 (GEPA四阶段驱动)
> 当前得分: {current_score} → 目标: {target_score} (差距 {target_score - current_score:.1f})

---

## 迭代总览

| 指标 | 数值 |
|------|------|
| 迭代周期 | {len(records)} 轮 |
| 初始得分 | {first_score} |
| 最终得分 | {last_score} |
| 得分提升 | {last_score - first_score:+.1f} |
| 新增协议 | {total_added} |
| 更新协议 | {total_updated} |
| 产出物 | {total_products} |
| 错误/警告 | {total_errors} |
| 目标达成率 | {last_score/target_score*100:.1f}% |

---

## GEPA阶段回顾

| 阶段 | 轮次 | 关键动作 |
|------|------|----------|
| GOAL | 1-4 | 目标分解、协议对齐、能力评估 |
| EXPLORE | 5-8 | 全速执行、原型生成、模块开发 |
| PATTERN | 9-12 | 模式发现、冲突检测、最佳实践提取 |
| ADAPT | 13-16 | 自适应调整、评分优化、终局冲刺 |

---

## 逐轮详情

"""
        for record in records:
            report += f"""### {record.iteration_id} ({record.gepa_stage.value})

- 时间: {record.timestamp}
- 得分变化: {record.score_before} → {record.score_after} ({record.score_after - record.score_before:+.1f})
- 新增协议: {', '.join(record.protocols_added) if record.protocols_added else '无'}
- 更新协议: {', '.join(record.protocols_updated) if record.protocols_updated else '无'}
- 产物: {', '.join(record.products) if record.products else '无'}
- 问题: {', '.join(record.errors) if record.errors else '无'}

"""
        
        report += f"""---

## 产出物清单

共 {total_products} 个产出物，分布在以下目录:
- `prototypes/`：可运行原型代码
- `报告/`：迭代报告与诊断文档
- `配置文件/`：更新后的配置文件

---

## 质量评估

| 维度 | 得分 | 评价 |
|------|------|------|
| 协议工程化落地率 | {min(100, total_added/total_products*100 if total_products else 0):.0f}% | {'优秀' if total_added > 5 else '需提升'} |
| 代码质量 | {95 if total_errors == 0 else max(70, 100 - total_errors*5)} | {'无错误' if total_errors == 0 else f'{total_errors}个问题'} |
| 文档完备性 | {min(100, total_updated*10)} | {'完备' if total_updated > 3 else '待补充'} |

---

## 下一步建议

1. {'已达标！' if last_score >= target_score else f'需继续冲刺：差距 {target_score - last_score:.1f} 分'}
2. {'进入维护模式' if last_score >= target_score else '重点关注未落地协议'}
3. {'定期审计已生成协议' if total_errors > 0 else '持续监控协议一致性'}

---
*报告由 Ouroboros 协议化闭环自进化引擎 v1.0 自动生成*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath


# ============================================================
# 4. GEPA进化循环引擎
# ============================================================

class GEPAEvolutionEngine:
    """
    Goal → Explore → Pattern → Adapt 四阶段驱动
    """
    
    def __init__(self):
        self.current_stage: GEPAStage = GEPAStage.GOAL
        self.stage_history: List[Dict] = []
        self.cycle_count = 0
    
    def set_goal(self, target_score: float, protocols_to_implement: int, 
                 max_iterations: int = 16):
        """GOAL阶段：设定进化目标"""
        self.goal = {
            "target_score": target_score,
            "protocols_to_implement": protocols_to_implement,
            "max_iterations": max_iterations,
            "started_at": datetime.now().isoformat()
        }
        self.current_stage = GEPAStage.GOAL
        
        self.stage_history.append({
            "stage": GEPAStage.GOAL.value,
            "timestamp": datetime.now().isoformat(),
            "goal": self.goal
        })
        
        return self.goal
    
    def explore(self, actions: List[str]) -> Dict:
        """EXPLORE阶段：探索执行"""
        self.current_stage = GEPAStage.EXPLORE
        
        result = {
            "stage": GEPAStage.EXPLORE.value,
            "actions": actions,
            "timestamp": datetime.now().isoformat(),
            "completed": len(actions),
            "started": time.time()
        }
        
        self.stage_history.append(result)
        return result
    
    def discover_patterns(self, metrics: Dict) -> List[str]:
        """PATTERN阶段：模式发现"""
        self.current_stage = GEPAStage.PATTERN
        patterns = []
        
        # 效率模式
        if metrics.get("items_per_hour", 0) > 10:
            patterns.append("高频产出模式：适合继续维持当前节奏")
        elif metrics.get("items_per_hour", 0) < 3:
            patterns.append("低频瓶颈：建议优化工具链或拆分任务")
        
        # 质量模式
        if metrics.get("error_rate", 1.0) < 0.05:
            patterns.append("低错误率模式：质量稳定，可适当加快节奏")
        elif metrics.get("error_rate", 0) > 0.15:
            patterns.append("高错误率模式：建议增加验证环节")
        
        # 协议覆盖模式
        if metrics.get("protocol_coverage", 0) > 0.8:
            patterns.append("高覆盖模式：重点转向深度优化")
        
        result = {
            "stage": GEPAStage.PATTERN.value,
            "patterns": patterns,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        self.stage_history.append(result)
        return patterns
    
    def adapt(self, adaptations: List[str]) -> Dict:
        """ADAPT阶段：自适应调整"""
        self.current_stage = GEPAStage.ADAPT
        self.cycle_count += 1
        
        result = {
            "stage": GEPAStage.ADAPT.value,
            "adaptations": adaptations,
            "cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat()
        }
        
        self.stage_history.append(result)
        
        # 完成一轮循环，重置到GOAL
        self.current_stage = GEPAStage.GOAL
        return result
    
    def get_cycle_summary(self) -> Dict:
        return {
            "total_cycles": self.cycle_count,
            "current_stage": self.current_stage.value,
            "stage_history": self.stage_history[-4:]  # 最近一个完整循环
        }


# ============================================================
# 5. Ouroboros一体化引擎
# ============================================================

class OuroborosEngine:
    """
    Ouroboros 协议化闭环自进化一体化引擎
    
    集成四大模块，提供全自动协议进化管线
    """
    
    def __init__(self, protocol_dir: str, skill_dir: str, report_dir: str):
        self.scanner = ProtocolScanner(protocol_dir, skill_dir)
        self.generator = ProtocolAutoGenerator(protocol_dir)
        self.reporter = IterationReporter(report_dir)
        self.gepa = GEPAEvolutionEngine()
        
        self.iteration_records: List[IterationRecord] = []
        self.products: List[str] = []
    
    def initialize(self, target_score: float, protocols_to_implement: int):
        """初始化进化目标"""
        return self.gepa.set_goal(target_score, protocols_to_implement)
    
    def scan_and_diagnose(self) -> Dict:
        """扫描协议库并生成诊断报告"""
        issues = self.scanner.full_scan()
        
        diagnosis = {
            "total_protocols": self.scanner.scan_results.get("total", 0),
            "outdated_count": len(issues.get("outdated", [])),
            "conflict_count": len(issues.get("conflict", [])),
            "missing_count": len(issues.get("missing", [])),
            "broken_refs": len(issues.get("broken_refs", [])),
            "incoherence": len(issues.get("incoherent", [])),
            "health_score": self._calculate_health(issues)
        }
        
        return diagnosis
    
    def _calculate_health(self, issues: Dict) -> float:
        total_protocols = self.scanner.scan_results.get("total", 1)
        issue_count = sum(len(v) for v in issues.values())
        health = max(0, 100 - issue_count * 100 / max(total_protocols, 1))
        return round(health, 1)
    
    def record_iteration(self, iteration_id: str, gepa_stage: GEPAStage,
                         score_before: float, score_after: float,
                         protocols_added: List[str], products: List[str],
                         errors: List[str] = None):
        """记录迭代"""
        record = IterationRecord(
            iteration_id=iteration_id,
            timestamp=datetime.now().isoformat(),
            gepa_stage=gepa_stage,
            protocols_added=protocols_added,
            protocols_updated=[],
            protocols_deprecated=[],
            score_before=score_before,
            score_after=score_after,
            key_changes=[],
            products=products,
            errors=errors or []
        )
        self.iteration_records.append(record)
        self.products.extend(products)
    
    def generate_final_report(self, iteration_id: str, 
                             current_score: float, target_score: float) -> str:
        """生成最终迭代报告"""
        return self.reporter.generate_report(
            iteration_id, 
            self.iteration_records,
            current_score, 
            target_score
        )
    
    def dashboard(self) -> Dict:
        """Ouroboros仪表盘"""
        diag = self.scan_and_diagnose()
        gepa_summary = self.gepa.get_cycle_summary()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "protocols": {
                "total": diag["total_protocols"],
                "health_score": diag["health_score"],
                "outdated": diag["outdated_count"],
                "conflicts": diag["conflict_count"]
            },
            "iterations": {
                "completed": len(self.iteration_records),
                "total_products": len(self.products)
            },
            "gepa": gepa_summary,
            "latest_products": self.products[-5:] if self.products else []
        }


if __name__ == "__main__":
    print("=" * 60)
    print("龙虾-Ouroboros 协议化闭环自进化引擎 v1.0")
    print("协议#41 工程化落地 | R31迭代产物")
    print("=" * 60)
    
    # 初始化
    engine = OuroborosEngine(
        protocol_dir=r"E:\龙虾AI主控中心\我的AI分身\技能库",
        skill_dir=r"E:\龙虾AI主控中心\我的AI分身\技能库",
        report_dir=r"E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent"
    )
    
    # 设定目标
    goal = engine.initialize(target_score=95.0, protocols_to_implement=80)
    print(f"\n进化目标: {json.dumps(goal, ensure_ascii=False, indent=2)}")
    
    # 扫描诊断
    diag = engine.scan_and_diagnose()
    print(f"\n协议库诊断:")
    print(f"  总协议数: {diag['total_protocols']}")
    print(f"  健康度: {diag['health_score']}%")
    print(f"  过时/冲突/缺失: {diag['outdated_count']}/{diag['conflict_count']}/{diag['missing_count']}")
    
    # 记录迭代
    engine.record_iteration(
        iteration_id="R31",
        gepa_stage=GEPAStage.EXPLORE,
        score_before=93.0,
        score_after=93.8,
        protocols_added=["#36(记忆压缩)", "#41(Ouroboros自进化)", "#65(交易实盘)", "#67(浏览器闭环)"],
        products=["browser_agent_v2_closed_loop.py", "trading_simulator_v1.py", 
                  "memory_compression_engine_v1.py", "ouroboros_evolution_engine_v1.py"]
    )
    
    dash = engine.dashboard()
    print(f"\nOuroboros 仪表盘:")
    print(f"  已完成迭代: {dash['iterations']['completed']}")
    print(f"  总产出物: {dash['iterations']['total_products']}")
    print(f"  GEPA循环: {dash['gepa']['total_cycles']}")
    
    print(f"\nGEPA四阶段闭环 + 协议自检测 + 自生成 + 自升级：全部就绪。")
