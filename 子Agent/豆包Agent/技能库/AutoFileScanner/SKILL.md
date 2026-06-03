# AutoFileScanner - 本地文件自主读取引擎
> 版本：v1.0  
> 自动生成：2026-05-31 R05  
> 来源：豆包Agent 6大自主能力补全  
> 对标：Marvis File Agent + OpenClaw Skills

## 触发条件
- **自动触发**：Agent启动时自动运行
- **事件触发**：豆包Agent目录下文件变化时（watchdog）
- **手动触发**：用户说"扫描文件"、"加载技能"、"读取目录"、"看看有什么"

## 能力描述
自动扫描 E:\龙虾AI主控中心\我的AI分身\子Agent\豆包Agent\ 下所有文件，构建索引，智能分类，提取可用能力标签并自动注册。

## 执行流程

### Phase 1: 目录树构建
1. 递归扫描根目录
2. 过滤非关键文件（.git/__pycache__/temp）
3. 构建完整文件树JSON（路径/大小/修改时间/类型）
4. 存储到 index.json

### Phase 2: 智能分类
- 路径含"架构" → architecture
- 路径含"迭代" → iteration  
- 路径含"能力" → capability
- 路径含"memory" → memory
- 路径含"技能" → skill

### Phase 3: 内容解析
- .md文件 → 提取标题层级、关键词、表格数据
- .json文件 → 解析结构化数据
- .txt文件 → 全文索引

### Phase 4: 能力自注册
- 从文件中提取"可用能力"标签
- 生成 capabilities.json
- 更新 Agent 能力清单

### Phase 5: 增量更新
- watchdog监控目录变化
- 新文件自动触发Phase 1→4
- 被删文件自动从索引移除

## 输出格式
```json
{
  "scan_time": "2026-05-31T03:00:00",
  "total_files": 25,
  "categories": {
    "architecture": 5,
    "iteration": 8,
    "capability": 3,
    "memory": 4,
    "skill": 5
  },
  "capabilities_registered": [
    "自进化引擎", "端云路由", "专家门徒", 
    "AutoFileScanner", "SkillForge", "MemoryOS"
  ]
}
```

## 安全审查
- 风险等级：SAFE
- 仅读取操作，不修改任何文件
- 不访问系统敏感路径

## 演化记录
- v1.0: 初始创建，基于R05迭代设计
