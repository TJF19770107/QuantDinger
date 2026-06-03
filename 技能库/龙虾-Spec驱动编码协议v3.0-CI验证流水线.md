# 龙虾-Spec驱动编码协议 v3.0（CI验证流水线升级）

> **协议编号**：#35
> **版本**：v3.0（升级自 v2.0 / v1.0 R08）
> **升级日期**：2026-06-02
> **触发**：R25 P0第三项 — 协议→工程化落地鸿沟攻坚
> **对标来源**：Codex Triggers自动修复+开PR + SWE-bench + OpenCode Zen 120K★
> **核心升级**：增加CI持续集成验证流水线，消除协议设计与工程落地断层

---

## 一、升级背景

### 1.1 问题诊断（R25报告）

| 维度 | R25评分 | 核心瓶颈 |
|------|--------|---------|
| 编程能力-工程化交付 | 88/100 | 协议多但缺少真实代码仓持续跑分验证 |
| 协议→工程化落地 | — | 83项协议中80%停留在设计文档阶段 |

**根因**：协议35 v2.0定义了生成技术规约+多子Agent并行探索，但缺少将规约自动编译为可执行代码、并在CI流水线中持续验证的闭环机制。

### 1.2 v1.0 → v2.0 → v3.0 演进

| 版本 | 轮次 | 核心能力 | 局限性 |
|------|------|---------|--------|
| v1.0 (R08) | #35 | 生成技术规约 + 多子Agent并行探索 + 择优 | 规约与代码脱节 |
| v2.0 (R24) | #35升级 | 规约→代码自动生成 + 单元测试 | 无CI持续验证 |
| **v3.0 (R25)** | #35升级 | **+ CI验证流水线 + SWE-bench跑分 + PR自动修复** | — |

---

## 二、CI验证流水线架构

```
┌─────────────────────────────────────────────────────────────────┐
│               Spec驱动编码 CI验证流水线 v3.0                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: Spec生成 (Spec Generation)                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 用户需求 → Spec文档（协议/接口/测试用例/验收标准）        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ↓                                       │
│  Stage 2: 代码生成 (Code Generation)                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Spec → 多子Agent并行编码 → Arena竞技场择优 → 代码产出    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ↓                                       │
│  Stage 3: CI验证流水线 (CI Pipeline) 【v3.0新增】               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │ 静态检查 │→│ 单元测试 │→│ 集成测试 │→│ 跑分   │ │   │
│  │  │ Lint     │  │ Pytest   │  │ 端到端   │  │ Benchmark│ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  │                         ↓                               │   │
│  │               ┌──────────┐  ┌──────────────┐           │   │
│  │               │ 自动修复 │→│ PR/Report     │           │   │
│  │               │ Self-heal│  │ 自动提交      │           │   │
│  │               └──────────┘  └──────────────┘           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ↓                                       │
│  Stage 4: 结果反馈 (Feedback Loop) 【v3.0新增】                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  CI结果 → 协议自进化引擎 → Spec优化 → 重新进入Stage 1    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、CI流水线详细配置

### 3.1 Stage 3.1：静态检查 (Lint & Type Check)

```yaml
# .github/workflows/ci-lint.yml
name: CI - Static Analysis
on:
  push:
    branches: [main, 'spec/**']
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install ruff mypy black isort

      - name: Ruff Lint
        run: ruff check . --output-format=github

      - name: Ruff Format Check
        run: ruff format --check .

      - name: Black Check
        run: black --check --diff .

      - name: isort Check
        run: isort --check-only --diff .

      - name: MyPy Type Check
        run: mypy src/ --strict
```

### 3.2 Stage 3.2：单元测试 (Unit Tests)

```yaml
# .github/workflows/ci-test.yml
name: CI - Unit Tests
on:
  push:
    branches: [main, 'spec/**']
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run Tests
        run: pytest tests/ -v --cov=src --cov-report=xml --cov-report=html -n auto

      - name: Coverage Check (≥85%)
        run: |
          coverage=$(python -c "import xml.etree.ElementTree as ET; tree=ET.parse('coverage.xml'); print(tree.getroot().get('line-rate'))")
          if (( $(echo "$coverage < 0.85" | bc -l) )); then
            echo "Coverage $coverage below 85% threshold"
            exit 1
          fi

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

### 3.3 Stage 3.3：集成测试 (Integration / E2E)

```yaml
# .github/workflows/ci-integration.yml
name: CI - Integration Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run Integration Tests
        run: pytest tests/integration/ -v --timeout=300

      - name: Run E2E Tests
        run: pytest tests/e2e/ -v --timeout=600
```

### 3.4 Stage 3.4：SWE-bench跑分 (Benchmark)

