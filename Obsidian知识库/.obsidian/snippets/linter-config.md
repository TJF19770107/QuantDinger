---
plugin: linter
version: 1.0
created: 2026-05-31
tags: [obsidian-config, linter]
---

# Linter 规则配置

## 插件简介

Obsidian Linter 用于自动格式化和规范 Markdown 文件内容，确保知识库文件风格统一。

## 核心规则

### Frontmatter 规则

```yaml
# 必须包含的 Frontmatter 字段
required-fields:
  - title
  - file_type
  - created
  - tags

# Frontmatter 排序
yaml-timestamp-sort: created
yaml-key-sort: true

# 日期格式
date-format: YYYY-MM-DD
```

### 标题规则

```yaml
# 标题格式
heading-style: atx        # 使用 # 风格
heading-blank-lines: true # 标题前后空行
h1-starts-on-line: 1      # H1 从第一行开始（Frontmatter 之后）
```

### 内容规则

```yaml
# 空白与标点
trailing-spaces: false    # 删除尾部空格
consecutive-blank-lines: 1 # 最多连续空行数
spacing-after-list-markers: true

# 强制规则
force-yaml-escape: true   # YAML 特殊字符转义
escape-yaml-special-chars: true

# Obsidian 特有
convert-bullet-list-markers: true  # 统一列表标记为 -
```

## 自动化设置

- **保存时自动格式化**：启用
- **手动触发**：`Ctrl+P` → Linter: Lint the current file
- **批量格式化**：`Ctrl+P` → Linter: Lint all files in the vault

## 排除规则

以下目录不应用 Linter：
- `.obsidian/`
- `.git/`
- `temp/`
- `旧模板归档/`
