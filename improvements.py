"""7 Improvements - sab user ne 2026-10-22 ko add karne ko kaha.

1. Kill Switch
2. News / Economic Calendar Filter
3. Multi-Timeframe + ATR Stop/Size
4. Strategy Versioning + Rollback
5. Paper vs Live Drift Monitor + Alerts
6. Correlation Check (Portfolio)
7. Real Cost Backtest (Spread + Commission + Swap)

Ye sab demo data par chalte hain, live me inki jagah asli calendar, ATR,
broker costs aur live P&L plug honge. Koi bhi improvement profit ki guarantee
nahi deta - ye galtiyan aur risk kam karte hain.
"""
import json
import os


class KillSwitch:
    def __init__(self, daily_loss_limit_pct=-5.0, max_drawdown_pct=20.0):
        self.daily_loss_limit = daily_loss_limit_pct
        self.max_drawdown = max_drawdown_pct
        self.daily_pnl = 0.0
        self.tripped = False

    def check(self, pnl_pct, drawdown_pct=0.0):
        self.daily_pnl += pnl_pct
        if self.daily_pnl <= self.daily_loss_limit or drawdown_pct >= self.max_drawdown:
            self.tripped = True
            print(f"[KillSwitch] TRIPPED! Daily PnL={self.daily_pnl:.2f}% Drawdown={drawdown_pct}% - trading RUK GAYI, manual review ke bina dobara nahi chalegi.")
            return False
        print(f"[KillSwitch] OK - Daily PnL={self.daily_pnl:.2f}% (limit {self.daily_loss_limit}%)")
        return True


HIGH_IMPACT_EVENTS = {
    "EURUSD": ["CPI", "FOMC"],
    "GBPUSD": ["CPI"],
    "BTCUSDT": ["FOMC"],
    "ETHUSDT": [],
}


def news_filter_blocked(symbol, demo_event_today=None):
    if demo_event_today and demo_event_today in HIGH_IMPACT_EVENTS.get(symbol, []):
        print(f"[NewsFilter] BLOCKED {symbol} - aaj high-impact news hai: {demo_event_today}, isliye is symbol par trade nahi lenge.")
        return True
    print(f"[NewsFilter] OK {symbol} - koi high-impact news block nahi hai (demo check).")
    return False


def multit_timeframe_confirm(short_trend, long_trend):
    ok = short_trend == long_trend
    print(f"[MultiTF] Short={short_trend} Long={long_trend} -> {'CONFIRMED' if ok else 'AVOID - timeframe mismatch'}")
    return ok


def atr_stop(base_stop_pct, volatility_pct):
    adjusted = base_stop_pct * (1 + volatility_pct / 10.0)
    print(f"[ATR] Base stop {base_stop_pct}% + volatility {volatility_pct:.2f}% -> Adjusted stop {adjusted:.2f}%")
    return round(adjusted, 2)


class StrategyVersioning:
    def __init__(self, filepath="strategy_versions.json"):
        self.filepath = filepath
        self.versions = []
        if os.path.exists(filepath):
            try:
                with open(filepath) as f:
                    self.versions = json.load(f)
            except Exception:
                self.versions = []

    def save_version(self, strategy_name, pnl_pct):
        version = {"version": len(self.versions) + 1, "strategy": strategy_name, "pnl_pct": pnl_pct}
        self.versions.append(version)
        with open(self.filepath, "w") as f:
            json.dump(self.versions, f, indent=2)
        if len(self.versions) >= 2:
            prev = self.versions[-2]["pnl_pct"]
            if pnl_pct < prev - 2.0:
                print(f"[Versioning] ROLLBACK! Nayi version {pnl_pct}% purani {prev}% se 2%+ kharab hai - purani version par wapas jao.")
                return "rollback"
        print(f"[Versioning] Version {version['version']} saved: {strategy_name} pnl={pnl_pct}%")
        return "keep"


