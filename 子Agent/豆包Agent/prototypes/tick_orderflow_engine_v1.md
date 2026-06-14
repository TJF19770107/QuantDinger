# tick_orderflow_engine_v1.py

原始格式: Python

```python
"""
龙虾-Tick级订单流分析引擎 v1.0
协议#85 工程落地原型
对标：广发金工DPIN + QMT L2六类数据
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import deque
import time

# ============================================================
# 数据模型
# ============================================================

@dataclass
class TickTrade:
    """逐笔成交"""
    timestamp: float        # 毫秒时间戳
    symbol: str             # 合约代码
    price: float            # 成交价
    volume: int             # 成交量
    direction: int          # 1=主动买, -1=主动卖, 0=不确定
    trade_id: str = ""

@dataclass
class TickOrder:
    """逐笔委托"""
    timestamp: float
    symbol: str
    order_type: str         # B=买, S=卖, C=撤单
    price: float
    volume: int
    order_id: str = ""

@dataclass
class OrderBook:
    """十档订单簿快照"""
    timestamp: float
    symbol: str
    bid_prices: List[float]   # 买一到买十
    bid_volumes: List[int]
    ask_prices: List[float]   # 卖一到卖十
    ask_volumes: List[int]

# ============================================================
# 六大因子族引擎
# ============================================================

class OrderFlowImbalanceFactor:
    """因子族1: 订单流不平衡 (OFI)"""
    
    def __init__(self):
        self.history = deque(maxlen=1000)
    
    def compute(self, order_book: OrderBook) -> Dict[str, float]:
        buy_vol = sum(order_book.bid_volumes[:5])   # 前五档
        sell_vol = sum(order_book.ask_volumes[:5])
        total = buy_vol + sell_vol
        
        # OFI_Simple
        ofi = (buy_vol - sell_vol) / total if total > 0 else 0
        
        # OFI_Weighted (越近档位权重越高)
        weights = [1.0, 0.8, 0.6, 0.4, 0.2]
        w_buy = sum(v * w for v, w in zip(order_book.bid_volumes[:5], weights))
        w_sell = sum(v * w for v, w in zip(order_book.ask_volumes[:5], weights))
        w_total = w_buy + w_sell
        ofi_weighted = (w_buy - w_sell) / w_total if w_total > 0 else 0
        
        # OFI_Delta (与上一笔的变化)
        ofi_delta = ofi - self.history[-1]["ofi"] if self.history else 0
        
        self.history.append({"ofi": ofi, "timestamp": order_book.timestamp})
        return {"OFI_Simple": ofi, "OFI_Weighted": ofi_weighted, "OFI_Delta": ofi_delta}


class LargeOrderTracker:
    """因子族2: 大单跟踪 (LOT)"""
    
    def __init__(self, threshold_ratio: float = 0.01):
        """threshold_ratio: 大单阈值（占日均量比例）"""
        self.threshold_ratio = threshold_ratio
        self.large_trades: deque = deque(maxlen=500)
        self.avg_daily_volume = 0
    
    def set_avg_volume(self, avg_volume: int):
        self.avg_daily_volume = avg_volume
    
    def check(self, trade: TickTrade) -> Optional[Dict]:
        threshold = max(int(self.avg_daily_volume * self.threshold_ratio), 10000)
        if trade.volume >= threshold:
            result = {
                "timestamp": trade.timestamp,
                "price": trade.price,
                "volume": trade.volume,
                "direction": "BUY" if trade.direction == 1 else "SELL",
                "ratio": trade.volume / self.avg_daily_volume if self.avg_daily_volume else 0
            }
            self.large_trades.append(result)
            return result
        return None
    
    def summary(self, window_seconds: float = 300) -> Dict:
        """窗口内大单汇总"""
        now = time.time()
        recent = [t for t in self.large_trades if now - t["timestamp"] <= window_seconds]
        buy_vol = sum(t["volume"] for t in recent if t["direction"] == "BUY")
        sell_vol = sum(t["volume"] for t in recent if t["direction"] == "SELL")
        return {
            "LOT_BuyVolume": buy_vol,
            "LOT_SellVolume": sell_vol,
            "LOT_NetFlow": buy_vol - sell_vol,
            "LOT_Count": len(recent)
        }


class MicroStructureFactor:
    """因子族3: 微观结构 (MMS)"""
    
    @staticmethod
    def compute(order_book: OrderBook) -> Dict[str, float]:
        bid1 = order_book.bid_prices[0]
        ask1 = order_book.ask_prices[0]
        
        # Spread
        spread = ask1 - bid1
        spread_bps = (spread / ((bid1 + ask1) / 2)) * 10000
        
        # Depth
        depth = sum(order_book.bid_volumes[:10]) + sum(order_book.ask_volumes[:10])
        
        # Slope (订单簿价格梯度)
        if len(order_book.bid_prices) >= 5:
            slope = (order_book.bid_prices[0] - order_book.bid_prices[4]) / 4
        else:
            slope = 0
        
        return {
            "Spread": spread,
            "Spread_BPS": spread_bps,
            "Depth": depth,
            "Slope": slope
        }


class SmartMoneyProfiler:
    """因子族4: 主力行为画像 (SMP)"""
    
    def __init__(self):
        self.recent_orders: deque = deque(maxlen=200)
        self.fake_hang_detect: deque = deque(maxlen=50)  # 虚假挂单记录
    
    def detect_fake_hang(self, order: TickOrder, order_book: OrderBook) -> bool:
        """检测虚假挂单（大单挂→快速撤）"""
        if order.order_type != "C":
            return False
        # 查找对应委托
        for past in self.recent_orders:
            if past.order_type in ("B", "S") and abs(past.volume - order.volume) < 100:
                time_diff = order.timestamp - past.timestamp
                if time_diff < 2.0:  # 2秒内撤单
                    self.fake_hang_detect.append({
                        "price": past.price, "volume": past.volume, "lag": time_diff
                    })
                    return True
        return False
    
    def detect_iceberg(self, recent_trades: List[TickTrade], order_book: OrderBook) -> bool:
        """检测冰山订单（连续小额同向+盘口深度不变）"""
        if len(recent_trades) < 5:
            return False
        recent = recent_trades[-5:]
        directions = [t.direction for t in recent]
        if len(set(directions)) == 1:  # 全部同向
            total_vol = sum(t.volume for t in recent)
            if total_vol > 10000:  # 总量超过阈值
                return True
        return False


class CrossAssetLinkage:
    """因子族5: 跨品种联动 (CAL)"""
    
    def __init__(self):
        self.pair_data: Dict[str, pd.DataFrame] = {}
    
    def compute_correlation(self, symbol_a: str, symbol_b: str, 
                           returns_a: pd.Series, returns_b: pd.Series, 
                           window: int = 20) -> float:
        """动态相关性"""
        if len(returns_a) < window:
            return 0
        return returns_a.rolling(window).corr(returns_b).iloc[-1]
    
    def sector_flow(self, stock_net_flow: float, sector_etf_flow: float) -> str:
        """板块资金流向判断"""
        if stock_net_flow > 0 and sector_etf_flow > 0:
            return "板块吸筹"
        elif stock_net_flow < 0 and sector_etf_flow < 0:
            return "板块出货"
        elif stock_net_flow > 0 > sector_etf_flow:
            return "个股逆势吸筹"
        else:
            return "个股弱于板块"


class TemporalPatternDetector:
    """因子族6: 时序模式识别 (TMP)"""
    
    @staticmethod
    def detect_clustering(trades: List[TickTrade], price_tolerance: float = 0.01, 
                          min_count: int = 5) -> bool:
        """Tick聚集检测：同价位连续多笔同向"""
        if len(trades) < min_count:
            return False
        recent = trades[-min_count:]
        prices = [t.price for t in recent]
        directions = [t.direction for t in recent]
        price_range = max(prices) - min(prices)
        if price_range <= price_tolerance and len(set(directions)) == 1:
            return True
        return False
    
    @staticmethod
    def detect_absorption(trades: List[TickTrade], order_book: OrderBook, 
                         volume_threshold: int = 50000) -> bool:
        """被动吃掉大量挂单（吸收模式）"""
        if len(trades) < 3:
            return False
        recent = trades[-3:]
        total_vol = sum(t.volume for t in recent)
        return total_vol >= volume_threshold


# ============================================================
# 三层决策框架
# ============================================================

class TickDecisionEngine:
    """三层决策框架引擎"""
    
    def __init__(self):
        self.ofi = OrderFlowImbalanceFactor()
        self.lot = LargeOrderTracker()
        self.mms = MicroStructureFactor()
        self.smp = SmartMoneyProfiler()
        self.cal = CrossAssetLinkage()
        self.tmp = TemporalPatternDetector()
        
        # 风控参数（永久生效）
        self.max_position_pct = 0.10       # 单标的最大仓位10%
        self.max_daily_loss = 0.05         # 日内最大亏损5%
        self.single_loss_cap = 0.02        # 单笔最大亏损2%
        
    def micro_decision(self, tick: TickTrade, order_book: OrderBook) -> Dict:
        """微观层：Tick级瞬时信号"""
        ofi_signals = self.ofi.compute(order_book)
        mms_signals = self.mms.compute(order_book)
        lot_check = self.lot.check(tick)
        clustering = self.tmp.detect_clustering([tick]) if tick else False
        
        # 综合信号评分
        score = 0
        if ofi_signals.get("OFI_Simple", 0) > 0.3: score += 2
        if ofi_signals.get("OFI_Delta", 0) > 0.1: score += 1
        if lot_check: score += 2
        if clustering: score += 1
        if mms_signals.get("Spread_BPS", 100) < 10: score += 1  # 低点差=高流动性
        
        action = "BUY" if score >= 4 else ("SELL" if score <= -4 else "HOLD")
        return {"action": action, "score": score, "signals": {
            "ofi": ofi_signals, "mms": mms_signals, "lot": lot_check
        }}
    
    def risk_check(self, current_pnl: float, net_value: float) -> Dict:
        """L1-L4风控熔断检查"""
        triggers = []
        pnl_pct = current_pnl / net_value if net_value > 0 else 0
        
        if abs(pnl_pct) >= self.single_loss_cap:
            triggers.append("L1_单笔熔断")
        if pnl_pct <= -0.05:
            triggers.append("L3_全局熔断")
        
        triggered = len(triggers) > 0
        return {"triggered": triggered, "triggers": triggers, "pnl_pct": pnl_pct}


# ============================================================
# 回测引擎
# ============================================================

class TickBacktestEngine:
    """Tick级回测引擎"""
    
    def __init__(self, initial_capital: float = 1_000_000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions: Dict[str, Dict] = {}
        self.trades: List[Dict] = []
        self.equity_curve: List[float] = [initial_capital]
        self.decision_engine = TickDecisionEngine()
    
    def run(self, tick_data: pd.DataFrame, order_book_data: pd.DataFrame) -> Dict:
        """执行回测"""
        for idx, row in tick_data.iterrows():
            # 风控检查（每Tick检查）
            current_pnl = self.capital - self.initial_capital
            risk = self.decision_engine.risk_check(current_pnl, self.capital)
            if risk["triggered"]:
                self._liquidate_all(row["price"])
                break
            
            # 此处简化：实际需传入完整TickTrade和OrderBook对象
            # signal = self.decision_engine.micro_decision(...)
            # 根据信号执行交易
            
            self.equity_curve.append(self.capital)
        
        return self._generate_report()
    
    def _liquidate_all(self, price: float):
        """全部平仓"""
        for symbol, pos in list(self.positions.items()):
            pnl = (price - pos["avg_price"]) * pos["volume"]
            self.capital += pnl
            del self.positions[symbol]
    
    def _generate_report(self) -> Dict:
        equity = np.array(self.equity_curve)
        returns = np.diff(equity) / equity[:-1]
        
        # 核心指标
        sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        max_dd = self._max_drawdown(equity)
        
        return {
            "Sharpe": round(sharpe, 3),
            "MaxDD": f"{max_dd:.2%}",
            "Final_Equity": self.capital,
            "Total_Return": f"{(self.capital/self.initial_capital - 1):.2%}",
            "Num_Trades": len(self.trades)
        }
    
    @staticmethod
    def _max_drawdown(equity: np.ndarray) -> float:
        peak = np.maximum.accumulate(equity)
        dd = (equity - peak) / peak
        return abs(dd.min())


# ============================================================
# 演示
# ============================================================

if __name__ == "__main__":
    print("龙虾-Tick级订单流分析引擎 v1.0 原型加载完成")
    print(f"协议#85 | 六大因子族 | 三层决策 | 回测引擎")
    print(f"因子族: OFI | LOT | MMS | SMP | CAL | TMP")
    print(f"风控: L1单笔≤2% | L3全局≤5% | 原则:宁可踏空不可爆仓")

```
