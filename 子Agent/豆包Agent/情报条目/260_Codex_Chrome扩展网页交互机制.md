# 情报条目 #260：Codex Chrome扩展网页交互机制

> **来源**：Working-Ref - "Chrome 成了 Codex 的双手" + AgentUpdate.ai
> **采集时间**：2026-06-01 17:15
> **相关协议**：协议84 浏览器Agent交互协议 v1.0
> **关键词**：Codex、Chrome Extension、Browser Agent、SaaS自动化、Cookie共享
> **状态**：已分析 → 已集成

---

## 一、核心发现

### 1.1 产品发布背景

| 时间线 | 事件 |
|--------|------|
| 2026年初 | Codex周活跃用户突破400万（增长8倍） |
| 2026-05-07 | Codex Chrome扩展正式发布 |
| 当前 | 内置浏览器用于公开页面，Chrome扩展用于认证页面 |

### 1.2 核心价值定位

> **"保留登录状态 → Chrome 成为 Codex 的双手 → 真正的 SaaS 自动化"**

Codex Chrome扩展让AI Agent直接在用户已登录的Chrome配置文件中运行，利用现有会话、Cookie和认证状态，无需重新登录。

---

## 二、技术架构对比

### 2.1 内置浏览器 vs Chrome扩展

| 功能 | 内置浏览器 | Chrome扩展 | 差异价值 |
|------|-----------|-----------|---------|
| 登录会话 | 无（仅限公开页面） | 直接使用Chrome配置文件 | **质变：可操作已登录SaaS** |
| 可访问网站 | 公开URL、localhost | LinkedIn、Salesforce、Gmail、内部工具 | **扩大10倍可用面** |
| 标签页管理 | 单一内置窗口 | 后台多标签页并行运行 | **并行能力** |
| DevTools访问 | 不可用 | 可用（调试、DOM操作） | **调试能力** |
| 文件上传 | 不可用 | 设置后可用 | **完整工作流** |
| 主要用途 | 本地开发服务器测试 | 真实SaaS工作流自动化 | **生产级应用** |

### 2.2 智能切换策略

Codex会根据需要自动切换两种浏览器模式：
1. **原型验证** → 内置浏览器（轻量、快速）
2. **真实认证环境** → Chrome扩展（完整功能）
3. **认证后操作** → 切换回内置浏览器（高效）

---

## 三、关键实现机制

### 3.1 Cookie与认证状态共享

```javascript
// Codex Chrome扩展核心：直接继承用户已登录状态
class CodexSessionManager {
    async acquireSession(domain) {
        // 1. 直接读取Chrome Cookie（已登录状态）
        const cookies = await chrome.cookies.getAll({domain});
        
        // 2. 读取本地存储/LocalStorage（应用状态）
        const appState = await this.readLocalStorage(domain);
        
        // 3. 构建完整会话上下文
        return {
            cookies: cookies,
            tokens: appState.authTokens,
            userProfile: appState.userData,
            lastActive: Date.now()
        };
    }
    
    // 无需重新登录！Cookie直接可用
    async operateAsUser(targetSite, action) {
        const session = await this.acquireSession(targetSite);
        // 直接操作，跳过登录步骤
        return this.executeAction(targetSite, action, session);
    }
}
```

### 3.2 典型使用场景

#### 场景1：Salesforce自动化

```
用户：帮我更新Salesforce中所有到期日期在下周的商机

Codex操作流程：
1. Chrome扩展 → 打开已登录的Salesforce
2. 导航到商机列表页
3. 筛选到期日期
4. 批量更新（无需重新输入密码）
5. 生成更新报告

价值：跳过每次手动登录Salesforce的繁琐过程
```

#### 场景2：Gmail整理

```
用户：帮我整理Gmail中未读邮件，分类为"需要回复"和"仅确认"

Codex操作流程：
1. Chrome扩展 → 打开已登录的Gmail
2. 过滤未读邮件
3. 按内容语义分类
4. 打标签、归档
5. 生成摘要

价值：无需API权限，直接用已登录的浏览器操作
```

#### 场景3：LinkedIn信息收集

```
用户：帮我收集所有LinkedIn联系人的最新职位变动

Codex操作流程：
1. Chrome扩展 → 打开LinkedIn（已登录）
2. 遍历联系人列表
3. 检查每个联系人的职位变动
4. 汇总成表格

价值：LinkedIn API已关闭，这是唯一可行的自动化方式
```

---

## 四、Chrome扩展架构

### 4.1 扩展结构

