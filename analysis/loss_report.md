# ProfBench loss-analysis report

_Run `1af59657-b7b7-48c1-8695-d18f27040d68` · scorer filter: `all` · generated 2026-04-29T21:52:12+00:00_

## Executive summary

**claude-opus-4-7** leads with an average score of **1.833** (91.7% of max, **83.3%** binary exact-match). The next-best model, **claude-sonnet-4-6**, trails by **0.222** on a 0–2 scale (1.611, 80.6% of max, 61.1% exact-match).

## Score table — per model

| model             |   n |   avg_score |   pct_of_max |   exact_match_pct |
|:------------------|----:|------------:|-------------:|------------------:|
| claude-opus-4-7   |  18 |       1.833 |         91.7 |              83.3 |
| claude-sonnet-4-6 |  18 |       1.611 |         80.6 |              61.1 |
| claude-haiku-4-5  |  18 |       1.167 |         58.3 |              22.2 |

## Score table — model × category

| model             |   close_and_controls |   invoice_processing |   supplier_data |   trade_and_tax |
|:------------------|---------------------:|---------------------:|----------------:|----------------:|
| claude-haiku-4-5  |                1.667 |                  1.2 |            1.25 |           0.833 |
| claude-opus-4-7   |                1.667 |                  2   |            1.75 |           1.833 |
| claude-sonnet-4-6 |                1.667 |                  1.6 |            1.5  |           1.667 |

## Score table — model × difficulty

| model             |   easy |   hard |   medium |
|:------------------|-------:|-------:|---------:|
| claude-haiku-4-5  |  1     |  1.333 |    1.111 |
| claude-opus-4-7   |  1.667 |  1.833 |    1.889 |
| claude-sonnet-4-6 |  1.333 |  1.5   |    1.778 |

## Score table — model × question type (FinanceQA-style)

_Tactical-basic = answerable from the context; tactical-assumption = requires inferring something not stated; conceptual = principles / no context. Per the FinanceQA paper, assumption-based questions are the killer category — frontier models score <5% there._

| model             |   conceptual |   tactical-assumption |   tactical-basic |
|:------------------|-------------:|----------------------:|-----------------:|
| claude-haiku-4-5  |        1.333 |                   1   |            1.182 |
| claude-opus-4-7   |        1.667 |                   2   |            1.818 |
| claude-sonnet-4-6 |        1.667 |                   1.5 |            1.636 |

**Binary exact-match rate (% scoring 2/2, FinanceQA convention):**

| model             |   conceptual |   tactical-assumption |   tactical-basic |
|:------------------|-------------:|----------------------:|-----------------:|
| claude-haiku-4-5  |         33.3 |                     0 |             27.3 |
| claude-opus-4-7   |         66.7 |                   100 |             81.8 |
| claude-sonnet-4-6 |         66.7 |                    50 |             63.6 |

## Score distribution (0 / 1 / 2 counts per model)

| model             |   score_0 |   score_1 |   score_2 |
|:------------------|----------:|----------:|----------:|
| claude-haiku-4-5  |         1 |        13 |         4 |
| claude-opus-4-7   |         0 |         3 |        15 |
| claude-sonnet-4-6 |         0 |         7 |        11 |

## Failure taxonomy

| Rank | Failure mode | Model | Score=0 count | Example question(s) |
| ---- | ------------ | ----- | ------------- | ------------------- |
| 1 | applying domain conventions | `claude-haiku-4-5` | 1 | `q_005` |

## Model-specific findings

### `claude-opus-4-7`
- Average score **1.833** (91.7% of max), n=18.
- distribution → 0s: 0, 1s: 3, 2s: 15.
- Strongest category: **invoice_processing** (avg 2.0). Weakest: **close_and_controls** (avg 1.667).

### `claude-sonnet-4-6`
- Average score **1.611** (80.6% of max), n=18.
- distribution → 0s: 0, 1s: 7, 2s: 11.
- Strongest category: **close_and_controls** (avg 1.667). Weakest: **supplier_data** (avg 1.5).

### `claude-haiku-4-5`
- Average score **1.167** (58.3% of max), n=18.
- distribution → 0s: 1, 1s: 13, 2s: 4.
- Strongest category: **close_and_controls** (avg 1.667). Weakest: **trade_and_tax** (avg 0.833).

## Inter-rater agreement (human vs. auto)

_No responses have both human and auto scores yet — agreement statistics are unavailable._

## Implications

- **Domain-level weak categories** (mean across all models < 1.5): `trade_and_tax` (avg 1.44). These are where the benchmark is doing real work — all models leak score here, so additional training data and rubric depth in these categories has the highest leverage.
- **Most discriminating categories** (largest score spread across models): `trade_and_tax` (spread 1.00), `invoice_processing` (spread 0.80). These categories separate frontier from smaller models and are the strongest candidates for an evaluation-only public release.
- **Highest-volume failure mode:** _applying domain conventions_ (1 score=0 occurrences). Targeted training data should prioritize worked examples in this mode.
- **Headroom for the leading model** (`claude-opus-4-7`): 0.167 points to ceiling. Calibrate the rubric (`scripts/compare.py`) before declaring this a true gap — score=1 responses may be rubric-too-narrow.
- **Score=1 share is 42.6% of all gradings** — calibration recommended. Run `python scripts/compare.py <run_id> 1` and triage each as (a) genuine model failure, (b) ideal_answer too narrow, or (c) rubric miscalibrated. Edits in (b)/(c) materially change the shape of the loss taxonomy above.
- **Annotation budget:** current pilot is **n=18** questions. To move from a pilot to a defensible Market-Bench-style submission, target 30–50 questions minimum — focus expansion on the weak categories above.