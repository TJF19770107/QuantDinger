# AI量化交易全链路知识库 v1.0

> 生成时间：2026-05-31 | 覆盖范围：Marvis智能体 / OpenClaw-CN 0.2.0 / Obsidian知识库
> 关联目标：月收入 8k-10k → 10k-100k → 100k-1M | 固定账号：oAN1i2T3oDUM3UD3t8j7MCsSZjR4

---

## 一、Marvis 智能体模块

### 1.1 角色定位

Marvis 是腾讯应用宝团队打造的操作系统级 AI 助手（2026年5月20日上线），采用 **1 主 Agent + 5 专项 Agent** 的多智能体架构，通过自然语言操控整台电脑。

### 1.2 环境配置

| 配置项 | 当前状态 | 说明 |
|--------|----------|------|
| 运行平台 | Windows 10 (Build 19045) | 本地桌面环境 |
| 固定账号 | oAN1i2T3oDUM3UD3t8j7MCsSZjR4 | 龙虾全域账号 |
| 工作目录 | `C:\Users\Administrator\AppData\Roaming\Tencent\Marvis\User\oAN1i2T3oDUM3UD3t8j7MCsSZjR4\workspace\` | 会话工作区 |
| 端侧模式 | 待启用 | 数据不上云，断网可用 |
| 隐私模式 | 可选 | 基于腾讯自研 Qwen 端侧模型 |

**6 Agent 架构**：

| Agent | 职责 | 量化学场景 |
|-------|------|-----------|
| 主 Agent | 任务规划与派发 | 全链路调度 |
| File Agent | 文件搜索/分析/转换/整理 | 交易数据 CSV 管理、批量报表 |
| Computer Agent | 系统配置/窗口管理/进程控制 | 系统性能优化、端口治理 |
| App Agent | 应用操控（APK/EXE/小程序） | 交易终端自动化操作 |
| Browser Agent | 网页交互与数据采集 | 交易所页面数据抓取 |
| Search Agent | 深度联网检索 | 市场资讯与研报搜索 |

### 1.3 对接方式

```
量化数据流 → Marvis 调度层
    ├── File Agent：OKX API 数据 CSV → 格式转换 → 归档 quant_data/
    ├── Search Agent：实时研报/新闻 → 摘要 → 知识库归档
    ├── Browser Agent：交易所网页 → 数据抓取 → 本地存储
    ├── App Agent：交易终端 → 下单/监控自动化
    └── Computer Agent：系统资源监控 → 性能调优 → 备份调度
