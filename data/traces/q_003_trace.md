# q_003 reasoning trace — AI DRAFT

> **[AI DRAFT — practitioner edits required]** This is a Claude-generated
> first draft following the structure of `q_003_template.md`. Sections 3
> (heuristics) and 4 (edge cases) are the most important to rewrite from
> your actual experience — those are where domain authenticity lives.
> Sections 1, 2, 5, 6 are framework material that's reasonable as drafted
> but should still be voiced in your style. Mark `[OK as drafted]` or
> `[REWRITTEN]` per section as you go so the AfterQuery submission can
> attest to expert authorship.

## 1. First glance

The first field I look at is the **PO number on the invoice header** —
not because it's diagnostic, but because routing errors account for
maybe 5% of what hits an AP queue. If the PO ref doesn't match what the
ticket says, I kick it back without analyzing anything else. Once that's
clean, I jump straight to the **GR status flag** — "final" vs "partial"
changes the entire shape of the resolution. Then I look at the **invoice
quantity vs GR quantity**, because that's the single largest dollar
exposure on any short-ship case.

Gut signal on this case before any math: **two flags hit immediately.**
The GR is marked final, and the invoice doesn't reference the GR
shortage. That tells me the supplier's billing system hasn't reconciled
with their shipping system — probably automated invoicing off the PO
quantity rather than the actual ship document. That pattern is common
enough that I'd guess this is supplier-system noise rather than fraud,
but I still hold the invoice until I confirm.

