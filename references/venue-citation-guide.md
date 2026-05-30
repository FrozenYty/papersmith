# Venue Citation Guide

Citation format and BibTeX requirements for major CS/ML conferences and
journals. Read this file when the user specifies a target venue.

Each entry lists: in-text citation style, BibTeX required/optional fields,
and the official style file where applicable.

**Self-check note**: Conference policies change annually. Fields marked
`[VERIFY: check <year> author kit]` should be confirmed against the
current year's call for papers or template download page.

---

## Top ML Conferences

### NeurIPS
- **In-text**: Author-year, `\citep{key}` for parenthetical, `\citet{key}`
  for textual. Uses `natbib` package.
- **Style file**: `neurips_<year>.sty` (bundled with template)
- **Required fields**: author, title, booktitle/journal, year
- **Optional**: volume, pages, doi, url
- **Template**: [VERIFY: check neurips.cc for current year templates]
- **Reference limit**: No explicit limit, but typically 30-60 references

### ICML
- **In-text**: Author-year, `\citep{key}` / `\citet{key}`. Uses `natbib`.
- **Style file**: `icml<year>.sty`
- **Required fields**: author, title, booktitle/journal, year
- **Optional**: volume, pages, doi
- **Template**: [VERIFY: check icml.cc for current year templates]

### ICLR
- **In-text**: Author-year, `\citep{key}` / `\citet{key}`. Uses `natbib`.
- **Style file**: `iclr<year>_conference.sty`
- **Required fields**: author, title, booktitle/journal, year
- **Template**: [VERIFY: check openreview.net for current ICLR style]
- **Note**: ICLR uses OpenReview; check the official template on their
  submission site rather than a standalone webpage.

---

## Computer Vision

### CVPR / ICCV / ECCV
- **In-text**: Numeric, `[1]`, `[2,3,4]`. IEEE style.
- **Style file**: `\bibliographystyle{IEEEtran}`
- **BibTeX required fields**:
  - `@article`: author, title, journal, year, volume, number, pages,
    month, doi
  - `@inproceedings`: author, title, booktitle, year, pages, doi
- **Template**: IEEEtran is bundled with most LaTeX distributions;
  [VERIFY: check cvpr.thecvf.com for conference-specific overrides]
- **Reference format**: `[1] J. Smith et al., "Paper Title," in
  *Proc. CVPR*, 2024, pp. 1234-1245.`
- **Note**: CVPR/ICCV require the `\bibliographystyle{IEEEtran}` call
  before `\bibliography{}`. Some years have a custom `.bst` file.

---

## NLP Conferences

### ACL / NAACL / EMNLP
- **In-text**: Author-year, `\ citep{key}` / `\citet{key}`.
  Uses `natbib` + `acl_natbib.bst`.
- **Style file**: `acl_natbib.bst` (bundled with ACL LaTeX template)
- **Required fields**: author, title, booktitle, year, address (for
  inproceedings), doi
- **Optional**: pages, url
- **Template**: [VERIFY: check aclanthology.org or aclweb.org for current
  style files; the ACL Anthology also provides BibTeX entries for all
  published papers]
- **Special rule**: All ACL-published papers have canonical BibTeX on
  the ACL Anthology. When verifying ACL citations, prefer the Anthology
  BibTeX over hand-edited entries.

---

## IEEE / ACM Journals

### IEEE (T-PAMI, TIP, TIFS, etc.)
- **In-text**: Numeric, `[1]`, `[2]-[5]`. Sequential by first citation.
- **Style file**: `\bibliographystyle{IEEEtran}`
- **Required fields** (strict — IEEE submission checkers verify these):
  `author`, `title`, `journal`, `year`, `volume`, `number`, `pages`,
  `month`, `doi`
- **Note**: IEEE journals reject submissions with missing `month` or
  `volume` fields. All-numeric month format: `month = {1}` (not `jan`).

### ACM (Computing Surveys, TOCS, SIGGRAPH, etc.)
- **In-text**: Numeric, `[1]`. Sequential by first citation.
- **Style file**: `\bibliographystyle{ACM-Reference-Format}`
- **Required fields**: author, title, booktitle/journal, year, doi
- **Template**: [VERIFY: check acm.org for current templates; ACM has
  migrated to a new LaTeX template in recent years]
- **Note**: ACM requires DOI for all references when available.

---

## General Science

### Nature
- **In-text**: Superscript numbers. `...as demonstrated¹².`
- **Style file**: Nature provides its own `.bst` in the author template.
- **Required fields**: author, title, journal, year, volume, pages, doi
- **Template**: [VERIFY: check nature.com for current LaTeX template]
- **Reference limit**: Typically 30-50 for Articles, fewer for Letters.
- **Note**: Nature's reference format is highly specific — use their
  official template only; don't approximate with standard styles.

### Science
- **In-text**: Numeric, `(1)`, `(2, 3)`. Parentheses, not brackets.
- **Style file**: Science provides proprietary `.bst` files.
- **Required fields**: author, title, journal, year, volume, pages, doi
- **Note**: Science has strict reference limits (~40 for Research Articles).
  [VERIFY: check science.org for current limits]

---

## Chinese Journals

### 计算机学报 (Chinese Journal of Computers)
### 软件学报 (Journal of Software)
### 自动化学报 (Acta Automatica Sinica)
- **In-text**: Sequential numeric, `[1]`, `[2-4]`.
- **Format standard**: GB/T 7714-2015
- **Example**: `[1] 张三, 李四. 基于深度学习的图像分类综述[J]. 计算机学报, 2024, 47(3): 567-589.`
- **BibTeX**: Most Chinese journals accept either GB/T 7714 BibTeX or
  manual formatting. Check the specific journal's author guidelines.
- **Required fields**: author (Chinese name order: surname first),
  title (Chinese + English translation often required), journal, year,
  volume, number, pages
- **Template**: [VERIFY: check each journal's official website for the
  most current LaTeX template]
- **Note**: Three journals above represent the broad GB/T family; other
  Chinese journals may use GB/T 7714 with minor variations.

---

## Cross-Venue Quick Reference

| Venue | In-text style | `.bst` file | Key quirk |
|---|---|---|---|
| NeurIPS/ICML/ICLR | Author-year `\citep{}` | `natbib` | — |
| CVPR/ICCV | Numeric `[1]` | `IEEEtran` | Requires `month` field |
| ACL/NAACL/EMNLP | Author-year `\citep{}` | `acl_natbib` | Canonical .bib on Anthology |
| IEEE journals | Numeric `[1]` | `IEEEtran` | Strict field requirements |
| ACM | Numeric `[1]` | `ACM-Reference-Format` | DOI required |
| Nature | Superscript numerals | `nature.bst` | Highly specific format |
| Science | Parentheses `(1)` | Proprietary | ~40 ref limit |
| Chinese journals | Numeric `[1]` | GB/T 7714-2015 | Chinese + English title |

---

## Self-Check for Citation Verifiability

When generating BibTeX for any venue, verify:

1. Every `\cite{}` in the `.tex` has a corresponding bib entry.
2. Every bib entry has at minimum: `author`, `title`, `year`, and a
   venue identifier (`journal` or `booktitle`).
3. The `doi` field is present whenever the paper has one — this is the
   single most important field for verifiability.
4. Author names are consistent across entries (no "J. Smith" vs "John
   Smith" for the same person).
5. [VERIFY: venue-specific quirks — check this file for the current
   target venue before submission.]
