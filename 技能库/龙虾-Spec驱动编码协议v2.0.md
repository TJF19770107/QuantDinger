# Spec驱动编码协议 v2.0（CI验证流水线升级）

> **协议编号**：35（升级）
> **版本**：v1.0 → v2.0
> **创建日期**：2026-05-31（v1.0）→ 2026-06-01（v2.0）
> **对标来源**：Qoder Quest 1.0（v1.0）+ Codex Triggers自动修复+开PR（v2.0升级）
> **升级目标**：从"Spec→代码生成"单向流程升级为"Spec→生成→CI测试→自动修复→PR→合并"全闭环验证
> **编程能力目标**：88→89+

---

## 一、v1.0 → v2.0 升级总览

| 组件 | v1.0（R08） | v2.0（R25） | 升级来源 |
|------|-----------|-----------|---------|
| **技术规约生成** | ✅ 已实现 | ✅ 保留 | Qoder Quest 1.0 |
| **多子Agent并行探索** | ✅ 已实现 | ✅ 保留 | Qoder Quest |
| **代码择优** | ✅ 已实现 | ✅ 保留 | Qoder Quest |
| **CI自动化测试** | ❌ 未实现 | ✅ **新增** | Codex Triggers |
| **失败自动修复** | ❌ 未实现 | ✅ **新增** | 协议18自愈编码 |
| **自动开PR** | ❌ 未实现 | ✅ **新增** | Codex PR工作流 |
| **合并前Review** | ❌ 未实现 | ✅ **新增** | Hermes Review Fork |
| **持续版本发布** | ❌ 未实现 | ✅ **新增** | CI/CD最佳实践 |

---

## 二、CI验证流水线架构

```
                          ┌─────────────────────────────┐
                          │     技术规约生成（Spec）       │
                          │     协议35 v1.0 原有能力      │
                          └─────────────┬───────────────┘
                                        ↓
              ┌─────────────────────────────────────────────────┐
              │            多子Agent并行代码生成                   │
              │     Agent A    Agent B    Agent C    Agent D     │
              │     (Python)   (Go)      (Rust)     (JS)        │
              └─────────────────────────┬───────────────────────┘
                                        ↓
              ┌─────────────────────────────────────────────────┐
              │              CI验证流水线 【v2.0新增】            │
              │  ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
              │  │ Lint检查  │→│ 单元测试  │→│ 集成/端到端测试│  │
              │  └──────────┘ └──────────┘ └───────────────┘  │
              │  ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
              │  │ 性能基准  │→│ 安全扫描  │→│ 覆盖率检查     │  │
              │  └──────────┘ └──────────┘ └───────────────┘  │
              └─────────────────────────┬───────────────────────┘
                                        ↓
                    ┌────────────────────────────────────┐
                    │        CI结果决策 【v2.0新增】       │
                    │  通过？→ 自动开PR → 合并            │
                    │  失败？→ 自愈修复 → 重跑CI          │
                    │  反复失败(≥3次)？→ 人工介入         │
                    └────────────────────────────────────┘
```

---

## 三、CI流水线核心配置

### 3.1 GitHub Actions / 通用CI配置

