# Academic Plotting Templates (Python)

19 chart templates matching `prompts/recommend-chart.md`. Read this file
when generating Python code for a paper figure. Each template assumes the
publication style block from `references/plotting-reference.md` is already
applied.

## Index

| # | Chart type | Section |
|---|---|---|
| 1 | Grouped vertical bar (SOTA comparison) | §I-1 |
| 2 | Horizontal bar (long labels) | §I-2 |
| 3 | Pareto front | §I-3 |
| 4 | Radar chart | §I-4 |
| 5 | Stacked bar | §I-5 |
| 6 | Line + confidence band | §II-6 |
| 7 | Line with zoomed inset | §II-7 |
| 8 | Scatter + fitted curve | §II-8 |
| 9 | ROC curve | §III-9 |
| 10 | Precision-Recall curve | §III-10 |
| 11 | Heatmap (confusion / correlation) | §IV-11 |
| 12 | Scatter (predicted vs true) | §IV-12 |
| 13 | Bubble chart | §IV-13 |
| 14 | Violin plot | §V-14 |
| 15 | Box plot | §V-15 |
| 16 | Donut / pie | §V-16 |
| 17 | Dual y-axis | §VI-17 |
| 18 | Bar + line combo | §VI-18 |
| 19 | Faceted grid (small multiples) | §VI-19 |

**Common preamble** — every template assumes:

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# (Apply rcParams from plotting-reference.md here)
```

For brevity, templates below skip the rcParams block and the imports —
include them in your actual script.

---

## §I — Value & Performance Comparison

### §I-1. Grouped vertical bar (SOTA comparison)

When 2-4 methods × 3-6 metrics. Paper-default chart for "we beat baselines."

```python
methods = ["Baseline-A", "Baseline-B", "Ours"]
metrics = ["Acc.", "F1", "AUC", "Recall"]
# shape: (n_methods, n_metrics)
values = np.array([[78.2, 75.1, 82.0, 71.5],
                   [80.4, 78.3, 84.1, 74.2],
                   [83.7, 81.9, 87.3, 78.0]])
errs = np.array([[0.5, 0.6, 0.4, 0.7],
                 [0.4, 0.5, 0.4, 0.6],
                 [0.3, 0.4, 0.3, 0.5]])  # ±1 SD over seeds

palette = ["#6C8EBF", "#82B366", "#9673A6"]   # IEEE: conv / pool / attn
x = np.arange(len(metrics))
width = 0.25
fig, ax = plt.subplots(figsize=(3.5, 2.6))
for i, (m, c) in enumerate(zip(methods, palette)):
    offset = (i - (len(methods)-1)/2) * width
    ax.bar(x + offset, values[i], width, yerr=errs[i],
           label=m, color=c, edgecolor="black", linewidth=0.5,
           error_kw={"linewidth": 0.8, "capsize": 2})
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylabel("Score (%)")
ax.set_ylim(60, 95)   # zoom in to where the action is
ax.legend(frameon=False, loc="upper left", ncol=3, columnspacing=1.0,
          handletextpad=0.4)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("fig_compare.pdf")
fig.savefig("fig_compare.png", dpi=600)
```

**Conventions:** Ours always last (rightmost bar of each group) and in the
emphasis color. Don't sort by performance. Y-axis starts above 0 only when
all bars are well above 0 — disclose this in the caption.

### §I-2. Horizontal bar (long labels / many entries)

When method names are long ("MoE-Mixtral-8x7B-Instruct-v0.1") or there are
≥8 entries. Avoids tilted x-labels.

```python
methods = ["GPT-4o", "Claude-3.5-Sonnet", "Llama-3.1-405B", "Qwen2.5-72B",
           "Mistral-Large-2", "Gemini-1.5-Pro", "Ours"]
scores  = [82.3, 81.7, 79.5, 78.8, 77.2, 80.1, 84.5]

# Sort ascending so the largest is on top
order = np.argsort(scores)
methods = [methods[i] for i in order]
scores = [scores[i] for i in order]
colors = ["#9673A6" if m == "Ours" else "#BDBDBD" for m in methods]

