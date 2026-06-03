# 双平台Agent部署协议 v1.0

> **协议编号**：83
> **对标来源**：OpenCode v1.3 GitLab Agent Platform
> **创建日期**：2026-06-01
> **状态**：Active
> **适用场景**：需要在GitHub和GitLab双平台部署AI Agent的企业级场景

---

## 一、协议概述

双平台Agent部署协议借鉴了OpenCode v1.3的GitLab Agent Platform设计，实现在GitHub和GitLab双平台的统一Agent部署、管理和运维，支持企业级多步认证、权限管理和WebSocket本地工具集成。

## 二、核心设计原则

1. **平台无关性**：核心Agent逻辑与平台解耦
2. **统一管理**：通过统一控制台管理双平台Agent
3. **安全优先**：支持企业级认证和权限控制
4. **本地集成**：通过WebSocket实现本地工具无缝集成

## 三、架构设计

### 3.1 整体架构

```
┌─────────────────┐    ┌─────────────────┐
│   GitHub平台    │    │   GitLab平台    │
│  (github.com)   │    │  (gitlab.com)   │
└────────┬────────┘    └────────┬────────┘
         │                       │
         └──────────┬────────────┘
                    │
         ┌──────────▼──────────┐
         │  统一Agent网关      │
         │  (Unified Gateway)  │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │  Agent核心服务      │
         │  (Core Service)     │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │  本地工具集成层     │
         │  (Local Tools)      │
         └─────────────────────┘
```

### 3.2 组件说明

| 组件 | 功能 | 技术实现 |
|------|------|----------|
| **统一Agent网关** | 平台协议转换、请求路由、认证代理 | Node.js + Express |
| **平台适配器** | GitHub API适配器、GitLab API适配器 | 平台SDK封装 |
| **Agent核心服务** | 任务调度、记忆管理、技能执行 | Python + FastAPI |
| **本地工具集成层** | WebSocket连接、本地工具调用、结果返回 | WebSocket Server |
| **配置管理中心** | 双平台配置、权限管理、密钥管理 | Redis + PostgreSQL |

## 四、平台特性对比与统一

### 4.1 GitHub vs GitLab Agent特性

| 特性 | GitHub | GitLab | 统一方案 |
|------|--------|--------|----------|
| **认证方式** | OAuth App / Personal Token | OAuth / Personal Token / SAML | 统一OAuth 2.1 + 多步认证 |
| **Webhook** | 支持 | 支持 | 统一Webhook处理器 |
| **API速率** | 5000请求/小时 | 无明确限制 | 智能路由+缓存 |
| **权限模型** | Repo/Org级别 | Project/Group级别 | 统一权限映射 |
| **部署方式** | GitHub Actions | GitLab CI/CD | 统一部署脚本 |
| **监控** | GitHub Insights | GitLab Metrics | 统一监控面板 |

### 4.2 统一接口设计

```typescript
// 统一平台接口
interface UnifiedPlatform {
  // 认证相关
  authenticate(config: AuthConfig): Promise<AuthResult>;
  refreshToken(refreshToken: string): Promise<AuthResult>;
  
  // 仓库操作
  getRepositories(options?: RepoOptions): Promise<Repository[]>;
  createRepository(repo: NewRepository): Promise<Repository>;
  getRepository(id: string): Promise<Repository>;
  
  // 代码操作
  getFileContent(repoId: string, path: string, ref?: string): Promise<FileContent>;
  createOrUpdateFile(repoId: string, path: string, content: FileUpdate): Promise<CommitResult>;
  
  // Webhook管理
  createWebhook(repoId: string, webhook: WebhookConfig): Promise<Webhook>;
  listWebhooks(repoId: string): Promise<Webhook[]>;
  
  // CI/CD
  triggerPipeline(repoId: string, branch: string, variables?: Record<string, string>): Promise<Pipeline>;
  getPipelineStatus(pipelineId: string): Promise<PipelineStatus>;
  
  // 权限检查
  checkPermission(repoId: string, permission: Permission): Promise<boolean>;
}

// 平台工厂
class PlatformFactory {
  static create(platform: 'github' | 'gitlab', config: PlatformConfig): UnifiedPlatform {
    switch (platform) {
      case 'github':
        return new GitHubAdapter(config);
      case 'gitlab':
        return new GitLabAdapter(config);
      default:
        throw new Error(`Unsupported platform: ${platform}`);
    }
  }
}
```

