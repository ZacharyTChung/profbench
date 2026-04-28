# Reasoning trace template — q_001 (supplier dedupe)

> Replace each `_[fill in]_` block with your actual reasoning. Don't polish.
> Once filled, paste into q_001's `ideal_answer` and run
> `python -m runner.eval refresh-questions`.
>
> Length target: 600–1000 words.

## The question (for reference)

Two supplier records — same TIN (12-3456789 vs 123456789), nearly identical
addresses, same bank ****4521, but different activity status (Record A
active recent, Record B dormant 18 months). Are they duplicates? Resolution?

---

## 1. First glance

What field do you look at first on a dedupe case, and why?

> _[fill in: e.g. "TIN first, always. Names get mangled, addresses change, but TIN normalization (strip non-digits) is the only field where same value = same legal entity..."]_

---

## 2. Decision points

### 2a. Identity verification

> _[fill in: how you confirm same legal entity — TIN, EIN structure, IRS TIN matching service, Secretary of State / D&B lookup if needed. What confidence threshold do you require before merging?]_

### 2b. Survivor selection

> _[fill in: rules of thumb — keep the active one? keep the most complete? keep the older record? When does the "newer is better" rule lose? What's your firm's policy?]_

### 2c. Pre-deactivation hygiene (the part models miss)

This is where all three Claude models lost their points on this question.
Walk through the steps you'd do BEFORE flipping the dormant record inactive.

> _[fill in: e.g. "Run a duplicate-payment sweep across both record IDs over the last 18 months — same amounts within ±$1, same invoice numbers, same dates. If anything pops, investigate before consolidating..." Be specific about the lookback window and what counts as a hit.]_

> _[fill in: e.g. "Migrate any open POs/payables/contracts from B to A — re-point them in the system, get sign-off from the buyers..." What's the sequence? Who has to approve?]_

> _[fill in: e.g. "Pull the bank account history on both records — even if currently same, was there a period where they diverged? That's a sign someone was running a side-channel..." What's the audit angle?]_

### 2d. Documentation

> _[fill in: what gets written down — what record was kept, what was inactivated, why, who approved, what control checks ran, what they returned]_

---

## 3. Heuristics

> _[fill in 4–6 working-knowledge shortcuts, e.g. "If the dormant record's bank account was changed within 30 days of going dormant, that's a fraud indicator not a cleanup task..."]_

---

## 4. Edge cases

> _[fill in: at least 3 — e.g. "If the two records are at the same TIN but different DBAs that file separate 1099s under different state tax IDs, they're the same federal entity but separate state filers — don't merge..." "If there's an active dispute or audit on either record, do nothing until resolved..."]_

---

## 5. Communication

If you had to explain the consolidation to the supplier and to the buyer
who owns the active relationship, what would you actually say?

> _[fill in]_

---

## 6. Why models miss this

Your read on why an LLM fails this question — what's missing from the
training data or the typical reasoning pattern?

> _[fill in: optional but valuable — your meta-observation about why frontier models don't name the lookback step]_
