# 龙虾-SkillOpt文本空间技能优化协议 v1.0

> **版本**：v1.0（R45 · 2026-06-02）
> **对标来源**：Microsoft Research SkillOpt（arXiv:2605.23904 / GitHub 3.3K Stars）
> **核心价值**：技能=可训练参数 · 文本空间优化 · 52/52全优
> **依赖**：协议#21 CASCADE双元技能 · 协议#38 技能全生命周期 · 协议#73 MUSE五阶段

---

## 一、核心洞察

**技能文档就是冻结Agent的"外部权重"**。内部权重用梯度下降优化，外部权重（技能文档）也应该有一套系统化的训练方法。

当前技能进化的三条路径：
| 路径 | 问题 |
|------|------|
| 手工编写 | 脆弱、不可扩展 |
| 一次性LLM生成 | 无迭代保证 |
| 无约束自我修订 | 越改越差（无验证门控） |

SkillOpt的解决路径：给技能文档一整套与权重空间优化对等的训练机制——**有证据、有步骤、有验证、有负反馈**。

---

## 二、五组件训练闭环

```
Rollout → Reflection → Bounded Edit → Validation Gate → Export
  ↑                                                      |
  └──────────────── 循环直到收敛 ←────────────────────────┘
```

### 2.1 Rollout（采样轨迹）≈ Forward Pass

- 冻结的目标模型拿着当前版本技能文档执行一批任务
- 记录完整执行轨迹：消息、工具调用、验证反馈、最终得分
- 产出"证据"，相当于神经网络前向传播结果

### 2.2 Reflection（分析成败）≈ Backward Pass

- 独立优化器模型分析执行轨迹
- 识别成功模式 vs 失败根因
- Minibatch reflection：分批处理轨迹，避免单条偏差

### 2.3 Bounded Edit（有界编辑）≈ Parameter Update

- 基于Reflection分析结果提出技能文档修改
- **文本编辑预算（cosine schedule）**：限制每次修改的字符数，防止无约束重写
- 编辑预算随训练递减（cosine衰减），早期大改、后期微调

### 2.4 Validation Gate（验证门控）≈ Early Stopping

- 保留验证集：候选技能 vs 当前最佳技能
- 候选低于基线 → 拒绝更新 → 保持当前最佳
- 防止"越训越差"的技能退化

### 2.5 Export（导出最佳）≈ Model Checkpoint

- 训练结束后导出验证集得分最高的技能版本
- 300-2000 token的最佳技能文档
- 可部署到任意Agent运行时

---

## 三、与深度学习对等映射

| 深度学习 | SkillOpt |
|---------|----------|
| Forward Pass | Rollout batch 采样轨迹 |
| Backward Pass | Minibatch reflection 分析成功/失败 |
| Parameter Update | Bounded Edit 文本编辑 |
| Learning Rate | 文本编辑预算（cosine schedule） |
| Validation Loss | 验证集性能得分 |
| Early Stopping | Validation Gate 拒绝退化 |
| Model Checkpoint | Export 导出最佳技能 |

---

## 四、52/52全优战绩

| 目标模型 | 基准测试 | 执行环境 | 结果 |
|---------|---------|---------|------|
| GPT-5.5 | 6个benchmark | Direct Chat | +23.5分 |
| GPT-5.5 | 6个benchmark | Codex | +24.8分 |
| GPT-5.5 | 6个benchmark | Claude Code | +19.1分 |
| Qwen3.5-4B | 6个benchmark | 3种Harness | 全最优/并列最优 |
| 其他5个模型 | 6个benchmark | 3种Harness | 全最优/并列最优 |

**结论**：7个目标模型×6个基准×3种执行环境 = **52/52全部组合取得最优或并列最优**。

---

## 五、防退化机制

| 机制 | 作用 |
|------|------|
| 文本编辑预算（cosine衰减） | 防止一次性大改破坏已有能力 |
| Validation Gate | 验证集得分低于基线时拒绝更新 |
| 冻结目标模型 | 只有技能文档可变，模型权重不动 |
| 独立优化器模型 | 分析者≠执行者，避免自我欺骗 |

---

## 六、部署流程

```
1. 初始化 best_skill.md（人工编写或LLM生成初始版本）
2. 配置训练参数：
   - 目标模型（冻结）
   - 优化器模型
   - 验证集任务列表
   - 编辑预算初始值 & cosine衰减率
   - 最大训练轮次
3. 启动训练循环：
   for epoch in range(max_epochs):
       rollout_results = rollout(target_model, best_skill, val_tasks)
       reflection = reflect(optimizer_model, rollout_results)
       candidate_skill = bounded_edit(optimizer_model, best_skill, reflection, budget)
       if validate(target_model, candidate_skill) > validate(target_model, best_skill):
           best_skill = candidate_skill
       budget *= cosine_decay(epoch)
4. export(best_skill) → 部署到Agent运行时
```

---

## 七、与龙虾技能体系融合

| 龙虾现有协议 | SkillOpt增强 |
|-------------|-------------|
| 协议#21 CASCADE双元技能 | +文本空间训练循环 |
| 协议#38 技能全生命周期 | +Validation Gate防退化 |
| 协议#73 MUSE五阶段 | +学习率调度+负反馈约束 |
| 协议#49 性能工程化 | +52/52全优验证基准 |

**融合路径**：龙虾技能库的现有技能文档（.md）可直接作为SkillOpt的初始best_skill.md，通过训练循环自动优化，无需人工改写。

---

*协议版本：v1.0 | 创建时间：2026-06-02 R45 | 对标：Microsoft SkillOpt*