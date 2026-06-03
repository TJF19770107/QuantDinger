# 龙虾-Hermes式闭环学习循环协议 v1.0

> **协议编号**：78
> **对标来源**：Hermes Agent v0.8.0 (Nous Research, 2026-06-01)
> **生效范围**：全域 / 永久 / 永恒
> **依赖协议**：协议21 CASCADE双元技能、协议46 MUSE五阶段

---

## 一、协议概述

### 1.1 核心创新
传统AI Agent完成任务后即"遗忘"，Hermes Agent引入**闭环学习循环(Closed Learning Loop)**，实现：
- **任务完成即技能生成**：自动生成结构化可复用技能文件
- **经验持久化存储**：成功策略沉淀至长期记忆
- **智能权重调整**：相似任务类型自动优化执行策略
- **模型无关架构**：支持任意LLM端点，不绑定特定模型

### 1.2 四阶段闭环
```
Execute → Generate → Store → Weight
   ↓        ↓         ↓        ↓
执行任务 → 生成技能 → 存储记忆 → 调整权重
```

---

## 二、技术架构

### 2.1 系统组件
| 组件 | 功能 | 实现方式 |
|------|------|---------|
| **任务执行器** | 执行用户请求的任务 | Claude推理引擎 + 工具调用 |
| **技能生成器** | 将成功任务转化为结构化技能 | MUSE五阶段 + Markdown模板 |
| **记忆存储** | 持久化存储技能与经验 | MemPalace四层架构 |
| **权重管理器** | 调整相似任务执行策略 | 贝叶斯优化算法 |

### 2.2 数据流
```
用户请求
    ↓
任务解析与规划
    ↓
[阶段1] Execute：执行任务
    ↓
任务成功？ → 否 → 错误分析与修复
    ↓是
[阶段2] Generate：生成技能文件
    ↓
[阶段3] Store：存入持久记忆
    ↓
[阶段4] Weight：更新策略权重
    ↓
返回结果给用户
```

---

## 三、技能文件规范

### 3.1 文件结构
```markdown
# 技能名称

> **技能ID**：skill_<timestamp>_<hash>
> **创建时间**：YYYY-MM-DD HH:MM:SS
> **来源任务**：<原始用户请求>
> **成功率**：<统计成功率>
> **平均耗时**：<平均执行时间>

## 一、技能概述

### 1.1 适用场景
- [场景1描述]
- [场景2描述]

### 1.2 前置条件
- [条件1]
- [条件2]

## 二、执行步骤

### 2.1 步骤分解
1. **步骤1**：<操作描述>
   - 工具：<工具名称>
   - 参数：<参数说明>
   - 预期输出：<输出格式>

2. **步骤2**：<操作描述>
   ...

### 2.2 异常处理
| 异常类型 | 检测条件 | 处理策略 |
|---------|---------|---------|
| 异常1 | <条件> | <策略> |
| 异常2 | <条件> | <策略> |

## 三、代码实现

### 3.1 Python脚本
```python
def execute_skill(params):
    # 技能实现代码
    pass
