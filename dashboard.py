"""Matt Trading Terminal - Local Dashboard for Antigravity
===============================================
Antigravity me ye folder kholo, phir run karo:
    python dashboard.py
Phir apne browser me kholo:
    http://127.0.0.1:8000

Ye dashboard SIRF local machine par chalta hai (127.0.0.1).
Internet par kholne ke liye isko public mat karo bina password ke.

Kya dikhata hai:
- Home / Overview, Markets, Agents, Strategies, Backtesting
- Paper Trading / Positions, Trade Journal, Learning / Self-Improvement
- Risk Management, MT5 Connection & Settings
- Weekly Review

Data kahan se aata hai:
- trade_journal.jsonl, lessons.json, strategy_versions.json, alerts.log
- Ye files main.py chalane par banti hain. Pehle ek baar main.py chalao:
    python main.py
- MT5 MCP: ye dashboard sirf ye check karta hai ki MT5 ka internal MCP
  port 127.0.0.1:22346 reachable hai ya nahi. Ye koi API key, password
  ya token NAHI bhejta aur NAHI mangta. Live MT5 data Antigravity ke
  MCP tools se lena hai, uski key Antigravity ki secure MCP settings me
  hi dalni hai, is file me kabhi nahi.

Safety:
- Mode hamesha demo/paper hi hai jab tak user khud real par switch na kahe
  aur MT5 MCP live + demo test pass na ho.
- Self-Improvement (learning.py) kabhi mat hatana - ye sabse important hai.
- Koi real order is dashboard se nahi bheja jata, ye sirf dekhne ke liye hai.
  Trading execution sirf ek jagah se honi chahiye, do terminal ek saath
  ek hi MT5 account par order na bhejein.
"""
import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("MATT_PORT", "8000"))
HOST = os.environ.get("MATT_HOST", "127.0.0.1")


def _read_json(path, default):
    try:
        with open(os.path.join(BASE, path)) as f:
            return json.load(f)
    except Exception:
        return default


def _read_lines(path, limit=50):
    try:
        with open(os.path.join(BASE, path)) as f:
            lines = [l.strip() for l in f if l.strip()]
            return lines[-limit:]
    except Exception:
        return []


def _read_text(path, default="Abhi koi report nahi bani hai. Pehle python main.py chalao."):
    try:
        with open(os.path.join(BASE, path)) as f:
            return f.read()
    except Exception:
        return default


def _mode():
    try:
        with open(os.path.join(BASE, "config.yaml")) as f:
            for line in f:
                if line.strip().startswith("mode:"):
                    return line.split(":", 1)[1].strip().split("#")[0].strip() or "demo"
    except Exception:
        pass
    return "demo"


def _mcp_reachable():
    """Sirf port check, koi credential nahi bheja jata."""
    try:
        s = socket.create_connection(("127.0.0.1", 22346), timeout=1)
        s.close()
        return True
    except Exception:
        return False


