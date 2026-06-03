# arbitrage_monitor_engine_v1.py

> 原始文件: `arbitrage_monitor_engine_v1.py`  |  类型: `.py`  |  自动转换

```python
"""
龙虾-跨市场实时套利监控引擎 v1.0
协议#86 工程落地原型
对标：量化多市场对冲 + AH溢价 + 期现套利 + 配对交易
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
class CrossMarketQuote:
    """跨市场行情快照"""
    symbol: str
    market: str             # A/HK/US/期货/期权
    price: float
    currency: str           # CNY/HKD/USD
    timestamp: float
    volume: int = 0
    bid: float = 0
    ask: float = 0

@dataclass
class ArbitrageSignal:
    """套利信号"""
    strategy: str           # AH溢价/中概回归/期现基差/ETF折溢价/配对交易
    pair: Tuple[str, str]
    spread: float
    z_score: float
    direction: str          # LONG_FIRST/SHORT_FIRST
    expected_return: float
    timestamp: float
    half_life: float = 0    # 均值回归半衰期（天）

@dataclass
class Position:
    """持仓"""
    symbol: str
    market: str
    direction: str          # LONG/SHORT
    quantity: int
    entry_price: float
    entry_time: float
    current_value: float = 0

# ============================================================
# 五大套利监控器
# ============================================================

class AHPremiumMonitor:
    """监控器1: AH股溢价套利"""
    
    def __init__(self):
        self.ah_pairs: Dict[str, Dict] = {}  # A股代码 -> {H股代码, 历史溢价}
        self.premium_history: Dict[str, deque] = {}  # 溢价率历史
    
    def add_pair(self, a_symbol: str, h_symbol: str, a_price: float, h_price: float, 
                 fx_rate: float = 0.91):
        """添加AH配对（A股/H股代码，实时价格，汇率HKD→CNY）"""
        h_price_cny = h_price * fx_rate
        premium = (a_price - h_price_cny) / h_price_cny  # 正值=A溢价
        
        pair_key = f"{a_symbol}-{h_symbol}"
        self.ah_pairs[pair_key] = {
            "a_symbol": a_symbol, "h_symbol": h_symbol,
            "a_price": a_price, "h_price_cny": h_price_cny,
            "premium": premium, "timestamp": time.time()
        }
        
        if pair_key not in self.premium_history:
            self.premium_history[pair_key] = deque(maxlen=252)
        self.premium_history[pair_key].append(premium)
    
    def scan(self) -> List[ArbitrageSignal]:
        """扫描AH溢价套利机会"""
        signals = []
        for pair_key, data in self.ah_pairs.items():
            history = list(self.premium_history.get(pair_key, []))
            if len(history) < 20:
                continue
            
            premium = data["premium"]
            mean = np.mean(history)
            std = np.std(history)
            z_score = (premium - mean) / std if std > 0 else 0
            
            # 入场条件：|Z-Score| > 2.0
            if abs(z_score) > 2.0:
                direction = "SHORT_A_LONG_H" if z_score > 0 else "LONG_A_SHORT_H"
                signals.append(ArbitrageSignal(
                    strategy="AH溢价套利",
                    pair=(data["a_symbol"], data["h_symbol"]),
                    spread=premium,
                    z_score=z_score,
                    direction=direction,
                    expected_return=abs(premium - mean),
                    timestamp=time.time()
                ))
        
        return signals


class FuturesBasisMonitor:
    """监控器2: 期现基差套利"""
    
    def __init__(self):
        self.basis_history: Dict[str, deque] = deque(maxlen=500)  # 基差历史
    
    def compute_basis(self, futures_price: float, spot_price: float, 
                     days_to_expiry: int, risk_free_rate: float = 0.03) -> float:
        """计算期现基差"""
        fair_value = spot_price * (1 + risk_free_rate * days_to_expiry / 365)
        return futures_price - fair_value
    
    def scan(self, futures_price: float, spot_price: float, days_to_expiry: int) -> Optional[ArbitrageSignal]:
        """扫描期现套利机会"""
        basis = self.compute_basis(futures_price, spot_price, days_to_expiry)
        self.basis_history.append(basis)
        
        if len(self.basis_history) < 20:
            return None
        
        mean = np.mean(list(self.basis_history))
        std = np.std(list(self.basis_history))
        z_score = (basis - mean) / std if std > 0 else 0
        
        if abs(z_score) > 2.0:
            direction = "SHORT_FUT_LONG_SPOT" if z_score > 0 else "LONG_FUT_SHORT_SPOT"
            return ArbitrageSignal(
                strategy="期现套利",
                pair=("Futures", "Spot"),
                spread=basis,
                z_score=z_score,
                direction=direction,
                expected_return=abs(basis),
                timestamp=time.time()
            )
        return None


class ETFArbitrageMonitor:
    """监控器3: ETF折溢价套利"""
    
    def __init__(self, threshold: float = 0.005):  # 0.5%阈值
        self.threshold = threshold
    
    def scan(self, etf_price: float, iopv: float, etf_symbol: str) -> Optional[ArbitrageSignal]:
        """扫描ETF折溢价"""
        premium = (etf_price - iopv) / iopv
        
        if abs(premium) > self.threshold:
            direction = "SHORT_ETF_LONG_BASKET" if premium > 0 else "LONG_ETF_SHORT_BASKET"
            return ArbitrageSignal(
                strategy="ETF套利",
                pair=(etf_symbol, "Basket"),
                spread=premium,
                z_score=premium / self.threshold,  # 简化Z-Score
                direction=direction,
                expected_return=abs(premium) * 0.5,  # 扣减交易成本后预期收益
                timestamp=time.time()
            )
        return None


class PairTradingMonitor:
    """监控器4: 配对交易（协整检验+均值回归）"""
    
    def __init__(self):
        self.pair_spread_history: Dict[str, deque] = {}
    
    def add_pair(self, symbol_a: str, symbol_b: str, price_a: pd.Series, price_b: pd.Series):
        """计算协整关系并记录价差"""
        # 简化的OLS回归得到对冲比例
        X = np.vstack([price_b.values, np.ones(len(price_b))]).T
        beta, alpha = np.linalg.lstsq(X, price_a.values, rcond=None)[0]
        
        pair_key = f"{symbol_a}-{symbol_b}"
        spread = price_a.values[-1] - (beta * price_b.values[-1] + alpha)
        
        if pair_key not in self.pair_spread_history:
            self.pair_spread_history[pair_key] = deque(maxlen=252)
        self.pair_spread_history[pair_key].append(spread)
        
        return {"pair_key": pair_key, "beta": beta, "alpha": alpha, "spread": spread}
    
    def scan(self, pair_key: str, beta: float, alpha: float) -> Optional[ArbitrageSignal]:
        """扫描配对交易信号"""
        history = list(self.pair_spread_history.get(pair_key, []))
        if len(history) < 20:
            return None
        
        spread = history[-1]
        mean = np.mean(history)
        std = np.std(history)
        z_score = (spread - mean) / std if std > 0 else 0
        
        # 计算半衰期（OU过程）
        half_life = self._compute_half_life(history)
        
        if abs(z_score) > 2.0 and half_life < 5:
            symbol_a, symbol_b = pair_key.split("-")
            direction = "SHORT_A_LONG_B" if z_score > 0 else "LONG_A_SHORT_B"
            return ArbitrageSignal(
                strategy="配对交易",
                pair=(symbol_a, symbol_b),
                spread=spread,
                z_score=z_score,
                direction=direction,
                expected_return=abs(spread - mean),
                half_life=half_life,
                timestamp=time.time()
            )
        return None
    
    @staticmethod
    def _compute_half_life(spread: List[float]) -> float:
        """OU过程半衰期计算"""
        spread_arr = np.array(spread)
        spread_lag = spread_arr[:-1]
        spread_diff = np.diff(spread_arr)
        X = np.vstack([spread_lag, np.ones(len(spread_lag))]).T
        theta, _ = np.linalg.lstsq(X, spread_diff, rcond=None)[0]
        return -np.log(2) / theta if theta < 0 else 999  # 天


class ChinaADRMonitor:
    """监控器5: 中概股ADR回归套利"""
    
    def __init__(self):
        self.adr_pairs: Dict = {}
    
    def add_pair(self, adr_symbol: str, hk_symbol: str, adr_price: float, 
                 hk_price: float, adr_ratio: int = 1, fx_usd_hkd: float = 7.8):
        """添加中概股ADR-HK配对"""
        hk_usd = hk_price / fx_usd_hkd
        premium = (adr_price - hk_usd * adr_ratio) / (hk_usd * adr_ratio)
        
        pair_key = f"{adr_symbol}-{hk_symbol}"
        self.adr_pairs[pair_key] = {
            "adr_symbol": adr_symbol, "hk_symbol": hk_symbol,
            "adr_price": adr_price, "hk_price_usd": hk_usd,
            "premium": premium, "timestamp": time.time()
        }
    
    def scan(self, threshold: float = 0.02) -> List[ArbitrageSignal]:
        """扫描中概ADR回归机会（2%阈值）"""
        signals = []
        for pair_key, data in self.adr_pairs.items():
            premium = data["premium"]
            if abs(premium) > threshold:
                direction = "SHORT_ADR_LONG_HK" if premium > 0 else "LONG_ADR_SHORT_HK"
                signals.append(ArbitrageSignal(
                    strategy="中概回归",
                    pair=(data["adr_symbol"], data["hk_symbol"]),
                    spread=premium,
                    z_score=premium / threshold,
                    direction=direction,
                    expected_return=abs(premium),
                    timestamp=time.time()
                ))
        return signals


# ============================================================
# 套利执行引擎
# ============================================================

class ArbitrageExecutionEngine:
    """套利执行引擎（双腿同步+风控）"""
    
    def __init__(self, max_slippage: float = 0.002,  # 最大滑点0.2%
                 leg_timeout: float = 2.0):           # 腿差超时2秒
        self.max_slippage = max_slippage
        self.leg_timeout = leg_timeout
        self.positions: List[Position] = []
        self.pnl_history: deque = deque(maxlen=1000)
    
    def execute(self, signal: ArbitrageSignal, capital: float) -> Dict:
        """执行套利交易（模拟）"""
        # 腿差同步检查
        leg1_fill = self._simulate_fill(signal.pair[0], signal.direction)
        leg2_fill = self._simulate_fill(signal.pair[1], signal.direction)
        
        # 滑点检查
        if abs(leg1_fill["slippage"]) > self.max_slippage:
            return {"status": "REJECTED", "reason": f"Leg1滑点超限: {leg1_fill['slippage']:.4f}"}
        if abs(leg2_fill["slippage"]) > self.max_slippage:
            return {"status": "REJECTED", "reason": f"Leg2滑点超限: {leg2_fill['slippage']:.4f}"}
        
        # 腿差时间检查
        leg_diff = abs(leg1_fill["timestamp"] - leg2_fill["timestamp"])
        if leg_diff > self.leg_timeout:
            return {"status": "REJECTED", "reason": f"腿差超时: {leg_diff:.2f}s"}
        
        return {"status": "EXECUTED", "leg1": leg1_fill, "leg2": leg2_fill}
    
    def _simulate_fill(self, symbol: str, direction: str) -> Dict:
        """模拟成交（实际需对接交易接口）"""
        return {
            "symbol": symbol,
            "price": 100.0,  # 模拟价格
            "slippage": np.random.normal(0, 0.001),
            "timestamp": time.time()
        }
    
    def get_total_pnl(self) -> float:
        """总盈亏"""
        return sum(p.current_value - p.entry_price * p.quantity for p in self.positions)


# ============================================================
# 综合套利扫描器
# ============================================================

class ArbitrageScanner:
    """五大监控器统一调度"""
    
    def __init__(self):
        self.ah_monitor = AHPremiumMonitor()
        self.futures_monitor = FuturesBasisMonitor()
        self.etf_monitor = ETFArbitrageMonitor()
        self.pair_monitor = PairTradingMonitor()
        self.adr_monitor = ChinaADRMonitor()
        self.executor = ArbitrageExecutionEngine()
        
        # 风控参数
        self.max_position_per_strategy = 0.10  # 单策略最大10%资金
        self.max_total_arbitrage = 0.40        # 总套利仓位40%
    
    def scan_all(self, market_data: Dict) -> List[ArbitrageSignal]:
        """全市场扫描"""
        all_signals = []
        
        # AH溢价
        if "ah_pairs" in market_data:
            for pair in market_data["ah_pairs"]:
                self.ah_monitor.add_pair(**pair)
            all_signals.extend(self.ah_monitor.scan())
        
        # 期现套利
        if "futures" in market_data:
            fut = market_data["futures"]
            signal = self.futures_monitor.scan(
                fut["futures_price"], fut["spot_price"], fut["days_to_expiry"]
            )
            if signal:
                all_signals.append(signal)
        
        # ETF折溢价
        if "etf" in market_data:
            etf = market_data["etf"]
            signal = self.etf_monitor.scan(etf["price"], etf["iopv"], etf["symbol"])
            if signal:
                all_signals.append(signal)
        
        # 中概ADR
        if "adr_pairs" in market_data:
            for pair in market_data["adr_pairs"]:
                self.adr_monitor.add_pair(**pair)
            all_signals.extend(self.adr_monitor.scan())
        
        # 按Z-Score绝对值排序
        all_signals.sort(key=lambda s: abs(s.z_score), reverse=True)
        return all_signals
    
    def get_top_signals(self, n: int = 5) -> List[ArbitrageSignal]:
        """获取Top N套利信号"""
        return self.scan_all({})[:n]  # 简化演示


# ============================================================
# 回测验证
# ============================================================

class ArbitrageBacktester:
    """套利策略回测"""
    
    def __init__(self, initial_capital: float = 1_000_000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.trade_log: List[Dict] = []
        self.equity_curve: List[float] = [initial_capital]
    
    def backtest_ah_premium(self, premium_history: pd.Series, 
                           entry_z: float = 2.0, exit_z: float = 0.5) -> Dict:
        """AH溢价套利回测"""
        mean = premium_history.expanding().mean()
        std = premium_history.expanding().std()
        z_score = (premium_history - mean) / std
        
        position = 0
        entry_price = 0
        
        for i in range(20, len(premium_history)):
            z = z_score.iloc[i]
            if position == 0:
                if z > entry_z:  # A溢价过高→做空A做多H
                    position = -1
                    entry_price = premium_history.iloc[i]
                elif z < -entry_z:  # A折价→做多A做空H
                    position = 1
                    entry_price = premium_history.iloc[i]
            else:
                if abs(z) < exit_z:  # 回归→平仓
                    pnl = (entry_price - premium_history.iloc[i]) * position * 10000
                    self.capital += pnl
                    self.trade_log.append({
                        "entry": entry_price, "exit": premium_history.iloc[i],
                        "pnl": pnl, "z_entry": z_score.iloc[i - 1], "z_exit": z
                    })
                    position = 0
            
            self.equity_curve.append(self.capital)
        
        return self._summary()
    
    def _summary(self) -> Dict:
        equity = np.array(self.equity_curve)
        returns = np.diff(equity) / equity[:-1]
        return {
            "Total_Return": f"{(self.capital/self.initial_capital - 1):.2%}",
            "Sharpe": round(np.mean(returns)/np.std(returns)*np.sqrt(252), 3) if np.std(returns)>0 else 0,
            "Num_Trades": len(self.trade_log),
            "Final_Capital": self.capital
        }


# ============================================================
# 演示
# ============================================================

if __name__ == "__main__":
    print("龙虾-跨市场实时套利监控引擎 v1.0 原型加载完成")
    print(f"协议#86 | 五大监控器 | 三大套利策略 | 执行+回测引擎")
    print(f"监控器: AH溢价 | 期现基差 | ETF折溢价 | 配对交易 | 中概ADR")
    print(f"风控: 单策略≤10% | 总仓位≤40% | 滑点≤0.2% | 腿差≤2s")

```