def drift_alert(backtest_pnl, paper_pnl, threshold=3.0):
    drift = abs(backtest_pnl - paper_pnl)
    if drift > threshold:
        print(f"[DriftMonitor] ALERT! Backtest {backtest_pnl}% vs Paper {paper_pnl}% - drift {drift:.2f}% > {threshold}% - strategy drift ho raha hai, review karo.")
        return True
    print(f"[DriftMonitor] OK - Backtest {backtest_pnl}% vs Paper {paper_pnl}% drift {drift:.2f}%")
    return False


CORRELATED_GROUPS = {
    "USD_FOREX": ["EURUSD", "GBPUSD"],
    "CRYPTO": ["BTCUSDT", "ETHUSDT"],
}


def correlation_check(symbol, active_symbols, max_group_exposure_pct=20.0):
    for group, members in CORRELATED_GROUPS.items():
        if symbol in members:
            others = [s for s in members if s in active_symbols and s != symbol]
            if others:
                print(f"[Correlation] WARNING {symbol} correlated hai {others} ke saath ({group}) - total exposure {max_group_exposure_pct}% se zyada mat rakho.")
                return False
    print(f"[Correlation] OK {symbol} - koi correlated active trade nahi hai.")
    return True


def real_cost_pnl(gross_pnl_pct, trades, spread_pct=0.05, commission_pct=0.02, swap_pct=0.01):
    cost = trades * (spread_pct + commission_pct + swap_pct)
    net = gross_pnl_pct - cost
    print(f"[RealCost] Gross {gross_pnl_pct}% - Spread/Commission/Swap {cost:.2f}% ({trades} trades) = Net {net:.2f}%")
    return round(net, 2)


# 9-13. Additional improvements - user ne 2026-10-22 ko sab add karne ko kaha
# 9 Partial Profit Booking, 10 Max Trades + Session Filter,
# 11 Strategy Ranking, 12 Telegram/WhatsApp Alerts (placeholder, no credentials),
# 13 Spread Widening Filter


def partial_profit_booking(entry_price, current_price, risk_pct=2.0):
    """1R profit par aadhi position close karo, baaki ka SL breakeven par le aao.
    1R = risk jitna profit. Demo me entry 100, risk 2% -> 1R price 102."""
    profit_pct = (current_price - entry_price) / entry_price * 100
    if profit_pct >= risk_pct:
        print(f"[PartialProfit] 1R hit! Profit {profit_pct:.2f}% >= risk {risk_pct}% - aadhi position close karo, baaki ka SL breakeven ({entry_price:.2f}) par le aao.")
        return {"action": "close_half", "new_sl": entry_price}
    print(f"[PartialProfit] Abhi 1R nahi hua: profit {profit_pct:.2f}% < risk {risk_pct}% - hold karo.")
    return {"action": "hold", "new_sl": None}


class DailyTradeLimiter:
    def __init__(self, max_trades_per_day=5):
        self.max_trades = max_trades_per_day
        self.count = 0

    def allow(self):
        if self.count >= self.max_trades:
            print(f"[DailyLimit] BLOCKED - aaj {self.count} trades ho chuke hain, limit {self.max_trades} hai.")
            return False
        self.count += 1
        print(f"[DailyLimit] OK - aaj ka trade {self.count}/{self.max_trades}")
        return True


def session_filter(market, hour_utc):
    """Forex: London + New York session 7-20 UTC me hi trade karo.
    Crypto: 24/7 chalta hai, isliye hamesha allowed.
    Low-liquidity time me Forex trade avoid karo."""
    if market == "Crypto":
        print(f"[Session] OK Crypto - 24/7 allowed, hour {hour_utc} UTC")
        return True
    ok = 7 <= hour_utc <= 20
    print(f"[Session] Forex hour {hour_utc} UTC -> {'ALLOWED (London/NY session)' if ok else 'BLOCKED - low liquidity session'}")
    return ok


def strategy_ranking(lessons):
    """lessons.json se har strategy ka profit/loss count nikal ke ranking do.
    Sabse acchi strategy pehle. Live me recent paper performance se ranking hogi."""
    scores = {}
    for key, entry in lessons.items():
        scores[key] = entry.get("profits", 0) - entry.get("losses", 0)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(f"[Ranking] Strategy ranking (profits-losses): {ranked}")
    return ranked