def status():
    journal = _read_lines("trade_journal.jsonl")
    lessons = _read_json("lessons.json", {})
    versions = _read_json("strategy_versions.json", [])
    total_pnl = 0.0
    for line in journal:
        try:
            total_pnl += float(json.loads(line).get("pnl_pct", 0) or 0)
        except Exception:
            pass
    return {
        "mode": _mode(),
        "mcp_local_port_reachable": _mcp_reachable(),
        "mcp_note": "Reachable hone ka matlab sirf port khula hai, live data Antigravity MCP tools se lo.",
        "journal_trades": len(journal),
        "total_demo_pnl_pct": round(total_pnl, 2),
        "lessons": lessons,
        "versions": versions,
        "journal": journal,
        "alerts": _read_lines("alerts.log"),
        "weekly_review": _read_text("weekly_review.md"),
    }


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="hi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Matt Trading Terminal - Local Dashboard</title>
<style>
body{font-family:Arial,sans-serif;background:#0f172a;color:#e2e8f0;margin:0;padding:20px}
h1{color:#fff} .card{background:#1e293b;border-radius:12px;padding:16px;margin:12px 0}
.pill{display:inline-block;background:#334155;border-radius:20px;padding:4px 12px;margin:2px}
.good{color:#4ade80} .warn{color:#facc15} .bad{color:#f87171}
pre{white-space:pre-wrap;word-break:break-word;background:#0b1220;padding:12px;border-radius:8px}
a{color:#7dd3fc}
button{background:#2563eb;color:#fff;border:0;padding:8px 14px;border-radius:8px;cursor:pointer}
.tabs button{background:#334155;margin:2px} .tabs button.active{background:#2563eb}
section{display:none} section.active{display:block}
</style></head><body>
<h1>Matt Trading Terminal</h1>
<p>Local dashboard - sirf is machine par. Mode: <b>{mode}</b> | MT5 MCP local port reachable: <b>{mcp}</b></p>
<p class="warn">Ye dashboard sirf dekhne ke liye hai. Isse koi real order nahi jata. Real par switch sirf tumhare explicit approval + demo test ke baad.</p>
<div class="tabs">
<button onclick="show(0)" class="active">Home</button><button onclick="show(1)">Markets</button>
<button onclick="show(2)">Agents</button><button onclick="show(3)">Strategies</button>
<button onclick="show(4)">Backtesting</button><button onclick="show(5)">Paper Trading</button>
<button onclick="show(6)">Trade Journal</button><button onclick="show(7)">Learning</button>
<button onclick="show(8)">Risk</button><button onclick="show(9)">MT5 Connection</button>
<button onclick="show(10)">Weekly Review</button>
</div>

<section class="active"><div class="card"><h2>1. Home / Overview</h2>
<p>Paper balance (demo): $10,000 | Journal trades: {trades} | Total demo PnL: {pnl}%</p>
<p>Markets: <span class="pill">Crypto: BTCUSDT</span> <span class="pill">Crypto: ETHUSDT</span> <span class="pill">Forex: EURUSD</span> <span class="pill">Forex: GBPUSD</span></p>
<p>Agents: Research, Strategy, Coding, Backtesting, Validation, Risk, Execution + Data, Macro, On-chain, QA, Stress Test, Monitor, Paper, Live</p>
</div></section>

<section><div class="card"><h2>2. Markets</h2><p>BTCUSDT, ETHUSDT, EURUSD, GBPUSD - Crypto + Forex, paper/demo mode.</p>
<p>Live price ke liye Antigravity me MT5 MCP connect karo, tab yahan live data aayega. Abhi demo data dikh raha hai.</p></div></section>

<section><div class="card"><h2>3. Agents</h2><p>Research -&gt; Strategy -&gt; Coding -&gt; Backtesting -&gt; Validation -&gt; Risk -&gt; Execution</p>
<p>Plus sub-bots: Data, Macro, On-chain, QA, Stress Test, Monitor, Paper, Live (design EXPANDED_TEAM.md me hai).</p></div></section>

<section><div class="card"><h2>4. Strategies</h2><p>Trend Following, Mean Reversion, Breakout - market regime ke hisaab se agents khud chunte hain. Koi fixed strategy nahi hai.</p></div></section>

<section><div class="card"><h2>5. Backtesting</h2><pre>{versions}</pre><p>Real cost (spread + commission + swap) ke baad net return nikala jata hai. Walk-forward + Monte Carlo bhi improvements.py me hai.</p></div></section>

<section><div class="card"><h2>6. Paper Trading / Positions</h2><p>Abhi paper/demo mode hai. Koi real order nahi gaya hai.</p><p>Improvements: Kill Switch, News Filter, Multi-Timeframe + ATR, ATR Trailing SL, Partial Profit, Daily Limit, Session Filter, Correlation, Spread Filter, Dynamic Allocation, Regime Shift.</p></div></section>

<section><div class="card"><h2>7. Trade Journal</h2><pre>{journal}</pre></div></section>

<section><div class="card"><h2>8. Learning / Self-Improvement - SABSE IMPORTANT</h2><p>Har trade ka profit/loss kyun hua, ye lesson me save hota hai. Ek combo me 2 loss ho to wo block hota hai, loss wale combo ka size aadha hota hai.</p><pre>{lessons}</pre></div></section>

<section><div class="card"><h2>9. Risk Management</h2><p>Risk/trade 1%, max exposure 20%, Kill Switch daily loss -5% / drawdown 20% par trading ruk jayegi. ATR Trailing SL profit lock karta hai.</p><h3>Alerts</h3><pre>{alerts}</pre></div></section>

<section><div class="card"><h2>10. MT5 Connection &amp; Settings</h2><p>Mode: {mode}</p><p>MT5 MCP local port 22346 reachable: {mcp}</p><p>{mcp_note}</p><p>MT5 password, API key ya token is dashboard me, is file me ya chat me mat dalna. Sirf Antigravity ki secure MCP settings me dalna, aur purani key ko Generate se naya kar lena.</p></div></section>

<section><div class="card"><h2>Weekly Review</h2><pre>{weekly}</pre></div></section>

<p><button onclick="location.reload()">Refresh</button> &nbsp; <a href="/api/status">API Status (JSON)</a></p>
<script>
function show(i){document.querySelectorAll('section').forEach((s,j)=>s.classList.toggle('active',j===i));document.querySelectorAll('.tabs button').forEach((b,j)=>b.classList.toggle('active',j===i));}
</script></body></html>
"""


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/api/status", "/api"):
            data = json.dumps(status(), indent=2).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        st = status()
        # .format() use nahi kar rahe, kyunki CSS me { } hote hain - sirf placeholders replace karo
        html = HTML_TEMPLATE
        html = html.replace("{mode}", _esc(st["mode"]))
        html = html.replace("{mcp}", "YES" if st["mcp_local_port_reachable"] else "NO - MT5 MCP abhi nahi chal raha ya port band hai")
        html = html.replace("{trades}", str(st["journal_trades"]))
        html = html.replace("{pnl}", str(st["total_demo_pnl_pct"]))
        html = html.replace("{versions}", _esc(json.dumps(st["versions"], indent=2)))
        html = html.replace("{journal}", _esc("\n".join(st["journal"])))
        html = html.replace("{lessons}", _esc(json.dumps(st["lessons"], indent=2)))
        html = html.replace("{alerts}", _esc("\n".join(st["alerts"])))
        html = html.replace("{mcp_note}", _esc(st["mcp_note"]))
        html = html.replace("{weekly}", _esc(st["weekly_review"]))
        html = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Matt Dashboard chal raha hai: http://{HOST}:{PORT}")
    print("Browser me ye link kholo. Band karne ke liye Ctrl+C dabao.")
    print("NOTE: Ye sirf local link hai. Internet par kholna ho to password + restricted IP ke bina mat kholna.")
    HTTPServer((HOST, PORT), Handler).serve_forever()
