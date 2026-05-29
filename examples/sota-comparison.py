# sota-comparison.py
# Grouped vertical bar (SOTA comparison): 3 methods × 4 metrics, ±1 SD error
# bars over 5 seeds. IEEE single-column, semantic palette, Type-42 fonts.
#
# Replace the `values` and `errs` arrays with your actual experiment results.
# The current numbers are placeholder demo data.

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# --- Publication-ready rcParams (from plotting-reference.md, IEEE style) ---
mpl.rcParams.update({
    # Fonts: Times New Roman, safe default across CS/Nature/IEEE
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    # Sizes (pt)
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 13,
    # Lines & markers
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.5,
    "lines.markersize": 5,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.minor.width": 0.5,
    "ytick.minor.width": 0.5,
    # Tick direction: "out" for IEEE (use "in" for Nature/Science)
    "xtick.direction": "out",
    "ytick.direction": "out",
    # Grid: off by default for bar charts
    "axes.grid": False,
    "grid.linewidth": 0.5,
    "grid.alpha": 0.4,
    # PDF font embedding (CRITICAL: Type-3 fails ACM/IEEE submission)
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    # IEEE single-column width
    "figure.figsize": (3.5, 2.6),
    "figure.constrained_layout.use": True,
})

# --- Data ---
# Placeholder values — REPLACE with your experiment results.
# Data averaged over 5 random seeds; error bars = ±1 SD.

methods = ["Baseline-A", "Baseline-B", "Ours"]
metrics = ["Accuracy", "F1", "AUC", "Recall"]

# Mean scores over 5 seeds — shape (3 methods, 4 metrics)
values = np.array([
    [78.2, 75.1, 82.0, 71.5],   # Baseline-A
    [80.4, 78.3, 84.1, 74.2],   # Baseline-B
    [83.7, 81.9, 87.3, 78.0],   # Ours
])

# Standard deviation over 5 seeds — shape (3 methods, 4 metrics)
errs = np.array([
    [0.5, 0.6, 0.4, 0.7],       # Baseline-A
    [0.4, 0.5, 0.4, 0.6],       # Baseline-B
    [0.3, 0.4, 0.3, 0.5],       # Ours
])

# IEEE semantic palette: convolution, pooling, attention-purple (Ours always
# last and in the emphasis color — do not re-sort by performance).
palette = ["#6C8EBF", "#82B366", "#9673A6"]

# --- Plot ---
x = np.arange(len(metrics))
width = 0.25                 # narrower bars for 3 groups avoids touching
fig, ax = plt.subplots(figsize=(3.5, 2.6))

for i, (method_name, color) in enumerate(zip(methods, palette)):
    offset = (i - (len(methods) - 1) / 2) * width
    ax.bar(
        x + offset, values[i], width,
        yerr=errs[i],
        label=method_name,
        color=color,
        edgecolor="black",
        linewidth=0.5,
        error_kw={"linewidth": 0.8, "capsize": 2},
    )

ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylabel("Score (%)")
# Y-axis zoomed to 60-95% to emphasize inter-method differences.
# Disclose this in the caption.
ax.set_ylim(60, 95)
ax.legend(
    frameon=False,
    loc="upper left",
    ncol=3,
    columnspacing=1.0,
    handletextpad=0.4,
)
ax.spines[["top", "right"]].set_visible(False)

# --- Save ---
out = "fig_sota_comparison"
fig.savefig(f"{out}.pdf")       # vector, for paper
fig.savefig(f"{out}.png", dpi=600)  # raster, for slides / preview
plt.close(fig)
print(f"Saved {out}.pdf and {out}.png")
