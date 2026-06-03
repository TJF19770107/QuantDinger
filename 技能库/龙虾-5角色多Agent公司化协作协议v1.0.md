# 5角色多Agent公司化协作协议 v1.0

> **版本**: v1.0 · 2026-06-01
> **协议编号**: #81
> **对标来源**: Controllable Agent (GitHub Yang1999code) + Paperclip (GitHub 64.2K★ · 2026年5月)
> **核心价值**: Coordinator/Planner/Coder/Reviewer/Memorizer 5角色 + 公司架构治理

---

## 一、协议概述

5角色多Agent公司化协作协议融合了Controllable Agent的5角色分工框架和Paperclip的公司架构治理理念，将多Agent协作组织为类公司结构的标准化模式，包含明确的角色职责、汇报关系、预算控制和审计日志。

---

## 二、5角色定义

| 角色 | 类公司对标 | 职责 | 输入 | 输出 |
|------|-----------|------|------|------|
| Coordinator | CEO | 全局监控+资源分配+冲突仲裁+进度管理 | 全局状态 | 调度指令+资源分配 |
| Planner | CTO | 需求分析+任务分解+方案设计+动态调整 | 用户需求 | 执行计划JSON |
| Coder | 工程师 | 执行编码+运行测试+自我修复 | 子任务 | 代码+测试结果 |
| Reviewer | QA/Code Review | 代码审查+质量验收+缺陷报告 | Coder输出 | Review Report |
| Memorizer | CKO（知识官） | 经验提炼+技能沉淀+知识管理 | 执行轨迹 | SKILL.md/经验条目 |

---

## 三、协作模式

### 3.1 默认协作流程
```
Coordinator接收任务 → Planner分解设计 → 
  Coder+Reviewer配对并行[多组] → 
  Coordinator汇总 → Memorizer沉淀 → 交付
```

### 3.2 Coder+Reviewer配对机制
- 每个Coder必须绑定一个Reviewer，形成配对单元
- 小模块即时审查：写完一个函数→立即审查，非等整个任务完成
- Reviewer发现缺陷→Coder即时修复→再次审查→通过

### 3.3 Coordinator干预条件
| 条件 | 干预动作 |
|------|---------|
| Coder连续3次未通过Review | 重新分配任务或降级 |
| 某配对单元阻塞超时 | 启动备用Coder+Reviewer |
| 用户中途插入指令 | 暂停当前执行→处理新指令→恢复 |
| 全局资源超预算 | 暂停低优先级任务→释放资源 |

---

## 四、公司化治理（Paperclip增强）

### 4.1 组织架构
```
CEO(Coordinator)
├── CTO(Planner)
├── Engineering Team
│   ├── Senior Coder + Senior Reviewer (复杂任务)
│   ├── Junior Coder + Junior Reviewer (简单任务)
│   └── Specialist Coder (特定领域/工具)
└── CKO(Memorizer)
```

### 4.2 目标对齐机制
- 每个子任务携带完整的上下文链：Mission → Project → Task
- Coder执行前必须确认理解任务目标和验收标准
- 偏离目标的任务由Coordinator及时发现并纠正

### 4.3 预算控制
- 每任务设置token预算（软上限）
- 超过80%预算触发预警→Coordinator评估是否继续
- 超过100%预算强制暂停→人工审批后继续

### 4.4 审计日志
- 所有角色间的通信记录全量存储
- 所有Coder的代码变更+Reviewer的审查意见全量追踪
- 日志格式：{timestamp} [{role}] [{action}] {detail}

---

## 五、Memorizer记忆系统

### 5.1 Wiki式记忆（Controllable Agent）
- 每次任务完成后，Memorizer提炼经验→写入Wiki
- 内容分类：成功模式/失败模式/工具使用技巧/协作优化建议
- 下次相似任务时自动注入相关Wiki条目到上下文

### 5.2 技能结晶
- 识别可复用的执行模式→固化为SKILL.md
- 结晶条件：同一模式成功执行≥3次
- 技能遵循agentskills.io开放标准

---

## 六、执行规范

1. 5角色不得合并：同一Agent实例不得同时担任多个角色
2. Coordinator不参与执行：只管人不管活，避免利益冲突
3. Reviewer独立于Coder：不同会话/不同上下文，确保审查客观
4. Planner全程在线：不是设计完就消失，执行中持续动态调整计划
5. Memorizer异步工作：不阻塞主流程，在任务完成后后台沉淀

---

## 七、安全约束

1. Coordinator的资源分配必须受全局安全策略约束
2. Coder执行代码前必须经Reviewer沙箱预检
3. 预算耗尽不得自动续费，必须人工审批
4. 审计日志不得篡改，写入后只追加不覆盖

---

## 八、与现有协议关系

| 协议 | 关系 | 说明 |
|------|------|------|
| #1 多Agent协同看板协议 | 升级 | #1定义协作模式，#81定义角色+公司治理 |
| #25 Lead-Specialist推理分发协议 | 互补 | #25定义推理分工，#81定义全流程角色 |
| #61 多Agent置信度验收协议 | 增强 | #61定义置信度，#81用Reviewer角色强化验收 |
| #78 端到端多Agent协同训练协议 | 互补 | #78定义训练，#81定义运行时代理结构 |

---

> 状态：ACTIVE | 执行者：豆包Agent
