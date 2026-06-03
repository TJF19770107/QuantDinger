---
name: "gstack_standard_workflow_template_v1.1"
description: "Gstack 标准工作流闭环模板（v1.1）：增加“龙虾标准五步法（完整版 v2.0）”强制校验映射与成本/性价比验收；仅合并叠加，不覆盖旧技能。"
---

# Gstack 标准工作流闭环模板（v1.1）

【适用范围】
- 本模板用于固化“Hermes↔Trae↔豆包（含 Bridge/Wechat Gateway）”在本地 Docker 环境中的标准联调/验收/复盘闭环。
- 输出口径：只记录可验证事实与变量名，不写任何密钥/口令/Cookie/密码明文。

## 0) 关键约束（硬口径）

- 成功判定只看真实链路 2xx/可用响应与终态事件，不以“容器 Up”代替验收。
- 密钥只允许“是否已设置/是否生效”检查，不允许在终端输出明文值。
- 合并更新：只新增版本化文件与索引项，不覆盖旧技能文件。
- 免费与性价比：优先本地免费资源；任何新增依赖必须给出成本核算与免费替代方案。

## 1) 五步法强制校验（与全域默认工作流对齐）

本模板执行时，必须同步满足 [TRAE_20260429_lobster_task_standard_workflow_full_v2.0.md](file:///E:/%E9%BE%99%E8%99%BEAI%E4%B8%BB%E6%8E%A7%E4%B8%AD%E5%BF%83/%E5%85%B1%E4%BA%AB%E6%8A%80%E8%83%BD%E5%BA%93/%E5%85%A8%E5%B1%80%E6%8A%80%E8%83%BD%E5%BA%93/TRAE_20260429_lobster_task_standard_workflow_full_v2.0.md) 的五步顺序：

- 第一步对标学习：明确同类拓扑与验收口径对标项（端口/健康检查/触发路径/SSE 终态）。
- 第二步全面诊断：先给出当前拓扑、端口、挂载、变量名、版本与连通性证据。
- 第三步落地执行：仅做增量改动（新增版本文件/新增配置块/新增索引项），禁止覆盖旧文件。
- 第四步全链路验收：按本模板 3)~6) 的真实链路验收口径逐项过关。
- 第五步复盘固化：输出验收报告与最小回滚路径，并把新增模板/技能登记进 INDEX.jsonl。

## 2) 三方握手（必做）

1. Hermes 健康检查（示例）：
   - `http://127.0.0.1:8642/health` 返回 200 且为 JSON
2. Bridge 健康检查（示例）：
   - `http://127.0.0.1:18091/bridge/health` 返回 200
3. WebUI 可达（示例）：
   - `http://127.0.0.1:6060/` 返回 200

握手输出物：
- `tripartite_handshake_link.json`（仅记录节点/端口/版本，不含任何密钥值）

## 3) 标准拓扑（参考实现）

### 3.1 Hermes Official（当前生产口径）

- 容器：`hermes-agent`（API/Gateway）
  - 端口：宿主 `127.0.0.1:8642-8670` → 容器 `8642-8670/tcp`
- 容器：`hermes-webui`（WebUI+BFF 反代）
  - 端口：宿主 `127.0.0.1:6060` → 容器 `6060/tcp`

### 3.2 Doubao Bridge（webhook→Hermes /v1/runs）

- 容器：`ai-bridge-1`
  - 端口：宿主 `127.0.0.1:18091` → 容器 `8091/tcp`
  - 关键挂载：
    - `E:\Hermes_Return` → `/host/Desktop/Hermes_Return`（RW，用于落盘回流）
    - `...\docker\doubao_bridge\bridge_service.py` → `/app/bridge_service.py`（RO，避免容器内漂移）

### 3.3 可选：Wechat Gateway（个人微信 webhook→Hermes）

- 容器：`ai-wechat-1`
  - 端口：宿主 `127.0.0.1:8092` → 容器 `8092/tcp`
  - 入站路径：`/wechat/receive`

## 4) 环境变量口径（只列变量名）

### 4.1 Hermes（调用方需要）

