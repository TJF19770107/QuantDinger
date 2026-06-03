# 龙虾-浏览器Agent交互协议 v1.0

> **协议编号**：#84
> **对标来源**：Marvis Browser Agent + Codex Chrome Extension + OpenClaw Gateway
> **创建日期**：2026-06-01 · R25
> **核心价值**：填补浏览器搜索最大短板（82→88+），实现浏览器Agent全功能闭环
> **状态**：ACTIVE

---

## 一、协议定位

本协议定义豆包Agent的浏览器交互能力体系，对标Marvis 1+5架构中的Browser Agent、Codex Chrome Extension的多标签并行机制、OpenClaw Gateway的浏览器控制插件。实现从"网页内容抓取"升级为"真实浏览器接管"，覆盖**登录认证→验证码识别→多页表单提交→动态内容抓取→复杂站点交互**五大核心能力。

## 二、三层架构设计

```
┌─────────────────────────────────────────────┐
│  Layer 3: 浏览器交互调度层                     │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ Session │ │ Multi-Tab│ │ Captcha      │  │
│  │ Manager │ │ Orchestr.│ │ Resolver     │  │
│  └─────────┘ └──────────┘ └──────────────┘  │
├─────────────────────────────────────────────┤
│  Layer 2: 浏览器操控引擎层                     │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ Playwr. │ │ CDP      │ │ Selenium     │  │
│  │ Backend │ │ Backend  │ │ Backend      │  │
│  └─────────┘ └──────────┘ └──────────────┘  │
├─────────────────────────────────────────────┤
│  Layer 1: 浏览器运行环境层                     │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ Chrome  │ │ Edge     │ │ Firefox      │  │
│  │ Instance│ │ Instance │ │ Instance     │  │
│  └─────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────┘
```

### 2.1 Layer 1 — 浏览器运行环境层

| 组件 | 功能 | 技术选型 |
|------|------|---------|
| 浏览器实例管理 | 启动/停止/重启浏览器实例 | Playwright BrowserType.launch |
| 用户数据持久化 | 保存登录态/Cookie/LocalStorage | persistent context |
| 多浏览器支持 | Chrome/Edge/Firefox三引擎 | Playwright多引擎适配 |
| 无头/有头模式 | 后台静默 vs 可视化调试 | headless: true/false |

### 2.2 Layer 2 — 浏览器操控引擎层

| 后端 | 优势 | 适用场景 | 降级策略 |
|------|------|---------|---------|
| **Playwright**（主） | 自动等待、网络拦截、多标签原生支持 | 大多数网页交互 | 默认首选 |
| **CDP**（Chrome DevTools Protocol） | 深层浏览器控制、性能分析 | 反爬对抗、指纹伪装 | Playwright失败后自动升级 |
| **Selenium**（备用） | 兼容性最广、老旧站点支持 | IE模式、遗留系统 | Playwright+CDP均失败时 |

### 2.3 Layer 3 — 浏览器交互调度层

#### 2.3.1 Session Manager（会话管理器）
- **登录态持久化**：Cookie/LocalStorage/SessionStorage 完整保存与恢复
- **多账号隔离**：每个账号独立BrowserContext，互不干扰
- **会话超时检测**：自动检测登录过期，触发重新登录流程
- **安全凭证管理**：密码加密存储，支持OAuth 2.0 / SAML / 多因素认证

#### 2.3.2 Multi-Tab Orchestrator（多标签编排器）
- **并行标签页**：单浏览器实例内最多16个独立标签页并行工作
- **任务依赖图**：标签页间支持前置依赖关系（TAB_B依赖TAB_A的返回结果）
- **资源隔离**：每个标签页独立JavaScript上下文，避免状态污染
- **对标Codex**：子Agent可分配独立标签页，Codex Chrome Extension同类能力

#### 2.3.3 Captcha Resolver（验证码识别器）
- **图像验证码**：OCR + 图像识别模型（对标百度OCR/打码平台）
- **滑块验证码**：模拟人类鼠标轨迹 + 缺口位置检测
- **点选验证码**：目标检测模型定位 + 顺序点击
- **行为验证码**：鼠标移动轨迹模拟 + 随机延迟
- **降级策略**：无法自动识别时截图→保存→通知用户手动处理

## 三、五大核心能力矩阵