fig, ax = plt.subplots(figsize=(3.5, 3.5))
ax.barh(methods, scores, color=colors, edgecolor="black", linewidth=0.5)
ax.set_xlabel("MMLU-Pro score (%)")
ax.set_xlim(70, 90)
# Annotate each bar with its value
for i, v in enumerate(scores):
    ax.text(v + 0.2, i, f"{v:.1f}", va="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("fig_horizontal.pdf")
fig.savefig("fig_horizontal.png", dpi=600)
```

**Conventions:** Always sort (ascending bottom→top puts the best at the
top). Highlight "Ours" with the emphasis color, others gray.

### §I-3. Pareto front (accuracy vs cost trade-off)

When there's a trade-off between two competing metrics. Standard for
efficiency papers.

```python
methods = ["A", "B", "C", "D", "E", "F", "Ours"]
params  = [7,  13, 33, 70, 175, 405, 22]   # billions
acc     = [62, 68, 73, 78, 82,  84,  80]   # %
on_front = [False, True, True, False, True, True, True]

palette = ["#9673A6" if m == "Ours" else
           "#D79B00" if f else "#BDBDBD"
           for m, f in zip(methods, on_front)]
fig, ax = plt.subplots(figsize=(3.5, 2.8))
ax.scatter(params, acc, c=palette, s=60, edgecolor="black", linewidth=0.6,
           zorder=3)
# Pareto-front line through frontier points
front_pts = sorted([(p, a) for p, a, f in zip(params, acc, on_front) if f])
ax.plot([p for p, _ in front_pts], [a for _, a in front_pts],
        color="#D79B00", linewidth=1.2, linestyle="--", zorder=2,
        label="Pareto front")
for m, p, a in zip(methods, params, acc):
    ax.annotate(m, (p, a), xytext=(5, 5), textcoords="offset points",
                fontsize=9)
ax.set_xscale("log")
ax.set_xlabel("Parameters (B)")
ax.set_ylabel("Accuracy (%)")
ax.legend(frameon=False, loc="lower right")
ax.grid(True, which="major", linewidth=0.4, alpha=0.4)
fig.savefig("fig_pareto.pdf")
fig.savefig("fig_pareto.png", dpi=600)
```

**Conventions:** X is the cost dimension (log scale common), Y is the
quality dimension. Frontier in dashed line, off-frontier points gray.

### §I-4. Radar chart (multi-dimensional capability)

When showing a model is well-rounded. ≤6 axes — more becomes unreadable.

```python
labels = ["Speed", "Accuracy", "Memory", "Robust.", "Calibr.", "Cost"]
# Each row is one method, normalized to [0, 1]
ours      = [0.85, 0.92, 0.78, 0.88, 0.81, 0.90]
baseline  = [0.72, 0.85, 0.68, 0.75, 0.70, 0.55]

n = len(labels)
angles = np.linspace(0, 2*np.pi, n, endpoint=False).tolist()
angles += angles[:1]   # close the loop
ours += ours[:1]; baseline += baseline[:1]

fig, ax = plt.subplots(figsize=(3.5, 3.5),
                      subplot_kw={"projection": "polar"})
ax.plot(angles, ours, color="#9673A6", linewidth=1.5, label="Ours")
ax.fill(angles, ours, color="#9673A6", alpha=0.20)
ax.plot(angles, baseline, color="#6C8EBF", linewidth=1.5, label="Baseline")
ax.fill(angles, baseline, color="#6C8EBF", alpha=0.15)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels)
ax.set_ylim(0, 1)
ax.set_rgrids([0.25, 0.5, 0.75], angle=0, fontsize=8)
ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1.30, 1.10))
fig.savefig("fig_radar.pdf")
fig.savefig("fig_radar.png", dpi=600)
```

**Conventions:** Normalize all axes to [0, 1] (or all to %). Two methods
max for clarity; three is the limit before lines overlap unreadably.

### §I-5. Stacked bar (composition of a total)

When breaking down a total metric: total inference time = load + forward + post-process.

```python
methods = ["Method A", "Method B", "Method C", "Ours"]
load    = [12, 14, 15, 11]
forward = [88, 102, 75, 62]
post    = [8,  12,  10, 7]

