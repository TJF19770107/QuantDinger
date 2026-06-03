# 豆包Agent - 当前版本状态
> 版本：v6.0 (R06)
> 状态：ACTIVE · 工程落地阶段
> 更新日期：2026-05-31

## 版本概述
R06 工程落地迭代：6大模块代码骨架生成完成、检查点体系初始化、任务队列首次自动调度、DeepSeek-Coder V3/Qwen3 Coder 480B-A35B/DGM/LoongFlow/WISE-Flow 技术情报对标。

## 三层协同架构（R04→R05→R06）

### Layer 3: 云端顾问层
- Marvis 主脑（云端大模型）：专家决策、安全最终审查、复杂模式提取
- 端云路由：6维度评分 → 端侧/端+云/云端三档
- 专家Token占比目标 < 15%
- **R06新增强**：DGM自进化验证闭环审查

### Layer 2: 本地执行层
- **DesktopController v2.0**：三层安全控制 + pywinauto UI自动化 + 审计日志
- **AutoFileScanner v2.0**：自动文件感知 + 代码骨架落地 + Watchdog增量更新
- **Shell/API 执行**：受限命令执行 + 操作白名单

### Layer 1: 自进化核心层
- **AutoWake v2.0**：自主唤醒引擎 + PES任务拆分 + 优先级抢占 + 超时熔断
- **MemoryOS v2.0**：三层记忆操作系统 + WISE-Flow工作流提取 + 压缩引擎
- **SkillForge v2.0**：自主技能锻造引擎 + DGM演化树 + LoongFlow PES融合
- **SafeGuard v2.0**：三环安全护栏 + 检查点管理器 + 动态阈值监控

## 六大Agent模块 (v6.0)
| 模块 | 版本 | 状态 | R06进展 |
|------|------|------|---------|
| 自进化Agent | v2.0 | ✅ 激活 | AutoWake+SkillForge+SafeGuard闭环 + 代码骨架 |
| 多Agent协调 | v1.0 | ✅ 激活 | AutoWake任务队列 + PES拆分 |
| 自主编码Agent | v1.0 | 🔄 规划中 | SkillForge代码生成基础已就绪 |
| 本地执行Agent | v2.0 | ✅ 激活 | DesktopController+AutoFileScanner代码骨架 |
| 记忆系统Agent | v2.0 | ✅ 激活 | MemoryOS三层架构 + 压缩引擎代码骨架 |
| 安全审查Agent | v2.0 | ✅ 激活 | SafeGuard三环护栏 + 检查点管理器代码骨架 |

## 新增基础设施 (R06)
| 基础设施 | 路径 | 说明 |
|---------|------|------|
| 检查点体系 | checkpoints/ | 稳定版本指针 + 回滚历史 + 检查点快照 |
| 任务队列 | task_queue.json | P0安全审查/P1迭代/P2扫描/P3归档 |
| 代码骨架 | 技能库/*/code/*.py | 6个模块Python工程代码 |
| 启动脚本 | auto_start.py | 一键启动全模块 |
| 审计日志 | audit/ | 操作审计结构化日志 |

## R06 技术对标新增
| 对标源 | 落地模块 |
|--------|---------|
| DeepSeek-Coder V3 (年度最佳Coding模型) | 能力对标矩阵 + 代码质量基准 |
| Qwen3 Coder 480B-A35B (Apache 2.0 MoE) | 自进化引擎MoE路由参考 |
| Darwin Gödel Machine (SWE-bench 20→50%) | SkillForge DGM演化树 |
| LoongFlow (PES范式 效率+60%) | AutoWake PES任务拆分 |
| WISE-Flow (工作流结构化经验) | MemoryOS记忆提取 |

## 差异化定位
**唯一手机端AI IDE + Agent**：用户可在手机上通过豆包APP完成全链路开发——写代码、跑程序、控桌面、自进化、安全回滚。

## 下轮目标（R07）
1. 6大模块代码骨架首次联调测试
2. 检查点体系首次自动快照
3. 任务队列首次PES自动调度执行
4. Qwen3 Coder 480B MoE架构深度研究
5. 技能演化树首次自动生成测试

---

> 当前版本声明：v6.0 R06
> 上一版本：v5.0 R05
> 状态：ACTIVE · 工程落地
