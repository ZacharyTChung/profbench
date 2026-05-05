# q_017 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **AICPA AAG-AUD** (vendor-master and disbursement
> control taxonomy), **ACFE *Report to the Nations*** (billing-scheme
> typology), and **PCAOB AS 2201** (ICFR control-design distinction).
> This is a **conceptual** question; minor `[Authority gap]` only on
> heuristics §3.

## 1. The two concepts

### Duplicate vendor record
**Same legal entity appears twice (or more) in the supplier master
under distinct vendor IDs.** The records may carry name variants,
slightly different addresses, or different bank accounts. The legal
entity is one; the master-data representation is multiple.

### Duplicate payment
**Same invoice paid twice (or more).** Same supplier, same invoice
content, same amount, same goods/services rendered — but two
payment events instead of one.

These are different problems with different control responses.

## 2. The control-axis distinction

| Aspect | Duplicate vendor record | Duplicate payment |
|---|---|---|
| **What's wrong** | Master-data shape | Transaction processing |
| **Where caught** | Vendor-master maintenance / onboarding | Invoice-processing pipeline |
| **Control type** | Preventive (don't create duplicates) + detective (find existing duplicates) | Detective (catch the second payment before / shortly after release) |
| **Primary control** | TIN / bank-account / address matching at vendor-add | Invoice-level dedupe rules (amount + date + vendor + invoice number) |
| **Risk profile** | Enables future duplicate payments + complicates 1099 reporting + obscures spend analytics | Direct cash loss + audit finding |
| **Severity if uncorrected** | Latent risk; may persist for years before triggering loss | Immediate loss |

## 3. Why both matter and how they interact

A duplicate vendor record **enables** duplicate payments — when the
same legal entity has two vendor IDs, an invoice can be entered
under each ID and pay twice without tripping the standard duplicate-
invoice check (which is keyed on vendor ID + invoice number, not on
legal entity).

But the converse isn't true: duplicate payments can occur without
any duplicate vendor record (e.g. resubmitted invoice with a slight
suffix variant, paid against the same vendor ID twice).

So:

- **Duplicate vendor records create a structural risk** that
  duplicate-payment detection cannot fully cover.
- **Duplicate-payment detection** is the operational backstop
  regardless of vendor-master quality.

A mature P2P control set covers both.

## 4. Detection rules — duplicate vendor record

Standard preventive + detective rules at vendor-master level:

- **TIN normalization match** at vendor-add. New vendor whose TIN
  matches an existing vendor's TIN flags for review.
- **Bank-account match.** New vendor whose bank routing + account
  matches an existing vendor's bank account flags for review.
- **Name normalization match** with phonetic / suffix tolerance
  (e.g. "Acme Corp" vs "Acme Corporation").
- **Address match** (with normalization for "Suite 200" vs "Ste 200"
  type variants).
- **Periodic master-data review** — quarterly or annually — running
  the same matchers across the existing vendor base.

## 5. Detection rules — duplicate payment

Standard detective rules (per ACFE billing-scheme guidance and
typical ERP duplicate-invoice-check configuration):

- Same vendor + same amount + same invoice date.
- Same vendor + same amount + invoice dates within 30 days.
- Same vendor + same invoice number (with prefix/suffix
  normalization).
- Same vendor + same PO reference + amounts within ±$1.

## 6. Control-design principle

Per PCAOB AS 2201, control-design analysis distinguishes between:

- **Design effectiveness** — does the control, as designed, address
  the risk? Duplicate-vendor and duplicate-payment require
  different design decisions because they address different risks.
- **Operating effectiveness** — does the control operate as
  designed? A duplicate-payment rule that runs only on Friday
  morning has a design that mostly works but operates with a 6-day
  exposure window.

Control-design matters because consolidating both risks into one
control (e.g. "the duplicate-payment rule will catch any
duplicate-vendor consequences") is a design failure — the
duplicate-payment rule cannot detect a payment that legitimately
matches one vendor record but is in fact owed to a different vendor
record for the same legal entity.

## 7. Heuristics

> **[Authority gap]**

- **The duplicate-vendor problem is much harder to discover than
  the duplicate-payment problem.** Duplicate payments produce a
  cash-out signal; duplicate vendors produce a latent risk that
  surfaces only when a specific combination of events occurs.
- **Vendor-master cleanup projects predictably surface duplicate
  payments.** Once the records are consolidated, the lookback
  duplicate-payment scan against the merged vendor IDs is the next
  step (see q_001 trace).

## 8. Process implication

The audit-defensible P2P control set documents both:

1. The vendor-master maintenance controls (preventive +
   periodic-detective on duplicates).
2. The invoice-processing duplicate-payment rules (detective at
   posting / pre-payment).
3. The interaction: duplicate-vendor cleanup triggers a duplicate-
   payment lookback as a control step.

Treating either in isolation leaves a known gap.
