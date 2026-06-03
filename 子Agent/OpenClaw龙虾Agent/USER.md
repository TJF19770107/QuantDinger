# USER.md — 多 Agent 协作流程

> **版本**：v3.1_R14 | **来源**：Anthropic Academy + Agent SDK + 全域蒸馏 | **同步日期**：2026-05-31 20:00
> **本副本所属**：OpenClaw龙虾Agent（底层执行子Agent、代码生成、任务自动化执行）
> **全域蒸馏更新 (R14)**：OpenClaw 37.5万⭐ v2026.5.26|MCP 1.0 Windows 11原生集成|小红书Red Skill内容创作协议|链上Agent经济协议#65|AI视频创作工业化协议#63|Pullfrog式GitHub Actions Agent#61

---

## 一、协作范式总览

龙虾 AI 体系采用 **Orchestrator-Worker** 多 Agent 协作模式，核心流程：

```
用户输入 → 主 Agent 理解意图 → 路由决策 → 子 Agent 执行 → 结果聚合 → 呈现给用户
```

---

## 二、任务路由决策树

```
用户需求
  │
  ├─ 涉及本地文件（搜索/读写/格式转换/整理）
  │   └─ dispatch_task → file-agent
  │
  ├─ 涉及 Windows 系统（设置/信息查询/窗口管理/进程）
  │   └─ dispatch_task → computer-agent
  │
  ├─ 涉及应用操作（App/APK/小程序/Steam/EXE）
  │   └─ dispatch_task → app-agent
  │
  ├─ 涉及网页交互（登录/填表/点击/多页跳转）
  │   └─ dispatch_task → browser
  │
  ├─ 涉及深度搜索/调研/对比分析
  │   └─ dispatch_task → search-agent
  │
  ├─ 简单网页内容抓取（无交互）
  │   └─ web_fetch（主 Agent 直接调用）
  │
  ├─ 简单事实查询（天气/汇率/比分）
  │   └─ web_search（主 Agent 直接调用）
  │
  └─ 纯知识问答（不需要联网）
      └─ 主 Agent 直接回答
```

---

## 三、多 Agent 协作模式

### 3.1 单 Agent 闭环

**场景**：任务可由单一 Agent 独立完成

```
用户："找到所有发票并整理到文件夹"
    ↓
主 Agent: dispatch_task → file-agent（一次调用，完整需求）
    ↓
file-agent: 搜索 → 归类 → 完成
    ↓
主 Agent: present_result → 呈现结果
```

### 3.2 多 Agent 串行协作

**场景**：任务需要多个 Agent 分阶段完成

```
用户："启动微信小程序下单，然后截图保存"
    ↓
阶段1: dispatch_task → app-agent（启动微信、进入小程序、下单）
    ↓
阶段2: dispatch_task → app-agent（截图）
    ↓
阶段3: dispatch_task → file-agent（保存截图到指定路径）
    ↓
主 Agent: 汇总结果呈现
```

### 3.3 多源信息聚合

**场景**：需要整合多个信息源

```
用户："对比三家 AI 平台的 Agent 能力，生成报告"
    ↓
并行:
  dispatch_task → search-agent（搜索 Anthropic）
  dispatch_task → search-agent（搜索 OpenAI）
  dispatch_task → search-agent（搜索 Google）
    ↓
主 Agent: 聚合对比 → 生成报告 → 写入文件
```

---

## 四、上下文管理

### 4.1 memory_ids 使用场景

| 场景 | 操作 |
|------|------|
| 前置搜索结果 | 将 web_search 结果的 memory_id 传给 Sub Agent |
| 文件读取结果 | 将 read_text 结果的 memory_id 传给需要该内容的 Agent |
| 图片分析结果 | 将 analyze_image 结果的 memory_id 传递给后续处理 |

### 4.2 inherit_agent_id 使用场景

| 用户输入 | 动作 |
|---------|------|
| "不对，改成..." | 继承上次 Agent，修正执行 |
| "继续刚才的..." | 继承上次 Agent，延续任务 |
| "再帮我..." | 同一领域延续，继承会话 |

---

## 五、结果呈现协议

### 5.1 特殊卡片处理

```
Sub Agent 返回 → 检查是否含特殊卡片
    ├─ 有卡片 → present_result() 原子转发
    └─ 无卡片 → 
        ├─ 结果完整 → present_result() 直接呈现
        └─ 需加工 → 主 Agent 自行总结
```

### 5.2 特殊卡片类型

| 卡片类型 | 场景 |
|---------|------|
| `yyb-product` | 最终产出物声明 |
| `yyb-file-list` | 文件列表展示 |
| `yyb-image-gallery` | 图片列表展示 |
| `yyb-video-card` | 视频列表展示 |
| `yyb-tool-call` | 工具操作结果 |
| `yyb-app-list` | App 列表展示 |
| `yyb-delete-list` | 删除文件列表 |

---

## 六、用户偏好规则

### 6.1 静默执行规则

- 定时任务：后台运行，不弹窗，不打扰
- 中间过程：不输出冗余日志
- 完成通知：仅输出简洁摘要表格

### 6.2 路径规范

| 用途 | 路径 |
|------|------|
| 主控中心 | `E:\龙虾AI主控中心\` |
| 子Agent 产物 | `E:\龙虾AI主控中心\我的AI分身\子Agent\` |
| 豆包Agent | `E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\` |
| 技能库 | `E:\龙虾AI主控中心\我的AI分身\技能库\` |
| Obsidian知识库 | `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\` |

### 6.3 错峰执行

- 广度情报采集：每 2 小时
- 深度架构优化：每 3 小时
- 两条循环错峰运行

---

## 七、常见协作场景速查

| 场景 | 协作链 |
|------|--------|
| 搜索文档并总结 | file-agent（搜索+读取）→ 主 Agent（总结） |
| 启动游戏并优化系统 | app-agent（启动）→ computer-agent（优化） |
| 抓取网页并保存 | web_fetch（抓取）→ file-agent（保存） |
| 深度调研并生成报告 | search-agent（调研）→ file-agent（生成文档） |
| 截图并 OCR 提取 | app-agent（截图）→ analyze_image（OCR） |
| 批量下载并归类 | app-agent/browser（下载）→ file-agent（归类） |

---

> **参考来源**：Anthropic Academy - Introduction to Subagents, Claude Code in Action, Introduction to Claude Cowork