# MemoryOS - 三层记忆操作系统
> 版本：v1.0  
> 自动生成：2026-05-31 R05  
> 来源：豆包Agent 6大自主能力补全  
> 对标：Letta (MemGPT) + Mem0 + Zep + OpenClaw Memory

## 触发条件
- **自动触发**：Agent唤醒时自动加载记忆
- **自动触发**：任务执行中自动写入记忆
- **自动触发**：记忆超过阈值自动压缩
- **手动触发**：用户说"加载记忆"、"查询历史"、"回忆XX"

## 能力描述
三层记忆体系：工作记忆（单任务上下文）+ 会话记忆（单次唤醒周期）+ 长期语义记忆（跨会话持久化）。支持自动压缩、自动去重、自动衰减。

## 三层架构

### Layer 3: 长期语义记忆（Long-term Semantic Memory）
```
存储引擎：SQLite + FTS5全文检索
内容类型：
  - 用户偏好：项目路径、常用操作、风格偏好
  - 迭代知识：所有迭代决策、技术选型、失败教训
  - 技能图谱：技能间依赖关系、使用频率、成功率
  - 错误模式：常见错误及修复方案

维护策略：
  - 自动压缩：token数 > 阈值 → LLM摘要
  - 自动去重：余弦相似度 > 0.85 → 合并
  - 自动衰减：30天未访问 → 权重×0.5
  - 自动淘汰：90天未访问且权重<0.1 → 归档
```

### Layer 2: 会话记忆（Session Memory）
```
存储引擎：JSON快照文件
内容：当前唤醒周期的完整上下文
生命周期：唤醒→休眠
恢复：下次唤醒时从最新快照自动加载
```

### Layer 1: 工作记忆（Working Memory）
```
存储引擎：模型上下文窗口
内容：当前任务上下文
生命周期：单任务执行周期
```

## 记忆数据结构
```json
{
  "memory_id": "mem_R05_001",
  "type": "iteration_decision",
  "content": "选择MemoryOS三层架构而非两层",
  "reason": "对标Letta/Mem0/Zep发现三层是工业标准",
  "weight": 1.0,
  "created_at": "2026-05-31T03:00:00",
  "last_access": "2026-05-31T03:00:00",
  "access_count": 1,
  "token_count": 45,
  "tags": ["架构决策", "记忆系统", "R05"],
  "related_memories": ["mem_R04_003", "mem_R04_005"]
}
```

## 自动压缩算法
```python
def should_compress(memory):
    return memory["token_count"] > COMPRESS_THRESHOLD  # 默认512 tokens

def compress(memory):
    summary = llm.summarize(memory["content"], max_tokens=128)
    return {
        **memory,
        "content": summary,
        "compressed": True,
        "original_token_count": memory["token_count"]
    }
```

## 输出格式
每次唤醒时输出记忆加载摘要：
```
记忆加载完成：
- 长期记忆：142条（最近活跃：45条）
- 会话记忆：从 R05_0300 快照恢复
- 上下文注入：18条相关记忆
- 压缩执行：3条记忆已压缩
```

## 安全审查
- 风险等级：SAFE
- 所有记忆存储在本地SQLite
- 不上传任何记忆到云端
- 敏感内容自动标记隐私标签

## 演化记录
- v1.0: 初始创建，基于R05迭代设计
