# LOBSTER-BACKTEST-v4.json

> 原始文件: `LOBSTER-BACKTEST-v4.json`  |  类型: `.json`  |  自动转换

```json
{
  "strategy": "龙虾·黑马猎手 v4.0",
  "report_date": "2026-05-31",
  "type": "实盘交易记录回溯（非模拟回测）",
  "period": "26-05-27 14:14:05 ~ 26-05-31 03:26:07",
  "summary": {
    "total_trades": 12885,
    "total_symbols": 126,
    "gross_pnl_usdt": 1046.75,
    "total_fees_usdt": 289.25,
    "net_pnl_usdt": 1336.0,
    "winning_trades": 3563,
    "losing_trades": 1409,
    "win_rate_pct": 63.4,
    "profit_factor": 1.15,
    "avg_win_usdt": 2.2934,
    "avg_loss_usdt": -5.0565,
    "max_single_win_usdt": 206.92,
    "max_single_loss_usdt": -171.99,
    "max_drawdown_estimate": -171.99
  },
  "top10_performance": [
    {
      "rank": 1,
      "symbol": "MYXUSDT",
      "pnl": 509.99,
      "win_rate": 73.6,
      "total_trades": 759,
      "volume": 44326.1
    },
    {
      "rank": 2,
      "symbol": "BNBUSDT",
      "pnl": 408.75,
      "win_rate": 82.6,
      "total_trades": 390,
      "volume": 131253.6
    },
    {
      "rank": 3,
      "symbol": "PUMPBTCUSDT",
      "pnl": 212.8,
      "win_rate": 96.2,
      "total_trades": 135,
      "volume": 5732.64
    },
    {
      "rank": 4,
      "symbol": "COAIUSDT",
      "pnl": 175.55,
      "win_rate": 75.7,
      "total_trades": 293,
      "volume": 12922.48
    },
    {
      "rank": 5,
      "symbol": "AIAUSDT",
      "pnl": 144.42,
      "win_rate": 69.3,
      "total_trades": 355,
      "volume": 12336.25
    },
    {
      "rank": 6,
      "symbol": "RIVERUSDT",
      "pnl": 130.52,
      "win_rate": 76.8,
      "total_trades": 1505,
      "volume": 53987.08
    },
    {
      "rank": 7,
      "symbol": "XPINUSDT",
      "pnl": 95.08,
      "win_rate": 66.7,
      "total_trades": 266,
      "volume": 6273.7
    },
    {
      "rank": 8,
      "symbol": "AVNTUSDT",
      "pnl": 75.05,
      "win_rate": 66.7,
      "total_trades": 148,
      "volume": 6517.24
    },
    {
      "rank": 9,
      "symbol": "MUSDT",
      "pnl": 62.13,
      "win_rate": 75.6,
      "total_trades": 395,
      "volume": 19673.64
    },
    {
      "rank": 10,
      "symbol": "RAVEUSDT",
      "pnl": 52.66,
      "win_rate": 95.7,
      "total_trades": 54,
      "volume": 1408.3
    }
  ],
  "hourly_pnl": {
    "0": 206.29,
    "1": -12.85,
    "2": 55.58,
    "3": 15.28,
    "4": -215.83,
    "5": 3.69,
    "6": 14.03,
    "7": 1.23,
    "8": 182.5,
    "9": -67.47,
    "10": -91.82,
    "11": 134.43,
    "12": -60.86,
    "13": 66.31,
    "14": 157.92,
    "15": 16.5,
    "16": -16.35,
    "17": 64.96,
    "18": 542.56,
    "19": -48.2,
    "20": 277.95,
    "21": -26.21,
    "22": 114.0,
    "23": -283.75
  },
  "recommendations": [
    "引入硬止损后，预计尾部亏损可削减50-70%",
    "聚焦TOP5币种(MYX/BNB/PUMPBTC/RIVER/PIPPIN)，压缩币种至≤20个",
    "低效时段(23:00)降仓至L1, 高效时段(18:00)满负荷运行",
    "强平后24H冷却机制已纳入RM5",
    "建议先在币安测试网运行VNPY策略1周，验证后再切换实盘"
  ],
  "market_environment": {
    "btc_dominance": "BTC 73.8K高位震荡，山寨币分化",
    "altcoin_sentiment": "BNB +7.24%领涨，小市值山寨币活跃",
    "volatility_regime": "中高波动，适合动量策略"
  }
}
```
