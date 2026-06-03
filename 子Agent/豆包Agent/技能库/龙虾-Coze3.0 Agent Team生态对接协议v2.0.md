# 龙虾-Coze3.0 Agent Team生态对接协议 v2.0

> **协议编号**: #161
> **对标来源**: Coze 3.0 (字节跳动, 2026-06-01) + Claude Code + Codex CLI + OpenClaw
> **上一版本**: v1.0 (协议#141, 2026-06-02)
> **版本**: v2.0
> **生效日期**: 2026-06-02
> **状态**: ✅ 已落地

---

## 一、协议概述

本协议升级自v1.0（协议#141），全面对接**Coze 3.0 Agent Team生态**，支持三端协同（macOS/Windows/iOS/Android/Web）、本地Agent接入（Claude Code/Codex CLI/OpenClaw）、云端Agent方案（Coze云电脑）、编程项目与视频项目的深度集成。

**核心升级**：
- 新增三端协同架构
- 新增本地Agent接入标准
- 新增云端Agent（Coze云电脑）对接
- 新增编程项目/视频项目空间集成
- 新增行业技能包对接

---

## 二、Coze 3.0 核心架构

### 2.1 Agent Team架构

```
用户
 └── Coze 3.0 项目空间
       ├── Agent A (Claude Code 本地接入)
       ├── Agent B (Codex CLI 本地接入)
       ├── Agent C (OpenClaw 本地接入)
       ├── Agent D (Coze云电脑-原生)
       └── Agent E (Coze云电脑-OpenClaw)
       
       [所有Agent共享项目上下文、文件、对话历史]
```

### 2.2 三端协同

| 端 | 功能 | 同步机制 |
|----|------|---------|
| **网页端** (coze.cn) | 完整功能，项目管理，Agent配置 | 实时WebSocket同步 |
| **桌面端** (macOS/Windows) | 本地文件访问，系统级集成 | 本地缓存+云端同步 |
| **移动端** (iOS/Android) | 任务查看，审批，轻量交互 | Push通知+增量同步 |

**协同场景**：
1. 在桌面端创建编程项目 → 移动端查看进度 → 网页端继续开发
2. 移动端收到Agent需要审批的通知 → 桌面端处理本地文件 → 结果同步至所有端

---

## 三、本地Agent接入标准

### 3.1 接入流程

```
Step 1: 在Coze 3.0中创建项目空间
Step 2: 进入"Agent管理" → "添加本地Agent"
Step 3: 选择Agent类型（Claude Code / Codex CLI / OpenClaw / 自定义）
Step 4: 配置本地Agent的API端点或本地路径
Step 5: 授权Coze访问本地文件（可选）
Step 6: 测试连接 → 接入成功
```

### 3.2 支持的本地Agent

| Agent | 接入方式 | 能力 | 限制 |
|-------|---------|------|------|
| Claude Code | CLI命令转发 | 编码/调试/重构 | 需要本地运行Claude Code |
| Codex CLI | REST API | 代码生成/测试 | 需要OpenAI API Key |
| OpenClaw | WebSocket | 全系统访问/记忆/技能 | 需要本地运行OpenClaw |
| 自定义 | OpenAPI 3.0规范 | 任意能力 | 需要自行实现接口 |

### 3.3 通信协议

```json
// Coze → 本地Agent 请求格式
{
  "request_id": "req_20260602_001",
  "project_context": {
    "project_id": "proj_abc123",
    "files": [{"path": "src/main.py", "content": "..."}],
    "conversation_history": [...]
  },
  "task": "实现用户登录功能",
  "agent_specific_config": {
    "model": "claude-opus-4.8",
    "temperature": 0.7
  }
}

// 本地Agent → Coze 响应格式
{
  "request_id": "req_20260602_001",
  "status": "completed",
  "result": {
    "files_modified": ["src/auth.py", "tests/test_auth.py"],
    "explanation": "已实现基于JWT的用户登录..."
  },
  "token_usage": {"input": 1200, "output": 3500}
}
```

---

## 四、云端Agent方案（Coze云电脑）

### 4.1 云电脑规格

| 规格 | CPU | 内存 | 存储 | 适用场景 |
|------|-----|------|------|---------|
| 基础版 | 4核 | 16GB | 100GB | 轻量开发/测试 |
| 标准版 | 8核 | 32GB | 200GB | 中型项目/多Agent |
| 专业版 | 16核 | 64GB | 500GB | 大型工程/并行Agent |

### 4.2 云电脑中的Agent运行时

```
Coze云电脑
  ├── Claude Code (云端版)
  ├── Codex CLI (云端版)
  ├── OpenClaw (云端版)
  ├── 豆包Agent (云端接入)
  └── 自定义Agent (Docker容器)
```

**优势**：
- 无需本地环境配置
- 7×24小时持续运行
- 多Agent并行无本地资源限制
- 与Coze项目空间原生集成

---

## 五、项目空间深度集成

### 5.1 编程项目

```
用户在Coze对话框:
  "创建一个Todo App，用React+TypeScript"

Coze流程:
  1. 创建编程项目空间
  2. 激活Agent Team:
     - 架构Agent: 设计项目结构
     - 前端Agent: 实现React组件
     - 后端Agent: 实现API接口
     - 测试Agent: 生成单元测试
  3. 多人协同: 设计师Agent改样式，开发Agent改逻辑
  4. 对话式部署: "帮我部署到Vercel"
  5. 项目同步至 code.coze.cn 管理
```

### 5.2 视频项目

```
用户在Coze对话框:
  "做一个产品宣传视频，1分钟，科技风格"

Coze流程:
  1. 创建视频项目空间
  2. 剧本Agent: 生成脚本（基于Seedance 2.0格式）
  3. 分镜Agent: 设计分镜头
  4. 生成Agent: 调用Seedance 2.0生成视频片段
  5. 音乐Agent: 生成或匹配背景音乐
  6. 剪辑Agent: 对话式剪辑（"把第3秒的转场改快一点"）
  7. 导出: 支持直接导出为剪映工程文件
```

---

## 六、行业技能包

### 6.1 技能包架构

```
行业技能包
  ├── 投研技能包
  │   ├── 财报分析Skill
  │   ├── 行业对比Skill
  │   ├── 估值模型Skill
  │   └── 风险提示Skill
  ├── 法务技能包
  │   ├── 合同审查Skill
  │   ├── 类案检索Skill
  │   ├── 法条查询Skill
  │   └── 法律备忘录Skill
  ├── 科研技能包
  │   ├── 文献综述Skill
  │   ├── 实验设计Skill
  │   ├── 数据分析Skill
  │   └── 论文撰写Skill
  └── 自媒体技能包
      ├── 选题分析Skill
      ├── 文案生成Skill
      ├── 封面设计Skill
      └── 发布规划Skill
```

### 6.2 技能包使用

```
用户: "帮我分析腾讯2025年Q4财报"

Coze自动:
  1. 检测需求类型 → 投研
  2. 加载"投研技能包"
  3. 激活财报分析Agent
  4. 执行:
     - 下载腾讯Q4财报（若未提供）
     - 提取关键指标（营收/净利润/毛利率等）
     - 同比/环比分析
     - 行业对比（与阿里/字节对比）
     - 估值分析（PE/PB/PS）
     - 风险提示
  5. 生成投研报告（Word/PDF）
```

---

## 七、与豆包Agent的集成

### 7.1 集成架构

```
豆包Agent
  ├── 本地运行（Windows/Mac/Linux）
  ├── 接入Coze 3.0项目空间（作为本地Agent）
  └── 能力暴露:
        ├── 文件读写（授权目录下）
        ├── 代码执行（沙箱隔离）
        ├── 记忆系统（MEMORY.md/USER.md）
        └── 技能库（skills/目录）
```

### 7.2 配置步骤

```bash
# 1. 在Coze 3.0中创建项目
# 2. 添加本地Agent → 选择"自定义"
# 3. 配置Webhook URL（豆包Agent监听地址）
# 4. 在豆包Agent中启用Coze适配器

# 豆包Agent配置（~/.lobster/config.yaml）
coze_adapter:
  enable: true
  coze_api_base: "https://api.coze.cn"
  coze_api_key: "pat_xxx"
  project_id: "proj_abc123"
  webhook_port: 8080
  allowed_directories:
    - "E:/工作文档"
    - "E:/代码项目"
```

### 7.3 协同场景

| 场景 | 参与Agent | 流程 |
|------|----------|------|
| 跨设备任务接力 | 豆包Agent(桌面端) + Coze云电脑Agent | 桌面端处理本地文件 → 结果同步至云电脑 → 云电脑继续后续任务 |
| 多模态任务 | 豆包Agent(代码) + OpenClaw(网页) + Claude Code(架构) | 各Agent专长分工，结果汇聚至Coze项目空间 |
| 长时间任务 | Coze云电脑Agent（主） + 豆包Agent（本地辅助） | 云电脑7×24运行，需要本地资源时调用豆包Agent |

---

## 八、部署指南

### 8.1 依赖

```bash
pip install requests aiohttp websockets
# 可选：Coze SDK（待官方发布）
```

### 8.2 配置文件

```yaml
coze3_integration:
  enable: true
  version: "3.0"
  api:
    base_url: "https://api.coze.cn"
    api_key: "${COZE_API_KEY}"
  project_space:
    enable: true
    auto_create: true
    space_name: "豆包Agent工作空间"
  local_agent_access:
    enable: true
    agents:
      - name: "豆包Agent"
        type: "custom"
        endpoint: "http://localhost:8080/webhook"
        capabilities: ["file_read", "file_write", "code_execute", "memory_access"]
  cloud_agent:
    enable: false  # 需要Coze云电脑订阅
    specification: "standard"  # basic/standard/professional
  skill_packages:
    - "investment_research"
    - "legal"
    - "scientific_research"
    - "content_creation"
```

### 8.3 启动方式

```bash
# 启动Coze 3.0适配器
python -m lobster.adapters.coze3 --enable

# 在Coze网页端完成Agent添加后，测试连接
python -m lobster.adapters.coze3 --test-connection
```

---

## 九、协议版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-02 | 初始版本（协议#141），基础Coze 3.0对接 |
| **v2.0** | **2026-06-02** | **全面升级：三端协同+本地Agent接入+云电脑+编程/视频项目+行业技能包** |

---

> **协议状态**: ✅ 已落地
> **对标产品**: Coze 3.0 (字节跳动, 2026-06-01发布)
> **集成协议**: #141(Coze3.0 v1) / #160(去中心化自组织Agent团队)
> **下一版本计划**: v3.0 支持ClawInstitute平台对接（协议#160）
