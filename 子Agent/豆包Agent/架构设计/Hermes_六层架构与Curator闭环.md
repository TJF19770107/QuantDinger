# Hermes Agent 六层架构与Curator自学习闭环
## 来源：NousResearch/hermes-agent 源码分析 (2026-05)

---

## 一、基本信息

| 维度 | 详情 |
|------|------|
| 仓库 | NousResearch/hermes-agent |
| Stars | 150,000+ |
| 语言 | Python (CLI/Agent核心) + TypeScript (Ink TUI) |
| 入口类 | AIAgent (~12k LOC) + HermesCLI (~11k LOC) |
| 测试 | ~17,000测试 / ~900测试文件 |
| 版本 | v0.2.0 ~ v0.13.0 (13个正式版本) |

---

## 二、六层架构骨架

```
L6 入口/UI: CLI + TUI(Ink React) + Gateway + ACP适配器
L5 编排: AIAgent 同步对话循环
L4 工具: 注册中心 + 自动发现机制
L3 推理: Provider适配器 + 缓存 + 压缩 + Curator
L2 持久化: SQLite + FTS5全文索引 + 插件记忆
L1 系统: ~/.hermes/ 配置 + .env + 7种执行后端
```

### 核心循环（来自 run_agent.py::run_conversation）

```python
while (api_call_count < self.max_iterations and iteration_budget.remaining > 0) \
        or self._budget_grace_call:
    if self._interrupt_requested: break
    response = client.chat.completions.create(
        model=model, messages=messages, tools=tool_schemas
    )
    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = handle_function_call(tool_call.name, tool_call.args, task_id)
            messages.append(tool_result_message(result))
        api_call_count += 1
    else:
        return response.content
```

四个关键设计：

| 设计 | 说明 |
|------|------|
| **同步而非异步** | 循环本身同步，异步只在IO边界 |
| **预算驱动** | max_iterations硬上限 + iteration_budget软预算 + budget_grace_call恩典调用 |
| **共享预算池** | 子Agent与父Agent共享同一个iteration_budget |
| **可中断** | 每轮检查_interrupt_requested，Ctrl+C或/stop立即拉出 |

---

## 三、Curator 自学习器（核心差异化能力）

### 配置参数

| 参数 | 作用 |
|------|------|
| curator.enabled | 总开关 |
| interval_hours | 触发周期 |
| min_idle_hours | 仅在idle时间窗工作，不抢占主对话 |
| stale_after_days | 过期skill判定 |
| archive_after_days | 自动归档 |
| backup | 备份钩子 |

### 闭环流程

```
执行 → 评估 → 提取 → 精炼 → 检索
  │      │      │      │      │
  完成任务 识别模式 提炼知识 写成skill 下次命中
```

### 复合增长效应

据Nous Research基准测试，持续使用数周后：**任务成功率提升40%**。

---

## 四、Tools vs Skills 关键区分

| 维度 | Tools | Skills |
|------|-------|--------|
| **形式** | Python函数 + JSON Schema | Markdown文档 |
| **执行** | 确定性解释执行 | LLM运行时解释 |
| **修改** | 需编辑源代码 | Curator可自动生成 |
| **注册** | tools/*.py + toolsets.py | skills/目录 |
| **发现** | 自动发现（registry.register） | 按名称调用 |

---

## 五、记忆系统

### SQLite + FTS5 全文索引

- 毫秒级关键词召回
- LLM摘要做语义压缩
- 不用向量库 → $5 VPS可运行
- context_compressor.py主动压缩防溢出

### 衍生记忆插件

| 插件 | 用途 |
|------|------|
| Honcho | 辩证用户建模 |
| mem0 | 通用键值记忆 |
| supermemory | 多模态长期记忆 |

---

## 六、Provider适配层

统一抽象20个Provider，通过api_mode字段切换：

| 适配器 | 协议 |
|--------|------|
| anthropic_adapter | Anthropic Messages API |
| codex_responses_adapter | OpenAI Codex Responses API |
| gemini_native_adapter | Google Gemini 原生 |
| gemini_cloudcode_adapter | Google Cloud Code Assist |
| copilot_acp_client | GitHub Copilot ACP |
| bedrock_adapter | AWS Bedrock |

---

## 七、7种执行后端

| 后端 | 适用场景 |
|------|---------|
| local | 本地shell |
| docker | 容器隔离 |
| ssh | 远程主机 |
| singularity | HPC容器 |
| modal | Serverless GPU |
| daytona | Serverless持久化沙箱 |
| vercel sandbox | 边缘运行时 |

---

## 八、豆包对标行动

| Hermes能力 | 豆包落地 |
|------------|---------|
| Curator自学习 | 后台异步学习器，从任务轨迹提炼技能 |
| SQLite+FTS5记忆 | 本地记忆基础设施，轻量高性能 |
| Tools vs Skills分离 | 能力层架构重组，可进化知识独立管理 |
| 同步while+预算循环 | 主Agent推理循环参考实现 |
| Agent级工具拦截 | todo/memory等特权工具走特殊路径 |
| 插件系统 | 自定义能力不侵入Core，走插件路径 |
