# AI Agent · MCP协议 · 多智能体协同 知识库
主题：AI Agent技术前沿与多智能体协同生态
日期：2026-05-28
版本：v1.0
来源：B站 · GitHub · 技术博客
学习时段：2023.01.01-2026.05.28

---

## 一、AI Agent 核心架构与入门教程

### 1.1 B站 2026版 AI Agent 入门到实战（全41集）
- 链接：https://www.bilibili.com/video/BV1h1A6zREB5/
- 发布：2026-02-27
- 核心内容：Agent核心架构、多Agent协作模式、AutoGen智能体开发、CrewAI+FastAPI打造多Agent协作应用、LangChain工具库集成、OpenAI Agents SDK
- 覆盖框架：CrewAI · AutoGen · MetaGPT · Swarm · PydanticAI · LangGraph
- 营收关联：Agent开发能力 → 企业级智能客服 → 技术咨询变现

### 1.2 Agent Skills 从入门到代码实战（全32集）
- 链接：https://www.bilibili.com/video/BV1sWrkBwEWJ/
- 发布：2026-01-16
- 核心内容：Agent Skills定义与Multi-Agent差异、Supervisor架构、MCP+Agent开发、AgenticRAG、工业级多Agent系统
- 亮点：手把手MCP服务端配置+Agent创建+部署全流程

### 1.3 AI Agent 从0到1搭建（LangGraph全流程）
- 链接：https://www.bilibili.com/video/BV1iUwkzqEz4/
- 发布：2026-03-19
- 核心内容：LangGraph节点与可控制性、持久化与记忆、人机交互、时光旅行、代码助手实战、Agent数字人项目

### 1.4 Agent Skills 保姆级教程
- 链接：https://www.bilibili.com/video/BV169cMzGEsa/
- 发布：2026-02-09
- 核心内容：Skill原理与实践、SQL助手实战、代码审查Skill、LangChain搭建Agent、MCP服务实战、LangGraph多智能体工作流

---

## 二、Claude Code · OpenClaw · Hermes 生态

### 2.1 OpenClaw — Personal AI Assistant
- 链接：https://openclaw.ai
- 特点：开源个人AI助手、持久化记忆、多平台通信集成(Discord/Slack/Telegram)、Cron定时任务、Skills插件生态
- 技术栈：角色入驻引导·心跳检测·自主运行·多模态交互
- 营收关联：个人AI助理定制服务 → 企业团队协作工具部署

### 2.2 Hermes Agent v0.6.0 (NousResearch)
- GitHub：https://github.com/NousResearch/hermes-agent
- 官网：https://hermes-ai.net
- Stars：101K+
- 核心能力：
  - 自主学习闭环：从经验中创建技能、使用中自我提升
  - MCP (Multi-Agent Communication Protocol)：多代理通信协议，任务分解+并行处理
  - FTS5跨会话记忆召回 + Honcho辩证用户建模
  - Cron调度系统、多实例Profile隔离
  - 支持飞书/企业微信/Telegram/Slack等多平台
- 营收关联：Hermes定制Agent → 多平台智能客服 → 企业内部AI调度

### 2.3 Hermes Agent v0.6.0 技术细节
- 发布：2026-03-30
- 关键更新：Profiles多实例隔离、MCP Server模式、Docker容器化、Fallback Provider链、95个PR
- 教程：https://www.agentupdate.ai/zh/tutorial/hermes-agent-tutorial/lesson-1
- 学习要点：MCP协议实现、多Agent网络构建、去中心化协作

---

## 三、黑客马拉松冠军项目

### 3.1 Lumina-Agent — 华为云鸿蒙Agent竞赛冠军（Rank 1）
- GitHub：https://github.com/LYZ0306/Lumina-Agent
- 发布：2026-02-08
- 核心方案：数据中心+记忆感知端到端语音指令系统
- 技术亮点：语音控制·记忆管理·数据驱动决策
- 营收关联：语音Agent技术 → 智能家居/车载场景落地

### 3.2 Deptheon — Agents in the Loop Hackathon 2025 冠军
- GitHub：https://github.com/aaryanmittal154/dpth
- 核心能力：完全自主AI Agent、多小时复杂工作流编排、网页研究+电话+邮件+代码执行、3000+工具接入
- 营收关联：自动化业务流程外包 → 高客单价企业服务

---

## 四、TRAE · AI IDE 编程生态

### 4.1 TRAE 年度报告（600万用户）
- 链接：https://finance.itbear.com.cn/html/2026-01/315439.html
- 数据：全球600万注册用户、近200国家、月活160万、全年200+次迭代
- SOLO模式：用户渗透率44%、问答规模增长13倍
- 营收关联：AI编程效率工具 → 软件开发外包/咨询

