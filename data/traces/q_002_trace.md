# q_002 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to AICPA AAG-AUD (PO/non-PO control taxonomy), COSO 2013
> principle 10 (control activities deployment), and the typical
> mid-market P2P policy patterns documented in CIPS *Procurement and
> Supply Management Body of Knowledge*. Heuristics (§3) and edge
> cases (§4) are flagged `[Authority gap]` for `REVIEW_REQUEST.md`.

## 1. The framework

Mid-market P2P policy distinguishes PO-backed from non-PO spend by
two orthogonal axes: **commitment recordability** and **risk profile**.
Goods purchases above a low threshold (typically ~$2.5k) require POs
because the commitment must be recorded against budget *before* the
liability arises. Services > $25k require POs for the same reason
plus stronger contractual terms. Recurring utilities and small office
supplies are policy carve-outs because the cost-of-control exceeds
the cost-of-error.

## 2. Per-invoice classification

### PG&E utility — $4,820 monthly electricity
**Non-PO.** Recurring utility under the standard policy carve-out
documented in AICPA AAG-AUD coverage of utility-class disbursements.
Approved against a utility budget line, not a PO commitment.

### Salesforce SaaS renewal — $84,000 annual
**PO-backed.** Services > $25k threshold; auto-renewal must be on a
PO so the commitment is recorded against budget and term/price are
locked. A renewal arriving without an active PO is itself an
exception (rogue spend) under the firm's spend-control policy.

### Latham & Watkins legal services — $11,500 retainer
**Non-PO** (or "PO-equivalent" via legal engagement letter). Legal
services on retainer are a recognized exception class because the
engagement letter functions as the contractual commitment record. AP
should confirm the engagement letter is on file and the spend tracks
against the retainer budget.

### Staples office supplies — $612
**Non-PO.** Below the goods-PO threshold (typically ~$2.5k); under
the firm's tail-spend policy this routes through a P-card or
employee-expense channel.

### Marketing agency creative work — typically > goods threshold
**PO-backed.** Services with a defined deliverable and a non-trivial
amount require a PO under the services-> $25k policy if applicable,
or a project-services PO under any project-spend policy.

## 3. Heuristics

> **[Authority gap]** Practitioner pattern-recognition for which
> non-PO invoices warrant escalation despite being technically
> within policy is the high-value SME content.

- **A non-PO invoice that would have triggered a PO requirement if it
  arrived for the first time tomorrow is rogue spend.** A SaaS
  renewal that has been running on auto-renew for years without a
  refreshed PO is the canonical case.
- **Legal engagement-letter-as-PO-equivalent is a control if and only
  if the engagement letter is on file.** Retainer billing without an
  engagement letter is a missing-control finding under SOX 404 P2P
  walkthroughs.

## 4. Edge cases

> **[Authority gap]**

- **Utility services from a non-traditional provider** (e.g. data-
  center colocation as "utility") may not qualify for the carve-out
  if the firm's policy enumerates specific providers/categories.
- **Salesforce-style auto-renewal where the renewal price exceeded
  the prior year's PO** is a price-variance exception requiring buyer
  re-approval before the new PO issues.

## 5. Controls

Under SOX 404 P2P walkthrough sampling, the auditor will confirm:
PO existed before the goods/services were committed, the PO matched
to GR and invoice within tolerance, the non-PO carve-outs were
exercised against an approved policy enumeration, and engagement-
letter-style alternatives were on file before the spend.
