# 豆包Agent能力矩阵_v2.3.json

> 原始文件: `豆包Agent能力矩阵_v2.3.json`  |  类型: `.json`  |  自动转换

```json
{
  "meta": {
    "agent_name": "豆包Agent",
    "version": "2.3.0",
    "last_updated": "2026-05-31",
    "schema_version": "1.0.0",
    "total_capabilities": 52,
    "new_in_v2.3": 18,
    "upgraded_in_v2.3": 7,
    "deprecated_in_v2.3": 2
  },
  "capabilities": [
    {
      "id": "THINK-LLM-001",
      "name": "多模型中枢调度",
      "layer": "THINK",
      "domain": "LLM",
      "description": "基于Claude Agent SDK的Central Orchestrator模式，实现多模型智能调度、Agent Graph原生支持",
      "benchmark_system": "Claude Agent SDK + Hermes",
      "status": "IN_PROGRESS",
      "priority": "P0",
      "code_template_ref": "src/think/orchestrator.py",
      "dependencies": ["THINK-LLM-002", "INFRA-LOCAL-001"]
    },
    {
      "id": "THINK-LLM-002",
      "name": "Chain-of-Thought深度推理",
      "layer": "THINK",
      "domain": "LLM",
      "description": "对标Gemini 2.5内置CoT，实现多步推理链，支持Long-Context Cache",
      "benchmark_system": "Gemini 2.5",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/think/cot_engine.py",
      "dependencies": ["THINK-CTX-001"]
    },
    {
      "id": "THINK-CTX-001",
      "name": "超长上下文管理(512K+)",
      "layer": "THINK",
      "domain": "CTX",
      "description": "对标Codex CLI 512K context + Gemini 1M+ token，实现长文本缓存与智能剪枝",
      "benchmark_system": "Codex CLI + Gemini 2.5",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/think/context_manager.py",
      "dependencies": ["INFRA-LOCAL-001"]
    },
    {
      "id": "THINK-MEM-001",
      "name": "Memory Bank长期记忆",
      "layer": "THINK",
      "domain": "MEM",
      "description": "对标Claude Agent SDK Memory Bank，实现持久化记忆存储、增量更新、语义检索",
      "benchmark_system": "Claude Agent SDK",
      "status": "IN_PROGRESS",
      "priority": "P1",
      "code_template_ref": "src/think/memory_bank.py",
      "dependencies": ["INFRA-LOCAL-003"]
    },
    {
      "id": "THINK-MEM-002",
      "name": "记忆增强自进化",
      "layer": "EVOL",
      "domain": "MEM",
      "description": "基于中文社区实践的记忆增强机制：自动技能发现、使用模式学习、偏好自适应",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/evol/memory_augment.py",
      "dependencies": ["THINK-MEM-001", "EVOL-REFLECT-001"]
    },
    {
      "id": "PLAN-REACT-001",
      "name": "ReAct推理-行动循环",
      "layer": "PLAN",
      "domain": "REACT",
      "description": "对标Codex CLI的ReAct/Reflexion循环模式：Think→Act→Observe→Reflect",
      "benchmark_system": "Codex CLI",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/plan/react_loop.py",
      "dependencies": ["THINK-LLM-001"]
    },
    {
      "id": "PLAN-REFLEX-001",
      "name": "Reflexion反思机制",
      "layer": "PLAN",
      "domain": "REFLEX",
      "description": "对标Codex CLI的Reflexion模式：失败后自动分析原因、调整策略、重新执行",
      "benchmark_system": "Codex CLI",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/plan/reflexion.py",
      "dependencies": ["PLAN-REACT-001", "THINK-MEM-001"]
    },
    {
      "id": "PLAN-PLANEXEC-001",
      "name": "Plan-Execute分步规划",
      "layer": "PLAN",
      "domain": "PLANEXEC",
      "description": "对标Codex CLI的Multi-step planning：先规划完整步骤链，再逐步执行并校验",
      "benchmark_system": "Codex CLI",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/plan/plan_execute.py",
      "dependencies": ["PLAN-REACT-001"]
    },
    {
      "id": "PLAN-CHECKPOINT-001",
      "name": "Checkpoint & Rollback",
      "layer": "PLAN",
      "domain": "CHECKPOINT",
      "description": "对标Codex CLI的Checkpoint机制：关键步骤自动存档，失败时可回滚至任意节点",
      "benchmark_system": "Codex CLI",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/plan/checkpoint.py",
      "dependencies": ["PLAN-PLANEXEC-001"]
    },
    {
      "id": "EXEC-CODE-001",
      "name": "全栈编码引擎",
      "layer": "EXEC",
      "domain": "CODE",
      "description": "对标Codex CLI编码引擎 + OpenCode工具链：代码生成、调试、重构、测试一体化",
      "benchmark_system": "Codex CLI + OpenCode",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/execute/code_engine.py",
      "dependencies": ["THINK-LLM-001", "TOOL-REGISTRY-001"]
    },
    {
      "id": "EXEC-CODE-002",
      "name": "Multi-Agent Coding",
      "layer": "EXEC",
      "domain": "CODE",
      "description": "对标AI IDE趋势：多Agent并行编码，代码审查Agent + 编码Agent + 测试Agent协同",
      "benchmark_system": "AI IDE趋势",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/multi_agent_coding.py",
      "dependencies": ["EXEC-CODE-001", "TOOL-REGISTRY-001"]
    },
    {
      "id": "EXEC-CODE-003",
      "name": "Autonomous PR",
      "layer": "EXEC",
      "domain": "CODE",
      "description": "对标AI IDE Autonomous PR：自动代码修改→生成PR→运行CI→根据结果迭代",
      "benchmark_system": "AI IDE趋势",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/execute/autonomous_pr.py",
      "dependencies": ["EXEC-CODE-002", "EXEC-GIT-001"]
    },
    {
      "id": "EXEC-CODE-004",
      "name": "代码预览卡片",
      "layer": "EXEC",
      "domain": "CODE",
      "description": "中文社区实践：手机端代码预览卡片，语法高亮、Diff对比、一键复制/运行",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/code_preview_card.tsx",
      "dependencies": ["EXEC-CODE-001"]
    },
    {
      "id": "EXEC-GIT-001",
      "name": "Git深度集成",
      "layer": "EXEC",
      "domain": "GIT",
      "description": "对标OpenCode + 中文社区：Git操作Agent化，自动commit、分支管理、冲突解决",
      "benchmark_system": "OpenCode + 中文社区实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/git_agent.py",
      "dependencies": ["EXEC-CODE-001"]
    },
    {
      "id": "EXEC-FILE-001",
      "name": "智能文件操作",
      "layer": "EXEC",
      "domain": "FILE",
      "description": "对标Marvis Workbody本地文件操作：读写、搜索、整理、转换一体化",
      "benchmark_system": "Marvis Workbody",
      "status": "IMPLEMENTED",
      "priority": "P0",
      "code_template_ref": "src/execute/file_ops.py",
      "dependencies": ["INFRA-LOCAL-002"]
    },
    {
      "id": "EXEC-FILE-002",
      "name": "文档深度处理",
      "layer": "EXEC",
      "domain": "FILE",
      "description": "豆包APP现有能力升级：PDF/Word/Excel/PPT解析、提取、生成、格式转换",
      "benchmark_system": "豆包APP现有",
      "status": "IMPLEMENTED",
      "priority": "P0",
      "code_template_ref": "src/execute/doc_processor.py",
      "dependencies": ["EXEC-FILE-001"]
    },
    {
      "id": "EXEC-SHELL-001",
      "name": "Shell执行沙箱",
      "layer": "EXEC",
      "domain": "SHELL",
      "description": "对标Marvis Workbody Shell执行 + Sandbox隔离：安全命令执行、环境隔离、资源限制",
      "benchmark_system": "Marvis Workbody",
      "status": "IN_PROGRESS",
      "priority": "P0",
      "code_template_ref": "src/execute/shell_sandbox.py",
      "dependencies": ["INFRA-SANDBOX-001"]
    },
    {
      "id": "EXEC-SHELL-002",
      "name": "端云协同执行",
      "layer": "EXEC",
      "domain": "SHELL",
      "description": "中文社区实践：本地执行优先，复杂任务云端卸载，执行结果自动同步",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/cloud_edge_executor.py",
      "dependencies": ["EXEC-SHELL-001", "INFRA-LOCAL-001"]
    },
    {
      "id": "TOOL-REGISTRY-001",
      "name": "Tool Registry中心化",
      "layer": "TOOL",
      "domain": "REGISTRY",
      "description": "对标Hermes Tool Registry：工具注册、发现、版本管理、参数校验中心化",
      "benchmark_system": "Hermes",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/tool/tool_registry.py",
      "dependencies": []
    },
    {
      "id": "TOOL-REGISTRY-002",
      "name": "技能自动发现与注册",
      "layer": "EVOL",
      "domain": "REGISTRY",
      "description": "中文社区实践：从使用模式中自动发现新技能，自动生成Tool Schema并注册",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/evol/auto_skill_discovery.py",
      "dependencies": ["TOOL-REGISTRY-001", "EVOL-OBSERVE-001"]
    },
    {
      "id": "TOOL-GATEWAY-001",
      "name": "Agent Gateway网关",
      "layer": "TOOL",
      "domain": "GATEWAY",
      "description": "对标OpenClaw：Agent Discovery + Message Routing + Auth/Quota管理",
      "benchmark_system": "OpenClaw",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/tool/agent_gateway.py",
      "dependencies": ["TOOL-REGISTRY-001"]
    },
    {
      "id": "TOOL-GATEWAY-002",
      "name": "消息导向中间件(MOM)",
      "layer": "TOOL",
      "domain": "GATEWAY",
      "description": "对标OpenClaw Message-Oriented Middleware：Agent间异步消息通信",
      "benchmark_system": "OpenClaw",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/tool/message_bus.py",
      "dependencies": ["TOOL-GATEWAY-001"]
    },
    {
      "id": "TOOL-GATEWAY-003",
      "name": "Dynamic Agent Composition",
      "layer": "TOOL",
      "domain": "GATEWAY",
      "description": "对标OpenClaw：根据任务动态组合多个Agent能力，运行时Agent编排",
      "benchmark_system": "OpenClaw",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/tool/dynamic_composer.py",
      "dependencies": ["TOOL-GATEWAY-001", "TOOL-REGISTRY-001"]
    },
    {
      "id": "TOOL-PLUGIN-001",
      "name": "插件生态管理器",
      "layer": "TOOL",
      "domain": "PLUGIN",
      "description": "升级豆包APP现有插件生态：插件市场、热加载、沙箱隔离、版本兼容性检查",
      "benchmark_system": "豆包APP现有",
      "status": "IN_PROGRESS",
      "priority": "P1",
      "code_template_ref": "src/tool/plugin_manager.py",
      "dependencies": ["INFRA-SANDBOX-001"]
    },
    {
      "id": "INFRA-LOCAL-001",
      "name": "本地模型部署(Ollama)",
      "layer": "INFRA",
      "domain": "LOCAL",
      "description": "对标Ollama + LM Studio：本地小模型部署、模型管理、量化推理",
      "benchmark_system": "Ollama + LM Studio",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/infra/ollama_deploy.py",
      "dependencies": []
    },
    {
      "id": "INFRA-LOCAL-002",
      "name": "本地向量数据库",
      "layer": "INFRA",
      "domain": "LOCAL",
      "description": "本地向量数据库：ChromaDB/LanceDB部署，支持语义搜索、RAG增强",
      "benchmark_system": "Local Vector DB",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/infra/vector_db.py",
      "dependencies": []
    },
    {
      "id": "INFRA-LOCAL-003",
      "name": "移动端本地推理引擎",
      "layer": "INFRA",
      "domain": "LOCAL",
      "description": "中文社区实践：MNN/ncnn/TFLite + Qualcomm AI Engine混合推理",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/infra/mobile_inference.py",
      "dependencies": ["INFRA-LOCAL-001"]
    },
    {
      "id": "INFRA-SANDBOX-001",
      "name": "多层安全沙箱",
      "layer": "INFRA",
      "domain": "SANDBOX",
      "description": "对标Marvis Workbody Sandbox：进程隔离、文件系统隔离、网络隔离三层防护",
      "benchmark_system": "Marvis Workbody",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/infra/sandbox.py",
      "dependencies": []
    },
    {
      "id": "INFRA-DEPLOY-001",
      "name": "Agent本地部署方案",
      "layer": "INFRA",
      "domain": "DEPLOY",
      "description": "完整本地部署方案：Docker Compose + 环境配置 + 健康检查 + 日志收集",
      "benchmark_system": "本地部署最佳实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "deploy/docker-compose.yml",
      "dependencies": ["INFRA-LOCAL-001", "INFRA-LOCAL-002"]
    },
    {
      "id": "EVOL-OBSERVE-001",
      "name": "执行观察器",
      "layer": "EVOL",
      "domain": "OBSERVE",
      "description": "自进化闭环第一步：全量行为日志采集、性能指标监控、异常检测",
      "benchmark_system": "自进化闭环",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/evol/observer.py",
      "dependencies": []
    },
    {
      "id": "EVOL-REFLECT-001",
      "name": "自我反思引擎",
      "layer": "EVOL",
      "domain": "REFLECT",
      "description": "自进化闭环第二步：失败模式分析、成功策略提炼、决策树优化",
      "benchmark_system": "自进化闭环",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/evol/reflect_engine.py",
      "dependencies": ["EVOL-OBSERVE-001", "THINK-MEM-001"]
    },
    {
      "id": "EVOL-UPDATE-001",
      "name": "能力自动更新器",
      "layer": "EVOL",
      "domain": "UPDATE",
      "description": "自进化闭环第三步：策略权重调整、Skill自动更新、模型微调触发",
      "benchmark_system": "自进化闭环",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/evol/auto_updater.py",
      "dependencies": ["EVOL-REFLECT-001", "TOOL-REGISTRY-001"]
    },
    {
      "id": "EXEC-MULTIMODAL-001",
      "name": "多模态对话引擎",
      "layer": "EXEC",
      "domain": "MULTIMODAL",
      "description": "豆包APP现有：图文混合输入、语音输入、多模态输出",
      "benchmark_system": "豆包APP现有",
      "status": "IMPLEMENTED",
      "priority": "P0",
      "code_template_ref": "src/execute/multimodal_engine.py",
      "dependencies": []
    },
    {
      "id": "EXEC-MULTIMODAL-002",
      "name": "语音+触控混合编码输入",
      "layer": "EXEC",
      "domain": "MULTIMODAL",
      "description": "中文社区实践：语音描述需求 + 触控选择代码模板，手机端编码交互优化",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/execute/voice_code_input.py",
      "dependencies": ["EXEC-MULTIMODAL-001", "EXEC-CODE-001"]
    },
    {
      "id": "THINK-AGENTGRAPH-001",
      "name": "Agent Graph执行引擎",
      "layer": "THINK",
      "domain": "AGENTGRAPH",
      "description": "对标Claude Agent SDK Agent Graph：DAG模式Agent编排，并行/串行/条件分支",
      "benchmark_system": "Claude Agent SDK",
      "status": "PLANNED",
      "priority": "P0",
      "code_template_ref": "src/think/agent_graph.py",
      "dependencies": ["THINK-LLM-001"]
    },
    {
      "id": "EXEC-IDE-001",
      "name": "Agentic IDE核心",
      "layer": "EXEC",
      "domain": "IDE",
      "description": "对标AI IDE趋势：内嵌代码编辑器、文件树、终端、调试器、Git面板",
      "benchmark_system": "AI IDE趋势",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/agentic_ide.py",
      "dependencies": ["EXEC-CODE-001", "EXEC-GIT-001", "EXEC-SHELL-001"]
    },
    {
      "id": "EXEC-IDE-002",
      "name": "Repo-aware上下文感知",
      "layer": "EXEC",
      "domain": "IDE",
      "description": "对标Codex CLI Repo-aware：自动感知项目结构、依赖关系、代码约定",
      "benchmark_system": "Codex CLI",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/repo_aware.py",
      "dependencies": ["EXEC-IDE-001", "THINK-CTX-001"]
    },
    {
      "id": "INFRA-LOCAL-004",
      "name": "端云协同架构",
      "layer": "INFRA",
      "domain": "LOCAL",
      "description": "中文社区实践：本地小模型处理简单任务+云端大模型处理复杂任务+无缝切换",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/infra/edge_cloud_bridge.py",
      "dependencies": ["INFRA-LOCAL-001", "INFRA-LOCAL-003"]
    },
    {
      "id": "THINK-LLM-003",
      "name": "多模型对比与投票",
      "layer": "THINK",
      "domain": "LLM",
      "description": "对标Hermes多模型调度：关键决策多模型投票、置信度评估、模型降级策略",
      "benchmark_system": "Hermes",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/think/model_voting.py",
      "dependencies": ["THINK-LLM-001"]
    },
    {
      "id": "PLAN-HIERARCHY-001",
      "name": "Hierarchical Agent分层",
      "layer": "PLAN",
      "domain": "HIERARCHY",
      "description": "对标Codex CLI Hierarchical Agent：主Agent分配子任务，子Agent独立执行并汇报",
      "benchmark_system": "Codex CLI",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/plan/hierarchical_agent.py",
      "dependencies": ["PLAN-PLANEXEC-001", "THINK-AGENTGRAPH-001"]
    },
    {
      "id": "TOOL-GATEWAY-004",
      "name": "多Agent注册中心",
      "layer": "TOOL",
      "domain": "GATEWAY",
      "description": "中文社区实践：基于消息队列的分布式Agent注册中心，心跳检测、负载均衡",
      "benchmark_system": "中文社区实践",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/tool/agent_registry.py",
      "dependencies": ["TOOL-GATEWAY-001", "TOOL-GATEWAY-002"]
    },
    {
      "id": "EXEC-FILE-003",
      "name": "文件整理智能体",
      "layer": "EXEC",
      "domain": "FILE",
      "description": "Upgraded: 智能文件分类、去重、归档，基于内容理解和用户习惯学习",
      "benchmark_system": "Marvis Workbody",
      "status": "IMPLEMENTED",
      "priority": "P1",
      "code_template_ref": "src/execute/file_organizer.py",
      "dependencies": ["EXEC-FILE-001", "THINK-MEM-001"]
    },
    {
      "id": "THINK-LLM-004",
      "name": "Long-Context Cache引擎",
      "layer": "THINK",
      "domain": "CTX",
      "description": "对标Gemini 2.5 Long-Context Cache：增量缓存、分级存储(热/温/冷)、智能淘汰",
      "benchmark_system": "Gemini 2.5",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/think/context_cache.py",
      "dependencies": ["THINK-CTX-001"]
    },
    {
      "id": "EXEC-CODE-005",
      "name": "代码审查Agent",
      "layer": "EXEC",
      "domain": "CODE",
      "description": "Multi-Agent Coding子组件：自动代码审查、安全漏洞扫描、最佳实践建议",
      "benchmark_system": "AI IDE趋势",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/code_reviewer.py",
      "dependencies": ["EXEC-CODE-002"]
    },
    {
      "id": "EXEC-CODE-006",
      "name": "测试生成Agent",
      "layer": "EXEC",
      "domain": "CODE",
      "description": "Multi-Agent Coding子组件：自动单元测试/集成测试生成、覆盖率分析",
      "benchmark_system": "AI IDE趋势",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/execute/test_generator.py",
      "dependencies": ["EXEC-CODE-002"]
    },
    {
      "id": "INFRA-SANDBOX-002",
      "name": "Docker容器化执行",
      "layer": "INFRA",
      "domain": "SANDBOX",
      "description": "代码执行隔离：Docker容器按需创建、资源限制(cgroup)、执行后自动清理",
      "benchmark_system": "Marvis Workbody + Docker",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/infra/docker_executor.py",
      "dependencies": ["INFRA-SANDBOX-001"]
    },
    {
      "id": "EVOL-FEEDBACK-001",
      "name": "用户反馈学习回路",
      "layer": "EVOL",
      "domain": "FEEDBACK",
      "description": "隐式+显式反馈融合：点赞/点踩、使用时长、任务完成率综合评价",
      "benchmark_system": "自进化闭环 + 中文社区实践",
      "status": "PLANNED",
      "priority": "P1",
      "code_template_ref": "src/evol/feedback_loop.py",
      "dependencies": ["EVOL-OBSERVE-001", "EVOL-REFLECT-001"]
    },
    {
      "id": "TOOL-REGISTRY-003",
      "name": "工具链版本兼容性管理",
      "layer": "TOOL",
      "domain": "REGISTRY",
      "description": "语义化版本兼容性矩阵：工具间依赖解析、破坏性变更检测、兼容性报告",
      "benchmark_system": "Hermes",
      "status": "PLANNED",
      "priority": "P2",
      "code_template_ref": "src/tool/version_compat.py",
      "dependencies": ["TOOL-REGISTRY-001"]
    }
  ],
  "gap_analysis": {
    "total_gaps": 12,
    "p0_gaps": [
      {
        "id": "GAP-P0-001",
        "capability": "THINK-LLM-002 (CoT深度推理)",
        "gap_description": "当前豆包APP缺少显式的Chain-of-Thought推理链，依赖模型隐式推理",
        "impact": "复杂多步任务成功率低，缺乏推理过程可解释性",
        "mitigation": "短期内使用提示工程模拟CoT，中期对标Gemini 2.5实现显式推理链"
      },
      {
        "id": "GAP-P0-002",
        "capability": "EXEC-CODE-001 (全栈编码引擎)",
        "gap_description": "无结构化编码Agent能力，无法自主完成编码-调试-测试闭环",
        "impact": "无法对标Codex/OpenCode等编码Agent，丧失开发者用户群",
        "mitigation": "优先实现Python/JS/Shell三类代码执行沙箱，再逐步扩展语言支持"
      },
      {
        "id": "GAP-P0-003",
        "capability": "TOOL-REGISTRY-001 (Tool Registry)",
        "gap_description": "工具调用无中心化注册机制，新增工具需修改核心代码",
        "impact": "工具生态扩展困难，插件间冲突风险高",
        "mitigation": "参考Hermes实现JSON Schema驱动的Tool Registry，支持热注册"
      }
    ],
    "p1_gaps": [
      {
        "id": "GAP-P1-001",
        "capability": "PLAN-REACT-001 (ReAct循环)",
        "gap_description": "当前无显式的Reasoning→Action→Observation循环框架"
      },
      {
        "id": "GAP-P1-002",
        "capability": "INFRA-SANDBOX-001 (安全沙箱)",
        "gap_description": "代码执行无隔离环境，存在安全风险"
      },
      {
        "id": "GAP-P1-003",
        "capability": "INFRA-LOCAL-001 (本地模型部署)",
        "gap_description": "纯云端依赖，离线场景能力大幅退化"
      },
      {
        "id": "GAP-P1-004",
        "capability": "EXEC-IDE-001 (Agentic IDE)",
        "gap_description": "无内嵌IDE能力，代码交互停留在纯文本层面"
      }
    ],
    "p2_gaps": [
      {
        "id": "GAP-P2-001",
        "capability": "EXEC-CODE-003 (Autonomous PR)",
        "gap_description": "无Git工作流自动化能力"
      },
      {
        "id": "GAP-P2-002",
        "capability": "EVOL-UPDATE-001 (自动更新器)",
        "gap_description": "自进化闭环未闭环，无自动策略更新机制"
      },
      {
        "id": "GAP-P2-003",
        "capability": "TOOL-GATEWAY-003 (Dynamic Composition)",
        "gap_description": "不支持运行时动态Agent组合"
      }
    ]
  },
  "deprecated_in_v2.3": [
    {
      "id": "DEP-001",
      "name": "单模型硬绑定模式",
      "reason": "被THINK-LLM-001多模型中枢调度替代"
    },
    {
      "id": "DEP-002",
      "name": "硬编码工具调用",
      "reason": "被TOOL-REGISTRY-001中心化注册替代"
    }
  ]
}

```
