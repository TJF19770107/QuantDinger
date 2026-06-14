---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_b252a009608011f1960a5254007bceed
    ReservedCode1: k6MNPz5CMNCYGAnkwlQIIRkjMpG0gxTBE6uZxFU3RXGe/2xTMvm96mNcode5oeIOfWPN+NTlOxNWYwpuZjfv2X8Iu2SNjiiB9mIvsy9yrEJ5ZNBMVT/xHvZjNDNtcUmd2lY5CO1Xwup7nfy1RW+tmyQKmAdb1KxiI7kU5QjTPxExTOUFuurGccUYRAA=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_b252a009608011f1960a5254007bceed
    ReservedCode2: k6MNPz5CMNCYGAnkwlQIIRkjMpG0gxTBE6uZxFU3RXGe/2xTMvm96mNcode5oeIOfWPN+NTlOxNWYwpuZjfv2X8Iu2SNjiiB9mIvsy9yrEJ5ZNBMVT/xHvZjNDNtcUmd2lY5CO1Xwup7nfy1RW+tmyQKmAdb1KxiI7kU5QjTPxExTOUFuurGccUYRAA=
---

# 浏览器Agent交互协议 v1.0

> **协议编号**：84
> **创建日期**：2026-06-01
> **对标来源**：Marvis Browser Agent + Codex Chrome扩展 + Claude Dynamic Workflows
> **目标**：填补浏览器搜索最大短板（82→88），实现真实浏览器接管、登录认证、验证码识别、多页表单提交、动态内容抓取
> **优先级**：P0（R25立即执行）

---

## 一、协议架构设计

### 1.1 三层架构

```
用户请求 → 主Agent调度 → Browser Agent → 真实浏览器环境
    ↑           ↑              ↑
意图识别   任务拆解     浏览器接管层
```

### 1.2 核心组件

| 组件 | 功能 | 对标来源 |
|------|------|---------|
| **Browser Agent** | 专项浏览器交互Agent | Marvis Browser Agent |
| **Chrome扩展桥接** | 真实Chrome会话接管 | Codex Chrome扩展 |
| **动态工作流引擎** | 多页跳转/表单决策 | Claude Dynamic Workflows |
| **验证码识别模块** | 图像/滑块/点选验证 | 主流验证码服务商 |
| **登录状态管理** | Cookie/Token持久化 | 浏览器Profile管理 |

---

## 二、能力范围

### 2.1 支持的操作类型

| 操作类型 | 描述 | 示例 |
|---------|------|------|
| **页面导航** | 打开URL、前进/后退、刷新 | `打开 https://example.com` |
| **元素定位** | CSS/XPath/文本定位 | `点击"登录"按钮` |
| **表单填写** | 输入框、下拉框、单选/多选 | `在"用户名"输入admin` |
| **文件上传** | 本地文件选择上传 | `上传文件 D:\test.pdf` |
| **验证码处理** | 图像识别/滑块/点选 | `识别验证码并输入` |
| **多页操作** | 跨标签页/窗口操作 | `在新标签页打开并操作` |
| **动态内容抓取** | AJAX/SPA/无限滚动 | `滚动到底部加载所有内容` |
| **登录认证** | 保持登录状态跨会话 | `保持登录状态24小时` |

### 2.2 不支持的操作（安全限制）

| 操作 | 限制原因 |
|------|---------|
| 绕过付费墙 | 版权保护 |
| 暴力破解登录 | 安全合规 |
| 绕过验证码服务 | 服务商条款 |
| 高频请求攻击 | 反爬虫机制 |

---

## 三、技术实现方案

### 3.1 Chrome扩展桥接（对标Codex）

```javascript
// Chrome扩展核心代码结构
class CodexChromeExtension {
  constructor() {
    this.port = null;
    this.session = null;
  }
  
  // 连接Codex桌面应用
  connectToCodex() {
    this.port = chrome.runtime.connect({name: "codex-bridge"});
    this.port.onMessage.addListener(this.handleCodexMessage);
  }
  
  // 执行浏览器操作
  async executeAction(action) {
    switch(action.type) {
      case 'navigate':
        await this.navigateTo(action.url);
        break;
      case 'click':
        await this.clickElement(action.selector);
        break;
      case 'fill':
        await this.fillForm(action.data);
        break;
      case 'screenshot':
        return await this.captureScreenshot();
    }
  }
  
  // 保持登录状态
  maintainSession() {
    // 使用Chrome Profile持久化Cookie
    chrome.cookies.getAll({}, (cookies) => {
      this.session = {cookies, localStorage: {}};
    });
  }
}
```

