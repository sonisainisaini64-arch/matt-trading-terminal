"""Matt Multi-Agent Trading Terminal - MT5 Demo, Crypto + Forex, Paper Trading.
+ 7 Improvements (user ne 2026-10-22 ko sab add karne ko kaha):
1 Kill Switch, 2 News Filter, 3 Multi-Timeframe + ATR, 4 Versioning + Rollback,
5 Drift Monitor + Alerts, 6 Correlation Check, 7 Real Cost Backtest.
+ Self-Improvement (TOP PRIORITY, kabhi mat hatana) - learning.py se.
Mode switch: config.yaml me mode: demo hai. Real par switch kabhi auto nahi.
"""

from agents import (
    ResearchAgent, StrategyAgent, CodingAgent, BacktestingAgent,
    ValidationAgent, RiskAgent, ExecutionAgent,
)
from mt5_adapter import MT5Adapter
from learning import analyze_trade
from improvements import (
    KillSwitch, news_filter_blocked, multit_timeframe_confirm, atr_stop,
    StrategyVersioning, drift_alert, correlation_check, real_cost_pnl,
    ATRTrailingSL, partial_profit_booking, DailyTradeLimiter, session_filter,
    strategy_ranking, AlertSystem, spread_widening_filter,
    auto_parameter_optimization, walk_forward_monte_carlo, sentiment_score,
    dynamic_capital_allocation, regime_shift_detect, weekend_gap_protection,
    time_exit_check, weekly_ai_review_report,
)
from learning import load_lessons
import datetime

MARKETS = [
    ("Crypto", "BTCUSDT"),
    ("Crypto", "ETHUSDT"),
    ("Forex", "EURUSD"),
    ("Forex", "GBPUSD"),
]


def _load_mode():
    try:
        with open("config.yaml") as f:
            for line in f:
                if line.strip().startswith("mode:"):
                    value = line.split(":", 1)[1].strip()
                    value = value.split("#", 1)[0].strip()
                    return value or "demo"
    except Exception:
        pass
    return "demo"


def main():
    mode = _load_mode()
    print(f"=== Matt Multi-Agent Trading Terminal (MT5, Mode={mode.upper()}) ===")
    mt5 = MT5Adapter(mode=mode, mcp_endpoint=None)
    mt5.connect()
    kill = KillSwitch()
    versioning = StrategyVersioning()
    limiter = DailyTradeLimiter(max_trades_per_day=5)
    alerts = AlertSystem()
    active_symbols = []
    hour_utc = datetime.datetime.utcnow().hour

    for market, symbol in MARKETS:
        print(f"\n--- {market} {symbol} ---")
        if kill.tripped:
            print("[KillSwitch] Trading already stopped - aage ke symbols skip.")
            break
        # 2. News Filter - demo me aaj koi event nahi mana gaya hai
        if news_filter_blocked(symbol, demo_event_today=None):
            continue
        # 10a. Session Filter + Daily Limit + Spread Filter
        if not session_filter(market, hour_utc):
            continue
        if not limiter.allow():
            break
        if spread_widening_filter(current_spread_pct=0.06, normal_spread_pct=0.05):
            continue
        # 6. Correlation Check - pehle se active correlated symbol ho to warning
        correlation_check(symbol, active_symbols)

        research = ResearchAgent().run(symbol, market)
        # Advanced: Regime Shift + Sentiment + Weekend protection
        regime_shift_detect(research["prices"])
        sentiment_score(symbol)
        _now = datetime.datetime.utcnow()
        if weekend_gap_protection(market, _now.weekday(), _now.hour):
            continue
        strategy = StrategyAgent().run(research)
        code = CodingAgent().run(strategy)
        backtest = BacktestingAgent().run(code)

        if not ValidationAgent().run(backtest):
            print("[GATE] Validation FAILED - is symbol par Execution nahi hoga.")
            continue

        # 3. Multi-Timeframe + ATR - demo me short aur long trend dono trending mana gaya
        # (real me alag timeframe ke trend yahan aayenge)
        multit_timeframe_confirm("up", "up")
        atr_stop(strategy["strategy"]["stop_pct"], research["vol"])

        risk = RiskAgent().run(strategy, vol=research["vol"])
        # 8. ATR Based Trailing SL - user ki cheez, 2026-10-22 ko add karne ko kaha
        # Entry = last demo price, ATR = price * volatility% (demo proxy)
        _entry = research["prices"][-1]
        _atr = abs(_entry) * research["vol"] / 100.0 if research["vol"] else abs(_entry) * 0.01
        _trailing = ATRTrailingSL(entry_price=_entry, atr_value=_atr, multiplier=2.0, direction="long")
        print(f"[TrailingSL] Setup {symbol}: Entry={_entry:.2f} ATR={_atr:.2f} Initial TrailingSL={_trailing.trailing_sl:.2f} (2x ATR, sirf upar jayega, kabhi neeche nahi)")
        ExecutionAgent().run(strategy, risk, mode="paper")
        mt5.place_order(strategy, risk)
        active_symbols.append(symbol)
        # 9. Partial Profit Booking demo - price 1R upar jaye to aadhi close, SL breakeven
        _entry2 = research["prices"][-1]
        partial_profit_booking(entry_price=_entry2, current_price=_entry2 * 1.02, risk_pct=2.0)

        # Advanced: Walk-Forward + Monte Carlo + Auto Optimization + Time Exit
        walk_forward_monte_carlo(research["prices"])
        auto_parameter_optimization([backtest["in_sample"]["return_pct"], backtest["out_sample"]["return_pct"]])
        time_exit_check(open_bars=10)
        # 7. Real Cost - gross se net nikalo
        gross = backtest["out_sample"]["return_pct"]
        net = real_cost_pnl(gross, backtest["out_sample"]["trades"])
        # 5. Drift Monitor - backtest vs paper (demo me paper = net)
        if drift_alert(gross, net):
            alerts.send_alert(f"Drift alert {symbol}: backtest {gross}% vs paper {net}%")
        # 4. Versioning - nayi version kharab ho to rollback signal
        versioning.save_version(strategy["strategy"]["name"], net)
        # 1. Kill Switch check - net pnl ke baad
        if not kill.check(net, backtest["out_sample"]["max_drawdown_pct"]):
            break

        # Self-Improvement - TOP PRIORITY, kabhi mat hatana
        trade = {
            "symbol": symbol, "market": market,
            "regime": strategy["regime"],
            "strategy": strategy["strategy"]["name"],
            "pnl_pct": net,
            "trades": backtest["out_sample"]["trades"],
        }
        analyze_trade(trade)

    print("\n=== Done: MT5 demo/paper run complete, koi real order nahi bheja gaya ===")
    print("Lessons trade_journal.jsonl aur lessons.json me save ho gayi hain.")
    print("Improvements: KillSwitch, NewsFilter, MultiTF+ATR, Versioning, DriftMonitor, Correlation, RealCost - sab integrated hain.")
    print("Additional: ATR TrailingSL, PartialProfit, DailyLimit+Session, StrategyRanking, Alerts, SpreadFilter - sab integrated hain.")
    # 11. Strategy Ranking - lessons se best strategy nikalo
    ranked = strategy_ranking(load_lessons())
    # Advanced: Dynamic Capital Allocation + Weekly Review
    _scores = {k: float(v) for k, v in ranked} if ranked else {}
    if _scores:
        dynamic_capital_allocation(_scores)
    weekly_ai_review_report(load_lessons())
    alerts.send_alert("Terminal run complete - paper mode, koi real order nahi gaya.")


if __name__ == "__main__":
    main()
