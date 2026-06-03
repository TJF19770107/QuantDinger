# 龙虾-SetOfMark视觉定位桌面操控协议 v1.0

> **协议编号**：63
> **对标来源**：Computer Use API 2026 + Set-of-Mark Prompting + Windows UI Automation
> **创建日期**：2026-06-01
> **适用Agent**：豆包Agent / DesktopController v3.0
> **依赖**：DesktopController v2.0+ / Windows UIA API

---

## 一、协议概述

本协议为桌面操控引入Set-of-Mark（SoM）视觉定位能力，将传统坐标定位升级为语义定位。结合Windows UIA（结构化数据）和视觉模型（像素级理解），实现"UIA优先、Vision兜底"的混合桌面操控架构。

## 二、混合操控架构

### 2.1 双通道决策树

```
用户意图 → 目标元素定位
              │
    ┌─────────┴─────────┐
    ▼                   ▼
UIA通道（优先）      Vision通道（兜底）
- 查询UI Automation    - 截取屏幕
  Tree                - SoM标注（编号框）
- 获取元素坐标/        - 视觉模型识别
  属性                - 语义定位目标
- 精确点击/输入        - 坐标点击/输入
    │                   │
    └─────────┬─────────┘
              ▼
        动作执行 + 验证
```

### 2.2 通道选择逻辑

| 场景 | 通道 | 说明 |
|------|------|------|
| 标准Windows应用 | UIA | Excel/Word/设置等 |
| Web浏览器 | CDP优先 | Chrome DevTools Protocol |
| 自定义/遗留应用 | Vision | 无UIA暴露的应用 |
| UIA失败 | Vision兜底 | 自动降级 |

## 三、Set-of-Mark视觉定位

### 3.1 SoM流程

1. **截图**：捕获当前屏幕/窗口
2. **元素检测**：使用视觉模型或UIA检测所有可交互元素
3. **编号标注**：在每个交互元素上绘制编号框（1, 2, 3, ...）
4. **视觉推理**：将标注后的图像发送给视觉模型
5. **语义定位**：模型返回"点击编号X"而非"点击(500,600)"

### 3.2 SoM优势

- **分辨率无关**：不依赖像素坐标，跨分辨率稳定
- **语义理解**：模型理解元素含义（"提交按钮"而非"第3个按钮"）
- **动态UI适应**：UI布局变化不影响定位

### 3.3 实施格式

```
输入：截图 + SoM标注图 + 任务描述
输出：{ "action": "click", "target": "box_4", "confidence": 0.95 }
```

## 四、Sandboxed Execution安全隔离

### 4.1 隔离级别

| 级别 | 场景 | 机制 |
|------|------|------|
| Level 1 | 文件操作 | 工作目录限定 |
| Level 2 | 应用操作 | Windows Sandbox |
| Level 3 | 系统操作 | Hyper-V隔离 |

### 4.2 Human-in-the-Loop触发条件

- 涉及密码/支付输入 → 暂停，等待用户手动输入
- 涉及系统设置修改 → 确认后执行
- 涉及删除操作 → 审核后执行

## 五、跨应用状态记忆

### 5.1 Session持久化

- Web登录态：保存Cookie/Token到加密存储
- 应用状态：保存窗口位置、最近打开文件列表
- 下次任务自动恢复，无需重复登录/导航

### 5.2 记忆格式

```json
{
  "app": "Chrome",
  "context": "Jira Dashboard",
  "state": {
    "url": "https://jira.company.com",
    "auth_token_encrypted": "...",
    "last_view": "Backlog"
  },
  "timestamp": "2026-06-01T12:00:00Z"
}
```

## 六、实施路径

| 阶段 | 内容 | 优先级 |
|------|------|--------|
| Phase 1 | SoM视觉标注引擎 + UIA/Vision混合路由 | P0 |
| Phase 2 | Sandboxed Execution集成 | P0 |
| Phase 3 | 跨应用状态记忆 + Session恢复 | P1 |
| Phase 4 | 远程桌面接管（移动端控制PC） | P2 |

---

> **版本**：v1.0
> **状态**：ACTIVE
> **关联文件**：desktop-controller-v2.0.md, 龙虾-EvoCUA进化式桌面操控协议v1.0.md, 龙虾-Windows桌面视觉操控协议v1.0.md
