# GEPA + SICA v2.0 三层自进化引擎融合方案

> **融合源**：GEPA (ICLR 2026 Oral) + Reflexion (Princeton/MIT) + HyperAgents DGM-H
> **目标**：豆包SICA进化器从 v1.0 升级为三层循环驱动的 v2.0
> **对标**：Hermes Agent Self-Evolution 5阶段路线图
> **版本**：v2.0 Draft

---

## 一、三层进化循环架构

```
SICA v2.0 = L1(Reflexion快循环) + L2(GEPA中循环) + L3(HyperAgents慢循环)

┌──────────────────────────────────────────────────────────────┐
│ L3: 系统慢循环 (HyperAgents DGM-H) - 周期: 周/月级            │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 跨域迁移 → 元认知自修改 → 统一代码库演化                    │ │
│ │ 触发: 累积100+次GEPA优化后触发元认知审查                    │ │
│ └──────────────────────────────────────────────────────────┘ │
│                          ↑ 向上反馈                           │
├──────────────────────────────────────────────────────────────┤
│ L2: 批次中循环 (GEPA) - 周期: 日/批次级                       │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 轨迹收集 → 反思性变异 → 帕累托选择 → PR审查                │ │
│ │ 触发: 每次任务完成自动收集轨迹，积累50+轨迹触发变异          │ │
│ └──────────────────────────────────────────────────────────┘ │
│                          ↑ 向上反馈                           │
├──────────────────────────────────────────────────────────────┤
│ L1: 运行时快循环 (Reflexion) - 周期: 实时                       │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 任务执行 → 结果评估 → 反思 → 即时修正 → 下次更好            │ │
│ │ 触发: 每次工具调用后自动评估，出错即反思                      │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## 二、L1 Reflexion 快循环（实时层）

```
Reflexion 反思循环伪代码：

def reflexion_loop(task, agent, max_iterations=3):
    memory = []
    
    for i in range(max_iterations):
        # Step 1: 执行
        action, result = agent.act(task, memory)
        
        # Step 2: 评估
        evaluator_prompt = f"""
        评估以下执行结果:
        任务: {task}
        动作: {action}
        结果: {result}
        
        判断:
        1. 是否成功完成?
        2. 是否有错误?
        3. 错误原因是什么?
        4. 下次应该如何改进?
        """
        evaluation = llm.evaluate(evaluator_prompt)
        
        # Step 3: 反思
        if evaluation.is_success:
            # 成功 → 沉淀经验
            memory.append({
                "type": "success",
                "pattern": extract_pattern(action),
                "lesson": evaluation.key_insight
            })
            return result
        else:
            # 失败 → 记录教训 → 重试
            reflection = llm.reflect(f"""
            执行失败。分析:
            动作: {action}
            错误: {evaluation.error}
            原因: {evaluation.root_cause}
            
            提出改进方案:
            """)
            memory.append({
                "type": "failure",
                "error": evaluation.error,
                "root_cause": evaluation.root_cause,
                "improvement": reflection
            })
            task = reflection.modified_task  # 改进后的任务
    
    return None  # 超过最大重试次数
```

**Reflexion 在豆包中的注入点**：

| 注入点 | 触发时机 | 反思内容 |
|--------|---------|---------|
| 工具调用后 | 每次 dispatch_task 返回 | 子Agent是否完成任务? 是否需要重试? |
| 文件操作后 | 每次 write_file/edit_file | 文件是否写入成功? 内容是否正确? |
| 搜索完成后 | web_search/web_fetch 返回 | 信息是否充分? 是否需要补充搜索? |
| 用户反馈后 | 用户纠正/补充 | 为什么理解偏差? 下次如何避免? |

## 三、L2 GEPA 中循环（批次层）

### 3.1 GEPA 核心算法

```
GEPA (Genetic-Pareto Prompt Evolution) 流程：

输入: 当前技能文件 SKILL.md + 执行轨迹集 traces[]
输出: 优化后的技能文件 SKILL_v2.md

步骤:
1. 轨迹解析
   - 读取执行轨迹，识别成功/失败模式
   - 提取工具调用序列、错误类型、恢复策略

2. 反思性变异 (Reflective Mutation)
   - LLM反思：为什么成功? 为什么失败?
   - 生成 5-10 个候选变体
   - 变体类型：步骤重组 / 条件增强 / 错误处理 / 工具优化

3. 帕累托前沿选择 (Pareto Frontier)
   - 在测试集上评估每个候选
   - 多维评分：成功率 / 执行时间 / Token消耗 / 鲁棒性
   - 保留帕累托最优的非支配解集

4. 约束门控 (Constraint Gate)
   - 测试套件 100% 通过
   - 技能文件不超过 15KB
   - 工具描述不超过 500字符
   - 语义不偏离原始目的

5. PR 提交
   - 最佳变体以PR形式提交
   - 人工审查后合并
```

### 3.2 豆包GEPA实现骨架

```python
# gepa_evolver.py - GEPA进化引擎骨架

import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Trace:
    task_id: str
    success: bool
    tool_calls: List[str]
    error_type: str | None
    recovery_actions: List[str]
    execution_time_ms: int
    token_used: int

@dataclass
class Variant:
    skill_text: str
    success_rate: float
    execution_time_ms: int
    token_used: int
    robustness_score: float