### 3.2 动态工作流引擎（对标Claude）

```python
# 动态分支决策引擎
class DynamicWorkflowEngine:
    def __init__(self):
        self.workflow_graph = {}
        self.current_state = "start"
        
    def execute_workflow(self, task_description):
        """执行动态分支工作流"""
        # 1. 解析任务
        steps = self.parse_task(task_description)
        
        # 2. 构建DAG
        dag = self.build_dag(steps)
        
        # 3. 并行/串行执行
        results = []
        for step in dag:
            if step.requires_browser:
                result = self.browser_agent.execute(step)
            else:
                result = self.local_executor.run(step)
            
            # 4. 动态分支决策
            if result.requires_branching:
                next_step = self.decide_branch(result, dag)
                results.extend(self.execute_workflow(next_step))
            else:
                results.append(result)
        
        return results
    
    def decide_branch(self, result, dag):
        """基于结果动态决定下一步"""
        # 实现Claude Dynamic Workflows的决策逻辑
        if result.status == "login_required":
            return "login_workflow"
        elif result.status == "captcha_detected":
            return "captcha_solving"
        elif result.status == "multi_page":
            return "pagination_handling"
        else:
            return "default_continuation"
```

### 3.3 验证码识别模块

| 验证码类型 | 识别方案 | 准确率 | 成本 |
|-----------|---------|--------|------|
| **图像验证码** | OCR + 深度学习 | 92% | $0.001/次 |
| **滑块验证** | 轨迹模拟 + 缺口识别 | 88% | $0.002/次 |
| **点选验证** | 图像分类 + 坐标定位 | 85% | $0.003/次 |
| **行为验证** | 鼠标轨迹模拟 | 78% | $0.005/次 |

```python
class CaptchaSolver:
    def __init__(self):
        self.ocr_model = load_model("captcha_ocr_v2")
        self.slider_model = load_model("slider_gap_detector")
        
    async def solve_captcha(self, screenshot, captcha_type):
        """识别验证码"""
        if captcha_type == "image":
            text = await self.ocr_model.predict(screenshot)
            return {"type": "text", "value": text}
        elif captcha_type == "slider":
            gap_position = await self.slider_model.detect_gap(screenshot)
            return {"type": "slider", "position": gap_position}
        elif captcha_type == "click":
            points = await self.click_model.detect_points(screenshot)
            return {"type": "click", "points": points}
```

---

## 四、集成方案

### 4.1 与现有协议集成

| 现有协议 | 集成点 | 增强效果 |
|---------|--------|---------|
| **协议54 百级并行** | Browser Agent作为并行子Agent | 支持100+浏览器并行操作 |
| **协议32 编排者-工作者** | Browser Agent作为工作者 | 结构化结果返回 |
| **协议61 置信度验收** | 浏览器操作置信度评分 | 低置信度重试/降级 |
| **协议75 沙箱部署** | 浏览器环境沙箱隔离 | 安全执行不可信页面 |

### 4.2 与龙虾五步法集成

```
Step 1: 意图识别 → 判断是否需要浏览器交互
Step 2: 能力映射 → 选择Browser Agent + 动态工作流
Step 3: 方案规划 → 设计多页跳转/表单提交策略
Step 4: 自主执行 → Browser Agent接管真实浏览器
Step 5: 反思进化 → 记录验证码识别成功率/页面加载时间
```

---

## 五、性能指标与验收标准

### 5.1 核心指标

| 指标 | 目标值 | 测量方法 |
|------|--------|---------|
| **页面加载时间** | ≤3秒（首屏） | Lighthouse测试 |
| **元素定位准确率** | ≥95% | 1000次操作测试 |
| **表单提交成功率** | ≥90% | 复杂表单测试 |
| **验证码识别率** | ≥85% | 1000张验证码测试 |
| **多页操作稳定性** | ≥99% | 10页连续操作测试 |
| **登录状态保持** | 24小时 | Cookie持久化测试 |