palette = ["#DAE8FC", "#6C8EBF", "#9673A6"]
fig, ax = plt.subplots(figsize=(3.5, 2.6))
ax.bar(methods, load,    color=palette[0], edgecolor="black",
       linewidth=0.5, label="Load")
ax.bar(methods, forward, color=palette[1], edgecolor="black",
       linewidth=0.5, bottom=load, label="Forward")
ax.bar(methods, post,    color=palette[2], edgecolor="black",
       linewidth=0.5, bottom=np.array(load)+np.array(forward),
       label="Post-process")
# Total annotation on top
totals = np.array(load) + np.array(forward) + np.array(post)
for i, t in enumerate(totals):
    ax.text(i, t + 2, f"{t}", ha="center", fontsize=9)
ax.set_ylabel("Latency (ms)")
ax.legend(frameon=False, loc="upper right", ncol=3,
          bbox_to_anchor=(1.0, 1.18))
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("fig_stacked.pdf")
fig.savefig("fig_stacked.png", dpi=600)
```

**Conventions:** Component order from bottom up should be largest at the
bottom (most stable visual base). Total annotated on top. ≤4 stack
components — more becomes unreadable.

---

## §II — Trends & Convergence

### §II-6. Line + confidence band (training curves)

The default for ML training curves. Shows mean over seeds with band for
variance.

```python
epochs = np.arange(1, 51)
# 5 random seeds → mean ± std
seeds = 5
acc_runs = 0.5 + 0.4 * (1 - np.exp(-epochs/15)) + \
           0.02 * np.random.RandomState(0).randn(seeds, len(epochs))
mean = acc_runs.mean(axis=0)
std  = acc_runs.std(axis=0)

fig, ax = plt.subplots(figsize=(3.5, 2.6))
ax.plot(epochs, mean, color="#9673A6", linewidth=1.5, label="Ours")
ax.fill_between(epochs, mean-std, mean+std, color="#9673A6", alpha=0.20)
ax.set_xlabel("Epoch"); ax.set_ylabel("Accuracy")
ax.set_xlim(1, 50)
ax.legend(frameon=False, loc="lower right")
ax.grid(True, linewidth=0.4, alpha=0.4)
fig.savefig("fig_curve.pdf")
fig.savefig("fig_curve.png", dpi=600)
```

**Conventions:** Caption MUST disclose what the band is: "Shaded region
indicates ±1 SD over 5 seeds." Use ≥3 seeds; ≥5 is more credible.

### §II-7. Line with zoomed inset

When the late-training advantage is small but matters.

```python
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

epochs = np.arange(1, 101)
ours = 0.50 + 0.45 * (1 - np.exp(-epochs/20))
base = 0.50 + 0.43 * (1 - np.exp(-epochs/22))

fig, ax = plt.subplots(figsize=(3.5, 2.6))
ax.plot(epochs, ours, color="#9673A6", linewidth=1.5, label="Ours")
ax.plot(epochs, base, color="#6C8EBF", linewidth=1.5, label="Baseline",
        linestyle="--")
ax.set_xlabel("Epoch"); ax.set_ylabel("Accuracy")
ax.legend(frameon=False, loc="lower right")
ax.grid(True, linewidth=0.4, alpha=0.4)

# Inset zoomed on epochs 80-100
axins = inset_axes(ax, width="40%", height="40%", loc="center right",
                   bbox_to_anchor=(0.0, -0.10, 1, 1),
                   bbox_transform=ax.transAxes)
axins.plot(epochs, ours, color="#9673A6", linewidth=1.5)
axins.plot(epochs, base, color="#6C8EBF", linewidth=1.5, linestyle="--")
axins.set_xlim(80, 100); axins.set_ylim(0.91, 0.96)
axins.tick_params(labelsize=7)
axins.grid(True, linewidth=0.3, alpha=0.4)
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5", linewidth=0.6)
fig.savefig("fig_inset.pdf")
fig.savefig("fig_inset.png", dpi=600)
```

**Conventions:** Inset placement avoids the data; tick fontsize smaller
than main axes; thin connector lines.

### §II-8. Scatter + fitted curve

Discrete data points that suggest a relationship.

```python
from scipy.optimize import curve_fit

x = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256])    # e.g., batch size
y = np.array([0.62, 0.68, 0.74, 0.78, 0.81, 0.83, 0.84, 0.845, 0.847])

def f(x, a, b, c): return a - b * np.exp(-c * np.log2(x))
popt, _ = curve_fit(f, x, y, p0=[0.85, 0.5, 0.3])
xx = np.logspace(0, np.log2(256), 100, base=2)
yy = f(xx, *popt)

fig, ax = plt.subplots(figsize=(3.5, 2.6))
ax.scatter(x, y, color="#9673A6", s=40, edgecolor="black", linewidth=0.5,
           zorder=3, label="Observed")
ax.plot(xx, yy, color="#D79B00", linewidth=1.5, linestyle="--",
        label=f"Fit: a-b·exp(-c·log₂x)")
ax.set_xscale("log", base=2)
ax.set_xlabel("Batch size"); ax.set_ylabel("Accuracy")
ax.legend(frameon=False, loc="lower right")
ax.grid(True, which="both", linewidth=0.4, alpha=0.4)
fig.savefig("fig_scatter_fit.pdf")
fig.savefig("fig_scatter_fit.png", dpi=600)
```

**Conventions:** State the fit form (in the legend or caption). Don't
fit a polynomial of degree > 3 — overfits visually. Include a goodness
metric (R² or RMSE) in the caption.

---

## §III — Model Evaluation & Classification

### §III-9. ROC curve

Standard for binary classification. AUC reported in legend.

```python
from sklearn.metrics import roc_curve, auc

# y_true, y_score from your model — shown for 3 models here
models = {
    "Baseline":  ("#6C8EBF", "--", y_score_a),
    "Strong":    ("#82B366", "-.", y_score_b),
    "Ours":      ("#9673A6", "-",  y_score_c),
}
fig, ax = plt.subplots(figsize=(3.5, 3.5))
for name, (color, ls, scores) in models.items():
    fpr, tpr, _ = roc_curve(y_true, scores)
    a = auc(fpr, tpr)
    ax.plot(fpr, tpr, color=color, linestyle=ls, linewidth=1.5,
            label=f"{name} (AUC={a:.3f})")
ax.plot([0, 1], [0, 1], color="#999", linewidth=0.8, linestyle=":",
        label="Random")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_aspect("equal")
ax.legend(frameon=False, loc="lower right", fontsize=9)
ax.grid(True, linewidth=0.4, alpha=0.4)
fig.savefig("fig_roc.pdf")
fig.savefig("fig_roc.png", dpi=600)
```

**Conventions:** Square aspect ratio. Diagonal y=x as the random baseline.
AUC always reported with 3 decimals. Vary line style so curves are
distinguishable in B&W.

### §III-10. Precision-Recall curve

Use when class imbalance is severe (positive ≪ negative). PR is more
faithful than ROC in this regime.

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

models = {
    "Baseline": ("#6C8EBF", "--", y_score_a),
    "Strong":   ("#82B366", "-.", y_score_b),
    "Ours":     ("#9673A6", "-",  y_score_c),
}
fig, ax = plt.subplots(figsize=(3.5, 3.5))
for name, (color, ls, scores) in models.items():
    p, r, _ = precision_recall_curve(y_true, scores)
    ap = average_precision_score(y_true, scores)
    ax.plot(r, p, color=color, linestyle=ls, linewidth=1.5,
            label=f"{name} (AP={ap:.3f})")
# Random baseline = positive class prevalence
prev = y_true.mean()
ax.axhline(prev, color="#999", linewidth=0.8, linestyle=":",
           label=f"Random (AP={prev:.3f})")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
ax.set_aspect("equal")
ax.legend(frameon=False, loc="lower left", fontsize=9)
ax.grid(True, linewidth=0.4, alpha=0.4)
fig.savefig("fig_pr.pdf")
fig.savefig("fig_pr.png", dpi=600)
```

**Conventions:** Random baseline = positive prevalence (NOT y=x). Average
Precision (AP) is the area under PR; report it in the legend.

---

## §IV — Data Relationships & Matrix Visualization

### §IV-11. Heatmap (confusion matrix / correlation)