### 4.2 TRAE 2025 技术演进时间线
- 链接：https://juejin.cn/post/7589172193151582244
- 关键节点：
  - 2025-01：国际版发布（IDE+插件双形态）
  - 2025-07：开源Trae-Agent、SOLO Beta上线
  - 2025-11：SOLO正式版上线（The Responsive Coding Agent）
- 营收关联：基于TRAE二次开发 → 企业定制IDE方案

### 4.3 TRAE Expert 开发体验
- 链接：https://developer.volcengine.com/articles/7588017842822807598
- 核心体验：291天使用、单日73次补全、最长116分钟对话
- 亮点：从智能辅助到自主执行的范式跃迁

---

## 五、Ollama · GGUF · 本地大模型部署

### 5.1 Ollama本地部署大模型完整实录
- 链接：https://blog.csdn.net/qq_41845870/article/details/160959861
- 发布：2026-05-10
- 核心内容：消费级PC从零搭建本地大模型API、镜像加速、GGUF手动导入、硬件约束评估
- 技术栈：Ollama · Qwen2.5 · OpenAI兼容API · localhost:11434/v1

### 5.2 个人本地部署大模型常用方式
- 链接：https://juejin.cn/post/7600670487408869428
- 发布：2026-01-30
- 核心内容：Ollama vs vLLM对比、多GPU负载均衡(OLLAMA_SCHED_SPREAD)、远程访问配置、REST API兼容OpenAI
- 量化选择：Q8_0(50%)·Q6_K(40%)·Q4_K_M(30%推荐)·Q3_K_M(22%)

### 5.3 Running LLMs Locally in 2026
- 链接：https://dev.to/lingdas1/the-complete-guide-to-running-llms-locally-in-2026-from-ollama-to-production-3d8b
- 发布：2026-05-23
- 核心内容：GGUF量化格式标准、HuggingFace自定义模型导入、生产环境部署

---

## 六、量化交易 · AI金融

### 6.1 B站量化交易全16集教程
- 链接：https://www.bilibili.com/video/BV1v7c7zZEw5/
- 发布：2026-02-18
- 核心内容：Python量化入门→股票策略→期货策略→多品种交易→期权策略→Alpha策略
- 营收关联：量化交易策略开发 → 策略售卖/信号订阅收入

### 6.2 个人AI量化交易系统构建指南
- 链接：https://xueqiu.com/7551088268/390617669
- 发布：2026-05-24
- 核心观点：2026年为"个人玩家AI量化元年"
- 五层技能体系：数据层→回测层→新闻监控层→决策层→风控层→执行层
- 框架对比：Olaos(长周期沙盒)·Hermes Agent(检索增强)
- 营收关联：AI量化策略 → 第一阶段月入8000-10000元核心路径

---

## 七、AI漫剧 · 网文创作 · 视频制作

### 7.1 AI漫剧制作全流程教学（30集）
- 链接：https://www.bilibili.com/video/BV1jLkeB8EaV/
- 发布：2026-01-19
- 核心流程：剧本→分镜→人物设计→运镜→剪辑→配音配乐
- 工具栈：即梦·豆包·剪映·ComfyUI

### 7.2 AI动态漫制作全流程
- 链接：https://www.bilibili.com/video/BV1DGPzzHEtT/
- 发布：2026-03-05
- 核心流程：分镜脚本+人物设计+视频生成+剪辑配音
- 营收关联：AI漫剧制作 → 短视频变现/网文IP漫改

---

## 八、技术落地与营收关联分析

| 学习方向 | 技术成熟度 | 营收路径 | 预估月收入 |
|---------|-----------|---------|-----------|
| AI Agent开发 | 成熟 | 企业智能客服定制 | 5000-15000 |
| 量化交易策略 | 中高 | 策略开发/信号订阅 | 3000-20000 |
| AI漫剧制作 | 中 | 短视频平台分成/接单 | 2000-8000 |
| 本地大模型部署 | 成熟 | 企业私有化部署咨询 | 5000-20000 |
| Hermes/OpenClaw定制 | 中高 | 企业AI助手部署 | 8000-30000 |
| TRAE插件开发 | 中 | 开发工具付费插件 | 2000-10000 |

---

## 九、去重状态

本次学习已通过 url_whitelist.json 完成去重，新增URL将全部写入白名单更新。

- 白名单原有条目：18条
- 本次新增：20条
- 更新后总计：38条
- 已跳过重复：0条

---

*生成时间：2026-05-28 | 来源：B站·GitHub·技术博客 | 状态：已归档*
