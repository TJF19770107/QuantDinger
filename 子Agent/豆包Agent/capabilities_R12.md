# capabilities_R12.json

> 原始文件: `capabilities_R12.json`  |  类型: `.json`  |  自动转换

```json
{
  "meta": {
    "version": "R12",
    "date": "2026-05-31",
    "total_capabilities": 36,
    "agent": "豆包Agent",
    "template": "龙虾全域官方模板-最终版v3.0",
    "previous_version": "R11 (33项)"
  },
  "capabilities": [
    {
      "id": 1,
      "name": "本地文件自主读取",
      "status": "STABLE",
      "version": "S01_v2.1",
      "source": "Hermes Episodic Memory + OpenClaw Workspace",
      "layer": "Layer2",
      "description": "本地文件自主读取、索引构建、智能分类、增量监控",
      "r12_change": null
    },
    {
      "id": 2,
      "name": "自主技能生成",
      "status": "STABLE",
      "version": "S02_v2.3",
      "source": "NVIDIA Verified Skills + Superpowers声明式标准",
      "layer": "Layer3",
      "description": "自主技能生成闭环：模式提取→质量评估→SKILL.md生成→注册",
      "r12_change": "GAP-004关闭：融合Superpowers声明式标准，v2.2→v2.3"
    },
    {
      "id": 3,
      "name": "桌面程序控制",
      "status": "STABLE",
      "version": "S03_v2.0",
      "source": "Codex macOS多应用 + Marvis操作系统级",
      "layer": "Layer2",
      "description": "三层安全控制：Shell→API→自动化，含安全白名单",
      "r12_change": null
    },
    {
      "id": 4,
      "name": "自主唤醒与执行",
      "status": "STABLE",
      "version": "S04_v2.3",
      "source": "Hermes cron + OpenClaw HEARTBEAT + FORGE广播",
      "layer": "Layer2",
      "description": "P0-P3任务优先级调度、4小时自动唤醒、超时熔断",
      "r12_change": "+Hermes动态优先级自适应调度，v2.2→v2.3"
    },
    {
      "id": 5,
      "name": "记忆自动加载",
      "status": "STABLE",
      "version": "S05_v2.3",
      "source": "OpenClaw SQLite-vec + Anthropic Tool Search",
      "layer": "Layer2",
      "description": "三层记忆体系：工作/会话/长期 + FTS5全文检索 + 向量化语义检索",
      "r12_change": "+向量化检索落地(GAP-005推进)，v2.2→v2.3"
    },
    {
      "id": 6,
      "name": "自我修正回滚",
      "status": "STABLE",
      "version": "S06_v2.2",
      "source": "FORGE毕业冻结 + GEA经验池 + Merkle回滚",
      "layer": "Layer6",
      "description": "三环安全：外环审查→中环监控→内环回滚 + 反蒸馏协议",
      "r12_change": null
    },
    {
      "id": 7,
      "name": "多Agent协调",
      "status": "ACTIVE",
      "version": "v2.4",
      "source": "Hermes Kanban Swarm v0.13 + OpenCode后台Agent",
      "layer": "Layer5",
      "description": "多Agent编排：Kanban看板+辩论引擎+异步任务引擎",
      "r12_change": "+OpenClaw语义匹配路由机制，v2.3→v2.4"
    },
    {
      "id": 8,
      "name": "安全审查Agent",
      "status": "ACTIVE",
      "version": "S06_v2.2",
      "source": "Hermes v0.13 brainworm三卡口",
      "layer": "Layer6",
      "description": "安全审查与威胁检测",
      "r12_change": null
    },
    {
      "id": 9,
      "name": "技术情报汇总",
      "status": "COMPLETED",
      "version": "R12",
      "source": "15路并行检索+40+信源",
      "layer": "Layer3",
      "description": "本轮产出：R12 v12.0报告 + 3新缺口 + 3新能力",
      "r12_change": "R11→R12情报汇总"
    },
    {
      "id": 10,
      "name": "技能库同步",
      "status": "COMPLETED",
      "version": "v2.4",
      "source": "NVIDIA技能治理 + ClawHub v4.1 + Superpowers生态",
      "layer": "Layer3",
      "description": "技能库版本同步与生态对齐",
      "r12_change": "+SkillForge v2.3同步"
    },
    {
      "id": 11,
      "name": "本地执行Agent",
      "status": "ACTIVE",
      "version": "S01_v2.1",
      "source": "DesktopController+AutoFileScanner",
      "layer": "Layer2",
      "description": "本地任务执行Agent组合",
      "r12_change": null
    },
    {
      "id": 12,
      "name": "架构设计",
      "status": "COMPLETED",
      "version": "v5.2",
      "source": "八层架构+十大对标",
      "layer": "All",
      "description": "八层架构全景设计：Layer1-自进化闭环~Layer8-感知扩展层",
      "r12_change": "+Layer 8感知扩展层 + AI on UI/Llama/Claude 3D对标，v5.1→v5.2"
    },
    {
      "id": 13,
      "name": "能力对标矩阵",
      "status": "COMPLETED",
      "version": "R12_v12.0",
      "source": "10系统×40维度",
      "layer": "All",
      "description": "十大对标系统能力矩阵（新增AI on UI/Llama/Claude 3D维度）",
      "r12_change": "新增3个对标维度"
    },
    {
      "id": 14,
      "name": "自进化Agent",
      "status": "ACTIVE",
      "version": "v2.2",
      "source": "FORGE广播+GEA经验池融合",
      "layer": "Layer3",
      "description": "自进化闭环：观察→反思→更新→执行",
      "r12_change": null
    },
    {
      "id": 15,
      "name": "记忆系统Agent",
      "status": "ACTIVE",
      "version": "S05_v2.3",
      "source": "三层架构+SQLite-vec+向量化检索",
      "layer": "Layer2",
      "description": "完整记忆系统：FTS5全文检索+向量相似度匹配",
      "r12_change": "+向量化检索全链路落地，v2.2→v2.3"
    },
    {
      "id": 16,
      "name": "主方案生成",
      "status": "COMPLETED",
      "version": "R12",
      "source": "15路情报合成",
      "layer": "All",
      "description": "本轮产出：R12 v12.0报告 + 缺口v2.6 + 能力v4.4",
      "r12_change": "R12全面方案生成"
    },
    {
      "id": 17,
      "name": "全网技术扫描",
      "status": "COMPLETED",
      "version": "15路并行+40信源",
      "source": "10大系统深度分析",
      "layer": "Layer3",
      "description": "全网技术情报采集与汇总",
      "r12_change": "新增：AI on UI/Llama/Claude 3D"
    },
    {
      "id": 18,
      "name": "持久目标引擎",
      "status": "DESIGNED",
      "version": "R06设计",
      "source": "Hermes /goal + HEARTBEAT",
      "layer": "Layer5",
      "description": "GoalStore持久化目标追踪",
      "r12_change": null
    },
    {
      "id": 19,
      "name": "任务看板系统",
      "status": "DESIGNED",
      "version": "R06设计+R12增强",
      "source": "Hermes Kanban Swarm v0.13 + OpenCode v2.0",
      "layer": "Layer5",
      "description": "Kanban看板+心跳回收+僵尸检测+可视化编排参考",
      "r12_change": "+OpenCode v2.0可视化编排参考"
    },
    {
      "id": 20,
      "name": "检查点快照系统",
      "status": "DESIGNED",
      "version": "R06设计",
      "source": "Hermes v0.13 Checkpoints v2 真修剪",
      "layer": "Layer5",
      "description": "Checkpoints快照+真修剪+断点恢复",
      "r12_change": null
    },
    {
      "id": 21,
      "name": "Agent通信协议",
      "status": "DESIGNED",
      "version": "R06设计",
      "source": "MCP+A2A+ACP三协议栈",
      "layer": "Layer5",
      "description": "多协议Agent通信栈",
      "r12_change": null
    },
    {
      "id": 22,
      "name": "代码智能感知",
      "status": "DESIGNED",
      "version": "R06设计",
      "source": "OpenCode LSP",
      "layer": "Layer4",
      "description": "LSP语言服务器自动加载+15种语言支持",
      "r12_change": null
    },
    {
      "id": 23,
      "name": "Meta自进化引擎",
      "status": "DESIGNED",
      "version": "R06设计",
      "source": "FORGE广播+GEA群体元学习",
      "layer": "Layer3",
      "description": "群体层面的元学习与自进化",
      "r12_change": null
    },
    {
      "id": 24,
      "name": "40维能力热力图",
      "status": "COMPLETED",
      "version": "R12",
      "source": "10系统×40维度",
      "layer": "All",
      "description": "跨系统能力差距热力图可视化",
      "r12_change": "新增AI on UI/Llama/Claude 3D维度"
    },
    {
      "id": 25,
      "name": "GEP基因组协议",
      "status": "DESIGNED",
      "version": "R06设计",
      "source": "Evolver",
      "layer": "Layer3",
      "description": "基因组编码协议，用于跨Agent能力传递",
      "r12_change": null
    },
    {
      "id": 26,
      "name": "IDE集成入口",
      "status": "DESIGNED",
      "version": "R06设计(R11重定位)",
      "source": "→ 三层栈适配器定位",
      "layer": "Layer5",
      "description": "三层栈适配器（放弃自建IDE，适配Cursor→Claude Code→Codex三层栈）",
      "r12_change": null
    },
    {
      "id": 27,
      "name": "豆包ACP v1.0",
      "status": "DESIGNED",
      "version": "R06设计",
      "source": "MCP/A2A/ACP三协议",
      "layer": "Layer5",
      "description": "自定义Agent通信协议",
      "r12_change": null
    },
    {
      "id": 28,
      "name": "代码模块精简(≥40%)",
      "status": "CLOSED",
      "version": "R10",
      "source": "Hermes v0.15 76%标杆",
      "layer": "All",
      "description": "代码模块精简优化（已关闭归档）",
      "r12_change": null
    },
    {
      "id": 29,
      "name": "群体自进化引擎",
      "status": "ACTIVE",
      "version": "v1.0",
      "source": "FORGE(冠军广播) + GEA(群体元学习)",
      "layer": "Layer3",
      "description": "多Agent群体层面的自进化协调",
      "r12_change": null
    },
    {
      "id": 30,
      "name": "脑虫防御系统",
      "status": "ACTIVE",
      "version": "v1.0",
      "source": "Hermes v0.13 brainworm三卡口",
      "layer": "Layer6",
      "description": "提示注入/脑虫攻击三卡口防御体系",
      "r12_change": null
    },
    {
      "id": 31,
      "name": "ToolCall 2.0管道",
      "status": "PLANNED",
      "version": "v1.0",
      "source": "Anthropic编程式工具调用+动态过滤+工具搜索",
      "layer": "Layer2",
      "description": "TypeScript编排→动态HTML过滤→懒加载工具定义",
      "r12_change": null
    },
    {
      "id": 32,
      "name": "Skills标准适配器",
      "status": "PLANNED",
      "version": "v1.0+",
      "source": "Superpowers v5.1 8平台通用Skills标准",
      "layer": "Layer3",
      "description": "声明式Skills→跨平台发现→MIT开源生态接入",
      "r12_change": "随GAP-004关闭完成声明式标准对齐"
    },
    {
      "id": 33,
      "name": "后台Agent引擎",
      "status": "PLANNED",
      "version": "v1.0",
      "source": "OpenCode v1.15后台子Agent+Hermes Kanban持久化",
      "layer": "Layer5",
      "description": "非阻塞执行→事件推送→心跳监控→僵尸回收",
      "r12_change": null
    },
    {
      "id": 34,
      "name": "AI on UI自动化引擎",
      "status": "PLANNED",
      "version": "v1.0",
      "source": "AI on UI v3.0（跨平台识别97%+动态UI适配92%）",
      "layer": "Layer8",
      "description": "跨平台UI元素识别→无代码录制自动化→动态UI布局自适应→自动化测试集成",
      "r12_change": "R12新增能力"
    },
    {
      "id": 35,
      "name": "Llama本地推理适配",
      "status": "PLANNED",
      "version": "v1.0",
      "source": "Llama Edge + 端侧分布式推理 + 安全模块",
      "layer": "Layer8",
      "description": "一键本地部署→端侧推理加速→多设备分布式协同→本地数据加密防窃取",
      "r12_change": "R12新增能力"
    },
    {
      "id": 36,
      "name": "3D能力预留接口",
      "status": "PLANNED",
      "version": "v1.0",
      "source": "Claude 3D能力体系（多模态融合93%+空间重建误差1.2%）",
      "layer": "Layer8",
      "description": "多模态融合接口预留→3D场景重建管线→AR/VR实时交互适配(<100ms)",
      "r12_change": "R12新增能力"
    }
  ],
  "statistics": {
    "total": 36,
    "stable": 8,
    "active": 11,
    "completed": 7,
    "designed": 7,
    "planned": 3,
    "closed": 1
  },
  "layer_distribution": {
    "Layer1_自进化闭环": 0,
    "Layer2_本地执行层": 7,
    "Layer3_自进化核心层": 10,
    "Layer4_智能感知层": 1,
    "Layer5_多Agent编排层": 8,
    "Layer6_安全治理层": 3,
    "Layer7_知识联动层": 0,
    "Layer8_感知扩展层": 3,
    "All_跨层": 4
  },
  "new_in_r12": {
    "capabilities": [34, 35, 36],
    "upgraded": [2, 4, 5, 7, 12, 15, 17, 32],
    "closed_gaps": ["GAP-004"],
    "new_gaps": ["GAP-031", "GAP-032", "GAP-033"]
  }
}

```