## 五、认证与安全

### 5.1 多步认证流程

```
用户访问 → 选择平台(GitHub/GitLab) → OAuth授权 → 获取Access Token
    ↓
存储Token → 定期刷新 → 权限验证 → 访问控制
```

### 5.2 企业级认证支持

| 认证类型 | GitHub支持 | GitLab支持 | 实现方案 |
|----------|------------|------------|----------|
| **OAuth 2.0** | ✅ | ✅ | 标准实现 |
| **OAuth 2.1** | ✅ (2026) | ✅ (2026) | 优先支持 |
| **SAML 2.0** | ✅ (企业版) | ✅ | 企业版支持 |
| **LDAP** | ❌ | ✅ | GitLab专用 |
| **个人访问令牌** | ✅ | ✅ | 统一管理 |
| **设备流** | ✅ | ✅ | 无头设备支持 |

### 5.3 密钥管理

```yaml
# 密钥配置文件示例
secrets:
  github:
    client_id: ${GITHUB_CLIENT_ID}
    client_secret: ${GITHUB_CLIENT_SECRET}
    app_id: ${GITHUB_APP_ID}
    private_key: ${GITHUB_PRIVATE_KEY}
    
  gitlab:
    client_id: ${GITLAB_CLIENT_ID}
    client_secret: ${GITLAB_CLIENT_SECRET}
    instance_url: ${GITLAB_INSTANCE_URL}
    
  encryption:
    algorithm: aes-256-gcm
    key: ${ENCRYPTION_KEY}
    
  storage:
    type: vault # 或 aws_secrets_manager, azure_key_vault
    config: ${VAULT_CONFIG}
```

## 六、WebSocket本地工具集成

### 6.1 连接建立流程

```
本地Agent启动 → 连接WebSocket服务器 → 身份验证 → 注册可用工具
    ↓
等待远程调用 → 执行本地工具 → 返回结果 → 保持连接心跳
```

### 6.2 协议设计

```typescript
// WebSocket消息协议
interface WSMessage {
  id: string;           // 消息ID
  type: 'request' | 'response' | 'event' | 'error';
  action?: string;      // 操作类型: tool_call, tool_result, heartbeat, register
  payload?: any;        // 消息负载
  timestamp: number;    // 时间戳
}

// 工具调用请求
interface ToolCallRequest {
  tool_name: string;
  parameters: Record<string, any>;
  context?: AgentContext;
  timeout?: number;     // 超时时间(ms)
}

// 工具调用响应
interface ToolCallResponse {
  success: boolean;
  result?: any;
  error?: string;
  execution_time: number;
  metadata?: Record<string, any>;
}
```

### 6.3 本地工具注册

```python
# 本地工具注册示例
class LocalToolRegistry:
    def __init__(self, websocket_client):
        self.client = websocket_client
        self.tools = {}
    
    def register_tool(self, tool_name: str, tool_func: callable, metadata: dict = None):
        """注册本地工具"""
        self.tools[tool_name] = {
            'function': tool_func,
            'metadata': metadata or {},
            'registered_at': datetime.now()
        }
        
        # 向服务器发送注册消息
        self.client.send({
            'type': 'event',
            'action': 'register_tool',
            'payload': {
                'tool_name': tool_name,
                'metadata': metadata
            }
        })
    
    async def handle_tool_call(self, request: dict) -> dict:
        """处理工具调用请求"""
        tool_name = request['tool_name']
        
        if tool_name not in self.tools:
            return {
                'success': False,
                'error': f'Tool not found: {tool_name}',
                'execution_time': 0
            }
        
        tool = self.tools[tool_name]
        start_time = time.time()
        
        try:
            # 执行工具
            result = await tool['function'](**request['parameters'])
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'result': result,
                'execution_time': execution_time,
                'metadata': {
                    'tool_name': tool_name,
                    'executed_at': datetime.now().isoformat()
                }
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'execution_time': execution_time
            }
```

