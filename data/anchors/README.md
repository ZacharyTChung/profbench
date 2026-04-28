# Anchor data for ProfBench questions

Real, public records pulled from government APIs. Each `anchor_q*.json` is
mapped to one question in `data/questions.json` and is intended to replace
synthesized values in that question's `context` so the scenario sits on real
data instead of made-up names/amounts.

## Files

| File | Anchors | Source | Use for |
| ---- | ------- | ------ | ------- |
| `anchor_q001_supplier_dedupe.json` | q_001 | USAspending.gov autocomplete API | Real recipient name variants — pick a pair to drop into q_001's `context` |
| `anchor_q004_duplicate_detection.json` | q_004 | data.cityofchicago.org Payments dataset (`s4vu-giwb`) | 35 real exact-duplicate clusters; top one is Heartland Human Care Services, $798,240.72 paid twice on contract 92320 |
| `anchor_q009_sanctions_screening.json` | q_009 | Treasury OFAC SDN list | 15 real SDN-listed entities/individuals/vessels stratified across Russia, Iran, cyber programs |

The other 7 questions (q_002, q_003, q_005, q_006, q_007, q_008, q_010) are
reasoning-driven — synthetic numbers are deliberate so the model is graded on
the reasoning, not record lookup. They do not need anchors.

## Raw / intermediate files (kept for traceability)

- `chicago_payments_raw.json` — 2,000-row sample
- `usaspending_recipients_raw.json` — top-50 recipients by total amount
- `lockheed_autocomplete.json` / `general_dynamics_autocomplete.json` — name-variant pulls
- `ofac_sdn.csv` — full SDN list (5.5 MB, ~18,800 records)
- `nyc_checkbook_raw.json` — failed query (wrong dataset id; ignore)
- `worldbank_procurement_raw.json` — empty response (ignore)
- `_build_anchors.py` — re-run to rebuild the per-question anchor JSONs

## How to use these in the benchmark

For q_001, q_004, and q_009, edit `data/questions.json` and replace the
synthesized `context` block with a real record from the corresponding anchor
file. Keep the question text and ideal answer; only the names/amounts/IDs in
the context need to change. Re-running the eval after the edit will exercise
the model against real-world inputs.

If you change a question's `id`, the runner will insert a new row; if you
keep the `id`, the runner will not update the existing row (upsert is by id
only — see `runner/eval.py:46`). To pick up edits to existing questions,
delete `db/profbench.db` and let the runner recreate it.

## Refreshing the data

```bash
cd data/anchors
# re-run the curl block from the conversation, or do it manually:
curl -sS "https://data.cityofchicago.org/resource/s4vu-giwb.json?\$limit=2000" \
  -o chicago_payments_raw.json
curl -sS -X POST "https://api.usaspending.gov/api/v2/autocomplete/recipient/" \
  -H "Content-Type: application/json" \
  -d '{"search_text":"lockheed","limit":15}' -o lockheed_autocomplete.json
curl -sSL "https://www.treasury.gov/ofac/downloads/sdn.csv" -o ofac_sdn.csv

python3 _build_anchors.py
```

All three sources are public, no API keys required, no rate limits at this
volume.
