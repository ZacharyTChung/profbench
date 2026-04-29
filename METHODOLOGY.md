# ProfBench methodology

This document describes what is built in this repository, the workflow used
to produce it, and how that workflow maps onto AfterQuery's expert-in-the-loop
data generation pipeline. The methodology is closely modeled on the FinanceQA
paper (Mateega, Georgescu, Tang — AfterQuery, 2025) — same question taxonomy
(tactical / conceptual, with tactical sub-divided into basic / assumption-based),
same exact-match scoring convention as the headline metric, same emphasis on
real-world on-the-job tasks over context-first benchmark designs.

## What this repo is

ProfBench is a domain-specific LLM evaluation harness. This particular instance
targets **procurement / source-to-pay** reasoning: supplier master data,
purchase orders, non-PO invoices, 3-way match, duplicate detection, Incoterms,
cross-border tax, period-close accruals, sanctions screening, and SOX P2P
controls.

It is functionally a **Market-Bench-style evaluation environment** — the same
genre of artifact AfterQuery produces for FinanceQA, Market-Bench, IDE-Bench,
Terminal-Bench, etc. — scoped down to one domain and run by a single
practitioner instead of a 100k-expert network.

## What is built (concretely)

### Data
- `data/questions.json` — 10 expert-style questions with rubrics, ideal answers, expected failure modes, and difficulty tags. Spans 4 categories: `supplier_data`, `invoice_processing`, `trade_and_tax`, `close_and_controls`. Difficulty mix: 2 easy / 4 medium / 4 hard.
- `data/anchors/` — real public records (USAspending, Chicago Payments, OFAC SDN) used to ground question scenarios in real-world data. Mapped per-question.
- `data/profbench_export.json` — Hugging Face-ready dataset export bundling questions, responses, and scores for one run.

### Harness
- `runner/eval.py` — CLI eval runner with Anthropic + OpenAI clients, dry-run mode, run_id tracking, SQLite persistence.
- `runner/models.py` — 5 model aliases: `claude` / `sonnet` (Sonnet 4.6), `opus` (Opus 4.7), `haiku` (Haiku 4.5), `gpt4o`. New models = subclass + add to `MODEL_REGISTRY`.

### Scoring
- `scorer/autoscore.py` — Claude-as-judge autograder using Opus 4.7 as the grader. Reads response + ideal answer + rubric and produces 0/1/2 with reasoning + confidence.
- `scorer/app.py` — Streamlit UI for human scoring (manual rubric grading).

### Analysis
- `analysis/report.py` — produces `analysis/loss_report.md` with per-model, per-category, per-difficulty breakdowns and inter-rater agreement.
- `leaderboard/generate.py` — produces `leaderboard/leaderboard.md` and `.html`.
- `data/export.py` — produces `data/profbench_export.json` for HF.
- `scripts/compare.py` — produces side-by-side `analysis/comparison_<run>.md` for rubric calibration. Use this to decide for each non-2 score whether the model genuinely fell short, the ideal answer was too narrow, or the rubric was miscalibrated.

### Persistence
- `db/profbench.db` — SQLite. Tables: `questions`, `responses`, `scores`. Keyed by run UUID. Gitignored.

## The workflow used

```
  ┌──────────────────────────────────────────────────────────────────┐
  │ 1. domain selection         procurement / source-to-pay          │
  │ 2. category taxonomy        4 categories × 3 difficulty tiers    │
  │ 3. question authoring       10 questions, expert-style scenarios │
  │ 4. ideal answer + rubric    0/1/2 tier definitions per question  │
  │ 5. anchor data              real records from public APIs        │
  └────────────────────┬─────────────────────────────────────────────┘
                       │
                       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │ 6. eval run                 N models × 10 questions → responses  │
  │ 7. autograde                Claude-as-judge → scores in DB       │
  │ 8. (optional) human grade   Streamlit UI → manual scores in DB   │
  └────────────────────┬─────────────────────────────────────────────┘
                       │
                       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │ 9. loss analysis            per-category, per-difficulty stats   │
  │ 10. comparison report       side-by-side for rubric calibration  │
  │ 11. leaderboard             cross-model rank table               │
  │ 12. dataset export          HF-ready JSON                        │
  └────────────────────┬─────────────────────────────────────────────┘
                       │
                       ▼
            calibrate, expand questions, repeat
```

## How this connects to AfterQuery's workflow

