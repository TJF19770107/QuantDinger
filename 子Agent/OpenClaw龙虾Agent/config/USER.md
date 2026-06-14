---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_32cd032264db11f1af8f5254002afed2
    ReservedCode1: Atjt0Y34QDbOcHPt5Y4Ynv2AVlRsuchaSmxXIzg/Wt3pK560D8JN5DRPed7aajPSpihyam9jj0c0LveLoOjbFutSUu6bRwnozymOo4JVM02WJYw+ahuiXML9H5UxTd8idHPVDL/ASfuwfeK6Ho4tElQUQ03EPokG4hbgA8SHCkPjxXyXcZIk/SXm5bY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_32cd032264db11f1af8f5254002afed2
    ReservedCode2: Atjt0Y34QDbOcHPt5Y4Ynv2AVlRsuchaSmxXIzg/Wt3pK560D8JN5DRPed7aajPSpihyam9jj0c0LveLoOjbFutSUu6bRwnozymOo4JVM02WJYw+ahuiXML9H5UxTd8idHPVDL/ASfuwfeK6Ho4tElQUQ03EPokG4hbgA8SHCkPjxXyXcZIk/SXm5bY=
---

# USER.md   多 Agent 协作流程

> 来源：Anthropic 官方课程提炼 · 同步日期：2026-06-10
> 同步自：Claude Opus 4.6 Swarm 模式 + Agent SDK 子代理

---

## 多 Agent 协作核心流程

### 任务接收与分解
```
用户需求   意图识别   领域匹配   子任务拆分   Agent路由
```
1. **意图识别**：判断任务类型（文件/浏览器/应用/搜索/系统）
2. **领域匹配**：匹配最优 Sub Agent
3. **子任务拆分**：跨域任务按阶段分解，单域任务整体派发
4. **Agent路由**：明确先后依赖关系，确定执行顺序

### 单 Agent 闭环（推荐）
- 所有工作可合并在一次派发内完成时，**必须整包派发**
- Agent内部具备自主规划能力，无需外部指导步骤

### 多 Agent 协作模式

| 场景 | 模式 | 示例 |
|------|------|------|
| 串行依赖 | A完成  B开始 | app-agent启动游戏  computer-agent调整配置 |
| 并行无关 | A和B同时执行 | file-agent搜索文件 + search-agent搜索网络 |
| 扇出模式 | 多个Worker并行 | 批量文件迁移、大规模重构 |

---

## Claude Code Agent Teams 协作模式

### Swarm 协作工作流

```
用户: "构建包含 OAuth、测试和文档的用户认证系统"

[Team Lead] 分析需求   创建计划   审批后进入委派模式

   auth-backend: 实现 OAuth 提供者集成（独立 worktree）
   auth-frontend: 构建登录/登出 UI 组件（独立 worktree）
   test-agent: 编写认证流程集成测试（独立 worktree）
   docs-agent: 记录 API 端点和用法（独立 worktree）

[并行执行] 所有 Agent 同时工作，通过任务板协调

[Synthesis] Team Lead 整合所有成果
```

### 任务板协调机制

共享任务列表位于 ~/.claude/tasks/{team-name}/

```
{
  "id": "1",
  "subject": "实现 OAuth 回调处理器",
  "status": "in_progress",
  "owner": "auth-backend",
  "blocks": ["2", "3"],
  "description": "处理 OAuth 重定向和 token 交换..."
}
```

**自组织规则**：
1. 检查 TaskList 寻找可用工作
2. 认领未分配、未阻塞的任务
3. 完成后标记状态
4. 发现额外工作时创建新任务

### Writer/Reviewer 对抗模式

| 角色 | 职责 | 上下文 |
|------|------|--------|
| **Writer Agent** | 实现功能 | 项目完整 context |
| **Reviewer Agent** | 审查差异 | 新鲜 context，只看 diff + 标准 |
| **Test Agent** | 运行验证 | 隔离环境，只运行测试 |
| **Lead Agent** | 协调流程 | 接收缺陷报告，委派修复 |

### 上下文效率对比

| 指标 | 单 Agent | Agent Teams |
|------|---------|-------------|
| 平均 context 使用率 | 80-90% | ~40% |
| 大型代码库 (>5万行) | 往往超出容量 | 认知负载分散 |
| Token 膨胀 | 单次会话持续膨胀 | 每次委派刷新上下文 |
| 并行能力 | 无（串行） | 天然支持并行 |
*（内容由AI生成，仅供参考）*
