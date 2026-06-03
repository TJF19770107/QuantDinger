# general_strategy.json

> 原始文件: `general_strategy.json`  |  类型: `.json`  |  自动转换

```json
---
file_type: 策略文档
created: 2026-05-30
tags: [量化交易, DOGE, 通用策略]
aliases: ['通用策略v1']
related: [[[general_strategy_v3.json]], [[black_horse_strategy.json]]]
---

{
  "strategy_name": "龙虾通用趋势策略 v1.0",
  "version": "1.0.0",
  "timeframe": "1D",
  "entry": {
    "bullish": "MA20 > MA50 > MA200 且 价格 > MA20",
    "timing": "RSI 50-65区间回调至MA20附近",
    "confirm": "VOL_RATIO > 1.3",
    "filter": "排除RSI > 80的超买状态"
  },
  "position": {
    "initial": "总仓位25%",
    "pyramid": "趋势确认后每突破ATR×2加仓10%，最多3次"
  },
  "risk": {
    "stop_loss": "入场价 - ATR×2",
    "max_position_risk": "单笔不超过总资金3%",
    "correlation_check": "同板块持仓不超过总仓位50%"
  },
  "exit": {
    "trend_end": "价格跌破MA50",
    "overbought": "RSI > 85 且 MACD顶背离",
    "trailing": "启用MA20跟踪止损"
  }
}
```
