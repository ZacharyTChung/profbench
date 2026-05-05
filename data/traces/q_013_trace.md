# q_013 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **UK VAT Act 1994, Schedule 4A** (place-of-supply rules
> for services), **HMRC VAT Notice 741A** (Place of supply of
> services), and post-Brexit guidance in **HMRC VAT Notice 700/57**.
> Heuristics (§3) and edge cases (§4) flagged `[Authority gap]`.

## 1. The VAT is incorrectly charged

Under post-Brexit UK B2B place-of-supply rules for digital and
consultancy services, the place of supply is the **customer's
location**, not the supplier's. With the customer in the US (no UK
establishment, no UK VAT registration), the supply is **outside the
scope of UK VAT**.

The supplier should not have charged the £4,800 VAT.

## 2. Reasoning

### General B2B rule (Schedule 4A para 16)
The default place-of-supply for B2B services post-Brexit is the
**place where the customer belongs**. "Belongs" is defined by:

- The customer's business establishment, or
- A fixed establishment to which the service is supplied, or
- Failing both, the customer's usual place of residence.

The US buyer has no UK establishment and no UK VAT registration. The
customer "belongs" in the US for these purposes.

### Digital / electronically-supplied services
SaaS subscriptions are **electronically-supplied services** (HMRC VAT
Notice 741A). For B2B electronically-supplied services to a non-UK
customer, the place of supply is **outside the scope of UK VAT**.
The supplier invoices without VAT.

### Reverse-charge applicability
For services supplied **into** the UK from abroad to a UK customer,
the UK customer self-accounts under the reverse charge. The reverse
direction (supplies from the UK to abroad) is simply outside the
scope — no reverse charge mechanism applies on the customer side
because no UK VAT applies in the first place.

## 3. AP actions

1. **Hold the invoice.** Do not pay the £4,800 VAT.
2. **Request a corrected invoice** from the supplier showing the
   service as outside the scope of UK VAT. The corrected invoice
   should typically include a note like "Outside the scope of UK VAT
   — customer outside the UK, B2B electronically-supplied service
   per VAT Act 1994 Schedule 4A."
3. **Pay the goods/service portion only** once the corrected
   invoice is received.
4. **Do not attempt to reclaim** the wrongly-charged VAT — the US
   buyer is not VAT-registered in the UK, so no reclaim path
   exists. The recovery path is supplier correction.

## 4. Heuristics

> **[Authority gap]**

- **Post-Brexit rules diverged from the EU framework but the
  customer-location principle for B2B services is the same.** The
  framework difference matters most for goods movement and for the
  EU One-Stop Shop registration; for B2B services the place-of-
  supply outcome is similar to EU Article 44.
- **A UK supplier's VAT-registration habit is to charge VAT by
  default.** Suppliers often misapply VAT to non-UK customers
  because their billing system defaults to "charge VAT." This is
  the most common variant of this question.

## 5. Edge cases

> **[Authority gap]**

- **The US buyer has a UK fixed establishment** that the service is
  supplied to (e.g. a UK subsidiary, a UK office) — the place-of-
  supply shifts to the UK; VAT applies. The "no UK presence" fact in
  this case rules that out.
- **The service includes UK-located physical work** (e.g. on-site IT
  installation in a UK data center) — different rules can apply
  for property-related services.
- **The supplier is a small business below the UK VAT threshold** —
  if not VAT-registered, no VAT should appear on any invoice; the
  presence of GB VAT registration here means this exception does
  not apply.

## 6. Process recommendation

For US-incorporated firms with global suppliers, AP should maintain
a **place-of-supply reference** by jurisdiction and service type.
The recurring failure mode is suppliers applying their domestic VAT
default when the customer-location principle would shift place of
supply outside that domestic regime. AP catching this saves the
firm from paying tax that doesn't apply and from a difficult
post-payment reclaim attempt.
