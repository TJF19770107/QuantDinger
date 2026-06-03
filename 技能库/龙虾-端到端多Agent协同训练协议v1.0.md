# 端到端多Agent协同训练协议 v1.0

> **版本**: v1.0 · 2026-06-01
> **协议编号**: #78
> **对标来源**: MetaAgent-X (Oregon State/UCSD/Amazon AGI/Penn State · 2026-05-30)
> **论文**: arxiv.org/abs/2605.14212
> **GitHub**: github.com/pettingllms-ai/PettingLLMs
> **核心价值**: Designer+Executor双角色RL协同进化 + 端到端训练闭环

---

## 一、协议概述

端到端多Agent协同训练协议定义了让同一个基座模型既学会"如何设计一个多Agent系统"（Designer角色），也学会"如何在这个系统中执行任务"（Executor角色），并通过强化学习让两种能力同时提升的标准化流程。

传统多Agent系统在模型外部"搭流程"，设计者再聪明，执行者不会随反馈进化。本协议将设计和执行都放进同一个端到端训练闭环中，打破固定执行器的能力天花板。

---

## 二、双角色定义

### 2.1 Designer（设计者）
- 职责：接收任务→分析复杂度→设计多Agent系统结构（角色分配/通信拓扑/任务分解）
- 输入：任务描述 + 环境约束
- 输出：System Design JSON（角色定义/拓扑图/通信协议）

### 2.2 Executor（执行者）
- 职责：按System Design JSON实例化Agent → 执行任务 → 收集反馈
- 输入：System Design JSON + 任务上下文
- 输出：执行轨迹 + 结果 + 性能指标

---

## 三、端到端训练闭环

```
Task → Designer(SD) → Executor(轨迹) → Reward(任务完成度+效率) → RL Update → Designer&Executor同时更新
```

| 阶段 | 动作 | 输出 |
|------|------|------|
| 1. 设计 | Designer分析任务，生成System Design | SD JSON |
| 2. 执行 | Executor按SD实例化Agent，执行任务 | 执行轨迹 |
| 3. 评估 | 计算Reward（任务完成度+通信效率+资源消耗） | Reward向量 |
| 4. 更新 | RL算法同时更新Designer和Executor参数 | 新模型权重 |

---

## 四、执行规范

### 4.1 设计规范
- Designer必须明确输出Agent数量、角色定义、通信拓扑（树/星/DAG/全连接）
- 每个子Agent必须有明确的能力边界和验收标准
- 通信协议必须定义消息格式和优先级

### 4.2 执行规范
- Executor必须严格按SD实例化Agent，不得私自增减
- 所有Agent间通信必须记录到执行轨迹
- 执行失败时，Executor必须标记失败节点并尝试单次重试

### 4.3 训练规范
- Reward设计：任务完成度(0.5) + 效率得分(0.3) + 通信合理性(0.2)
- 训练频率：每完成N个任务后执行一次RL update（N可配置，建议≥10）
- 评估指标：Success Rate / Steps-to-Completion / Communication Overhead

---

## 五、安全约束

1. Designer不得设计可执行系统级破坏性操作的Agent角色
2. Executor执行前必须进行Designer输出的安全审查
3. 端到端训练期间，模型不得访问生产环境，仅限沙箱训练
4. 训练数据中的任务不得包含真实用户敏感信息

---

## 六、与现有协议关系

| 协议 | 关系 | 说明 |
|------|------|------|
| #41 协议化闭环自进化协议 | 互补 | #41定义资源建模+版本管理，#78定义端到端训练 |
| #48 双层元Agent解冻协议 | 升级 | #48定义双层概念，#78提供具体RL训练方法 |
| #25 Lead-Specialist推理分发协议 | 增强 | #25定义运行时角色分发，#78训练时优化角色设计 |
| #42 Swarm多Agent拓扑调度协议 | 互补 | #42定义DAG拓扑，#78自动学习最优拓扑 |

---

> 状态：ACTIVE | 执行者：豆包Agent
