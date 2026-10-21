# Matt Terminal - Expanded AI Trading Team (Images wali style)

User ne 2026-10-22 ko 7 images bheji jo ek AI trading team ka poora workflow
dikhati hain. Ye file us style ka apna version hai - poster ka copy nahi,
kyunki poster ke exact graphics, prompts aur repos hamare paas nahi hain.
Jo numbers images me example ke taur par dikhe the, wo hamare terminal ke
asli result nahi hain, isliye yahan unko result ke taur par nahi likha gaya hai.

## 7 Specialized Agents - One Workflow

Main team:
1. Research Bot - Market themes, macro, sentiment, news, ideas
2. Strategy Bot - Hypothesis define karo, entry/exit rules, indicators, multiple variants
3. Coding Bot - Strategy ko modular Python code me badlo, backtest, optimize
4. Validation Bot - Out-of-sample testing, robustness, bias detection, performance review
5. Risk Bot - Position sizing, drawdown limits, stress testing, risk approval
6. Portfolio Bot - Capital allocate karo, strategies diversify karo, rebalance rules
7. Execution Bot - Broker API se connect karo (paper pehle), order monitor karo, alerts do

Sub-bots jo inke andar kaam karte hain:
- Data Bot: Price, News, Macro, On-chain, Fundamental, Alternative data collect karo
- Macro Bot: Economic data, market regime
- On-chain Bot: Crypto on-chain flows (jab Crypto trade ho)
- Backtest Bot: Realistic fees, slippage, market hours ke saath backtest
- QA Bot: No look-ahead bias, no data leakage, no survivorship bias, alignment check
- Stress Test Bot: Parameter sensitivity, alag-alag periods, Monte Carlo jaisi checks
- Monitor Bot: Live P&L, slippage, order rejection, strategy drift, alerts
- Paper Bot: Paper trading dry run, real capital ke bina
- Live Bot: Sirf approved hone par, chhote capital se shuru, gradually scale karo

## Complete Workflow - 8 Steps

1. Collect Data - Multiple sources se better research aur signals
2. Research & Analyze - Research agents data analyze karke trading ideas banayein
3. Generate Strategies - Insights ko testable trading hypotheses me badlo
4. Convert to Code - Coding agent strategy ko clean, modular code me badle
5. Backtest & Optimize - Historical data par realistic costs ke saath test karo
6. Validate & Stress Test - Robustness, overfitting, bias checks
7. Risk Assessment - Exposure, drawdown, position size, risk approval
8. Execute & Monitor - Broker ko deploy karo, performance monitor karo

Short workflow: Research -> Develop -> Test -> Validate -> Execute

## Data Inputs (Left) / Outputs (Right)

Inputs: Price Data, News & Sentiment, Macro & On-chain, Fundamental Data, Alternative Data
Outputs: Tested Strategies, Performance Reports, Paper Trading, Live Trading (Approved only), Logs & Alerts

## Markets

Pehle user choice: Crypto (BTC, ETH) + Forex (EURUSD, GBPUSD)
Images me aur bhi dikhe: NIFTY, BANKNIFTY, XAUUSD (Gold)
Ye markets tabhi add honge jab user confirm kare - abhi Crypto/Forex primary hain.

## Execution Rules (Example - code me gate banenge)

- Agar position sizing ya risk limit fail ho to order nahi jayega
- Daily loss limit cross ho to trading ruk jayegi (kill switch)
- Sirf validated aur risk-approved strategy hi execute hogi
- Paper trading pehle, sufficient period ke baad hi live ki baat hogi

## Monitoring Dashboard (Future live version me)

Live P&L, Open Trades, Win Rate, Max Drawdown, Risk Status: Normal
Ye sab tabhi asli honge jab MT5 MCP live connect hoga. Abhi demo preview me ye blank/demo hain.

## Deployment Checklist

- Backtest complete
- Out-of-sample testing passed
- Risk limits configured
- Paper trading sufficient period tak chala
- Live monitoring set hai
- Small capital se shuru, manual review ke baad scale karo
