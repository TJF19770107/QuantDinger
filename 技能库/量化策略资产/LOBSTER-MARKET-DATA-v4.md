# LOBSTER-MARKET-DATA-v4.json

> ⚠️ **数据过期标注 [GAP-003]**: 行情快照日期为2026-05-31，当前已过7天。BTC/ETH/BNB等核心标的价格可能已发生显著变化，建议执行 `LOBSTER-MARKET-DATA-v5` 重新拉取CoinGecko/Binance最新行情。

原始格式: JSON

```json
{
  "pull_date": "2026-05-31",
  "pull_time": "2026-05-31 20:07:08",
  "source": "CoinGecko API (Binance blocked)",
  "note": "Binance API不可达(Python超时)，已通过CoinGecko+WebSearch补全关键行情",
  "prices": {
    "BTCUSDT": {
      "price": 73833,
      "24h_change_pct": 0.46,
      "source": "CoinGecko"
    },
    "ETHUSDT": {
      "price": 2019.66,
      "24h_change_pct": 0.25,
      "source": "CoinGecko"
    },
    "BNBUSDT": {
      "price": 721.57,
      "24h_change_pct": 7.24,
      "source": "CoinGecko"
    },
    "MYXUSDT": {
      "price": 0.2434,
      "24h_change_pct": -4.39,
      "source": "WebSearch/Binance Futures"
    }
  },
  "market_environment": {
    "btc_dominance": "BTC 73.8K高位震荡，山寨币分化",
    "altcoin_sentiment": "BNB +7.24%领涨，小市值山寨币活跃",
    "volatility_regime": "中高波动，适合动量策略"
  }
}
```
