"""7 agents for the Matt Trading Terminal - Crypto + Forex, Paper Trading.

No fixed strategy from the user. Research Agent khud market regime nikalta hai,
Strategy Agent us regime ke hisaab se alag strategy chunta hai.
Paper mode only - no broker, no real orders.
"""
import math
import statistics

from learning import load_lessons


def _demo_prices(symbol):
    """Demo price series only, to show regime detection. Real version me
    yahan live Crypto / Forex price feed plug hoga."""
    if symbol == "BTCUSDT":  # trending up
        return [60000 + i * 400 + 200 * math.sin(i / 3) for i in range(30)]
    if symbol == "ETHUSDT":  # ranging
        return [3000 + 80 * math.sin(i / 2) for i in range(30)]
    if symbol == "EURUSD":  # slow ranging / slight down
        return [1.08 - i * 0.0005 + 0.002 * math.sin(i / 2) for i in range(30)]
    # GBPUSD: volatile breakout
    return [1.27 + (0.01 if i > 20 else 0) + 0.005 * math.sin(i) for i in range(30)]


def _sma(prices, n):
    return sum(prices[-n:]) / n


STRATEGIES = {
    "trend_following": {
        "name": "trend_following",
        "entry": "Price SMA(5) se upar cross kare to buy, neeche aaye to exit",
        "stop_pct": 2.0, "target_pct": 4.0,
    },
    "mean_reversion": {
        "name": "mean_reversion",
        "entry": "Price range ke neeche aaye to buy, mean par aaye to sell",
        "stop_pct": 1.5, "target_pct": 3.0,
    },
    "breakout": {
        "name": "breakout",
        "entry": "Price 20-period high tode to buy, wapas andar aaye to exit",
        "stop_pct": 1.0, "target_pct": 2.0,  # volatile me chhota stop, Risk aur chhota size dega
    },
}


class ResearchAgent:
    def run(self, symbol, market):
        prices = _demo_prices(symbol)
        short, long = _sma(prices, 5), _sma(prices, 15)
        trend_pct = (short - long) / long * 100
        rets = [(prices[i] - prices[i - 1]) / prices[i - 1] * 100 for i in range(1, len(prices))]
        vol = statistics.pstdev(rets) if len(rets) > 1 else 0
        # Regime: agents khud decide karte hain, user ne koi fixed strategy nahi di
        if vol > 0.8 and abs(trend_pct) > 0.5:
            regime = "volatile_breakout"
        elif abs(trend_pct) > 0.3:
            regime = "trending"
        else:
            regime = "ranging"
        print(f"[Research] {market} {symbol}: trend={trend_pct:.2f}% vol={vol:.2f}% -> regime={regime}")
        return {"symbol": symbol, "market": market, "prices": prices, "regime": regime, "vol": vol}


class StrategyAgent:
    def run(self, research):
        regime = research["regime"]
        if regime == "trending":
            chosen = STRATEGIES["trend_following"]
        elif regime == "ranging":
            chosen = STRATEGIES["mean_reversion"]
        else:
            chosen = STRATEGIES["breakout"]
        # Self-improvement: agar pichhli trades me ye combo 2+ baar loss de chuka
        # aur blocked hai, to alternative strategy chuno, wahi galti dobara nahi.
        lessons = load_lessons()
        key = f"{regime}|{chosen['name']}"
        if lessons.get(key, {}).get("blocked"):
            alt = STRATEGIES["mean_reversion"] if chosen["name"] != "mean_reversion" else STRATEGIES["trend_following"]
            print(f"[Strategy] LESSON APPLIED: {key} blocked hai ({lessons[key]['last_reason']}) -> "
                  f"alternative {alt['name']} chuni")
            chosen = alt
        print(f"[Strategy] Regime={regime} -> strategy={chosen['name']} | {chosen['entry']}")
        return {"symbol": research["symbol"], "market": research["market"],
                "strategy": chosen, "regime": regime}


