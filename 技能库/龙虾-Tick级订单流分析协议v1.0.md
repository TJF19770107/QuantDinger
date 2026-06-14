---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_b7fd8906608011f1aa435254002afed2
    ReservedCode1: r2x586L6lwM4Nwlpqoi6afBy/QjF+rDbGqePT/g1M7COh/A43S6FCPB5rMihhi2YmSyNqg0e/LJUJUtVSe/FXb0tyyqPZR9cSc3bRIj0RpyaFpxLMFDjsTOGhrnjml4VPZq5VBtn/vjkK7hY6hcRpqt8gUU6k61H3WjBUlLXfmSowUht13/NDQJPq/Y=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_b7fd8906608011f1aa435254002afed2
    ReservedCode2: r2x586L6lwM4Nwlpqoi6afBy/QjF+rDbGqePT/g1M7COh/A43S6FCPB5rMihhi2YmSyNqg0e/LJUJUtVSe/FXb0tyyqPZR9cSc3bRIj0RpyaFpxLMFDjsTOGhrnjml4VPZq5VBtn/vjkK7hY6hcRpqt8gUU6k61H3WjBUlLXfmSowUht13/NDQJPq/Y=
---

# Tick级订单流分析协议 v1.0

> **协议编号**：85
> **创建日期**：2026-06-01
> **对标来源**：L2市场深度标准 + 订单流足迹图 + 量化交易最佳实践
> **目标**：从L2逐笔委托级别分析主力资金流向，补全交易策略从90→93
> **优先级**：P0（R25立即执行）

---

## 一、协议架构

### 1.1 数据层级模型

```
L3: 策略层（多策略联动 + 跨市场套利 + 动态仓位管理）
↑
L2: 分析层（订单流分析 + 主力行为识别 + 异常检测）
↑
L1: 数据层（Tick逐笔成交 + L2逐笔委托 + 五档深度）
```

### 1.2 核心能力矩阵

| 能力 | 当前（R24） | 目标（R40） | 对标来源 |
|------|-----------|------------|---------|
| **数据粒度** | 分钟K线 | Tick级逐笔 | L2市场深度标准 |
| **订单分析** | 粗粒度 | L2委托簿分析 | Order Flow Footprint Chart |
| **主力识别** | 大单统计 | 订单流画像 + 冰山订单检测 | 量化私募最佳实践 |
| **实时性** | 延迟15秒 | 实时推送 | 极速交易柜台 |

---

## 二、Tick数据结构

### 2.1 逐笔成交（Tick Trade）

```json
{
  "tick_id": "20260601_093000_001",
  "symbol": "000001.SZ",
  "timestamp": "2026-06-01T09:30:00.123+08:00",
  "price": 12.58,
  "volume": 5000,
  "amount": 62900.00,
  "direction": "BUY",
  "bid_price": 12.57,
  "ask_price": 12.59,
  "trade_type": "ACTIVE_BUY",
  "sequence": 123456789
}
```

### 2.2 L2逐笔委托（L2 Order）

```json
{
  "order_id": "ORD_20260601_001",
  "symbol": "000001.SZ",
  "timestamp": "2026-06-01T09:30:00.000+08:00",
  "side": "BUY",
  "type": "LIMIT",
  "price": 12.57,
  "volume": 10000,
  "status": "NEW",
  "broker": "国泰君安",
  "order_ip": "202.xx.xx.xx"
}
```

### 2.3 五档盘口（Market Depth）

```json
{
  "symbol": "000001.SZ",
  "timestamp": "2026-06-01T09:30:00.000+08:00",
  "bids": [
    {"price": 12.57, "volume": 50000},
    {"price": 12.56, "volume": 80000},
    {"price": 12.55, "volume": 120000},
    {"price": 12.54, "volume": 60000},
    {"price": 12.53, "volume": 100000}
  ],
  "asks": [
    {"price": 12.59, "volume": 30000},
    {"price": 12.60, "volume": 70000},
    {"price": 12.61, "volume": 45000},
    {"price": 12.62, "volume": 90000},
    {"price": 12.63, "volume": 55000}
  ]
}
```