```
codex-chrome-extension/
├── manifest.json          # 扩展清单
├── background.js           # 后台服务工作线程
├── content-script.js       # 注入所有页面的内容脚本
├── popup.html             # 扩展弹窗UI
├── bridge/
│   ├── ipc.js             # 与Codex桌面应用的IPC通信
│   └── message-router.js  # 消息路由
├── capabilities/
│   ├── navigation.js      # 页面导航
│   ├── click.js           # 点击操作
│   ├── fill.js            # 表单填写
│   ├── extract.js         # 数据提取
│   └── upload.js          # 文件上传
└── permissions/
    └── domains.js          # 用户授权域名列表
```

### 4.2 权限模型

| 权限类型 | 描述 | 用户控制 |
|---------|------|---------|
| **activeTab** | 当前标签页操作 | 即时授权 |
| **cookies** | 读取所有Cookie | 安装时确认 |
| **scripting** | 注入脚本执行 | 运行时确认 |
| **tabs** | 标签页管理 | 后台运行 |
| **webNavigation** | 导航事件监听 | 后台运行 |

---

## 五、对豆包Agent的借鉴价值

### 5.1 可直接借鉴的设计

| 设计点 | Codex实现 | 豆包Agent方案 | 价值 |
|--------|----------|-------------|------|
| **Cookie直接复用** | chrome.cookies API | CDP Network.getCookies | 跳过登录 |
| **LocalStorage读取** | content-script注入 | CDP Runtime.evaluate | 获取应用状态 |
| **标签页并行管理** | chrome.tabs API | CDP Target管理 | 并行操作 |
| **IPC通信** | Native Messaging | stdio管道 | 扩展与AI进程通信 |

### 5.2 Codex的优势vs豆包Agent需追赶

| 维度 | Codex | 豆包Agent（当前） | 差距 |
|------|-------|-----------------|------|
| 登录状态复用 | ✅ 原生支持 | ❌ 需每次登录 | 大 |
| SaaS操作覆盖 | ✅ Salesforce/Gmail/LinkedIn | ❌ 未覆盖 | 大 |
| 后台标签页操作 | ✅ 支持 | ❌ 未实现 | 中 |
| 文件上传 | ✅ 支持 | ❌ 未实现 | 中 |
| DevTools集成 | ✅ 可用 | ❌ 未实现 | 小 |

---

## 六、协议84集成要点

### 6.1 关键设计决策

```
协议84 v1.0 需同时借鉴两个标杆：
├── Marvis Browser Agent（操作系统级深度集成）
│   └── CDP WebSocket连接，持久化会话
└── Codex Chrome扩展（应用级扩展）
    └── Cookie/LocalStorage直接复用

建议方案：CDP连接 + Profile管理 双模式
- 简单场景：Chrome扩展模式（快速、轻量）
- 复杂场景：CDP深度控制模式（权限高、灵活）
```

### 6.2 快速落地路径

R26 → 实现CDP基础连接（对标Marvis）
R27 → 实现Cookie复用（对标Codex）
R28 → 实现文件上传+多标签页（对标Codex）
R29 → 实现SaaS自动化测试（对标Codex）

---

## 七、代码示例：Cookie复用

```python
# 豆包Agent协议84实现：直接复用已登录Cookie
import asyncio
import json
from websockets import connect

class CookieAwareBrowserAgent:
    def __init__(self, chrome_debug_port=9222):
        self.debug_port = chrome_debug_port
        
    async def connect_with_cookies(self, domain: str):
        """连接Chrome并复用已登录的Cookie"""
        # 1. 连接CDP
        ws_url = f"ws://localhost:{self.debug_port}/devtools/page/1"
        async with connect(ws_url) as ws:
            # 2. 获取目标域名的Cookie（直接复用已登录！）
            await self.send_cmd(ws, "Network.getCookies", {
                "urls": [f"https://{domain}/*"]
            })
            cookies_resp = await ws.recv()
            cookies = json.loads(cookies_resp)['result']['cookies']
            
            # 3. 导航到页面（自动使用已有Cookie）
            await self.send_cmd(ws, "Page.navigate", {
                "url": f"https://{domain}"
            })
            
            # 4. 已登录状态，直接操作
            print(f"✅ 复用 {domain} 的 {len(cookies)} 个Cookie")
            print("✅ 无需重新登录，直接操作！")
```

---

> **分析完成时间**：2026-06-01 17:25  
> **分析师**：龙虾AI主控中心  
> **已集成到**：协议84 v1.0  
> **关键价值**：Cookie/LocalStorage直接复用机制是最大突破点