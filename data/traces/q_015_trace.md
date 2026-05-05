# q_015 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to the **Harmonized Tariff Schedule of the United States
> (HTS)** maintained by USITC; **USTR Section 301 actions against
> China** (Federal Register notices for Lists 1–4 and exclusions);
> **19 CFR § 141.1** (importer-of-record liability); **CBP Form
> 7501** (Entry Summary) and CBP "informed compliance" publications.
> Heuristics (§3) and edge cases (§4) flagged `[Authority gap]`.

## 1. The supplier invoice is correct as billed

Under FOB Incoterms 2020 (Free on Board), the supplier's
responsibility ends when goods are loaded onto the vessel at the
named port of shipment. **All US import duties — including Section
301 tariffs — are the buyer's cost**, paid to US Customs and Border
Protection (CBP) at entry, **not paid to the supplier**.

The absence of a Section 301 tariff line on the supplier invoice is
**correct, not an error**. Section 301 tariffs are import-side
duties; they don't flow through the supplier's billing.

## 2. What's actually critical (the buyer's responsibility)

### HTS classification validation
The supplier's claimed HTS classification (8541.59.00) is a starting
point, but **the importer of record (the buyer) is legally
responsible for the correctness of the classification** under 19
CFR § 141.1 — not the supplier. CBP's "informed compliance"
doctrine treats the importer's reasonable-care obligation as
non-delegable.

8541.59.00 covers "Other diodes; transistors and similar
semiconductor devices; semiconductor based transducers..." — for
microcontrollers, the typical correct classification is in **HTS
8542** (Electronic integrated circuits), specifically subheadings
like 8542.31 or 8542.39 for processors/controllers. **The supplier's
classification appears wrong**.

This matters because:

- **Section 301 List 3 / List 4 tariff rates differ across HTS
  codes.** Misclassification can under- or over-state the duty.
- **Misclassification creates importer liability** for unpaid
  duties (plus interest, penalties) on audit. CBP can re-classify
  retroactively.
- **The buyer may also miss available exclusions** if the wrong HTS
  code is used.

### Section 301 applicability and rate
For Chinese-origin microcontrollers, the buyer must determine:

1. The **correct HTS classification** (8542.x most likely).
2. Whether that HTS line is on **Section 301 Lists 1, 2, 3, or 4A**.
3. The **applicable additional duty rate** (historically 7.5–25%
   depending on list and post-Phase-One-deal adjustments).
4. Whether any **product exclusion** applies (USTR has issued and
   periodically renewed exclusions for specific HTS lines).

Both the underlying HTS duty (typically low or zero for
semiconductor codes) **and** the Section 301 additional duty are
the buyer's cost at entry.

### Importer-of-record duties and reasonable care
The "buyer's customs broker has flagged the absence of a Section
301 line" suggests the broker is doing a sanity-check, not
identifying an error. The broker is a service provider; the
importer-of-record retains the legal responsibility (19 CFR §
141.1). The buyer must:

- Confirm or correct the HTS classification.
- Compute the duty owed (base HTS rate + Section 301 additional).
- Pay the duty to CBP at entry via the broker on Form 7501.
- Maintain records for **5 years** per CBP recordkeeping rules.

## 3. Resolution path

1. **Pay the supplier** for the goods value as billed once the
   invoice is otherwise correct. The supplier owes nothing on
   tariffs.
2. **Independently verify HTS classification** with the buyer's
   customs broker / trade-compliance function. Do not rely on the
   supplier's HTS code.
3. **Compute total landed cost** including Section 301 additional
   duty. This is a budgeting and pricing question, not a supplier
   pushback question.
4. **Ensure recordkeeping** — supplier invoice, BOL, packing list,
   CBP entry summary, classification reasoning, duty payment
   evidence — for the 5-year window.

## 4. Heuristics

> **[Authority gap]**

- **HTS classification is the importer's responsibility, period.**
  Suppliers' HTS codes are advisory and frequently wrong; CBP holds
  the importer liable for the actual classification.
- **Section 301 is paid to CBP, never to the supplier.** AP teams
  occasionally reject China invoices for "missing tariff line" — a
  procedural mistake that delays payment without addressing the
  real issue.
- **FOB shifts the customs burden to the buyer at the port of
  shipment.** Under DDP (Delivered Duty Paid), the supplier would
  bear the duty cost; under FOB, the buyer does.

## 5. Edge cases

> **[Authority gap]**

- **The supplier offers DDP terms instead** — the supplier handles
  US import including Section 301; supplier's invoice would show a
  loaded price. Importer-of-record can still be the supplier or its
  US agent; classification responsibility flows to whoever signed
  the entry.
- **Goods are entered under a duty-deferral mechanism** (foreign-
  trade zone, bonded warehouse, drawback) — the duty calculation is
  same but timing/recovery shifts.
- **Available USTR exclusion for the HTS line** — the buyer can
  claim exclusion at entry; documenting the exclusion claim is its
  own audit trail.
- **Country-of-origin question** — if the chips were assembled in
  China but the substantive transformation happened elsewhere, the
  origin determination is itself a CBP-defensible analysis.

## 6. Process recommendation

For any China-origin import program, the firm should run a periodic
HTS classification review with trade-compliance function (or
external counsel). Supplier-provided HTS codes should be treated as
advisory inputs, not as the basis for entry. The Section 301 program
has changed materially several times since 2018; classification
audits catch both over- and under-payment.
