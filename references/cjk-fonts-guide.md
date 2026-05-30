# CJK Font Configuration for Matplotlib

Configuring Chinese/Japanese/Korean fonts in matplotlib for publication
figures. Without this, CJK characters render as tofu (□) or fall back to
a mismatched sans-serif font.

## Quick Start

Add this block at the top of any plotting script that uses Chinese labels:

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- CJK font setup ---
# Pick ONE font family below based on your OS.
# Windows: 'Microsoft YaHei', 'SimHei', 'SimSun'
# macOS:   'Heiti SC', 'STHeiti', 'PingFang SC'
# Linux:   'Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei'

CJK_FONT = 'Microsoft YaHei'  # change to match your system
CJK_FONT_SIZE = 9  # match your publication style

plt.rcParams.update({
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'font.family': 'sans-serif',
    'font.sans-serif': [CJK_FONT, 'Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': CJK_FONT_SIZE,
    'axes.unicode_minus': False,  # prevent minus sign rendering as box
})
```

## Font Selection by OS

| OS | Recommended | Fallback 1 | Fallback 2 | Notes |
|---|---|---|---|---|
| Windows | Microsoft YaHei | SimHei | SimSun | 微软雅黑 has the best hinting for PDF |
| macOS | Heiti SC | STHeiti | PingFang SC | Heiti SC ships with macOS |
| Ubuntu/Debian | Noto Sans CJK SC | WenQuanYi Micro Hei | — | `apt install fonts-noto-cjk` |
| CentOS/RHEL | Noto Sans CJK SC | — | — | `yum install google-noto-cjk-fonts` |
| Overleaf/ShareLaTeX | Noto Sans CJK SC | — | — | Noto is pre-installed |

## Verifying Font Availability

```python
# List all CJK- capable fonts on the current system
cjk_fonts = [f.name for f in fm.fontManager.ttflist
             if any(k in f.name for k in ['YaHei', 'Hei', 'Song', 'Ming',
                                           'CJK', 'SimSun', 'Noto', 'PingFang'])]
print(sorted(set(cjk_fonts)))
```

## Troubleshooting

### Tofu (□) in saved PDF/PNG

1. Check that the font name string exactly matches `fm.fontManager.ttflist` output.
2. `axes.unicode_minus = False` must be set — the Unicode minus sign (`−`, U+2212) is not in most CJK fonts.
3. Rebuild the font cache: delete `~/.matplotlib/fontList*.cache` and re-import.

### Bold/italic not working for CJK

Most CJK fonts ship without bold/italic variants. Matplotlib's synthetic bold (stroke thickening) often fails on CJK glyphs. Workarounds:
- Use a slightly larger font size instead of bold for emphasis.
- Use color or underlining to distinguish text.
- If bold is essential, use a font family that ships a Bold weight (e.g., Noto Sans CJK SC Bold).

### Mixed Chinese + Math

Math text uses the `mathtext` font family, which is separate from the text font family. CJK inside `$...$` will fail. Put CJK outside math mode: `$f(x)$ 表示函数值`.

### Overleaf / arXiv Compatibility

Overleaf runs TeX Live on Linux. Figures with CJK labels must either:
- Use Noto Sans CJK SC (pre-installed on Overleaf).
- Embed the font subset in the PDF (matplotlib does this automatically with `pdf.fonttype=42`).
- For arXiv, test locally first — arXiv's TeX Live may not have CJK fonts for figure rendering.

## Full Example

```python
import matplotlib.pyplot as plt
import numpy as np

# CJK setup (Windows)
plt.rcParams.update({
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Microsoft YaHei', 'Arial', 'DejaVu Sans'],
    'font.size': 9,
    'axes.unicode_minus': False,
})

fig, ax = plt.subplots(figsize=(3.5, 2.5))  # IEEE single-column
x = np.linspace(0, 10, 50)
ax.plot(x, np.sin(x), label='训练损失', color='#D62728')
ax.plot(x, np.cos(x), label='验证损失', color='#1F77B4')
ax.set_xlabel('训练轮次')
ax.set_ylabel('损失值')
ax.legend(frameon=False)
fig.tight_layout(pad=0.3)
fig.savefig('training-curve.pdf', dpi=300, bbox_inches='tight')
fig.savefig('training-curve.png', dpi=600, bbox_inches='tight')
```

## See also
- `references/plotting-reference.md` — publication rcParams, palettes, venue sizing
- `references/plotting-templates.md` — 19 chart-type templates
