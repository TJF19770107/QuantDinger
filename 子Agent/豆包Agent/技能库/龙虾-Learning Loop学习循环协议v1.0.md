# 龙虾-Learning Loop学习循环协议 v1.0

> 协议编号: 117 | 版本: v1.0 | 来源: Hermes Agent Learning Loop + KEPA引擎
> 生效范围: 全部分身子Agent | 依赖: Lobster5Steps + ECCFramework + KBArchiving

---

## 一、核心理念

Learning Loop = LLM的"反向传播"。传统大模型靠梯度更新权重，Hermes靠经验反向传播优化技能与策略——不用重训模型，就能让能力持续进化。

## 二、7阶段自动闭环

| 阶段 | 动作 | 产物 | 耗时 |
|------|------|------|------|
| 1. 任务执行 | Agent通过多轮工具调用完成任务 | 执行轨迹(trajectory) | 2-5分钟 |
| 2. 模式识别 | 分析成功路径，识别可复用模式 | 候选Skill片段 | 10-20秒 |
| 3. 知识提取 | 将执行步骤抽象为通用流程 | Skill草稿 | 5-10秒 |
| 4. Skill创建 | 生成Skill文件(Markdown格式) | .hermes/skills/xxx.md | 5秒 |
| 5. 使用验证 | 下次遇到类似任务时加载Skill | 性能对比数据 | N/A |
| 6. 迭代优化 | 根据使用反馈改进Skill | Skill新版本 | 按需触发 |
| 7. Nudge提示 | 主动建议用户持久化高价值Skill | 用户确认后写入磁盘 | N/A |

## 三、KEPA引擎核心

**KEPA = Knowledge Enhanced Prompt Adaptation（知识增强提示词自适应）**

```
用户输入 → LLM推理 → 工具调用 → 返回结果
                ↓                       ↓
         检索已有Skills             任务成功?
                ↓                       ↓ YES
         如果匹配，直接复用          提取成功路径
                                        ↓
                                 生成新Skill或优化现有Skill
                                        ↓
                                   提示用户持久化
                                        ↓
                                 下次直接使用 ✓
```

## 四、实战验证基准

以GitHub代码质量分析为例：
- 第1次执行：15步，120秒
- 第2次执行（复用Skill）：3步，30秒
- 效率提升：75%

## 五、龙虾体系集成

| Hermes组件 | 龙虾对应 | 集成状态 |
|-----------|---------|---------|
| Learning Loop | Lobster5Steps (Step1→Step5闭环) | ✅ 已适配 |
| KEPA引擎 | ECCFramework (错误修正+迭代优化) | ✅ 已映射 |
| Nudge机制 | ask_user (用户确认持久化) | ✅ 已映射 |
| Skill沉淀 | KBArchiving (知识库归档) | ✅ 已映射 |
| 轨迹存储 | MemoryMgr (记忆管理) | ✅ 已映射 |

## 六、触发规则

- 任何任务执行成功后，自动触发阶段2-4（模式识别→知识提取→Skill创建）
- 用户确认后触发阶段7（Nudge持久化）
- 下次相似任务自动触发阶段5（使用验证）