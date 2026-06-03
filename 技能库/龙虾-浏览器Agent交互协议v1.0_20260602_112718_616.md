# 龙虾-浏览器Agent交互协议 v1.0

> **协议编号**：#84
> **版本**：v1.0
> **创建日期**：2026-06-02
> **对标来源**：Marvis Browser Agent + Codex Chrome扩展 + OpenClaw Gateway Web + Claude Dynamic Workflows
> **核心定位**：填补豆包Agent浏览器搜索能力最大短板（82分→85+），实现通用网页检索、账号登录、验证码识别、多页表单提交、动态内容抓取、复杂站点交互六大核心能力

---

## 一、协议定位

### 1.1 问题诊断

根据R25对标评估报告，浏览器搜索能力是豆包Agent**最大短板**（82分，-18%）：

| 子维度 | 豆包Agent | Marvis | Claude | 差距 |
|--------|----------|--------|--------|------|
| 网页交互 | 70 | 90 | 85 | -20 |
| 动态内容抓取 | 80 | 85 | 88 | -8 |
| 多源整合 | 82 | 85 | 90 | -8 |
| 信息检索 | 85 | 88 | 92 | -7 |

**核心瓶颈**：缺少真实浏览器接管能力——无法处理登录/验证码/多页表单/动态内容抓取等需要浏览器交互的深度搜索任务。

### 1.2 对标分析

| 对标Agent | 浏览器能力 | 可借鉴要点 |
|-----------|----------|-----------|
| **Marvis Browser Agent** | 操作系统层级内置浏览器Agent，支持网页导航、表单填写、动态内容抓取 | 三层架构：导航层→交互层→提取层 |
| **Codex Chrome扩展** | Chrome扩展实现网页操控，支持锁屏远程操作，Appshots上下文注入 | Chrome扩展注入 + Appshots视觉感知 |
| **OpenClaw Gateway** | 多渠道Web交互，支持OAuth/表单/文件上传，Gateway统一路由 | Gateway模式 + 安全纵深防御 |
| **Claude Dynamic Workflows** | 动态搜索分支决策，多源交叉验证，上下文感知搜索路径 | 动态分支决策 + 多源交叉验证 |

---

