# captcha_resolver_v2.py

原始格式: Python

```python
"""
龙虾-验证码完整识别引擎 v2.0
协议#84 深度补充：数学滑块缺口检测 + 点选顺序识别 + 行为验证
"""

import numpy as np
import base64
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance

# ============================================================
# 图像预处理流水线
# ============================================================

class ImagePreprocessor:
    """统一图像预处理"""
    
    @staticmethod
    def to_grayscale(image: Image.Image) -> Image.Image:
        return image.convert("L")
    
    @staticmethod
    def threshold(image: Image.Image, threshold: int = 127) -> Image.Image:
        gray = ImagePreprocessor.to_grayscale(image)
        return gray.point(lambda p: 255 if p > threshold else 0)
    
    @staticmethod
    def denoise(image: Image.Image, radius: int = 2) -> Image.Image:
        return image.filter(ImageFilter.MedianFilter(radius))
    
    @staticmethod
    def enhance_edges(image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.FIND_EDGES)
    
    @staticmethod
    def normalize(image: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)


# ============================================================
# 1. 滑块验证码缺口检测
# ============================================================

class SliderGapDetector:
    """
    滑块缺口检测（模板匹配+边缘检测）
    算法：Canny边缘检测 → 模板匹配 → 缺口坐标定位
    """
    
    def __init__(self):
        self.sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        self.sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    def detect_gap(self, background_image: Image.Image, 
                  template_image: Optional[Image.Image] = None) -> Dict:
        """
        检测滑块缺口位置
        
        Args:
            background_image: 背景图（带缺口）
            template_image: 滑块模板（可选，自动提取）
        
        Returns:
            {"x": 缺口X坐标, "y": Y坐标, "confidence": 置信度, "method": 检测方法}
        """
        
        # 预处理
        bg_gray = ImagePreprocessor.to_grayscale(background_image)
        bg_array = np.array(bg_gray, dtype=np.float32)
        
        # 边缘检测
        edges = self._canny_edge(bg_array)
        
        # 方法1: 模板匹配（如有模板）
        if template_image is not None:
            result = self._template_match(edges, template_image)
            if result["confidence"] > 0.6:
                return result
        
        # 方法2: 缺口轮廓检测（无模板时）
        return self._contour_detect(edges, background_image.size)
    
    def _canny_edge(self, img_array: np.ndarray) -> np.ndarray:
        """简化Canny边缘检测"""
        # Sobel算子
        Gx = self._conv2d(img_array, self.sobel_x)
        Gy = self._conv2d(img_array, self.sobel_y)
        
        magnitude = np.sqrt(Gx**2 + Gy**2)
        direction = np.arctan2(Gy, Gx)
        
        # 非极大值抑制
        suppressed = self._non_max_suppression(magnitude, direction)
        
        # 双阈值
        high_thresh = np.percentile(suppressed, 90)
        low_thresh = high_thresh * 0.5
        edges = self._hysteresis(suppressed, low_thresh, high_thresh)
        
        return edges
    
    def _conv2d(self, img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        h, w = img.shape
        kh, kw = kernel.shape
        pad_h, pad_w = kh // 2, kw // 2
        padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        result = np.zeros_like(img)
        for i in range(h):
            for j in range(w):
                result[i, j] = np.sum(padded[i:i+kh, j:j+kw] * kernel)
        return result
    
    def _non_max_suppression(self, mag: np.ndarray, angle: np.ndarray) -> np.ndarray:
        h, w = mag.shape
        result = np.zeros_like(mag)
        angle = angle * 180 / np.pi % 180
        
        for i in range(1, h-1):
            for j in range(1, w-1):
                a = angle[i, j]
                if (0 <= a < 22.5) or (157.5 <= a < 180):
                    n1, n2 = mag[i, j+1], mag[i, j-1]
                elif 22.5 <= a < 67.5:
                    n1, n2 = mag[i-1, j+1], mag[i+1, j-1]
                elif 67.5 <= a < 112.5:
                    n1, n2 = mag[i-1, j], mag[i+1, j]
                else:
                    n1, n2 = mag[i-1, j-1], mag[i+1, j+1]
                
                result[i, j] = mag[i, j] if mag[i, j] >= max(n1, n2) else 0
        
        return result
    
    def _hysteresis(self, img: np.ndarray, low: float, high: float) -> np.ndarray:
        strong = img >= high
        weak = (img >= low) & (img < high)
        
        from collections import deque
        h, w = img.shape
        edges = strong.copy()
        q = deque()
        for i in range(h):
            for j in range(w):
                if strong[i, j]:
                    q.append((i, j))
        
        while q:
            i, j = q.popleft()
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < h and 0 <= nj < w and weak[ni, nj] and not edges[ni, nj]:
                        edges[ni, nj] = True
                        q.append((ni, nj))
        
        return edges.astype(np.uint8) * 255
    
    def _template_match(self, edges: np.ndarray, template: Image.Image) -> Dict:
        """模板匹配（NCC归一化互相关）"""
        tpl_gray = np.array(ImagePreprocessor.to_grayscale(template), dtype=np.float32)
        tpl_edges = self._canny_edge(tpl_gray)
        
        th, tw = tpl_edges.shape
        eh, ew = edges.shape
        
        if th > eh or tw > ew:
            return {"confidence": 0, "x": 0, "y": 0, "method": "template_match_failed"}
        
        # 滑动窗口NCC
        tpl_mean = np.mean(tpl_edges)
        tpl_std = np.std(tpl_edges)
        
        max_ncc = -1
        best_x, best_y = 0, 0
        
        for y in range(0, eh - th, 5):  # 步长5加速
            for x in range(0, ew - tw, 5):
                window = edges[y:y+th, x:x+tw]
                win_mean = np.mean(window)
                win_std = np.std(window)
                if win_std == 0 or tpl_std == 0:
                    continue
                ncc = np.mean((window - win_mean) * (tpl_edges - tpl_mean)) / (win_std * tpl_std)
                if ncc > max_ncc:
                    max_ncc = ncc
                    best_x, best_y = x, y
        
        return {
            "confidence": round(max_ncc, 3),
            "x": best_x + tw // 2,
            "y": best_y,
            "method": "template_matching_ncc"
        }
    
    def _contour_detect(self, edges: np.ndarray, img_size: Tuple[int, int]) -> Dict:
        """轮廓检测缺口位置"""
        w, h = img_size
        
        # 寻找最大外接矩形缺口（背景中亮度突变处）
        # 垂直投影：找到缺口边缘
        col_sum = np.sum(edges, axis=0)
        gradient = np.abs(np.diff(col_sum))
        
        if len(gradient) < 3:
            return {"confidence": 0, "x": w // 2, "y": h // 2, "method": "contour_fallback"}
        
        peak_idx = np.argmax(gradient)
        peak_value = gradient[peak_idx]
        max_grad = np.max(gradient)
        
        confidence = peak_value / max_grad if max_grad > 0 else 0
        
        return {
            "confidence": round(confidence, 3),
            "x": peak_idx + 1,
            "y": h // 2,
            "method": "contour_detection"
        }


# ============================================================
# 2. 点选验证码识别
# ============================================================

class ClickOrderRecognizer:
    """
    点选顺序识别
    识别图中文字/图标 → 按语序排序 → 输出点击坐标序列
    """
    
    # 中文语序映射表
    CN_ORDER_MAP = {
        "一": 0, "二": 1, "三": 2, "四": 3, "五": 4,
        "六": 5, "七": 6, "八": 7, "九": 8, "十": 9,
        "壹": 0, "贰": 1, "叁": 2, "肆": 3, "伍": 4,
        "甲": 0, "乙": 1, "丙": 2, "丁": 3,
        "A": 0, "B": 1, "C": 2, "D": 3, "E": 4,
        "1": 0, "2": 1, "3": 2, "4": 3, "5": 4,
        "①": 0, "②": 1, "③": 2, "④": 3, "⑤": 4,
    }
    
    def __init__(self):
        self.slider_detector = SliderGapDetector()
    
    def recognize_order(self, image: Image.Image, 
                       targets: List[str]) -> List[Dict]:
        """
        识别点选顺序
        
        Args:
            image: 验证码大图
            targets: 需点击的目标文字列表（如["甲", "丙", "乙"]）
        
        Returns:
            [{"text": "甲", "x": 120, "y": 45, "order": 1}, ...]
        """
        results = []
        
        # 分割子图（基于连通域）
        sub_images = self._segment_characters(image)
        
        for i, (sub_img, bbox) in enumerate(sub_images):
            # OCR识别（简化：位置映射）
            # 实际需集成PaddleOCR/Tesseract
            recognized = self._ocr_single(sub_img)
            
            if recognized in self.CN_ORDER_MAP:
                order = self.CN_ORDER_MAP[recognized]
                results.append({
                    "text": recognized,
                    "x": bbox[0] + bbox[2] // 2,
                    "y": bbox[1] + bbox[3] // 2,
                    "order": order
                })
        
        # 按order排序
        results.sort(key=lambda r: r.get("order", 999))
        return results
    
    def _segment_characters(self, image: Image.Image) -> List[Tuple]:
        """字符分割（连通域分析）"""
        gray = ImagePreprocessor.to_grayscale(image)
        binary = ImagePreprocessor.threshold(image, 150)
        arr = np.array(binary)
        
        # 连通域标注
        from collections import deque
        h, w = arr.shape
        visited = np.zeros((h, w), dtype=bool)
        components = []
        
        for y in range(h):
            for x in range(w):
                if arr[y, x] < 128 and not visited[y, x]:
                    # BFS连通域
                    q = deque([(y, x)])
                    min_x, min_y = x, y
                    max_x, max_y = x, y
                    
                    while q:
                        cy, cx = q.popleft()
                        if visited[cy, cx]:
                            continue
                        visited[cy, cx] = True
                        min_x, min_y = min(min_x, cx), min(min_y, cy)
                        max_x, max_y = max(max_x, cx), max(max_y, cy)
                        
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                ny, nx = cy+dy, cx+dx
                                if 0 <= ny < h and 0 <= nx < w and arr[ny, nx] < 128 and not visited[ny, nx]:
                                    q.append((ny, nx))
                    
                    # 过滤噪点（面积>50像素）
                    area = (max_x - min_x) * (max_y - min_y)
                    if area > 50:
                        sub = image.crop((min_x, min_y, max_x+1, max_y+1))
                        components.append((sub, (min_x, min_y, max_x-min_x, max_y-min_y)))
        
        return components
    
    def _ocr_single(self, _image: Image.Image) -> str:
        """单字符识别（需集成PaddleOCR）"""
        return ""  # 占位，返回空表示需Fallback


# ============================================================
# 3. 行为验证模拟
# ============================================================

class BehaviorSimulator:
    """
    行为验证模拟器
    模拟人类鼠标轨迹（加速→匀速→减速→微调）
    """
    
    @staticmethod
    def generate_trajectory(start_x: int, start_y: int, 
                           target_x: int, target_y: int,
                           duration_ms: float = 800) -> List[Dict]:
        """生成人类鼠标轨迹"""
        
        points = []
        total_distance = np.sqrt((target_x - start_x)**2 + (target_y - start_y)**2)
        num_points = int(duration_ms / 10)  # 每10ms一个点
        
        for i in range(num_points):
            t = i / num_points
            
            # 缓动函数（贝塞尔曲线）
            eased = BehaviorSimulator._ease_out_cubic(t)
            
            # 当前位置
            cx = start_x + (target_x - start_x) * eased
            cy = start_y + (target_y - start_y) * eased
            
            # 加入人类随机扰动（2-5px Gaussian）
            cx += np.random.normal(0, 3 if t < 0.7 else 1)
            cy += np.random.normal(0, 2)
            
            # 中间微停顿（模拟犹豫）
            if 0.3 < t < 0.35:
                cy += np.random.normal(0, 8)
            if 0.7 < t < 0.75:
                cx += np.random.normal(0, 5)
            
            points.append({"x": round(cx, 1), "y": round(cy, 1), "t": i * 10})
        
        return points
    
    @staticmethod
    def _ease_out_cubic(t: float) -> float:
        return 1 - (1 - t) ** 3
    
    @staticmethod
    def generate_click_pattern(num_clicks: int = 3) -> List[Dict]:
        """生成点击时序（人类点击间隔分布）"""
        clicks = []
        intervals = np.random.gamma(shape=2, scale=0.4, size=num_clicks - 1)
        # Gamma分布模拟人类点击间隔：均值~800ms，方差~320ms
        
        total = 0
        for i in range(num_clicks):
            clicks.append({
                "click_id": i,
                "timestamp_ms": total,
                "duration_ms": np.random.normal(80, 20)  # 按下到释放
            })
            if i < num_clicks - 1:
                total += max(intervals[i] * 1000, 200)
        
        return clicks


# ============================================================
# 4. 统一验证码识别器（三层策略）
# ============================================================

class UnifiedCaptchaSolver:
    """
    统一验证码识别器
    整合：滑块缺口检测 | 点选顺序识别 | 行为验证模拟 | 图片文字OCR
    """
    
    CAPTCHA_TYPES = {
        "slider": {"detector": "slider", "strategy": "gap_detection"},
        "click_order": {"detector": "click", "strategy": "ocr+order"},
        "image_text": {"detector": "ocr", "strategy": "cnn_ocr"},
        "behavior": {"detector": "behavior", "strategy": "trajectory"},
        "reCAPTCHA": {"detector": "recaptcha", "strategy": "audio_fallback"},
    }
    
    def __init__(self):
        self.slider = SliderGapDetector()
        self.click = ClickOrderRecognizer()
        self.behavior = BehaviorSimulator()
        self.stats = {"solved": 0, "failed": 0, "fallback": 0}
    
    def solve(self, captcha_type: str, **kwargs) -> Dict:
        """
        主入口：识别验证码
        
        Args:
            captcha_type: slider / click_order / image_text / behavior / reCAPTCHA
            **kwargs: 类型特定参数
        
        Returns:
            {
                "success": bool,
                "result": {...},     # 类型特定结果
                "confidence": float, # 置信度
                "strategy": str,     # 使用的策略
                "fallback": bool     # 是否触发fallback
            }
        """
        
        if captcha_type not in self.CAPTCHA_TYPES:
            return {"success": False, "error": f"Unknown captcha type: {captcha_type}"}
        
        try:
            if captcha_type == "slider":
                return self._solve_slider(kwargs)
            elif captcha_type == "click_order":
                return self._solve_click_order(kwargs)
            elif captcha_type == "image_text":
                return self._solve_image_text(kwargs)
            elif captcha_type == "behavior":
                return self._solve_behavior(kwargs)
            elif captcha_type == "reCAPTCHA":
                return self._solve_recaptcha(kwargs)
        except Exception as e:
            self.stats["failed"] += 1
            return {"success": False, "error": str(e), "fallback": True}
    
    def _solve_slider(self, kwargs: Dict) -> Dict:
        """解决滑块验证码"""
        bg = kwargs.get("background_image")  # PIL Image
        tpl = kwargs.get("template_image")   # PIL Image or None
        
        if bg is None:
            return {"success": False, "error": "Missing background_image"}
        
        result = self.slider.detect_gap(bg, tpl)
        
        if result["confidence"] < 0.5:
            self.stats["fallback"] += 1
            return {
                "success": False,
                "result": result,
                "confidence": result["confidence"],
                "strategy": "gap_detection_low_confidence",
                "fallback": True,
                "fallback_msg": "缺口检测置信度不足，建议人工处理"
            }
        
        # 生成拖动轨迹
        trajectory = self.behavior.generate_trajectory(0, result["y"], result["x"], result["y"])
        
        self.stats["solved"] += 1
        return {
            "success": True,
            "result": {
                "gap_x": result["x"],
                "gap_y": result["y"],
                "trajectory": trajectory[:20],  # 前20个轨迹点
                "duration_ms": len(trajectory) * 10
            },
            "confidence": result["confidence"],
            "strategy": "slider_gap_detection"
        }
    
    def _solve_click_order(self, kwargs: Dict) -> Dict:
        """解决点选验证码"""
        image = kwargs.get("image")
        targets = kwargs.get("targets", [])
        
        if image is None:
            return {"success": False, "error": "Missing image"}
        
        results = self.click.recognize_order(image, targets)
        
        if not results:
            self.stats["fallback"] += 1
            return {
                "success": False,
                "result": [],
                "strategy": "ocr_fallback",
                "fallback": True,
                "fallback_msg": "未识别到有效文字，需人工处理或接入PaddleOCR"
            }
        
        self.stats["solved"] += 1
        return {
            "success": True,
            "result": results,
            "confidence": 0.8,
            "strategy": "click_order_recognition"
        }
    
    def _solve_image_text(self, kwargs: Dict) -> Dict:
        """解决图片文字验证码"""
        image = kwargs.get("image")
        
        if image is None:
            return {"success": False, "error": "Missing image"}
        
        # OCR识别（需PaddleOCR/Tesseract）
        return {
            "success": False,
            "result": {"text": ""},
            "strategy": "ocr_not_configured",
            "fallback": True,
            "fallback_msg": "OCR引擎未配置，请安装PaddleOCR或Tesseract"
        }
    
    def _solve_behavior(self, kwargs: Dict) -> Dict:
        """解决行为验证（始终成功）"""
        num_clicks = kwargs.get("num_clicks", 1)
        start = kwargs.get("start", (0, 0))
        target = kwargs.get("target", (200, 200))
        
        trajectory = self.behavior.generate_trajectory(
            start[0], start[1], target[0], target[1]
        )
        clicks = self.behavior.generate_click_pattern(num_clicks)
        
        self.stats["solved"] += 1
        return {
            "success": True,
            "result": {
                "trajectory": trajectory,
                "click_pattern": clicks
            },
            "confidence": 0.95,
            "strategy": "behavior_simulation"
        }
    
    def _solve_recaptcha(self, _kwargs: Dict) -> Dict:
        return {
            "success": False,
            "result": {},
            "strategy": "audio_fallback",
            "fallback": True,
            "fallback_msg": "reCAPTCHA需音频Fallback通道，建议人工介入"
        }


# ============================================================
# 演示
# ============================================================

if __name__ == "__main__":
    print("龙虾-验证码完整识别引擎 v2.0 原型加载完成")
    print(f"协议#84 深度补充 | 滑块缺口检测 | 点选顺序识别 | 行为模拟")
    
    solver = UnifiedCaptchaSolver()
    
    # 测试行为验证
    result = solver.solve("behavior", num_clicks=3, start=(50, 100), target=(300, 250))
    print(f"\n行为验证: success={result['success']}, strategy={result['strategy']}")
    print(f"  轨迹点数: {len(result['result']['trajectory'])}")
    print(f"  点击次数: {len(result['result']['click_pattern'])}")
    
    # 测试滑块（无实际图片时返回fallback）
    from PIL import Image as PILImage
    dummy = PILImage.new("RGB", (400, 200), "white")
    result2 = solver.solve("slider", background_image=dummy)
    print(f"\n滑块检测: success={result2['success']}, fallback={result2.get('fallback')}")
    
    print(f"\n统计: solved={solver.stats['solved']}, failed={solver.stats['failed']}, fallback={solver.stats['fallback']}")

```