```python
labels = ["cat", "dog", "fox", "wolf", "rabbit"]
cm = np.array([[42, 1, 2, 0, 5],
               [1, 38, 0, 6, 5],
               [3, 0, 31, 2, 14],
               [0, 7, 1, 39, 3],
               [4, 4, 12, 1, 29]])
cm_norm = cm / cm.sum(axis=1, keepdims=True)

fig, ax = plt.subplots(figsize=(3.5, 3.2))
im = ax.imshow(cm_norm, cmap="Blues", vmin=0, vmax=1, aspect="equal")
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
ax.set_xlabel("Predicted"); ax.set_ylabel("True")
# Annotate with values
for i in range(cm_norm.shape[0]):
    for j in range(cm_norm.shape[1]):
        v = cm_norm[i, j]
        c = "white" if v > 0.5 else "black"
        ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                color=c, fontsize=8)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
fig.savefig("fig_cm.pdf")
fig.savefig("fig_cm.png", dpi=600)
```

**Conventions:** For confusion matrices, normalize by row (true-class
prevalence) and report in [0,1]. For correlation matrices use `RdBu_r`
with `vmin=-1, vmax=1`. Annotate values when ≤10×10; skip for larger.

### §IV-12. Scatter (predicted vs true, regression)

```python
y_true = ...  # ground truth
y_pred = ...  # model output

fig, ax = plt.subplots(figsize=(3.0, 3.0))
ax.scatter(y_true, y_pred, color="#9673A6", s=20, alpha=0.6,
           edgecolor="none")
# y=x reference
lo, hi = min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())
ax.plot([lo, hi], [lo, hi], color="#999", linewidth=0.8, linestyle="--",
        label="y = x")
# R² annotation
from sklearn.metrics import r2_score
r2 = r2_score(y_true, y_pred)
ax.text(0.05, 0.95, f"R² = {r2:.3f}", transform=ax.transAxes,
        fontsize=10, va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                  edgecolor="#999", linewidth=0.5))
ax.set_xlabel("Ground truth"); ax.set_ylabel("Predicted")
ax.set_aspect("equal")
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
ax.legend(frameon=False, loc="lower right")
ax.grid(True, linewidth=0.4, alpha=0.4)
fig.savefig("fig_pred_true.pdf")
fig.savefig("fig_pred_true.png", dpi=600)
```

**Conventions:** Square axes, y=x reference line dashed gray. R² in
upper-left text box. If many points, lower `alpha` to 0.3 and increase
`s` slightly.

### §IV-13. Bubble chart

Scatter + size-encoded third dimension.

```python
methods = ["A", "B", "C", "D", "E", "Ours"]
params  = [7, 13, 33, 70, 175, 22]      # B params
flops   = [0.5, 1.2, 4, 12, 40, 2.5]    # TFLOPs
acc     = [60, 68, 73, 78, 82, 80]      # %

# Bubble area ∝ params; use sqrt scaling so visual area is linear
sizes = np.sqrt(np.array(params)) * 30
colors = ["#9673A6" if m == "Ours" else "#BDBDBD" for m in methods]

fig, ax = plt.subplots(figsize=(3.5, 2.8))
ax.scatter(flops, acc, s=sizes, c=colors, alpha=0.7,
           edgecolor="black", linewidth=0.6)
for m, x, y in zip(methods, flops, acc):
    ax.annotate(m, (x, y), xytext=(8, 0), textcoords="offset points",
                fontsize=9, va="center")
ax.set_xscale("log")
ax.set_xlabel("FLOPs (T)"); ax.set_ylabel("Accuracy (%)")
ax.grid(True, which="major", linewidth=0.4, alpha=0.4)
# Bubble size legend
for size_val in [10, 50, 200]:
    ax.scatter([], [], s=np.sqrt(size_val)*30, c="gray", alpha=0.6,
               edgecolor="black", linewidth=0.6, label=f"{size_val}B")
ax.legend(title="Params", frameon=False, loc="lower right",
          labelspacing=1.2, fontsize=8, title_fontsize=9)
fig.savefig("fig_bubble.pdf")
fig.savefig("fig_bubble.png", dpi=600)
```

