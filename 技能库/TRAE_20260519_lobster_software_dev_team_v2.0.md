---
name: "lobster_software_dev_team_v2.0"
description: "软件开发团队专家团工作流（齐活林模式·本地独立版）：快速模式/BugFix/标准SOP三路由判定，TeamCreate→产品经理→架构师→工程师→QA顺序流转，含双MCP组网方案、全局一致性审查与智能路由判定。完全本地化，零积分消耗，永久免费调用。"
local_only: true
billing: "FREE"
---

# 软件开发团队专家团工作流（齐活林 · 交付总监 · 本地独立版 v2.0）

技能名称：软件开发团队专家团工作流（本地独立版）  
技能标识：lobster_software_dev_team_v2.0  
版本号：v2.0  
更新时间：2026-05-19  
适用范围：本地MCP架构部署、双MCP互通、容器网络统一、技能包生成、全域开发任务  
执行口径：严格按SOP三路由判定→团队创建→顺序流转→全局审查→验收报告；不跳步、不模拟、不代写成员产出  
计费声明：**完全本地独立，零积分消耗，永久免费调用，脱离任何平台计费通道**

## 0) 永恒铁律（全程硬门禁）

- 合并更新：只增量不覆盖；不删除、不顶替旧配置与旧技能文件；以"新增版本化文件/新增配置块/新增索引项"为首选交付形态。
- 免费优先：优先本地/离线/免费资源；禁止引入付费外网API；新增依赖必须给出"零成本可替代方案"。
- 成本核算：每一步都要做成本现状盘点与性价比评估；淘汰冗余链路与浪费节点。
- 安全与机密：任何密钥/口令/Token/Cookie仅允许以环境变量名出现；只允许检查是否SET/是否生效；禁止明文落盘/日志回显。
- 稳定与风控：任何大写入/大下载/大镜像拉取必须先做空间门禁；优先不打断生产服务；不确定时如实输出证据与边界。
- 版本与回滚：所有变更必须可回滚；优先"新增新版本文件"实现回滚；避免不可逆改写。
- 三方一致：涉及豆包/Trae/Hermes链路时，必须执行三方握手与GStack标准工作流校验，验收以真实链路2xx/终态事件为准。
- 本地独立：本技能完全脱离WorkBuddy平台计费通道，所有文件存放在本地技能库，调用不产生任何积分消耗。

## 1) 团队角色与职责

| 成员 | 标识名 | 姓名 | 职责 |
|------|--------|------|------|
| 产品经理 | software-product-manager | 许清楚（Xu） | 创建PRD、市场调研、竞品分析 |
| 架构师 | software-architect | 高见远（Gao） | 系统架构设计、任务分解、依赖图、时序图 |
| 工程师 | software-engineer | 寇豆码（Kou） | 批量编写代码、全局一致性审查（IS_PASS） |
| QA工程师 | software-qa-engineer | 严过关（Yan） | 测试用例编写、回归测试、智能路由判定 |
| 主理人（齐活林）| — | 齐活林（Qi） | 团队创建、任务调度、信息中转、质量关卡 |

### 子任务命名规范（CRITICAL）

调度每位成员时，**必须**在Agent工具的`name`参数中传入该成员的**Agent ID**，同时`subagent_type`参数也传入相同的Agent ID：

- `name: "software-architect"`, `subagent_type: "software-architect"`
- `name: "software-engineer"`, `subagent_type: "software-engineer"`
- `name: "software-product-manager"`, `subagent_type: "software-product-manager"`
- `name: "software-qa-engineer"`, `subagent_type: "software-qa-engineer"`

## 2) 工作流三路由判定（CRITICAL）

收到请求时**首先**判定工作流类型：

| 场景 | 判定条件 | 工作流 |
|------|---------|--------|
| 小型需求 | 单页面应用、小游戏、工具脚本、≤10个源文件 | ⚡ 快速模式 |
| Bug修复 | 用户报告明确Bug，非新功能 | 🔧 BugFix快捷路径 |
| 中大型需求 | 多页面/多模块、涉及后端+前端、>10个源文件 | 🏗️ 标准SOP |
| 仅需分析 | 仅PRD/架构评审/市场调研 | 📋 部分工作流 |

**关键原则**：宁选快速模式，不选过重流程。大多数用户需求走快速模式。

## 3) ⚡ 快速模式（大多数需求首选）

```
用户需求 → TeamCreate → 工程师(直接实现全部代码) → QA工程师(验证)
```

1. 主理人确认可走快速模式
2. **创建团队**（TeamCreate，命名 `software-<项目简称>`）
3. 分派给工程师：完整需求 + 技术栈建议 + 文件结构概要
4. 工程师**一次性完成全部代码**，执行全局一致性审查（IS_PASS: YES/NO）
5. IS_PASS: YES → 生成代码摘要 → 交给QA → 测试通过 → 交付完成

