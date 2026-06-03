# LOBSTER-VNPY-CONFIG-v4.json

> 原始文件: `LOBSTER-VNPY-CONFIG-v4.json`  |  类型: `.json`  |  自动转换

```json
{
  "strategy_name": "LobsterBlackHorseV4",
  "vt_symbols": [
    "MYXUSDT.BINANCE",
    "BNBUSDT.BINANCE",
    "PUMPBTCUSDT.BINANCE",
    "COAIUSDT.BINANCE",
    "AIAUSDT.BINANCE",
    "RIVERUSDT.BINANCE",
    "XPINUSDT.BINANCE",
    "AVNTUSDT.BINANCE"
  ],
  "class_name": "LobsterBlackHorseStrategy",
  "parameters": {
    "entry_momentum_period": 20,
    "momentum_vol_threshold": 1.5,
    "ma_short": 20,
    "ma_mid": 50,
    "ma_long": 100,
    "rsi_period": 14,
    "rsi_oversold": 25,
    "rsi_overbought": 75,
    "adx_period": 14,
    "adx_threshold": 25,
    "boll_period": 20,
    "boll_dev": 2.0,
    "vol_compression": 0.5,
    "max_positions": 8,
    "fixed_size": 1,
    "stop_loss_pct": 0.02,
    "take_profit_levels": [
      0.05,
      0.1,
      0.2
    ],
    "trailing_stop_pct": 0.03,
    "daily_loss_limit": 0.05,
    "max_drawdown": 0.15
  },
  "risk_control": {
    "single_trade_risk_pct": 0.02,
    "daily_risk_pct": 0.05,
    "max_drawdown_pct": 0.15,
    "max_positions": 8,
    "single_symbol_max_pct": 0.25
  }
}
```
