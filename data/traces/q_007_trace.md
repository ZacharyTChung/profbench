# q_007 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **EU Council Directive 2006/112/EC** (the EU VAT
> Directive), Articles 44 (B2B place of supply) and 196 (reverse
> charge); **Council Implementing Regulation (EU) 282/2011**, Article
> 22 (establishment-confirmation requirement on the supplier);
> European Commission *Explanatory Notes on EU VAT Place of Supply
> Rules*. Heuristics (§3) and edge cases (§4) are flagged
> `[Authority gap]`. **q_007 is the question most exposed to author-
> depth limits in trade_and_tax** — see `REVIEW_REQUEST.md`.

## 1. The VAT is incorrectly charged

Under EU VAT B2B place-of-supply rules, the place of supply for a
service supplied to a taxable person is **where the customer is
established or has a fixed establishment to which the service is
supplied** (Council Directive 2006/112/EC Article 44).

Two facts determine the answer here:

1. The buyer is **US-incorporated with no EU permanent establishment**
   — the buyer's establishment for VAT purposes is the US.
2. The buyer's German VAT registration (DE123456789) was triggered by
   a **consignment-stock arrangement**, not by establishing a fixed
   place of business in Germany.

Holding a VAT registration in a member state is **not equivalent to
having a fixed establishment** there. The German VAT registration
was created for the limited purpose of accounting for VAT on the
consignment-stock transactions, not because the buyer set up
operations in Germany.

The relevant "capacity" in which the buyer received the consulting
service is its **US-establishment capacity**, not its
German-VAT-registration capacity. The service is **outside the scope
of EU VAT** — the place of supply is the US.

## 2. The Article 22 establishment-confirmation requirement

Under **Council Implementing Regulation 282/2011, Article 22**, the
supplier is required to confirm which establishment the service is
supplied to before applying VAT. The supplier should have asked the
customer for a written confirmation of the establishment receiving
the service. The fact that the supplier saw a German VAT ID on file
is **not sufficient** — Article 22 specifically requires the
establishment determination, not the VAT-ID-based assumption.

The supplier's procedural failure here is part of why the wrong VAT
treatment was applied.

## 3. AP actions

1. **Hold the invoice.** Do not pay the German VAT.
2. **Request a corrected invoice** from the supplier showing the
   service as outside-the-scope of EU VAT (typically annotated
   "reverse charge — Article 44 EU VAT Directive" or equivalent).
3. **Provide the supplier with a written establishment confirmation**
   stating that the service is supplied to the US establishment, not
   to any German fixed establishment, in line with Article 22.
4. **Do not attempt to reclaim the VAT** through the German
   registration. The VAT was wrongly charged; the recovery path is
   supplier correction, not customer reclaim. Reclaiming wrongly-
   charged VAT through a registration that is not the establishment
   receiving the service can create its own audit issue.

## 4. Reverse-charge applicability

Because the buyer is established outside the EU, **reverse charge
under Article 196 does not apply** in the standard B2B-within-EU
sense. The transaction is simply outside the scope of EU VAT.

If the service had been supplied to an EU-established taxable person
in a different member state, Article 196 reverse charge would have
applied — the supplier would invoice without VAT and the customer
would self-account in their own member state. That is not the
situation here.

## 5. Heuristics

> **[Authority gap]**

- **VAT registration ≠ fixed establishment.** This is the single
  most-confused distinction in EU VAT B2B services analysis.
  Registration for a specific transaction class (consignment stock,
  distance sales) does not create the establishment that determines
  place of supply.
- **The supplier's Article 22 obligation is the customer's
  protection.** A supplier that did not request the establishment
  confirmation has applied VAT on assumption rather than evidence;
  the correction obligation is on the supplier.

## 6. Edge cases

> **[Authority gap]**

- **The buyer has a fixed establishment in Germany** (a small office,
  a few employees) **but the service is supplied to the US head
  office.** Article 22 requires evidence of which establishment the
  service is supplied to; the Article 44 analysis applies to that
  establishment. Documentation matters.
- **The service is performed on physical property located in the EU
  member state** (e.g., real-estate consulting on a building in
  Frankfurt). Different place-of-supply rule applies (Article 47);
  the analysis above does not.
- **Mixed-supply contracts** with both consulting and consignment-
  stock components require separate place-of-supply analysis per
  component.

## 7. Process recommendation

For a US-incorporated entity holding EU VAT registrations, AP should
maintain a **document of capacity** for each registration — what
establishment created the registration, what transaction classes it
covers, and which suppliers have been notified of the establishment-
receiving-the-service. This document is the firm's Article 22
instrument from the customer side.
