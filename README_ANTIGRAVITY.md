# Matt Trading Terminal - Antigravity Version

Ye folder Muse se banaye hue terminal ka full code hai, Antigravity me
dalne ke liye ready. Isme pehle se sab kuch hai, Antigravity ko sirf
dashboard ko MT5 MCP se jodna aur local link par chalana hai.

## Files
- main.py - terminal ka main run, 7 agents + sab improvements
- agents.py - Research, Strategy, Coding, Backtesting, Validation, Risk, Execution
- learning.py - Self-Improvement, SABSE IMPORTANT, kabhi mat hatana
- improvements.py - Kill Switch se leke Weekly Review tak sab improvements
- mt5_adapter.py - MT5 demo/paper adapter, real mode blocked bina MCP + approval ke
- dashboard.py - local dashboard, http://127.0.0.1:8000, sirf dekhne ke liye
- config.yaml - mode: demo, real kabhi auto nahi hoga
- ANTIGRAVITY_PROMPT.md - Antigravity me paste karne wala ready prompt
- mcp_template.json - MCP config ka TEMPLATE, isme koi asli key nahi hai
- run_windows.bat / run.sh - chalane ke liye scripts

## Chalane ka tareeka (Windows, MT5 wali machine par)
1. Antigravity me ye folder kholo.
2. ANTIGRAVITY_PROMPT.md wala prompt paste karo.
3. Antigravity ki secure MCP settings me MT5 MCP add karo.
   API key / password kabhi is folder ki file me, chat me ya screenshot me mat dalna.
4. Phir:
   ```
   python main.py
   python dashboard.py
   ```
   Browser me: http://127.0.0.1:8000

## Safety - zaroor padhna
- Abhi paper/demo mode hi hai. Backtest ya paper profit future profit ki guarantee nahi hai.
- Real par switch sirf tumhare explicit approval + demo test pass hone ke baad.
- Do terminal ek saath ek hi MT5 account par order na bhejein, warna double trade hogi.
- Dashboard ko bina password ke internet par public mat karo.
- Purani API key jo kahin share hui ho, use MT5 me Generate se naya kar lo.
