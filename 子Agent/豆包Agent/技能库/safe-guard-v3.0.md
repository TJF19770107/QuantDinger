
# SafeGuard v3.0 — 自我修正与安全回滚能力

> 技能ID：SKILL_SAFE_GUARD_v3.0  
> 状态：ACTIVE  
> 创建：2026-05-31 R08（v2.0 升级至 v3.0）  
> 上一版本：v2.0 (R07)  
> 依赖：AutoFileScanner v1.0, MemoryOS v2.0  
> 被依赖：DesktopController v2.0, SkillForge v3.0, AutoWake v2.0, 自进化闭环

---

## 一、技能定位

SafeGuard 是豆包Agent的"免疫系统"，提供三层安全防护：事前审查（操作风险评估）、事中监控（异常实时检测）、事后恢复（自动回滚+崩溃恢复）。它是确保Agent在自主进化过程中不会"自我毁灭"的最后防线。

```
SafeGuard v3.0
    │
    ├── 事前审查 (Pre-execution)
    │   ├── 三级风险定级（🔴🟡🟢）
    │   ├── 操作白名单/黑名单
    │   └── 权限代理审查
    │
    ├── 事中监控 (In-execution)
    │   ├── 错误率监控
    │   ├── 文件变更监控
    │   ├── 性能下降检测
    │   └── 资源泄漏检测
    │
    └── 事后恢复 (Post-execution)
        ├── 自动回滚（基于检查点）
        ├── 崩溃恢复
        ├── 防误进化（新能力需测试通过）
        └── 安全护栏永久生效
```

---

## 二、核心能力（v3.0 增强项）

### 2.1 三级风险定级体系

```
🔴 高风险 → 必须二次确认 + 检查点快照
├── 格式化/清空存储、回收站
├── 批量破坏性操作（删友/退群/批量删除）
├── 系统关键项（注册表/服务/驱动）
├── 修改核心架构文件
└── 永久删除（绕过回收站）

🟡 中风险 → 需确认 + 审计日志
├── 覆盖/替换文件（无备份）
├── 配置变更（环境变量/启动项）
├── 终止非系统进程
├── 安装/卸载应用
└── AI自主判断的非破坏性变更

🟢 低风险 → 自动执行 + 记录日志
├── 只读操作（查询/列目录/读取文件）
├── 创建非系统文件/目录
├── 复制文件（不改原文件）
└── 无害的临时写入
```

### 2.2 异常自动检测引擎

```python
class AnomalyDetector:
    """多维度异常检测"""

    # 检测维度与阈值
    THRESHOLDS = {
        "error_rate": 0.3,         # 30秒内错误率超过30%
        "crash_count": 3,          # 3次连续崩溃
        "file_change_rate": 50,    # 单次操作修改超过50个文件
        "memory_spike_mb": 1024,   # 内存1分钟内暴增1GB
        "cpu_spike_percent": 90,   # CPU持续>90%超过60秒
        "disk_free_mb": 100,       # 磁盘空间<100MB
        "response_time_ms": 60000, # 单操作超过60秒
        "stall_time_ms": 300000,   # 5分钟无响应
    }

    def check_all(self, metrics: RuntimeMetrics) -> List[Alert]:
        """全维度异常检测。
        
        Returns:
            触发的告警列表（可能为空）
        """
        ...

    def should_rollback(self, alerts: List[Alert]) -> bool:
        """判断是否应触发自动回滚。"""
        ...
```

### 2.3 自动回滚机制

```
异常检测 → 触发规则匹配 → 定位目标检查点 → Diff对比 → 执行回滚 → 验证 → 记录
   |            |              |               |          |         |        |
Anomaly    AutoRollback   checkpoints/   变更清单   文件还原  冒烟测试  审计日志
Detector   Engine         stable.json    (可选)     (自动)    (自动)    (永久)
```

### 2.4 防误进化机制