---

## 三、订单流分析算法

### 3.1 订单流足迹图

```python
class OrderFlowFootprint:
    """
    订单流足迹图分析器
    对标：Bookmap / Sierra Chart / ATAS 订单流工具
    """
    
    def __init__(self):
        self.price_levels = {}
        self.delta = {}
    
    def process_tick(self, tick):
        """处理逐笔成交，更新各价格级别的买卖量"""
        price = tick['price']
        if price not in self.price_levels:
            self.price_levels[price] = {'bid_vol': 0, 'ask_vol': 0}
        
        if tick['direction'] == 'BUY':
            self.price_levels[price]['ask_vol'] += tick['volume']
            self.delta[price] = self.delta.get(price, 0) + tick['volume']
        else:
            self.price_levels[price]['bid_vol'] += tick['volume']
            self.delta[price] = self.delta.get(price, 0) - tick['volume']
    
    def calculate_footprint(self, bar_start, bar_end):
        """
        计算单根K线的足迹图
        返回每个价格级别的：买方成交量 | 价格 | 卖方成交量
        """
        footprint = []
        for price in sorted(self.price_levels.keys(), reverse=True):
            level = self.price_levels[price]
            delta = self.delta.get(price, 0)
            footprint.append({
                'bid_vol': level['bid_vol'],
                'price': price,
                'ask_vol': level['ask_vol'],
                'delta': delta,
                'imbalance': 'BUY' if delta > 0 else 'SELL' if delta < 0 else 'NEUTRAL'
            })
        return footprint
    
    def detect_absorption(self, footprint):
        """
        吸收检测：大量卖单被买方吸收，价格不跌
        这是主力吸筹的典型信号
        """
        for level in footprint:
            if level['bid_vol'] > level['ask_vol'] * 3:  # 卖方量远超买方
                if self.price_change_ok(level):  # 但价格未明显下跌
                    return {
                        'signal': 'ABSORPTION',
                        'price': level['price'],
                        'bid_vol': level['bid_vol'],
                        'ask_vol': level['ask_vol'],
                        'confidence': 0.75
                    }
        return None
```

### 3.2 主力资金流向分析

```python
class PrimaryCapitalFlow:
    """
    主力资金流向分析器
    基于大单、连续成交、委托簿变化识别主力行为
    """
    
    def __init__(self, threshold_multiplier=3.0):
        self.avg_volume = 0
        self.threshold = 0
        self.block_trades = []
        self.iceberg_suspicions = []
    
    def calculate_baseline(self, recent_ticks):
        """计算平均成交量基准"""
        volumes = [t['volume'] for t in recent_ticks[-1000:]]
        self.avg_volume = sum(volumes) / len(volumes)
        self.threshold = self.avg_volume * self.threshold_multiplier
    
    def detect_block_trade(self, tick):
        """检测大单（超过平均成交量3倍）"""
        if tick['volume'] > self.threshold:
            self.block_trades.append({
                'timestamp': tick['timestamp'],
                'price': tick['price'],
                'volume': tick['volume'],
                'direction': tick['direction'],
                'multiplier': tick['volume'] / self.avg_volume
            })
            return True
        return False
    
    def detect_iceberg_order(self, order_book, min_refresh_count=5):
        """
        冰山订单检测
        算法：同一价格档位连续出现相同量级的挂单补充
        """
        suspicious_levels = []
        for level_id, level_data in order_book.levels.items():
            if level_data['refresh_count'] >= min_refresh_count:
                volumes = level_data['refresh_volumes']
                # 检查是否每次补充量级一致（冰山订单特征）
                if len(set(volumes)) <= 2:  # 量级高度一致
                    self.iceberg_suspicions.append({
                        'price': level_data['price'],
                        'side': level_data['side'],
                        'total_volume': sum(volumes),
                        'refresh_count': len(volumes),
                        'confidence': min(0.9, len(volumes) / 10)
                    })
        return self.iceberg_suspicions
    
    def calculate_fund_flow_score(self, window_ticks):
        """
        计算主力资金流向综合评分
        返回值：[-100, 100]，正值表示主力流入，负值表示主力流出
        """
        buy_power = 0
        sell_power = 0
        
        for tick in window_ticks:
            if tick['volume'] > self.threshold:  # 仅统计大单
                if tick['direction'] == 'BUY':
                    buy_power += tick['amount']
                else:
                    sell_power += tick['amount']
        
        if buy_power + sell_power == 0:
            return 0
        
        score = (buy_power - sell_power) / (buy_power + sell_power) * 100
        return max(-100, min(100, score))
```

