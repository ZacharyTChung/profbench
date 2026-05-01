# ProfBench code tour

A reading guide for the ProfBench codebase. Read this top-to-bottom and
you should be able to navigate the repo without grep.

For *what* the project does and *why*, see [README.md](README.md) and
[METHODOLOGY.md](METHODOLOGY.md). This file is about the **code**.

Every Python file in the repo has a module-level docstring at the top of
the file — read that for the per-file scope. This tour explains the
**connections between modules** that no single docstring can show.

---

## 5-minute read

If you have five minutes, read these three things in order:

1. [`runner/__init__.py`](runner/__init__.py) — the SQLite schema (3
   tables: `questions`, `responses`, `scores`). Understanding these
   tables is enough to understand the rest of the system.
2. [`runner/eval.py:142-240`](runner/eval.py) — the `run` command.
   This is the central loop: load questions → call models → write
   responses to DB.
3. [`scorer/autoscore.py:57-97`](scorer/autoscore.py) — the autograder.
   This is where the rubric meets the response and produces a 0/1/2.

Everything else (analysis, leaderboard, export) reads from the same
three tables and turns them into reports.

---

## Repository layout

```
profbench/
├── README.md              # public-facing summary, status, results table
├── METHODOLOGY.md         # how the benchmark was built and the AfterQuery mapping
├── REVIEW_REQUEST.md      # SME outreach materials
├── CODE_TOUR.md           # you are here
├── requirements.txt       # pinned Python dependencies
│
├── runner/                # eval orchestration + DB helpers + model API wrappers
│   ├── __init__.py        # SQLite schema, get_db(), init_db(), now_iso()
│   ├── eval.py            # CLI: `run`, `refresh-questions`, `list-runs`
│   └── models.py          # ClaudeClient / OpusClient / HaikuClient / GPT4oClient
│
├── scorer/                # grading: autograder + Streamlit UI for human scoring
│   ├── __init__.py        # package marker
│   ├── autoscore.py       # CLI: `python -m scorer.autoscore --run-id <id>`
│   └── app.py             # Streamlit UI: `streamlit run scorer/app.py`
│
├── analysis/              # post-run analytics
│   ├── __init__.py        # package marker
│   ├── stats.py           # pure-function aggregations over the scores table
│   ├── report.py          # CLI: produces analysis/loss_report.md
│   ├── loss_report.md     # latest generated loss-analysis report
│   ├── triage_score1.md   # hand-written triage of score-1 responses
│   └── comparison_<run>.md  # side-by-side review files (one per script run)
│
├── leaderboard/           # cross-model leaderboard
│   ├── __init__.py        # package marker
│   ├── generate.py        # CLI: writes leaderboard.md + leaderboard.html
│   ├── leaderboard.md     # latest markdown leaderboard
│   └── leaderboard.html   # latest single-file HTML leaderboard
│
├── data/                  # questions, anchor data, traces, dataset export
│   ├── __init__.py        # package marker
│   ├── questions.json     # the 18-question benchmark itself (source of truth)
│   ├── export.py          # CLI: writes data/profbench_export.json (HF format)
│   ├── profbench_export.json  # latest Hugging Face-ready export
│   ├── anchors/           # real public records used to ground question scenarios
│   │   ├── _build_anchors.py    # one-shot anchor builder
│   │   ├── README.md            # documents what each anchor file contains
│   │   └── anchor_q*.json + raw json/csv pulls
│   └── traces/            # reasoning-trace drafts (cited-authority style in v0.3)
│       ├── q_001_template.md / q_001_trace.md
│       ├── q_003_template.md / q_003_trace.md
│       └── q_010_template.md / q_010_trace.md
│
├── scripts/               # standalone utilities not part of the runtime pipeline
│   └── compare.py         # builds analysis/comparison_<run>.md
│
└── db/                    # SQLite database (gitignored)
    └── profbench.db       # created on first run; schema in runner/__init__.py
```

---

## The data flow

The system has one canonical pipeline. Most CLIs are stages in it:

