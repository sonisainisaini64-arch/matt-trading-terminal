"""Self-Improvement / Learning Loop - sabse main part.

Har trade ke baad Learning Agent ye likhta hai:
  - Trade kya thi: symbol, market, regime, strategy
  - Result kya tha: profit ya loss, kitna %
  - Kyun hua (simple, explainable reason, koi black-box nahi):
      * Loss + volatile regime -> breakout/volatility me size/stop galat tha
      * Loss + trending me mean_reversion -> trend ke against trade ki
      * Loss + ranging me trend_following -> range me trend chase kiya
      * Profit + regime-strategy match -> ye combo kaam karta hai, isko rakho
  - Agli baar kya badlega: size kam, stop badal, ya us combo ko block karo

Ye lessons.json aur trade_journal.jsonl me save hote hain, taaki agle run me
Strategy aur Risk agent unko padh ke wahi galti dobara na karein.
Loss ko chhupana nahi, usse seekhna hi is loop ka kaam hai.
"""
import json
import os

JOURNAL = "trade_journal.jsonl"
LESSONS = "lessons.json"


def load_lessons():
    if not os.path.exists(LESSONS):
        return {}
    try:
        with open(LESSONS) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_lessons(lessons):
    with open(LESSONS, "w") as f:
        json.dump(lessons, f, indent=2)


def analyze_trade(trade):
    """trade = {symbol, market, regime, strategy, pnl_pct, trades}
    Returns lesson dict and saves it."""
    symbol, regime, strategy = trade["symbol"], trade["regime"], trade["strategy"]
    pnl = trade["pnl_pct"]
    key = f"{regime}|{strategy}"

    # 1. Journal me har trade likho
    with open(JOURNAL, "a") as f:
        f.write(json.dumps(trade) + "\n")

    # 2. Reason nikalo
    if pnl < -1:
        if regime == "volatile_breakout":
            reason = "Volatile market me breakout trade loss me gaya - size/stop bahut bada tha"
            action = "volatile me size aadha karo, stop tight rakho"
        elif regime == "trending" and strategy == "mean_reversion":
            reason = "Trending market me trend ke against mean-reversion trade ki - isliye loss"
            action = "Trending me mean_reversion avoid karo"
        elif regime == "ranging" and strategy == "trend_following":
            reason = "Ranging market me trend chase kiya - range me trend nahi chalta"
            action = "Ranging me trend_following avoid karo"
        else:
            reason = "Strategy ne is regime me loss diya - size kam karo aur dobara test karo"
            action = "Size kam karo, phir se backtest karo"
        outcome = "loss"
    elif pnl > 1:
        reason = "Regime aur strategy ka match sahi tha - is combo ne profit diya"
        action = "Is combo ko rakho, size normal rakho"
        outcome = "profit"
    else:
        reason = "Trade me koi clear edge nahi dikha - aur trades ka data chahiye"
        action = "Koi badlav nahi, aur data jama karo"
        outcome = "neutral"

    lessons = load_lessons()
    entry = lessons.get(key, {"losses": 0, "profits": 0, "last_reason": "", "last_action": ""})
    if outcome == "loss":
        entry["losses"] += 1
    elif outcome == "profit":
        entry["profits"] += 1
    entry["last_reason"] = reason
    entry["last_action"] = action
    # 2 loss ek hi combo me ho to us combo ko block karne ka signal
    entry["blocked"] = entry["losses"] >= 2 and entry["losses"] > entry["profits"] + 1
    lessons[key] = entry
    _save_lessons(lessons)

    lesson = {"key": key, "outcome": outcome, "pnl_pct": pnl,
              "reason": reason, "action": action, "blocked": entry["blocked"]}
    print(f"[Learning] {symbol} {strategy} ({regime}) pnl={pnl}% -> {outcome.upper()}")
    print(f"[Learning] Kyun: {reason}")
    print(f"[Learning] Agli baar: {action} | Blocked={entry['blocked']}")
    return lesson