### 3.3 主力行为动态分析

```python
class PrimaryBehaviorDynamics:
    """
    主力行为动态分析模块（新增）
    识别：吸筹、洗盘、拉升、出货 四大阶段
    """
    
    def __init__(self):
        self.behavior_states = {
            'ACCUMULATING': '吸筹阶段',
            'SHAKING': '洗盘阶段', 
            'PUMPING': '拉升阶段',
            'DISTRIBUTING': '出货阶段',
            'UNKNOWN': '未知'
        }
        self.state_history = []
        
    def classify_behavior(self, fund_flow_score, price_change, volume_ratio, delta_imbalance):
        """
        基于多维特征识别主力当前行为阶段
        """
        # 吸筹特征：大单买入但价格不涨（吸收卖压）
        if fund_flow_score > 40 and price_change < 0.01 and volume_ratio > 1.5:
            return 'ACCUMULATING'
        
        # 洗盘特征：大单卖出但价格不跌、缩量
        elif fund_flow_score < -30 and price_change > -0.02 and volume_ratio < 0.8:
            return 'SHAKING'
        
        # 拉升特征：大单买入推动价格上涨、放量
        elif fund_flow_score > 50 and price_change > 0.02 and volume_ratio > 2.0:
            return 'PUMPING'
        
        # 出货特征：大单卖出推动价格下跌、放量
        elif fund_flow_score < -50 and price_change < -0.01 and volume_ratio > 1.8:
            return 'DISTRIBUTING'
        
        return 'UNKNOWN'
    
    def generate_behavior_report(self, symbol, timeframe):
        """
        生成主力行为分析报告
        """
        report = f"""
# {symbol} 主力行为动态分析报告
**分析时段**：{timeframe}

## 行为阶段判定
| 阶段 | 判断依据 | 置信度 |
|------|---------|--------|
| 当前阶段 | {self._get_current_behavior()} | {self._get_confidence()}% |

## 关键指标
- 资金流向评分：{self._get_fund_flow_score()}
- 大单占比：{self._get_block_ratio()}%
- 冰山订单检测：{self._get_iceberg_count()}处
- 吸收信号：{self._get_absorption_signals()}次

## 操作建议
{self._generate_advice()}

## 风控提醒
- 当前风控级别：{self._get_risk_level()}
- 建议仓位：{self._suggest_position()}%
"""
        return report
```

---

## 四、与现有技能集成

### 4.1 数据源对接

| 数据源 | 接入方式 | 覆盖范围 |
|--------|---------|---------|
| **ths-advanced-analysis** | 分钟K线 + 部分Tick | A股/港股 |
| **westockdata** | 日K线 + 资金流向 | A股/港股/美股 |
| **ai-trader** | 回测引擎 | 多市场 |
| **聚宽/米筐** | Tick数据（需另接入） | A股 |
| **TD Ameritrade API** | L2数据 | 美股 |

### 4.2 交易策略集成

