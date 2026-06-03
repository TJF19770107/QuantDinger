# 龙虾AI分身 · Self-Skill 专属技能包 v2.5（R34蒸馏）

**版本**：v2.5 | **生成日期**：2026-06-02  
**基础配置**：SOUL v2.3(R33) / USER v2.1(R33) / AGENTS v2.1(R33) / 角色总说明书 v2.0(R33)  
**对齐标准**：agent-skills 7强制命令 + Google 47.3K⭐标准  
**输出目录**：技能库 / 子Agent / MCP配置  

---

## 一、技能协议总览（R34状态）

| 协议编号 | 名称 | 状态 | R34变化 |
|:---:|------|:---:|:---:|
| #83 | AI分身蒸馏专家 | S1 活跃 | 维持 |
| #84 | Skills生态标准化 | S1 活跃 | 维持 |
| #85 | Agentic AI硬件适配 | S1 活跃 | 维持 |
| #86 | 企业级MCP安全隧道 | S1 活跃 | 维持 |
| #87 | 多平台Agent协同 | S1 活跃 | 维持 |
| #88 | Goal模式Agent持久化执行 | S1 活跃 | 维持 |
| #89 | Dynamic Workflows多Agent并行 | S0 孵化 | 维持 |
| #90 | AI视频创作商业闭环 | S1 活跃 | 维持 |
| #91 | 三层自进化统计合并 | S1 活跃 | R34正式运行 |
| #92 | SkillOS五态管理 | S1 活跃 | R34初始化 |
| #93 | 影子Agent安全复盘 | S1 活跃 | 维持 |
| #94 | Goal模式持久化执行v2 | S0 孵化 | R34新增 |
| #95 | 全分身版本一致性校验 | S1 活跃 | 维持 |

---

## 二、R34 Self-Skill 核心能力矩阵

### 2.1 蒸馏能力（#83 核心）

```yaml
name: lobster-distillation-expert
description: 六步全自动AI分身蒸馏，含五道质量门控与Goal模式持久化执行
version: 2.5
type: self-skill
lifecycle: S1_ACTIVE
steps:
  - 前置读取：角色总说明书+SOUL+USER+AGENTS
  - 分析自己：生成用户人格画像v2.5
  - 制定计划：生成AI分身进化规划v2.5
  - 文件转换：扫描非MD文件并无损转换
  - 构建知识库：更新知识库索引与图谱
  - 创建Self-Skill：生成专属技能包更新
  - 更新核心配置：SOUL/USER/AGENTS版本同步
  - 全域同步：三Agent配置同步+MD5校验
quality_gates:
  G1: 实事求是（零幻觉）
  G2: MD5去重
  G3: 路径合规
  G4: 对标校验
  G5: 全局一致性
```

### 2.2 三层自进化能力（#91 R34正式运行）

```yaml
name: lobster-three-layer-evolution
description: L1实时反思 + L2延迟统计 + L3定期合并
version: 1.0
lifecycle: S1_ACTIVE
triggers:
  L1: 每次蒸馏完成后触发
  L2: 每6次蒸馏触发（R29-R34窗口）
  L3: 每24次蒸馏触发（R45首次）
outputs:
  L1: 本轮质量评估
  L2: 6轮趋势分析
  L3: 骨架级优化方案
```

### 2.3 SkillOS五态管理（#92 R34初始化）

```yaml
name: lobster-skillos-lifecycle
description: 技能生命周期五态管理
version: 1.0
lifecycle: S1_ACTIVE
states:
  S0: 孵化（概念阶段，如#94 Goal v2）
  S1: 活跃（正式运行）
  S2: 冻结（30天未调用或主动冻结）
  S3: 退役（功能被替代）
  S4: 重生（重新评估有价值）
r34_actions:
  - 初始化五态登记表
  - 评估13项协议当前状态
  - 识别S0孵化→S1升级路径
  - 识别S1→S2冻结候选
```

---

## 三、MCP工具能力清单（R34）

```yaml
mcp_servers:
  - name: lobster-distillation
    description: AI分身蒸馏工具链
    tools:
      - read_config: 读取角色总说明书及三元组
      - generate_profile: 生成人格画像
      - generate_plan: 生成进化规划
      - scan_files: 扫描非MD文件
      - update_kb_index: 更新知识库索引
      - sync_agents: 同步三Agent配置
      - verify_md5: MD5去重校验
      - generate_report: 生成蒸馏总报告

  - name: lobster-evolution
    description: 三层自进化统计工具
    tools:
      - L1_reflect: 实时反思执行
      - L2_aggregate: 6轮延迟统计
      - L3_merge: Curator定期合并
      - evolution_report: 进化统计报告生成

  - name: lobster-skillos
    description: SkillOS五态管理工具
    tools:
      - scan_skills: 扫描全部技能协议
      - evaluate_state: 评估五态状态
      - transition: 执行状态转换
      - merge_umbrella: 伞状合并触发
      - cross_pollinate: 跨Agent交叉授粉

  - name: lobster-quant
    description: 量化策略资产工具
    tools:
      - LOBSTER_BLACK_HORSE: 黑马策略引擎v4
      - LOBSTER_PSYCHOLOGY: 交易心理画像v4
      - LOBSTER_BACKTEST: 回测引擎v4
      - LOBSTER_MARKET_DATA: 市场数据v4
      - LOBSTER_VNPY: VNPY配置v4
      - LOBSTER_BINANCE: 币安配置v4
      - LOBSTER_MICRO_DOGE: 微策略引擎

  - name: lobster-shadow-agent
    description: 影子Agent安全审计
    tools:
      - audit_log: 安全审计日志
      - layer_check: 六层隔离检查
      - boundary_test: 边界渗透测试
      - incident_response: 安全事件响应
```

---

## 四、R34新增：#94 Goal模式持久化执行v2

```yaml
name: lobster-goal-mode-v2
protocol: "#94"
description: Goal模式Agent持久化执行v2升级版
version: 2.0
status: S0_孵化
upgrade_from: "#88 v1.0"
enhancements:
  - 心跳间隔优化：15s→10s
  - 僵尸进程自动回收：30s→20s
  - 新增checkpoint快照机制（基于MD5状态指纹）
  - 新增多Agent并行goal协调（对接#89 Dynamic Workflows）
  - 中断恢复成功率目标：95%→99%
dependencies:
  - SOUL.md v2.3（持久化执行原则）
  - AGENTS.md v2.1（执行可验证性协议）
  - Hermes Agent v3.9_R33（五层执行保障）
target_r35: 正式化
```

---

## 五、Agent能力对标（R34）

| 能力维度 | 豆包Agent | Hermes Agent | OpenClaw Agent | 状态 |
|---------|:---:|:---:|:---:|:---:|
| 人格一致性 | 100% | 100% | 100% | ✅ |
| 技能协议覆盖率 | 92/92 | 15/92 | 10/92 | ↑ |
| 执行可验证性 | 强制 | 强制 | 强制 | ✅ |
| Goal模式持久化 | 支持 | 支持 | — | ↑ |
| Dynamic Workflows | — | 候选 | — | 🔄 |
| SkillOS五态响应 | 主控 | 执行 | 监听 | R34 |
| 三层自进化参与 | L1+L2 | L1+L2+L3 | L1 | R34 |

---

*Self-Skill专属技能包 v2.5 | R34全域蒸馏 | 2026-06-02*
