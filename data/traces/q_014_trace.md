# q_014 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to the **Excise Tax Act (Canada)**, particularly Schedule
> VI Part V (zero-rated exports of services) and section 142
> (place-of-supply rules); **CRA GST/HST Memorandum 4.5.3**
> (Exports — Services and Intellectual Property); **CRA GST/HST
> Notice 191** (place-of-supply for B2B services). Heuristics (§3)
> and edge cases (§4) flagged `[Authority gap]`.

## 1. The HST is incorrectly charged

Under Canadian GST/HST place-of-supply rules for B2B services, the
place of supply for services performed for a **non-resident customer
with no permanent establishment in Canada** is generally **outside
Canada — zero-rated** (technically, an *exported service* under the
Excise Tax Act Schedule VI Part V).

The supplier's reasoning ("work originated from Toronto") confuses
**where the work was performed** with **place of supply**. Place of
supply turns on the customer's residence and presence, not the
supplier's geography.

## 2. Reasoning

### Place of supply for services to non-residents
Per Excise Tax Act Schedule VI Part V (Exported Supplies), services
supplied to a non-resident person are zero-rated for GST/HST
purposes if specific conditions are met:

- The customer is a **non-resident of Canada** at the time the
  service is performed.
- The service is **not in respect of real property in Canada**, not
  a transportation service, and not on tangible property situated
  in Canada at the time of the service.
- The customer is **not in Canada** at any time when the customer
  has contact with the supplier in relation to the supply.

Strategy consulting for a US buyer with no Canadian presence
satisfies the export-services test.

### The "work performed in Canada" misunderstanding
The fact that two weeks of the engagement were performed at the
buyer's New York office (US-located) reinforces the export
treatment, not the supplier's HST claim. Even if all the work had
been performed in Canada (the consultant working from Toronto), the
service is still supplied to the non-resident buyer and qualifies
for zero-rating under Schedule VI Part V if the standard conditions
are met. **Where the supplier's input labor occurs is not the
controlling factor.**

## 3. AP actions

1. **Hold the invoice.** Do not pay the HST portion.
2. **Request a corrected invoice** showing the service as
   **zero-rated for GST/HST** under Schedule VI Part V (Excise Tax
   Act). The corrected invoice should typically reference the
   non-resident export classification.
3. **Pay the service portion** once the corrected invoice is
   received.
4. **Do not attempt to reclaim the wrongly-charged HST** — the US
   buyer is not GST/HST-registered in Canada, so no reclaim path
   through Canadian filings exists. The recovery path is supplier
   correction.

## 4. Documentation expectations

The supplier needs to retain documentation supporting zero-rating
(per CRA GST/HST Memorandum 4.5.3):

- Evidence of the customer's non-resident status (typically a
  written declaration from the customer, or commercial documentation
  showing the customer's address outside Canada).
- Evidence of the service classification (engagement letter
  describing the consulting work).
- Evidence the customer is not in Canada when contacting the
  supplier (typically not a high bar for ordinary B2B engagements).

The buyer can assist by providing a non-residence declaration if
requested.

## 5. Heuristics

> **[Authority gap]**

- **Where the work was performed is not controlling.** Place of
  supply for services turns on the customer's residence and
  presence, not the supplier's labor location.
- **Canadian suppliers default to charging HST.** The supplier's
  billing system defaults to applying HST per the supplier's home
  province. Manually overriding for non-resident customers requires
  a deliberate choice the supplier may not make automatically.
- **The 2-weeks-in-NY fact is irrelevant to the HST question** —
  it's an income-tax / nexus question for the consultant
  personally, not a place-of-supply question for the firm.

## 6. Edge cases

> **[Authority gap]**

- **The service relates to real property in Canada** (e.g.
  consulting on a Canadian-located building) — different rule;
  HST applies based on property location.
- **The buyer has a Canadian permanent establishment** that the
  service is supplied to — HST applies (no longer a non-resident
  export).
- **The service is supplied to multiple recipients, some Canadian
  and some not** — apportionment may apply; the export portion
  zero-rated, the Canadian portion taxable.

## 7. Process recommendation

For US firms engaging Canadian suppliers regularly, AP should
maintain a **non-resident declaration template** ready to send to
suppliers on request. This makes the supplier's documentation burden
trivial and removes the "I had to charge HST because I had no
documentation" excuse.