- `HERMES_BASE_URL`（示例：`http://host.docker.internal:8642`）
- `HERMES_API_TOKEN`（Bearer，必配；仅检查是否 SET）
- `HERMES_LOCAL_KEY`（可选；仅检查是否 SET）
- `HERMES_API_TOKEN_HEADER` / `HERMES_LOCAL_KEY_HEADER`（仅当你自定义 header 名时使用）

### 4.2 Bridge（触发与回推）

- `DOUBAO_WEBHOOK_SECRET`（入站鉴权，可选但建议启用）
- `DOUBAO_USER_TRIGGER_WORD`（触发词前缀）
- `DOUBAO_USER_TRIGGER_TOKEN`（口令门禁；必须通过环境变量设置）
- `DOUBAO_REPLY_API_URL`（可选：配置后可回推到豆包侧）
- `DOUBAO_REPLY_AUTH_HEADER` / `DOUBAO_REPLY_AUTH_TOKEN`（可选：回推鉴权）
- `HERMES_RUN_TIMEOUT_S`（Hermes 运行总超时上限）

### 4.3 安全风险门禁（建议）

- 禁止把任何敏感值写进仓库 `.env` 文件；推荐用系统环境变量注入。
- 若历史已存在明文 `.env`，应迁移后立即轮换旧值。

## 5) 标准工作流（闭环）

### 5.1 启动

1. 启动 Docker 组件（compose/up 或一键启动脚本）。
2. 等待 Hermes 2xx 健康检查通过。
3. 确认 Hermes Gateway 运行（用于扫码直连通道）：
   - `docker exec hermes-agent sh -lc "/opt/hermes/.venv/bin/hermes gateway status"`

### 5.2 触发（webhook→Hermes）

1. Doubao/Wechat 入站 webhook 到 Bridge/Gateway。
2. Bridge 解析消息文本，必须满足：
   - 以 `DOUBAO_USER_TRIGGER_WORD` 开头
   - 携带正确口令（来自 `DOUBAO_USER_TRIGGER_TOKEN`；不允许在日志中回显）
3. Bridge 调用 Hermes：
   - `POST /v1/runs`（通常返回 202 started）
   - 监听 `GET /v1/runs/{run_id}/events`（SSE）直到 `run.completed`

### 5.3 验收（必须全部通过才算“跑通”）

- Bridge /bridge/health 200（且 stats/errors 不持续增长）
- Hermes /health 200 + /v1/health 200
- 至少一次 `POST /v1/runs` 成功返回 2xx（202/200 均可），并在合理超时内得到 completed/failed 终态事件

### 5.4 成本与性价比验收（必须给结论）

- 资源占用：对比改动前后磁盘/日志/镜像体积，确认没有引入无意义膨胀。
- 复杂度：链路节点与端口数量不增加或有明确收益理由；避免重复代理/重复转发。
- 稳定性：新增组件必须有健康检查与最小回滚路径。

### 5.5 回滚（最小破坏）

- 只回滚“本次新增/变更的单一环节”，避免全链路重建：
  - 先停 Bridge / Gateway，再停 WebUI，最后才考虑 Hermes
- 配置回滚优先级：
  1) 恢复上一次可用的 docker-compose 与 env 变量名集合
  2) 恢复 Bridge 代码到只读挂载的上一个版本文件
  3) 仍不稳定才执行容器升级回滚流程（按 ops_docker_auto_upgrade 口径）

## 6) 常见踩坑与对策（速查）

- 大量 404：优先检查 Hermes Base URL 是否指向真实 API 端口；其次检查是否误用 outbox 轮询路径。
- 401 invalid_api_key：Hermes Key 缺失/失效；只做“是否 SET”检查，按密钥生命周期流程轮换。
- 202 被误判失败：下游以 2xx 判成功，或桥接层统一 202→200。
- SSE ReadTimeout：拉长读超时，或在 Bridge 内部把 run_timeout_s 作为总上限并做断线重连策略。

## 7) 关联技能（可组合调用）

- lobster_tripartite_handshake_v1.0（三方握手）
- lobster_task_standard_workflow_full_v2.0（五步法完整版·全域默认）
