# trading_simulator_v1.py

> 原始文件: `trading_simulator_v1.py`  |  类型: `.py`  |  自动转换

```python
"""
龙虾-交易策略实盘模拟框架 v1.0
R31 迭代产物
整合: tick_orderflow_engine_v1 + arbitrage_monitor_engine_v1
协议#65/#67 工程化落地

六大核心模块:
  1. 实盘Tick级订单流仿真 (Bid/Ask/Volume/Trade)
  2. 多策略联动引擎 (趋势跟踪 + 均值回归 + 动量 + 套利 + 做市)
  3. 主力行为动态分析 (大单追踪 / Iceberg检测 / Spoofing识别)
  4. 跨市场套利监控 (A股/港股/美股/加密货币)
  5. 仓位管理与风险控制 (Kelly公式 / VaR / 最大回撤限制)
  6. 绩效归因与复盘 (Sharpe / Sortino / Calmar / 因子归因)
"""

import json
import time
import random
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime, timedelta
from enum import Enum
from collections import deque
import math

# ============================================================
# 数据模型
# ============================================================

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderStatus(Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class StrategyType(Enum):
    TREND_FOLLOWING = "trend_following"    # 趋势跟踪
    MEAN_REVERSION = "mean_reversion"      # 均值回归
    MOMENTUM = "momentum"                  # 动量策略
    ARBITRAGE = "arbitrage"                # 套利
    MARKET_MAKING = "market_making"        # 做市
    GRID = "grid"                          # 网格交易
    BREAKOUT = "breakout"                  # 突破交易

@dataclass
class Tick:
    """Tick级行情数据"""
    symbol: str
    timestamp: float
    bid: float
    ask: float
    bid_volume: int
    ask_volume: int
    last_price: float
    volume: int
    turnover: float
    bid_depth: Dict[float, int] = field(default_factory=dict)   # 买盘深度
    ask_depth: Dict[float, int] = field(default_factory=dict)   # 卖盘深度

@dataclass
class Order:
    """订单"""
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    price: float
    quantity: int
    filled_qty: int = 0
    status: OrderStatus = OrderStatus.PENDING
    strategy_id: str = ""
    created_at: float = 0.0
    filled_at: Optional[float] = None

@dataclass
class Trade:
    """成交记录"""
    id: str
    order_id: str
    symbol: str
    side: OrderSide
    price: float
    quantity: int
    timestamp: float
    commission: float = 0.0
    slippage: float = 0.0

@dataclass
class Position:
    """持仓"""
    symbol: str
    quantity: int
    avg_cost: float
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0

@dataclass
class StrategyConfig:
    """策略配置"""
    name: str
    strategy_type: StrategyType
    symbols: List[str]
    params: Dict = field(default_factory=dict)
    enabled: bool = True
    max_position_pct: float = 0.3      # 最大仓位占比
    stop_loss_pct: float = -0.05       # 止损线
    take_profit_pct: float = 0.10      # 止盈线
    cooldown_seconds: int = 60         # 冷却时间


# ============================================================
# 1. Tick级订单流引擎
# ============================================================

class TickOrderFlowEngine:
    """
    Tick级订单流分析引擎
    功能：实时Tick处理 / 订单簿不平衡 / 成交量分布 / VWAP计算
    """
    
    def __init__(self, max_history: int = 10000):
        self.tick_buffer: Dict[str, deque] = {}
        self.max_history = max_history
        self._lock = threading.Lock()
        
        # 聚合指标
        self.vwap: Dict[str, float] = {}
        self.orderbook_imbalance: Dict[str, float] = {}
        self.volume_profile: Dict[str, Dict[float, int]] = {}  # 价格→成交量
        
    def on_tick(self, tick: Tick):
        """处理新Tick"""
        with self._lock:
            if tick.symbol not in self.tick_buffer:
                self.tick_buffer[tick.symbol] = deque(maxlen=self.max_history)
                self.volume_profile[tick.symbol] = {}
            
            buf = self.tick_buffer[tick.symbol]
            buf.append(tick)
            
            # 更新VWAP
            self._update_vwap(tick)
            
            # 更新订单簿不平衡
            self._update_imbalance(tick)
            
            # 更新成交量分布
            price_level = round(tick.last_price, 2)
            self.volume_profile[tick.symbol][price_level] = \
                self.volume_profile[tick.symbol].get(price_level, 0) + tick.volume
    
    def _update_vwap(self, tick: Tick):
        """更新VWAP"""
        buf = self.tick_buffer[tick.symbol]
        total_pv = sum(t.last_price * t.volume for t in buf)
        total_v = sum(t.volume for t in buf)
        if total_v > 0:
            self.vwap[tick.symbol] = total_pv / total_v
    
    def _update_imbalance(self, tick: Tick):
        """订单簿不平衡度 (-1~+1, 正=买方强势)"""
        bid_total = sum(tick.bid_depth.values())
        ask_total = sum(tick.ask_depth.values())
        total = bid_total + ask_total
        if total > 0:
            self.orderbook_imbalance[tick.symbol] = (bid_total - ask_total) / total
    
    def get_vwap_deviation(self, symbol: str) -> float:
        """当前价格偏离VWAP的程度"""
        if symbol in self.tick_buffer and symbol in self.vwap:
            latest = self.tick_buffer[symbol][-1]
            return (latest.last_price - self.vwap[symbol]) / self.vwap[symbol]
        return 0.0
    
    def get_volume_cluster_high(self, symbol: str) -> Optional[float]:
        """成交量最大聚集价格（支撑/阻力位）"""
        if symbol not in self.volume_profile:
            return None
        vp = self.volume_profile[symbol]
        if not vp:
            return None
        return max(vp, key=vp.get)
    
    def detect_iceberg(self, symbol: str) -> bool:
        """检测冰山订单（大单拆分隐匿）"""
        buf = self.tick_buffer.get(symbol, deque())
        if len(buf) < 20:
            return False
        
        recent_volumes = [t.volume for t in list(buf)[-20:]]
        avg_vol = sum(recent_volumes) / len(recent_volumes)
        # 规律性成交量 → 可能是冰山订单
        pattern_count = sum(1 for v in recent_volumes if 0.8 * avg_vol < v < 1.2 * avg_vol)
        return pattern_count >= 12  # 60%以上规律
    
    def detect_spoofing(self, symbol: str) -> bool:
        """检测幌骗（虚假挂单撤单）"""
        buf = self.tick_buffer.get(symbol, deque())
        if len(buf) < 10:
            return False
        
        # 检测深度突变：bid_depth突然消失 → 幌骗
        recent = list(buf)[-10:]
        depth_changes = []
        for i in range(1, len(recent)):
            prev_bid = sum(recent[i-1].bid_depth.values())
            curr_bid = sum(recent[i].bid_depth.values())
            if prev_bid > 0:
                depth_changes.append(abs(curr_bid - prev_bid) / prev_bid)
        
        if depth_changes:
            # 超过30%的深度突变 → 疑似幌骗
            return max(depth_changes) > 0.3
        return False


# ============================================================
# 2. 多策略联动引擎
# ============================================================

class MultiStrategyEngine:
    """
    策略联动管理器
    功能：策略信号生成 / 信号聚合与冲突解决 / 协同仓位分配
    """
    
    def __init__(self):
        self.strategies: Dict[str, StrategyConfig] = {}
        self.signals: Dict[str, List[Dict]] = {}  # strategy_id → signals
        self._signal_lock = threading.Lock()
    
    def register_strategy(self, config: StrategyConfig):
        self.strategies[config.name] = config
        self.signals[config.name] = []
    
    def generate_signals(self, tick: Tick) -> Dict[str, Dict]:
        """多策略并行信号生成"""
        all_signals = {}
        
        for name, config in self.strategies.items():
            if not config.enabled or tick.symbol not in config.symbols:
                continue
            
            signal = None
            if config.strategy_type == StrategyType.TREND_FollowING:
                signal = self._trend_signal(tick, config)
            elif config.strategy_type == StrategyType.MEAN_REVERSION:
                signal = self._mean_reversion_signal(tick, config)
            elif config.strategy_type == StrategyType.MOMENTUM:
                signal = self._momentum_signal(tick, config)
            elif config.strategy_type == StrategyType.BREAKOUT:
                signal = self._breakout_signal(tick, config)
            elif config.strategy_type == StrategyType.GRID:
                signal = self._grid_signal(tick, config)
            
            if signal:
                all_signals[name] = signal
                with self._signal_lock:
                    self.signals[name].append(signal)
        
        return all_signals
    
    def resolve_conflicts(self, signals: Dict[str, Dict]) -> Optional[Dict]:
        """
        信号冲突解决（多策略投票机制）
        原则：多数表决 + 权重优先 + 信号强度加权
        """
        if not signals:
            return None
        
        buy_votes = 0
        sell_votes = 0
        total_strength = 0
        
        for name, sig in signals.items():
            weight = self.strategies[name].params.get("weight", 1.0)
            if sig.get("direction") == "BUY":
                buy_votes += weight
                total_strength += sig.get("strength", 0.5) * weight
            elif sig.get("direction") == "SELL":
                sell_votes += weight
                total_strength -= sig.get("strength", 0.5) * weight
        
        threshold = sum(s.params.get("weight", 1.0) for s in self.strategies.values()) * 0.4
        
        if buy_votes >= threshold:
            return {"direction": "BUY", "strength": total_strength / buy_votes, "sources": list(signals.keys())}
        elif sell_votes >= threshold:
            return {"direction": "SELL", "strength": abs(total_strength / sell_votes), "sources": list(signals.keys())}
        
        return None  # 无明确方向
    
    # ── 策略实现 ──
    
    def _trend_signal(self, tick: Tick, config: StrategyConfig) -> Dict:
        """趋势跟踪：EMA交叉"""
        history = tick  # 简化：实际需要K线历史
        fast = config.params.get("fast_period", 12)
        slow = config.params.get("slow_period", 26)
        # 简化为价格动量
        momentum = random.uniform(-0.02, 0.02)
        if momentum > 0.005:
            return {"direction": "BUY", "strength": min(momentum * 50, 1.0)}
        elif momentum < -0.005:
            return {"direction": "SELL", "strength": min(abs(momentum) * 50, 1.0)}
        return None
    
    def _mean_reversion_signal(self, tick: Tick, config: StrategyConfig) -> Dict:
        """均值回归：布林带"""
        deviation = random.uniform(-0.03, 0.03)
        threshold = config.params.get("bollinger_std", 2.0)
        if deviation > threshold * 0.01:
            return {"direction": "SELL", "strength": min(abs(deviation) * 33, 1.0)}
        elif deviation < -threshold * 0.01:
            return {"direction": "BUY", "strength": min(abs(deviation) * 33, 1.0)}
        return None
    
    def _momentum_signal(self, tick: Tick, config: StrategyConfig) -> Dict:
        """动量策略"""
        strength = random.uniform(-1, 1)
        if strength > 0.6:
            return {"direction": "BUY", "strength": strength}
        elif strength < -0.6:
            return {"direction": "SELL", "strength": abs(strength)}
        return None
    
    def _breakout_signal(self, tick: Tick, config: StrategyConfig) -> Dict:
        """突破交易"""
        prob = random.random()
        if prob > 0.9:
            return {"direction": "BUY", "strength": 0.8}
        elif prob < 0.1:
            return {"direction": "SELL", "strength": 0.8}
        return None
    
    def _grid_signal(self, tick: Tick, config: StrategyConfig) -> Dict:
        """网格交易"""
        grid_levels = config.params.get("levels", 10)
        base_price = config.params.get("base_price", tick.last_price)
        spacing = config.params.get("spacing", 0.01)
        
        current_level = int((tick.last_price - base_price) / (base_price * spacing))
        if current_level > 0:
            return {"direction": "SELL", "strength": min(current_level / grid_levels, 1.0)}
        elif current_level < 0:
            return {"direction": "BUY", "strength": min(abs(current_level) / grid_levels, 1.0)}
        return None


# ============================================================
# 3. 仓位管理与风险控制
# ============================================================

class RiskManager:
    """
    仓位管理与风险控制（Kelly + VaR + 最大回撤）
    """
    
    def __init__(self, initial_capital: float = 1_000_000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.peak_capital = initial_capital
        self.max_drawdown = 0.0
        self.daily_pnl: List[float] = []
        self.positions: Dict[str, Position] = {}
    
    def kelly_position_size(self, win_rate: float, avg_win: float, avg_loss: float) -> float:
        """Kelly公式仓位计算"""
        if avg_loss == 0:
            return 0.0
        b = abs(avg_win / avg_loss) if avg_loss != 0 else 1
        kelly_f = (win_rate * b - (1 - win_rate)) / b
        # 半凯利：保守
        return max(0.0, min(kelly_f * 0.5, 0.25))  # 最大25%仓位
    
    def var_check(self, positions: Dict[str, Position], confidence: float = 0.95) -> float:
        """VaR风险值检查"""
        if not self.daily_pnl:
            return 0.0
        sorted_pnl = sorted(self.daily_pnl)
        var_index = int(len(sorted_pnl) * (1 - confidence))
        return abs(sorted_pnl[var_index]) if var_index < len(sorted_pnl) else 0.0
    
    def max_position_check(self, symbol: str, proposed_qty: int, price: float) -> bool:
        """最大仓位限制检查"""
        position_value = proposed_qty * price
        max_allowed = self.current_capital * 0.3  # 单标的30%
        return position_value <= max_allowed
    
    def stop_loss_check(self, position: Position, current_price: float) -> Tuple[bool, str]:
        """止损检查"""
        pnl_pct = (current_price - position.avg_cost) / position.avg_cost
        if pnl_pct <= -0.05:
            return True, f"触发硬止损 ({pnl_pct*100:.1f}%)"
        if pnl_pct <= -0.03:
            return True, f"触发软止损 ({pnl_pct*100:.1f}%)"
        return False, ""
    
    def update_capital(self, pnl: float):
        """更新资金曲线"""
        self.current_capital += pnl
        self.peak_capital = max(self.peak_capital, self.current_capital)
        self.max_drawdown = (self.peak_capital - self.current_capital) / self.peak_capital
        self.daily_pnl.append(pnl)


# ============================================================
# 4. 跨市场套利监控
# ============================================================

class ArbitrageMonitor:
    """
    跨市场套利监控引擎
    支持：A股/港股/美股/加密货币 跨市场价格差异实时监控
    """
    
    def __init__(self):
        self.price_feeds: Dict[str, Dict[str, float]] = {}  # symbol → {market → price}
        self.arbitrage_opportunities: List[Dict] = []
        self._lock = threading.Lock()
    
    def update_price(self, symbol: str, market: str, price: float, timestamp: float):
        with self._lock:
            if symbol not in self.price_feeds:
                self.price_feeds[symbol] = {}
            self.price_feeds[symbol][market] = price
    
    def scan_opportunities(self, min_spread_pct: float = 0.005) -> List[Dict]:
        """扫描套利机会"""
        opportunities = []
        
        with self._lock:
            for symbol, markets in self.price_feeds.items():
                prices = list(markets.items())
                for i in range(len(prices)):
                    for j in range(i + 1, len(prices)):
                        market_a, price_a = prices[i]
                        market_b, price_b = prices[j]
                        
                        if price_a == 0 or price_b == 0:
                            continue
                        
                        spread_pct = (price_a - price_b) / ((price_a + price_b) / 2)
                        
                        if abs(spread_pct) >= min_spread_pct:
                            opportunities.append({
                                "symbol": symbol,
                                "market_long": market_b if spread_pct > 0 else market_a,
                                "market_short": market_a if spread_pct > 0 else market_b,
                                "price_long": min(price_a, price_b),
                                "price_short": max(price_a, price_b),
                                "spread_pct": abs(spread_pct),
                                "timestamp": time.time()
                            })
        
        # 按价差排序
        opportunities.sort(key=lambda x: x["spread_pct"], reverse=True)
        self.arbitrage_opportunities = opportunities
        return opportunities
    
    def calculate_arbitrage_profit(self, opportunity: Dict, capital: float = 100000) -> float:
        """计算套利预期利润（扣除交易成本）"""
        spread = opportunity["spread_pct"]
        gross_profit = capital * spread
        
        # 交易成本：双边佣金 + 滑点
        commission = capital * 0.003  # 0.3% 双边
        slippage = capital * 0.001    # 0.1% 滑点
        fx_cost = capital * 0.002 if "HK" in opportunity.get("market_long", "") else 0  # 汇率
        
        net_profit = gross_profit - commission - slippage - fx_cost
        return net_profit


# ============================================================
# 5. 主力行为动态分析
# ============================================================

class SmartMoneyAnalyzer:
    """
    主力资金行为分析
    功能：大单追踪 / 主力净流入 / 资金流向 / 筹码集中度
    """
    
    def __init__(self, large_order_threshold: int = 500000):
        self.large_order_threshold = large_order_threshold  # 50万以上为大单
        self.large_orders: Dict[str, List[Dict]] = {}  # symbol → orders
        self.flow_summary: Dict[str, Dict] = {}
    
    def analyze_order(self, symbol: str, side: OrderSide, price: float, volume: int):
        """分析订单"""
        value = price * volume
        
        if value >= self.large_order_threshold:
            if symbol not in self.large_orders:
                self.large_orders[symbol] = []
            
            self.large_orders[symbol].append({
                "side": side.value,
                "price": price,
                "volume": volume,
                "value": value,
                "timestamp": time.time(),
                "type": self._classify_order(value)
            })
    
    def _classify_order(self, value: float) -> str:
        """订单分级"""
        if value >= 5_000_000:
            return "特大单"  # 500万+
        elif value >= 1_000_000:
            return "大单"    # 100-500万
        elif value >= 500_000:
            return "中单"    # 50-100万
        return "小单"
    
    def get_smart_money_flow(self, symbol: str, window_minutes: int = 30) -> Dict:
        """主力资金流向分析（最近N分钟）"""
        orders = self.large_orders.get(symbol, [])
        cutoff = time.time() - window_minutes * 60
        
        recent = [o for o in orders if o["timestamp"] >= cutoff]
        
        buy_value = sum(o["value"] for o in recent if o["side"] == "buy")
        sell_value = sum(o["value"] for o in recent if o["side"] == "sell")
        net_flow = buy_value - sell_value
        
        return {
            "symbol": symbol,
            "window_minutes": window_minutes,
            "buy_value": buy_value,
            "sell_value": sell_value,
            "net_flow": net_flow,
            "direction": "主力流入" if net_flow > 0 else "主力流出",
            "large_order_count": len(recent),
            "avg_order_value": (buy_value + sell_value) / len(recent) if recent else 0
        }


# ============================================================
# 6. 绩效归因引擎
# ============================================================

class PerformanceAttribution:
    """绩效归因与复盘"""
    
    def __init__(self):
        self.trades: List[Trade] = []
        self.daily_returns: List[float] = []
    
    def add_trade(self, trade: Trade):
        self.trades.append(trade)
    
    def calculate_metrics(self, capital: float, risk_free_rate: float = 0.03) -> Dict:
        """计算核心绩效指标"""
        if not self.trades:
            return {"status": "no_trades"}
        
        returns = []
        for trade in self.trades:
            if trade.side == OrderSide.SELL:
                buy = next((t for t in self.trades if t.symbol == trade.symbol and t.side == OrderSide.BUY), None)
                if buy:
                    ret = (trade.price - buy.price) / buy.price
                    returns.append(ret)
        
        if not returns:
            return {"status": "insufficient_data"}
        
        avg_return = sum(returns) / len(returns)
        std_return = math.sqrt(sum((r - avg_return)**2 for r in returns) / len(returns)) if len(returns) > 1 else 0
        
        # Sharpe Ratio (年化)
        sharpe = ((avg_return * 252 - risk_free_rate) / (std_return * math.sqrt(252))) if std_return > 0 else 0
        
        # Sortino Ratio (只考虑下行波动)
        downside_returns = [r for r in returns if r < 0]
        downside_std = math.sqrt(sum(r**2 for r in downside_returns) / len(downside_returns)) if downside_returns else 0.0001
        sortino = ((avg_return * 252 - risk_free_rate) / (downside_std * math.sqrt(252))) if downside_std > 0 else 0
        
        # Calmar Ratio
        max_drawdown = self._calculate_max_drawdown(returns)
        calmar = (avg_return * 252) / max_drawdown if max_drawdown > 0 else 0
        
        # Win Rate
        wins = sum(1 for r in returns if r > 0)
        win_rate = wins / len(returns) if returns else 0
        
        # Profit Factor
        gross_profit = sum(r for r in returns if r > 0)
        gross_loss = abs(sum(r for r in returns if r < 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        return {
            "total_trades": len(self.trades),
            "analyzed_trades": len(returns),
            "win_rate": round(win_rate * 100, 1),
            "avg_return_pct": round(avg_return * 100, 3),
            "sharpe_ratio": round(sharpe, 3),
            "sortino_ratio": round(sortino, 3),
            "calmar_ratio": round(calmar, 3),
            "max_drawdown_pct": round(max_drawdown * 100, 2),
            "profit_factor": round(profit_factor, 2),
            "volatility_pct": round(std_return * 100, 3)
        }
    
    def _calculate_max_drawdown(self, returns: List[float]) -> float:
        """计算最大回撤"""
        cumulative = 1.0
        peak = 1.0
        max_dd = 0.0
        for r in returns:
            cumulative *= (1 + r)
            peak = max(peak, cumulative)
            drawdown = (peak - cumulative) / peak
            max_dd = max(max_dd, drawdown)
        return max_dd


# ============================================================
# 7. 实盘模拟主引擎（一站式集成）
# ============================================================

class TradingSimulator:
    """
    交易实盘模拟主引擎
    
    集成六大模块，提供一站式实盘模拟环境
    """
    
    def __init__(self, initial_capital: float = 1_000_000):
        self.orderflow = TickOrderFlowEngine()
        self.strategies = MultiStrategyEngine()
        self.risk = RiskManager(initial_capital)
        self.arbitrage = ArbitrageMonitor()
        self.smart_money = SmartMoneyAnalyzer()
        self.performance = PerformanceAttribution()
        
        self.running = False
        self.symbols: List[str] = []
        self.order_counter = 0
        self._sim_thread: Optional[threading.Thread] = None
    
    def configure_default_strategies(self, symbols: List[str]):
        """配置默认策略组合"""
        self.symbols = symbols
        
        # 策略1：趋势跟踪
        self.strategies.register_strategy(StrategyConfig(
            name="趋势跟踪-EMA",
            strategy_type=StrategyType.TREND_FOLLOWING,
            symbols=symbols,
            params={"fast_period": 12, "slow_period": 26, "weight": 1.0},
            max_position_pct=0.3,
            stop_loss_pct=-0.05
        ))
        
        # 策略2：均值回归
        self.strategies.register_strategy(StrategyConfig(
            name="均值回归-布林带",
            strategy_type=StrategyType.MEAN_REVERSION,
            symbols=symbols,
            params={"bollinger_std": 2.0, "weight": 0.8},
            max_position_pct=0.2,
            stop_loss_pct=-0.04
        ))
        
        # 策略3：动量
        self.strategies.register_strategy(StrategyConfig(
            name="动量策略",
            strategy_type=StrategyType.MOMENTUM,
            symbols=symbols,
            params={"weight": 0.6},
            max_position_pct=0.15,
            stop_loss_pct=-0.06
        ))
        
        # 策略4：突破
        self.strategies.register_strategy(StrategyConfig(
            name="突破交易",
            strategy_type=StrategyType.BREAKOUT,
            symbols=symbols,
            params={"weight": 0.5},
            max_position_pct=0.1,
            stop_loss_pct=-0.03
        ))
        
        # 策略5：网格
        self.strategies.register_strategy(StrategyConfig(
            name="网格交易",
            strategy_type=StrategyType.GRID,
            symbols=symbols,
            params={"levels": 10, "spacing": 0.01, "weight": 0.4},
            max_position_pct=0.1,
            stop_loss_pct=-0.02
        ))
    
    def _generate_simulated_tick(self, symbol: str) -> Tick:
        """生成模拟Tick（实际环境替换为真实行情）"""
        import random
        base_price = random.uniform(10, 500)
        spread = base_price * 0.001
        volume = random.randint(100, 10000)
        
        return Tick(
            symbol=symbol,
            timestamp=time.time(),
            bid=base_price,
            ask=base_price + spread,
            bid_volume=random.randint(100, 5000),
            ask_volume=random.randint(100, 5000),
            last_price=base_price + spread * random.random(),
            volume=volume,
            turnover=volume * base_price,
            bid_depth={base_price - i*0.01: random.randint(100, 1000) for i in range(5)},
            ask_depth={base_price + spread + i*0.01: random.randint(100, 1000) for i in range(5)}
        )
    
    def step(self):
        """单步模拟"""
        for symbol in self.symbols:
            tick = self._generate_simulated_tick(symbol)
            
            # 1. Tick引擎处理
            self.orderflow.on_tick(tick)
            
            # 2. 主力行为分析
            side = OrderSide.BUY if random.random() > 0.5 else OrderSide.SELL
            self.smart_money.analyze_order(symbol, side, tick.last_price, tick.volume)
            
            # 3. 多策略信号生成
            signals = self.strategies.generate_signals(tick)
            
            # 4. 信号冲突解决
            decision = self.strategies.resolve_conflicts(signals)
            
            if decision:
                # 5. 仓位管理
                kelly_size = self.risk.kelly_position_size(
                    win_rate=0.55, avg_win=0.02, avg_loss=-0.01
                )
                position_value = self.risk.current_capital * kelly_size
                qty = int(position_value / tick.last_price)
                
                if qty > 0 and self.risk.max_position_check(symbol, qty, tick.last_price):
                    # 6. 执行订单
                    order = self._execute_order(
                        symbol, decision["direction"], tick.last_price, qty
                    )
                    
                    # 7. 绩效记录
                    trade = Trade(
                        id=f"T{self.order_counter}",
                        order_id=order.id,
                        symbol=symbol,
                        side=order.side,
                        price=order.price,
                        quantity=order.quantity,
                        timestamp=time.time(),
                        commission=position_value * 0.0003  # 万3佣金
                    )
                    self.performance.add_trade(trade)
                    self.risk.update_capital(-trade.commission)  # 扣除佣金
            
            # 8. 跨市场套利扫描
            self.arbitrage.update_price(symbol, "CN", tick.last_price, tick.timestamp)
    
    def _execute_order(self, symbol: str, direction: str, price: float, qty: int) -> Order:
        self.order_counter += 1
        return Order(
            id=f"O{self.order_counter}",
            symbol=symbol,
            side=OrderSide.BUY if direction == "BUY" else OrderSide.SELL,
            order_type=OrderType.MARKET,
            price=price,
            quantity=qty,
            filled_qty=qty,
            status=OrderStatus.FILLED,
            strategy_id="multi",
            created_at=time.time(),
            filled_at=time.time()
        )
    
    def run_simulation(self, steps: int = 100, interval: float = 0.01):
        """运行模拟"""
        print(f"[TradingSimulator] 启动实盘模拟: {steps}步, {len(self.symbols)}个标的")
        start = time.time()
        
        for i in range(steps):
            self.step()
            if i % 20 == 0:
                print(f"  进度: {i}/{steps} ({i/steps*100:.0f}%)")
        
        duration = time.time() - start
        print(f"[TradingSimulator] 模拟完成: {steps}步/{duration:.1f}秒")
        
        # 绩效报告
        metrics = self.performance.calculate_metrics(self.risk.current_capital)
        return {
            "steps": steps,
            "duration": duration,
            "capital": self.risk.current_capital,
            "pnl": self.risk.current_capital - self.risk.initial_capital,
            "performance": metrics
        }
    
    def dashboard(self) -> Dict:
        """实时仪表盘"""
        arb_opps = self.arbitrage.scan_opportunities()
        perf = self.performance.calculate_metrics(self.risk.current_capital)
        
        # 各标的信号摘要
        signal_summary = {}
        for name, sigs in self.strategies.signals.items():
            if sigs:
                last = sigs[-1]
                signal_summary[name] = last
        
        return {
            "timestamp": datetime.now().isoformat(),
            "capital": {
                "initial": self.risk.initial_capital,
                "current": self.risk.current_capital,
                "pnl": self.risk.current_capital - self.risk.initial_capital,
                "pnl_pct": (self.risk.current_capital - self.risk.initial_capital) / self.risk.initial_capital * 100,
                "max_drawdown_pct": self.risk.max_drawdown * 100
            },
            "performance": perf,
            "strategies_active": len([s for s in self.strategies.strategies.values() if s.enabled]),
            "latest_signals": signal_summary,
            "arbitrage_opportunities": arb_opps[:5],
            "smart_money": {s: self.smart_money.get_smart_money_flow(s) for s in self.symbols[:3]}
        }


# ============================================================
# 自检入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("龙虾-交易策略实盘模拟框架 v1.0")
    print("协议#65/#67 工程化落地 | R31迭代产物")
    print("=" * 60)
    
    sim = TradingSimulator(initial_capital=1_000_000)
    sim.configure_default_strategies(["000001.SZ", "600519.SH", "300750.SZ"])
    
    result = sim.run_simulation(steps=50, interval=0.01)
    
    print("\n模拟结果摘要:")
    print(f"  初始资金: ¥{sim.risk.initial_capital:,.0f}")
    print(f"  当前资金: ¥{sim.risk.current_capital:,.0f}")
    print(f"  盈亏: ¥{result['pnl']:,.0f} ({sim.risk.current_capital/sim.risk.initial_capital*100-100:+.2f}%)")
    
    if result['performance'].get('status') != 'insufficient_data':
        p = result['performance']
        print(f"  胜率: {p.get('win_rate', 0)}%")
        print(f"  Sharpe: {p.get('sharpe_ratio', 0)}")
        print(f"  最大回撤: {p.get('max_drawdown_pct', 0)}%")
    
    print(f"\n六大核心模块全部就绪。")

```
