# 龙虾_多Provider抽象层 v1.0

> **来源**：OpenCode Provider Abstraction Layer
> **类型**：融合技能 · 模型适配
> **融合日期**：2026-05-31（R06）

---

## 一、核心哲学

> **Agent 的价值在 tooling 层，而非模型层。**
> 切换模型应当是配置变更，而非代码变更。

OpenCode 通过统一的 Provider Adapter 接口支持 75+ LLM Provider，包括商业模型、开源模型和本地模型。

## 二、架构设计

```
┌────────────────────────────────────┐
│           Model Interface           │
│   (统一接口: chat / stream / tool)  │
├────────────────────────────────────┤
│         Provider Adapter           │
│   ┌──────┬──────┬──────┬──────┐    │
│   │Claude│ GPT  │Gemini│Local │    │
│   │Adapter│Adapter│Adapter│Adapter│   │
│   └──┬───┘──┬───┘──┬───┘──┬───┘    │
│      │      │      │      │        │
│  Anthropic OpenAI Google Ollama    │
│    API     API    API   vLLM      │
└────────────────────────────────────┘
```

## 三、Provider 注册表

| Provider | 模型 | 类型 | 费用 | 延迟 | 适用场景 |
|----------|------|------|------|------|---------|
| Anthropic | Claude 4.x | 商业 | 高 | 中 | 深度推理/复杂任务 |
| OpenAI | GPT-5.x | 商业 | 高 | 低 | 快速代码生成 |
| Google | Gemini 3.5 | 商业 | 低 | 极低 | 大批量/高性价比 |
| Ollama | Llama 3/Qwen3 | 本地 | 免费 | 高 | 隐私敏感/离线 |
| OpenRouter | 多模型路由 | 聚合 | 中 | 中 | 灵活切换 |
| Models.dev | 75+ Provider | 聚合 | - | - | 最大选择范围 |

## 四、适配器接口规范

```json
{
  "provider": "anthropic|openai|google|ollama|...",
  "model": "claude-4|gpt-5|gemini-3.5-flash|llama3|...",
  "mode": "chat|stream|tool_use",
  "request": {
    "messages": [...],
    "tools": [...],
    "max_tokens": 4096,
    "temperature": 0.7
  },
  "response": {
    "text": "...",
    "tool_calls": [...],
    "usage": {
      "prompt_tokens": 0,
      "completion_tokens": 0
    }
  }
}
```

## 五、性价比路由策略（借鉴Gemini 3.5 Flash）

```
任务分类 → 模型选择:

简单任务 (文件读取/搜索/简单问答)
  → Gemini 3.5 Flash (4x速度, 半价)

中等任务 (代码生成/文件编辑/分析)
  → Claude/GPT 平衡模式

复杂任务 (多文件重构/深度推理/长上下文)
  → Claude 深度推理模式

隐私任务 (敏感文件/本地数据)
  → 本地模型 (Ollama/Qwen3)
```

## 六、与豆包Agent融合

豆包Agent应实现：
1. **多Provider配置**：用户可选择默认模型+备选模型
2. **自动降级**：主Provider不可用时自动切换备选
3. **任务路由**：根据任务复杂度自动选择最合适的模型
4. **本地模型优先**：隐私模式下强制使用本地模型