**默认技术栈**：Vite + React + MUI + Tailwind CSS

## 4) 🔧 BugFix快捷路径

```
用户Bug报告 → TeamCreate → 工程师(定位+修复) → QA工程师(回归测试)
```

1. 创建团队（`software-bugfix-<问题简称>`）
2. 分派工程师：Bug描述 + 重现步骤 + 期望行为
3. 工程师定位问题文件并修复
4. QA仅运行回归测试确认修复

## 5) 🏗️ 标准SOP工作流（中大型需求）

```
用户需求 → 产品经理(PRD) → 架构师(系统设计+任务分解) → 工程师(代码实现) → QA工程师(测试验证)
```

### 逐步流程

1. **接收用户需求**：分析范围，确定工作流类型
2. **分派产品经理（许清楚）**：
   - 简单PRD（默认）：产品目标 + 用户故事 + 需求池（P0/P1/P2）+ UI设计稿 + 待确认问题
   - 完整PRD（用户明确要求时）：增加竞品分析 + Mermaid象限图 + 市场定位
3. **分派架构师（高见远）**：PRD完成后一次性输出：
   - 实现方案 + 框架选型
   - 文件列表及相对路径
   - 数据结构和接口（类图）
   - 程序调用流程（时序图）
   - **任务列表**（有序、含依赖、按实现顺序）
   - 依赖包列表
   - 共享知识（跨文件约定）
   - 待明确事项
4. **分派工程师（寇豆码）**：按任务列表批量编写代码：
   - 同一模块相关文件一起写
   - 全部完成后执行**全局一致性审查**（IS_PASS: YES/NO）
   - IS_PASS: NO → 修复（最多2轮）
   - IS_PASS: YES → 生成代码摘要 → 交给QA
5. **分派QA工程师（严过关）**：
   - 为核心模块编写测试用例
   - 运行测试并做**智能路由判定**：
     - 源码有Bug → 反馈工程师修复
     - 测试代码有Bug → QA自行修复
     - 全部通过 → 报告成功
   - 最多2轮测试

## 6) 协作铁律（严禁行为）

- ❌ 禁止跳过"建立团队"正式流程，直接模拟成员发言
- ❌ 禁止自己代写任何团队成员的专业产出（PRD/架构/代码/测试）
- ❌ 禁止跳过前序阶段直接进入后续阶段（快速模式/BugFix除外）
- ❌ 禁止让成员互相直连通信，所有跨成员信息流必须经主理人中转
- ❌ 禁止成员产出不经对应成员输出就直接采信

## 7) 质量关卡（CRITICAL）

| 关卡 | 负责人 | 判定标准 |
|------|--------|---------|
| 全局一致性审查 | 工程师 | IS_PASS: YES/NO |
| 智能路由判定 | QA工程师 | Engineer/QA/NoOne |
| 计划审批 | 主理人（用户）| approve/reject |

## 8) 双MCP组网方案（龙虾架构专用）

### 8.1 当前架构状态

| 容器 | 状态 | 端口 | lobster-network IP |
|------|------|------|-------------------|
| ai-doubao2-1 | ✅ 运行 | 18000→8000 | 172.19.0.4 |
| ai-bridge-1 | ✅ 运行 | 18091→8091 | 172.19.0.2 |
| hermes-agent | ✅ 运行 | 8642→8642 | 172.19.0.5 |
| hermes-webui | ✅ 运行 | 6060→6060 | 172.19.0.6 |
| ollama | ✅ 运行 | 11435→11434 | 172.19.0.3 |
| ai-openclaw2-1 | ✅ 运行 | 28789→18789 | 172.19.0.7 |

### 8.2 MCP客户端配置（mcp.json）

路径：`C:\Users\Administrator\.workbuddy\mcp.json`

```json
{
  "mcpServers": {
    "doubao-api": {
      "url": "http://127.0.0.1:18000/v1",
      "description": "豆包免费API代理 (OpenAI兼容)",
      "transport": "streamable-http"
    },
    "hermes-gateway": {
      "url": "http://127.0.0.1:18091",
      "description": "Hermes MCP桥接服务",
      "transport": "sse"
    },
    "ollama-local": {
      "url": "http://127.0.0.1:11435",
      "description": "Ollama本地模型服务",
      "transport": "streamable-http"
    },
    "hermes-agent": {
      "url": "http://127.0.0.1:8642",
      "description": "Hermes Agent服务",
      "transport": "sse"
    },
    "openclaw": {
      "url": "http://127.0.0.1:28789",
      "description": "OpenClaw服务",
      "transport": "sse"
    }
  }
}
```

### 8.3 端口规范

- **18000**：豆包API（唯一公网网关入口，Cloudflare Tunnel: doubao.tjf19770107.cn）
- **8642**：Hermes Agent独立服务
- **禁用**：8095、8096（无用冗余端口）

