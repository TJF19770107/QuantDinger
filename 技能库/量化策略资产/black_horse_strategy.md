# black_horse_strategy.json

原始格式: JSON

```json
---
file_type: 策略文档
created: 2026-05-30
tags: [量化交易, DOGE, 黑马策略]
aliases: ['黑马策略v1']
related: [[[black_horse_strategy_v3.json]], [[general_strategy.json]]]
---

{
  "strategy_name": "龙虾黑马策略 v1.0 (Lobster Black Horse Strategy)",
  "version": "1.0.0",
  "created": "2026-05-30 16:18:47",
  "based_on": "2021年4-5月DOGE十倍行情复现",
  "market_type": "CRYPTO",
  "timeframe": [
    "1D",
    "4H"
  ],
  "entry_rules": {
    "primary": [
      "RSI(14) > 55 且 < 75 (强趋势但不极端)",
      "价格 > MA20 且 MA20 > MA50 (多头排列)",
      "MACD柱状图为正且连续3日扩大",
      "成交量 > VOL_MA20 × 1.5 (放量确认)"
    ],
    "social_sentiment": [
      "社交媒体提及量7日均值 > 30日均值 × 3 (事件驱动确认)",
      "Google Trends搜索指数处于上升通道",
      "Elon Musk / 名人推文作为催化剂信号"
    ],
    "confirmation": "上述条件至少满足3/4，且有明确的事件催化剂"
  },
  "position_management": {
    "initial_entry": "总仓位30%",
    "add_position": {
      "trigger": "价格突破前高且回调不破MA20",
      "size": "每次追加总仓位15%，最多追加2次",
      "max_total": "总仓位60%"
    },
    "scale_out": {
      "level_1": "RSI > 85 时减仓25%",
      "level_2": "价格偏离MA20超过40%时减仓25%",
      "level_3": "ATH附近减仓剩余50%"
    }
  },
  "risk_management": {
    "stop_loss": "MA20下方3%或ATR×2.5，取较紧者",
    "max_drawdown": "单笔交易最大回撤不超过入场资金的15%",
    "trailing_stop": "盈利>50%后启动MA10跟踪止损",
    "black_swan_protection": "30分钟内跌幅>15%时市价全平"
  },
  "exit_rules": {
    "signal_exit": [
      "RSI > 90 且 MACD柱状图开始缩小",
      "价格跌破MA10",
      "成交量萎缩至VOL_MA20的50%以下",
      "事件催化剂兑现(Sell the News)"
    ],
    "time_exit": "持仓超过90天自动减仓50%",
    "catastrophe_exit": "24小时内跌幅>30%时无条件全平"
  },
  "black_horse_specific": {
    "name": "暴利行情专属·龙虾追风策略",
    "description": "针对社交媒体驱动的Meme币脉冲行情的专用子策略",
    "key_indicators": [
      "DOGE/类似Meme币7日涨幅>100%",
      "热搜/社交媒体提及暴增",
      "交易所新增用户数激增",
      "合约资金费率极端正值(>0.1%)"
    ],
    "special_rules": {
      "entry": "确认催化剂+突破前3日高点+放量>2倍",
      "position": "初始仓位不超过总资金20%",
      "trailing_stop": "盈利>100%后启用小时级别ATR×3跟踪",
      "profit_lock": "涨幅每50%锁定20%利润"
    }
  }
}
```
