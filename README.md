# 1). ExampleForGIT
i used this repo to practice the features in GIT only.

# 2). Original prompt
Original prompt
[rule] you are expert in python and Node.JS
[context] this is the requirement.
1. Need the python code to plot the in the futuristic graphs and you please make the suitable dataset.
2. After you complete the item.1. pls transfer the futuristic graphs to make the Website by Node.JS.
3. you are free to design the code, dataset and the graphic design.
[task] pls read the [context] and make it.
[format] Pls use python and Node.JS as long as possible. it is ok if need to use another language code.


# 3). Copilot
Builds a full-stack futuristic data dashboard from scratch: Python generates neon-styled charts from synthetic datasets; Node.js/Express serves them via an interactive SPA.

Python (python/generate_charts.py)
Synthesizes 4 forward-looking datasets (2020–2060) saved as CSVs in python/data/:
Tech Adoption — sigmoid-curve forecasts for Quantum Computing, BCI, Fusion Energy, AGI, Nano-Medicine
Space Economy — stacked revenue projections by sector (USD Billion)
Energy Transition — normalised global energy mix share by source
AI vs Human — benchmark scores across 11 AI milestones
Renders all charts with Matplotlib using a dark #050d1a background + neon cyan/magenta/green/yellow palette; outputs PNGs to web/public/images/
Writes web/charts_meta.json consumed by the server
Node.js (web/)
server.js: Express static server + /api/charts JSON endpoint; rate-limited (100 req/15 min); fails fast with a clear message if charts_meta.json is missing
Frontend (public/): animated starfield canvas, live UTC clock, category filter bar, responsive 2-column card grid, click-to-expand lightbox (Esc / backdrop-click to dismiss)
# One-time chart generation
python3 python/generate_charts.py

# Start dashboard
cd web && npm install && npm start  # → http://localhost:3000
Screenshots
Dashboard — full view
Dashboard full view

Lightbox — expanded chart
<img width="1280" height="1392" alt="image" src="https://github.com/user-attachments/assets/7bd56173-54f9-42d6-9126-f55e8b989050" />

Lightbox expanded
<img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/623876d2-51cd-4bcd-83ba-74cb70e66417" />


# 4). Final result
🚀 NEXUS Futuristic Data Dashboard
What was implemented
Python (python/)
generate_charts.py — single script that:

Creates 4 synthetic futuristic datasets (saved as CSV in python/data/):

tech_adoption.csv — sigmoid-curve adoption forecasts for Quantum Computing, BCI, Fusion Energy, AGI, Nano-Medicine (2025–2060)
space_economy.csv — stacked revenue by sector in USD Billion (2025–2055)
energy_transition.csv — normalised share of global energy by source (2020–2060)
ai_performance.csv — AI vs Human benchmark scores across 11 milestones
Plots 4 neon-on-dark futuristic charts using Matplotlib (#050d1a background, neon cyan/magenta/green/yellow palette) and saves PNGs to web/public/images/

Writes web/charts_meta.json (consumed by the Node.js server)

Node.js (web/)
File	Role
server.js	Express server — static assets + /api/charts JSON endpoint (rate-limited, startup error-handled)
public/index.html	SPA shell
public/css/style.css	Futuristic dark/neon CSS (responsive)
public/js/main.js	Animated starfield, live UTC clock, filter bar, card grid, click-to-expand lightbox
To run locally
bash
# 1. Generate charts (one-time)
python3 python/generate_charts.py

# 2. Start the website
cd web && npm install && npm start
# → http://localhost:3000
Security
Rate-limiting applied to /api/ (100 req / 15 min) — CodeQL 0 alerts
HTML output is entity-escaped before DOM insertion to prevent XSS