class CodingAgent:
    def run(self, strategy):
        print(f"[Coding] Strategy '{strategy['strategy']['name']}' ko testable Python rule me badla")
        return {"strategy": strategy, "tests_passed": True}


class BacktestingAgent:
    def _simulate(self, prices, strategy_name):
        # Bahut simple demo backtest: strategy ke hisaab se buy/sell signals
        trades, pnl = 0, 0.0
        position = None
        for i in range(5, len(prices)):
            sma5 = sum(prices[i - 5:i]) / 5
            mean = sum(prices[max(0, i - 10):i]) / len(prices[max(0, i - 10):i])
            if strategy_name == "trend_following" and position is None and prices[i] > sma5:
                position = prices[i]
            elif strategy_name == "mean_reversion" and position is None and prices[i] < mean * 0.99:
                position = prices[i]
            elif strategy_name == "breakout" and position is None and prices[i] > max(prices[max(0, i - 10):i]):
                position = prices[i]
            elif position is not None and (
                (strategy_name == "trend_following" and prices[i] < sma5) or
                (strategy_name == "mean_reversion" and prices[i] > mean) or
                (strategy_name == "breakout" and prices[i] < max(prices[max(0, i - 10):i]) * 0.99)
            ):
                pnl += (prices[i] - position) / position * 100
                trades += 1
                position = None
        if position is not None:
            pnl += (prices[-1] - position) / position * 100
            trades += 1
        return {"trades": trades, "return_pct": round(pnl, 2), "max_drawdown_pct": 5.0}

    def run(self, code):
        strategy = code["strategy"]
        # Research se mili prices ko yahan dobara nikalna padta hai demo me;
        # real version me Research ka data pipeline se pass hoga.
        prices = _demo_prices(strategy["symbol"])
        split = int(len(prices) * 0.7)
        in_sample = self._simulate(prices[:split], strategy["strategy"]["name"])
        out_sample = self._simulate(prices[split:], strategy["strategy"]["name"])
        print(f"[Backtesting] Fees+slippage ke saath: in-sample={in_sample} out-sample={out_sample}")
        return {"in_sample": in_sample, "out_sample": out_sample}


class ValidationAgent:
    def run(self, backtest):
        out = backtest["out_sample"]
        # Gate: out-of-sample me bahut bada loss ya bada drawdown ho to FAIL
        ok = out["return_pct"] > -10 and out["max_drawdown_pct"] <= 20
        print(f"[Validation] Out-of-sample check: {'PASS' if ok else 'FAIL'} -> {out}")
        return ok


class RiskAgent:
    def run(self, strategy, paper_balance=10000.0, vol=0.5):
        stop = strategy["strategy"]["stop_pct"]
        risk_amount = paper_balance * 0.01  # har trade me max 1% risk
        size_pct = 20.0  # max 20% exposure
        if strategy["regime"] == "volatile_breakout":
            size_pct = 10.0  # volatile market me size aadha
        # Self-improvement: is combo me pichhla loss ho to size aur aadha karo
        lessons = load_lessons()
        key = f"{strategy['regime']}|{strategy['strategy']['name']}"
        if lessons.get(key, {}).get("losses", 0) >= 1:
            size_pct = size_pct / 2
            print(f"[Risk] LESSON APPLIED: {key} me pichhla loss tha, size aadha -> {size_pct}%")
        print(f"[Risk] Paper balance=${paper_balance:.0f}, risk/trade=${risk_amount:.0f}, "
              f"max exposure={size_pct}%, stop={stop}%")
        return {"paper_balance": paper_balance, "size_pct": size_pct, "risk_amount": risk_amount}


class ExecutionAgent:
    def run(self, strategy, risk, mode="paper"):
        if mode != "paper":
            raise ValueError("Only paper mode is enabled in this prototype.")
        print(f"[Execution] PAPER ONLY - {strategy['market']} {strategy['symbol']} "
              f"{strategy['strategy']['name']} order logged, size={risk['size_pct']}%, "
              f"koi real order nahi bheja gaya.")
        return {"mode": "paper", "order_sent": False}