class GEPAEngine:
    def __init__(self, skill_path: str, eval_dataset_path: str):
        self.skill_path = skill_path
        self.eval_dataset = self.load_dataset(eval_dataset_path)
        self.traces: List[Trace] = []
    
    def collect_trace(self, trace: Trace):
        """收集执行轨迹"""
        self.traces.append(trace)
    
    def should_evolve(self) -> bool:
        """判断是否触发进化：失败率>20% 或 累积50+轨迹"""
        if len(self.traces) < 50:
            return False
        failure_rate = sum(1 for t in self.traces[-50:] if not t.success) / 50
        return failure_rate > 0.2
    
    def reflective_mutate(self, current_skill: str, traces: List[Trace]) -> List[str]:
        """反思性变异：LLM分析失败原因，生成候选变体"""
        prompt = f"""
你是AI Agent技能优化器。分析以下执行轨迹，优化技能文件。

当前技能:
{current_skill}

执行轨迹 (最近{len(traces)}条):
{self.format_traces(traces)}

请生成5个优化变体，每个变体应针对性解决轨迹中暴露的问题:
1. 分析主要失败模式
2. 对每种失败模式提出改进
3. 生成变体文本

输出JSON格式:
[
  {{"variant_id": 1, "changes": "描述改动", "text": "完整技能文本"}},
  ...
]
"""
        variants_json = llm.generate(prompt)
        variants = json.loads(variants_json)
        return [v["text"] for v in variants]
    
    def pareto_select(self, variants: List[str]) -> List[Variant]:
        """帕累托前沿选择：多维评分保留非支配解"""
        evaluated = []
        for v_text in variants:
            scores = self.evaluate(v_text, self.eval_dataset)
            evaluated.append(Variant(
                skill_text=v_text,
                success_rate=scores["success_rate"],
                execution_time_ms=scores["execution_time"],
                token_used=scores["token_used"],
                robustness_score=scores["robustness"]
            ))
        
        # 帕累托前沿：不被任何其他候选在所有维度上超越
        pareto_optimal = []
        for i, v in enumerate(evaluated):
            dominated = False
            for j, other in enumerate(evaluated):
                if i == j:
                    continue
                if (other.success_rate >= v.success_rate and
                    other.robustness_score >= v.robustness_score and
                    other.execution_time_ms <= v.execution_time_ms and
                    other.token_used <= v.token_used and
                    (other.success_rate > v.success_rate or
                     other.robustness_score > v.robustness_score or
                     other.execution_time_ms < v.execution_time_ms or
                     other.token_used < v.token_used)):
                    dominated = True
                    break
            if not dominated:
                pareto_optimal.append(v)
        
        return pareto_optimal
```

### 3.3 五阶段实施路线

| 阶段 | 进化对象 | 难度 | 预计轮次 | Hermes对标 |
|------|---------|------|---------|-----------|
| Phase 1 | SKILL.md 技能文件 | ⭐⭐ | R08-R10 | ✅ 已实现 |
| Phase 2 | 工具描述 (tool descriptions) | ⭐⭐⭐ | R11-R13 | 🔧 计划中 |
| Phase 3 | 系统提示 (system prompt) | ⭐⭐⭐⭐ | R14-R16 | 🔧 计划中 |
| Phase 4 | 工具实现代码 (tool code) | ⭐⭐⭐⭐⭐ | R17-R19 | 🔧 计划中 |
| Phase 5 | 持续改进流水线 (CI/CD) | ⭐⭐⭐ | R20+ | 📋 计划中 |

## 四、L3 HyperAgents 慢循环（系统层）

```
HyperAgents DGM-H 三层循环在豆包中的映射：

DGM-H Layer 1: 任务层适应 (已实现 ✓)
  → 对应 SICA L1 Reflexion + L2 GEPA
  → 单任务内优化 + 批次进化

DGM-H Layer 2: 领域层迁移 (待实现 📋)
  → 跨领域能力泛化
  → 例如：文件操作优化经验 → 迁移到代码生成
  → 触发条件：某领域进化饱和（连续3轮无提升）

DGM-H Layer 3: 架构层自修改 (远期 🔮)
  → 元认知审查：当前架构是否合理？
  → 自动重构 Skills 组织方式
  → 统一代码库演化
  → 触发条件：累积100+次GEPA优化后触发
```

---

## 五、与Hermes对标差距

| 特性 | Hermes Agent | 豆包 SICA v2.0 | 差距 |
|------|-------------|---------------|------|
| 运行时技能生成 | ✅ 自动（5+工具调用/纠错后触发） | 🔧 L1 Reflexion中实现 | 小 |
| 离线批量进化 | ✅ GEPA + DSPy + PR审查 | 📋 L2 GEPA骨架设计完成 | 中 |
| 技能渐进加载 | ✅ 四层渐进（Tier 0-3） | 📋 待GenericAgent实现 | 小 |
| GEPA所有Phase | 🔧 Phase 1完成，Phase 2-5计划 | 📋 Phase 1骨架待编码 | 大 |
| 自进化流水线 | ✅ hermes-agent-self-evolution 独立仓库 | 📋 Phase 5计划 | 大 |
| Atropos RL训练 | ✅ 批量轨迹生成+RL训练 | 📋 未规划 | 大 |

---

> 创建时间：2026-05-31 17:00
> 状态：设计完成 · Phase 1 骨架代码待实现