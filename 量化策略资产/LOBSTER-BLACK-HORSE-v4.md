# LOBSTER-BLACK-HORSE-v4.json

> 原始文件: `LOBSTER-BLACK-HORSE-v4.json`  |  类型: `.json`  |  自动转换

```json
{
  "strategy_name": "LOBSTER-BLACK-HORSE-v4",
  "version": "4.8",
  "created": "2026-05-31",
  "updated": "2026-06-01T20:00:00+08:00",
  "status": "active",
  "last_iteration_report": "币安龙头黑马预测报告_20260601_1900.md",
  "type": "breakout_momentum",
  "market": "perpetual_contract",
  "description": "龙虾黑马策略 v4.8 — v4.7基础 + 全域缺口专项补叠化。LAB专属参数精细优化：布林带外溢阈值30→22%、RSI上限75→72、贪婪熔断阈值70%→65%、熔断冷却48h→72h、ATR倍数2.5→2.2(常态)、仓位15%→12%、模拟交易期7→10天。新增7项LAB专属参数：追踪步长覆盖、RSI底背离要求、成交量峰值检测、停火重入延迟、资金费率上限、交易所风控监控、非对称盈亏比。",
  "design_philosophy": {
    "core_idea": "Breakout confirmation with volume validation and multi-factor scoring. Trend is friend, but discipline is life.",
    "signal_priority": "Only trade A-grade composite signals. B-grade = observe only, C-grade = no trade.",
    "no_trade_principle": "宁可踏空不可爆仓。永不满仓，保留30%以上备用金。极端行情触发贪婪熔断48h强制观望。代码强制止损——开仓API stopLossPrice必填，缺失拒绝执行。"
  },
  "core_indicators": [
    "EMA",
    "Volume_Profile",
    "RSI",
    "MACD",
    "Bollinger_Bands"
  ],
  "entry_rules": {
    "primary_breakout": {
      "condition": "价格突破布林带上轨（做多）/ 下轨（做空）",
      "confirmation": "成交量 > 20周期均量的 1.3 倍",
      "filter": "突破K线收盘价必须在布林带外侧",
      "volume_threshold_multiplier": 1.3,
      "entry_retracement_ratio": 0.382,
      "bollinger_extreme_pause": "价格超布林带上轨 30% 时触发暂停，不参与任何方向交易（v4.3新增，v4.4保持）"
    },
    "multi_factor_score": {
      "factors": {
        "ema_trend": "EMA20 > EMA50（做多）/ EMA20 < EMA50（做空）",
        "rsi_filter": "RSI(14) 30-75 之间（ETF催化标的），山寨币收紧至 30-75（v4.6优化：LAB极端超买显示80仍太激进）",
        "macd_histogram": "MACD 柱状图与价格方向同向且加速",
        "volume_breakout": "当前成交量 > 过去20周期均值 + 1.5标准差",
        "bollinger_position": "价格在布林带内或刚突破（不超30%），超30%触发暂停（v4.3新增，v4.4保持）"
      },
      "minimum_score": "5因子中至少4项达标方可入场（A级）",
      "etf_catalyst_weight": 0.3,
      "market_sentiment_filter": "恐惧贪婪指数 < 30时半仓，> 70时减仓；ETF催化标的（etf_exemption_flag=true）在恐惧区间可豁免半仓"
    },
    "signal_grade": {
      "A_grade": "主突破条件 + 5因子中≥4达标 + 布林带不超22% → 标准仓位",
      "B_grade": "主突破条件 + 5因子中≥3达标 + 布林带不超22% → 观望（不入场）",
      "C_grade": "主突破条件 + 2因子或以下 或 布林带超22% → 不入场"
    },
    "no_naked_short_rule": "多头趋势（EMA20>EMA50且价格高于EMA20）中禁止裸空；仅日线吞没阴线+MACD死叉+量能衰竭三条件同时满足方可做空。v4.5强化：三条件缺一不可，任一条件不满足禁止开空。极端多头行情（5日涨幅>80%）下做空三条件校验更加严格——需连续2根日线吞没阴线确认。",
    "pyramid_entry": {
      "status": "enabled",
      "description": "金字塔式加仓（v4.4新增）",
      "tier_1": {
        "ratio": 0.5,
        "condition": "入场信号触发",
        "description": "首仓50%"
      },
      "tier_2": {
        "ratio": 0.3,
        "condition": "浮盈 ≥ 3% + 4H EMA维持多头排列 + MACD未死叉",
        "description": "确认方向后追加30%"
      },
      "tier_3": {
        "ratio": 0.2,
        "condition": "浮盈 ≥ 8% + 日线收盘确认突破 + 成交量持续放量",
        "description": "趋势加速追加20%"
      },
      "anti_pyramid_rule": "禁止倒金字塔加仓。亏损状态下严禁追加仓位。"
    },
    "daily_trade_limit": {
      "status": "enabled",
      "max_trades_per_day": 3,
      "description": "每日交易上限3笔（v4.4新增）。达到上限后强制冷却，复盘当日所有交易后再决定次日操作。",
      "cooldown_action": "当日超限后禁止新开仓，仅允许平仓操作"
    },
    "extreme_market_circuit_breaker": {
      "status": "enabled",
      "version": "v4.5新增",
      "greed_circuit_breaker": {
        "trigger": "5日涨幅 > 65%",
        "action": "强制观望48小时，信号等级自动降一级（A→B, B→C）",
        "cooldown_hours": 72,
        "description": "贪婪熔断：极端上涨行情禁止追高，防止FOMO驱动交易"
      },
      "volatility_circuit_breaker": {
        "trigger": "5日振幅 > 100%",
        "action": "仓位上限从15%降至10%，杠杆上限从2x降至1x",
        "position_cap_override": 0.1,
        "leverage_override": 1,
        "description": "波动率熔断：极端波动环境自动收缩风险敞口"
      },
      "bollinger_extreme_no_entry": {
        "trigger": "价格超布林带22%以上",
        "action": "禁止任何方向新开仓，仅允许减仓或平仓",
        "description": "v4.8优化：阈值从25%收紧至22%，LAB极端行情(超46%)显示25%仍偏宽"
      }
    },
    "buy_trend_confirmation_delay": {
      "status": "enabled",
      "version": "v4.5新增",
      "confirmation_bars": 2,
      "bar_timeframe": "4H",
      "condition": "做多突破信号需连续2根4H阳线收盘确认后方可入场",
      "description": "BUY方向趋势确认延迟机制：防止极端行情下的假突破追高，尤其针对SELL偏好(90.29%)交易者做多时的确认偏误"
    },
    "etf_outflow_circuit_breaker": {
      "status": "enabled",
      "version": "v4.6新增",
      "trigger_5day": "ETF连续5日净流出 → 全账户杠杆降至1x",
      "trigger_10day": "ETF连续10日净流出 → 暂停所有新开仓（当前已触发10日$20亿流出）",
      "description": "ETF流出熔断（v4.6正式化）：机构资金持续流出是趋势反转的领先指标，不亚于技术面极端行情"
    },
    "fear_index_layering": {
      "status": "enabled",
      "version": "v4.6新增",
      "tier_30": "恐惧指数<30 → 半仓+杠杆1x",
      "tier_20": "恐惧指数<20 → 暂停新开仓",
      "tier_10": "恐惧指数<10 → 仅允许持有BTC",
      "current_value": 29,
      "current_tier": "tier_30（半仓+杠杆1x）",
      "description": "恐惧指数分层保护（v4.6正式化）：29逼近20触发线，需密切关注"
    },
    "lab_circuit_linkage": {
      "status": "enabled",
      "version": "v4.6新增",
      "trigger": "LAB触发贪婪熔断或波动率熔断 → 全BSC生态标的（BNB/CAKE/LISTA/TWT等）信号自动降级一级",
      "description": "LAB专属熔断联动（v4.6正式化）：LAB作为BSC生态'金丝雀'标的，其极端行情预示生态系统性风险"
    }
  },
  "exit_rules": {
    "stop_loss": {
      "type": "动态ATR止损",
      "atr_multiplier": 1.8,
      "atr_multiplier_altcoin": 2.5,
      "atr_period": 14,
      "max_loss_pct_single": 0.05,
      "max_loss_pct_single_mainstream": 0.03,
      "description": "止损价 = 入场价 - (ATR(14) × multiplier)。ETF催化标的 1.8，山寨币 2.5。单笔亏损上限：山寨币 ≤ 账户净值 5%，主流币 ≤ 3%。v4.5升级为代码强制：开仓API stopLossPrice为必填字段，缺省则拒绝开仓。每日UTC 0:00自动校验所有持仓止损状态。",
      "code_enforced": true,
      "daily_audit": true,
      "api_required_field": "stopLossPrice"
    },
    "take_profit": {
      "type": "追踪止盈 + 阶梯目标（自修复）",
      "trailing_pct": 0.04,
      "trailing_pct_altcoin_extreme": 0.03,
      "trailing_activation_threshold": 0.02,
      "target_1": {
        "pct": 0.08,
        "close_ratio": 0.3
      },
      "target_2": {
        "pct": 0.18,
        "close_ratio": 0.3
      },
      "target_3": {
        "pct": 0.3,
        "close_ratio": 0.4
      },
      "profit_ratio_repair": {
        "status": "enabled",
        "min_profit_ratio_target": 1.5,
        "trailing_step_initial": 0.01,
        "trailing_step_day3": 0.005,
        "trailing_step_day5": 0.003,
        "description": "盈亏比自修复追踪止盈算法（v4.3新增，v4.4强化）：盈亏比硬约束 ≥ 1.5:1。盈利达2%启动追踪止盈，步长随持仓时间收缩——第1天步长1%，第3天收缩至0.5%，第5天收缩至0.3%。"
      }
    },
    "time_exit": {
      "max_holding_days": 7,
      "description": "持仓超过7天强制平仓"
    },
    "reverse_signal_exit": {
      "description": "多因子评分降至1分或以下时强制平仓，不等待止损触发"
    }
  },
  "risk_management": {
    "max_position_risk_single": 0.05,
    "max_position_risk_single_mainstream": 0.03,
    "max_portfolio_risk": 0.06,
    "max_drawdown": 0.15,
    "leverage": {
      "default": 3,
      "max": 5,
      "altcoin_default": 2,
      "altcoin_max": 2,
      "max_leverage_condition": "信号强度A级且市场波动率处于30日低位；ETF催化A级信号可至4x；山寨币严格限制2x"
    },
    "daily_loss_limit": 0.05,
    "daily_loss_limit_altcoin_override": 0.03,
    "weekly_loss_limit": 0.1,
    "weekly_loss_action": "仓位降至50%",
    "monthly_loss_limit": 0.15,
    "monthly_loss_action": "暂停策略执行，全面复盘",
    "circuit_breaker": "三级熔断机制（v4.4升级）：日回撤≥5%暂停当日交易；周回撤≥10%降仓至50%；月回撤≥15%暂停策略。LAB单品种日亏损≥3%触发独立熔断。",
    "capital_reserve_rule": {
      "status": "enabled",
      "min_reserve_pct": 0.3,
      "description": "永不满仓，保留30%以上备用金应对极端行情（v4.4新增铁律）"
    },
    "etf_exemption": {
      "enabled": true,
      "condition": "标的具备ETF/机构催化因素时，恐惧贪婪指数低于sentiment_exemption_threshold仍可豁免半仓限制",
      "sentiment_exemption_threshold": 35
    },
    "post_liquidation_recovery": {
      "status": "enabled",
      "version": "v4.6强化",
      "recovery_days": 10,
      "max_position_pct": 0.03,
      "max_leverage": 0.5,
      "daily_trade_limit": 1,
      "profit_ratio_override": 2.0,
      "entry_confirmation_bars": 3,
      "description": "爆仓恢复期v4.6强化：爆仓后10天内仓位上限3%、杠杆0.5x、日交易上限1笔、盈亏比≥2.0、入场确认3根4H阳线。渐进重建信心，禁止报复性交易。恢复期从7→10天，仓位5%→3%，杠杆1x→0.5x"
    }
  },
  "position_sizing": {
    "method": "风险平价仓位",
    "formula": "仓位大小 = (账户净值 × 单笔风险比例) / (入场价与止损价之差)",
    "max_position_pct": 0.25,
    "max_position_pct_altcoin": 0.15,
    "min_position_notional": 100,
    "capital_allocation": {
      "breakout_strategy": 0.7,
      "scalp_strategy": 0.2,
      "reserve": 0.1
    },
    "total_exposure_limit": 0.7,
    "total_exposure_description": "总仓位上限70%，确保30%+备用金（v4.4新增）"
  },
  "backtest_parameters": {
    "start_date": "2025-01-01",
    "end_date": "2026-05-31",
    "initial_capital": 10000,
    "commission_rate": 0.0004,
    "slippage": 0.0001,
    "funding_rate_daily": 0.0001,
    "data_frequency": "1h",
    "benchmark": "BTC/USDT buy-and-hold",
    "metrics_required": [
      "total_return",
      "sharpe_ratio",
      "max_drawdown",
      "win_rate",
      "profit_factor",
      "calmar_ratio",
      "sortino_ratio"
    ],
    "out_of_sample_required": true,
    "out_of_sample_period": "最近3个月",
    "validation_threshold": "夏普比率 ≥ 原版90%，最大回撤 ≤ 原版110%"
  },
  "self_evolution_signals": {
    "profit_ratio_repair_algorithm": {
      "status": "enabled",
      "description": "盈亏比自修复追踪止盈算法：基于 68 笔 LAB 历史数据训练，盈利达 2% 启动追踪（步长 1%），随持仓时间动态收缩追踪步长。v4.4 盈亏比硬约束提升至 1.5:1。",
      "training_samples": 68,
      "last_trained": "2026-06-01",
      "hard_constraint": 1.5
    },
    "bollinger_extreme_pause": {
      "status": "enabled",
      "threshold": 0.22,
      "description": "价格超布林带上轨/下轨 30% 时触发趋势暂停",
      "backtest_result": "历史回测：LAB 极端外溢后 72h 回调概率 >80%"
    },
    "altcoin_rsi_differential": {
      "status": "enabled",
      "rsi_upper_altcoin": 72,
      "rsi_upper_etf": 75,
      "description": "山寨币 RSI 上限收紧至 75（v4.6优化：LAB极端超买显示80仍太激进）"
    },
    "overtrading_cooldown": {
      "status": "enabled",
      "max_trades_per_day": 3,
      "description": "过度交易冷却机制（v4.4新增）：每日交易上限3笔，超限后强制冷却，仅允许平仓"
    },
    "pyramid_position_building": {
      "status": "enabled",
      "tiers": [
        0.5,
        0.3,
        0.2
      ],
      "description": "金字塔加仓模块（v4.4新增）：首仓50%→确认追加30%→加速追加20%，禁止倒金字塔"
    },
    "extreme_market_circuit_breaker": {
      "status": "enabled",
      "version": "v4.5新增",
      "greed_pause_hours": 72,
      "volatility_amp_threshold": 1.0,
      "description": "极端行情熔断模块：5日涨幅>80%触发贪婪熔断48h，5日振幅>100%触发仓位收缩至10%/杠杆降至1x"
    },
    "buy_trend_confirmation_delay": {
      "status": "enabled",
      "version": "v4.5新增",
      "confirmation_bars": 2,
      "bar_timeframe": "4H",
      "description": "BUY方向趋势确认延迟机制：需连续2根4H阳线收盘确认突破，防止SELL偏好交易者做多时的确认偏误"
    },
    "stop_loss_code_enforcement": {
      "status": "enabled",
      "version": "v4.5新增",
      "api_required": true,
      "daily_audit": true,
      "description": "止损代码强制执行：开仓API stopLossPrice必填字段，每日UTC 0:00自动校验持仓止损状态，缺失则强制市价平仓"
    },
    "post_liquidation_recovery": {
      "status": "enabled",
      "version": "v4.6强化",
      "recovery_days": 10,
      "max_position_pct": 0.03,
      "max_leverage": 0.5,
      "daily_trade_limit": 1,
      "profit_ratio_override": 2.0,
      "entry_confirmation_bars": 3,
      "description": "LAB专属爆仓恢复期v4.6强化：10天内仓位3%/杠杆0.5x/日交易1笔上限。比通用恢复期更严格，因为LAB是唯一爆仓品种，心理创伤需更长时间恢复"
    },
    "bsc_ecosystem_health": {
      "status": "enabled",
      "version": "v4.5新增",
      "monitored_metrics": {
        "bsc_tvl": "$19.5B",
        "bsc_lsd_tvl": "$895M (占全链1.7%)",
        "bsc_meme_sector_cap": "$252M",
        "pancakeswap_tvl_status": "领先BSC DEX",
        "bsc_active_users": "待接入API实时数据"
      },
      "alert_thresholds": {
        "bsc_tvl_drop_20pct": "BSC TVL月度下降>20% → 全BSC生态标的自动降级一级",
        "bsc_lsd_growth_30pct": "BSC LSD TVL月度增长>30% → LISTA升级至A级关注",
        "pancakeswap_tvl_spike": "PancakeSwap TVL周增长>20% → CAKE自动升级至A级"
      },
      "description": "BSC生态健康度监控模块：实时追踪BSC TVL、LSD赛道、Meme板块、PancakeSwap TVL等核心指标，对BSC生态标的进行联动风控与信号增强"
    },
    "lab_exchange_risk_monitor": {
      "status": "enabled",
      "version": "v4.8新增",
      "description": "交易所风控监控模块：交易所降杠杆/调整费率 → 自动触发谨慎信号，LAB信号降一级"
    },
    "lab_volume_climax_cooling": {
      "status": "enabled",
      "version": "v4.8新增",
      "trigger": "24h成交量达7日均量3倍",
      "action": "48h冷却，禁止新开仓",
      "description": "LAB成交量峰值检测：放量过猛通常预示短期顶部"
    },
    "lab_funding_rate_guard": {
      "status": "enabled",
      "version": "v4.8新增",
      "trigger": "资金费率>+2%",
      "action": "禁止做多方向新开仓",
      "description": "LAB资金费率上限：>+2%极端环境多头成本过高"
    }
  },
  "lab_usdt_tuning": {
    "atr_multiplier": 2.2,
    "max_position_pct": 0.12,
    "leverage_max": 1,
    "stop_loss_hard": true,
    "daily_loss_limit_override": 0.03,
    "trailing_pct_altcoin_extreme": 0.03,
    "trailing_activation_threshold": 0.02,
    "rsi_upper_altcoin": 72,
    "bollinger_pause_threshold": 0.22,
    "bollinger_period_altcoin": 10,
    "no_naked_short": true,
    "profit_ratio_repair_algorithm": "enabled",
    "max_single_loss_pct": 0.05,
    "profit_ratio_hard_constraint": 1.5,
    "current_signal": "C级 — 七重否决严禁参与（战争+恢复期+贪婪+RSI+布林带+波动率+ETF流出）",
    "current_signal_detail": "EMA趋势✅ / 成交量✅ / RSI❌(>90) / MACD⚠️收窄 / 布林带❌(超上轨46%) + 战争熔断🔴 + 贪婪熔断🔴(72h) + 波动率熔断🔴 + 布林带极端外溢🔴 + 爆仓恢复期Day1/14🔴 + ETF流出熔断🔴",
    "recommended_entry_zone": "$5.50 - $5.95（条件：贪婪熔断48h冷却+RSI(4H)<75+布林带外溢<30%+MACD未死叉）",
    "entry_trigger": "①贪婪熔断48h冷却完成；②价格回落至$5.95以下；③RSI(4H)<75；④布林带外溢<30%；⑤MACD未出现日线死叉。5条件全满足=A级，缺1=B级，缺2=C级",
    "max_position_pct_normal": 0.15,
    "max_position_pct_description": "常态15%，极端行情（5日涨幅>80%或振幅>100%）自动降至10%",
    "leverage_max_normal": 2,
    "leverage_max_description": "常态2x，极端行情自动降至1x",
    "stop_loss_code_enforced": true,
    "stop_loss_api_required": true,
    "extreme_greed_pause_hours": 72,
    "extreme_volatility_amp_threshold": 1.0,
    "extreme_volatility_position_cap": 0.1,
    "extreme_volatility_max_leverage": 1,
    "post_liquidation_recovery_days": 10,
    "post_liquidation_max_position": 0.03,
    "post_liquidation_max_leverage": 0.5,
    "buy_trend_confirmation_bars": 2,
    "profit_ratio_extreme_override": 2.0,
    "post_liquidation_simulation_days": 10,
    "lab_trailing_step_initial_override": 0.008,
    "lab_trailing_step_initial_override_description": "LAB专属追踪止盈步长覆盖为0.8%（常态1%），适配更高波动",
    "lab_rsi_divergence_required": true,
    "lab_rsi_divergence_required_description": "LAB做多需RSI出现底背离，防止RSI>90时禁止做多形同虚设",
    "lab_volume_climax_detection": true,
    "lab_volume_climax_detection_trigger": "24h成交量达7日均量3倍 → 48h冷却",
    "lab_funding_rate_ceiling": 0.02,
    "lab_funding_rate_ceiling_description": "资金费率>+2%时禁止做多（当前MEXC +3%极端）",
    "lab_exchange_risk_monitor": true,
    "lab_exchange_risk_monitor_description": "交易所降杠杆/调整费率 → 自动触发谨慎信号",
    "lab_profit_ratio_asymmetric": {
      "long": 1.5,
      "short": 2.0
    },
    "lab_profit_ratio_asymmetric_description": "LAB盈亏比非对称：做多≥1.5，做空≥2.0（做空风险更高）"
  },
  "bnb_tuning": {
    "atr_multiplier": 1.8,
    "max_position_pct": 0.25,
    "leverage_max": 3,
    "stop_loss_hard": true,
    "daily_loss_limit_override": 0.03,
    "trailing_pct": 0.04,
    "trailing_activation_threshold": 0.02,
    "rsi_upper_etf": 75,
    "bollinger_pause_threshold": 0.3,
    "bollinger_period_etf": 20,
    "no_naked_short": true,
    "profit_ratio_repair_algorithm": "enabled",
    "max_single_loss_pct": 0.03,
    "profit_ratio_hard_constraint": 1.5,
    "current_signal": "C级 — 不参与（$687跌破$700和200MA，恐惧22极度恐惧，ETF连续9日净流出逼近10日熔断）",
    "current_signal_detail": "EMA趋势❌(价格在200MA下方) / RSI✅(40-45) / MACD❌(死叉/零轴下) / 布林带✅(接近下轨) / 成交量❌(下跌放量) | 恐惧22→半仓+杠杆1x | 爆仓恢复期仓位3%/杠杆0.5x | 多因子2/5=C级，ETF催化加成→B级，LAB联动降级→C级",
    "recommended_entry_zone": "等待收复$734并站稳2根4H阳线 + 恐惧指数≥35 + ETF资金流出逆转",
    "entry_trigger": "①价格收复$734并站稳2根4H阳线收盘确认；②RSI(4H)不处于超卖；③MACD出现底背离或金叉；④恐惧贪婪指数回升至35+；⑤BTC ETF出现单日净流入。5条件全满足=A级，缺1=B级，缺2=C级",
    "stop_loss_price": "$790（已触发）",
    "take_profit_levels": {
      "tp1": "待收复$734后重新计算",
      "tp2": "待收复$734后重新计算",
      "tp3": "待收复$734后重新计算"
    },
    "position_pct_actual": 0,
    "leverage_actual": 0.5,
    "risk_reward_ratio": "N/A（已止损出局）",
    "key_support": [
      "$670-$654（200日EMA+颈线位+OKX策略师强支撑）",
      "$644（50日MA）",
      "$600（心理关口）"
    ],
    "key_resistance": [
      "$700（心理关口，已失守）",
      "$716-$735（前区间上沿）",
      "$734（200日MA，关键阻力）"
    ],
    "fear_greed_override": "半仓规则（恐惧22 < 30）+ ETF流出熔断预警（连续9日净流出逼近10日阈值）",
    "stop_loss_code_enforced": true,
    "stop_loss_api_required": true,
    "buy_trend_confirmation_bars": 2,
    "profit_ratio_extreme_override": 2.0,
    "max_position_pct_normal": 0.3,
    "max_position_pct_description": "常态30%（主流币25% + ETF催化加成），恐惧指数<30时半仓降至15%",
    "leverage_max_normal": 3,
    "leverage_max_description": "常态3x，ETF催化A级可至4x",
    "short_three_condition_check": "三条件未同时满足：日线吞没阴线❌ + MACD死叉❌ + 量能衰竭⚠️ → 禁止裸空"
  },
  "iteration_log": [
    {
      "version": "4.8",
      "date": "2026-06-01T20:00:00+08:00",
      "report": "LAB_USDT永续合约交易分析报告_20260601_全域缺口专项补_v5.0.md",
      "changes": [
        "v4.7→v4.8 全域缺口专项补·量化策略叠化",
        "【P1】LAB布林带外溢阈值: 25%→22%（LAB超上轨46%显示25%仍偏宽）",
        "【P1】LAB RSI上限: 75→72（LAB>90时75形同虚设）",
        "【P1】贪婪熔断阈值: 70%→65%（LAB 5日96.68%显示70%触发过晚）",
        "【P1】贪婪熔断冷却时间: 48h→72h（极端行情需更久冷却）",
        "【P1】LAB ATR倍数(常态): 2.5→2.2（波动率收敛迹象，7日首现-9.85%回调）",
        "【P1】LAB仓位上限(常态): 15%→12%（聚焦TOP5，防止过度分散）",
        "【P1】模拟交易期: 7天→10天（延长以增强实盘信心）",
        "【P1】新增LAB专属参数N01: 追踪止盈步长覆盖0.8%",
        "【P1】新增LAB专属参数N02: RSI底背离要求做多",
        "【P1】新增LAB专属参数N03: 成交量峰值检测(3倍7日均量→48h冷却)",
        "【P1】新增LAB专属参数N04: 资金费率上限(>+2%禁止做多)",
        "【P1】新增LAB专属参数N05: 交易所风控监控(降杠杆→信号降级)",
        "【P1】新增LAB专属参数N06: 非对称盈亏比(做多≥1.5/做空≥2.0)",
        "【P0】新增全局参数N04: 停火重入延迟(停火后7天冷却期)",
        "【现状】LAB七重熔断同时激活 → 严禁任何方向新开仓",
        "【现状】BTC $73,678，恐惧指数29，美伊周末再次交火"
      ],
      "triggers": [
        "全域缺口专项补·量化策略叠化任务启动",
        "LAB仍处极端超买($12.03)，七重熔断全激活",
        "美伊周末再次交火：美军打击伊朗雷达站，革命卫队反击美军基地",
        "BTC ETF连续4周流出$42.1亿+，机构需求持续反转",
        "交易心理画像v2.3：三重认知根节点锁定(止损缺失/虚假安全感/战争脱敏)",
        "v4.7→v4.8叠化原则：从'通用山寨币参数'向'LAB专属精细化参数'进化"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T19:00:00+08:00",
      "report": "币安龙头黑马预测报告_20260601_1900.md",
      "changes": [
        "v4.7定时预测闭环：战争黑天鹅熔断持续激活 — 全账户暂停新开仓",
        "BNB C级 — $689（-4.79%），200MA $734未收复，多因子2/5，ETF催化部分定价，未来7-14天回调概率80%",
        "CAKE C级 — $1.56（+4.74%），与BNB脱钩需监控，无独立催化",
        "LAB七重熔断（战争+布林带+贪婪+RSI+波动率+爆仓恢复+ETF）→严禁参与",
        "LISTA/TWT C级 — 数据不足，BSC生态联动降级",
        "C01-C05候选参数：战争分级响应/ETF流出7日优化/恐惧脱敏反向指标/BNB-BTC相对强弱/CAKE-BNB脱钩监控",
        "ETF连续3周流出$42.1亿，本周$16.7亿（2026年第二大周流出），机构需求引擎持续反转",
        "恐惧指数29（异常偏高）— 战争脱敏警示激活，v4.7 fear_desensitization_warning生效"
      ],
      "triggers": [
        "每2小时定时预测闭环触发",
        "美伊军事冲突持续，BTC从$80K→$73K（-8.75%），战争黑天鹅熔断激活",
        "BTC ETF连续3周流出$42.1亿，本周$16.7亿为2026年单周第二大流出",
        "恐惧贪婪指数29（恐惧但异常偏高），战争脱敏风险",
        "全网24h爆仓$1.93亿，空头近时段反遭轧空($35.74M空)",
        "BNB $689（-4.79%）异常弱于大盘，200MA $734关键阻力未收复",
        "LAB六重熔断+爆仓恢复期Day 1/14，七重否决",
        "PCE通胀3.8%偏高，美联储降息无望，可能升息"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T18:00:00+08:00",
      "report": "币安龙头黑马预测报告_20260601_1800.md",
      "changes": [
        "v4.6定时预测闭环：宏观恶化——恐惧指数22(极度恐惧)、ETF连续9日净流出逼近10日熔断、BNB -5.26%跌破$700和200MA",
        "全线C级/熔断禁止，本轮零开仓。v4.6三层保护机制（恐惧分层+ETF熔断+LAB联动）同时激活",
        "v4.7候选建议：ETF流出熔断7日优化、恐惧指数BTC豁免、BNB-BTC相对强弱指标、LAB流动性熔断",
        "bnb_tuning：信号更新，支撑/阻力位重算，入场条件0/5不满足",
        "candidate参数评估：C01-C04四个新建议"
      ],
      "triggers": [
        "每2小时定时预测闭环触发",
        "恐惧贪婪指数从29降至22（极度恐惧），逼近tier_20暂停新开仓触发线",
        "BTC ETF连续9日净流出$14.2亿/周，逼近10日熔断阈值",
        "BNB -5.26%跌破$700心理支撑和200MA($734)，异常弱于BTC(-0.7%)",
        "全网$1.91亿-$2.07亿爆仓，多头持续失血",
        "PCE通胀3.8%偏高，美伊谈判延长一周，宏观压力不减",
        "LAB $12.52 +192.43%周涨幅，Connors RSI 95.40，流动性/市值比0.22%"
      ],
      "verified": false
    },
    {
      "date": "2026-05-31T14:00:00+08:00",
      "report": "币安龙头黑马预测报告_20260531_1400.md",
      "changes": [
        "v1.0→v4.0初始参数"
      ],
      "verified": false
    },
    {
      "date": "2026-05-31T23:00:00+08:00",
      "report": "币安龙头黑马预测报告_20260531_2300.md",
      "changes": [
        "v4.0→v4.1迭代"
      ],
      "verified": false
    },
    {
      "date": "2026-05-31T23:53:48+08:00",
      "report": "币安龙头黑马预测报告_20260531_2353.md",
      "changes": [
        "v4.1差异化风控"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T00:00:00+08:00",
      "report": "LAB-USDT永续合约交易分析报告_20260601.md",
      "changes": [
        "v4.1→v4.2 LAB专属"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T03:00:00+08:00",
      "report": "LAB-USDT永续合约交易分析报告_20260601_v2.md",
      "changes": [
        "v4.2→v4.3叠化：ATR 2.0→2.5，仓位25%→15%，杠杆3x→2x，日熔断5%→3%",
        "新增布林带极端外溢暂停（超30%），新增禁止裸空规则",
        "新增盈亏比自修复追踪止盈算法",
        "山寨币RSI上限80→75收紧，多因子4→5因子",
        "止盈2阶梯→3阶梯，新增self_evolution_signals模块"
      ],
      "triggers": [
        "LAB $8.70极端超买",
        "5日+98% 振幅118%",
        "爆仓$7.461",
        "盈亏比0.27全局最差"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T06:00:00+08:00",
      "report": "LABUSDT永续合约交易分析报告.md",
      "changes": [
        "v4.3→v4.4全域专家模式蒸馏迭代",
        "盈亏比硬约束 1.0→1.5",
        "单笔最大亏损 2%→3%-5%弹性区间（山寨币5%/主流币3%）",
        "新增金字塔加仓模块（50%→30%→20%三批建仓）",
        "新增每日交易上限3笔 + 冷却机制",
        "新增资金管理铁律：总仓位≤70%，保留30%+备用金",
        "回撤熔断升级为三级：日5%/周10%/月15%",
        "阶梯止盈目标上调：TP1 3%→8%, TP2 6%→18%, TP3 10%→30%",
        "止盈平仓比例调整：30/30/40（原30/30/40不变，比例优化）",
        "新增 out_of_sample_required 回测验证门槛"
      ],
      "triggers": [
        "全域专家模式蒸馏：7项核心交易心理特征重塑",
        "交易者类型转型：高频日内→波段交易",
        "风险偏好更新：稳健进取型（单笔回撤3-5%）",
        "持仓周期调整：4H-日线波段为主",
        "资金管理强化：金字塔加仓+永不满仓+30%备用金"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T07:00:00+08:00",
      "report": "币安龙头黑马预测报告_20260601_0700.md",
      "changes": [
        "v4.4 定时预测闭环：币安龙头黑马全量扫描",
        "BNB综合评级A级（92/100），做多方向确认",
        "CAKE综合评级B级（68/100），观望待PancakeSwap催化",
        "LABUSDT评级B级（55/100），布林带超上轨46%+RSI>90触发极端外溢暂停",
        "新增策略优化建议 O01-O05（BNB专属参数/CAKE触发阈值/LAB情绪指标/实时数据管道/多时间框架确认）"
      ],
      "triggers": [
        "每2小时定时预测闭环触发",
        "BNB机构ETF催化+生态爆发预期",
        "LAB $8.6953 极端超买（5日+96.68%），布林带暂停保护激活",
        "CAKE缺乏独立催化，需等待BSC TVL突破"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T07:50:00+08:00",
      "report": "LAB-USDT永续合约交易分析报告_20260601_v3.md",
      "changes": [
        "v4.4→v4.5叠化：LAB爆仓事件深度复盘驱动",
        "【P0】止损从文档规则升级为代码强制：开仓API stopLossPrice必填，每日自动校验",
        "【P0】新增极端行情熔断模块：贪婪熔断48h（5日涨幅>80%）+ 波动率熔断（5日振幅>100%仓位降至10%/杠杆1x）",
        "【P0】布林带极端外溢从'暂停'升级为'禁止新开仓'",
        "【P1】BUY方向新增趋势确认延迟：需连续2根4H阳线确认突破",
        "【P1】做空三条件强制校验：缺一不可，极端行情下需连续2根日线吞没阴线",
        "【P1】新增爆仓恢复期规则：7天仓位5%/杠杆1x",
        "【P1】极端行情盈亏比硬约束自动提升至2.0（常态1.5）",
        "lab_usdt_tuning全量重评估：max_position_pct=0.10(极端)/0.15(常态)，leverage=1x(极端)/2x(常态)，信号从B级→C级",
        "current_optimized_values新增11个参数",
        "self_evolution_signals新增4个模块"
      ],
      "triggers": [
        "LAB $7.461爆仓事件深度复盘：止损=0是直接原因，认知-执行鸿沟是根因",
        "LAB极端多头行情持续：$8.6953，5日+96.68%，振幅118%，布林带超上轨46%，RSI>90",
        "交易心理画像v1.6蒸馏：核心发现——v1.5认知框架完整但执行层断裂",
        "三重熔断同时触发：布林带极端外溢 + 贪婪熔断 + RSI极端超买"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T11:51:00+08:00",
      "report": "币安龙头黑马预测报告_20260601_1151.md",
      "changes": [
        "v4.5 定时预测闭环：币安龙头黑马全量扫描",
        "BNB综合评级C级 — 价格$707已跌破止损$790和支撑$734，双重失守",
        "CAKE综合评级B级 — PancakeSwap基本面扎实但缺乏独立催化",
        "LISTA/TWT数据不足，纳入下轮扫描清单",
        "宏观环境恶化：恐惧指数29、BTC ETF连续9日净流出、$526M爆仓",
        "新增策略优化建议 O01-O05（基本面-价格背离度/ETF流出熔断/恐惧指数分层/止损后反弹再入场/API数据管道）",
        "bnb_tuning参数全量更新：信号B→C，仓位15%→0%，杠杆2x→1x，支撑/阻力位重算"
      ],
      "triggers": [
        "每2小时定时预测闭环触发",
        "BNB -4.64%远超BTC -1.32%，异常弱势",
        "BTC ETF连续9日净流出，机构需求引擎反转",
        "恐惧指数29持续恐惧区间",
        "全网$526M爆仓，多头重创"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T16:26:00+08:00",
      "report": "币安龙头黑马预测报告_20260601_1626.md",
      "changes": [
        "v4.5 定时预测闭环：币安龙头黑马全量扫描",
        "BNB综合评级B级 — VanEck ETF+产品发布+GENIUS空投三重催化，但利好兑现80%回调概率",
        "BNB价格$711-$733，多因子仅2/5(C级)，ETF催化加成至B级观望",
        "CAKE评级C级 — PancakeSwap TVL $1.1B未突破，缺乏独立催化",
        "LAB三重熔断+爆仓恢复期 — 严禁参与",
        "宏观恶化：恐惧29、BTC ETF连续10日流出>$20亿、全网$2.48亿爆仓、美伊地缘悬而未决",
        "v4.6候选参数触发评估：ETF流出熔断线(10日)已触发，恐惧指数分层(<20)逼近触发",
        "策略建议O07-O10：ETF流出熔断/恐惧指数分层正式化(P0) + 基本面背离度/止损再入场(P1) + 社交过热降级(P2)",
        "bnb_tuning参数更新：支撑$670→$670-$654扩展，阻力$716→$716-$735扩展，MACD恶化标注",
        "爆仓恢复期Day 1/7，仓位5%/杠杆1x硬约束，本轮零开仓"
      ],
      "triggers": [
        "每2小时定时预测闭环触发",
        "BNB +11%驱动：VanEck ETF+币安产品发布+GENIUS空投",
        "BTC ETF连续10日净流出>$20亿，机构需求引擎反转",
        "全网$2.48亿爆仓/104,342人，多头重创",
        "恐惧指数29，已持续一周<30",
        "美伊谈判延长一周，地缘风险悬而未决"
      ],
      "verified": false
    },
    {
      "date": "2026-06-01T16:45:00+08:00",
      "report": "LAB_USDT永续合约交易分析报告_20260601_全域缺口专项补.md",
      "changes": [
        "v4.5→v4.6全域缺口专项补·量化策略叠化",
        "【P0】ETF流出熔断正式化：连续10日净流出 → 暂停所有新开仓",
        "【P0】恐惧指数分层正式化：<20暂停新开仓，<10仅允许持有BTC",
        "【P0】LAB专属熔断联动：LAB触发贪婪熔断时，全BSC生态标的自动降级一级",
        "【P1】贪婪熔断阈值优化：80%→70%（LAB显示80%仍太激进）",
        "【P1】布林带外溢阈值优化：30%→25%（LAB超上轨46%显示30%仍太激进）",
        "【P1】山寨币RSI上限优化：80→75（LAB RSI>90显示80仍太激进）",
        "【P1】爆仓恢复期强化：恢复期7→10天，仓位5%→3%，杠杆1x→0.5x，日交易1笔上限，盈亏比≥2.0，入场确认3根4H阳线",
        "【P2】基本面-价格背离度指标：RWA TVL增长>50%且价格下跌>20% → 信号+1级",
        "【P2】止损后反弹再入场：止损出局后48h内价格收复止损价+1% → 允许半仓重新入场",
        "【P2】社交过热降级：Twitter/X提及量24h增长>500% → 信号自动-1级",
        "【P2】多交易所数据聚合：整合MEXC/Binance/OKX的LAB数据，取中位数",
        "【P2】链上数据监控：LAB持币地址变化>20% → 信号调整",
        "【P2】期权数据集成：期权IV>150% → 波动率预警",
        "v4.6候选参数正式化：etf_outflow_circuit_breaker, fear_index_layering, lab_circuit_linkage 从candidate升级为正式参数",
        "交易心理画像v1.9→v2.0：LAB专项画像全量更新，三重熔断+恢复期硬约束，情绪状态'谨慎乐观'→'冷静等待'"
      ],
      "triggers": [
        "全域缺口专项补任务启动：嗡阿喇巴札那谛，龙虾五步法启动",
        "LAB极端行情：$11.95-$12.03，突破前高$8.67，布林带超上轨46%，RSI>90",
        "三重熔断同时触发：布林带极端外溢+贪婪熔断+波动率熔断+爆仓恢复期",
        "MEXC调整资金费率：+3%/-3%每小时结算，杠杆100x→50x",
        "交易心理画像v2.0蒸馏：基于LAB $7.461爆仓和$11.95极端行情双重心理锚点",
        "v4.6候选参数评估完成：ETF流出熔断(10日)已触发，恐惧指数分层(29<30)逼近触发"
      ],
      "verified": false
    },
    {
      "version": "4.7",
      "date": "2026-06-01T19:00:00+08:00",
      "changes": [
        "【P0】战争黑天鹅熔断：美伊军事冲突触发全账户暂停新开仓，仅允许减仓/平仓；冲突升级为全面战争→全账户清仓+恢复期重置Day 0",
        "【P0】爆仓恢复期强化：10→14天，最大仓位3%→2%，新增7天模拟交易期（恢复期结束后强制执行），抄底禁止令（24h跌幅>15%+恐惧<25→72h禁止抄底）",
        "【P0】仓位渐进恢复：2%→5%→10%三阶段，分别需模拟期盈利/连续5笔盈利/连续10笔盈利+战争结束",
        "【P1】回撤阈值收紧：日5%→3%，周10%→7%，月15%→10%，战争环境需更敏感熔断",
        "【P1】战争ATR倍数：山寨币止损倍数 2.5→3.5，适应战争环境极端波动",
        "【P1】恐惧脱敏预警：恐惧指数29但战争进行中→触发'虚假安全感'预警，防止交易者麻痹大意",
        "【P2】创伤后评估机制：恢复期后强制7天模拟交易验证策略有效性",
        "新增参数：war_black_swan_enabled, post_liquidation_simulation_days, anti_dip_buying_ban_*, war_atr_multiplier_altcoin, drawdown_daily/weekly/monthly_limit, fear_desensitization_warning_enabled, position_progressive_recovery_tiers",
        "交易心理画像v2.1→v2.2：新增宏观黑天鹅·美伊战争附录，第三认知根节点'创伤后虚假安全感'，情绪状态🟡谨慎乐观→🔴防御观望"
      ],
      "triggers": [
        "全域缺口专项补任务：嗡阿喇巴札那谛，龙虾五步法启动",
        "美伊战争黑天鹅：美国6月1日打击伊朗Goruk和Qeshm岛，BTC $80K→$73K暴跌8.75%",
        "BTC ETF连续9日净流出$28亿，三周累计流出$42.1亿，逼近10日熔断阈值",
        "恐惧贪婪指数29（恐惧但异常偏高），战争脱敏风险",
        "LAB极端高位：$11.95-$12.03，布林带超上轨46%，RSI>90，六重熔断触发",
        "交易心理画像v2.2蒸馏：爆仓后空仓无意中规避黑天鹅→识别'虚假安全感'",
        "war_black_swan_circuit_breaker从零创建（v4.6无此概念）"
      ],
      "verified": false
    }
  ],
  "parameters_to_optimize": [
    "ema_fast_period",
    "ema_slow_period",
    "rsi_period",
    "rsi_upper",
    "rsi_lower",
    "atr_multiplier",
    "trailing_pct",
    "bollinger_period",
    "bollinger_std",
    "volume_threshold_multiplier",
    "entry_retracement_ratio",
    "etf_catalyst_weight",
    "market_sentiment_upper",
    "market_sentiment_lower",
    "etf_exemption_flag",
    "sentiment_exemption_threshold",
    "bollinger_pause_threshold",
    "profit_ratio_repair_enabled",
    "trailing_activation_threshold",
    "no_naked_short",
    "pyramid_tier_ratios",
    "daily_trade_limit",
    "max_single_loss_pct",
    "capital_reserve_pct",
    "extreme_greed_pause_hours",
    "extreme_volatility_amp_threshold",
    "extreme_volatility_position_cap",
    "extreme_volatility_max_leverage",
    "post_liquidation_recovery_days",
    "stop_loss_code_enforced",
    "buy_trend_confirmation_bars",
    "profit_ratio_extreme_override"
  ],
  "v4.6_candidate_parameters": {
    "etf_outflow_circuit_breaker": {
      "status": "formalized",
      "formalized_in": "v4.6",
      "description": "已正式化到 extreme_circuit_breakers.etf_outflow_circuit_breaker"
    },
    "fear_index_tiers": {
      "status": "formalized",
      "formalized_in": "v4.6",
      "description": "已正式化到 extreme_circuit_breakers.fear_index_layering"
    },
    "lab_circuit_linkage": {
      "status": "formalized",
      "formalized_in": "v4.6",
      "description": "已正式化到 extreme_circuit_breakers.lab_circuit_linkage"
    },
    "fundamental_divergence_bonus": {
      "status": "proposed",
      "trigger": "RWA TVL增长>50% 且 价格下跌>20% → 信号自动+1级",
      "description": "基本面-价格背离度指标（P1候选）：捕捉被恐慌错杀的优质标的"
    },
    "stop_loss_reentry_rule": {
      "status": "proposed",
      "trigger": "止损出局后48h内价格收复止损价+1% → 允许半仓重新入场",
      "description": "止损后反弹再入场逻辑（P1候选）：防止止损后踏空反弹"
    },
    "social_overheat_degration": {
      "status": "proposed",
      "trigger": "Twitter/X提及量24h增长>500% → 信号自动-1级",
      "description": "社交过热降级（P2候选）：防止社交狂热驱动FOMO交易"
    },
    "multi_exchange_aggregation": {
      "status": "proposed",
      "trigger": "整合MEXC/Binance/OKX的LAB数据取中位数",
      "description": "多交易所数据聚合（P2候选）：防止单一交易所价格/费率操纵"
    },
    "onchain_holder_monitor": {
      "status": "proposed",
      "trigger": "LAB持币地址数变化>20% → 信号调整",
      "description": "链上数据监控（P2候选）：大户动向是价格的领先指标"
    },
    "options_iv_monitor": {
      "status": "proposed",
      "trigger": "期权IV>150% → 波动率高级预警",
      "description": "期权数据集成（P2候选）：IV异常飙升预示极端波动"
    }
  },
  "v4.7_candidate_parameters": {
    "war_escalation_tiered_response": {
      "status": "proposed",
      "priority": "P0",
      "trigger": "局部冲突→全账户暂停新开仓（当前）; 全面战争→全账户清仓+恢复期重置Day 0（占位）",
      "description": "C01 战争黑天鹅分级响应：当前v4.7仅支持单一'全账户暂停'，实际局部冲突与全面战争风险级别不同，需两档差异化响应"
    },
    "etf_outflow_7day_early_warning": {
      "status": "proposed",
      "priority": "P0",
      "trigger": "ETF连续7日净流出并累计>$20亿 → 提前触发半仓+杠杆1x预警",
      "description": "C02 ETF流出预警线从10日优化为7日：当前已连续3周流出$42.1亿，10日阈值太慢"
    },
    "fear_desensitization_contrary_indicator": {
      "status": "proposed",
      "priority": "P1",
      "trigger": "恐惧指数>25 且 战争/重大黑天鹅进行中 → 触发额外谨慎信号，自动降仓至30%",
      "description": "C03 恐惧脱敏反向指标：恐惧指数29在战争背景下异常偏高，需识别虚假安全感"
    },
    "bnb_btc_relative_strength": {
      "status": "proposed",
      "priority": "P1",
      "trigger": "BNB/BTC比率跌破0.009 → BNB信号自动降级一级",
      "description": "C04 BNB-BTC相对强弱：当前BNB -4.79%远超BTC -0.72%，相对弱势异常"
    },
    "cake_bnb_decoupling_monitor": {
      "status": "proposed",
      "priority": "P2",
      "trigger": "CAKE涨>3% 且 BNB跌>3% 同日 → CAKE信号自动降级一级",
      "description": "C05 CAKE与BNB脱钩监控：当前CAKE +4.74%但BNB -4.79%，生态领头羊弱势时小弟独立上涨不可持续"
    }
  },
  "current_optimized_values": {
    "rsi_upper": 72,
    "rsi_upper_altcoin": 72,
    "bollinger_std": 2.2,
    "volume_threshold_multiplier": 1.3,
    "entry_retracement_ratio": 0.382,
    "etf_catalyst_weight": 0.3,
    "market_sentiment_upper": 70,
    "market_sentiment_lower": 30,
    "etf_exemption_flag": true,
    "sentiment_exemption_threshold": 35,
    "atr_multiplier_etf": 1.8,
    "atr_multiplier_altcoin": 2.2,
    "trailing_pct": 0.04,
    "bollinger_period_altcoin": 10,
    "trailing_pct_altcoin_extreme": 0.03,
    "trailing_activation_threshold": 0.02,
    "bollinger_pause_threshold": 0.22,
    "no_naked_short": true,
    "profit_ratio_repair_enabled": true,
    "profit_ratio_hard_constraint": 1.5,
    "max_position_pct_altcoin": 0.12,
    "leverage_altcoin_max": 2,
    "daily_loss_limit_altcoin": 0.03,
    "max_single_loss_pct_altcoin": 0.05,
    "max_single_loss_pct_mainstream": 0.03,
    "daily_trade_limit": 3,
    "capital_reserve_pct": 0.3,
    "pyramid_tier_ratios": [
      0.5,
      0.3,
      0.2
    ],
    "extreme_greed_pause_hours": 72,
    "extreme_volatility_amp_threshold": 1.0,
    "extreme_volatility_position_cap": 0.1,
    "extreme_volatility_max_leverage": 1,
    "post_liquidation_recovery_days": 14,
    "post_liquidation_max_position": 0.02,
    "post_liquidation_max_leverage": 0.5,
    "post_liquidation_simulation_days": 10,
    "post_liquidation_simulation_required": true,
    "anti_dip_buying_ban_trigger_24h_drop_pct": 0.15,
    "anti_dip_buying_ban_trigger_sentiment": 25,
    "anti_dip_buying_ban_cooling_hours": 72,
    "war_black_swan_enabled": true,
    "war_black_swan_action": "halt_all_new_positions_allow_close_only",
    "war_black_swan_escalation": "full_liquidation_reset_recovery_day_zero",
    "war_black_swan_deescalation_condition": "ceasefire_signed_plus_72h_no_attack",
    "war_atr_multiplier_altcoin": 3.5,
    "drawdown_daily_limit": 0.03,
    "drawdown_weekly_limit": 0.07,
    "drawdown_monthly_limit": 0.1,
    "fear_desensitization_warning_enabled": true,
    "position_progressive_recovery_tiers": [
      0.02,
      0.05,
      0.1
    ],
    "position_progressive_recovery_conditions": [
      "sim_period_win",
      "5_consecutive_win",
      "10_consecutive_win_war_over"
    ],
    "stop_loss_code_enforced": true,
    "stop_loss_api_required": true,
    "buy_trend_confirmation_bars": 2,
    "profit_ratio_extreme_override": 2.0,
    "max_position_pct_altcoin_normal": 0.15,
    "lab_trailing_step_initial_override": 0.008,
    "lab_rsi_divergence_required": true,
    "lab_volume_climax_trigger_multiplier": 3.0,
    "lab_volume_climax_cooldown_hours": 48,
    "lab_funding_rate_ceiling": 0.02,
    "lab_exchange_risk_monitor": true,
    "lab_profit_ratio_asymmetric_long": 1.5,
    "lab_profit_ratio_asymmetric_short": 2.0
  },
  "war_ceasefire_reentry_delay_days": 7,
  "war_ceasefire_reentry_delay_description": "v4.8新增：停火后72h→7天冷却期，防止假停火陷阱。停火协议签署后需等待7天无攻击方可解除战争熔断。",
  "v4.9_candidates": {
    "C04_bnb_btc_relative_strength": {
      "status": "candidate",
      "description": "BNB已连续两周跑输BTC。当BNB/BTC比率跌破0.0094(当前~0.0094)关键支撑时触发额外预警。此指标可提前感知BNB生态资金流出。",
      "suggested_threshold": 0.0090,
      "action": "BNB/BTC<阈值→BNB相关标的降为D级，自动排除做多候选"
    },
    "C05_etf_outflow_weighted": {
      "status": "candidate",
      "description": "当前连续10日触发，不考虑量级。建议增加累计日均流出>$5B作为并行触发条件，提升熔断精准度。",
      "suggested_threshold": "连续10日 且 日均流出>$5B"
    },
    "C06_lab_cooldown_timer": {
      "status": "candidate",
      "description": "LAB连续多周期处于极端区域(RSI>72)。建议加入冷却计时器：需在正常波动区间(RSI<72且布林带外溢<22%)停留≥6个周期方可解除禁令。",
      "suggested_cooldown_cycles": 6
    },
    "C07_recovery_position_ladder": {
      "status": "candidate",
      "description": "当前爆仓恢复期Day1-14统一2%仓位×0.5x杠杆。建议Day8+适度放宽至5%×1x(若战争解除+ETF转流入+恐惧>40同时满足)。",
      "phase": {
        "day1_7": {"max_position_pct": 0.02, "max_leverage": 0.5},
        "day8_14": {"max_position_pct": 0.05, "max_leverage": 1.0, "requires": ["war_ceasefire", "etf_inflow_resumed", "fear_greed_above_40"]}
      }
    }
  },
  "strategy_iteration_log": {
    "v4.0": {"date": "2026-05", "trigger": "初始版本", "report": ""},
    "v4.1_4.6": {"date": "2026-05_06-01", "trigger": "多轮迭代至4.6", "report": "见报告库"},
    "v4.7": {"date": "2026-06-01", "time": "12:00", "trigger": "BNB跌破$687创3个月新低，LAB涨60%+触发4项否决", "report": "币安龙头黑马预测报告_20260601_1200.md", "key_changes": ["BNB评级B→C","LAB专属否决项1-4激活","BNB/CAKE/LISTA/TWT专属参数新增"]},
    "v4.7_update": {"date": "2026-06-01", "time": "14:00", "trigger": "战情维持，市场整体下沉", "report": "币安龙头黑马预测报告_20260601_1400.md", "key_changes": ["LAB风控参数无变化","BNB $680-$687","战争黑天鹅确认"]},
    "v4.7_update2": {"date": "2026-06-01", "time": "16:00", "trigger": "LAB涨至$8.68，新增否决项5-7", "report": "币安龙头黑马预测报告_20260601_1600.md", "key_changes": ["LAB否决项扩至7项","新增LAB 24h成交量异常/盘口深度/低流通高FDV否决"]},
    "v4.8": {"date": "2026-06-01", "time": "18:00", "trigger": "新增爆仓恢复机制+停火冷却期+七大LAB否决项固化", "report": "币安龙头黑马预测报告_20260601_1800.md", "key_changes": ["LAB爆仓$7.461→爆仓恢复期14天(仓位2%/杠杆0.5x)","停火冷却72h→7天","7项LAB否决固化","LAB交易参数7项新增"]},
    "v4.8_snapshot": {"date": "2026-06-01", "time": "20:00", "trigger": "BNB从$707继续下行至$695(-5.4%/24h)，战情延续(美军打击伊朗Goruk/Qeshm岛)", "report": "币安龙头黑马预测报告_20260601_2000.md", "key_changes": ["BNB跌破$700，距200MA($734)差-5.3%","CAKE $1.44 RSI47.91中性","LAB $12.52(+192%周)7否决全激活","ETF流出第9日预警","新增v4.9候选4项(C04~C07)"]}
  }
}
```
