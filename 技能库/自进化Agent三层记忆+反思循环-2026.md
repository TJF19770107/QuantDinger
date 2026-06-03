# 技能：自进化Agent三层记忆+反思循环
> 提取自：第1轮豆包Agent迭代 | 来源：MUSE / Hermes Agent / EverOS / Autogenesis Protocol
> 版本：v1.0 | 日期：2026-05-31

## 自进化闭环

```
规划(Plan) → 执行(Execute) → 反思(Reflect) → 提取经验(Extract)
    ↑                                              ↓
    └────────── 经验注入优化下次规划 ←──────────────┘
```

## 三层记忆系统

| 层级 | 名称 | 存储 | 生命周期 | 用途 |
|------|------|------|---------|------|
| L1 | 工作记忆 | JSON状态 | 会话级 | 当前目标、子任务列表、工具返回 |
| L2 | 情景记忆 | SQLite FTS5 | 项目级 | 任务轨迹、决策记录、踩坑日志 |
| L3 | 技能记忆 | Markdown文件 | 永久级 | SOP、模板、工具链、判断器 |

## 反思机制（对标MUSE）

1. 子任务完成后自动触发反思回合
2. 评估成功/失败 → 结构化经验提取
3. 失败任务获得"第二次机会"（无检索探索模式）
4. 成功轨迹 → SOP标准作业程序（变量模板参数化）

## GEPA进化算法（对标Hermes Agent）

- 类反向传播迭代提示词
- 训练效率比GRPO高35倍
- 全程API调用，无需GPU
- PR提交 + 人工审查合并

## 来源
- [MUSE框架](https://www.aiexpress.news/17899.html)
- [Hermes Agent](https://bytesort.blog.csdn.net/article/details/161058490)
- [EverOS](https://www.solosoft.dev/zh-tw/post/everos-agent-memory-2026)
- [Autogenesis Protocol](https://arxiv.org/abs/2604.15034)
- [SkillOS范式](https://www.53ai.com/news/tishicijiqiao/2026051116870.html)
