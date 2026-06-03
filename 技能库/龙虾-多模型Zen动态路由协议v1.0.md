# 龙虾-多模型Zen动态路由协议 v1.0

## 协议元信息

- **协议编号**：#77
- **协议版本**：v1.0
- **对标来源**：OpenCode Zen（120K GitHub Stars，75+模型Provider）
- **发布日期**：2026-06-01
- **所属迭代**：R20

---

## 一、核心原理

OpenCode Zen通过75+模型Provider动态路由，将每个任务自动匹配到最优模型（质量/成本/延迟三维平衡）。实测成本降低70%，同时保持或提升任务质量。

**核心突破**：不再用"一个模型打天下"，而是为每个任务动态选择最合适的模型，像CPU调度一样智能。

---

## 二、动态路由引擎

### 2.1 任务分析器
```
输入：用户请求
输出：任务画像

任务画像 = {
    type: "coding" | "reasoning" | "creative" | "search" | "math" | "translation" | "chat",
    complexity: 1-10,
    context_length: N tokens,
    latency_sensitive: true/false,
    cost_sensitive: true/false,
    quality_critical: true/false,
    privacy_required: true/false
}
```

### 2.2 模型评分矩阵
```
对每个可用模型：
    quality_score = benchmark分数 × 用户反馈权重
    cost_score = 输入Token单价 × context_length + 输出Token单价 × 预估输出长度
    latency_score = 预估推理时间
    
    final_score = (
        quality_weight × quality_score +
        cost_weight × (1 / cost_score) +
        latency_weight × (1 / latency_score)
    )

权重由用户策略决定：
- 质量优先：quality=0.7, cost=0.15, latency=0.15
- 成本优先：quality=0.3, cost=0.5, latency=0.2
- 平衡模式：quality=0.4, cost=0.3, latency=0.3
```

### 2.3 智能降级链
```
主模型失败 → 自动切换
Claude Opus 4.8 (失败) → GPT-4o (失败) → Gemini 2.5 Pro (失败) → Claude Sonnet 4 (保底)
```

降级链按任务类型定制：
- **编码任务**：Claude Opus → GPT-4o → Claude Sonnet
- **创意任务**：GPT-4o → Claude Opus → Gemini 2.5
- **数学任务**：GPT-4o → Claude Opus → Gemini 2.5
- **翻译任务**：Gemini 2.5 → GPT-4o → Claude Sonnet

### 2.4 本地优先策略
```
if local_model_available and privacy_required:
    route_to_local()  # Ollama/LM Studio，零成本+零延迟
elif local_model_quality >= threshold:
    route_to_local()  # 质量够用优先本地
else:
    route_to_cloud()  # 质量不够才上云
```

---

## 三、75+ Provider支持

### 云端Provider（部分列表）

| Provider | 代表模型 | 擅长 | 成本 |
|----------|---------|------|------|
| Anthropic | Claude Opus 4.8 | 编码/推理 | 高 |
| OpenAI | GPT-4o | 通用/创意 | 中高 |
| Google | Gemini 2.5 Pro | 多模态/搜索 | 中 |
| MiniMax | MiniMax M2.7 | 中文/创意 | 低 |
| 阶跃星辰 | Step 3.5 Flash | 中文/推理 | 低 |
| DeepSeek | DeepSeek-V3 | 推理/数学 | 低 |
| Kimi | Moonshot | 长文档 | 低 |
| 智谱 | GLM-4 | 中文通用 | 低 |
| 腾讯 | Hy3 Preview | 中文/安全 | 低 |

### 本地Provider

| Provider | 代表模型 | 适用场景 |
|----------|---------|---------|
| Ollama | LLaMA 3 / Mistral / Qwen | 隐私优先任务 |
| LM Studio | 各种GGUF模型 | 桌面端离线推理 |
| vLLM | 自部署开源模型 | 企业级本地部署 |

---

## 四、成本优化策略

| 策略 | 描述 | 节省 |
|------|------|------|
| 模型分级 | 简单任务→低成本模型，复杂任务→高成本模型 | ~40% |
| 本地优先 | 质量够用就本地跑，省Token费 | ~30% |
| Cache复用 | 相同或相似请求复用上一轮结果（限非时间敏感） | ~15% |
| Batch合并 | 多个小请求合并为一次API调用 | ~10% |
| 合计 | | **~70%** |

---

## 五、集成方式（接入龙虾五步法）

### Step 1：意图识别
- 用户请求 → 任务分析器提取任务画像

### Step 2：能力映射
- 查询模型评分矩阵 → 计算每个可用模型的final_score
- 检查本地模型可用性 → 本地优先判断

### Step 3：方案规划
- 选择最优模型 + 降级链
- 如用户指定模型 → 使用指定模型（覆盖自动路由）

### Step 4：自主执行
- 调用主模型 → 成功：返回结果
- 调用主模型 → 失败：自动切换到降级链下一个模型 → 直到成功

### Step 5：反思进化
- 记录本次模型选择的质量+成本+延迟 → 更新模型评分矩阵
- 积累用户反馈 → 微调质量权重

---

## 六、安全约束

1. **数据隔离**：本地模型的数据绝不外传；云端模型仅传输必要上下文
2. **模型黑名单**：安全评分<阈值的模型自动加入黑名单
3. **审计日志**：每次模型调用的Provider/Model/Token数/成本记录到审计日志
4. **密钥管理**：API Key存储在加密配置中，绝不硬编码
5. **隐私强制**：用户设置"隐私优先"→强制路由到本地模型（忽略成本/质量权重）

---

## 七、预期效果

| 指标 | Zen路由前 | Zen路由后 |
|------|---------|----------|
| 月均Token成本 | 基准 | **降低70%** |
| 简单任务响应时间 | 依赖顶级模型（慢） | 路由到低成本快速模型 |
| 复杂任务质量 | 单一模型天花板 | 自动选择最优模型 |
| 隐私保障 | 全部上云 | 隐私任务本地处理 |
| 模型故障应对 | 单点故障 | 自动降级链无缝切换 |

---

## 八、与已有协议的关系

| 已有协议 | 关系 |
|---------|------|
| 协议50 多模型无感切换协议 | Zen替代协议50（升级为75+Provider动态路由+成本优化） |
| 协议59 本地混合推理网关 | Zen替代协议59（统一为本地+云端动态路由） |
| 协议61 多Agent置信度验收 | Zen的降级链与协议61互补（模型降级+Agent交叉验证） |

---

> **协议状态**：已激活 ✅
> **依赖**：OpenRouter API / 各模型Provider API Key
> **建议轮次**：R21实现Zen路由核心引擎，逐步接入75+Provider
