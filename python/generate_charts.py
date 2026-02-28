"""
Futuristic Data Visualization Script
Generates four futuristic-themed charts and saves them as PNG images
for embedding in the Node.js website.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
from matplotlib.gridspec import GridSpec

# ── Output directory ────────────────────────────────────────────────────────
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "web", "public", "images")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ── Colour palette (neon on dark) ────────────────────────────────────────────
BG = "#050d1a"
GRID = "#0a1f3a"
NEON_CYAN = "#00eeff"
NEON_MAGENTA = "#ff00cc"
NEON_GREEN = "#00ff88"
NEON_YELLOW = "#ffee00"
NEON_ORANGE = "#ff6600"
NEON_BLUE = "#4466ff"
TEXT = "#c0d8f0"
ACCENT = "#ffffff"

PALETTE = [NEON_CYAN, NEON_MAGENTA, NEON_GREEN, NEON_YELLOW, NEON_ORANGE, NEON_BLUE]

def apply_futuristic_style(fig, ax_list):
    """Apply dark futuristic styling to every axes in ax_list."""
    fig.patch.set_facecolor(BG)
    for ax in ax_list:
        ax.set_facecolor(GRID)
        ax.tick_params(colors=TEXT, labelsize=9)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.title.set_color(ACCENT)
        for spine in ax.spines.values():
            spine.set_edgecolor(NEON_CYAN)
            spine.set_linewidth(0.8)
        ax.grid(color=NEON_CYAN, linestyle="--", linewidth=0.3, alpha=0.35)


# ════════════════════════════════════════════════════════════════════════════
#  CHART 1 – Technology Adoption Forecast 2025-2060
# ════════════════════════════════════════════════════════════════════════════
def chart_tech_adoption():
    years = np.arange(2025, 2061)
    rng = np.random.default_rng(42)

    def sigmoid(x, L, k, x0):
        return L / (1 + np.exp(-k * (x - x0)))

    techs = {
        "Quantum Computing": sigmoid(years, 95, 0.25, 2040) + rng.normal(0, 1.2, len(years)),
        "Brain-Computer Interface": sigmoid(years, 80, 0.22, 2045) + rng.normal(0, 1.0, len(years)),
        "Fusion Energy": sigmoid(years, 70, 0.20, 2048) + rng.normal(0, 1.0, len(years)),
        "AGI Systems": sigmoid(years, 60, 0.30, 2038) + rng.normal(0, 0.8, len(years)),
        "Nano-Medicine": sigmoid(years, 88, 0.24, 2042) + rng.normal(0, 1.1, len(years)),
    }
    df = pd.DataFrame(techs, index=years)
    df = df.clip(lower=0, upper=100)
    df.to_csv(os.path.join(DATA_DIR, "tech_adoption.csv"))

    fig, ax = plt.subplots(figsize=(10, 5.5))
    apply_futuristic_style(fig, [ax])

    for (col, color) in zip(df.columns, PALETTE):
        ax.plot(years, df[col], color=color, linewidth=2, label=col)
        ax.fill_between(years, df[col], alpha=0.08, color=color)

    ax.set_title("TECHNOLOGY ADOPTION FORECAST  2025 – 2060", fontsize=13,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Adoption Rate (%)", fontsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, 105)
    legend = ax.legend(fontsize=8, framealpha=0, labelcolor=TEXT,
                       loc="upper left", ncol=1)
    for line in legend.get_lines():
        line.set_linewidth(2)

    fig.tight_layout(pad=1.5)
    path = os.path.join(OUT_DIR, "chart_tech_adoption.png")
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    print(f"  ✔ Saved {path}")


# ════════════════════════════════════════════════════════════════════════════
#  CHART 2 – Space Economy Revenue by Sector (2025-2055)
# ════════════════════════════════════════════════════════════════════════════
def chart_space_economy():
    years = np.arange(2025, 2056, 5)
    sectors = {
        "Satellite Services": [200, 280, 380, 510, 680, 870, 1100],
        "Launch & Transport":  [30,  55,  95,  160, 250, 380, 560],
        "Space Tourism":       [2,   8,   22,  55,  130, 270, 500],
        "Asteroid Mining":     [0,   1,   5,   18,  60,  180, 450],
        "Lunar Economy":       [0,   0,   3,   12,  40,  120, 320],
        "Space Manufacturing": [1,   4,   14,  40,  100, 220, 440],
    }
    df = pd.DataFrame(sectors, index=years)
    df.to_csv(os.path.join(DATA_DIR, "space_economy.csv"))

    fig, ax = plt.subplots(figsize=(10, 5.5))
    apply_futuristic_style(fig, [ax])

    bottom = np.zeros(len(years))
    for (col, color) in zip(df.columns, PALETTE):
        bars = ax.bar(years, df[col], bottom=bottom, color=color,
                      alpha=0.85, label=col, width=3.5, edgecolor=BG, linewidth=0.4)
        bottom += df[col].values

    ax.set_title("SPACE ECONOMY REVENUE BY SECTOR  (USD Billion)", fontsize=13,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Revenue (USD Billion)", fontsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:,.0f}B"))
    ax.set_xlim(2021, 2059)
    legend = ax.legend(fontsize=8, framealpha=0, labelcolor=TEXT, loc="upper left")
    for patch in legend.get_patches():
        patch.set_linewidth(0)

    fig.tight_layout(pad=1.5)
    path = os.path.join(OUT_DIR, "chart_space_economy.png")
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    print(f"  ✔ Saved {path}")


# ════════════════════════════════════════════════════════════════════════════
#  CHART 3 – Global Energy Transition 2020-2060
# ════════════════════════════════════════════════════════════════════════════
def chart_energy_transition():
    years = np.arange(2020, 2061)
    rng = np.random.default_rng(7)

    def decay(start, end, k):
        return start * np.exp(-k * (years - 2020)) + end * (1 - np.exp(-k * (years - 2020)))

    sources = {
        "Fossil Fuels":    decay(80, 8, 0.055) + rng.normal(0, 0.5, len(years)),
        "Solar":           decay(5, 38, 0.065) + rng.normal(0, 0.3, len(years)),
        "Wind":            decay(6, 28, 0.058) + rng.normal(0, 0.3, len(years)),
        "Nuclear Fusion":  decay(0, 12, 0.090) + rng.normal(0, 0.2, len(years)),
        "Hydrogen":        decay(1, 10, 0.070) + rng.normal(0, 0.2, len(years)),
        "Other Renewables":decay(8, 4, -0.02) + rng.normal(0, 0.2, len(years)),
    }
    df = pd.DataFrame(sources, index=years).clip(lower=0)
    # normalise rows to 100 %
    df = df.div(df.sum(axis=1), axis=0) * 100
    df.to_csv(os.path.join(DATA_DIR, "energy_transition.csv"))

    fig, ax = plt.subplots(figsize=(10, 5.5))
    apply_futuristic_style(fig, [ax])

    ax.stackplot(years, [df[c] for c in df.columns],
                 labels=df.columns, colors=PALETTE, alpha=0.78)
    ax.set_title("GLOBAL ENERGY MIX TRANSITION  2020 – 2060  (%)", fontsize=13,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Share of Total Energy (%)", fontsize=10)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, 100)
    legend = ax.legend(fontsize=8, framealpha=0, labelcolor=TEXT,
                       loc="upper right", ncol=2)

    fig.tight_layout(pad=1.5)
    path = os.path.join(OUT_DIR, "chart_energy_transition.png")
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    print(f"  ✔ Saved {path}")


# ════════════════════════════════════════════════════════════════════════════
#  CHART 4 – AI Benchmark Performance vs Human Baseline
# ════════════════════════════════════════════════════════════════════════════
def chart_ai_performance():
    records = [
        # year, task, ai_score, human_score
        (2015, "Image Recognition",  96.4, 94.9),
        (2016, "Speech Recognition", 91.2, 94.0),
        (2017, "Go (game)",          99.8, 60.0),
        (2018, "Reading Comprehension", 87.4, 86.8),
        (2019, "Language Modeling",  89.0, 89.8),
        (2020, "Protein Folding",    92.4, 70.0),
        (2021, "Code Generation",    67.7, 72.3),
        (2022, "Text Reasoning",     90.4, 89.8),
        (2023, "Multimodal Bench.",  88.7, 86.4),
        (2024, "Complex Reasoning",  84.6, 83.1),
        (2025, "Scientific Research",82.0, 80.5),
    ]
    df = pd.DataFrame(records, columns=["year", "task", "ai", "human"])
    df.to_csv(os.path.join(DATA_DIR, "ai_performance.csv"), index=False)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    apply_futuristic_style(fig, [ax])

    x = np.arange(len(df))
    width = 0.38
    bars1 = ax.bar(x - width / 2, df["ai"],    width, color=NEON_CYAN,    label="AI System",
                   edgecolor=BG, linewidth=0.4, alpha=0.9)
    bars2 = ax.bar(x + width / 2, df["human"], width, color=NEON_MAGENTA, label="Human Baseline",
                   edgecolor=BG, linewidth=0.4, alpha=0.9)

    # label the bars
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:.1f}",
                ha="center", va="bottom", fontsize=6.5, color=NEON_CYAN)
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:.1f}",
                ha="center", va="bottom", fontsize=6.5, color=NEON_MAGENTA)

    ax.set_title("AI vs HUMAN PERFORMANCE ON BENCHMARK TASKS  (Score / 100)", fontsize=12,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Benchmark Task & Year", fontsize=10)
    ax.set_ylabel("Score", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"{r.task}\n({r.year})" for r in df.itertuples()],
        rotation=30, ha="right", fontsize=7.5
    )
    ax.set_ylim(0, 115)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.legend(fontsize=9, framealpha=0, labelcolor=TEXT)
    ax.axhline(100, color=TEXT, linewidth=0.6, linestyle=":", alpha=0.5)
    ax.text(len(df) - 0.5, 101.5, "Human = 100 baseline", fontsize=7,
            color=TEXT, ha="right", alpha=0.7)

    fig.tight_layout(pad=1.5)
    path = os.path.join(OUT_DIR, "chart_ai_performance.png")
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    print(f"  ✔ Saved {path}")


# ════════════════════════════════════════════════════════════════════════════
#  Write chart metadata JSON consumed by the Node.js server
# ════════════════════════════════════════════════════════════════════════════
def write_metadata():
    meta = [
        {
            "id": "tech_adoption",
            "title": "Technology Adoption Forecast",
            "subtitle": "Adoption rates for breakthrough technologies (2025–2060)",
            "image": "/images/chart_tech_adoption.png",
            "category": "Technology"
        },
        {
            "id": "space_economy",
            "title": "Space Economy Revenue by Sector",
            "subtitle": "Projected revenue in USD Billion (2025–2055)",
            "image": "/images/chart_space_economy.png",
            "category": "Space"
        },
        {
            "id": "energy_transition",
            "title": "Global Energy Transition",
            "subtitle": "Share of total energy by source (2020–2060)",
            "image": "/images/chart_energy_transition.png",
            "category": "Energy"
        },
        {
            "id": "ai_performance",
            "title": "AI vs Human Performance",
            "subtitle": "Benchmark scores across major AI milestones",
            "image": "/images/chart_ai_performance.png",
            "category": "Artificial Intelligence"
        },
    ]
    dest = os.path.join(os.path.dirname(__file__), "..", "web", "charts_meta.json")
    with open(dest, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  ✔ Saved {dest}")


# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating futuristic charts…\n")
    chart_tech_adoption()
    chart_space_economy()
    chart_energy_transition()
    chart_ai_performance()
    write_metadata()
    print("\nAll done.")
