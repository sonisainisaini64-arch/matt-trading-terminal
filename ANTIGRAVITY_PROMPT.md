# Antigravity me paste karne wala prompt - copy karo, poora paste karo

```
Mujhe is folder me Matt Trading Terminal ka local dashboard banana hai.
Ye folder me pehle se main.py, agents.py, learning.py, improvements.py,
mt5_adapter.py, config.yaml aur dashboard.py maujood hai. Inko dobara
mat likhna, inhi ko base banao.

KAAM:
1. Sabse pehle is folder ke code ko padho aur samjho. Self-Improvement
   (learning.py, trade_journal.jsonl, lessons.json, main.py me
   analyze_trade() ka call) KABHI mat hatana - ye sabse important hai.
2. MT5 ka MCP add karo. MT5 isi machine par chal raha hai, uska internal
   MCP server Options > MCP tab me Enable hai, address
   http://127.0.0.1:22346/mcp hai. API key main tumhe Antigravity ki
   secure MCP settings me dunga, tum use code me, chat me ya screenshot
   me kabhi mat likhna, aur purani key ko Generate se naya karne ko bolo
   agar wo kahin share hui ho.
3. dashboard.py ko aisa banao ki browser me http://127.0.0.1:8000 par
   ye sections dikhein, click karke khulne wale tabs ke saath:
   Home, Markets, Agents, Strategies, Backtesting, Paper Trading,
   Trade Journal, Learning / Self-Improvement, Risk Management,
   MT5 Connection & Settings, Weekly Review.
4. Dashboard sirf dekhne ke liye hai. Is dashboard se koi real order
   mat bhejna. Trading execution sirf ek jagah se hogi.
   Mode hamesha demo/paper hi rakho, jab tak main khud real par switch
   na kahun aur demo test pass na ho.
5. Jab MT5 MCP live ho jaye to dashboard me live price, account balance
   aur positions MT5 MCP se dikhao. MCP na mile to demo data dikhao aur
   saaf likho ki "MCP not connected, demo data".
6. Dashboard chalane ke baad mujhe local link do aur batao ki kaunsi
   file me kya change kiya hai. Local link ko internet par public mat
   karo bina password ke.
7. Markets: Crypto + Forex (BTCUSDT, ETHUSDT, EURUSD, GBPUSD).
   Improvements jo pehle se hain unko mat hatana: Kill Switch, News Filter,
   Multi-Timeframe + ATR, ATR Trailing SL, Partial Profit, Daily Limit,
   Session Filter, Correlation, Spread Filter, Dynamic Allocation,
   Regime Shift, Walk-Forward + Monte Carlo, Sentiment, Weekly Review.
```

## Antigravity me steps
1. Antigravity kholo > is folder ko Open karo.
2. Upar wala prompt paste karo aur Run karo.
3. Antigravity ki MCP settings me MT5 MCP add karo (endpoint upar diya hai,
   API key secure settings me hi dalo).
4. Terminal me chalao:
   - `python main.py`  (pehle ek baar, taaki journal/lessons ban jayein)
   - `python dashboard.py` (dashboard ke liye)
5. Browser me kholo: http://127.0.0.1:8000
6. Agar dashboard me "MCP not connected" dikhe to MT5 me Options > MCP
   me Enable internal server tick hai ya nahi, aur MT5 chal raha hai ya
   nahi, ye check karo. MT5 band ho to MCP bhi band hoga.
