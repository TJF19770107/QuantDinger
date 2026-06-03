# 龙虾-BYOK模型无关CI Agent协议 v1.0

> **对标**: Pullfrog (Colin McDonnell/Zod作者, 2026-05-12)
> **状态**: ✅ R45落地
> **版本**: v1.0 · 2026-06-02

---

## 一、协议概述

定义豆包Agent在CI/CD环境中的BYOK(Bring-Your-Own-Key)运行范式。Agent完全运行在仓库CI环境内，零托管依赖，模型无关，一键切换LLM提供商。

## 二、核心机制

### 2.1 BYOK架构

```
仓库 .github/workflows/pullfrog.yml
  ├─ API Key: GitHub Secrets (不入仓库)
  ├─ LLM Provider: 配置项一键切换
  └─ Agent逻辑: 开源代码审计
```

支持提供商: Anthropic / OpenAI / Google / Mistral / DeepSeek / OpenRouter

### 2.2 GitHub Actions原生运行时

- 零托管依赖，完全运行在仓库CI环境
- 单文件配置 (pullfrog.yml)
- 触发方式: @pullfrog标记 / webhook自动触发 / cron定时

### 2.3 专用MCP Git服务器

- 创建PR / 留下review / 读取CI日志 / 管理issue
- Shell命令子进程隔离，无敏感环境变量访问
- 内置无头浏览器：端到端测试+截图+UI迭代

### 2.4 五合一覆盖

| 能力 | 对标 | 触发方式 |
|------|------|---------|
| PR Review | CodeRabbit | 新PR自动 / @pullfrog |
| Issue Triage | GitHub Actions | 新Issue自动 |
| CI自动修复 | - | CI失败自动 |
| 合并冲突解决 | - | 冲突检测自动 |
| 计划生成 | - | Issue标记 |

## 三、安全边界

- API Key仅存储在GitHub Secrets
- Agent运行在隔离的GitHub Actions沙箱
- Shell命令无敏感环境变量访问
- 所有操作有完整审计日志
- PR/Merge操作需人工最终批准

## 四、与现有协议的协同

| 协同协议 | 协同点 |
|---------|-------|
| #164 自验证驱动测试时扩展 | CI修复时先自验证再提交 |
| #167 诚实性自检协议 | PR Review中主动标记不确定性 |
| #131 Durable Execution v2.0 | CI Agent崩溃自动恢复 |