```yaml
# .github/workflows/ci-benchmark.yml
name: CI - SWE-bench Benchmark
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 */6 * * *'  # 每6小时自动跑分

jobs:
  benchmark:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v4

      - name: Setup SWE-bench
        run: |
          git clone https://github.com/princeton-nlp/SWE-bench.git
          cd SWE-bench
          pip install -e .

      - name: Run SWE-bench Lite
        run: |
          python -m swebench.harness.run_evaluation \
            --dataset_name princeton-nlp/SWE-bench_Lite \
            --predictions_path predictions.json \
            --max_workers 4 \
            --run_id lobster_agent_$(date +%Y%m%d_%H%M) \
            --timeout 900

      - name: Parse Results
        run: |
          python scripts/parse_swebench_results.py \
            --output benchmark_results.json

      - name: Upload Benchmark Results
        uses: actions/upload-artifact@v4
        with:
          name: swebench-results
          path: benchmark_results.json

      - name: Check Score Regression
        run: |
          python scripts/check_regression.py \
            --current benchmark_results.json \
            --baseline baseline_results.json \
            --threshold -2.0
```

### 3.5 Stage 3.5：自动修复 (Self-healing)

```yaml
# .github/workflows/ci-auto-fix.yml
name: CI - Auto Fix & PR
on:
  workflow_run:
    workflows: ["CI - Static Analysis", "CI - Unit Tests"]
    types: [completed]

jobs:
  auto-fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_branch }}

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install ruff black isort

      - name: Auto-fix Lint Issues
        run: |
          ruff check --fix .
          black .
          isort .

      - name: Create Auto-fix PR
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: "🤖 [Auto-fix] CI lint/test failures auto-repair"
          title: "🤖 Auto-fix: CI pipeline failures"
          body: |
            ## Auto-fix Summary
            This PR was automatically generated to fix CI pipeline failures.

            ### Fixed Issues:
            - Ruff lint errors
            - Black formatting
            - isort import ordering

            ### CI Status:
            - Triggered by: ${{ github.event.workflow_run.name }}
            - Branch: ${{ github.event.workflow_run.head_branch }}

            Please review and merge if the fixes are correct.
          branch: auto-fix/ci-repairs
          delete-branch: true
          labels: |
            automated
            ci-fix
```

---

## 四、协议规范升级

### 4.1 Spec文档模板升级

```yaml
# spec.yaml — 工程规约定义文件
name: "user-auth-service"
version: "1.0.0"
spec_version: "3.0"  # v3.0新增字段

# === v3.0新增：CI验证配置 ===
ci:
  lint:
    tools: [ruff, mypy, black, isort]
    strict_mode: true
  test:
    framework: pytest
    min_coverage: 85
    matrix:
      os: [ubuntu-latest, windows-latest]
      python: ['3.11', '3.12']
  integration:
    e2e_tests: true
    timeout_seconds: 600
  benchmark:
    dataset: SWE-bench_Lite
    min_resolve_rate: 25.0
    max_regression: -2.0

# === 原有字段 ===
interfaces:
  - name: "POST /auth/login"
    method: POST
    path: "/auth/login"
    request:
      body:
        username: {type: string, required: true}
        password: {type: string, required: true, min_length: 8}
    response:
      200:
        body:
          token: {type: string}
          expires_in: {type: integer}
    tests:
      - name: "login_success"
        input: {username: "test@example.com", password: "ValidP@ss1"}
        expect: {status: 200}
      - name: "login_invalid_password"
        input: {username: "test@example.com", password: "short"}
        expect: {status: 401}
      - name: "login_missing_field"
        input: {username: "test@example.com"}
        expect: {status: 400}

acceptance_criteria:
  - "所有API端点返回正确的HTTP状态码"
  - "单元测试覆盖率 ≥ 85%"
  - "SWE-bench Lite resolve rate ≥ 25%"
  - "无critical/high安全漏洞"
```

### 4.2 代码生成增强

