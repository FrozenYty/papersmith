# Academic Plotting Reference (Python)

Read this file before generating any matplotlib/seaborn plotting code for a
paper figure. It enforces the conventions that separate publication-ready
figures from "looks fine on a Jupyter screen" figures.

## Workflow

When the user asks for a chart, do this in order:

1. **Pick the chart type** — if not already chosen, route through
   `prompts/recommend-chart.md` first.
2. **Read the relevant template** in `references/plotting-templates.md`
   (19 templates, indexed by the same chart-type names as recommend-chart).
3. **Apply the publication style block** from this file (rcParams +
   color palette + sizing).
4. **Adapt to the user's data** — change variable names, axis labels,
   legend, but KEEP the style invariants from this file.
5. **Save in two formats**: `.pdf` (vector, for paper) and `.png` (300 dpi,
   for slides/preview). Both with `bbox_inches='tight'`.

## Publication Style Block (paste-ready)

This rcParams block matches what NeurIPS / CVPR / IEEE / Nature-family
journals expect. Drop into the top of every plotting script.

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

# --- Publication-ready rcParams ---
mpl.rcParams.update({
    # Fonts: Times New Roman is the safe default across CS/Nature/IEEE.
    # For ML/CS conferences, "Times New Roman" or "DejaVu Serif" are accepted.
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",  # math glyphs match Times
    # Sizes (in pt): titles 12, labels 11, ticks 10, legend 10, annotation 9
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
    # Tick direction inward (Nature/Science style); use "out" for IEEE
    "xtick.direction": "in",
    "ytick.direction": "in",
    # Grid: light, on by default for line/scatter; off for bar
    "axes.grid": False,
    "grid.linewidth": 0.5,
    "grid.alpha": 0.4,
    # Spines: keep all four; some venues prefer top/right off — leave decision
    # to per-template.
    # PDF font embedding (CRITICAL for paper submission)
    "pdf.fonttype": 42,   # TrueType, not Type-3 (Type-3 fails ACM/IEEE checkers)
    "ps.fonttype": 42,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    # Figure size (single-column paper figure default)
    "figure.figsize": (3.5, 2.6),
    "figure.constrained_layout.use": True,
})
```

**Why each setting matters:**
- `pdf.fonttype = 42` is the single most-failed paper submission check. Type
  3 fonts cause text to render as outlines, breaking copy-paste from PDF and
  failing IEEE PDF eXpress / ACM Type 3 detection. **Always 42.**
- `xtick.direction = in` is the Nature/Science convention. Switch to `out`
  for IEEE style. Don't mix.
- `figure.figsize = (3.5, 2.6)` is the IEEE single-column width (3.5 in =
  88.9 mm). For double-column / NeurIPS-wide, use (7.0, 2.6) or (7.0, 4.0).
- `constrained_layout.use = True` removes the need for manual
  `plt.tight_layout()` and handles legends-outside-axes correctly.

## Figure Sizing (by venue)

| Venue / column | Width inches | Width mm | Use case |
|---|---|---|---|
| IEEE single-column | 3.5 | 88.9 | One figure per column |
| IEEE double-column | 7.16 | 181.9 | Wide figure spanning both cols |
| NeurIPS / ICML / ICLR text width | ~5.5 | ~140 | Standard one-column width |
| ACL text width | ~5.5 | ~140 | Same |
| Nature single-column | 3.5 | ~88 | Standard |
| Nature double-column | 7.2 | ~183 | Spanning |

Aspect ratio: avoid arbitrary squares. Default 4:3 (1.33) for charts with
a single y-axis; 5:3 (1.67) for time-series; 1:1 for scatterplots and
heatmaps when both dimensions are the same kind of data.

## Color Palettes

**Match `drawio-reference.md` so figures across paper sections look
consistent.** Don't introduce new palettes mid-paper.

```python
# Nature 2025 — neutral-leaning, good for 5-6 categories
nature_pal = ["#433764", "#E48566", "#A05179", "#C66571", "#C6C687", "#668441"]

# Science 2025 — soft, pastel-like, good for visualization-heavy figures
science_pal = ["#928B92", "#E3C7D5", "#FCF0E4", "#6B879D", "#72AABB", "#E48078"]

# Cell 2025 — high-saturation, good for ≥6 categories
cell_pal = ["#FA756E", "#D68E04", "#93A906", "#13BB38", "#05C1A2",
            "#0EB9E4", "#639DFC", "#DB70FE"]

# Nature Physics 2025 — primary-color emphasis, good for 4-6 categories
np_pal = ["#FF3533", "#FEC71A", "#2AD92D", "#35E7DF", "#2C97FF", "#2F2FFD"]