class AlertSystem:
    """Telegram/WhatsApp alerts ka placeholder.
    Asli bot token / chat ID kabhi code ya chat me mat likhna.
    Jab user secure tareeke se dega, tab yahan Telegram/WhatsApp API call lagega.
    Abhi alert ko console + alerts.log me likha jata hai."""

    def __init__(self, logfile="alerts.log"):
        self.logfile = logfile

    def send_alert(self, message):
        print(f"[ALERT] {message}")
        try:
            with open(self.logfile, "a") as f:
                f.write(message + "\n")
        except Exception:
            pass
        return True


def spread_widening_filter(current_spread_pct, normal_spread_pct=0.05, max_multiple=3.0):
    """Spread normal se 3x zyada badh jaye to trade mat lo - slippage bahut hoga."""
    if current_spread_pct > normal_spread_pct * max_multiple:
        print(f"[SpreadFilter] BLOCKED - spread {current_spread_pct}% normal {normal_spread_pct}% se {max_multiple}x zyada hai.")
        return True
    print(f"[SpreadFilter] OK - spread {current_spread_pct}% normal range me hai.")
    return False


# 8. ATR Based Trailing SL - user ki cheez, 2026-10-22 ko add karne ko kaha
class ATRTrailingSL:
    """Long trade ke liye: price upar jaye to trailing SL bhi upar jayega,
    kabhi neeche nahi aayega. Price trailing SL ko touch kare to exit,
    taaki profit lock ho jaye aur loss bada na ho.
    Short trade ke liye ulta: price neeche jaye to trailing SL neeche jayega.
    ATR = Average True Range ka simple demo version: price ki volatility.
    Default multiplier = 2.0 x ATR, user badal sakta hai."""

    def __init__(self, entry_price, atr_value, multiplier=2.0, direction="long"):
        self.entry = entry_price
        self.atr = atr_value
        self.multiplier = multiplier
        self.direction = direction
        if direction == "long":
            self.trailing_sl = entry_price - atr_value * multiplier
            self.highest = entry_price
        else:
            self.trailing_sl = entry_price + atr_value * multiplier
            self.lowest = entry_price

    def update(self, price):
        if self.direction == "long":
            if price > self.highest:
                self.highest = price
                new_sl = price - self.atr * self.multiplier
                if new_sl > self.trailing_sl:
                    self.trailing_sl = new_sl
            hit = price <= self.trailing_sl
        else:
            if price < self.lowest:
                self.lowest = price
                new_sl = price + self.atr * self.multiplier
                if new_sl < self.trailing_sl:
                    self.trailing_sl = new_sl
            hit = price >= self.trailing_sl
        print(f"[TrailingSL] Price={price:.2f} TrailingSL={self.trailing_sl:.2f} "
              f"ATR={self.atr:.2f} x{self.multiplier} -> {'EXIT HIT' if hit else 'hold'}")
        return hit

    def demo_run(self):
        """Demo: price pehle upar jaye, phir wapas aaye - trailing SL profit lock karega."""
        print("[TrailingSL] Demo run: entry, phir price up, phir wapas")
        prices = [self.entry, self.entry * 1.02, self.entry * 1.05, self.entry * 1.03, self.entry * 1.01]
        for p in prices:
            if self.update(p):
                print(f"[TrailingSL] Demo exit at {p:.2f}, profit lock hua.")
                return p
        print("[TrailingSL] Demo end, trailing SL abhi hit nahi hua.")
        return None


# 14-20. Advanced improvements - user ne 2026-10-22 ko sab add karne ko kaha
# 14 Auto Parameter Optimization, 15 Walk-Forward + Monte Carlo,
# 16 Sentiment Analysis, 17 Dynamic Capital Allocation,
# 18 Regime Shift Detection, 19 Weekend Gap + Time Exit,
# 20 Weekly AI Review Report
import random
import statistics


