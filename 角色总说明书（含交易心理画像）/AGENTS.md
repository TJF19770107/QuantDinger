# AGENTS.md — 龙虾AI分身体系 · 工作规则

版本号：v3.0 (2026-06-01 · R30)
基于：R11-R30 19轮全域迭代蒸馏
上一版本：v2.2 (R26)
核心升级：Managed Agents全量整合（Dreaming协议/Outcomes闭环/Multiagent编排）

---

## 一、三大子Agent职责边界

### 豆包AI Agent（v10.5_R30）
- **能力**：对话理解、任务规划、知识问答、技能调用
- **执行机制**：goal模式持久化执行 + Outcomes验证闭环
- **不盲信**：交叉验证后输出，不确定时明确告知

### Hermes Agent（v4.0_R30）
- **能力**：系统操作、工具调用、MCP Server管理、跨平台控制
- **Windows原生支持**：Win 10/11原生，通过GitBash运行Shell
- **五层防烂尾**：心跳/僵尸回收/退出拦截/幻觉拦截/重试预算
- **新增**：Dreaming记忆巩固——定时回顾历史会话→生成纠正Playbook

### OpenClaw龙虾Agent（v4.0_R30）
- **能力**：文件操作、代码生成、数据分析、工作流编排
- **Swarm模式**：多Agent并行编排（支持16并发+1000上限）
- **新增**：Multiagent Orchestration——20 Agent × 25 并行工具调用

---

## 二、Agent间协作协议（v3.0）

### 2.1 消息路由

| 消息类型 | 路由目标 | 优先级 |
|------|------|:---:|
| 系统操作 | Hermes Agent | P0 |
| 文件操作 | OpenClaw Agent | P0 |
| 知识问答 | 豆包Agent | P0 |
| 跨域任务 | 主Agent协调 | P0 |
| Dreaming回顾 | Hermes→全Agent广播 | P1 |
| Outcomes评分 | 独立评分Agent | P0 |

### 2.2 知识库读写

- 所有Agent共享同一知识库路径
- 写入权限：主Agent（统一写入，避免冲突）
- 读取权限：三子Agent全部可读
- MD5校验：写入前检查去重

### 2.3 Dreaming记忆巩固协议（R30新增）

```
触发条件：每2小时定时任务执行后，或用户主动触发
执行流程：
  1. Hermes Agent回顾最近N轮迭代日志和产出
  2. 抽取共同模式和成功经验
  3. 生成纯文本备忘录+结构化Playbook
  4. 广播至全Agent共享知识库
  5. 后续会话引用Playbook作为参考
安全约束：
  - 不直接修改模型权重
  - 所有回顾日志可审计
  - Playbook存储于知识库/迭代日志/
```

### 2.4 Outcomes独立评分协议（R30新增）

```
触发条件：任何关键任务产出后自动触发
执行流程：
  1. 主Agent定义验收标准（格式/风格/准确性/完整性）
  2. 独立评分Agent在新上下文中审查产出
  3. 评分Agent指出缺口→工作Agent依回馈重试
  4. 直到达标或达到最大重试次数
  5. 保留完整审计记录
最大重试：3次
超限处理：标记为P0人工审核
```

### 2.5 Multiagent并行编排协议（R30新增）

```
触发条件：任务规模超过单Agent处理能力时自动触发
能力上限：
  - 目标：支持最多20个子Agent并行（当前对标Anthropic标准）
  - 每个子Agent最多25次工具调用
  - 并发上限：16
编排模式：
  1. Supervisor模式（默认）：主Agent拆任务→分发→汇总
  2. Swarm模式：无中心协调，Agent间直接通信
  3. Dynamic Workflows模式：JS编排脚本，无上下文窗口污染
审计要求：所有子Agent输入/输出/评分/迭代全程可追溯
```

### 2.6 执行可验证性协议（R26→R30强化）

```
原则：做与验分离（Outcomes机制的核心）
验证层级：
  L1 自检：执行Agent自身检查（快速但不可靠）
  L2 独立评分：Outcomes独立Grader审查（可靠但慢）
  L3 对抗验证：两个Agent分别执行后交叉比对（最强但最贵）
验证要求：
  - P0任务：必须L2+L3双验证
  - P1任务：L2验证
  - P2任务：L1自检
```

---

## 三、安全事件分级响应

| 等级 | 定义 | 响应 | 审批 |
|:---:|------|------|:---:|
| 🔴 P0 | 格式化/重置/系统破坏 | 强制挂起+用户确认 | 必须 |
| 🟡 P1 | 配置变更/批量覆盖 | Outcomes验证+用户告知 | 建议 |
| 🟢 P2 | 只读/创建/临时写入 | 自动执行+事后报告 | 不需要 |

---

## 四、技能协议路由表

| 编号 | 协议名称 | 负责Agent | 版本 |
|:---:|------|------|:---:|
| #83 | AI分身蒸馏专家 | 豆包 | R26 |
| #84 | Skills标准化协议 | 豆包 | R26 |
| #85 | 多Agent协作协议v2 | OpenClaw | R26 |
| #86 | 实时市场数据采集协议 | Hermes | R26 |
| #87 | 全域记忆融合引擎 | 全Agent | R26 |
| #88 | Goal模式Agent持久化执行 | 全Agent | R26候选 |
| #89 | Dynamic Workflows多Agent并行验证 | OpenClaw | R26候选 |
| #90 | AI视频创作商业闭环 | 豆包 | R26候选 |
| #91 | Managed Agents Dreaming记忆巩固 | Hermes | R30候选 |
| #92 | Managed Agents Outcomes独立评分 | 全Agent | R30候选 |
| #93 | Dynamic Workflows多Agent并行编排 | OpenClaw | R30候选 |

---

## 五、配置同步流程

### 5.1 版本号规范
```
格式：vMAJOR.MINOR_R轮次
示例：
  v3.0_R30 → SOUL/USER/AGENTS 第3次大版本升级，R30轮次
  v10.5_R30 → 豆包Agent 第10次大版本升级，R30同步
  v4.0_R30 → Hermes/OpenClaw 第4次大版本升级，R30同步
```

### 5.2 MD5校验流程
1. 主Agent生成配置文件
2. 计算MD5，写入版本记录
3. 同步至三子Agent
4. 三子Agent读取后本地MD5对比
5. 不一致→回滚并标记异常

### 5.3 同步触发条件
- 每轮全域迭代后自动触发
- 用户主动要求时触发
- Dreaming发现偏差时触发纠正

---

## 六、R30版本演进记录

| 文件 | R26版本 | R30版本 | 核心变更 |
|------|:---:|:---:|------|
| SOUL.md | v2.2 | v3.0 | +不盲信细则 +Dreaming/Outcomes/Multiagent |
| USER.md | v2.2 | v3.0 | +Managed Agents关注域 +Dynamic Workflows |
| AGENTS.md | v2.2 | v3.0 | +Dreaming协议+Outcomes协议+Multiagent协议 |
| 角色总说明书 | v1.9 | v2.0 | Code with Claude 2026全量整合 |

---

*AGENTS.md v3.0 | R30全域迭代 | 工作规则*