```
data/questions.json
        │
        │  (1) python -m runner.eval run --models <aliases>
        │       loads questions → calls each model → writes to `responses` table
        ▼
   ┌─────────────┐
   │  responses  │  (one row per question × model × run)
   └─────┬───────┘
         │
         │  (2) python -m scorer.autoscore --run-id <id>
         │       reads responses → calls Opus 4.7 as grader → writes to `scores` table
         │
         │  (2b, optional) streamlit run scorer/app.py
         │       human reviewer scores responses through the UI → also writes to `scores`
         ▼
   ┌─────────────┐
   │   scores    │  (one row per response × scorer_type, where scorer_type ∈ {auto, human})
   └─────┬───────┘
         │
         ├─ python -m analysis.report --run-id <id>      → analysis/loss_report.md
         ├─ python -m leaderboard.generate --run-id <id> → leaderboard/leaderboard.{md,html}
         ├─ python -m data.export --run-id <id>          → data/profbench_export.json
         └─ python scripts/compare.py <run_id> [score]   → analysis/comparison_<run>.md
```

Every stage reads from SQLite (`db/profbench.db`) keyed by `run_id`.
The `run_id` is a UUID created in step (1) and printed to stdout —
keep it; every downstream stage takes it as an argument.

---

## Module-by-module tour

### `runner/`

**`runner/__init__.py`** — The package init does double duty as the
**database module**. It defines `SCHEMA` (three CREATE TABLE statements
+ four indexes), exports `get_db()` for connections, and `init_db()`
which creates tables and runs ALTER-TABLE migrations for older DBs that
predate the FinanceQA-aligned columns (added in v0.2.0). When you
need to query the DB from anywhere else in the codebase, you import
`from runner import get_db, init_db, now_iso`.

**`runner/eval.py`** — Three Typer CLI commands:

- `run` — the central loop. Optional `--models` (comma-separated
  aliases like `claude,opus,haiku,gpt4o`), `--limit`, `--ids`,
  `--dry-run`, `--refresh-questions`. Generates a fresh UUID, calls
  each model on each question, writes responses with `tokens_used` and
  `latency_ms`. The `--dry-run` flag short-circuits before any API
  call — useful for verifying prompts.
- `refresh-questions` — re-reads `data/questions.json` and UPDATEs
  existing rows in place. Use after editing question text, ideal
  answers, or rubrics so changes take effect without bumping ids or
  wiping the DB. Past responses/scores are preserved.
- `list-runs` — table of all run UUIDs grouped by `(run_id, model)`
  with timestamps and counts.

The internal helper `_load_questions_into_db(refresh: bool)` is the
function to read if you want to understand how `data/questions.json`
becomes the `questions` table.

**`runner/models.py`** — Defines a small `ModelClient` abstract base
class with a single `complete(question, context) -> dict` method, plus
concrete subclasses:

- `ClaudeClient` (Sonnet 4.6 by default) — uses the Anthropic SDK with
  the `messages.create` API.
- `OpusClient` and `HaikuClient` — subclasses of `ClaudeClient` that
  only override the `name` (model id) field.
- `GPT4oClient` — uses the OpenAI SDK with `chat.completions.create`.

The `MODEL_REGISTRY` dict at the bottom maps short aliases to client
classes. `build_client(alias)` instantiates one. All clients use
`_retry()` (exponential backoff, max 3 attempts) for transient
failures. API keys come from `.env` via `python-dotenv`. Adding a
new model = subclass `ModelClient`, implement `complete()`, register
in `MODEL_REGISTRY`.

The `SYSTEM_PROMPT` constant at the top is shared across all clients
and is also exposed for `--dry-run` to show what would be sent.

### `scorer/`

**`scorer/autoscore.py`** — Claude as autograder.
The `autoscore(question, response, rubric)` function builds a single
user message containing the question, ideal answer, rubric, and
candidate response, sends it to `AUTOGRADER_MODEL` (Opus 4.7), and
parses the returned JSON `{score, reasoning, confidence}`. The
`_extract_json` helper is forgiving — it tolerates fenced code blocks
and stray preamble.

The `score` CLI command reads all responses for a run, calls
`autoscore()` on each, and writes results to the `scores` table with
`scorer_type='auto'`. `--overwrite` re-grades responses that already
have an auto score; otherwise they're skipped.

