# q_003 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Written for the v0.3
> framing described in [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Sections are anchored to AICPA AAG-AUD (3-way match as a control activity),
> COSO 2013 (Control Activities principle 10), Incoterms 2020 (ICC 723E,
> freight allocation), and SAP / Oracle ERP documentation on tolerance
> behavior. Working-practitioner heuristics (§3) and edge cases (§4) are the
> sections most weakened by the absence of an SME and are explicitly flagged
> for `REVIEW_REQUEST.md` upgrade.

## 1. First-pass triage

The 3-way match is the canonical P2P control activity referenced in COSO
2013 (principle 10, "selects and develops control activities") and tested
under PCAOB AS 2201 as an entity-level control over disbursements. The
question is whether the invoice can be released for payment given the
PO and goods-receipt (GR) it must reconcile to.

Two facts dominate the case before any arithmetic:

1. The GR is marked **final delivery — short ship per supplier**. Under
   standard ERP convention (SAP MM-IV-LIV documentation; Oracle Payables
   Implementation Guide), a "final delivery" indicator closes the open
   commitment on the PO line and prevents follow-on receipts against
   that line. The 5-unit shortage is therefore not a future-receivable.
2. The invoice bills the original 100 units, not the 95 actually
   received. This is a quantity-over-receipt exception independent of
   any tolerance calculation.

These two facts together drive the resolution path even before the
tolerance math is run.

## 2. Decision points

### 2a. Quantity reconciliation

Math: 100 invoiced − 95 received = 5 units / 5.00% variance against the
PO's ±5% quantity tolerance. Over-bill exposure: 5 × $10.00 = $50.00.

The boundary case (5.00% exactly at the ±5% threshold) is genuinely
**ambiguous in industry**. Two conventions coexist:

- **Strictly less than (`<`):** 5.00% is *out* of tolerance. SAP MM
  default behavior per the OPlA/OPlB tolerance configuration table.
- **Less than or equal (`≤`):** 5.00% is *in* tolerance. Common in
  Oracle Payables and several mid-market ERPs.

A defensible response **states which convention is being applied** and
reasons consistently from there. ProfBench's q_003 rubric is calibrated
to accept either as long as the convention is named (per `analysis/triage_score1.md`).

The convention question is, however, **subordinate to the
final-delivery flag** in this case. Whether or not the variance
auto-releases by tolerance, the matching principle from invoice-to-GR
prohibits payment for goods that have not been and will not be
received. AICPA AAG-AUD's coverage of disbursement controls treats
this as a no-tolerance exception class.

### 2b. Price variance

Math: $10.20 vs. PO $10.00 = $0.20 / 2.00% variance against ±2%
tolerance. Same boundary case. Over-bill at PO quantity:
100 × $0.20 = $20.00.

Even where the variance auto-releases under `≤` convention, COSO 2013
principle 10 ("control activities are deployed through policies that
establish what is expected") supports surfacing boundary cases to the
buyer for explicit acknowledgment rather than silent auto-release. The
audit-trail value of an explicit approval outweighs the ~2 minutes of
processing friction.

### 2c. Freight line

The invoice carries $35.00 freight; the PO does not. Allocation depends
on the contractually agreed Incoterm. Incoterms 2020 (ICC Publication
723E) defines eleven trade terms; the freight-bearing party varies by
term:

- **EXW, FCA:** buyer bears freight beyond the named place. A freight
  line on the invoice is contractually defensible.
- **CPT, CIP, CFR, CIF:** seller bears freight to the named destination
  and freight is built into the unit price. A separate freight line on
  the invoice is **not** contractually defensible without amendment.
- **DAP, DPU, DDP:** seller bears freight to destination. Same logic.

The PO does not state an Incoterm in this case. Where the firm's
purchasing-policy default is "freight included unless explicitly priced
on the PO," the freight line is unauthorized and rejects to the buyer.
Where the policy inverts, the freight may be allowable. Either way, the
**absence of an Incoterm on a non-trivial PO is itself a sourcing
control gap** worth flagging separately under COSO principle 12
("deploys through policies and procedures").

### 2d. Resolution path

The invoice holds. Three workstreams in parallel:

1. **Quantity:** confirm the short-ship with receiving (verify the GR
   is accurate and the missing 5 units are not in a side bin or on
   another GR). On confirmation, request a credit memo from the
   supplier for 5 × $10.00 = $50.00, OR request a corrected invoice at
   95 units. Credit memos generally close faster in ERP workflows.
2. **Price:** route to the buyer (sourcing) for variance approval. If
   the buyer approves, the PO is updated via change order — not silent
   acceptance — to preserve audit-trail integrity (PCAOB AS 2201
   requirement that controls operate evidentiarily). If the buyer
   rejects, the supplier reissues at PO price.
3. **Freight:** route to the buyer for contractual review against the
   firm's Incoterms / freight policy. If unauthorized, reject the line.
   If accepted, the freight moves to the PO via change order before
   payment.

Net 30 starts only when the **corrected** invoice is received in good
order. Update the supplier portal so payment-term clocks are not gamed
by the original (defective) invoice date.

## 3. Working heuristics

> **[Authority gap]** The four notes below are framework-derivable
> rather than practitioner-rolodex content. The most valuable
> heuristics in 3-way match exception handling — the ones an experienced
> AP analyst would write from memory — are explicitly out of scope for
> this cited-authority draft. See `REVIEW_REQUEST.md` for the SME ask.

- **Final-delivery indicator overrides tolerance percentages on the
  quantity line.** Tolerance frameworks address acceptable measurement
  variance; "final delivery" closes the commitment and removes the
  variance interpretation — invoiced units beyond received units cannot
  be matched.
- **Price-variance approvals belong on the PO via change order, not in
  email or one-time release.** PCAOB AS 2201 and SOX 404 ICFR
  walkthroughs sample for end-to-end audit reconstructability; an
  approval that doesn't move the PO leaves an evidence gap.
- **Freight charges absent an Incoterm should be challenged.**
  Incoterms 2020 implicitly governs allocation, but only when stated.
  Silent freight allocation defaults to firm policy, which is a weaker
  contractual position than a stated Incoterm.
- **Net-30 starts on the corrected invoice in good order**, not on the
  original. Most master purchase agreements use "received in good
  order" language; a defective original does not satisfy that
  condition. Suppliers occasionally argue otherwise and require
  pushback citing the MPA clause.

## 4. Edge cases

> **[Authority gap, same caveat as §3.]** Standard guidance
> covers the cases below; the high-value edge cases — the unusual
> patterns that experienced AP teams develop reflexes for — are out of
> scope here.

- **GR marked "partial" rather than "final":** the missing 5 units may
  arrive on a follow-on shipment. Hold the invoice until the next
  receipt posts; do not request a credit memo prematurely.
- **Supplier provides an amended shipping document showing 100 units
  shipped, contradicting the GR:** route to receiving for re-count
  (cycle audit or physical recount). Do not adjust based on supplier
  documentation alone — the GR is the firm's authoritative receipt
  record.
- **PO is a blanket / call-off contract with multiple scheduled
  deliveries:** the "final delivery" indicator on a single GR may not
  close the contract. Verify call-off schedule before treating the
  shortage as terminal.
- **Foreign-currency PO with FX revaluation between order and invoice
  dates:** price-variance interpretation needs a currency-pair lens
  before the tolerance check. The PO's FX rate at booking, not the
  invoice date's spot rate, is typically the comparison base — but
  treatment varies by firm policy and ERP configuration.

## 5. Controls and segregation of duties

PCAOB AS 2201 ("An Audit of Internal Control over Financial Reporting
that is Integrated with an Audit of Financial Statements") and COSO
2013 principle 10 jointly establish the 3-way match as a key control
over disbursements. Segregation requirements:

- **AP clerk** identifies and posts the exception. Authority ends at
  posting the hold; the clerk cannot approve any variance.
- **Buyer (sourcing)** approves price and freight variances within
  their delegation-of-authority (DoA) limit; above limit, escalates per
  the DoA matrix.
- **Receiver** confirms quantity facts independently. The receiver
  cannot also be the buyer or AP clerk for the same transaction
  (incompatible-functions principle under COSO).
- **AP supervisor** signs off on variance approval going into the
  system. The supervisor cannot have been the original poster.

All exception approvals must be reconstructable end-to-end from system
records without referring to email — this is the standard SOX 404
walkthrough requirement for the 3-way match control.

## 6. Communication

The supplier-facing communication has six bullet points (the literal
content varies by firm template):

- Reference our PO #4500-22871 and your invoice INV-88412.
- Goods receipt confirms 95 units received, marked final delivery.
- Invoice bills 100 units; please reissue at 95 units, or provide a
  credit memo for 5 units × $10.00 = $50.00.
- Price variance: PO at $10.00/unit; invoice at $10.20/unit. Provide
  the contractual basis for the price change, or reissue at PO price.
  If the change is approved by our buyer, a PO change order will be
  issued before payment.
- Freight charge of $35.00 is not authorized on this PO. Please remove
  or provide the contractual / Incoterms basis.
- Net 30 begins from receipt of the corrected invoice in good order.

## Why models miss this

The combination of facts that frontier models tend to under-weight:

1. **Final-delivery indicator overriding tolerance percentages.** The
   reasoning chain "GR-final → cannot pay for unshipped units
   regardless of tolerance percentage" requires holding two facts in
   working memory and noticing they conflict. Many model responses
   apply tolerance heuristics in isolation and fail to integrate the
   final-delivery signal.
2. **Naming the tolerance convention being applied.** Some models
   treat 5.00% as definitionally "in tolerance" without acknowledging
   the `<` vs `≤` ambiguity. The q_003 rubric specifically rewards
   responses that name their convention.
3. **The freight line as an Incoterms question, not a "is it
   reasonable" question.** Freight allocation is contractual, not
   discretionary; a model that approves the freight on a "looks like a
   normal small freight charge" basis misses the control framing.

## How to convert into the q_003 ideal_answer field

Sections 1–6 concatenate to a ~1100-word answer suitable for the
`ideal_answer` field in `data/questions.json`. The current ideal_answer
already incorporates the tolerance-convention calibration; this trace
expands the surrounding reasoning chain. Refresh via:

```bash
python -m runner.eval refresh-questions
python -m scorer.autoscore --run-id <run_id> --overwrite
python -m analysis.report --run-id <run_id>
```