## 七、部署与运维

### 7.1 部署架构

```
┌─────────────────────────────────────────────────┐
│                云平台/自托管                    │
│  ┌─────────────┐      ┌─────────────┐         │
│  │   GitHub    │      │   GitLab    │         │
│  │   Agent     │      │   Agent     │         │
│  └─────────────┘      └─────────────┘         │
│          │                    │                │
│          └──────────┬─────────┘                │
│                     │                          │
│            ┌────────▼────────┐                 │
│            │  统一网关服务   │                 │
│            │  (K8s部署)     │                 │
│            └────────┬────────┘                 │
│                     │                          │
│            ┌────────▼────────┐                 │
│            │  数据库集群     │                 │
│            │  (PostgreSQL)   │                 │
│            └────────┬────────┘                 │
│                     │                          │
│            ┌────────▼────────┐                 │
│            │  缓存/消息队列  │                 │
│            │  (Redis/RabbitMQ)│                │
│            └─────────────────┘                 │
└─────────────────────────────────────────────────┘
                     │
            ┌────────▼────────┐
            │  开发者本地环境 │
            │  (Local Agent)  │
            └─────────────────┘
```

### 7.2 部署配置

```yaml
# docker-compose.yml 示例
version: '3.8'

services:
  # 统一网关
  gateway:
    image: doubao-agent-gateway:latest
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/agent
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  # Agent核心服务
  agent-core:
    image: doubao-agent-core:latest
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/agent
      - REDIS_URL=redis://redis:6379
      - GITHUB_CONFIG=/config/github.yaml
      - GITLAB_CONFIG=/config/gitlab.yaml
    volumes:
      - ./config:/config
    depends_on:
      - db
      - redis
  
  # 数据库
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=agent
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  # Redis
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 7.3 监控与告警

| 监控指标 | 阈值 | 告警方式 |
|----------|------|----------|
| **API成功率** | < 95% | Slack/Email/PagerDuty |
| **响应时间** | > 5s | Slack/Email |
| **WebSocket连接数** | > 1000 | Slack |
| **内存使用率** | > 80% | PagerDuty |
| **磁盘使用率** | > 85% | Email |
| **认证失败率** | > 10% | Slack/Email |

## 八、豆包Agent升级项（U132）

### 8.1 升级内容

1. **新增GitLab平台适配器**
2. **实现统一网关服务**
3. **集成WebSocket本地工具**
4. **添加多步认证支持**
5. **建立统一监控面板**

### 8.2 预期效果

- **平台覆盖扩展**：从GitHub单平台扩展到双平台
- **企业兼容性**：支持企业级认证和权限管理
- **开发体验**：本地工具无缝集成，提升开发效率
- **运维简化**：统一管理双平台Agent，降低运维成本

## 九、迁移与兼容性

### 9.1 从单平台迁移到双平台

1. **配置迁移**：现有GitHub配置自动迁移到新系统
2. **数据迁移**：Agent记忆、任务历史等数据迁移
3. **权限映射**：GitHub权限自动映射到统一权限模型
4. **逐步切换**：支持并行运行，逐步迁移

### 9.2 向后兼容性

- **API兼容**：保持现有GitHub Agent API不变
- **配置兼容**：支持现有配置文件格式
- **工具兼容**：现有本地工具无需修改
- **客户端兼容**：现有客户端可继续使用

## 十、协议版本

- **v1.0** (2026-06-01)：初始版本，基于OpenCode v1.3 GitLab Agent Platform设计
- **未来规划**：v2.0将支持更多平台（Bitbucket、Azure DevOps等）

---

> **集成状态**：待集成
> **优先级**：中
> **预计工作量**：4-5人周
> **依赖**：GitHub/GitLab API SDK、WebSocket服务器、OAuth 2.1库
