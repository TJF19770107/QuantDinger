# 长程Harness编排协议 v1.0

> **创建时间**：2026-05-31 R06
> **对标来源**：Harness Engineering (53AI, 2026-04-08)
> **类型**：编排层 · 任务执行
> **状态**：ACTIVE

---

## 一、协议目标

为豆包Agent处理长程任务（>100文件、跨会话、亿级Token）提供系统化编排框架，解决上下文耗尽、中断无法恢复、规模放大行为不可控三大难题。

---

## 二、四大核心原则

### 2.1 任务拆解（Task Decomposition）

**粒度公式**（以 Claude Sonnet 200K 上下文为例）：

```
有效上下文 ≈ 200K Token
子任务消耗 = Prompt模板(1K) + 输入文件(30K-60K) + Agent工作过程(60K-180K)
子任务消耗 ≈ 90K-240K Token
经验上限 ≈ 3000行代码/子任务
```

**检验标准**：子任务Token消耗经常逼近上下文80% → 缩小粒度；仅用30-40% → 放大粒度。

**特殊规则**：同目录文件应放同一组（共享import/类型定义/配置），Agent可见完整局部上下文。

### 2.2 并行执行（Parallel Execution）

```
子任务 = 独立CLI进程（非对话内嵌套）
dispatch.js  → 首批启动（前N个，N=并发上限）
poll.js      → 后续监控 + 补位
外部脚本控制并发数：资源充裕10路，紧张3路，动态调整
```

**禁止**在主Agent会话中嵌套调用子Agent（到第30个子任务时上下文堆积29个历史，白白消耗Token）。

### 2.3 可续传（Resumability）

```
File As Progress：每个子任务状态持久化到任务清单JSON文件
状态枚举：pending → running → done / done_with_warnings / failed
中断后新会话 → 读取清单 → 跳过已完成 → 从断点继续
```

### 2.4 完成条件（Completion Conditions）

```
程序化校验（零Token）：编译通过 / 构建成功 / 单元测试通过
Evaluator校验（独立会话）：跨模型（如Sonnet做事 + GPT评价）
允许局部妥协：done_with_warnings → 99%完成可合入，剩余人工处理
禁止局部失败阻塞全局：5/1000失败 ≠ 阻塞其他995
```

---

## 三、任务边界三种模式

| 模式 | 策略 | 场景 | 关键规则 |
|------|------|------|---------|
| **无依赖** | 直接并行 | i18n提取 | 子任务不共享状态、不交叉引用 |
| **有依赖** | 拓扑排序+优先级批次 | JS→TS迁移 | 同优先级并行，跨优先级串行 |
| **有冲突** | Git Worktree物理隔离 | Code Review批量修复 | 各自独立修改 → 静止态统一合并 → Agent解决冲突 |

---

## 四、Prompt确定性原则

**禁止模式**：主Agent"理解"任务后自由发挥传给子Agent → 指令变形、上下文丢失

**正确模式**：`build-prompt.js` 程序化组装
```javascript
generateQuery({ files, rules, branch, outputFormat })
// → 所有子任务收到结构一致的指令
```

---

## 五、跨模型Evaluator

```
独立会话 → 干净上下文 → 不受执行过程干扰 → 客观评价
Sonnet 做事 + GPT 评价 → 不同"视角"降低偏见
```

---

## 六、调度生命周期

```
build-prompt.js   → 程序化组装Prompt
dispatch.js       → 创建Worktree + 生成Prompt + spawn子进程
poll.js（循环）   → 检查状态 → 成功→合入 / 失败→retry或标记FAILED
merge-results.js  → 合并所有产出
final-report.js   → 生成完成报告
```

---

> **豆包Agent集成点**：动态工作流引擎 v1.0 → 集成 Harness 编排
> **前置依赖**：Git、Node.js、任务清单 JSON Schema
> **协议版本**：v1.0 | R06