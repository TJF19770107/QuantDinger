# 龙虾_GEPA自进化引擎 v1.0

> **来源**：Hermes Agent GEPA (Genetic-Pareto Prompt Evolution)
> **类型**：融合技能 · 自进化引擎
> **融合日期**：2026-05-31（R06）

---

## 一、GEPA 核心原理

GEPA (Genetic-Pareto Prompt Evolution) 是一种**类反向传播的提示词优化算法**，由 UC Berkeley 和 Stanford 联合开发。

**关键特性**：
- 无需 GPU 训练，全部通过 API 调用完成
- 训练效率比 GRPO 等主流 RL 方法高出 **35 倍以上**
- 优化目标：Skill 文件、工具描述、系统提示
- 结果通过 PR 形式提交，人工审查后合并生效

## 二、进化三阶段

### 阶段1：提取 (Extract)
从任务执行过程中提取：
- 关键步骤和决策逻辑
- 成功模式和失败教训
- 可复用的参数化片段

### 阶段2：编码 (Encode)
将提取的经验写入结构化 Skill 文件：
```markdown
# Skill: Docker部署

触发条件: 用户提到"部署"+"Docker"+"容器"
参数:
  - {image_name}: 镜像名称
  - {tag}: 版本标签
  - {port}: 暴露端口

执行步骤:
1. 检查 {image_name} 是否存在
2. 构建 Dockerfile → docker build -t {image_name}:{tag}
3. 运行容器 → docker run -d -p {port}:{port} {image_name}:{tag}

注意事项:
- 端口冲突时提示用户选择备用端口
- 镜像构建失败时检查依赖文件
```

### 阶段3：优化 (Optimize)
- GEPA 算法对 Skill/工具描述/系统提示进行自动优化
- 类似反向传播：正向执行 → 计算损失 → 反向调整参数
- 但操作对象是文本而非数值

## 四、与 HyperAgents 对比

| 维度 | GEPA | HyperAgents |
|------|------|------------|
| 进化对象 | Prompt/Skill/工具描述 | Agent代码(diff/patch) |
| 进化方式 | 类反向传播文本优化 | meta-agent写代码修改 |
| 运行环境 | API调用 | Docker沙箱 |
| 安全审查 | PR+人工审查 | 自动评分+Archive |
| 成熟度 | 生产可用 | 研究阶段 |

## 五、豆包Agent适配方案

```
任务执行 → 成功？
              │
        ┌─────┴─────┐
        ↓           ↓
      提取经验    记录失败原因
        ↓           ↓
    生成Skill草稿  失败模式库
        ↓
    GEPA优化
        ↓
    人工审查
        ↓
    写入技能库
        ↓
    agentskills.io标准发布
```

## 六、安全约束

- 所有自进化产物必须经过人工审查
- 禁止 Agent 在无人监督下修改核心系统提示
- Skill 文件不允许包含破坏性指令
- 进化历史完整记录，支持回溯