# ExampleForGIT
i used this repo to practice the features in GIT only.

# 
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
