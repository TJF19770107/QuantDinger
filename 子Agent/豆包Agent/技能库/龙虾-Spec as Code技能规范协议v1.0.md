# 龙虾-Spec as Code技能规范协议 v1.0

> 协议编号: 120 | 版本: v1.0 | 来源: Hermes双层技能架构 + SKILL.md HARDLINE标准
> 生效范围: 全域技能库 | 依赖: KBArchiving + AgentIter

---

## 一、核心理念

**Spec as Code = 自然语言即代码**

传统Agent的技能完全依赖人工编写（Python/YAML），一旦发布就固定不变。
Hermes彻底颠覆：所有Skill用纯自然语言Markdown编写，Agent通过skill_manager_tool自主完成create/patch/delete。

## 二、双层技能架构

| 类型 | 路径 | 说明 |
|------|------|------|
| 内置技能（12技能锁） | 我的AI分身/技能库/ | 全域模板锁死，不可删减 |
| 可选技能（扩展技能） | 子Agent/豆包Agent/技能库/ | 较重/专业化技能，按需加载 |

## 三、SKILL.md 规范

```yaml
---
name: skill_name
description: "一句话描述（≤60字符，以句号结尾）"
version: "1.0.0"
author: "@作者"
license: MIT
platforms: [windows, linux, macos]
metadata:
  tags: [tag1, tag2]
  category: 分类
  related_skills: [关联技能]
  config:
    key: "配置说明"
---

# 技能标题

## 触发条件
- 触发词/条件描述

## 前置条件
- API密钥、MCP服务器等依赖

## 执行步骤
1. 使用原生工具 `tool_name` 执行步骤1
2. 使用 `tool_name2` 执行步骤2

## 已知限制
- 限制说明

## 验证方法
- 测试验证步骤
```

## 四、硬性标准（对标Hermes HARDLINE）

| # | 标准 | 说明 |
|---|------|------|
| 1 | description ≤ 60字符 | 避免列表膨胀，以句号结尾 |
| 2 | 使用原生工具引用 | `search_files` 而非 `grep`，`read_file` 而非 `cat` |
| 3 | 平台声明 | POSIX特有原语的技能必须声明平台 |
| 4 | 作者署名 | 归功于人类贡献者 |
| 5 | 脚本目录规则 | 辅助脚本必须放在 `scripts/` 目录 |
| 6 | 测试要求 | 必须有 `tests/skills/test_<skill>_skill.py` |

## 五、Agent自主操作

Agent可通过以下六种操作管理Skills：

| 操作 | 说明 |
|------|------|
| create | 创建新Skill文件 |
| patch | 修改现有Skill内容 |
| delete | 删除废弃Skill |
| list | 列出所有可用Skills |
| execute | 执行指定Skill |
| status | 查询Skill使用统计 |

## 六、安全审计优势

- 审Markdown比审几千行Python代码简单10倍
- 所有Skills纯文本，可读可审查
- 无隐藏代码执行风险
- 版本历史清晰可追溯