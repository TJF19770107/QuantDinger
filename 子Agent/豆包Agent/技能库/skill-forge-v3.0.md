
# SkillForge v3.0 — 自主技能生成能力

> 技能ID：SKILL_SKILL_FORGE_v3.0  
> 状态：ACTIVE  
> 创建：2026-05-31 R08（v2.0 升级至 v3.0）  
> 上一版本：v2.0 (R07)  
> 依赖：AutoFileScanner v1.0, MemoryOS v2.0, SafeGuard v3.0  
> 被依赖：自进化闭环, SICA Evolver

---

## 一、技能定位

SkillForge 是豆包Agent的技能工厂，负责从迭代报告、执行日志、成功模式中自动提炼新技能、生成标准化 SKILL.md 文件、注册到技能库、管理版本生命周期。它是自进化闭环中「技能沉淀」环节的核心执行者。

```
执行日志 / 迭代报告 / 缺口清单
         │
         ▼
    SkillForge v3.0
         │
    ┌────┼────┬──────────┐
    ▼    ▼    ▼          ▼
  提炼  生成  审查      注册
  模式  SKILL  SafeGuard capabilities.json
         │
         ▼
    AutoFileScanner ──→ 确认入库
         │
         ▼
    MemoryOS ──→ 记录技能变化
```

---

## 二、核心能力（v3.0 增强项相对 v2.0）

### 2.1 模式识别引擎

| 模式类型 | 触发条件 | 萃取路径 |
|---------|---------|---------|
| 成功模式 | 同类任务 ≥3 次成功执行 | 提取最优参数组合 + 执行路径编码为模板 |
| 失败模式 | ≥2 次同类失败 | 提取失败原因 + 绕行方案 + 前置检查清单 |
| 高效模式 | 执行耗时 < 历史均值 50% | 提取加速技巧 + 快捷路径 |
| 协作模式 | 多Agent协同完成 | 提取 Agent 编排模板 + 数据流 DAG |

### 2.2 自动SKILL.md生成

从迭代报告自动提取技能描述，按标准模板生成：

```markdown
# {skill_name} v{version} — {简短描述}

> 技能ID：SKILL_{NAME}_v{version}
> 状态：ACTIVE
> 创建：{date} R{round}
> 依赖：{deps}
> 被依赖：{rev_deps}

## 一、技能定位
{自动从迭代报告摘要提取}

## 二、核心能力
{自动从能力矩阵提取}

## 三、接口定义
{自动从代码骨架提取函数签名}

## 四、使用方式
{自动从执行日志提取示例}

## 五、安全约束
{自动继承 SafeGuard 规则}

## 六、版本历史
{自动追加版本记录}
```

### 2.3 自动注册到 capabilities.json

```json
{
  "capabilities": {
    "SKILL_{NAME}_v{version}": {
      "name": "{skill_name}",
      "version": "{version}",
      "file": "技能库/{file_name}.md",
      "status": "ACTIVE",
      "dependencies": ["...", "..."],
      "registered_at": "2026-05-31T12:30:00",
      "registered_by": "SkillForge v3.0"
    }
  }
}
```

### 2.4 技能版本管理

```
v1.0 → v2.0 → v3.0 → ...
  │      │      │
  └── 旧版本自动标记为 DEPRECATED
  └── 保留历史版本文件（技能库/archive/）
  └── MemoryOS 记录版本演变历程
```

### 2.5 技能去重检查

```python
def check_duplicate(new_skill: SkillMetadata, existing_skills: List[SkillMetadata]) -> DuplicateReport:
    """三重去重检查：
    1. 名称相似度 > 0.85 → 疑似重复
    2. 关键词重叠率 > 0.7 → 可能合并
    3. 依赖关系高度同构 → 建议升级现有技能
    """
    ...
```

---

## 三、接口定义

### 3.1 Python 类接口

