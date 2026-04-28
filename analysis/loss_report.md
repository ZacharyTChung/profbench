# ProfBench loss-analysis report

_Run `c65d76c7-bf3a-4cb7-a7fb-23a92ba83b83` · scorer filter: `all` · generated 2026-04-28T08:41:56+00:00_

## Executive summary

**claude-opus-4-7** leads with an average score of **1.8** (90.0% of max). The next-best model, **claude-sonnet-4-6**, trails by **0.3** on a 0–2 scale (1.5, 75.0% of max).

## Score table — per model

| model             |   n |   avg_score |   pct_of_max |
|:------------------|----:|------------:|-------------:|
| claude-opus-4-7   |  10 |         1.8 |           90 |
| claude-sonnet-4-6 |  10 |         1.5 |           75 |
| claude-haiku-4-5  |  10 |         1.1 |           55 |

## Score table — model × category

| model             |   close_and_controls |   invoice_processing |   supplier_data |   trade_and_tax |
|:------------------|---------------------:|---------------------:|----------------:|----------------:|
| claude-haiku-4-5  |                  1.5 |                1.333 |             1   |           0.667 |
| claude-opus-4-7   |                  2   |                1.667 |             1.5 |           2     |
| claude-sonnet-4-6 |                  2   |                1.667 |             1   |           1.333 |

## Score table — model × difficulty

| model             |   easy |   hard |   medium |
|:------------------|-------:|-------:|---------:|
| claude-haiku-4-5  |    1   |   1.25 |     1    |
| claude-opus-4-7   |    1   |   2    |     2    |
| claude-sonnet-4-6 |    1.5 |   1.75 |     1.25 |

## Score distribution (0 / 1 / 2 counts per model)

| model             |   score_0 |   score_1 |   score_2 |
|:------------------|----------:|----------:|----------:|
| claude-haiku-4-5  |         1 |         7 |         2 |
| claude-opus-4-7   |         0 |         2 |         8 |
| claude-sonnet-4-6 |         1 |         3 |         6 |

## Failure taxonomy

| Rank | Failure mode | Model | Score=0 count | Example question(s) |
| ---- | ------------ | ----- | ------------- | ------------------- |
| 1 | applying domain conventions | `claude-sonnet-4-6` | 1 | `q_005` |
| 2 | applying domain conventions (cross-border tax) | `claude-haiku-4-5` | 1 | `q_006` |

## Model-specific findings

### `claude-opus-4-7`
- Average score **1.8** (90.0% of max), n=10.
- distribution → 0s: 0, 1s: 2, 2s: 8.
- Strongest category: **close_and_controls** (avg 2.0). Weakest: **supplier_data** (avg 1.5).

### `claude-sonnet-4-6`
- Average score **1.5** (75.0% of max), n=10.
- distribution → 0s: 1, 1s: 3, 2s: 6.
- Strongest category: **close_and_controls** (avg 2.0). Weakest: **supplier_data** (avg 1.0).

### `claude-haiku-4-5`
- Average score **1.1** (55.0% of max), n=10.
- distribution → 0s: 1, 1s: 7, 2s: 2.
- Strongest category: **close_and_controls** (avg 1.5). Weakest: **trade_and_tax** (avg 0.667).

## Inter-rater agreement (human vs. auto)

_No responses have both human and auto scores yet — agreement statistics are unavailable._

## Implications

- **Domain-level weak categories** (mean across all models < 1.5): `supplier_data` (avg 1.17), `trade_and_tax` (avg 1.33). These are where the benchmark is doing real work — all models leak score here, so additional training data and rubric depth in these categories has the highest leverage.
- **Most discriminating categories** (largest score spread across models): `trade_and_tax` (spread 1.33), `close_and_controls` (spread 0.50). These categories separate frontier from smaller models and are the strongest candidates for an evaluation-only public release.
- **Highest-volume failure mode:** _applying domain conventions (cross-border tax)_ (1 score=0 occurrences). Targeted training data should prioritize worked examples in this mode.
- **Headroom for the leading model** (`claude-opus-4-7`): 0.2 points to ceiling. Calibrate the rubric (`scripts/compare.py`) before declaring this a true gap — score=1 responses may be rubric-too-narrow.
- **Score=1 share is 40.0% of all gradings** — calibration recommended. Run `python scripts/compare.py <run_id> 1` and triage each as (a) genuine model failure, (b) ideal_answer too narrow, or (c) rubric miscalibrated. Edits in (b)/(c) materially change the shape of the loss taxonomy above.
- **Annotation budget:** current pilot is **n=10** questions. To move from a pilot to a defensible Market-Bench-style submission, target 30–50 questions minimum — focus expansion on the weak categories above.