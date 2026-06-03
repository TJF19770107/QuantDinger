# R10 原始情报汇编 · 2026-05-31

## 一、Claude 生态 (7条)

### 1. Claude Opus 4.8 + Dynamic Workflows
- 来源: 腾讯网 2026-05-29
- 链接: https://new.qq.com/rain/a/20260529A08I4700
- 摘要: Opus 4.8发布，价格不变。核心亮点Dynamic Workflows——单任务调度数百子Agent并行，自动规划→分配→执行→验证→汇总。SWE-Bench Pro +4.9%。Computer Use和金融分析基准均有提升。
- 启示: 百级子Agent并行调度模式可直接对标豆包多Agent能力提升目标。

### 2. Claude Agent SDK
- 来源: coolai123.com
- 链接: https://www.coolai123.com/tool/claude-agent-sdk
- 摘要: Anthropic官方Agent开发框架，Q1 2026发布。内置文件/终端/浏览器工具，多Agent协调编排，持续执行不中断，自评估迭代至达标，自托管。
- 启示: SDK的低层级非侵入架构——不强加编排逻辑，模型自主决策——值得豆包借鉴。

### 3. Claude Code 2026 + Code w/ Claude大会
- 来源: 稀土掘金 2026-05-11
- 链接: https://juejin.cn/post/7637897508347052066
- 摘要: 三界面(CLI/IDE/Desktop)，五大发布：速率翻倍、Advisor Tool(Sonnet执行+Opus评审)、Managed Agents三件套(Multi-agent/Outcomes/Dreaming)。
- 启示: Advisor Tool的分层模型策略——廉价模型执行+昂贵模型评审——可降低豆包运行成本。

### 4. Claude Managed Agents实战
- 来源: CSDN 2026-05-27
- 链接: https://blog.csdn.net/zhangkaiadl/article/details/161446854
- 摘要: Outcomes+Multiagent+Webhooks三件套公测。Outcomes成功率+10pp，docx质量+8.4%，pptx+10.1%。独立Grader模型在独立context打分。
- 启示: Outcomes的Rubric→Grader→迭代闭环是任务质量保障的成熟范式。

### 5. Claude Computer Use + Dispatch
- 来源: claude.com 2026-03-23
- 链接: https://claude.com/blog/dispatch-and-computer-use
- 摘要: Claude Cowork/Code中启用Computer Use，可点击、导航屏幕、打开文件、使用浏览器。Dispatch支持手机端分配任务。
- 启示: 手机→桌面Agent的远程任务分配模式，对标豆包桌面控制+移动端协同。

### 6. Claude Code安装配置
- 来源: 稀土掘金 2026-05-27
- 链接: https://juejin.cn/post/7644205077851914278
- 摘要: 2026年新增Computer Use GUI操控、MCP工具协议。全代码库理解、多文件协同修改、自主工程化执行、Git全流程。
- 启示: Computer Use + MCP工具协议的组合是桌面Agent的完整解决方案。

### 7. Claude Opus 4.8 诚实度提升
- 来源: 腾讯网 2026-05-29
- 摘要: Opus 4.8对齐表现接近内部Claude Mythos预览版。更适合大型代码仓库、长时间无人值守、自纠错、Computer Use。
- 启示: 自纠错+长时间无人值守是豆包定时任务场景的核心需求。

---

## 二、Codex/OpenAI 生态 (2条)

### 8. Codex CLI 0.132 + 移动端
- 来源: 博客园 2026-05-20
- 链接: https://www.cnblogs.com/qiniushanghai/p/20151068
- 摘要: 83.9k Stars。移动端远程连接(iOS/Android通过ChatGPT App连接Mac)。Triggers自动化流水线响应GitHub Issue自动修Bug开PR。Hooks功能GA。Chrome扩展。三档审批(suggest/auto-edit/full-auto)。全计划开放(Free/Plus/Pro)。
- 启示: 移动端远程+Triggers事件驱动自动化是下一代Agent标配。

### 9. Codex CLI新手指南
- 来源: 博客园 2026-05-20
- 链接: https://www.cnblogs.com/qiniushanghai/p/20092961
- 摘要: Apache 2.0开源。本地终端运行，直接操作项目目录。三档审批模式，默认codex-mini-latest模型。
- 启示: 开源+本地终端+三档审批的架构是豆包Agent的参考范式。

---

## 三、Gemini/Google 生态 (4条)

### 10. Gemini 3.5 Flash发布
- 来源: 腾讯网 2026-05-28
- 链接: https://new.qq.com/rain/a/20260528A08CYA00
- 摘要: 专为Agent工作流设计。速度4x于竞品前沿模型，Flash版12x加速。编码和自主Agent能力最强。内部测试中从零构建完整OS，API耗费<$1000。
- 启示: 低成本+高速的Agent专用模型是豆包降低运行成本的关键方向。

