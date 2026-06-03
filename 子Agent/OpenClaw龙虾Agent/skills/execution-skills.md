# OpenClaw龙虾Agent · 底层执行技能

> 版本：v595 · 初始化阶段
> 适用Agent：OpenClaw龙虾Agent
> 父规则：角色总说明书 v1.0 / 龙虾全域模板 v2.4

---

## 技能1：Gateway性能引擎

### 核心指标
| 指标 | 基线 | 目标(R15) |
|------|------|----------|
| 请求吞吐 | 1000 req/s | 4100x预热 |
| P50延迟 | <50ms | <20ms |
| P99延迟 | <500ms | <200ms |
| 并发连接 | 1000 | 5000+ |

### 优化策略
- 连接池预热（4100x）
- 请求批处理合并
- 缓存层（LRU + TTL）
- 异步IO，非阻塞

---

## 技能2：插件联动框架

### 多Provider抽象层
```
插件管理 
  ├── VNPY (量化交易Provider)
  ├── Obsidian (知识管理Provider)
  ├── Trae (AI编程Provider)
  ├── MCP 1.4 (多Agent通信Provider)
  └── 自定义Provider (user-defined)
```

### 插件生命周期
1. **注册**: 发现插件 → 验证签名 → 注册Provider
2. **激活**: 懒加载 → 按需激活
3. **执行**: 隔离执行 → 结果回调
4. **卸载**: 资源释放 → 注销

---

## 技能3：MCP协议集成

### MCP 1.4 RC特性
| 特性 | 状态 | 说明 |
|------|------|------|
| 无状态化 | ✅ 支持 | 请求不依赖服务器状态 |
| Streamable HTTP | ✅ 支持 | 流式传输+背压控制 |
| 智能审批 | ✅ 集成 | SmartApprovals安全审查 |
| ACP兼容 | ✅ 兼容 | Agent通信协议网关 |

### 通信拓扑
```
OpenClaw Gateway 
  ↕ (MCP 1.4 + ACP)
  ├── 豆包Agent (交互层)
  ├── Hermes Agent (调度层)
  └── 外部Provider (VNPY/Obsidian/Trae)
```

---

## 技能4：文件系统操作

### 能力矩阵
| 操作 | 工具 | 权限控制 |
|------|------|---------|
| 文件读取 | read_file/read_text | 全文件类型，安全区 |
| 文件写入 | write_file | UTF-8编码，MD5去重 |
| 文件删除 | delete | 回收站机制，系统禁写 |
| 格式转换 | convert_file | 文档/图片/PDF互转 |
| 批量操作 | python_executor | ECC错误修正，3次降级 |

### 禁区
- `C:\Windows` `C:\Program Files` `C:\Users\Default`
- 系统隐藏文件（.系统标记）
- 锁定文件（跳过+日志）

---

> 🦞 OpenClaw龙虾Agent · 技能定义 v595