```python
# spec_codegen_v3.py — v3.0增强代码生成器
class SpecDrivenCodeGeneratorV3:
    """v3.0：带CI验证的Spec驱动代码生成器"""

    def generate_from_spec(self, spec_path: str) -> GeneratedProject:
        """
        从Spec文件生成完整项目，包括：
        1. 源代码（v2.0能力）
        2. 单元测试（v2.0能力）
        3. CI流水线配置（v3.0新增）
        4. Dockerfile/DevContainer（v3.0新增）
        5. SWE-bench跑分配置（v3.0新增）
        """
        spec = self._load_spec(spec_path)

        project = GeneratedProject(
            source_code=self._generate_source(spec),
            tests=self._generate_tests(spec),
            ci_pipeline=self._generate_ci_config(spec),       # NEW v3.0
            docker=self._generate_docker_config(spec),        # NEW v3.0
            benchmark=self._generate_benchmark_config(spec),  # NEW v3.0
        )

        # v3.0: 自动运行CI验证
        if spec.get('ci', {}).get('auto_validate', True):
            result = self._run_ci_pipeline(project)
            if not result.passed:
                project = self._auto_fix_and_retry(project, result)

        return project

    def _generate_ci_config(self, spec: dict) -> CIConfig:
        """根据Spec生成GitHub Actions CI配置"""
        ci_spec = spec.get('ci', {})

        workflows = []

        # 静态检查
        if ci_spec.get('lint'):
            workflows.append(self._gen_lint_workflow(ci_spec['lint']))

        # 单元测试
        if ci_spec.get('test'):
            workflows.append(self._gen_test_workflow(ci_spec['test']))

        # 集成测试
        if ci_spec.get('integration'):
            workflows.append(self._gen_integration_workflow(ci_spec['integration']))

        # Benchmark
        if ci_spec.get('benchmark'):
            workflows.append(self._gen_benchmark_workflow(ci_spec['benchmark']))

        # 自动修复
        workflows.append(self._gen_autofix_workflow())

        return CIConfig(workflows=workflows)

    def _auto_fix_and_retry(self, project, ci_result) -> GeneratedProject:
        """自动修复CI失败 + 重试（最多3次）"""
        for attempt in range(3):
            fixes = self._analyze_failures(ci_result)
            project = self._apply_fixes(project, fixes)
            ci_result = self._run_ci_pipeline(project)
            if ci_result.passed:
                break
        return project
```

---

## 五、运行日志与评分体系

### 5.1 CI运行日志格式

```json
{
  "run_id": "ci_run_20260602_120000",
  "spec_name": "user-auth-service",
  "spec_version": "1.0.0",
  "protocol_version": "3.0",
  "timestamp": "2026-06-02T12:00:00Z",
  "stages": {
    "lint": {
      "status": "passed",
      "duration_seconds": 45,
      "details": {
        "ruff": {"errors": 0, "warnings": 0},
        "mypy": {"errors": 0},
        "black": {"files_reformatted": 0}
      }
    },
    "unit_test": {
      "status": "passed",
      "duration_seconds": 120,
      "details": {
        "total": 156,
        "passed": 156,
        "failed": 0,
        "coverage": 89.3
      }
    },
    "integration": {
      "status": "passed",
      "duration_seconds": 340,
      "details": {
        "total": 12,
        "passed": 12,
        "failed": 0
      }
    },
    "benchmark": {
      "status": "passed",
      "duration_seconds": 1800,
      "details": {
        "swebench_lite_resolve_rate": 28.5,
        "baseline": 26.0,
        "delta": 2.5,
        "regression": false
      }
    }
  },
  "overall_status": "passed",
  "programming_score": {
    "code_generation": 91,
    "test_coverage": 89,
    "benchmark_performance": 28.5,
    "engineering_maturity": 90
  }
}
```

### 5.2 编程能力评分联动

| CI指标 | 对应维度 | 评分影响 |
|--------|---------|---------|
| Lint通过率 | 代码质量 | <100%→扣分 |
| 测试覆盖率 | 调试能力 | <85%→每降1%扣0.5分 |
| 集成测试通过率 | 工程化交付 | <100%→每失败1个扣1分 |
| SWE-bench resolve rate | 代码生成 | >25%→加分 |
| 自动修复成功率 | 自愈能力 | >80%→加分 |
| 回归检测通过 | 稳定性 | 回归→扣2分 |

### 5.3 编程能力评分目标

| 指标 | R25基线 | R28目标 | R33目标 |
|------|--------|--------|--------|
| 代码生成 | 90 | 91 | 93 |
| 调试能力 | 85 | 87 | 90 |
| 重构能力 | 88 | 89 | 91 |
| 工程化交付 | 88 | 90 | 92 |
| SWE-bench Lite | — | ≥25% | ≥30% |
| CI自动修复率 | — | ≥60% | ≥80% |

---

## 六、与现有协议的协同

| 协议 | 协同方式 | 说明 |
|------|---------|------|
| 协议18 自愈式编码闭环 | 自动修复链路 | CI失败→自愈修复→重跑 |
| 协议7 自进化编码闭环 | 评分驱动进化 | SWE-bench评分→淘汰弱方案 |
| 协议8 Arena竞技场协议 | 多方案择优 | 多子Agent并行生成→benchmark择优 |
| 协议41 协议化闭环自进化 | 协议评估 | CI结果→协议优化建议 |
| 协议46 源码级自进化安全 | 安全约束 | 自动修复前安全检查 |
| 协议62 三阶段渐进式架构 | 分阶段推进 | Phase1夯实编码→Phase2架构升级 |

---

> **协议版本**：v3.0
> **升级日期**：2026-06-02
> **升级来源**：R25 P0第三项 — Codex Triggers自动修复+开PR
> **状态**：设计规范完成 → 待GitHub Actions实际部署
> **下一步**：R29在真实代码仓中部署CI流水线并跑分
> **归属**：龙虾全域技能协议体系 #35 v3.0
