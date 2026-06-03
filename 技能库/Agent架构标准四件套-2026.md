# 技能：2026 Agent架构标准四件套
> 提取自：第1轮豆包Agent迭代 | 来源：Claude Code / Codex CLI / Gemini CLI / OpenCode 趋同分析
> 版本：v1.0 | 日期：2026-05-31

## 触发条件
当Agent需要执行自主任务（编码、文件操作、系统管理、多步推理）时自动加载。

## 核心架构

### 1. ReAct Loop
```
while (task_not_complete && turns < max_turns):
    think()      # LLM推理下一步
    act()        # 调用工具
    observe()    # 收集工具返回
    if emergency: break
```

### 2. Tool System
- MCP原生客户端（stdio + Streamable HTTP）
- Dispatch Map路由（工具→优先级→回退）
- 工具Schema标准化（JSON Schema）

### 3. Context Manager
- 工作记忆：当前会话状态（JSON，< 2K tokens）
- 情景记忆：项目级轨迹（FTS5全文索引）
- 技能记忆：可复用SOP（Markdown变量模板）

### 4. Permission Layer
- 只读操作：自动放行
- 文件写入：路径白名单
- 系统变更：用户确认 + 沙箱

## 来源
- [夜雨聆风 - Claude Code源码泄露分析](https://www.yeyulingfeng.com/486509.html)
- [王骏 - 四大CLI趋同分析](https://www.wangjun.dev/2026/05/claude-code-vs-codex-vs-gemini-vs-opencode/)
