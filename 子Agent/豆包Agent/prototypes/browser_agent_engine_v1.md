# browser_agent_engine_v1.py

原始格式: Python

```python
"""
龙虾-浏览器Agent交互引擎 v1.0
协议#84 工程落地原型
对标：Marvis Browser Agent + Codex Chrome Extension
"""

import asyncio
import json
import os
import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path

# ============================================================
# 数据模型
# ============================================================

@dataclass
class BrowserConfig:
    headless: bool = True
    browser_type: str = "chromium"  # chromium|firefox|webkit
    user_data_dir: str = ""
    viewport: dict = field(default_factory=lambda: {"width": 1920, "height": 1080})
    slow_mo: int = 100  # 毫秒，模拟人类操作延迟
    max_tabs: int = 16
    proxy: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class ExtractionConfig:
    selectors: List[str] = field(default_factory=list)
    extract_text: bool = True
    extract_links: bool = False
    extract_images: bool = False
    wait_for_selector: Optional[str] = None
    scroll_to_bottom: bool = False

@dataclass  
class Session:
    id: str
    cookies: List[Dict]
    local_storage: Dict
    created_at: float
    domain: str

# ============================================================
# 核心引擎
# ============================================================

class BrowserAgentEngine:
    """浏览器Agent三层架构核心引擎"""
    
    def __init__(self, config: BrowserConfig):
        self.config = config
        self.playwright = None
        self.browser = None
        self.contexts: Dict[str, Any] = {}  # 多账号隔离
        self.active_tabs: Dict[str, Any] = {}
        self.session_dir = Path(config.user_data_dir) / "sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
    async def start(self):
        """Layer 1: 浏览器实例启动"""
        from playwright.async_api import async_playwright
        self.playwright = await async_playwright().start()
        launch_args = {
            "headless": self.config.headless,
            "slow_mo": self.config.slow_mo,
        }
        if self.config.proxy:
            launch_args["proxy"] = {"server": self.config.proxy}
        self.browser = await self.playwright.chromium.launch(**launch_args)
        
    async def create_context(self, account_id: str) -> Any:
        """Layer 2: 独立BrowserContext（多账号隔离）"""
        context = await self.browser.new_context(
            viewport=self.config.viewport,
            user_agent=self.config.user_agent,
            storage_state=self._load_session(account_id)
        )
        self.contexts[account_id] = context
        return context
    
    async def navigate(self, url: str, account_id: str = "default", 
                       wait_strategy: str = "networkidle") -> Any:
        """页面导航（自动等待）"""
        context = self.contexts.get(account_id) or await self.create_context(account_id)
        page = await context.new_page()
        await page.goto(url, wait_until=wait_strategy)
        self.active_tabs[id(page)] = page
        return page
    
    async def click(self, page: Any, selector: str, strategy: str = "smart") -> bool:
        """智能点击（自动降级策略）"""
        strategies = {
            "smart": [f"text={selector}", f"[aria-label='{selector}']", 
                      f"button:has-text('{selector}')", selector],
            "text": [f"text={selector}"],
            "css": [selector]
        }
        for s in strategies.get(strategy, [selector]):
            try:
                await page.click(s, timeout=3000)
                return True
            except:
                continue
        return False
    
    async def fill_form(self, page: Any, form_data: Dict[str, str]) -> bool:
        """表单填充（自动字段匹配）"""
        try:
            for field, value in form_data.items():
                # 智能选择器降级链
                for sel in [f"input[name='{field}']", f"#{field}", 
                           f"[placeholder*='{field}']", f"label:has-text('{field}') + input"]:
                    try:
                        await page.fill(sel, value)
                        break
                    except:
                        continue
            return True
        except Exception as e:
            print(f"Form fill error: {e}")
            return False
    
    async def extract_data(self, page: Any, config: ExtractionConfig) -> Dict:
        """动态内容提取"""
        result = {"url": page.url, "timestamp": time.time()}
        
        if config.wait_for_selector:
            await page.wait_for_selector(config.wait_for_selector, timeout=10000)
        
        if config.scroll_to_bottom:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)
        
        if config.extract_text:
            result["text"] = await page.evaluate("document.body.innerText")
        
        if config.extract_links:
            result["links"] = await page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href]'))
                    .map(a => ({text: a.innerText, href: a.href}))
                    .filter(l => l.href.startsWith('http'))
            }""")
        
        return result
    
    async def parallel_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """Layer 3: 多标签并行执行（对标Codex多标签）"""
        async def run_single(task):
            page = await self.navigate(task["url"], task.get("account", "default"))
            if task.get("actions"):
                for action in task["actions"]:
                    if action["type"] == "click":
                        await self.click(page, action["selector"])
                    elif action["type"] == "fill":
                        await self.fill_form(page, action["data"])
            if task.get("extract"):
                return await self.extract_data(page, ExtractionConfig(**task["extract"]))
            return {"status": "completed", "url": task["url"]}
        
        results = await asyncio.gather(*[run_single(t) for t in tasks])
        return results
    
    def _save_session(self, account_id: str, cookies: List[Dict], local_storage: Dict):
        """登录态持久化"""
        session_path = self.session_dir / f"{account_id}.json"
        session = Session(
            id=account_id, cookies=cookies, local_storage=local_storage,
            created_at=time.time(), domain=""
        )
        session_path.write_text(json.dumps(session.__dict__, ensure_ascii=False))
    
    def _load_session(self, account_id: str) -> Optional[Dict]:
        """恢复登录态"""
        session_path = self.session_dir / f"{account_id}.json"
        if session_path.exists():
            data = json.loads(session_path.read_text())
            return {"cookies": data.get("cookies", []), 
                    "origins": [{"origin": data.get("domain", "*"), 
                                "localStorage": [{"name": k, "value": v} 
                                    for k, v in data.get("local_storage", {}).items()]}]}
        return None
    
    async def stop(self):
        """安全关闭"""
        for ctx in self.contexts.values():
            await ctx.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

# ============================================================
# 反爬对抗模块
# ============================================================

class AntiDetection:
    """反爬对抗策略注入"""
    
    STEALTH_JS = """
    // WebGL指纹伪装
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Intel Inc.';
        if (parameter === 37446) return 'Intel Iris OpenGL Engine';
        return getParameter.call(this, parameter);
    };
    // 隐藏自动化特征
    delete navigator.__proto__.webdriver;
    Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
    Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN','zh','en']});
    """
    
    @staticmethod
    async def inject_stealth(page: Any):
        await page.add_init_script(AntiDetection.STEALTH_JS)
    
    @staticmethod
    async def human_scroll(page: Any):
        """模拟人类滚动模式"""
        import random
        total_height = await page.evaluate("document.body.scrollHeight")
        viewport = page.viewport_size["height"]
        current = 0
        while current < total_height:
            scroll_step = random.randint(100, 400)
            current += scroll_step
            await page.evaluate(f"window.scrollTo(0, {current})")
            await asyncio.sleep(random.uniform(0.5, 2.0))

# ============================================================
# 使用示例
# ============================================================

async def demo():
    config = BrowserConfig(
        headless=False,
        user_data_dir="./browser_data",
        slow_mo=150
    )
    engine = BrowserAgentEngine(config)
    await engine.start()
    
    # 示例：搜索+提取
    page = await engine.navigate("https://www.google.com")
    await engine.click(page, "接受全部", strategy="smart")
    await engine.fill_form(page, {"q": "AI Agent 2026"})
    
    # 关闭
    await engine.stop()

if __name__ == "__main__":
    print("龙虾-浏览器Agent交互引擎 v1.0 原型加载完成")
    print(f"协议#84 | 三层架构 | Playwright后端 | {BrowserAgentEngine.__doc__}")

```