AfterQuery's published pipeline (per their public materials) has 5 steps:

1. **Expert identification & data capture** — recruit ~100k vetted professionals
2. **Capture reasoning steps** — record step-by-step expert decision-making, edge cases
3. **Structure data for SFT & RL** — prompt-response pairs (SFT) + rubric-based reward signals (RL)
4. **Build evaluation environments** — Terminal-Bench, Market-Bench, etc.
5. **Multi-stage post-training** — SFT on golden trajectories → RLVR (Reinforcement Learning from Verified Rewards)

Mapping ProfBench to those steps:

| AQ step | What it requires | ProfBench coverage |
| ------- | --------------- | ------------------ |
| 1 — expert identification | Many vetted experts | The author of this repo *is* one expert. Solo single-domain coverage. |
| 2 — reasoning steps | Step-by-step traces, not just final answers | **Partial.** Current `ideal_answer` field stores polished final answers, not reasoning traces. **This is the load-bearing upgrade for SFT-quality data.** |
| 3a — SFT pairs | Expert chain-of-thought as training pairs | Not produced today. Reachable by reformatting `ideal_answer` to traces. |
| 3b — RL + rubrics | Rubrics as reward signals | ✅ rubrics exist in 0/1/2 format. Coarse but usable. |
| 4 — eval environment | Market-Bench-style harness | ✅ this is exactly what ProfBench is. |
| 5 — actual training | Anthropic-scale infra | Out of scope. Not a solo-doable step. |

ProfBench in its current form is a **step-4 deliverable** — a procurement-domain
evaluation environment. It does not by itself train a model. It produces three
things that *feed* the AfterQuery pipeline:

1. A **measurement** of where current frontier models leak score on procurement reasoning (the loss taxonomy in `analysis/loss_report.md`).
2. A **comparative leaderboard** across models, useful for both lab consumers (which model to ship) and labs themselves (which capability to prioritize next).
3. A **rubric-graded dataset** in HF format. AQ can use the rubrics directly as reward signals (step 3b) and the questions as held-out evals (step 4).

## What this is not

- **Not a training dataset.** SFT data needs reasoning traces (step 2), not static ideal answers. Reformatting questions toward traces is the pending upgrade.
- **Not an agentic eval.** Current questions are single-turn Q&A. No tool use, no multi-turn workflows. AfterQuery's Terminal-Bench / UI-Bench tier requires that and would require new harness work.
- **Not a multimodal eval.** Procurement records are often spreadsheets, PDFs, scanned invoices. Current questions are text-only.

These three gaps are the realistic v2 directions if scope expands.

## Calibration discipline

The benchmark only works if the rubric is calibrated. Specifically: when a
model gets a 0 or 1, you must distinguish three cases before editing anything:

- **(a) the model genuinely fell short** — keep the score, the benchmark is working
- **(b) the `ideal_answer` was too narrow** — broaden the ideal answer
- **(c) the rubric tier definitions were miscalibrated** — fix the rubric

`scripts/compare.py <run_id>` produces a side-by-side review file that makes
this triage tractable. Walk through every non-2 score before declaring a run
final. Inflating scores by editing the dataset toward what the model already
does is the failure mode that destroys the benchmark's value.

## Methodology caveats

- **Self-grading bias:** the autograder uses Opus 4.7. When Opus 4.7 is itself one of the evaluated models, that's self-grading bias — note in any published report. Mitigation: cross-grade with a different model family (e.g., GPT-4o or Gemini) when keys are available.
- **Single grader:** one autograder pass per response. AfterQuery production-grade methodology runs multiple grader passes and reports inter-grader agreement. To approximate, run human scoring via `scorer/app.py` on a subset and compute auto-vs-manual agreement.
- **Sample size:** 10 questions is a pilot. A defensible Market-Bench-style submission targets 50-200 questions across more diverse failure modes.
- **Single domain expert:** all questions, ideal answers, and rubrics come from one practitioner. AQ's published methodology emphasizes peer review by multiple domain experts to catch idiosyncratic biases.

## Question taxonomy (FinanceQA-aligned)

Following the FinanceQA paper's three-way split:

