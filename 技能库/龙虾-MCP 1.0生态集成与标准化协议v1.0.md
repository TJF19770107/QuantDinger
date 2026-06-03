# 龙虾-MCP 1.0生态集成与标准化协议 v1.0

> **协议编号**：#56
> **版本**：v1.0（R13迭代 · 2026-06-01）
> **对标来源**：MCP 1.0正式版 + Linux Foundation托管 + Windows 11原生集成
> **核心价值**：MCP Server统一注册/会话恢复/安全权限粒化/跨模型互操作
> **激活条件**：涉及MCP协议集成、跨Agent工具调用、标准化生态对接时激活

---

## 一、协议概述

本协议基于MCP 1.0正式版（2026年4月，Linux Foundation托管）制定，为龙虾AI主控中心提供完整的MCP生态集成能力，实现与外部MCP Server的标准化对接、会话恢复、权限管理及跨模型互操作。

## 二、MCP Server注册与发现

### 2.1 统一注册表接入

```
注册表地址: mcp:registry/<server-name>
认证方式: OAuth 2.1 + PKCE
版本管理: Semantic Versioning
依赖解析: 自动安装依赖链
```

### 2.2 本地Server清单

| Server名称 | 用途 | 传输方式 | 状态 |
|-----------|------|---------|------|
| file-system | 文件操作 | stdio | ACTIVE |
| shell-executor | 命令执行 | stdio | ACTIVE |
| knowledge-base | 知识检索 | streamable-http | ACTIVE |

### 2.3 远程动态加载

```
配置格式: mcp:registry/marvis-file-manager@1.0.0
优先级: 远程 > 本地（版本更新时自动切换）
```

## 三、会话恢复机制

### 3.1 会话状态保存

| 保存内容 | 频率 | 存储位置 |
|---------|------|---------|
| 上下文窗口 | 每轮对话 | 记忆库 |
| 工具调用链 | 每次工具调用 | 子Agent日志 |
| 任务进度 | 每步骤完成 | 工作流库 |
| 跨天任务 | 每会话结束 | 变量库 |

### 3.2 恢复流程

1. 检测是否有待恢复会话（session_id存在且未过期）
2. 加载上下文窗口快照
3. 重新建立MCP连接
4. 恢复工具调用链状态
5. 从中断点继续执行

### 3.3 安全增强提案（SEPs）

| 权限类型 | 细粒度控制 |
|---------|-----------|
| 文件访问 | 按文件夹授权，而非全局 |
| API调用 | 按endpoint授权白名单 |
| 数据范围 | 读写分离，部分数据只读 |
| 用户确认 | 敏感操作二次确认弹窗 |

## 四、跨模型互操作

### 4.1 模型无关调用

MCP工具调用与底层模型解耦，支持：
- Claude系列
- GPT系列
- Gemini系列
- Llama系列
- 国产模型（DeepSeek/Qwen/GLM）

### 4.2 模型路由表

| 操作类型 | 推荐模型 | 备选模型 |
|---------|---------|---------|
| 复杂推理 | Claude Opus | GPT-4o |
| 快速响应 | Claude Sonnet | Gemini Flash |
| 代码生成 | Claude Code | Codex CLI |
| 中文优化 | Qwen-Max | DeepSeek-V3 |

## 五、执行流程

```
Step 1: 检测MCP依赖 → 扫描任务所需的MCP工具
Step 2: 注册表查询 → 搜索可用MCP Server
Step 3: 会话建立 → OAuth认证 + 权限申请
Step 4: 工具调用 → MCP原语（tools/call, resources/read, prompts/get）
Step 5: 会话保存 → 状态快照 + 权限审计日志
```

---

> 协议版本：v1.0
> 创建时间：2026-06-01 R13迭代
> 下次审查：R14迭代