**Conventions:** Bubble area (not radius) encodes the value — use
sqrt scaling on the size argument since matplotlib treats `s` as area.
Provide a size legend.

---

## §V — Statistical Distributions & Composition

### §V-14. Violin plot (distribution shape)

Better than box plot when distribution shape matters (e.g., bimodal).

```python
groups = ["Ours", "Baseline-A", "Baseline-B"]
data = [np.random.RandomState(s).normal(0.8, 0.05, 200) for s in range(3)]

fig, ax = plt.subplots(figsize=(3.5, 2.8))
parts = ax.violinplot(data, positions=range(len(groups)),
                      showmeans=False, showmedians=True, widths=0.7)
palette = ["#9673A6", "#6C8EBF", "#82B366"]
for pc, c in zip(parts["bodies"], palette):
    pc.set_facecolor(c); pc.set_edgecolor("black"); pc.set_alpha(0.7)
    pc.set_linewidth(0.6)
parts["cmedians"].set_color("black"); parts["cmedians"].set_linewidth(1.0)
parts["cmaxes"].set_color("black"); parts["cmaxes"].set_linewidth(0.6)
parts["cmins"].set_color("black"); parts["cmins"].set_linewidth(0.6)
parts["cbars"].set_color("black"); parts["cbars"].set_linewidth(0.6)
ax.set_xticks(range(len(groups))); ax.set_xticklabels(groups)
ax.set_ylabel("Accuracy")
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("fig_violin.pdf")
fig.savefig("fig_violin.png", dpi=600)
```

**Conventions:** Show median as a horizontal line; don't show means
unless you're claiming a parametric model. Color-fill the violin bodies
for category distinction.

### §V-15. Box plot

When distribution shape matters less; you just want quartiles + outliers.

```python
groups = ["Ours", "Baseline-A", "Baseline-B"]
data = [np.random.RandomState(s).normal(0.8, 0.05, 200) for s in range(3)]
palette = ["#9673A6", "#6C8EBF", "#82B366"]

fig, ax = plt.subplots(figsize=(3.5, 2.8))
bp = ax.boxplot(data, labels=groups, widths=0.5, patch_artist=True,
                medianprops=dict(color="black", linewidth=1.0),
                flierprops=dict(marker="o", markersize=3,
                                markerfacecolor="black", alpha=0.5))
for patch, c in zip(bp["boxes"], palette):
    patch.set_facecolor(c); patch.set_edgecolor("black")
    patch.set_linewidth(0.6); patch.set_alpha(0.7)
ax.set_ylabel("Accuracy")
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("fig_box.pdf")
fig.savefig("fig_box.png", dpi=600)
```

**Conventions:** Box = Q1-Q3, whiskers = 1.5×IQR by default. Outliers as
small circles. Don't enable `notch=True` unless you want to show CI on
the median (reviewers may ask what the notch means).

### §V-16. Donut / pie

Categorical proportions. Donut preferred over pie (center label space).

```python
labels = ["Loading", "Tokenization", "Forward pass", "Decoding", "Other"]
sizes  = [12, 8, 65, 12, 3]
palette = ["#DAE8FC", "#82B366", "#9673A6", "#FFE6CC", "#999999"]

fig, ax = plt.subplots(figsize=(3.5, 3.5))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=palette, startangle=90,
    autopct="%1.1f%%", pctdistance=0.78,
    wedgeprops=dict(width=0.4, edgecolor="white", linewidth=1.5))
for at in autotexts:
    at.set_color("black"); at.set_fontsize(9)
# Center text (the "donut hole" advantage)
ax.text(0, 0, "Total\n245 ms", ha="center", va="center",
        fontsize=11, fontweight="bold")
ax.set_aspect("equal")
fig.savefig("fig_donut.pdf")
fig.savefig("fig_donut.png", dpi=600)
```

**Conventions:** ≤6 slices; with more, switch to a horizontal bar chart.
Sort slices by size for readability. Use `startangle=90` so the largest
slice starts at the top.

---

## §VI — Composite Layouts

### §VI-17. Dual y-axis (different units)

When two metrics with incompatible units must share x.