```python
# 龙虾五步法 Step3 方案规划中集成订单流分析
class EnhancedStrategyPlanner:
    def __init__(self):
        self.order_flow = OrderFlowFootprint()
        self.capital_flow = PrimaryCapitalFlow()
        self.behavior_dynamics = PrimaryBehaviorDynamics()
    
    def plan_trade(self, symbol, market_condition):
        # 1. 订单流分析
        footprint = self.order_flow.calculate_footprint(...)
        absorption = self.order_flow.detect_absorption(footprint)
        
        # 2. 主力资金检测
        block_trades = self.capital_flow.block_trades
        icebergs = self.capital_flow.iceberg_suspicions
        fund_score = self.capital_flow.calculate_fund_flow_score(...)
        
        # 3. 行为动态分析
        behavior = self.behavior_dynamics.classify_behavior(
            fund_score, price_change, volume_ratio, delta
        )
        
        # 4. 综合决策
        if behavior == 'ACCUMULATING' and absorption:
            return {"action": "BUY", "reason": "主力吸筹+吸收信号", "confidence": 0.8}
        elif behavior == 'DISTRIBUTING':
            return {"action": "SELL", "reason": "主力出货信号", "confidence": 0.85}
        
        return {"action": "WAIT", "reason": "信号不明确", "confidence": 0.5}
```

---

## 五、风控增强

### 5.1 Tick级风控指标

| 指标 | 计算公式 | 阈值 | 触发动作 |
|------|---------|------|---------|
| **瞬时波动率** | 最近100笔Tick标准差 | >3% | 减仓50% |
| **买卖失衡** | 大单买入/大单卖出 | >5:1或<1:5 | 暂停交易 |
| **撤单率** | 撤单量/总委托量 | >60% | 警惕假单 |
| **流动性枯竭** | 最低档/最高档挂单量 | <100手 | 停止交易 |

### 5.2 熔断机制升级

```python
# 融合Tick数据的多重熔断（升级自用户偏好规则）
class TickFuseBreaker:
    def __init__(self):
        self.fuse_levels = {
            'L1_soft': {'drawdown': 0.12, 'action': '减仓至50%'},
            'L2_hard': {'drawdown': 0.15, 'action': '平仓所有'},
            'L3_emergency': {'tick_volatility': 0.05, 'action': '紧急熔断+报警'}
        }
    
    def check(self, tick_data, position):
        # 原有回撤熔断
        if position.drawdown > 0.15:
            return {'fuse': 'L2_hard', 'action': '全平'}
        
        # 新增Tick级熔断
        tick_vol = self.calc_tick_volatility(tick_data)
        if tick_vol > 0.05:
            return {'fuse': 'L3_emergency', 'action': '紧急熔断'}
        
        return None
```

---

## 六、验收标准

### 6.1 功能验收

| 测试项 | 验收标准 |
|--------|---------|
| Tick数据接收 | 延迟≤500ms |
| 订单流足迹图生成 | 准确率≥98% |
| 大单检测 | 误报率<5% |
| 冰山订单识别 | 准确率≥80% |
| 主力行为分类 | 准确率≥75% |

### 6.2 性能验收

| 指标 | 目标值 |
|------|--------|
| 单只股票Tick处理速度 | ≥10000条/秒 |
| 同时监控股票数 | ≥50只 |
| 内存占用 | ≤2GB |
| 全天回测速度 | ≤30秒（1年数据） |

---

## 七、预期效果

| 维度 | 当前分 | 目标分 | 提升 |
|------|--------|--------|------|
| **交易博弈策略** | 90 | 93 | +3 |
| **综合加权影响** | 90.7 | 91.15 | +0.45 |

---

> **协议状态**：v1.0 草案  
> **创建者**：龙虾AI主控中心  
> **创建时间**：2026-06-01 17:20  
> **情报条目**：#261 L2 Tick数据标准与订单流分析
> **下一版本**：v1.1（R27实现Tick数据接入后）
*（内容由AI生成，仅供参考）*
