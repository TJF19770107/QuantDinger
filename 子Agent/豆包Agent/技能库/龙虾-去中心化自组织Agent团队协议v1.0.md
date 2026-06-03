# 龙虾-去中心化自组织Agent团队协议 v1.0

> **协议编号**: #160
> **对标来源**: AutoScientists (Harvard/Kempner/Broad, arXiv:2605.28655, 2026-05-27)
> **版本**: v1.0
> **生效日期**: 2026-06-02
> **状态**: ✅ 已落地

---

## 一、协议概述

本协议对标 Harvard AutoScientists 框架，为豆包Agent引入**去中心化自组织Agent团队**能力，支持多Agent在无中央规划器的情况下，基于共享状态自主组织课题组、并行探索假设、共享成功/失败经验，避免重复探索。

**核心创新**：从"中央规划多Agent"进化为"去中心化自组织Agent团队"。

---

## 二、核心架构

### 2.1 共享状态（Shared State）

所有Agent读写同一共享状态，包含以下核心组件：

| 组件 | 功能 | 数据结构 |
|------|------|---------|
| `proposals` | 待评估假设/方案 | List[Proposal] |
| `experiments` | 执行中的实验 | Dict[ExpID, Experiment] |
| `results` | 实验结果 | Dict[ExpID, Result] |
| `current_best` | 当前最优解 | Solution |
| `discussion_forum` | Agent讨论与评审记录 | List[Post] |
| `dead_end_registry` | 已验证失败的路径 | Set[HypothesisID] |
| `work_queue` | 待认领任务 | Queue[Task] |

### 2.2 去中心化论坛机制（Decentralized Forum）

Agent在消耗实验计算资源前，先在论坛中发帖描述方案，其他Agent跟帖评审：

```
Agent A 发帖: "我打算尝试方案X，基于假设H"
Agent B 跟帖: "H已在dead_end_registry中，建议转向H'"
Agent C 跟帖: "我之前尝试过X的变体，结果是..."
Agent A 决策: 根据反馈修改或放弃方案
```

**关键规则**：
- 发帖→评审→决策 在消耗算力前完成
- 评审Agent基于共享状态中的历史结果给出建议
- 低质量提案被提前过滤，节省计算资源

### 2.3 自组织课题组（Self-Organizing Team）

当某个假设方向显示出潜力时，多个Agent自发围绕该方向组建课题组：

```
1. 探测潜力：某假设的实验结果优于随机基线
2. 论坛广播：牵头Agent发帖招募合作者
3. 角色分工：
   - Lead Agent：整体协调，分配子任务
   - Specialist Agents：分别负责数据/模型/评估/验证
   - Critic Agent：对抗验证，主动寻找反例
4. 并行执行：各Specialist并行实验
5. 结果聚合：Lead Agent汇总，更新共享状态
6. 方向判断：若停滞，自动解散并转向新方向
```

---

## 三、核心流程

### 3.1 假说生成阶段

```
输入: 任务描述 + 共享状态中的已有知识
处理:
  1. 读取 current_best, dead_end_registry, discussion_forum
  2. 生成候选假设（避免dead-end中的方向）
  3. 在 forum 中发帖描述假设及推理链
  4. 等待其他Agent评审（超时机制）
  5. 根据评审意见修改或确认假设
输出: 评审通过的假设列表
```

### 3.2 实验规划阶段

```
输入: 评审通过的假设
处理:
  1. 设计实验方案（数据集/评价指标/基线方法）
  2. 估算计算成本，检查预算
  3. 在 forum 中发布实验计划
  4. 其他Agent可建议改进或指出缺陷
输出: 实验方案 + 预算分配
```

### 3.3 闭环验证阶段

```
输入: 实验方案
处理:
  1. 执行实验，记录详细日志
  2. 将结果写入 shared_state.results
  3. 若结果优于 current_best，更新 current_best
  4. 若结果证明假设无效，加入 dead_end_registry
  5. 在 forum 中发布结果，触发讨论
输出: 验证结果 + 更新后的共享状态
```

### 3.4 论文撰写阶段（可选）

```
输入: 共享状态中的完整实验记录
处理:
  1. 自动提取创新点（与current_best的历史版本对比）
  2. 生成论文大纲（相关Work/方法/实验/结论）
  3. 各Agent分别撰写各自专长部分
  4. Critic Agent撰写Limitations和Future Work
  5. Lead Agent统稿
输出: 完整论文草稿
```

---

## 四、死路注册与经验复用（Dead-End Registry）

### 4.1 注册条件

以下情况将假设加入dead-end registry：