**`scorer/app.py`** — A single-file Streamlit UI for human scoring.
Sidebar lets the reviewer pick a run + model + "unscored only" filter.
Main panel shows one response at a time with the ideal answer hidden
behind an expander (so the reviewer scores against the rubric first).
Saves write to the `scores` table with `scorer_type='human'`. There's
no auth or multi-user state — it's a personal tool for one reviewer.

### `analysis/`

**`analysis/stats.py`** — Pure functions, no side effects. Each
function reads from SQLite via `_scores_dataframe()` and returns a
pandas DataFrame:

- `per_model_average` — average score, % of max, FinanceQA-style
  binary exact-match (% scoring 2/2). Sorts descending by avg.
- `per_question_type` — FinanceQA's tactical-basic /
  tactical-assumption / conceptual breakdown.
- `per_category`, `per_difficulty` — same shape, different group-by.
- `failure_mode_frequency` — count of score=0 responses grouped by
  `expected_failure_mode` and model.
- `score_distribution` — 0/1/2 histogram per model.
- `inter_rater_agreement` — when both human and auto scores exist on
  the same `response_id`, computes exact-match, within-±1, and mean
  absolute difference.
- `example_failures` — for each failure mode, returns a few example
  question_ids that scored 0 (used in the loss report's failure
  taxonomy table).

If you want to add a new analytic, this is the file. Keep functions
pure: `analysis/report.py` is what calls them and renders the markdown.

**`analysis/report.py`** — Reads from `stats.py`, produces
`analysis/loss_report.md`. The markdown has eight sections including
an **auto-derived implications** section (`_implications()`) that
turns the dataframes into bulleted insights without hand-editing —
e.g., "universal weak categories (mean < 1.5)", "most discriminating
categories (largest score spread across models)", "score-1 share is
{X}% — calibration recommended".

### `leaderboard/`

**`leaderboard/generate.py`** — Reads from `analysis/stats.py`,
produces both a markdown leaderboard and a self-contained HTML page
(no external CSS/JS — the styles are embedded in `HTML_TEMPLATE` as a
string). Per-model cards show avg score, % of max, n, best/worst
category. The HTML is self-hostable; the markdown drops into a README
or Hugging Face dataset card.

### `data/`

**`data/export.py`** — Bundles questions + one run's responses +
those responses' scores into a single JSON in the shape Hugging Face
expects. Writes to `data/profbench_export.json`. The `metadata` block
records `version`, `domain`, `categories`, `created_at`, plus the
question-bank size. The `--run-id` flag is optional: omit to export a
question-bank-only dataset (no model responses).

**`data/anchors/_build_anchors.py`** — One-shot script that turns
raw fetched JSON / CSV (`lockheed_autocomplete.json`,
`chicago_payments_raw.json`, `ofac_sdn.csv`, etc.) into per-question
anchor files (`anchor_q001_supplier_dedupe.json`,
`anchor_q004_duplicate_detection.json`,
`anchor_q009_sanctions_screening.json`). Run from `data/anchors/`;
idempotent. The raw files are checked in so anyone can rebuild
without re-hitting the source APIs.

### `scripts/`

**`scripts/compare.py`** — Standalone utility (not a Typer CLI; just
`python scripts/compare.py <run_id> [score_filter]`). Joins
`questions × responses × scores` for a run and writes a
side-by-side markdown file (`analysis/comparison_<run>.md`). Each
question entry shows: question, context, rubric, ideal answer, model
response, grader verdict, plus a fill-in slot for the (a)/(b)/(c)
calibration triage described in METHODOLOGY.md.

The optional second argument filters to a single score value
(typically `1` to triage the borderline cases). Output filename gets
a `_score{N}` suffix when filtered.

---

## Database schema

Defined in [`runner/__init__.py:19-66`](runner/__init__.py). Three
tables:

### `questions`

The benchmark itself, loaded from `data/questions.json` on first run
and refreshed via `runner.eval refresh-questions`. Columns include
`id` (PK), `domain`, `category`, `difficulty`, `question`, `context`,
`ideal_answer`, `rubric` (JSON-encoded text), `expected_failure_mode`,
plus the FinanceQA-aligned tagging columns added in v0.2.0:
`question_type`, `requires_assumption`, `source_grounded`,
`source_doc`. The migration in `init_db()` ALTERs older DBs to add
those columns.