```python
class EvolutionGuard:
    """防误进化：新能力必须通过测试才能合并"""
    
    GATE_CHECKS = [
        "safety_review",        # 安全审查通过
        "test_suite_pass",      # 测试套件全部通过
        "backward_compat",      # 向后兼容性检查
        "regression_test",      # 已有功能无退化
        "sandbox_validation",   # 沙箱环境验证通过
        "peer_review",          # 其他Agent交叉审查（可选）
    ]
    
    def validate_evolution(self, evolution: EvolutionCycle) -> GateResult:
        """进化门控：所有检查通过才允许合并。
        
        Args:
            evolution: SICA进化周期对象
        
        Returns:
            GateResult: {passed: bool, failed_checks: [...], recommendations: [...]}
        """
        ...
```

### 2.5 崩溃恢复

```python
class CrashRecovery:
    """崩溃恢复引擎"""
    
    def detect_crash(self) -> bool:
        """检测Agent是否崩溃。
        
        检测方法：
        1. 心跳日志超过2分钟未更新
        2. 任务队列中有超时未完成的任务
        3. 进程不存在但任务标记为运行中
        """
        ...
    
    def recover(self) -> RecoveryReport:
        """执行崩溃恢复。
        
        恢复步骤：
        1. 加载最后稳定检查点 (stable_checkpoint.json)
        2. 回滚未完成的任务到 pending 状态
        3. 重新加载 MemoryOS 最后记忆
        4. 执行冒烟测试（5个基础操作验证）
        5. 写入恢复日志
        """
        ...
    
    def smoke_test(self) -> bool:
        """冒烟测试：快速验证基础功能是否正常。
        
        测试项：
        - 读取一个已知文件
        - 写入一个临时文件
        - 查询任务队列
        - 读取心率日志
        - 获取系统信息
        """
        ...
```

---

## 三、接口定义

### 3.1 Python 类接口

```python
class SafeGuard:
    """安全护栏 v3.0"""

    def __init__(
        self,
        checkpoints_dir: str,            # checkpoints/ 目录
        auto_file_scanner=None,          # AutoFileScanner实例
        memory_os=None,                  # MemoryOS实例
        rules_path: str = None            # 自定义规则文件路径
    ):
        self.risk_engine = RiskEngine()              # 风险定级引擎
        self.anomaly_detector = AnomalyDetector()     # 异常检测器
        self.evolution_guard = EvolutionGuard()       # 防误进化
        self.crash_recovery = CrashRecovery()         # 崩溃恢复
        self.snapshot_mgr = SnapshotManager(checkpoints_dir)
        self.rollback_engine = AutoRollbackEngine(self.snapshot_mgr, rules_path)
        self.scanner = auto_file_scanner
        self.memory = memory_os

    # ========== 事前审查 ==========

    def assess_risk(self, action: Action) -> RiskAssessment:
        """评估操作风险等级。
        
        分析 action 的类型、目标路径、影响范围，
        返回风险等级和是否需要确认。
        
        Returns:
            RiskAssessment: {level: HIGH/MEDIUM/LOW, 
                             requires_confirmation: bool,
                             requires_snapshot: bool}
        """
        ...

    def review_operation(self, action: Action) -> ReviewResult:
        """审查操作是否允许执行。
        
        检查清单：
        1. 目标路径是否在系统禁区
        2. 操作类型是否在黑名单
        3. 是否需要快照备份
        4. 是否需要用户确认
        
        Returns:
            ReviewResult: {allowed: bool, reason: str, conditions: [...]}
        """
        ...

    def review_skill(self, skill_path: str) -> SecurityReview:
        """审查新技能文件的安全性（SkillForge联动）。
        
        检查项：
        - 技能描述中是否包含高风险操作
        - 依赖链是否完整且安全
        - 接口定义是否合理（无后门）
        - 权限声明与实际操作是否一致
        """
        ...

    # ========== 事中监控 ==========

    def monitor(self, metrics: RuntimeMetrics) -> MonitorReport:
        """实时监控运行指标。
        
        Returns:
            MonitorReport: {status: OK/WARNING/CRITICAL, 
                            alerts: [...], 
                            recommendation: ...}
        """
        ...

    def check_health(self) -> HealthReport:
        """执行健康检查（AutoWake定时触发）。
        
        检查项：
        - 磁盘空间 >100MB
        - 内存使用 <2GB
        - CPU使用 <90%
        - 任务队列无死锁
        - 检查点完整性
        """
        ...

    # ========== 事后恢复 ==========

    def auto_rollback(self, trigger: str, context: dict) -> RollbackResult:
        """自动回滚到上一个稳定版本。
        
        Args:
            trigger: 触发原因（如 "error_rate_exceeded"）
            context: 触发上下文
        
        Returns:
            RollbackResult: {success, snapshot_used, files_restored, verification}
        """
        ...

    def recover_from_crash(self) -> RecoveryReport:
        """崩溃恢复入口。"""
        return self.crash_recovery.recover()

    def create_safety_snapshot(self, reason: str) -> str:
        """创建安全快照（重大操作前自动调用）。
        
        Returns:
            snapshot_id
        """
        ...

    # ========== 进化防护 ==========

    def gate_evolution(self, evolution: EvolutionCycle) -> GateResult:
        """进化门控审查。"""
        return self.evolution_guard.validate_evolution(evolution)

    def verify_checkpoint_integrity(self, checkpoint_id: str) -> bool:
        """验证检查点完整性。"""
        return self.snapshot_mgr.verify_snapshot(checkpoint_id)["valid"]

    # ========== 审计 ==========

    def log_safety_event(self, event: SafetyEvent) -> None:
        """记录安全事件到 MemoryOS。"""
        ...

    def get_safety_report(self, hours: int = 24) -> SafetyReport:
        """生成安全报告。"""
        ...
```