```python
class SkillForge:
    """自主技能生成工厂 v3.0"""

    def __init__(
        self,
        skill_lib_dir: str,         # 技能库目录路径
        auto_file_scanner=None,     # AutoFileScanner实例
        memory_os=None,             # MemoryOS实例
        safe_guard=None             # SafeGuard实例
    ):
        self.skill_dir = Path(skill_lib_dir)
        self.archive_dir = self.skill_dir / "archive"
        self.scanner = auto_file_scanner
        self.memory = memory_os
        self.safe_guard = safe_guard
        self.capabilities_path = self.skill_dir.parent / "capabilities.json"

    # ========== 技能萃取 ==========

    def extract_from_iteration(self, report_path: str) -> List[SkillBlueprint]:
        """从迭代报告中提取潜在技能。
        
        解析报告中的「能力注入」「缺口分析」章节，
        提取未覆盖的能力项作为新技能蓝图。
        
        Args:
            report_path: R07/R08等迭代报告路径
        
        Returns:
            技能蓝图列表，每个包含 name/description/deps/code_skeleton
        """
        ...

    def extract_from_evolution(self, cycle: EvolutionCycle) -> Optional[SkillBlueprint]:
        """从SICA进化周期中提取新技能（成功进化→技能沉淀）。
        
        Args:
            cycle: SICAEvolver产生的进化周期对象
        
        Returns:
            如果质量评分 >= 阈值，返回技能蓝图；否则 None
        """
        ...

    def extract_from_execution_log(self, log_path: str) -> List[SkillBlueprint]:
        """从执行日志中挖掘可复用的成功模式。
        
        分析日志中的重复成功路径，识别高频操作组合，
        编码为标准化技能模板。
        """
        ...

    # ========== 技能生成 ==========

    def generate_skill_md(self, blueprint: SkillBlueprint) -> str:
        """根据蓝图生成完整的 SKILL.md 文本。
        
        自动填充标准模板的所有章节：
        定位 → 能力 → 接口 → 使用 → 安全 → 版本
        
        Returns:
            完整的 Markdown 文本
        """
        ...

    def save_skill(self, skill_md_text: str, file_name: str) -> str:
        """将生成的 SKILL.md 保存到技能库目录。
        
        自动处理：
        - 目录创建
        - 文件名冲突（添加数字后缀）
        - 编码统一 UTF-8
        
        Returns:
            保存的绝对路径
        """
        ...

    # ========== 技能注册 ==========

    def register_to_capabilities(self, skill_path: str, blueprint: SkillBlueprint) -> bool:
        """将新技能注册到 capabilities.json。
        
        - 解析 SKILL.md 的 Front Matter
        - 追加到 capabilities.json 并去重
        - 通知 AutoFileScanner 重新索引
        """
        ...

    # ========== 版本管理 ==========

    def upgrade_skill(self, skill_name: str, changes: str) -> str:
        """升级现有技能到下一版本。
        
        1. 读取当前版本
        2. 计算新版本号 (vX.0 → vX+1.0)
        3. 归档旧版本到 archive/
        4. 生成新 SKILL.md
        5. 更新 capabilities.json
        """
        ...

    def deprecate_skill(self, skill_name: str, reason: str) -> bool:
        """弃用技能，标记为 DEPRECATED，不移除文件。"""
        ...

    # ========== 去重与审查 ==========

    def check_duplicate(self, blueprint: SkillBlueprint) -> DuplicateReport:
        """检查新技能是否与已有技能重复。
        
        返回详情：
        - duplicate_confidence: 0-1
        - similar_skills: 相似技能列表
        - recommendation: "create_new" / "upgrade_existing" / "merge"
        """
        ...

    def review_skill(self, skill_path: str) -> QualityScore:
        """SafeGuard 联动审查：新生成的技能是否符合安全规范。
        
        检查项：
        - 不包含高风险操作
        - 权限声明合理
        - 依赖链完整
        - 无循环依赖
        """
        ...

    # ========== 统计查询 ==========

    def get_skill_stats(self) -> dict:
        """获取技能库统计：总数/活跃/弃用/版本分布"""
        ...

    def get_dependency_graph(self) -> dict:
        """构建技能依赖关系图（有向图）。"""
        ...
```