```yaml
# .github/workflows/agent-ci-pipeline.yml
name: Agent CI Verification Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  # Codex Triggers 触发
  repository_dispatch:
    types: [agent-code-generated]

jobs:
  lint:
    name: Lint检查
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Python Lint
        run: |
          pip install ruff black mypy
          ruff check .
          black --check .
      - name: Shell Lint
        run: |
          shfmt -d .
          shellcheck *.sh

  unit-test:
    name: 单元测试
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest --cov=. --cov-report=json --junitxml=test-results.xml
      - name: Coverage check
        run: |
          COVERAGE=$(python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])")
          if [ "$COVERAGE" -lt 80 ]; then
            echo "❌ Coverage $COVERAGE% < 80% threshold"
            exit 1
          fi

  integration-test:
    name: 集成测试
    needs: unit-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Integration tests
        run: pytest tests/integration/ -v

  performance-benchmark:
    name: 性能基准测试
    needs: unit-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Benchmark
        run: |
          python -m pytest tests/benchmarks/ --benchmark-json=benchmark.json
      - name: Compare baseline
        run: python scripts/compare_benchmark.py benchmark.json

  security-scan:
    name: 安全扫描
    needs: unit-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Bandit scan
        run: bandit -r . -f json -o security-report.json
      - name: Check critical issues
        run: python scripts/check_security.py security-report.json

  auto-fix:
    name: 自动修复 【v2.0核心新增】
    needs: [lint, unit-test, integration-test, performance-benchmark, security-scan]
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: AI Self-heal
        run: |
          python scripts/ai_self_heal.py \
            --errors-from "test-results.xml,security-report.json" \
            --max-attempts 3 \
            --auto-commit
      - name: Re-run CI after fix
        uses: ./.github/actions/trigger-self-test

  auto-pr:
    name: 自动开PR 【v2.0核心新增】
    needs: [unit-test, integration-test, performance-benchmark, security-scan]
    if: success()
    runs-on: ubuntu-latest
    steps:
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          title: "🤖 [Agent Auto] Spec驱动的代码生成 - $(date +%Y%m%d-%H%M)"
          body: |
            ## 自动生成的代码PR
            
            **技术规约**：[spec链接]
            **生成时间**：$(date)
            **CI验证**：✅ 全部通过
            
            ### 测试结果
            - Lint：✅
            - 单元测试：✅ (覆盖率: XX%)
            - 集成测试：✅
            - 性能基准：✅
            - 安全扫描：✅
            
            ---
            *本PR由Agent自动创建，CI已验证通过*
          branch: agent-code-$(date +%Y%m%d-%H%M)
          delete-branch: true
```

### 3.2 自愈修复引擎

```python
#!/usr/bin/env python3
"""AI Self-Healing Engine - 从CI失败中自动修复代码"""
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict

class SelfHealingEngine:
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.attempt = 0
        self.fix_history = []
    
    def load_errors(self, test_results_path: str, security_report_path: str) -> List[Dict]:
        """加载CI流程中产生的错误"""
        errors = []
        
        # 解析测试失败
        if Path(test_results_path).exists():
            with open(test_results_path) as f:
                test_data = json.load(f)
                for suite in test_data.get('testsuites', []):
                    for case in suite.get('testcases', []):
                        if case.get('failure'):
                            errors.append({
                                'type': 'TEST_FAILURE',
                                'file': case.get('classname', '').replace('.', '/') + '.py',
                                'test': case.get('name'),
                                'message': case['failure'].get('message', ''),
                                'traceback': case['failure'].get('text', '')
                            })
        
        # 解析安全漏洞
        if Path(security_report_path).exists():
            with open(security_report_path) as f:
                sec_data = json.load(f)
                for issue in sec_data.get('results', []):
                    if issue.get('issue_severity') in ['HIGH', 'MEDIUM']:
                        errors.append({
                            'type': 'SECURITY_ISSUE',
                            'file': issue.get('filename'),
                            'line': issue.get('line_number'),
                            'issue': issue.get('issue_text'),
                            'severity': issue.get('issue_severity')
                        })
        
        return errors
    
    def analyze_error(self, error: Dict) -> str:
        """分析错误根因"""
        if error['type'] == 'TEST_FAILURE':
            return self._analyze_test_failure(error)
        elif error['type'] == 'SECURITY_ISSUE':
            return self._analyze_security_issue(error)
        return "unknown error type"
    
    def generate_fix(self, error: Dict, source_code: str) -> str:
        """生成修复代码"""
        if error['type'] == 'TEST_FAILURE':
            return self._fix_test_failure(error, source_code)
        elif error['type'] == 'SECURITY_ISSUE':
            return self._fix_security_issue(error, source_code)
        return source_code
    
    def apply_and_verify(self, file_path: str, fixed_code: str, test_command: str) -> bool:
        """应用修复并验证"""
        # 备份原文件
        backup = file_path + '.bak'
        Path(file_path).rename(backup)
        
        # 写入修复代码
        with open(file_path, 'w') as f:
            f.write(fixed_code)
        
        # 运行测试验证
        result = subprocess.run(test_command, shell=True, capture_output=True)
        
        if result.returncode == 0:
            self.fix_history.append({
                'file': file_path,
                'attempt': self.attempt,
                'success': True
            })
            return True
        else:
            # 恢复原文件
            Path(backup).rename(file_path)
            return False
    
    def run(self, errors_file: str) -> bool:
        """主运行循环：解析错误→分析→修复→验证"""
        errors = self.load_errors(errors_file, errors_file.replace('test', 'security'))
        
        if not errors:
            print("✅ No errors found, skipping auto-fix")
            return True
        
        fixed_count = 0
        for error in errors:
            while self.attempt < self.max_attempts:
                self.attempt += 1
                print(f"🔧 Attempt {self.attempt}/{self.max_attempts} for {error['file']}")
                
                # 读取源码
                with open(error['file'], 'r') as f:
                    source = f.read()
                
                # 生成修复
                fixed = self.generate_fix(error, source)
                
                # 应用并验证
                if self.apply_and_verify(error['file'], fixed, 
                                        f"pytest {error.get('test', error['file'])} -v"):
                    fixed_count += 1
                    break
                else:
                    print(f"❌ Fix attempt {self.attempt} failed")
            
            if self.attempt >= self.max_attempts:
                print(f"⚠️ Max attempts reached for {error['file']}, manual intervention needed")
                return False
            
            self.attempt = 0  # Reset for next error
        
        print(f"✅ Auto-fixed {fixed_count}/{len(errors)} errors")
        return True

if __name__ == '__main__':
    engine = SelfHealingEngine()
    success = engine.run(sys.argv[2])  # --errors-from 文件
    sys.exit(0 if success else 1)
```