### 3.2 数据结构

```python
@dataclass
class Action:
    action_type: str       # read/write/delete/execute/modify_config
    target_path: str       # 目标文件/目录路径
    params: dict           # 操作参数
    source: str            # 调用来源（skill名称）

@dataclass
class RiskAssessment:
    level: str             # HIGH / MEDIUM / LOW
    requires_confirmation: bool
    requires_snapshot: bool
    reasons: List[str]
    mitigations: List[str]

@dataclass
class ReviewResult:
    allowed: bool
    reason: str
    conditions: List[str]  # 允许条件（如 "先备份"）

@dataclass
class MonitorReport:
    status: str            # OK / WARNING / CRITICAL
    alerts: List[Alert]
    recommendation: str

@dataclass
class Alert:
    alert_id: str
    type: str              # error_rate/memory_spike/file_change/disk_low/stall
    severity: str          # WARNING / CRITICAL
    message: str
    timestamp: str
    metrics: dict

@dataclass
class RollbackResult:
    success: bool
    snapshot_id: str
    files_restored: int
    files_skipped: int
    verification: bool
    elapsed_ms: float

@dataclass
class RecoveryReport:
    success: bool
    detected_crash: bool
    snapshot_used: str
    tasks_reset: int
    smoke_test_passed: bool
    memory_reloaded: bool
    log: List[str]

@dataclass
class GateResult:
    passed: bool
    failed_checks: List[str]
    recommendations: List[str]
    overall_score: float

@dataclass
class RuntimeMetrics:
    error_rate: float
    memory_mb: float
    cpu_percent: float
    disk_free_mb: float
    active_tasks: int
    pending_tasks: int
    last_heartbeat: str
    file_changes_pending: int

@dataclass
class SafetyEvent:
    event_id: str
    type: str             # risk_assessment/anomaly_detected/rollback/evolution_gate
    severity: str
    description: str
    action_taken: str
    timestamp: str
```

---

## 四、自动回滚规则引擎