## 二、三层架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    浏览器Agent三层架构                      │
├─────────────────────────────────────────────────────────┤
│  Layer 1: 导航与感知层 (Navigation & Perception)          │
│  - URL导航 / 搜索引擎集成 / 页面DOM感知 / 截图快照         │
│  - 对标：Marvis Browser Agent 导航层 + Codex Appshots     │
├─────────────────────────────────────────────────────────┤
│  Layer 2: 交互与控制层 (Interaction & Control)            │
│  - 点击/输入/滚动/拖拽 / 表单填写 / 文件上传 / 下拉选择     │
│  - 对标：Codex Chrome扩展交互 + OpenClaw表单处理           │
├─────────────────────────────────────────────────────────┤
│  Layer 3: 提取与分析层 (Extraction & Analysis)            │
│  - 结构化数据提取 / 多页合并 / 动态内容等待 / 多源交叉验证  │
│  - 对标：Claude Dynamic Workflows + Marvis内容提取         │
└─────────────────────────────────────────────────────────┘
```

### 2.1 Layer 1：导航与感知层

**功能矩阵**：

| 功能 | 描述 | 优先级 | 对标 |
|------|------|--------|------|
| URL导航 | 打开指定URL，支持GET/POST参数 | P0 | Marvis |
| 搜索引擎集成 | 调用Google/Bing/Baidu等搜索引擎，自动翻页 | P0 | Marvis + Claude |
| 页面DOM感知 | 获取页面HTML/DOM结构，识别关键元素 | P0 | Codex Chrome |
| 截图快照 | 对当前页面/特定元素截图，用于视觉验证 | P0 | Codex Appshots |
| 等待条件 | 等待特定元素出现/消失/属性变化 | P1 | Claude |
| JavaScript执行 | 在页面上下文中执行JS代码 | P1 | Codex Chrome |
| Cookie管理 | 读取/设置/清除Cookie | P1 | OpenClaw |
| 代理配置 | 支持HTTP/HTTPS/SOCKS5代理 | P2 | 通用 |

**页面感知协议**：

```json
{
  "action": "perceive",
  "url": "https://example.com",
  "options": {
    "wait_for_selector": ".content-loaded",
    "timeout_ms": 10000,
    "screenshot": true,
    "extract_dom": true,
    "extract_text": true
  },
  "response": {
    "title": "页面标题",
    "url": "最终URL（含重定向）",
    "status_code": 200,
    "dom_summary": "关键DOM元素摘要",
    "text_content": "提取的文本内容",
    "screenshot_path": "截图保存路径",
    "links": ["提取的所有链接"],
    "forms": ["检测到的表单"]
  }
}
```

### 2.2 Layer 2：交互与控制层

**功能矩阵**：

| 功能 | 描述 | 优先级 | 对标 |
|------|------|--------|------|
| 点击 | 点击指定元素（选择器/坐标/文本） | P0 | Codex Chrome |
| 输入文本 | 在input/textarea中输入文本 | P0 | Codex Chrome |
| 表单填写 | 批量填写表单字段 | P0 | OpenClaw |
| 下拉选择 | 选择select/option元素 | P0 | Codex Chrome |
| 文件上传 | 上传本地文件到input[type=file] | P1 | OpenClaw |
| 键盘操作 | 模拟键盘快捷键/特殊键 | P1 | Codex |
| 滚动 | 滚动到指定位置/元素 | P1 | Marvis |
| 拖拽 | 鼠标拖拽操作 | P2 | Codex |
| iframe切换 | 切换到iframe上下文 | P1 | 通用 |
| 弹窗处理 | alert/confirm/prompt处理 | P1 | 通用 |
| 多标签管理 | 打开/切换/关闭标签页 | P2 | Marvis |

**交互指令协议**：

```json
{
  "action": "interact",
  "sequence": [
    {
      "type": "navigate",
      "url": "https://example.com/login"
    },
    {
      "type": "wait",
      "selector": "#login-form",
      "timeout_ms": 5000
    },
    {
      "type": "fill_form",
      "fields": {
        "#username": "user@example.com",
        "#password": "***"
      }
    },
    {
      "type": "click",
      "selector": "#login-button"
    },
    {
      "type": "wait",
      "condition": "url_changed",
      "timeout_ms": 10000
    }
  ],
  "options": {
    "screenshot_on_step": true,
    "retry_on_failure": 2,
    "step_delay_ms": 500
  }
}
```

### 2.3 Layer 3：提取与分析层

**功能矩阵**：

| 功能 | 描述 | 优先级 | 对标 |
|------|------|--------|------|
| 结构化提取 | CSS选择器/XPath提取结构化数据 | P0 | Claude |
| 多页合并 | 自动翻页并合并多页数据 | P0 | Claude Dynamic Workflows |
| 动态内容等待 | 等待AJAX/WebSocket加载完成 | P0 | Marvis |
| 多源交叉验证 | 从多个来源验证同一信息 | P1 | Claude |
| 表格提取 | 自动识别并提取HTML表格 | P0 | 通用 |
| JSON-LD提取 | 提取页面结构化数据标记 | P1 | 通用 |
| 差异检测 | 对比两次抓取结果的差异 | P2 | 自定义 |
| 增量抓取 | 仅提取自上次抓取后的新增内容 | P2 | 自定义 |

**提取协议**：

```json
{
  "action": "extract",
  "rules": [
    {
      "name": "article_list",
      "selector": ".article-item",
      "fields": {
        "title": ".title::text",
        "link": "a::attr(href)",
        "date": ".date::text",
        "summary": ".summary::text"
      },
      "multiple": true
    }
  ],
  "options": {
    "pagination": {
      "selector": ".next-page",
      "max_pages": 10
    },
    "dedup": true,
    "cross_validate": {
      "enabled": true,
      "sources": ["source_a", "source_b"]
    }
  }
}
```

---

## 三、五大核心能力

### 3.1 账号登录与Session管理

```
┌─────────────────────────────────────────┐
│         登录Session管理流程               │
├─────────────────────────────────────────┤
│  1. 检测登录状态（Cookie/Session检测）    │
│  2. 无Session → 导航到登录页              │
│  3. 填写凭据（从安全存储获取）             │
│  4. 处理验证码（见3.2）                   │
│  5. 提交登录表单                          │
│  6. 验证登录成功（URL跳转/元素检测）       │
│  7. 保存Session（Cookie持久化）           │
│  8. Session过期自动续期                   │
└─────────────────────────────────────────┘
```

**安全约束**：
- 凭据存储在加密的本地安全存储中（协议66 MCP安全纵深防御）
- 禁止明文记录凭据到日志
- Session Cookie加密持久化
- 支持OAuth 2.1 / SAML / 多因素认证流程

### 3.2 验证码识别

| 验证码类型 | 处理策略 | 优先级 |
|-----------|---------|--------|
| 文本验证码 | OCR识别（Tesseract/PaddleOCR） | P0 |
| 滑块验证码 | 模拟滑块轨迹（加速→匀速→减速） | P1 |
| 点选验证码 | 视觉模型识别目标位置 | P1 |
| 旋转验证码 | 视觉模型计算旋转角度 | P2 |
| reCAPTCHA | 降级处理：提示用户手动完成或使用音频验证码 | P1 |
| 短信验证码 | 监听短信/邮件 → 自动提取验证码 | P1 |

### 3.3 多页表单提交

```
┌──────────────────────────────────────────────┐
│           多页表单工作流                       │
├──────────────────────────────────────────────┤
│  Step 1: 识别表单结构（字段数/页数/验证规则）  │
│  Step 2: 生成填写计划（字段→值映射）           │
│  Step 3: 逐页填写 + 截图验证                   │
│  Step 4: 处理验证错误（自动修正/人工介入）      │
│  Step 5: 提交前预览确认                         │
│  Step 6: 最终提交 + 保存确认码                  │
└──────────────────────────────────────────────┘
```

### 3.4 动态内容抓取

| 动态类型 | 检测方法 | 处理策略 |
|---------|---------|---------|
| AJAX加载 | 监听XHR请求 | 等待请求完成 + 超时兜底 |
| 无限滚动 | 检测滚动条位置变化 | 自动滚动 → 检测新内容 → 重复 |
| WebSocket推送 | 监听WS消息 | 累积数据 → 定期快照 |
| 懒加载图片 | 检测img[loading=lazy] | 滚动到元素位置触发加载 |
| Shadow DOM | 检测shadowRoot | 穿透Shadow DOM边界提取 |
| 单页应用(SPA) | 检测路由变化 | 监听popstate/hashchange |

### 3.5 复杂站点交互

| 场景 | 策略 | 对标参考 |
|------|------|---------|
| 电商比价 | 并行打开多个商品页 → 提取价格/库存 → 交叉比较 | Claude Dynamic Workflows |
| 金融数据采集 | 登录→导航→筛选日期→下载CSV→解析 | Codex Chrome |
| 社交媒体监控 | 登录→搜索话题→翻页采集→情感分析 | Marvis |
| 表单批量提交 | 读取本地数据→逐条填写表单→提交→记录结果 | OpenClaw |
| 文件批量下载 | 解析下载列表→逐个点击下载→重命名→归档 | Codex |

---

## 四、技术实现方案

### 4.1 技术选型

| 组件 | 方案 | 选择理由 |
|------|------|---------|
| 浏览器引擎 | Playwright (Chromium) | 跨平台、支持headless/headed、API完善 |
| 截图方案 | Playwright内置截图 | 全页/元素/视口三种模式 |
| OCR引擎 | PaddleOCR | 中文识别精度高、离线可用 |
| Cookie管理 | Playwright storageState | 原生支持Session持久化 |
| 并发控制 | asyncio + Semaphore | Python原生异步并发 |
| 安全沙箱 | 协议66 MCP安全纵深防御 | 凭据隔离 + 操作审计 |

### 4.2 核心API设计

```python
class BrowserAgent:
    """浏览器Agent核心类"""

    # === Layer 1: 导航与感知 ===
    async def navigate(self, url: str, **options) -> PageState
    async def perceive(self, selector: str = None) -> PagePerception
    async def screenshot(self, path: str, full_page: bool = True) -> str
    async def wait_for(self, condition: WaitCondition, timeout_ms: int) -> bool

    # === Layer 2: 交互与控制 ===
    async def click(self, selector: str, **options) -> ActionResult
    async def type_text(self, selector: str, text: str) -> ActionResult
    async def fill_form(self, fields: dict) -> ActionResult
    async def select_option(self, selector: str, value: str) -> ActionResult
    async def upload_file(self, selector: str, file_path: str) -> ActionResult
    async def scroll(self, direction: str, amount: int) -> ActionResult

    # === Layer 3: 提取与分析 ===
    async def extract(self, rules: List[ExtractRule]) -> ExtractionResult
    async def extract_table(self, selector: str) -> pd.DataFrame
    async def paginate_and_extract(self, rules, max_pages: int) -> ExtractionResult
    async def cross_validate(self, data, sources: List[str]) -> ValidationResult

    # === Session管理 ===
    async def login(self, credentials: Credentials) -> SessionState
    async def save_session(self, path: str) -> str
    async def restore_session(self, path: str) -> SessionState

    # === 高级工作流 ===
    async def execute_workflow(self, workflow: WorkflowDefinition) -> WorkflowResult
    async def parallel_browse(self, urls: List[str], extract_rules) -> List[ExtractionResult]
