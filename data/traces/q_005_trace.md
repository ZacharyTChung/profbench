# q_005 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **Incoterms 2020 (ICC Publication 723E)**, specifically
> the FCA rule (Free Carrier) at A4 / A6 / A9 (seller's obligations)
> and B4 / B6 / B9 (buyer's obligations). Heuristics (§3) and edge
> cases (§4) are flagged `[Authority gap]`.

## 1. The Incoterm sets the cost split

**FCA Hamburg port terminal** (Incoterms 2020) means the seller's
delivery obligation is to deliver the goods, **cleared for export**,
to the carrier nominated by the buyer at the named place. The seller
bears all costs up to and including delivery at that named place;
the buyer bears costs from that point onward, including main
carriage.

When the named place is **not the seller's premises** (here, "Hamburg
port terminal" rather than the seller's Stuttgart facility), the
seller is responsible for delivery to that named place — meaning
inland freight from Stuttgart to Hamburg is **the seller's cost**, not
billable separately to the buyer.

## 2. Line-by-line classification

### Line 1 — Components €50,000.00
**Accept.** Goods value is the contracted PO amount.

### Line 2 — Inland freight, Stuttgart → Hamburg €1,800.00
**Push back.** Under FCA at a named place not equal to the seller's
premises, transport to the named place is the seller's cost (per
Incoterms 2020 FCA A4). The seller cannot bill this separately; it
should be embedded in the unit price or absorbed.

### Line 3 — Export clearance fees €450.00
**Push back.** FCA A7 (export clearance) makes the seller responsible
for **carrying out and paying for** all export-clearance formalities
required by the country of export. This is a seller cost, not
billable.

### Line 4 — Loading at Hamburg terminal €350.00
**Borderline; depends on configuration.** Under FCA A4, when delivery
is at a place other than the seller's premises, the seller is
considered to have delivered when the goods are placed at the
disposal of the carrier *on the seller's means of transport, ready
for unloading*. Loading onto the buyer's nominated carrier at the
terminal is **the buyer's responsibility** under the standard
reading. So this charge from the seller is questionable — clarify
the operational details before paying.

### Line 5 — Marine freight, Hamburg → US port €4,200.00
**Push back to the seller — should not be on this invoice at all.**
Under FCA, main carriage is the buyer's cost arranged with the
buyer's carrier. If the seller arranged it, that's a deviation from
the agreed Incoterm and should be addressed contractually before
paying. If it represents a charge the seller's freight forwarder
incurred and is passing through, that's still the buyer's cost only
if the buyer authorized the arrangement — otherwise reject.

## 3. Heuristics

> **[Authority gap]**

- **The Incoterm wins over invoice line items.** When the invoice
  contradicts the Incoterm, the contractual default is the Incoterm,
  not the invoice.
- **"FCA seller's premises" vs "FCA named place" is the most
  commonly confused Incoterm distinction.** Under FCA seller's
  premises, the seller's cost stops at their loading dock. Under FCA
  named place ≠ premises, the seller's cost extends to that named
  place.

## 4. Edge cases

> **[Authority gap]**

- **The PO uses "FCA Hamburg" without specifying terminal vs
  airport vs city** — defaults vary by industry and prior course of
  dealing. Clarify at PO issuance, not at invoice review.
- **Buyer-instructed exception** where the buyer asked the seller to
  arrange main carriage and pass through cost — legitimate but
  requires a written instruction; absent the instruction, reject.

## 5. Resolution

Hold the invoice. Request a corrected invoice from the seller showing
only the goods value. If lines 2–5 represent costs the buyer has
accepted in side-channel correspondence, those costs should be added
to the PO via change order before the invoice issues, not bolted on
ex-post.
