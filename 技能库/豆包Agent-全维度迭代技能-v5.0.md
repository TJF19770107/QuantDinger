# 豆包Agent技能库同步 · 全维度迭代 v5.0
## 同步时间: 2026-05-31 04:40

---

## 一、核心架构升级（v4.0 → v5.0）

### 1.1 执行引擎升级：while-loop 状态机（对标 Claude Code 50万行源码）
```python
async def agent_loop(messages):
    while True:
        response = await call_model(messages)
        if not response.tool_calls:
            return response.text
        tool_results = await execute_tools(response.tool_calls)
        messages = [...messages, response, ...tool_results]
```
护城河：七级权限 + 五层上下文压缩 + Hooks引擎 + Git Worktree隔离 + MCP协议

### 1.2 自进化闭环增强：Hermes Skill Pipeline 对标
```
复杂任务 → 自动检测（≥5步） → Skill沉淀 → 成功率跟踪 → 自动优化
长期不用 → Prune淘汰 → archive → 重叠Skill → Consolidate整合
```

### 1.3 双层推理架构：Soul-Worker（对标 Eve V2U）
- Soul 层（本地GPU）：Qwen2.5:7B Q4_K_M 量化，权重 baked 人格，低延迟
- Worker 层（云端API）：Doubao-Seed-2.0-Pro/Code，40轮工具调用循环，131K上下文

### 1.4 Dreaming 自主思考（对标 Claude Managed Agents）
AutoWake 触发 → 回顾历史 → 整理记忆 → 提取规律 → 更新知识图谱

---

## 二、豆包 AI IDE 蓝图

### 2.1 三面架构（对标 Google Antigravity）
- Editor Surface：多文件编辑 + Diff预览 + 代码分析
- Terminal Surface：Shell执行 + Build工具 + Git操作
- Browser Surface：集成浏览器 + localhost视觉验证 + 截图审查

### 2.2 Mission Control（对标 Antigravity Agent Manager）
- 并行 Agent 调度（上限5）
- 状态仪表盘（Running/Pending/Done/Failed）
- 异步执行非阻塞

### 2.3 模型路由
简单任务 → Qwen2.5:7B（本地6GB显卡，免费）
编码任务 → Doubao-Seed-2.0-Code（云端强编码）
架构决策 → Gemini 3 Deep Think / Claude Sonnet
多模态 → Doubao Vision

---

## 三、15技能完整清单

| 编号 | 技能 | 状态 | 对标 |
|------|------|------|------|
| S01 | AutoFileScanner | ✅ 已部署 | OpenClaw Workspace |
| S02 | SkillForge | ✅ 已部署 ⬆ 自动触发+进化 | Hermes Skill Pipeline |
| S03 | DesktopController | ✅ 已部署 | Claude Cowork |
| S04 | AutoWake | ✅ 已部署 ⬆ Dreaming三步 | Claude Managed Agents |
| S05 | MemoryOS | ✅ 已部署 ⬆ FTS5+5层压缩 | Hermes SQLite + Claude Context |
| S06 | SafeGuard | ✅ 已部署 ⬆ 七级权限 | Claude Code Permission |
| S07 | CodeAgent | 🆕 已设计 | Claude Code while-loop |
| S08 | MissionControl | 🆕 已设计 | Antigravity Agent Manager |
| S09 | ModelRouter | 🆕 已设计 | 智能路由分发 |
| S10 | BrowserSurface | 🆕 已设计 | Antigravity Browser |
| S11 | SoulWorker | 🆕 已设计 | Eve V2U 双层架构 |
| S12 | SteerInjector | 🆕 已设计 | Eve V2U STEER |
| S13 | SkillPruner | 📋 计划中 | Hermes Curator v0.12.0 |
| S14 | GitWorktree | 📋 计划中 | Claude Code Worktree |
| S15 | HookEngine | 📋 计划中 | Claude Code Hooks |

---

## 四、四级记忆系统 v5.0

```
L1: 即时上下文 → 当前推理窗口
L2: 短期工作记忆 → 会话内摘要，5层压缩管线
L3: 长期结构化记忆 → SQLite + FTS5 全文检索 + 知识图谱
L4: 经验技能库 → Skill 沉淀 + 成功率跟踪 + 自动进化
```

---

## 五、MCP标准工具总线 v5.0

新增 MCP Server 规划：
- 豆包文件系统 MCP Server
- 豆包 Shell 执行 MCP Server
- 豆包浏览器 MCP Server（Browser Surface）
- 豆包 Git Worktree MCP Server
- 豆包 数据库查询 MCP Server

---

*同步至: E:\龙虾AI主控中心\我的AI分身\技能库\*
*主方案: 2026-05-31_R05_全维度迭代升级报告_v5.0.md*
*能力状态: capabilities.json v5.0 (15技能, 7系统对标, 11 GAP追踪)*