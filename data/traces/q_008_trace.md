# q_008 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to the **matching principle** (FASB ASC 720; IAS 1
> presentation), **ASC 405** (liabilities), SAP Help Portal
> documentation on the **GR/IR** (Goods Receipt/Invoice Receipt)
> clearing account, and AICPA AAG-AUD coverage of period-close
> accruals. Heuristics (§3) and edge cases (§4) flagged
> `[Authority gap]`.

## 1. The accounting principle

The matching principle (FASB ASC 720; IAS 1) requires expense
recognition in the period the service is **rendered**, regardless of
invoice timing. As of 2026-03-31:

- **$150k of services have been rendered** through month-end (per
  the supplier's status report received 2026-03-30).
- **$50k remains to be rendered** in subsequent periods.

The $150k must hit March P&L. The $50k is **not accruable** —
services not yet rendered, no constructive obligation beyond the PO
commitment to pay if services are rendered. Accruing the full $200k
would over-state March expense.

## 2. The manual-accrual path

Common in non-SAP environments and for services POs that do not
generate goods receipts.

**At 2026-03-31:**
```
DR  Consulting expense        150,000
   CR  Accrued liabilities       150,000
```

This recognizes the expense in March against an accrual account
(reversal candidate) without an invoice in hand.

**At 2026-04-01 (reversal — common pattern):**
```
DR  Accrued liabilities       150,000
   CR  Consulting expense          150,000
```

Reversal undoes the accrual. When the supplier's Q1-final invoice
arrives in April for the actual amount delivered:

```
DR  Consulting expense        [actual]
   CR  AP — Strategy Consulting Co.   [actual]
```

Net effect: March correctly carries $150k; April carries the
true-up between accrual and actual (typically zero if the supplier
billed exactly $150k for Q1 work).

## 3. The SAP-style GR/IR path

For services POs configured with service-entry sheets (SES):

**At 2026-03-31** — accept the service entry sheet for $150k of
services rendered:
```
DR  Consulting expense        150,000
   CR  GR/IR clearing             150,000
```

**At invoice receipt** (April), against the same SES:
```
DR  GR/IR clearing            150,000
   CR  AP — Strategy Consulting Co. 150,000
```

Net effect on the clearing account: zero, once the invoice matches
the SES. The GR/IR account temporarily holds the accrual without
needing a separate manual journal entry; the SES is the audit-
evident record of work received.

The remaining $50k of PO commitment **is not recognized** until
either an SES posts (services rendered) or the invoice arrives.

## 4. Why $50k is not accruable

ASC 405-10 and IAS 37 both require a present obligation arising from
past events for liability recognition. The $50k of PO commitment
represents **a contractual obligation to pay if services are
rendered**, not a present obligation for services already rendered.
Accruing it would mis-classify a future obligation as a present one
and overstate the period's expense.

The PO commitment does, however, belong in the firm's commitments
disclosure (per ASC 440 / IAS 37 contingencies and commitments)
where material.

## 5. SOX P2P and SoD considerations

The SES posting for $150k requires segregation of duties:

- **Project owner / requester** confirms services were rendered (the
  receiver-equivalent role for services).
- **AP supervisor** approves the SES posting going into the system.
- **The same person cannot approve the SES and approve the invoice
  match.**

The matching-principle classification ($150k accruable, $50k not)
is itself a SOX 404 walkthrough sample target — auditors look for
period-end accruals that systematically over- or under-state on the
"easy" assumption that the full PO would be accrued.

## 6. GR/IR aging considerations

If the SES posts at $150k in March but the invoice does not arrive
within the GR/IR aging policy (typically 60–90 days), the open GR/IR
balance flags for review. Long-aged GR/IR balances are a control
finding — they indicate either:

- Services were posted as rendered but the supplier never billed
  (possibly because services were *not* actually rendered).
- The invoice arrived but failed to match (3-way-match exception).
- The PO is closed but the SES is orphaned.

## 7. Heuristics

> **[Authority gap]**

- **Status reports are evidence; PO commitment is not.** Accruals
  must be supported by evidence of work rendered, not by
  contractual amounts.
- **Reverse manual accruals on day 1 of the next month** to keep the
  P&L clean. Trying to net the accrual against the invoice in-place
  is a common bookkeeping error that obscures audit trail.

## 8. Edge cases

> **[Authority gap]**

- **The status report is from the supplier (self-reported)** rather
  than from the project owner — apply more skepticism, especially
  near period-close. Independent confirmation by the project owner
  is the stronger evidence.
- **Performance bonus / contingent-fee structures** in the
  engagement letter complicate the "services rendered" measurement;
  the bonus portion may not be accruable until milestones are met.
- **The supplier's Q1 work may include re-performances of work
  rejected by the project owner**, which should not be billed nor
  accrued.
