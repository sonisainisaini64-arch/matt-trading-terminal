# Cloud Windows VPS Setup - MT5 + Matt Terminal

User choice (2026-10-21): Cloud Windows VPS par MT5 chalana, local PC ke bajay.

## 1. VPS chuno - minimum spec
- OS: Windows Server (licensed, provider se)
- CPU: 2 cores minimum, 4 cores behtar agar 3+ terminals / agents chalane hain
- RAM: 4 GB minimum, 8 GB behtar
- Disk: 70 GB SSD/NVMe minimum
- IP: 1 dedicated IP
- Location: Broker ke server ke sabse paas wali location chuno (London, New York,
  Amsterdam, Singapore, ya Mumbai/Noida agar broker India ke paas hai)
- Uptime: 99.9% ya zyada

## 2. VPS milne ke baad steps (order me)
1. RDP se VPS me login karo, Windows update karo.
2. Apne broker ka MT5 download karke install karo, demo account se login karo.
   Pehle demo hi, real tabhi jab demo test pass ho.
3. MT5 ko auto-start par lagao, taaki VPS reboot ke baad bhi terminal khud khul jaye.
4. MCP servers install karo - metaeditor, terminal, marketdata wale.
   Har MCP ka naya auth token banao. Purane tokens jo chat me aa chuke hain,
   unko dobara use mat karna - unko rotate karo.
5. Firewall me sirf MCP ports kholo, aur sirf zaroori IP / auth ke saath.
   MCP ko bina auth ke internet par mat kholo.
6. Muse ko VPS ka public IP / MCP endpoint + naya auth secure tareeke se do.
   Password / token chat me mat bhejo.
7. Pehle demo par pura test karo: price feed, paper order, learning loop.
   Sab pass ho to hi real switch ki baat hogi, aur wo bhi alag approval se.

## 3. Kya Muse ko chahiye jab VPS ready ho
- VPS provider + plan + location
- VPS ka public IP (sirf tab jab tum chaho, secure tareeke se)
- MT5 demo account ka server naam (password nahi)
- MCP endpoints aur naya auth (secure link se, chat me nahi)
- Broker ka naam aur uske server ki location (latency ke liye)

## 4. Kya abhi nahi karna
- VPS order / payment Muse se bina tumhari approval ke nahi hoga.
- Real account par trade bina demo test aur bina alag approval ke nahi hoga.
- Purane tokens dobara use nahi karne.