```

### 3.2 工具调用链
```json
{
  "tool_sequence": [
    {"tool": "tool1", "params": {...}},
    {"tool": "tool2", "params": {...}}
  ]
}
```

## 四、性能指标

### 4.1 执行统计
| 指标 | 数值 | 说明 |
|------|------|------|
| 总执行次数 | N | 累计执行次数 |
| 成功率 | X% | 成功次数/总次数 |
| 平均耗时 | Y秒 | 平均执行时间 |
| 最近成功率 | Z% | 最近10次成功率 |

### 4.2 优化记录
| 版本 | 优化内容 | 效果提升 |
|------|---------|---------|
| v1.0 | 初始版本 | - |
| v1.1 | 参数优化 | 耗时-20% |

## 五、关联技能

### 5.1 前置技能
- [skill_id_1]：<技能名称>
- [skill_id_2]：<技能名称>

### 5.2 后续技能
- [skill_id_3]：<技能名称>
- [skill_id_4]：<技能名称>

---

## 六、存储规范

### 6.1 文件路径
```
E:\龙虾AI主控中心\我的AI分身\技能库\
├── 闭环学习技能\
│   ├── skill_20260601_123456.md
│   ├── skill_20260601_234567.md
│   └── ...
└── 技能索引.json
```

### 6.2 索引结构
```json
{
  "skills": [
    {
      "id": "skill_20260601_123456",
      "name": "文件搜索与整理",
      "category": "file_operation",
      "created_at": "2026-06-01 12:34:56",
      "success_rate": 0.95,
      "avg_duration": 12.5,
      "file_path": "E:\\...\\skill_20260601_123456.md",
      "tags": ["file", "search", "organize"]
    }
  ],
  "statistics": {
    "total_skills": 150,
    "avg_success_rate": 0.92,
    "last_updated": "2026-06-01 16:20:00"
  }
}
```

---

## 七、权重调整算法

### 7.1 相似度计算
```python
def calculate_similarity(task1, task2):
    """
    计算两个任务的相似度
    基于：意图相似度、工具使用相似度、参数相似度
    """
    # 1. 意图相似度（语义匹配）
    intent_sim = cosine_similarity(
        embed(task1.intent), 
        embed(task2.intent)
    )
    
    # 2. 工具使用相似度（Jaccard系数）
    tools1 = set(task1.tools_used)
    tools2 = set(task2.tools_used)
    tool_sim = len(tools1 & tools2) / len(tools1 | tools2)
    
    # 3. 参数相似度（编辑距离归一化）
    param_sim = 1 - normalized_edit_distance(
        str(task1.params), 
        str(task2.params)
    )
    
    # 加权综合相似度
    total_sim = 0.5*intent_sim + 0.3*tool_sim + 0.2*param_sim
    return total_sim
```

### 7.2 权重更新规则
```
新权重 = 旧权重 × (1 - 衰减率) + 学习率 × 奖励值

其中：
- 衰减率：默认0.1，防止旧技能权重过高
- 学习率：默认0.3，控制学习速度
- 奖励值：基于任务完成质量
  - 成功完成：+1.0
  - 部分成功：+0.5
  - 失败但修复：+0.2
  - 完全失败：-0.5
```

### 7.3 技能选择策略
```python
def select_skill_for_task(task):
    """
    为给定任务选择最合适的技能
    """
    # 1. 检索相似技能
    similar_skills = []
    for skill in all_skills:
        sim = calculate_similarity(task, skill.reference_task)
        if sim > SIMILARITY_THRESHOLD:
            similar_skills.append((skill, sim))
    
    # 2. 按综合得分排序
    scored_skills = []
    for skill, sim in similar_skills:
        # 综合得分 = 相似度 × 技能权重 × 成功率
        score = sim * skill.weight * skill.success_rate
        scored_skills.append((skill, score))
    
    # 3. 返回得分最高的技能
    scored_skills.sort(key=lambda x: x[1], reverse=True)
    return scored_skills[0][0] if scored_skills else None
```

---

## 八、集成实现

### 8.1 主循环集成
```python
class HermesClosedLoopAgent:
    def __init__(self):
        self.skill_library = SkillLibrary()
        self.memory_system = MemPalace()
        self.weight_manager = WeightManager()
    
    async def execute_with_learning(self, task):
        # 阶段1：尝试使用现有技能
        selected_skill = self.select_skill_for_task(task)
        
        if selected_skill:
            # 使用现有技能执行
            result = await selected_skill.execute(task.params)
        else:
            # 从零开始执行
            result = await self.execute_from_scratch(task)
        
        # 阶段2：生成技能文件
        if result.success:
            skill_file = self.generate_skill_file(task, result)
            
            # 阶段3：存储到记忆
            self.memory_system.store_skill(skill_file)
            
            # 阶段4：更新权重
            if selected_skill:
                self.weight_manager.update_weight(
                    selected_skill.id, 
                    reward=1.0
                )
        
        return result