# IEEE / CVPR / NeurIPS ML standard — semantic by component (matches
# drawio-reference.md IEEE palette)
ieee_pal = {
    "attention":     "#9673A6",
    "convolution":   "#6C8EBF",
    "rnn":           "#28A745",
    "pooling":       "#82B366",
    "norm":          "#999999",
    "fc":            "#D79B00",
    "input":         "#B85450",
    "output":        "#D6B656",
}
```

**Selection rule:** ≤6 categories → Nature or Nature Physics; ≥7 categories
→ Cell. For ML papers comparing methods (yours vs baselines), use the IEEE
semantic mapping where the colors mean something (your method = attention
purple, etc.) rather than arbitrary.

**Colorblind-safe**: Cell and Nature Physics palettes are reasonably CB-safe
already. For diverging data (e.g., heatmaps), use `cmap="RdBu_r"` (built-in,
CB-safe) or `cmap="coolwarm"`. **Don't use `jet` or `rainbow`** — they fail
CB tests and obscure data structure.

## Statistical Conventions

**Error bars / confidence intervals — pick one and disclose it:**
- 1 standard deviation: `yerr=std`. Common in ML.
- 95% CI from N runs: `yerr=1.96 * std / sqrt(N)`. Better for ≤10 runs.
- 95% CI from bootstrap: use `seaborn.barplot(errorbar="ci")` or compute
  with `scipy.stats.bootstrap`.

State which one in the figure caption: "Error bars indicate ±1 SD over 5
seeds." Don't use error bars without disclosing what they represent.

**Significance markers (only when statistically tested):**
- `ns` (not significant)
- `*` p < 0.05
- `**` p < 0.01
- `***` p < 0.001
Place over the bar pair being compared with a horizontal bracket. Don't add
stars to figures where the test wasn't run.

**Multiple-run plotting (e.g., training curves):**
- Show the mean as a solid line.
- Show the variance as a semi-transparent band: `ax.fill_between(x,
  mean-std, mean+std, alpha=0.2, color=color)`.
- Don't use individual run lines unless N ≤ 3 (otherwise noise dominates).

## Scale Treatments

**Broken axis** (when a few outliers compress the rest):

```python
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[1, 3])
# Plot the same data on both
ax1.bar(...); ax2.bar(...)
# Limit each
ax1.set_ylim(80, 100)   # outlier range
ax2.set_ylim(0, 20)     # main range
# Hide the spines between
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.tick_params(labeltop=False, top=False)
ax2.xaxis.tick_bottom()
# Diagonal break marks
d = .015
kwargs = dict(transform=ax1.transAxes, color="k", clip_on=False, lw=0.8)
ax1.plot((-d, +d), (-d, +d), **kwargs)
ax1.plot((1-d, 1+d), (-d, +d), **kwargs)
kwargs.update(transform=ax2.transAxes)
ax2.plot((-d, +d), (1-d, 1+d), **kwargs)
ax2.plot((1-d, 1+d), (1-d, 1+d), **kwargs)
```

**Log scale** (data spans orders of magnitude, e.g. parameter counts):

```python
ax.set_yscale("log")
# Major ticks at decades; minor at 2,3,...,9
from matplotlib.ticker import LogLocator, NullFormatter
ax.yaxis.set_major_locator(LogLocator(base=10, numticks=8))
ax.yaxis.set_minor_locator(LogLocator(base=10, subs=range(2,10), numticks=80))
ax.yaxis.set_minor_formatter(NullFormatter())
```

**Symlog** (data crosses zero with wide range): `ax.set_yscale("symlog",
linthresh=1)`. Linthresh is the cutoff below which the scale is linear.

## Saving Figures

```python
out = "fig_results"
fig.savefig(f"{out}.pdf")           # vector, for paper
fig.savefig(f"{out}.png", dpi=300)  # raster, for slides / preview
```

**Don't:** save as `.jpg` (lossy compression on text), `.eps` (deprecated;
modern paper systems prefer PDF), or low-dpi PNG (300 dpi minimum).

**Don't:** use `plt.show()` in a script intended for batch generation; it
blocks. Use `plt.close(fig)` after saving.

## Common Pitfalls (real failures observed)

1. **Type 3 font failure** — submission gets desk-rejected by ACM/IEEE
   compliance check. Fix: `pdf.fonttype = 42`. Always.
2. **Default matplotlib blue/orange** — looks "made with matplotlib" rather
   than designed. Fix: set a palette from this file, or pass
   `color=palette[i]` explicitly.
3. **Unreadable axis ticks** — auto-generated dense labels. Fix: set
   `MaxNLocator(6)` or specify ticks explicitly.
4. **Legend covering data** — happens with `loc='best'`. Fix: pin with
   `loc='upper left'` or move outside: `bbox_to_anchor=(1.02, 1)`.
5. **Inconsistent units** — "Time (s)" vs "Time" vs "time(s)". Fix: pick
   one convention per paper. Usually "Time (s)" with capitalized first
   letter and unit in parens.
6. **Stretched aspect ratio** — figure is 12:3 because the user copied the
   default. Fix: set `figsize` per the venue table above.
7. **No baseline comparison** — bar chart with only the proposed method.
   Always include baselines for ML comparisons.
8. **Error bars without disclosure** — caption says "results" but doesn't
   say if bars are SD/SE/CI. Always disclose.
9. **Color carrying critical info** — only color distinguishes lines, fails
   for colorblind readers and B&W printing. Fix: also vary linestyle (`-`,
   `--`, `:`, `-.`) or marker (`o`, `s`, `^`, `D`).
10. **Title set in script when caption goes in LaTeX** — duplicates info.
    For paper figures, omit `ax.set_title(...)` and put the description
    in `\caption{...}`. For slides, do set the title.

## Self-check (before saving)

```
1. fonttype 42 set:                            pass/fail
2. Figure size matches venue width:            pass/fail
3. Palette from this file (not default):       pass/fail
4. Error bars disclosed in caption:            pass/fail
5. Axis labels include units:                  pass/fail
6. Title omitted (paper) or set (slides):      pass/fail
7. Saved as both .pdf and .png:                pass/fail
8. Legend doesn't cover data:                  pass/fail
9. Lines distinguishable in B&W (linestyle):   pass/fail
10. No `jet` / `rainbow` colormap:             pass/fail
```

## Optional: SciencePlots integration

If `SciencePlots` (`pip install SciencePlots`) is installed, you can shorten
the rcParams block to:

```python
import scienceplots
plt.style.use(["science", "ieee"])  # or "nature", "high-vis"
```

This sets fonts, sizes, ticks, and colors close to the IEEE / Nature
conventions in one line. Still set `pdf.fonttype = 42` explicitly afterward
because some SciencePlots styles miss it.