- **Tactical-basic** — answerable from the provided context. Tests precision recalculation, application of accounting/procurement conventions, real-world calculation standards. The dominant category in the v0.1 pilot (11 of 18 questions).
- **Tactical-assumption** — requires inferring something not stated in the context. The killer category in FinanceQA's results: frontier models scored <5% on assumption questions even when they scored 40-60% on tactical-basic. Currently 4 of 18 questions in ProfBench (q_006 W-8/source-of-income split, q_007 EU VAT establishment, q_009 sanctions/UBO chain, q_015 HTS classification).
- **Conceptual** — no context, tests principles, conventions, the structure of relationships between metrics or controls. 3 of 18 questions (q_016 DPO stock/flow, q_017 duplicate-vendor vs duplicate-payment, q_018 control-failure tier hierarchy).

The mix is deliberately weighted toward tactical because tactical-basic and tactical-assumption together are what FinanceQA shows is uniquely missing from existing benchmarks.

## Scoring conventions

ProfBench reports two scores per response:

1. **Rubric score (0/1/2)** — the practitioner-authored 3-tier grading. More granular than the FinanceQA convention; useful for *calibration* (where a "1" tells you something specific is missing rather than just "wrong").
2. **Binary exact-match (% scoring 2/2)** — the FinanceQA-paper-aligned headline metric. "No partial credit" reflects the operational reality that an 80% answer in finance / procurement still requires line-by-line verification by a human and therefore provides minimal practical value. This is the number to compare against the FinanceQA results table for cross-domain context.

Both metrics are reported in `analysis/loss_report.md` and `leaderboard/leaderboard.md`.

## Reference texts (for question authoring)

When practitioner-authoring or validating questions, the following sources are the canonical references for procurement / source-to-pay reasoning:

- **PCAOB AS 2201**, *An Audit of Internal Control over Financial Reporting* — for SOX P2P control framing
- **AS 1301**, *Communications with Audit Committees*
- **COSO 2013** Internal Control – Integrated Framework
- **Incoterms 2020**, ICC Publication 723E
- **IRS Publication 1281**, *Backup Withholding for Missing and Incorrect Name/TINs*
- **IRS Publication 515**, *Withholding of Tax on Nonresident Aliens and Foreign Entities*
- **EU Council Directive 2006/112/EC** (VAT Directive) and Council Implementing Regulation 282/2011
- **UK VAT Act 1994** Schedule 4A; HMRC VAT Notice 741A
- **Excise Tax Act (Canada)** Schedule VI Part V (zero-rated exports of services)
- **OFAC** Specially Designated Nationals (SDN) list and FAQ on the 50% rule
- **BIS** Export Administration Regulations (EAR) Part 744 and Entity List
- **FinCEN** Beneficial Ownership Information rule (31 CFR §1010.380)
- **CIPS** Procurement and Supply Management body of knowledge
- **AICPA Audit Guide** sections on P2P controls

Citing primary sources rather than secondary summaries is what keeps the rubric defensible during peer review.

## Pending work (in priority order)

1. Walk `analysis/comparison_<run>.md` for every non-2 score; classify (a)/(b)/(c); make narrow rubric edits where warranted.
2. Convert `ideal_answer` from polished prose to step-by-step reasoning traces — pushes the artifact from step-4-only to step-2-adjacent.
3. Expand from 10 to 30-50 questions covering more failure modes.
4. Cross-grader run (different model family as judge) to retire self-grading bias.
5. Manual scoring on a subset → inter-rater agreement statistics.
6. Multi-turn / agentic version of select questions (give the model real tools to call; score on tool-use trajectory). Scope = significant.

## References (paper-style citation list)

- Mateega, S., Georgescu, C., & Tang, D. (2025). *FinanceQA: A Benchmark for Evaluating Financial Analysis Capabilities of Large Language Models*. AfterQuery. Hugging Face dataset: `AfterQuery/FinanceQA`.
- Holthausen, R. W., & Zmijewski, M. E. (2014). *Corporate valuation: theory, evidence & practice* (2nd ed.). Cambridge Business Publishers.
- Koller, T., Goedhart, M., & Wessels, D. (2020). *Valuation: Measuring and Managing the Value of Companies* (7th ed.). John Wiley & Sons.
- SEC Staff Accounting Bulletin No. 99 (1999), *Materiality*.
- PCAOB AS 2201, *An Audit of Internal Control over Financial Reporting*.
- COSO 2013, *Internal Control – Integrated Framework*.
- ICC Publication 723E, *Incoterms 2020*.
- IRS Publication 1281; IRS Publication 515.
- EU Council Directive 2006/112/EC; Council Implementing Regulation 282/2011.

