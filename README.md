# ProfBench

A domain-specific LLM evaluation harness modeled directly on the
[FinanceQA](https://huggingface.co/datasets/AfterQuery/FinanceQA) paper
(Mateega, Georgescu, Tang — AfterQuery, 2025). Same question taxonomy
(tactical / conceptual; tactical sub-divided into basic / assumption-based),
same exact-match scoring as the headline metric, same emphasis on real-world
on-the-job tasks rather than context-first benchmark designs.

This instance targets **procurement / source-to-pay** reasoning instead of
finance: supplier master data, purchase orders and non-PO spend, invoice
processing, trade compliance (Incoterms, W-8/1042-S, EU VAT, Section 301
tariffs), period-close accruals, and SOX P2P controls.

ProfBench is built around the [AfterQuery](https://afterquery.com/) workflow —
expert-in-the-loop authoring of questions, ideal answers, and rubrics, scored
either manually in a Streamlit UI or by Claude as autograder. See
[METHODOLOGY.md](METHODOLOGY.md) for the full FinanceQA-aligned methodology
and the AfterQuery pipeline mapping.

> **v0.3 framing note.** The author has operational depth in supplier-data /
> procurement-operations and shallower depth in trade-and-tax and SOX / close
> controls. Where practitioner experience does not extend, reasoning-trace
> drafts are written in **cited-authority style** (anchored to PCAOB AS 2201,
> COSO 2013, OFAC FAQ, FinCEN BOI, IRS Pub 1281/515, Incoterms 2020, etc.)
> rather than working-practitioner voice. This is eval-defensible but a
> knowingly weaker substitute for AfterQuery-grade SFT data. See
> [METHODOLOGY.md § Authorship constraint](METHODOLOGY.md#authorship-constraint)
> and [REVIEW_REQUEST.md](REVIEW_REQUEST.md) for the external-review plan.

## What is ProfBench

A local toolkit that lets a domain expert: (1) curate a question bank of hard,
realistic professional tasks, (2) run one or more LLMs over those tasks via
API, (3) score responses against a 0–2 rubric (manually or via Claude
autograder), and (4) generate a loss-analysis report, comparative leaderboard,
and Hugging Face-ready dataset export.

## Motivation

Frontier models post strong scores on broad knowledge benchmarks but
consistently underperform on domain-specific professional reasoning — applying
domain conventions, generating assumptions, multi-step arithmetic, and
reconciling ambiguous facts. ProfBench is designed to surface those gaps in
procurement work and produce the loss taxonomy needed to target them with
future training data.

## Benchmark design

- **Question taxonomy** (FinanceQA-aligned):
  - `question_type` — `tactical` (context-bound, applied) or `conceptual` (no context, principles)
  - `requires_assumption` — bool; tactical questions where the responder must infer something not stated. **The killer category** — FinanceQA shows frontier models score <5% here.
  - `source_grounded` — bool; context drawn from a real public document (e.g. SEC filing, OFAC SDN, USAspending record)
- **Domain categories.** `supplier_data`, `invoice_processing`, `trade_and_tax`,
  `close_and_controls` — orthogonal to question type; describes the procurement
  subdomain.
- **Difficulty levels.** `easy` / `medium` / `hard`. Trivia excluded.
- **Rubric.** Three-level per question:
  - `0` — incorrect or missing key reasoning
  - `1` — correct approach but incomplete or with minor errors
  - `2` — correct, complete, and professional-grade
- **Scoring (two metrics).**
  - **Average rubric score (0-2)** — granular, useful for calibration.
  - **Binary exact-match (% scoring 2/2)** — the FinanceQA-paper-aligned
    headline metric. "No partial credit" matches the operational reality that
    an 80% answer in finance / procurement still requires line-by-line
    verification by a human.
- **Failure modes.** Every question is tagged with an `expected_failure_mode`
  so loss analysis can group questions by the kind of reasoning they stress.
- **Anchor data.** Real public records (USAspending, Chicago Payments, OFAC
  SDN) live under `data/anchors/`, mapped per-question, to ground scenarios in
  reality without exposing any private data.

## Quick start

```bash
# 1. Install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# edit .env and paste your real ANTHROPIC_API_KEY

# 3. Smoke test (no API calls)
python -m runner.eval run --dry-run --limit 3

# 4. Run the eval (default = Sonnet 4.6)
python -m runner.eval run --models sonnet
# or run multiple Claude family members in one command:
python -m runner.eval run --models opus,sonnet,haiku
# capture the printed run_id

# 5. Auto-score with Claude as judge (Opus 4.7 by default)
python -m scorer.autoscore --run-id <run_id>

# 6. Generate analysis, leaderboard, dataset export
python -m analysis.report --run-id <run_id>
python -m leaderboard.generate --run-id <run_id>
python -m data.export --run-id <run_id>

# 7. Side-by-side review for rubric calibration
python scripts/compare.py <run_id>           # all questions
python scripts/compare.py <run_id> 1         # only the score=1 ones

# 8. After editing data/questions.json, refresh the DB without bumping ids
python -m runner.eval refresh-questions
# (or pass --refresh-questions to a `run` invocation to do both at once)
```

Optional: `streamlit run scorer/app.py` for human rubric scoring (writes to
the same DB as `scorer_type='human'`; auto-vs-manual agreement is reported by
`analysis/report.py`).

## Model aliases

Defined in `runner/models.py`:

| Alias | Model |
| ----- | ----- |
| `claude` / `sonnet` | Claude Sonnet 4.6 |
| `opus` | Claude Opus 4.7 |
| `haiku` | Claude Haiku 4.5 |
| `gpt4o` | OpenAI GPT-4o (requires `OPENAI_API_KEY`) |

Add a new model = subclass `ModelClient` and add to `MODEL_REGISTRY`.

## Results

Latest pilot run (18 questions, Claude family, Opus 4.7 as judge):

| Model | Avg (0–2) | Exact match (FinanceQA-style) |
| ----- | --------- | ----------------------------- |
| Claude Opus 4.7 | 1.833 (91.7%) | 83.3% |
| Claude Sonnet 4.6 | 1.611 (80.6%) | 61.1% |
| Claude Haiku 4.5 | 1.167 (58.3%) | 22.2% |

Full breakdown by category × difficulty in `analysis/loss_report.md`;
generated by `python -m leaderboard.generate --run-id <run_id>`.

## Failure analysis

`analysis/loss_report.md` breaks down score by model × category × difficulty
and includes auto-derived implications (universal weak categories, most
discriminating categories, calibration prompts, annotation-budget heuristics)
based on the actual run data — no manual fill-in.

For per-response review: `scripts/compare.py <run_id>` produces a side-by-side
review file (`analysis/comparison_<run>.md`) structured for rubric calibration.
For each non-2 score, decide whether the model genuinely fell short, the
ideal answer was too narrow, or the rubric was miscalibrated.

`analysis/triage_score1.md` (when present) is a pre-categorized triage of
score-1 responses — AI-generated best-guess (a)/(b)/(c) classifications for
the practitioner to review/override.

## Dataset

The Hugging Face-ready export lives at
[data/profbench_export.json](data/profbench_export.json). Bundles questions,
responses, and scores for the most recent run.

## Methodology

See [METHODOLOGY.md](METHODOLOGY.md) for the full workflow description and the
mapping to AfterQuery's expert-in-the-loop data generation pipeline.

## Code tour

See [CODE_TOUR.md](CODE_TOUR.md) for a top-to-bottom walkthrough of the
codebase — the data flow, per-module purpose, database schema, and
"I want to do X" recipes.

## Status (v0.3)

- ✅ 18 questions across 4 categories, 3 difficulties (15 tactical / 3 conceptual; 4 require assumption; 3 source-grounded)
- ✅ Eval harness, autograder, leaderboard, auto-derived loss implications, HF export
- ✅ Multi-model pilot run on full 18Q (Opus 4.7, Sonnet 4.6, Haiku 4.5) — numbers above; see `leaderboard/leaderboard.md`
- ✅ Anchor data for q_001 (supplier dedupe), q_004 (duplicate detection), q_009 (sanctions)
- ✅ Cited-authority reasoning traces for **all 18 questions** (`data/traces/`) — anchored to PCAOB / COSO / OFAC / FinCEN / IRS / Incoterms / EU VAT Directive / Excise Tax Act primary sources rather than working-practitioner voice (see [METHODOLOGY.md § Authorship constraint](METHODOLOGY.md#authorship-constraint))
- ✅ Cross-grader judge support (`scorer.autoscore --judge gpt4o`) — non-Anthropic key retires self-grading bias on demand
- ✅ q_003 rubric calibrated to accept both tolerance conventions (`<` and `≤`) per `analysis/triage_score1.md`
- ✅ Score-1 triage written for the latest run (`analysis/triage_score1.md`)
- ⚠ Author depth is uneven across categories: operational depth in `supplier_data`; cited-authority-only in `trade_and_tax` and `close_and_controls`. External SME validation pending — see [REVIEW_REQUEST.md](REVIEW_REQUEST.md)
- ⚠ Single grader (no peer review yet)
- ⚠ Self-grading bias when Opus 4.7 is among evaluated models (also acts as judge)
- ☐ External SME review of cited-authority traces and `ideal_answer` fields ([REVIEW_REQUEST.md](REVIEW_REQUEST.md))
- ☐ Expansion to 30+ questions (18 of 30 done) — skewing toward assumption-based and source-grounded
- ☐ Execute a cross-grader run (code wired; needs `OPENAI_API_KEY` or equivalent in `.env`)
- ☐ Manual scoring on a subset via `scorer/app.py` to populate inter-rater agreement

## Citation

```bibtex
@misc{profbench2026,
  title  = {ProfBench: A domain-specific LLM benchmark for procurement / source-to-pay reasoning},
  author = {Chung, Zachary T.},
  year   = {2026},
  note   = {Version 0.3.0}
}
```