### 11. Google I/O 2026
- 来源: 电脑之家 2026-05-25
- 链接: https://article.pchome.net/content-2195759.html
- 摘要: Antigravity 2.0(Agent优先IDE)，Antigravity CLI，内置跨平台终端沙盒，凭证遮盖，强化Git策略。Gemini Spark个人Agent(Workspace深度集成)。CodeMender安全Agent。
- 启示: Antigravity 2.0的Agent优先IDE理念——不造编辑器，成为Agent运行容器——与豆包方向一致。

### 12. Gemini 3.5 Flash编码自主代理
- 来源: 搜狐 2026-05-20
- 链接: https://www.sohu.com/a/1025319782_362225
- 摘要: 超越3.1 Pro，编码/Agent/多模态推理全面领先。适合多Agent协同长时间任务。金融自动化数周工作流。
- 启示: 多Agent长时间协同的模型选型参考。

### 13. Gemini API Managed Agents
- 来源: ai.google.dev 2026-05-25
- 链接: https://ai.google.dev/gemini-api/docs/changelog?hl=zh-tw
- 摘要: Gemini API Managed Agents公开预览。安全隔离Google托管Linux沙箱。Antigravity Agent自主规划/推理/编码/文件管理/网络浏览。
- 启示: 托管沙箱+自主Agent是Google的Agent产品化路径。

---

## 四、Hermes 生态 (4条)

### 14. Hermes SWARM v2.1
- 来源: chaobro.com 2026-05-03
- 链接: https://chaobro.com/posts/hermes-agent-v21-swarm-multi-agent-orchestration-2026
- 摘要: 无限Agent编排。Orchestrator Chat+Control Plane+Kanban TaskBoard+Reports+Inbox。9种协作模式。SQLite原子认领。进程级隔离。熔断机制。
- 启示: SWARM的Kanban+原子认领+熔断是成熟的多Agent任务分配范式。

### 15. Hermes自我进化深度解析
- 来源: CSDN 2026-04-13
- 链接: https://blog.csdn.net/weixin_57908930/article/details/160099180
- 摘要: Skill自动生成(任务完成→抽象为Skill→下次直接调用)。四层记忆(用户画像/Agent记忆/技能库/会话历史)。GEPA自进化。50k Stars。工具调用记录可导出训练数据。
- 启示: Skill自动生成+四层记忆是豆包自进化闭环的理想参照。

### 16. Hermes Workspace Mobile
- 来源: halmob.com 2026-04-23
- 链接: https://www.halmob.com/blog/hermes-workspace-mobile-agent-orchestration
- 摘要: 手机端完整Agent编排。实时工具执行+Face ID审批。记忆浏览器。技能目录。终端。文件检查器。推送通知。
- 启示: 手机端完整Agent控制面板是移动端协同的参考架构。

### 17. Hermes Multi-Agent架构
- 来源: hermes-agent.ai
- 链接: https://hermes-agent.ai/blog/hermes-agent-multi-agent
- 摘要: Orchestrator+Worker模式。零上下文成本管道(execute_code)。模型分层(廉价快速Kimi做Orchestrator+Claude做Validator)。
- 启示: 零上下文成本管道+模型分层是低成本多Agent的关键技术。

---

## 五、OpenClaw 生态 (2条)

### 18. OpenClaw v2026.5.12-beta.6
- 来源: openclawchronicles.com
- 链接: http://openclawchronicles.com/posts/openclaw-2026-5-13-beta6-release
- 摘要: Gateway v4 Protocol(deltaText+replace帧流式)。Cron Inspection API。Agent间Session预创建。maxPingPongTurns升至20。Copilot图片理解修复。
- 启示: Gateway v4的流式增量传输+Agent间Session是豆包Gateway升级方向。

### 19. OpenClaw 2026软件工厂
- 来源: popularaitools.ai
- 链接: https://popularaitools.ai/blog/openclaw-ai-agent-software-factory-2026
- 摘要: 247k Stars。自进化Agent(自主写代码创建新能力)。长期记忆。主动自动化。5 Agent+Mac Studio(512GB)运行软件工厂。Node.js服务。
- 启示: 自进化Agent写代码创建新能力的机制是豆包SkillForge的终极形态。

---

## 六、自进化/记忆 生态 (1条)

### 20. EverOS/EverMind
- 来源: 网易 2026-04-14
- 链接: https://www.163.com/dy/article/KQG85CM90511AQHO.html
- 摘要: ACL 2026双论文(EverMemOS+HyperMem)。Agent Memory自进化。超图记忆。面向Agent友好型Infra。
- 启示: 超图记忆结构可能是豆包记忆系统升级方向。

---

## 统计

| 指标 | 数值 |
|------|------|
| 情报来源 | 7大生态 |
| 有效条目 | 20条 |
| Claude | 7条 |
| Codex | 2条 |
| Gemini | 4条 |
| Hermes | 4条 |
| OpenClaw | 2条 |
| 自进化/记忆 | 1条 |
