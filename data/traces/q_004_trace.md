# q_004 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to ACFE *Report to the Nations* (billing-scheme typology;
> duplicate-payment detection), AICPA AAG-AUD (P2P disbursement
> controls), and standard ERP duplicate-detection rule design (SAP MM
> "duplicate invoice check" tcode `OMRDC`; Oracle Payables Invoice
> Approval Workflow). Heuristics (§3) and edge cases (§4) are flagged
> `[Authority gap]`.

## 1. Verdict and signals

**This is a duplicate with very high confidence.** Five signals
align, each independently meaningful per ACFE billing-scheme detection
guidance:

1. **Same vendor (V-44120, exact match).**
2. **Same amount to the cent ($4,287.50).** ACFE classifies
   to-the-cent matches within a short window from the same vendor as
   the **single strongest duplicate signal** — the false-positive rate
   is low because legitimate identical-amount billings cluster around
   round-number contractual figures, not arbitrary $4,287.50.
3. **Same PO reference (6710).** Two distinct invoices for the same
   PO at the same amount is highly unusual unless the PO authorized
   identical milestone payments and the GR posted twice, which is
   itself an investigation trigger.
4. **Different invoice numbers** (NB-2024-1142 vs NB-2024-1142R).
   The "R" suffix is the canonical "resubmission" / "reissue"
   convention — supplier billing systems append a suffix when an
   original invoice was lost or queried, not realizing the original
   already paid.
5. **Short-window proximity** (within 30 days). Standard ERP
   duplicate-check windows look back 90 days; 30-day window catches
   the high-confidence cluster.

## 2. Resolution path

1. Hold invoice 2 (do not pay).
2. Confirm invoice 1's payment posted and cleared (treasury
   confirmation).
3. Contact the supplier with invoice 1's payment reference and ask
   them to confirm whether invoice 2 was a duplicate submission or a
   second legitimate billing for separate goods/services.
4. If duplicate: cancel invoice 2 in AP; document for the duplicate-
   payment monitoring report.
5. If not duplicate (rare): require supplier documentation showing
   what invoice 2 covers that invoice 1 did not. Without that
   documentation, do not pay.

## 3. Automated duplicate-detection rules

Standard ERP rules (SAP `OMRDC`, Oracle Payables equivalent) flag
candidate duplicates when N or more of the following match:

- **Same vendor + same amount + same invoice date** — strongest rule;
  near-zero false-positive rate.
- **Same vendor + same amount + invoice dates within 30 days** —
  catches resubmission cases like this one.
- **Same vendor + same invoice number (with prefix/suffix
  normalization)** — catches the "R"/"-1"/"v2" suffix pattern.
- **Same vendor + same PO reference + amounts within ±$1** — catches
  near-amount duplicates from rounding or adjustment.
- **Same vendor + same amount + amounts within ±$1 + dates within 7
  days** — catches near-amount near-date clusters.

## 4. Heuristics

> **[Authority gap]**

- **Suffix-on-invoice-number is a duplicate signal until proven
  otherwise.** Suppliers rarely use suffix conventions for genuinely
  distinct billings; the suffix almost always means "we resent
  this."
- **PO-referenced duplicates are stronger evidence than non-PO
  duplicates** because the PO acts as a constraint: the PO authorized
  one billing event, not two.

## 5. Edge cases

> **[Authority gap]**

- **Milestone-billing POs with multiple identical milestones** (e.g.
  a project PO authorizing 4 × $4,287.50 milestone payments)
  legitimately produce identical-amount billings. The PO terms
  determine whether this is a duplicate or a legitimate second
  milestone.
- **Credit-rebill cycles** where a credit memo offsets the original
  and a corrected invoice issues at the same amount. Look for the
  credit memo before declaring duplicate.

## 6. Controls

ACFE billing-scheme typology and AICPA AAG-AUD classify the
duplicate-payment monitoring report as a **detective control** that
should run continuously, not periodically. Findings should route to
AP supervisor (not the original poster) for resolution and to internal
audit for trend analysis. Duplicate-payment frequency by vendor is a
SOX 404 ICFR walkthrough sampling target.
