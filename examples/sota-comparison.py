# fig_sota_comparison.py
# Grouped vertical bar comparing 3 methods on 4 metrics, with ±1 SD error
# bars over 5 seeds. Demo for academic-writing-toolkit §I-1.

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# --- Publication-ready rcParams (from plotting-reference.md) ---
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 13,
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.5,
    "lines.markersize": 5,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "axes.grid": False,
    "pdf.fonttype": 42,   # Type-42 TrueType — required for ACM/IEEE submission
    "ps.fonttype": 42,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "figure.figsize": (3.5, 2.6),
    "figure.constrained_layout.use": True,
})

# --- Data ---
# 3 methods compared on 4 standard NLP benchmarks; values are accuracy (%)
# averaged over 5 random seeds. Error bars represent ±1 SD across seeds.
methods = ["Baseline-A", "Baseline-B", "Ours"]
metrics = ["MMLU", "GSM8K", "HumanEval", "BBH"]

values = np.array([
    [78.2, 75.1, 82.0, 71.5],   # Baseline-A
    [80.4, 78.3, 84.1, 74.2],   # Baseline-B
    [83.7, 81.9, 87.3, 78.0],   # Ours
])
errs = np.array([
    [0.5, 0.6, 0.4, 0.7],
    [0.4, 0.5, 0.4, 0.6],
    [0.3, 0.4, 0.3, 0.5],
])

# IEEE-semantic palette: Ours in attention-purple to draw the eye.
palette = ["#6C8EBF", "#82B366", "#9673A6"]

# --- Plot ---
x = np.arange(len(metrics))
width = 0.25
fig, ax = plt.subplots(figsize=(3.5, 2.6))

for i, (method, color) in enumerate(zip(methods, palette)):
    offset = (i - (len(methods) - 1) / 2) * width
    ax.bar(
        x + offset, values[i], width,
        yerr=errs[i], label=method,
        color=color, edgecolor="black", linewidth=0.5,
        error_kw={"linewidth": 0.8, "capsize": 2.5, "ecolor": "#333"},
    )

ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylabel("Accuracy (%)")
# Y-limit zoomed to where the differences are visible (disclose in caption).
ax.set_ylim(60, 95)
ax.legend(
    frameon=False, loc="upper left", ncol=3,
    columnspacing=1.0, handletextpad=0.4,
    bbox_to_anchor=(0.0, 1.18),
)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="x", which="both", bottom=True, top=False)

# --- Save ---
out = "fig_sota_comparison"
fig.savefig(f"{out}.pdf")
fig.savefig(f"{out}.png", dpi=300)
plt.close(fig)
print(f"Wrote {out}.pdf and {out}.png")
