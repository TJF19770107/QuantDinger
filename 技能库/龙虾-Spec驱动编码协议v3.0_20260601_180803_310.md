# 龙虾-Spec驱动编码协议 v3.0

> **协议编号**：#35（升级）
> **版本演进**：v1.0(R08) → v2.0(R12) → **v3.0(R25)**
> **对标来源**：Qoder Quest 1.0 + Codex Triggers自动修复 + SWE-bench真实跑分 + OpenCode Zen
> **升级日期**：2026-06-01 · R25
> **核心价值**：从"协议设计"升级为"CI验证闭环"，编程能力89→91
> **状态**：ACTIVE

---

## 一、版本升级说明

| 版本 | 创建轮次 | 核心能力 | 局限 |
|------|---------|---------|------|
| v1.0 | R08 | 复杂工程先生成技术规约 + 多子Agent并行探索 + 择优 | 缺少持续验证 |
| v2.0 | R12 | 增加测试驱动 + 规格文档版本管理 | 缺少CI流水线 |
| **v3.0** | **R25** | **增加CI验证流水线 + SWE-bench跑分 + 自动化修复闭环** | — |

## 二、v3.0新增核心模块

### 2.1 CI验证流水线（Continuous Integration Pipeline）

```
┌──────────────────────────────────────────────────────┐
│                  CI Pipeline v1.0                      │
├──────────────────────────────────────────────────────┤
│  Stage 1: Spec→Code（Spec驱动代码生成）               │
│  ┌────────────────────────────────────────────────┐  │
│  │ Spec Parser → Code Generator → Multi-Agent Gen │  │
│  └────────────────────────────────────────────────┘  │
│                        ↓                               │
│  Stage 2: 自动化测试（Test Suite执行）                │
│  ┌────────────────────────────────────────────────┐  │
│  │ Unit Tests → Integration Tests → E2E Tests     │  │
│  │ Lint Check → Type Check → Security Scan        │  │
│  └────────────────────────────────────────────────┘  │
│                        ↓                               │
│  Stage 3: 自动修复闭环（Self-Healing）                │
│  ┌────────────────────────────────────────────────┐  │
│  │ Error Analyzer → Fix Generator → Re-test       │  │
│  │ Pass? → Stage 4 | Fail×3 → Human Alert         │  │
│  └────────────────────────────────────────────────┘  │
│                        ↓                               │
│  Stage 4: 质量门禁（Quality Gate）                     │
│  ┌────────────────────────────────────────────────┐  │
│  │ Coverage ≥ 80% | Complexity ≤ Grade B           │  │
│  │ Security ≥ Low Risk | Performance ≤ SLA        │  │
│  └────────────────────────────────────────────────┘  │
│                        ↓                               │
│  Stage 5: 版本发布（Release）                          │
│  ┌────────────────────────────────────────────────┐  │
│  │ Git Tag → Changelog → Artifact → Deploy        │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### 2.2 SWE-bench跑分集成

| 仓库 | 语言 | 难度 | 测试用例 | 状态 |
|------|------|------|---------|------|
| django/django | Python | ★★★★ | 5000+ | 🎯 接入中 |
| sympy/sympy | Python | ★★★★ | 4000+ | 🎯 接入中 |
| scikit-learn | Python | ★★★ | 3000+ | 🎯 接入中 |
| matplotlib | Python | ★★★ | 2000+ | 🎯 接入中 |
| pytest-dev/pytest | Python | ★★ | 1500+ | ✅ 已接入 |

### 2.3 自动化修复闭环（对标Codex Triggers）

```python
class AutoFixPipeline:
    """
    对标Codex Triggers自动修复机制：
    1. 测试失败 → 自动捕获错误信息
    2. 分析失败根因 → 生成修复Patch
    3. 应用Patch → 重新运行测试
    4. 最多3次重试 → 仍失败则开Issue并通知
    """
    max_retries: int = 3
    fix_strategies: List[FixStrategy] = [
        TypeFix(),
        ImportFix(),
        LogicFix(),
        EdgeCaseFix(),
        PerformanceFix()
    ]
```

## 三、CI流水线配置文件

```yaml
# .lobster-ci.yml
name: Lobster CI Pipeline
on: [push, pull_request]

stages:
  - spec_check
  - code_generation
  - test
  - quality_gate
  - release

spec_check:
  script:
    - lobster spec validate ./specs/
    - lobster spec complexity --max C

code_generation:
  needs: [spec_check]
  parallel:
    max_agents: 5
  script:
    - lobster codegen --spec ./specs/ --output ./src/

test:
  needs: [code_generation]
  script:
    - pytest --cov --cov-report=json
    - ruff check ./src/
    - mypy ./src/
    - bandit -r ./src/

auto_fix:
  needs: [test]
  when: on_failure
  max_retries: 3
  script:
    - lobster autofix --error-log ./test-results/errors.json
    - pytest --lf  # 只重跑失败的测试
  on_max_retries:
    - lobster issue create --from-error-log

quality_gate:
  needs: [test]
  checks:
    coverage: ">=80%"
    complexity: "<=B"
    security: "low"
    performance: "<=200ms p95"

release:
  needs: [quality_gate]
  script:
    - lobster changelog generate
    - git tag v$(lobster version next)
    - lobster artifact build
```

## 四、编程能力评分演进预测

| 子维度 | v2.0得分 | v3.0目标 | 提升来源 |
|--------|---------|---------|---------|
| 代码生成 | 90 | 92 | CI流水线+Spec质量校验 |
| 调试能力 | 85 | 88 | 自动修复闭环 |
| 重构能力 | 88 | 89 | SWE-bench持续跑分驱动 |
| 工程化交付 | 88 | 91 | 五阶段CI验证 |
| **编程综合** | **89** | **91** | **+2** |

## 五、与协议84/85/86的联动

| 新协议 | 联动点 | 价值 |
|--------|--------|------|
| 协议84 浏览器Agent | CI流水线可触发浏览器端到端测试 | UI层自动化验证 |
| 协议85 Tick订单流 | 策略代码CI包含回测精度验证 | 量化策略质量保障 |
| 协议86 跨市场套利 | 多市场数据源CI一致性校验 | 数据质量闭环 |

## 六、工程落地计划

| 阶段 | 内容 | 轮次 |
|------|------|------|
| P0 | CI流水线Stage1-3（Spec→Code→Test） | R26 |
| P0 | SWE-bench 5仓接入 + 首次跑分 | R27 |
| P1 | 自动修复闭环 + 质量门禁 | R28 |
| P1 | 与协议84/85/86联动验证 | R29 |
| P2 | 全维度编程能力验证报告 | R30 |

---

> **协议版本**：v3.0（由v2.0升级）
> **对标基准**：Codex SWE-bench (S级) / OpenCode Zen (A+级) / Qoder Quest 1.0 (A级)
> **协议编号**：#35（升级）
> **升级轮次**：R25
