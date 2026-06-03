# 龙虾-Gateway极致热启动协议 v1.0

> **协议编号**：66
> **对标来源**：OpenClaw Gateway v4.2 (2026-05-22)
> **创建轮次**：R18
> **创建时间**：2026-06-01
> **状态**：ACTIVE

---

## 一、协议概述

本协议通过三级缓存策略实现Agent Gateway的极致冷/热启动性能，将能力清单查询（/models端点）从20秒压缩至5毫秒（4000×加速）。缓存覆盖channel catalogs、plugin metadata、provider auth state三大热点数据，实现Agent唤醒后即时获得完整能力清单。

## 二、三级缓存架构

### 2.1 L1：内存热缓存（5ms响应）

```
缓存内容：
  - Channel catalogs（消息平台渠道目录，如Slack/Discord/微信/钉钉/企业微信）
  - Plugin metadata（插件元数据：名称/版本/能力声明/依赖关系）
  - Provider auth state（模型提供商认证状态：OpenAI/Anthropic/Google/本地模型）

生命周期：
  - 进程存活期间有效
  - 任何L2/L3更新事件触发L1增量刷新
  - 进程退出时自动释放

更新策略：
  - 写穿（Write-Through）：更新先写L2，L2成功后更新L1
  - 读时刷新（Refresh-on-Read）：L1命中但TTL过期时，异步刷新并返回旧值
```

### 2.2 L2：磁盘温缓存（200ms响应）

```
缓存内容：
  - 编译后的shrinkwrap包完整性校验数据
  - 预解析的MCP Server清单
  - Compiled plugin dependency graph
  - Provider capability matrix（各模型提供商的能力矩阵）

生命周期：
  - 跨进程重启有效
  - 增量更新（仅变更部分重新计算）
  - 包版本变更时自动触发全量重建

存储格式：
  - SQLite数据库（结构化查询）
  - 每类缓存独立表
  - 带版本号和校验和
```

### 2.3 L3：全量冷启动（20s）

```
仅在以下条件触发：
  - 首次安装（无L2缓存）
  - L2缓存版本不匹配（Gateway升级后）
  - 用户手动清除缓存

包含：
  - 完整channel/plugin/provider目录重建
  - 所有依赖解析和编译
  - 所有MCP Server能力发现
  - 构建L2缓存并回写磁盘
```

## 三、性能数据

| 操作 | 优化前 | 优化后 | 提升倍数 |
|------|--------|--------|---------|
| /models 端点 | 20s | 5ms | **4000×** |
| Gateway启动 | 15s | 2s | 7.5× |
| 插件加载 | 3s/插件 | 50ms | 60× |
| Provider认证 | 1.5s/provider | 5ms | 300× |

## 四、Windows专属增强

### 4.1 安全命令Shim

```
安装/更新/服务路径命令通过shim层执行：
  - 路径规范化：统一使用NT路径格式
  - 权限校验：拒绝写入%WINDIR%、%PROGRAMFILES%
  - 完整性检查：比对文件哈希防篡改
```

### 4.2 回滚机制

```
升级流程：
  1. 备份当前版本到 rollback/ 目录
  2. 安装新版本
  3. 运行完整性检查
  4. 验证通过 → 标记新版本为 stable
  5. 验证失败 → 自动回滚到 rollback/ 备份
  6. 保留最近3个版本备份供手动恢复
```

### 4.3 LaunchAgent交接修复

```
服务进程平滑切换：
  Old Agent进程 → [接收SIGTERM] → 完成当前任务 → 优雅退出
  New Agent进程 → [继承配置] → [加载L2缓存] → [接管服务端口]
  Zero-downtime切换目标：< 1秒
```

## 五、包完整性校验

### 5.1 Shrinkwrap机制

```
npm包发布前生成shrinkwrap文件：
  - 锁定所有依赖的精确版本
  - 记录每个包的SHA-256哈希
  - 包接受通道（Package Acceptance Lane）自动校验

校验流程：
  安装请求 → 提取包 + shrinkwrap → 计算实际哈希
  → 与shrinkwrap声明比对 → 不匹配则拒绝安装
```

## 六、豆包Agent适配方案

1. **L1缓存**：豆包Agent启动时缓存5个子Agent的能力清单和模型Provider状态，实现毫秒级Agent能力查询
2. **L2缓存**：将技能库索引、MCP Server清单、插件依赖图持久化到SQLite，跨会话复用
3. **热启动验证**：Agent唤醒后2秒内完成L1/L2加载，即使用户连续多轮对话也无需等待
4. **包校验**：技能协议文件写入时附带SHA-256签名，SkillForge加载前校验完整性
5. **回滚机制**：每次自动升级前备份当前版本至E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\checkpoints\