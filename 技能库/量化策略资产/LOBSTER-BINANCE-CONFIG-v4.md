# LOBSTER-BINANCE-CONFIG-v4.json

> ⚠️ **缺口标注 [GAP-001]**: 标的清单缺少AI Agent代币板块（VIRTUAL USDT / LUNA USDT 等）。基于P0-006行动项和二次蒸馏趋势#1（AI×Crypto价值传导），建议在下一版本 `LOBSTER-BINANCE-CONFIG-v5` 中新增AI Agent代币专项监控列表。

原始格式: JSON

```json
{
  "version": "4.0.1",
  "strategy": "LobsterBlackHorseV4",
  "api_note": "需要配置API Key/Secret，权限：合约交易+读取",
  "exchange": {
    "name": "binance",
    "market": "futures",
    "testnet": false
  },
  "symbols": {
    "primary": [
      "MYXUSDT",
      "BNBUSDT",
      "PUMPBTCUSDT",
      "COAIUSDT",
      "AIAUSDT"
    ],
    "secondary": [
      "RIVERUSDT",
      "XPINUSDT",
      "AVNTUSDT",
      "MUSDT",
      "RAVEUSDT"
    ],
    "auto_discover": true,
    "min_volume_24h": 1000000,
    "max_concurrent": 8
  },
  "entry": {
    "momentum_breakout": {
      "enabled": true,
      "weight": 0.25
    },
    "pullback_support": {
      "enabled": true,
      "weight": 0.25
    },
    "volatility_breakout": {
      "enabled": true,
      "weight": 0.2
    },
    "trend_follow": {
      "enabled": true,
      "weight": 0.2
    },
    "reversal_sniper": {
      "enabled": true,
      "weight": 0.1
    }
  },
  "position": {
    "mode": "isolated",
    "leverage": {
      "default": 10,
      "max": 20
    },
    "sizing": {
      "L1": 0.05,
      "L2": 0.1,
      "L3": 0.15,
      "L4": 0.2,
      "L5": 0.5
    }
  },
  "risk": {
    "stop_loss_pct": 0.02,
    "trailing_stop": 0.03,
    "take_profit": [
      0.05,
      0.1,
      0.2
    ],
    "daily_loss_limit": 0.05,
    "max_drawdown": 0.15,
    "consecutive_loss_pause": 3,
    "liquidation_cooldown_hours": 24
  },
  "targets": {
    "monthly_return": "15-30%",
    "max_drawdown": "15%",
    "win_rate": "65%+",
    "pf_target": 1.5
  }
}
```
