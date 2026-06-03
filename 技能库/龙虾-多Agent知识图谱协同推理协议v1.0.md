# 龙虾-多Agent知识图谱协同推理协议 v1.0

> 协议编号: #115 | 版本: v1.0 | 创建日期: 2026-06-01
> 对标来源: Hermes TencentDB Agent Memory + EverOS HyperMem超图引擎 + Claude Managed Agents跨会话共享
> 生效范围: 龙虾AI体系全线Agent

---

## 一、协议概述

多Agent知识图谱协同推理协议定义了一个**Agent间知识共享与协同推理**的标准框架。通过超图结构将不同Agent的记忆、推理结果和领域知识关联成统一的知识图谱，使Agent能够访问和利用其他Agent的经验，实现体系级的集体智能。

---

## 二、核心架构

### 2.1 三层知识图谱

```
┌──────────────────────────────────────────┐
│             L3: 推理层（Inference）        │
│   跨Agent推理链 + 因果关联 + 决策路径      │
│   例：Agent A发现X → Agent B基于X推演Y    │
├──────────────────────────────────────────┤
│             L2: 关联层（Association）      │
│   Agent间关系 + 任务依赖 + 知识引用        │
│   例：file-agent结果→被computer-agent使用  │
├──────────────────────────────────────────┤
│             L1: 实体层（Entity）           │
│   文件/任务/配置/Agent实例/协议/技能       │
│   例：SOUL.md、报告、search-agent实例      │
└──────────────────────────────────────────┘
```

### 2.2 超图节点类型

| 节点类型 | 示例 | 属性 |
|---------|------|------|
| Agent | file-agent, search-agent, app-agent | 能力域、工具集、状态 |
| Document | SOUL.md, R32报告, 协议文件 | 路径、版本、摘要向量 |
| Task | 搜索任务, 文件整理, 报告生成 | 状态、优先级、关联Agent |
| Concept | "自进化", "多Agent协作", "记忆策展" | 领域、置信度、来源 |
| Memory | 经验记录、错误模式、成功模板 | 时效性、复用次数、评分 |

### 2.3 超边关系类型

| 关系 | 示例 | 权重 |
|------|------|------|
| PRODUCED_BY | 报告 ← Agent | 1.0 |
| USED_IN | 文件 → 任务 | 0.8 |
| SIMILAR_TO | 概念A ↔ 概念B | 0.6 |
| DEPENDS_ON | 任务A → 任务B | 0.9 |
| LEARNED_FROM | 经验 ← 任务 | 0.7 |
| COLLABORATED_WITH | Agent A ↔ Agent B | 0.5 |

---

## 三、协同推理机制

### 3.1 推理触发

```
用户任务
    ↓
主Agent分解 → 子任务T1, T2, T3
    ↓
查询知识图谱:
  ├── 是否有Agent执行过类似任务？
  ├── 是否有相关经验/错误模式？
  ├── 是否有现成的协议/技能可用？
  └── 其他Agent的推理结果是否有参考价值？
    ↓
注入相关上下文 → 子Agent执行 → 结果回写知识图谱
```

### 3.2 交叉验证机制

当多个Agent对同一问题产生推理结果时：

```python
def cross_validate(results):
    if len(results) >= 2:
        consensus = find_consensus(results)
        confidence = calculate_confidence(results, consensus)
        if confidence < 0.7:
            flag_for_review(consensus, results)
        return consensus, confidence
    return results[0], 1.0
```

### 3.3 知识继承链

```
Agent A (执行任务X, 成功)
    ↓ 提炼经验
知识图谱节点 E1 (错误模式: 路径编码问题)
    ↓ 下次任务Y触发
Agent B (查询到E1, 自动避免相同错误)
    ↓ 执行成功
知识图谱节点 E2 (成功模板: 路径处理最佳实践)
```

---

## 四、图谱操作接口

### 4.1 查询接口

| 操作 | 接口 | 说明 |
|------|------|------|
| 实体查询 | query_entity(id) | 按ID查询节点 |
| 关系查询 | query_relations(entity, rel_type) | 查询指定关系 |
| 语义搜索 | semantic_search(query, top_k) | 向量相似度搜索 |
| 路径查询 | find_path(entity_a, entity_b) | 查找两节点间最短路径 |
| 子图导出 | export_subgraph(center, depth) | 以某节点为中心导出k-hop子图 |

### 4.2 写入接口

| 操作 | 接口 | 说明 |
|------|------|------|
| 创建节点 | create_node(type, props) | 创建实体/概念/记忆节点 |
| 创建关系 | create_edge(src, dst, rel_type, weight) | 创建超边 |
| 更新属性 | update_node(id, props) | 更新节点属性 |
| 合并节点 | merge_nodes(id_a, id_b) | 合并重复节点 |

### 4.3 存储格式

```json
{
  "graph_id": "lobster_kg_v2",
  "version": "1.0",
  "nodes": {
    "agent_file_001": {
      "type": "Agent",
      "name": "file-agent",
      "capabilities": ["文件搜索", "文档分析", "格式转换"],
      "status": "active",
      "embedding": [0.12, -0.34, ...]
    }
  },
  "edges": [
    {
      "source": "agent_file_001",
      "target": "doc_soal_md",
      "type": "MODIFIED",
      "weight": 0.9,
      "timestamp": "2026-06-01T14:30:00Z"
    }
  ]
}
```

---

## 五、记忆共享与隔离

### 5.1 共享记忆池

| 记忆类型 | 共享范围 | 示例 |
|---------|---------|------|
| 全局经验 | 全体Agent | 错误模式库、成功模板库 |
| 领域经验 | 同类型Agent | 文件操作最佳实践、搜索策略 |
| 任务上下文 | 同一任务的Agent链 | 文件路径、中间结果 |
| 私有记忆 | 单个Agent | 会话历史、工具偏好 |

### 5.2 记忆更新策略

```
Agent完成任务
    ↓
提取可共享经验（去隐私+抽象化）
    ↓
提交至共享记忆池（带置信度评分）
    ↓
其他Agent下次任务时自动查询
    ↓
高价值记忆通过Dreaming固化为长期知识
```

---

## 六、协同推理质量指标

| 指标 | 计算方式 | 目标 |
|------|---------|------|
| 知识命中率 | 查询数/有效命中数 | >60% |
| 推理加速比 | 无图谱用时/有图谱用时 | >1.3x |
| 错误避免率 | 避免的错误/总错误数 | >40% |
| 跨Agent知识复用 | 复用的知识条数/总知识 | >25% |
| 图谱一致性 | 重复节点率 | <5% |

---

> 版本: v1.0 | 关联协议: #64 超图多层记忆引擎 | #37 Dreaming跨会话元学习 | #67 双记忆协同进化
> 文件: E:\龙虾AI主控中心\我的AI分身\技能库\龙虾-多Agent知识图谱协同推理协议v1.0.md
