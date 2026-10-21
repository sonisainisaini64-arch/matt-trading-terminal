# Matt Multi-Agent Trading Terminal - MT5 Demo, Self-Improving

> ⚠️ SABSE IMPORTANT - KABHI MAT HATANA: Self-Improvement / Learning Loop
> User ne 2026-10-22 ko phir se confirm kiya hai ki ye terminal ki sabse
> important cheez hai. Har future version, redesign ya rebuild me learning.py,
> trade_journal.jsonl, lessons.json aur main.py me analyze_trade() ka call
> zaroor rakhna hai. Iske bina terminal adhoora mana jayega.

User ki choice (2026-10-21):
- Platform: **MT5 - Demo account** (user abhi khol raha hai, MCP baad me dega)
- Markets: **Crypto + Forex**
- Mode: **Paper / Demo only** abhi, baad me user chahe to **Real par switch** kar sakega
- Strategy: **Koi fixed strategy nahi** - agents khud research karke market ke
  hisaab se alag strategy chunte hain
- **Sabse main: Self-Improvement** - agents apni trades se seekhte rahein

## MT5 + MCP kaise chalega

1. Tum MT5 me demo account kholo.
2. Tum jo MCP doge, uska endpoint `config.yaml` me `mt5.mcp_endpoint` par aayega.
   Tab `mt5_adapter.py` me MCP wali jagah plug hogi - abhi wo jagah ready hai,
   lekin MCP connected nahi hai, isliye demo prices use ho rahe hain.
3. MT5 password kabhi chat me ya is file me mat likhna. Wo MCP ke secure
   tareeke se hi handle hoga.
4. **Demo -> Real switch:** `config.yaml` me `mode: demo` se `mode: real` tabhi
   badlega jab tum khud kaho. Real mode me bhi bina MCP live aur bina tumhari
   alag approval ke koi order nahi jayega. Ye switch kabhi auto nahi hoga.

## Self-Improvement Loop - kaise seekhte hain agents

Har trade ke baad `learning.py` ye kaam karta hai:
- Trade ko `trade_journal.jsonl` me likhta hai
- Profit ya loss ka simple reason nikalta hai, jaise:
  - Volatile me breakout loss -> size/stop galat tha
  - Trending me mean-reversion loss -> trend ke against trade ki
  - Ranging me trend-following loss -> range me trend chase kiya
  - Regime-strategy match profit -> is combo ko rakho
- Lesson ko `lessons.json` me save karta hai
- Agle run me Strategy Agent blocked combo ko avoid karke alternative chunta hai,
  aur Risk Agent pichhle loss wale combo ka size aadha kar deta hai

Ek loss se hi strategy block nahi hoti - ek hi regime+strategy combo me 2 loss
ho to hi wo blocked hota hai, taaki ek random loss se acchi strategy na chhute.

## 7 Agents

Research -> Strategy (regime ke hisaab se) -> Coding -> Backtesting ->
Validation (Gate) -> Risk (Gate) -> Execution (MT5 Demo / Paper)

## 7 Improvements - Sab Add Ho Gaye (2026-10-22, user ne sab add karne ko kaha)

`improvements.py` me hain aur `main.py` me integrated hain, test run pass hai:
1. Kill Switch - Daily loss -5% ya drawdown 20% par trading ruk jayegi, manual review ke bina dobara nahi chalegi
2. News Filter - High-impact news (CPI, FOMC etc.) ke time us symbol par trade block hogi
3. Multi-Timeframe + ATR - Short aur long trend confirm ho to hi trade, stop volatility ke hisaab se adjust hoga
4. Strategy Versioning + Rollback - Nayi version purani se 2%+ kharab ho to purani par rollback signal
5. Drift Monitor + Alerts - Backtest vs Paper me 3%+ drift ho to alert
6. Correlation Check - EURUSD/GBPUSD aur BTC/ETH jaise correlated pairs par total exposure limit warning
7. Real Cost Backtest - Gross se spread + commission + swap ghata ke net return nikala jata hai

## Additional Improvements - Sab Add Ho Gaye (2026-10-22, user ne sab add karne ko kaha)

8. ATR Trailing SL - user ki cheez, price upar jaye to SL upar, kabhi neeche nahi, profit lock
9. Partial Profit Booking - 1R par aadhi position close, baaki ka SL breakeven par
10. Max Trades Per Day (5) + Session Filter - Forex sirf London/NY session 7-20 UTC, Crypto 24/7
11. Strategy Ranking - lessons se best strategy ranking, recent paper performance ke hisaab se
12. Alerts System - Kill Switch, Drift, run complete par alert log hota hai; Telegram/WhatsApp ke liye bot token/chat ID secure tareeke se dena padega, chat me nahi
13. Spread Widening Filter - Spread normal se 3x zyada ho to trade block

## Advanced Improvements - Sab Add Ho Gaye (2026-10-22, user ne sab add karne ko kaha)

14. Auto Parameter Optimization - Recent win rate dekh ke SMA aur ATR multiplier tune hota hai
15. Walk-Forward + Monte Carlo - Prices ko folds me test karo, 100 random scenarios me mean aur worst 5% nikalo
16. Sentiment Analysis - Symbol ka demo sentiment score (-1 se +1), live me news text se banega
17. Dynamic Capital Allocation - Best strategy ko zyada capital (min 10%, max 40% per combo, total normalize)
18. Regime Shift Detection - Pehle half vs dusre half trend compare, sign change ya vol jump par shift alert
19. Weekend Gap + Time Exit - Forex Friday 20 UTC ke baad / weekend par close, trade 20 bars se zyada open rahe to time exit
20. Weekly AI Review Report - lessons + journal se weekly_review.md banta hai, best/worst strategy aur recommendations ke saath

## Chalane ka tareeka

```bash
python3 main.py
```

## Safety

- Abhi paper/demo mode hi hai. Real money, leverage aur Crypto/Forex me bada
  loss ka risk hota hai. Backtest ya paper profit future profit ki guarantee nahi hai.
- MCP milne ke baad pehle demo par poora test karenge, phir hi real ki baat hogi.
