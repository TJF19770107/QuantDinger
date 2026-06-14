# session_manager_v1.py

原始格式: Python

```python
"""
龙虾-浏览器Agent会话管理器 v1.0
协议#84 补充模块：登录态管理+验证码识别
"""

import json
import time
import base64
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
from cryptography.fernet import Fernet

# ============================================================
# 会话管理器
# ============================================================

@dataclass
class SessionData:
    account_id: str
    domain: str
    cookies: List[Dict]
    local_storage: Dict
    session_storage: Dict
    created_at: float
    last_access: float
    expires_at: Optional[float] = None
    oauth_token: Optional[str] = None

class SessionManager:
    """登录态全生命周期管理"""
    
    def __init__(self, storage_dir: str = "./sessions", encryption_key: Optional[bytes] = None):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.active_sessions: Dict[str, SessionData] = {}
        
        # 加密密钥管理
        self.cipher = Fernet(encryption_key or Fernet.generate_key())
        self._load_persisted_sessions()
    
    def save_session(self, account_id: str, domain: str, cookies: List[Dict],
                    local_storage: Dict, session_storage: Dict) -> SessionData:
        """保存会话（加密存储）"""
        session = SessionData(
            account_id=account_id, domain=domain,
            cookies=cookies, local_storage=local_storage,
            session_storage=session_storage,
            created_at=time.time(), last_access=time.time(),
            expires_at=self._extract_expiry(cookies)
        )
        
        # 加密敏感数据
        session_data = json.dumps(session.__dict__, ensure_ascii=False)
        encrypted = self.cipher.encrypt(session_data.encode())
        
        # 写入磁盘
        session_path = self.storage_dir / f"{account_id}_{self._hash_domain(domain)}.enc"
        session_path.write_bytes(encrypted)
        
        self.active_sessions[account_id] = session
        return session
    
    def load_session(self, account_id: str, domain: str) -> Optional[SessionData]:
        """加载会话"""
        # 先查内存
        if account_id in self.active_sessions:
            session = self.active_sessions[account_id]
            if not self._is_expired(session):
                session.last_access = time.time()
                return session
        
        # 再查磁盘
        session_path = self.storage_dir / f"{account_id}_{self._hash_domain(domain)}.enc"
        if session_path.exists():
            try:
                decrypted = self.cipher.decrypt(session_path.read_bytes())
                data = json.loads(decrypted)
                session = SessionData(**data)
                if not self._is_expired(session):
                    self.active_sessions[account_id] = session
                    return session
            except:
                pass
        
        return None
    
    def invalidate_session(self, account_id: str):
        """使会话失效"""
        if account_id in self.active_sessions:
            del self.active_sessions[account_id]
        # 删除磁盘文件
        for f in self.storage_dir.glob(f"{account_id}_*.enc"):
            f.unlink()
    
    def get_playwright_storage_state(self, account_id: str, domain: str) -> Optional[Dict]:
        """转换为Playwright storage_state格式"""
        session = self.load_session(account_id, domain)
        if not session:
            return None
        
        return {
            "cookies": session.cookies,
            "origins": [{
                "origin": session.domain,
                "localStorage": [{"name": k, "value": v} 
                    for k, v in session.local_storage.items()]
            }]
        }
    
    def _is_expired(self, session: SessionData) -> bool:
        if session.expires_at:
            return time.time() > session.expires_at
        
        # 默认7天超时
        return (time.time() - session.last_access) > 7 * 86400
    
    def _extract_expiry(self, cookies: List[Dict]) -> Optional[float]:
        for c in cookies:
            if c.get("name", "").lower() in ("session", "__cf_bm"):
                return None  # Session cookie无固定过期
        # 取最近过期cookie的时间
        expiries = [c.get("expires", 0) for c in cookies if "expires" in c]
        return max(expiries) if expiries else None
    
    @staticmethod
    def _hash_domain(domain: str) -> str:
        return hashlib.sha256(domain.encode()).hexdigest()[:16]
    
    def _load_persisted_sessions(self):
        """启动时加载已持久化会话"""
        for f in self.storage_dir.glob("*.enc"):
            try:
                decrypted = self.cipher.decrypt(f.read_bytes())
                data = json.loads(decrypted)
                session = SessionData(**data)
                if not self._is_expired(session):
                    self.active_sessions[session.account_id] = session
            except:
                continue


# ============================================================
# 验证码识别器
# ============================================================

class CaptchaResolver:
    """
    验证码识别器（三层策略）
    Layer1: 本地OCR + 图像识别
    Layer2: 第三方API（百度OCR/打码平台）
    Layer3: 保存截图→人工处理
    """
    
    CAPTCHA_TYPES = ["image_text", "slider", "click_order", "behavior"]
    
    def __init__(self, ocr_api_key: Optional[str] = None, fallback_dir: str = "./captcha_fallbacks"):
        self.ocr_api_key = ocr_api_key
        self.fallback_dir = Path(fallback_dir)
        self.fallback_dir.mkdir(parents=True, exist_ok=True)
        self.retry_count: Dict[str, int] = {}
    
    async def solve(self, captcha_type: str, image_data: bytes, 
                   context: Optional[Dict] = None) -> Dict:
        """主入口：自动识别验证码"""
        
        if captcha_type not in self.CAPTCHA_TYPES:
            return {"success": False, "error": f"不支持的验证码类型: {captcha_type}"}
        
        # 尝试次数控制
        captcha_hash = hashlib.md5(image_data).hexdigest()
        self.retry_count[captcha_hash] = self.retry_count.get(captcha_hash, 0) + 1
        if self.retry_count[captcha_hash] > 3:
            return await self._fallback_to_human(captcha_type, image_data)
        
        # Layer 1: 本地识别
        result = await self._local_solve(captcha_type, image_data, context)
        if result.get("success"):
            return result
        
        # Layer 2: 第三方API
        if self.ocr_api_key:
            result = await self._api_solve(captcha_type, image_data)
            if result.get("success"):
                return result
        
        # Layer 3: 人工处理
        return await self._fallback_to_human(captcha_type, image_data)
    
    async def _local_solve(self, captcha_type: str, image_data: bytes, 
                          context: Optional[Dict]) -> Dict:
        """本地识别策略"""
        if captcha_type == "image_text":
            # 基础OCR（实际需集成tesseract/paddleocr）
            return {"success": False, "error": "本地OCR未配置引擎"}
        
        elif captcha_type == "slider":
            # 滑块缺口检测（需集成OpenCV模板匹配）
            return {"success": False, "error": "滑块检测未配置模型"}
        
        elif captcha_type == "click_order":
            # 点选顺序检测（需集成目标检测模型）
            return {"success": False, "error": "点选检测未配置模型"}
        
        return {"success": False, "error": "未知类型"}
    
    async def _api_solve(self, captcha_type: str, image_data: bytes) -> Dict:
        """第三方API识别"""
        # 百度OCR / 打码平台接口（需实际配置）
        return {"success": False, "error": "API未配置"}
    
    async def _fallback_to_human(self, captcha_type: str, image_data: bytes) -> Dict:
        """降级：保存截图通知人工"""
        timestamp = int(time.time())
        img_path = self.fallback_dir / f"captcha_{captcha_type}_{timestamp}.png"
        img_path.write_bytes(image_data)
        
        return {
            "success": False,
            "fallback": True,
            "image_path": str(img_path),
            "message": f"验证码需要人工处理，已保存至: {img_path}"
        }


# ============================================================
# 多因素认证处理
# ============================================================

class MFAHandler:
    """MFA/二次验证处理"""
    
    def __init__(self):
        self.pending_mfa: Dict[str, Dict] = {}
    
    def detect_mfa_page(self, page_content: str) -> Optional[str]:
        """检测是否进入MFA页面"""
        mfa_keywords = [
            "two-factor", "2fa", "mfa", "verification code",
            "验证码", "双重认证", "两步验证", "短信验证",
            "authenticator", "security code", "确认码"
        ]
        for keyword in mfa_keywords:
            if keyword.lower() in page_content.lower():
                return keyword
        return None
    
    def request_user_input(self, mfa_type: str) -> Dict:
        """请求用户输入MFA验证码"""
        mfa_id = hashlib.md5(f"{mfa_type}_{time.time()}".encode()).hexdigest()[:8]
        self.pending_mfa[mfa_id] = {
            "type": mfa_type,
            "timestamp": time.time(),
            "status": "waiting"
        }
        return {
            "mfa_id": mfa_id,
            "type": mfa_type,
            "message": f"需要{mfa_type}验证，请输入验证码",
            "timeout": 300  # 5分钟超时
        }


# ============================================================
# 演示
# ============================================================

if __name__ == "__main__":
    print("龙虾-浏览器Agent会话管理器 v1.0 原型加载完成")
    print(f"协议#84 补充 | Session持久化 | Captcha三级策略 | MFA处理")
    
    # 演示会话管理
    sm = SessionManager()
    session = sm.save_session(
        account_id="demo_user",
        domain="https://example.com",
        cookies=[{"name": "token", "value": "abc123", "expires": time.time()+86400}],
        local_storage={"theme": "dark"},
        session_storage={}
    )
    print(f"\n会话已创建: account={session.account_id}, domain={session.domain}")
    
    loaded = sm.load_session("demo_user", "https://example.com")
    print(f"会话已加载: {'成功' if loaded else '失效'}")

```