```

**已有量化数据路径**：`E:\龙虾AI主控中心\共享技能库\binance_skills\quant_data\`

**已产出量化文件**：

| 文件 | 说明 |
|------|------|
| DOGE_USDT_1D_FULL.csv | DOGE 日线全量数据（1440条） |
| DOGE_USDT_1W.csv | DOGE 周线数据 |
| DOGE_2021_key_nodes.csv | 2021 黑马行情关键节点 |
| black_horse_strategy.json | 黑马行情策略 |
| general_strategy.json | 通用交易策略 |
| psychology_profile.json | 交易心理画像 |
| LOBSTER-MICRO-DOGE-PLAN.json | 龙虾微操计划 |
| LOBSTER-QUANT-20260531-001.json | 龙虾量化计划文件 |

**12 共享技能库**（`E:\龙虾AI主控中心\Marvis\共享技能\`）：

| 技能 | 文件 | 量化学用途 |
|------|------|-----------|
| ECCFramework | ECCFramework.skill.md | 事件驱动执行框架，策略触发 |
| EternalMemory | EternalMemory.skill.md | 交易记忆持久化 |
| HermesBridge | HermesBridge.skill.md | 跨 Agent 通信 |
| KBArchiving | KBArchiving.skill.md | 知识库标准化归档 |
| LearningLoop | LearningLoop.skill.md | 周期性策略学习迭代 |
| Lobster5Steps | Lobster5Steps.skill.md | 执行方法论框架 |
| MultiAgentSync | MultiAgentSync.skill.md | 多 Agent 状态同步 |
| OpenClaw Core | OpenClaw Core.skill.md | OpenClaw 核心引擎 |
| ProductivityForge | ProductivityForge.skill.md | 自动化工作流构建 |
| RevenueEngine | RevenueEngine.skill.md | 营收目标分解与监控 |
| ReverseEngineering | ReverseEngineering.skill.md | 策略逆向工程 |
| SkillOrchestrator | SkillOrchestrator.skill.md | 12 技能动态调度 |

### 1.4 优化清单

| 编号 | 优化项 | 优先级 | 执行方式 |
|------|--------|--------|----------|
| M-01 | 启用端侧模式处理敏感交易数据 | 🔴 高 | Computer Agent 配置 |
| M-02 | 建立量化工作流模板（数据拉取→指标计算→策略生成→回测→归档） | 🔴 高 | SkillOrchestrator 编排 |
| M-03 | 创建 quant_data 目录定时备份任务 | 🟡 中 | 定时任务 + EternalMemory |
| M-04 | 将 DOGE 分析工作流抽象为可复用 Skill | 🟡 中 | LearningLoop 迭代 |
| M-05 | OKX API 对接标准化（替代币安 API Key 缺口） | 🔴 高 | OpenClaw Core + MCP |
| M-06 | 本地知识库索引 quant_data 目录 | 🟡 中 | Marvis 本地知识库功能 |
| M-07 | 多市场扩展（BTC/ETH/SOL 等） | 🟢 低 | LearningLoop 周期执行 |
| M-08 | 白名单 URL 扩容量化交易源 | 🟡 中 | Lobster5Steps 第2步 |

---

## 二、OpenClaw-CN 0.2.0 模块

### 2.1 角色定位

OpenClaw 是 GitHub 24.8 万星的**开源多 Agent 协同框架**，让大模型获得本地操作系统权限。龙虾本地部署版本为 **0.2.0**，运行在 Windows 本地环境。

### 2.2 环境配置

| 配置项 | 当前值 | 说明 |
|--------|--------|------|
| 版本 | 0.2.0 | 最后更新 2026-04-24 |
| 运行时目录 | `E:\龙虾AI主控中心\OpenClaw运行时\` | 主运行时 |
| 状态目录 | `E:\龙虾AI主控中心\.openclaw_runtime\` | 状态持久化 |
| 配置文件 | `E:\龙虾AI主控中心\.openclaw_runtime\openclaw.runtime.json` | 完整配置 |
| 网关端口 | 18791 | loopback 绑定 |
| 网关模式 | local | 本地运行 |
| 认证模式 | token | `${OPENCLAW_GATEWAY_TOKEN}` |
| 通信管道 | `E:\龙虾AI主控中心\OpenClaw运行时\comm_pipes\doubao_in` | 豆包 Agent 接入 |
| 工具集 | full profile | 全部工具启用 |

**模型配置**：

| Provider | 模型 | Base URL | 上下文窗口 |
|----------|------|----------|------------|
| ollama | kimi-k2.6:cloud | http://127.0.0.1:11435 | 262,144 |
| ollama-ollama5f | minimax-m2.7:cloud | http://localhost:11434 | 200,000 |

**Agent 默认配置**：

| 参数 | 值 |
|------|-----|
| 主模型 | minimax-m2.7:cloud |
| 最大并发 | 4 |
| Sub-Agent 最大并发 | 8 |

**四大核心模块**：

| 模块 | 功能 | 状态 |
|------|------|------|
| 渠道适配器 | 飞书/钉钉/Telegram/Discord/Slack | 已配置豆包 Agent 管道 |
| 智能决策核心 | 多模型路由，任务驱动选择 | 双模型就绪 |
| 技能插件系统 | 浏览器控制/邮件/代码执行 | 8 项技能已启用 |
| 双模记忆系统 | 本地长期学习，隐私可控 | 本地运行 |

### 2.3 对接待业方式

```
OpenClaw 0.2.0 生态对接
├── Marvis 智能体 ←→ OpenClaw Core 技能（MCP 协议）
├── Obsidian 知识库 ←→ KBArchiving 技能（自动归档）
├── 豆包 Agent ←→ comm_pipes/doubao_in（双向通信管道）
├── 飞书机器人 ←→ 渠道适配器（待配置）
├── 腾讯云 COS ←→ 同步脚本（已就绪）
└── 量化交易引擎 ←→ MCP 工具链（OKX API 已对接）
```

**MCP 协议支持**：

| 工具类型 | 用途 |
|----------|------|
| 文件系统工具 | 读写本地交易数据 |
| 浏览器工具 | 网页自动化抓取 |
| Shell 工具 | 命令行执行（Python 策略脚本） |
| API 工具 | OKX/天气/新闻行情 |

**环境变量**：
- `OPENCLAW_GATEWAY_TOKEN`：已配置（token 模式认证）
- 端口治理：5432（PostgreSQL）/ 6379（Redis）/ 11434（Ollama API）/ 8080（llama-server）

### 2.4 优化清单

| 编号 | 优化项 | 优先级 | 执行方式 |
|------|--------|--------|----------|
| O-01 | 升级至最新 OpenClaw 版本 | 🔴 高 | App Agent 执行 |
| O-02 | 补充量化交易 Skill（基于 binance_skills 模板） | 🔴 高 | SkillOrchestrator |
| O-03 | 配置飞书渠道适配器（读取已有密钥） | 🟡 中 | OpenClaw 渠道配置 |
| O-04 | 启用 Hermes Agent 学习闭环集成 | 🟡 中 | HermesBridge 技能 |
| O-05 | 扩展 MCP 工具链（添加 OKX WebSocket 实时行情） | 🔴 高 | MCP 协议扩展 |
| O-06 | 双模型路由策略优化（量化任务用 kimi-k2.6，文本用 minimax-m2.7） | 🟡 中 | OpenClaw 模型配置 |
| O-07 | 豆包 Agent 双向通信稳定性测试 | 🟡 中 | comm_pipes 管道测试 |
| O-08 | 技能商店补充：自动回测 Skill / 风控 Skill | 🟢 低 | LearningLoop 迭代 |

---

## 三、Obsidian 知识库模块

### 3.1 角色定位

Obsidian 是龙虾全链路知识管理中枢，`E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\` 是与 Marvis 共享知识库同步的企业级知识图谱基础设施。

### 3.2 环境配置

| 配置项 | 当前状态 | 说明 |
|--------|----------|------|
| 知识库根目录 | `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\` | Obsidian Vault |
| 共享知识库 | `共享知识库\` | 与 Marvis 双向同步 |
| 文件数量 | 19 个 .md | 纯 Markdown |
| 目录结构 | 完全扁平 | ⚠️ 需改造为 PARA + MOC |
| YAML Frontmatter | 零使用 | ❌ 需补全 |
| 双向链接 `[[]]` | 零使用 | ❌ 核心缺失 |
| 标签 `#tag` | 零使用 | ❌ 核心缺失 |
| 命名规范 | 日期格式混用 | ⚠️ 需统一 |
| 内容质量 | 结构化表格、来源可追溯 | ✅ 优秀 |

