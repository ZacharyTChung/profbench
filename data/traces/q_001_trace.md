# q_001 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Written for the v0.3
> framing described in [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Sections are anchored to IRS Pub 2108A (TIN matching), IRS Pub 1281
> (backup withholding for missing/incorrect TINs), AICPA AAG-AUD (vendor
> master controls), COSO 2013 (Control Activities), PCAOB AS 2201 (ICFR
> testing), and ACFE *Report to the Nations* (billing-scheme typology
> and dormant-vendor risk). Working detection heuristics (§3) and edge
> cases (§4) are most weakened by the absence of an SME and are flagged
> for `REVIEW_REQUEST.md` upgrade. Note: the supplier_data category is
> the strongest authorship area for this benchmark, so this trace is
> closer to practitioner-grade than q_003 or q_010.

## 1. First-pass triage

The Taxpayer Identification Number (TIN) is the only field where same
value reliably means same legal entity. Names suffer from suffix
variants, abbreviations, case differences, and DBA layering; addresses
change with relocations, branch openings, and P.O. box routing; phone
numbers are reassigned. **TIN normalization** — strip non-digits,
compare 9-digit sequences — is the IRS-aligned convention for
duplicate detection (per IRS Pub 2108A's TIN matching program design).

In this case both records present TIN `123456789`. That is the primary
duplicate signal. The bank-account match (Chase ****4521 on both) and
address match (100 Main St / 100 Main Street, same city/state/ZIP) are
corroborators that reduce the chance these are two intentionally-
maintained records (e.g., separate divisions of a parent under one
EIN). With TIN + bank + address all aligned, this is a high-confidence
duplicate.

## 2. Decision points

### 2a. Identity verification

The TIN match alone is sufficient to declare the duplicate *unless* a
named exception applies:

- **Disregarded entities under one EIN.** Some IT systems split a
  disregarded-entity LLC from its tax parent for 1099 routing reasons,
  even though the IRS treats them as one filer. The bank-account match
  here rules that exception out.
- **Same-TIN entities at different reorganization stages.** A
  predecessor and successor entity may share an EIN during a transition
  window even though state-level registrations differ. No evidence of
  that pattern in this fact set.

The IRS TIN Matching program (IRS Pub 2108A) is the authoritative
external check where firms want to validate TIN-name pairings beyond
internal matching. Mature AP functions integrate this check at vendor
onboarding; whether a given firm runs it pre-merge is a procedural
choice.

### 2b. Survivor selection

Three rules in order of priority:

1. **Active wins over dormant.** Record A had activity 30 days ago;
   Record B's last activity was 18 months ago. Merging into the
   dormant record forces a data migration on the live relationship and
   introduces unnecessary disruption risk.
2. **More-complete wins.** Record A includes "Suite 200" in the
   address; Record B does not. Other things equal, the more-complete
   record carries forward.
3. **Older wins (audit lineage)** when the first two rules are
   indeterminate. Longer-lived records carry more transaction history,
   and breaking that lineage costs reporting continuity for SOX
   walkthroughs.

Survivor: Record A.

### 2c. Pre-deactivation control sweep

This is the section where standard frontier-model responses on this
question consistently lose points (see `analysis/triage_score1.md` —
all three Claude family models missed the duplicate-payment lookback).
The sweep has three components, all anchored to AICPA AAG-AUD
guidance on disbursement controls:

1. **Open-document migration.** Re-point any open POs, in-flight
   invoices, payment runs, and contracts that reference Record B's
   vendor ID over to Record A. Sign-off from the buyer or contract
   owner is required for each migration. Deactivating B under a live
   PO breaks the AP path on the next invoice and risks duplicate-vendor
   re-creation.
2. **Duplicate-payment lookback** across both record IDs over a
   defined window. Standard parameters:
   - Same amount within ±$1
   - Same invoice number with prefix/suffix normalization
   - Same date within a 30-day window
   The lookback window matches the longer of (the dormant record's
   lifespan) and the firm's standard SOX work-paper retention
   (typically 24 months). ACFE *Report to the Nations* identifies
   billing-scheme detection lookback as a foundational anti-fraud
   control; once the records merge, the audit trail to discriminate
   payments by vendor ID becomes harder to follow.
3. **Bank-account history review** on both records. Even though both
   currently show ****4521, divergence in the past may indicate a
   period when payments routed to a different bank account. The
   bank-change audit log on each vendor ID should be pulled and
   inspected; ACFE classifies bank-account-change patterns within a
   short window of dormancy as a fraud-screen indicator.

### 2d. Documentation

The merge action requires documented evidence supporting future SOX
404 walkthrough sampling. Minimum content:

- Both vendor IDs and the canonical name of the surviving record.
- Trigger for the consolidation (master-data review, new invoice
  surfacing, duplicate-payment hit).
- TIN / bank / address match evidence.
- Open-document migration list with buyer sign-offs.
- Lookback results (clean / hits investigated / outcome).
- Approver chain — proposer (clerk), reviewer (supervisor),
  master-data steward who executed the change.

This documentation is the audit-sampleable artifact for SOX vendor-
master walkthroughs.

## 3. Working heuristics

> **[Authority gap]** Practitioner heuristics specific to this domain
> are the highest-value content the user can add. The notes below are
> derivable from ACFE / AICPA framework material; the rolodex content
> requires SME input.

- **Bank-account history is the fraud signal, not the dedupe signal.**
  Per ACFE billing-scheme typology, when a bank account on a
  "duplicate" was changed within ~30 days of the record going dormant,
  this is a fraud indicator that requires escalation before
  consolidating, not a routine cleanup task.
- **Same TIN, different legal entity types (Inc vs LLC) typically
  means reorganization, not duplication.** The IRS may treat them as
  separate for tax purposes during a transition window even when they
  share an EIN. Link as related parties; do not merge.
- **A dormant record with current TIN, current bank, and no recent
  activity is more suspicious than an active duplicate.** ACFE
  classifies this pattern as consistent with shelf-keeping for a
  potential side-payment scheme.

## 4. Edge cases

> **[Authority gap, same caveat as §3.]**

- **Different DBAs with separate state tax registrations under one
  EIN.** They are the same federal entity but file separately at state
  level. Do not merge in master; link via parent reference instead.
- **One record has an active dispute, audit hold, or open litigation
  reference.** Do nothing until resolved — merging during an open
  issue contaminates the investigation record.
- **The dormant record has open contracts that have not been billed
  against in the dormancy period.** Confirm contract status with legal
  before deactivating; auto-renewing contracts that have no recent
  billing may still be active.
- **Pending 1099 reporting cycle.** If the consolidation crosses a
  1099 cycle boundary, payments under the dormant record's TIN must
  reconcile to that record's 1099 even after merge. Coordinate with
  the tax function before deactivating mid-cycle.

## 5. Communication

If consolidation requires outward communication:

- **To the supplier:** "We have consolidated your vendor records in
  our system. All future invoices should reference [Record A's vendor
  ID]. No change to remit-to information or payment terms."
- **To internal AP:** notification that vendor ID [B] is being
  inactivated and that any held items should be re-routed to vendor
  ID [A].
- **To the buyer who owns the active relationship:** confirmation of
  the surviving record and migration of open documents.

## Why models miss this

Frontier models on this question correctly identify the TIN match and
the survivor-selection logic. The uniform gap is on the
**pre-deactivation control sweep** — specifically the duplicate-payment
lookback. The dedupe pattern is well-represented in training data
(it's basic master-data hygiene); the **control-step sequence**
(lookback → migrate → deactivate, in that order, with documentation)
is procedural knowledge that comes from working in a SOX-controlled AP
function rather than from textbook material. Training data has "how
to detect duplicates" but tends to lack "what control hygiene a senior
AP person runs before merging."

## How to convert into the q_001 ideal_answer field

The q_001 `ideal_answer` field in `data/questions.json` was the first
to receive practitioner validation in v0.1.4. This trace expands the
reasoning chain behind that ideal_answer and is consistent with it.
Refresh via:

```bash
python -m runner.eval refresh-questions
python -m scorer.autoscore --run-id <run_id> --overwrite
python -m analysis.report --run-id <run_id>
```