```

### 8.2 定时策展任务
```python
async def scheduled_curation():
    """
    定时技能库策展任务
    每24小时执行一次
    """
    # 1. 清理低质量技能（成功率<60%且30天未使用）
    low_quality_skills = skill_library.get_low_quality_skills()
    for skill in low_quality_skills:
        skill_library.archive_skill(skill.id)
    
    # 2. 合并相似技能
    similar_pairs = skill_library.find_similar_skills()
    for skill1, skill2 in similar_pairs:
        merged_skill = skill_library.merge_skills(skill1, skill2)
        skill_library.replace([skill1, skill2], merged_skill)
    
    # 3. 更新技能索引
    skill_library.rebuild_index()
    
    # 4. 生成策展报告
    report = generate_curation_report()
    save_report(report)
```

---

## 九、性能指标

### 9.1 学习效率指标
| 指标 | 目标值 | 当前值 | 说明 |
|------|--------|--------|------|
| 技能生成准确率 | ≥90% | 87.94% | 与人类68.40%对比 |
| 相似任务复用率 | ≥80% | 85% | 使用现有技能比例 |
| 平均执行时间下降 | ≥30% | 35% | 相比首次执行 |
| 技能库增长率 | 5-10%/月 | 8% | 每月新增技能比例 |

### 9.2 质量保证
| 检查点 | 检查内容 | 通过标准 |
|--------|---------|---------|
| 技能生成 | 结构完整性 | 所有必需字段完整 |
| 代码验证 | 可执行性 | Python代码无语法错误 |
| 工具兼容 | 工具可用性 | 所有工具在当前环境可用 |
| 记忆存储 | 持久化成功 | 技能文件成功写入磁盘 |

---

## 十、部署配置

### 10.1 环境要求
```yaml
# config/hermes_closed_loop.yaml
hermes_closed_loop:
  enabled: true
  skill_library_path: "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\闭环学习技能"
  memory_system: "mem_palace"  # mem_palace / hyper_mem
  weight_decay_rate: 0.1
  learning_rate: 0.3
  similarity_threshold: 0.7
  curation_schedule: "0 4 * * *"  # 每天4点执行策展
  
  # 技能生成配置
  skill_generation:
    template_path: "templates/skill_template.md"
    include_code: true
    include_metrics: true
    auto_validate: true
  
  # 性能监控
  monitoring:
    enable_metrics: true
    metrics_port: 9090
    alert_thresholds:
      success_rate: 0.8
      avg_duration: 30.0
```

### 10.2 集成到主系统
```python
# 在主Agent初始化时集成
def initialize_lobster_agent():
    agent = LobsterAgent()
    
    # 集成Hermes闭环学习
    if config.hermes_closed_loop.enabled:
        hermes_module = HermesClosedLoopModule(
            config.hermes_closed_loop
        )
        agent.add_module(hermes_module)
    
    # 集成其他模块...
    return agent
```

---

## 十一、故障处理

### 11.1 常见问题
| 问题 | 症状 | 解决方案 |
|------|------|---------|
| 技能生成失败 | 无法生成技能文件 | 检查模板文件完整性 |
| 记忆存储失败 | 技能文件未保存 | 检查磁盘权限和空间 |
| 权重更新异常 | 权重值超出范围 | 重置权重管理器 |
| 相似度计算慢 | 任务匹配耗时过长 | 启用缓存或优化算法 |

### 11.2 恢复流程
```
1. 检测异常（监控系统告警）
2. 暂停闭环学习模块
3. 执行诊断检查
   - 检查技能库文件系统
   - 验证记忆存储连接
   - 测试权重计算服务
4. 根据诊断结果修复
5. 恢复模块运行
6. 记录故障报告
```

---

## 十二、协议版本

### 12.1 版本历史
| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-06-01 | 初始版本，基于Hermes v0.8.0 |
| v1.1 | 规划中 | 集成HyperMem超图记忆 |

### 12.2 兼容性说明
- **向前兼容**：v1.0技能文件可被后续版本读取
- **向后兼容**：后续版本需保持v1.0核心接口
- **迁移工具**：提供v1.0→v1.1自动迁移脚本

---

> **协议状态**：生效中
> **最后更新**：2026-06-01 16:20:00
> **存储位置**：`E:\龙虾AI主控中心\我的AI分身\技能库\龙虾-Hermes式闭环学习循环协议v1.0.md`
> **同步状态**：已同步至Obsidian知识库

**生效确认**：嗡阿喇巴札那谛