```json
{
  "rules": [
    {
      "id": "ARR_001",
      "trigger": "critical_error_rate",
      "condition": "error_rate > 0.3 AND active_tasks > 3",
      "action": "rollback_to_last_stable",
      "cooldown_seconds": 3600,
      "description": "错误率超过30%且活跃任务>3时自动回滚"
    },
    {
      "id": "ARR_002",
      "trigger": "memory_overflow",
      "condition": "memory_mb > 2048 AND memory_trend = 'increasing'",
      "action": "compress_memory_and_alert",
      "cooldown_seconds": 600,
      "description": "内存超过2GB且持续增长时压缩记忆"
    },
    {
      "id": "ARR_003",
      "trigger": "skill_degradation",
      "condition": "skill_success_rate < 0.3 AND skill_activation_count > 10",
      "action": "deactivate_skill_and_rollback",
      "cooldown_seconds": 7200,
      "description": "技能成功率低于30%时停用并回滚相关文件"
    },
    {
      "id": "ARR_004",
      "trigger": "file_corruption",
      "condition": "checksum_mismatch_on_critical_files",
      "action": "restore_from_snapshot",
      "cooldown_seconds": 0,
      "description": "关键文件校验失败时立即从快照恢复"
    },
    {
      "id": "ARR_005",
      "trigger": "disk_space_critical",
      "condition": "disk_free_mb < 100",
      "action": "compress_and_clean_temp",
      "cooldown_seconds": 300,
      "description": "磁盘空间<100MB时清理临时文件"
    },
    {
      "id": "ARR_006",
      "trigger": "agent_stall",
      "condition": "last_heartbeat_age_seconds > 300",
      "action": "crash_recovery",
      "cooldown_seconds": 60,
      "description": "心跳超过5分钟未更新时执行崩溃恢复"
    }
  ]
}
```

---

## 五、安全护栏永久生效机制

```python
class PermanentSafetyGuard:
    """永久安全护栏：不可跳过的最终防线"""
    
    IMMUTABLE_RULES = [
        "禁止格式化任何磁盘",
        "禁止删除系统目录文件",
        "禁止修改 .ssh / .env / 私钥文件",
        "禁止绕过 SafeGuard 审查",
        "禁止执行未经审查的 PowerShell 命令",
        "禁止修改 SafeGuard 自身的规则文件",
    ]
    
    def enforce(self, action: Action) -> EnforcementResult:
        """强制执行不可变规则。
        
        即使是 Agent 自身也不能修改这些规则，
        确保无论自进化到什么程度，核心安全约束永不失效。
        """
        for rule in self.IMMUTABLE_RULES:
            if self._violates(action, rule):
                return EnforcementResult(
                    allowed=False,
                    violated_rule=rule,
                    message=f"违反不可变安全规则: {rule}"
                )
        return EnforcementResult(allowed=True)
```

---

## 六、与其他技能的接口契约

| 调用方 | 被调用方 | 接口 | 触发时机 |
|--------|---------|------|---------|
| DesktopController | SafeGuard | `review_operation(action)` | 每次桌面操作前 |
| SkillForge | SafeGuard | `review_skill(path)` | 新技能生成后 |
| AutoWake | SafeGuard | `check_health()` | 每小时安全检查 |
| SICA Evolver | SafeGuard | `gate_evolution(cycle)` | 进化合并前 |
| 自进化闭环 | SafeGuard | `create_safety_snapshot()` | 重大操作前 |
| 所有Skill | SafeGuard | `assess_risk(action)` | 高风险操作前 |

---

## 七、崩溃恢复流程图

```
检测到崩溃（心跳超时 / 任务超时）
         │
         ▼
   加载最后检查点 ← stable_checkpoint.json
         │
         ▼
   回滚未完成任务 → 状态设为 pending
         │
         ▼
   重新加载 MemoryOS → 从 memory/ 加载记忆
         │
         ▼
   执行冒烟测试（5项） → 基础功能验证
         │
    ┌────┴────┐
    ▼         ▼
  通过      失败
    │         │
    ▼         ▼
  恢复正常  降级模式
  记录日志  通知用户
           手动介入
```

---

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | R04 | 初始版本：基础安全审查 |
| v2.0 | R07 | 增强：自动回滚规则引擎 + 检查点快照增强 |
| v3.0 | R08 | 增强：三级风险定级体系、异常自动检测、防误进化门控、崩溃恢复、永久安全护栏 |