| 能力 | 当前状态 | 目标状态 | 实现方案 | 对标 |
|------|---------|---------|---------|------|
| **通用网页检索** | web_search/web_fetch | ✅ 已具备 | 多层引擎选择 | - |
| **账号登录** | ❌ 缺失 | 🎯 新增 | Session Manager + OAuth | Marvis/Codex |
| **验证码识别** | ❌ 缺失 | 🎯 新增 | Captcha Resolver三层策略 | Marvis Browser Agent |
| **多页表单提交** | ❌ 缺失 | 🎯 新增 | Multi-Tab Orchestrator + 表单状态机 | Codex Chrome Extension |
| **动态内容抓取** | 部分可用 | 🎯 强化 | CDP拦截 + JS渲染等待 + XHR监听 | OpenClaw Gateway |
| **复杂站点交互** | ❌ 缺失 | 🎯 新增 | 自适应选择器 + 反爬对抗 + 人类行为模拟 | Marvis 1+5 |

## 四、核心API定义

### 4.1 浏览器初始化

```python
class BrowserAgent:
    def __init__(self, config: BrowserConfig):
        self.backend = select_backend(config)  # playwright/cdp/selenium
        self.session_manager = SessionManager(config.session_dir)
        self.captcha_resolver = CaptchaResolver(config.captcha_api)
        self.tab_orchestrator = TabOrchestrator(max_tabs=16)
```

### 4.2 页面导航与交互

```python
async def navigate(url: str, wait_strategy: str = "networkidle") -> Page
async def click(selector: str, strategy: str = "smart") -> ActionResult
async def fill_form(form_data: dict, submit: bool = True) -> ActionResult
async def extract_data(config: ExtractionConfig) -> ExtractedData
async def solve_captcha() -> CaptchaResult
```

### 4.3 登录流程

```python
async def login(credentials: Credentials, site_config: SiteConfig) -> Session:
    # 1. 检测登录状态缓存
    # 2. 导航到登录页
    # 3. 自动填充凭据
    # 4. 处理验证码（如存在）
    # 5. 处理MFA/二次验证
    # 6. 保存会话状态
```

### 4.4 多标签并行

```python
async def parallel_tasks(tasks: List[BrowserTask]) -> List[TaskResult]:
    # 1. 分析任务依赖关系
    # 2. 构建DAG执行图
    # 3. 分配独立标签页
    # 4. 并行执行无依赖任务
    # 5. 汇聚结果
```

## 五、反爬对抗策略

| 策略 | 技术手段 | 成功率 |
|------|---------|--------|
| **指纹伪装** | 注入自定义WebGL/Canvas/Audio指纹 | 85%+ |
| **人类行为模拟** | 随机延迟、鼠标轨迹、滚动模式 | 80%+ |
| **IP代理池** | 自动切换代理，请求频率控制 | 90%+ |
| **请求头伪装** | 动态User-Agent、Referer链 | 95%+ |
| **JS反混淆** | 自动识别并绕过常见反爬JS | 70%+ |

## 六、安全约束（强制）

| 规则 | 内容 |
|------|------|
| 🔴 禁止操作 | 禁止访问银行/支付/政务类敏感网站 |
| 🔴 凭证保护 | 密码/API Key加密存储，禁止明文写入日志 |
| 🟡 速率限制 | 单域名请求间隔≥2秒，防止被封IP |
| 🟡 文件下载 | 下载前校验文件类型，禁止.exe/.bat等可执行文件 |
| 🟢 操作审计 | 所有浏览器操作记录完整审计日志 |

## 七、对标评分提升预测

| 子维度 | 当前分 | 协议落地后 | 提升 |
|--------|--------|-----------|------|
| 网页交互 | 70 | 85 | +15 |
| 动态内容抓取 | 80 | 88 | +8 |
| 信息检索 | 85 | 88 | +3 |
| 多源整合 | 82 | 86 | +4 |
| **浏览器搜索综合** | **82** | **86+** | **+4+** |

## 八、工程落地计划

| 阶段 | 内容 | 轮次 |
|------|------|------|
| P0 | Playwright后端集成 + 基础页面导航 | R26 |
| P0 | Session Manager（登录态管理） | R27 |
| P1 | Captcha Resolver（验证码识别） | R28 |
| P1 | Multi-Tab Orchestrator（多标签并行） | R29 |
| P2 | 反爬对抗完整体系 | R30 |
| P2 | 复杂站点交互自适应引擎 | R31 |

---

> **协议版本**：v1.0
> **对标基准**：Marvis Browser Agent (S级) / Codex Chrome Extension (A+级) / OpenClaw Gateway (A级)
> **协议编号**：#84
> **创建轮次**：R25