### `responses`

One row per `(question_id, model, run_id)`. Stores the raw model
response, `tokens_used`, `latency_ms`, and the run UUID. Foreign-keyed
to `questions(id)`. Indexes on `run_id` and `model` keep the
common queries fast.

### `scores`

One row per `(response_id, scorer_type)`. `scorer_type` is
`'auto'` (autograder) or `'human'` (Streamlit UI). The same response
can have both an auto score and a human score — that's how
`stats.inter_rater_agreement()` finds pairs to compare. `scorer_notes`
is JSON for auto scores (`{reasoning, confidence}`) and free text for
human scores.

---

## Common workflows

### "I want to add a new model"

1. Open `runner/models.py`.
2. Subclass `ModelClient`, implement `complete(question, context)` to
   return `{response, tokens, latency_ms}`. The `_retry()` helper is
   already available — wrap your API call in a callable and pass it.
3. Add an entry to `MODEL_REGISTRY` mapping a short alias to your
   class.
4. Run with `python -m runner.eval run --models <your-alias>`.

### "I want to edit a question and re-grade against the new rubric"

1. Edit `data/questions.json`. Don't bump the id.
2. `python -m runner.eval refresh-questions` (updates the DB row).
3. `python -m scorer.autoscore --run-id <id> --overwrite` (re-grades
   the same responses against the new rubric).
4. `python -m analysis.report --run-id <id>` to see the new scores.

### "I want to inspect why a model got a 1 on a question"

1. `python scripts/compare.py <run_id> 1` — produces
   `analysis/comparison_<run_id>_score1.md` filtered to score-1
   responses only.
2. Read the file. For each row, decide whether (a) the model fell
   short, (b) the ideal answer was too narrow, or (c) the rubric was
   miscalibrated.
3. (b) and (c) justify edits to `data/questions.json` followed by the
   refresh + re-grade workflow above.

### "I want to add a new analytic to the loss report"

1. Open `analysis/stats.py`. Write a new pure function that returns a
   DataFrame.
2. Open `analysis/report.py`. Import your function from `stats`, call
   it inside `generate_cmd`, render its DataFrame into the report
   sections list.
3. (Optional) If the analytic should drive an auto-derived implication,
   add a branch to `_implications()` that inspects the DataFrame and
   appends a bullet.

### "I want to publish the dataset to Hugging Face"

1. `python -m data.export --run-id <id>` — produces
   `data/profbench_export.json`.
2. The JSON has a top-level `metadata` block, a `questions` array, and
   a `results` block with this run's responses + scores. Check the
   `version` field in `data/export.py:27` and bump it before any new
   public release.
3. Upload `data/profbench_export.json` along with README content
   sourced from `README.md` and `METHODOLOGY.md`.

---

## Where to look first when something breaks

- **`ModuleNotFoundError`** — pip install missed a step. Run
  `pip install -r requirements.txt` inside the venv.
- **`ANTHROPIC_API_KEY is not set`** — `.env` not loaded.
  `runner/models.py` calls `load_dotenv()` at import; verify `.env`
  exists at the repo root and has the key.
- **`autograder returned non-JSON output`** — the grader's response
  failed `_extract_json()`. The raw text is in the exception message;
  most often it's a fenced-code-block edge case. Adjust the regex in
  `scorer/autoscore.py:44-54` if needed.
- **`No responses found for run_id=...`** — the run id is wrong (try
  `python -m runner.eval list-runs`) or the DB at `db/profbench.db`
  was wiped. Rebuilding the DB requires re-running the eval.
- **Streamlit UI shows no runs** — `db/profbench.db` is empty. Run an
  eval first, then refresh the page.
- **Scores look wrong after editing a question** — refresh the DB
  (`refresh-questions`) and re-grade with `--overwrite`. The `scores`
  table is keyed by `response_id`, not by question content, so old
  scores attached to the old responses persist until you overwrite.

---

*Document version 1.0 — created in v0.3, 2026-04-30. Update when
adding a module, a CLI command, or a database column.*
