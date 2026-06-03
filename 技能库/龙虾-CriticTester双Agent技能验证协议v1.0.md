# 龙虾-CriticTester双Agent技能验证协议 v1.0

> **协议编号**：62
> **对标来源**：ASG Pipeline 2026 + Self-Improvement Loop + E2B Sandbox
> **创建日期**：2026-06-01
> **适用Agent**：豆包Agent / SkillForge v4.0
> **依赖**：SkillForge v3.0+ / Docker或E2B沙盒

---

## 一、协议概述

本协议为SkillForge技能生成引擎增加Critic-Tester双Agent协作验证模式。在原有"生成→存储"基础上，增加"审查→测试→修复→再审查"闭环，确保每一个自主生成的技能都经过严格的自动化质量把关。

## 二、五阶段ASG流水线

```
Phase 1: Ingestion（摄取）
    ↓  读取报告/文档 → 语义分解 → 提取可行动知识点
Phase 2: Translation（翻译）
    ↓  Intent-to-Skill → 代码生成 → 库选择
Phase 3: Verification（验证）★ 本协议新增
    ↓  Critic Agent审查 → Tester Agent测试 → Debug循环
Phase 4: Vectorization（向量化）
    ↓  技能嵌入 → 存储到向量库 → 元数据标记
Phase 5: Composition（组合）
    ↓  用户查询 → 检索匹配技能 → 技能链组合执行
```

## 三、Critic-Tester双Agent设计

### 3.1 Critic Agent（审查者）

**职责**：
- 代码逻辑审查：技能实现的逻辑是否与源文档一致
- 安全审查：代码是否存在安全漏洞
- 最佳实践审查：命名规范、性能、可维护性
- 与已有技能的去重审查：是否与现有技能功能重复

**输出**：
```json
{
  "pass": true/false,
  "issues": ["问题1", "问题2"],
  "score": 0-100,
  "merge_suggestion": "可合并至技能XYZ"  // 如检测到重复
}
```

### 3.2 Tester Agent（测试者）

**职责**：
- 自动生成Unit Tests
- 在沙盒中执行生成的技能代码
- 收集执行结果、错误日志、性能数据
- 失败时回传错误信息给Creator修复

**输出**：
```json
{
  "tests_total": 10,
  "tests_passed": 9,
  "tests_failed": 1,
  "failures": [{"test": "test_edge_case", "error": "..."}],
  "execution_time_ms": 234
}
```

### 3.3 自修复循环

```
Creator生成技能 → Critic审查 → 不通过 → Creator修复
                                      ↓ 通过
                                Tester测试 → 失败 → Creator修复+Critic重审
                                      ↓ 通过
                                存储到技能库
```

最大修复循环次数：3次（超过则标记为"需人工介入"）

## 四、沙盒安全执行

### 4.1 隔离要求

- Docker容器或E2B沙盒执行
- 无网络访问（除白名单API）
- CPU/内存资源限制
- 执行超时：30秒
- 文件系统只读（除指定临时目录）

### 4.2 禁止行为

- 禁止访问本地敏感文件
- 禁止网络请求到非白名单地址
- 禁止修改系统配置
- 禁止执行系统命令（除白名单）

## 五、去重与Meta-Skill合并

### 5.1 技能相似度检测

- 对新生成技能与已有技能库做向量相似度计算
- 相似度 > 0.85 → 建议合并
- 相似度 0.7-0.85 → 标记为"可能重复"

### 5.2 Meta-Skill合并策略

- 相似技能自动提取公共逻辑 → 生成Meta-Skill基类
- 差异逻辑保留为特化子技能
- 合并后自动回归测试所有子技能

## 六、实施路径

| 阶段 | 内容 | 优先级 |
|------|------|--------|
| Phase 1 | Critic Agent代码审查 + 安全扫描 | P0 |
| Phase 2 | Tester Agent单元测试自动生成 + 沙盒执行 | P0 |
| Phase 3 | 自修复循环（Creator-Critic-Tester闭环） | P1 |
| Phase 4 | 去重检测 + Meta-Skill合并 | P2 |

---

> **版本**：v1.0
> **状态**：ACTIVE
> **关联文件**：skill-forge-v3.0.md, SkillForge/SKILL.md
