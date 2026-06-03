# 龙虾-Rubric自纠正复盘协议 v1.0

> **对标来源**：Claude Managed Agents Outcomes (2026-05-06)
> **版本**：v1.0
> **状态**：ACTIVE
> **所属模块**：Claude推理引擎 → Phase 5 结果复盘
> **创建**：2026-05-31 R07

---

## 一、协议目标

将Claude Managed Agents的Outcomes Rubric-Graded自纠正循环融入豆包Agent推理引擎的"结果复盘"阶段，从简单的质量验证升级为结构化Rubric驱动的多轮自纠正，确保输出质量达标。

---

## 二、Rubric定义规范

### 2.1 Rubric结构

```json
{
  "rubric_id": "report_quality_v1",
  "criteria": [
    {
      "id": "C1",
      "name": "事实准确",
      "description": "所有数据/引用可追溯到来源",
      "weight": 0.40,
      "scoring": { "type": "0-1_continuous" }
    },
    {
      "id": "C2",
      "name": "结构完整",
      "description": "包含摘要/正文/结论三段式",
      "weight": 0.30,
      "scoring": { "type": "boolean" }
    },
    {
      "id": "C3",
      "name": "语言规范",
      "description": "无语法错误/专业术语正确/格式统一",
      "weight": 0.30,
      "scoring": { "type": "0-1_continuous" }
    }
  ],
  "passing_score": 0.80,
  "max_attempts": 3,
  "grader_model": "lightweight"
}
```

### 2.2 评分类型

| 评分类型 | 说明 | 适用场景 |
|---------|------|---------|
| boolean | 通过/不通过（0或1） | 格式检查、结构完整性 |
| 0-1_continuous | 0到1连续评分 | 质量维度、准确性 |
| 1-5_likert | 1~5分李克特量表 | 主观评价维度 |
| custom | 自定义评分函数 | 特殊业务逻辑 |

---

## 三、Grader独立评审机制

### 3.1 独立上下文窗口

Grader在**独立上下文窗口**中运行，不共享Agent的执行历史。关键设计：

- Grader只看到：任务要求 + 输出内容 + Rubric定义
- Grader看不到：Agent的内部推理链、中间步骤
- 目的：消除"盲点共享"，避免Agent自评时的确认偏误

### 3.2 反馈结构

```json
{
  "attempt": 2,
  "total_score": 0.72,
  "passed": false,
  "criterion_scores": {
    "C1": { "score": 0.85, "passed": true },
    "C2": { "score": 1.0, "passed": true },
    "C3": { "score": 0.45, "passed": false }
  },
  "feedback": {
    "C3": "第3段存在2处术语混用（'Agent'/'智能体'交替），第5段有1处主谓不一致。建议统一术语并修正语法。"
  }
}
```

---

## 四、自纠正循环

### 4.1 循环流程

```
Agent输出 → Grader评分
                │
        ┌───────┴───────┐
        │               │
    score ≥ 0.80    score < 0.80
        │               │
        ▼               ▼
    通过，输出      Grader反馈 → Agent修正 → 重新评分
                                        │
                                ┌───────┴───────┐
                                │               │
                          score ≥ 0.80    score < 0.80
                                │          attempt < 3?
                                │               │
                                ▼          ┌────┴────┐
                            通过，输出    是：继续  否：熔断
                                         修正      输出+警告
```

### 4.2 收敛判据

| 条件 | 动作 |
|------|------|
| 连续2轮分数无提升 | 停止迭代，输出当前最优 |
| 单维度始终不通过 | 标记该维度为"已知限制" |
| attempt耗尽 | 输出+标注未达标维度 |
| 单轮修正耗时 > 60s | 触发超时熔断 |

---

## 五、成本控制

### 5.1 Grader模型策略

| 场景 | Grader模型 | 理由 |
|------|-----------|------|
| 简单格式检查 | 轻量模型 | Rubric简单，无需深度理解 |
| 内容质量审查 | 中等模型 | 需要语义理解 |
| 安全合规审查 | 高性能模型 | 不可出错 |

### 5.2 成本公式

```
总成本 = Agent执行成本 + Grader评分成本 × (1 + 重试次数)
```

建议：复杂度高的任务用高性能Agent+轻量Grader（Grader只做格式/结构检查），简单任务反之。

---

## 六、集成到推理引擎

增强Phase 5"结果复盘"：

```
原有: 输出 → 简单质量验证 → 完成

R07: 输出 → Grader Rubric评分
                │
        ┌───────┴───────┐
        │               │
      通过           不通过
        │               │
        ▼               ▼
    复盘报告       结构化反馈注入
                    → Agent修正
                    → 重新评分(最多3轮)
                    → 复盘报告(含评分历程)
```

---

> 版本：v1.0 (R07)
> 下一版本：v2.0 Grader模型自适应选择 + Rubric自动生成