### 3.2 数据结构

```python
@dataclass
class SkillBlueprint:
    """技能蓝图：提炼→生成之间的中间表示"""
    name: str                      # 技能名称
    version: str                   # 版本号，如 "v1.0"
    description: str               # 一句话描述
    category: str                  # 分类：scanner/controller/memory/safety/forge/evolution
    dependencies: List[str]        # 依赖技能ID列表
    capabilities: List[str]        # 核心能力列表
    code_interface: str            # Python类接口签名
    safety_level: str              # 风险等级：LOW/MEDIUM/HIGH
    source: str                    # 来源：iteration_report/execution_log/sica_cycle
    source_detail: str             # 来源详情

@dataclass
class DuplicateReport:
    duplicate_confidence: float    # 0-1，>0.7建议合并
    similar_skills: List[str]      # 相似技能名称列表
    overlap_keywords: List[str]    # 重叠关键词
    recommendation: str            # "create_new" / "upgrade_existing" / "merge"

@dataclass
class QualityScore:
    score: float                   # 0-100
    dimensions: dict               # {可复现性:30, 通用性:20, 效率:20, 安全性:20, 文档:10}
    issues: List[str]              # 问题清单
    recommendation: str            # "activate" / "review" / "reject"
```

---

## 四、技能生成流水线

```
┌─────────────────────────────────────────────────────┐
│                  SkillForge 流水线                    │
├─────────────────────────────────────────────────────┤
│  1. 输入源                                           │
│     ├── 迭代报告（R08→新技能蓝图）                     │
│     ├── 执行日志（成功模式→新技能蓝图）                 │
│     └── SICA进化周期（成功进化→技能沉淀）              │
│                    ↓                                  │
│  2. 模式识别 ← PatternMatcher                         │
│     识别成功/失败/高效/协作四类模式                    │
│                    ↓                                  │
│  3. 蓝图生成 ← BlueprintGenerator                     │
│     将识别的模式编码为 SkillBlueprint                  │
│                    ↓                                  │
│  4. 去重检查 ← DuplicateChecker                       │
│     与已有技能对比，避免重复                           │
│                    ↓                                  │
│  5. 质量评估 ← QualityScorer                          │
│     可复现性/通用性/效率/安全性/文档 五维评分          │
│                    ↓                                  │
│  6. 安全审查 ← SafeGuard.review_skill()               │
│     高风险操作检查 / 权限审查 / 依赖环检测             │
│                    ↓                                  │
│  7. 生成 & 保存                                       │
│     ├── 生成 SKILL.md 文本（标准模板）                 │
│     ├── 保存到 技能库/ 目录                            │
│     └── 注册到 capabilities.json                      │
│                    ↓                                  │
│  8. 联动通知                                          │
│     ├── AutoFileScanner → 重新索引                    │
│     └── MemoryOS → 记录 "new_skill_created" 事件      │
└─────────────────────────────────────────────────────┘
```

---

## 五、与其他技能的接口契约

| 调用方 | 接口 | 数据流向 |
|--------|------|---------|
| AutoFileScanner | `load_skill_files()` 返回 | 现有技能元数据 → 去重判断 |
| MemoryOS | `record_event("new_skill")` | 技能创建事件 → 长期记忆 |
| SafeGuard | `review_skill(path)` | 技能安全审查请求 → 审查结果 |
| SICA Evolver | `extract_from_evolution(cycle)` | 进化周期 → 技能蓝图 |
| 自进化闭环 | `extract_from_iteration(report)` | 迭代报告 → 技能蓝图 |

---

## 六、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | R04 | 初始版本：基础技能模板生成 |
| v2.0 | R07 | 增强：支持SICA进化周期技能萃取、质量评分体系 |
| v3.0 | R08 | 增强：去重检查、技能版本管理、AutoFileScanner/MemoryOS/SafeGuard全域联动 |
