# #166 ACS Agent控制规范接入

协议编号: #166
状态: 候选 (R47新增)
创建日期: 2026-06-03
关联情报: 微软Build 2026 · ACS开源标准 · Agent行为策略文件

---

## 一、协议背景

微软在Build 2026大会上发布Agent控制规范（ACS），这是一个新的开源标准，旨在为开发者提供更一致、更细粒度的方法来控制AI Agent的行为。ACS让开发、合规和安全团队能够为Agent定义策略文件，规定Agent可以做什么、绝对不能做什么、何时需要人类批准，以及应记录哪些证据供审查。ACS以SDK形式发布，附带LangChain、OpenAI Agents SDK、Anthropic Agents SDK、AutoGen、CrewAI、Semantic Kernel等插件。

## 二、协议目标

1. 将ACS标准纳入龙虾AI分身安全体系
2. 为三Agent分别定义策略文件（允许/禁止/审批/审计）
3. 与Mythos Glasswing形成双层安全防护

## 三、预期影响
- 安全机制维度加固（100→100维持，证据链更新）
- 沙箱隔离维度增强
- Skills生态新增安全协议子类

## 四、候选状态
待Mythos全面开放+ACS成熟度验证后推进正式化。