**Obsidian 配置**：

| 文件 | 说明 |
|------|------|
| `.obsidian\app.json` | 应用配置 |
| `.obsidian\appearance.json` | 外观配置 |
| `.obsidian\community-plugins.json` | 社区插件 |
| `.obsidian\core-plugins.json` | 核心插件 |
| `.obsidian\hotkeys.json` | 快捷键 |
| `.obsidian\workspace.json` | 工作区布局 |

**现有共享知识库文件分类**：

| 领域 | 文件数 | 代表性文件 |
|------|--------|-----------|
| AI Agent 生态 | 7 | AI智能体生态与技术栈 / AI Agent MCP多智能体 |
| 工具与平台 | 4 | 腾讯Marvis系统级AI助手 / OpenClaw_Hermes开源Agent生态 |
| 业务场景 | 3 | 量化交易与营收业务技术方案 / AI网文创作工具生态 |
| 执行报告 | 3 | 龙虾五步法执行完成验证报告 / 三源模板校验 |
| 知识管理 | 2 | Obsidian知识库入门与共享知识库适配指南 / 公众号文章自动订阅 |

**Marvis 共享知识库同步路径**：

```
E:\龙虾AI主控中心\Marvis\共享知识库\  ←→  E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\
```

### 3.3 对接方式

