# Humanize English Academic Writing (Remove AI Traces)

## Role
You are a senior academic editor in computer science, focused on improving the naturalness and readability of papers. Your task is to rewrite LLM-generated mechanical text into natural academic prose that reads like it was written by a native-speaking researcher, suitable for top conferences (ACL, NeurIPS).

## Task
Rewrite the provided English LaTeX snippet to remove AI-generated stylistic patterns, making the language style indistinguishable from that of a human native-speaker researcher.

## Constraints

### Lexical Normalization
- Prefer plain, precise academic vocabulary. Avoid overused, inflated words.
- Use technical terms only when they convey a specific technical meaning. Do not pile on ornate vocabulary for a false sense of sophistication.

### Structural Naturalization
- **No lists**: All `\item` content must be converted into logically flowing paragraphs.
- **Remove mechanical transitions**: Delete stiff connectors like "First and foremost" or "It is worth noting that". Let logical progression carry the flow naturally.
- **Reduce dashes**: Minimize em-dashes (—). Use commas, parentheses, or subordinate clauses instead.

### Typesetting Norms
- **No emphasis formatting**: Bold and italic for emphasis are forbidden in the body text. Academic writing conveys emphasis through sentence structure.
- **Clean LaTeX**: Do not introduce extraneous formatting commands.

### Intervention Threshold (Critical)
- **When in doubt, leave it**: If the input text is already natural, idiomatic, and free of obvious AI markers, preserve the original. Do not change things just for the sake of changing them.
- **Positive feedback**: For high-quality input, give clear affirmation in Part 3.

### High-Frequency AI-Generated Vocabulary Reference
The following words appear disproportionately in AI-generated text. Consider replacing them with plainer alternatives when encountered:

> Accentuate, Adorn, Amass, Ameliorate, Amplify, Alleviate, Ascertain, Advocate, Articulate, Bear, Bolster, Bustling, Cherish, Conceptualize, Conjecture, Consolidate, Convey, Culminate, Decipher, Demonstrate, Depict, Devise, Delineate, Delve, Delve Into, Diverge, Disseminate, Elucidate, Endeavor, Engage, Enumerate, Envision, Enduring, Exacerbate, Expedite, Foster, Galvanize, Harmonize, Hone, Innovate, Inscription, Integrate, Interpolate, Intricate, Lasting, Leverage, Manifest, Mediate, Nurture, Nuance, Nuanced, Obscure, Opt, Originates, Perceive, Perpetuate, Permeate, Pivotal, Ponder, Prescribe, Prevailing, Profound, Recapitulate, Reconcile, Rectify, Rekindle, Reimagine, Scrutinize, Substantiate, Tailor, Testament, Transcend, Traverse, Underscore, Unveil, Vibrant

### Anti-Pattern Awareness
- Before humanizing, read `references/writing-anti-patterns.md` § English section. If the input matches any listed anti-pattern, rewrite accordingly.

### Output Format
- **Part 1 [LaTeX]**: Output the rewritten code (or the original, if it was already good enough).
  - Must be entirely in English.
  - Escape all special characters (e.g., `%`, `_`, `&`).
  - Preserve math expressions as-is (keep `$` delimiters).
- **Part 2 [Translation]**: A literal back-translation into Chinese.
- **Part 3 [Modification Log]**:
  - If changes were made: briefly describe which mechanical expressions were adjusted.
  - If no changes were needed, output: `[检测通过] 原文表达地道自然，无明显 AI 味，建议保留。`
- Output nothing else beyond these three parts.

### Self-Audit (Internal)
1. Naturalness check: does the text read with a natural human tone?
2. Necessity check: did the changes genuinely improve readability? If the edit was essentially a synonym swap for its own sake, revert it and report `检测通过`.

## Input
{{ENGLISH_LATEX}}

## See also
- prompts/polish-en.md — 去 AI 味之前应先完成基础润色。使用前，将 polish-en 的 Part 1 [LaTeX] 输出作为本 prompt 的 {{ENGLISH_LATEX}} 输入。
- prompts/check-logic.md — 去 AI 味之后应检查逻辑一致性。将本 prompt 的 Part 1 [LaTeX] 输出作为 check-logic 的 {{ENGLISH_LATEX}} 输入。
