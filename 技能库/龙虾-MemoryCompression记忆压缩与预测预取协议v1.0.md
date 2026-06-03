# 龙虾-MemoryCompression记忆压缩与预测预取协议 v1.0

> **协议编号**：66
> **对标来源**：Memory OS 2026 + MemGPT/Letta + Hippocampus-Inspired Replay
> **创建日期**：2026-06-01
> **适用Agent**：豆包Agent / MemoryOS v3.0
> **依赖**：MemoryOS v2.0+ / Dreaming记忆策展协议 / 向量数据库

---

## 一、协议概述

本协议为MemoryOS引入三层记忆压缩机制（遗忘协议）和预测预取能力。核心理念：记忆不是无限存储，而是智能分级压缩——近期高保真、中期语义摘要、远期原子事实。同时，系统在空闲时预测用户下一步需求并预加载相关记忆，降低响应延迟。

## 二、Memory OS六层架构

```
┌──────────────────────────────────────┐
│          L0: Working Memory          │ ← 当前对话上下文（高保真）
│          (LLM Context Window)        │
├──────────────────────────────────────┤
│          L1: Short-Term Memory       │ ← 本次会话历史（完整对话）
│          (会话级缓存)                 │
├──────────────────────────────────────┤
│          L2: Recent Memory           │ ← 近7天交互（摘要+关键事实）
│          (近期压缩存储)               │
├──────────────────────────────────────┤
│          L3: Semantic Memory         │ ← 7-30天（语义向量索引）
│          (语义事实存储)               │
├──────────────────────────────────────┤
│          L4: Core Memory             │ ← 永久保留（用户画像/偏好）
│          (核心画像)                    │
├──────────────────────────────────────┤
│          L5: Knowledge Graph         │ ← 跨会话实体关系图
│          (知识图谱)                    │
└──────────────────────────────────────┘
```

## 三、Memory Compression遗忘协议

### 3.1 三级压缩策略

| 层级 | 时间范围 | 存储形式 | 压缩率 |
|------|---------|---------|--------|
| L0 | 当前会话 | 完整原始文本 | 0% |
| L1 | 本次会话 | 完整对话（结构化） | ~10% |
| L2 | 1-7天 | 摘要 + 关键事实 | ~70% |
| L3 | 7-30天 | 语义向量 + 原子事实 | ~90% |
| L4 | 永久 | 用户画像 + 关键偏好 | ~95% |

### 3.2 Atomic Fact Extraction（原子事实提取）

原始记忆："用户在2026年5月31日说喜欢用VSCode开发Python，使用黑色主题，偏好Tab缩进"

压缩后：
```json
{
  "facts": [
    {"entity": "user", "attribute": "preferred_editor", "value": "VSCode"},
    {"entity": "user", "attribute": "preferred_language", "value": "Python"},
    {"entity": "user", "attribute": "editor_theme", "value": "dark"},
    {"entity": "user", "attribute": "indent_style", "value": "tab"}
  ],
  "source": "2026-05-31_session_143",
  "confidence": 0.95
}
```

### 3.3 Temporal Decay（时间衰减）

```python
memory_weight = base_weight * exp(-λ * days_since_last_access)

# λ (衰减系数) 可配置：
# - 用户偏好：λ=0.01（慢衰减，永久保留）
# - 任务上下文：λ=0.1（中速衰减）
# - 临时信息：λ=0.5（快速衰减）
```

### 3.4 冲突解决

- 旧事实与新事实冲突 → 新事实覆盖（带时间戳）
- 多个来源不一致 → 标记为"待确认"
- 明确撤回 → 立即删除（非衰减）

## 四、Hippocampus-Inspired Replay（离线巩固）

### 4.1 机制

在系统空闲时（低负载），自动执行记忆巩固：

1. 从L2/L3中随机采样记忆片段
2. 重新处理和提炼
3. 发现跨会话模式（如用户每周五下午做代码Review）
4. 更新L4核心画像和L5知识图谱

### 4.2 触发条件

- CPU使用率 < 20%
- 连续空闲时间 > 5分钟
- 每日定时（如凌晨3:00）

## 五、Predictive Prefetching（预测预取）

### 5.1 预测逻辑

基于用户行为模式预测下一步可能需要的记忆：

- 时间模式：周一早上→加载工作相关记忆
- 任务模式：打开VSCode→预加载最近编辑的项目上下文
- 对话模式：提到"上次那个Bug"→预加载最近的Bug修复记忆

### 5.2 预取策略

| 策略 | 说明 | 命中率目标 |
|------|------|-----------|
| 时间驱动 | 基于时间段预测 | 60%+ |
| 任务驱动 | 基于当前活跃任务 | 75%+ |
| 关联驱动 | 基于知识图谱关系 | 80%+ |

### 5.3 实现

```
空闲时：
  → 分析用户行为模式
  → 预测下一步可能触达的记忆
  → 预加载到L0/L1
  → 用户提问时零延迟响应
```

## 六、State Summary Token（跨会话恢复）

### 6.1 概念

每次会话结束时生成一个高度压缩的"状态摘要Token"（State Summary Token），包含：
- 上次会话的核心上下文
- 未完成的任务
- 关键决策和结论
- 用户当时情绪/状态

### 6.2 恢复流程

新会话启动 → 加载State Summary Token → Agent"回忆"上次状态 → 无缝衔接

```json
{
  "session_id": "sess_20260601_001",
  "summary_embedding": [0.12, -0.45, ...], // 256维压缩向量
  "pending_tasks": ["完成R18迭代报告"],
  "key_decisions": ["采用Agentic RAG架构"],
  "user_state": "满意，期待R19"
}
```

## 七、实施路径

| 阶段 | 内容 | 优先级 |
|------|------|--------|
| Phase 1 | Atomic Fact Extraction + 三级压缩 | P1 |
| Phase 2 | Temporal Decay时间衰减引擎 | P1 |
| Phase 3 | Hippocampus-Inspired离线巩固 | P2 |
| Phase 4 | Predictive Prefetching预测预取 | P2 |
| Phase 5 | State Summary Token跨会话恢复 | P2 |

---

> **版本**：v1.0
> **状态**：ACTIVE
> **关联文件**：memory-os-v2.0.md, MemoryOS/SKILL.md, 龙虾-Dreaming记忆策展协议v1.0.md, 龙虾-Hy-Memory六层记忆框架协议v1.0.md
