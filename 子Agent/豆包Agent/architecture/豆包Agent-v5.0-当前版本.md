# 豆包Agent - 当前版本状态
> 版本：v5.0 (R05)  
> 状态：ACTIVE  
> 更新日期：2026-05-31

## 版本概述
R05 全维度迭代升级：补齐6大自主能力（自主读文件、自主学技能、自主生成技能、自主控桌面、自主唤醒与执行、安全回滚），整合自进化引擎v2.0。

## 三层协同架构（R04 + R05）

### Layer 3: 云端顾问层
- Marvis 主脑（云端大模型）：专家决策、安全最终审查、复杂模式提取
- 端云路由：6维度评分 → 端侧/端+云/云端三档
- 专家Token占比目标 < 15%

### Layer 2: 本地执行层
- DesktopController：三层安全控制（Shell/API/自动化）
- AutoFileScanner：自动文件感知与能力注册
- Shell/API 执行：受限命令执行

### Layer 1: 自进化核心层
- **AutoWake**：自主唤醒引擎（定时/事件/监听三模式 + 优先级队列）
- **MemoryOS**：三层记忆操作系统（Working/Session/Long-term + 自动压缩衰减）
- **SkillForge**：自主技能锻造引擎（模式提取 → 技能生成 → 自动注册）
- **SafeGuard**：三环安全护栏（执行前审查 + 运行时监控 + 自动回滚）

## 六大Agent模块
| 模块 | 状态 | R05进展 |
|------|------|---------|
| 自进化Agent | ✅ 激活 | AutoWake+SkillForge+SafeGuard闭环 |
| 多Agent协调 | 🔄 规划中 | 基于AutoWake任务队列 |
| 自主编码Agent | 🔄 规划中 | 基于SkillForge代码生成 |
| 本地执行Agent | ✅ 激活 | DesktopController+AutoFileScanner |
| 记忆系统Agent | ✅ 激活 | MemoryOS三层架构 |
| 安全审查Agent | ✅ 激活 | SafeGuard三环护栏 |

## 差异化定位
**唯一手机端AI IDE + Agent**：用户可在手机上通过豆包APP完成全链路开发——写代码、跑程序、控桌面、自进化、安全回滚。

## 下轮目标（R06）
1. 6大技能模块代码骨架工程落地
2. 检查点体系初始化
3. 任务队列首次自动调度测试
4. DeepSeek Coder V3 / Qwen3 Coder 480B 追踪
