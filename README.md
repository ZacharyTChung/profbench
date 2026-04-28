# ProfBench

A domain-specific LLM evaluation harness in the style of FinanceQA, Market-Bench,
and IDE-Bench. This instance targets **procurement / source-to-pay** reasoning:
supplier master data, purchase orders and non-PO spend, invoice processing,
trade compliance (Incoterms, W-8/1042-S, EU VAT), period-close accruals, and
SOX P2P controls.

ProfBench is built around the [AfterQuery](https://afterquery.com/) workflow —
expert-in-the-loop authoring of questions, ideal answers, and rubrics, scored
either manually in a Streamlit UI or by Claude as autograder. See
[METHODOLOGY.md](METHODOLOGY.md) for how this maps to the AfterQuery data
generation pipeline.

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

- **Task categories.** `supplier_data`, `invoice_processing`, `trade_and_tax`,
  `close_and_controls` — covering supplier master/dedupe/risk, PO and non-PO
  processing including 3-way match and duplicate detection, Incoterms and
  cross-border tax, and period-close/SOX P2P controls.
- **Difficulty levels.** `easy` / `medium` / `hard`. Trivia excluded.
- **Rubric.** Three-level per question:
  - `0` — incorrect or missing key reasoning
  - `1` — correct approach but incomplete or with minor errors
  - `2` — correct, complete, and professional-grade
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

_See `analysis/loss_report.md` and `leaderboard/leaderboard.md` for the
latest run. Pilot results across the Claude family are in those files
(generated from `python -m leaderboard.generate --run-id ...`)._

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

## Status (v0.1)

- ✅ 10 questions across 4 categories, 3 difficulties
- ✅ Eval harness, autograder, leaderboard, auto-derived loss implications, HF export
- ✅ Multi-model pilot run (Opus 4.7, Sonnet 4.6, Haiku 4.5) — see `leaderboard/leaderboard.md`
- ✅ Anchor data for q_001 (supplier dedupe), q_004 (duplicate detection), q_009 (sanctions)
- ✅ Reasoning-trace template (`data/traces/q_003_template.md`) — pending practitioner fill
- ⚠ Ideal answers are first-pass; awaiting full expert validation (see `analysis/triage_score1.md`)
- ⚠ Single domain expert (no peer review yet)
- ⚠ Self-grading bias when Opus 4.7 is among evaluated models (also acts as judge)
- ☐ Reasoning traces filled in (template exists for q_003; replicate for all 10)
- ☐ Expansion to 30+ questions
- ☐ Cross-grader run with non-Anthropic judge (requires OpenAI / Google key)

## Citation

```bibtex
@misc{profbench2026,
  title  = {ProfBench: A domain-specific LLM benchmark for procurement / source-to-pay reasoning},
  author = {Chung, Zachary T.},
  year   = {2026},
  note   = {Version 0.1.0}
}
```