### 8.4 容器互通验证命令

```bash
# 内网互通验证（从容器内）
docker exec ai-doubao2-1 python3 -c "import urllib.request; r=urllib.request.urlopen('http://172.19.0.2:8091/',timeout=5); print(r.status)"
docker exec ai-bridge-1 python3 -c "import urllib.request; r=urllib.request.urlopen('http://172.19.0.3:11434/api/tags',timeout=5); print(r.status)"

# 宿主机端口可达验证
curl -s http://127.0.0.1:18000/v1/models | head -5
curl -s http://127.0.0.1:18091/ | head -5
curl -s http://127.0.0.1:11435/api/tags | head -5
```

## 8) Cloudflare Tunnel配置信息

### 8.1 Cloudflare官方资源

| 资源 | 地址 |
|------|------|
| Cloudflare Zero One Console | https://one.dash.cloudflare.com/ |
| Cloudflare Tunnel下载 | https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/ |
| Tunnel管理面板 | https://one.dash.cloudflare.com/_/tunnels |
| 官方文档 | https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/ |

### 8.2 当前隧道配置

```yaml
# 隧道ID: ff624654-b1af-431d-8c3a-f645b0b1e21b
# 配置文件: C:\Users\Administrator\.cloudflared\config.yml

tunnel: ff624654-b1af-431d-8c3a-f645b0b1e21b
credentials-file: C:\Users\Administrator\.cloudflared\ff624654-b1af-431d-8c3a-f645b0b1e21b.json

ingress:
  - hostname: doubao.tjf19770107.cn
    path: /qrcode
    service: http://localhost:18091
  - hostname: doubao.tjf19770107.cn
    service: http://localhost:18000
  - service: http_status:404
```

### 8.3 隧道令牌

```
eyObRkt2Mjc0LTg4MTMtNDhjYS05NzI2LTk0Mjg2YTJkOGFhNCJ9
```

### 8.4 端口转发规则

| 公网域名 | 路径 | 内网目标 |
|----------|------|----------|
| doubao.tjf19770107.cn | /qrcode | localhost:18091 |
| doubao.tjf19770107.cn | / | localhost:18000 |

## 9) 端口规范（强制执行）

### 9.1 端口分配表

| 端口 | 服务 | 说明 | 可见性 |
|------|------|------|--------|
| 18000 | 豆包API | **唯一公网网关** | 公网+内网 |
| 18091 | ai-bridge | Bridge桥接服务 | 内网 |
| 8642 | hermes-agent | Hermes独立服务 | 内网 |
| 6060 | hermes-webui | WebUI管理面板 | 内网 |
| 28789 | ai-openclaw2-1 | OpenClaw服务 | 内网 |
| 17000 | frps | FRP控制面板 | 内网 |
| 19100 | frpc | FRP数据面 | 内网 |
| 11435 | ollama | 本地模型 | 内网 |

### 9.2 禁用端口

- **8095**：已废弃，禁用
- **8096**：已废弃，禁用
- **8081**：BrowserBase MCP（技能包模式，无需本地SSE）

### 9.3 验证命令

```bash
# 端口占用检测
netstat -ano | findstr "18000 18091 8642 6060 28789"

# 服务健康检测
curl -s http://localhost:18000/v1/models | head -3
curl -s http://localhost:28789/health
curl -s http://localhost:18091/ | head -3
```

## 10) 一键启动脚本

| 脚本 | 路径 | 功能 |
|------|------|------|
| 一键启动双MCP集群 | `lobster_software_dev_team_v2.0/一键启动双MCP集群.bat` | 双MCP集群+Cloudflare隧道同步启动 |
| 全容器自检 | `lobster_software_dev_team_v2.0/全容器自检.bat` | 链路验证+二维码生成 |

## 11) 交付总结规范

工作流完成后汇报：
- **TL;DR**：一句话说明交付了什么
- **交付概览**：交付状态、测试通过率、已知问题数
- **文件清单**：所有创建/修改的文件路径
- **用户下一步建议**：3-5条（启动命令、部署建议等）

## 12) 关联技能（可组合调用）

- lobster_task_standard_workflow_full_v2.0（五步法完整版·全域默认）
- gstack_standard_workflow_template_v1.1（GStack标准工作流模板）
- lobster_tripartite_handshake_v1.0（三方握手）
- lobster_codex_benchmark_v1.0（Codex能力对标）
- lobster_claude_mem_gstack_bridge_v1.0（Claude MEM接入）

## 13) 变更记录

- v1.0 (2026-05-19)：初始版本，三路由+四角色+协作铁律+质量关卡
- v2.0 (2026-05-19)：升级为本地独立版，增加双MCP组网方案、本地独立声明、计费声明、容器互通验证、端口规范、openclaw2-1纳入统一网络、Cloudflare Tunnel配置信息、一键启动脚本