def auto_parameter_optimization(recent_pnls, sma_period=5, atr_multiplier=2.0):
    """Recent PnL dekh ke settings tune karo. Loss zyada ho to ATR multiplier badhao
    (stop wider, jaldi hit na ho), win rate accha ho to default rakho."""
    if not recent_pnls:
        print(f"[AutoOpt] No recent PnL - default SMA={sma_period} ATRx={atr_multiplier}")
        return {"sma_period": sma_period, "atr_multiplier": atr_multiplier}
    wins = sum(1 for p in recent_pnls if p > 0)
    win_rate = wins / len(recent_pnls)
    new_atr = atr_multiplier
    new_sma = sma_period
    if win_rate < 0.4:
        new_atr = round(atr_multiplier + 0.5, 2)
        new_sma = sma_period + 2
        print(f"[AutoOpt] Win rate {win_rate:.0%} low hai - SMA {sma_period}->{new_sma}, ATRx {atr_multiplier}->{new_atr} (wider stop, slow signal)")
    else:
        print(f"[AutoOpt] Win rate {win_rate:.0%} OK hai - SMA={sma_period} ATRx={atr_multiplier} same rakho")
    return {"sma_period": new_sma, "atr_multiplier": new_atr}


def walk_forward_monte_carlo(prices, folds=3, simulations=100):
    """Walk-forward: prices ko folds me baant ke har fold ka return nikalo.
    Monte Carlo: returns ko shuffle karke 100 random scenarios banao, mean aur worst 5% nikalo.
    Ye batata hai strategy sirf ek period me acchi to nahi lagi."""
    if len(prices) < folds + 1:
        print("[WalkForward] Data kam hai, walk-forward skip")
        return {"folds": [], "mc_mean": 0.0, "mc_worst5": 0.0}
    n = len(prices) // folds
    fold_returns = []
    for i in range(folds):
        chunk = prices[i*n:(i+1)*n+1] if i < folds-1 else prices[i*n:]
        if len(chunk) >= 2 and chunk[0]:
            fold_returns.append(round((chunk[-1]-chunk[0])/chunk[0]*100, 2))
    returns = [(prices[i+1]-prices[i])/prices[i] for i in range(len(prices)-1) if prices[i]]
    rng = random.Random(42)
    sim_totals = []
    for _ in range(simulations):
        # Random sampling with replacement - har scenario me alag return sequence banti hai,
        # isliye final total alag hota hai (sirf shuffle karne se total same rehta, wo galat hota)
        sampled = [rng.choice(returns) for _ in returns]
        sim_totals.append(sum(sampled)*100)
    sim_totals.sort()
    worst5 = round(sim_totals[max(0, int(len(sim_totals)*0.05)-1)], 2)
    mean = round(statistics.mean(sim_totals), 2) if sim_totals else 0.0
    print(f"[WalkForward] Fold returns: {fold_returns}")
    print(f"[MonteCarlo] 100 scenarios: mean {mean}%, worst 5% {worst5}%")
    return {"folds": fold_returns, "mc_mean": mean, "mc_worst5": worst5}


DEMO_SENTIMENT = {"BTCUSDT": 0.6, "ETHUSDT": 0.3, "EURUSD": -0.2, "GBPUSD": 0.1}
POSITIVE_WORDS = ["bullish", "growth", "strong", "rally", "up", "positive"]
NEGATIVE_WORDS = ["bearish", "crash", "weak", "down", "negative", "fear"]


def sentiment_score(symbol, news_text=""):
    """Demo sentiment: symbol ka base score + news text me positive/negative words.
    Live me news API se asli text aayega. Score -1 se +1 tak."""
    base = DEMO_SENTIMENT.get(symbol, 0.0)
    text = news_text.lower()
    score = base + 0.1 * sum(1 for w in POSITIVE_WORDS if w in text) - 0.1 * sum(1 for w in NEGATIVE_WORDS if w in text)
    score = max(-1.0, min(1.0, round(score, 2)))
    label = "positive" if score > 0.2 else "negative" if score < -0.2 else "neutral"
    print(f"[Sentiment] {symbol} score {score} ({label})")
    return score


