# 龙虾AI分身 · Self-Skill 专属技能包 v2.4（R33蒸馏）

**版本**：v2.4 | **生成日期**：2026-06-02 01:52  
**基础配置**：SOUL v2.3(R33) / USER v2.1(R33) / AGENTS v2.1(R33)  
**对齐标准**：agent-skills 7强制命令 + Google 47.3K⭐标准  
**输出目录**：技能库 / 子Agent / MCP配置  

---

## 一、新增专属技能协议（#91-#95）

### #91 三层自进化统计合并技能
```yaml
name: lobster-evolution-stats
description: 三层自进化统计合并，L1实时反思+L2延迟统计+L3定期合并→统一进化报告
version: 1.0
type: skill
agent: 豆包Agent
trigger: 每2小时蒸馏任务
lifecycle: ACTIVE
dependencies:
  - SOUL.md v2.3 (三层自进化原则)
  - Curator馆长引擎配置
actions:
  - 读取L1脏计数日志
  - 读取L2边车统计数据
  - 触发L3 Curator合并（如≥7天）
  - 生成三层统计报告
output: 定时任务/蒸馏日志/三层进化统计_R{轮次}_{日期}.md
```

### #92 SkillOS五态管理技能
```yaml
name: lobster-skillos-manager
description: SkillOS五态生命周期管理：NEW→ACTIVE→DORMANT→ARCHIVED→REVIVE
version: 1.0
type: skill
agent: 豆包Agent
trigger: 技能策展任务 / Curator馆长评估
lifecycle: ACTIVE
dependencies:
  - AGENTS.md v2.1 (SkillOS配置)
  - Curator馆长引擎
actions:
  - 扫描技能库所有协议
  - 评估五态（Rubric评分+使用频率+覆盖度）
  - 执行状态转换（DORMANT→ARCHIVED / REVIVE→ACTIVE）
  - 伞状合并触发（同场景≥3碎片技能）
  - 跨Agent交叉授粉标记
output: 技能库/SkillOS五态登记表_{日期}.md
```

### #93 影子Agent安全复盘技能
```yaml
name: lobster-shadow-audit
description: 影子Agent六层隔离安全复盘：不阻塞主Agent，异步审计
version: 1.0
type: skill
agent: Hermes Agent
trigger: 脏计数≥8 / 每24小时
lifecycle: ACTIVE
dependencies:
  - AGENTS.md v2.1 (影子Agent安全配置)
  - SOUL.md v2.3 (六层舱壁隔离)
isolation:
  - permission: 最小只读权限
  - data: 仅注入摘要，非原始数据
  - network: 全部阻断外网
  - file: 仅读写技能库
  - process: fork独立子进程，120s超时
  - audit: 独立日志文件，90天滚动归档
actions:
  - 回放主Agent执行轨迹
  - 提取重复失败模式
  - 生成改进建议
  - 写入审计日志
output: 子Agent/豆包Agent/审计日志/shadow_audit_{日期}.json
```

### #94 Goal模式持久化执行技能（#88正式化升级）
```yaml
name: lobster-goal-persistence
description: Goal模式持久化执行：心跳保持+断点续跑+完成确认
version: 2.0
type: skill
agent: 全Agent通用
trigger: 预估执行>10min 或 20+文件操作
lifecycle: ACTIVE
dependencies:
  - SOUL.md v2.3 (持久化执行原则9.7)
  - AGENTS.md v2.1 (Goal模式配置)
protocol: "#88正式化"
config:
  heartbeat_interval: 15s
  heartbeat_timeout: 30s
  checkpoint_on_steps: true
  stall_timeout: 300s
  max_retry_per_step: 3
actions:
  - 状态锁初始化
  - 每步骤后序列化检查点
  - 每15s发送心跳信号
  - 僵死检测→唤醒→断点续跑
  - IO验证确认完成
output: 定时任务/蒸馏日志/_goal_checkpoint.json
```

### #95 全分身版本一致性校验技能
```yaml
name: lobster-version-sync
description: 三Agent（豆包+Hermes+OpenClaw）版本一致性MD5校验+同步
version: 1.0
type: skill
agent: 豆包Agent
trigger: 每12小时
lifecycle: ACTIVE
dependencies:
  - SOUL.md v2.3 (统一路径原则)
  - USER.md v2.1 (全分身同步流程)
actions:
  - 读取豆包/Hermes/OpenClaw三端核心配置MD5
  - 比对SOUL.md / USER.md / AGENTS.md一致性
  - 标记不一致项
  - 触发同步修复
  - 生成一致性报告
output: 定时任务/蒸馏日志/版本一致性报告_{日期}.md
```

