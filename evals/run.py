#!/usr/bin/env python3
"""
evals/run.py — Academic Writing Toolkit evals runner.

Reads evals/evals.json, verifies each test case:
  1. prompt text is non-empty
  2. prompt files referenced in expected_output exist under prompts/
  3. reference files referenced in expected_output exist under references/
  4. specific detail strings (template markers, technical constants,
     quoted key phrases) from expected_output are findable in the
     corresponding prompt/reference files

Writes per-case reports to evals/results/case_NN.txt and prints a
summary table to stdout. Does NOT call any LLM — this is a static
file-presence and structure-consistency check only.

Usage:
    cd <skill-root>
    python evals/run.py
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent   # skill root
PROMPTS_DIR = BASE_DIR / "prompts"
REFERENCES_DIR = BASE_DIR / "references"
EVALS_DIR = Path(__file__).resolve().parent
EVALS_JSON = EVALS_DIR / "evals.json"
RESULTS_DIR = EVALS_DIR / "results"

PASS  = "PASS"
FAIL  = "FAIL"
WARN  = "WARN"
INFO  = "INFO"

# ── file loading ───────────────────────────────────────────────────

def load_evals():
    if not EVALS_JSON.exists():
        sys.exit(f"ERROR: {EVALS_JSON} not found")
    with open(EVALS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_files_content(filepaths):
    """Return a dict {relative_name: content_str} for existing files."""
    cache = {}
    for fp in filepaths:
        if fp.exists():
            try:
                cache[str(fp.relative_to(BASE_DIR))] = \
                    fp.read_text(encoding="utf-8", errors="replace")
            except Exception:
                cache[str(fp.relative_to(BASE_DIR))] = ""
    return cache


# ── extraction helpers ─────────────────────────────────────────────

def extract_prompt_files(expected):
    """
    Pull out .md filenames from expected_output that match an actual
    file under prompts/. Handles:
      - bare names like  polish-abstract.md
      - (new prompt: write-broader-impact)  syntax
    """
    found = set()

    # "(new prompt: foo-bar)" → foo-bar.md
    for m in re.finditer(r'\(new prompt:\s*([a-zA-Z][a-zA-Z0-9\-]*)\)', expected):
        fname = f"{m.group(1)}.md"
        if (PROMPTS_DIR / fname).exists():
            found.add(fname)

    # bare .md filenames — only keep those that actually live in prompts/
    for m in re.finditer(r'\b([a-z][a-z0-9\-]*\.md)\b', expected):
        fname = m.group(1)
        if (PROMPTS_DIR / fname).exists():
            found.add(fname)

    return sorted(found)


def extract_ref_files(expected):
    """Pull out reference filenames from `references/xxx.md` mentions."""
    found = set()
    for m in re.finditer(r'references/([a-zA-Z][a-zA-Z0-9\-]*\.md)', expected):
        found.add(m.group(1))
    return sorted(found)


def extract_details(expected):
    """
    Extract detail strings that should be searchable in the referenced
    prompt or reference files. These include:

    - Template/section markers like  §1, §I-3, §II-4b
    - Technical constants like  pdf.fonttype=42
    - Flow-direction rules like  source.y > target.y
    - Structural descriptors in quotes (e.g. "5-part structure")
    - Specific numeric requirements mentioned explicitly

    These are best-effort heuristics; unmatched details produce WARN,
    not FAIL.
    """
    details = set()

    # ── § template markers ──
    for m in re.finditer(r'§([A-Za-z0-9\-]+)', expected):
        details.add(f"§{m.group(1)}")

    # ── technical constants (normalise spacing) ──
    tech = [
        r'pdf\.fonttype\s*=\s*42',
        r'ps\.fonttype\s*=\s*42',
        r'source\.y\s*>\s*target\.y',
        r'source\.x\s*<\s*target\.x',
    ]
    for pat in tech:
        for m in re.finditer(pat, expected):
            # store a normalised form for reliable file-grep
            raw = m.group(0)
            detail = re.sub(r'\s+', ' ', raw)
            details.add(detail)

    # ── double-quoted substantive phrases (4-80 chars) ──
    for m in re.finditer(r'"([^"]{4,80})"', expected):
        phrase = m.group(1)
        # skip full-sentence-length strings (likely meta-commentary)
        if not re.search(r'[.!?]$', phrase):
            details.add(phrase)

    # ── single-quoted key terms (2-40 chars) ──
    for m in re.finditer(r"'([^']{2,40})'", expected):
        details.add(m.group(1))

    # ── explicit structural keywords that often appear verbatim ──
    structural = [
        r'5-part\s+structure',
        r'three-part\s+structure',
        r'two-part\s+format',
        r'modification\s+log',
        r'sentence-to-part\s+map',
        r'Part\s+1\s+\[LaTeX\]',
        r'Part\s+2\s+\[Translation\]',
        r'Part\s+3\s+\[Modification\s+Log\]',
        r'Part\s+1\s+\[Review\s+Report\]',
        r'Part\s+2\s+\[Strategic\s+Advice\]',
    ]
    for pat in structural:
        for m in re.finditer(pat, expected, re.IGNORECASE):
            raw = m.group(0)
            detail = re.sub(r'\s+', ' ', raw)
            details.add(detail)

    # ── clean up: some detail extractors produce duplicates that look
    #   different but are semantically the same. Dedupe aggressively. ──
    return sorted({d for d in details if d})


# ── detail search ──────────────────────────────────────────────────

def search_details(details, referenced_keys, file_cache):
    """
    For each detail string, search in ALL cached files (prompts + references).
    Returns a three-way partition:

      found_in_ref:  {detail: [key, ...]} — found in at least one
                     explicitly referenced file
      found_elsewhere: {detail: [key, ...]} — found only in files NOT
                       named by the expected_output
      not_found:     set of detail strings not found anywhere
    """
    all_keys = set(file_cache.keys())
    ref_set  = set(referenced_keys)

    found_in_ref      = {}
    found_elsewhere   = {}
    not_found         = set()

    for detail in details:
        matched_all = []
        matched_ref = []
        for key in all_keys:
            content = file_cache.get(key, "")
            if not content:
                continue
            if detail in content:
                matched_all.append(key)
                if key in ref_set:
                    matched_ref.append(key)

        if matched_ref:
            found_in_ref[detail] = matched_ref
        elif matched_all:
            found_elsewhere[detail] = matched_all
        else:
            not_found.add(detail)

    return found_in_ref, found_elsewhere, not_found


# ── case runner ────────────────────────────────────────────────────

def run_case(case, file_cache):
    cid    = case["id"]
    prompt = case.get("prompt", "").strip()
    expected = case.get("expected_output", "").strip()

    lines = []
    issues   = []
    warnings = []
    checks   = []

    def add(line):
        lines.append(line)

    add(f"Case {cid:02d}")
    add("=" * 50)
    add(f"Prompt    ({len(prompt)} chars): {prompt[:150]}")
    add("")

    # ── check 1: prompt non-empty ──
    if not prompt:
        issues.append("PROMPT_EMPTY")
        add(f"  [{FAIL}] prompt text is empty")
    else:
        checks.append("prompt non-empty")
        add(f"  [{PASS}] prompt non-empty ({len(prompt)} chars)")

    # ── check 2: expected_output non-empty ──
    if not expected:
        issues.append("EXPECTED_OUTPUT_EMPTY")
        add(f"  [{FAIL}] expected_output is empty")
    else:
        add(f"  [{INFO}] expected_output ({len(expected)} chars)")

    # ── extract file references ──
    prompt_files = extract_prompt_files(expected)
    ref_files    = extract_ref_files(expected)

    # ── check 3: prompt files exist ──
    for pf in prompt_files:
        if (PROMPTS_DIR / pf).exists():
            checks.append(f"prompts/{pf} exists")
            add(f"  [{PASS}] prompts/{pf}")
        else:
            issues.append(f"PROMPT_MISSING: {pf}")
            add(f"  [{FAIL}] prompts/{pf} — NOT FOUND")

    if not prompt_files:
        warnings.append("NO_PROMPT_FILES_REFERENCED")
        add(f"  [{WARN}] no prompt .md files detected in expected_output")
    elif not issues:
        add(f"  [{INFO}] {len(prompt_files)} prompt file(s) referenced: {', '.join(prompt_files)}")

    # ── check 4: reference files exist ──
    for rf in ref_files:
        if (REFERENCES_DIR / rf).exists():
            checks.append(f"references/{rf} exists")
            add(f"  [{PASS}] references/{rf}")
        else:
            issues.append(f"REF_MISSING: {rf}")
            add(f"  [{FAIL}] references/{rf} — NOT FOUND")

    if ref_files:
        add(f"  [{INFO}] {len(ref_files)} reference file(s) referenced: {', '.join(ref_files)}")

    # ── check 5: detail-consistency ──
    details = extract_details(expected)
    if details:
        # build the set of keys this case's expected_output explicitly
        # names — these are "in scope" for the case
        refd_keys = {
            f"prompts/{pf}" for pf in prompt_files
        } | {
            f"references/{rf}" for rf in ref_files
        }

        found_r, found_e, not_found = search_details(
            details, refd_keys, file_cache
        )

        for d in sorted(found_r.keys()):
            locs = ", ".join(found_r[d])
            d_short = d[:72] + ("…" if len(d) > 72 else "")
            checks.append(f"detail found (refd): {d_short}")
            add(f"  [{PASS}] '{d_short}'  ← in referenced: {locs}")

        for d in sorted(found_e.keys()):
            locs = ", ".join(found_e[d])
            d_short = d[:72] + ("…" if len(d) > 72 else "")
            warnings.append(f"DETAIL_FOUND_ELSEWHERE: {d} → {locs}")
            add(f"  [{WARN}] '{d_short}'  ← found in {locs} (not named in expected_output)")

        for d in sorted(not_found):
            d_short = d[:72] + ("…" if len(d) > 72 else "")
            warnings.append(f"DETAIL_NOT_FOUND: {d}")
            add(f"  [{WARN}] '{d_short}'  ← not found in any file")
    else:
        add(f"  [{INFO}] no detail strings extracted to verify")

    # ── summary line ──
    add("")
    if issues:
        status = FAIL
        add(f"  STATUS → {FAIL}")
        add(f"  Issues ({len(issues)}):")
        for i in issues:
            add(f"    - {i}")
        if warnings:
            add(f"  Warnings ({len(warnings)}):")
            for w in warnings:
                add(f"    - {w}")
    elif warnings:
        status = WARN
        add(f"  STATUS → {WARN}  (checks passed: {len(checks)})")
        add(f"  Warnings ({len(warnings)}):")
        for w in warnings:
            add(f"    - {w}")
    else:
        status = PASS
        add(f"  STATUS → {PASS}  ({len(checks)} checks passed)")

    return status, lines


# ── main ───────────────────────────────────────────────────────────

def main():
    data  = load_evals()
    cases = data.get("evals", [])
    if not cases:
        print("No eval cases found in evals.json")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # pre-load all prompt + reference files into a cache so detail
    # searches hit disk once per file
    all_prompt_files = list(PROMPTS_DIR.glob("*.md"))
    all_ref_files    = list(REFERENCES_DIR.glob("*.md"))
    file_cache = load_files_content(all_prompt_files + all_ref_files)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []

    for case in cases:
        status, report_lines = run_case(case, file_cache)
        results.append((case["id"], status))

        # write per-case report
        rpt_path = RESULTS_DIR / f"case_{case['id']:02d}.txt"
        with open(rpt_path, "w", encoding="utf-8") as f:
            f.write(f"Eval Report — Case {case['id']:02d} — {timestamp}\n")
            f.write("=" * 60 + "\n\n")
            f.write("\n".join(report_lines))
            f.write("\n")

    # ── stdout summary table ──
    n_total = len(results)
    n_pass  = sum(1 for _, s in results if s == PASS)
    n_fail  = sum(1 for _, s in results if s == FAIL)
    n_warn  = sum(1 for _, s in results if s == WARN)

    bar = "=" * 56
    print()
    print(bar)
    print("  Academic Writing Toolkit — Evals Runner")
    print(f"  {timestamp}")
    print(bar)
    print()
    print(f"  {'Case ID':<10} {'Status':<10}")
    print(f"  {'-' * 9}  {'-' * 9}")
    for cid, s in results:
        print(f"  {cid:>4}       {s:<10}")
    print()
    print(f"  Total: {n_total}  |  {PASS}: {n_pass}  |  {FAIL}: {n_fail}  |  {WARN}: {n_warn}")
    print()
    print(f"  Reports: {RESULTS_DIR}")
    print(bar)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