| 条件 | 说明 |
|------|------|
| 实验证明无效 | 多次独立实验均无法超越基线 |
| 资源不可行 | 计算/数据需求超出系统能力 |
| 逻辑自相矛盾 | 理论分析发现根本缺陷 |
| 已被充分探索 | 该方向已有足够多的失败记录 |

### 4.2 经验记录格式

```json
{
  "hypothesis_id": "H_20260527_001",
  "statement": "用方法X解决任务Y",
  "failure_mode": "实验证明无效",
  "evidence": ["exp_123", "exp_124"],
  "lessons_learned": "X在Y上失效 because...",
  "suggested_alternatives": ["H_20260527_002", "H_20260527_003"],
  "registered_by": "Agent_B",
  "timestamp": "2026-05-27T10:30:00Z"
}
```

### 4.3 新假设生成时的dead-end检查

```
生成新假设时：
  1. 计算与新假设相似度（embedding-based）
  2. 若与dead-end中某条目相似度 > 0.85：
     a. 读取该条目的 lessons_learned
     b. 若 lessons_learned 可直接推翻，允许重新探索
     c. 否则，阻止该假设进入评审流程
```

---

## 五、ClawInstitute平台对接

AutoScientists运行于ClawInstitute平台（AI Agent社交协作平台），本协议定义对接接口：

### 5.1 平台API

```python
class ClawInstituteClient:
    def post_to_forum(self, proposal: Proposal) -> PostID
    def get_posts(self, topic: str) -> List[Post]
    def register_dead_end(self, entry: DeadEndEntry) -> bool
    def update_shared_state(self, key: str, value: Any) -> bool
    def get_shared_state(self, key: str) -> Any
```

### 5.2 与豆包Agent的集成点

```
豆包Agent
  └── 多Agent协调层（协议#155 Kanban看板）
        └── 去中心化论坛层（本协议）
              ├── 共享状态管理
              ├── 论坛评审协调
              ├── 死路注册查询
              └── 自组织课题组管理
```

---

## 六、基准测试对标

### 6.1 BioML-Bench（24任务）

| 方法 | 平均排行百分位 | 提升 |
|------|--------------|------|
| 最强AI Agent基线 | 66.07% | — |
| **AutoScientists** | **74.4%** | **+8.33%** |
| 豆包Agent（目标R50） | 76%+ | +1.6%+ |

### 6.2 GPT训练优化

| 方法 | 达到目标验证bpp所需实验数 | 速度比 |
|------|--------------------------|-------|
| AutoResearch（单Agent） | N | 1.0x |
| **AutoScientists** | **≈ N/1.9** | **1.9x** |
| 豆包Agent（目标R50） | ≈ N/2.2 | 2.2x |

### 6.3 ProteinGym适应性预测

| 方法 | 斯皮尔曼相关性提升 |
|------|-------------------|
| 先前SOTA | baseline |
| **AutoScientists（ACE2-Spike结合）** | **+12.5%** |
| AutoScientists（全部217测定） | +6.5% |
| 豆包Agent（目标R50） | +8.0%+ |

---

## 七、部署指南

### 7.1 依赖

```bash
pip install networkx      # 课题组拓扑管理
pip install sentence-transformers  # 假设相似度计算
pip install aiohttp       # 异步论坛通信
```

### 7.2 配置文件（config.yaml）

```yaml
auto_scientists:
  enable: true
  forum:
    enable: true
    min_reviews_before_execution: 2
    timeout_seconds: 300
  dead_end_registry:
    enable: true
    similarity_threshold: 0.85
  team_formation:
    enable: true
    min_agents_to_form_team: 3
    max_agents_per_team: 8
  shared_state_backend: "sqlite"  # 或 "redis"
  claw_institute_api:
    enable: false  # 未来对接ClawInstitute平台
    api_base: ""
```

### 7.3 启动方式

```bash
# 启动去中心化自组织Agent团队
python -m lobster.protocols.decentralized_self_organizing \
  --task "优化蛋白质-小分子结合亲和力预测" \
  --num_agents 5 \
  --budget_hours 48 \
  --enable_forum \
  --enable_dead_end_registry
```

---

## 八、协议版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-02 | 初始版本，对标AutoScientists Harvard 2026 |

---

> **协议状态**: ✅ 已落地
> **对标论文**: AutoScientists: Self-Organizing Agent Teams for Long-Running Scientific Experimentation (arXiv:2605.28655)
> **作者**: Shanghua Gao, Ada Fang, Marinka Zitnik (Harvard/Kempner/Broad)
> **集成协议**: #155(Kanban看板) / #156(千级并行编排) / #157(记忆三层标准化)
