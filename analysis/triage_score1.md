# Score-1 triage — run `c65d76c7-bf3a-4cb7-a7fb-23a92ba83b83`

12 score-1 responses across the three Claude models. For each, the table lists
what the grader said the response was missing and my **best-guess** triage
class:

- **(a) genuine model failure** — keep the score, benchmark working as intended
- **(b) ideal_answer too narrow** — broaden the ideal answer
- **(c) rubric miscalibrated** — adjust the tier-2 wording

These guesses are AI-generated and **should be treated as research assistance,
not domain judgment**. Override every row where your professional reading
differs.

---

## q_001 — supplier_data / easy (3 models lost a point)

All three Claude models hit the duplicate-via-TIN-normalization core; all three
miss the "18-month duplicate-payment lookback as a control step."

| Model | What was missed | My guess | Why |
|---|---|---|---|
| opus | Explicit duplicate-payment lookback across both record IDs | (a) | Working AP teams explicitly run a lookback when discovering a dup vendor; this is prescriptive, not optional |
| sonnet | Open-doc migration step (POs/invoices from B→A); duplicate-payment lookback | (a) | Two specific control steps missed; both are standard pre-deactivation hygiene |
| haiku | Duplicate-payment lookback; open-doc migration only implied | (a) | Same as above |

**Pattern:** all three models miss the same control. **Decision call for you:** is the lookback a hard tier-2 requirement (verdict (a) — keep score) or merely a "nice-to-mention" (verdict (b) — broaden ideal answer to allow "addresses duplicate-payment risk in any prescriptive form")?

---

## q_002 — invoice_processing / easy (opus + haiku lost a point)

Sonnet got 2 here, proving the rubric is achievable.

| Model | What was missed | My guess | Why |
|---|---|---|---|
| opus | After-the-fact PO control issue; legal engagement-letter-as-PO-equivalent conditions | (a) | These are concrete control nuances Sonnet captured; Opus genuinely shorter on the SOX angle |
| haiku | Auto-renewal-without-PO flag; after-the-fact PO; legal engagement-letter conditions | (a) | Smaller model missed multiple nuances Sonnet captured |

**Decision call:** likely (a) on both — Sonnet is the existence proof.

---

## q_003 — invoice_processing / medium (sonnet + haiku lost a point)

Both interpret 5%/2% as WITHIN tolerance; ideal answer says "less than" → out of tolerance. Opus got 2.

| Model | What was missed | My guess | Why |
|---|---|---|---|
| sonnet | Tolerance-edge interpretation (treats boundary as in-tolerance, not out) | **(c)** | Industry split on this — some ERPs use `≤`, some use `<`. The rubric is too prescriptive about which interpretation is "correct" |
| haiku | Same tolerance treatment + missed that the invoice bills 100 when only 95 were received | (a) for the qty miss, **(c)** for the tolerance | The qty issue is a real failure; the tolerance ambiguity is rubric-side |

**Strong (c) candidate.** I flagged this in the original draft notes — recommend updating tier-2 to: "correctly identifies the boundary case AND states which tolerance convention they're applying" rather than mandating a specific convention.

---

## q_005 — trade_and_tax / medium (haiku only)

| Model | What was missed | My guess | Why |
|---|---|---|---|
| haiku | Accepted inland freight + export clearance as billable; FCA principle that they're embedded in price | (a) | Opus and Sonnet got 2; this is a Haiku-specific FCA gap |

Decision call: (a) — clean Haiku weakness.

---

## q_007 — trade_and_tax / hard (haiku only)

| Model | What was missed | My guess | Why |
|---|---|---|---|
| haiku | Article 22 of Implementing Regulation 282/2011 (establishment-confirmation requirement) | (a) or (c) | Article 22 is a specific citation. If naming the citation is required for tier-2, (a). If the underlying *concept* (buyer must confirm which establishment) is enough, (c) — broaden tier-2 |

**Borderline.** My lean: (c) — the underlying concept is what matters; pinning tier-2 on a specific regulation citation is fragile (regulations get re-numbered).

---

## q_008 — close_and_controls / hard (haiku only)

| Model | What was missed | My guess | Why |
|---|---|---|---|
| haiku | Did not explicitly state remaining $50k is NOT accruable; missed GR/IR aging + SOX SoD considerations | (a) | The $50k exclusion is a hard accounting requirement — over-accruing is an audit finding |

Decision call: (a) — clean Haiku weakness.

---

## q_009 — supplier_data / hard (sonnet + haiku lost a point)

Opus got 2. Both Sonnet and Haiku miss OFAC 50% rule + FinCEN BOI.

| Model | What was missed | My guess | Why |
|---|---|---|---|
| sonnet | OFAC 50% rule; FinCEN BOI / CTA citation; independent bank-account callback control | (a) | Opus existence proof. These are nameable, citable, working-screening regimes. |
| haiku | Same as Sonnet plus other regime gaps | (a) | Same logic |

**Decision call:** likely (a) on both — Opus shows tier-2 is achievable.

---

## Summary recommendation

If you accept my best guesses, the only **rubric edits** would be:

- **q_003**: rewrite tier-2 to accept either tolerance convention (`<` vs `≤`) as long as the model names which convention it's applying. ~10 minutes of editing.
- **q_007** *(optional)*: rewrite tier-2 to require the Article 22 *concept* but not the specific citation. ~5 minutes.

Everything else is the benchmark working: the score-1 responses reflect real model gaps that are observable across the family. **9 of 12 score-1s are likely (a).**

After your edits, bump the question ids (e.g. `q_003` → `q_003_v2`) so the
runner picks them up — or use the new `--refresh-questions` flag (see the
polish work below) to update existing rows in place.