---

## 四、集成测试验证矩阵

### 4.1 测试层级

| 层级 | 测试类型 | 覆盖目标 | 失败时自愈策略 |
|------|---------|---------|--------------|
| **L1: 单元测试** | pytest/unittest | 每个函数/类 ≥80% | 修改函数实现 |
| **L2: 集成测试** | 模块间接口测试 | 核心流程100%覆盖 | 修改接口适配 |
| **L3: 端到端测试** | 用户故事级测试 | 关键路径 | 需要人工Review |
| **L4: 性能基准** | 基准回归 | 性能不退化>5% | 重写热点路径 |
| **L5: 安全扫描** | Bandit/SonarQube | 零高危漏洞 | 移除危险代码 |

### 4.2 性能基准阈值

```yaml
performance_baselines:
  api_response_time:
    p50: 50ms
    p95: 200ms
    p99: 500ms
    degradation_tolerance: 5%
  
  memory_usage:
    baseline: 256MB
    peak: 512MB
    degradation_tolerance: 10%
  
  cpu_usage:
    idle: 5%
    load: 70%
    spike_tolerance: 15%
```

---

## 五、与其他协议联动

| 协议 | 联动点 | 作用 |
|------|--------|------|
| **协议18 自愈编码闭环** | CI失败→自愈修复循环 | 生成→测试→报错→修复→重跑 |
| **协议54 百级并行** | 多代码方案并行生成+并行CI | 提升生成效率 |
| **协议61 置信度验收** | CI结果置信度评分 | 低分方案不进入PR |
| **协议74 源码级元重写** | 从CI错误直接修改Python源码 | 自愈修复核心引擎 |
| **协议62 三阶段架构** | Phase1编码→Phase2 CI验证→Phase3发布 | 协议映射到CI阶段 |

---

## 六、验收标准

### 6.1 CI流水线达标条件

| 检查项 | 阈值 | 不达标处理 |
|--------|------|-----------|
| Lint检查 | 0 错误 | 尝试自动格式修复 |
| 单元测试通过率 | 100% | 自愈修复（最多3次） |
| 代码覆盖率 | ≥80% | 生成补充测试用例 |
| 集成测试通过率 | 100% | 人工介入 |
| 安全扫描 | 0 高危 | 自动移除高危代码 |
| 性能退化 | ≤5% | 回滚+重生成 |

### 6.2 编程能力闭环验证指标

| 指标 | v1.0 | v2.0目标 |
|------|------|---------|
| CI自动化率 | 0% | ≥90% |
| 自愈成功率 | N/A | ≥70% |
| PR自动合并率 | N/A | ≥80% |
| 从生成到合并延迟 | 不可测 | ≤30分钟 |
| 代码质量稳定性 | 不可测 | ≥95%通过率 |

---

## 七、预期效果

| 维度 | 影响 | 提升 |
|------|------|------|
| **编程能力** | CI验证+自愈修复闭环 | 88→89+ |
| **工程化交付** | 自动PR+合并 | +2分 |
| **自愈回滚** | CI失败自动修复 | +1分 |
| **综合加权** | — | +0.2 |

---

> **协议状态**：v2.0 已升级  
> **升级来源**：协议35 v1.0 + Codex Triggers + 协议18自愈编码  
> **创建时间**：2026-06-01 17:25  
> **升级项编号**：U135
> **编程能力**：88→89（+1）