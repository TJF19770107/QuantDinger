# LOBSTER-BLACK-HORSE-v4.json

原始格式: JSON

```json
{
  "strategy_name": "LOBSTER-BLACK-HORSE-v4",
  "version": "4.12.11",
  "edition": "PERSONALIZED — 专属交易者适配版",
  "created": "2026-05-31",
  "updated": "2026-06-05 08:44:25",
  "status": "ACTIVE_CONTINUOUS_ITERATION",
  "last_iteration_report": "LAB_USDT永续合约交易分析报告_20260605.md",
  "type": "breakout_momentum",
  "market": "perpetual_contract",
  "description": "龙虾黑马策略 v4.12.11 专属版 — v4.12.10→v4.12.11全域缺口专项补·叠化。第七认知根节点「谈判信号反复依赖症」从候选正式确认。新增S22(LAB溢价回归检测)/S23(战争降级72h延迟)/S24(恐惧回升谈判过滤)三参数正式激活。七重熔断7.0/7.0维持，全账户零开仓，60天冷却。",
  "design_philosophy": {
    "core_idea": "Breakout confirmation with volume validation and multi-factor scoring. Trend is friend, but discipline is life.",
    "signal_priority": "Only trade A-grade composite signals. B-grade = observe only, C-grade = no trade.",
    "no_trade_principle": "宁可踏空不可爆仓。永不满仓，保留30%以上备用金。极端行情触发贪婪熔断48h强制观望。代码强制止损——开仓API stopLossPrice必填，缺失拒绝执行。",
    "v4.12.4_taoist": "道家心法八条融入策略哲学：道可道非常道（市场不可预测）、天之道利而不害（顺势不逆势）、为学日益为道日损（减频提质）、知止不殆（熔断即止）、知足不辱（阶梯止盈）、致虚极守静笃（空仓是策略）、反者道之动（暴跌即反转前兆但需确认）、大巧若拙（简单规则胜复杂模型）",
    "v4.12.5_taoist": "道家心法八条融入策略哲学并下沉至API/脚本层强制检查：道可道非常道（市场不可预测→熔断优先）/天之道利而不害（顺势不逆势→战争Level4零开仓即顺势）/为学日益为道日损（减频提质→日均45.9→0笔）/知止不殆（熔断即止→七重熔断API强制）/知足不辱（阶梯止盈→≥1.5盈亏比API校验）/致虚极守静笃（空仓是策略→60天冷却API强制）/反者道之动（暴跌即反转前兆但需D1/D3/D5确认→五条件API校验）/大巧若拙（简单规则胜复杂模型→熔断规则从Markdown下沉至API层）"
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
      "bollinger_extreme_pause": "价格超布林带上轨 22% 时触发暂停，不参与任何方向交易（v4.12.4收紧：从30%降至22%，LAB超46%验证30%过宽）"
    },
    "multi_factor_score": {
      "factors": {
        "ema_trend": "EMA20 > EMA50（做多）/ EMA20 < EMA50（做空）",
        "rsi_filter": "RSI(14) 30-72 之间（ETF催化标的），山寨币收紧至 30-72（v4.12.4收紧：LAB极端超买显示75仍太激进）",
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
      "version": "v4.6新增 → v4.9.2新增tier_25",
      "tier_30": "恐惧指数<30 → 半仓+杠杆1x",
      "tier_25": "恐惧指数<25 → 仓位上限50%+杠杆0.5x（v4.9.2新增）",
      "tier_20": "恐惧指数<20 → 暂停新开仓",
      "tier_10": "恐惧指数<10 → 仅允许持有BTC（本轮触发：恐惧=9）",
      "tier_5_candidate": "候选恐惧指数<5 → 全账户仅持有现金/USDT，连BTC也不持有（v4.10.2候选）",
      "current_value": 46,
      "current_tier": "tier_30（恐惧46，中性偏恐惧。46>30暂不触发tier_30半仓。但七重熔断叠加完全封锁开销。）",
      "description": "恐惧指数分层保护：23→tier_25（极度恐惧区间，23<25触发tier_25仓位上限50%+杠杆0.5x。v4.12.5更新：恐惧31→23断崖下跌-8pts，D1假阳性脱敏模式再次验证。）"
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
      "atr_multiplier_altcoin": 2.2,
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
      "description": "价格超布林带上轨/下轨 22% 时触发趋势暂停（v4.12.4收紧：从30%降至22%）",
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
    },
    "war_escalation_warning_level": {
      "status": "enabled",
      "version": "v4.9.2新增",
      "current_level": 2,
      "levels": {
        "0": {
          "name": "停火",
          "action": "正常交易"
        },
        "1": {
          "name": "局部冲突",
          "action": "全账户暂停新开仓"
        },
        "2": {
          "name": "全面战争预警",
          "action": "仓位0%预警，距全账户清仓仅一步",
          "trigger": "伊朗威胁/计划封锁霍尔木兹海峡"
        },
        "3": {
          "name": "全面战争",
          "action": "全账户清仓+恢复期重置Day0",
          "trigger": "伊朗实际封锁霍尔木兹海峡"
        }
      },
      "description": "战争升级预警等级（v4.9.2正式化）：当前Level 2——伊朗于22:31宣布暂停与美谈判+全面封锁霍尔木兹海峡+曼德海峡。一旦伊朗实际封锁海峡，直接升级至Level 3全账户清仓。"
    },
    "oil_crypto_correlation": {
      "status": "enabled",
      "version": "v4.9.2新增",
      "monitored_assets": [
        "WTI原油",
        "布伦特原油"
      ],
      "trigger_5pct": "原油单日涨跌幅>5% → 全局风控收紧（仓位上限×0.5）",
      "trigger_10pct": "原油单日涨跌幅>10% → 暂停所有新开仓+仅允许减仓",
      "current_values": {
        "wti": 94.2,
        "wti_change_pct": 7.8,
        "brent": 97.23,
        "brent_change_pct": 6.7
      },
      "current_status": "双轨触发——WTI+7.8%/Brent+6.7%均>5%，全局仓位上限已×0.5",
      "description": "原油-加密联动监控（v4.9.2新增）：伊朗封锁霍尔木兹海峡→原油飙涨→全球风险资产承压。WTI/Brent双轨实时监控，原油极端波动是加密市场的领先风险指标。"
    },
    "fear_index_tier_25": {
      "status": "enabled",
      "version": "v4.9.2新增",
      "trigger": "恐惧指数<25 → 仓位上限50%+杠杆0.5x",
      "current_value": 23,
      "current_status": "已触发——23<25，仓位上限50%+杠杆0.5x强制约束",
      "description": "恐惧指数tier_25中间层（v4.9.2新增）：填补<20（暂停新开仓）与<30（半仓+杠杆1x）之间的风控缺口。当前恐惧23已触发，半仓从默认50%进一步压缩至25%。"
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
    "current_signal": "C级 — 七重熔断全激活7.0/7.0：战争🔴Level4(昨晚仍有交火)+波动率🔴(日振幅42%)+贪婪🔴(7日+234%)+布林带🔴(远超22%)+爆仓恢复🔴(Day5/60)+ETF流出🟡(12日累计$38.7亿后本周转流入$11.5亿)+D2溢价🔴(5x)。战争出现降级曙光（黎以停火+S18）但昨晚仍有交火，严禁任何方向开仓。",
    "current_signal_detail": "EMA趋势⚠️(价格极端高位无参考) / RSI⚠️(60-75回落但仍偏高) / MACD❌(日线顶背离) / 布林带❌(远超22%) / 成交量❌(缩量反弹量价背离) | 战争Level4🔴(昨晚仍有交火) + 爆仓恢复Day5/60🔴 + D2溢价5x🔴 + 波动率🔴 + 贪婪🔴 + ETF🟡(本周转净流入观察) + 恐惧46=tier_30 | 多因子0/5=C级",
    "recommended_entry_zone": "$7.50 - $10.00（条件：战争降级至Level≤2 + 72h无攻击 + 8个4H周期企稳 + 合约溢价<1.5x + ETF连续5日净流入 + 恐惧≥35稳定7日 + 恢复期Day30+）",
    "entry_trigger": "①战争降级至Level1+72h无攻击；②LAB价格在$3.50-$4.80区间企稳至少8个4H周期+成交量缩量确认；③爆仓恢复期Day8+（仓位可放宽至5%）；④ETF流出出现逆转（单日净流入>=$5亿）；⑤恐惧贪婪指数回升至35+。全满足=A级，缺1=B级，缺2=C级",
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
    "fear_greed_override": "tier_25规则：恐惧23<25→仓位上限50%+杠杆0.5x（v4.9.2新增中间层）。ETF流出熔断预警（连续10日净流出$29.7亿）",
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
      "version": "4.12.11",
      "date": "2026-06-05",
      "timestamp": "2026-06-05 08:44:25",
      "changes": [
        "第七认知根节点「谈判信号反复依赖症」从候选正式确认（源自交易心理画像v3.4候选→v3.5正式）",
        "新增S22(LAB溢价回归检测): 合约溢价从>3.0x恢复至<2.0x → D2从🔴→🟡，P0优先级",
        "新增S23(战争降级72h延迟确认): S18任一下降级信号触发后需72h无新攻击方可正式降级，P1优先级",
        "新增S24(恐惧回升谈判过滤): 恐惧回升若伴有特朗普口头信号，需额外7日确认，P1优先级",
        "交易心理画像根节点#7正式化后新增行为约束：单一口头信号不作为交易决策依据",
        "LAB/USDT分析报告v5.6生成：全方向禁止交易，信号C级0/5因子，七重熔断7.0/7.0",
        "回测验证待办新增：溢价收敛模型回测/战争降级72h价格行为/恐惧假阳性量化"
      ],
      "trigger": "全域缺口专项补·量化策略叠化 定时任务",
      "report": "LAB_USDT永续合约交易分析报告_20260605.md"
    },
    {
      "version": "4.12.9",
      "date": "2026-06-05 06:00:00",
      "report": "LAB_USDT永续合约交易分析报告_20260605.md",
      "changes": [
        "v4.12.8→v4.12.9 全域缺口专项补·量化策略叠化",
        "【P0】战争态势关键转折监控→激活：黎以停火（6/4首个实质性积极信号）+特朗普愿会面+40艘商船通行海峡。战争Level4维持但新增降级曙光监控S18。",
        "【P1】ETF反转检测S19→激活：12日累计流出$38.7亿后本周6/3-4转入净流入$11.5亿。需连续5日净流入方可作为解除条件之一。",
        "【P1】恐惧回升验证S20→激活：恐惧11→46（+35pts），D1稳定性检测：46>25但仅1日，需持续7日方可降级。新增谈判反复依赖症预警。",
        "【数据】BTC $81,306（较$62K回升31%），恐惧46（中性偏恐惧），VIX 18.29，10Y 4.45%。",
        "【数据】LAB $14.94-$16.83，7日+234%，30日+821%，合约溢价约5x。D2溢价熔断超强触发维持。",
        "【数据】6/4晚波斯湾再次交火：美军打LEXIE油轮→伊朗打帕纳亚号→美军炸格什姆岛→伊朗击落无人机。停火脆弱。",
        "【闭环】全账户零开仓。七重熔断7.0/7.0。60天冷却维持。解除条件0/5→新增黎以停火+谈判开启二项积极但未满足解除。",
        "【新增】S18战争降级曙光监控、S19 ETF反转检测、S20恐惧回升验证、S21谈判反复依赖症预警（第七认知根节点候选）"
      ],
      "triggers": [
        "全域缺口专项补·量化策略叠化任务",
        "黎以停火+特朗普愿会面+40艘商船通行海峡→战争降级曙光但昨晚仍有交火",
        "BTC从$62K回升至$81,306(+31%)，恐惧11→46，ETF转净流入",
        "LAB继续极端超买：7日+234%，合约溢价5x",
        "BTC ETF 12日累计流出$38.7亿后首次周度转正",
        "交易心理画像v3.3→v3.4：新增第七认知根节点候选"
      ],
      "verified": false
    },
    {
      "version": "4.12.7",
      "date": "2026-06-03 21:54:00",
      "report": "币安龙头黑马预测报告_20260603_2154.md",
      "changes": [
        "v4.12.6→v4.12.7 定时预测闭环·币安龙头黑马全量扫描",
        "【P0】S12恐惧tier_10强化→激活：恐惧11(昨日23→今日11/-12pts)，距COVID崩盘极值8仅3pts。tier_10规则（仅允许持有BTC）强化执行。C19 tier_5候选逼近监控。",
        "【P0】S13波动率熔断升级→激活：BTC 30d vol 56.88%→60%+，波动率熔断权重0.5→1.0，与ETF/战争/爆仓平级。全市场暴跌6%+加剧波动。",
        "【P0】S14战争Level4+第三国卷入→激活：伊朗首次打击科威特民用机场(1死多伤)，科威特关闭领空。战争从'美伊双方面'升级为'多国卷入'，外溢风险实质化。",
        "【P1】S15 D1恐惧稳定性7日规则→第5次验证：恐惧29→9→29→10→31→23→11，六次剧烈震荡持续证伪'短期回升即平静'假设。",
        "【P1】S16 S10 CAKE-BNB脱钩规则→验证：CAKE从+4.17%逆势(v4.12.6)→-5.25%跟随BNB暴跌(本轮)，S10准确预警假性独立行情不可持续。",
        "【P0】S17 C19 tier_5候选逼近→监控中：恐惧11距tier_5阈值5仅差6pts。若跌破5，触发全账户仅持现金/USDT。",
        "【数据】BTC ~$66,000-$67,000(-6%+)，跌破$67K，4月5日以来最低，距历史高点$12.6万累计回调近50%。",
        "【数据】ETH跌破$1,900(-5%+)，SOL -9%+，BNB -6%+，狗狗币 -8%+。全市场无差别屠杀。",
        "【数据】24h全网爆仓$16.13亿/25万+人，2月以来最高。",
        "【数据】恐惧指数11（极度恐慌），昨日23(-12pts)。16个月持续恐惧区间(480+天)。",
        "【数据】ETF连续11日净流出$35亿创历史最长记录。Strategy首次减持BTC。Coinbase -5%，MSTR -9%+。",
        "【数据】WTI原油$93.76(+5.49%)，Brent ~$96，原油联动双轨触发维持。",
        "【数据】美伊6/2-6/3激烈互袭：美军打伊朗油轮→伊朗打美以船只→美军炸格什姆岛→伊朗导弹无人机打第五舰队总部+科威特/巴林基地。科威特机场遭袭1死多伤，关闭领空。",
        "【闭环】全账户零开仓。七重熔断7.0/7.0（恐惧tier_10+波动率升级）。60天冷却。解除条件0/4。交易心理画像v3.2核心诊断100%验证。"
      ],
      "triggers": [
        "定时任务：AI分身×量化策略·币安龙头黑马预测闭环（每2小时）",
        "全市场崩盘：BTC -6%+/ETH -5%+/BNB -6%+/SOL -9%+，$16.13亿爆仓/25万+人",
        "恐惧指数23→11断崖(-12pts)：D1假阳性脱敏第5次验证",
        "美伊骤然升级：6/2-6/3激烈互袭，伊朗首次打击第三国(科威特)民用机场",
        "ETF连续11日流出$35亿+Strategy首次减持+Coinbase -5%：三重机构撤退",
        "S10 CAKE-BNB脱钩规则验证：CAKE从逆势+4.17%→跟随暴跌-5.25%",
        "C19 tier_5候选逼近：恐惧11距全账户现金化阈值仅6pts"
      ],
      "verified": true
    },
    {
      "version": "4.12.6",
      "date": "2026-06-03 08:00:00",
      "report": "币安龙头黑马预测报告_20260603_0800.md",
      "changes": [
        "v4.12.5→v4.12.6 定时预测闭环·币安龙头黑马全量扫描",
        "【P0】S07 ETF流出权重升级→激活：etf_outflow_weight 0.35→0.40。ETF连续11日流出$35亿+IBIT机构撤退确认，ETF流出已从'需求减弱'升级为'需求负贡献'。",
        "【P0】S08机构撤退综合预警→激活：新增institution_retreat_warning。ETF流出+MSTR减持+Coinbase跌5%三信号叠加，机构需求端系统性熄火。",
        "【P0】S09战争Level4主动军事打击升级→激活：美军6/2打击伊朗方向油轮'Lexie'号，从'封锁'升级为'主动军事打击商船'。",
        "【P1】S10 CAKE-BNB脱钩强化→激活：CAKE+4.17% vs BNB-4.87%二次验证脱钩信号不可持续，自动降级规则强化。",
        "【P1】S11 D1恐惧长期低位钝化监控→激活：恐惧指数16个月持续恐惧区间史无前例，新增区分'理性恐惧'与'非理性恐慌'机制。",
        "【数据】BTC ~$66,500(-6%+)，跌破$67K，4月5日以来最低，距历史高点$12.6万累计回调近50%。",
        "【数据】全网24h爆仓$16.13亿/25万+人，2月以来最高。ETF连续11日流出$35亿创历史最长记录。",
        "【数据】Strategy首次减持32 BTC（$250万），打破'只买不卖'承诺。MSTR股票跌超9%。",
        "【数据】WTI $93.76(+5.49%)，Brent $96.00(+4.24%)，原油联动双轨触发。",
        "【数据】恐惧指数~10-15极度恐惧，16个月持续恐惧区间。BNB $659(-4.87%)，CAKE $1.58(+4.17%逆势)。",
        "【数据】美军6/2打击伊朗方向油轮+伊朗南部6/3凌晨爆炸声，战争Level4维持。",
        "【闭环】全账户零开仓。七重熔断7.0/7.0。冷却期60天。解除条件四要素0/4。"
      ],
      "triggers": [
        "定时任务：AI分身×量化策略·币安龙头黑马预测闭环（每2小时）",
        "BTC跌破$67K，Strategy首次减持BTC+ETF连续11日流出形成'三重机构撤退'",
        "美军首次实际攻击伊朗方向商船+伊朗南部爆炸声→战争烈度升级",
        "CAKE+4.17% vs BNB-4.87%脱钩二次确认→v4.7 C05规则触发",
        "恐惧指数16个月持续低位→D1稳定性检测领域新问题：长期钝化vs恐慌",
        "恐惧指数29→31→10-15持续走弱→D1假阳性脱敏模式第4次验证"
      ],
      "verified": false
    },
    {
      "version": "4.9",
      "date": "2026-06-01T23:00:00+08:00",
      "report": "LAB_USDT永续合约交易分析报告_20260601_叠化v4.9.md",
      "changes": [
        "v4.8→v4.9 全域缺口专项补·量化策略叠化",
        "【验证】战争黑天鹅熔断保护价值：LAB $12.03→$4.29(-64.35%)，若v4.7未熔断追高则浮亏惨重",
        "【新增】暴跌后反转识别模块：极端超买暴跌>60%后，需连续6个4H周期企稳+MACD底背离+RSI<30后金叉",
        "【升级】战争分级响应v2：局部冲突→全账户暂停（当前）；全面战争(伊朗封锁霍尔木兹)→全账户清仓+恢复期重置Day0",
        "【新增】爆仓恢复暴跌情境豁免：空仓期间标的暴跌>50%，Day8+可放宽仓位至5%（替代原需战争解除+ETF转流入+恐惧>40三条件）",
        "【新增】黑天鹅避险价值追踪：记录每次战争熔断避免的潜在损失",
        "【解除】LAB布林带外溢熔断（价格从超46%回落至正常区间）",
        "【解除】LAB贪婪熔断（价格暴跌后5日涨幅转负）",
        "【解除】LAB RSI超买（从>90回落）",
        "【仍激活】战争黑天鹅熔断（美伊冲突升级+伊朗威胁封锁霍尔木兹海峡）",
        "【仍激活】ETF流出熔断（连续3周流出>$30亿）",
        "【仍激活】爆仓恢复期（Day2/14，仓位2%/杠杆0.5x）",
        "【仍激活】波动率熔断（暴跌后振幅待确认）",
        "交易心理画像 v2.0→v2.3：三重认知根节点(止损缺失/虚假安全感/战争脱敏)锁定",
        "",
        "——— v4.9→v4.9.2 叠化 ———",
        "【P0】C09战争分级响应v2正式化（candidate→formalized）",
        "【P0】C08暴跌反转条件强化：6→8个4H周期确认+新增成交量缩量企稳确认",
        "【P0】新增加war_escalation_warning_level（0/1/2/3四级）直接反射伊朗局势",
        "【P0】新增原油-加密联动监控oil_crypto_correlation（WTI+Brent双轨）",
        "【P0】新增恐惧指数tier_25中间层（<25仓位上限50%+杠杆0.5x）",
        "【触发】伊朗22:31封锁海峡→war_escalation_warning_level=2→全账户仓位0%",
        "【触发】WTI+7.8%/Brent+6.7%→oil_crypto_correlation双轨触发→仓位上限×0.5",
        "【触发】恐惧指数29→23→tier_25触发→仓位上限50%+杠杆0.5x",
        "全账户零开仓：四重熔断叠加（战争🔴+ETF流出🔴+爆仓恢复🔴+波动率🟡）"
      ],
      "triggers": [
        "全域缺口专项补·量化策略叠化任务",
        "LAB $12.03→$4.29暴跌(-64.35%)验证v4.7战争熔断保护价值",
        "美伊冲突升级：伊朗威胁封锁霍尔木兹海峡，原油飙涨7%",
        "BTC $73K→$72K，全网24h爆仓>$2.47亿(超14万人)",
        "ETF连续3周流出>$30亿，本周$14亿(2026年第二大周流出)",
        "恐惧贪婪指数29（恐惧），战争脱敏警示持续",
        "LAB七重熔断→四重激活（布林带/RSI/贪婪已解除）"
      ],
      "verified": false
    },
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
    },
    {
      "version": "4.12.0",
      "date": "2026-06-02 09:07:39",
      "changes": [
        "【P0】D1恐惧稳定性检测 → 激活：恐惧需稳定25+持续5日方可降级，防止9→29假性回升",
        "【P0】D2合约现货溢价熔断 → 激活：永续溢价>30%禁止该品种做多",
        "【P1】D3无量反弹量价背离 → 激活：暴跌>60%后反弹>30%+量<50%→信号自动降级",
        "【P1】D4 MSTR减持权重升级 → 激活：全账户仓位系数0.5→0.15，新增90天禁开仓规则",
        "【P1】D5霍尔木兹通行量监控 → 激活：新增曼德海峡次级监控(D5.1)，战争Level 3→4",
        "【数据】BTC $71500(-2.88%), BNB $635(-5.60%), BNB/BTC=0.00888(<0.010 D级排除)",
        "【数据】ETF连续9日净流出~$28B, MSTR 2022年以来首次减持32 BTC",
        "【数据】伊朗暂停谈判+双海峡威胁+实际攻击美以船只→战争Level4",
        "【数据】恐惧指数10(tier_10), WTI +6.16%, 24h爆仓$5.23B/14.5万人",
        "【产出】币安龙头黑马预测报告_20260602_0907，零标的通过，七重熔断全量激活",
        "【闭环】交易心理画像v2.7→v2.8：战争脱敏假阳性验证，创伤期IV确认，Day 0重置"
      ],
      "triggers": [
        "定时任务：AI分身×量化策略·币安龙头黑马预测闭环（每2小时）",
        "战争升级：伊朗暂停谈判+双海峡威胁+革命卫队攻击美以船只",
        "MSTR首次减持：打破'永不卖出'承诺",
        "ETF连续9日流出创最长记录",
        "恐惧指数从29断崖回落至10，验证战争脱敏假阳性",
        "v5.1 LAB分析报告五项发现全部触发确认"
      ],
      "verified": false
    },
    {
      "version": "4.12.3",
      "date": "2026-06-02 15:22:00",
      "changes": [
        "【P12】恐惧29→23二次走弱确认D1假阳性脱敏模式稳定。恐惧需稳定≥25持续5日方可降级，当前23不满足→D1检测维持。",
        "【P13】LAB合约溢价再恶化确认：1.396x→5.41x（$17.36/$3.21），D2溢价熔断从弱触发升级为超强触发。庄家控盘明确，禁止做多方向维持。",
        "【C18候选】交易日志目录为空（E:\\龙虾AI主控中心\\我的AI分身\\量化策略资产\\交易日志\\），建议建立API自动归档机制补齐数据缺口。",
        "【确认】七重熔断6.0/7.0维持，全账户零开仓维持，60天冷却期维持。解除条件四要素0/4全部未满足。",
        "【确认】BNB/BTC=0.00888 D级自动排除。CAKE C级+熔断禁止。LAB D2溢价熔断超强触发。HYPE非BNB生态仅观察。",
        "【确认】特朗普口头信号不构成降级依据（v2.7已证伪一次口头信号）。战争Level 4维持。",
        "【产出】币安龙头黑马预测报告_20260602_1522，零标的通过",
        "【闭环】策略v4.12.2→v4.12.3 参数确认迭代，无新增正式参数，C18候选建议归档机制"
      ],
      "triggers": [
        "定时任务：AI分身×量化策略·币安龙头黑马预测闭环（每2小时）",
        "恐惧指数29→23二次走弱，D1假阳性脱敏模式持续验证",
        "LAB合约溢价5.41x极端恶化，D2超强触发",
        "交易日志目录为空发现：数据完整性缺口需补齐",
        "BTC逼近$70,000心理关口，市场承压持续",
        "地缘冲突无降温信号：伊朗实际攻击美以船只"
      ],
      "verified": false
    },
    {
      "version": "4.12.2",
      "date": "2026-06-02 14:00:00",
      "changes": [
        "【P0】P10 ETF流出权重升级 → 激活：etf_outflow_weight 0.25→0.35（11天/$4.84亿新高，IBIT $4.40亿/91%）",
        "【P0】P11 恐惧tier_25再触发协议 → 激活：恐惧23<25，D1稳定性检测验证29→23假阳性",
        "【确认】P03.1 ETF双日确认加罚触发：6/1流出$4.84亿>$5亿→追加3天冷却",
        "【确认】D2 LAB合约溢价再触发：$17.36/$3.21=5.41x（v4.12.0时1.396x已触发，现在极端恶化）",
        "【验证】D1恐惧稳定性检测：恐惧29→23的48h内二次暴跌，假阳性脱敏模式确认",
        "【数据】BTC ~$70,851(-3.58%), BNB ~$770(-2.37%), CAKE $1.87(-3.34%), TWT $0.87(-2.93%)",
        "【数据】LAB $17.36(+92.73%), 合约溢价5.41x, 末日战车行情",
        "【数据】恐惧指数23重回极度恐慌, ETF流出11天累计~$33B+",
        "【数据】特朗普声称一周内重启谈判 → 不降级（v2.7已证伪一次口头信号）",
        "【数据】HYPE $74.40-$75+ 创历史新高，本轮唯一逆势标的（非BNB生态+熔断禁止）",
        "【产出】币安龙头黑马预测报告_20260602_1400，零标的通过",
        "【闭环】全账户零开仓，七重熔断权重6.0/7.0，60天冷却期维持"
      ],
      "triggers": [
        "定时任务：AI分身×量化策略·币安龙头黑马预测闭环（每2小时）",
        "ETF流出加速：11天/$4.84亿新高，IBIT单日$4.40亿占91%",
        "恐惧指数29→23二次暴跌：D1假阳性脱敏模式确认",
        "LAB +92.73%至$17.36：合约溢价5.41x，D2再触发",
        "特朗普口头信号：声称一周内重启谈判（v2.7已证伪，不降级）",
        "MSTR减持2日追踪：等待6/2是否继续减持"
      ],
      "verified": false
    },
    {
      "version": "4.12.5",
      "date": "2026-06-02 17:30:00",
      "changes": [
        "【P0】S01 D2溢价升级全品种警告→激活：溢价>3.0x禁止全BSC生态+全品种新开仓",
        "【P0】S02熔断API层强制执行→激活：七重熔断任一触发→API硬编码拒绝开仓",
        "【P1】S03 D1稳定性检测5日→7日延长：恐惧31→23二次走弱验证假阳性",
        "【P1】S04每日纪律清单API自动化→候选：自动七重熔断状态+机会成本日记+交易日志归档",
        "【P1】S05道家心法API校验→激活：八条心法逐条API层强制检查",
        "【P1】S06多交易所溢价异常监控→激活：LAB全交易所合约溢价>2.0x自动触发D2",
        "【数据】恐惧23-31五段震荡D1假阳性确认，D1稳定7日延长",
        "【数据】LAB合约溢价5.41x→D2升级全品种警告",
        "【数据】七重熔断全量激活7.0/7.0，全账户零开仓，60天冷却",
        "【产出】LAB_USDT分析报告v5.4（趋势C级/关键价位/仓位风控/道家心法/专属信号）",
        "【闭环】策略v4.12.4→v4.12.5（S01-S06六项参数新增），交易心理画像v3.0已验证"
      ],
      "triggers": [
        "嗡阿喇巴札那谛，龙虾五步法启动·全域缺口专项补·量化策略叠化",
        "恐惧指数31→23二次走弱D1假阳性持续验证",
        "LAB合约溢价5.41x超强触发D2→升级全品种警告",
        "v3.0第六认知根节点「熔断后违规交易」→策略API强制执行需求",
        "道家心法八条从文档哲学下沉至API/脚本层",
        "交易心理画像v3.0核心诊断100%验证，无结构变化"
      ]
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
    "etf_outflow_weight_in_circuit_breaker": 0.4,
    "etf_outflow_weight_desc": "v4.12.6升级：ETF连续11天流出$35亿创历史最长记录+IBIT机构撤退确认+Strategy首次减持。ETF流出已从'需求减弱'升级为'需求负贡献'，权重0.35→0.40。",
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
    "post_liquidation_recovery_no_reverse_trade": true,
    "post_liquidation_recovery_no_reverse_trade_desc": "v4.10.1新增：爆仓恢复期内禁止开反向单（做空），防止情绪化追空抄底。对齐交易心理画像'止损缺失'根节点。",
    "anti_dip_buying_ban_trigger_24h_drop_pct": 0.15,
    "anti_dip_buying_ban_trigger_sentiment": 25,
    "anti_dip_buying_ban_cooling_hours": 72,
    "mstr_divestiture_warning": true,
    "mstr_divestiture_desc": "v4.10.2新增：Strategy Inc.(MSTR)首次自2022年减持32 BTC(~$2.5M, avg $77,135/BTC)。CEO Phong Le公开表示'可能卖出部分持仓'，打破'永不卖出'承诺。触发全账户仓位上限额外×0.5系数（叠加现有熔断）。信号意义远超量级——机构'永不卖出'信仰崩塌是2020年减半以来最严重的情绪转折。",
    "panic_peak_intervention_protocol": "恐惧9级恐慌极值干预协议(v4.10.2正式化)：①禁止一切'抄底'思维——恐惧9(2020/3 COVID以来最低)是反向诱惑最高时，也是受损最大时。②禁止任何非BTC开仓思考——tier_10规则下仅BTC允许。③每周至少2次重读交易心理画像§四(爆仓创伤根节点)。④如恐惧跌破5触发C17候选tier_5：全账户仅持现金/USDT。",
    "bnb_btc_ratio_actual": 0.0088,
    "bnb_btc_ratio_action": "v4.10.2：0.0088已跌破v4.9 C04阈值0.009→全BNB生态D级自动排除。BNB -9.15%/24h远超BTC -2.88%，资金从BNB生态加速外逃。",
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
    "lab_profit_ratio_asymmetric_short": 2.0,
    "crash_reversal_detection_enabled": true,
    "crash_reversal_confirmation_cycles": 8,
    "crash_reversal_min_drop_pct": 0.6,
    "war_escalation_full_liquidation_trigger": "iran_blockade_hormuz",
    "crash_avoidance_bonus_days": 0,
    "black_swan_protection_value_tracking_enabled": true,
    "war_escalation_warning_level": 3.5,
    "war_escalation_warning_level_desc": "0=停火/1=局部冲突/2=全面战争预警(仓位0%)/3=全面战争(全账户清仓+重置Day0)/3.5=全面战争+关键海峡封锁(等效Level3+)。当前3.5——伊朗6/1暂停谈判+计划彻底封锁霍尔木兹海峡+启动曼德海峡战线+科威特全国防空警报+美伊互相军事打击+美军引导不足日均3艘商船通行(vs战前日均100+)。v4.11.0 P02专属：霍尔木兹信号权重额外追加7天冷却。",
    "war_desensitization_detector": {
      "status": "enabled",
      "version": "v4.11.0-P01",
      "description": "战争脱敏检测器：防止交易者习惯战争环境后冲动开仓。当恐惧指数连续3日<15时触发，追加7天冷却期。源自交易心理画像v2.7第五认知根节点'战争脱敏'。",
      "trigger": "fear_greed_index < 15 for >= 3 consecutive days",
      "action": "追加7天冷却期，覆盖恢复期结束时间",
      "rationale": "恐惧9持续3日=交易者可能开始'习惯'恐慌→脱敏→冲动开仓→爆仓"
    },
    "hormuz_signal_weight": {
      "status": "enabled",
      "version": "v4.11.0-P02",
      "description": "霍尔木兹海峡信号权重增强。全球油路封锁对风险资产的冲击远超普通战争Level3，实际等效Level3.5。",
      "extra_cooldown_days": 7,
      "trigger": "hormuz_blockade_active",
      "current": true,
      "daily_commercial_traffic": "日均3艘(vs战前100+)",
      "action": "war_level有效值+0.5，冷却期叠加7天"
    },
    "etf_outflow_acceleration_penalty": {
      "status": "enabled",
      "version": "v4.11.0-P03",
      "description": "ETF流出加速惩罚。单日流出>$5亿→追加3天冷静期。机构行为领先散户3-5天，加速流出=加速撤离。",
      "trigger": "BTC_ETF_daily_outflow > $500M",
      "action": "追加3天冷静期",
      "current_day_outflow": "$544.94M（已触发）",
      "cumulative_10day_outflow": "约$30B+"
    },
    "extreme_drawdown_secondary_protection": {
      "status": "enabled",
      "version": "v4.11.0-P04",
      "description": "极端回撤二次保护。恢复期结束后首次开仓若亏损>2%，自动回退7天模拟交易期。防止'急着回本'心态。",
      "trigger": "first_position_after_recovery_profit < -2%",
      "action": "回退7天模拟交易期，重新评估策略有效性"
    },
    "opportunity_cost_journal": {
      "status": "enabled",
      "version": "v4.11.0-P05",
      "description": "机会成本日记。每日强制记录'如果今天我开了仓会怎样'，用于元认知训练，防止'踏空焦虑'导致冲动开仓。",
      "frequency": "daily",
      "format": "假设开仓方向/入场价/当前价/盈亏评估",
      "purpose": "事后验证'踏空焦虑'的合理性，积累元认知数据"
    },
    "fear_index_tier_25_enabled": true,
    "fear_index_tier_25_desc": "<25→仓位上限50%+杠杆0.5x。填补<20暂停新开仓与<30半仓之间的缺口。当前9已触发tier_10(仅BTC)，tier_25/tier_20/tier_10三重叠加。",
    "fear_index_tier_10_enabled": true,
    "fear_index_tier_10_desc": "v4.10.2：恐惧9(29→9断崖式恶化-25pts)触发tier_10——仅允许持有BTC，禁止一切非BTC新开仓。逼近2020/3 COVID崩盘(8)水平。候选tier_5：恐惧<5→全账户仅持现金。",
    "oil_crypto_correlation_enabled": true,
    "oil_crypto_correlation_desc": "WTI+Brent双轨监控。原油单日>5%→全局风控收紧(仓位上限×0.5)。当前WTI+6.16%/Brent+5.8%已触发",
    "P10_etf_outflow_weight_upgrade": {
      "status": "activated",
      "version": "v4.12.2",
      "previous_weight": 0.25,
      "new_weight": 0.35,
      "trigger": "ETF单日$4.84亿(IBIT $4.40亿/91%)创新高+连续11天累计~$33B+",
      "ibitt_concentration_alert": "IBIT占91%→大型机构赎回非散户恐慌"
    },
    "P11_fear_tier_25_retrigger": {
      "status": "activated",
      "version": "v4.12.2",
      "current_fear": 23,
      "trajectory": "10→29→10→29→23（五段式震荡）",
      "action": "tier_25约束维持，D1要求5日稳定方可降级",
      "desensitization_confirmed": true,
      "false_positive_pattern": "恐惧29不是真正平静，而是特朗普口头信号造成的短时情绪透支"
    },
    "P03.1_etf_daily_double_confirm": {
      "status": "triggered",
      "version": "v4.12.2",
      "trigger_data": "6/1流出$4.84亿>$5亿阈值",
      "action": "追加3天冷却",
      "pending": "等待6/2数据确认是否追加第二轮"
    },
    "D2_lab_contract_premium": {
      "status": "re-confirmed",
      "current_ratio": 5.41,
      "threshold": 1.3,
      "lab_contract": 17.36,
      "lab_spot": 3.21,
      "note": "v4.12.5升级：合约溢价5.41x超强触发→D2溢价熔断从'禁止做多'升级为'全BSC生态品种警告+全品种新开仓禁止'。庄家对倒拉盘明确，末日战车信号确认。"
    },
    "P12_fear_d1_stability_confirm": {
      "status": "confirmed",
      "version": "v4.12.3",
      "current_fear": 23,
      "trajectory": "10→29→10→29→23（五段震荡→二次走弱）",
      "stable_above_25_days": 0,
      "required_days": 7,
      "conclusion": "D1假阳性脱敏模式确认。恐惧<25不满足降级条件。",
      "note": "v4.12.5升级：恐惧需稳定≥25持续7日方可降级（原5日）。恐惧31→23二次走弱验证假阳性脱敏模式，5日仍不足确保稳定性。"
    },
    "P13_lab_d2_premium_severe": {
      "status": "confirmed",
      "version": "v4.12.3",
      "previous_ratio": 1.396,
      "current_ratio": 5.41,
      "contract_price": 17.36,
      "spot_price": 3.21,
      "severity": "超强触发（从1.396x弱触发升级为5.41x超强触发）",
      "note": "LAB合约溢价从D2初触发1.396x恶化至5.41x，庄家对倒拉盘明确可见。末日战车信号进一步确认。D2溢价熔断从'禁止做多'可升级为'全品种警告'。"
    },
    "C18_transaction_log_archive": {
      "status": "candidate",
      "priority": "P1",
      "issue": "交易日志目录为空，12,885笔历史订单未在本地归档",
      "path": "E:\\龙虾AI主控中心\\我的AI分身\\量化策略资产\\交易日志\\",
      "suggestion": "建立币安API自动归档机制，将实时订单历史同步至本地交易日志目录。当前依赖内存/报告库中的数据间接还原，存在数据丢失风险。"
    },
    "S07_etf_outflow_weight_upgrade_v4.12.6": {
      "status": "activated",
      "version": "v4.12.6",
      "previous_weight": 0.35,
      "new_weight": 0.4,
      "trigger": "ETF连续11日流出$35亿创历史最长记录+IBIT单日$4.40亿占91%+Strategy首次减持BTC",
      "rationale": "ETF流出已从'需求减弱信号'升级为'需求负贡献因子'。连续11日净流出打破所有历史记录，IBIT机构赎回占91%表明非散户恐慌而是机构系统性撤退。叠加MSTR首次减持——最坚定的'永不卖出'多头也在撤退——三重机构撤退形成需求端系统性熄火。",
      "action": "etf_outflow_weight从0.35升级至0.40，ETF流出在熔断权重中占比升至40%"
    },
    "S08_institution_retreat_warning": {
      "status": "activated",
      "version": "v4.12.6",
      "priority": "P0",
      "description": "机构撤退综合预警。ETF流出+MSTR减持+Coinbase跌5%三信号叠加，机构需求端系统性熄火。当三信号同时触发时，全账户仓位上限额外×0.5系数（叠加现有熔断）。",
      "trigger_signals": {
        "signal_1": "ETF连续≥10日净流出（当前11日/$35亿）",
        "signal_2": "Strategy/MSTR减持BTC（当前：首次减持32 BTC）",
        "signal_3": "Coinbase股价单周跌幅>10%（当前：-5%逼近）"
      },
      "current_status": "信号1+2已触发（2/3），机构撤退高度预警",
      "action_on_3_of_3": "全账户仓位上限额外×0.5（叠加七重熔断后实际为0%×0.5=0%）"
    },
    "S09_war_level4_active_military_strike": {
      "status": "activated",
      "version": "v4.12.6",
      "priority": "P0",
      "description": "战争Level4主动军事打击升级。美军6月2日在阿拉伯湾对伊朗方向油轮'Lexie'号发射'地狱火'导弹致其丧失航行能力，伊朗南部格什姆岛6月3日凌晨传出爆炸声。从'封锁海峡'升级为'主动军事打击商船'，战争烈度实质性升级。",
      "trigger": "美军对伊朗方向商船发射导弹+伊朗本土爆炸声",
      "action": "战争Level4维持+追加7天冷却期（重叠60天）",
      "latest_events": [
        "6/2：美军对'Lexie'号发射导弹致其丧失航行能力",
        "6/3凌晨：伊朗南部格什姆岛传出爆炸声（性质待确认）",
        "6/2：美国制裁伊朗加密货币交易平台及相关人员",
        "停火协议周三到期，伊朗未决定是否派代表团"
      ]
    },
    "S10_cake_bnb_decoupling_strengthened": {
      "status": "activated",
      "version": "v4.12.6",
      "priority": "P1",
      "description": "CAKE-BNB脱钩监控规则强化。CAKE +4.17% vs BNB -4.87%二次验证v4.7 C05脱钩信号不可持续。生态领头羊弱势时小弟独立上涨是典型的短期资金博弈现象，不可持续。",
      "current_data": {
        "cake_24h": "+4.17%",
        "bnb_24h": "-4.87%",
        "decoupling_triggered": true,
        "decoupling_count": 2
      },
      "strengthened_rule": "CAKE涨>3%且BNB跌>3%同日，且此前7日内BNB跌幅>5%→CAKE信号自动降两级（A→C级），而非原规则的一级",
      "rationale": "二次验证确认脱钩信号为假性独立行情。在七重熔断环境下，即使不考虑熔断，CAKE也不具备独立上涨的基本面支撑。"
    },
    "S11_fear_longterm_stagnation_monitor": {
      "status": "activated",
      "version": "v4.12.6",
      "priority": "P1",
      "description": "D1恐惧长期低位钝化监控。恐惧指数自2025年1月30日以来持续处于恐惧区间（16个月+），创历史最长记录。此前D1稳定性检测仅关注短期波动（假阳性脱敏），但长期钝化是另一类风险——交易者可能将'持续恐惧'等同于'市场已触底'。",
      "current_status": {
        "fear_value": "~10-15（极度恐惧）",
        "days_in_fear_zone": "480+天（2025.1.30至今）",
        "historical_record": "超过2018-2019熊市持续时间",
        "d1_stable_above_25_days": 0
      },
      "monitoring_rules": {
        "rule_1": "恐惧指数连续480+天<50→触发长期钝化黄色预警",
        "rule_2": "长期钝化预警期间，任何基于'恐惧触底'逻辑的开仓必须额外经过5日恐惧确认（非7日D1规则）",
        "rule_3": "区分'理性恐惧'（战争+ETF流出+机构撤退合理定价）与'非理性恐慌'（社交网络恐慌情绪过度放大）"
      },
      "rationale": "16个月恐惧区间可能意味着两种截然相反的情景：①市场长期合理定价地缘+宏观风险（理性恐惧）；②市场过度悲观已接近历史性底部（非理性恐慌）。当前有压倒性证据支持情景①——战争Level4+ETF创纪录流出+Strategy首次减持均为客观基本面恶化——因此维持零开仓。"
    },
    "S18_war_deescalation_monitor": {
      "status": "activated",
      "version": "v4.12.9",
      "priority": "P0",
      "description": "战争降级曙光监控。6/4黎以停火协议达成（被视为伊朗接受和平协议的重要前提），特朗普表示愿与伊朗最高领袖会面，近40艘商船通过霍尔木兹海峡。这三个信号构成战争Level4以来首个实质性积极信号组合。但6/4晚仍有交火，停火极其脆弱。",
      "signals": {
        "signal_1_israel_lebanon_ceasefire": "6/4黎以停火→✅达成",
        "signal_2_trump_meeting_offer": "特朗普愿会面→✅口头信号（v2.7已证伪一次口头信号，需实际行动）",
        "signal_3_hormuz_commercial_traffic": "近40艘商船通行→✅有限恢复（vs战前日均100+）",
        "signal_4_ceasefire_stability": "72h无攻击→❌未满足（6/4晚仍有交火）"
      },
      "action": "战争Level4维持，但新增降级曙光监控。需四信号全满足+72h无攻击方可考虑降级至Level3。当前0/4。",
      "deescalation_conditions_count": "0/4"
    },
    "S19_etf_reversal_detection": {
      "status": "activated",
      "version": "v4.12.9",
      "priority": "P1",
      "description": "ETF反转检测。此前BTC ETF连续12个交易日累计流出$38.7亿创历史最长记录，但本周6月3-4日转入净流入$11.5亿。需连续5日净流入方可作为解除条件之一。",
      "current_status": "6/3-4净流入$11.5亿（2/5日），但6/2仍流出$5.19亿。反转信号初步但未确认。",
      "trigger": "BTC ETF连续5日净流入",
      "action": "ETF流出熔断从🔴→🟡观察"
    },
    "S20_fear_recovery_verification": {
      "status": "activated",
      "version": "v4.12.9",
      "priority": "P1",
      "description": "恐惧指数回升验证。恐惧从11极度恐慌→46中性偏恐惧（+35pts），是战争以来最大回升。按D1稳定性检测规则，46>25但仅1日，需稳定≥25持续7日方可降级。同时新增谈判反复依赖症预警：若恐惧回升主要由特朗普口头谈判信号驱动，则回升可能是假阳性。",
      "current_value": 46,
      "days_above_25": 1,
      "required_days": 7,
      "warning": "若恐惧回升源于特朗普口头信号而非实质性停火，可能再度上演29→10假阳性模式"
    },
    "S21_negotiation_dependency_warning": {
      "status": "activated",
      "version": "v4.12.9",
      "priority": "P1",
      "description": "谈判信号反复依赖症预警（交易心理画像第七认知根节点候选）。特朗普口头信号反复无常是美伊冲突的核心特征：6/1特朗普称一周内达成协议→6/2伊朗指责美方违反停火→6/5特朗普又称愿与最高领袖会面。交易者可能过度依赖口头信号波动做决策，忽视信号反复无常的本质。",
      "evidence": [
        "v2.7特朗普口头信号证伪→恐惧29→9",
        "v4.12.2特朗普声称一周内重启谈判→不降级（正确）",
        "v4.12.9特朗普愿会面→需实际行动验证非口头信号"
      ],
      "action": "谈判信号需配合实际行动验证（72h无攻击+海峡通行恢复+外交渠道确认），单一口头信号不作为降级依据"
    }
  },
  "war_ceasefire_reentry_delay_days": 30,
  "war_ceasefire_reentry_delay_description": "v4.10.1更新：Level3全面战争升级为30天冷却期。停火协议签署+30天无攻击+海峡通航恢复三重条件方可解除战争熔断。",
  "v4.9_candidates": {
    "C04_bnb_btc_relative_strength": {
      "status": "formalized",
      "formalized_in": "v4.10.2",
      "description": "BNB-BTC比率0.0088已跌破v4.9建议阈值0.009→全BNB生态D级自动排除。BNB -9.15%/24h远超BTC -2.88%，资金从BNB生态加速外逃。此指标成功提前预警BNB生态衰退。",
      "suggested_threshold": 0.009,
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
        "day1_7": {
          "max_position_pct": 0.02,
          "max_leverage": 0.5
        },
        "day8_14": {
          "max_position_pct": 0.05,
          "max_leverage": 1.0,
          "requires": [
            "war_ceasefire",
            "etf_inflow_resumed",
            "fear_greed_above_40"
          ]
        }
      }
    },
    "C08_crash_reversal_pattern": {
      "status": "formalized",
      "formalized_in": "v4.9.2",
      "description": "暴跌后反转识别模块（v4.9.2强化：6→8周期+成交量确认）：极端超买暴跌>60%后，需连续8个4H周期企稳+MACD底背离+RSI<30后金叉+成交量缩量企稳方可入场。LAB $12.03→$4.29(-64.35%)是典型场景。",
      "suggested_cycles": 8,
      "min_drop_pct": 0.6,
      "confirmations": [
        "price_stabilization_8_cycles",
        "macd_bullish_divergence",
        "rsi_golden_cross_below_30",
        "volume_shrink_stabilization"
      ]
    },
    "C09_war_escalation_tiered_v2": {
      "status": "formalized",
      "formalized_in": "v4.9.2",
      "description": "战争分级响应v2：局部冲突→全账户暂停新开仓（当前）；全面战争(伊朗封锁霍尔木兹海峡)→全账户清仓+恢复期重置Day0。已正式化为current_optimized_values.war_escalation_warning_level。",
      "tiers": {
        "0_ceasefire": "正常交易",
        "1_local_conflict": {
          "action": "halt_all_new_positions",
          "current": false
        },
        "2_full_scale_war_warning": {
          "trigger": "iran_threaten_blockade_hormuz",
          "action": "position_0_percent_alert_only",
          "current": true
        },
        "3_full_scale_war": {
          "trigger": "iran_actual_blockade_hormuz",
          "action": "full_liquidation_reset_day_zero",
          "current": false
        }
      }
    }
  },
  "v4.12.0_candidates": {
    "D1_fear_stability_detection": {
      "status": "activated",
      "priority": "P0",
      "trigger": "恐惧指数回升至>30但维持<5日",
      "action": "维持当前tier_10状态，不降级",
      "rationale": "恐惧9→29的断崖式回升可能是'死猫反弹'式情绪波动，需稳定≥5日方可作为解除条件。源自LAB 2026-06-02分析报告v5.1发现D2。",
      "suggested_stable_days": 5,
      "activated_date": "2026-06-02 09:07:39"
    },
    "D2_contract_spot_premium_circuit": {
      "status": "activated",
      "priority": "P0",
      "trigger": "永续合约价/现货价 > 1.30",
      "action": "禁止该品种做多方向新开仓",
      "current": "LAB合约$4.48/现货$3.21=1.396（已触发）",
      "rationale": "溢价>30%暗示庄家控盘/流动性操纵，风险极高。源自v5.1发现D4。",
      "suggested_threshold": 1.3,
      "activated_date": "2026-06-02 09:07:39"
    },
    "D3_crash_rebound_volume_divergence": {
      "status": "activated",
      "priority": "P1",
      "trigger": "暴跌>60%后反弹>30% 且 成交量<暴跌前7日均量50%",
      "action": "信号自动降一级（A→B, B→C）",
      "rationale": "无量反弹=诱多陷阱。LAB 2026-05-31→2026-06-02反弹+58.3%但成交量萎缩。源自v5.1发现D1。",
      "suggested_crash_threshold": 0.6,
      "suggested_rebound_threshold": 0.3,
      "suggested_volume_ratio": 0.5,
      "activated_date": "2026-06-02 09:07:39"
    },
    "D4_mstr_divestiture_weight_upgrade": {
      "status": "activated",
      "priority": "P1",
      "trigger": "Strategy Inc.减持BTC",
      "action": "全账户仓位上限×0.3（从×0.5升级）",
      "rationale": "'永不卖出'信仰崩塌>普通机构流出，信号意义远超量级。源自v5.1发现D3。",
      "current": "已减持32 BTC(~$2.5M)，触发mstr_divestiture_warning",
      "activated_date": "2026-06-02 09:07:39",
      "confirmed": true,
      "confirmed_detail": "2026-06-01: Strategy Inc.出售32 BTC (~$2.5M)，2022年以来首次减持",
      "new_weight": 0.15,
      "additional_rule": "MSTR连续减持>3日 → 全账户禁止新开仓90天"
    },
    "D5_hormuz_traffic_recovery_monitor": {
      "status": "activated",
      "priority": "P1",
      "trigger": "霍尔木兹日均商船通行恢复至>50艘",
      "action": "war_escalation_weight从0.5降至0（等效Level3→2.5）",
      "rationale": "海峡通行量是战争实际封锁程度的客观指标。当前日均3艘(vs战前100+)。源自v5.1发现D5。",
      "suggested_recovery_threshold": 50,
      "current_traffic": 3,
      "activated_date": "2026-06-02 09:07:39",
      "war_level_update": "Level 3→4",
      "mandeb_strait_sub_monitor": {
        "status": "activated",
        "trigger": "伊朗圣城旅指挥官卡尼暗示曼德海峡将与霍尔木兹保持一致",
        "action": "等效战争权重+0.2"
      }
    }
  },
  "strategy_iteration_log": {
    "v4.0": {
      "date": "2026-05",
      "trigger": "初始版本",
      "report": ""
    },
    "v4.1_4.6": {
      "date": "2026-05_06-01",
      "trigger": "多轮迭代至4.6",
      "report": "见报告库"
    },
    "v4.7": {
      "date": "2026-06-01",
      "time": "12:00",
      "trigger": "BNB跌破$687创3个月新低，LAB涨60%+触发4项否决",
      "report": "币安龙头黑马预测报告_20260601_1200.md",
      "key_changes": [
        "BNB评级B→C",
        "LAB专属否决项1-4激活",
        "BNB/CAKE/LISTA/TWT专属参数新增"
      ]
    },
    "v4.7_update": {
      "date": "2026-06-01",
      "time": "14:00",
      "trigger": "战情维持，市场整体下沉",
      "report": "币安龙头黑马预测报告_20260601_1400.md",
      "key_changes": [
        "LAB风控参数无变化",
        "BNB $680-$687",
        "战争黑天鹅确认"
      ]
    },
    "v4.7_update2": {
      "date": "2026-06-01",
      "time": "16:00",
      "trigger": "LAB涨至$8.68，新增否决项5-7",
      "report": "币安龙头黑马预测报告_20260601_1600.md",
      "key_changes": [
        "LAB否决项扩至7项",
        "新增LAB 24h成交量异常/盘口深度/低流通高FDV否决"
      ]
    },
    "v4.8": {
      "date": "2026-06-01",
      "time": "18:00",
      "trigger": "新增爆仓恢复机制+停火冷却期+七大LAB否决项固化",
      "report": "币安龙头黑马预测报告_20260601_1800.md",
      "key_changes": [
        "LAB爆仓$7.461→爆仓恢复期14天(仓位2%/杠杆0.5x)",
        "停火冷却72h→7天",
        "7项LAB否决固化",
        "LAB交易参数7项新增"
      ]
    },
    "v4.8_snapshot": {
      "date": "2026-06-01",
      "time": "20:00",
      "trigger": "BNB从$707继续下行至$695(-5.4%/24h)，战情延续(美军打击伊朗Goruk/Qeshm岛)",
      "report": "币安龙头黑马预测报告_20260601_2000.md",
      "key_changes": [
        "BNB跌破$700，距200MA($734)差-5.3%",
        "CAKE $1.44 RSI47.91中性",
        "LAB $12.52(+192%周)7否决全激活",
        "ETF流出第9日预警",
        "新增v4.9候选4项(C04~C07)"
      ]
    },
    "v4.9": {
      "date": "2026-06-01",
      "time": "23:00",
      "trigger": "LAB $12.03→$4.29暴跌(-64.35%)，美伊冲突升级(伊朗威胁封锁霍尔木兹)，ETF连续3周流出>$30亿",
      "report": "LAB_USDT永续合约交易分析报告_20260601_叠化v4.9.md",
      "key_changes": [
        "v4.8→v4.9叠化：暴跌反转识别模块+战争分级响应v2+爆仓恢复暴跌情境豁免+黑天鹅避险价值追踪",
        "LAB七重熔断→四重激活：布林带/RSI/贪婪因暴跌解除，战争/ETF/爆仓恢复/波动率仍激活",
        "LAB $4.29(-64.35% from $12.03)，入场区间重算$3.50-$4.80",
        "战争分级响应v2：局部冲突→暂停(当前)；全面战争(封锁霍尔木兹)→全账户清仓+重置Day0",
        "爆仓恢复期Day2/14，新增暴跌情境豁免(Day8+可放宽至5%)",
        "交易心理画像v2.0→v2.3：三重认知根节点锁定"
      ]
    },
    "v4.9.2": {
      "date": "2026-06-01",
      "time": "23:30",
      "trigger": "伊朗22:31宣布暂停与美国谈判+全面封锁霍尔木兹海峡+曼德海峡。WTI原油飙$94.20(+7.8%)，布伦特$97.23(+6.7%)。BTC跌破$73K，恐惧指数29→23极度恐惧。C09全面战争预警激活。",
      "report": "币安龙头黑马预测报告_20260601_2330.md",
      "key_changes": [
        "C09战争分级响应v2正式化：从candidate→P0正式模块。伊朗'计划封锁海峡'=仓位0%预警，'实际封锁'=全账户清仓+重置Day0",
        "C08暴跌反转条件强化：6个→8个4H周期确认，新增成交量缩量企稳确认",
        "战争升级预警等级新参数：war_escalation_warning_level（0=停火/1=局部冲突/2=全面战争预警/3=全面战争）",
        "原油-加密联动监控模块新增：WTI+Brent双轨追踪，原油单日>5%→全局风控收紧至仓位上限+50%熔断",
        "恐惧指数tier_25中间层新增：<25→仓位上限50%+杠杆0.5x（填补<20暂停与<30半仓之间的缺口）",
        "恐惧指数更新：29→23（极度恐惧）逼近<20暂停线+新增<25中间层已触发",
        "BNB $733→$695(-5.39%)：ETF催化已定价80%，利好兑现后回调，C级维持",
        "CAKE $1.43：跟随BNB下行，无独立催化，C级维持",
        "LAB $3.83-$4.29：+14.74%反弹但四重熔断仍激活（战争🔴+ETF流出🔴+爆仓恢复🔴+波动率🟡），C级维持",
        "黑天鹅避险价值追踪追加：伊朗封锁海峡·原油飙涨→全球风险资产崩盘正在规避中",
        "全账户零开仓：C09全面战争预警下ETF流出+爆仓恢复+波动率四重熔断叠加"
      ]
    },
    "v4.10.0": {
      "date": "2026-06-02",
      "time": "03:00",
      "trigger": "伊朗重开霍尔木兹海峡+美伊60天停火延长。WTI原油暴跌-11.31%至$83.98，Brent -9.97%至$89.48。恐惧指数9（极度恐慌极值），BTC $64,823(-8.39%/24h,-21.71%/7d)。ETF流出-$544.94M/日加速。",
      "report": "币安龙头黑马预测报告_20260602_0300.md",
      "key_changes": [
        "C10战争熔断Level修正：伊朗重开海峡→war_escalation_warning_level 2→1（局部冲突），新增7天停火冷却期（6月9日解除）",
        "C11恐惧指数tier_10极值强化：恐惧<15→仅允许持有BTC，禁止一切非BTC新开仓。恐惧指数9触发此规则",
        "战争熔断降级不解除：60天停火期间仍为Level1局部冲突，需7天冷却期方降为Level0",
        "五重熔断实时：ETF流出🔴+爆仓恢复🔴Day3/14+恐惧tier_10🔴+波动率🟡+战争🟡Level1",
        "BNB $651.61(-3.3%)：支撑$640，五重熔断下禁止开仓",
        "CAKE $1.43(-5.83%)：tier_10禁止非BTC，无开仓资格",
        "LAB $4.29(持平)：爆仓恢复Day3/14，仓位2%/杠杆0.5x",
        "原油解除联动预警：WTI从$107峰值回落23.7%，原油-加密通胀传导压力解除",
        "最早可开仓日期≥6月13日（爆仓恢复期结束+等待战争冷却/恐惧回升/ETF流出停止）",
        "全账户零开仓：五重熔断叠加，仅允许持有现有BTC"
      ]
    },
    "v4.10.1": {
      "date": "2026-06-02",
      "time": "03:13",
      "trigger": "美伊60天停火破裂。伊朗6/1暂停中间人谈判+计划彻底封锁霍尔木兹海峡+启动曼德海峡新战线。WTI原油+6.16%。BTC $71,500(-2.88%/24h)。恐惧指数29（脱离极度恐慌）。ETF连续10日流出$30B。Strategy Inc.(MSTR)首次减持BTC。24h全网爆仓$5.23B/14.5万人。",
      "report": "币安龙头黑马预测报告_20260602_0313.md",
      "key_changes": [
        "C12战争熔断Level升级：美伊停火破裂→war_escalation_warning_level 2→3（全面战争），冷却期7天→30天",
        "恐惧指数tier_10解除：恐惧9→29，脱离极度恐慌，恢复山寨币开仓权限（恐惧🟡，非🔴）",
        "ETF流出权重显性化：etf_outflow_weight_in_circuit_breaker=0.25（25%），ETF流出上升为核心驱动因子",
        "爆仓恢复期反向下单禁令：post_liquidation_recovery_no_reverse_trade=true，对齐交易心理画像'止损缺失'根节点",
        "五重熔断实时：ETF流出🔴+爆仓恢复🔴Day4/14+恐惧🟡(29)+波动率🟡+战争🔴Level3",
        "全账户零开仓：三重红灯（ETF🔴+爆仓🔴+战争🔴）叠加，禁止一切新开仓",
        "最早可开仓日期≥6月13日（爆仓恢复期Day14达标）+需ETF流出收敛+战争降温三重确认"
      ]
    },
    "v4.11.0_PERSONALIZED": {
      "date": "2026-06-02",
      "time": "04:30",
      "trigger": "全域缺口专项补·量化策略叠化。战争Level3确认升级（伊朗暂停谈判+封锁霍尔木兹+美伊互相打击+科威特防空警报）。交易心理画像v2.7蒸馏——第五认知根节点'战争脱敏'。恢复期Day4→Day0重置，14天→30天冷却期，7天→14天模拟交易。",
      "report": "LAB_USDT永续合约交易分析报告_20260602_全域缺口专项补_v5.0.md",
      "key_changes": [
        "P01战争脱敏检测器：恐惧<15连续3日→追加7天冷却。源自画像v2.7'战争脱敏'认知根节点。",
        "P02霍尔木兹信号权重：Level3有效值→3.5，全球油路封锁额外追加7天冷却。",
        "P03 ETF流出加速惩罚：单日>$5亿→追加3天冷静期。当前$544.94M/日已触发。",
        "P04极端回撤二次保护：恢复期后首仓亏损>2%→回退7天模拟交易。防'急着回本'。",
        "P05机会成本日记：每日强制记录'若开仓会怎样'，元认知训练。",
        "P06恢复期规则重置：Day 0（2026-06-02）+30天冷却+14天模拟交易+三条件解除清单。",
        "P07专属三条件解除：战争降级≤1+ETF恢复流入+恐惧>50，三者同时满足方可评估恢复。",
        "策略从通用版v4.10.2升级为专属版v4.11.0，新增5个专属参数模块。",
        "七重熔断实时：ETF流出🔴+爆仓恢复🔴Day0/30+恐惧tier_10🔴(9)+波动率🟡+战争🔴Level3(等效3.5)+原油联动🔴+霍尔木兹权重🔴。",
        "全账户零开仓，30天冷却期，14天模拟交易期。保全本金是第一优先级。"
      ]
    },
    "v4.10.2": {
      "date": "2026-06-02",
      "time": "05:05",
      "trigger": "恐惧指数9→极度恐慌极值(29→9/-25pts断崖式恶化)。Strategy Inc.(MSTR)减持32 BTC。BNB -9.15%远超BTC -2.88%。伊朗暂停谈判+计划封锁霍尔木兹+曼德海峡新战线。ETF流出$544.94M/日加速。全网爆仓$5.23B/14.5万人。WTI原油+6.16%。",
      "report": "币安龙头黑马预测报告_20260602_0505.md",
      "key_changes": [
        "C13恐惧tier_10极值确认：恐惧9触发tier_10（仅BTC）。29→9断崖式恶化(-25pts)，逼近2020/3 COVID崩盘水平(8)",
        "C14 Strategy减持信号：MSTR打破'永不卖出'承诺→新增mstr_divestiture_warning参数→全账户仓位上限额外×0.5",
        "C15恐慌极值干预协议：禁止'抄底'思维+禁止非BTC开仓思考+每周2次心理画像重读",
        "C16 BNB下跌加速：-9.15%/24h，BNB/BTC比率0.0088触发C04正式化→全BNB生态D级自动排除",
        "C17候选tier_5：恐惧<5→全账户仅持有现金/USDT",
        "六重熔断叠加：战争🔴Level3+ETF流出🔴+爆仓恢复🔴Day4/14+恐惧tier_10🔴(9)+波动率🟡+原油联动🔴",
        "全账户零开仓（维持）：且恐惧tier_10下仅允许持有现有BTC，禁止任何非BTC新开仓思考",
        "最早可开仓日期≥6月13日+需ETF流出收敛+战争降温+恐惧回升三重确认"
      ]
    },
    "v4.11.1_PERSONALIZED": {
      "date": "2026-06-02",
      "time": "09:00",
      "trigger": "比特币短线反弹+10.2%（$64,823→$71,466）。恐惧指数从9跳升至29（+20pts），脱离tier_10极度恐慌但仍在恐慌区间。BNB价差异常：Binance $630 vs DEX $661（$31差价）。MSTR首次减持32 BTC确认机构撤离信号。特朗普预计'未来一周内'达成停火协议。WTI原油维持高价（供给冲击）。",
      "report": "币安龙头黑马预测报告_20260602_0858.md",
      "key_changes": [
        "P08恐惧阈值动态映射：恐惧9→29(+20pts)，tier_10→tier_8降级。恐惧<30维持半仓约束，其他五重熔断（战争/ETF/爆仓/原油/霍尔木兹）仍完全封锁开销",
        "P09 BNB/BTC双源校验规则：Binance与DEX双源报价强制校验，任一源<0.009即触发D级自动排除（本轮Binance 0.00882已触发）",
        "P03.1 ETF流出双日确认加罚：单日流出>$500M→3天冷却，若次日继续流出>阈値→追加3天冷却",
        "七重熔断全激活不变：ETF流出🔴+爆仓恢复🔴Day0/30+恐惧tier_8🔴(29)+波动率🟡+战争🔴Level3(等效3.5)+原油联动🔴+霍尔木兹权重🔴",
        "全账户零开仓（维持），30天冷却，14天模拟交易期。P07三条件解除进度0/3（战争降级❌+ETF恢复❌+恐惧>50❌）",
        "最早可开仓日期≥6月13日+需ETF流出收敛+战争降温+恐惧回升三重确认"
      ]
    },
    "v4.12.2": {
      "date": "2026-06-02",
      "time": "14:00",
      "trigger": "全域缺口专项补·量化策略叠化闭环。LAB/USDT永续合约完整分析（趋势/关键价位/仓位风控/七重熔断）。交易心理画像v2.8蒸馏（恐惧31/战争Level4/创伤期IV/恢复期60天）。策略叠化v4.12.1→v4.12.2。",
      "report": "LAB_USDT永续合约交易分析报告_20260602_全域缺口专项补_v5.2.md",
      "key_changes": [
        "【P0】E1恐惧稳定性自动校验 → 新增：恐惧指数连续3日稳定≥25且单日波动<10pts→方可降级tier",
        "【P0】E2合约现货溢价阈值收紧 → 1.30→1.15（印度溢价77%显示1.30过宽）",
        "【P1】E3 ETF流出二次派生熔断 → 连续3日加速流出（日环比+20%）→追加7天冷却",
        "【数据】BTC $70,913(-0.6%)，恐惧31(tier_8)，24h爆仓$7.5135亿",
        "【数据】ETF三周累计流出超$30亿，机构持续撤离",
        "【数据】战争Level4维持（双海峡威胁+美以船只攻击），霍尔木兹日均3艘",
        "【数据】LAB印度市场报价₹1,586.17(+77.38%/24h)，合约现货溢价39.6%",
        "【七重熔断】ETF流出🔴+爆仓恢复🔴Day0/60+恐惧tier_8🔴(31)+波动率🟡+战争🔴Level4+原油联动🔴+霍尔木兹权重🔴",
        "【产出】LAB_USDT分析报告v5.2（趋势判断C级/关键价位/仓位风控/七重熔断评估）",
        "【产出】交易心理画像v2.9（恐惧31更新/战争Level4/创伤期IV/恢复期60天/市场冲击表B.2）",
        "【闭环】策略版本v4.12.2（iteration_log新增/市场状态同步/candidates E1-E3）/子Agent配置同步v4.12.2+v2.9"
      ],
      "triggers": [
        "全域缺口专项补·量化策略叠化任务（第一步：交易心理画像更新v2.8→v2.9）",
        "LAB/USDT永续合约分析（趋势判断/关键价位/仓位风控/七重熔断评估）",
        "策略叠化v4.12.1→v4.12.2（iteration_log新增v4.12.2条目/candidates E1-E3）",
        "闭环校验（SHA256哈希清单/子Agent配置同步/产出物落盘验证）"
      ],
      "verified": true
    },
    "v4.12.4": {
      "date": "2026-06-02",
      "time": "16:00",
      "trigger": "定时任务·币安龙头黑马预测闭环（每2小时）。恐惧23→29→23五次震荡确认D1假阳性脱敏。ETF流出11日$4.84亿创新高（IBIT$4.40亿占91%大型机构赎回）。特朗普口头信号再证伪。霍尔木兹通行15艘/24h封锁实质化。BNB降至$705-710(-2.37%)。BTC逼近$70K关口。WTI原油$92.16(+5.49%)。",
      "report": "币安龙头黑马预测报告_20260602_1600.md",
      "key_changes": [
        "P14恐惧23→D1二次确认：10→29→10→29→23五次震荡确认D1假阳性脱敏模式稳定。恐惧需稳定≥25持续5日方可降级。",
        "P15 ETF流出11日$4.84亿确认：IBIT$4.40亿占91%，大型机构赎回非散户恐慌。P03.1 ETF双日确认加罚维持。",
        "P16特朗普口头信号再证伪：声称'一周内'达成协议，但伊朗外交部指责美以持续违反停火。v2.7已证伪一次口头信号，不降级。",
        "P17霍尔木兹通行15艘/24h确认：战前日均100+→当前15艘，封锁实质化。D5监控维持。",
        "C19候选tier_5：恐惧<5触发tier_5→全账户仅持现金/USDT。监控中。",
        "七重熔断全量激活7.0/7.0：ETF流出🔴+爆仓恢复🔴Day0/60+恐惧tier_25🔴(23)+波动率🟡+战争🔴Level4+原油联动🔴(WTI+5.49%)+霍尔木兹权重🔴",
        "全账户零开仓（维持），60天冷却期，21天模拟。解除条件四要素0/4（战争降级❌+ETF恢复❌+恐惧>50❌+霍尔木兹>50艘❌）",
        "零标的通过：BNB D级排除（BNB/BTC 0.00888）、CAKE C级熔断禁止、LAB D级溢价5.41x禁止、LISTA/TWT C级数据不足排除。"
      ],
      "verified": true
    },
    "v4.12.5": {
      "date": "2026-06-02",
      "time": "18:00",
      "trigger": "定时任务·币安龙头黑马预测闭环（每2小时）。BTC跌破$70K心理关口($69,973，自4/8以来首次)。恐惧指数31→23断崖下跌(-8pts)，D1假阳性脱敏模式再次验证。24h全网爆仓恶化至$7.95亿(+5.9% from $7.51亿)，多单$6.8亿占85%。ETH跌破$2,000($1,996)。ETF 6/1流出$4.84亿创新高(IBIT$4.40亿占91%)。WTI原油维持$92+高位。美伊局势无降温信号。",
      "report": "币安龙头黑马预测报告_20260602_1800.md",
      "key_changes": [
        "P18 BTC跌破$70K: $69,973(-3.56%/24h)，盘中$70,686逼近14天谷底$70,961，自4/8以来首次",
        "P19 恐惧31→23断崖: -8pts，D1假阳性脱敏模式再次验证。恐惧23触发tier_25(仓位50%+杠杆0.5x)",
        "P20 全网爆仓恶化: $7.95亿(+5.9%)，多单$6.8亿占85%，多头惨遭血洗",
        "P21 ETH跌破$2,000: $1,996(-0.96%)，盘中$1,956，山寨币流动性坍塌加速",
        "七重熔断7.0/7.0全量激活维持，全账户零开仓，60天冷却期，解除条件0/4",
        "零标的通过: BNB D级排除(BNB/BTC 0.00888)、CAKE C级熔断禁止、LAB D级溢价5.41x禁止、LISTA/TWT C级数据不足",
        "C19 tier_5监控中: 恐惧23距5仍有距离。E1-E3候选建议正式化"
      ],
      "verified": true
    },
    "v4.12.10": {
      "date": "2026-06-05",
      "time": "07:09",
      "trigger": "定时任务·币安龙头黑马预测闭环（每2小时）。BTC $81,306(+25% from $62K谷底)。恐惧23→46(+23pts)。ETF本周转净流入$11.5亿（前12日流出$38.7亿→逆转）。战争Level4→谈判曙光期过渡。LAB 7日+234%至$14.94-$16.83。BNB $729.98三重催化（范达ETF+美股交易+GENIUS空投）。CAKE $1.58跟随。",
      "report": "币安龙头黑马预测报告_20260605_0709.md",
      "key_changes": [
        "S22 ETF流入反转确认candidate：连续3日净流入>=$20亿→etf_outflow_weight 1.0→0.3",
        "S23 恐惧回升确认candidate：连续3日>50+波动<10pts→fear_index 1.0→0.3",
        "S24 谈判曙光监控candidate：正式停火→war_escalation 1.0→0.3+7天冷却",
        "市场三重积极信号：ETF逆转+恐惧46+谈判曙光，解除进度30-35%",
        "BNB B+评级但BNB/BTC 0.00888 D级排除维持——基本面与比率脱节",
        "LAB 7日+234%但溢价5.41x+7否决全激活——妖币不可追",
        "全账户零开仓维持，七重熔断7.0/7.0，最早可开仓≥2026-08-01",
        "S18-S21四信号维持激活，S22-S24新增三信号监控熔断解除路径"
      ],
      "verified": true
    }
  },
  "v4.12.2_candidates": {
    "E1_fear_stability_auto_check": {
      "status": "candidate",
      "priority": "P0",
      "trigger": "恐惧指数连续3日稳定≥25 且 单日波动<10pts",
      "action": "方可降级tier（如tier_10→tier_8），否则维持当前tier",
      "rationale": "恐惧9→29→10的假阳性震荡显示单日回升不可信。源自v4.12.2叠化发现E1。",
      "suggested_stable_days": 3,
      "suggested_max_daily_swing": 10,
      "activated_date": "2026-06-02 14:00:00"
    },
    "E2_contract_spot_premium_tighten": {
      "status": "candidate",
      "priority": "P0",
      "trigger": "永续合约价/现货价 > 1.15",
      "action": "禁止该品种做多方向新开仓",
      "current": "LAB合约$5.75/现货$4.14=1.396（已触发D2@1.30）",
      "rationale": "印度溢价77.38%显示1.30阈值过宽，庄家控盘信号需更早捕获。源自v4.12.2叠化发现E2。",
      "suggested_threshold": 1.15,
      "activated_date": "2026-06-02 14:00:00"
    },
    "E3_etf_outflow_secondary_penalty": {
      "status": "candidate",
      "priority": "P1",
      "trigger": "ETF连续3日加速流出（日环比+20%）",
      "action": "追加7天冷却期",
      "rationale": "D4 MSTR减持已触发，但ETF流出加速（日$544.94M）未充分惩罚。连续加速流出=机构恐慌性撤离。源自v4.12.2叠化发现E3。",
      "suggested_acceleration_threshold_pct": 20,
      "current_day_outflow": "$544.94M",
      "prior_day_outflow": "$500M+",
      "activated_date": "2026-06-02 14:00:00"
    },
    "C19_tier_5_cash_only": {
      "status": "candidate",
      "priority": "P0",
      "trigger": "恐惧指数 < 5",
      "action": "全账户仅持有现金/USDT，禁止持有任何加密货币（含BTC）",
      "rationale": "恐惧23已触发tier_25，若继续恶化至<5，逼近2020/3 COVID崩盘极值(8)，需全账户现金化保护。源自v4.12.4 P14发现恐惧二次下探后C17升级。",
      "current_fear": 23,
      "threshold": 5,
      "activated_date": "2026-06-02 16:00:00"
    }
  },
  "market_state": {
    "seven_circuit_breakers": {
      "1_etf_outflow": {
        "status": "🔴",
        "weight": 1.0,
        "detail": "ETF连续11日净流出累计~$35B+，但6/5本周转净流入$11.5亿（重大逆转）。IBIT $4.40亿/日赎回已反转。S22:连续3日净流入后ETF熔断可降级。当前Day1/3。Strategy减持32 BTC已Price-in。",
        "trigger": "10日累计>$15B",
        "updated": "2026-06-03 21:54:00"
      },
      "2_liquidation_recovery": {
        "status": "🔴",
        "weight": 1.0,
        "detail": "Day 0/60冷却期，因战争Level4+第三国卷入维持。爆仓恢复期Day0/BEATUSDT三阶段亏损确认。",
        "trigger": "账户曾爆仓",
        "updated": "2026-06-03 21:54:00"
      },
      "3_fear_index": {
        "status": "🔴",
        "weight": 1.0,
        "detail": "恐惧指数46（中性偏恐惧，昨日23/+23pts）。D1假阳性脱敏模式已验证6次。S23:连续3日>50+波动<10pts方可降级。当前46/50差4pts。",
        "trigger": "恐惧11 = tier_10（仅BTC）",
        "updated": "2026-06-03 21:54:00"
      },
      "4_volatility": {
        "status": "🔴",
        "weight": 1.0,
        "detail": "BTC 30d ann vol 60%+，全市场-6%+暴跌加剧波动。S13权重0.5→1.0升级，与ETF/战争/爆仓平级。",
        "trigger": "vol>45%即预警，vol>55%熔断升级",
        "updated": "2026-06-03 21:54:00"
      },
      "5_war_escalation": {
        "status": "🔴",
        "weight": 1.0,
        "detail": "Level 4维持，但「全面战争确认期」→「谈判曙光期」过渡。美伊信息交换重启迹象，远未达成停火。S24:正式停火方可降级+7天冷却。第七认知根节点「谈判信号反复依赖症」——口头信号已证伪至少2次。",
        "trigger": "美伊军事冲突+海峡封锁+第三国卷入",
        "updated": "2026-06-03 21:54:00",
        "equivalent_weight": 4.0,
        "third_country_involvement": "科威特（机场遭袭/1死多伤/领空关闭）+巴林（第五舰队总部遭袭）",
        "hormuz_traffic": "24艘/24h（vs战前100+，伊朗强化管控宣示）",
        "transition_note": "全面战争确认期→谈判曙光期过渡"
      },
      "6_oil_correlation": {
        "status": "🔴",
        "weight": 0.7,
        "detail": "WTI $93.76(+5.49%)，Brent ~$96，战争驱动原油暴力拉升，美伊激烈互袭加剧供给恐慌。",
        "trigger": "单日涨跌>5%",
        "updated": "2026-06-03 21:54:00"
      },
      "7_hormuz_weight": {
        "status": "🔴",
        "weight": 1.0,
        "detail": "伊朗宣布24艘获通行许可（vs之前15艘略升），但伊朗强化管控宣示。霍尔木兹海峡通行仍然高度受限。美伊对峙持续，双方海上封锁为谈判施压工具。",
        "trigger": "通行量<50艘/日",
        "updated": "2026-06-03 21:54:00",
        "mandeb_strait_warning": true
      }
    },
    "total_breaker_weight": 7.0,
    "max_weight": 7.0,
    "account_state": "全账户零开仓",
    "cooldown_days_remaining": 60,
    "simulation_days_remaining": 21,
    "earliest_possible_entry": "2026-08-01",
    "updated": "2026-06-05 07:09:39"
  },
  "bnb_btc_exclusion": {
    "status": "🔴 D级自动排除",
    "current_ratio": 0.00888,
    "threshold": 0.01,
    "gap": "-11.2%",
    "updated": "2026-06-02 18:00:00",
    "note": "BNB ~$690 (₹65,814, -2.37%)，BNB/BTC 0.00888 维持D级排除。BTC跌破$70K（$69,973），全市场下行加速。全BNB生态排除联动。零标的通过。"
  },
  "v4.12.5_candidates": {
    "S01_d2_premium_full_warning": {
      "status": "activated",
      "priority": "P0",
      "trigger": "D2溢价>3.0x（任一交易所）",
      "action": "全BSC生态新开仓禁止+全品种新开仓禁止",
      "rationale": "LAB合约溢价5.41x不仅影响LAB，庄家对倒拉盘行为暗示BSC生态系统性操纵风险。源自v5.4分析报告。",
      "activated_date": "2026-06-02 17:30:00"
    },
    "S02_circuit_breaker_api_enforcement": {
      "status": "activated",
      "priority": "P0",
      "trigger": "七重熔断任一触发",
      "action": "API层硬编码拒绝开仓请求",
      "rationale": "交易心理画像v3.0第六认知根节点「熔断后违规交易」：38笔订单/78笔交易在七重熔断全激活下执行。Markdown文档→交易执行完全断裂。策略规则必须下沉至API/脚本层。",
      "activated_date": "2026-06-02 17:30:00"
    },
    "S03_d1_stability_extend_7days": {
      "status": "activated",
      "priority": "P1",
      "trigger": "恐惧指数需稳定≥25持续7日方可降级",
      "action": "原5日→7日",
      "rationale": "恐惧31→23二次走弱验证D1假阳性脱敏模式，5日仍不足确保稳定性。源自v5.4分析报告。",
      "previous_days": 5,
      "new_days": 7,
      "activated_date": "2026-06-02 17:30:00"
    },
    "S04_daily_discipline_api_automation": {
      "status": "candidate",
      "priority": "P1",
      "trigger": "每日UTC 0:00自动执行",
      "action": "自动生成七重熔断状态报告+机会成本日记+交易日志归档",
      "rationale": "C18交易日志归档缺口解决方案。当前12,885笔订单无本地归档。",
      "activated_date": "2026-06-02 17:30:00"
    },
    "S05_taoist_api_check": {
      "status": "activated",
      "priority": "P1",
      "trigger": "每次开仓API调用前执行",
      "action": "道家心法八条逐条API校验，任一不通过则拒绝开仓",
      "rationale": "将道家心法从文档哲学下沉至API层强制检查，防止执行层断裂。",
      "activated_date": "2026-06-02 17:30:00"
    },
    "S06_multi_exchange_premium_monitor": {
      "status": "activated",
      "priority": "P1",
      "trigger": "任一交易所LAB合约溢价>2.0x",
      "action": "全交易所溢价异常警告+自动触发D2",
      "rationale": "OKX $8.55 vs 现货$3.21=2.66x，扩大D2监控至全交易所。",
      "activated_date": "2026-06-02 17:30:00"
    }
  },
  "v4_12_10_candidates": {
    "S22_etf_inflow_reversal": {
      "status": "candidate",
      "priority": "P1",
      "trigger": "ETF连续3日净流入 且 累计>=$20亿",
      "action": "etf_outflow_weight 1.0→0.3（熔断降级为监控）",
      "rationale": "本周ETF净流入$11.5亿→若持续3日可提前解除ETF熔断。当前Day1/3。",
      "current_status": "ETF净流入Day1（6/5），累计$11.5亿",
      "days_required": 3,
      "min_cumulative_usd": 20000000000,
      "activated_date": "2026-06-05 07:09:39"
    },
    "S23_fear_recovery": {
      "status": "candidate",
      "priority": "P1",
      "trigger": "恐惧指数连续3日>50 且 单日波动<10pts",
      "action": "fear_index_weight 1.0→0.3（熔断降级为监控）",
      "rationale": "恐惧23→46(+23pts)回升显著，但D1假阳性脱敏模式已验证6次。需连续3日>50方可降级。",
      "current_status": "恐惧46（距50阈值差4pts），D1假阳性历史率83%",
      "days_required": 3,
      "min_value": 50,
      "max_daily_swing": 10,
      "activated_date": "2026-06-05 07:09:39"
    },
    "S24_ceasefire_monitor": {
      "status": "candidate",
      "priority": "P0",
      "trigger": "美伊正式宣布停火协议 或 联合国安理会停火决议通过",
      "action": "war_escalation_weight 1.0→0.3（等效Level4→Level2），仍需7天冷却期",
      "rationale": "交易心理画像v3.4记录「谈判曙光期」但远未达成。第七认知根节点「谈判信号反复依赖症」——口头信号已证伪至少2次。仅正式协议方可降级。",
      "current_status": "谈判信号反复，无正式协议",
      "cooldown_days": 7,
      "activated_date": "2026-06-05 07:09:39"
    }
  },
  "special_monitoring_params": {
    "S22": {
      "name": "LAB溢价回归检测",
      "priority": "P0",
      "status": "ACTIVE",
      "description": "合约溢价从>3.0x恢复至<2.0x → D2熔断从🔴→🟡",
      "trigger_threshold": "合约/现货溢价 < 2.0x",
      "current_state": {
        "premium": "5.41x",
        "status": "🔴 未触发"
      },
      "added_in": "v4.12.11"
    },
    "S23": {
      "name": "战争降级72h延迟确认",
      "priority": "P1",
      "status": "ACTIVE",
      "description": "S18任一下降级信号触发后需72h无新攻击方可正式降级",
      "trigger_threshold": "72h无新攻击+外交渠道确认",
      "current_state": {
        "since_last_attack": "<24h",
        "status": "🔴 未触发（6/4晚仍有交火）"
      },
      "added_in": "v4.12.11"
    },
    "S24": {
      "name": "恐惧回升谈判过滤",
      "priority": "P1",
      "status": "ACTIVE",
      "description": "恐惧回升若伴有特朗普口头信号，需额外7日确认",
      "trigger_threshold": "恐惧回升≥25且稳定7日，同时无口头信号驱动的假阳性",
      "current_state": {
        "fear_greed": 46,
        "oral_signal_active": true,
        "stable_days": 1,
        "status": "🟡 观察（恐惧46仅1日）"
      },
      "added_in": "v4.12.11"
    }
  }
}
```
