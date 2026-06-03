---
plugin: templater
version: 1.0
created: 2026-05-31
tags: [obsidian-config, templater]
---

# Templater 插件配置说明

## 插件简介

Templater 是 Obsidian 的高级模板引擎，支持在模板中使用 JavaScript 语法动态生成内容。

## 核心配置

### 模板目录
```
PARA/03-Resources/策略模板/
```

### 模板语法变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{date}}` | 当前日期 | 2026-05-31 |
| `{{time}}` | 当前时间 | 14:30:00 |
| `{{title}}` | 文件名 | 策略文档模板 |
| `{{date:YYYY-MM-DD}}` | 格式化日期 | 2026-05-31 |

### 快捷触发命令

| 快捷键 | 功能 |
|--------|------|
| Alt+N | 从模板新建文件 |
| Alt+Shift+N | 插入模板内容 |

## 模板文件列表

- `策略文档模板.md` — 新建策略文档时使用
- `交易复盘模板.md` — 新建复盘记录时使用
- `行情分析模板.md` — 新建行情分析时使用

## 使用方式

1. `Ctrl+P` → Templater: Insert template → 选择模板
2. 或直接 `Alt+N` 从模板新建文件
