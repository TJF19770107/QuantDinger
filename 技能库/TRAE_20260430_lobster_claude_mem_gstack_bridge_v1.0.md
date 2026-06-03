# Claude MEM × GStack 接入（合规版 v1.0）

技能名称：Claude MEM × GStack 接入（合规版）  
技能标识：lobster_claude_mem_gstack_bridge_v1.0  
版本号：v1.0  
更新时间：2026-04-30  
目标：为 Claude Code 的 claude-mem 持久记忆做本地化安装/验收/回滚，并对齐 gstack/Hermes skills 注入链路；全程遵守“密钥不落盘、不写日志、仅环境变量注入”的门禁。  

## 关键结论

- `mehmetcanfarsak/claude-mem` 可能出现 404，不作为可用安装源
- 可用替代源：`thedotmack/claude-mem`；推荐 `npx -y claude-mem install`（非 `npm -g`）
- 默认 Web Viewer 端口：37777（仅作为验收观测入口）

## 门禁（强制）

- 联网安装门禁：仅当用户显式允许并设置 `LOBSTER_ALLOW_NET_INSTALL=1` 才可联网下载与安装
- 不泄密门禁：任何文档/日志/输出禁止出现 Token/Key/Cookie/密码明文，只允许写变量名与 SET/EMPTY

## 最小流程（install → verify → rollback）

### 1) 预检

- Node 与 npm 可用（建议 Node LTS）
- gstack skills 注入链路存在（以宿主 `C:\Users\Administrator\.claude\skills` 为单一入口，容器侧通过挂载读取）

### 2) 安装（受门禁控制）

- 未开门禁时：只输出缺口清单，不执行安装
- 已开门禁时：执行 `npx -y claude-mem install`

### 3) 验收

- Viewer 可访问（HTTP 200/可加载页面）：`http://127.0.0.1:37777`
- 新会话可读取到历史摘要（以“是否注入摘要/是否能检索到关键规则”为准，不强制暴露明文内容）

### 4) 回滚

- 优先使用 claude-mem 官方卸载/关闭方式
- 若无法确认卸载命令：采用“最小破坏回滚”——停止 worker/移除插件注册项/验收 37777 不再监听

## 与 gstack/Hermes 的分工

- claude-mem：跨会话记忆压缩/检索（Claude Code 内）
- gstack：工作流方法论（investigate→plan→review→qa→ship）与可审计的 context-save/restore
- Hermes：宿主 skills 注入到容器侧，只读挂载，不改 Docker/WSL 结构

