# ProfBench loss-analysis report

_Run `1af59657-b7b7-48c1-8695-d18f27040d68` · scorer filter: `all` · generated 2026-04-28T19:17:37+00:00_

## Executive summary

**claude-opus-4-7** leads with an average score of **1.933** (96.7% of max). The next-best model, **claude-sonnet-4-6**, trails by **0.333** on a 0–2 scale (1.6, 80.0% of max).

## Score table — per model

| model             |   n |   avg_score |   pct_of_max |
|:------------------|----:|------------:|-------------:|
| claude-opus-4-7   |  15 |       1.933 |         96.7 |
| claude-sonnet-4-6 |  15 |       1.6   |         80   |
| claude-haiku-4-5  |  15 |       1.133 |         56.7 |

## Score table — model × category

| model             |   close_and_controls |   invoice_processing |   supplier_data |   trade_and_tax |
|:------------------|---------------------:|---------------------:|----------------:|----------------:|
| claude-haiku-4-5  |                  1.5 |                1.333 |            1.25 |           0.833 |
| claude-opus-4-7   |                  2   |                2     |            2    |           1.833 |
| claude-sonnet-4-6 |                  2   |                1.333 |            1.5  |           1.667 |

## Score table — model × difficulty

| model             |   easy |   hard |   medium |
|:------------------|-------:|-------:|---------:|
| claude-haiku-4-5  |      1 |    1.2 |    1.125 |
| claude-opus-4-7   |      2 |    2   |    1.875 |
| claude-sonnet-4-6 |      1 |    1.6 |    1.75  |

## Score distribution (0 / 1 / 2 counts per model)

| model             |   score_0 |   score_1 |   score_2 |
|:------------------|----------:|----------:|----------:|
| claude-haiku-4-5  |         1 |        11 |         3 |
| claude-opus-4-7   |         0 |         1 |        14 |
| claude-sonnet-4-6 |         0 |         6 |         9 |

## Failure taxonomy

| Rank | Failure mode | Model | Score=0 count | Example question(s) |
| ---- | ------------ | ----- | ------------- | ------------------- |
| 1 | applying domain conventions | `claude-haiku-4-5` | 1 | `q_005` |

## Model-specific findings

### `claude-opus-4-7`
- Average score **1.933** (96.7% of max), n=15.
- distribution → 0s: 0, 1s: 1, 2s: 14.
- Strongest category: **close_and_controls** (avg 2.0). Weakest: **trade_and_tax** (avg 1.833).

### `claude-sonnet-4-6`
- Average score **1.6** (80.0% of max), n=15.
- distribution → 0s: 0, 1s: 6, 2s: 9.
- Strongest category: **close_and_controls** (avg 2.0). Weakest: **invoice_processing** (avg 1.333).

### `claude-haiku-4-5`
- Average score **1.133** (56.7% of max), n=15.
- distribution → 0s: 1, 1s: 11, 2s: 3.
- Strongest category: **close_and_controls** (avg 1.5). Weakest: **trade_and_tax** (avg 0.833).

## Inter-rater agreement (human vs. auto)

_No responses have both human and auto scores yet — agreement statistics are unavailable._

## Implications

- **Domain-level weak categories** (mean across all models < 1.5): `trade_and_tax` (avg 1.44). These are where the benchmark is doing real work — all models leak score here, so additional training data and rubric depth in these categories has the highest leverage.
- **Most discriminating categories** (largest score spread across models): `trade_and_tax` (spread 1.00), `supplier_data` (spread 0.75). These categories separate frontier from smaller models and are the strongest candidates for an evaluation-only public release.
- **Highest-volume failure mode:** _applying domain conventions_ (1 score=0 occurrences). Targeted training data should prioritize worked examples in this mode.
- **Score=1 share is 40.0% of all gradings** — calibration recommended. Run `python scripts/compare.py <run_id> 1` and triage each as (a) genuine model failure, (b) ideal_answer too narrow, or (c) rubric miscalibrated. Edits in (b)/(c) materially change the shape of the loss taxonomy above.
- **Annotation budget:** current pilot is **n=15** questions. To move from a pilot to a defensible Market-Bench-style submission, target 30–50 questions minimum — focus expansion on the weak categories above.