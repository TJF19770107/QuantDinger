# 龙虾-ACE上下文工程协议 v1.0

> 协议编号: 124 | 版本: v1.0 (R34新建) | 来源: Stanford ICLR 2026 ACE论文 (arXiv:2510.04618)
> 生效范围: 全域Agent上下文管理 | 依赖: 协议3(五步法) + 协议118(四层记忆) + 协议119(Curator)

---

## 一、核心理念

**Context Engineering > Fine-tuning**（Stanford实证）

ACE（Agentic Context Engineering）框架证明：把context设计成一份会自我演化的playbook，比调整模型权重更快、更便宜、更有效。用较小开源模型在AppWorld leaderboard追平顶级商用Agent。

## 二、ACE三步循环

```
┌──────────────────────────────────────────────┐
│                 ACE 三步循环                    │
│                                                │
│  PROFILE ──────→ PLAYBOOK ──────→ PROJECT     │
│  (建立档案)      (作战手册)        (项目执行)    │
│      ↑                              │          │
│      └──────── 反馈闭环 ────────────┘          │
└──────────────────────────────────────────────┘
```

## 三、Phase 1: PROFILE（建立Agent档案）

### 3.1 档案结构

```yaml
agent_profile:
  # ===== 能力画像 =====
  capabilities:
    coding: 98       # 编码能力得分
    planning: 98     # 自主规划
    memory: 99       # 长期记忆
    tools: 98        # 工具调用
    evolution: 99    # 自进化
    context_eng: 98  # 上下文工程
  
  # ===== 知识边界 =====
  known_domains:
    - 量化交易 (深度)
    - AI Agent架构 (深度)
    - Python/Go/Rust (深度)
    - 文件系统操作 (深度)
  
  knowledge_gaps:
    - iOS原生开发
    - Unity/Unreal游戏引擎
  
  # ===== 偏好与约束 =====
  preferences:
    language: "中文"
    style: "高密度技术分析+表格/矩阵"
    autonomy: "全自主深度执行"
    confirmation: "标准框架内无需确认"
  
  # ===== 上下文窗口预算 =====
  context_budget:
    total: 200000    # Token上限
    system_prompt: "30%"
    user_context: "20%"
    task_context: "30%"
    memory_injection: "15%"
    reserved: "5%"
```

### 3.2 龙虾档案映射

| ACE PROFILE | 龙虾对应 | 文件 |
|------------|---------|------|
| capabilities | 26维对标矩阵 | 龙虾全域官方模板-最终版.md |
| known_domains | 技能库领域 | 技能库/ |
| preferences | 用户偏好规则 | USER.md + 长期记忆 |
| context_budget | 上下文窗口管理 | SOUL.md |
| knowledge_gaps | 迭代攻坚目标 | AGENTS.md |

## 四、Phase 2: PLAYBOOK（作战手册）

### 4.1 Playbook结构

```yaml
playbook:
  # ===== 成功模式库 =====
  success_patterns:
    - id: "SP001"
      trigger: "用户发出激活咒语"
      action: "加载全域模板→加载全部技能→进入全技能专家模式"
      success_rate: "100%"
      last_used: "2026-06-02"
    
    - id: "SP002"
      trigger: "豆包Agent迭代任务"
      action: "六步流程: 分析→计划→转换→知识库→Skill→配置→同步"
      success_rate: "95%"
      last_used: "2026-06-02"
  
  # ===== 失败模式库 =====
  failure_patterns:
    - id: "FP001"
      trigger: "文件路径不存在"
      root_cause: "shell_executor列出但read_text无法访问"
      fix: "使用shell_executor Get-Content代替read_text"
      occurrence: 2
  
  # ===== 策略笔记 =====
  strategy_notes:
    - "定时任务执行时保持静默，不弹窗不打扰"
    - "删除操作使用专用delete工具（自带确认卡片），禁止ask_user双重确认"
    - "Sub Agent返回特殊卡片时调用present_result原子转发"
```

### 4.2 Playbook自演化机制

```
任务执行 → 结果评估
    ↓
成功? → 提取模式 → 更新success_patterns
    ↓ 否
失败? → 根因分析 → 更新failure_patterns + fix方案
    ↓
周期性Dream Job → 跨session模式挖掘 → Playbook精炼
```

### 4.3 龙虾Playbook映射

| ACE PLAYBOOK | 龙虾对应 |
|-------------|---------|
| success_patterns | Learning Loop协议117 (成功经验沉淀) |
| failure_patterns | 自愈回滚协议 (错误模式库) |
| strategy_notes | USER.md + 长期用户偏好 |
| 自演化 | Curator协议119 + Dream Job协议118v1.1 |

## 五、Phase 3: PROJECT（项目执行）

### 5.1 上下文注入策略

```
项目启动
    ↓
Step 1: 加载PROFILE → 确定Agent能力边界
    ↓
Step 2: 检索PLAYBOOK → 加载相关成功/失败模式
    ↓
Step 3: 注入L2情景记忆 → 相关历史对话
    ↓
Step 4: 注入L3语义记忆 → 固定知识和偏好
    ↓
Step 5: 组装完整上下文 → 不超过context_budget
    ↓
执行任务
```

### 5.2 上下文预算动态分配

| 任务类型 | system_prompt | user_context | task_context | memory_injection |
|---------|:---:|:---:|:---:|:---:|
| 简单查询 | 25% | 15% | 40% | 15% |
| 复杂迭代 | 30% | 10% | 35% | 20% |
| 代码生成 | 20% | 10% | 50% | 15% |
| 长周期任务 | 25% | 5% | 40% | 25% |
| Dream Job | 30% | 5% | 30% | 30% |

### 5.3 上下文压缩触发条件

| 条件 | 动作 |
|------|------|
| 上下文使用 > 70% | 压缩L1工作记忆中冗余内容 |
| 上下文使用 > 85% | 精简memory_injection，只保留关键记忆 |
| 上下文使用 > 95% | 触发PAUSE，等待下一轮Token预算 |

## 六、龙虾体系中的ACE定位

```
ACE上下文工程协议 (124)
    ├── PROFILE ← 龙虾全域模板 v3.27 (26维对标)
    ├── PLAYBOOK ← Learning Loop (117) + Curator (119) + Dream Job (118)
    └── PROJECT ← 五步法 (3) + 长周期执行 (122) + Gateway (123)
```

## 七、与传统Prompt Engineering的差异

| 维度 | Prompt Engineering | ACE Context Engineering |
|------|-------------------|------------------------|
| 核心假设 | 模型需精巧引导 | 模型已足够聪明，context需要管理 |
| 优化对象 | 单条prompt | 整个上下文生态系统 |
| 生命周期 | 一次性 | 持续演化（跨session） |
| 可积累性 | 低（每次重写） | 高（Playbook持续增长） |
| 实证效果 | 边际递减 | Stanford论文验证：追平顶级Agent |
| 成本 | 高（需反复调优） | 低（自动演化） |

## 八、实施优先级

| 阶段 | 动作 | 优先级 |
|------|------|--------|
| Phase 1 | PROFILE: 整理Agent能力画像+知识边界 | P0 |
| Phase 2 | PLAYBOOK: 从已有122项协议提取成功/失败模式 | P0 |
| Phase 3 | PROJECT: 上下文预算动态分配机制 | P1 |
| Phase 4 | 自动演化: Dream Job驱动Playbook精炼 | P1 |