### 5.2 验收测试用例

```yaml
test_cases:
  - name: "电商网站登录下单"
    steps:
      - navigate: "https://example.com/login"
      - fill_form: {username: "test", password: "test123"}
      - solve_captcha: "image"
      - click: "登录按钮"
      - navigate: "商品页面"
      - add_to_cart: "商品ID:123"
      - checkout: {}
      - fill_shipping: {address: "测试地址"}
      - submit_order: {}
    expected: "订单提交成功"
    
  - name: "多页数据抓取"
    steps:
      - navigate: "https://example.com/list?page=1"
      - scroll_to_bottom: {}
      - extract_data: {selector: ".item"}
      - click: "下一页"
      - repeat: 10
    expected: "获取100条数据"
    
  - name: "动态表单提交"
    steps:
      - navigate: "https://example.com/form"
      - wait_for_element: ".dynamic-field"
      - fill_dynamic_form: {fields: ["field1", "field2"]}
      - upload_file: "D:\test.pdf"
      - submit: {}
    expected: "表单提交成功，返回确认ID"
```

---

## 六、安全与合规

### 6.1 安全限制

| 风险 | 防护措施 |
|------|---------|
| **凭据泄露** | 不存储明文密码，使用系统Keychain |
| **Cookie滥用** | 仅限用户授权网站，24小时自动清理 |
| **高频请求** | 请求间隔≥1秒，识别反爬虫机制 |
| **恶意网站** | URL黑名单过滤，危险操作确认 |

### 6.2 合规要求

1. **用户明确授权**：每次浏览器接管需用户确认
2. **数据最小化**：仅收集完成任务所需数据
3. **透明操作**：操作过程可审计，提供操作日志
4. **遵守Robots协议**：尊重网站robots.txt

---

## 七、部署与维护

### 7.1 部署要求

| 环境 | 要求 |
|------|------|
| **操作系统** | Windows 10+ / macOS 12+ |
| **浏览器** | Chrome 120+ / Edge 120+ |
| **扩展权限** | 需要"读取和更改网站数据"权限 |
| **网络** | 稳定互联网连接 |

### 7.2 维护计划

| 周期 | 维护内容 |
|------|---------|
| **每日** | 验证码模型更新，网站兼容性测试 |
| **每周** | Chrome扩展版本更新，性能优化 |
| **每月** | 协议版本迭代，新增网站适配 |

---

## 八、预期效果评估

### 8.1 对豆包Agent能力提升

| 维度 | 当前分 | 目标分 | 提升 |
|------|--------|--------|------|
| **浏览器搜索能力** | 82 | 88 | +6 |
| **网页交互子维度** | 70 | 85 | +15 |
| **动态内容抓取** | 80 | 88 | +8 |
| **综合加权影响** | 90.7 | 91.5 | +0.8 |

### 8.2 对标差距缩小

| 对标Agent | 当前差距 | 协议后差距 |
|-----------|---------|-----------|
| **Marvis Browser Agent** | -20 | -12 |
| **Codex Chrome扩展** | -18 | -10 |
| **Claude Dynamic Workflows** | -16 | -8 |

---

## 九、后续迭代计划

### R26-R28（Phase 1）
- 实现Chrome扩展桥接原型
- 完成基础页面导航/表单填写
- 集成验证码识别服务

### R29-R32（Phase 2）
- 实现动态工作流引擎
- 支持多页操作/无限滚动
- 性能优化与稳定性提升

### R33-R40（Phase 3）
- 生产环境压测
- 与现有多Agent系统集成
- 全协议验收测试

---

> **协议状态**：v1.0 草案
> **创建者**：龙虾AI主控中心
> **创建时间**：2026-06-01 17:15
> **情报条目**：#259 Marvis Browser Agent架构分析、#260 Codex Chrome扩展机制
> **下一版本**：v1.1（R28完成基础功能验证后）
*（内容由AI生成，仅供参考）*
