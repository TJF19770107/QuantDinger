---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 58152cf0aacf686f4558d7a7c43bec24_48c350a361a611f18f065254007bceed
    ReservedCode1: oasTN1tvsB8EGCh/giHLH2z+ecl1FYqciM44+vfkZtX2NOvyJteO9+OXW+CtGTyjo+Qpa6zOXZRSkltr+g+pRz7h002XpnKZecCufRXvl1vtJDwMeQAkwGxiiZDohuPFqy9O/ugTen0lYD7L/L7JH9KRjsMpEJlaacDmuNq7rRJY5KMB4NmDebgmL7E=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 58152cf0aacf686f4558d7a7c43bec24_48c350a361a611f18f065254007bceed
    ReservedCode2: oasTN1tvsB8EGCh/giHLH2z+ecl1FYqciM44+vfkZtX2NOvyJteO9+OXW+CtGTyjo+Qpa6zOXZRSkltr+g+pRz7h002XpnKZecCufRXvl1vtJDwMeQAkwGxiiZDohuPFqy9O/ugTen0lYD7L/L7JH9KRjsMpEJlaacDmuNq7rRJY5KMB4NmDebgmL7E=
---

- **$Schema**: https://json-schema.org/draft/2020-12/schema
- **Name**: ai_avatar_distillation
- **Version**: 1.0.0
- **Description**: 执行AI分身全自动蒸馏流程，通过六步法（分析自己→制定计划→文件转换→构建知识库→创建self-skill→更新核心配置）实现AI分身从原始数据到完整数字延伸的闭环转化
- **Type**: mcp_tool

# Input

## Schema
- **Type**: object

### Properties

#### Trigger Type
- **Type**: string

##### Enum
- scheduled
- manual
- iteration
- anomaly
- **Default**: scheduled
- **Description**: scheduled=定时触发（每2小时）| manual=手动触发（用户发送蒸馏关键词）| iteration=迭代后触发（R23+迭代完成校验后）| anomaly=异常触发（配置漂移检测）

#### Base Directory
- **Type**: string
- **Default**: E:\龙虾AI主控中心\我的AI分身
- **Description**: AI分身根目录路径

#### Step Filter
- **Type**: array

##### Items
- **Type**: integer
- **Minimum**: 1
- **Maximum**: 6

##### Default
- 1
- 2
- 3
- 4
- 5
- 6
- **Description**: 要执行的步骤编号列表，默认全执行。例如 [3, 4] 仅执行文件转换和构建知识库

#### Dry Run
- **Type**: boolean
- **Default**: False
- **Description**: 是否为试运行模式，true 时仅做路径校验和可行性检查，不实际写入

### Required


# Output

## Schema
- **Type**: object

### Properties

#### Status
- **Type**: string

##### Enum
- success
- partial
- failed
- **Description**: 全局执行状态

#### Report Path
- **Type**: string
- **Description**: 蒸馏报告的完整路径，例如 E:\龙虾AI主控中心\我的AI分身\定时任务\蒸馏日志\蒸馏报告_20260601.md

#### Step Results
- **Type**: array

##### Items
- **Type**: object

###### Properties

###### Step
- **Type**: integer
- **Description**: 步骤编号 1-6

###### Step Name
- **Type**: string
- **Description**: 步骤名称

###### Status
- **Type**: string

###### Enum
- success
- failed
- skipped
- **Description**: 该步骤执行状态

###### Products
- **Type**: array

###### Items
- **Type**: string
- **Description**: 该步骤产出文件的完整路径列表

###### Duration Seconds
- **Type**: number
- **Description**: 该步骤执行耗时（秒）

###### Error
- **Type**: string
- **Description**: 失败原因（仅 status=failed 时有值）

###### Required
- step
- step_name
- status
- **Description**: 各步骤的详细执行结果

#### Products
- **Type**: array

##### Items
- **Type**: string
- **Description**: 全部产出物文件路径的汇总列表

#### Quality Gates
- **Type**: object

##### Properties

###### G1 Factuality
- **Type**: string

###### Enum
- PASS
- FAIL

###### G2 Dedup
- **Type**: string

###### Enum
- PASS
- FAIL

###### G3 Path Compliance
- **Type**: string

###### Enum
- PASS
- FAIL

###### G4 Benchmark
- **Type**: string

###### Enum
- PASS
- FAIL
- N/A

###### G5 Consistency
- **Type**: string

###### Enum
- PASS
- FAIL
- N/A
- **Description**: 五道质量门控通过状态

#### Started At
- **Type**: string
- **Format**: date-time
- **Description**: 执行开始时间 (ISO 8601)

#### Completed At
- **Type**: string
- **Format**: date-time
- **Description**: 执行完成时间 (ISO 8601)

### Required
- status
- report_path
- started_at

# Metadata
- **Author**: 龙虾AI主控中心
- **License**: Internal Use Only

## Tags
- distillation
- avatar
- automation
- knowledge-base
- self-skill
- **Category**: 定时任务

## Concurrency
- **Max Instances**: 1
- **Description**: 单实例运行，禁止并发。多次触发自动排队
- **Timeout Seconds**: 1800
- **Description**: 单次蒸馏最长 30 分钟，超时自动终止并报告

# Agent Routing

## Doubao Agent
- **Role**: 分析/索引 Agent

### Assigned Steps
- 1
- 4
- 5

### Capabilities
- 人格画像分析
- 知识库索引构建
- 技能协议设计

### Permissions

#### Read
- 角色总说明书/
- 知识库/
- 记忆库/
- 技能库/

#### Write
- 知识库/
- 技能库/

#### Execute
- python_executor

## Hermes Agent
- **Role**: 调度/校验/规划 Agent

### Assigned Steps
- 2
- 6

### Capabilities
- 进化规划
- 全局一致性校验
- 全流程调度
- 回滚控制

### Permissions

#### Read
- 所有目录

#### Write
- 知识库/
- 子Agent/
- 角色总说明书/

#### Execute
- shell_executor

## Openclaw Agent
- **Role**: 执行/归档 Agent

### Assigned Steps
- 3
- 5

### Capabilities
- 文件批量转换
- MD5去重
- 产物归档
- 格式转换脚本

### Permissions

#### Read
- 所有目录

#### Write
- 定时任务/蒸馏日志/
- 知识库/
- 技能库/

#### Execute
- python_executor
- shell_executor
*（内容由AI生成，仅供参考）*