```python
epochs = np.arange(1, 51)
loss = 2.5 * np.exp(-epochs/15) + 0.3
acc  = 100 * (1 - np.exp(-epochs/12))

fig, ax1 = plt.subplots(figsize=(3.5, 2.6))
c1, c2 = "#B85450", "#6C8EBF"
l1, = ax1.plot(epochs, loss, color=c1, linewidth=1.5, label="Loss")
ax1.set_xlabel("Epoch"); ax1.set_ylabel("Loss", color=c1)
ax1.tick_params(axis="y", labelcolor=c1)

ax2 = ax1.twinx()
l2, = ax2.plot(epochs, acc, color=c2, linewidth=1.5, linestyle="--",
               label="Accuracy")
ax2.set_ylabel("Accuracy (%)", color=c2)
ax2.tick_params(axis="y", labelcolor=c2)

ax1.legend(handles=[l1, l2], frameon=False, loc="center right")
fig.savefig("fig_dualy.pdf")
fig.savefig("fig_dualy.png", dpi=600)
```

**Conventions:** Color-code the y-axis labels and ticks to match each
line. Use line style (solid vs dashed) to reinforce the distinction.
Avoid 3+ y-axes — readers can't track them.

### §VI-18. Bar + line combo (foreground / background layering)

For long-tail distributions: bars are sample counts, line is per-class
metric.

```python
classes = [f"C{i}" for i in range(10)]
counts  = [1200, 800, 500, 320, 210, 150, 100, 70, 45, 25]   # long-tail
acc     = [92, 89, 84, 80, 75, 72, 68, 64, 61, 58]

fig, ax1 = plt.subplots(figsize=(3.5, 2.6))
ax1.bar(classes, counts, color="#DAE8FC", edgecolor="#6C8EBF",
        linewidth=0.6, label="Sample count")
ax1.set_xlabel("Class"); ax1.set_ylabel("Sample count", color="#6C8EBF")
ax1.tick_params(axis="y", labelcolor="#6C8EBF")
ax1.set_yscale("log")

ax2 = ax1.twinx()
ax2.plot(classes, acc, color="#B85450", marker="o", markersize=4,
         linewidth=1.5, label="Accuracy")
ax2.set_ylabel("Accuracy (%)", color="#B85450")
ax2.tick_params(axis="y", labelcolor="#B85450")
ax2.set_ylim(50, 100)

# Combined legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, frameon=False, loc="upper right", fontsize=9)
fig.savefig("fig_barline.pdf")
fig.savefig("fig_barline.png", dpi=600)
```

**Conventions:** Bars in muted color (background role), line in saturated
color with markers (foreground). Log y-axis when long-tail spans ≥2
orders of magnitude.

### §VI-19. Faceted grid (small multiples)

When too many comparisons make one chart cluttered.

```python
import seaborn as sns

# Synthetic data: 4 datasets × 3 methods × 5 seeds
import pandas as pd
rows = []
for ds in ["MNIST", "CIFAR-10", "CIFAR-100", "ImageNet-100"]:
    for method in ["Baseline", "Strong", "Ours"]:
        for seed in range(5):
            acc = (90 if ds == "MNIST" else 75 if ds == "CIFAR-10"
                   else 60 if ds == "CIFAR-100" else 70)
            acc += {"Baseline": 0, "Strong": 3, "Ours": 6}[method]
            acc += np.random.RandomState(seed).normal(0, 1)
            rows.append((ds, method, acc))
df = pd.DataFrame(rows, columns=["dataset", "method", "acc"])

g = sns.catplot(data=df, x="method", y="acc", col="dataset",
                kind="bar", height=2.0, aspect=0.9,
                palette=["#6C8EBF", "#82B366", "#9673A6"],
                errorbar=("ci", 95), capsize=0.15,
                edgecolor="black", linewidth=0.5)
g.set_titles("{col_name}")
g.set_axis_labels("", "Accuracy (%)")
g.tight_layout()
g.savefig("fig_facets.pdf")
fig.savefig("fig_facets.png", dpi=600)
```

**Conventions:** Share y-axis across facets so readers can compare
across panels (`sharey=True` is `catplot` default). Per-panel titles
just name the subset variable. Use ≤6 facets; more becomes a wall.
