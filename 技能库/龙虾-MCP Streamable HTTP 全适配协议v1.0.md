# 龙虾-MCP Streamable HTTP 全适配协议 v1.0

> **协议编号**：#160
> **版本**：v1.0
> **对标来源**：Gemini 2.5 Pro MCP + Codex MCP stdio/HTTP + MCP OAuth 2.1
> **生效范围**：豆包Agent · MCP集成层
> **创建轮次**：R44

---

## 一、设计目标

全面适配MCP 2026年核心升级——Streamable HTTP传输、Elicitation、Sampling、Task等新特性，对标Gemini 2.5 Pro原生MCP支持和Codex的双模式MCP集成，将豆包Agent的MCP适配从传统SSE模式升级到完整的Streamable HTTP + 新原语支持。

## 二、MCP 2026 协议栈全景

```
MCP Client (豆包Agent)
  │
  ├─ Transport: Streamable HTTP (替代 SSE-only)
  │   · 更好的可扩展性
  │   · 支持双向流
  │   · 长连接复用
  │
  ├─ Primitives:
  │   ├─ Tools: 工具暴露（TypeScript/Python/C#/Java SDK）
  │   ├─ Resources: 资源存取（结构化数据）
  │   ├─ Prompts: 指令模板
  │   ├─ Elicitation (NEW): 服务端请求用户输入
  │   ├─ Sampling (NEW): 服务端请求LLM完成
  │   └─ Task (实验性 NEW): 耐久请求追踪
  │
  └─ Security:
      ├─ OAuth 2.1 集成
      └─ 细粒度 Scope 权限
```

## 三、Streamable HTTP 传输适配

### 3.1 对比 SSE-only 模式

| 维度 | SSE-only（旧） | Streamable HTTP（新） |
|------|---------------|---------------------|
| 连接管理 | 单向长连接 | 双向流 |
| 扩展性 | 受限于SSE | HTTP/2多路复用 |
| 断线重连 | 手动重连 | 自动恢复 |
| 防火墙穿透 | 需要WebSocket | 标准HTTP端口 |
| 负载均衡 | 复杂 | 原生支持 |

### 3.2 豆包Agent实现方案

```yaml
mcp_transport:
  default: "streamable-http"
  fallback: "stdio"  # 本地MCP Server降级方案
  
  streamable_http:
    endpoint: "https://mcp-gateway.local/v1"
    headers:
      Authorization: "Bearer ${MCP_TOKEN}"
    timeout: 30s
    retry:
      max_attempts: 3
      backoff: "exponential"
  
  stdio:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-*"]
    env:
      NODE_ENV: "production"
```

## 四、新原语适配

### 4.1 Elicitation（用户输入请求）

**对标**：Gemini 2.5 Pro MCP Elicitation

```python
# MCP Server 请求用户输入
@server.tool("confirm_deployment")
async def confirm_deployment(env: str) -> dict:
    result = await server.elicit(
        prompt=f"确认部署到 {env} 环境？",
        input_type="confirmation",  # confirmation / text / file / select
        options=["确认", "取消", "查看详情"]
    )
    return {"status": "confirmed" if result == "确认" else "cancelled"}
```

**豆包Agent处理流程**：
```
MCP Server 发送 elicit 请求
  → 豆包Agent接收 → 转换为ask_user表单
    → 用户交互 → 结果回传MCP Server
```

### 4.2 Sampling（LLM完成请求）

**对标**：Gemini 2.5 Pro MCP Sampling

```python
# MCP Server 请求LLM完成
@server.tool("summarize_logs")
async def summarize_logs(log_source: str) -> dict:
    logs = await fetch_logs(log_source)
    summary = await server.sample(
        messages=[{"role": "user", "content": f"总结以下日志：{logs[:5000]}"}],
        max_tokens=500,
        temperature=0.3
    )
    return {"summary": summary.content}
```

**豆包Agent处理流程**：
```
MCP Server 发送 sample 请求
  → 豆包Agent接收 → 调用模型推理
    → 结果返回MCP Server
```

### 4.3 Task（耐久请求追踪 - 实验性）

**对标**：Gemini 2.5 Pro MCP Task (Experimental)

```python
# 长时间运行的任务
@server.task("process_large_file")
async def process_large_file(file_path: str) -> TaskResult:
    task = TaskTracker.create(
        task_id=uuid4(),
        status="running",
        progress=0,
        started_at=datetime.now()
    )
    
    try:
        for chunk in read_file_async(file_path, chunk_size="100MB"):
            task.progress += chunk.size / total_size
            await process_chunk(chunk)
        
        task.status = "completed"
        return TaskResult(success=True)
    except Exception as e:
        task.status = "failed"
        return TaskResult(success=False, error=str(e))
```

**豆包Agent支持**：
- 轮询Task进度（HTTP 202 Accepted + Retry-After）
- Task超时自动取消
- 延迟结果获取

## 五、MCP Server 标准化接入

### 5.1 一键注册命令

```bash
# 注册一个MCP Server到豆包Agent
doubao mcp register \
  --name="github" \
  --command="npx" \
  --args="-y @modelcontextprotocol/server-github" \
  --env GITHUB_TOKEN=$GITHUB_TOKEN \
  --transport streamable-http
```

### 5.2 MCP Server 清单

| 分类 | Server | 用途 | 状态 |
|------|--------|------|:---:|
| 文件系统 | @modelcontextprotocol/server-filesystem | 安全文件操作 | ✅ |
| 版本控制 | @modelcontextprotocol/server-github | GitHub操作 | ✅ |
| 数据库 | @modelcontextprotocol/server-postgres | PostgreSQL查询 | ✅ |
| 知识库 | @modelcontextprotocol/server-rag | RAG检索 | ✅ |
| 浏览器 | @anthropic/mcp-server-puppeteer | 网页自动化 | 🔄 |
| 代码分析 | @modelcontextprotocol/server-code-analysis | 静态分析 | 🔄 |

### 5.3 OAuth 2.1 安全集成

**对标**：MCP March 2026 OAuth 2.1 集成

```yaml
mcp_security:
  auth: "oauth2.1"
  token_endpoint: "https://auth.mcp-gateway.local/oauth/token"
  scopes:
    - "mcp:tools:read"
    - "mcp:tools:execute"
    - "mcp:resources:read"
    - "mcp:sampling:invoke"
  token_rotation:
    enabled: true
    interval: "1h"
```

## 六、与已有协议的协同

| 已有协议 | 协同方式 |
|---------|---------|
| #121 A2A+MCP三层协议栈 v1.1 | MCP升级到Streamable HTTP后，A2A Agent Card通过MCP Tool暴露 |
| #17 MCP桥接集成协议 v1.0 | 升级传输层：stdio → Streamable HTTP |
| #66 MCP安全纵深防御协议 v1.0 | 增加OAuth 2.1认证 + Scope权限 |
| #103 多后端沙箱弹性部署协议 v2.0 | MCP Server在沙箱内运行，Token限制继承 |

## 七、性能指标

| 指标 | 目标 | 对标 |
|------|:---:|------|
| MCP Server 发现延迟 | <500ms | Gemini |
| 工具调用延迟增加 | <50ms | Codex |
| Streamable HTTP 重连 | <1s | — |
| 并发MCP连接 | 10+ | Codex |

---

> **协议版本**：v1.0
> **创建轮次**：R44（2026-06-02）
> **下一次评审**：R45（计划MCP适配97→98，Task原语脱离实验性后升级）
