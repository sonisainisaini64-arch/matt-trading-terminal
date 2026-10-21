"""MT5 Adapter - Demo first, Real only on explicit switch.

Abhi MCP connected nahi hai, isliye ye adapter demo/simulated mode me kaam
karta hai. Jab tum MT5 demo account + MCP doge, tab yahan sirf ye badlega:
  - mcp_endpoint / server config.yaml me bhara jayega
  - get_prices() aur place_order() ke andar MCP tool call lagega
  - mode tab bhi 'demo' hi rahega, jab tak tum real par switch na kaho

Real mode ka guard:
  - mode == 'real' hone par bhi, bina MCP live connection aur bina tumhari
    alag approval ke koi order nahi jayega. Ye adapter tab error dega.
"""


class MT5Adapter:
    def __init__(self, mode="demo", mcp_endpoint=None):
        self.mode = mode
        self.mcp_endpoint = mcp_endpoint
        self.mcp_connected = False  # tum MCP doge tab hi True hoga, test ke baad

    def connect(self):
        if self.mode == "real" and not self.mcp_connected:
            raise RuntimeError(
                "REAL MODE BLOCKED: MT5 MCP live connected nahi hai. "
                "Pehle demo par test karo, phir explicit approval se real switch karo."
            )
        if self.mcp_connected:
            print(f"[MT5] Connected via MCP ({self.mode} account) - endpoint set hai")
        else:
            print(f"[MT5] Demo mode (simulated) - MCP abhi connected nahi hai, "
                  f"isliye demo prices use ho rahe hain. Tum MCP doge tab isko plug karenge.")
        return True

    def get_prices(self, symbol):
        # MCP plug-in point: yahan future me MT5 MCP se live prices aayenge.
        # Abhi agents.py ka demo price data use hota hai.
        return None

    def place_order(self, strategy, risk):
        if self.mode == "real" and not self.mcp_connected:
            raise RuntimeError("REAL MODE BLOCKED: MCP live nahi hai, order nahi bheja gaya.")
        print(f"[MT5] {self.mode.upper()} order logged: {strategy['symbol']} "
              f"{strategy['strategy']['name']} size={risk['size_pct']}% - "
              f"{'REAL order via MCP (future)' if self.mode == 'real' else 'koi real order nahi'}")
        return {"mode": self.mode, "order_sent": self.mode == "real" and self.mcp_connected}