```

### 4.3 安全护栏

| 层级 | 措施 | 依据 |
|------|------|------|
| 输入验证 | URL白名单/黑名单，禁止访问localhost/内网 | 安全纵深L1 |
| 操作审计 | 记录所有浏览器操作的完整日志 | 安全纵深L5 |
| 凭据隔离 | 登录凭据加密存储，内存使用后立即清除 | 安全纵深L2 |
| 网络隔离 | 可选代理/VPN通道，防止IP泄露 | 安全纵深L3 |
| 内容过滤 | 下载文件病毒扫描，禁止执行下载的可执行文件 | 安全纵深L4 |

---

## 五、与现有协议的关系

| 现有协议 | 关联方式 | 说明 |
|---------|---------|------|
| 协议66 MCP安全纵深防御 | 安全底座 | 浏览器操作的安全认证和审计 |
| 协议33 视觉桌面操控 | 互补 | 当Playwright无法覆盖时，降级为视觉操控 |
| 协议53 Windows桌面视觉操控 | 互补 | Windows环境下的浏览器视觉操作 |
| 协议34 动态工作流分支决策 | 驱动 | 搜索路径的动态分支决策 |
| 协议54 JS脚本百级并行 | 扩展 | 多站点并行采集时批量调度 |
| 龙虾五步法 Step1/Step4 | 集成 | 意图识别→自主执行搜索 |

---

## 六、评估指标

| 指标 | 基线（R25前） | R25目标 | R28目标 |
|------|-------------|---------|---------|
| 网页交互成功率 | 0%（无此能力） | 60% | 85% |
| 登录流程自动化率 | 0% | 50% | 80% |
| 动态内容抓取覆盖率 | 30%（静态页面） | 60% | 85% |
| 多源交叉验证率 | 10%（手动） | 40% | 70% |
| 单次搜索平均耗时 | 5-30秒 | 8-60秒 | 5-45秒 |
| 浏览器搜索能力得分 | 82 | 85 | 88 |

---

> **协议版本**：v1.0
> **创建日期**：2026-06-02
> **状态**：草案阶段 → 待工程实现
> **下一步**：R26深度对标分析（Marvis+Codex+OpenClaw源码级研究）
> **归属**：龙虾全域技能协议体系 #84