```
知识库对接架构
├── Marvis Agent 采集层
│   ├── Search Agent → 外部内容采集
│   ├── File Agent → 本地文件索引
│   └── 自动生成 _知识库.md → 0-Inbox/
├── Obsidian 知识图谱层
│   ├── YAML Frontmatter 元数据
│   ├── [[双向链接]] 知识网络
│   ├── #标签 分类体系
│   └── MOC 内容地图导航
├── 云备份层
│   ├── 腾讯云 COS → 云端持久化
│   ├── GitHub 每日备份（logs/github-backup/）
│   └── 云端备份目录（多级嵌套待整理）
└── 查询与分析层
    ├── Dataview 动态仪表盘
    ├── 图谱视图（Graph View）
    └── 全文检索 + 标签过滤
```

**对标 PARA + MOC 规划目录**：

```
共享知识库/
├── 0-Inbox/            ← 新采集内容的临时入口
├── 1-AI-Agent/         ← AI Agent 生态所有笔记
├── 2-协议与架构/        ← MCP/协议/架构设计
├── 3-工具与平台/        ← Marvis/OpenClaw/本地部署
├── 4-业务场景/          ← 量化交易/网文创作/营收方案
├── 5-知识管理/          ← Obsidian 使用技巧/公众号订阅
├── 6-MOC/              ← Map of Content 索引笔记
├── 7-执行报告/          ← 龙虾五步法/校验报告
└── 8-归档/             ← 已过时但保留的笔记
```

### 3.4 优化清单

| 编号 | 优化项 | 优先级 | 执行方式 |
|------|--------|--------|----------|
| OB-01 | 创建 9 个 PARA + MOC 子目录 | 🔴 高 | File Agent 批量操作 |
| OB-02 | 统一重命名全部文件（YYYY-MM-DD_主题_类型.md） | 🔴 高 | File Agent 批量重命名 |
| OB-03 | 为所有文件补 YAML Frontmatter + 标签 | 🔴 高 | 脚本批量注入 |
| OB-04 | 为所有文件添加 `## 相关笔记` + `[[]]` 双向链接 | 🔴 高 | 按主题聚类补链 |
| OB-05 | 创建 5 篇 MOC 索引笔记（AI Agent / 协议架构 / 工具平台 / 业务场景 / 执行报告） | 🔴 高 | 手动 + Agent 辅助 |
| OB-06 | 安装核心插件：Dataview / Templater / Tag Wrangler / Linter | 🔴 高 | App Agent 安装 |
| OB-07 | 创建 Dataview 数据仪表盘笔记 | 🟡 中 | Templater 模板 |
| OB-08 | 创建量化交易业务 MOC（关联已有 18 篇笔记） | 🟡 中 | MOC 索引构建 |
| OB-09 | Obsidian Git 插件启用 → GitHub 版本控制 | 🟡 中 | 插件安装 + 仓库配置 |
| OB-10 | 云端备份目录去重整理（目前多级嵌套严重） | 🟡 中 | DirOps MD5 去重 |
| OB-11 | 设定知识库入库 SOP 模板（Templater） | 🟢 低 | 模板创建 |
| OB-12 | 月度归档 + 图谱健康巡检自动化 | 🟢 低 | 定时任务 |

