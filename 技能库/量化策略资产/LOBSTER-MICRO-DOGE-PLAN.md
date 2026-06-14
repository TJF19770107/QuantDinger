# LOBSTER-MICRO-DOGE-PLAN.json

原始格式: JSON

```json
---
file_type: 策略文档
created: 2026-05-31
tags: [量化交易, DOGE, LOBSTER]
aliases: ['LOBSTER微型DOGE计划']
related: [[[LOBSTER-QUANT-20260531-001.json]]]
---

{
  "strategy_name": "龙虾DOGE微账户作战方案 v2.0",
  "account_fit": "51.48 USDT 微账户",
  "strategy_base": "black_horse_strategy + general_strategy 融合降频版",
  "timeframe": [
    "1D (主)",
    "4H (辅助确认)"
  ],
  "current_market_context": {
    "date": "2026-05-31",
    "note": "需实时拉取DOGE当前价格与指标，方案中提供阈值框架"
  },
  "entry_protocol": {
    "condition_1": {
      "indicator": "RSI(14)",
      "threshold": "55 < RSI < 75",
      "status": "待实时校验"
    },
    "condition_2": {
      "indicator": "MA排列",
      "threshold": "价格 > MA20 > MA50",
      "status": "待实时校验"
    },
    "condition_3": {
      "indicator": "MACD",
      "threshold": "柱状图为正且连续3日扩大",
      "status": "待实时校验"
    },
    "condition_4": {
      "indicator": "成交量",
      "threshold": "VOL > VOL_MA20 × 1.5",
      "status": "待实时校验"
    },
    "confirmation_required": "至少满足3/4条件 + 明确事件催化剂",
    "entry_size": "1.54 USDT (总资产3%)，试仓",
    "max_total_position": "15.48 USDT (合约主仓上限)"
  },
  "add_position_rules": {
    "trigger": "价格突破前高且回调不破MA20",
    "size_per_add": "总仓位5%（约2.57 USDT）",
    "max_adds": 2,
    "max_total_contract": "30.89 USDT（60%上限，含未实现盈亏）"
  },
  "stop_loss": {
    "hard_stop": "入场价 - ATR(14)×2.5 或 MA20下方3%，取较紧者",
    "max_loss_per_trade": "1.54 USDT (总资产3%)",
    "black_swan_stop": "30分钟内跌幅 > 15% → 市价全平"
  },
  "take_profit": {
    "level_1": "RSI > 85 → 减仓25%，锁定利润",
    "level_2": "盈利 > 50% → 启动MA10跟踪止损",
    "level_3": "盈利 > 100% → 锁定50%利润，剩余跑MA10",
    "level_4": "价格偏离MA20 > 40% → 减仓50%",
    "sell_the_news": "事件催化剂兑现当日，强制减仓70%"
  },
  "position_sizing_table": [
    {
      "stage": "观望",
      "contract_exposure": "0 USDT",
      "condition": "不足3/4入场条件"
    },
    {
      "stage": "试仓",
      "contract_exposure": "1.54 USDT (3x)",
      "condition": "满足3/4条件"
    },
    {
      "stage": "初仓",
      "contract_exposure": "7.74 USDT (3x)",
      "condition": "突破确认+成交量放大"
    },
    {
      "stage": "加仓1",
      "contract_exposure": "13.16 USDT (3x)",
      "condition": "突破前高+回踩MA20"
    },
    {
      "stage": "加仓2",
      "contract_exposure": "18.32 USDT (3x)",
      "condition": "趋势加速+RSI<75"
    },
    {
      "stage": "满仓",
      "contract_exposure": "23.22 USDT (3x)",
      "condition": "强趋势+事件催化"
    },
    {
      "stage": "止盈1",
      "contract_exposure": "减25%",
      "condition": "RSI>85"
    },
    {
      "stage": "止盈2",
      "contract_exposure": "减50%",
      "condition": "盈利>100%"
    },
    {
      "stage": "清仓",
      "contract_exposure": "0 USDT",
      "condition": "跌破MA20或催化剂兑现"
    }
  ],
  "risk_controls": {
    "max_daily_loss": "4.12 USDT (总资产8%) → 强制停止交易24h",
    "max_drawdown_per_trade": "1.54 USDT (总资产3%)",
    "correlation_limit": "Meme币板块总敞口不超过总仓位50%",
    "weekend_rule": "周六日合约仓位减半（流动性薄）",
    "news_blackout": "重大宏观事件（FOMC/CPI）前4小时清仓"
  },
  "meta": {
    "report_id": "LOBSTER-QUANT-20260531-001",
    "generated": "2026-05-31T10:30:00+08:00",
    "template": "龙虾全域官方模板.最终版",
    "咒语激活": "嗡阿喇巴札那谛",
    "account_snapshot_date": "2026-05-31",
    "version": "2.0.0"
  },
  "account_snapshot": {
    "total_assets": {
      "usdt": 51.48,
      "cny_approx": 348.5,
      "exchange_rate": 6.77
    },
    "daily_pnl": {
      "absolute_usdt": 16.52,
      "rate_percent": 41.13,
      "note": "极端单日收益，推测为高杠杆合约单向行情捕获"
    },
    "account_distribution": {
      "futures": {
        "usdt": 40.5,
        "percent": 78.7,
        "risk_level": "HIGH"
      },
      "spot": {
        "usdt": 6.9,
        "percent": 13.4,
        "risk_level": "LOW"
      },
      "alpha": {
        "usdt": 3.51,
        "percent": 6.8,
        "risk_level": "MEDIUM"
      },
      "funding": {
        "usdt": 0.57,
        "percent": 1.1,
        "risk_level": "CRITICAL_LOW"
      }
    },
    "profit_source_analysis": {
      "primary_driver": "合约高杠杆方向交易",
      "estimated_leverage_range": "10x - 50x",
      "sustainability": "不可线性外推，极端行情依赖度极高",
      "comparable_to_2021_DOGE": "类似2021-04-16脉冲行情(0.125→0.44)的单日收益率级别"
    }
  }
}
```