---

## 二、MCP配置更新

### 2.1 新增 MCP Server
```json
{
  "mcpServers": {
    "lobster-curator": {
      "command": "python",
      "args": ["E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent\\curator_engine.py"],
      "env": {
        "SKILL_LIB_PATH": "E:\\龙虾AI主控中心\\我的AI分身\\技能库",
        "AUDIT_LOG_PATH": "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent\\审计日志"
      },
      "description": "Curator馆长引擎MCP：技能评分合并清理"
    },
    "lobster-shadow": {
      "command": "python",
      "args": ["E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\HermesAgent\\shadow_agent.py"],
      "env": {
        "ISOLATION_LEVEL": "maximum",
        "MAX_RUNTIME": "120",
        "AUDIT_RETENTION": "90"
      },
      "description": "影子Agent MCP：安全复盘审计"
    },
    "lobster-evolution": {
      "command": "python",
      "args": ["E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent\\evolution_stats.py"],
      "env": {
        "L1_LOG_PATH": "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent\\进化统计\\L1",
        "L2_LOG_PATH": "E:\\龙虾AI主控中心\\我的AI分身\\子Agent\\豆包Agent\\进化统计\\L2"
      },
      "description": "三层自进化统计MCP：L1+L2+L3合并"
    }
  }
}
```

### 2.2 现有MCP配置更新
| Server | 变更 | 说明 |
|--------|------|------|
| filesystem-mcp | 限定目录扩展 | 允许读取审计日志路径 |
| github-mcp | 无变更 | 保持现有权限 |

---

## 三、Agent能力升级清单

### 3.1 豆包Agent（v10.3_R26 → v10.4_R33）
| 能力 | 变更 | 状态 |
|------|------|:---:|
| 三层自进化统计 | 新增 #91 | ACTIVE |
| SkillOS五态管理 | 新增 #92 | ACTIVE |
| Goal模式持久化 | #88 候选→正式 | ACTIVE |
| 全分身一致性 | 新增 #95 | ACTIVE |
| Curator馆长 | 配置激活 | ACTIVE |

### 3.2 Hermes Agent（v3.8_R26 → v3.9_R33）
| 能力 | 变更 | 状态 |
|------|------|:---:|
| 影子Agent审计 | 新增 #93 | ACTIVE |
| Goal模式心跳监控 | 升级心跳检测 | ACTIVE |
| 五层防烂尾 | 维持 #88 | ACTIVE |

### 3.3 OpenClaw龙虾Agent（v3.8_R26 → v3.9_R33）
| 能力 | 变更 | 状态 |
|------|------|:---:|
| 安全审计日志 | 新增日志归档 | ACTIVE |
| 插件管理 | 维持现有 | STABLE |

---

## 四、技能协议完整清单（R33更新）

| 编号 | 名称 | 状态 | 变更 |
|:---:|------|:---:|------|
| #83 | AI分身蒸馏专家 | ACTIVE | 维持 |
| #84 | GitHub Skills生态标准化 | ACTIVE | 维持 |
| #85 | Agentic AI硬件适配 | ACTIVE | 维持 |
| #86 | 企业级MCP安全隧道 | ACTIVE | 维持 |
| #87 | 多平台Agent协同 | ACTIVE | 维持 |
| #88 | Goal模式Agent持久化执行 | ACTIVE | **正式化** |
| #89 | Dynamic Workflows多Agent并行 | CANDIDATE | 候选 |
| #90 | AI视频创作商业闭环分析 | ACTIVE | **正式化** |
| #91 | 三层自进化统计合并 | ACTIVE | **新增** |
| #92 | SkillOS五态管理 | ACTIVE | **新增** |
| #93 | 影子Agent安全复盘 | ACTIVE | **新增** |
| #94 | Goal模式持久化执行v2 | ACTIVE | **升级** |
| #95 | 全分身版本一致性校验 | ACTIVE | **新增** |

**总计**：87项 → **92项**（新增5项：#91-#95，#94为#88升级版）

---

*自动蒸馏 · 第⑤步完成 | Self-Skill v2.4 | 2026-06-02 01:52*