> [AI DRAFT — practitioner: rewrite to match your actual triage order. The "5% routing error" stat is a guess. Add anything specific about your firm's queue tooling.]

## 2. Decision points

### 2a. Quantity check

100 invoiced – 95 received = 5 units short, 5.00% variance against
±5% tolerance. The invoice over-bills by 5 × $10.00 = $50.00.

The tolerance edge is genuinely ambiguous. **Both `<` and `≤` are
defensible** — SAP defaults to strictly-less-than (so 5.00% is out of
tolerance), some Oracle and mid-market systems use less-than-or-equal
(so 5.00% would auto-release). I work in [SAP / Oracle / etc — fill in
your firm's ERP convention here]. Under my firm's convention, this is
[in / out of] tolerance.

But the convention question is actually a distraction here, because of
the GR's "final delivery" marker. **Whether or not the variance auto-
releases by tolerance, you cannot pay for units that won't arrive.**
Final-delivery means the missing 5 units will not be received on a
follow-on shipment — they're gone. Paying the invoice as-billed pays
for goods that don't exist. That's a no-tolerance exception regardless
of how the variance percentage rounds.

> [AI DRAFT — practitioner: rewrite the convention paragraph from your firm's actual ERP behavior. The "GR-final-trumps-tolerance" rule is correct in my reading but you'll have a sharper way to phrase it.]

### 2b. Price check

$10.20 vs $10.00 = $0.20, 2.00% variance against ±2% tolerance. Same
boundary case. Under `<`, out of tolerance; under `≤`, in. Over-bill at
PO quantity = $20.00.

Even when the price variance auto-releases by ERP tolerance, **best
practice is to surface boundary-case variances to the buyer for
acknowledgment** rather than auto-pay. Two minutes of friction here
prevents a downstream credit-memo cycle when the buyer notices a
month later that their price commitment moved without their consent.

### 2c. Freight line

$35 freight on the invoice, none on the PO. The first question is
contractual: what's the firm's default? My firm operates on **freight
included unless explicitly priced on the PO** (because a freight line
on the PO requires sourcing approval; absent that approval, freight is
seller's cost). If your firm operates the inverse, the conclusion
flips.

The Incoterms angle is implicit because there's no Incoterm stated on
the PO. Domestic-only POs often omit Incoterms and rely on the firm's
default freight policy; international POs that omit Incoterms are a
sourcing-control gap that should be flagged separately.

> [AI DRAFT — practitioner: state your firm's actual freight default policy here.]

### 2d. Resolution path

Hold the invoice; don't pay. Three workstreams in parallel:

1. **Quantity:** confirm short-ship with receiving (was the GR
   accurate? are the missing 5 units actually missing or in a side
   bin?). If confirmed short, request a credit memo from the supplier
   for 5 × $10.00 = $50.00, OR have them reissue at 95 units. Credit
   memo is faster to close in most ERP setups.

2. **Price:** route to the buyer (sourcing) for variance approval.
   Buyer either approves the increase (and updates the PO via change
   order — important: change order, not silent acceptance, because
   sourcing approval that doesn't move the PO leaves an audit gap) or
   rejects and demands invoice reissue at PO price.

3. **Freight:** route to the buyer; if not contractually owed, reject
   the line. If accepted, again move it to the PO via change order.

Net 30 starts only when the **corrected** invoice is received in good
order. Update the supplier portal so payment-term clocks aren't gamed.

## 3. Heuristics — the rules of thumb

> [AI DRAFT — practitioner: this section needs to come from your real-world rolodex. I'm drafting placeholder rules from general working knowledge. Expect to rewrite all of these.]

- **Final-delivery marker beats tolerance.** When I see "final" on the
  GR and the invoice still bills original quantity, 9 times of 10 it's
  the supplier billing off the PO instead of the ship doc. Request a
  credit memo not a re-bill — closes faster.
- **Boundary-case price variances always go to the buyer**, even when
  the ERP would auto-release. The two minutes of friction is cheaper
  than a downstream credit-memo cycle.
- **Freight line on a non-international PO without sourcing approval =
  reject every time.** The exception is so rare it's not worth coding
  around.
- **Net 30 starts on the corrected invoice, not the original.** Some
  suppliers will try to argue the original date holds; the contract
  language usually says "received in good order" which the original
  was not.
- [Practitioner: add 2-3 more from your actual experience]

## 4. Edge cases — what would change my recommendation

> [AI DRAFT — practitioner: this section is the most valuable for SFT data. Real edge cases you've encountered are what frontier models can't pattern-match. Expect to rewrite or expand substantially.]

- **GR marked "partial" instead of "final":** I'd wait for the next
  receipt before doing anything on quantity. The missing 5 units might
  still be on a follow-on shipment.
- **Supplier provides a re-issued shipping document showing 100 units
  shipped, contradicting the GR:** route to receiving for re-count and
  cycle audit. Don't take the supplier's word; physically verify before
  paying any invoice that contradicts a posted GR.
- **The PO is marked "blanket / call-off" with multiple deliveries:**
  the "final delivery" marker on a single GR doesn't necessarily mean
  the contract is closed; check whether more call-offs are scheduled.
- [Practitioner: add 2-3 from your real history]

## 5. Controls and segregation

SOX P2P three-way match is the operative control. The roles must split:

- **AP clerk** identifies the exception, posts the hold, but cannot
  approve any variance. Their authority ends at posting the hold.
- **Buyer (sourcing)** approves price and freight variances within
  delegation; above delegation, escalates per the DoA matrix.
- **Receiver** confirms quantity facts. Receiver cannot also be the
  buyer or AP clerk for the same transaction.
- **AP supervisor** signs off on the variance approval going into the
  system, and the supervisor cannot have been the original poster.

All exception approvals must be documented in the system to support the
SOX 'invoice-to-PO/GR three-way match' control test. The audit trail
should be reconstructable end-to-end without referring to email.

## 6. Communication

If I had to write the email to the supplier on this case, the bullets
would be:

- Reference our PO #4500-22871 and your invoice INV-88412.
- Our goods receipt confirms 95 units received and was marked final
  delivery; please confirm whether the 5-unit shortage is intentional.
- Your invoice bills 100 units; please reissue at 95 units, OR provide
  a credit memo for 5 units × $10.00 = $50.00.
- Price variance: PO is at $10.00/unit; invoice is at $10.20/unit. We
  need either an explanation of the price change or a corrected
  invoice. If the change is approved, our buyer [name] will issue a PO
  change order to update the unit price.
- Freight charge of $35 is not authorized on this PO. Please remove or
  provide the contractual basis.
- Net 30 will start from receipt of the corrected invoice in good order.

## Why models miss this

> [AI DRAFT — practitioner-optional but valuable] My read on why frontier models leak score on this question: they pattern-match on the variance percentages and apply tolerance heuristics, but they don't internalize that **the final-delivery flag overrides the tolerance question for the quantity line**. The reasoning chain "GR-final → cannot pay for unshipped units regardless of tolerance percentage" requires holding two facts in working memory and noticing they conflict. That's where the model loses the point even when it gets the math right.

---

## How to convert this trace into the q_003 ideal_answer field

When you've edited this draft to your satisfaction, concatenate sections
1-6 (sections 7+ are notes for you, not for the model) and paste into
the `ideal_answer` field in `data/questions.json` for q_003. Then run:

```bash
python -m runner.eval refresh-questions
python -m scorer.autoscore --run-id <run_id> --overwrite  # re-grade against the new ideal answer
python -m analysis.report --run-id <run_id>               # see the new scores
```