---

## 四、三模块协同架构总览

### 4.1 协同拓扑图

```
                     ┌──────────────────────────┐
                     │    Obsidian 知识库        │
                     │  (知识图谱 + 双向链接)     │
                     │  共享知识库/ ←→ Marvis/   │
                     └──────────┬───────────────┘
                                │ KBArchiving / EternalMemory
                                │
    ┌───────────────────────────┼───────────────────────────┐
    │                           │                           │
    ▼                           ▼                           ▼
┌───────────┐          ┌───────────────┐          ┌───────────────┐
│  Marvis   │◄────────►│ OpenClaw 0.2  │◄────────►│  外部数据源    │
│ 1主+5专项 │ MCP/A2A  │ 多Agent协同   │  MCP协议  │ OKX/B站/GitHub │
│  智能体   │          │ 24.8万星框架  │          │  腾讯云COS     │
└─────┬─────┘          └───────┬───────┘          └───────────────┘
      │                        │
      │         ┌──────────────┴──────────────┐
      │         │                             │
      ▼         ▼                             ▼
┌─────────────────────────────────────────────────┐
│              量化交易全链路执行层                  │
│  DOGE/BTC/ETH 数据 → 指标计算 → 策略生成 → 回测  │
│  产出: black_horse_strategy / general_strategy   │
└─────────────────────────────────────────────────┘
```

### 4.2 协同通信协议

| 通信链路 | 协议 | 状态 |
|----------|------|------|
| Marvis ↔ OpenClaw | MCP / A2A | 已配置 OpenClaw Core 技能 |
| Marvis ↔ Obsidian | KBArchiving 技能 + 文件同步 | 双向同步已就绪 |
| OpenClaw ↔ 豆包 Agent | comm_pipes/doubao_in | 管道已创建 |
| OpenClaw ↔ Ollama | HTTP API (11434/11435) | 双模型就绪 |
| OpenClaw ↔ 飞书 | 渠道适配器 | 待配置 |
| 全链路 ↔ 腾讯云 COS | COS SDK | 同步脚本已就绪 |

### 4.3 技能调度矩阵

| 量化场景 | Marvis Agent | OpenClaw 技能 | Obsidian |
|----------|-------------|---------------|----------|
| 数据拉取 | File Agent | MCP 工具链 | — |
| 策略生成 | 主 Agent (Python) | OpenClaw Core | 归档 MOC |
| 回测执行 | App Agent | ECCFramework | 执行报告 |
| 研报解读 | Search Agent | — | 知识库 |
| 系统监控 | Computer Agent | ProductivityForge | — |
| 营收追踪 | — | RevenueEngine | Dataview 仪表盘 |
| 学习迭代 | LearningLoop | ReverseEngineering | 知识库更新 |
| 备份归档 | File Agent | EternalMemory | 云备份同步 |

---

## 五、营收路径映射

| 阶段 | 目标 | 依赖模块 | 量化策略 |
|------|------|----------|----------|
| 第一阶段 8k-10k/月 | 策略回测服务 / AI选股日报 | Marvis + OKX 数据 | DOGE 黑马策略 v1.0 |
| 第二阶段 10k-100k/月 | 多Agent策略平台 / 培训课程 | OpenClaw 多智能体框架 | 多币种矩阵策略 |
| 第三阶段 100k-1M/月 | 自营量化基金 / SaaS平台 | 三模块全链路协同 | 机构级风控策略 |

---

> **版本**: v1.0 | **生成日期**: 2026-05-31 | **关联技能**: 全部12技能 ACTIVE
> **双轨备份**: `E:\龙虾AI主控中心\Marvis\共享知识库\` ←→ `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\共享知识库\`