def dynamic_capital_allocation(scores, total_capital=10000.0):
    """Jo symbol/strategy ka score zyada hai use zyada capital, kam ko kam.
    Min 10%, max 40% per symbol, phir normalize karo taaki total 100% ho."""
    if not scores:
        return {}
    raw = {k: max(0.1, v + 1.0) for k, v in scores.items()}
    total = sum(raw.values())
    alloc = {}
    for k, v in raw.items():
        pct = max(0.10, min(0.40, v / total))
        alloc[k] = round(pct * total_capital, 2)
    # Normalize to total capital
    s = sum(alloc.values())
    if s:
        alloc = {k: round(v / s * total_capital, 2) for k, v in alloc.items()}
    print(f"[Allocation] Dynamic capital: {alloc} (total ${total_capital})")
    return alloc


def regime_shift_detect(prices):
    """Pehle half aur dusre half ka trend/vol compare karo. Sign change ya vol 50%+ jump ho to shift."""
    if len(prices) < 10:
        print("[RegimeShift] Data kam hai, shift check skip")
        return False
    mid = len(prices) // 2
    first = prices[:mid]
    second = prices[mid:]
    t1 = (first[-1]-first[0])/first[0] if first[0] else 0
    t2 = (second[-1]-second[0])/second[0] if second[0] else 0
    shift = (t1 > 0) != (t2 > 0) or abs(t2) > abs(t1) * 1.5 + 0.01
    print(f"[RegimeShift] First half trend {t1*100:.2f}%, second half {t2*100:.2f}% -> {'SHIFT DETECTED - strategy switch karo' if shift else 'No shift'}")
    return shift


def weekend_gap_protection(market, weekday, hour_utc):
    """Forex: Friday 20 UTC ke baad weekend gap risk hai, position close/reduce karo.
    Crypto: weekend par bhi chalta hai. weekday: 0=Mon ... 4=Fri, 5=Sat, 6=Sun."""
    if market != "Forex":
        print(f"[Weekend] {market} weekend par bhi chalta hai - no close needed")
        return False
    if weekday == 4 and hour_utc >= 20:
        print("[Weekend] Forex Friday 20 UTC+ - weekend gap risk, position close/reduce karo")
        return True
    if weekday >= 5:
        print("[Weekend] Forex weekend hai - trading band hai")
        return True
    print("[Weekend] OK - weekday Forex trading allowed")
    return False


def time_exit_check(open_bars, max_bars=20):
    """Trade max_bars se zyada open rahe aur kuch na kare to time exit karo."""
    if open_bars > max_bars:
        print(f"[TimeExit] Trade {open_bars} bars se open hai (> {max_bars}) - time exit karo")
        return True
    print(f"[TimeExit] OK - trade {open_bars} bars se open hai")
    return False


def weekly_ai_review_report(lessons, journal_path="trade_journal.jsonl", out_path="weekly_review.md"):
    """Lessons + journal se weekly review banao: total trades, best/worst strategy, repeat mistakes, recommendations."""
    total_trades = 0
    try:
        with open(journal_path) as f:
            lines = [l for l in f if l.strip()]
            total_trades = len(lines)
    except Exception:
        total_trades = 0
    best = None
    worst = None
    if lessons:
        scored = {k: v.get("profits", 0) - v.get("losses", 0) for k, v in lessons.items()}
        best = max(scored, key=scored.get)
        worst = min(scored, key=scored.get)
    report = []
    report.append("# Weekly AI Review Report\n")
    report.append(f"Total journal trades: {total_trades}\n")
    report.append(f"Best strategy combo: {best}\n")
    report.append(f"Worst strategy combo: {worst}\n")
    report.append("Repeat mistakes: jo combo 2 baar loss de, use block karo - ye learning loop me already hai.\n")
    report.append("Recommendation: worst combo ka size kam rakho, best combo ko dynamic allocation me zyada capital do.\n")
    report.append("Note: Ye demo data se bana report hai, real trades ke baad asli review banega.\n")
    with open(out_path, "w") as f:
        f.write("\n".join(report))
    print(f"[WeeklyReview] Report ban gaya: {out_path} - total trades {total_trades}, best {best}, worst {worst}")
    return out_path
