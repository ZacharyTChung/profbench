# ProfBench comparison — run `1af59657-b7b7-48c1-8695-d18f27040d68`

For each question below: read the model's response next to the ideal answer, then categorize:

- **(a) model fell short** — keep the question, score is honest
- **(b) ideal_answer too narrow** — the model's response is actually acceptable; broaden the ideal answer (do not change the question)
- **(c) rubric miscalibrated** — tier definitions need to be more specific so the grader doesn't mark partial answers down unfairly

Only (b) and (c) justify editing `data/questions.json`. (a) is the benchmark working as intended.

---

## q_005 — trade_and_tax · medium · **score 0/2** (model: `claude-haiku-4-5`)

_Expected failure mode: applying domain conventions_

### Question

Review the supplier invoice against the PO and Incoterms. Which charges should the buyer accept, and which should be pushed back to the supplier? Cite the Incoterms 2020 rule.

### Context

```
PO from US buyer to a German manufacturer:
  Goods:        €50,000 of electronic components
  Incoterms:    FCA Hamburg (Incoterms 2020)
  Named place:  Hamburg port terminal

Supplier invoice (in EUR):
  Line 1: Components                           €50,000.00
  Line 2: Inland freight, Stuttgart → Hamburg   €1,200.00
  Line 3: Export customs clearance fee            €350.00
  Line 4: Loading/handling at Hamburg terminal     €180.00
  Line 5: Marine cargo insurance                   €420.00
  Total:                                         €52,150.00

Separately, the buyer has received an invoice from its own freight forwarder for ocean freight Hamburg → New York and US import duty.
```

### Rubric

- **0**: Accepts the supplier invoice as billed, or applies CIF/CIP/DAP cost allocation to FCA, or gets the freight allocation backwards
- **1**: Correctly rejects the inland freight and export clearance lines but mishandles insurance, terminal handling, or fails to cite Incoterms 2020 FCA
- **2**: Correctly addresses every line with reference to FCA seller/buyer obligations, flags the terminal-handling ambiguity rather than guessing, and references Incoterms 2020 FCA explicitly

### Ideal answer

Under Incoterms 2020 FCA at a named place that is not the seller's premises (here, 'Hamburg port terminal'), the seller's delivery obligation is to deliver the goods, cleared for export, to the carrier nominated by the buyer at the named place. The seller bears all costs up to and including delivery at that named place; the buyer bears costs from that point onward, including the main carriage.

Line-by-line:
- Line 1, Components €50,000 — accept. PO price.
- Line 2, Inland freight Stuttgart → Hamburg €1,200 — REJECT. Pre-carriage to the named place is the seller's cost under FCA. It must already be embedded in the price; charging it separately is a double charge unless the PO explicitly priced ex-works and added pre-carriage as a quoted line, which is not the case here.
- Line 3, Export customs clearance €350 — REJECT. Under FCA, the seller is responsible for export clearance and bears the cost (Incoterms 2020 FCA, A7/A9). Cannot be on-billed.
- Line 4, Loading/handling at Hamburg terminal €180 — DEPENDS. Under FCA at a terminal that is not the seller's premises, the seller is considered to have delivered when the goods are placed at the disposal of the carrier at the named place; loading onto the buyer's onward carrier is generally the buyer's cost. Terminal handling charges (THC) at the FCA point are commonly the buyer's responsibility unless the parties have agreed otherwise. Push back to clarify whether this is THC for receipt at terminal (seller) or loading onto the ocean carrier (buyer); if loading onto buyer's vessel, accept; if receipt-side handling, reject.
- Line 5, Marine cargo insurance €420 — REJECT. Under FCA, neither party has a contractual obligation to insure (Incoterms 2020 FCA, A5/B5). If the buyer wanted insurance, they would arrange it themselves. Supplier cannot impose insurance and on-bill it.

Separately invoiced freight forwarder charges (ocean freight, US import duty, US delivery) are correctly the buyer's responsibility under FCA — accept those on the forwarder invoice, not the supplier invoice.

Action: hold supplier invoice for €52,150; request a corrected invoice for €50,000 + (terminal-handling line only if it relates to loading onto the buyer's vessel, with documentation). If the supplier disputes, the contract Incoterms term and Incoterms 2020 reference (ICC publication 723E) is the authority.

Note on a 2020-vs-2010 nuance: Incoterms 2020 added an option for FCA shipments to specify that the buyer instruct the carrier to issue a bill of lading 'on board' to the seller — relevant for L/C settlement, not for cost allocation here.

### Model response

# Analysis of Supplier Invoice Against FCA Hamburg (Incoterms 2020)

## FCA Definition (Incoterms 2020)
Under FCA, the seller's obligations end when goods are "placed at the disposal of the buyer" at the named place (Hamburg terminal). The seller must:
- Deliver goods to the carrier/terminal at the named place
- Bear costs of inland transport to that point
- Handle export clearance
- The buyer assumes all costs and risks **from delivery at the named place onward**

---

## Line-by-Line Review

| Line Item | Should Accept? | Reasoning |
|-----------|---|---|
| **Components €50,000** | ✅ YES | Core goods per PO |
| **Inland freight Stuttgart → Hamburg €1,200** | ✅ YES | Pre-delivery transport to named place; seller's obligation under FCA Rule A4 |
| **Export customs clearance €350** | ✅ YES | Seller must clear goods for export per FCA Rule A2 |
| **Loading/handling at Hamburg terminal €180** | ❌ **REJECT** | This occurs **at** the named place where risk/cost transfers to buyer. Ambiguous but typically the buyer arranges final terminal handling under FCA |
| **Marine cargo insurance €420** | ❌ **REJECT** | Seller has no obligation to insure beyond the named place. Per FCA Rule A5, the buyer arranges insurance. This is the buyer's cost. |

---

## Recommendation

**Accept:** €51,550.00 (Components + inland freight + export clearance)

**Push back:** €600.00 (terminal handling + insurance)

### Rationale
FCA transfers risk and cost responsibility at the named place. The supplier invoices for services **beyond** that point, which are the buyer's responsibility. The buyer—or buyer's freight forwarder—should absorb these costs along with ocean freight and import duties already being handled separately.

### Grader verdict

- **Score:** 0
- **Confidence:** high
- **Reasoning:** The candidate accepts the inland freight (€1,200) and export clearance (€350) charges as separate line items, which is incorrect. Under FCA, while these are the seller's obligations, they should be embedded in the price, not billed separately on top of the PO price of €50,000. This is the 'gets the freight allocation backwards' / accepts double-charging error. The candidate also fails to flag the terminal-handling ambiguity properly (rejects outright rather than noting the dependency on whether it's receipt-side or loading onto buyer's vessel). The insurance rejection is correct, but the overall handling of the invoice is fundamentally wrong - the buyer would be paying twice for inland freight and export clearance.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_001 — supplier_data · easy · **score 1/2** (model: `claude-opus-4-7`)

_Expected failure mode: domain vocabulary and normalization_

### Question

Are these two supplier master records duplicates? If yes, what is the correct resolution and which record should survive as the canonical entry? Justify briefly.

### Context

```
Record A:
  Name:    Acme Industrial Corp
  TIN:     12-3456789
  Address: 100 Main St, Suite 200, Newark, NJ 07102
  Bank:    Chase ****4521
  Status:  Active, last invoice 30 days ago

Record B:
  Name:    ACME INDUSTRIAL CORPORATION
  TIN:     123456789
  Address: 100 Main Street, Newark, NJ 07102
  Bank:    Chase ****4521
  Status:  Active, no activity in 18 months
```

### Rubric

- **0**: Says they are not duplicates, or fails to identify the TIN match, or recommends keeping both records active without rule-out reasoning, or merges without any control-step consideration
- **1**: Identifies them as duplicates via TIN normalization but treats name/address/contact variance as purely cosmetic, does not consider DBA or acquisition exceptions, OR misses the duplicate-payment lookback / open-document migration / bank-history checks before deactivation
- **2**: Two-step framing (identity vs operational merge); identifies TIN as primary identity key; explicitly rules out DBA structure, acquisition/restructuring, and operating-unit separation as exception classes before merging; treats address/name/contact divergences as investigation triggers not cosmetic; prescribes the full pre-deactivation control sweep (open-doc migration, duplicate-payment lookback ≥24mo, bank-history check); addresses survivor selection with reasoning and documentation for SOX evidence

### Ideal answer

Yes, these are duplicates — but the analysis is two-step, not one-step. The first step is identity (is this the same legal entity?); the second is operational consolidation (should the two records be merged?). They are not the same question.

**Step 1 — identity (TIN is primary).** The TINs are identical: '12-3456789' and '123456789' are the same nine-digit EIN; the hyphen is display formatting and TIN normalization (strip non-digits) is the correct primary-key match. With matching TIN, the records refer to the same legal entity for federal tax purposes. Name variance ('Corp' vs 'CORPORATION', case) and minor address formatting ('St' vs 'Street', the missing suite line) corroborate but don't determine — TIN match alone is sufficient for identity.

**Step 2 — investigate before merging.** Same legal entity does not automatically mean the two records should be merged. Three exception classes need to be ruled out before consolidation:

- **DBA structure.** A single legal entity (one TIN) frequently operates under multiple trade names — DBAs registered separately. 'Acme Industrial Corp' and 'ACME INDUSTRIAL CORPORATION' could be one DBA structure where one record represents the parent legal name and another represents an active DBA. Same TIN, different names, both valid records — deactivating either one breaks invoicing for that DBA. Confirm with the supplier whether they file as a single trade name or operate DBAs before merging.
- **Acquisition / restructuring.** If the supplier was acquired in the last 24 months, both records may be intentionally retained: one for the legacy entity continuing limited operations under inherited contracts, one for the post-acquisition business. The TIN can be inherited or transitional. Pull the W-9 dates on both records and check whether they bracket a known acquisition or restructuring; if so, do not merge without confirming with the supplier's controller which entity is the surviving operating unit.
- **Operating-unit separation under one TIN.** Even within a single legal entity with no DBAs and no recent M&A, divisions can intentionally maintain separate vendor records to keep AP segregated by business unit (different remit-to, different contacts, different cost centers). Merging breaks that segregation.

The address, name, and contact divergences in this fact pattern are mild enough to fit "same operating unit, formatting variance" — but in any real case they should be questioned, not waved off as cosmetic. Address differences in particular should be confirmed: a change to a P.O. box, an unusual locality, or a recent change correlated with the dormancy is a fraud-screen indicator that overrides the consolidation question entirely.

**Step 3 — if Step 2 confirms a true duplicate, consolidate with the following control steps in order:**

1. Migrate open documents from Record B to Record A — open POs, in-flight invoices, recurring payment runs, active contracts. Buyer/contract owner sign-off on each migration. Don't deactivate B under live POs; that breaks the AP path on the next invoice.
2. Run a duplicate-payment lookback across both vendor IDs over a window of at least Record B's lifespan or the firm's standard SOX lookback (typically 24 months), whichever is longer. Match on amount within ±$1, normalized invoice numbers, and dates within a 30-day window. Investigate any hits *before* consolidation — once merged, the trail across two IDs gets harder to reconstruct.
3. Pull the bank-account history on both records. Even though both currently show ****4521, was there ever a divergence? A period where Record B's bank was different is a fraud-screen flag (someone may have routed payments to a side account before you started looking).
4. Survivor selection: Record A (active, recent activity, more complete address). Deactivate B with a cross-reference to A so historical reporting rolls up cleanly.

**Documentation:** the consolidation decision, the DBA/acquisition rule-out, the lookback results, and the bank-history check are all SOX-relevant evidence for the next vendor-master walkthrough. Maker-checker on the consolidation execution: AP clerk proposes, master-data steward executes, audit-line reviewer signs off.

### Model response

# Duplicate Determination

**Yes — Records A and B are duplicates of the same legal entity.** This is a classic master-data duplication pattern, not two distinct suppliers.

## Evidence Supporting the Match

| Attribute | Record A | Record B | Assessment |
|---|---|---|---|
| Legal Name | Acme Industrial Corp | ACME INDUSTRIAL CORPORATION | Match (case + "Corp"/"Corporation" abbreviation variant) |
| TIN/EIN | 12-3456789 | 123456789 | **Exact match** (formatting only — IRS EINs are 9 digits) |
| Address | 100 Main St, Suite 200 | 100 Main Street | Same street/city/ZIP; A has suite-level granularity |
| Bank Account | Chase ****4521 | Chase ****4521 | **Exact match** |
| ZIP | 07102 | 07102 | Match |

The **TIN + bank account + address + name** quadruple match is decisive. TIN alone is generally sufficient under IRS rules (one EIN per legal entity); combined with an identical bank routing/account, the probability of a false-positive match is effectively zero.

## Recommended Resolution

**Survivor: Record A.** Record B should be **merged into A and deactivated** (not deleted — retain for audit trail).

### Justification for choosing A as canonical
1. **Recent transactional activity** (invoice 30 days ago) — A is the record AP is actually paying against. Disturbing it risks payment disruption.
2. **More complete address** — includes the Suite 200 sub-premise, which improves 1099 deliverability and remit-to accuracy.
3. **Properly formatted TIN** (`12-3456789`) — matches IRS EIN presentation standard and is more likely to pass TIN-matching validation.
4. **Record B has been dormant 18 months** — strong indicator it is a legacy/orphaned duplicate created before deduplication controls or via a separate onboarding event (e.g., different requester, different business unit).

## Resolution Steps (Operational)

1. **Freeze Record B** immediately (block for new POs and payments) to prevent further divergence.
2. **Reassign open documents on B** — re-point any open POs, contracts, unpaid invoices, or pending receipts from B → A. Verify there are none given the 18-month inactivity, but confirm.
3. **Merge transaction history** — link B's historical spend, 1099 history, and document attachments to A for reporting continuity (most ERPs, e.g., SAP MDG, Oracle, Coupa, support a vendor merge function).
4. **Mark B as "Merged — Duplicate of A"** with a cross-reference field pointing to A's vendor ID. Set status to Inactive/Blocked. Do **not** hard-delete — retain for 7-year audit/tax retention.
5. **Validate downstream**: 1099 YTD totals, open AP aging, and any procurement catalog references now resolve to A only.
6. **Root-cause check**: investigate why duplicate was created (likely TIN was entered without the hyphen, bypassing the duplicate-check rule). Tighten the master-data rule to **normalize TIN (strip non-numerics) before uniqueness check**, and apply fuzzy-match on name + exact match on TIN/bank at vendor creation.

## Risk Flags to Clear Before Merge
- Confirm both records have **no open payments in flight** to avoid double-pay.
- Confirm 1099-MISC/1099-NEC totals for the current tax year are not split across both records; if they are, consolidate before year-end filing.
- Verify the bank account on file matches the supplier's most recent remittance instruction (the matching ****4521 is supportive but should be re-confirmed via callback control if any payment data changes during the merge).

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies the records as duplicates via TIN normalization and selects Record A as survivor with good reasoning. It includes some control steps (freeze, reassign open docs, merge history, cross-reference, retention) and even adds a root-cause check and 1099 consideration. However, it misses key rubric elements for a 2: (1) no two-step framing distinguishing identity from operational merge; (2) does not rule out DBA structure, acquisition/restructuring, or operating-unit separation as exception classes — instead assumes duplication and proceeds to merge; (3) treats name/address variances as cosmetic/supportive rather than investigation triggers; (4) does not prescribe a duplicate-payment lookback (≥24 months) across both vendor IDs; (5) does not call for a bank-history divergence check as a fraud screen. These are substantive omissions that the rubric explicitly flags for the 1-tier.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_001 — supplier_data · easy · **score 1/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: domain vocabulary and normalization_

### Question

Are these two supplier master records duplicates? If yes, what is the correct resolution and which record should survive as the canonical entry? Justify briefly.

### Context

```
Record A:
  Name:    Acme Industrial Corp
  TIN:     12-3456789
  Address: 100 Main St, Suite 200, Newark, NJ 07102
  Bank:    Chase ****4521
  Status:  Active, last invoice 30 days ago

Record B:
  Name:    ACME INDUSTRIAL CORPORATION
  TIN:     123456789
  Address: 100 Main Street, Newark, NJ 07102
  Bank:    Chase ****4521
  Status:  Active, no activity in 18 months
```

### Rubric

- **0**: Says they are not duplicates, or fails to identify the TIN match, or recommends keeping both records active without rule-out reasoning, or merges without any control-step consideration
- **1**: Identifies them as duplicates via TIN normalization but treats name/address/contact variance as purely cosmetic, does not consider DBA or acquisition exceptions, OR misses the duplicate-payment lookback / open-document migration / bank-history checks before deactivation
- **2**: Two-step framing (identity vs operational merge); identifies TIN as primary identity key; explicitly rules out DBA structure, acquisition/restructuring, and operating-unit separation as exception classes before merging; treats address/name/contact divergences as investigation triggers not cosmetic; prescribes the full pre-deactivation control sweep (open-doc migration, duplicate-payment lookback ≥24mo, bank-history check); addresses survivor selection with reasoning and documentation for SOX evidence

### Ideal answer

Yes, these are duplicates — but the analysis is two-step, not one-step. The first step is identity (is this the same legal entity?); the second is operational consolidation (should the two records be merged?). They are not the same question.

**Step 1 — identity (TIN is primary).** The TINs are identical: '12-3456789' and '123456789' are the same nine-digit EIN; the hyphen is display formatting and TIN normalization (strip non-digits) is the correct primary-key match. With matching TIN, the records refer to the same legal entity for federal tax purposes. Name variance ('Corp' vs 'CORPORATION', case) and minor address formatting ('St' vs 'Street', the missing suite line) corroborate but don't determine — TIN match alone is sufficient for identity.

**Step 2 — investigate before merging.** Same legal entity does not automatically mean the two records should be merged. Three exception classes need to be ruled out before consolidation:

- **DBA structure.** A single legal entity (one TIN) frequently operates under multiple trade names — DBAs registered separately. 'Acme Industrial Corp' and 'ACME INDUSTRIAL CORPORATION' could be one DBA structure where one record represents the parent legal name and another represents an active DBA. Same TIN, different names, both valid records — deactivating either one breaks invoicing for that DBA. Confirm with the supplier whether they file as a single trade name or operate DBAs before merging.
- **Acquisition / restructuring.** If the supplier was acquired in the last 24 months, both records may be intentionally retained: one for the legacy entity continuing limited operations under inherited contracts, one for the post-acquisition business. The TIN can be inherited or transitional. Pull the W-9 dates on both records and check whether they bracket a known acquisition or restructuring; if so, do not merge without confirming with the supplier's controller which entity is the surviving operating unit.
- **Operating-unit separation under one TIN.** Even within a single legal entity with no DBAs and no recent M&A, divisions can intentionally maintain separate vendor records to keep AP segregated by business unit (different remit-to, different contacts, different cost centers). Merging breaks that segregation.

The address, name, and contact divergences in this fact pattern are mild enough to fit "same operating unit, formatting variance" — but in any real case they should be questioned, not waved off as cosmetic. Address differences in particular should be confirmed: a change to a P.O. box, an unusual locality, or a recent change correlated with the dormancy is a fraud-screen indicator that overrides the consolidation question entirely.

**Step 3 — if Step 2 confirms a true duplicate, consolidate with the following control steps in order:**

1. Migrate open documents from Record B to Record A — open POs, in-flight invoices, recurring payment runs, active contracts. Buyer/contract owner sign-off on each migration. Don't deactivate B under live POs; that breaks the AP path on the next invoice.
2. Run a duplicate-payment lookback across both vendor IDs over a window of at least Record B's lifespan or the firm's standard SOX lookback (typically 24 months), whichever is longer. Match on amount within ±$1, normalized invoice numbers, and dates within a 30-day window. Investigate any hits *before* consolidation — once merged, the trail across two IDs gets harder to reconstruct.
3. Pull the bank-account history on both records. Even though both currently show ****4521, was there ever a divergence? A period where Record B's bank was different is a fraud-screen flag (someone may have routed payments to a side account before you started looking).
4. Survivor selection: Record A (active, recent activity, more complete address). Deactivate B with a cross-reference to A so historical reporting rolls up cleanly.

**Documentation:** the consolidation decision, the DBA/acquisition rule-out, the lookback results, and the bank-history check are all SOX-relevant evidence for the next vendor-master walkthrough. Maker-checker on the consolidation execution: AP clerk proposes, master-data steward executes, audit-line reviewer signs off.

### Model response

## Duplicate Assessment: **Yes, these are duplicates**

### Evidence of Identity

| Field | Record A | Record B | Assessment |
|-------|----------|----------|------------|
| Name | Acme Industrial Corp | ACME INDUSTRIAL CORPORATION | Same entity, abbreviated vs. full legal name |
| TIN | 12-3456789 | 123456789 | **Identical** — same EIN, different formatting only |
| Address | 100 Main St, Suite 200, Newark, NJ 07102 | 100 Main Street, Newark, NJ 07102 | Same address; A includes suite detail |
| Bank | Chase ****4521 | Chase ****4521 | **Identical** |

The TIN is the definitive identifier — it is the same number in both records. Combined with matching bank account and address, this is unambiguously one legal entity.

---

## Resolution

### ✅ Record A should survive as the canonical entry

**Reasons:**

1. **Active and current** — transacted within 30 days; Record B has been dormant 18 months, suggesting it is a stale/legacy entry likely created by a data entry variant
2. **More complete address** — includes Suite 200, which is the more precise mailing/remittance detail
3. **Properly formatted TIN** — the hyphenated format (`12-3456789`) matches IRS EIN standard, reducing downstream compliance risk (e.g., 1099 filing)
4. **Name format** — "Acme Industrial Corp" likely matches the DBA or the name used on active purchase orders

### Action Items
- **Merge** any open POs, invoices, or payment history from Record B into Record A
- **Inactivate/archive** Record B (do not hard-delete, to preserve audit trail)
- **Enrich** Record A with the full legal name from Record B (`ACME INDUSTRIAL CORPORATION`) stored as an alias/DBA field for legal document matching
- **Root-cause** how the duplicate was created (system migration? manual entry?) to prevent recurrence

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The candidate correctly identifies the records as duplicates via TIN normalization and selects Record A as survivor with reasonable justification. However, it falls short of a 2: it does not provide the two-step framing (identity vs operational merge), does not rule out DBA structure, acquisition/restructuring, or operating-unit separation as exception classes (in fact it casually suggests the name might be a DBA but then proceeds to merge anyway), treats address/name variance as cosmetic rather than investigation triggers, and crucially misses the pre-deactivation control sweep — no duplicate-payment lookback, no bank-history divergence check, and only a vague 'merge open POs' rather than a controlled migration with sign-off. SOX/maker-checker documentation is also absent.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_001 — supplier_data · easy · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: domain vocabulary and normalization_

### Question

Are these two supplier master records duplicates? If yes, what is the correct resolution and which record should survive as the canonical entry? Justify briefly.

### Context

```
Record A:
  Name:    Acme Industrial Corp
  TIN:     12-3456789
  Address: 100 Main St, Suite 200, Newark, NJ 07102
  Bank:    Chase ****4521
  Status:  Active, last invoice 30 days ago

Record B:
  Name:    ACME INDUSTRIAL CORPORATION
  TIN:     123456789
  Address: 100 Main Street, Newark, NJ 07102
  Bank:    Chase ****4521
  Status:  Active, no activity in 18 months
```

### Rubric

- **0**: Says they are not duplicates, or fails to identify the TIN match, or recommends keeping both records active without rule-out reasoning, or merges without any control-step consideration
- **1**: Identifies them as duplicates via TIN normalization but treats name/address/contact variance as purely cosmetic, does not consider DBA or acquisition exceptions, OR misses the duplicate-payment lookback / open-document migration / bank-history checks before deactivation
- **2**: Two-step framing (identity vs operational merge); identifies TIN as primary identity key; explicitly rules out DBA structure, acquisition/restructuring, and operating-unit separation as exception classes before merging; treats address/name/contact divergences as investigation triggers not cosmetic; prescribes the full pre-deactivation control sweep (open-doc migration, duplicate-payment lookback ≥24mo, bank-history check); addresses survivor selection with reasoning and documentation for SOX evidence

### Ideal answer

Yes, these are duplicates — but the analysis is two-step, not one-step. The first step is identity (is this the same legal entity?); the second is operational consolidation (should the two records be merged?). They are not the same question.

**Step 1 — identity (TIN is primary).** The TINs are identical: '12-3456789' and '123456789' are the same nine-digit EIN; the hyphen is display formatting and TIN normalization (strip non-digits) is the correct primary-key match. With matching TIN, the records refer to the same legal entity for federal tax purposes. Name variance ('Corp' vs 'CORPORATION', case) and minor address formatting ('St' vs 'Street', the missing suite line) corroborate but don't determine — TIN match alone is sufficient for identity.

**Step 2 — investigate before merging.** Same legal entity does not automatically mean the two records should be merged. Three exception classes need to be ruled out before consolidation:

- **DBA structure.** A single legal entity (one TIN) frequently operates under multiple trade names — DBAs registered separately. 'Acme Industrial Corp' and 'ACME INDUSTRIAL CORPORATION' could be one DBA structure where one record represents the parent legal name and another represents an active DBA. Same TIN, different names, both valid records — deactivating either one breaks invoicing for that DBA. Confirm with the supplier whether they file as a single trade name or operate DBAs before merging.
- **Acquisition / restructuring.** If the supplier was acquired in the last 24 months, both records may be intentionally retained: one for the legacy entity continuing limited operations under inherited contracts, one for the post-acquisition business. The TIN can be inherited or transitional. Pull the W-9 dates on both records and check whether they bracket a known acquisition or restructuring; if so, do not merge without confirming with the supplier's controller which entity is the surviving operating unit.
- **Operating-unit separation under one TIN.** Even within a single legal entity with no DBAs and no recent M&A, divisions can intentionally maintain separate vendor records to keep AP segregated by business unit (different remit-to, different contacts, different cost centers). Merging breaks that segregation.

The address, name, and contact divergences in this fact pattern are mild enough to fit "same operating unit, formatting variance" — but in any real case they should be questioned, not waved off as cosmetic. Address differences in particular should be confirmed: a change to a P.O. box, an unusual locality, or a recent change correlated with the dormancy is a fraud-screen indicator that overrides the consolidation question entirely.

**Step 3 — if Step 2 confirms a true duplicate, consolidate with the following control steps in order:**

1. Migrate open documents from Record B to Record A — open POs, in-flight invoices, recurring payment runs, active contracts. Buyer/contract owner sign-off on each migration. Don't deactivate B under live POs; that breaks the AP path on the next invoice.
2. Run a duplicate-payment lookback across both vendor IDs over a window of at least Record B's lifespan or the firm's standard SOX lookback (typically 24 months), whichever is longer. Match on amount within ±$1, normalized invoice numbers, and dates within a 30-day window. Investigate any hits *before* consolidation — once merged, the trail across two IDs gets harder to reconstruct.
3. Pull the bank-account history on both records. Even though both currently show ****4521, was there ever a divergence? A period where Record B's bank was different is a fraud-screen flag (someone may have routed payments to a side account before you started looking).
4. Survivor selection: Record A (active, recent activity, more complete address). Deactivate B with a cross-reference to A so historical reporting rolls up cleanly.

**Documentation:** the consolidation decision, the DBA/acquisition rule-out, the lookback results, and the bank-history check are all SOX-relevant evidence for the next vendor-master walkthrough. Maker-checker on the consolidation execution: AP clerk proposes, master-data steward executes, audit-line reviewer signs off.

### Model response

# Duplicate Analysis

## Conclusion
**Yes, these are duplicates with high confidence (95%+).**

## Justification

### Strong Matching Indicators
1. **TIN (Tax ID)**: Both resolve to the same entity
   - Record A: 12-3456789
   - Record B: 123456789
   - These are identical (the hyphen is formatting only)

2. **Business Name**: Functionally identical
   - Minor variations (Corp vs. Corporation, capitalization) are standard formatting differences

3. **Address**: Same location with minor formatting differences
   - Both reference 100 Main St/Street, Newark, NJ 07102
   - Record A includes Suite 200; Record B omits it (likely a detail discrepancy)

4. **Bank Account**: Identical Chase account ending in 4521

### Minor Discrepancies
- **Activity status**: Record A shows recent activity (30 days); Record B shows 18-month inactivity
- **Address detail**: Suite 200 present in A, absent in B

---

## Recommended Resolution

**Record A should survive** as the canonical entry because:

1. **Recency**: Active within 30 days (vs. 18 months dormant) suggests current operational status
2. **Completeness**: Includes Suite 200 detail, providing more precise location information
3. **Data quality**: Recent activity validates the information

**Action items**:
- Merge Record B into Record A
- Consolidate all transaction history from both records
- Update address to include Suite 200
- Investigate the 18-month gap in Record B's activity
- Delete or archive Record B

This consolidation prevents payment splits, duplicate invoicing, and reporting inaccuracies.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** Identifies duplicates via TIN normalization correctly and selects Record A as survivor with reasonable justification. However, treats name/address variances as cosmetic formatting differences rather than investigation triggers. Does not consider DBA structure, acquisition/restructuring, or operating-unit separation as exception classes. Misses the critical pre-deactivation controls: duplicate-payment lookback across both vendor IDs, bank-history check for prior divergence, open-document migration with sign-off, and SOX documentation. The 'merge and delete' recommendation lacks the control sweep required for a score of 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_002 — invoice_processing · easy · **score 1/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: applying domain conventions_

### Question

For each of the five incoming invoices below, classify whether it should be processed as PO-backed or non-PO, and give a one-line reason. Assume a typical mid-market policy: goods purchases require a PO; services > $25k require a PO; recurring utilities and statutory payments are PO-exempt.

### Context

```
1. Invoice from PG&E for $4,820 — monthly electricity for HQ, recurring.
2. Invoice from Salesforce for $84,000 — annual SaaS renewal, last year was on a PO.
3. Invoice from Latham & Watkins for $11,500 — legal services on a retainer, no SOW referenced.
4. Invoice from Staples for $612 — office supplies, references PO #4500987.
5. Invoice from BrandWorks Agency for $48,000 — marketing campaign, references SOW-2024-17.
```

### Rubric

- **0**: Misclassifies two or more invoices, or applies the rules without reference to thresholds/carve-outs
- **1**: Classifies all five correctly but misses the nuance on the SaaS auto-renewal, the legal carve-out conditions, or the after-the-fact PO control issue
- **2**: Classifies all five correctly and surfaces at least two control nuances (auto-renewal-without-PO as rogue spend, after-the-fact PO concern, legal-engagement-letter as PO equivalent)

### Ideal answer

1. PG&E utility — non-PO. Recurring utility under the policy carve-out; covered by an approved utility budget line, not a PO commitment.
2. Salesforce SaaS renewal — PO-backed. Services > $25k threshold; auto-renewal should be on a PO so the commitment is recorded against budget and the term/price are locked. If the renewal arrived without an active PO, that is itself an exception (rogue spend) and should be remediated before payment.
3. Latham & Watkins legal — non-PO is acceptable per typical legal carve-outs (matter-based, hard to scope at PO time), but only if the firm is on the approved counsel list and the spend is within the matter budget set by GC. Otherwise route as exception. The retainer should still hit a contract/engagement letter on file; SOX-relevant orgs often require the engagement letter to function as the PO equivalent.
4. Staples office supplies — PO-backed. Goods purchase referencing PO #4500987; standard 3-way match path (PO + GR + invoice).
5. BrandWorks marketing — PO-backed. Services > $25k. SOW-2024-17 should map to a PO that references the SOW; many orgs treat the SOW as the commitment document but require a PO created from it. If no PO exists, hold the invoice and create one retroactively only if policy permits 'after-the-fact' POs (many do not, and it is a control finding).

### Model response

# Invoice Classification

| # | Vendor | Amount | Classification | Reason |
|---|--------|--------|----------------|--------|
| 1 | PG&E | $4,820 | **Non-PO** | Recurring utility invoice; explicitly exempt from PO requirement under standard policy. |
| 2 | Salesforce | $84,000 | **PO Required (gap)** | Annual SaaS renewal >$25k qualifies as a service requiring a PO, but none is referenced — prior PO must be located or a new one raised before payment. |
| 3 | Latham & Watkins | $11,500 | **Non-PO** | Legal services on retainer fall below the $25k services threshold, so no PO is required; retainer agreement serves as the authorization. |
| 4 | Staples | $612 | **PO-Backed** | Goods purchase with a valid PO referenced (#4500987); process via 3-way match regardless of low value. |
| 5 | BrandWorks Agency | $48,000 | **PO-Backed** | Marketing services >$25k with an SOW referenced (SOW-2024-17); a corresponding PO should exist and must be matched before payment. |

---

## Key Decision Logic

- **Threshold test:** Services ≤ $25k → Non-PO acceptable; Services > $25k → PO required.
- **Goods test:** *Any* goods purchase (Staples) → PO required regardless of amount.
- **Utility/recurring exemption:** PG&E qualifies; no further PO overhead needed.
- **Watch item — Salesforce (#2):** This is the highest-risk invoice in the batch. It is large, has no PO cited, and was previously on a PO, suggesting an oversight. **Do not pay until a PO is issued or formally waived by an authorized approver.**

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** All five invoices are classified correctly (PG&E non-PO, Salesforce PO-required with gap flagged, Latham non-PO, Staples PO-backed, BrandWorks PO-backed). The candidate surfaces the Salesforce auto-renewal-without-PO issue as rogue spend/gap (one nuance). However, it misses the after-the-fact PO control concern for BrandWorks and does not mention the legal engagement letter functioning as a PO equivalent or the conditions (approved counsel list, matter budget) for the legal carve-out. Only one of the required two-plus control nuances is clearly surfaced.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_002 — invoice_processing · easy · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: applying domain conventions_

### Question

For each of the five incoming invoices below, classify whether it should be processed as PO-backed or non-PO, and give a one-line reason. Assume a typical mid-market policy: goods purchases require a PO; services > $25k require a PO; recurring utilities and statutory payments are PO-exempt.

### Context

```
1. Invoice from PG&E for $4,820 — monthly electricity for HQ, recurring.
2. Invoice from Salesforce for $84,000 — annual SaaS renewal, last year was on a PO.
3. Invoice from Latham & Watkins for $11,500 — legal services on a retainer, no SOW referenced.
4. Invoice from Staples for $612 — office supplies, references PO #4500987.
5. Invoice from BrandWorks Agency for $48,000 — marketing campaign, references SOW-2024-17.
```

### Rubric

- **0**: Misclassifies two or more invoices, or applies the rules without reference to thresholds/carve-outs
- **1**: Classifies all five correctly but misses the nuance on the SaaS auto-renewal, the legal carve-out conditions, or the after-the-fact PO control issue
- **2**: Classifies all five correctly and surfaces at least two control nuances (auto-renewal-without-PO as rogue spend, after-the-fact PO concern, legal-engagement-letter as PO equivalent)

### Ideal answer

1. PG&E utility — non-PO. Recurring utility under the policy carve-out; covered by an approved utility budget line, not a PO commitment.
2. Salesforce SaaS renewal — PO-backed. Services > $25k threshold; auto-renewal should be on a PO so the commitment is recorded against budget and the term/price are locked. If the renewal arrived without an active PO, that is itself an exception (rogue spend) and should be remediated before payment.
3. Latham & Watkins legal — non-PO is acceptable per typical legal carve-outs (matter-based, hard to scope at PO time), but only if the firm is on the approved counsel list and the spend is within the matter budget set by GC. Otherwise route as exception. The retainer should still hit a contract/engagement letter on file; SOX-relevant orgs often require the engagement letter to function as the PO equivalent.
4. Staples office supplies — PO-backed. Goods purchase referencing PO #4500987; standard 3-way match path (PO + GR + invoice).
5. BrandWorks marketing — PO-backed. Services > $25k. SOW-2024-17 should map to a PO that references the SOW; many orgs treat the SOW as the commitment document but require a PO created from it. If no PO exists, hold the invoice and create one retroactively only if policy permits 'after-the-fact' POs (many do not, and it is a control finding).

### Model response

# Invoice Classification Analysis

| Invoice | Vendor | Amount | Classification | Reason |
|---------|--------|--------|-----------------|--------|
| 1 | PG&E | $4,820 | **Non-PO** | Recurring utility; PO-exempt per policy |
| 2 | Salesforce | $84,000 | **PO-backed** | SaaS renewal >$25k services threshold; prior PO history confirms process |
| 3 | Latham & Watkins | $11,500 | **Non-PO** | Legal retainer services under $25k threshold; retainer structure typically operates outside PO requirement |
| 4 | Staples | $612 | **PO-backed** | Goods purchase with explicit PO reference (#4500987) |
| 5 | BrandWorks Agency | $48,000 | **PO-backed** | Services >$25k threshold; SOW-2024-17 indicates contractual backing; requires PO support |

## Key Reasoning Notes
- **Salesforce & BrandWorks** both exceed the $25k services trigger, making PO backing mandatory.
- **Latham & Watkins**, while a service provider, falls below the threshold at $11.5k and operates on a retainer model (typically pre-authorized without per-invoice POs).
- **Staples** is goods-based and includes an explicit PO reference.
- **PG&E** qualifies for the utilities exemption as a recurring statutory payment.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** All five invoices are classified correctly with proper reference to thresholds and carve-outs. However, the response misses the key control nuances: it does not flag the auto-renewal-without-PO as potential rogue spend, does not raise the after-the-fact PO concern for BrandWorks, and does not mention the engagement letter functioning as a PO equivalent for legal. It also doesn't condition the legal non-PO treatment on approved counsel list/matter budget.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_003 — invoice_processing · medium · **score 1/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: multi-step arithmetic and control reasoning_

### Question

Walk through the 3-way match for the documents below. Identify every exception, quantify the variance, and state the resolution path including which roles must approve and which controls apply.

### Context

```
PO #4500-22871
  Line 1: 100 units of part #X-77 @ $10.00 = $1,000.00
  Tolerance: ±2% price, ±5% quantity
  Status: Open, no prior receipts

Goods Receipt (GR) #50032118
  Line 1: 95 units received, marked 'final delivery — short ship per supplier'
  Receiver: warehouse staff

Invoice INV-88412 from supplier
  Line 1: 100 units @ $10.20 = $1,020.00
  Plus freight: $35.00
  Invoice total: $1,055.00
  Payment terms: Net 30
```

### Rubric

- **0**: Identifies fewer than two of the three exceptions, computes the variances incorrectly, or pays the invoice as-is
- **1**: Identifies all three exceptions and the basic resolution but misses role segregation, treats freight as automatically payable, or fails to flag the boundary case at all (5.00% qty / 2.00% price exactly at tolerance)
- **2**: Identifies all three exceptions with correct math, explicitly states which tolerance convention is being applied (strictly-less-than vs less-than-or-equal — both are defensible) and reasons consistently from that, addresses each through the proper role (AP / buyer / receiver), and references SOX three-way-match control and segregation of duties

### Ideal answer

Three exceptions:

1. Quantity variance — invoice 100 units vs. GR 95 units = 5-unit / 5.00% variance. The GR is marked final delivery, so the missing 5 units will not be received. The invoice over-bills by 5 units × $10.00 = $50.00. Tolerance is ±5% on quantity. **Both `<` and `≤` are defensible conventions in industry — SAP defaults to `<` while some Oracle / mid-market systems use `≤`. State which convention the responder is applying and reason consistently.** Under `<`, 5.00% is out of tolerance → exception. Under `≤`, 5.00% is in tolerance but is still a quantity issue against a final-delivery GR (you cannot pay for unshipped units), so it routes as a no-tolerance exception regardless. Either way, the resolution is the same: do not pay for the 5 unshipped units.

2. Price variance — $10.20 vs. PO $10.00 = $0.20 / 2.00% variance. Tolerance ±2%, same boundary question. Under `<`, out of tolerance → exception. Under `≤`, in tolerance → auto-release per ERP. Over-bill at PO quantity = 100 × $0.20 = $20.00. Even under `≤`, best practice is to surface boundary-case variances to the buyer rather than auto-pay; documenting the convention explicitly is the audit-defensible move.

3. Unauthorized freight — $35.00 freight line is not on the PO. Whether freight is allowable depends on the Incoterms / freight policy on the PO. If the PO is silent and policy is 'freight included unless on PO,' reject the freight line.

Resolution path:
- Hold the invoice; do not pay.
- Quantity: confirm short-ship with receiving and request a credit memo from the supplier for the 5 unshipped units, OR have supplier reissue the invoice for 95 units. Do not pay against a quantity not received.
- Price: route to the buyer (sourcing) for variance approval. Buyer either approves the increase (and updates the PO via change order) or rejects and demands the invoice be reissued at PO price.
- Freight: route to the buyer; if not contractually owed, reject.
- Net 30 starts only when the corrected invoice is received in good order — flag the supplier portal accordingly so payment-term clocks are not gamed.

Controls and segregation:
- AP clerk identifies and posts the exception but cannot approve the variance.
- Buyer (sourcing) approves price/freight variances within their delegation; above delegation, escalate per the DOA matrix.
- Receiver confirms quantity facts but is not the same person as buyer or AP (segregation under SOX P2P).
- All exception approvals must be documented in the system to support the SOX 'invoice-to-PO/GR three-way match' control test.

### Model response

# 3-Way Match Analysis: PO #4500-22871 / GR #50032118 / INV-88412

---

## Overview of 3-Way Match Logic

A 3-way match validates that:
1. **PO → GR**: What was ordered vs. what was received
2. **PO → Invoice**: What was ordered vs. what was billed
3. **GR → Invoice**: What was received vs. what was billed

All three legs must reconcile within defined tolerances before payment is released.

---

## Step 1: Document Comparison Matrix

| Field | PO #4500-22871 | GR #50032118 | INV-88412 | Match? |
|---|---|---|---|---|
| Quantity | 100 units | 95 units | 100 units | ❌ **Fail** |
| Unit Price | $10.00 | N/A | $10.20 | ❌ **Fail** |
| Line Amount | $1,000.00 | $950.00* | $1,020.00 | ❌ **Fail** |
| Freight | $0.00 | N/A | $35.00 | ❌ **Fail** |
| Invoice Total | $1,000.00 | N/A | $1,055.00 | ❌ **Fail** |

*GR implied value = 95 units × $10.00 PO price = $950.00

---

## Step 2: Exception Identification and Quantification

---

### Exception 1 — Quantity Variance (GR vs. Invoice)

| | Value |
|---|---|
| Invoice quantity | 100 units |
| Received quantity | 95 units |
| **Variance** | **5 units short** |
| Variance % | **5.0%** |
| PO tolerance | ±5% quantity |
| Tolerance threshold (qty) | 95–105 units acceptable |
| Within tolerance? | ✅ 95 units is exactly at the lower bound |

**Critical nuance — billing vs. receipt mismatch:**
Even though 95 units received is *at* the quantity tolerance floor on the PO, **the invoice bills for 100 units, not 95 units**. The fundamental rule of 3-way match is that payment should never exceed goods actually received. The supplier has marked the GR as *"final delivery — short ship"*, meaning no further delivery is expected.

> **Net exposure: Supplier is billing for 5 units never received = $51.00** *(5 × $10.20 invoiced price, or 5 × $10.00 PO price = $50.00 depending on resolution)*

**Resolution required:** Invoice must be corrected to 95 units, OR a credit memo of $51.00 (or $50.00 at PO price) must be obtained before payment. This is a **hard block** — paying for undelivered goods is not a tolerance matter.

---

### Exception 2 — Unit Price Variance (PO vs. Invoice)

| | Value |
|---|---|
| PO unit price | $10.00 |
| Invoiced unit price | $10.20 |
| **Variance** | **$0.20/unit** |
| Variance % | **2.0%** |
| PO tolerance | ±2% price |
| Tolerance threshold | $9.80–$10.20/unit |
| Within tolerance? | ✅ **Exactly at upper bound** |

**Analysis:** $10.20 is technically within the ±2% price tolerance. However, many ERP systems apply this as a *strict less-than* test (i.e., < 2%, not ≤ 2%), which would make this a boundary exception requiring human review. The on-the-margin nature of this variance warrants scrutiny regardless.

> **Net price exposure at 95 units payable: $0.20 × 95 = $19.00 above PO value**

**Resolution path:** If the system treats "exactly at tolerance" as passing, this clears automatically. If it flags boundary conditions (best practice), it routes to **AP Supervisor** for approval with Purchasing awareness. Purchasing should also confirm whether the price increase was pre-agreed (e.g., a price change notification not yet reflected in the PO).

---

### Exception 3 — Freight Charge (Invoice vs. PO)

| | Value |
|---|---|
| PO freight | $0.00 (not included) |
| Invoiced freight | $35.00 |
| **Variance** | **$35.00** |
| Within PO scope? | ❌ **No — not authorized on PO** |

**Analysis:** The PO contains no freight provision. This is an *unordered charge* — a line item with no corresponding PO line and no GR. This is one of the most common fraud/error vectors in AP and triggers a hard exception regardless of dollar amount.

**Possible legitimate scenarios:**
- Freight terms on the contract/PO are FOB Destination (supplier pays) — no freight should be charged
- Freight terms are FOB Origin (buyer pays) — freight is legitimate but the PO must be amended to include it
- Freight was verbally agreed outside the PO — PO amendment required to create audit trail

> **Exposure: $35.00 unauthorized charge**

**Resolution path:** Cannot be auto-approved. Requires **Purchasing review** to verify freight terms, potential **PO amendment** to add a freight line, and **AP Supervisor approval**. If terms indicate FOB Destination, supplier must issue a credit memo for $35.00.

---

### Exception 4 — Total Invoice Amount vs. Payable Amount

| | Value |
|---|---|
| Invoice total submitted | $1,055.00 |
| Maximum payable (95 units × $10.20 + $0 freight) | $969.00 |
| Maximum payable (95 units × $10.00 PO price) | $950.00 |
| **Total overbilling vs. goods received at PO price** | **$105.00** |
| **Total overbilling vs. invoice as submitted** | **$86.00** *(if freight resolved)* |

---

## Step 3: Consolidated Exception Register

| # | Exception | Type | Variance | Tolerance | Auto-Clear? | Severity |
|---|---|---|---|---|---|---|
| 1 | Invoice qty (100) vs. received qty (95) | Quantity – billing overstatement | 5 units / $50–$51 | Qty at tolerance floor, but billing rule violated | ❌ **Hard Block** | 🔴 Critical |
| 2 | Unit price $10.20 vs. PO $10.00 | Price variance | $0.20/unit / 2.0% | At ±2% boundary | ⚠️ Boundary | 🟡 Medium |
| 3 | Freight $35.00 not on PO | Unauthorized charge | $35.00 | No tolerance — not in scope | ❌ **Hard Block** | 🔴 Critical |
| 4 | Invoice total $1,055 vs. payable $950 | Cumulative overbilling | $105.00 | N/A | ❌ **Hard Block** | 🔴 Critical |

---

## Step 4: Resolution Paths by Exception

---

### Exception 1 — Quantity Overbilling

**Immediate action:**
- AP places invoice in **"Blocked for Payment"** status in ERP
- AP contacts supplier to request a **credit memo for 5 units** (at invoiced price: $51.00)
- Alternatively, supplier issues a **revised invoice for 95 units @ $10.20 = $969.00** (subject to Exception 2 resolution)

**Roles:**
- **AP Clerk** — identifies and documents exception, contacts supplier
- **AP Supervisor** — approves hold, documents in exception log
- **Receiving/Warehouse** — confirms final delivery status in writing; GR should be marked "Final Delivery" in ERP to close PO line

**Controls applied:**
- Goods-receipt-based invoice verification (GR-IV): system should block payment above received quantity
- Final delivery flag on GR prevents re-opening for additional receipts
- Three-way match hard rule: *pay what was received*

---

### Exception 2 — Unit Price at Tolerance Boundary

**Immediate action:**
-

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The candidate identifies all three exceptions with reasonable math and addresses resolution paths. However, it has notable issues: (1) On the boundary convention, it mentions strict-less-than vs ≤ for the price variance but does NOT explicitly state and consistently apply one convention — it hedges. For the quantity variance, it says 95 units is 'at the lower bound' / within tolerance without applying the same boundary analysis consistently (the 5/100 = 5% should trigger the same < vs ≤ discussion). (2) It does not reference SOX three-way-match controls or segregation of duties explicitly (mentions AP Clerk/Supervisor/Receiving/Purchasing roles but no SOX P2P control framework or SoD principle). (3) Routes price variance to 'AP Supervisor' rather than the buyer/sourcing as the primary approver. These gaps align with the rubric's level 1 description (identifies all three but misses role segregation / SOX control reference / inconsistent boundary handling).

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_003 — invoice_processing · medium · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: multi-step arithmetic and control reasoning_

### Question

Walk through the 3-way match for the documents below. Identify every exception, quantify the variance, and state the resolution path including which roles must approve and which controls apply.

### Context

```
PO #4500-22871
  Line 1: 100 units of part #X-77 @ $10.00 = $1,000.00
  Tolerance: ±2% price, ±5% quantity
  Status: Open, no prior receipts

Goods Receipt (GR) #50032118
  Line 1: 95 units received, marked 'final delivery — short ship per supplier'
  Receiver: warehouse staff

Invoice INV-88412 from supplier
  Line 1: 100 units @ $10.20 = $1,020.00
  Plus freight: $35.00
  Invoice total: $1,055.00
  Payment terms: Net 30
```

### Rubric

- **0**: Identifies fewer than two of the three exceptions, computes the variances incorrectly, or pays the invoice as-is
- **1**: Identifies all three exceptions and the basic resolution but misses role segregation, treats freight as automatically payable, or fails to flag the boundary case at all (5.00% qty / 2.00% price exactly at tolerance)
- **2**: Identifies all three exceptions with correct math, explicitly states which tolerance convention is being applied (strictly-less-than vs less-than-or-equal — both are defensible) and reasons consistently from that, addresses each through the proper role (AP / buyer / receiver), and references SOX three-way-match control and segregation of duties

### Ideal answer

Three exceptions:

1. Quantity variance — invoice 100 units vs. GR 95 units = 5-unit / 5.00% variance. The GR is marked final delivery, so the missing 5 units will not be received. The invoice over-bills by 5 units × $10.00 = $50.00. Tolerance is ±5% on quantity. **Both `<` and `≤` are defensible conventions in industry — SAP defaults to `<` while some Oracle / mid-market systems use `≤`. State which convention the responder is applying and reason consistently.** Under `<`, 5.00% is out of tolerance → exception. Under `≤`, 5.00% is in tolerance but is still a quantity issue against a final-delivery GR (you cannot pay for unshipped units), so it routes as a no-tolerance exception regardless. Either way, the resolution is the same: do not pay for the 5 unshipped units.

2. Price variance — $10.20 vs. PO $10.00 = $0.20 / 2.00% variance. Tolerance ±2%, same boundary question. Under `<`, out of tolerance → exception. Under `≤`, in tolerance → auto-release per ERP. Over-bill at PO quantity = 100 × $0.20 = $20.00. Even under `≤`, best practice is to surface boundary-case variances to the buyer rather than auto-pay; documenting the convention explicitly is the audit-defensible move.

3. Unauthorized freight — $35.00 freight line is not on the PO. Whether freight is allowable depends on the Incoterms / freight policy on the PO. If the PO is silent and policy is 'freight included unless on PO,' reject the freight line.

Resolution path:
- Hold the invoice; do not pay.
- Quantity: confirm short-ship with receiving and request a credit memo from the supplier for the 5 unshipped units, OR have supplier reissue the invoice for 95 units. Do not pay against a quantity not received.
- Price: route to the buyer (sourcing) for variance approval. Buyer either approves the increase (and updates the PO via change order) or rejects and demands the invoice be reissued at PO price.
- Freight: route to the buyer; if not contractually owed, reject.
- Net 30 starts only when the corrected invoice is received in good order — flag the supplier portal accordingly so payment-term clocks are not gamed.

Controls and segregation:
- AP clerk identifies and posts the exception but cannot approve the variance.
- Buyer (sourcing) approves price/freight variances within their delegation; above delegation, escalate per the DOA matrix.
- Receiver confirms quantity facts but is not the same person as buyer or AP (segregation under SOX P2P).
- All exception approvals must be documented in the system to support the SOX 'invoice-to-PO/GR three-way match' control test.

### Model response

# 3-Way Match Analysis: PO #4500-22871

## Document Comparison

| Element | PO | GR | Invoice | Match Status |
|---------|----|----|---------|--------------|
| **Quantity** | 100 units | 95 units | 100 units | ❌ EXCEPTION |
| **Unit Price** | $10.00 | N/A | $10.20 | ❌ EXCEPTION |
| **Freight** | Not specified | N/A | $35.00 | ❌ EXCEPTION |
| **Line Total** | $1,000.00 | N/A | $1,020.00 + $35.00 = $1,055.00 | ❌ EXCEPTION |

---

## Exception #1: Quantity Variance

**Variance Quantification:**
- PO quantity: 100 units
- GR quantity: 95 units
- **Shortfall: 5 units (-5%)**
- **Tolerance allowance: ±5%**

**Status:** ✅ **WITHIN TOLERANCE**
- The -5% variance equals the upper limit of the acceptable tolerance band

**Resolution Path:**
1. **Quality Assurance/Receiving**: Verify that 5-unit shortfall is acceptable given "final delivery — short ship per supplier" notation
2. **Procurement (approval required)**: Accept short receipt and close PO quantity remaining (5 units) or issue follow-up PO if units are still needed
3. **Control applied**: Quantity tolerance check
4. **Action**: Match GR to PO at 95 units; document final delivery status

---

## Exception #2: Unit Price Variance

**Variance Quantification:**
- PO unit price: $10.00
- Invoice unit price: $10.20
- **Variance: +$0.20 per unit (+2%)**
- **Tolerance allowance: ±2%**

**Status:** ❌ **AT TOLERANCE BOUNDARY** (requires judgment)
- The +2% variance equals the upper limit of acceptable tolerance
- On 95 units received: $0.20 × 95 = **$19.00 additional cost**

**Resolution Path:**
1. **Procurement**: Determine if price increase was pre-authorized or if supplier unilaterally changed terms
2. **Finance/AP (approval required)**: 
   - If pre-authorized: process
   - If unauthorized: contact supplier to challenge variance and request credit memo or price correction
3. **Control applied**: Price tolerance check
4. **Decision gates**: 
   - Approve if change order or prior communication exists
   - Reject/negotiate if this is a unilateral price increase outside authorized terms

---

## Exception #3: Freight Charge

**Variance Quantification:**
- PO freight specification: **None stated** (typically "FOB destination" assumed, placing freight responsibility on supplier)
- Invoice freight: $35.00
- **Variance: +$35.00 (undefined baseline)**

**Status:** ❌ **CRITICAL EXCEPTION – REQUIRES CLARIFICATION**

**Resolution Path:**
1. **Procurement (immediate action)**: Verify PO terms regarding freight responsibility
   - Is this FOB Shipping Point (buyer pays) or FOB Destination (seller absorbs)?
   - Was freight included in the $10.00 unit price or separate?
   
2. **Supplier verification**: Contact supplier to confirm whether $35 freight is legitimately owed
   
3. **Finance/AP (approval required)**: 
   - **If FOB Shipping Point:** Approve freight as legitimate cost
   - **If FOB Destination:** Reject freight and demand credit memo; do not pay supplier charge
   
4. **Control applied**: Terms and conditions validation; freight responsibility check

---

## Summary of Approvals Required

| Exception | Approving Role | Control Type | Recommended Action |
|-----------|---------------|--------------|--------------------|
| Quantity (-5%) | Procurement | Quantity tolerance | **ACCEPT** – within ±5% |
| Price (+2%) | Finance/AP & Procurement | Price tolerance | **CONDITIONAL ACCEPT** – verify authorization |
| Freight ($35) | Procurement & Finance | Terms validation | **CONDITIONAL ACCEPT** – verify FOB terms |

---

## Overall 3-Way Match Decision

**Status: ❌ EXCEPTION – HOLD FOR APPROVAL**

**Cannot process invoice for payment until:**

1. ✅ Quantity exception cleared (at tolerance boundary)
2. ⚠️ Price increase authorized or credit memo obtained
3. ⚠️ Freight responsibility confirmed and legitimacy validated

**Recommended Invoice Status:** 
- Create **hold** in accounts payable system
- Flag for Procurement Manager and Finance Controller review
- Estimated resolution time: 2–3 business days pending supplier response

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response identifies all three exceptions with mostly correct math (quantity 5 units/5%, price $0.20/2%, freight $35). It flags both the quantity and price as boundary cases requiring judgment, which is good. However, it does not explicitly state which tolerance convention (< vs ≤) is being applied and reason consistently from that — it just calls them 'at tolerance boundary' without naming the convention. Critically, it accepts the quantity variance as within tolerance without recognizing that a final-delivery short-ship means you cannot pay for unshipped units regardless of tolerance (the invoice bills 100 but only 95 were received — this is a $50 overbill). It also does not reference SOX three-way-match control or segregation of duties explicitly, and the role assignments mix AP and Procurement without clear SoD framing. Freight handling is reasonable but treats it as conditional rather than defaulting to reject-if-not-on-PO. Meets level 1 criteria but falls short of level 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_005 — trade_and_tax · medium · **score 1/2** (model: `claude-opus-4-7`)

_Expected failure mode: applying domain conventions_

### Question

Review the supplier invoice against the PO and Incoterms. Which charges should the buyer accept, and which should be pushed back to the supplier? Cite the Incoterms 2020 rule.

### Context

```
PO from US buyer to a German manufacturer:
  Goods:        €50,000 of electronic components
  Incoterms:    FCA Hamburg (Incoterms 2020)
  Named place:  Hamburg port terminal

Supplier invoice (in EUR):
  Line 1: Components                           €50,000.00
  Line 2: Inland freight, Stuttgart → Hamburg   €1,200.00
  Line 3: Export customs clearance fee            €350.00
  Line 4: Loading/handling at Hamburg terminal     €180.00
  Line 5: Marine cargo insurance                   €420.00
  Total:                                         €52,150.00

Separately, the buyer has received an invoice from its own freight forwarder for ocean freight Hamburg → New York and US import duty.
```

### Rubric

- **0**: Accepts the supplier invoice as billed, or applies CIF/CIP/DAP cost allocation to FCA, or gets the freight allocation backwards
- **1**: Correctly rejects the inland freight and export clearance lines but mishandles insurance, terminal handling, or fails to cite Incoterms 2020 FCA
- **2**: Correctly addresses every line with reference to FCA seller/buyer obligations, flags the terminal-handling ambiguity rather than guessing, and references Incoterms 2020 FCA explicitly

### Ideal answer

Under Incoterms 2020 FCA at a named place that is not the seller's premises (here, 'Hamburg port terminal'), the seller's delivery obligation is to deliver the goods, cleared for export, to the carrier nominated by the buyer at the named place. The seller bears all costs up to and including delivery at that named place; the buyer bears costs from that point onward, including the main carriage.

Line-by-line:
- Line 1, Components €50,000 — accept. PO price.
- Line 2, Inland freight Stuttgart → Hamburg €1,200 — REJECT. Pre-carriage to the named place is the seller's cost under FCA. It must already be embedded in the price; charging it separately is a double charge unless the PO explicitly priced ex-works and added pre-carriage as a quoted line, which is not the case here.
- Line 3, Export customs clearance €350 — REJECT. Under FCA, the seller is responsible for export clearance and bears the cost (Incoterms 2020 FCA, A7/A9). Cannot be on-billed.
- Line 4, Loading/handling at Hamburg terminal €180 — DEPENDS. Under FCA at a terminal that is not the seller's premises, the seller is considered to have delivered when the goods are placed at the disposal of the carrier at the named place; loading onto the buyer's onward carrier is generally the buyer's cost. Terminal handling charges (THC) at the FCA point are commonly the buyer's responsibility unless the parties have agreed otherwise. Push back to clarify whether this is THC for receipt at terminal (seller) or loading onto the ocean carrier (buyer); if loading onto buyer's vessel, accept; if receipt-side handling, reject.
- Line 5, Marine cargo insurance €420 — REJECT. Under FCA, neither party has a contractual obligation to insure (Incoterms 2020 FCA, A5/B5). If the buyer wanted insurance, they would arrange it themselves. Supplier cannot impose insurance and on-bill it.

Separately invoiced freight forwarder charges (ocean freight, US import duty, US delivery) are correctly the buyer's responsibility under FCA — accept those on the forwarder invoice, not the supplier invoice.

Action: hold supplier invoice for €52,150; request a corrected invoice for €50,000 + (terminal-handling line only if it relates to loading onto the buyer's vessel, with documentation). If the supplier disputes, the contract Incoterms term and Incoterms 2020 reference (ICC publication 723E) is the authority.

Note on a 2020-vs-2010 nuance: Incoterms 2020 added an option for FCA shipments to specify that the buyer instruct the carrier to issue a bill of lading 'on board' to the seller — relevant for L/C settlement, not for cost allocation here.

### Model response

# Review of Supplier Invoice vs. FCA Hamburg (Incoterms 2020)

## The Governing Rule: FCA Incoterms 2020

Under **FCA (Free Carrier) Hamburg**, the seller's obligations end when the goods are delivered, cleared for export, to the carrier (or another person nominated by the buyer) **at the named place — Hamburg port terminal**.

Key allocations under Incoterms 2020 FCA:

| Obligation | Seller (Germany) | Buyer (US) |
|---|---|---|
| **A2 / B2 – Delivery** | Deliver to carrier at named place | Take delivery at named place |
| **A4 / B4 – Carriage** | No obligation (unless agreed); buyer arranges main carriage | Contracts main carriage |
| **A5 / B5 – Insurance** | No obligation | No obligation (neither party must insure) |
| **A7 / B7 – Export/Import clearance** | Export clearance is seller's responsibility | Import clearance is buyer's |
| **A9 / B9 – Cost allocation** | All costs until delivered to carrier at named place, including export clearance | All costs after delivery |

Critically, when the named place is a **terminal** (as here — Hamburg port terminal), per **FCA A2**: *"If the named place is… any other place, the goods are delivered when… loaded on the buyer's means of transport [or] placed at the disposal of the carrier… on the seller's means of transport ready for unloading."* The seller's costs run up to that point of delivery (FCA A9).

---

## Line-by-Line Assessment

| Line | Charge | Amount | Accept / Push Back | Rationale |
|---|---|---|---|---|
| **1** | Components | €50,000.00 | ✅ **Accept** | Goods per PO. |
| **2** | Inland freight Stuttgart → Hamburg | €1,200.00 | ✅ **Accept** | Pre-carriage to the named place is the seller's cost. **FCA A4 & A9(a)** — seller bears all costs relating to the goods until delivered at the named place. |
| **3** | Export customs clearance | €350.00 | ✅ **Accept** | Export formalities and their cost are explicitly the seller's obligation. **FCA A7(a) & A9(b)** — *"the seller must… carry out and pay for all export clearance formalities… duties, taxes and any other costs."* |
| **4** | Loading/handling at Hamburg terminal | €180.00 | ✅ **Accept** | Delivery at a terminal under FCA includes placing the goods at the disposal of the carrier ready for unloading from the seller's means of transport — handling/loading onto the carrier at the named place is on the seller's side of the delivery point. **FCA A2 & A9(a)**. (If your contract instead positioned the delivery point as "before loading," this would be debatable — but with the named place being the terminal itself, terminal handling charges incurred to effect delivery to the carrier are seller's costs.) |
| **5** | Marine cargo insurance | €420.00 | ❌ **Push back / Reject** | **Under FCA, neither party is obliged to insure (A5 / B5).** Risk transfers to the buyer at the named place (FCA A3/B3), so any marine cargo insurance covering the Hamburg → New York leg is for the buyer's account and the buyer's choice. The seller cannot unilaterally bill insurance not requested in the PO. If the buyer wanted seller-procured insurance, the parties would have used **CIP** (or agreed it expressly). |

---

## Recommended Action

1. **Accept and pay** Lines 1, 2, 3, and 4 — total **€51,730.00**.
2. **Reject Line 5 (€420.00)** and request a **credit note / revised invoice**. Cite FCA A5/B5 (Incoterms 2020): no insurance obligation on either party; risk had passed to the buyer at Hamburg, so seller-arranged marine insurance was neither required nor authorized in the PO.
3. **Confirm separately** with your freight forwarder that the ocean freight Hamburg → New York and US import duty/clearance are correctly being borne by the buyer — they should be (FCA B4, B7(b), B9).

## Watch-Outs for Future POs

- If you want the seller to handle main carriage and/or insurance, switch to **CPT** or **CIP Hamburg/New York**.
- Under FCA 2020, you can request a **bill of lading with on-board notation** from the carrier (new in 2020, FCA A6/B6) — useful if you have a letter of credit requiring it.
- Make sure the **named place is precise** ("Hamburg port terminal, [specific terminal/address]") to avoid ambiguity over who pays terminal handling charges (THC) — a common dispute area.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The candidate correctly identifies FCA 2020 rules, cites A5/B5 for insurance rejection, and correctly handles Lines 1 and 5. However, it gets Lines 2 and 3 backwards from the rubric's expectation: the rubric says inland freight and export clearance should be REJECTED as separate line items (they should be embedded in the price, not on-billed separately), while the candidate accepts them. The candidate's reasoning that these are seller's costs under FCA is technically correct regarding obligation, but misses the invoicing point that on-billing them separately is improper double-charging. Additionally, the candidate confidently accepts Line 4 rather than flagging the terminal-handling ambiguity as the rubric requires. The candidate does correctly handle insurance with proper Incoterms 2020 FCA citation, which matches the level-1 criteria partially but inverts which lines to reject.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_005 — trade_and_tax · medium · **score 1/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: applying domain conventions_

### Question

Review the supplier invoice against the PO and Incoterms. Which charges should the buyer accept, and which should be pushed back to the supplier? Cite the Incoterms 2020 rule.

### Context

```
PO from US buyer to a German manufacturer:
  Goods:        €50,000 of electronic components
  Incoterms:    FCA Hamburg (Incoterms 2020)
  Named place:  Hamburg port terminal

Supplier invoice (in EUR):
  Line 1: Components                           €50,000.00
  Line 2: Inland freight, Stuttgart → Hamburg   €1,200.00
  Line 3: Export customs clearance fee            €350.00
  Line 4: Loading/handling at Hamburg terminal     €180.00
  Line 5: Marine cargo insurance                   €420.00
  Total:                                         €52,150.00

Separately, the buyer has received an invoice from its own freight forwarder for ocean freight Hamburg → New York and US import duty.
```

### Rubric

- **0**: Accepts the supplier invoice as billed, or applies CIF/CIP/DAP cost allocation to FCA, or gets the freight allocation backwards
- **1**: Correctly rejects the inland freight and export clearance lines but mishandles insurance, terminal handling, or fails to cite Incoterms 2020 FCA
- **2**: Correctly addresses every line with reference to FCA seller/buyer obligations, flags the terminal-handling ambiguity rather than guessing, and references Incoterms 2020 FCA explicitly

### Ideal answer

Under Incoterms 2020 FCA at a named place that is not the seller's premises (here, 'Hamburg port terminal'), the seller's delivery obligation is to deliver the goods, cleared for export, to the carrier nominated by the buyer at the named place. The seller bears all costs up to and including delivery at that named place; the buyer bears costs from that point onward, including the main carriage.

Line-by-line:
- Line 1, Components €50,000 — accept. PO price.
- Line 2, Inland freight Stuttgart → Hamburg €1,200 — REJECT. Pre-carriage to the named place is the seller's cost under FCA. It must already be embedded in the price; charging it separately is a double charge unless the PO explicitly priced ex-works and added pre-carriage as a quoted line, which is not the case here.
- Line 3, Export customs clearance €350 — REJECT. Under FCA, the seller is responsible for export clearance and bears the cost (Incoterms 2020 FCA, A7/A9). Cannot be on-billed.
- Line 4, Loading/handling at Hamburg terminal €180 — DEPENDS. Under FCA at a terminal that is not the seller's premises, the seller is considered to have delivered when the goods are placed at the disposal of the carrier at the named place; loading onto the buyer's onward carrier is generally the buyer's cost. Terminal handling charges (THC) at the FCA point are commonly the buyer's responsibility unless the parties have agreed otherwise. Push back to clarify whether this is THC for receipt at terminal (seller) or loading onto the ocean carrier (buyer); if loading onto buyer's vessel, accept; if receipt-side handling, reject.
- Line 5, Marine cargo insurance €420 — REJECT. Under FCA, neither party has a contractual obligation to insure (Incoterms 2020 FCA, A5/B5). If the buyer wanted insurance, they would arrange it themselves. Supplier cannot impose insurance and on-bill it.

Separately invoiced freight forwarder charges (ocean freight, US import duty, US delivery) are correctly the buyer's responsibility under FCA — accept those on the forwarder invoice, not the supplier invoice.

Action: hold supplier invoice for €52,150; request a corrected invoice for €50,000 + (terminal-handling line only if it relates to loading onto the buyer's vessel, with documentation). If the supplier disputes, the contract Incoterms term and Incoterms 2020 reference (ICC publication 723E) is the authority.

Note on a 2020-vs-2010 nuance: Incoterms 2020 added an option for FCA shipments to specify that the buyer instruct the carrier to issue a bill of lading 'on board' to the seller — relevant for L/C settlement, not for cost allocation here.

### Model response

# Incoterms 2020 FCA Analysis: Supplier Invoice Review

## The Governing Rule

Under **Incoterms 2020 FCA (Free Carrier) — Named Place: Hamburg Port Terminal**, the risk and cost allocation is:

> **Seller's obligation terminates when the goods are delivered to the carrier (or nominated party) at the named place.** The seller bears all costs *up to and including* delivery at that point. The buyer bears all costs *from* that point onward.

The critical interpretive question is therefore: **what is included in "delivery at the Hamburg port terminal"?**

---

## Line-by-Line Analysis

| Line | Charge | Amount | Buyer Accept? | Reasoning |
|---|---|---|---|---|
| **1** | Electronic components | €50,000 | ✅ **Accept** | Core contract value; unambiguous |
| **2** | Inland freight Stuttgart → Hamburg | €1,200 | ✅ **Accept** | Seller must deliver goods *to* the named place; inland transport to Hamburg is explicitly the seller's cost under FCA (A9/B9 of Incoterms 2020) |
| **3** | Export customs clearance fee | €350 | ✅ **Accept** | Under FCA **A2**, the *seller* is responsible for export clearance — obtaining export licence and carrying out all customs formalities for export. This is a seller's obligation, but the cost is properly passed through as part of delivery cost |
| **4** | Loading/handling at Hamburg terminal | €180 | ⚠️ **Dispute — clarify** | This is the **critical ambiguity** (see detailed note below) |
| **5** | Marine cargo insurance | €420 | ❌ **Reject / Push back** | Under FCA, the seller has **no obligation** to procure insurance (FCA A5 explicitly states the seller has no obligation to the buyer to make a contract of insurance). Post-delivery insurance is the buyer's risk and cost. The buyer has already arranged its own forwarder; this is a duplicate/unauthorized charge |

---

## Detailed Notes

### Line 3 — Export Customs Clearance (Accept)
Incoterms 2020 **FCA A2** states:

> *"The seller must obtain, at its own risk and expense, any export licence or other official authorisation and carry out all customs formalities necessary for the export of the goods."*

The €350 fee is the seller's legal obligation under the rules. The seller may include it in the invoice as a cost of delivery, so the buyer should **accept this charge** — it would be improper for the seller *not* to clear export customs.

---

### Line 4 — Loading/Handling at Hamburg Terminal (⚠️ Dispute)

This requires careful analysis of **FCA A4** (Delivery):

> *"If the named place is the seller's premises, delivery is complete when the goods are loaded on the collecting vehicle. **If the named place is any other place**, delivery is complete when the goods are placed at the disposal of the carrier on the seller's arriving means of transport, **ready for unloading**."*

Because the named place is **Hamburg port terminal** (not the seller's premises):
- The seller delivers goods **to the terminal**, placing them at the carrier's disposal
- **Loading onto the vessel is the buyer's/carrier's responsibility**

**However**, terminal handling charges (THC) at the port of origin are a grey area:

- If this €180 is the **terminal reception/handling fee** for receiving the goods at the terminal → arguably the **seller's cost** (part of delivering *to* that place)
- If this is a **vessel loading charge** (lifting goods onto the ship) → **buyer's cost**

**Action:** The buyer should **request a breakdown** of what the €180 covers. If it is a vessel-loading/stevedoring charge, it must be rejected. If it is a terminal intake/handling fee, it may be acceptable.

> *Note: Incoterms 2020 FCA also introduced the new "bill of lading clause" (A6/B6) allowing the buyer to instruct its carrier to issue an on-board B/L to the seller — but this does not shift cost allocation.*

---

### Line 5 — Marine Insurance (❌ Reject)

Incoterms 2020 **FCA A5** is explicit:

> *"The seller has **no obligation** to the buyer to make a contract of insurance."*

Correspondingly, **FCA B5** states:

> *"The buyer has **no obligation** to the seller to make a contract of insurance."*

Under FCA, insurance for the ocean leg is entirely at the **buyer's discretion and expense**. The seller has:
1. No obligation to insure
2. No authority to charge the buyer for insurance the buyer did not request

The buyer has separately engaged its own freight forwarder for the ocean leg. This €420 charge is **unauthorized, duplicative, and contrary to the Incoterms 2020 allocation**. The buyer should formally reject it and request a credit note.

---

## Summary & Recommended Action

| | Amount | Decision |
|---|---|---|
| Components | €50,000.00 | ✅ Accept |
| Inland freight | €1,200.00 | ✅ Accept |
| Export customs clearance | €350.00 | ✅ Accept |
| Terminal loading/handling | €180.00 | ⚠️ Request itemization |
| Marine insurance | €420.00 | ❌ Reject — request credit note |
| **Uncontested payable** | **€51,550.00** | (excluding Line 4 pending clarification) |

**Formal response to supplier should:**
1. Approve payment of €51,550 (Lines 1–3)
2. Request written breakdown of Line 4 before approval
3. Issue written rejection of Line 5 citing **Incoterms 2020 FCA A5** and the absence of any insurance instruction in the purchase order, and request a corrected invoice/credit note for €420

### Grader verdict

- **Score:** 1
- **Confidence:** medium
- **Reasoning:** The candidate correctly rejects the marine insurance charge with proper Incoterms 2020 FCA A5/B5 citation, and correctly flags the terminal handling ambiguity rather than guessing. However, it accepts the inland freight (Line 2) and export clearance (Line 3) as separately billable charges, which contradicts the ideal answer. The ideal answer treats these as seller obligations that should already be embedded in the PO price, not separately on-billed. While the candidate correctly identifies these as seller obligations under FCA, it incorrectly concludes they can be passed through as separate line items, which represents a partial misunderstanding of cost allocation versus invoicing. The Incoterms 2020 FCA references are explicit and accurate. This falls between scores 1 and 2, but because it mishandles two lines (accepting them when they should be rejected as double-billing), it aligns more with score 1.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_006 — trade_and_tax · medium · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: applying domain conventions (cross-border tax)_

### Question

A new supplier has provided a W-9. Is the form valid for this entity? What forms should AP request, what withholding applies, and what year-end reporting is required? Spend will be ~$50,000/year for consulting services performed partly in the US.

### Context

```
Supplier setup packet:
  Legal name on W-9:  Crescent Advisory LLC
  Federal classification box checked: 'Individual/sole proprietor or single-member LLC'
  TIN provided:       SSN of the LLC's owner
  Owner:              Mr. A. Vasquez, citizen and resident of Mexico (per supplier's onboarding form)
  Entity formation:   Delaware single-member LLC
  Services:           Consulting; ~60% of work performed at client US offices, ~40% performed remotely from Mexico
  Contract value:     $50,000/year
```

### Rubric

- **0**: Accepts the W-9, or issues a 1099 to the owner, or claims that a foreign-owned single-member LLC is a US person for withholding
- **1**: Recognizes that W-8BEN is required and that 1042-S applies, but mishandles source-of-income (treats all $50k as US-source or all as foreign), or omits the treaty/PE analysis, or misses the disregarded-entity reasoning
- **2**: Correctly identifies the disregarded-entity rule, requests W-8BEN from the owner, splits US-source vs. foreign-source by where services are performed, addresses 30% default and treaty/PE considerations, and identifies 1042/1042-S (not 1099) as year-end reporting

### Ideal answer

The W-9 is invalid for this entity. A US single-member LLC with a foreign owner is treated as a 'disregarded entity' for US federal tax purposes (Treas. Reg. §301.7701-3); the LLC itself is disregarded and the owner is the relevant tax person. Because the owner is a non-resident alien (NRA), the correct form is W-8BEN (not W-9). W-9 is only for US persons.

AP actions:
1. Reject the W-9. Request a Form W-8BEN from Mr. Vasquez personally (not from the LLC). The W-8BEN must include Mr. Vasquez's Mexican tax residence and, if claiming treaty benefits, his foreign TIN (RFC) and the relevant US-Mexico tax treaty article.
2. Determine source of income. US-source service income is FDAP if not ECI, and is determined by where the services are performed:
   - 60% performed in the US → US-source.
   - 40% performed in Mexico → foreign-source, generally not subject to US withholding.
3. Apply withholding. Default rate on US-source FDAP service income to an NRA is 30% (IRC §1441). The US-Mexico income tax treaty may reduce this for certain categories — for independent personal services / business profits, treaty relief generally requires that the NRA does not have a US permanent establishment / fixed base. If the consultant is regularly working at US offices, examine whether a fixed base exists; if it does, treaty relief may not apply and the income could be ECI taxable on a net basis (in which case the consultant files Form 1040-NR and the withholding regime differs).
4. Documentation. Retain the W-8BEN; renew every 3 years or sooner if circumstances change. Maintain a contemporaneous record allocating service days US vs. foreign — that allocation is the basis for the source determination and is auditable.
5. Year-end reporting. File Form 1042-S (not 1099-NEC or 1099-MISC) reporting the gross US-source amount paid and the tax withheld; file Form 1042 transmittal. 1099 reporting does not apply because the payee is a foreign person.

References: IRS Publication 515 (Withholding of Tax on Nonresident Aliens and Foreign Entities), Form W-8BEN instructions, IRC §§1441, 1442, 861, Treas. Reg. §301.7701-3.

### Model response

# W-9 Validity Assessment & Compliance Requirements

## W-9 Validity: **NO – INVALID**

The W-9 is **not valid** for this entity. Here's why:

### Critical Issues:

1. **Wrong TIN Type**
   - The form claims "Individual/sole proprietor or single-member LLC" but provides an SSN
   - A Delaware LLC—even single-member—has a distinct legal entity status and should have an EIN
   - SSN provision is only appropriate for true sole proprietors, not LLCs

2. **Foreign Owner – FIRPTA Implications**
   - Mr. Vasquez is a Mexican citizen/resident
   - A US entity (Delaware LLC) with a foreign owner presents Foreign Investment in Real Property Tax Act (FIRPTA) and tax residency questions
   - The W-9 doesn't capture this critical information

3. **Incomplete Classification**
   - Single-member LLCs are treated as disregarded entities for federal tax purposes **only if the owner is a US person**
   - Foreign ownership changes this treatment; the entity should be treated as a corporation unless a special election exists

---

## Required Forms & Documentation

### **Request from Supplier:**

| Form | Purpose |
|------|---------|
| **Corrected W-9** OR **Form W-8BEN-E** | If foreign person, W-8BEN-E (Certificate of Beneficial Ownership) is likely required instead of W-9 |
| **EIN Documentation** | Proof the LLC obtained an EIN; request updated W-9 with EIN |
| **IRS Form 8288-B** | If FIRPTA applies (for 1099 income paid to foreign entity) |
| **Tax Residency Certificate** | From Mexico, to assess treaty benefits |

### **Clarification Needed:**
- Does the LLC have an EIN, or is it genuinely disregarded (treated as sole proprietorship)?
- Is Mr. Vasquez claiming US tax residency or treaty benefits?

---

## Withholding Requirements

### **Scenario 1: If LLC Should File W-9 (with EIN)**
- **No backup withholding** if valid W-9 received
- Standard 1099-NEC reporting

### **Scenario 2: If W-8BEN-E Should Be Filed (Foreign Person)**
- **Withholding: 30%** on US-source income under IRC §1441/1442
- May be reduced to **10-15%** if Mexico tax treaty applies (depending on service classification)
- This applies to the consulting payments

### **Current Invalid Status:**
- Legally, **30% backup withholding** should apply under IRC §3406 until valid documentation is received
- Alternatively, withhold as if W-8BEN-E applies (30% or treaty rate)

---

## Year-End Reporting

| Form | Threshold | Notes |
|------|-----------|-------|
| **Form 1099-NEC** (Box 1: Nonemployee Compensation) | $600+ paid | Required if LLC is US entity with valid EIN |
| **Form 1042-S** | If withholding under §1441 | Required if foreign person; reports withholding |
| **Form 8288** (FIRPTA) | If applicable | May be required depending on entity classification |

**Reporting Recipient:**
- SSN listed = potentially incorrect tax ID for the entity
- If W-8BEN-E filed, report using foreign taxpayer ID per IRS rules

---

## Recommended Action Plan

1. **Request corrected documentation immediately** – do not process payments until resolved
2. **Treat as INVALID** – implement 30% withholding pending corrected docs
3. **Obtain clarification** on LLC's EIN status
4. **Request appropriate form:**
   - W-9 with EIN (if LLC properly formed and owner claims US tax residency), OR
   - W-8BEN-E (if foreign person not claiming US residency)
5. **Consult tax advisor** on FIRPTA applicability for consulting services
6. **Document all correspondence** for IRS compliance

---

## Summary Table

| Element | Status | Action |
|---------|--------|--------|
| W-9 Validity | ❌ Invalid | Request correction |
| Withholding Rate | 30% (pending) | Apply until valid docs received; may reduce if treaty applies |
| EIN Required | ✅ Yes | Request from supplier |
| 1099-NEC | Required at $600+ | Use correct EIN when valid |
| Foreign Owner Docs | ✅ Required | Obtain W-8BEN-E or tax residency certificate |

This situation requires **immediate resolution** before processing significant payments to avoid IRS penalties and compliance failures.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies the W-9 as invalid and recognizes that a W-8 form and 1042-S reporting are needed. However, it has significant errors: (1) it recommends W-8BEN-E instead of W-8BEN (the owner is an individual NRA, and the LLC is disregarded, so W-8BEN from the individual is correct); (2) it incorrectly states that foreign ownership changes disregarded-entity treatment to corporation—this is wrong; the entity remains disregarded under Treas. Reg. §301.7701-3; (3) it completely misses the source-of-income analysis (60% US/40% Mexico split based on where services are performed); (4) treaty/PE (fixed base) analysis is superficial; (5) introduces irrelevant FIRPTA references (FIRPTA applies to real property, not consulting). It does still keep 1099-NEC as a possibility, which is incorrect for a foreign payee. Partial credit warranted — meets the '1' criteria of recognizing W-8/1042-S but mishandling source and missing disregarded-entity reasoning.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_007 — trade_and_tax · hard · **score 1/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: assumption generation across jurisdictions_

### Question

Is the German VAT correctly charged on this invoice? What should AP do, and is the VAT reclaimable? Reason from EU VAT place-of-supply rules.

### Context

```
Buyer:    US-incorporated company with no EU permanent establishment, but registered for German VAT (DE VAT ID DE123456789) because of an earlier consignment-stock arrangement.
Supplier: German consulting firm, registered for VAT in Germany only.
Service:  Strategy consulting, performed remotely from Germany, deliverable consumed by the buyer's US headquarters (the German VAT registration is unrelated to this engagement).

Supplier invoice:
  Net fee:           €40,000.00
  German VAT 19%:     €7,600.00
  Invoice total:     €47,600.00
  Buyer's DE VAT ID is shown on the invoice header.
  Note line: 'VAT charged per German law.'
```

### Rubric

- **0**: Accepts the VAT as charged, or claims it is reclaimable simply because a DE VAT ID exists, or applies reverse charge between two German parties
- **1**: Correctly identifies that VAT should not have been charged but reasons via reverse charge instead of out-of-scope, or omits the Article 22 establishment-confirmation step, or does not address reclaim mechanics
- **2**: Correctly identifies the place of supply as the US under Article 44 based on which establishment consumes the service, distinguishes out-of-scope from reverse charge, recommends invoice rejection plus Article 22 establishment confirmation, and addresses why reclaim is not the right path

### Ideal answer

The VAT is incorrectly charged. The analysis turns on the EU VAT place-of-supply rules and which 'capacity' the buyer is acting in.

B2B services place of supply (Council Directive 2006/112/EC Article 44): for services supplied to a taxable person, the place of supply is where the customer is established or has a fixed establishment to which the service is supplied. Two facts here:

1. The buyer's establishment is the US (no EU permanent establishment).
2. The deliverable is consumed by the US headquarters; the German VAT registration is incidental and unrelated to this engagement.

Therefore the place of supply is the US, which is outside the EU VAT system. The supply is outside the scope of EU VAT. The German supplier should not have charged German VAT.

The presence of the buyer's DE VAT ID on the invoice does not, by itself, change the place of supply — Article 44 is about where the customer is established for the service consumed, not which VAT IDs the customer happens to hold. A buyer with multiple establishments must communicate to the supplier which establishment is receiving the service (Implementing Regulation 282/2011, Article 22). The supplier's apparent default to 'this is German because we see a DE VAT ID' is incorrect when the deliverable is consumed elsewhere.

Note: had the service been received by the buyer's German activity (the consignment-stock operation), the place of supply would be Germany, and the supplier would charge German VAT, which the buyer could reclaim via its German VAT return. That is the alternate fact pattern.

The distinct 'reverse charge' question: if the place of supply had been Germany but the supplier and customer were in different EU states with both VAT-registered, Article 196 reverse charge would apply (customer self-accounts). That is not this case because both parties are in Germany for VAT purposes if the German establishment is the recipient. Reverse charge does not apply to a US-recipient supply because the US is outside EU VAT entirely — it is simply out of scope.

AP action:
1. Reject the invoice. Email the supplier explaining that under Article 44 the place of supply is the US (the establishment consuming the service), not Germany, and that the deliverable is unrelated to the buyer's German VAT registration.
2. Provide written confirmation of which establishment is receiving the service (Implementing Regulation 282/2011, Article 22) — this is the supplier's documentation requirement to avoid charging VAT.
3. Request a corrected invoice for €40,000 net, no VAT, with a note 'Outside scope of EU VAT — place of supply outside EU per Article 44, Directive 2006/112/EC.'
4. Reclaimability: not applicable. The €7,600 is not VAT properly due; it is not reclaimable through the German VAT return because the underlying supply is out of scope. If the supplier refuses to credit and reissue, the buyer would have to pay €47,600 and pursue an Article 13th Directive refund (refund to non-EU established taxable persons) or, more practically, dispute with the supplier — but the right answer is to fix the invoice, not to reclaim VAT that should never have been charged.

References: Council Directive 2006/112/EC Articles 44, 196; Council Implementing Regulation 282/2011 Articles 10–13, 21–22; 13th VAT Directive 86/560/EEC (refund to non-EU businesses).

### Model response

# Analysis of German VAT Treatment on This Invoice

## 1. Applicable Place-of-Supply Rule

The governing provision is **Article 44 of the EU VAT Directive 2006/112/EC** (implemented in Germany via **§ 3a Abs. 2 UStG**):

> *"The place of supply of services to a taxable person acting as such shall be the place where that person has established his business."*

### Is the Buyer a "Taxable Person" for Article 44 Purposes?

This is the critical question, and the answer is **yes** — but requires careful reasoning.

A US company with **no EU establishment** can still qualify as a taxable person under Article 44 if it is registered for VAT in an EU Member State. The ECJ has consistently held that VAT registration *per se* constitutes evidence of taxable-person status (see **C-421/10, Stoppelkamp**; **C-97/06, Navicon**). The buyer holds DE VAT ID **DE123456789**, which the supplier has correctly noted on the invoice.

However, one must address the nuance in **Article 44 and the Implementing Regulation (EU) No 282/2011, Articles 21–22**: where a taxable person has multiple establishments, the supply is attributed to the establishment that **actually uses the service**. Here:

| Factor | Assessment |
|---|---|
| Buyer's EU establishment? | **None** — the DE VAT ID arises solely from a consignment-stock arrangement (warehouse/fiscal presence), not a fixed establishment for these services |
| Where is the service consumed? | US headquarters — strategy consulting deliverable consumed there |
| Does the DE registration constitute a "fixed establishment" attracting this supply? | **No** — a mere VAT registration without human and technical resources to receive/consume the service does **not** constitute a fixed establishment (confirmed in **C-605/12, Welmory**; **C-547/18, Titanium**) |

### Conclusion on Place of Supply

Because:
- The buyer is a taxable person (has a DE VAT ID)
- Its **business is established in the US**
- The DE VAT registration is not a fixed establishment capable of consuming strategy consulting services
- The service is consumed at the US headquarters

**→ The place of supply is the United States (where the recipient is established), NOT Germany.**

---

## 2. VAT Treatment That Should Apply

Under **§ 3a Abs. 2 UStG**, the supply is **outside the scope of German VAT**. The correct invoice treatment is:

| Element | Correct Treatment |
|---|---|
| German VAT | **Not chargeable — €0** |
| Invoice notation | "Reverse charge — Art. 44 VAT Directive / § 3a Abs. 2 UStG — VAT to be accounted for by the recipient" |
| Buyer's US-side obligation | No EU VAT self-assessment arises (supply is outside EU VAT scope entirely, as the buyer has no EU establishment) |
| Buyer's DE VAT registration | Irrelevant to determining place of supply for this service |

> ⚠️ **The supplier has incorrectly applied German VAT.** Showing the buyer's DE VAT ID on the invoice does not automatically trigger Article 44 treatment *in Germany*; rather, it should have triggered the supplier's recognition that the buyer is a taxable person and that Article 44 applies — pointing supply *away from* Germany.

---

## 3. Is the €7,600 VAT Reclaimable?

### Route 1: Input Tax Deduction (§ 15 UStG / Art. 168 VAT Directive)
**Not available.** Input tax deduction requires the purchased service to be used for taxable transactions *within Germany*. The buyer has no German taxable activity related to this service; the consulting is consumed in the US. Deduction under the German VAT return is **blocked**.

### Route 2: EU VAT Refund Directive (2008/9/EC) — "8th Directive"
**Not available** to this buyer. Directive 2008/9/EC applies to taxable persons established in another **EU Member State**. The buyer is US-established.

### Route 3: EU-Non-EU Refund (13th Directive / § 59–61 UStDV)
**Potentially available in principle**, but with a critical obstacle:

| Condition | Status |
|---|---|
| Claimant established outside EU | ✅ US company |
| Claimant not registered/liable for VAT in Germany (beyond the refund itself) | ❌ **Fails** — buyer holds an active DE VAT ID |
| Reciprocity (US–Germany) | Partially recognized, but moot given above |

**Germany's Bundeszentralamt für Steuern (BZSt) will reject a 13th Directive refund claim from an entity holding a German VAT registration.** The expectation is that such entities account for themselves via their VAT return — creating a circular problem since Route 1 is also blocked.

### Route 4: Recovery via Corrected Invoice
**This is the correct and only practical path:**

```
Buyer should reject the invoice and request a credit note + corrected invoice.
```

The supplier **should not have charged VAT**. Under **§ 14c Abs. 1 UStG**, incorrectly invoiced VAT is nonetheless owed to the Finanzamt by the supplier until a correction is made. The correction mechanism is:

1. Supplier issues a **credit note** cancelling the original invoice
2. Supplier issues a **corrected invoice** for €40,000 net, €0 VAT, with the reverse-charge notation
3. Supplier reclaims the €7,600 from the Finanzamt via its VAT return
4. Buyer pays only €40,000

---

## 4. AP Action Plan

### Immediate Steps

- [ ] **Do not pay the VAT portion** (or pay under protest/in escrow pending correction)
- [ ] **Issue a formal invoice rejection notice** to the supplier citing:
  - Art. 44 VAT Directive / § 3a Abs. 2 UStG
  - The DE VAT ID does not constitute a fixed establishment for this service
  - Place of supply = United States
- [ ] **Request a corrected invoice** (credit note + new invoice at €40,000 / zero VAT)
- [ ] **Document the rejection** in the AP file for audit purposes

### If Supplier Disputes / Correction Is Delayed

- [ ] Escalate to tax counsel to issue a formal legal position letter
- [ ] Consider whether payment of €47,600 is commercially necessary; if so, pursue correction aggressively before the supplier's **VAT correction deadline** (generally within the same VAT assessment period)
- [ ] **Do not attempt a 13th Directive refund** — it will fail and consume time/cost

### Internal Controls Flag

> The buyer's AP team should implement a **screening rule**: when a US entity's DE VAT ID appears on an inbound service invoice from a German supplier, verify place-of-supply treatment *before* payment. A DE VAT ID on the invoice header does not mean German VAT applies — it may in fact mean Article 44 B2B rules *should* have exported the supply.

---

## 5. Summary Table

| Issue | Conclusion |
|---|---|
| Place of supply under Art. 44 | **United States** (buyer's place of business) |
| German VAT correctly charged? | **No — incorrectly charged** |
| Correct VAT on invoice | **€0; reverse charge notation** |
| €7,600 reclaimable via German VAT return? | **No** |
| €7,600 reclaimable via 13th Directive? | **No** (active DE VAT ID disqualifies) |
| Correct remedy | **Corrected invoice from supplier** |
| AP priority action | **Reject invoice; request credit note + corrected invoice** |

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The candidate correctly identifies that VAT should not have been charged, correctly applies Article 44, correctly notes that a VAT registration is not a fixed establishment (citing Welmory and Titanium), and addresses reclaim mechanics thoroughly (rejecting input tax deduction, 8th Directive, and 13th Directive routes). However, the response conflates 'out-of-scope' with 'reverse charge' — it recommends the corrected invoice carry a 'Reverse charge — Art. 44' notation, when the ideal answer explicitly distinguishes that reverse charge does NOT apply to a US recipient because the US is outside EU VAT entirely; the correct notation is 'outside scope of EU VAT.' This is precisely the rubric-1 failure mode ('reasons via reverse charge instead of out-of-scope'). Additionally, while the candidate cites Implementing Regulation 282/2011 Articles 21-22, it does not clearly recommend the Article 22 written establishment-confirmation step as part of AP's action plan. These omissions match the rubric-1 description.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_007 — trade_and_tax · hard · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: assumption generation across jurisdictions_

### Question

Is the German VAT correctly charged on this invoice? What should AP do, and is the VAT reclaimable? Reason from EU VAT place-of-supply rules.

### Context

```
Buyer:    US-incorporated company with no EU permanent establishment, but registered for German VAT (DE VAT ID DE123456789) because of an earlier consignment-stock arrangement.
Supplier: German consulting firm, registered for VAT in Germany only.
Service:  Strategy consulting, performed remotely from Germany, deliverable consumed by the buyer's US headquarters (the German VAT registration is unrelated to this engagement).

Supplier invoice:
  Net fee:           €40,000.00
  German VAT 19%:     €7,600.00
  Invoice total:     €47,600.00
  Buyer's DE VAT ID is shown on the invoice header.
  Note line: 'VAT charged per German law.'
```

### Rubric

- **0**: Accepts the VAT as charged, or claims it is reclaimable simply because a DE VAT ID exists, or applies reverse charge between two German parties
- **1**: Correctly identifies that VAT should not have been charged but reasons via reverse charge instead of out-of-scope, or omits the Article 22 establishment-confirmation step, or does not address reclaim mechanics
- **2**: Correctly identifies the place of supply as the US under Article 44 based on which establishment consumes the service, distinguishes out-of-scope from reverse charge, recommends invoice rejection plus Article 22 establishment confirmation, and addresses why reclaim is not the right path

### Ideal answer

The VAT is incorrectly charged. The analysis turns on the EU VAT place-of-supply rules and which 'capacity' the buyer is acting in.

B2B services place of supply (Council Directive 2006/112/EC Article 44): for services supplied to a taxable person, the place of supply is where the customer is established or has a fixed establishment to which the service is supplied. Two facts here:

1. The buyer's establishment is the US (no EU permanent establishment).
2. The deliverable is consumed by the US headquarters; the German VAT registration is incidental and unrelated to this engagement.

Therefore the place of supply is the US, which is outside the EU VAT system. The supply is outside the scope of EU VAT. The German supplier should not have charged German VAT.

The presence of the buyer's DE VAT ID on the invoice does not, by itself, change the place of supply — Article 44 is about where the customer is established for the service consumed, not which VAT IDs the customer happens to hold. A buyer with multiple establishments must communicate to the supplier which establishment is receiving the service (Implementing Regulation 282/2011, Article 22). The supplier's apparent default to 'this is German because we see a DE VAT ID' is incorrect when the deliverable is consumed elsewhere.

Note: had the service been received by the buyer's German activity (the consignment-stock operation), the place of supply would be Germany, and the supplier would charge German VAT, which the buyer could reclaim via its German VAT return. That is the alternate fact pattern.

The distinct 'reverse charge' question: if the place of supply had been Germany but the supplier and customer were in different EU states with both VAT-registered, Article 196 reverse charge would apply (customer self-accounts). That is not this case because both parties are in Germany for VAT purposes if the German establishment is the recipient. Reverse charge does not apply to a US-recipient supply because the US is outside EU VAT entirely — it is simply out of scope.

AP action:
1. Reject the invoice. Email the supplier explaining that under Article 44 the place of supply is the US (the establishment consuming the service), not Germany, and that the deliverable is unrelated to the buyer's German VAT registration.
2. Provide written confirmation of which establishment is receiving the service (Implementing Regulation 282/2011, Article 22) — this is the supplier's documentation requirement to avoid charging VAT.
3. Request a corrected invoice for €40,000 net, no VAT, with a note 'Outside scope of EU VAT — place of supply outside EU per Article 44, Directive 2006/112/EC.'
4. Reclaimability: not applicable. The €7,600 is not VAT properly due; it is not reclaimable through the German VAT return because the underlying supply is out of scope. If the supplier refuses to credit and reissue, the buyer would have to pay €47,600 and pursue an Article 13th Directive refund (refund to non-EU established taxable persons) or, more practically, dispute with the supplier — but the right answer is to fix the invoice, not to reclaim VAT that should never have been charged.

References: Council Directive 2006/112/EC Articles 44, 196; Council Implementing Regulation 282/2011 Articles 10–13, 21–22; 13th VAT Directive 86/560/EEC (refund to non-EU businesses).

### Model response

# VAT Treatment Analysis

## Place of Supply Determination

Under **EU VAT Directive Article 44**, services are supplied where the customer is **established**. The critical question is: where is the buyer established for VAT purposes?

**Key facts:**
- Buyer: US-incorporated, no EU permanent establishment
- Buyer's place of establishment: **United States** (not Germany)
- German VAT registration: exists but is **unrelated** to this consulting engagement (legacy from consignment stock)
- Service consumption point: irrelevant under Article 44

## Correct VAT Treatment

**The German VAT is INCORRECTLY charged.**

### Reasoning:

1. **Place of supply rule**: Services to a customer established **outside the EU** are **exempt from VAT** under Article 44(1) of the VAT Directive.

2. **Buyer's VAT status is immaterial**: The buyer's German VAT registration does not establish them as "established in Germany" for this transaction. Registration for one specific business activity (consignment stock) does not extend to all service purchases.

3. **Correct outcome**: The supply should be treated as a **reverse-charge situation** or more accurately, as a **supply outside the scope of EU VAT**. The supplier should **not charge VAT**.

---

## Actions for Accounts Payable

| Action | Rationale |
|--------|-----------|
| **Contact the supplier immediately** | Request a corrected invoice without VAT (€40,000.00 net only) |
| **Provide documentation** | Supply proof of US establishment (incorporation documents, business address, etc.) and explain the German VAT ID is unrelated to this transaction |
| **Reference the VAT exemption** | Cite Article 44 VAT Directive—services to customers outside the EU are out of scope |
| **Request credit note** | If already paid, obtain a credit note for €7,600.00 |

---

## VAT Recoverability

**The VAT is NOT reclaimable** because:

1. **It shouldn't have been charged** in the first place (the supply is out of scope, not a taxable supply to a registered entity)
2. US companies cannot reclaim German VAT (no establishment in Germany for this transaction)
3. Claiming VAT that shouldn't exist creates audit risk

**Proper treatment**: The invoice should show €40,000.00 net with a notation such as:
> *"VAT exempt—customer established outside the EU (Article 44 VAT Directive)"*

---

## Conclusion

**No, the VAT is incorrectly charged.** The supplier has misapplied German law by relying on the buyer's German VAT ID rather than correctly identifying the buyer's place of establishment (USA). AP should request a corrected invoice for €40,000.00 net.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies that VAT was incorrectly charged and that the place of supply is outside the EU under Article 44, with the buyer established in the US. It correctly notes that the German VAT ID does not change the analysis and that reclaim is not the right path. However, it has notable weaknesses: (1) it conflates reverse-charge with out-of-scope ('should be treated as a reverse-charge situation or more accurately, as a supply outside the scope') rather than cleanly distinguishing them; (2) it does not cite or invoke Implementing Regulation 282/2011 Article 22 regarding the buyer's obligation to confirm which establishment receives the service; (3) it incorrectly states 'service consumption point: irrelevant under Article 44' when in fact the consuming establishment is central to the analysis when a buyer has multiple establishments. These omissions and the muddled reverse-charge framing place it at level 1 rather than 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_009 — supplier_data · hard · **score 1/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: assumption generation across multiple regulatory regimes_

### Question

What screening should run on this supplier as part of onboarding? Identify the red flags, the legal/regulatory regimes that apply, and the recommended onboarding decision.

### Context

```
Onboarding request for a new supplier:
  Legal name:           Pacific Trade Solutions LLC
  Formation:            Delaware (formed 2025-11-04)
  Registered agent:     A national registered-agent service
  Listed UBO:           Ivan Petrov, residential address in Limassol, Cyprus
  Bank:                 Latvia (SWIFT routing)
  Goods supplied:       Electronic components (microcontrollers, FPGAs, RF components)
  Shipped from:         Hong Kong, via a freight forwarder unknown to the buyer
  Initial PO request:   $250,000
  Expected annual spend: $1,000,000
  Other notes: supplier requested a 50% prepayment on the first PO, citing 'manufacturing capacity reservation.'
```

### Rubric

- **0**: Onboards the supplier without enhanced due diligence, or misses sanctions/export-control regimes entirely, or treats the prepayment as routine
- **1**: Identifies sanctions and export-control concerns but misses the OFAC 50% rule, the FinCEN BOI requirement, the bank-callback control, or the graduated-onboarding recommendation
- **2**: Identifies all major red flags, names the relevant regimes (OFAC including 50% rule, EU/UK/UN sanctions, BIS EAR including Entity List, FinCEN BOI, FCPA), recommends specific verification steps including independent bank-account verification and prepayment rejection, and proposes graduated onboarding with ongoing screening

### Ideal answer

This packet has multiple red flags that, taken together, require enhanced due diligence and a hold on onboarding pending resolution. Treat as high-risk.

Red flags:
1. Newly formed Delaware LLC (Nov 2025) with no operating history — shell-company indicator.
2. UBO with a Russian-origin name and Cyprus residence — Cyprus is a known nexus for Russian-affiliated structures and has been a focal jurisdiction since 2022 EU/US Russia sanctions; not disqualifying on its own but raises sanctions-screening priority.
3. Bank in Latvia — Baltic banking has been the subject of multiple sanctions-evasion enforcement actions; payment routing must be verified.
4. Goods are dual-use electronics shipped from Hong Kong — high export-control risk for diversion to Russia or other restricted end-users; HK has been heavily flagged by US BIS as a diversion hub.
5. 50% prepayment request — common precursor to fraud or to funds-routing schemes; legitimate semiconductor distributors rarely require 50% prepay from a buyer with no relationship history.
6. Freight forwarder unknown to the buyer — diversion-risk indicator.

Applicable screening regimes:
- Sanctions screening: name and identifier screening of the entity, the UBO, and the Latvian bank against:
  - OFAC SDN, OFAC sectoral lists, OFAC 50% rule (entities ≥50% owned by SDN persons are themselves blocked even if not listed)
  - EU consolidated financial sanctions list
  - UK HMT (OFSI) consolidated list
  - UN Security Council list
  - Canadian, Swiss, Australian, Japanese sanctions lists if relevant
- Beneficial ownership: under the Corporate Transparency Act / FinCEN BOI rule (effective 2024), reporting companies disclose UBOs to FinCEN. The buyer should require the supplier to provide its FinCEN BOI report or equivalent evidence and verify UBO identity (passport, address verification). Confirm UBO is not a sanctioned person and not on OFAC's 50% derivative blocking.
- Export controls (US): even though the buyer is the US importer, if components are of US origin or contain US-origin technology subject to the EAR, the supplier and consignee chain must be screened against:
  - BIS Entity List, Unverified List, Military End User List, Denied Persons List
  - State Department debarred parties (ITAR, if applicable)
  - Non-SDN Menu-Based Sanctions List, NS-CMIC list
  ECCN of components must be determined; if controlled (e.g., 3A001 microelectronics, 3A002 RF), end-use and end-user statements required, and an export license may be needed for shipment from HK depending on classification.
- AML/KYC (under the buyer's own AML program if a financial institution; otherwise as commercial best practice and to support OFAC compliance): source of funds, payment routing verification, callback to the UBO via independently-obtained contact info — never via the contact provided in the onboarding packet.
- Anti-bribery: under FCPA, also screen for connections to foreign officials; Cyprus politically-exposed-persons screening on the UBO.

Recommended decision:
- Do NOT onboard or release any PO until:
  a) Sanctions screening on entity, UBO, and bank is clear across all relevant lists (with the OFAC 50% derivative test applied to UBO ownership chain).
  b) UBO identity is verified independently (government ID, address verification not via the same packet).
  c) Components are classified (ECCN); if controlled, end-use/end-user statements obtained and BIS license requirements assessed; HK consignee screened against Entity List.
  d) Bank account is verified by independent callback to the supplier using contact info NOT taken from the onboarding packet (mitigates business-email-compromise / account takeover risk).
  e) The 50% prepayment is rejected as a non-starter for a first engagement with a new high-risk supplier; if any prepayment, it should be against a performance bond or escrow, and only after all other diligence is clear.
- Even if all of the above is clear, recommend graduated onboarding: first PO at significantly less than $250k, with a denied-parties screen rerun on every shipment (suppliers can be added to lists between transactions) and a 12-month review.

References: 31 CFR Part 501 et seq. (OFAC), OFAC FAQ on 50% rule, 31 CFR §1010.380 (FinCEN BOI), 15 CFR Parts 730–774 (BIS EAR), BIS Entity List, EU Council Regulation 833/2014 as amended (Russia sanctions), FCPA (15 USC §78dd-1 et seq.).

### Model response

# Supplier Onboarding Risk Assessment: Pacific Trade Solutions LLC

---

## Executive Summary

This supplier profile presents **an exceptionally high concentration of serious red flags** spanning sanctions exposure, export control violations, financial crime, and procurement fraud. The combination of factors is not coincidental-looking; it matches documented typologies used to circumvent U.S. export controls on dual-use electronics. **A standard onboarding approval is contraindicated. Enhanced due diligence (EDD) at minimum, and likely rejection or referral to legal/compliance, is warranted before any commercial engagement.**

---

## I. Required Screening Checks

### A. Sanctions & Restricted-Party Screening

| Screen | Authority | Rationale |
|---|---|---|
| OFAC SDN & Consolidated Sanctions List | 31 C.F.R. Parts 500–598 | UBO (Ivan Petrov), entity, freight forwarder, and bank must all be screened. Russian-sounding name + Cyprus address is a documented sanctions-evasion profile. |
| EU Consolidated Sanctions List | EU Reg. 269/2014 et seq. | Cyprus is EU jurisdiction; Limassol is a known offshore hub for Russian-connected entities. |
| UK OFSI Sanctions List | Policing, Crime, Sanctions & AML Act 2017 | If your entity has UK nexus. |
| BIS Entity List / Denied Persons List / Unverified List | EAR 15 C.F.R. Part 744 | Freight forwarder identity is unknown—this alone triggers an Unverified List check concern. |
| State Dept. Debarred/Nonproliferation Lists | ITAR 22 C.F.R. Parts 120–130 | RF components in particular may be USML-adjacent. |
| UN Consolidated List | UN Charter Art. 25 | Global baseline. |

> **Critical note:** Screening must cover **all associated parties**: UBO, any directors/officers, the Latvian bank, the Hong Kong freight forwarder (once identified), and any intermediate entities.

---

### B. Export Control Classification

| Action | Regulatory Basis |
|---|---|
| Classify each SKU under the Commerce Control List (CCL) | EAR 15 C.F.R. Part 774 |
| Determine ECCN for microcontrollers, FPGAs, and RF components | Many fall under ECCN 3A001 (electronics); RF components frequently under 3A001.b; FPGAs can reach 3A001.a.7 |
| Assess AT (Anti-Terrorism), NS (National Security), and MT (Missile Technology) controls | EAR Part 738 |
| Determine if end-use/end-user certificate is required or if a license exception applies | EAR Part 740 |
| Evaluate whether items are subject to Russia/Belarus/Iran "foreign direct product rule" (FDPR) | EAR § 734.9 — expanded dramatically post-Feb 2022 |

> **Key finding:** Microcontrollers, FPGAs, and RF components are precisely the components identified by BIS, NSA, and allied agencies as being systematically procured through front companies to supply Russian military and defense programs. The U.S. has issued multiple alerts (including the Oct. 2023 BIS/OFAC/DOJ tri-agency advisory) specifically naming this procurement typology.

---

### C. Anti-Money Laundering / Know Your Business (KYB)

- **UBO verification:** Obtain certified corporate documents; confirm Ivan Petrov's identity via government-issued ID, proof of address, and adverse media. Limassol, Cyprus is a Tier-1 high-risk jurisdiction for Russian illicit finance.
- **Beneficial ownership chain:** Confirm no intervening shell layers obscuring ultimate control. Delaware single-member LLCs are trivial to form anonymously; formation date of **November 2025** means the entity is **days or weeks old**—a major red flag.
- **Correspondent banking risk:** Latvia's banking sector has been subject to multiple FinCEN and FATF actions for Russian money laundering exposure (ABLV Bank shutdown 2018; ongoing elevated risk). A Latvian bank receiving $250K–$1M in prepayments for electronics from a brand-new Delaware LLC is a textbook suspicious transaction pattern.
- **PEP screening:** Check Ivan Petrov against Politically Exposed Persons databases (World-Check, Dow Jones, etc.).
- **Adverse media search:** Full Boolean search across English, Russian, and Latvian language sources.

---

### D. Corporate Integrity / Fraud Screening

- Certificate of Formation verification (Delaware Division of Corporations).
- Registered agent identity (national RA services are legitimate but confirm no mass-registration fraud pattern).
- Verify physical operating address and manufacturing capability—**no evidence of actual manufacturing has been provided.**
- Freight forwarder identification: Refusal or inability to name the forwarder is itself a disqualifying factor under BIS guidance.

---

## II. Red Flag Analysis

### 🔴 Critical / Disqualifying Red Flags

| # | Red Flag | Why It Matters |
|---|---|---|
| 1 | **Goods are dual-use electronics (MCUs, FPGAs, RF)** | The most commonly cited product category in BIS enforcement actions related to Russia/Iran/China procurement networks. Subject to strict EAR controls; may require export licenses. |
| 2 | **Entity formed November 2025** (days/weeks old) | Newly formed shell-style entities are a primary procurement-evasion vehicle. No operational history, no track record, no auditable performance. |
| 3 | **UBO domiciled in Limassol, Cyprus** | Limassol is the preeminent hub for Russian offshore finance; EU/US/UK typology documents specifically flag this geography for sanctions evasion. |
| 4 | **Russian-name UBO + Cyprus address + Latvian bank** | This exact three-node combination appears in documented Russian procurement networks for sanctioned goods. It is a recognized typology, not a coincidence. |
| 5 | **Unknown freight forwarder** | EAR requires due diligence on all parties in the export chain. An unknown forwarder prevents Red Flag screening and may itself violate EAR "know your customer" obligations. BIS explicitly lists "refusal to identify end-user" as a Red Flag requiring transaction refusal. |
| 6 | **50% prepayment ($125,000) requested** | Classic fraud/advance-fee pattern. Also, prepayment to a Latvian account for goods shipped from Hong Kong by an unknown forwarder is a high-risk funds-transfer structure. |
| 7 | **Shipment origin: Hong Kong** | Post-2020, Hong Kong is no longer treated as a separate export control destination from mainland China (EAR § 740.2); it is also a documented transshipment node for controlled U.S.-origin electronics to Russia and Iran. |

### 🟠 Elevated / Compounding Risk Factors

| # | Red Flag | Why It Matters |
|---|---|---|
| 8 | **Delaware formation + national registered agent** | Anonymized ownership structure; no reputational accountability for the registered agent. |
| 9 | **No verifiable manufacturing capability** | Claim of "manufacturing capacity reservation" is contradicted by zero evidence of a factory, supply chain, or prior business. |
| 10 | **$1M annual spend** | Size is large enough to be material to enforcement agencies if things go wrong; small enough to be below some automated reporting thresholds—a structuring-adjacent concern. |
| 11 | **Freight forwarder unknown to the buyer** | Suggests the supplier controls the logistics chain entirely, preventing the buyer from conducting independent verification of the destination of goods. |
| 12 | **No references, certifications, or auditable history** | Standard supplier qualification cannot be completed. |

---

## III. Applicable Legal & Regulatory Regimes

### United States
| Regime | Key Provisions |
|---|---|
| **Export Administration Regulations (EAR)** | 15 C.F.R. Parts 730–774; Red Flag guidance at Supp. 3 to Part 732; Entity List (Part 744). Potential civil penalties up to $364,992/violation or twice transaction value; criminal up to $1M/violation + imprisonment. |
| **International Emergency Economic Powers Act (IEEPA)** | 50 U.S.C. § 1701 et seq.; basis for OFAC Russia/Belarus/Iran/Cuba sanctions programs. |
| **Bank Secrecy Act /

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response identifies all major red flags comprehensively and names most relevant regimes (OFAC, EU, UK OFSI, UN, BIS EAR including Entity List, ITAR, IEEPA). However, the response is truncated mid-sentence at 'Bank Secrecy Act /' and does not explicitly address several rubric-required elements: the OFAC 50% rule for derivative blocking, the FinCEN BOI/Corporate Transparency Act requirement, the independent bank-account callback verification control, explicit prepayment rejection recommendation, and graduated onboarding with ongoing screening. FCPA is also not mentioned. While the response is strong on red flag identification and screening lists, the absence of these specific controls and the truncation place it at level 1 rather than 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_009 — supplier_data · hard · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: assumption generation across multiple regulatory regimes_

### Question

What screening should run on this supplier as part of onboarding? Identify the red flags, the legal/regulatory regimes that apply, and the recommended onboarding decision.

### Context

```
Onboarding request for a new supplier:
  Legal name:           Pacific Trade Solutions LLC
  Formation:            Delaware (formed 2025-11-04)
  Registered agent:     A national registered-agent service
  Listed UBO:           Ivan Petrov, residential address in Limassol, Cyprus
  Bank:                 Latvia (SWIFT routing)
  Goods supplied:       Electronic components (microcontrollers, FPGAs, RF components)
  Shipped from:         Hong Kong, via a freight forwarder unknown to the buyer
  Initial PO request:   $250,000
  Expected annual spend: $1,000,000
  Other notes: supplier requested a 50% prepayment on the first PO, citing 'manufacturing capacity reservation.'
```

### Rubric

- **0**: Onboards the supplier without enhanced due diligence, or misses sanctions/export-control regimes entirely, or treats the prepayment as routine
- **1**: Identifies sanctions and export-control concerns but misses the OFAC 50% rule, the FinCEN BOI requirement, the bank-callback control, or the graduated-onboarding recommendation
- **2**: Identifies all major red flags, names the relevant regimes (OFAC including 50% rule, EU/UK/UN sanctions, BIS EAR including Entity List, FinCEN BOI, FCPA), recommends specific verification steps including independent bank-account verification and prepayment rejection, and proposes graduated onboarding with ongoing screening

### Ideal answer

This packet has multiple red flags that, taken together, require enhanced due diligence and a hold on onboarding pending resolution. Treat as high-risk.

Red flags:
1. Newly formed Delaware LLC (Nov 2025) with no operating history — shell-company indicator.
2. UBO with a Russian-origin name and Cyprus residence — Cyprus is a known nexus for Russian-affiliated structures and has been a focal jurisdiction since 2022 EU/US Russia sanctions; not disqualifying on its own but raises sanctions-screening priority.
3. Bank in Latvia — Baltic banking has been the subject of multiple sanctions-evasion enforcement actions; payment routing must be verified.
4. Goods are dual-use electronics shipped from Hong Kong — high export-control risk for diversion to Russia or other restricted end-users; HK has been heavily flagged by US BIS as a diversion hub.
5. 50% prepayment request — common precursor to fraud or to funds-routing schemes; legitimate semiconductor distributors rarely require 50% prepay from a buyer with no relationship history.
6. Freight forwarder unknown to the buyer — diversion-risk indicator.

Applicable screening regimes:
- Sanctions screening: name and identifier screening of the entity, the UBO, and the Latvian bank against:
  - OFAC SDN, OFAC sectoral lists, OFAC 50% rule (entities ≥50% owned by SDN persons are themselves blocked even if not listed)
  - EU consolidated financial sanctions list
  - UK HMT (OFSI) consolidated list
  - UN Security Council list
  - Canadian, Swiss, Australian, Japanese sanctions lists if relevant
- Beneficial ownership: under the Corporate Transparency Act / FinCEN BOI rule (effective 2024), reporting companies disclose UBOs to FinCEN. The buyer should require the supplier to provide its FinCEN BOI report or equivalent evidence and verify UBO identity (passport, address verification). Confirm UBO is not a sanctioned person and not on OFAC's 50% derivative blocking.
- Export controls (US): even though the buyer is the US importer, if components are of US origin or contain US-origin technology subject to the EAR, the supplier and consignee chain must be screened against:
  - BIS Entity List, Unverified List, Military End User List, Denied Persons List
  - State Department debarred parties (ITAR, if applicable)
  - Non-SDN Menu-Based Sanctions List, NS-CMIC list
  ECCN of components must be determined; if controlled (e.g., 3A001 microelectronics, 3A002 RF), end-use and end-user statements required, and an export license may be needed for shipment from HK depending on classification.
- AML/KYC (under the buyer's own AML program if a financial institution; otherwise as commercial best practice and to support OFAC compliance): source of funds, payment routing verification, callback to the UBO via independently-obtained contact info — never via the contact provided in the onboarding packet.
- Anti-bribery: under FCPA, also screen for connections to foreign officials; Cyprus politically-exposed-persons screening on the UBO.

Recommended decision:
- Do NOT onboard or release any PO until:
  a) Sanctions screening on entity, UBO, and bank is clear across all relevant lists (with the OFAC 50% derivative test applied to UBO ownership chain).
  b) UBO identity is verified independently (government ID, address verification not via the same packet).
  c) Components are classified (ECCN); if controlled, end-use/end-user statements obtained and BIS license requirements assessed; HK consignee screened against Entity List.
  d) Bank account is verified by independent callback to the supplier using contact info NOT taken from the onboarding packet (mitigates business-email-compromise / account takeover risk).
  e) The 50% prepayment is rejected as a non-starter for a first engagement with a new high-risk supplier; if any prepayment, it should be against a performance bond or escrow, and only after all other diligence is clear.
- Even if all of the above is clear, recommend graduated onboarding: first PO at significantly less than $250k, with a denied-parties screen rerun on every shipment (suppliers can be added to lists between transactions) and a 12-month review.

References: 31 CFR Part 501 et seq. (OFAC), OFAC FAQ on 50% rule, 31 CFR §1010.380 (FinCEN BOI), 15 CFR Parts 730–774 (BIS EAR), BIS Entity List, EU Council Regulation 833/2014 as amended (Russia sanctions), FCPA (15 USC §78dd-1 et seq.).

### Model response

# Supplier Onboarding Risk Assessment

## RED FLAGS (Severity: HIGH)

| Flag | Risk Category | Concern |
|------|---------------|---------|
| **Recent formation (2025-11-04)** | Structuring risk | Entity created days before onboarding request; suggests potential shell company |
| **Delaware LLC + offshore UBO** | Beneficial ownership opacity | Delaware allows privacy; Limassol (Cyprus) residence suggests asset/tax structuring |
| **Latvian banking** | Sanctions/AML risk | Non-standard banking for electronics supplier; Latvia is EU but proximity to Russian sanctions evasion concerns |
| **UBO in Cyprus** | Geopolitical risk | Cyprus is known facilitator for sanctions evasion and opaque ownership structures |
| **Unknown freight forwarder** | Supply chain opacity | Prevents visibility into actual sourcing; common in sanctions evasion schemes |
| **Hong Kong origin** | Export control risk | Electronics from HK via unknown routes raise ITAR/EAR concerns (microcontrollers, FPGAs, RF components are sensitive) |
| **50% prepayment demand** | Fraud/insolvency risk | Unusual for established suppliers; indicates either financial distress or fraud intent |
| **High initial spend ($1M annually)** | Concentration risk | Large commitment to high-risk entity |

---

## APPLICABLE LEGAL/REGULATORY REGIMES

### 1. **U.S. Export Controls** (if buyer is U.S.-based)
- **EAR (15 CFR Part 730-774)**: Microcontrollers, FPGAs, and RF components may be controlled
- **ITAR (22 CFR Parts 120-130)**: If any content is defense-related
- **Commerce Department / BIS**: End-use verification required; Hong Kong → unknown destination raises concerns
- **Risk**: Violation penalties up to $300,000+ per violation; criminal liability

### 2. **Office of Foreign Assets Control (OFAC)**
- **Sanctions screening**: Mandatory for Cyprus-based UBO, Latvian banking
- **Russian sanctions evasion**: Particular concern given Latvia's proximity; Cyprus is common funnel
- **Risk**: Civil penalties $20,000+ per violation; criminal penalties up to $1M

### 3. **Anti-Money Laundering (AML) / Know Your Customer (KYC)**
- **USA PATRIOT Act, Section 312**: Enhanced due diligence for high-risk jurisdictions
- **CIP/CDD Rules**: Bank Secrecy Act compliance
- **EU AML Directive (if EU buyer)**: Stricter beneficial ownership requirements
- **Risk**: Regulatory sanctions, account closure, reporting obligations

### 4. **Foreign Corrupt Practices Act (FCPA)**
- Lower risk but relevant if Cyprus/Latvia presence involves hidden ownership
- Indirect corruption risk via opaque payment chains

### 5. **Customs & Border Protection (CBP)**
- Supply chain security; importer security filing (if importing to U.S.)
- C-TPAT eligibility assessment

---

## RECOMMENDED ONBOARDING DECISION

### **RECOMMENDATION: REJECT or CONDITIONAL HOLD**

**Do not proceed without substantial remediation.**

### Rationale:

1. **Composite Risk Profile**: This is not a single red flag but a **pattern consistent with sanctions evasion, export control violations, or fraud**:
   - Overnight incorporation + offshore UBO + opaque sourcing = structuring pattern
   - High-value electronics + indirect routing + prepayment demand = classic risk triad

2. **Regulatory Exposure**: Any transaction carries material legal risk (export control, OFAC, AML violations)

3. **Reputational Risk**: Association with high-risk supplier damages compliance posture and buyer's own regulatory standing

---

## CONDITIONAL PATH (If commercial necessity exists)

If the buyer cannot reject outright, implement **Phase 1: Enhanced Due Diligence (EDD)**:

### Required actions before any PO:

1. **Beneficial Ownership Verification**
   - Full corporate registry search (Delaware SoS, Cyprus registry)
   - Request certified UBO declaration with source-of-funds documentation
   - Conduct adverse-media search on Ivan Petrov (OFAC, sanctions lists, criminal databases)
   - Consider third-party verification service (e.g., Dun & Bradstreet, LexisNexis)

2. **Export Control Compliance**
   - **EAR Classification**: Confirm all goods are EAR99 or obtain commodity jurisdiction (CJ) from BIS
   - **End-use certification**: Require written certification that goods are not for: Iranian, North Korean, Syrian, Cuban, Crimean end-users; not for proliferation
   - **Validate freight forwarder**: Obtain name, contact, and NVOCC license; audit sourcing logistics

3. **OFAC/Sanctions Screening**
   - Run supplier, UBO, bank, and beneficial owners through:
     - OFAC Consolidated Sanctions List (SDN)
     - EU consolidated sanctions list
     - UN consolidated list
     - UK, Canada, Australia equivalent lists
   - Monitor quarterly for updates

4. **AML/KYC Deep Dive**
   - Request: Corporate formation documents, UBO affidavit, source-of-funds statement, bank reference
   - Verify bank account legitimacy (contact Latvian bank directly)
   - Assess purpose of Cyprus residency and timing

5. **Payment Terms Restructuring**
   - **Reject 50% prepayment** as unacceptable; offer standard Net 30 or escrow arrangement
   - Use letters of credit (LC) or escrow to reduce fraud risk
   - Require performance bond for large orders

6. **Supply Chain Transparency**
   - Require full bill of materials sourcing
   - Direct shipment to buyer (not freight forwarder's warehouse) to maintain custody/control
   - Third-party audit of manufacturing facility if prepayment demanded

---

## ESCALATION

**Recommend immediate escalation to:**
- Compliance officer
- Chief Procurement Officer
- Legal counsel (export control specialist)
- Risk/Treasury (pre-payment authorization)

This should be a **board-level or senior executive decision** given regulatory exposure.

---

## CONCLUSION

| Decision | Rationale |
|----------|-----------|
| **Proceed as-is?** | ❌ **No** – unacceptable regulatory risk |
| **Proceed with conditions?** | ⚠️ **Only if EDD clears ALL red flags** – likely 4–8 weeks |
| **Reject?** | ✅ **Recommended** – unless strategic necessity overrides compliance |

The pattern here is **too consistent with bad-faith actors** to proceed without extraordinary diligence.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response identifies most major red flags (shell company, Cyprus UBO, Latvian banking, HK shipping, prepayment, unknown forwarder) and names the key regimes (EAR/BIS, OFAC, AML/KYC, FCPA, ITAR). It recommends rejection or EDD with sanctions screening across multiple jurisdictions, prepayment rejection, and ongoing monitoring. However, it misses several specific items required for a score of 2: (1) the OFAC 50% rule for derivative blocking is not mentioned; (2) the FinCEN BOI rule under the Corporate Transparency Act (31 CFR §1010.380) is not specifically cited—only generic 'beneficial ownership verification' is mentioned; (3) the BIS Entity List, Unverified List, and Military End User List are not specifically named; (4) the bank verification suggests 'contact Latvian bank directly' but does not specify independent callback using contact info NOT from the onboarding packet (BEC mitigation); (5) graduated onboarding with reduced first PO and rescreening per shipment is not clearly proposed. This fits the rubric's level 1 description of identifying sanctions/export concerns but missing the OFAC 50% rule, FinCEN BOI, bank-callback control, and graduated onboarding.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_010 — close_and_controls · hard · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: multi-step controls reasoning under SOX_

### Question

Diagnose the SOX P2P control failures that allowed this pattern. Describe the specific control activities that should have prevented or detected it, and how to remediate. Address whether this is likely a material weakness.

### Context

```
Fact pattern (composite, in the style of SEC AAER ghost-vendor cases):

Over an 18-month period at a SOX-registrant company, an AP clerk processed payments to 'Northern Logistics Services LLC' totaling $480,000 across 49 invoices. Investigation after a tip from a coworker revealed:
- The AP clerk had access in the ERP to (a) create new vendor master records, (b) approve invoices under $10,000, and (c) initiate ACH payment runs.
- Northern Logistics had been added to the vendor master by the AP clerk, with the clerk's home P.O. box as the remit-to address and a bank account in the name of a relative.
- All 49 invoices were 'non-PO' for 'logistics services,' with amounts ranging from $9,800 to $9,950.
- No contract or SOW was on file for the supplier.
- The company's policy requires PO coverage for all services > $10,000 and CFO approval for new vendor adds for spend > $50,000/year, but these thresholds were never tripped because of how the activity was structured.
- The external auditor selected the vendor master change log as a routine SOX walkthrough sample but had not selected any of the 49 invoices in their substantive sample.
```

### Rubric

- **0**: Misses segregation of duties as the primary failure, or treats this as a single-control gap, or fails to address material-weakness analysis
- **1**: Identifies SoD and one or two other gaps, but misses the threshold-clustering analytic, the employee-vendor match control, the cumulative-spend trigger, or the material-weakness reasoning
- **2**: Identifies SoD plus at least four additional control gaps (vendor-master maker-checker, employee-vendor match, cluster-below-threshold analytic, rolling-cumulative-spend escalation, ITGC access review), proposes specific remediations for each, and reaches a defensible material-weakness conclusion under AS 2201 with the right reasoning (severity by potential not actual loss)

### Ideal answer

Failed controls and design defects:

1. Segregation of duties (the primary failure). Under PCAOB AS 2201 and the COSO 2013 framework, the P2P cycle requires segregation across at minimum: vendor-master maintenance, invoice approval, and payment initiation. A single employee with all three privileges has end-to-end control of cash disbursement to a vendor of their own creation. This is the textbook ghost-vendor enabler. The control deficiency is in the access design (entitlement grants), not just in operation.

2. Vendor-master change controls. Adding a new vendor should require:
   - Independent maker-checker approval (the clerk who keys the add cannot be the approver).
   - W-9 / W-8 on file before activation; TIN match against IRS TIN matching service.
   - Address verification, including a check that the remit-to is not a P.O. box matching an employee's known address (an automated employee-vendor address/bank match is a common detective control).
   - Bank account verification via independent callback to a phone number for the supplier obtained from a public source (not the supplier packet itself).
   The failure here permitted the clerk to set the remit-to to their own P.O. box and the bank account to a relative.

3. Threshold-cluster monitoring (structuring). Forty-nine invoices clustered in a $150 band immediately below the $10,000 PO/approval threshold is a textbook structuring pattern. A standard analytic — distribution of invoice amounts by vendor compared to authorization thresholds — would have flagged this within weeks. Additional analytics: Benford's-law deviation on first-digit distribution, invoice-frequency anomalies for new vendors. This is a detective control gap.

4. Non-PO services without contract. Policy required POs for services > $10k and the supplier had no contract or SOW. The non-PO pathway should require:
   - A contract or engagement letter referenced on the invoice for any services vendor.
   - Periodic review of non-PO spend by vendor to flag vendors with high cumulative non-PO spend (this vendor had $480k cumulative — should have been escalated long before the 18-month mark).

5. New-vendor-spend escalation. The policy required CFO approval for new-vendor spend > $50,000/year, but the threshold was applied to a single invoice / single PO, not cumulatively over a rolling 12 months. A 12-month rolling cumulative trigger would have caught this within ~5 invoices (~$50k).

6. ITGC / access review. Periodic access reviews (typically quarterly) should have flagged the toxic combination of entitlements held by the AP clerk. The fact that this combination was granted and never reviewed is an ITGC deficiency.

Remediation:
- Re-design role-based access in the ERP to enforce segregation: vendor-master role, invoice-approval role, payment-initiation role are mutually exclusive. Document in an SoD matrix and enforce via GRC tooling.
- Implement maker-checker on vendor-master adds and changes; require an independent reviewer outside AP.
- Implement employee-vendor matching analytic (compare vendor remit-to addresses, phone numbers, and bank accounts to employee HR data) — run continuously, alert on match.
- Implement threshold-cluster analytic on invoice amounts vs. authorization thresholds, by vendor and across vendors.
- Implement rolling-12-month cumulative spend trigger for new vendors to feed CFO approval gating.
- Lower the PO requirement threshold for services or eliminate the non-PO services pathway entirely.
- Remediate the ITGC: implement quarterly SoD-conflict access reviews with documented review evidence.
- Targeted lookback: examine all vendors added by this clerk and all non-PO vendors with high cumulative spend over the past 24 months; assess for similar patterns.

Material-weakness assessment:
Under PCAOB AS 2201, a control deficiency is a material weakness if there is a reasonable possibility that a material misstatement of the financial statements would not be prevented or detected on a timely basis. This case:
- The deficiency is in access design and SoD — pervasive, not isolated.
- The same SoD weakness could enable misstatements far larger than $480k; severity is judged by potential, not just actual loss.
- $480k is below typical materiality for a SOX registrant of meaningful size, but the controls' inability to prevent a more material occurrence is what drives the conclusion.
- The structuring pattern was not detected by management; the auditor did not happen to sample these invoices; detection came from a tip — meaning neither preventive nor detective controls operated effectively.
Likely conclusion: material weakness in P2P internal controls, requiring disclosure under Item 9A of Form 10-K and re-evaluation of management's ICFR assertion. If the misstatement crosses materiality after the lookback, restatement may be required. Auditor will reassess scope and is required to communicate to the audit committee under AS 1301.

References: PCAOB AS 2201 ('An Audit of Internal Control over Financial Reporting'), AS 1301 ('Communications with Audit Committees'), COSO 2013 framework, SEC Regulation S-K Item 308, SEC AAERs on ghost-vendor and structuring schemes (representative cases — user should anchor to a specific cited AAER if used in publication).

### Model response

# SOX Procure-to-Pay Control Failure Analysis

## I. Control Failures Diagnosis

### A. Root Cause Map

This fraud exploited **layered control gaps**, each individually exploitable:

| Control Layer | Failure | Mechanism |
|---|---|---|
| **Preventive: Segregation of Duties (SoD)** | Incompatible roles consolidated | Single clerk: vendor master create + invoice approval + payment initiation |
| **Preventive: New Vendor Authorization** | Threshold-based bypass | CFO approval triggered at >$50K/year; structured at $9,800–$9,950 invoices to avoid threshold |
| **Preventive: Purchase Order Requirement** | Threshold-based bypass | Policy required POs for >$10K services; all invoices stayed under $10K |
| **Detective: Invoice Substantive Testing** | Sampling gap | External auditor tested vendor *master changes* but not invoices from new vendors; internal audit absent or similarly narrow |
| **Detective: Completeness/Existence** | No independent matching | No three-way match (PO-receipt-invoice) enforced for non-PO invoices; no "null PO" flag or control |
| **Preventive: Vendor Due Diligence** | No beneficial ownership validation | No requirement to verify payee identity, address legitimacy, or beneficial ownership of vendor bank account |
| **Preventive: Exception Monitoring** | No alert on patterns | No rule to flag: multiple invoices from single vendor under threshold, or clustering of high-value transactions just below approval limits |

---

## II. Specific Control Activities That Should Have Prevented or Detected

### A. **Preventive Controls (Should Have Stopped Entry)**

#### 1. **Segregation of Duties (SoD) Enforcement**
   - **Current state:** Clerk had vendor master create, invoice approval, and payment initiation rights.
   - **Required control:** 
     - Vendor master creation → assigned to Procurement only
     - Invoice approval → assigned to separate Finance/AP role with different supervisor
     - Payment initiation → Treasury/AP Supervisor (independent of both above)
   - **Implementation:** Role-based access control (RBAC) in ERP with preventive SoD matrix; periodic access reviews with sign-off.

#### 2. **New Vendor Master Authorization Workflow (Tiered)**
   - **Current state:** No approval required; clerk self-approved.
   - **Required control:**
     - All new vendors (regardless of projected spend) require:
       - *Tier 1:* Procurement manager approval + business justification
       - *Tier 2:* For >$50K/year: CFO approval
       - *Tier 3:* Due diligence (below)
     - Mandatory delay (e.g., 48 hours) between approval and payment eligibility
   - **System:** Workflow engine in ERP; no vendor becomes "active for payment" until approval chain complete.

#### 3. **Vendor Due Diligence (Beneficial Ownership)**
   - **Current state:** None. Home P.O. box accepted without question.
   - **Required control:**
     - All new vendors must provide:
       - W-9 or W-8BEN (signed, with valid SSN/EIN)
       - Bank account verification (ACH mandate matching on file)
       - Beneficial ownership certification (if high-risk)
     - For individuals or non-standard addresses: photo ID copy + address verification (utility bill)
   - **Red flag:** P.O. boxes, home addresses, or personal bank accounts for service vendors → escalate to CFO.

#### 4. **PO Requirement with No Threshold Bypass**
   - **Current state:** Policy allows non-PO for <$10K; clerk exploited by staying just under.
   - **Required control:**
     - **Eliminate dollar-based exemption.** Require PO for *all* service engagements, regardless of amount, prior to invoice approval.
     - PO must reference statement of work (SOW) or contract.
     - System should reject invoices without valid PO link (field-level validation).

#### 5. **Exception Monitoring & Outlier Detection**
   - **Current state:** No rules flagging patterns.
   - **Required control:**
     - Automated alerts in ERP for:
       - Multiple non-PO invoices (>2) from same vendor within 60 days
       - Invoices clustered within $500 of a policy threshold (e.g., $9,500–$10,000)
       - Vendor added and first invoice approved within 5 days
       - Non-standard payment addresses (P.O. boxes, residential)
     - Route to CFO/Audit for review before payment.

---

### B. **Detective Controls (Should Have Found It)**

#### 1. **Three-Way Invoice Matching**
   - **Current state:** No matching enforced for non-PO invoices.
   - **Required control:**
     - All invoices require match to: **PO + receipt/delivery + invoice** (3-way).
     - For "non-PO" invoices, require signed service completion certificate or manager sign-off in ERP.
     - System should block payment if match exceptions unresolved.

#### 2. **Vendor Master Change Audit Trail & Review**
   - **Current state:** Auditor sampled change log but did not correlate to subsequent payments.
   - **Required control:**
     - Monthly management review of all new vendor adds (by vendor master owner, not creator).
     - Review must compare vendor details on file (address, bank account) to first invoices and payments received.
     - Sign-off and document review; escalate mismatches.
   - **Audit sampling:** When new vendor is sampled in vendor master testing, **anchor to subsequent invoice/payment testing** (e.g., test first 5 invoices from new vendor).

#### 3. **Periodic Vendor Master Cleansing**
   - **Current state:** No cleanup or validation of existing vendors.
   - **Required control:**
     - Quarterly/semi-annual review of all vendors, especially those:
       - Unused for >6 months
       - Added recently with >$100K cumulative spend
       - With high-risk characteristics (residential address, family-named accounts, etc.)
     - Revalidate ownership, address, and business legitimacy; remove inactive records.

#### 4. **Transaction-Level Monitoring Dashboard**
   - **Current state:** No real-time red flag system.
   - **Required control:**
     - Dashboard tracking:
       - Vendors by total spend (cumulative)
       - Payment concentration (top 20 vendors = X% of spend)
       - Average invoice size by vendor
       - Invoices by approval pathway (PO vs. non-PO)
     - Flag vendors: high spend + non-PO + no contract + new.

#### 5. **External Audit Program Design**
   - **Current state:** Tested vendor master changes in isolation; did not test invoices from new vendors.
   - **Required control:**
     - Substantive audit program should:
       - Test all vendors added in period (smaller population)
       - For each new vendor, test **all invoices** (not a sample)
       - Inspect supporting documentation (contract, SOW, delivery proof)
       - Verify payee (bank account, address) to supporting evidence
     - Use data analytics to identify "outlier" invoices (just-under-threshold clustering).

---

## III. Remediation Roadmap

### **Immediate (0–30 days)**
1. **Suspend the AP clerk's access** to vendor master creation and invoice approval; conduct forensic review of all prior transactions.
2. **Halt all payments to Northern Logistics** and initiate asset recovery (contact bank, relative).
3. **Retest all 49 invoices** against contract/SOW requirements; determine if recoverable as fraud or theft.

### **Short-term (30–90 days)**
1. **Remediate SoD:** Revoke clerk's vendor master and approval rights; reassign to entry-only data-entry role with segregated approvers.
2. **Implement automated SoD matrix** in ERP with user access provisioning controls; prohibit role combinations.
3. **Vendor due diligence:** Require W-9, beneficial ownership certification, and address verification for all active vendors; flag for manual review vendors with home addresses or P.O. boxes.
4. **PO requirement:** Remove dollar-based exemption; enforce PO requirement in system configuration (invoice rejection logic).
5. **Exception monitoring:** Configure ERP alerts for:
   - Multiple non-PO invoices from same vendor
   - Transactions clustered under

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response thoroughly identifies SoD as the primary failure and addresses vendor master controls, PO threshold bypass, due diligence, and exception monitoring including threshold-clustering detection. It also proposes detailed remediation. However, it has significant gaps against the rubric's requirements for a score of 2: (1) it does not address the material-weakness analysis under AS 2201 at all — the response is cut off before reaching this critical conclusion, missing the 'severity by potential not actual loss' reasoning; (2) the ITGC periodic access review is only briefly mentioned; (3) the rolling 12-month cumulative spend trigger is touched on lightly but not framed as the cumulative-vs-single-invoice distinction; (4) the employee-vendor data match analytic (comparing vendor remit-to/bank to HR data) is not explicitly proposed, though P.O. box red flags are mentioned. The absence of any material weakness conclusion is a major rubric gap that prevents a score of 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_012 — supplier_data · medium · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: BEC defense / control rigor under social-engineering pressure_

### Question

An existing supplier with 4 years of clean history has emailed AP requesting a change to their bank account on file. The email is on company letterhead, signed by the CFO, and references the correct vendor ID and a recent invoice. What is the correct AP response? What controls apply, and why?

### Context

```
From: cfo@acmemfg-supplier.com
To:   ap@buyer.com
Subject: Bank Account Update — Vendor V-77821 Acme Manufacturing Supplier Inc

Hello AP team,

Due to a recent banking relationship change, please update our remittance information for invoice INV-2026-0847 (currently outstanding $48,200) and all future payments.

New bank details:
  Bank:           First Continental Trust, Wilmington DE
  Routing:        031176110
  Account:        7740559218

Please confirm receipt and that this change has been applied. Thank you,

Maria Velez
CFO, Acme Manufacturing Supplier Inc
```

### Rubric

- **0**: Applies the bank change based on the email, or relies solely on the email's apparent legitimacy (letterhead, signature) to authorize
- **1**: Recognizes the BEC risk and requires verification, but uses contact info from the request itself (e.g. calls the phone number on the letterhead), or omits the in-flight-payment hold, or omits maker-checker on the change application
- **2**: Rejects the email as the basis for the change, prescribes callback verification using independent contact info (NOT from the request), holds the in-flight payment until verification completes, includes maker-checker and bank-letter verification of new account, and addresses the BEC pattern explicitly

### Ideal answer

[AI DRAFT — practitioner review required] **Reject the bank change request as submitted. Do not apply the change based on the email.** This is the canonical Business Email Compromise (BEC) pattern; AP teams that comply with email-based bank change requests are the single largest source of payment fraud in the procurement function.

Why this email triggers controls regardless of how legitimate it looks:
- BEC attackers spoof letterhead, signatures, and email metadata. None of those are evidence of legitimacy.
- Attackers often time requests to coincide with a real outstanding invoice (INV-2026-0847 mentioned here) to manufacture urgency and verisimilitude.
- The 'CFO signature' is not a control — AP does not have CFO signatures on file to compare against, and even if it did, signatures are trivially forged on email attachments.

Mandatory control: **callback verification using contact information NOT obtained from the request itself.**
- Pull the supplier's phone number from the vendor master record (validated at onboarding), or from an independent source (the supplier's official website found via independent search, D&B, or the SAM.gov record if applicable).
- Do NOT use the phone number listed in the email signature, the email reply path, or any phone number on letterhead attached to the request — all of those are attacker-controlled.
- Speak to a known contact at the supplier (ideally the AR contact you've worked with before, not the CFO) and verbally confirm the bank change.
- Document the callback: who was called, at what number, what was confirmed, by whom.

Additional controls before applying the change:
1. **Maker-checker on the change.** AP clerk who receives the request cannot be the one who applies it in the system.
2. **Verify the new bank account is in the supplier's legal name** by requesting a voided check or bank letter from the new bank. (Attackers sometimes route to accounts in slightly different names — 'Acme Mfg Supplier Inc' instead of 'Acme Manufacturing Supplier Inc' — that match enough to clear casual review.)
3. **Notify the original bank-on-file** with a delay window (e.g. 3 business days) before the change goes live. If the change was unauthorized, the supplier will hear about it and can object before money moves.
4. **Hold any in-flight payment** (the $48,200 INV-2026-0847) at the OLD bank account until verification is complete. Don't pay to either bank until the verification clears.

If the request is verified: apply the change with proper documentation. If verification fails or the supplier denies sending the request: treat as confirmed BEC attempt — do not pay either account, escalate to information security and the supplier's legitimate management contact, and consider whether to file an IC3 report (FBI Internet Crime Complaint Center).

References: FBI Public Service Announcement on BEC (multiple updates 2019-2023); NIST SP 800-181 (controls); typical SOX P2P control mapping for vendor master changes.

### Model response

# Analysis: Bank Account Change Request

## The Correct AP Response: **REJECT this request and verify through independent channels**

Despite the apparent legitimacy markers, this email exhibits classic **Business Email Compromise (BEC)** or payment fraud characteristics. The correct response is a controlled verification process, not immediate approval.

## Critical Controls That Apply

### 1. **Segregation of Duties (SOD)**
- The CFO should NOT initiate banking changes via email to AP
- Finance policy should require:
  - Written request on official letterhead submitted through secure channels
  - Independent verification by accounting management
  - Treasury/Finance controller approval (not just CFO request)

### 2. **Dual Verification Requirement**
Contact the supplier **using independently verified contact information**:
- Call the phone number from previous correspondence or official vendor file
- Request confirmation from a different signatory/authorized person
- Never use contact details provided in the suspicious email
- Verify through LinkedIn, company website, or recent business dealings

### 3. **Change Management Control**
- **Who approves?** Controller or Treasurer (not AP staff alone)
- **Documentation required:** Signed form with original authorization, not email
- **Audit trail:** Maintain proof of verification
- **Waiting period:** Consider 2-3 day holding period before processing large payments

### 4. **Payment Control Review**
- Flag for review: First change in 4 years + immediate large payment outstanding
- Verify invoice INV-2026-0847 legitimacy independently
- Consider delaying this specific payment pending verification

## Red Flags Present

| Flag | Risk Level | Why |
|------|-----------|-----|
| Email-only request | **HIGH** | BEC hallmark |
| Urgent implicit framing | **MEDIUM** | Creates pressure to skip controls |
| Large outstanding amount | **MEDIUM** | High fraud payoff |
| Routing/account format suspicious | **MEDIUM** | Generic bank name; verify routing number legitimacy |
| "Recent change" justification | **MEDIUM** | Common pretext |

## Recommended AP Response Template

```
Dear Maria,

Thank you for notifying us of the banking relationship change. Per our 
internal controls policy, we require independent verification of all 
bank account changes.

I will contact your office at [independently verified number] to 
confirm this request with an authorized signatory.

We will process the update once verification is complete.

Best regards,
AP Department
```

## Why This Matters

- **Fraud frequency:** BEC targeting accounts payable is among the highest-loss fraud categories (FBI reported $43B+ in losses 2013-2021)
- **Credential compromise:** Attacker may have accessed email but not full banking authority
- **Reversibility:** Wire frauds are extremely difficult to recover once sent

**The 4-year clean history actually increases risk**: fraudsters invest time building trust before the exploit.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly rejects the email-based change and requires independent callback verification using contact info NOT from the email — a strong core. It mentions delaying the specific payment ('Consider delaying') and includes some segregation of duties. However, it falls short of a 2: it does not explicitly require a maker-checker control on the change application itself (separating who receives from who applies in the vendor master), it does not require a voided check or bank letter to verify the new account is in the supplier's legal name, and the in-flight payment hold is framed as 'consider' rather than mandatory hold at the OLD bank. It also doesn't mention notifying the original bank-on-file. These are key elements the rubric requires for a 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_013 — trade_and_tax · medium · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: applying domain conventions (post-Brexit UK B2B place-of-supply)_

### Question

A UK-incorporated software supplier has invoiced a US buyer for an annual SaaS subscription and added 20% UK VAT to the invoice. The buyer has no UK presence and no UK VAT registration. Is the VAT correctly charged? Reason from post-Brexit UK B2B place-of-supply rules. What should AP do?

### Context

```
Invoice (issued in GBP):
  Supplier:   Cumberland Software Ltd, London UK
                VAT registration: GB287654321
  Buyer:      [US buyer, no UK establishment, no UK VAT registration]
  Service:    Annual SaaS subscription, 'CumberlandHR' enterprise tier
  Period:     12 months, current period
  Net fee:    £24,000.00
  UK VAT 20%:  £4,800.00
  Total:      £28,800.00

Supplier note on invoice: 'VAT charged per UK VAT Act 1994 as amended.'
```

### Rubric

- **0**: Accepts the VAT as correctly charged, or treats this as a reverse-charge scenario between UK and US, or claims the VAT is reclaimable through some standard mechanism
- **1**: Recognizes that VAT should not have been charged but reasons via reverse charge instead of out-of-scope, OR fails to cite the place-of-supply rule (Sch 4A para 16 / VAT Notice 741A), OR mishandles the reclaim discussion
- **2**: Correctly identifies the place of supply as the US under UK B2B rules, distinguishes out-of-scope from reverse charge, recommends rejection and corrected invoice, addresses why reclaim is not the right path, and references the relevant UK VAT Act provision and HMRC guidance

### Ideal answer

[AI DRAFT — practitioner review required] **The VAT is incorrectly charged.** Under post-Brexit UK B2B place-of-supply rules for digital and consultancy services, the place of supply is the **customer's location**, not the supplier's. With the customer in the US (no UK establishment), the supply is **outside the scope of UK VAT**. The supplier should not have charged the £4,800 VAT.

Reasoning:
- The UK VAT Act 1994 Schedule 4A para 16 (and the implementing rules in HMRC VAT Notice 741A) sets the place of supply for B2B services received by a non-UK customer as the customer's country.
- For digital/electronically-supplied services (SaaS qualifies as a 'use and enjoyment' of digital services), the same place-of-supply rule applies post-Brexit: customer's country.
- The customer here is US-established. US is outside the UK and outside the EU. The supply is outside the scope of UK VAT — the supplier should issue the invoice without VAT and note 'Outside scope of UK VAT — place of supply outside UK per VAT Act 1994 Sch 4A para 16.'

This is distinct from the EU reverse-charge mechanism. Reverse charge applies between two EU VAT-registered parties when the place of supply shifts to the customer; the customer self-accounts. The US-recipient case here is not reverse charge — it's simply out of scope. There is no UK VAT liability for either party on this transaction.

AP action:
1. Reject the invoice. Email the supplier explaining that the place of supply for this SaaS service is the US (the customer's country) under UK VAT Act 1994 Sch 4A para 16, and that the supply is outside the scope of UK VAT.
2. Provide written confirmation that the buyer has no UK establishment and is not UK VAT-registered. The supplier needs this for their own VAT records to support the zero-VAT treatment.
3. Request a corrected invoice for £24,000 net, no VAT, with a note 'Outside scope of UK VAT — customer outside UK per Sch 4A para 16.'
4. Reclaimability: not applicable. The £4,800 is not VAT properly due, and a US buyer with no UK VAT registration has no UK return to reclaim on. The 13th Directive equivalent (UK VAT refund scheme for non-UK businesses) is theoretically available but practically slow and only refunds VAT properly charged on certain expenses — not VAT erroneously charged on out-of-scope supplies. The right path is to fix the invoice, not to reclaim.

If the supplier refuses to credit and reissue: the buyer could pay the £24,000 net amount only and let the supplier dispute, but that creates a contractual issue. Better to escalate to the supplier's tax / finance team rather than accepting the invoice as-billed and writing off £4,800.

Note: the answer would change if the buyer had a UK VAT registration that was the actual recipient of the service (e.g. a UK branch that uses the SaaS). In that case, place of supply could be the UK and the VAT would be properly charged and reclaimable. This fact pattern explicitly excludes that.

References: UK VAT Act 1994 Schedule 4A para 16; HMRC VAT Notice 741A 'Place of supply of services'; HMRC guidance on Brexit transition for B2B services.

### Model response

# VAT Treatment Analysis: UK SaaS Supply to US B2B Customer

## Correct Answer: VAT is **incorrectly charged** and should be **removed**

---

## Reasoning: Post-Brexit B2B Place-of-Supply Rules

### 1. **Applicable Rule: MOSS/OSS Reverse Charge**

Post-Brexit (from 1 January 2021), the UK adopted the **One-Stop Shop (OSS) regime** for B2B digital services. The key principle:

**Place of supply of B2B digital services = location of the customer's establishment** (not the supplier's location)

### 2. **Application to This Scenario**

- **Supplier:** Cumberland Software Ltd (UK-established)
- **Customer:** US buyer (established outside UK/EU)
- **Service type:** SaaS (classified as "electronically supplied service")

**Critical point:** When the customer is established outside the UK, the supply is **outside the scope of UK VAT**.

### 3. **Relevant Legislative Framework**

- **VATA 1994, Schedule 5, paragraph 2(k)** (as amended post-Brexit)
- **VAT Notice 741D (Digital Services)** – HMRC guidance

The supply qualifies for **zero-rating or exemption from UK VAT** because:
- The customer has no UK establishment
- The supply is not made to a UK consumer
- The supply does not constitute a UK domestic B2B transaction

### 4. **What *Should* Have Happened**

The supplier should have:

| Action | Reason |
|--------|--------|
| **Not charged UK VAT** | Customer established outside UK scope |
| **Obtained customer's tax status confirmation** | To verify non-UK establishment (e.g., US tax ID, business registration) |
| **Applied reverse charge** | Under B2B digital services rules, VAT is the customer's responsibility in their own jurisdiction |

---

## Accounts Payable (AP) Actions

### **Immediate Steps:**

1. **Request VAT adjustment/credit note** from Cumberland Software Ltd
   - Cite: Post-Brexit OSS rules; customer is US-established; supply outside UK VAT scope
   - Request revised invoice showing £0 VAT

2. **Document the customer's tax status**
   - Provide US tax identification (EIN or equivalent)
   - Confirm no UK VAT registration or establishment

3. **Do NOT pay the invoiced VAT amount**
   - The £4,800 should be removed
   - Pay only the £24,000 net fee

4. **Record corrective entry** (when credit note received):
   - Debit: VAT/Tax paid (if initially recorded)
   - Credit: Accounts Payable

### **If Supplier Refuses:**

- Escalate to supplier's finance/legal team with HMRC guidance reference
- Consider reporting to HMRC if intentional mischarge is suspected
- Document all communication for audit trail

---

## Summary

**The VAT is incorrectly charged** under post-Brexit B2B place-of-supply rules. The supply is **outside the scope of UK VAT** because the customer is established in the US. AP should request removal of the £4,800 VAT charge and pay only £24,000.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The candidate correctly identifies that VAT should not have been charged and that the supply is outside the scope of UK VAT due to the US customer location. However, it conflates the situation with reverse charge ('Applied reverse charge' in the table, MOSS/OSS framing), which the ideal answer explicitly distinguishes from out-of-scope treatment. It also cites incorrect legislative references (Schedule 5 para 2(k) and VAT Notice 741D) rather than the correct Schedule 4A para 16 and VAT Notice 741A. It does not address reclaimability. These issues match the rubric's level 1 criteria (reasons via reverse charge instead of out-of-scope, fails to cite correct place-of-supply rule).

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_014 — trade_and_tax · medium · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: applying domain conventions (Canadian GST/HST place-of-supply for exported services)_

### Question

A Canadian supplier has invoiced a US buyer for consulting services. The invoice charges 13% Ontario HST. The services were performed by a Toronto-based consultant who travelled to the buyer's New York office for two on-site weeks; the remaining work was performed remotely from Toronto. Is the HST correctly charged? What should AP do?

### Context

```
Invoice (issued in CAD):
  Supplier:   Northbridge Consulting Group Inc, Toronto ON
                GST/HST registration: 879214687 RT0001
  Buyer:      [US buyer, no Canadian presence, no Canadian GST/HST registration]
  Service:    Strategy consulting, 6-week engagement
              - 2 weeks on-site at buyer's New York office
              - 4 weeks remote work from Toronto
  Net fee:           CAD 75,000.00
  Ontario HST 13%:   CAD 9,750.00
  Total:             CAD 84,750.00

Supplier note: 'HST charged per Ontario rate as work originated from our Toronto office.'
```

### Rubric

- **0**: Accepts the HST as correctly charged, or applies the supplier's 'work originated in Toronto' reasoning, or claims reclaimability via a standard mechanism
- **1**: Recognizes the HST should not have been charged but misses the zero-rated-export framing (treats it as out-of-scope or reverse-charge), OR fails to cite Excise Tax Act Schedule VI Part V, OR mishandles the on-site-vs-remote split (e.g. argues the on-site portion should be subject to HST)
- **2**: Correctly identifies the supply as a zero-rated exported service under Schedule VI Part V section 7, addresses why the supplier's office-of-origin reasoning is wrong, addresses the on-site vs remote split correctly (it strengthens not weakens the zero-rating), prescribes rejection and corrected invoice, and addresses the reclaim impossibility

### Ideal answer

[AI DRAFT — practitioner review required] **The HST is incorrectly charged.** Under Canadian GST/HST place-of-supply rules for B2B services, the place of supply for services performed for a non-resident customer with no permanent establishment in Canada is generally **outside Canada — zero-rated** (technically, an exported service under the Excise Tax Act). The supplier's reasoning ('work originated from Toronto') is the wrong test; the place of supply for services is determined by the customer's location and where the service is consumed, not the supplier's office location.

Reasoning:
- Excise Tax Act (Canada) Schedule VI Part V section 7 and section 23 zero-rate exported services to non-residents under specified conditions: the customer is not a resident of Canada, the service is not consumed in Canada, and the service is not in respect of real property or tangible personal property situated in Canada.
- All three conditions are met here: the customer is US-resident, the deliverable is consumed in the US (the consulting work serves the US buyer's strategic decisions), and the engagement is not real-property-related.
- The 2 weeks on-site in New York actually strengthens the zero-rating argument — the work is physically being performed in the US during that period. The 4 weeks of remote work from Toronto does not change this; the place of consumption is the customer's US location.
- Under Schedule VI Part V section 7, the supplier should zero-rate the supply (charge 0% HST) and document the customer's non-resident status for their own GST/HST records. The supplier remains entitled to claim ITCs (Input Tax Credits) on inputs used to provide the service even though the output is zero-rated.

AP action:
1. Reject the HST line. Email the supplier explaining that under Schedule VI Part V section 7 of the Excise Tax Act, the supply is zero-rated as an exported service to a non-resident.
2. Provide written confirmation of non-residency: the buyer is a US-incorporated entity with no permanent establishment in Canada and no Canadian GST/HST registration.
3. Request a corrected invoice for CAD 75,000 net, 0% HST.
4. Reclaimability: not available to the US buyer. Canada does not have a 13th-Directive-equivalent refund scheme for non-resident businesses on erroneously-charged HST. The right path is correction of the invoice, not reclaim.

Distinct fact patterns where HST WOULD be correctly charged:
- If the customer had a Canadian permanent establishment using the service (HST charged, reclaimable on Canadian return).
- If the service related to real property situated in Canada (HST always charged regardless of customer residency).
- If the service was consumed primarily in Canada (e.g. consulting on a Canadian regulatory filing).

None of those apply here.

References: Excise Tax Act (Canada) Schedule VI Part V sections 7 and 23; CRA GST/HST Memorandum 4.5.3 'Exports — Services and Intellectual Property'; CRA guidance on place of supply for services.

### Model response

# Analysis: HST Applicability to Cross-Border Consulting Services

## The Issue
The supplier has incorrectly applied HST to this invoice. The charging rationale ("work originated from our Toronto office") is not the correct test under Canadian tax law.

## Correct Tax Treatment

### GST/HST Rules for Cross-Border Services
Under the **GST/HST Act (Part IX of the Excise Tax Act)**, the place of supply for services is determined by **where the recipient uses or intends to use the service**, not where it originates.

**Key provision:** For most B2B services to non-resident purchasers:
- If the recipient is a non-resident without a permanent establishment in Canada
- And the service is performed for use **outside Canada**
- The supply is **zero-rated (0% GST/HST)**

### Application to This Engagement

**On-site services (2 weeks in New York):**
- Clearly performed outside Canada
- Zero-rated

**Remote services (4 weeks from Toronto):**
- The service is consumed by a US-based buyer with no Canadian presence
- The buyer's intended use of the consulting work is **in the US** (presumably to benefit their US operations)
- Should also be **zero-rated**

**Result:** The entire CAD 75,000 service fee should be zero-rated. HST of CAD 9,750 should **not be charged**.

---

## What AP Should Do

1. **Contact the supplier immediately** and request a corrected invoice showing:
   - Net fee: CAD 75,000.00
   - HST: CAD 0.00
   - Total: CAD 75,000.00

2. **Document the correction** by noting:
   - Buyer is a non-resident US entity
   - No Canadian GST/HST registration
   - No Canadian permanent establishment
   - Services intended for use outside Canada

3. **Request CRA documentation** (if available):
   - Ask if the supplier holds a CRA ruling confirming zero-rating eligibility
   - Or obtain written confirmation the supplier understands the zero-rating rule

4. **Verify compliance** in your records to ensure:
   - Payment reflects the corrected amount (CAD 75,000)
   - No HST input tax credit is claimed on the overpaid amount
   - Documentation supports the zero-rating position

---

## Summary
**The HST is incorrectly charged.** The invoice should be zero-rated, reducing the total to CAD 75,000. Request immediate correction.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies that HST should not be charged, correctly rebuts the supplier's 'office of origin' reasoning, correctly handles the on-site/remote split (both zero-rated), and prescribes rejection with a corrected invoice. However, it fails to cite Schedule VI Part V section 7 specifically — it only references 'Part IX of the Excise Tax Act' generally, which is the GST imposition section, not the zero-rating schedule. It also does not address the reclaim impossibility for the US buyer. Per the rubric, missing the Schedule VI Part V citation drops it to a 1.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_015 — trade_and_tax · hard · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: multi-step trade compliance reasoning (HTS classification + Section 301 + importer-of-record responsibility)_

### Question

A Chinese supplier invoices a US buyer for $180,000 of microcontroller chips (HTS classification 8541.59.00). The supplier did not include any Section 301 tariff line on the invoice. The buyer's customs broker has not yet filed entry. What does AP need to verify, what cost is the buyer's vs. supplier's, and what specific control steps apply?

### Context

```
Purchase order PO-94427:
  Supplier:   Shenzhen Lianxin Microelectronics Ltd, China
  Goods:      24,000 microcontrollers, HTS 8541.59.00 (per supplier's commercial invoice)
  Country of origin: China
  Incoterms:  FOB Shenzhen (Incoterms 2020)
  PO value:   $180,000.00

Supplier commercial invoice:
  Goods:      $180,000.00
  Freight:    $0 (FOB — buyer arranges)
  Total:      $180,000.00
  No tariff or duty line

Buyer's customs broker has the entry queued but has not yet filed.

Known context: HTS 8541.59.00 covers semiconductor devices; some sub-classifications are subject to Section 301 List 3 tariffs (currently 25% as of recent rate schedules) and additional Section 301 List 4A tariffs depending on classification.
```

### Rubric

- **0**: Treats the missing tariff as a supplier-invoice error or asks the supplier to add it, OR fails to identify the importer's classification responsibility, OR ignores Section 301
- **1**: Identifies that Section 301 tariffs are the buyer's cost and not the supplier's, but misses the importer-classification-responsibility duty (19 U.S.C. §1484), OR misses the HTS classification challenge (8541 vs 8542 distinction), OR omits country-of-origin / First Sale / FTZ considerations entirely
- **2**: Identifies tariff payment responsibility correctly, prescribes independent HTS classification review citing importer's §1484 duty of reasonable care, raises the 8541 vs 8542 sub-classification question, addresses country of origin / First Sale / FTZ / drawback as relevant control steps, and structures the response as a control-and-documentation workflow not just a tariff calculation

### Ideal answer

[AI DRAFT — practitioner review required] **The supplier invoice is correct as billed under FOB Incoterms — Section 301 tariffs are the buyer's cost, paid to US Customs and Border Protection (CBP) at entry, not paid to the supplier.** The absence of a tariff line on the supplier invoice is correct, not an error.

What AP needs to verify (and what's actually critical):

1. **HTS classification validation — independent of the supplier's claim.** The supplier wrote 8541.59.00 on their commercial invoice, but **the importer of record (the buyer) is legally responsible for accurate classification under 19 U.S.C. §1484 — 'reasonable care' standard.** Suppliers routinely misclassify either by error or to evade tariffs. AP/compliance should confirm classification with the customs broker before entry filing. A broker working from the supplier's stated HTS without independent review is providing a service, not an opinion. Validation steps:
   - Review the actual product specs against the HTS classification rules (USITC Harmonized Tariff Schedule).
   - For semiconductor devices, distinguish between 8541.59.00 (other diodes/transistors), 8542.31.00 (electronic integrated circuits — processors/controllers, often duty-free), and other 8541/8542 sub-classifications. The product description 'microcontroller' would more typically classify under 8542.31 (processors) than 8541.59 (transistors). **A misclassification at 8541 vs 8542 changes the duty exposure dramatically** — 8542.31.00 has historically been duty-free at MFN rate, while 8541.59 has a small MFN duty plus potentially Section 301 if the underlying product is China-origin and on the relevant list.

2. **Country of origin verification.** Section 301 applies to goods *of Chinese origin*. The supplier is in China but the goods could be assembled in China from components sourced elsewhere. Country of origin under 19 CFR §134 is determined by substantial transformation — where the article was last substantially transformed. This usually doesn't move the analysis (China for a Chinese-supplier-to-China-shipment) but it's worth confirming, especially if the chip is actually a Taiwanese or Korean die packaged in China.

3. **Section 301 tariff applicability.** Once HTS and origin are confirmed, check the current Section 301 list status for that exact HTS at the time of entry:
   - List 3 (25%) and List 4A (7.5%) are the most common applicable lists for electronics.
   - Some HTS codes were excluded or had exclusions that expired/were renewed. The USTR exclusion process is dynamic.
   - If 8541.59.00 is on the list at entry date (likely), Section 301 duty = $180,000 × applicable rate. At 25% List 3, that's $45,000.
   - Plus normal MFN duty (small for this HTS, often <2%).
   - Plus Merchandise Processing Fee (MPF, 0.3464% capped) and Harbor Maintenance Fee (HMF, 0.125%) for ocean shipments.

4. **First Sale rule consideration.** If the goods passed through a middleman (Hong Kong trading company → US buyer), First Sale for Export valuation might allow declaring the original factory price rather than the middleman price for duty purposes — savings can be material. Requires documentation chain.

5. **Foreign Trade Zone (FTZ) opportunity** if the buyer operates one — defer or eliminate Section 301 if goods are processed/re-exported.

6. **Drawback opportunity** if the goods are re-exported within 5 years — duty paid at entry is recoverable.

What AP / the broker SHOULDN'T do:
- Don't ask the supplier to add the Section 301 amount to their invoice. The supplier doesn't pay this; CBP collects it from the importer at entry.
- Don't rely on the supplier's stated HTS as authoritative.
- Don't file entry without confirming current Section 301 status at the actual entry date — list status changes.

Control steps:
- Document the independent HTS classification review (who, when, basis).
- Document Section 301 status verification at entry date.
- Reconcile broker entry summary (CBP Form 7501) against expectations: declared HTS, declared origin, declared value, calculated duties.
- Capture any First Sale or FTZ election in the broker file.
- Annual review of HTS/origin classifications for recurring vendors.

References: 19 U.S.C. §1484 (importer reasonable care); 19 CFR §134 (country of origin); USTR Section 301 actions and exclusion lists; USITC Harmonized Tariff Schedule; CBP guidance on First Sale for Export.

### Model response

# Analysis: Section 301 Tariff Implications for PO-94427

## What AP Needs to Verify

### 1. **Precise HTS Sub-classification**
- **8541.59.00 is broad.** AP must work with the customs broker to confirm the *exact* sub-classification of these microcontrollers
- Determine whether the specific chips fall under:
  - **Section 301 List 3** (25% additional duty)
  - **Section 301 List 4A** (additional percentage TBD by current rate schedule)
  - **Neither list** (standard tariff only applies)
- This requires technical specifications: chip type, capacity, functionality, country-specific design origin

### 2. **Country of Origin Confirmation**
- Verify that China is truly the country of origin (not transshipment through China)
- Confirm no qualifying inputs from trade agreement countries (USMCA, etc.)

### 3. **Cost/Price Verification**
- Confirm the $180,000 invoice reflects actual transaction value (not undervaluation)
- Verify no hidden costs are embedded elsewhere in the supply chain

---

## Cost Allocation: Buyer vs. Supplier

| **Cost Element** | **Responsibility** | **Rationale** |
|---|---|---|
| **Goods: $180,000** | **Supplier's invoice** | Reflects goods price per commercial invoice |
| **Standard tariff (HTS 8541.59.00)** | **Buyer's responsibility** | Duty obligation falls on importer of record |
| **Section 301 List 3 (25%)** | **Buyer's responsibility** | Applied at U.S. border; supplier did not invoice it |
| **Section 301 List 4A (if applicable)** | **Buyer's responsibility** | Applied at U.S. border; supplier did not invoice it |
| **Freight (FOB Shenzhen)** | **Buyer arranges & pays** | Explicitly stated in Incoterms 2020 FOB term |
| **Customs brokerage fees** | **Buyer's responsibility** | Standard import service cost |

**Key Point:** The supplier's invoice is *ex-duties*. Section 301 tariffs are **imposed by U.S. customs law** and are the buyer's cost, not something the supplier should have pre-invoiced.

---

## Specific Control Steps AP Should Implement

### **Before Entry Filing (Immediate)**

1. **Halt the broker's entry filing** until sub-classification is confirmed
   - Request technical data sheet or detailed product specifications from supplier
   - Provide specs to customs broker for definitive HTS classification

2. **Calculate total landed cost scenarios:**
   - Scenario A: Standard duty only (baseline)
   - Scenario B: Standard duty + List 3 (25%)
   - Scenario C: Standard duty + List 3 + List 4A
   - Present cost impact analysis to procurement/finance

3. **Evaluate supply chain alternatives:**
   - Can this component be sourced from non-List 3/4A countries?
   - Are there qualifying USMCA suppliers?
   - Cost-benefit: higher unit price vs. tariff savings?

### **At Entry Filing**

4. **Ensure broker has complete information:**
   - Provide accurate HTS classification (confirmed)
   - Confirm origin as China
   - Flag that Section 301 tariffs *will apply* (do not leave blank)

5. **Entry documentation must show:**
   - Goods value: $180,000
   - Applicable tariff line with duty rate
   - Section 301 duty line with applicable rate(s)

### **After Entry**

6. **Post-import audit:**
   - Verify duties paid match the HTS classification confirmed
   - Keep customs broker correspondence on file (classification basis)
   - Monitor for future tariff rate changes

7. **Accrual in accounting:**
   - Cost of goods should include: $180,000 (goods) + standard tariff + Section 301 tariff
   - Flag any variance from budgeted rates

---

## Risk Flags

⚠️ **Supplier did not list tariff on invoice** — This is common (supplier may not track U.S. tariff), but AP should confirm supplier understands buyer (importer of record) bears duty cost.

⚠️ **Section 301 rates are fluid** — Confirm current rates before filing; rates have changed within the 301 program.

⚠️ **Misclassification penalty** — If wrong HTS is filed, customs can assess penalties. Classification certainty is critical.

---

## Summary Table: Who Pays What

| **Cost** | **Payer** | **Timing** |
|---|---|---|
| Microcontrollers | Buyer (paid supplier $180K) | Already incurred |
| Standard HTS tariff | Buyer | At customs entry |
| Section 301 duties | Buyer | At customs entry |
| Freight & insurance | Buyer | Before/at entry |
| Brokerage | Buyer | At/after entry |

**Total landed cost ≈ $180,000 + tariffs + freight + brokerage.**

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies that Section 301 tariffs are the buyer's responsibility paid to CBP, not the supplier, and that the supplier invoice is correct as-is. It addresses HTS sub-classification verification, country of origin, and provides a control workflow. However, it misses key elements required for a score of 2: (1) it does not cite or invoke the importer's reasonable care duty under 19 U.S.C. §1484, (2) it does not raise the critical 8541 vs 8542 sub-classification question (microcontrollers more likely belong under 8542.31 as integrated circuits, which would dramatically change duty exposure), and (3) it omits First Sale for Export, FTZ, and drawback considerations entirely. It treats classification validation generically rather than challenging the supplier's stated HTS on technical grounds.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_016 — invoice_processing · easy · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: applying domain conventions (stock-flow accounting principle)_

### Question

Accounts Payable Days (also called Days Payables Outstanding, DPO) is computed using the AVERAGE accounts-payable balance over the period rather than the ending balance. Why? What problem does the averaging convention solve, and what would go wrong if a junior analyst used the ending AP balance instead?

### Rubric

- **0**: Says ending AP is correct, OR fails to identify the stock/flow distinction, OR gives a definition without explaining the averaging convention
- **1**: Identifies that average AP is correct but does not articulate the stock/flow consistency reasoning, OR misses the end-of-period-anomaly distortion, OR gives the formula without the principle
- **2**: Articulates the stock/flow consistency principle as the underlying reason, identifies end-of-period anomalies as the concrete distortion that averaging solves, addresses comparability across firms, and references the canonical formula with the average-AP convention

### Ideal answer

[AI DRAFT — practitioner review required] DPO uses the AVERAGE accounts-payable balance because it reconciles a stock measure (AP, a balance-sheet item that exists as a snapshot) with a flow measure (purchases or COGS, an income-statement item that accumulates over a period). The averaging convention converts the stock measure into something comparable to the flow measure by representing the typical AP level throughout the period rather than a single point-in-time snapshot.

What goes wrong with ending AP:

1. **End-of-period anomalies distort the metric.** A company that pushes invoices out the door in the last week of the year (to compress AP for working-capital reporting) or holds invoices in the last week (to stretch DPO) will produce an ending balance that does not reflect typical operations. Average AP smooths these end-effects.

2. **Consistency between numerator and denominator.** Purchases or COGS is an over-the-period number. If the denominator covers the full period, the numerator should represent the period too — average AP does that; ending AP doesn't.

3. **Comparability across companies.** Different firms close their books on different cycles; ending AP varies systematically with fiscal calendar. Averaged AP is more comparable.

4. **Audit defensibility.** Stock/flow consistency is a documented accounting principle (Holthausen & Zmijewski 2014). Using ending AP without disclosure invites a sourcing-quality challenge during diligence.

The canonical formula is therefore: DPO = (Average AP / Purchases) × N, where 'Average AP' is typically (Beginning AP + Ending AP) / 2 for annual analysis or a more granular average (monthly average) for shorter-period analysis. Some firms use COGS in the denominator instead of Purchases as a practical proxy when Purchases isn't disclosed; the stock/flow consistency principle still requires averaging.

### Model response

# Accounts Payable Days (DPO): Why Averaging Matters

## The Core Principle

DPO measures the *average length of time* a company takes to pay its suppliers. Using an average AP balance ensures the metric reflects the typical payment cycle throughout the period, not a snapshot that may be unrepresentative.

## Problems Solved by Averaging

### 1. **Seasonality and Timing Distortions**
Ending balances are highly vulnerable to when they're measured:
- A retailer's AP on December 31 might be artificially inflated (post-holiday inventory purchases, pre-payment)
- A retailer's AP on January 31 might be artificially depressed (post-holiday payment cycle complete)
- A single snapshot misses the actual operational reality

### 2. **Year-End Management Manipulation**
Companies may intentionally manipulate period-end balances:
- Accelerate payables to improve cash position before period-end
- Delay payment timing specifically to inflate AP at fiscal year-end
- Averaging dampens the impact of these tactical decisions

### 3. **One-Time or Extraordinary Events**
Ending balances can reflect non-recurring circumstances:
- A major acquisition might spike payables temporarily
- A supply-chain disruption might create unusual payment deferrals
- Averaging smooths over these anomalies

## What Goes Wrong With Ending Balance

Using only the ending AP balance creates specific analytical failures:

| Problem | Impact on DPO |
|---------|---------------|
| **Overstates DPO** if year-end AP was unusually high | Suggests company pays slower than reality |
| **Understates DPO** if year-end AP was unusually low | Suggests company pays faster than reality |
| **Reduces comparability** across periods | Makes trend analysis unreliable |
| **Enables seasonality gaming** | Quarter-to-quarter comparisons become distorted |

### Concrete Example
- Company with typical AP of $10M but ends period with $15M (exceptional timing)
- Using $15M ending balance overstates DPO by 50%
- Average of $10M correctly reflects actual payment behavior

## Best Practice

**Calculate DPO as:**
$$\text{DPO} = \frac{\text{Average Accounts Payable}}{\text{COGS}} \times \text{Days in Period}$$

Where Average AP = (Beginning AP + Ending AP) ÷ 2

This is consistent with how analysts calculate Days Inventory Outstanding (DIO) and Days Sales Outstanding (DSO)—all three use averages to create comparable working capital metrics across periods and companies.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response identifies that average AP is correct and addresses end-of-period anomalies (manipulation, seasonality, one-time events) well. It also touches on comparability and provides the canonical formula. However, it does not explicitly articulate the stock/flow consistency principle—the fundamental reason that AP is a balance-sheet stock measure that must be reconciled with an income-statement flow measure (COGS/Purchases). This is the core conceptual reasoning the rubric requires for a 2, and the response treats averaging more as a smoothing technique than as a stock/flow reconciliation principle.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_017 — invoice_processing · medium · **score 1/2** (model: `claude-haiku-4-5`)

_Expected failure mode: domain conventions (P2P control taxonomy)_

### Question

Explain the difference between a 'duplicate vendor record' and a 'duplicate payment.' Both are control concerns and both can result in improper cash outflows, but they are caught by different control regimes. What's the distinction, and why is it operationally important to keep the two regimes separate?

### Rubric

- **0**: Treats the two as the same concept, OR fails to distinguish master-data from transaction-stream controls, OR provides only one regime's controls without the other
- **1**: Distinguishes the two phenomena but does not articulate the different control regimes, OR misses the bridge-case (duplicate payment across two duplicate vendor records), OR addresses only one of the operational-importance reasons
- **2**: Cleanly distinguishes master-data hygiene from transaction-stream control, names specific controls in each regime, identifies the bridge case (cross-vendor-ID matching), and addresses at least two of: ownership separation, audit-evidence separation, remediation-path differences

### Ideal answer

[AI DRAFT — practitioner review required] **Duplicate vendor record** = the same legal entity appears twice (or more) in the supplier master under distinct vendor IDs. The records may have variant names, slightly different addresses, possibly different bank accounts. The legal entity is one; the master-data representation is multiple.

**Duplicate payment** = the same invoice (same supplier, same invoice number, same amount, same period) gets paid more than once. Could happen against a single vendor record (e.g., supplier resubmits the invoice with a slight number variation and AP doesn't catch the match) or across two duplicate vendor records (the harder case to detect).

The two are categorically distinct because they sit on different sides of the P2P process and are caught by different controls:

**Duplicate vendor record** is a master-data hygiene issue. Caught by:
- Periodic vendor-master cleansing routines
- TIN-based dedupe analytics (anchor on TIN, surface variant names)
- Maker-checker on new vendor adds
- Employee-vendor match analytics (employee data crossed against vendor data)
This regime operates BEFORE invoices are entered. It's a preventive control on the master data.

**Duplicate payment** is a transaction-stream issue. Caught by:
- (Vendor + invoice number) exact match at invoice entry
- (Vendor + amount + date within window) fuzzy match
- Cross-vendor amount + PO match (catches duplicates across two duplicate vendor records — the bridge case)
- Reverse-amount matching (catches re-billing after a credit memo)
This regime operates AT invoice entry and is a detective/preventive control on the transaction.

**Why the distinction is operationally important:**

1. **Different ownership.** Master-data hygiene typically sits with a procurement-ops or master-data steward team. Duplicate-payment monitoring sits with AP. Conflating the two leads to ownership confusion and gap.

2. **Different audit evidence.** SOX P2P walkthroughs sample the two regimes separately. A vendor-master walkthrough samples vendor adds; a duplicate-payment walkthrough samples payment runs. Auditors expect distinct evidence trails.

3. **Different remediation paths.** A duplicate vendor record gets fixed by consolidation (with the multi-step pre-merge control sweep — see q_001). A duplicate payment gets fixed by recovery (vendor refund, contra-payable, or write-off if uncollectible).

4. **The bridge case is where both regimes matter.** When a duplicate payment occurs ACROSS two duplicate vendor records, it would have been prevented if the master-data regime had caught the duplicate vendor first. This is why duplicate-payment monitoring should include cross-vendor-ID amount matching as a backstop to master-data hygiene gaps.

Keeping the two distinct in the controls framework, in the audit workpapers, and in role assignments ensures both gaps get coverage rather than each assuming the other will catch it.

### Model response

# Duplicate Vendor Record vs. Duplicate Payment: A Critical Distinction

## Core Definitions

**Duplicate Vendor Record**: Two or more master file entries for the same actual vendor (same entity, different master records)

**Duplicate Payment**: A single vendor record is paid twice for the same invoice or obligation (same obligation, multiple disbursements)

## Key Operational Differences

| Aspect | Duplicate Vendor Record | Duplicate Payment |
|--------|------------------------|-------------------|
| **Root Cause** | Data entry error, merger/acquisition, inadequate deduplication | System glitch, processing error, human mistake in payment cycle |
| **When Detected** | During vendor master file maintenance | During payment processing or reconciliation |
| **Scope of Risk** | All future transactions with that vendor | Single transaction or invoice |
| **Correction Complexity** | Requires consolidation; touches historical records | Requires reversal/credit memo |

## Control Regime Implications

### Duplicate Vendor Record Controls
- **Ownership**: Accounts Payable/Procurement
- **Mechanisms**: 
  - Tax ID matching before master file approval
  - Periodic duplicate analysis (vendor name fuzzy matching)
  - Single approval gate for vendor creation
  - Hierarchical vendor hierarchies to prevent parent/subsidiary confusion

### Duplicate Payment Controls
- **Ownership**: Treasury/Disbursements and Accounts Payable
- **Mechanisms**:
  - Invoice number matching (three-way match: PO-receipt-invoice)
  - Positive pay programs (payment approval flags)
  - Reconciliation of payments to invoice register
  - Exception reporting for unusual vendor payment patterns

## Why Separation Matters Operationally

**1. Prevention vs. Detection**
- Vendor record controls are *preventive* (stop bad data entering the system)
- Payment controls are *detective* (catch errors before cash leaves)

**2. Organizational Accountability**
- Vendor master maintenance is a one-time procurement responsibility
- Payment processing is continuous and owned by finance/treasury—mixing accountability dilutes oversight

**3. System Architecture**
- Duplicate vendor controls typically sit in the ERP's master data governance layer
- Duplicate payment controls operate in the cash disbursement sub-ledger—different system features, different audit trails

**4. Cost-Benefit Efficiency**
- Combining controls creates redundant checks (expensive) or gaps if either fails
- Separate regimes allow each to be right-sized to its risk

**5. Exception Handling Clarity**
- If a duplicate payment occurs, you know it's a *transaction processing* failure, not a data quality issue
- This distinction drives where remediation resources go and prevents blame-shifting between departments

## Practical Example

**Scenario**: ABC Corp entered "Acme Manufacturing Inc." twice in the vendor master (duplicate record). Later, ABC's procurement team paid Invoice #1001 twice using the legitimate vendor record.

- **Control Gap 1**: Vendor deduplication process failed → duplicate master record
- **Control Gap 2**: Invoice matching process failed → duplicate payment

Investigating only *one* failure would miss the systemic weaknesses in both procurement governance *and* payment integrity. These are distinct control failures requiring different remediation.

---

**Bottom line**: Treating these as a single control issue masks whether your problem is systematic (vendor data quality) or episodic (payment processing error), leading to over-controls in one area and under-controls in another.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response cleanly distinguishes the two phenomena and articulates different control regimes with specific controls in each (TIN matching, fuzzy matching for vendor records; three-way match, positive pay, reconciliation for payments). It addresses multiple operational-importance reasons including ownership separation, system architecture/audit trails, and exception handling. However, it misses the critical bridge case—where a duplicate payment occurs ACROSS two duplicate vendor records, which is the hardest case to detect and the reason cross-vendor-ID amount matching is needed as a backstop. The practical example actually shows the two issues as independent rather than as the bridge case. Per the rubric, missing the bridge case caps the score at 1.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_018 — close_and_controls · hard · **score 1/2** (model: `claude-opus-4-7`)

_Expected failure mode: control framework reasoning under SOX (multi-tier diagnosis)_

### Question

An improper payment was made. The same observable outcome ($X to wrong supplier or wrong amount) could be the result of a tactical 3-way-match exception that AP missed, OR a SOX P2P control design failure. The IT and audit treatment of these two diagnoses is very different. Explain the canonical hierarchy of control failures (transaction-level → policy-level → design-level), what evidence distinguishes each, and why it matters which diagnosis applies.

### Rubric

- **0**: Conflates the three tiers, OR fails to identify that the same observable can have different diagnoses, OR misses the audit / disclosure / remediation differences entirely
- **1**: Distinguishes the three tiers but does not address the bottom-up investigation order, OR misses the audit/disclosure thresholds (control deficiency / significant deficiency / material weakness), OR gives only one of the four 'why it matters' reasons
- **2**: Distinguishes all three tiers with concrete examples, addresses the audit / disclosure / remediation hierarchy (control deficiency → significant deficiency → material weakness), explains the bottom-up investigation order, gives a worked example showing the same observable resolving differently across tiers, and references the relevant audit framework (AS 2201 / COSO)

### Ideal answer

[AI DRAFT — practitioner review required] The canonical control-failure hierarchy goes from narrowest to broadest:

**Tier 1 — Transaction-level failure (a single control instance failed to operate).**
The control existed and was designed correctly, but in this specific transaction it didn't catch the issue. Example: 3-way match was supposed to flag the price variance but the AP clerk overrode it without proper documentation. The clerk's override is the failure point.

Evidence: the audit trail shows the control SHOULD have triggered (the variance was within the configured threshold), AND it shows manual override or bypass. The control configuration itself is correct.

Remediation: re-train the operator, tighten override authority, add maker-checker on overrides. Narrow remediation, narrow disclosure.

**Tier 2 — Policy-level failure (the control is designed correctly but the policy that governs it has a gap).**
The control as designed wouldn't have caught this fact pattern because the policy didn't anticipate the scenario. Example: 3-way match was configured for goods POs but services POs were exempted by policy without compensating control; an improper payment on a services PO slips through.

Evidence: the audit trail shows the control did not trigger BECAUSE the transaction was out of the policy scope. No bypass occurred — the policy itself is the gap.

Remediation: rewrite the policy to close the carve-out, add the compensating control, document the change. Broader remediation: every transaction in the policy gap window may need lookback review.

**Tier 3 — Design-level failure (the control framework itself is structurally inadequate).**
The control as conceived cannot prevent the class of issue that occurred. Example: a single AP clerk has vendor-master add + invoice approval + payment initiation entitlements. The 3-way match working perfectly does not stop this person from creating a ghost vendor and routing payments to themselves — that's not what 3-way match controls. The SoD design is the failure.

Evidence: the audit trail may show no individual control fired or failed; the loss occurred *between* controls or *outside* their scope. The framework, not the operation, is the gap.

Remediation: redesign the control framework — entitlement architecture, SoD matrix, ITGC review cadence. Broadest remediation. Material weakness assessment. SOX 404 disclosure consideration. Possible restatement.

**Why the diagnosis matters:**

1. **Audit treatment.** Tier-1 is a 'control deficiency.' Tier-2 is typically a 'significant deficiency.' Tier-3 is most likely a 'material weakness.' Each has different SOX disclosure thresholds and different external-auditor responses.

2. **Disclosure.** Material weakness requires Form 10-K Item 9A disclosure and adverse ICFR opinion; significant deficiency may not require external disclosure but requires audit committee communication. Control deficiency may stay in internal-audit workpapers.

3. **Scope of remediation effort.** Tier-1 affects one role/process. Tier-2 affects every transaction in the policy gap window — lookback scope is significant. Tier-3 affects every transaction the design failure could have enabled — lookback scope is comprehensive (per the q_010 fact pattern, this is what drives the 24-36-month all-vendor lookback).

4. **Investigation methodology.** Tier-1 is a process review (interview the clerk, review the override). Tier-2 is a policy review (compare written policy to the risk universe). Tier-3 is an architecture review (entitlement model, SoD matrix, ITGC) and typically pulls in IT audit, IS security, and possibly external counsel.

5. **Where the same observable can be diagnosed differently.** A duplicate-payment fact pattern could be Tier-1 if the AP clerk missed an obvious match the system flagged; Tier-2 if the duplicate-detection rules don't cover cross-vendor-ID matching (a policy gap); Tier-3 if the same person who added the duplicate vendor is also approving payments (an SoD design gap that enabled the duplicate vendor in the first place). The diagnosis drives whether you fix the operator, the policy, or the architecture — and getting the diagnosis wrong leads to either over- or under-remediation.

The canonical investigation order is bottom-up: confirm Tier-1 first (was this an operator failure?), only escalate to Tier-2 if the operator-failure hypothesis doesn't fit (the system should have caught it but the configuration didn't), and only escalate to Tier-3 if the policy-failure hypothesis doesn't fit (the configuration was right but the framework was inadequate).

References: PCAOB AS 2201 (definitions of control deficiency, significant deficiency, material weakness); COSO 2013 framework Component 4 'Control Activities' and Component 5 'Monitoring Activities'; SEC Regulation S-K Item 308.

### Model response

# The Canonical Hierarchy of Control Failures in P2P

When an improper payment surfaces, the audit/IT response depends entirely on *which layer* of the control stack failed. Treating a design failure as an operating failure (or vice versa) is one of the most common — and most expensive — mistakes in SOX 404 remediation, because it determines scope, materiality assessment, and disclosure obligations.

## The Three-Tier Hierarchy

### Tier 1 — Transaction-Level (Operating Effectiveness) Failure
**Definition:** The control was properly designed, was in place, and *should* have caught the error, but a specific instance of execution failed. The control framework is sound; a human or automated step misfired once (or a small, bounded number of times).

**Examples in P2P:**
- AP clerk overrode a 3-way-match exception flag without proper review.
- A duplicate invoice was paid because the clerk keyed a slightly different invoice number, defeating the ERP duplicate check.
- Approver clicked through a workflow without reviewing supporting documentation.

**Evidence that points here:**
- The control *exists* in the system (configurable tolerance, mandatory match, segregation enforced in roles).
- Other transactions in the population *did* trigger the control correctly.
- Logs show the exception was raised but mishandled, or the override field was used.
- Sampling shows a low deviation rate (within tolerable thresholds, e.g., < ~5–10% depending on frequency).

**Treatment:** Operating deficiency. Generally remediable through retraining, supervision, or tightening of override permissions. Usually does *not* require restating the control conclusion if isolated and compensating controls exist.

---

### Tier 2 — Policy-Level Failure
**Definition:** The control performed exactly as specified, but the *policy it enforces* is wrong, stale, or inconsistent with risk. The system did what it was told; what it was told was inadequate.

**Examples in P2P:**
- Tolerance thresholds (e.g., $500 or 10% price variance) are too loose, so the 3-way-match passed a genuinely improper invoice.
- Vendor master maintenance policy doesn't require re-validation of bank details, so a payment routed correctly per policy went to a fraudulent account.
- Delegation-of-authority matrix permits a manager to approve payments to a vendor they onboarded — policy gap, not execution gap.
- Policy carves out "emergency vendors" with no PO requirement; the carve-out itself is the hole.

**Evidence that points here:**
- The control log shows *no exception* — the transaction passed cleanly.
- The configuration matches the documented policy.
- Reviewing similar transactions reveals a *systematic* pattern (not isolated).
- Root-cause analysis traces back to a written policy, threshold table, or approval matrix that authorized the behavior.

**Treatment:** Typically a deficiency in the **control environment / policy layer**. Remediation requires policy revision, re-baselining of thresholds, and often re-testing of historical population because the gap was open across all transactions during the period.

---

### Tier 3 — Design-Level (SOX) Failure
**Definition:** The control, even if operating perfectly to its policy, *cannot* achieve the assertion it is mapped to. There is a structural defect in the control architecture: a missing control, an unmitigated risk in the risk-and-control matrix (RACM), or a control whose logic does not address the financial-statement assertion (existence, accuracy, completeness, valuation, cutoff, rights/obligations).

**Examples in P2P:**
- No control exists to detect a payment to a vendor whose bank details were changed *after* PO approval but *before* payment release. The 3-way-match was never designed to catch this — it's outside its scope.
- The same individual can create a vendor, raise a PO, approve the invoice, and release payment because SoD was never configured into the role design.
- 3-way-match is configured only for goods POs, not service POs, leaving an entire transaction class unmatched.
- No control covers non-PO invoices above materiality — the design simply has a gap.

**Evidence that points here:**
- Walkthroughs and the RACM show *no control* is mapped to the risk that materialized.
- Even a perfectly executed run of every existing control would not have prevented or detected the error.
- The improper payment exploited a path that the control narrative does not contemplate.
- IT general controls (ITGCs) — change management, access provisioning, configuration — may also be implicated if the design gap stems from unauthorized config drift.

**Treatment:** This is the most serious finding. Under PCAOB AS 2201 / SOX 404, a design deficiency typically escalates to **significant deficiency or material weakness** depending on magnitude and likelihood, because the *potential* misstatement is not bounded by a single failure — every transaction in scope is exposed. Requires:
- New control design and implementation.
- Management's reassessment of ICFR effectiveness.
- Possible 8-K disclosure (Item 4.02 in extreme cases).
- External auditor re-scoping.

---

## How to Distinguish Them — The Diagnostic Test

| Question | Tier 1 (Operating) | Tier 2 (Policy) | Tier 3 (Design) |
|---|---|---|---|
| Did the control fire? | Yes, but was overridden/ignored | No — transaction passed | No — no control exists for this risk |
| Is the configuration correct per policy? | Yes | Yes | N/A — gap in RACM |
| Is the policy itself adequate? | Yes | **No** | May or may not be relevant |
| Is the risk mapped in the RACM? | Yes | Yes | **No** |
| Would re-running the control prevent recurrence? | Yes (with discipline) | No (need policy change) | No (need new control) |
| Population exposure | Isolated | Systematic within policy scope | Entire risk universe unprotected |

---

## Why the Diagnosis Matters

1. **Scope of remediation.** Tier 1 is local (retrain a clerk). Tier 2 requires policy

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response distinguishes all three tiers with concrete P2P examples, provides a useful diagnostic table, and references PCAOB AS 2201 and SOX 404. However, the response is truncated at 'Tier 2 requires policy' and does not complete the 'Why the diagnosis matters' section. As a result, it does not fully address the bottom-up investigation order, does not clearly articulate the audit hierarchy mapping (control deficiency → significant deficiency → material weakness — it only mentions material weakness for Tier 3), does not provide the worked example showing the same observable resolving differently across tiers, and gives only a partial 'why it matters' discussion. This meets the Tier-1 distinction criteria but misses several key elements required for a 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_018 — close_and_controls · hard · **score 1/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: control framework reasoning under SOX (multi-tier diagnosis)_

### Question

An improper payment was made. The same observable outcome ($X to wrong supplier or wrong amount) could be the result of a tactical 3-way-match exception that AP missed, OR a SOX P2P control design failure. The IT and audit treatment of these two diagnoses is very different. Explain the canonical hierarchy of control failures (transaction-level → policy-level → design-level), what evidence distinguishes each, and why it matters which diagnosis applies.

### Rubric

- **0**: Conflates the three tiers, OR fails to identify that the same observable can have different diagnoses, OR misses the audit / disclosure / remediation differences entirely
- **1**: Distinguishes the three tiers but does not address the bottom-up investigation order, OR misses the audit/disclosure thresholds (control deficiency / significant deficiency / material weakness), OR gives only one of the four 'why it matters' reasons
- **2**: Distinguishes all three tiers with concrete examples, addresses the audit / disclosure / remediation hierarchy (control deficiency → significant deficiency → material weakness), explains the bottom-up investigation order, gives a worked example showing the same observable resolving differently across tiers, and references the relevant audit framework (AS 2201 / COSO)

### Ideal answer

[AI DRAFT — practitioner review required] The canonical control-failure hierarchy goes from narrowest to broadest:

**Tier 1 — Transaction-level failure (a single control instance failed to operate).**
The control existed and was designed correctly, but in this specific transaction it didn't catch the issue. Example: 3-way match was supposed to flag the price variance but the AP clerk overrode it without proper documentation. The clerk's override is the failure point.

Evidence: the audit trail shows the control SHOULD have triggered (the variance was within the configured threshold), AND it shows manual override or bypass. The control configuration itself is correct.

Remediation: re-train the operator, tighten override authority, add maker-checker on overrides. Narrow remediation, narrow disclosure.

**Tier 2 — Policy-level failure (the control is designed correctly but the policy that governs it has a gap).**
The control as designed wouldn't have caught this fact pattern because the policy didn't anticipate the scenario. Example: 3-way match was configured for goods POs but services POs were exempted by policy without compensating control; an improper payment on a services PO slips through.

Evidence: the audit trail shows the control did not trigger BECAUSE the transaction was out of the policy scope. No bypass occurred — the policy itself is the gap.

Remediation: rewrite the policy to close the carve-out, add the compensating control, document the change. Broader remediation: every transaction in the policy gap window may need lookback review.

**Tier 3 — Design-level failure (the control framework itself is structurally inadequate).**
The control as conceived cannot prevent the class of issue that occurred. Example: a single AP clerk has vendor-master add + invoice approval + payment initiation entitlements. The 3-way match working perfectly does not stop this person from creating a ghost vendor and routing payments to themselves — that's not what 3-way match controls. The SoD design is the failure.

Evidence: the audit trail may show no individual control fired or failed; the loss occurred *between* controls or *outside* their scope. The framework, not the operation, is the gap.

Remediation: redesign the control framework — entitlement architecture, SoD matrix, ITGC review cadence. Broadest remediation. Material weakness assessment. SOX 404 disclosure consideration. Possible restatement.

**Why the diagnosis matters:**

1. **Audit treatment.** Tier-1 is a 'control deficiency.' Tier-2 is typically a 'significant deficiency.' Tier-3 is most likely a 'material weakness.' Each has different SOX disclosure thresholds and different external-auditor responses.

2. **Disclosure.** Material weakness requires Form 10-K Item 9A disclosure and adverse ICFR opinion; significant deficiency may not require external disclosure but requires audit committee communication. Control deficiency may stay in internal-audit workpapers.

3. **Scope of remediation effort.** Tier-1 affects one role/process. Tier-2 affects every transaction in the policy gap window — lookback scope is significant. Tier-3 affects every transaction the design failure could have enabled — lookback scope is comprehensive (per the q_010 fact pattern, this is what drives the 24-36-month all-vendor lookback).

4. **Investigation methodology.** Tier-1 is a process review (interview the clerk, review the override). Tier-2 is a policy review (compare written policy to the risk universe). Tier-3 is an architecture review (entitlement model, SoD matrix, ITGC) and typically pulls in IT audit, IS security, and possibly external counsel.

5. **Where the same observable can be diagnosed differently.** A duplicate-payment fact pattern could be Tier-1 if the AP clerk missed an obvious match the system flagged; Tier-2 if the duplicate-detection rules don't cover cross-vendor-ID matching (a policy gap); Tier-3 if the same person who added the duplicate vendor is also approving payments (an SoD design gap that enabled the duplicate vendor in the first place). The diagnosis drives whether you fix the operator, the policy, or the architecture — and getting the diagnosis wrong leads to either over- or under-remediation.

The canonical investigation order is bottom-up: confirm Tier-1 first (was this an operator failure?), only escalate to Tier-2 if the operator-failure hypothesis doesn't fit (the system should have caught it but the configuration didn't), and only escalate to Tier-3 if the policy-failure hypothesis doesn't fit (the configuration was right but the framework was inadequate).

References: PCAOB AS 2201 (definitions of control deficiency, significant deficiency, material weakness); COSO 2013 framework Component 4 'Control Activities' and Component 5 'Monitoring Activities'; SEC Regulation S-K Item 308.

### Model response

# Canonical Hierarchy of P2P Control Failures: Diagnostic Framework

## I. The Core Diagnostic Problem

The observable fact—*payment went to wrong vendor or wrong amount*—is **equifinal**: multiple distinct causal chains produce the same symptom. Treating a design failure as a transaction exception wastes resources and leaves the organization perpetually exposed. Treating a transaction exception as a design failure triggers disproportionate remediation, SOX restatement risk, and potential material weakness disclosure. Getting the diagnosis right is not administrative tidiness; it has audit, financial reporting, and regulatory consequences.

---

## II. The Three-Level Hierarchy of Control Failures

### Level 1 — Transaction-Level (Execution) Failure

**Definition:** The control *existed*, was *designed correctly*, and was *operative*—but the individual transaction was not processed in conformance with it. A human or system actor deviated from the prescribed procedure on *this specific instance*.

**Canonical P2P example:**
- 3-way match was configured in ERP; invoice tolerance thresholds were set; workflow routing was active.
- AP clerk overrode a system hold, approved a price variance outside tolerance, or simply keyed wrong data.
- The exception is *isolated and traceable* to that clerk's action on that date.

**What this is NOT:** A systemic control failure. The control worked in the other 4,000 transactions processed that period.

---

### Level 2 — Policy/Compliance (Operating Effectiveness) Failure

**Definition:** The control exists and is designed correctly, but it is *not being consistently followed* across a population of transactions. The control is operative on paper but failing in practice—a behavioral or governance gap, not an architectural one.

**Canonical P2P example:**
- 3-way match policy requires all POs >$5,000 to have signed receipt confirmation before payment release.
- Testing reveals that 35% of sampled invoices in that range were paid without matched receiving reports.
- No single actor is responsible; the failure pattern is systemic across multiple approvers or business units.
- The *design* (the written policy, the ERP configuration) is sound; *execution* across the population is not.

This level is where **SOX operating effectiveness deficiencies** typically manifest—and where PCAOB AS 2201 draws the distinction between a *significant deficiency* and a *material weakness* based on likelihood and magnitude of misstatement.

---

### Level 3 — Design-Level (Control Design) Failure

**Definition:** The control as *designed* is insufficient to prevent or detect the risk even if followed perfectly. No amount of diligent execution of the stated procedure would have caught the improper payment. The architecture of the control is flawed.

**Canonical P2P examples:**
- 3-way match is configured but tolerance bands are set so wide (+/−15% on unit price, no cap on total variance) that a fraudulent invoice for $2.1M passes auto-approval against a $2.0M PO.
- Segregation of duties matrix allows a single user role to create vendor, create PO, and approve payment in one system profile.
- The ERP enforces match only on PO line count, not on unit price or total amount—so quantity match passes while price manipulation succeeds.
- No compensating control (management review of variance reports, vendor master change audits) exists downstream.

This is the canonical **SOX control design deficiency**: the control could never have worked, regardless of operator diligence.

---

## III. Evidentiary Standards That Distinguish Each Level

| Evidence Dimension | Level 1 (Transaction) | Level 2 (Policy/Operating) | Level 3 (Design) |
|---|---|---|---|
| **Population testing** | Single or rare isolated instance; all other transactions conform | Pattern across multiple transactions/periods; statistically significant exception rate | *All* transactions subject to the control are theoretically exposed; failure rate is irrelevant—the control cannot work |
| **Control configuration audit** | ERP logs show control was active, properly configured, correct thresholds | ERP logs show control active; workflow bypasses or manual overrides are frequent | Configuration review, design documentation, or walkthroughs reveal the control specification itself is deficient |
| **User access/role review** | Proper SOD in place; single actor with appropriate access deviated | Proper SOD in place; multiple actors deviated consistently | SOD violation is *built into the role matrix*; no single actor is uniquely culpable |
| **Audit trail evidence** | Override log entry with specific user/timestamp; one-off exception | Override log shows recurring pattern across users; or no log entries exist because bypasses were normalized | Override not required—the transaction passed *cleanly through* all controls; no exception flag was raised |
| **Recurrence pattern** | Not recurrent; first offense or rare | Recurrent across reporters, periods, or entities | Every transaction in scope is potentially affected; detection by exception testing is impossible within the control |
| **Root cause interview** | "I knew the rule; I made a mistake / chose to deviate" | "We weren't trained" / "That's how we've always done it" / "The manager told us to get invoices out" | "I followed the procedure exactly"—the procedure itself would not catch this scenario |
| **Control gap in flowchart** | No gap in the designed process flow | No gap in the designed process flow; gap is in execution | Gap visible in process design documentation, RACI, system configuration spec |
| **Prior period comparability** | Prior periods clean | Prior periods show similar exception rates | Prior periods *also* clean in detected exceptions—because the control *never* would have flagged this |

---

## IV. Why the Diagnosis Determines Everything Downstream

### A. IT/System Remediation Scope

| Diagnosis | IT Action Required |
|---|---|
| Transaction failure | None required to the control itself. Possibly: user access review, re-training, disciplinary action. ERP configuration unchanged. |
| Policy/operating failure | Possibly: system enforcement tightening (reduce manual override permissions), workflow hardening, automated escalation rules. IT change management ticket scope is *narrow and targeted*. |
| Design failure | **Mandatory control redesign.** ERP configuration change, potentially requiring full SDLC/change management cycle, UAT, re-documentation of control description, update to control matrix. May require interim compensating controls during remediation window. |

A design failure treated as a transaction error means the redesign never happens—the organization continues to issue the same SOX representation about a control that *cannot work*.

---

### B. SOX Implications (AS 2201 / COSO Framework)

**If it's a transaction error:**
- Not a control deficiency at all under SOX unless the error itself represents a financial statement misstatement above threshold.
- Correcting entry; no impact to management's assessment of ICFR.
- External auditor testing of the control would find it operative; control reliance holds.

**If it's an operating effectiveness failure:**
- Constitutes a **control deficiency** under PCAOB AS 2201.
- Severity determination: *significant deficiency* (more than remote possibility of more-than-inconsequential misstatement) or *material weakness* (reasonable possibility of material misstatement).
- Must be evaluated at the *population level* for aggregate exposure.
- Management must document, remediate *before year-end* if possible, or disclose in 10-K/annual report internal control assessment.
- Auditor cannot place reliance on the control; must perform *substantive procedures* to cover the gap.

**If it's a design deficiency:**
- Under COSO and AS 2201, **a control that is not designed to achieve its objective is a deficiency regardless of whether a misstatement occurred.**
- Design deficiency is frequently the more severe classification because it implies the control *never provided assurance*—not just that it failed intermittently.
- Requires retroactive consideration: was the control ineffective in prior periods? Does this affect prior representations?
- External auditor must: (1) not rely on the control for *any* period, (2) expand substantive testing, (3) evaluate whether aggregation with other deficiencies creates a material weakness.
- **IT general controls (ITGCs)** come into scope if the design flaw exists in system configuration—because the reliability of system-generated reports used in financial reporting is now in question.

---

### C. Fraud vs. Error Bifurcation

The hierarchy also informs the auditor's obligation under **AU-C Section 240 / ISA 240**:

- **Transaction failure** with indicators of intentionality (e.g., vendor master manipulation, split invoices just below approval thresholds) → **fraud risk indicator**; escalate to forensic investigation, potential FCPA/regulatory exposure.
- **Policy failure** with no intentionality → management override risk, tone

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response distinguishes all three tiers with concrete P2P examples, provides extensive evidence tables, and addresses audit/disclosure/remediation differences. It references AS 2201 and COSO. However, it has two notable gaps relative to the rubric for a 2: (1) It does NOT explain the bottom-up investigation order (confirm Tier-1 first, escalate only if hypothesis doesn't fit). (2) It does not provide a worked example showing the same observable resolving differently across all three tiers — while it gives separate examples per tier, it doesn't walk through one fact pattern (like the duplicate payment) being diagnosed three different ways. Additionally, the candidate's Tier 2 framing diverges somewhat from the ideal (it frames Tier 2 as operating effectiveness/non-compliance rather than policy scope gaps), though this is a defensible alternative taxonomy. Given the missing investigation order and missing cross-tier worked example, this fits the '1' criteria.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_002 — invoice_processing · easy · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: applying domain conventions_

### Question

For each of the five incoming invoices below, classify whether it should be processed as PO-backed or non-PO, and give a one-line reason. Assume a typical mid-market policy: goods purchases require a PO; services > $25k require a PO; recurring utilities and statutory payments are PO-exempt.

### Context

```
1. Invoice from PG&E for $4,820 — monthly electricity for HQ, recurring.
2. Invoice from Salesforce for $84,000 — annual SaaS renewal, last year was on a PO.
3. Invoice from Latham & Watkins for $11,500 — legal services on a retainer, no SOW referenced.
4. Invoice from Staples for $612 — office supplies, references PO #4500987.
5. Invoice from BrandWorks Agency for $48,000 — marketing campaign, references SOW-2024-17.
```

### Rubric

- **0**: Misclassifies two or more invoices, or applies the rules without reference to thresholds/carve-outs
- **1**: Classifies all five correctly but misses the nuance on the SaaS auto-renewal, the legal carve-out conditions, or the after-the-fact PO control issue
- **2**: Classifies all five correctly and surfaces at least two control nuances (auto-renewal-without-PO as rogue spend, after-the-fact PO concern, legal-engagement-letter as PO equivalent)

### Ideal answer

1. PG&E utility — non-PO. Recurring utility under the policy carve-out; covered by an approved utility budget line, not a PO commitment.
2. Salesforce SaaS renewal — PO-backed. Services > $25k threshold; auto-renewal should be on a PO so the commitment is recorded against budget and the term/price are locked. If the renewal arrived without an active PO, that is itself an exception (rogue spend) and should be remediated before payment.
3. Latham & Watkins legal — non-PO is acceptable per typical legal carve-outs (matter-based, hard to scope at PO time), but only if the firm is on the approved counsel list and the spend is within the matter budget set by GC. Otherwise route as exception. The retainer should still hit a contract/engagement letter on file; SOX-relevant orgs often require the engagement letter to function as the PO equivalent.
4. Staples office supplies — PO-backed. Goods purchase referencing PO #4500987; standard 3-way match path (PO + GR + invoice).
5. BrandWorks marketing — PO-backed. Services > $25k. SOW-2024-17 should map to a PO that references the SOW; many orgs treat the SOW as the commitment document but require a PO created from it. If no PO exists, hold the invoice and create one retroactively only if policy permits 'after-the-fact' POs (many do not, and it is a control finding).

### Model response

# Invoice Classification

Applying the stated policy: goods → PO required; services > $25k → PO required; recurring utilities/statutory → PO-exempt.

| # | Vendor | Amount | Classification | Reason |
|---|--------|--------|----------------|--------|
| 1 | PG&E | $4,820 | **Non-PO** | Recurring utility — explicitly PO-exempt under policy. |
| 2 | Salesforce | $84,000 | **PO-backed (PO required)** | Service > $25k threshold; prior year was on a PO — a renewal PO should be raised before processing. |
| 3 | Latham & Watkins | $11,500 | **Non-PO** | Professional services under the $25k threshold and covered by an existing retainer; no SOW needed. |
| 4 | Staples | $612 | **PO-backed** | Goods purchase referencing PO #4500987 — process via 3-way match (PO, receipt, invoice). |
| 5 | BrandWorks Agency | $48,000 | **PO-backed** | Service > $25k; SOW-2024-17 should be tied to a corresponding PO before payment. |

## Key Flags for AP
- **Salesforce**: Do **not** process until a renewal PO is issued — high-value SaaS without a current-year PO is a control gap.
- **Latham & Watkins**: Confirm the retainer agreement is on file as the controlling document in lieu of a PO/SOW.
- **BrandWorks**: Verify SOW-2024-17 is linked to an active PO; if only the SOW exists, route to Procurement to raise one before payment.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** All five invoices are correctly classified. The response surfaces multiple control nuances: (1) Salesforce auto-renewal without a current PO flagged as a control gap/rogue spend equivalent, (2) Latham & Watkins retainer agreement noted as the controlling document in lieu of a PO (engagement-letter-as-PO-equivalent nuance), and (3) BrandWorks SOW needing to be linked to an active PO before payment, implicitly addressing the after-the-fact PO concern. Minor weakness: doesn't explicitly call out approved counsel list condition or explicitly prohibit retroactive POs, but meets the bar of two+ control nuances.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_003 — invoice_processing · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: multi-step arithmetic and control reasoning_

### Question

Walk through the 3-way match for the documents below. Identify every exception, quantify the variance, and state the resolution path including which roles must approve and which controls apply.

### Context

```
PO #4500-22871
  Line 1: 100 units of part #X-77 @ $10.00 = $1,000.00
  Tolerance: ±2% price, ±5% quantity
  Status: Open, no prior receipts

Goods Receipt (GR) #50032118
  Line 1: 95 units received, marked 'final delivery — short ship per supplier'
  Receiver: warehouse staff

Invoice INV-88412 from supplier
  Line 1: 100 units @ $10.20 = $1,020.00
  Plus freight: $35.00
  Invoice total: $1,055.00
  Payment terms: Net 30
```

### Rubric

- **0**: Identifies fewer than two of the three exceptions, computes the variances incorrectly, or pays the invoice as-is
- **1**: Identifies all three exceptions and the basic resolution but misses role segregation, treats freight as automatically payable, or fails to flag the boundary case at all (5.00% qty / 2.00% price exactly at tolerance)
- **2**: Identifies all three exceptions with correct math, explicitly states which tolerance convention is being applied (strictly-less-than vs less-than-or-equal — both are defensible) and reasons consistently from that, addresses each through the proper role (AP / buyer / receiver), and references SOX three-way-match control and segregation of duties

### Ideal answer

Three exceptions:

1. Quantity variance — invoice 100 units vs. GR 95 units = 5-unit / 5.00% variance. The GR is marked final delivery, so the missing 5 units will not be received. The invoice over-bills by 5 units × $10.00 = $50.00. Tolerance is ±5% on quantity. **Both `<` and `≤` are defensible conventions in industry — SAP defaults to `<` while some Oracle / mid-market systems use `≤`. State which convention the responder is applying and reason consistently.** Under `<`, 5.00% is out of tolerance → exception. Under `≤`, 5.00% is in tolerance but is still a quantity issue against a final-delivery GR (you cannot pay for unshipped units), so it routes as a no-tolerance exception regardless. Either way, the resolution is the same: do not pay for the 5 unshipped units.

2. Price variance — $10.20 vs. PO $10.00 = $0.20 / 2.00% variance. Tolerance ±2%, same boundary question. Under `<`, out of tolerance → exception. Under `≤`, in tolerance → auto-release per ERP. Over-bill at PO quantity = 100 × $0.20 = $20.00. Even under `≤`, best practice is to surface boundary-case variances to the buyer rather than auto-pay; documenting the convention explicitly is the audit-defensible move.

3. Unauthorized freight — $35.00 freight line is not on the PO. Whether freight is allowable depends on the Incoterms / freight policy on the PO. If the PO is silent and policy is 'freight included unless on PO,' reject the freight line.

Resolution path:
- Hold the invoice; do not pay.
- Quantity: confirm short-ship with receiving and request a credit memo from the supplier for the 5 unshipped units, OR have supplier reissue the invoice for 95 units. Do not pay against a quantity not received.
- Price: route to the buyer (sourcing) for variance approval. Buyer either approves the increase (and updates the PO via change order) or rejects and demands the invoice be reissued at PO price.
- Freight: route to the buyer; if not contractually owed, reject.
- Net 30 starts only when the corrected invoice is received in good order — flag the supplier portal accordingly so payment-term clocks are not gamed.

Controls and segregation:
- AP clerk identifies and posts the exception but cannot approve the variance.
- Buyer (sourcing) approves price/freight variances within their delegation; above delegation, escalate per the DOA matrix.
- Receiver confirms quantity facts but is not the same person as buyer or AP (segregation under SOX P2P).
- All exception approvals must be documented in the system to support the SOX 'invoice-to-PO/GR three-way match' control test.

### Model response

# 3-Way Match Analysis: PO #4500-22871 / GR #50032118 / INV-88412

## Reasoning: The 3-Way Match Framework

A 3-way match validates that **PO ≡ GR ≡ Invoice** across three dimensions:
1. **Quantity** (Invoice qty ≤ GR qty ≤ PO qty, within tolerance)
2. **Price** (Invoice unit price ≈ PO unit price, within tolerance)
3. **Item/identity** (same part number, same supplier, same PO line)

I'll walk each comparison, then identify exceptions, quantify them, and route each to its resolution path.

---

## Step 1: Pairwise Comparisons

### A. PO ↔ GR (Receipt vs. Order)
| Field | PO | GR | Delta |
|---|---|---|---|
| Quantity | 100 | 95 | **−5 units (−5.0%)** |
| Status | Open | Final delivery flagged | Closure event |

- Quantity tolerance is ±5%. The variance is **exactly at the −5% boundary** (95 ≤ 100 × 0.95). Whether this passes depends on whether tolerance is *inclusive* (≤5%) or *exclusive* (<5%); most ERPs (SAP MM, Oracle) treat boundary as **within tolerance**.
- However, the receiver flagged **"final delivery — short ship"**, which converts an open quantity into a *closed* line with under-delivery. This triggers a **PO line closure / under-delivery acceptance** decision, separate from tolerance math.

### B. PO ↔ Invoice (Billing vs. Order)
| Field | PO | Invoice | Delta |
|---|---|---|---|
| Quantity billed | 100 | 100 | 0 |
| Unit price | $10.00 | $10.20 | **+$0.20 (+2.0%)** |
| Extended | $1,000.00 | $1,020.00 | +$20.00 |
| Freight | Not specified on PO | $35.00 | **Unplanned charge** |

- Price variance is **at the +2% tolerance ceiling** — borderline pass on the unit price field itself.
- Freight of **$35.00 is not on the PO** → unplanned delivery cost. This is an **out-of-tolerance exception regardless of price tolerance** because it's a new cost element, not a variance on an existing one.

### C. GR ↔ Invoice (Billing vs. Receipt) — the critical leg
| Field | GR | Invoice | Delta |
|---|---|---|---|
| Quantity | 95 received | 100 billed | **+5 units over-billed** |

- Supplier invoiced **for goods not received**. This is the most material exception: a **quantity over-billing of $51.00** (5 × $10.20).
- Combined with the "final delivery" flag, the missing 5 units **will never arrive**, so this is not a timing difference — it is a hard discrepancy.

---

## Step 2: Exception Register (Quantified)

| # | Exception | Type | Magnitude | Severity |
|---|---|---|---|---|
| **E1** | Invoice qty (100) > GR qty (95) | **Quantity over-bill** | 5 units = **$51.00** | **High** — block payment |
| **E2** | Unit price $10.20 vs PO $10.00 | Price variance | +$0.20/unit = +$20.00 (+2.0%) | Low — at tolerance edge |
| **E3** | Unplanned freight $35.00 | Unplanned cost | $35.00 | Medium — needs PO amendment or accept/reject |
| **E4** | Short shipment flagged "final" | PO closure event | 5 units undelivered | Medium — supply continuity / demand impact |

**Total invoice exposure to be withheld or adjusted:** $51.00 (qty) + potentially $35.00 (freight) = **up to $86.00 of $1,055.00**.
**Approvable amount on a clean match:** 95 × $10.00 = **$950.00** (PO price applied to GR qty).

---

## Step 3: Resolution Paths

### E1 — Quantity Over-Bill ($51.00) — *Primary Block*
- **Control:** GR-based Invoice Verification (ERIV / "GR-based IV" flag in SAP). Invoice cannot exceed GR quantity. System auto-blocks for payment.
- **Action:** AP Clerk parks/blocks the invoice. Issue **debit memo request** or require supplier **credit note for 5 units @ invoiced price ($51.00)**.
- **Approver:** AP Supervisor authorizes the block; **Buyer/Procurement** confirms with supplier in writing that the 5 units are not coming.
- **SoD control:** The person creating the GR cannot be the same person approving the invoice or issuing the credit memo.

### E2 — Price Variance (+2%, $20.00)
- **Control:** Price tolerance check at IV. At the +2% boundary, system behavior depends on configuration (inclusive vs. exclusive).
- **Action:** Two options:
  1. If price was contractually updated, **Buyer amends PO** to $10.20 (PO change order, re-approved per DoA).
  2. If not, supplier issues credit note for the $20 overage, or AP posts price variance to **PPV (Purchase Price Variance) GL account** if within auto-post threshold.
- **Approver:** **Buyer** (procurement) for PO amendment; **Cost Accounting / Controller** owns PPV account review.

### E3 — Unplanned Freight $35.00
- **Control:** Unplanned delivery costs handling (SAP T-code MIRO field; Oracle "freight" line). Policy typically requires PO to include freight terms (Incoterms).
- **Action:** Verify Incoterms on PO:
  - If **DDP/CIP/CPT** (freight prepaid by supplier) → freight is **not payable**; reject the $35.00.
  - If **FOB Origin / EXW

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The candidate identifies all three core exceptions (quantity, price, freight) with correct math ($50/$51 quantity overbill, $20 price variance, $35 unplanned freight). It explicitly addresses the boundary case for both the 5% quantity and 2% price tolerances, noting inclusive vs exclusive conventions. It routes each exception to the proper role (AP clerk blocks, Buyer/Procurement for PO amendment and supplier confirmation, Cost Accounting for PPV) and explicitly invokes segregation of duties (GR creator cannot approve invoice). It references GR-based IV control and DoA. The response is cut off at the end but has already delivered the substantive content needed for a 2. Minor weakness: doesn't explicitly name 'SOX three-way-match control' but does reference SoD and control framework adequately.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_004 — invoice_processing · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: pattern matching and control logic_

### Question

Are these two invoices a duplicate? Walk through the signals you would use, recommend a resolution, and describe the duplicate-detection rules a P2P system should run automatically to catch this pattern.

### Context

```
Invoice 1
  Supplier:    Northbridge Logistics LLC (vendor #V-44120)
  Invoice #:   NB-2024-1142
  Invoice date: 2026-02-08
  Amount:      $4,287.50
  PO ref:      6710
  Status:      Posted, paid via ACH on 2026-02-19

Invoice 2
  Supplier:    Northbridge Logistics LLC (vendor #V-44120)
  Invoice #:   1142-A
  Invoice date: 2026-02-22
  Amount:      $4,287.50
  PO ref:      6710
  Status:      Submitted, awaiting AP review
```

### Rubric

- **0**: Says it is not a duplicate, or pays the second invoice, or misses the PO/amount/vendor co-occurrence
- **1**: Identifies the duplicate but only cites one or two signals, or omits the resolution workflow, or omits automated detection rules
- **2**: Identifies it as a duplicate citing multiple signals (amount + vendor + PO + invoice-number family + timing), gives a control-aware resolution path, and lists at least three automated detection rules including the one that catches this exact case

### Ideal answer

Yes, this is a duplicate with very high confidence. Signals:

- Same vendor (V-44120, exact).
- Same amount to the cent ($4,287.50). Identical to-the-cent amounts within a short window from the same vendor are the single strongest duplicate signal.
- Same PO reference (6710). Two distinct invoices for the same PO and the same amount is highly unusual unless the PO was for two identical milestone payments — in which case the supplier would normally use distinct invoice numbers and reference the milestones.
- Invoice numbers are near-identical: 'NB-2024-1142' and '1142-A'. The '-A' suffix is a textbook resubmission pattern — vendors append it when they believe the original was lost, rejected, or unpaid. The vendor here likely re-sent because they did not see payment confirmation between 02-08 (issue) and 02-22 (resubmit), even though payment ran on 02-19.
- 14-day gap is consistent with a resubmission cycle, not a separate billing event.

Resolution path:
- Do not pay Invoice 2.
- AP clerk posts a 'suspected duplicate' hold; routes to AP supervisor (segregation: clerk identifies, supervisor confirms).
- Pull the remittance for Invoice 1 (2026-02-19 ACH) and email the supplier with the remittance reference; ask them to confirm receipt and to void Invoice 2 in their system.
- Document the disposition for the SOX duplicate-payment control workpaper.
- If Invoice 1 was actually voided/canceled before pay (it was not, here), then Invoice 2 might be a legitimate resubmission — only then process under the original PO.

Duplicate-detection rules a P2P system should run:
1. Exact match on (vendor + invoice_number) — catches re-keying.
2. Exact match on (vendor + amount + invoice_date within ±N days, e.g. 30) — catches the same invoice resubmitted under a slightly different number.
3. Fuzzy match on invoice_number (Levenshtein distance ≤ 2, or shared substring ≥ 6 chars) within a vendor — catches the '1142' / '1142-A' / 'NB-2024-1142' family.
4. (vendor + amount + PO + invoice_date within window) — catches the case here even when invoice numbers differ entirely.
5. Cross-vendor amount match within window — catches duplicate payments across two duplicate vendor records (relates to q_001).
6. Reverse-amount match — catches a credit memo paired against a re-billed invoice for the same amount.

The (vendor + amount + PO + window) rule is what would have caught this case automatically.

### Model response

# Duplicate Invoice Analysis: NB-2024-1142 vs. 1142-A

## Verdict

**Yes — this is almost certainly a duplicate.** Invoice 2 should be blocked from payment pending vendor confirmation. The pattern is a classic "modified invoice number" duplicate, which is one of the most common (and most often missed) duplicate-payment scenarios in P2P operations.

---

## Signals Used to Reach That Conclusion

I would weight the signals like this — any one is suspicious, the combination is conclusive:

| Signal | Invoice 1 | Invoice 2 | Match? |
|---|---|---|---|
| Vendor ID | V-44120 | V-44120 | **Exact** |
| Amount | $4,287.50 | $4,287.50 | **Exact (to the cent)** |
| PO reference | 6710 | 6710 | **Exact** |
| Invoice number | NB-2024-1142 | 1142-A | **Fuzzy match** — "1142" is the core token; "-A" is a common re-submission suffix |
| Invoice date | 2026-02-08 | 2026-02-22 | 14 days apart — within a typical "resubmission window" |
| Status sequence | Posted & paid 2026-02-19 | Submitted 2026-02-22 | Invoice 2 arrived **3 days after** Invoice 1 was paid — consistent with a vendor not seeing the ACH yet and re-billing |

### Why the invoice-number difference is not exonerating
Vendors and AP clerks routinely create "new" invoice numbers when:
- A vendor's AR system flags the original as unpaid (because remittance hasn't posted on their side) and auto-generates a follow-up with an "-A", "R", "REV", or "/2" suffix.
- A clerk re-keys a paper or PDF copy and the system rejects the original number as already on file, so they tweak it.
- The invoice was scanned twice via different intake channels (email + portal).

The substring `1142` appearing in both numbers, paired with identical vendor/amount/PO, is the giveaway.

---

## Recommended Resolution

1. **Place Invoice 2 on hold** in AP (do not approve, do not three-way match through to payment).
2. **Cross-check the remittance**: confirm the ACH on 2026-02-19 (Invoice 1) cleared and was applied by the bank.
3. **Contact Northbridge Logistics AR** with the remittance advice (ACH date, amount, reference). Ask them to confirm whether 1142-A represents:
   - (a) the same charge being re-billed (most likely → reject and close),
   - (b) a credit/rebill pair where an offsetting credit memo is missing (request the credit memo), or
   - (c) genuinely new work under PO 6710 that coincidentally matches the amount (require a distinct delivery/service proof and a different PO line or release).
4. **If duplicate confirmed**: reject Invoice 2 with reason code "Duplicate of NB-2024-1142", notify the requester, and log the event against the vendor master for trend tracking.
5. **If genuine**: require the vendor to reissue with a unique invoice number unrelated to 1142, attach distinct supporting documentation (POD, timesheet, etc.), and re-submit. Annotate the AP record so a future auditor sees the disposition.
6. **Recover if already paid** (not the case here, but worth noting as standard SOP): issue a debit memo or request refund; do not net against future invoices without written vendor agreement, as that complicates 1099/audit trails.

---

## Automated Duplicate-Detection Rules a P2P System Should Run

A mature P2P platform (SAP, Coupa, Oracle, Workday, etc.) should run these checks **at invoice intake, before workflow routing, and again immediately before payment release**.

### Tier 1 — Exact-match rules (hard block)
1. **Same vendor + same invoice number** (case- and whitespace-normalized) → block as duplicate. *(Would not have caught this case — that's why Tier 2 exists.)*
2. **Same vendor + same amount + same invoice date** → block.
3. **Same vendor + same PO + same amount + same invoice date** → block.

### Tier 2 — Fuzzy / near-match rules (soft block, route to AP review)
4. **Same vendor + same amount + invoice numbers with high similarity** (Levenshtein ≤ 2, or one is a substring of the other after stripping non-alphanumerics, or one differs only by a trailing token like `-A`, `R`, `REV`, `/2`, `COPY`) → flag. **This is the rule that catches NB-2024-1142 vs 1142-A.**
5. **Same vendor + same amount + same PO + invoice dates within N days** (typical N = 30–90) → flag.
6. **Same vendor + same amount + invoice date within N days, regardless of PO** → flag (catches non-PO duplicates).
7. **Same vendor + same amount where prior invoice is already PAID within the last 60 days** → elevated flag (highest financial risk: payment has already left the bank).

### Tier 3 — Cross-entity / cross-vendor rules
8. **Same bank account / remit-to + same amount + same invoice number across different vendor records** → block (catches the "duplicate vendor master" loophole, e.g., "Northbridge Logistics LLC" and "Northbridge Logistics" set up as two vendors).
9. **Same tax ID + same amount + similar invoice number** → flag.
10. **Same scanned-document hash (MD5/SHA on the PDF) or OCR text similarity above threshold** → block (catches the same file submitted via two channels).

### Tier 4 — Behavioral / pattern rules
11. **Invoice received within X days after a payment to the same vendor for the same amount** → flag (specifically targets the "vendor didn't see the ACH yet" pattern, which is exactly what this case looks like).
12. **Round-amount or repeating-amount clustering** for a single vendor over a short window → flag for

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the duplicate, cites all key signals (vendor, amount, PO, invoice number family, timing), provides a control-aware resolution path with hold/vendor confirmation/recovery steps, and lists numerous automated detection rules including the specific rule (vendor + amount + PO + date window, and fuzzy invoice number match) that would catch this case.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_004 — invoice_processing · medium · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: pattern matching and control logic_

### Question

Are these two invoices a duplicate? Walk through the signals you would use, recommend a resolution, and describe the duplicate-detection rules a P2P system should run automatically to catch this pattern.

### Context

```
Invoice 1
  Supplier:    Northbridge Logistics LLC (vendor #V-44120)
  Invoice #:   NB-2024-1142
  Invoice date: 2026-02-08
  Amount:      $4,287.50
  PO ref:      6710
  Status:      Posted, paid via ACH on 2026-02-19

Invoice 2
  Supplier:    Northbridge Logistics LLC (vendor #V-44120)
  Invoice #:   1142-A
  Invoice date: 2026-02-22
  Amount:      $4,287.50
  PO ref:      6710
  Status:      Submitted, awaiting AP review
```

### Rubric

- **0**: Says it is not a duplicate, or pays the second invoice, or misses the PO/amount/vendor co-occurrence
- **1**: Identifies the duplicate but only cites one or two signals, or omits the resolution workflow, or omits automated detection rules
- **2**: Identifies it as a duplicate citing multiple signals (amount + vendor + PO + invoice-number family + timing), gives a control-aware resolution path, and lists at least three automated detection rules including the one that catches this exact case

### Ideal answer

Yes, this is a duplicate with very high confidence. Signals:

- Same vendor (V-44120, exact).
- Same amount to the cent ($4,287.50). Identical to-the-cent amounts within a short window from the same vendor are the single strongest duplicate signal.
- Same PO reference (6710). Two distinct invoices for the same PO and the same amount is highly unusual unless the PO was for two identical milestone payments — in which case the supplier would normally use distinct invoice numbers and reference the milestones.
- Invoice numbers are near-identical: 'NB-2024-1142' and '1142-A'. The '-A' suffix is a textbook resubmission pattern — vendors append it when they believe the original was lost, rejected, or unpaid. The vendor here likely re-sent because they did not see payment confirmation between 02-08 (issue) and 02-22 (resubmit), even though payment ran on 02-19.
- 14-day gap is consistent with a resubmission cycle, not a separate billing event.

Resolution path:
- Do not pay Invoice 2.
- AP clerk posts a 'suspected duplicate' hold; routes to AP supervisor (segregation: clerk identifies, supervisor confirms).
- Pull the remittance for Invoice 1 (2026-02-19 ACH) and email the supplier with the remittance reference; ask them to confirm receipt and to void Invoice 2 in their system.
- Document the disposition for the SOX duplicate-payment control workpaper.
- If Invoice 1 was actually voided/canceled before pay (it was not, here), then Invoice 2 might be a legitimate resubmission — only then process under the original PO.

Duplicate-detection rules a P2P system should run:
1. Exact match on (vendor + invoice_number) — catches re-keying.
2. Exact match on (vendor + amount + invoice_date within ±N days, e.g. 30) — catches the same invoice resubmitted under a slightly different number.
3. Fuzzy match on invoice_number (Levenshtein distance ≤ 2, or shared substring ≥ 6 chars) within a vendor — catches the '1142' / '1142-A' / 'NB-2024-1142' family.
4. (vendor + amount + PO + invoice_date within window) — catches the case here even when invoice numbers differ entirely.
5. Cross-vendor amount match within window — catches duplicate payments across two duplicate vendor records (relates to q_001).
6. Reverse-amount match — catches a credit memo paired against a re-billed invoice for the same amount.

The (vendor + amount + PO + window) rule is what would have caught this case automatically.

### Model response

# Duplicate Invoice Analysis: NB-2024-1142 vs. 1142-A

---

## 1. Signal-by-Signal Assessment

| Signal | Invoice 1 | Invoice 2 | Risk Interpretation |
|--------|-----------|-----------|---------------------|
| **Vendor** | Northbridge Logistics LLC / V-44120 | Same | ⚠️ Identical — necessary condition for a duplicate |
| **Amount** | $4,287.50 | $4,287.50 | 🔴 Exact match — strong duplicate signal |
| **PO Reference** | 6710 | 6710 | 🔴 Same PO — implies same underlying obligation |
| **Invoice Number** | NB-2024-1142 | 1142-A | 🟡 Similar, not identical — classic resubmission pattern (suffix added) |
| **Invoice Date** | 2026-02-08 | 2026-02-22 | 🟡 14-day gap — consistent with a vendor resubmitting after perceived non-payment |
| **Payment Status** | Posted, paid via ACH 2026-02-19 | Awaiting AP review | 🔴 First is fully paid; second would create double payment |

**Composite verdict: High-confidence duplicate.** Four of six signals are hard matches, and the two that differ (invoice number and date) follow a pattern that is *characteristic* of intentional or accidental resubmission, not a second legitimate transaction.

---

## 2. Why the Differences Don't Exonerate Invoice 2

### Invoice number variation (`NB-2024-1142` → `1142-A`)
- Vendors and their AR staff frequently strip prefixes, add suffixes, or reformat invoice numbers when resubmitting via a different channel (email vs. portal) or when an AR system auto-generates a follow-up number.
- The suffix "-A" is a textbook indicator of a "resent" document, not a new one.
- A *genuinely new* invoice for new services would carry a completely independent number (e.g., NB-2024-1198).

### Date gap (Feb 8 → Feb 22)
- Invoice 1 was paid on Feb 19. Invoice 2 was dated Feb 22 — three days *after* payment. This is consistent with a vendor's AR department not yet seeing the ACH settlement and resubmitting.
- It is **not** consistent with a second delivery/service event, because the PO reference is identical and no new PO line is cited.

### Same PO, same amount
- If a second legitimate service had been rendered, a conscientious vendor would reference a new PO line, a new delivery receipt, or a different amount. Neither is present.

---

## 3. Recommended Resolution

### Immediate actions (AP team)

1. **Place a system hold on Invoice 2 (1142-A)** before it advances further in the approval workflow.
2. **Confirm payment of Invoice 1** by pulling the ACH remittance detail and verifying the bank's cleared-payment record — do not rely solely on system status.
3. **Contact Northbridge Logistics AP/AR** with the cleared payment evidence (ACH trace number, payment date, amount). Request written confirmation that 1142-A is a duplicate and should be voided.
4. **Document the resolution** in the vendor file and attach the vendor's confirmation to Invoice 2's record before marking it as a duplicate/closed.

### If the vendor disputes (edge case)
- Request a goods receipt or service confirmation tied to PO 6710 that post-dates Feb 8.
- Request the vendor's own AR ledger showing what they believe is outstanding.
- If no supporting documentation can be produced, reject Invoice 2 formally in writing.

### Escalation triggers
- If amounts or PO lines had minor differences, escalate to procurement to verify whether a change order occurred.
- If the vendor cannot be reached within 5 business days, escalate to the Vendor Management or Procurement team per your vendor dispute SOP.

---

## 4. Automated Duplicate-Detection Rules for a P2P System

A well-designed procure-to-pay system should run these checks at **invoice ingestion** (before human review), not after approval.

### Tier 1 — Hard Blocks (auto-reject / mandatory hold)

| Rule ID | Logic | Rationale |
|---------|-------|-----------|
| **DUP-01** | Same vendor ID + exact invoice number + exact amount → block | Trivial exact duplicate |
| **DUP-02** | Same vendor ID + same PO reference + same amount + status = "Paid" → block | Prevents double payment on closed PO |
| **DUP-03** | Same vendor ID + same invoice number (case-insensitive, stripped of whitespace) + amount within ±0% → block | Catches formatting variants of same number |

### Tier 2 — Fuzzy Holds (route to AP review queue with duplicate flag)

| Rule ID | Logic | Threshold / Parameters |
|---------|-------|----------------------|
| **DUP-04** | Same vendor ID + invoice number similarity score ≥ 85% (edit distance / Jaro-Winkler) + same amount | Catches prefix/suffix changes like "NB-2024-1142" vs. "1142-A" |
| **DUP-05** | Same vendor ID + same PO line(s) + same amount + invoice date within *N* days of existing invoice | Configurable window, typically 30–60 days |
| **DUP-06** | Same vendor ID + same amount + same invoice date ± *N* days + no distinct PO/receipt reference | Catches invoices with no PO ref but suspicious amount/date match |
| **DUP-07** | Same vendor ID + invoice number contains numeric substring of an existing paid invoice | Catches reformatted resubmissions (1142 appearing inside 1142-A, REV-1142, etc.) |

### Tier 3 — Behavioral / Statistical Signals (feed to fraud/analytics dashboard)

| Rule ID | Logic | Purpose |
|---------|-------|---------|
| **DUP-08** | Vendor submits invoice within *X* days of confirmed ACH/check payment for same PO | Flag likely AR communication lag vs. intentional resubmission |
| **DUP-09** | Vendor has >2 duplicate flags in rolling 12 months | Triggers vendor master review and potential audit |
| **DUP-10** | Invoice amount matches a prior paid invoice exactly AND falls just below an approval threshold | Combines duplicate and threshold-splitting detection |

### Implementation Design Principles

```
Invoice Received
      │
      ▼
[Normalize data]  ← strip whitespace, standardize case, parse amounts
      │
      ▼
[Tier 1 Rules]  ─── Hard match? ──► Auto-hold + notify AP manager
      │ No hard match
      ▼
[Tier 2 Rules]  ─── Fuzzy match? ──► Route to AP review with match explanation
      │ No fuzzy match                  (show matched invoice side-by-side)
      ▼
[Tier 3 Rules]  ─── Behavioral flag? ──► Log to analytics; soft alert
      │
      ▼
[Normal approval workflow]
```

**Key design requirements:**
- Rules must fire **before** the invoice is visible to approvers, to prevent approval under time pressure.
- Match explanations must be **human-readable** (e.g., "This invoice matches paid invoice NB-2024-1142 on vendor, PO, and amount; invoice numbers differ by suffix only").
- Rules should be **tunable by vendor** — a high-volume vendor may legitimately send many invoices against one PO (blanket POs), requiring adjusted thresholds.
- All holds must generate an **audit trail** with timestamp, rule triggered, and resolution action.

---

## Summary

> **These invoices are almost certainly a duplicate.** The exact match on vendor, amount, and PO number combined with the payment status of Invoice 1 and the resubmission-patterned invoice number of Invoice 2 present an overwhelming case. Invoice 2 should be placed on hold immediately, payment confirmation shared with the vendor, and the invoice closed as a duplicate upon vendor acknowledgment. A P2P system with Tier 1 rule DUP-02 (same vendor + same PO + same amount + prior paid status) would have caught this automatically at ingestion, before any human review was required.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** Identifies the duplicate with high confidence, cites all key signals (vendor, amount, PO, invoice-number family with -A suffix pattern, 14-day timing gap, payment status). Provides a control-aware resolution workflow including hold, ACH verification, vendor contact, documentation, and escalation. Lists 10 automated detection rules organized in tiers, including DUP-02 which explicitly catches this exact case (vendor + PO + amount + paid status) and DUP-04 for the fuzzy invoice number match.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_004 — invoice_processing · medium · **score 2/2** (model: `claude-haiku-4-5`)

_Expected failure mode: pattern matching and control logic_

### Question

Are these two invoices a duplicate? Walk through the signals you would use, recommend a resolution, and describe the duplicate-detection rules a P2P system should run automatically to catch this pattern.

### Context

```
Invoice 1
  Supplier:    Northbridge Logistics LLC (vendor #V-44120)
  Invoice #:   NB-2024-1142
  Invoice date: 2026-02-08
  Amount:      $4,287.50
  PO ref:      6710
  Status:      Posted, paid via ACH on 2026-02-19

Invoice 2
  Supplier:    Northbridge Logistics LLC (vendor #V-44120)
  Invoice #:   1142-A
  Invoice date: 2026-02-22
  Amount:      $4,287.50
  PO ref:      6710
  Status:      Submitted, awaiting AP review
```

### Rubric

- **0**: Says it is not a duplicate, or pays the second invoice, or misses the PO/amount/vendor co-occurrence
- **1**: Identifies the duplicate but only cites one or two signals, or omits the resolution workflow, or omits automated detection rules
- **2**: Identifies it as a duplicate citing multiple signals (amount + vendor + PO + invoice-number family + timing), gives a control-aware resolution path, and lists at least three automated detection rules including the one that catches this exact case

### Ideal answer

Yes, this is a duplicate with very high confidence. Signals:

- Same vendor (V-44120, exact).
- Same amount to the cent ($4,287.50). Identical to-the-cent amounts within a short window from the same vendor are the single strongest duplicate signal.
- Same PO reference (6710). Two distinct invoices for the same PO and the same amount is highly unusual unless the PO was for two identical milestone payments — in which case the supplier would normally use distinct invoice numbers and reference the milestones.
- Invoice numbers are near-identical: 'NB-2024-1142' and '1142-A'. The '-A' suffix is a textbook resubmission pattern — vendors append it when they believe the original was lost, rejected, or unpaid. The vendor here likely re-sent because they did not see payment confirmation between 02-08 (issue) and 02-22 (resubmit), even though payment ran on 02-19.
- 14-day gap is consistent with a resubmission cycle, not a separate billing event.

Resolution path:
- Do not pay Invoice 2.
- AP clerk posts a 'suspected duplicate' hold; routes to AP supervisor (segregation: clerk identifies, supervisor confirms).
- Pull the remittance for Invoice 1 (2026-02-19 ACH) and email the supplier with the remittance reference; ask them to confirm receipt and to void Invoice 2 in their system.
- Document the disposition for the SOX duplicate-payment control workpaper.
- If Invoice 1 was actually voided/canceled before pay (it was not, here), then Invoice 2 might be a legitimate resubmission — only then process under the original PO.

Duplicate-detection rules a P2P system should run:
1. Exact match on (vendor + invoice_number) — catches re-keying.
2. Exact match on (vendor + amount + invoice_date within ±N days, e.g. 30) — catches the same invoice resubmitted under a slightly different number.
3. Fuzzy match on invoice_number (Levenshtein distance ≤ 2, or shared substring ≥ 6 chars) within a vendor — catches the '1142' / '1142-A' / 'NB-2024-1142' family.
4. (vendor + amount + PO + invoice_date within window) — catches the case here even when invoice numbers differ entirely.
5. Cross-vendor amount match within window — catches duplicate payments across two duplicate vendor records (relates to q_001).
6. Reverse-amount match — catches a credit memo paired against a re-billed invoice for the same amount.

The (vendor + amount + PO + window) rule is what would have caught this case automatically.

### Model response

# Duplicate Invoice Analysis

## Signal Assessment

| Signal | Invoice 1 | Invoice 2 | Risk Level |
|--------|-----------|-----------|-----------|
| **Supplier** | Northbridge Logistics LLC (V-44120) | Northbridge Logistics LLC (V-44120) | 🔴 CRITICAL |
| **Amount** | $4,287.50 | $4,287.50 | 🔴 CRITICAL |
| **PO Reference** | 6710 | 6710 | 🔴 CRITICAL |
| **Invoice #** | NB-2024-1142 | 1142-A | 🟡 MODERATE |
| **Invoice Date** | 2026-02-08 | 2026-02-22 | 🟡 MODERATE |
| **Payment Status** | Already paid (2026-02-19) | Pending review | 🔴 CRITICAL |

## Analysis

**Likelihood: Very High (95%+ confidence this is a duplicate)**

The convergence of three critical signals—identical vendor, identical amount, and identical PO reference—is highly suspicious. The nearly identical invoice numbers (NB-2024-1142 vs. 1142-A) and 14-day gap suggest this could be:
1. **Duplicate submission** by the vendor (most likely)
2. **Amended invoice** that should have replaced the original (less likely, would typically show clear notation)
3. **System error** resubmitting the same invoice with variant numbering

The fact that Invoice 1 is already paid via ACH makes paying Invoice 2 particularly dangerous.

---

## Recommended Resolution

1. **Immediate Action**: Flag Invoice 2 as "Hold Pending Investigation"
2. **Contact Northbridge Logistics**: Request clarification on whether 1142-A is:
   - A duplicate (request withdrawal)
   - A separate charge (request supporting documentation)
   - An amended invoice (request explanation of differences)
3. **Do NOT approve/pay** Invoice 2 until confirmed
4. **Document** the hold reason and vendor response
5. **If confirmed duplicate**: Reject Invoice 2 and notify vendor of duplicate submission policy

---

## Automated Duplicate Detection Rules

A robust P2P system should implement these rules in sequence:

### **Tier 1: Exact Match Rules** (Block immediately)
```
IF (vendor_ID = previous AND 
    amount = previous AND 
    PO_ref = previous AND 
    invoice_date within 90 days)
THEN flag = "PROBABLE_DUPLICATE" 
     action = "HOLD"
```

### **Tier 2: High-Confidence Patterns** (Manual review required)
```
IF (vendor_ID = previous AND 
    amount = previous AND 
    PO_ref = previous AND 
    invoice_date within 90 days AND
    payment_status_1 = "PAID")
THEN flag = "HIGH_RISK_DUPLICATE_PAID"
     action = "ESCALATE_TO_MANAGER"
     alert = "PREVENT_DUPLICATE_PAYMENT"
```

### **Tier 3: Similar Invoice Numbers** (Investigate)
```
IF (vendor_ID = previous AND 
    amount = previous AND 
    invoice_number_similarity ≥ 85%)
THEN flag = "VARIANT_INVOICE_NUMBER"
     action = "HOLD_AND_REVIEW"
```

### **Tier 4: 3-Way Match Failures** (Validation)
```
IF (PO_amount ≠ invoice_amount OR
    invoice_qty ≠ PO_qty)
THEN flag = "3WAY_MISMATCH"
     action = "REQUIRE_EXCEPTION_APPROVAL"
```

### **Tier 5: Payment Duplicate Check** (Preventive)
```
BEFORE payment_approval:
IF (vendor_ID + amount + PO_ref 
    exists in paid_invoices within 60 days)
THEN block_payment = TRUE
     alert = "DUPLICATE_PAYMENT_ATTEMPTED"
```

---

## Additional System Controls

- **Vendor duplicate submission monitoring**: Track frequency from each vendor
- **Email notification rule**: Alert AP manager when similar invoices detected
- **Workflow requirement**: Mandatory review for any holds before approval
- **Audit trail**: Maintain full history of flagged invoices and resolutions
- **Reconciliation report**: Monthly report of caught duplicates and vendor patterns

This multi-layered approach catches the duplicate at system level, preventing financial loss and vendor compliance issues.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the duplicate with high confidence, cites multiple signals (vendor, amount, PO, invoice number similarity, timing/14-day gap, payment status), provides a control-aware resolution path (hold, contact vendor, do not pay, document, reject if confirmed), and lists multiple automated detection rules including the critical (vendor + amount + PO + date window) rule that catches this exact case. It also includes invoice number similarity matching for the '1142'/'1142-A' family.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_006 — trade_and_tax · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: applying domain conventions (cross-border tax)_

### Question

A new supplier has provided a W-9. Is the form valid for this entity? What forms should AP request, what withholding applies, and what year-end reporting is required? Spend will be ~$50,000/year for consulting services performed partly in the US.

### Context

```
Supplier setup packet:
  Legal name on W-9:  Crescent Advisory LLC
  Federal classification box checked: 'Individual/sole proprietor or single-member LLC'
  TIN provided:       SSN of the LLC's owner
  Owner:              Mr. A. Vasquez, citizen and resident of Mexico (per supplier's onboarding form)
  Entity formation:   Delaware single-member LLC
  Services:           Consulting; ~60% of work performed at client US offices, ~40% performed remotely from Mexico
  Contract value:     $50,000/year
```

### Rubric

- **0**: Accepts the W-9, or issues a 1099 to the owner, or claims that a foreign-owned single-member LLC is a US person for withholding
- **1**: Recognizes that W-8BEN is required and that 1042-S applies, but mishandles source-of-income (treats all $50k as US-source or all as foreign), or omits the treaty/PE analysis, or misses the disregarded-entity reasoning
- **2**: Correctly identifies the disregarded-entity rule, requests W-8BEN from the owner, splits US-source vs. foreign-source by where services are performed, addresses 30% default and treaty/PE considerations, and identifies 1042/1042-S (not 1099) as year-end reporting

### Ideal answer

The W-9 is invalid for this entity. A US single-member LLC with a foreign owner is treated as a 'disregarded entity' for US federal tax purposes (Treas. Reg. §301.7701-3); the LLC itself is disregarded and the owner is the relevant tax person. Because the owner is a non-resident alien (NRA), the correct form is W-8BEN (not W-9). W-9 is only for US persons.

AP actions:
1. Reject the W-9. Request a Form W-8BEN from Mr. Vasquez personally (not from the LLC). The W-8BEN must include Mr. Vasquez's Mexican tax residence and, if claiming treaty benefits, his foreign TIN (RFC) and the relevant US-Mexico tax treaty article.
2. Determine source of income. US-source service income is FDAP if not ECI, and is determined by where the services are performed:
   - 60% performed in the US → US-source.
   - 40% performed in Mexico → foreign-source, generally not subject to US withholding.
3. Apply withholding. Default rate on US-source FDAP service income to an NRA is 30% (IRC §1441). The US-Mexico income tax treaty may reduce this for certain categories — for independent personal services / business profits, treaty relief generally requires that the NRA does not have a US permanent establishment / fixed base. If the consultant is regularly working at US offices, examine whether a fixed base exists; if it does, treaty relief may not apply and the income could be ECI taxable on a net basis (in which case the consultant files Form 1040-NR and the withholding regime differs).
4. Documentation. Retain the W-8BEN; renew every 3 years or sooner if circumstances change. Maintain a contemporaneous record allocating service days US vs. foreign — that allocation is the basis for the source determination and is auditable.
5. Year-end reporting. File Form 1042-S (not 1099-NEC or 1099-MISC) reporting the gross US-source amount paid and the tax withheld; file Form 1042 transmittal. 1099 reporting does not apply because the payee is a foreign person.

References: IRS Publication 515 (Withholding of Tax on Nonresident Aliens and Foreign Entities), Form W-8BEN instructions, IRC §§1441, 1442, 861, Treas. Reg. §301.7701-3.

### Model response

# Analysis: Crescent Advisory LLC Supplier Setup

## 1. Is the W-9 Valid? **No.**

A W-9 may only be signed by a **U.S. person** (U.S. citizen, U.S. resident alien, domestic entity, or domestic estate/trust). Here, the critical issue is the look-through rule for single-member LLCs:

- A domestic single-member LLC (SMLLC) that has not elected corporate treatment is a **disregarded entity** for U.S. tax purposes.
- For Forms W-9/W-8, you look through the LLC to its **owner**.
- The owner, Mr. Vasquez, is a **nonresident alien (NRA)** — a Mexican citizen and resident.
- An NRA is **not a U.S. person** and cannot sign a W-9, regardless of whether the LLC was formed in Delaware. Delaware formation is irrelevant; tax status follows the owner.
- The "Individual/sole proprietor or single-member LLC" box being checked with the owner's SSN actually confirms disregarded-entity treatment — which makes the W-9 invalid because the regarded taxpayer is foreign.

The W-9 must be **rejected**.

## 2. Forms AP Should Request

Request the appropriate **Form W-8** from the *owner* (the disregarded LLC itself does not file a W-8 in its own name — the beneficial owner does, and may note the DRE's name on the appropriate line):

- **Form W-8BEN** — for Mr. Vasquez as an individual NRA beneficial owner.
  - Part I: Mr. Vasquez's name, Mexican address, country of citizenship, and foreign TIN (Mexican RFC) or U.S. ITIN if he has one.
  - The DRE's name and U.S. address may be entered on line 7 (reference) so payments routed to the LLC tie to the W-8.
  - Part II: He may claim **U.S.–Mexico income tax treaty** benefits (Article 14, Independent Personal Services, or Article 7, Business Profits — depending on facts) for the portion of services performed in the U.S., **but only if he has no U.S. fixed base/permanent establishment and meets the day-count tests**. Given ~60% of work is performed onsite at U.S. client offices, a fixed base or PE is plausible; treaty relief may not be available. A U.S. TIN (ITIN/SSN) is required to claim treaty benefits.

Additionally collect:
- A **services allocation statement** from the supplier identifying the portion of compensation attributable to services performed inside vs. outside the U.S. (this drives sourcing and withholding).

If the supplier refuses to provide a W-8, treat as undocumented foreign payee → presume foreign and apply 30% withholding on U.S.-source amounts.

## 3. Withholding Analysis

Source of personal services income is determined by **where the services are performed** (IRC §861(a)(3) / §862(a)(3)):

| Component | Sourcing | Treatment |
|---|---|---|
| ~60% performed in the U.S. (~$30,000) | **U.S.-source** compensation to an NRA for personal services | Subject to NRA withholding |
| ~40% performed in Mexico (~$20,000) | **Foreign-source** | Not subject to U.S. withholding or 1042-S reporting; not reportable on 1099 |

**Withholding rate on the U.S.-source portion:**
- Default: **30%** under IRC §1441 (NRA withholding on FDAP / compensation for personal services).
- Possible **graduated withholding via Form 8233** if the services are treated as those of an independent contractor employee-like arrangement — but typically for a contractor relationship, §1441 30% applies and **Form 8233** is the vehicle to claim a treaty exemption for personal services compensation. (Form W-8BEN is generally for FDAP other than personal services compensation; **Form 8233 is the correct form to claim treaty exemption on compensation for independent personal services performed in the U.S.**)
- **Correction/best practice:** For the U.S.-performed services portion, request **Form 8233** (not W-8BEN) if Mr. Vasquez wants to claim U.S.–Mexico treaty benefits on that compensation. Form 8233 requires a U.S. TIN (ITIN or SSON). Submit Form 8233 to the IRS and wait 10 days before reducing withholding.
- For the foreign-performed (Mexico) portion: no U.S. withholding regardless of documentation, because the income is foreign-source.

**Practical posture absent a valid 8233 with treaty claim:** withhold **30% on the ~$30,000 U.S.-source portion** = $9,000/year.

**Note on the §1446(f) / ECI consideration:** Compensation for personal services performed in the U.S. by an NRA is generally **ECI** (effectively connected income), but payors of compensation for independent personal services apply §1441 30% gross withholding (not §1446) unless 8233 reduces it. The recipient files Form 1040-NR to true up.

## 4. Year-End Reporting

- **Form 1042-S** — issued to Mr. Vasquez (with DRE info as applicable) reporting the **U.S.-source** gross amount paid and tax withheld. Income code typically **17** (independent personal services) or **16** (scholarship/other) — use **17** here. Recipient code: individual.
- **Form 1042** — annual withholding tax return filed by the payor reporting aggregate 1042-S amounts and depositing withheld tax (deposits per the §1461 schedule).
- **Form 1042-T** — transmittal for paper 1042-S filings.
- **Do NOT issue Form 1099-NEC.** A 1099 is issued only to U.S. persons; using a 1099 here would be incorrect even though the LLC has a U.S. EIN/SSN.
- The **foreign-source portion** (~$20,000) is **not reported** on either 1099 or 1042-S.

## 5. Summary Action List for AP

1. **Reject the W-9.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the disregarded entity rule, rejects the W-9, requests W-8BEN (and additionally Form 8233 for treaty claim on personal services—which is actually more technically accurate than the ideal answer), splits source by where services are performed (60% US/40% Mexico), addresses the 30% default withholding under §1441, discusses treaty/PE/fixed base considerations, and correctly identifies 1042/1042-S reporting (not 1099). All rubric elements for a score of 2 are met.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_006 — trade_and_tax · medium · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: applying domain conventions (cross-border tax)_

### Question

A new supplier has provided a W-9. Is the form valid for this entity? What forms should AP request, what withholding applies, and what year-end reporting is required? Spend will be ~$50,000/year for consulting services performed partly in the US.

### Context

```
Supplier setup packet:
  Legal name on W-9:  Crescent Advisory LLC
  Federal classification box checked: 'Individual/sole proprietor or single-member LLC'
  TIN provided:       SSN of the LLC's owner
  Owner:              Mr. A. Vasquez, citizen and resident of Mexico (per supplier's onboarding form)
  Entity formation:   Delaware single-member LLC
  Services:           Consulting; ~60% of work performed at client US offices, ~40% performed remotely from Mexico
  Contract value:     $50,000/year
```

### Rubric

- **0**: Accepts the W-9, or issues a 1099 to the owner, or claims that a foreign-owned single-member LLC is a US person for withholding
- **1**: Recognizes that W-8BEN is required and that 1042-S applies, but mishandles source-of-income (treats all $50k as US-source or all as foreign), or omits the treaty/PE analysis, or misses the disregarded-entity reasoning
- **2**: Correctly identifies the disregarded-entity rule, requests W-8BEN from the owner, splits US-source vs. foreign-source by where services are performed, addresses 30% default and treaty/PE considerations, and identifies 1042/1042-S (not 1099) as year-end reporting

### Ideal answer

The W-9 is invalid for this entity. A US single-member LLC with a foreign owner is treated as a 'disregarded entity' for US federal tax purposes (Treas. Reg. §301.7701-3); the LLC itself is disregarded and the owner is the relevant tax person. Because the owner is a non-resident alien (NRA), the correct form is W-8BEN (not W-9). W-9 is only for US persons.

AP actions:
1. Reject the W-9. Request a Form W-8BEN from Mr. Vasquez personally (not from the LLC). The W-8BEN must include Mr. Vasquez's Mexican tax residence and, if claiming treaty benefits, his foreign TIN (RFC) and the relevant US-Mexico tax treaty article.
2. Determine source of income. US-source service income is FDAP if not ECI, and is determined by where the services are performed:
   - 60% performed in the US → US-source.
   - 40% performed in Mexico → foreign-source, generally not subject to US withholding.
3. Apply withholding. Default rate on US-source FDAP service income to an NRA is 30% (IRC §1441). The US-Mexico income tax treaty may reduce this for certain categories — for independent personal services / business profits, treaty relief generally requires that the NRA does not have a US permanent establishment / fixed base. If the consultant is regularly working at US offices, examine whether a fixed base exists; if it does, treaty relief may not apply and the income could be ECI taxable on a net basis (in which case the consultant files Form 1040-NR and the withholding regime differs).
4. Documentation. Retain the W-8BEN; renew every 3 years or sooner if circumstances change. Maintain a contemporaneous record allocating service days US vs. foreign — that allocation is the basis for the source determination and is auditable.
5. Year-end reporting. File Form 1042-S (not 1099-NEC or 1099-MISC) reporting the gross US-source amount paid and the tax withheld; file Form 1042 transmittal. 1099 reporting does not apply because the payee is a foreign person.

References: IRS Publication 515 (Withholding of Tax on Nonresident Aliens and Foreign Entities), Form W-8BEN instructions, IRC §§1441, 1442, 861, Treas. Reg. §301.7701-3.

### Model response

# W-9 / Tax Compliance Analysis: Crescent Advisory LLC

---

## 1. Is the W-9 Valid?

**No — the W-9 is invalid and should be rejected.**

### Problems with the submitted W-9

| Issue | Why It Matters |
|---|---|
| **W-9 is the wrong form entirely** | W-9 is for U.S. persons (citizens, resident aliens, domestic entities). A single-member LLC owned by a nonresident alien (NRA) is itself treated as a foreign person for U.S. tax purposes. |
| **SSN used as TIN** | The owner is a Mexican citizen and resident — he almost certainly does not have (or is not entitled to use) an SSN for this purpose; even if he had an ITIN, that still would not make the W-9 correct. |
| **Federal classification box** | "Individual/sole proprietor or single-member LLC" is checked, but a disregarded LLC owned by an NRA is **disregarded up to the foreign owner** — the payee is treated as the foreign individual, not as a domestic entity. |
| **Underlying representation is false** | By submitting a W-9, the vendor is implicitly certifying U.S. person status under penalties of perjury. That certification is incorrect. |

> **Regulatory basis:** Treas. Reg. §301.7701-2(a); §1.1441-1(b)(2)(ii); Rev. Proc. 2017-15; IRS Pub. 515. A domestic LLC that is disregarded and owned by a foreign person is treated as a **foreign person** — the LLC's U.S. formation state is irrelevant to its federal tax classification.

---

## 2. Correct Forms AP Should Request

### Step A — Substitute W-8BEN (Primary Form)

**Form W-8BEN** (Certificate of Foreign Status of Beneficial Owner for United States Tax Withholding and Reporting — Individuals)

- Completed by **Mr. A. Vasquez** as the beneficial owner
- Must include:
  - Full legal name
  - Country of citizenship (Mexico)
  - Permanent residence address in Mexico
  - Foreign TIN (RFC — *Registro Federal de Contribuyentes* — from Mexico's SAT) **or** ITIN if he has one
  - Signature + date (valid 3 years from date signed, absent change in circumstances)
- **No treaty claim is available on this form** in this fact pattern (explained below)

> **Why W-8BEN and not W-8BEN-E?** The LLC is disregarded; the beneficial owner is an individual. W-8BEN-E is for foreign entities that are *not* disregarded or that are treated as corporations. Here we look through the disregarded LLC to the NRA owner.

### Step B — Consider Requesting W-8ECI if Owner Has U.S. EIN and Will File

If the services are effectively connected with a U.S. trade or business (USTB) and the owner **will file** a U.S. Form 1040-NR, he could instead submit **Form W-8ECI** (Certificate of Foreign Person's Claim That Income Is Effectively Connected With the Conduct of a Trade or Business in the United States), naming the LLC's U.S. EIN. This would eliminate withholding but imposes a filing obligation. AP should request this only if the vendor proactively raises it and provides a U.S. EIN.

---

## 3. Withholding Analysis

### Threshold Question: Is the Income "Fixed, Determinable, Annual, or Periodical" (FDAP) or Effectively Connected Income (ECI)?

| Category | Withholding Rule |
|---|---|
| **FDAP — U.S.-source income** | 30% withholding under §1441 |
| **ECI** | NRA files 1040-NR; graduated rates apply; withholding may be reduced/eliminated via W-8ECI |

Consulting fees to an NRA can be either, depending on facts. Here, ~60% is performed at U.S. client offices → that portion is almost certainly U.S.-source income. The analysis:

### Source of Income Rules for Personal Services (§861(a)(3) / §862(a)(3))

- Income from personal services is sourced **where the services are performed**
- ~60% performed in the U.S. → **U.S.-source income**
- ~40% performed in Mexico → **foreign-source income** (not subject to U.S. withholding)

### Withholding Calculation (Default — W-8BEN with No Treaty Claim)

| Income Component | Amount | Rate | Withholding |
|---|---|---|---|
| U.S.-source portion (60%) | $30,000 | 30% | **$9,000** |
| Foreign-source portion (40%) | $20,000 | 0% | $0 |
| **Total annual withholding** | | | **$9,000** |

### Treaty Consideration — U.S.–Mexico Treaty

The U.S.-Mexico Income Tax Treaty (1992, as amended) **Article 14 (Independent Personal Services)** and **Article 7 (Business Profits)** may reduce or eliminate withholding. However:

- Treaty benefits require a **permanent establishment (PE)** / **fixed base** analysis
- If Vasquez has a fixed base or PE in the U.S. (arguable given 60% of work at client offices — though likely not sufficient to constitute a fixed base if he has no dedicated office), the U.S. may still tax
- **More commonly:** Article 14 exempts NRA independent services income from U.S. tax if the individual does **not** have a fixed base regularly available in the U.S.
- Whether client offices constitute a "fixed base" is a facts-and-circumstances test — AP should **not** make this determination unilaterally

> **AP's conservative position:** Withhold at 30% on the U.S.-source portion **unless and until** the vendor provides a W-8BEN with a valid treaty claim (Part II of W-8BEN) supported by a Tax Residency Certificate (*Constancia de Residencia Fiscal*) from Mexico's SAT, and your legal/tax team approves the treaty position.

### Note on the §861(a)(3) De Minimis Exception
Under §861(a)(3), compensation for personal services performed in the U.S. is *not* U.S.-source if: (a) the NRA is present in the U.S. fewer than 90 days in the tax year, (b) compensation does not exceed $3,000, and (c) the services are for a foreign employer. None of these conditions appear to be met here ($50,000 contract; U.S. client). This exception does **not** apply.

---

## 4. Year-End Reporting

### Form 1042 and 1042-S (Not 1099)

| Form | Filed By | Due Date | Purpose |
|---|---|---|---|
| **Form 1042-S** (per payee) | Withholding agent (your company) | March 15 of following year | Reports income paid to foreign person and tax withheld; copy to vendor |
| **Form 1042** (aggregate) | Withholding agent | March 15 of following year | Annual withholding tax return summarizing all NRA payments |

- **No Form 1099** should be issued — 1099 is for U.S. persons only
- Income code on 1042-S: **Code 42** (other income) or **Code 27** (other U.S.-source income) — most likely **Code 42** for independent personal services
- Exemption code if treaty applies: **Code 04** (exempt under tax treaty)
- Chapter 3 status code: **16** (Individual)
- Recipient's country code: **MX**

### Deposit Requirements
- Withheld taxes must be deposited via **EFTPS**
- Quarterly deposits required if withholding < $2,000/quarter threshold; otherwise monthly or more frequently per §1461 regulations
- On $9,000/year withheld: likely **quarterly deposits** ($2,250/quarter)

---

## 5. Additional Compliance Considerations

### ITIN / Foreign TIN
- If the vendor does not have a U.S. ITIN or EIN, AP should still accept the W-8BEN with the Mexican RFC number (foreign TIN) — the IRS accepts foreign TINs on W-8 series forms
- If no TIN of any kind is provided, AP

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the disregarded entity rule with proper regulatory citations, requests W-8BEN from the owner (not the LLC), correctly splits US-source (60%) vs foreign-source (40%) based on where services are performed, addresses the 30% default withholding rate under §1441, discusses the US-Mexico treaty and PE/fixed base analysis, and correctly identifies Forms 1042 and 1042-S as the year-end reporting (explicitly noting 1099 is inappropriate). It even adds useful detail on the §861(a)(3) de minimis exception, W-8ECI alternative, and deposit requirements.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_007 — trade_and_tax · hard · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: assumption generation across jurisdictions_

### Question

Is the German VAT correctly charged on this invoice? What should AP do, and is the VAT reclaimable? Reason from EU VAT place-of-supply rules.

### Context

```
Buyer:    US-incorporated company with no EU permanent establishment, but registered for German VAT (DE VAT ID DE123456789) because of an earlier consignment-stock arrangement.
Supplier: German consulting firm, registered for VAT in Germany only.
Service:  Strategy consulting, performed remotely from Germany, deliverable consumed by the buyer's US headquarters (the German VAT registration is unrelated to this engagement).

Supplier invoice:
  Net fee:           €40,000.00
  German VAT 19%:     €7,600.00
  Invoice total:     €47,600.00
  Buyer's DE VAT ID is shown on the invoice header.
  Note line: 'VAT charged per German law.'
```

### Rubric

- **0**: Accepts the VAT as charged, or claims it is reclaimable simply because a DE VAT ID exists, or applies reverse charge between two German parties
- **1**: Correctly identifies that VAT should not have been charged but reasons via reverse charge instead of out-of-scope, or omits the Article 22 establishment-confirmation step, or does not address reclaim mechanics
- **2**: Correctly identifies the place of supply as the US under Article 44 based on which establishment consumes the service, distinguishes out-of-scope from reverse charge, recommends invoice rejection plus Article 22 establishment confirmation, and addresses why reclaim is not the right path

### Ideal answer

The VAT is incorrectly charged. The analysis turns on the EU VAT place-of-supply rules and which 'capacity' the buyer is acting in.

B2B services place of supply (Council Directive 2006/112/EC Article 44): for services supplied to a taxable person, the place of supply is where the customer is established or has a fixed establishment to which the service is supplied. Two facts here:

1. The buyer's establishment is the US (no EU permanent establishment).
2. The deliverable is consumed by the US headquarters; the German VAT registration is incidental and unrelated to this engagement.

Therefore the place of supply is the US, which is outside the EU VAT system. The supply is outside the scope of EU VAT. The German supplier should not have charged German VAT.

The presence of the buyer's DE VAT ID on the invoice does not, by itself, change the place of supply — Article 44 is about where the customer is established for the service consumed, not which VAT IDs the customer happens to hold. A buyer with multiple establishments must communicate to the supplier which establishment is receiving the service (Implementing Regulation 282/2011, Article 22). The supplier's apparent default to 'this is German because we see a DE VAT ID' is incorrect when the deliverable is consumed elsewhere.

Note: had the service been received by the buyer's German activity (the consignment-stock operation), the place of supply would be Germany, and the supplier would charge German VAT, which the buyer could reclaim via its German VAT return. That is the alternate fact pattern.

The distinct 'reverse charge' question: if the place of supply had been Germany but the supplier and customer were in different EU states with both VAT-registered, Article 196 reverse charge would apply (customer self-accounts). That is not this case because both parties are in Germany for VAT purposes if the German establishment is the recipient. Reverse charge does not apply to a US-recipient supply because the US is outside EU VAT entirely — it is simply out of scope.

AP action:
1. Reject the invoice. Email the supplier explaining that under Article 44 the place of supply is the US (the establishment consuming the service), not Germany, and that the deliverable is unrelated to the buyer's German VAT registration.
2. Provide written confirmation of which establishment is receiving the service (Implementing Regulation 282/2011, Article 22) — this is the supplier's documentation requirement to avoid charging VAT.
3. Request a corrected invoice for €40,000 net, no VAT, with a note 'Outside scope of EU VAT — place of supply outside EU per Article 44, Directive 2006/112/EC.'
4. Reclaimability: not applicable. The €7,600 is not VAT properly due; it is not reclaimable through the German VAT return because the underlying supply is out of scope. If the supplier refuses to credit and reissue, the buyer would have to pay €47,600 and pursue an Article 13th Directive refund (refund to non-EU established taxable persons) or, more practically, dispute with the supplier — but the right answer is to fix the invoice, not to reclaim VAT that should never have been charged.

References: Council Directive 2006/112/EC Articles 44, 196; Council Implementing Regulation 282/2011 Articles 10–13, 21–22; 13th VAT Directive 86/560/EEC (refund to non-EU businesses).

### Model response

# Analysis: Is the German VAT Correctly Charged?

## Short Answer
**No, the German VAT is incorrectly charged.** AP should reject the invoice and request a corrected one with no VAT. The €7,600 is **not reclaimable** in its current form.

---

## Reasoning from EU Place-of-Supply Rules

### Step 1: Classify the service and the customer
- **Service type:** Strategy consulting — a general B2B service with no special place-of-supply rule (not real estate, not events admission, not transport, etc.).
- **Customer status:** A US-incorporated company is a **taxable person** (business) for VAT purposes. The fact that it has no EU permanent establishment does not change this — possession of a VAT ID is evidence of taxable-person status, but the substantive test is whether the recipient carries on an economic activity.

### Step 2: Apply the B2B general rule (Art. 44 VAT Directive 2006/112/EC; §3a(2) UStG)
For B2B general services, the place of supply is **where the customer is established** (or has the fixed establishment that receives the service).

- The buyer's **business establishment is in the US**.
- The buyer has **no fixed establishment in Germany** (or anywhere in the EU). The German VAT registration exists only because of a consignment-stock arrangement; a VAT registration is **not** a fixed establishment.
- The deliverable is consumed at US HQ, confirming the recipient is the US head office.

➡️ **Place of supply = United States.** The transaction is **outside the scope of EU VAT entirely.**

### Step 3: Why the buyer's German VAT ID on the invoice is a red herring
A VAT ID alone does not determine place of supply. Under Art. 44 VATD and the CJEU's reasoning (e.g., *Welmory*, C-605/12), what matters is the establishment that actually **receives and uses** the service. Here, the recipient is the US HQ. The supplier should have:
- obtained evidence of the customer's status and the establishment receiving the service (Art. 21–22 of Implementing Regulation 282/2011),
- concluded the service is supplied outside the EU,
- issued an invoice **without VAT**, with a note such as *"Not subject to German VAT — place of supply outside the EU, §3a(2) UStG / Art. 44 VATD."*

### Step 4: Why even a "reverse-charge to the DE VAT ID" answer would be wrong
One might be tempted to argue: "The buyer has a German VAT ID, so treat it as a German B2B supply with reverse charge." That is incorrect because:
- The German registration relates to a **different activity** (consignment stock) and the recipient establishment of *this* service is the US HQ.
- §3a(2) UStG looks to the establishment to which the service is rendered, not to any VAT ID the customer happens to hold.
- Therefore there is no German taxable transaction at all — neither a forward-charge nor a reverse-charge one.

### Step 5: Reclaimability of the €7,600 as charged

| Route | Available? | Why |
|---|---|---|
| Deduction via German VAT return (the buyer files DE returns due to consignment stock) | **No** | VAT incorrectly charged ("Steuer unrichtig ausgewiesen", §14c UStG) is **not deductible input VAT** per settled CJEU case law (*Genius Holding* C-342/87; *Stadeco* C-566/07) and BFH practice. |
| 13th Directive refund (Dir. 86/560/EEC) for non-EU businesses | **No** | Same reason — only correctly charged VAT is refundable; also Germany applies a reciprocity test for US claimants, and the buyer is registered in DE anyway. |
| Recovery from the supplier | **Yes** | The supplier must issue a corrected invoice and refund the €7,600. The supplier then corrects its own output VAT with the Finanzamt under §14c(1) UStG. |

---

## What AP Should Do

1. **Do not pay the VAT portion.** Pay only the net €40,000 — or, preferably, hold the entire invoice pending correction.
2. **Reject the invoice** and request a corrected invoice from the German consultant showing:
   - Net €40,000, no VAT,
   - The buyer's US address as the recipient establishment (the DE VAT ID should be removed or, at minimum, not used as the basis for invoicing this engagement),
   - A reference such as: *"Nicht steuerbar in Deutschland — Ort der sonstigen Leistung im Drittland, §3a Abs. 2 UStG / Art. 44 MwStSystRL."*
3. **Do not attempt to deduct the €7,600** in any German VAT return the buyer files for its consignment-stock activity — this would expose the buyer to assessment, interest, and penalties.
4. **Document the analysis** (recipient establishment, use of the deliverable at US HQ, irrelevance of the DE VAT ID for this service) in the engagement file to support the VAT-free treatment.
5. If the supplier refuses to correct, escalate — the supplier remains liable for the wrongly invoiced VAT under §14c UStG until the invoice is corrected, and the buyer has no path to recover it from the tax authority.

---

## Key Authorities
- **Art. 44, Council Directive 2006/112/EC** — B2B general place-of-supply rule.
- **§3a(2) UStG** — German implementation.
- **Arts. 20–22, Council Implementing Regulation (EU) 282/2011** — identifying the recipient establishment.
- **CJEU, *Welmory* (C-605/12)** — VAT registration ≠ fixed establishment.
- **CJEU, *Genius Holding* (C-342/87); *Stadeco* (C-566/07)** — no input-VAT deduction for incorrectly invoiced VAT.
- **§14c UStG** — supplier's liability and correction mechanism for wrongly charged VAT.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the place of supply as the US under Article 44 based on which establishment consumes the service, explicitly distinguishes out-of-scope from reverse charge (Step 4), recommends invoice rejection, references Article 22 of Implementing Regulation 282/2011 for establishment confirmation, and thoroughly addresses why reclaim is not the right path (with a clear table covering deduction, 13th Directive, and supplier recovery routes). It also adds valuable supporting authorities (Welmory, Genius Holding, §14c UStG).

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_008 — close_and_controls · hard · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: multi-step accounting (matching principle and clearing accounts)_

### Question

What is the correct accounting at month-end and the following month? Walk through the GR/IR (or accrual) postings and explain how this would look in an SAP-style services-PO setup vs. a manual accrual.

### Context

```
Today is 2026-03-31 (month-end close).
PO #4500-77002 — services PO with Strategy Consulting Co.
  PO total:    $200,000
  Services:    Q1 strategy engagement
  Status as of 2026-03-31: vendor's status report (received 2026-03-30) confirms $150,000 of services delivered through month-end; project is on track; remaining $50,000 will be delivered in April.
  No invoice received from vendor by close.
Invoice received 2026-04-12: $150,000 referencing PO #4500-77002, milestone 1.
```

### Rubric

- **0**: Accrues the full $200k, or recognizes the expense in April, or omits the reversing entry in the manual path, or confuses GR/IR with AP
- **1**: Recognizes $150k in March correctly but mixes up the manual-vs-SES paths, omits the GR/IR clearing mechanic, or does not flag that the remaining $50k is non-accruable
- **2**: Correctly accrues $150k in March only, presents both manual-with-reversal and SES-with-GR/IR paths with clean journal entries, addresses GR/IR aging review and SOX segregation, and explicitly excludes the $50k as non-accruable

### Ideal answer

Concept: the matching principle (ASC 720; IAS 1) requires that expense be recognized in the period the service is rendered, regardless of invoice timing. $150k of services were rendered in March, so $150k must hit March P&L. The remaining $50k is not accruable — services not yet rendered and there is no constructive obligation beyond the PO commitment.

Manual-accrual path (simpler, common in non-SAP environments):

March 31 — accrual entry:
  Dr. Consulting expense              $150,000
     Cr. Accrued liabilities (or 'Accrued expenses')  $150,000

April 1 — reversing entry (auto-reverse JE):
  Dr. Accrued liabilities              $150,000
     Cr. Consulting expense                            $150,000

April 12 — invoice posted normally:
  Dr. Consulting expense              $150,000
     Cr. Accounts payable                              $150,000

Net effect: March P&L = $150k expense (correct), April P&L = $0 net for this milestone (correct), AP open at $150k pending payment.

SAP-style services-PO path with Service Entry Sheet (SES):

March 30–31 — operations / project owner enters SES against PO #4500-77002 for $150k of milestone-1 services delivered. SES approval triggers automatic GR-equivalent posting:
  Dr. Consulting expense              $150,000
     Cr. GR/IR clearing account                        $150,000

April 12 — invoice receipt against the SES (logistics invoice verification, MIRO):
  Dr. GR/IR clearing                   $150,000
     Cr. Accounts payable                              $150,000

GR/IR clears to zero on the matched line. March P&L correctly reflects $150k. No reversing entry needed because the SES, not a manual JE, drove the expense.

Key points and audit considerations:
- The $50k of unrendered services must NOT be accrued. Accruing for not-yet-performed services would overstate March expense and is an audit finding.
- The accrual must be supported by evidence — here, the vendor's status report dated 2026-03-30 is the source document. Without contemporaneous evidence of services rendered, the accrual is unsupported.
- GR/IR balances are a standard month-end review focus: aged GR/IR items represent either unrecorded liabilities (services received not invoiced — should be in this bucket) or stale receipts that need investigation. The balance here will sit at $150k credit from March 31 until April 12, then clear.
- SOX P2P control: the role entering the SES (project owner) must be different from the AP role posting the invoice and from the role approving payment. Same segregation as q_003.
- If the vendor invoiced $160k in April (not $150k), the $10k delta would be a price/scope variance — exception per the 3-way logic in q_003, route to buyer.

### Model response

# Month-End Close Accounting for Services PO #4500-77002

## The Core Principle

Under accrual accounting (and ASC 606 / IFRS 15 from the customer's expense recognition perspective, mirrored against the vendor's revenue), expense is recognized **when services are received**, not when the invoice arrives or cash is paid. The vendor's status report dated 2026-03-30 is your evidence that $150,000 of services have been performed through 3/31. Therefore, $150,000 belongs in Q1 P&L regardless of invoice timing.

The $50,000 remaining is **not** accrued — those services have not yet been rendered (executory portion of the contract).

---

## Approach 1: SAP-Style Services PO with Service Entry Sheet (SES) / GR-based IV

In an SAP MM services-PO setup, the mechanism is a **Service Entry Sheet** (transaction ML81N) that functions as the services equivalent of a goods receipt. The PO is flagged "GR-based IV" so invoices must match an accepted SES.

### 3/31/2026 — Post and approve SES for $150,000 (milestone 1)

| Account | Dr | Cr |
|---|---|---|
| Consulting Expense (cost center) | 150,000 | |
| GR/IR Clearing – Services | | 150,000 |

- This is automatic on SES approval (acceptance).
- The PO commitment of $200,000 is reduced; $50,000 remains as open commitment.
- **No accrual JE is needed** — the SES *is* the accrual mechanism. GR/IR-Services sits on the balance sheet as a liability (effectively "received not invoiced").

### 4/12/2026 — Invoice receipt via MIRO, $150,000 referencing PO and SES

| Account | Dr | Cr |
|---|---|---|
| GR/IR Clearing – Services | 150,000 | |
| Accounts Payable – Vendor | | 150,000 |

- Three-way match: PO line ↔ SES ↔ invoice. GR/IR clears to zero for milestone 1.
- No P&L impact in April for milestone 1 — expense was already recognized in March.

### Later in April — when remaining services are delivered

A second SES for $50,000 is posted, generating Dr Expense / Cr GR/IR-Services, followed by the next invoice that clears GR/IR to AP.

### Why this is the preferred path
- Auditable: SES carries vendor confirmation, approver, date, PO reference.
- Self-reversing in the sense that GR/IR auto-clears on invoice — no manual reversal entry, no risk of double-counting.
- GR/IR aging report at any point shows received-but-not-invoiced exposure.

---

## Approach 2: Manual Accrual (PO not configured for SES, or services not entered timely)

If no SES is posted by close, the PO shows $0 received and no expense has hit the GL. Finance must book a **manual month-end accrual** based on the vendor status report.

### 3/31/2026 — Accrual JE (often booked as auto-reversing)

| Account | Dr | Cr |
|---|---|---|
| Consulting Expense | 150,000 | |
| Accrued Liabilities – Services Received Not Invoiced | | 150,000 |

- Supporting documentation: vendor status report dated 3/30, PO reference, project manager sign-off attesting $150K delivered.
- Typically flagged **auto-reverse on day 1 of next period**.

### 4/1/2026 — Auto-reversal

| Account | Dr | Cr |
|---|---|---|
| Accrued Liabilities – Services RNI | 150,000 | |
| Consulting Expense | | 150,000 |

### 4/12/2026 — Invoice booked normally against PO (no SES path)

| Account | Dr | Cr |
|---|---|---|
| Consulting Expense | 150,000 | |
| Accounts Payable – Vendor | | 150,000 |

- The April debit to expense is exactly offset by the April 1 reversal credit, so **net April P&L impact = $0** and March correctly carries the full $150,000.
- If the invoice had differed from the accrual (say $148K), the variance ($2K) would naturally fall into April expense — acceptable for immaterial true-ups.

---

## Comparison Summary

| Feature | SES / GR-IV (SAP-native) | Manual Accrual |
|---|---|---|
| Liability account | GR/IR Clearing – Services | Accrued Liabilities |
| Trigger for expense | SES acceptance | Manual JE based on evidence |
| Reversal needed? | No — clears against invoice | Yes — auto-reverse next period |
| Three-way match | Yes (PO/SES/Invoice) | No (PO/Invoice only) |
| Risk of double-count | Low (system-controlled) | Moderate (relies on reversal) |
| Audit trail | Strong, embedded in PO | Depends on JE backup quality |

---

## Key Points for the Close File

1. **$150,000 expense in March 2026**, $50,000 remains open commitment — *not* accrued.
2. Evidence of performance = vendor status report 3/30 + PO + internal PM confirmation. Cutoff is satisfied.
3. The $50,000 April delivery is recognized in April when services are rendered (via second SES or April-end accrual if invoice lags again).
4. If using manual accrual, ensure the JE is set to **auto-reverse 4/1** to prevent double-booking when the 4/12 invoice posts to expense.
5. The accrual/GR-IR balance at 3/31 of $150,000 is a current liability and should tie to the GR/IR-Services aging or accrual schedule supporting the close.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly accrues $150k in March only, explicitly excludes the $50k as non-accruable, presents both the SES/GR-IR path and manual accrual with reversing entry with clean journal entries, addresses GR/IR aging review, and discusses audit trail/three-way match controls. Minor gap: SOX segregation of duties is not explicitly called out by name, though audit trail and approver controls are mentioned. Overall meets the rubric criteria for a 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_008 — close_and_controls · hard · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: multi-step accounting (matching principle and clearing accounts)_

### Question

What is the correct accounting at month-end and the following month? Walk through the GR/IR (or accrual) postings and explain how this would look in an SAP-style services-PO setup vs. a manual accrual.

### Context

```
Today is 2026-03-31 (month-end close).
PO #4500-77002 — services PO with Strategy Consulting Co.
  PO total:    $200,000
  Services:    Q1 strategy engagement
  Status as of 2026-03-31: vendor's status report (received 2026-03-30) confirms $150,000 of services delivered through month-end; project is on track; remaining $50,000 will be delivered in April.
  No invoice received from vendor by close.
Invoice received 2026-04-12: $150,000 referencing PO #4500-77002, milestone 1.
```

### Rubric

- **0**: Accrues the full $200k, or recognizes the expense in April, or omits the reversing entry in the manual path, or confuses GR/IR with AP
- **1**: Recognizes $150k in March correctly but mixes up the manual-vs-SES paths, omits the GR/IR clearing mechanic, or does not flag that the remaining $50k is non-accruable
- **2**: Correctly accrues $150k in March only, presents both manual-with-reversal and SES-with-GR/IR paths with clean journal entries, addresses GR/IR aging review and SOX segregation, and explicitly excludes the $50k as non-accruable

### Ideal answer

Concept: the matching principle (ASC 720; IAS 1) requires that expense be recognized in the period the service is rendered, regardless of invoice timing. $150k of services were rendered in March, so $150k must hit March P&L. The remaining $50k is not accruable — services not yet rendered and there is no constructive obligation beyond the PO commitment.

Manual-accrual path (simpler, common in non-SAP environments):

March 31 — accrual entry:
  Dr. Consulting expense              $150,000
     Cr. Accrued liabilities (or 'Accrued expenses')  $150,000

April 1 — reversing entry (auto-reverse JE):
  Dr. Accrued liabilities              $150,000
     Cr. Consulting expense                            $150,000

April 12 — invoice posted normally:
  Dr. Consulting expense              $150,000
     Cr. Accounts payable                              $150,000

Net effect: March P&L = $150k expense (correct), April P&L = $0 net for this milestone (correct), AP open at $150k pending payment.

SAP-style services-PO path with Service Entry Sheet (SES):

March 30–31 — operations / project owner enters SES against PO #4500-77002 for $150k of milestone-1 services delivered. SES approval triggers automatic GR-equivalent posting:
  Dr. Consulting expense              $150,000
     Cr. GR/IR clearing account                        $150,000

April 12 — invoice receipt against the SES (logistics invoice verification, MIRO):
  Dr. GR/IR clearing                   $150,000
     Cr. Accounts payable                              $150,000

GR/IR clears to zero on the matched line. March P&L correctly reflects $150k. No reversing entry needed because the SES, not a manual JE, drove the expense.

Key points and audit considerations:
- The $50k of unrendered services must NOT be accrued. Accruing for not-yet-performed services would overstate March expense and is an audit finding.
- The accrual must be supported by evidence — here, the vendor's status report dated 2026-03-30 is the source document. Without contemporaneous evidence of services rendered, the accrual is unsupported.
- GR/IR balances are a standard month-end review focus: aged GR/IR items represent either unrecorded liabilities (services received not invoiced — should be in this bucket) or stale receipts that need investigation. The balance here will sit at $150k credit from March 31 until April 12, then clear.
- SOX P2P control: the role entering the SES (project owner) must be different from the AP role posting the invoice and from the role approving payment. Same segregation as q_003.
- If the vendor invoiced $160k in April (not $150k), the $10k delta would be a price/scope variance — exception per the 3-way logic in q_003, route to buyer.

### Model response

# Accounting Treatment: Services PO Accrual at Month-End Close

## Conceptual Framework First

For services POs, the **recognition trigger** is *services rendered*, not invoice receipt. Because $150,000 of services were delivered through March 31 (confirmed by vendor status report) but **no invoice exists**, we have a classic **accrued liability** situation — an obligation that must be recorded in the period the expense was incurred.

The remaining $50,000 has **not** been delivered; it is an **executory obligation** and is correctly **not accrued**.

---

## SAP-Style Services PO Setup

### How SAP Handles Services POs

In SAP (MM module), services are handled via:
- **Service Entry Sheets (SES)** — the mechanism that records service receipt, analogous to a goods receipt (GR) for materials
- **GR/IR Clearing Account** — an automated bridge between the expense recognition and the vendor payable
- **Three-way match** at payment: PO ↔ SES ↔ Invoice

### Step 1 — 2026-03-31: Service Entry Sheet Posted

The business creates and **approves an SES** for $150,000 confirming services received through month-end.

```
AUTOMATIC POSTING (ML81N / SES Approval):

Dr  Professional Services Expense        $150,000
    [P&L — Strategy Consulting, Q1]
        Cr  GR/IR Clearing — Services   $150,000
            [Balance Sheet Liability]
```

**What this means:**
- The **expense hits Q1 P&L** ✓ (matching principle satisfied)
- The **GR/IR account** sits on the balance sheet as a current liability — it represents "we have received value; invoice is pending"
- The vendor (AP) account is **not yet credited** because no invoice exists
- The GR/IR is NOT a vendor payable yet; it's an interim clearing account

**Balance Sheet at 2026-03-31:**

| Account | Amount |
|---|---|
| GR/IR Clearing — Services (Current Liability) | $150,000 Cr |
| Accrued Expenses — per traditional view | (replaced by GR/IR in SAP) |

---

### Step 2 — 2026-04-12: Invoice Received ($150,000)

AP department posts the invoice via **MIRO** (Logistics Invoice Verification):

```
AUTOMATIC POSTING (MIRO — Invoice Verification):

Dr  GR/IR Clearing — Services           $150,000
        Cr  Accounts Payable — Strategy Consulting Co.  $150,000
```

**What this means:**
- The GR/IR account is **cleared to zero** — the bridge is collapsed
- A proper **vendor payable** is now established
- The expense does **not hit April P&L** — it was already recognized in March ✓
- Three-way match is satisfied: PO $200,000 ✓ | SES $150,000 ✓ | Invoice $150,000 ✓

**P&L Impact: Zero in April for this transaction ✓**

---

### Step 3 — April: Remaining $50,000 Delivered

When remaining services are confirmed (another SES):

```
Dr  Professional Services Expense        $50,000
        Cr  GR/IR Clearing — Services    $50,000
```

Then upon invoice receipt for milestone 2:

```
Dr  GR/IR Clearing — Services            $50,000
        Cr  Accounts Payable              $50,000
```

---

## Manual Accrual Setup (Non-SAP / No SES Process)

When there is no system-driven GR/IR mechanism, the accounting team books a **manual journal entry** directly.

### Step 1 — 2026-03-31: Manual Accrual

```
MANUAL JOURNAL ENTRY — Period Close:

Dr  Professional Services Expense        $150,000
        Cr  Accrued Liabilities           $150,000

Supporting documentation:
  - Vendor status report dated 2026-03-30
  - PO #4500-77002 ($200,000 total)
  - Approver sign-off
```

**Key difference from SAP:** This entry requires **human initiation** — it will not post automatically. Finance must have a robust accrual checklist to catch it.

---

### Step 2 — April: Reverse the Accrual

Standard practice is to **reverse the manual accrual** on the first day of April (or when the invoice arrives):

```
REVERSAL — 2026-04-01 (auto-reverse if set up):

Dr  Accrued Liabilities                  $150,000
        Cr  Professional Services Expense $150,000
```

This temporarily creates a **credit balance in expense** in April.

---

### Step 3 — 2026-04-12: Post the Invoice

```
INVOICE POSTING — 2026-04-12:

Dr  Professional Services Expense        $150,000
        Cr  Accounts Payable              $150,000
```

**Net April P&L effect:** Reversal ($150,000) Cr + Invoice ($150,000) Dr = **$0 net** ✓

The expense remains entirely in Q1, which is the correct outcome.

> ⚠️ **Risk in manual process:** If the reversal is forgotten OR the invoice is miscoded to a different account/period, P&L will be misstated. This is why auto-reverse entries and/or a cutoff checklist are critical controls.

---

## Side-by-Side Comparison

| Dimension | SAP / GR-IR Model | Manual Accrual |
|---|---|---|
| **Trigger** | SES approval (system-driven) | Manual JE at close |
| **Balance sheet account** | GR/IR Clearing (technical clearing) | Accrued Liabilities |
| **Expense recognition** | Automatic upon SES | Manual — risk of omission |
| **Invoice posting** | Clears GR/IR via MIRO | Reversal + AP entry |
| **April P&L impact** | Zero (no additional entry) | Zero IF reversal done correctly |
| **Three-way match** | Systematic (PO/SES/Invoice) | Manual comparison |
| **Audit trail** | System-generated, timestamp | JE with supporting docs |
| **Error risk** | Lower — system enforces | Higher — human-dependent |
| **Remaining $50K** | New SES in April | New accrual in April |

---

## Key Accounting Principles Applied

1. **Accrual Basis / Matching Principle:** Expense recognized when services are received (March), not when cash is paid or invoice arrives (April)
2. **Completeness:** $150,000 confirmed received must be in the financial statements at 3/31 regardless of invoice status
3. **Cutoff:** The $50,000 not yet delivered is **correctly excluded** — accruing undelivered services would be a prepaid asset issue, not a liability
4. **Executory contracts:** The undelivered $50,000 is an executory obligation (both parties still performing) — no liability recognition until performance occurs

---

## Summary of Ledger Impact

```
                    MARCH 2026          APRIL 2026
                    ──────────          ──────────
P&L Expense:        $150,000            $0
Balance Sheet:      +$150,000 Liability  Clears to $0
Vendor Payable:     $0                  $150,000 (→ paid per terms)
```

The economic substance is fully captured in Q1, the vendor is paid in April on proper terms, and the financial statements across both periods are accurate.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** Correctly accrues $150k in March only, presents both manual-with-reversal and SES-with-GR/IR paths with clean journal entries, explicitly excludes the $50k as non-accruable (executory), and addresses audit/control risks. Minor gap: doesn't explicitly call out SOX segregation of duties between SES entry and AP invoice posting, and GR/IR aging review is only lightly implied rather than stated. However, the core rubric requirements are met thoroughly.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_008 — close_and_controls · hard · **score 2/2** (model: `claude-haiku-4-5`)

_Expected failure mode: multi-step accounting (matching principle and clearing accounts)_

### Question

What is the correct accounting at month-end and the following month? Walk through the GR/IR (or accrual) postings and explain how this would look in an SAP-style services-PO setup vs. a manual accrual.

### Context

```
Today is 2026-03-31 (month-end close).
PO #4500-77002 — services PO with Strategy Consulting Co.
  PO total:    $200,000
  Services:    Q1 strategy engagement
  Status as of 2026-03-31: vendor's status report (received 2026-03-30) confirms $150,000 of services delivered through month-end; project is on track; remaining $50,000 will be delivered in April.
  No invoice received from vendor by close.
Invoice received 2026-04-12: $150,000 referencing PO #4500-77002, milestone 1.
```

### Rubric

- **0**: Accrues the full $200k, or recognizes the expense in April, or omits the reversing entry in the manual path, or confuses GR/IR with AP
- **1**: Recognizes $150k in March correctly but mixes up the manual-vs-SES paths, omits the GR/IR clearing mechanic, or does not flag that the remaining $50k is non-accruable
- **2**: Correctly accrues $150k in March only, presents both manual-with-reversal and SES-with-GR/IR paths with clean journal entries, addresses GR/IR aging review and SOX segregation, and explicitly excludes the $50k as non-accruable

### Ideal answer

Concept: the matching principle (ASC 720; IAS 1) requires that expense be recognized in the period the service is rendered, regardless of invoice timing. $150k of services were rendered in March, so $150k must hit March P&L. The remaining $50k is not accruable — services not yet rendered and there is no constructive obligation beyond the PO commitment.

Manual-accrual path (simpler, common in non-SAP environments):

March 31 — accrual entry:
  Dr. Consulting expense              $150,000
     Cr. Accrued liabilities (or 'Accrued expenses')  $150,000

April 1 — reversing entry (auto-reverse JE):
  Dr. Accrued liabilities              $150,000
     Cr. Consulting expense                            $150,000

April 12 — invoice posted normally:
  Dr. Consulting expense              $150,000
     Cr. Accounts payable                              $150,000

Net effect: March P&L = $150k expense (correct), April P&L = $0 net for this milestone (correct), AP open at $150k pending payment.

SAP-style services-PO path with Service Entry Sheet (SES):

March 30–31 — operations / project owner enters SES against PO #4500-77002 for $150k of milestone-1 services delivered. SES approval triggers automatic GR-equivalent posting:
  Dr. Consulting expense              $150,000
     Cr. GR/IR clearing account                        $150,000

April 12 — invoice receipt against the SES (logistics invoice verification, MIRO):
  Dr. GR/IR clearing                   $150,000
     Cr. Accounts payable                              $150,000

GR/IR clears to zero on the matched line. March P&L correctly reflects $150k. No reversing entry needed because the SES, not a manual JE, drove the expense.

Key points and audit considerations:
- The $50k of unrendered services must NOT be accrued. Accruing for not-yet-performed services would overstate March expense and is an audit finding.
- The accrual must be supported by evidence — here, the vendor's status report dated 2026-03-30 is the source document. Without contemporaneous evidence of services rendered, the accrual is unsupported.
- GR/IR balances are a standard month-end review focus: aged GR/IR items represent either unrecorded liabilities (services received not invoiced — should be in this bucket) or stale receipts that need investigation. The balance here will sit at $150k credit from March 31 until April 12, then clear.
- SOX P2P control: the role entering the SES (project owner) must be different from the AP role posting the invoice and from the role approving payment. Same segregation as q_003.
- If the vendor invoiced $160k in April (not $150k), the $10k delta would be a price/scope variance — exception per the 3-way logic in q_003, route to buyer.

### Model response

# Accounting Analysis: Services PO with Month-End Accrual

## Month-End Close (2026-03-31)

### Correct Accounting Entry

**Debit:** Operating Expense (Strategy Consulting) — $150,000  
**Credit:** Accrued Expenses (Services Payable) — $150,000

**Rationale:**
- Vendor's status report (received 2026-03-30) constitutes reliable evidence of delivery
- Services were rendered in Q1 (period of receipt)
- Revenue recognition principle & matching principle require expense recognition when services are received, *not* when invoiced
- The vendor's delay in invoicing doesn't defer the accrual obligation

---

## SAP-Style Services PO Setup (GR/IR Process)

### Month-End (2026-03-31)

1. **Goods Receipt (GR) posting** for services:
   - System creates a GR document based on vendor's status report or internal confirmation
   - PO line item for $150,000 is matched to the GR
   - **GR/IR clearing account** (balance sheet) is automatically credited:
     - **Debit:** Expense account — $150,000
     - **Credit:** GR/IR Clearing Account — $150,000

2. **Result at 2026-03-31:**
   - Expense recognized: $150,000 ✓
   - GR/IR Clearing Account balance: $150,000 (liability side)
   - Outstanding: $50,000 (undelivered, not accrued)

### April (2026-04-12) — Invoice Receipt

3. **Invoice Receipt (IR) posting:**
   - Vendor's invoice ($150,000) is entered in the system
   - System matches IR to the existing GR (3-way match: PO → GR → IR)
   - **Match successful:** GR/IR clearing account is cleared
   
   **Posting:**
   - **Debit:** GR/IR Clearing Account — $150,000
   - **Credit:** Accounts Payable — $150,000

4. **Result after IR:**
   - GR/IR Clearing Account: $0 (cleared)
   - Accounts Payable: $150,000 (vendor liability)
   - Expense: $150,000 (already recognized in March) — *no reversal*

---

## Manual Accrual Approach

### Month-End (2026-03-31)

**Accrual Journal Entry (manual):**
- **Debit:** Consulting Expense — $150,000
- **Credit:** Accrued Expenses Payable — $150,000

**Tracking required:**
- Create a manual accrual log or spreadsheet
- Flag for reversal or settlement in April

### April (2026-04-12) — Invoice Receipt

**Option A: Reverse-and-replace approach**
- **Debit:** Accrued Expenses Payable — $150,000
- **Credit:** Consulting Expense — $150,000
  *(Reverse the accrual)*

- **Debit:** Consulting Expense — $150,000
- **Credit:** Accounts Payable — $150,000
  *(Record actual invoice)*

**Option B: Direct settlement approach**
- **Debit:** Accrued Expenses Payable — $150,000
- **Credit:** Accounts Payable — $150,000
  *(Settle the accrual with the invoice)*
- Expense remains at $150,000 (not duplicated)

---

## Key Differences: SAP GR/IR vs. Manual Accrual

| Aspect | SAP GR/IR | Manual Accrual |
|--------|-----------|----------------|
| **Automation** | Automatic 3-way match (PO→GR→IR) | Manual matching & reversal tracking |
| **Clearing mechanism** | GR/IR clearing account | Accrued Expenses Payable |
| **Timing flexibility** | Built-in for delayed invoices | Requires vigilant reversal management |
| **Error risk** | Lower (systematic matching) | Higher (duplicate accruals, forgotten reversals) |
| **Reporting clarity** | Clean (GR/IR shows unmatched items) | Requires accrual reserve review |
| **April reconciliation** | Automatic match clears the account | Manual reversal required |

---

## Bottom Line

**Both methods yield the same result:**
- **March:** $150,000 expense recognized
- **April:** Invoice reduces payable; expense stays at $150,000 (no duplicate)

**However, SAP's GR/IR is superior** because:
- The clearing account acts as a self-correcting mechanism
- Three-way matching prevents invoice fraud and duplicate payments
- No manual reversal discipline required

**Critical point:** The undelivered $50,000 should **not** be accrued as of 2026-03-31, since it has not been received. It will be accrued when delivered in April (or when a binding confirmation of April delivery exists at month-end).

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response correctly accrues $150k in March, explicitly excludes the $50k as non-accruable, presents both the SAP GR/IR path with clearing account mechanics and the manual accrual path with reversal entries, and explains the 3-way match. It mentions reporting clarity for GR/IR aging. Minor weakness: SOX segregation of duties is not explicitly addressed, and the manual path's Option A doesn't specify auto-reversal on April 1 (instead reverses on April 12), though it achieves the same net result. Overall meets the rubric's level 2 criteria substantively.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_009 — supplier_data · hard · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: assumption generation across multiple regulatory regimes_

### Question

What screening should run on this supplier as part of onboarding? Identify the red flags, the legal/regulatory regimes that apply, and the recommended onboarding decision.

### Context

```
Onboarding request for a new supplier:
  Legal name:           Pacific Trade Solutions LLC
  Formation:            Delaware (formed 2025-11-04)
  Registered agent:     A national registered-agent service
  Listed UBO:           Ivan Petrov, residential address in Limassol, Cyprus
  Bank:                 Latvia (SWIFT routing)
  Goods supplied:       Electronic components (microcontrollers, FPGAs, RF components)
  Shipped from:         Hong Kong, via a freight forwarder unknown to the buyer
  Initial PO request:   $250,000
  Expected annual spend: $1,000,000
  Other notes: supplier requested a 50% prepayment on the first PO, citing 'manufacturing capacity reservation.'
```

### Rubric

- **0**: Onboards the supplier without enhanced due diligence, or misses sanctions/export-control regimes entirely, or treats the prepayment as routine
- **1**: Identifies sanctions and export-control concerns but misses the OFAC 50% rule, the FinCEN BOI requirement, the bank-callback control, or the graduated-onboarding recommendation
- **2**: Identifies all major red flags, names the relevant regimes (OFAC including 50% rule, EU/UK/UN sanctions, BIS EAR including Entity List, FinCEN BOI, FCPA), recommends specific verification steps including independent bank-account verification and prepayment rejection, and proposes graduated onboarding with ongoing screening

### Ideal answer

This packet has multiple red flags that, taken together, require enhanced due diligence and a hold on onboarding pending resolution. Treat as high-risk.

Red flags:
1. Newly formed Delaware LLC (Nov 2025) with no operating history — shell-company indicator.
2. UBO with a Russian-origin name and Cyprus residence — Cyprus is a known nexus for Russian-affiliated structures and has been a focal jurisdiction since 2022 EU/US Russia sanctions; not disqualifying on its own but raises sanctions-screening priority.
3. Bank in Latvia — Baltic banking has been the subject of multiple sanctions-evasion enforcement actions; payment routing must be verified.
4. Goods are dual-use electronics shipped from Hong Kong — high export-control risk for diversion to Russia or other restricted end-users; HK has been heavily flagged by US BIS as a diversion hub.
5. 50% prepayment request — common precursor to fraud or to funds-routing schemes; legitimate semiconductor distributors rarely require 50% prepay from a buyer with no relationship history.
6. Freight forwarder unknown to the buyer — diversion-risk indicator.

Applicable screening regimes:
- Sanctions screening: name and identifier screening of the entity, the UBO, and the Latvian bank against:
  - OFAC SDN, OFAC sectoral lists, OFAC 50% rule (entities ≥50% owned by SDN persons are themselves blocked even if not listed)
  - EU consolidated financial sanctions list
  - UK HMT (OFSI) consolidated list
  - UN Security Council list
  - Canadian, Swiss, Australian, Japanese sanctions lists if relevant
- Beneficial ownership: under the Corporate Transparency Act / FinCEN BOI rule (effective 2024), reporting companies disclose UBOs to FinCEN. The buyer should require the supplier to provide its FinCEN BOI report or equivalent evidence and verify UBO identity (passport, address verification). Confirm UBO is not a sanctioned person and not on OFAC's 50% derivative blocking.
- Export controls (US): even though the buyer is the US importer, if components are of US origin or contain US-origin technology subject to the EAR, the supplier and consignee chain must be screened against:
  - BIS Entity List, Unverified List, Military End User List, Denied Persons List
  - State Department debarred parties (ITAR, if applicable)
  - Non-SDN Menu-Based Sanctions List, NS-CMIC list
  ECCN of components must be determined; if controlled (e.g., 3A001 microelectronics, 3A002 RF), end-use and end-user statements required, and an export license may be needed for shipment from HK depending on classification.
- AML/KYC (under the buyer's own AML program if a financial institution; otherwise as commercial best practice and to support OFAC compliance): source of funds, payment routing verification, callback to the UBO via independently-obtained contact info — never via the contact provided in the onboarding packet.
- Anti-bribery: under FCPA, also screen for connections to foreign officials; Cyprus politically-exposed-persons screening on the UBO.

Recommended decision:
- Do NOT onboard or release any PO until:
  a) Sanctions screening on entity, UBO, and bank is clear across all relevant lists (with the OFAC 50% derivative test applied to UBO ownership chain).
  b) UBO identity is verified independently (government ID, address verification not via the same packet).
  c) Components are classified (ECCN); if controlled, end-use/end-user statements obtained and BIS license requirements assessed; HK consignee screened against Entity List.
  d) Bank account is verified by independent callback to the supplier using contact info NOT taken from the onboarding packet (mitigates business-email-compromise / account takeover risk).
  e) The 50% prepayment is rejected as a non-starter for a first engagement with a new high-risk supplier; if any prepayment, it should be against a performance bond or escrow, and only after all other diligence is clear.
- Even if all of the above is clear, recommend graduated onboarding: first PO at significantly less than $250k, with a denied-parties screen rerun on every shipment (suppliers can be added to lists between transactions) and a 12-month review.

References: 31 CFR Part 501 et seq. (OFAC), OFAC FAQ on 50% rule, 31 CFR §1010.380 (FinCEN BOI), 15 CFR Parts 730–774 (BIS EAR), BIS Entity List, EU Council Regulation 833/2014 as amended (Russia sanctions), FCPA (15 USC §78dd-1 et seq.).

### Model response

# Supplier Onboarding Risk Assessment: Pacific Trade Solutions LLC

## Executive Summary

This supplier profile exhibits a **dense cluster of high-risk indicators** that closely match published typologies for **Russia/Belarus sanctions evasion** and **export-control diversion of dual-use electronics**. Onboarding should be **paused pending Enhanced Due Diligence (EDD)**, with a strong default toward **rejection** unless every red flag is independently and documentarily resolved.

---

## 1. Red Flags Identified

### Entity / Ownership Red Flags
- **Brand-new Delaware LLC (formed Nov 2025)** with no operating history, yet quoting a $1M/year program — classic shell-company indicator.
- **Use of a national registered-agent service** (no physical U.S. nexus, no employees, no warehouse).
- **Russian-national UBO resident in Cyprus** — Cyprus is a well-documented jurisdiction for Russia-linked corporate layering (FinCEN/FATF/EU 14th sanctions package commentary).
- **Mismatch of nationalities, jurisdictions, and trade flows** (RU national → CY residence → DE entity → LV bank → HK shipping → U.S. buyer): the textbook "jurisdictional chain" pattern flagged by BIS, OFAC, FinCEN, and the UK/EU joint export-control alerts.

### Financial Red Flags
- **Latvian SWIFT bank account.** Latvia is a known transit corridor for Russia/CIS-linked funds; several Latvian banks have prior AML enforcement actions (ABLV, PNB). A U.S. supplier banking in Latvia with no commercial reason is anomalous.
- **50% prepayment demand** on a first PO with no track record — payment-terms anomaly cited in FinCEN Alert FIN-2022-Alert003 and the BIS/FinCEN Joint Alerts (June 2022, May 2023) on Russia evasion.
- **"Manufacturing capacity reservation"** rationale is weak: Pacific Trade Solutions is a *trader*, not a manufacturer.

### Goods / Logistics Red Flags
- **Microcontrollers, FPGAs, and RF components** are **Common High Priority List (CHPL) items** — the U.S./EU/UK/JP coordinated list of items found in Russian weapons recovered in Ukraine. Many fall under ECCNs **3A001, 3A090, 3A991, 5A001, 5A991** and are subject to Russia/Belarus FDP rules under EAR §746.8 and §734.9.
- **Shipped from Hong Kong** — designated by BIS as an elevated diversion-risk jurisdiction; HK-based forwarders are repeatedly named in BIS Entity List actions for Russia transshipment.
- **Freight forwarder unknown to buyer** — eliminates buyer's ability to verify end-use/end-user and breaks the "Know Your Cargo" chain.

### Pattern Match
Combined, these indicators match **at least 7 of the 10 evasion typologies** in the BIS/FinCEN Joint Alert (May 19, 2023) and the EU Commission's Sept 2023 guidance to operators on the "No-Russia clause."

---

## 2. Applicable Legal & Regulatory Regimes

| Regime | Relevance |
|---|---|
| **OFAC sanctions (31 CFR 500-series)** | SDN/SSI/Sectoral screening of entity, UBO, bank, forwarder. Russia/Belarus EOs 14024, 14071, 14114 (secondary-sanctions risk for non-U.S. financial institutions handling these flows). |
| **EAR / BIS export controls (15 CFR Parts 730-774)** | CHPL items + Russia/Belarus FDP rule (§746.8); Entity List & MEU List screening; "red flag" guidance in Supplement No. 3 to Part 732; **reverse export-control risk** even on imports if items are re-exported or if buyer has knowledge of diversion. |
| **BIS/FinCEN Joint Alerts (June 2022, May 2023)** | Defines exactly this fact pattern. |
| **FinCEN CDD Rule (31 CFR 1010.230)** & **Corporate Transparency Act / FinCEN BOI** | UBO verification obligations. |
| **AML / Bank Secrecy Act** (if buyer is a financial institution; otherwise best practice) | SAR considerations on prepayment + Latvia routing. |
| **EU 14th Sanctions Package "No-Russia clause"** (Reg. 833/2014, Art. 12g) | Required contractual prohibition on re-export to Russia for CHPL goods; applies to EU counterparties in chain. |
| **UK OFSI / OTSI** and **Japan METI / Canada SEMA** controls | Mirror CHPL controls; relevant if any group affiliate touches the transaction. |
| **FCPA / UK Bribery Act** | Shell-company + offshore payment pattern is also a corruption typology. |
| **U.S. Customs (19 USC; CBP)** | Country-of-origin, valuation, forced-labor (UFLPA) and antidumping exposure on HK-routed electronics. |
| **ITAR (22 CFR 120-130)** | Only if any RF/FPGA item is USML-listed — must be screened. |

---

## 3. Required Screening Steps

1. **Sanctions screening** (entity, UBO Ivan Petrov with DOB/POB, registered agent, Latvian bank + correspondent, freight forwarder once identified) against:
   - OFAC SDN, SSI, Non-SDN MES, 50%-Rule analysis
   - BIS Entity List, MEU, Unverified List, Denied Persons List
   - State Department AECA debarments
   - EU consolidated list, UK OFSI, UN, Canada, Japan, Australia, Switzerland

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response identifies all major red flags (new shell LLC, Russian UBO in Cyprus, Latvian bank, dual-use electronics from HK, unknown forwarder, 50% prepayment). It names all required regimes: OFAC including explicit 50% rule analysis, EU/UK/UN/Canada/Japan/Australia/Switzerland sanctions, BIS EAR with Entity List/MEU/UVL/DPL, FinCEN BOI/CTA, and FCPA. It adds value with CHPL, FDP rules, and BIS/FinCEN joint alerts. The executive summary recommends pausing onboarding pending EDD with default toward rejection. However, the response appears truncated mid-list (step 1 of screening steps) and does not explicitly complete the recommendations on independent bank callback verification, explicit prepayment rejection, or graduated onboarding with ongoing screening—these key control recommendations from the rubric are not clearly articulated in the visible portion. Still, the substantive coverage of regimes and red flags is thorough enough to merit a 2, though the missing explicit bank-callback control and graduated onboarding recommendation make this borderline.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_010 — close_and_controls · hard · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: multi-step controls reasoning under SOX_

### Question

Diagnose the SOX P2P control failures that allowed this pattern. Describe the specific control activities that should have prevented or detected it, and how to remediate. Address whether this is likely a material weakness.

### Context

```
Fact pattern (composite, in the style of SEC AAER ghost-vendor cases):

Over an 18-month period at a SOX-registrant company, an AP clerk processed payments to 'Northern Logistics Services LLC' totaling $480,000 across 49 invoices. Investigation after a tip from a coworker revealed:
- The AP clerk had access in the ERP to (a) create new vendor master records, (b) approve invoices under $10,000, and (c) initiate ACH payment runs.
- Northern Logistics had been added to the vendor master by the AP clerk, with the clerk's home P.O. box as the remit-to address and a bank account in the name of a relative.
- All 49 invoices were 'non-PO' for 'logistics services,' with amounts ranging from $9,800 to $9,950.
- No contract or SOW was on file for the supplier.
- The company's policy requires PO coverage for all services > $10,000 and CFO approval for new vendor adds for spend > $50,000/year, but these thresholds were never tripped because of how the activity was structured.
- The external auditor selected the vendor master change log as a routine SOX walkthrough sample but had not selected any of the 49 invoices in their substantive sample.
```

### Rubric

- **0**: Misses segregation of duties as the primary failure, or treats this as a single-control gap, or fails to address material-weakness analysis
- **1**: Identifies SoD and one or two other gaps, but misses the threshold-clustering analytic, the employee-vendor match control, the cumulative-spend trigger, or the material-weakness reasoning
- **2**: Identifies SoD plus at least four additional control gaps (vendor-master maker-checker, employee-vendor match, cluster-below-threshold analytic, rolling-cumulative-spend escalation, ITGC access review), proposes specific remediations for each, and reaches a defensible material-weakness conclusion under AS 2201 with the right reasoning (severity by potential not actual loss)

### Ideal answer

Failed controls and design defects:

1. Segregation of duties (the primary failure). Under PCAOB AS 2201 and the COSO 2013 framework, the P2P cycle requires segregation across at minimum: vendor-master maintenance, invoice approval, and payment initiation. A single employee with all three privileges has end-to-end control of cash disbursement to a vendor of their own creation. This is the textbook ghost-vendor enabler. The control deficiency is in the access design (entitlement grants), not just in operation.

2. Vendor-master change controls. Adding a new vendor should require:
   - Independent maker-checker approval (the clerk who keys the add cannot be the approver).
   - W-9 / W-8 on file before activation; TIN match against IRS TIN matching service.
   - Address verification, including a check that the remit-to is not a P.O. box matching an employee's known address (an automated employee-vendor address/bank match is a common detective control).
   - Bank account verification via independent callback to a phone number for the supplier obtained from a public source (not the supplier packet itself).
   The failure here permitted the clerk to set the remit-to to their own P.O. box and the bank account to a relative.

3. Threshold-cluster monitoring (structuring). Forty-nine invoices clustered in a $150 band immediately below the $10,000 PO/approval threshold is a textbook structuring pattern. A standard analytic — distribution of invoice amounts by vendor compared to authorization thresholds — would have flagged this within weeks. Additional analytics: Benford's-law deviation on first-digit distribution, invoice-frequency anomalies for new vendors. This is a detective control gap.

4. Non-PO services without contract. Policy required POs for services > $10k and the supplier had no contract or SOW. The non-PO pathway should require:
   - A contract or engagement letter referenced on the invoice for any services vendor.
   - Periodic review of non-PO spend by vendor to flag vendors with high cumulative non-PO spend (this vendor had $480k cumulative — should have been escalated long before the 18-month mark).

5. New-vendor-spend escalation. The policy required CFO approval for new-vendor spend > $50,000/year, but the threshold was applied to a single invoice / single PO, not cumulatively over a rolling 12 months. A 12-month rolling cumulative trigger would have caught this within ~5 invoices (~$50k).

6. ITGC / access review. Periodic access reviews (typically quarterly) should have flagged the toxic combination of entitlements held by the AP clerk. The fact that this combination was granted and never reviewed is an ITGC deficiency.

Remediation:
- Re-design role-based access in the ERP to enforce segregation: vendor-master role, invoice-approval role, payment-initiation role are mutually exclusive. Document in an SoD matrix and enforce via GRC tooling.
- Implement maker-checker on vendor-master adds and changes; require an independent reviewer outside AP.
- Implement employee-vendor matching analytic (compare vendor remit-to addresses, phone numbers, and bank accounts to employee HR data) — run continuously, alert on match.
- Implement threshold-cluster analytic on invoice amounts vs. authorization thresholds, by vendor and across vendors.
- Implement rolling-12-month cumulative spend trigger for new vendors to feed CFO approval gating.
- Lower the PO requirement threshold for services or eliminate the non-PO services pathway entirely.
- Remediate the ITGC: implement quarterly SoD-conflict access reviews with documented review evidence.
- Targeted lookback: examine all vendors added by this clerk and all non-PO vendors with high cumulative spend over the past 24 months; assess for similar patterns.

Material-weakness assessment:
Under PCAOB AS 2201, a control deficiency is a material weakness if there is a reasonable possibility that a material misstatement of the financial statements would not be prevented or detected on a timely basis. This case:
- The deficiency is in access design and SoD — pervasive, not isolated.
- The same SoD weakness could enable misstatements far larger than $480k; severity is judged by potential, not just actual loss.
- $480k is below typical materiality for a SOX registrant of meaningful size, but the controls' inability to prevent a more material occurrence is what drives the conclusion.
- The structuring pattern was not detected by management; the auditor did not happen to sample these invoices; detection came from a tip — meaning neither preventive nor detective controls operated effectively.
Likely conclusion: material weakness in P2P internal controls, requiring disclosure under Item 9A of Form 10-K and re-evaluation of management's ICFR assertion. If the misstatement crosses materiality after the lookback, restatement may be required. Auditor will reassess scope and is required to communicate to the audit committee under AS 1301.

References: PCAOB AS 2201 ('An Audit of Internal Control over Financial Reporting'), AS 1301 ('Communications with Audit Committees'), COSO 2013 framework, SEC Regulation S-K Item 308, SEC AAERs on ghost-vendor and structuring schemes (representative cases — user should anchor to a specific cited AAER if used in publication).

### Model response

# Diagnosis: SOX P2P Control Failures in a Ghost-Vendor Scheme

## 1. Root-Cause Control Failures

### A. Segregation of Duties (SoD) Failure — The Primary Defect

The AP clerk simultaneously held three incompatible ERP roles that, together, constitute the classic "ghost vendor" toxic combination:

| Function | Risk When Combined |
|---|---|
| Create/maintain vendor master | Can introduce fictitious payee |
| Approve invoices (<$10K) | Can authorize payment to that payee |
| Initiate ACH payment runs | Can release cash to that payee |

This is a **prima facie SoD violation**. Vendor master maintenance must be segregated from invoice processing/approval, and both must be segregated from payment execution (the "three-way separation" embedded in COSO 2013 Principle 10 and codified in every standard P2P control matrix). Any one of those three duties stripped from the clerk would have broken the scheme.

### B. Threshold-Structuring Vulnerability (Control Design Failure)

Policy thresholds were **single-transaction, not aggregated**:
- $10,000 PO threshold → defeated by 49 invoices at $9,800–$9,950 (textbook structuring/"smurfing").
- $50,000/year new-vendor CFO approval → never triggered because no aggregation logic monitored cumulative spend by new vendors.

This is a **control design deficiency** — the controls *operated as designed* but were designed in a way that a knowledgeable insider could circumvent. Auditors will treat this as more serious than a pure operating failure because it implies management did not perform a competent fraud risk assessment (AS 2110 / COSO Principle 8).

### C. Vendor Master Onboarding Controls Missing or Ineffective

Standard onboarding controls that were absent or bypassed:
- No independent vendor validation (W-9/W-8, TIN matching with IRS, business registration check, D-U-N-S, OFAC).
- No verification that remit-to address is a commercial location (a P.O. box — particularly an *employee's* P.O. box — should fail address validation).
- No employee-vendor cross-match against HR master (address, bank account, phone, tax ID, emergency contact, dependent SSNs).
- No bank-account-ownership verification (e.g., Plaid/penny-test, callback to vendor at independently sourced number).
- No "maker-checker" on vendor master adds — the creator was effectively the approver.

### D. Invoice Processing Controls

- **Non-PO invoices** were accepted for recurring services with no contract/SOW on file. A compensating control for non-PO spend (department-head certification, contract reference required, recurring-vendor exception report) was either missing or not enforced.
- **No three-way match** because no PO existed; there was no compensating receipt/service-confirmation control from an operations owner.
- Invoice approval delegation of authority (DOA) was set at $10K — appropriate in isolation, but with no aggregation rule per vendor/per period, the clerk had effectively unlimited authority within a calendar window.

### E. Payment (Disbursement) Controls

- ACH payment runs were initiated by the same person who approved the underlying invoices.
- Apparently no positive pay / ACH filter, no dual release in the banking platform, and no review of the proposed payment register by Treasury before transmission.

### F. Detective / Monitoring Controls

- No periodic vendor master review (dormant vendors, new-vendor activity, duplicate addresses/banks, P.O. box remit-tos, employee-vendor matches).
- No continuous-control-monitoring (CCM) analytics: invoices clustered just below approval thresholds (Benford-style), single-approver vendors, round-dollar non-PO vendors, vendors with no PO history, vendors paid only by ACH to a single account.
- The scheme was caught by a tip — i.e., the **whistleblower hotline was the only effective control**, which the ACFE consistently shows is the leading detection method but cannot be relied upon as a SOX control.

### G. Auditor's Sampling Outcome (Not a Company Control Failure, but Relevant)

The external auditor sampled the vendor master change log (walkthrough) and missed the issue because (i) walkthrough samples are typically n=1 and not designed to detect fraud, and (ii) substantive AP testing was monetary-unit-sample biased toward larger items, so $9,800 invoices were below the sampling radar. This illustrates why **management cannot rely on the external audit as a detective control** — a point the SEC has emphasized in AAERs.

---

## 2. Specific Controls That Should Have Prevented or Detected This

**Preventive:**
1. **SoD rule set in the ERP/GRC tool** flagging the combination Vendor-Master-Maint + Invoice-Approve + Payment-Run as a critical SoD conflict; mitigated only with documented compensating controls.
2. **Maker-checker on vendor master** with the checker being a Procurement or Vendor Management function, not AP.
3. **Automated vendor validation** at onboarding: TIN match, OFAC, address verification, employee-vendor cross-match (address, bank, tax ID, phone), bank-account ownership confirmation via independent callback to a number obtained from a public source.
4. **Aggregated thresholds**: PO requirement triggered when *cumulative* non-PO spend with a vendor exceeds $10K in a rolling 12-month period; new-vendor CFO approval triggered prospectively at onboarding for any vendor expected to exceed $50K *or* retroactively when actual spend approaches the threshold.
5. **Non-PO invoice control**: contract/SOW reference required; business-owner (not AP) approval; quarterly certification by department heads of all non-PO spend.
6. **Payment dual control**: AP initiates, Treasury releases in the bank; positive pay / ACH whitelist by vendor bank account.

**Detective:**
7. **Quarterly vendor master review** by Internal Audit /

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response identifies SoD as the primary failure and covers all required additional control gaps: vendor-master maker-checker, employee-vendor matching, threshold-cluster/structuring analytics, rolling cumulative spend escalation, and ITGC-style SoD rule sets/access reviews. It proposes specific remediations for each (GRC SoD rules, maker-checker, automated validation, aggregated thresholds, dual control, CCM analytics). The response was truncated before completing the material-weakness analysis under AS 2201, which is a notable gap — the rubric explicitly requires a defensible material-weakness conclusion with reasoning on severity by potential not actual loss. However, the response does touch on design vs. operating deficiency framing and references AS 2110/COSO. The truncation prevents full credit confidence, but the substantive content delivered meets the level-2 bar for control identification and remediation. Given the missing explicit material-weakness conclusion, this is borderline between 1 and 2; leaning 2 because of the breadth and specificity of controls covered.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_010 — close_and_controls · hard · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: multi-step controls reasoning under SOX_

### Question

Diagnose the SOX P2P control failures that allowed this pattern. Describe the specific control activities that should have prevented or detected it, and how to remediate. Address whether this is likely a material weakness.

### Context

```
Fact pattern (composite, in the style of SEC AAER ghost-vendor cases):

Over an 18-month period at a SOX-registrant company, an AP clerk processed payments to 'Northern Logistics Services LLC' totaling $480,000 across 49 invoices. Investigation after a tip from a coworker revealed:
- The AP clerk had access in the ERP to (a) create new vendor master records, (b) approve invoices under $10,000, and (c) initiate ACH payment runs.
- Northern Logistics had been added to the vendor master by the AP clerk, with the clerk's home P.O. box as the remit-to address and a bank account in the name of a relative.
- All 49 invoices were 'non-PO' for 'logistics services,' with amounts ranging from $9,800 to $9,950.
- No contract or SOW was on file for the supplier.
- The company's policy requires PO coverage for all services > $10,000 and CFO approval for new vendor adds for spend > $50,000/year, but these thresholds were never tripped because of how the activity was structured.
- The external auditor selected the vendor master change log as a routine SOX walkthrough sample but had not selected any of the 49 invoices in their substantive sample.
```

### Rubric

- **0**: Misses segregation of duties as the primary failure, or treats this as a single-control gap, or fails to address material-weakness analysis
- **1**: Identifies SoD and one or two other gaps, but misses the threshold-clustering analytic, the employee-vendor match control, the cumulative-spend trigger, or the material-weakness reasoning
- **2**: Identifies SoD plus at least four additional control gaps (vendor-master maker-checker, employee-vendor match, cluster-below-threshold analytic, rolling-cumulative-spend escalation, ITGC access review), proposes specific remediations for each, and reaches a defensible material-weakness conclusion under AS 2201 with the right reasoning (severity by potential not actual loss)

### Ideal answer

Failed controls and design defects:

1. Segregation of duties (the primary failure). Under PCAOB AS 2201 and the COSO 2013 framework, the P2P cycle requires segregation across at minimum: vendor-master maintenance, invoice approval, and payment initiation. A single employee with all three privileges has end-to-end control of cash disbursement to a vendor of their own creation. This is the textbook ghost-vendor enabler. The control deficiency is in the access design (entitlement grants), not just in operation.

2. Vendor-master change controls. Adding a new vendor should require:
   - Independent maker-checker approval (the clerk who keys the add cannot be the approver).
   - W-9 / W-8 on file before activation; TIN match against IRS TIN matching service.
   - Address verification, including a check that the remit-to is not a P.O. box matching an employee's known address (an automated employee-vendor address/bank match is a common detective control).
   - Bank account verification via independent callback to a phone number for the supplier obtained from a public source (not the supplier packet itself).
   The failure here permitted the clerk to set the remit-to to their own P.O. box and the bank account to a relative.

3. Threshold-cluster monitoring (structuring). Forty-nine invoices clustered in a $150 band immediately below the $10,000 PO/approval threshold is a textbook structuring pattern. A standard analytic — distribution of invoice amounts by vendor compared to authorization thresholds — would have flagged this within weeks. Additional analytics: Benford's-law deviation on first-digit distribution, invoice-frequency anomalies for new vendors. This is a detective control gap.

4. Non-PO services without contract. Policy required POs for services > $10k and the supplier had no contract or SOW. The non-PO pathway should require:
   - A contract or engagement letter referenced on the invoice for any services vendor.
   - Periodic review of non-PO spend by vendor to flag vendors with high cumulative non-PO spend (this vendor had $480k cumulative — should have been escalated long before the 18-month mark).

5. New-vendor-spend escalation. The policy required CFO approval for new-vendor spend > $50,000/year, but the threshold was applied to a single invoice / single PO, not cumulatively over a rolling 12 months. A 12-month rolling cumulative trigger would have caught this within ~5 invoices (~$50k).

6. ITGC / access review. Periodic access reviews (typically quarterly) should have flagged the toxic combination of entitlements held by the AP clerk. The fact that this combination was granted and never reviewed is an ITGC deficiency.

Remediation:
- Re-design role-based access in the ERP to enforce segregation: vendor-master role, invoice-approval role, payment-initiation role are mutually exclusive. Document in an SoD matrix and enforce via GRC tooling.
- Implement maker-checker on vendor-master adds and changes; require an independent reviewer outside AP.
- Implement employee-vendor matching analytic (compare vendor remit-to addresses, phone numbers, and bank accounts to employee HR data) — run continuously, alert on match.
- Implement threshold-cluster analytic on invoice amounts vs. authorization thresholds, by vendor and across vendors.
- Implement rolling-12-month cumulative spend trigger for new vendors to feed CFO approval gating.
- Lower the PO requirement threshold for services or eliminate the non-PO services pathway entirely.
- Remediate the ITGC: implement quarterly SoD-conflict access reviews with documented review evidence.
- Targeted lookback: examine all vendors added by this clerk and all non-PO vendors with high cumulative spend over the past 24 months; assess for similar patterns.

Material-weakness assessment:
Under PCAOB AS 2201, a control deficiency is a material weakness if there is a reasonable possibility that a material misstatement of the financial statements would not be prevented or detected on a timely basis. This case:
- The deficiency is in access design and SoD — pervasive, not isolated.
- The same SoD weakness could enable misstatements far larger than $480k; severity is judged by potential, not just actual loss.
- $480k is below typical materiality for a SOX registrant of meaningful size, but the controls' inability to prevent a more material occurrence is what drives the conclusion.
- The structuring pattern was not detected by management; the auditor did not happen to sample these invoices; detection came from a tip — meaning neither preventive nor detective controls operated effectively.
Likely conclusion: material weakness in P2P internal controls, requiring disclosure under Item 9A of Form 10-K and re-evaluation of management's ICFR assertion. If the misstatement crosses materiality after the lookback, restatement may be required. Auditor will reassess scope and is required to communicate to the audit committee under AS 1301.

References: PCAOB AS 2201 ('An Audit of Internal Control over Financial Reporting'), AS 1301 ('Communications with Audit Committees'), COSO 2013 framework, SEC Regulation S-K Item 308, SEC AAERs on ghost-vendor and structuring schemes (representative cases — user should anchor to a specific cited AAER if used in publication).

### Model response

# SOX Procure-to-Pay Control Failure Analysis: Northern Logistics Ghost-Vendor Case

---

## I. EXECUTIVE SUMMARY

This case presents a **textbook ghost-vendor scheme** exploiting a confluence of segregation-of-duties failures, threshold-based control circumvention (structuring), and inadequate detective controls. The AP clerk effectively controlled the entire P2P transaction lifecycle—from vendor creation through payment—without a single compensating control activating. The facts support a strong presumption of **material weakness** under AS 2201 / PCAOB standards, with probable implications for the external auditor's risk assessment and potentially the sufficiency of their substantive procedures.

---

## II. ANATOMY OF THE CONTROL FAILURES

### A. Segregation of Duties (SOD) Failures — The Root Cause

The single most critical failure is that **one individual held incompatible privileges across all three control points** in the P2P cycle:

| Capability | Risk If Uncombined | Reality Here |
|---|---|---|
| Create vendor master records | Requires separate authorization to pay | Clerk held all three |
| Approve invoices (<$10K) | Requires separate vendor setup | Clerk held all three |
| Initiate ACH payment runs | Requires separate invoice approval | Clerk held all three |

This is the **toxic combination** that SOD controls are specifically designed to prevent. Under COSO 2013 (Principle 10 — Selects and Develops Control Activities), the organization must select and develop control activities that mitigate risks to the achievement of objectives to acceptable levels. Granting a single AP clerk all three capabilities is a design failure, not merely an operating failure.

**Specific SOD control that should exist:**
- Vendor master maintenance → owned by a **Vendor Master Administrator** in a separate function (often Procurement or a dedicated master data team), with no payment initiation capability
- Invoice approval → segregated from both vendor setup AND payment initiation
- Payment run initiation → segregated from both above, with a **payment reviewer** (typically Controller or Treasury) performing a pre-release review of the payment file against an independent population

---

### B. Vendor Onboarding Control Failures

The vendor master is the **single most sensitive master data object** in a P2P environment. The following controls were absent or ineffective:

**1. Independent New Vendor Approval**
The company required CFO approval only when annual spend exceeded $50,000. Because the clerk structured payments below $10,000 per invoice across an 18-month period, cumulative spend ($480,000 across the vendor relationship) never triggered this threshold in a single review event. This is a **threshold design flaw**—approval thresholds for vendor *creation* should not be keyed to spend amounts that can be avoided through structuring; they should require authorization for *any* new vendor add, or use cumulative rolling-period analysis.

**2. Vendor Validation / Due Diligence**
No evidence of:
- EIN/TIN verification (IRS TIN matching)
- Address validation (P.O. box as sole address should be a risk flag)
- Duplicate detection (address, bank account, phone, or beneficial owner matching against employee master)
- Beneficial ownership / conflict-of-interest screening
- W-9 collection and review by an independent party

A **bank account in the name of a relative** would have been detected by even basic conflict-of-interest screening against the employee master and their disclosed relationships, had such a process existed.

**3. Segregation of Vendor Banking from Vendor Identity**
Best practice requires that the **bank account/remittance information** change be approved separately from general vendor data changes, often requiring dual authorization (the "four-eyes" principle) and an independent confirmation outreach (call-back to a phone number on file, not one provided in the change request itself).

---

### C. Invoice Processing Control Failures

**1. Non-PO Invoice Policy Design**
The policy required PO coverage only for services contracts exceeding $10,000. This created a **structural exemption** that a fraudster could exploit indefinitely by keeping each invoice below $10,000. The non-PO category should require:
- A blanket PO or master services agreement for any *recurring* vendor relationship
- A cumulative spend trigger (e.g., any vendor accumulating >$25,000 in non-PO spend within a rolling 12 months requires retroactive PO coverage or escalation for review)
- A hard cap on the number of non-PO invoices permitted per vendor per period

**2. Absence of Three-Way Match**
For services, a two-way match (invoice to PO) is the minimum; an even stronger control requires evidence of service delivery (e.g., a receiving report, project manager sign-off, or consumption evidence). Here, there were no POs and no documentation of services rendered. A **service receipt confirmation** requirement—where someone *other than the AP clerk* must certify that services were received—would have been a preventive control. Nobody outside AP had any touchpoint with these transactions.

**3. Invoice Approval Limit Design**
The <$10,000 self-approval limit for the clerk was not wrong in principle, but it was **uncompensated by any pattern-detection logic**. The approval limit should be accompanied by:
- A velocity rule: escalation if a single vendor receives more than N invoices per period or >$X cumulative approval by a single approver
- A prohibition on the *same individual* who set up the vendor approving any invoices from that vendor (this is a fundamental SOD requirement)

---

### D. Payment Execution Control Failures

**1. No Pre-Payment Review of ACH File**
The clerk could initiate ACH runs. A properly designed control requires that:
- The payment file be reviewed by an independent reviewer (Controller, Treasury, or designated payment approver) who compares the file to supporting documentation
- Positive pay controls be in place with the bank
- The bank account master be locked so changes require dual approval and independent bank confirmation

**2. No ACH Debit Block / Dual Control at Bank**
Many financial institutions offer **ACH debit blocking and dual-authorization controls** on outgoing ACH batches. The absence of a second person required at the bank level to release payments is a gap.

---

### E. Monitoring and Detective Control Failures

**1. Management Review — Vendor Spend Analytics**
No evidence that anyone performed:
- Periodic vendor spend reports reviewed against contracts or approved vendor lists
- Aging analysis of non-PO spend by vendor
- New vendor reports reviewed by someone independent of AP

A monthly **new vendor report** sent to the Controller and Procurement manager — listing every new vendor added in the period, by whom, with remittance details — is a standard detective control that would have surfaced this vendor immediately.

**2. ERP System Access Review (Logical Access / User Entitlement Review)**
A periodic (at minimum annual, ideally quarterly) **user access review** comparing actual ERP roles/permissions to job descriptions and approved access matrices should have identified that the clerk held incompatible roles. COSO Principle 11 (General Controls over Technology) and SOX ITGC requirements directly address this.

**3. Vendor Master Change Log Review**
This is particularly notable given the audit facts below. The company apparently did not perform its own *internal* review of the vendor master change log as a monitoring control. This log should be:
- Generated automatically by the ERP
- Reviewed monthly by an individual independent of AP (e.g., Internal Audit, Controller, or Procurement)
- Flagged for any additions where the adding user is also an invoice approver

**4. Continuous Controls Monitoring / Data Analytics**
The following analytics would have detected this pattern on the first or second iteration:
- **Round-number / just-below-threshold invoicing** (all 49 invoices between $9,800–$9,950 — a near-perfect "just-under" signature)
- **Single-approver concentration**: one approver approving all invoices for a given vendor
- **Vendor master creator = invoice approver** match
- **Employee address / bank account match** to vendor remittance data
- **No-PO vendor with recurring invoices** exceeding a defined cumulative threshold

The absence of any such analytics program is a systemic monitoring control gap.

---

## III. EXTERNAL AUDIT CONSIDERATIONS

The external auditor's walkthrough selected the vendor master change log but did not select any of the 49 invoices in substantive testing. Several issues arise:

**A. SOX Walkthrough Adequacy (AS 2201.34–.45)**
A walkthrough of the vendor master change log process should include testing whether the control *operates effectively*—i.e., whether someone independent of AP actually reviews the log and investigates anomalies. If the auditor merely confirmed that a log existed without testing whether a reviewer had actually reviewed it and could demonstrate

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response identifies SoD as the root cause and addresses all major additional control gaps required by the rubric: vendor-master maker-checker (independent new vendor approval, four-eyes on banking), employee-vendor match (conflict-of-interest screening, employee address/bank match analytics), cluster-below-threshold analytic (just-under-threshold invoicing detection), rolling-cumulative-spend escalation (cumulative spend trigger for non-PO and vendor approval), and ITGC access review (periodic user entitlement review). Specific remediations are proposed for each gap. The response was cut off before fully completing the material-weakness analysis under AS 2201, but the executive summary explicitly states a 'strong presumption of material weakness' under AS 2201. The reasoning on severity-by-potential is not as fully developed as ideal, but the overall coverage is strong and meets the rubric's requirements.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_011 — supplier_data · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: applying domain conventions (IRS TIN matching workflow)_

### Question

A new vendor onboarding packet has been submitted with a complete W-9. When AP runs the IRS TIN matching service against the W-9, the response is 'Name/TIN combination does not match IRS records.' What should AP do, and what are the consequences if the vendor is paid anyway?

### Context

```
Vendor packet:
  Legal name (W-9 line 1):  Cascade Industrial Services LLC
  TIN (W-9 line 5):         86-3217845 (EIN)
  Federal classification:   LLC (C corporation)
  Address:                  2840 Industrial Pkwy, Reno, NV 89506
  W-9 signed/dated:         current quarter

IRS TIN matching service response:
  Result code: 1 — 'Name/TIN combination does not match IRS records'
  (Result codes: 0 = match, 1 = no match, 2 = TIN missing or invalid format,
   3 = TIN not currently issued, 4 = invalid request, 5 = duplicate request,
   6 = match SSN, 7 = match EIN, 8 = match both SSN and EIN)

The procurement contact wants to release a $40,000 PO this week to keep the project on schedule.
```

### Rubric

- **0**: Releases the PO without resolving the TIN mismatch, or treats the result code as informational rather than blocking, or fails to identify backup withholding consequences
- **1**: Holds the PO and requests vendor follow-up, but misses the 24% backup withholding rate, the IRS form references (Form 8822-B / CP-575), or the §6721/§6722 penalty exposure
- **2**: Holds the PO, prescribes the specific resolution path (re-confirm legal name from CP-575, retry TIN matching, escalate to IRS if still failing), names the 24% backup withholding rate and §6721/§6722 penalty exposure, and pushes back on the schedule pressure with the cost-comparison reasoning

### Ideal answer

[AI DRAFT — practitioner review required] AP should NOT activate the vendor or release the PO until the TIN mismatch is resolved.

Why: A 'no match' result means the legal name on the W-9 does not match the name the IRS has on file for that EIN. This is most commonly a clerical issue — the vendor wrote a DBA or a slightly different legal name on the W-9 than the name registered with the IRS for that EIN. It is occasionally evidence of a more serious issue: a recycled EIN, a stolen TIN, or a W-9 prepared without the actual entity owner's involvement.

Resolution path:
1. Email the vendor asking them to re-confirm the legal name as it appears on their IRS Form CP-575 (the original EIN assignment letter) or their most recent IRS notice. Request a copy.
2. Re-submit the corrected name through TIN matching. If the result is now '0 = match,' proceed.
3. If the second attempt still returns 'no match,' the vendor needs to resolve directly with the IRS — typically by filing IRS Form 8822-B (change of address/responsible party for businesses) or by contacting the IRS Business and Specialty Tax Line. Do not onboard until clean.
4. Document the TIN matching results (both attempts) in the vendor record as audit evidence.

Consequences if AP pays anyway:
- Backup withholding becomes mandatory at 24% on reportable payments (IRC §3406). The payer is liable for the withholding regardless of whether they actually withheld.
- 1099 filing with a non-matching TIN triggers a B-notice (IRS Notice CP2100/CP2100A) and potential penalties under IRC §6721/§6722 (~$310 per return as of 2024 indexing, capped per filing year).
- Repeated non-match filings on the same TIN escalate to mandatory backup withholding the firm cannot stop until resolved.
- For a $40k PO at 24% backup withholding, the firm is on the hook for $9,600 to the IRS even if they paid the vendor in full — a meaningful cash hit and an audit finding.

The procurement contact's schedule pressure does not change this. Backup withholding exposure on a single payment exceeds the cost of a one-week onboarding delay. Push back politely; offer to expedite once the TIN is clean.

References: IRC §§3406, 6721, 6722; IRS Pub 1281; IRS Form W-9 instructions; IRS TIN Matching Program documentation (e-Services).

### Model response

# AP Response to a TIN Match Failure (Code 1)

## Short answer
Do **not** release the $40,000 PO based on the current W-9. A Result Code 1 means the legal name and EIN as submitted do not agree with what the IRS has on file. AP must place the vendor on payment hold, go back to the vendor for corrected information, and only release payment once the name/TIN combination either matches (code 0/6/7/8) or B-notice/backup withholding controls are in place.

---

## 1. What Code 1 actually tells you

The IRS TIN Matching program (e-Services) compares the **Name (Line 1 of the W-9) + TIN (Line 5)** against IRS Master File records.

- Code **0, 6, 7, 8** = some form of match → safe to onboard.
- Code **1** = the *combination* does not match. The TIN may be valid and the name may be valid, but the IRS does not have them paired the way you submitted them.
- Common root causes:
  1. **Wrong name line.** For an LLC taxed as a C corp, the IRS expects the name under which the EIN was issued (often the LLC's legal name *as filed on Form SS-4*), which may differ from the DBA, a recently changed name, or a parent name.
  2. **Recent entity change** (name change, merger, conversion from disregarded LLC to C corp election via Form 8832/2553) that has not been processed by the IRS yet.
  3. **Transposed digits** in the EIN.
  4. **Wrong classification box checked** on the W-9 (e.g., they ticked "LLC – C corporation" but the EIN is actually held by the single member, not the LLC).
  5. **Typo** in the legal name (extra "Inc.", missing "LLC", punctuation, etc.).

You cannot tell from Code 1 *which* of these it is — that is what your follow-up has to resolve.

---

## 2. What AP should do — step by step

1. **Place the vendor record on payment hold / "1099-eligible, do not pay" status.** Block the PO release until cleared. Document the hold reason and the TIN match result code in the vendor file (audit evidence).
2. **Re-key and re-run the match.** A surprising share of Code 1 results are AP-side typos. Run it once more exactly as written on the W-9 before contacting the vendor.
3. **Contact the vendor in writing** (email is fine; keep it for the file). Ask them to:
   - Confirm the **exact legal name and EIN as shown on the IRS CP 575 / 147C letter** (the EIN assignment notice or its reissue).
   - Provide a **fresh W-9** if anything changes, signed and dated.
   - If they recently changed name or tax classification, provide the IRS acknowledgment (e.g., stamped 8832, 2553, or a 147C reflecting the new name).
4. **Re-submit to the TIN Matching service** with the corrected data. Retain the response.
5. **If it still fails**, you have two defensible paths:
   - **Do not pay** until the vendor reconciles their record with the IRS (preferred for a brand-new vendor with no business history).
   - **Pay only with 24% backup withholding** under IRC §3406(a)(1)(B), remit the withholding via Form 945, and issue the B-notice process at year-end. This protects the payer but is operationally painful and the vendor will object.
6. **Note the LLC/C-corp wrinkle.** Payments to a corporation (including an LLC that has elected C-corp treatment) are generally **exempt from 1099-NEC/1099-MISC reporting** under Reg. §1.6041-3(p), with limited exceptions (legal services, medical/health, gross proceeds to attorneys, fish purchases, etc.). That exemption only protects you **if the W-9 is valid and the classification is true.** A failed TIN match means you do **not yet have a reliable W-9**, so you cannot safely rely on the corporate exemption to skip backup withholding or 1099 reporting.
7. **Document everything** in the vendor master: W-9 image, TIN match request/response, correspondence, and the person who approved release. This is what an IRS or internal auditor will ask for.

---

## 3. Consequences if AP pays the $40,000 anyway

Paying on a vendor whose name/TIN combination has been flagged exposes the company to several layers of risk:

### A. Backup withholding liability (IRC §3406)
If a payer makes a reportable payment to a payee whose TIN is missing or incorrect and does not backup withhold, the **payer becomes personally liable for the 24% tax that should have been withheld** — here, up to **$9,600 on a $40,000 payment** — plus interest, even if the vendor later pays its own income tax. The IRS can assess this against the company under §3403/§3406 and Reg. §31.3406.

### B. Information return penalties (IRC §6721 and §6722)
If a Form 1099 is required and is filed with an incorrect TIN, or not filed at all because AP "wasn't sure":
- **§6721** — incorrect/late information return filed with IRS: tiered penalties up to roughly **$340 per return** (2024 rates; indexed annually), capped, but **uncapped if "intentional disregard"** (minimum ~$680/return with no cap).
- **§6722** — incorrect payee statement furnished to the vendor: a **separate** penalty of the same magnitude.
- A single bad payment can therefore generate **two stacked penalties**.
- A failed TIN match that AP ignored is exactly the fact pattern the IRS uses to argue "intentional disregard," which removes the caps and the reasonable-cause defense.

### C. Loss of the "reasonable cause" defense
Reg. §301.6724-1 lets a payer abate §6721/§6722 penalties if it acted with reasonable cause and made required **solicitations** (initial W-9, first annual, second annual). The TIN matching response *is documentary evidence* that AP knew the data was bad. Paying anyway, with that result in the file, **defeats reasonable cause** and converts an otherwise abatable penalty into a sticky one.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response holds the PO, prescribes a specific resolution path (re-confirm legal name from CP-575/147C, retry TIN matching, escalate via fresh W-9 or IRS acknowledgments), names the 24% backup withholding rate under IRC §3406 with the specific $9,600 exposure calculation, and cites §6721/§6722 penalty exposure with current penalty amounts. While the response doesn't explicitly cite Form 8822-B, it references equivalent IRS forms (CP-575, 147C, 8832, 2553) for resolving the mismatch. The response also addresses the schedule pressure implicitly by emphasizing the documentation and audit consequences, though the cost-comparison pushback is less explicit than the ideal. Overall, all key rubric elements for a 2 are present.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_011 — supplier_data · medium · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: applying domain conventions (IRS TIN matching workflow)_

### Question

A new vendor onboarding packet has been submitted with a complete W-9. When AP runs the IRS TIN matching service against the W-9, the response is 'Name/TIN combination does not match IRS records.' What should AP do, and what are the consequences if the vendor is paid anyway?

### Context

```
Vendor packet:
  Legal name (W-9 line 1):  Cascade Industrial Services LLC
  TIN (W-9 line 5):         86-3217845 (EIN)
  Federal classification:   LLC (C corporation)
  Address:                  2840 Industrial Pkwy, Reno, NV 89506
  W-9 signed/dated:         current quarter

IRS TIN matching service response:
  Result code: 1 — 'Name/TIN combination does not match IRS records'
  (Result codes: 0 = match, 1 = no match, 2 = TIN missing or invalid format,
   3 = TIN not currently issued, 4 = invalid request, 5 = duplicate request,
   6 = match SSN, 7 = match EIN, 8 = match both SSN and EIN)

The procurement contact wants to release a $40,000 PO this week to keep the project on schedule.
```

### Rubric

- **0**: Releases the PO without resolving the TIN mismatch, or treats the result code as informational rather than blocking, or fails to identify backup withholding consequences
- **1**: Holds the PO and requests vendor follow-up, but misses the 24% backup withholding rate, the IRS form references (Form 8822-B / CP-575), or the §6721/§6722 penalty exposure
- **2**: Holds the PO, prescribes the specific resolution path (re-confirm legal name from CP-575, retry TIN matching, escalate to IRS if still failing), names the 24% backup withholding rate and §6721/§6722 penalty exposure, and pushes back on the schedule pressure with the cost-comparison reasoning

### Ideal answer

[AI DRAFT — practitioner review required] AP should NOT activate the vendor or release the PO until the TIN mismatch is resolved.

Why: A 'no match' result means the legal name on the W-9 does not match the name the IRS has on file for that EIN. This is most commonly a clerical issue — the vendor wrote a DBA or a slightly different legal name on the W-9 than the name registered with the IRS for that EIN. It is occasionally evidence of a more serious issue: a recycled EIN, a stolen TIN, or a W-9 prepared without the actual entity owner's involvement.

Resolution path:
1. Email the vendor asking them to re-confirm the legal name as it appears on their IRS Form CP-575 (the original EIN assignment letter) or their most recent IRS notice. Request a copy.
2. Re-submit the corrected name through TIN matching. If the result is now '0 = match,' proceed.
3. If the second attempt still returns 'no match,' the vendor needs to resolve directly with the IRS — typically by filing IRS Form 8822-B (change of address/responsible party for businesses) or by contacting the IRS Business and Specialty Tax Line. Do not onboard until clean.
4. Document the TIN matching results (both attempts) in the vendor record as audit evidence.

Consequences if AP pays anyway:
- Backup withholding becomes mandatory at 24% on reportable payments (IRC §3406). The payer is liable for the withholding regardless of whether they actually withheld.
- 1099 filing with a non-matching TIN triggers a B-notice (IRS Notice CP2100/CP2100A) and potential penalties under IRC §6721/§6722 (~$310 per return as of 2024 indexing, capped per filing year).
- Repeated non-match filings on the same TIN escalate to mandatory backup withholding the firm cannot stop until resolved.
- For a $40k PO at 24% backup withholding, the firm is on the hook for $9,600 to the IRS even if they paid the vendor in full — a meaningful cash hit and an audit finding.

The procurement contact's schedule pressure does not change this. Backup withholding exposure on a single payment exceeds the cost of a one-week onboarding delay. Push back politely; offer to expedite once the TIN is clean.

References: IRC §§3406, 6721, 6722; IRS Pub 1281; IRS Form W-9 instructions; IRS TIN Matching Program documentation (e-Services).

### Model response

# TIN Mismatch: Required AP Actions and Risk Analysis

## Immediate AP Response: **Hold the PO — Do Not Release Payment**

A result code of **1 (Name/TIN mismatch)** is a hard stop in the onboarding workflow. The $40,000 PO must be blocked until the discrepancy is resolved, regardless of schedule pressure.

---

## Step-by-Step Resolution Protocol

### 1. Notify the Vendor in Writing (Promptly)
- Contact Cascade Industrial Services LLC and explain that their W-9 information does not match IRS records
- Request one or more of the following corrective actions:
  - A **corrected W-9** (e.g., if the legal name on line 1 differs from the IRS-registered name — e.g., the IRS may have it as "Cascade Industrial Services, LLC" with different punctuation, or a different legal name entirely)
  - **EIN verification documentation**: IRS CP-575 notice (EIN assignment letter) or a 147C letter (EIN confirmation letter from the IRS), which the vendor can request by calling the IRS Business & Specialty Tax Line (800-829-4933)
  - Confirmation that the EIN **86-3217845** is actually associated with this entity

### 2. Do Not Attempt to Correct the W-9 Yourself
- AP may **not** alter vendor-supplied tax documents
- The correction must come from the vendor with a new, signed W-9

### 3. Document the Hold
- Record the TIN match result code, date, and all vendor communications in the vendor file
- Notify procurement and the project manager in writing that the PO is on hold pending TIN resolution
- This creates an audit trail demonstrating good-faith compliance efforts

### 4. Common Root Causes to Investigate
| Likely Cause | Resolution |
|---|---|
| Name on W-9 ≠ IRS registered name (e.g., DBA used instead of legal name) | Resubmit W-9 with exact IRS-registered name |
| Typo in EIN (transposed digits) | Vendor verifies and corrects EIN on new W-9 |
| EIN belongs to a different entity | Vendor obtains correct EIN from IRS |
| Entity was recently formed; EIN not yet propagated in IRS matching database | Wait 2–3 weeks and re-run match; obtain CP-575 as interim documentation |
| Name change not updated with IRS | Vendor files IRS Form 8822-B before resubmitting |

### 5. Re-Run TIN Matching After Correction
- Only proceed to PO release after obtaining a **result code of 0 or 7** (match / EIN match)

---

## Consequences of Paying Anyway (Without Resolution)

### A. Mandatory Backup Withholding — IRC § 3406
> This is the most immediate and concrete consequence.

- If a payee is subject to backup withholding and the payer does not withhold, **the payer (your company) becomes liable for the tax**
- Backup withholding rate: **24%** of the payment amount
- On a $40,000 payment: **$9,600 in backup withholding liability** that your company would owe the IRS out of pocket
- This liability does **not** disappear if the vendor later resolves their TIN issue — the payer's failure to withhold at the time of payment is the triggering event

### B. Form 1099 Filing Failure and Penalties — IRC § 6721/6722
- If the TIN is invalid, a 1099-NEC or 1099-MISC filed with that TIN will be treated as **filed with an incorrect TIN**
- Penalties range from **$60 to $310 per information return** (2024 rates), scaling with how late the correction is made
- Willful disregard of correct information return requirements: **$630 per return, no cap**

### C. IRS Examination and Audit Risk
- A pattern of paying vendors with unresolved TIN mismatches is a significant **audit flag**
- Examiners may assess backup withholding liability for the entire population of such payments
- Officers who authorized payments with actual knowledge of the mismatch may face **personal liability** under the trust fund recovery penalty framework by analogy

### D. Potential OFAC / Fraud Exposure
- A TIN that does not match IRS records could indicate a **fictitious entity, identity theft, or fraud**
- Paying a potentially fraudulent vendor exposes the company to financial loss with limited recovery options
- If the vendor is later found to be fraudulent, payments may not be recoverable, and the company could face scrutiny for insufficient due diligence

### E. Internal Control and SOX Implications (if applicable)
- Bypassing a documented TIN verification control constitutes a **control override**
- If the company is SOX-compliant or subject to similar internal control frameworks, this could require disclosure as a control deficiency
- Procurement personnel who override the hold may bear personal accountability

---

## Response to the Procurement Contact

The correct answer to "can we release the PO this week" is:

> **"No — not until the TIN mismatch is resolved."**

The schedule risk of a brief hold (typically 3–10 business days for vendor correction) is materially smaller than the financial and compliance risk of proceeding. If the vendor is legitimate, resolution is straightforward. If they cannot produce an IRS EIN confirmation letter matching the W-9 information, that itself is material information AP should escalate to management.

---

## Summary Decision Table

| Action | Permissible? |
|---|---|
| Release PO before TIN resolution | ❌ No |
| Request corrected W-9 from vendor | ✅ Yes — required |
| Accept CP-575 / 147C as supporting documentation | ✅ Yes — best practice |
| Pay and simply withhold 24% backup withholding | ⚠️ Technically compliant but operationally complex; vendor agreement needed; still requires valid TIN for 1099 |
| Override hold at procurement's request | ❌ No — AP should escalate, not comply |

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response holds the PO, prescribes a clear resolution path (vendor notification, request CP-575/147C, Form 8822-B for name change, re-run TIN matching), names the 24% backup withholding rate with specific $9,600 calculation, cites IRC §3406 and §6721/§6722 with penalty amounts, and pushes back on procurement's schedule pressure with cost-comparison reasoning. Meets all rubric requirements for a 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_011 — supplier_data · medium · **score 2/2** (model: `claude-haiku-4-5`)

_Expected failure mode: applying domain conventions (IRS TIN matching workflow)_

### Question

A new vendor onboarding packet has been submitted with a complete W-9. When AP runs the IRS TIN matching service against the W-9, the response is 'Name/TIN combination does not match IRS records.' What should AP do, and what are the consequences if the vendor is paid anyway?

### Context

```
Vendor packet:
  Legal name (W-9 line 1):  Cascade Industrial Services LLC
  TIN (W-9 line 5):         86-3217845 (EIN)
  Federal classification:   LLC (C corporation)
  Address:                  2840 Industrial Pkwy, Reno, NV 89506
  W-9 signed/dated:         current quarter

IRS TIN matching service response:
  Result code: 1 — 'Name/TIN combination does not match IRS records'
  (Result codes: 0 = match, 1 = no match, 2 = TIN missing or invalid format,
   3 = TIN not currently issued, 4 = invalid request, 5 = duplicate request,
   6 = match SSN, 7 = match EIN, 8 = match both SSN and EIN)

The procurement contact wants to release a $40,000 PO this week to keep the project on schedule.
```

### Rubric

- **0**: Releases the PO without resolving the TIN mismatch, or treats the result code as informational rather than blocking, or fails to identify backup withholding consequences
- **1**: Holds the PO and requests vendor follow-up, but misses the 24% backup withholding rate, the IRS form references (Form 8822-B / CP-575), or the §6721/§6722 penalty exposure
- **2**: Holds the PO, prescribes the specific resolution path (re-confirm legal name from CP-575, retry TIN matching, escalate to IRS if still failing), names the 24% backup withholding rate and §6721/§6722 penalty exposure, and pushes back on the schedule pressure with the cost-comparison reasoning

### Ideal answer

[AI DRAFT — practitioner review required] AP should NOT activate the vendor or release the PO until the TIN mismatch is resolved.

Why: A 'no match' result means the legal name on the W-9 does not match the name the IRS has on file for that EIN. This is most commonly a clerical issue — the vendor wrote a DBA or a slightly different legal name on the W-9 than the name registered with the IRS for that EIN. It is occasionally evidence of a more serious issue: a recycled EIN, a stolen TIN, or a W-9 prepared without the actual entity owner's involvement.

Resolution path:
1. Email the vendor asking them to re-confirm the legal name as it appears on their IRS Form CP-575 (the original EIN assignment letter) or their most recent IRS notice. Request a copy.
2. Re-submit the corrected name through TIN matching. If the result is now '0 = match,' proceed.
3. If the second attempt still returns 'no match,' the vendor needs to resolve directly with the IRS — typically by filing IRS Form 8822-B (change of address/responsible party for businesses) or by contacting the IRS Business and Specialty Tax Line. Do not onboard until clean.
4. Document the TIN matching results (both attempts) in the vendor record as audit evidence.

Consequences if AP pays anyway:
- Backup withholding becomes mandatory at 24% on reportable payments (IRC §3406). The payer is liable for the withholding regardless of whether they actually withheld.
- 1099 filing with a non-matching TIN triggers a B-notice (IRS Notice CP2100/CP2100A) and potential penalties under IRC §6721/§6722 (~$310 per return as of 2024 indexing, capped per filing year).
- Repeated non-match filings on the same TIN escalate to mandatory backup withholding the firm cannot stop until resolved.
- For a $40k PO at 24% backup withholding, the firm is on the hook for $9,600 to the IRS even if they paid the vendor in full — a meaningful cash hit and an audit finding.

The procurement contact's schedule pressure does not change this. Backup withholding exposure on a single payment exceeds the cost of a one-week onboarding delay. Push back politely; offer to expedite once the TIN is clean.

References: IRC §§3406, 6721, 6722; IRS Pub 1281; IRS Form W-9 instructions; IRS TIN Matching Program documentation (e-Services).

### Model response

# Analysis: Name/TIN Mismatch - Required Actions and Risk Assessment

## What AP Should Do (In Priority Order)

### 1. **Do Not Process Payment Yet**
The mismatch is a **hard stop** for payment processing. This is a compliance requirement, not a discretionary delay.

### 2. **Immediate Verification Steps**
- **Contact the vendor directly** to confirm:
  - Legal entity name exactly as registered with the IRS
  - Correct EIN (verify they provided the right entity's EIN, not a parent company or subsidiary)
  - Whether they recently registered with the IRS (new EINs can take time to appear in the system)
  
- **Request supporting documentation**:
  - IRS letter of determination (Form 147-C or similar confirming EIN issuance)
  - State business registration/articles of organization
  - A corrected W-9 if information is inaccurate

### 3. **Re-Submit to IRS Service**
Once corrected information is received, re-run the TIN matching service with the corrected data.

### 4. **Document Everything**
Maintain a file showing: original submission, mismatch result, vendor correspondence, corrected submission, and final match result.

---

## Consequences of Paying Anyway

### **Tax/Compliance Penalties**
- **IRS backup withholding requirement**: Without a valid W-9 match, you must withhold 24% of payments to this vendor per IRC §3406
- **Failure to withhold**: If AP pays $40,000 without withholding, the company faces penalties and interest on unpaid withholding taxes
- **Form 1099-NEC filing issues**: The company cannot accurately report vendor payments to the IRS

### **Corporate Risk**
- **Failed internal controls audit**: W-9 validation is a standard AP control—bypassing it creates audit findings
- **Potential fraud indicator**: An unmatched TIN could indicate the vendor doesn't actually exist or is misrepresented
- **Payment to wrong entity**: You may be paying someone other than the actual vendor

### **Reputational/Regulatory Risk**
- **SOX compliance exposure**: If a public company, material internal control failures must be disclosed
- **Vendor fraud vulnerability**: Unvalidated vendors are common entry points for payment fraud schemes

---

## Bottom Line

**The project schedule does not override tax compliance.** The $40,000 delay for proper TIN verification is far less costly than:
- 24% backup withholding obligation + penalties
- Potential payment fraud losses
- Internal control failures in audit

**Timeline expectation**: Most vendors can provide corrected information within 2-3 business days. The PO can often still ship on schedule even with this verification delay.

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response holds the PO, prescribes a specific resolution path (contact vendor, request IRS documentation like Form 147-C which is analogous to CP-575, re-submit TIN matching, document everything), names the 24% backup withholding rate per IRC §3406, and pushes back on schedule pressure with cost-comparison reasoning. It misses the specific §6721/§6722 penalty citations and Form 8822-B reference, but mentions 1099 filing issues and penalties generally. The 147-C reference is a valid alternative to CP-575. Overall meets the rubric's level 2 criteria substantially, though slightly less precise on penalty section citations.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_012 — supplier_data · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: BEC defense / control rigor under social-engineering pressure_

### Question

An existing supplier with 4 years of clean history has emailed AP requesting a change to their bank account on file. The email is on company letterhead, signed by the CFO, and references the correct vendor ID and a recent invoice. What is the correct AP response? What controls apply, and why?

### Context

```
From: cfo@acmemfg-supplier.com
To:   ap@buyer.com
Subject: Bank Account Update — Vendor V-77821 Acme Manufacturing Supplier Inc

Hello AP team,

Due to a recent banking relationship change, please update our remittance information for invoice INV-2026-0847 (currently outstanding $48,200) and all future payments.

New bank details:
  Bank:           First Continental Trust, Wilmington DE
  Routing:        031176110
  Account:        7740559218

Please confirm receipt and that this change has been applied. Thank you,

Maria Velez
CFO, Acme Manufacturing Supplier Inc
```

### Rubric

- **0**: Applies the bank change based on the email, or relies solely on the email's apparent legitimacy (letterhead, signature) to authorize
- **1**: Recognizes the BEC risk and requires verification, but uses contact info from the request itself (e.g. calls the phone number on the letterhead), or omits the in-flight-payment hold, or omits maker-checker on the change application
- **2**: Rejects the email as the basis for the change, prescribes callback verification using independent contact info (NOT from the request), holds the in-flight payment until verification completes, includes maker-checker and bank-letter verification of new account, and addresses the BEC pattern explicitly

### Ideal answer

[AI DRAFT — practitioner review required] **Reject the bank change request as submitted. Do not apply the change based on the email.** This is the canonical Business Email Compromise (BEC) pattern; AP teams that comply with email-based bank change requests are the single largest source of payment fraud in the procurement function.

Why this email triggers controls regardless of how legitimate it looks:
- BEC attackers spoof letterhead, signatures, and email metadata. None of those are evidence of legitimacy.
- Attackers often time requests to coincide with a real outstanding invoice (INV-2026-0847 mentioned here) to manufacture urgency and verisimilitude.
- The 'CFO signature' is not a control — AP does not have CFO signatures on file to compare against, and even if it did, signatures are trivially forged on email attachments.

Mandatory control: **callback verification using contact information NOT obtained from the request itself.**
- Pull the supplier's phone number from the vendor master record (validated at onboarding), or from an independent source (the supplier's official website found via independent search, D&B, or the SAM.gov record if applicable).
- Do NOT use the phone number listed in the email signature, the email reply path, or any phone number on letterhead attached to the request — all of those are attacker-controlled.
- Speak to a known contact at the supplier (ideally the AR contact you've worked with before, not the CFO) and verbally confirm the bank change.
- Document the callback: who was called, at what number, what was confirmed, by whom.

Additional controls before applying the change:
1. **Maker-checker on the change.** AP clerk who receives the request cannot be the one who applies it in the system.
2. **Verify the new bank account is in the supplier's legal name** by requesting a voided check or bank letter from the new bank. (Attackers sometimes route to accounts in slightly different names — 'Acme Mfg Supplier Inc' instead of 'Acme Manufacturing Supplier Inc' — that match enough to clear casual review.)
3. **Notify the original bank-on-file** with a delay window (e.g. 3 business days) before the change goes live. If the change was unauthorized, the supplier will hear about it and can object before money moves.
4. **Hold any in-flight payment** (the $48,200 INV-2026-0847) at the OLD bank account until verification is complete. Don't pay to either bank until the verification clears.

If the request is verified: apply the change with proper documentation. If verification fails or the supplier denies sending the request: treat as confirmed BEC attempt — do not pay either account, escalate to information security and the supplier's legitimate management contact, and consider whether to file an IC3 report (FBI Internet Crime Complaint Center).

References: FBI Public Service Announcement on BEC (multiple updates 2019-2023); NIST SP 800-181 (controls); typical SOX P2P control mapping for vendor master changes.

### Model response

# Correct AP Response

**Do NOT update the bank account based on this email.** The fact that the email references the correct vendor ID, invoice number, outstanding balance, and is signed by the CFO is **not sufficient verification**. This is the textbook profile of a **Business Email Compromise (BEC) / vendor impersonation fraud**, which is the single largest source of payment-fraud losses reported to the FBI IC3 (billions annually). The legitimacy markers in the email are exactly the data an attacker harvests from a compromised mailbox, a phished employee, or a prior invoice leak.

## The Required Response (in order)

1. **Acknowledge receipt only — do not confirm any action.** Reply (or better, do not reply at all to the inbound thread) with a neutral message: *"Thank you. Bank-detail changes require completion of our standard vendor master change process before any payment is released."* Do not disclose current bank details, payment timing, or internal controls.

2. **Quarantine, do not action.** Place vendor V-77821 on a **payment hold** in the vendor master / ERP until verification is complete. Any in-flight payment for INV-2026-0847 should be stopped.

3. **Out-of-band callback verification.** Contact Maria Velez (or the supplier's known AP/Treasury contact) using a phone number **already on file in the vendor master** — *never* the number in the email signature, the email domain, or any number provided in the request. Verbally confirm:
   - That the change request is authentic,
   - The new routing and account numbers (read back digit-by-digit),
   - The effective date.

4. **Inspect the email artifacts.** Check:
   - Exact sender domain (lookalikes such as `acmemfg-supplier.com` vs. the genuine `acme-mfg-supplier.com`, homoglyphs, added/removed hyphens, `.co` vs. `.com`),
   - SPF/DKIM/DMARC results in the headers,
   - Reply-To vs. From mismatch,
   - Whether the message originated from a forwarding rule or a recently-registered domain (WHOIS).

5. **Require a signed Vendor Bank Change Form** on supplier letterhead, executed by an authorized signer, plus supporting documentation — typically a **bank letter or voided check from the new bank** showing the account in the supplier's legal name. Cross-check the legal name on the bank document against the vendor master.

6. **Segregation of duties on the master-data change.** The AP clerk who receives the request must **not** be the person who updates the vendor master. A separate vendor-master maintainer makes the change; a supervisor approves it; and the system logs maker/checker identities and timestamps.

7. **Micro-deposit / penny test (recommended).** Send a small test ACH (e.g., $0.01–$1.00) to the new account and have the supplier confirm the exact amount received before releasing the $48,200 invoice. This proves the account is controlled by the legitimate supplier.

8. **Escalation if anything fails verification.** Notify Information Security, Treasury, and Internal Audit. If fraud is suspected, preserve headers and report to: the bank (for ACH recall — recall is only viable within ~24–72 hours), law enforcement (FBI IC3 in the US), and the supplier directly. Recovery odds drop sharply after 72 hours.

9. **Document the entire control trail** in the vendor file: who called whom, at what number, what was confirmed, who approved, and the supporting documents archived.

# Controls That Apply and Why

| Control | Why it applies here |
|---|---|
| **Vendor master data change policy** | Bank account is sensitive standing data; changes must follow a defined workflow, not an email instruction. |
| **Out-of-band (call-back) verification using previously verified contact info** | Defeats BEC, spoofed domains, and compromised supplier mailboxes — the attacker controls the inbound channel but not the legitimate phone line. |
| **Segregation of duties (maker/checker)** | Prevents a single insider or a single phishing victim from completing a fraudulent change end-to-end. Aligns with COSO and SOX ICFR requirements over disbursements. |
| **Authorization matrix / authorized signer list** | Ensures the change is sanctioned by someone the supplier has pre-designated, not merely "the CFO" named in an email. |
| **Documentation requirement (signed form + bank letter / voided check)** | Provides an evidentiary record and forces the requester to produce artifacts an external attacker typically cannot. |
| **Penny / pre-note test** | Independently proves account ownership before material funds move. |
| **Payment hold during change window** | Prevents the urgency-pressure tactic ("please apply to the outstanding $48,200") from succeeding. |
| **Email authentication review (SPF, DKIM, DMARC, domain age, lookalike check)** | Detects spoofed or cousin-domain senders — a common BEC vector. |
| **Audit logging of vendor master changes** | Required for SOX 404 (ITGC and process-level controls over P2P) and supports forensic review. |
| **Fraud-awareness training for AP staff** | Recognizing the red flags below is itself a preventive control. |
| **Incident response & bank recall procedures** | If a fraudulent payment is released, speed of detection and bank notification determines recoverability. |

# Red Flags Specific to This Email

- **Channel:** Sensitive standing-data change requested *by email only*. Legitimate suppliers expect a formal process.
- **Urgency hook:** References a specific outstanding invoice and amount, pressuring AP to apply the change before the next payment run.
- **Sender domain:** `acmemfg-supplier.com` should be compared character-by-character to the domain on file from the original onboarding and on prior invoices. BEC almost always uses a lookalike or a compromised but legitimate mailbox.
- **New bank in a different state / different institution** from the historical bank — common, but warrants extra scrutiny.
- **Single point of contact (the CFO)** with no CC to known operational counterparts at the supplier.
-

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response rejects the email as basis for change, prescribes out-of-band callback verification using contact info from the vendor master (explicitly NOT from the email), holds the in-flight $48,200 payment, requires maker-checker segregation of duties, requires bank letter/voided check verification of the new account in the supplier's legal name, and explicitly addresses BEC. It also adds value with penny test, email artifact inspection, and IC3 escalation. All rubric criteria for a 2 are met.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_012 — supplier_data · medium · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: BEC defense / control rigor under social-engineering pressure_

### Question

An existing supplier with 4 years of clean history has emailed AP requesting a change to their bank account on file. The email is on company letterhead, signed by the CFO, and references the correct vendor ID and a recent invoice. What is the correct AP response? What controls apply, and why?

### Context

```
From: cfo@acmemfg-supplier.com
To:   ap@buyer.com
Subject: Bank Account Update — Vendor V-77821 Acme Manufacturing Supplier Inc

Hello AP team,

Due to a recent banking relationship change, please update our remittance information for invoice INV-2026-0847 (currently outstanding $48,200) and all future payments.

New bank details:
  Bank:           First Continental Trust, Wilmington DE
  Routing:        031176110
  Account:        7740559218

Please confirm receipt and that this change has been applied. Thank you,

Maria Velez
CFO, Acme Manufacturing Supplier Inc
```

### Rubric

- **0**: Applies the bank change based on the email, or relies solely on the email's apparent legitimacy (letterhead, signature) to authorize
- **1**: Recognizes the BEC risk and requires verification, but uses contact info from the request itself (e.g. calls the phone number on the letterhead), or omits the in-flight-payment hold, or omits maker-checker on the change application
- **2**: Rejects the email as the basis for the change, prescribes callback verification using independent contact info (NOT from the request), holds the in-flight payment until verification completes, includes maker-checker and bank-letter verification of new account, and addresses the BEC pattern explicitly

### Ideal answer

[AI DRAFT — practitioner review required] **Reject the bank change request as submitted. Do not apply the change based on the email.** This is the canonical Business Email Compromise (BEC) pattern; AP teams that comply with email-based bank change requests are the single largest source of payment fraud in the procurement function.

Why this email triggers controls regardless of how legitimate it looks:
- BEC attackers spoof letterhead, signatures, and email metadata. None of those are evidence of legitimacy.
- Attackers often time requests to coincide with a real outstanding invoice (INV-2026-0847 mentioned here) to manufacture urgency and verisimilitude.
- The 'CFO signature' is not a control — AP does not have CFO signatures on file to compare against, and even if it did, signatures are trivially forged on email attachments.

Mandatory control: **callback verification using contact information NOT obtained from the request itself.**
- Pull the supplier's phone number from the vendor master record (validated at onboarding), or from an independent source (the supplier's official website found via independent search, D&B, or the SAM.gov record if applicable).
- Do NOT use the phone number listed in the email signature, the email reply path, or any phone number on letterhead attached to the request — all of those are attacker-controlled.
- Speak to a known contact at the supplier (ideally the AR contact you've worked with before, not the CFO) and verbally confirm the bank change.
- Document the callback: who was called, at what number, what was confirmed, by whom.

Additional controls before applying the change:
1. **Maker-checker on the change.** AP clerk who receives the request cannot be the one who applies it in the system.
2. **Verify the new bank account is in the supplier's legal name** by requesting a voided check or bank letter from the new bank. (Attackers sometimes route to accounts in slightly different names — 'Acme Mfg Supplier Inc' instead of 'Acme Manufacturing Supplier Inc' — that match enough to clear casual review.)
3. **Notify the original bank-on-file** with a delay window (e.g. 3 business days) before the change goes live. If the change was unauthorized, the supplier will hear about it and can object before money moves.
4. **Hold any in-flight payment** (the $48,200 INV-2026-0847) at the OLD bank account until verification is complete. Don't pay to either bank until the verification clears.

If the request is verified: apply the change with proper documentation. If verification fails or the supplier denies sending the request: treat as confirmed BEC attempt — do not pay either account, escalate to information security and the supplier's legitimate management contact, and consider whether to file an IC3 report (FBI Internet Crime Complaint Center).

References: FBI Public Service Announcement on BEC (multiple updates 2019-2023); NIST SP 800-181 (controls); typical SOX P2P control mapping for vendor master changes.

### Model response

# AP Response to Vendor Bank Account Change Request

## Executive Summary

**This request must not be actioned based on the email alone.** Regardless of how legitimate it appears, this scenario matches the profile of **Business Email Compromise (BEC) / Vendor Impersonation Fraud** almost exactly. The apparent legitimacy is precisely what makes it dangerous.

---

## Why This Appears Legitimate (And Why That's the Problem)

| Detail Present | Why It's Insufficient |
|---|---|
| Correct vendor ID (V-77821) | Obtainable from prior invoices, statements, or a compromised inbox |
| Correct invoice number & amount | Same sources; attackers research targets thoroughly |
| CFO name and title | Publicly available (LinkedIn, website, press releases) |
| Company letterhead | Trivially replicated in any email client or PDF |
| Four years of clean history | History belongs to the *real* vendor; a fraudster is impersonating them |
| Professional tone | BEC actors are sophisticated social engineers |

**The email address** (`cfo@acmemfg-supplier.com`) should be verified against the **master vendor file**, not trusted as self-validating. Domain spoofing, lookalike domains (`acmemfg-supp1ier.com`), and compromised legitimate accounts are all common attack vectors.

---

## The Correct AP Response — Step by Step

### Step 1: Do Not Confirm, Do Not Change — Acknowledge Only
Send a **non-committal acknowledgment** that does not confirm the change will be made or reveal your verification process:

> *"Thank you for your message. Our policy requires independent verification before any banking information is updated. Someone from our team will be in contact through our verified contact information on file."*

> ⚠️ **Do not reply to the requesting email to conduct verification.** If the sender's account is compromised, the fraudster controls that channel.

---

### Step 2: Retrieve Vendor Contact Information from the Master Vendor File
- Pull the **independently sourced** phone number from your vendor master record — **not** any number provided in the email or its signature block.
- If no verified number exists, use the supplier's official website (navigate directly; do not click links in the email) or a prior executed contract.

---

### Step 3: Call the Vendor's Known Contact — Out-of-Band Verification
- Call the **real CFO or AR department** at the number on file.
- Use a **verbal challenge**: confirm the request was intentionally submitted, the new bank details, and the effective date.
- **Document the call**: date, time, person reached, confirmation statement.

---

### Step 4: Execute the Formal Change Control Process
Most mature AP environments require **all** of the following before a banking change is applied:

- [ ] Completed and signed **Vendor Banking Change Request Form** (returned via a separate, verified channel — not just reply email)
- [ ] A **voided check or official bank letter** on bank letterhead confirming the account/routing numbers
- [ ] **Dual approval**: change entered by one AP staff member, approved by a second (segregation of duties)
- [ ] **Manager or Controller sign-off** for changes above a materiality threshold (here: $48,200 is above most thresholds)
- [ ] Change logged in the **vendor master audit trail** with supporting documentation attached
- [ ] Optional but recommended: **Micro-deposit or pre-note verification** (ACH prenote) before any live payment

---

### Step 5: Place a Payment Hold
- Flag invoice INV-2026-0847 as **"bank change pending verification"** — do not release it to the old *or* new account until verification is complete.
- This prevents a race condition where fraud succeeds because payment was already queued.

---

### Step 6: Notify Internal Stakeholders
- Alert the **Controller, Treasurer, and/or CFO** immediately — a request of this nature should not be silently processed.
- Notify **IT/Information Security**: the vendor's email domain may be compromised, which is a third-party risk issue.
- If your company has a **fraud hotline or financial crime team**, loop them in.

---

### Step 7: Validate the Routing Number Independently
Routing number **031176110** can be validated against the Federal Reserve's public routing directory or your bank's tools:
- Verify it actually belongs to "First Continental Trust, Wilmington DE."
- Note: A *matching* routing number does not authenticate the request — it just eliminates one red flag.

---

## Why These Controls Exist — The Control Framework

### 1. Segregation of Duties (SoD)
No single person should be able to both *enter* and *approve* a vendor master change. This limits insider fraud and catches errors.

### 2. Out-of-Band Verification
The attack vector is the email channel. Verification must occur on a **completely separate, independently sourced channel** (phone call to a known number). This is the single most important detective control.

### 3. Vendor Master Change Authorization Policy
Changes to banking data are among the **highest-risk changes** in the P2P cycle. They require more scrutiny than even the original vendor onboarding, because the stakes are immediately financial.

### 4. Audit Trail / Immutable Logging
Every change to vendor master data must be logged with who, what, when, and the authorization basis — essential for forensic investigation if fraud occurs.

### 5. Payment Pre-Notification
Some organizations notify vendors via the **old contact on file** when banking changes are made (a "change confirmation" to the original email/contact). This gives the real vendor a chance to raise an alarm.

### 6. Materiality Thresholds
$48,200 exceeds typical low-dollar auto-approval limits; it almost certainly requires **controller-level review** under a properly designed authority matrix.

---

## Red Flags Present in This Specific Request

```
⚠ Urgency implied by referencing an outstanding invoice
⚠ CFO (executive) requesting what is typically an AR/accounting function
⚠ "Due to a recent banking relationship change" — vague, unverifiable explanation
⚠ Request covers both the current invoice AND all future payments (maximizes fraud yield)
⚠ Request to "confirm receipt and that this change has been applied" (pressure for quick action)
⚠ Email alone with no accompanying formal documentation
```

---

## What Happens If You Don't Follow These Controls

| Scenario | Outcome |
|---|---|
| Change made without verification | $48,200 wire/ACH sent to fraudster's account — **unrecoverable in most cases** |
| ACH sent | ~24–48 hr recall window, success not guaranteed |
| Wire sent | Recovery rate extremely low; FBI IC3 complaint possible but funds likely gone |
| Reputational/legal exposure | AP staff termination risk; company liability; potential vendor relationship damage |
| Ongoing fraud | All future payments redirected until discovered |

---

## Bottom Line

> **Legitimate vendors never object to proper verification procedures.** If the real Maria Velez submitted this request, she will understand and appreciate a 24–48 hour verification delay. If the request was fraudulent, your controls just saved your company $48,200 — and potentially all future payments to this vendor.

**The correct AP response is: acknowledge, hold, verify out-of-band, document, obtain dual approval, then act.**

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response explicitly rejects acting on the email, prescribes out-of-band callback verification using contact info from the vendor master file (not from the request), holds the in-flight $48,200 payment until verification, requires dual approval (maker-checker/SoD), requires bank letter or voided check, and explicitly addresses the BEC pattern. It also adds notification of stakeholders and routing number validation. All rubric criteria for a 2 are met.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_013 — trade_and_tax · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: applying domain conventions (post-Brexit UK B2B place-of-supply)_

### Question

A UK-incorporated software supplier has invoiced a US buyer for an annual SaaS subscription and added 20% UK VAT to the invoice. The buyer has no UK presence and no UK VAT registration. Is the VAT correctly charged? Reason from post-Brexit UK B2B place-of-supply rules. What should AP do?

### Context

```
Invoice (issued in GBP):
  Supplier:   Cumberland Software Ltd, London UK
                VAT registration: GB287654321
  Buyer:      [US buyer, no UK establishment, no UK VAT registration]
  Service:    Annual SaaS subscription, 'CumberlandHR' enterprise tier
  Period:     12 months, current period
  Net fee:    £24,000.00
  UK VAT 20%:  £4,800.00
  Total:      £28,800.00

Supplier note on invoice: 'VAT charged per UK VAT Act 1994 as amended.'
```

### Rubric

- **0**: Accepts the VAT as correctly charged, or treats this as a reverse-charge scenario between UK and US, or claims the VAT is reclaimable through some standard mechanism
- **1**: Recognizes that VAT should not have been charged but reasons via reverse charge instead of out-of-scope, OR fails to cite the place-of-supply rule (Sch 4A para 16 / VAT Notice 741A), OR mishandles the reclaim discussion
- **2**: Correctly identifies the place of supply as the US under UK B2B rules, distinguishes out-of-scope from reverse charge, recommends rejection and corrected invoice, addresses why reclaim is not the right path, and references the relevant UK VAT Act provision and HMRC guidance

### Ideal answer

[AI DRAFT — practitioner review required] **The VAT is incorrectly charged.** Under post-Brexit UK B2B place-of-supply rules for digital and consultancy services, the place of supply is the **customer's location**, not the supplier's. With the customer in the US (no UK establishment), the supply is **outside the scope of UK VAT**. The supplier should not have charged the £4,800 VAT.

Reasoning:
- The UK VAT Act 1994 Schedule 4A para 16 (and the implementing rules in HMRC VAT Notice 741A) sets the place of supply for B2B services received by a non-UK customer as the customer's country.
- For digital/electronically-supplied services (SaaS qualifies as a 'use and enjoyment' of digital services), the same place-of-supply rule applies post-Brexit: customer's country.
- The customer here is US-established. US is outside the UK and outside the EU. The supply is outside the scope of UK VAT — the supplier should issue the invoice without VAT and note 'Outside scope of UK VAT — place of supply outside UK per VAT Act 1994 Sch 4A para 16.'

This is distinct from the EU reverse-charge mechanism. Reverse charge applies between two EU VAT-registered parties when the place of supply shifts to the customer; the customer self-accounts. The US-recipient case here is not reverse charge — it's simply out of scope. There is no UK VAT liability for either party on this transaction.

AP action:
1. Reject the invoice. Email the supplier explaining that the place of supply for this SaaS service is the US (the customer's country) under UK VAT Act 1994 Sch 4A para 16, and that the supply is outside the scope of UK VAT.
2. Provide written confirmation that the buyer has no UK establishment and is not UK VAT-registered. The supplier needs this for their own VAT records to support the zero-VAT treatment.
3. Request a corrected invoice for £24,000 net, no VAT, with a note 'Outside scope of UK VAT — customer outside UK per Sch 4A para 16.'
4. Reclaimability: not applicable. The £4,800 is not VAT properly due, and a US buyer with no UK VAT registration has no UK return to reclaim on. The 13th Directive equivalent (UK VAT refund scheme for non-UK businesses) is theoretically available but practically slow and only refunds VAT properly charged on certain expenses — not VAT erroneously charged on out-of-scope supplies. The right path is to fix the invoice, not to reclaim.

If the supplier refuses to credit and reissue: the buyer could pay the £24,000 net amount only and let the supplier dispute, but that creates a contractual issue. Better to escalate to the supplier's tax / finance team rather than accepting the invoice as-billed and writing off £4,800.

Note: the answer would change if the buyer had a UK VAT registration that was the actual recipient of the service (e.g. a UK branch that uses the SaaS). In that case, place of supply could be the UK and the VAT would be properly charged and reclaimable. This fact pattern explicitly excludes that.

References: UK VAT Act 1994 Schedule 4A para 16; HMRC VAT Notice 741A 'Place of supply of services'; HMRC guidance on Brexit transition for B2B services.

### Model response

# Analysis: UK VAT on SaaS Supplied to a US Business

## Reasoning from UK Place-of-Supply Rules

**1. Nature of the supply**
A SaaS subscription is an "electronically supplied service" under UK law (VAT Act 1994, Sch 4A; Notice 741A). For B2B place-of-supply purposes it falls under the **general B2B rule**, not a special rule — the digital-services special rules only matter for B2B2C/B2C cross-border supplies.

**2. General B2B place-of-supply rule (s.7A VATA 1994)**
For services supplied business-to-business, the place of supply is **where the customer belongs** (i.e., where the customer has its business establishment). This rule was unchanged by Brexit; it mirrors pre-Brexit rules and continues to apply to all non-UK customers, EU and non-EU alike.

**3. Applying the rule here**
- Customer belongs in the **United States**.
- Customer has no UK fixed establishment, no UK VAT registration, and is acting as a business (B2B).
- Therefore the **place of supply is the US**, which is **outside the scope of UK VAT**.

**4. Evidence the supplier needs**
For B2B treatment, the UK supplier must be satisfied the customer is in business outside the UK. Acceptable evidence (Notice 741A §5.2) includes a US tax/EIN reference, business website, contracts, certificate of commercial status, or any other commercial evidence. The supplier should hold this on file — but cannot use the absence of such evidence as a reason to charge UK VAT to a clearly non-UK business customer; it would simply default to B2C treatment, and even then a SaaS supplied B2C in the US is still outside UK VAT (digital services to non-UK consumers also fall outside UK VAT post-Brexit; only UK consumers attract UK VAT).

**5. Conclusion on the invoice**
The supplier has **incorrectly charged £4,800 of UK VAT.** The supply is outside the scope of UK VAT regardless of whether the customer is treated as B2B or B2C, because the customer is located in the US.

The correct invoice treatment is:
- Net £24,000.00
- VAT £0.00 (outside the scope of UK VAT — general B2B rule, place of supply = customer location, s.7A VATA 1994)
- A narrative such as: *"Outside the scope of UK VAT — general rule B2B services, place of supply USA"* (some suppliers also reference "reverse charge may apply in customer's jurisdiction," though no reverse charge exists in the US — there is no federal VAT).

The supplier's note ("VAT charged per UK VAT Act 1994 as amended") is incorrect; the same Act puts this supply outside the scope of UK VAT.

---

## What AP Should Do

1. **Do not pay the VAT line.** Place the invoice on hold.
2. **Do not attempt to recover the VAT.** As a US entity with no UK VAT registration, the buyer has no right of input recovery through a UK return. A 13th Directive-style refund route does not apply to a US business in the UK except via the UK overseas refund scheme (VAT Notice 723A), and HMRC will refuse a refund of VAT that was **incorrectly charged** — the buyer's only remedy is from the supplier.
3. **Contact the supplier and request a corrected invoice / credit note** for the full £4,800, citing:
   - VATA 1994 s.7A (general B2B place-of-supply rule),
   - HMRC Notice 741A §6 (B2B services to overseas business customers),
   - The supply is outside the scope of UK VAT; place of supply is the US.
4. **Provide supporting evidence of business status** to the supplier if not already on file: US incorporation documents, EIN letter, business address, website — to satisfy the supplier's B2B-evidence requirement under Notice 741A §5.2.
5. **Pay only the net £24,000.00** once a corrected invoice is received (or pay £24,000 now against a credit note for £4,800, depending on AP policy and the supplier's cooperation).
6. **US side:** Confirm with tax/AP whether any **US state-level sales/use tax** obligation arises on the SaaS purchase (many states tax SaaS — e.g., NY, TX, WA, MA — and use tax self-assessment may be required). This is independent of the UK VAT issue.
7. **Document the file** with the legal basis for rejecting the VAT, in case of later supplier dispute or internal audit query.

## Bottom Line

UK VAT was charged in error. The £4,800 is not a legitimate cost and is not recoverable from HMRC. AP should withhold the VAT element, demand a corrected zero-VAT invoice citing the general B2B place-of-supply rule (s.7A VATA 1994 / Notice 741A), and pay only the £24,000 net.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The candidate correctly identifies the supply as outside the scope of UK VAT (not reverse charge), cites the relevant UK VAT Act provision (s.7A VATA 1994, though the ideal cites Sch 4A para 16 - both are relevant place-of-supply provisions), references HMRC Notice 741A, recommends rejection and a corrected invoice, and explicitly addresses why reclaim is not the right path (notes 13th Directive/VAT Notice 723A doesn't apply to incorrectly charged VAT). It also distinguishes the situation from reverse charge by noting no US federal VAT exists. The bonus point about US state sales/use tax is a practical addition. Minor citation difference (s.7A vs Sch 4A para 16) but s.7A is the actual general rule provision.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_013 — trade_and_tax · medium · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: applying domain conventions (post-Brexit UK B2B place-of-supply)_

### Question

A UK-incorporated software supplier has invoiced a US buyer for an annual SaaS subscription and added 20% UK VAT to the invoice. The buyer has no UK presence and no UK VAT registration. Is the VAT correctly charged? Reason from post-Brexit UK B2B place-of-supply rules. What should AP do?

### Context

```
Invoice (issued in GBP):
  Supplier:   Cumberland Software Ltd, London UK
                VAT registration: GB287654321
  Buyer:      [US buyer, no UK establishment, no UK VAT registration]
  Service:    Annual SaaS subscription, 'CumberlandHR' enterprise tier
  Period:     12 months, current period
  Net fee:    £24,000.00
  UK VAT 20%:  £4,800.00
  Total:      £28,800.00

Supplier note on invoice: 'VAT charged per UK VAT Act 1994 as amended.'
```

### Rubric

- **0**: Accepts the VAT as correctly charged, or treats this as a reverse-charge scenario between UK and US, or claims the VAT is reclaimable through some standard mechanism
- **1**: Recognizes that VAT should not have been charged but reasons via reverse charge instead of out-of-scope, OR fails to cite the place-of-supply rule (Sch 4A para 16 / VAT Notice 741A), OR mishandles the reclaim discussion
- **2**: Correctly identifies the place of supply as the US under UK B2B rules, distinguishes out-of-scope from reverse charge, recommends rejection and corrected invoice, addresses why reclaim is not the right path, and references the relevant UK VAT Act provision and HMRC guidance

### Ideal answer

[AI DRAFT — practitioner review required] **The VAT is incorrectly charged.** Under post-Brexit UK B2B place-of-supply rules for digital and consultancy services, the place of supply is the **customer's location**, not the supplier's. With the customer in the US (no UK establishment), the supply is **outside the scope of UK VAT**. The supplier should not have charged the £4,800 VAT.

Reasoning:
- The UK VAT Act 1994 Schedule 4A para 16 (and the implementing rules in HMRC VAT Notice 741A) sets the place of supply for B2B services received by a non-UK customer as the customer's country.
- For digital/electronically-supplied services (SaaS qualifies as a 'use and enjoyment' of digital services), the same place-of-supply rule applies post-Brexit: customer's country.
- The customer here is US-established. US is outside the UK and outside the EU. The supply is outside the scope of UK VAT — the supplier should issue the invoice without VAT and note 'Outside scope of UK VAT — place of supply outside UK per VAT Act 1994 Sch 4A para 16.'

This is distinct from the EU reverse-charge mechanism. Reverse charge applies between two EU VAT-registered parties when the place of supply shifts to the customer; the customer self-accounts. The US-recipient case here is not reverse charge — it's simply out of scope. There is no UK VAT liability for either party on this transaction.

AP action:
1. Reject the invoice. Email the supplier explaining that the place of supply for this SaaS service is the US (the customer's country) under UK VAT Act 1994 Sch 4A para 16, and that the supply is outside the scope of UK VAT.
2. Provide written confirmation that the buyer has no UK establishment and is not UK VAT-registered. The supplier needs this for their own VAT records to support the zero-VAT treatment.
3. Request a corrected invoice for £24,000 net, no VAT, with a note 'Outside scope of UK VAT — customer outside UK per Sch 4A para 16.'
4. Reclaimability: not applicable. The £4,800 is not VAT properly due, and a US buyer with no UK VAT registration has no UK return to reclaim on. The 13th Directive equivalent (UK VAT refund scheme for non-UK businesses) is theoretically available but practically slow and only refunds VAT properly charged on certain expenses — not VAT erroneously charged on out-of-scope supplies. The right path is to fix the invoice, not to reclaim.

If the supplier refuses to credit and reissue: the buyer could pay the £24,000 net amount only and let the supplier dispute, but that creates a contractual issue. Better to escalate to the supplier's tax / finance team rather than accepting the invoice as-billed and writing off £4,800.

Note: the answer would change if the buyer had a UK VAT registration that was the actual recipient of the service (e.g. a UK branch that uses the SaaS). In that case, place of supply could be the UK and the VAT would be properly charged and reclaimable. This fact pattern explicitly excludes that.

References: UK VAT Act 1994 Schedule 4A para 16; HMRC VAT Notice 741A 'Place of supply of services'; HMRC guidance on Brexit transition for B2B services.

### Model response

# Analysis: UK VAT on B2B SaaS Supply to a US Buyer

## Executive Summary

**The VAT has been incorrectly charged.** Under post-Brexit UK B2B place-of-supply rules, this supply is outside the scope of UK VAT. The £4,800 VAT should not appear on this invoice. AP should reject the VAT charge and request a corrected invoice.

---

## 1. Legal Framework

### The Governing Rule: "General Rule" for B2B Services

The place of supply for services is governed by the **Value Added Tax Act 1994 (VATA 1994)**, as amended, together with the **VAT (Place of Supply of Services) Order 1992 (SI 1992/3121)**, itself substantially rewritten to reflect the UK's post-Brexit position (largely mirroring what was EU VAT Directive 2006/112/EC, Articles 44–59, as it stood at IP completion day, 31 December 2020).

**The General Rule for B2B services** (Schedule 4A, VATA 1994, paragraph 1, as amended):

> Where a supply of services is made to a **taxable person acting as such**, the place of supply is the **country where the recipient belongs**.

This is the post-Brexit UK codification of what was formerly the EU "reverse charge" B2B rule. The supplier's note citing "VAT Act 1994 as amended" ironically invokes the very legislation that makes the charge incorrect.

### Is the US Buyer a "Relevant Business Person"?

HMRC guidance (VAT Notice 741A, Section 5) defines the recipient as a **"relevant business person"** when they are:
- a **taxable person** (i.e., registered or required to register for VAT/GST/sales tax in their own country), **or**
- a **non-taxable legal person** registered for VAT purposes in any country

A US corporation purchasing enterprise SaaS for business use clearly qualifies as a **business customer** (a relevant business person) even without UK VAT registration. UK VAT registration of the *recipient* is **not** a prerequisite for the general B2B rule to apply.

---

## 2. Classification of the Supply

### Is SaaS a "Digital Service" or a General B2B Service?

| Consideration | Analysis |
|---|---|
| **Nature of supply** | Access to hosted software (CumberlandHR) over the internet — clearly an **electronically supplied service** |
| **VATA 1994 Schedule 4A, paragraph 8 / 9** | Special rules for electronically supplied services to *consumers* (B2C) — these override the general rule only for B2C |
| **B2B transaction?** | Yes — the buyer is a business entity, not a private individual |
| **B2B override** | For B2B, the **general rule (recipient's location) governs**, not the digital services special rule |

The digital services special rule (which would locate supply where the consumer belongs, and which operates differently) applies to **B2C** only. For a **B2B** supply, the general rule prevails regardless of whether the service is "digital."

**Conclusion:** The place of supply is the **United States** (where the business recipient belongs).

---

## 3. Place of Supply Determination

Applying the General Rule:

```
Place of supply = Country where recipient belongs
Recipient      = US corporation, belongs in the United States
Place of supply = UNITED STATES
Result         = Supply is OUTSIDE THE SCOPE OF UK VAT
```

There is **no UK VAT liability** on this transaction. The supplier should have issued a zero-rated or, more precisely, **out-of-scope** invoice with a notation such as:

> *"Supply outside scope of UK VAT — general rule, recipient belongs outside the UK (VAT Notice 741A)."*

The supplier should still report the value on its **VAT Return Box 6** (total value of sales) but with **no output tax**, and may still recover related input tax (as this is a supply made in the course of business).

---

## 4. Why the Supplier's Position Is Wrong

| Supplier's implicit reasoning | Why it fails |
|---|---|
| "We are a UK company, so we charge UK VAT" | UK establishment of the **supplier** is irrelevant for B2B services under the general rule |
| "CumberlandHR is delivered from UK servers" | Physical location of servers/infrastructure does not determine place of supply for services |
| "The buyer has no UK VAT number to quote" | A UK VAT number from the recipient is not required to apply the general rule; supplier must establish business status by other means (order forms, business communications, contractual representations) |
| "VAT Act 1994 as amended supports the charge" | The amended Act (Schedule 4A) is precisely what *removes* UK VAT jurisdiction here |

The absence of a UK VAT number for the buyer shifts the **evidential burden** to the supplier to establish business status, but in an enterprise SaaS subscription context (formal contract, business email domains, enterprise tier pricing, company registration details) this is straightforwardly satisfied.

---

## 5. Impact on the Buyer

Because this supply is **outside the scope of UK VAT**, the buyer:
- **Cannot register for UK VAT** simply to recover this tax (no UK taxable supplies, no registration entitlement on that basis)
- **Has no reverse-charge obligation** in the UK (it has no UK VAT registration)
- **Cannot reclaim the incorrectly charged VAT** via the UK's overseas refund scheme (VATA 1994 s.39 / SI 1995/2999), because that scheme applies to **correctly charged** UK VAT on supplies made *in* the UK — not to VAT charged in error on an out-of-scope supply
- The US buyer **may have US sales/use tax obligations** to self-assess under its own state rules — that is a separate matter entirely

---

## 6. What AP Should Do — Action Plan

### Immediate Actions

1. **Do not pay the VAT element (£4,800.00)**
   - Pay only the net fee of £24,000.00 (subject to any contractual payment terms and commercial judgment), or hold the entire invoice pending correction.
   - Document the rationale contemporaneously.

2. **Issue a formal written dispute to the supplier**
   Draft a letter/email that:
   - Identifies the invoice by number/date
   - States that the supply is outside the scope of UK VAT under **VATA 1994 Schedule 4A, General Rule** (B2B, recipient belongs in US)
   - Cites **HMRC VAT Notice 741A, Section 5** and the post-Brexit place-of-supply rules
   - Confirms buyer's status as a business customer (provide company registration, business address, representation that purchase is for business purposes)
   - Requests a **corrected/replacement VAT invoice** showing:
     - Net: £24,000.00
     - UK VAT: £0.00
     - Notation: "Outside scope of UK VAT — B2B general rule, recipient belongs outside UK"

3. **Do not attempt to reclaim the VAT** through any UK mechanism — there is no valid route.

### If Supplier Refuses to Correct

4. **Escalate to supplier's finance/tax director**, attaching this analysis.

5. **Consider HMRC involvement**: HMRC has the power under VATA 1994 s.80 to require repayment of over-declared output tax to the supplier (the supplier can itself make a s.80 error correction claim). You can alert HMRC if the supplier persistently refuses — though this is typically a last resort.

6. **Legal/contractual route**: If the contract is silent on VAT jurisdiction, consider whether there is a misrepresentation in the invoice. Enterprise SaaS contracts often include a tax clause warranting that the supplier will only charge applicable taxes — if so, this may be a contract breach.

7. **Escalate internally**: Flag to your tax/legal team and CFO; consider withholding the disputed £4,800 in escrow pending resolution.

---

## 7. Summary Table

| Issue | Correct Position |
|---|---|
| **Applicable rule** | VATA 1994 Sch. 4A — General Rule (B2B) |
| **Place of supply** | United States (recipient's location) |
| **UK VAT due?** | **No — outside scope of UK VAT** |
| **VAT correctly charged?** | **No** |
| **Amount incorrectly charged** | £4,800.00 |
| **Correct invoice total** |

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the supply as outside the scope of UK VAT under the B2B general rule, with place of supply being the US (recipient's location). It distinguishes this from reverse charge (noting buyer has no UK reverse-charge obligation). It cites VATA 1994 Schedule 4A and HMRC VAT Notice 741A. It correctly addresses why reclaim is not the right path (overseas refund scheme doesn't apply to VAT charged in error on out-of-scope supplies). It recommends rejecting the invoice and requesting correction. Minor quibble: cites Sch 4A para 1 (general rule) rather than para 16, but the general rule citation is substantively correct and arguably more accurate for the analysis. All rubric requirements for a 2 are met.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_014 — trade_and_tax · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: applying domain conventions (Canadian GST/HST place-of-supply for exported services)_

### Question

A Canadian supplier has invoiced a US buyer for consulting services. The invoice charges 13% Ontario HST. The services were performed by a Toronto-based consultant who travelled to the buyer's New York office for two on-site weeks; the remaining work was performed remotely from Toronto. Is the HST correctly charged? What should AP do?

### Context

```
Invoice (issued in CAD):
  Supplier:   Northbridge Consulting Group Inc, Toronto ON
                GST/HST registration: 879214687 RT0001
  Buyer:      [US buyer, no Canadian presence, no Canadian GST/HST registration]
  Service:    Strategy consulting, 6-week engagement
              - 2 weeks on-site at buyer's New York office
              - 4 weeks remote work from Toronto
  Net fee:           CAD 75,000.00
  Ontario HST 13%:   CAD 9,750.00
  Total:             CAD 84,750.00

Supplier note: 'HST charged per Ontario rate as work originated from our Toronto office.'
```

### Rubric

- **0**: Accepts the HST as correctly charged, or applies the supplier's 'work originated in Toronto' reasoning, or claims reclaimability via a standard mechanism
- **1**: Recognizes the HST should not have been charged but misses the zero-rated-export framing (treats it as out-of-scope or reverse-charge), OR fails to cite Excise Tax Act Schedule VI Part V, OR mishandles the on-site-vs-remote split (e.g. argues the on-site portion should be subject to HST)
- **2**: Correctly identifies the supply as a zero-rated exported service under Schedule VI Part V section 7, addresses why the supplier's office-of-origin reasoning is wrong, addresses the on-site vs remote split correctly (it strengthens not weakens the zero-rating), prescribes rejection and corrected invoice, and addresses the reclaim impossibility

### Ideal answer

[AI DRAFT — practitioner review required] **The HST is incorrectly charged.** Under Canadian GST/HST place-of-supply rules for B2B services, the place of supply for services performed for a non-resident customer with no permanent establishment in Canada is generally **outside Canada — zero-rated** (technically, an exported service under the Excise Tax Act). The supplier's reasoning ('work originated from Toronto') is the wrong test; the place of supply for services is determined by the customer's location and where the service is consumed, not the supplier's office location.

Reasoning:
- Excise Tax Act (Canada) Schedule VI Part V section 7 and section 23 zero-rate exported services to non-residents under specified conditions: the customer is not a resident of Canada, the service is not consumed in Canada, and the service is not in respect of real property or tangible personal property situated in Canada.
- All three conditions are met here: the customer is US-resident, the deliverable is consumed in the US (the consulting work serves the US buyer's strategic decisions), and the engagement is not real-property-related.
- The 2 weeks on-site in New York actually strengthens the zero-rating argument — the work is physically being performed in the US during that period. The 4 weeks of remote work from Toronto does not change this; the place of consumption is the customer's US location.
- Under Schedule VI Part V section 7, the supplier should zero-rate the supply (charge 0% HST) and document the customer's non-resident status for their own GST/HST records. The supplier remains entitled to claim ITCs (Input Tax Credits) on inputs used to provide the service even though the output is zero-rated.

AP action:
1. Reject the HST line. Email the supplier explaining that under Schedule VI Part V section 7 of the Excise Tax Act, the supply is zero-rated as an exported service to a non-resident.
2. Provide written confirmation of non-residency: the buyer is a US-incorporated entity with no permanent establishment in Canada and no Canadian GST/HST registration.
3. Request a corrected invoice for CAD 75,000 net, 0% HST.
4. Reclaimability: not available to the US buyer. Canada does not have a 13th-Directive-equivalent refund scheme for non-resident businesses on erroneously-charged HST. The right path is correction of the invoice, not reclaim.

Distinct fact patterns where HST WOULD be correctly charged:
- If the customer had a Canadian permanent establishment using the service (HST charged, reclaimable on Canadian return).
- If the service related to real property situated in Canada (HST always charged regardless of customer residency).
- If the service was consumed primarily in Canada (e.g. consulting on a Canadian regulatory filing).

None of those apply here.

References: Excise Tax Act (Canada) Schedule VI Part V sections 7 and 23; CRA GST/HST Memorandum 4.5.3 'Exports — Services and Intellectual Property'; CRA guidance on place of supply for services.

### Model response

# Analysis: HST on Cross-Border Consulting Services

## Short Answer

**No — the HST is incorrectly charged.** AP should **reject the invoice and request a corrected (zero-rated) invoice** showing GST/HST at 0%, not pay it as issued. The supplier's rationale ("work originated from our Toronto office") is wrong — place-of-supply for GST/HST purposes is determined by the *recipient's* address, not the supplier's location.

---

## Reasoning

### 1. Is the supply taxable in Canada at all?

Consulting services supplied by a GST/HST-registered Canadian supplier to a non-resident are generally **zero-rated** (taxable at 0%) under **Schedule VI, Part V, section 23 of the Excise Tax Act (ETA)**, provided:

- The recipient is a **non-resident** of Canada;
- The recipient is **not registered for GST/HST**;
- The service is not specifically excluded (s. 23 excludes services rendered to an individual physically present in Canada when the service is performed, services in respect of Canadian real property, advisory services relating to Canadian tax/litigation, etc. — none apply here).

The US buyer has no Canadian presence and is not GST/HST-registered. Strategy consulting is not on the exclusion list. **The entire CAD 75,000 supply is zero-rated.**

The fact that 4 of 6 weeks were performed in Toronto, and 2 weeks on-site in New York, **does not change this**. Section 23 zero-rating turns on the *status of the recipient*, not on where the consultant physically sat. (And the on-site portion in New York would, if anything, only strengthen — never weaken — the zero-rating analysis.)

### 2. The supplier's place-of-supply argument is wrong

The Ontario 13% rate would only apply if the supply were *taxable in Canada* and the place-of-supply rules pointed to Ontario. For services, the place-of-supply rules in the **New Harmonized Value-Added Tax System Regulations** look primarily to the **address of the recipient obtained by the supplier in the ordinary course of business** — not to where the supplier performs the work.

Since the recipient's business address is in New York, the place of supply would be outside Canada in any event — reinforcing that no HST (Ontario or otherwise) should apply.

The supplier's note ("HST charged per Ontario rate as work originated from our Toronto office") reflects a common but incorrect supplier-centric view.

### 3. Why this matters to the US buyer

- The buyer **cannot recover** the CAD 9,750 of HST. It is not GST/HST-registered in Canada, so it cannot claim input tax credits.
- A non-resident rebate is **not available** for HST that was charged in error on a zero-rated supply — CRA's position is that the buyer's remedy is to **obtain a refund/credit from the supplier**, who in turn adjusts its net tax under **ETA s. 232** (refund or credit of tax charged in error) within two years.
- Paying the invoice as-is means a straight CAD 9,750 leakage.

### 4. What AP should do

1. **Do not pay the HST line.** Place the invoice on hold.
2. **Send a written query to the supplier** stating that, because the recipient is a non-resident of Canada that is not registered for GST/HST, the consulting services qualify as a zero-rated export of services under ETA Schedule VI, Part V, s. 23, and request a **revised invoice** showing:
   - Net fee: CAD 75,000.00
   - GST/HST at 0% (zero-rated export of services): CAD 0.00
   - Total: CAD 75,000.00
   - The supplier's GST/HST registration number (879214687 RT0001) — still required on the invoice even when zero-rated, for the supplier's records.
3. **Request supporting documentation** the supplier should retain (and ideally provide) to substantiate zero-rating: evidence of the buyer's non-residence and non-registration — typically a signed certification from the buyer confirming (a) it is not resident in Canada and (b) it is not registered for GST/HST. Many Canadian suppliers ask for this routinely; providing it up front usually unblocks the corrected invoice quickly.
4. **If the supplier refuses to reissue**, options are:
   - Pay only the net CAD 75,000 and dispute the HST line, citing s. 23 of Schedule VI; or
   - Pay in full under protest and require the supplier to issue a **s. 232 credit note** for CAD 9,750 within two years of the original invoice.
5. **Document the file** with the legal basis (ETA Schedule VI, Part V, s. 23; place-of-supply regulations) so the same issue can be flagged on future Canadian-supplier invoices — this error pattern is common.

### 5. Side note on US/state tax

Separately, AP/Tax should consider whether the **on-site New York portion** triggers any **New York State sales/use tax** or **non-resident withholding** considerations on the supplier's side — but those are independent of the Canadian HST question and do not justify the HST charge.

---

## Bottom Line

| Item | Correct treatment |
|---|---|
| Net fee | CAD 75,000.00 |
| GST/HST | **0% — zero-rated export of services (ETA Sch. VI, Pt. V, s. 23)** |
| Total payable | **CAD 75,000.00** |
| Action | Reject invoice; request corrected zero-rated invoice; provide non-resident/non-registration certification if requested |

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the supply as zero-rated under ETA Schedule VI Part V (cites section 23, which is one of the two relevant sections in the ideal answer). It explicitly addresses why the supplier's 'work originated in Toronto' reasoning is wrong, correctly handles the on-site/remote split (noting NY work strengthens not weakens zero-rating), prescribes rejection and a corrected invoice, and addresses reclaim impossibility (no ITC available, no rebate, remedy is supplier correction via s. 232). All rubric criteria for a 2 are met.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_014 — trade_and_tax · medium · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: applying domain conventions (Canadian GST/HST place-of-supply for exported services)_

### Question

A Canadian supplier has invoiced a US buyer for consulting services. The invoice charges 13% Ontario HST. The services were performed by a Toronto-based consultant who travelled to the buyer's New York office for two on-site weeks; the remaining work was performed remotely from Toronto. Is the HST correctly charged? What should AP do?

### Context

```
Invoice (issued in CAD):
  Supplier:   Northbridge Consulting Group Inc, Toronto ON
                GST/HST registration: 879214687 RT0001
  Buyer:      [US buyer, no Canadian presence, no Canadian GST/HST registration]
  Service:    Strategy consulting, 6-week engagement
              - 2 weeks on-site at buyer's New York office
              - 4 weeks remote work from Toronto
  Net fee:           CAD 75,000.00
  Ontario HST 13%:   CAD 9,750.00
  Total:             CAD 84,750.00

Supplier note: 'HST charged per Ontario rate as work originated from our Toronto office.'
```

### Rubric

- **0**: Accepts the HST as correctly charged, or applies the supplier's 'work originated in Toronto' reasoning, or claims reclaimability via a standard mechanism
- **1**: Recognizes the HST should not have been charged but misses the zero-rated-export framing (treats it as out-of-scope or reverse-charge), OR fails to cite Excise Tax Act Schedule VI Part V, OR mishandles the on-site-vs-remote split (e.g. argues the on-site portion should be subject to HST)
- **2**: Correctly identifies the supply as a zero-rated exported service under Schedule VI Part V section 7, addresses why the supplier's office-of-origin reasoning is wrong, addresses the on-site vs remote split correctly (it strengthens not weakens the zero-rating), prescribes rejection and corrected invoice, and addresses the reclaim impossibility

### Ideal answer

[AI DRAFT — practitioner review required] **The HST is incorrectly charged.** Under Canadian GST/HST place-of-supply rules for B2B services, the place of supply for services performed for a non-resident customer with no permanent establishment in Canada is generally **outside Canada — zero-rated** (technically, an exported service under the Excise Tax Act). The supplier's reasoning ('work originated from Toronto') is the wrong test; the place of supply for services is determined by the customer's location and where the service is consumed, not the supplier's office location.

Reasoning:
- Excise Tax Act (Canada) Schedule VI Part V section 7 and section 23 zero-rate exported services to non-residents under specified conditions: the customer is not a resident of Canada, the service is not consumed in Canada, and the service is not in respect of real property or tangible personal property situated in Canada.
- All three conditions are met here: the customer is US-resident, the deliverable is consumed in the US (the consulting work serves the US buyer's strategic decisions), and the engagement is not real-property-related.
- The 2 weeks on-site in New York actually strengthens the zero-rating argument — the work is physically being performed in the US during that period. The 4 weeks of remote work from Toronto does not change this; the place of consumption is the customer's US location.
- Under Schedule VI Part V section 7, the supplier should zero-rate the supply (charge 0% HST) and document the customer's non-resident status for their own GST/HST records. The supplier remains entitled to claim ITCs (Input Tax Credits) on inputs used to provide the service even though the output is zero-rated.

AP action:
1. Reject the HST line. Email the supplier explaining that under Schedule VI Part V section 7 of the Excise Tax Act, the supply is zero-rated as an exported service to a non-resident.
2. Provide written confirmation of non-residency: the buyer is a US-incorporated entity with no permanent establishment in Canada and no Canadian GST/HST registration.
3. Request a corrected invoice for CAD 75,000 net, 0% HST.
4. Reclaimability: not available to the US buyer. Canada does not have a 13th-Directive-equivalent refund scheme for non-resident businesses on erroneously-charged HST. The right path is correction of the invoice, not reclaim.

Distinct fact patterns where HST WOULD be correctly charged:
- If the customer had a Canadian permanent establishment using the service (HST charged, reclaimable on Canadian return).
- If the service related to real property situated in Canada (HST always charged regardless of customer residency).
- If the service was consumed primarily in Canada (e.g. consulting on a Canadian regulatory filing).

None of those apply here.

References: Excise Tax Act (Canada) Schedule VI Part V sections 7 and 23; CRA GST/HST Memorandum 4.5.3 'Exports — Services and Intellectual Property'; CRA guidance on place of supply for services.

### Model response

# HST Analysis: Cross-Border Consulting Services

## Short Answer

**No, the HST is incorrectly charged.** The supply qualifies as a **zero-rated export of services** under the *Excise Tax Act* (ETA), and the supplier should have charged **0% HST**. AP should reject the HST portion and request a corrected invoice.

---

## Legal Framework

### The Governing Rule: Zero-Rating of Exported Services

Under the ETA, Schedule VI, Part V, Section 23, a supply of a service is **zero-rated** (taxable at 0%) when:

> The service is supplied to a **non-resident person** who is **not registered** for GST/HST, provided the service is not performed in Canada in respect of real property situated in Canada, goods situated in Canada at the time of performance, or an individual who is in Canada at the time the service is performed.

The key relief provision is **ETA s. 7, Schedule VI, Part V** (exported services), specifically that consulting/advisory services supplied to non-resident, non-registered recipients are zero-rated when the supply meets the export criteria.

---

## Analysis of Each Element

### 1. Recipient Status ✅ Zero-Rating Condition Met
| Criterion | Fact | Conclusion |
|---|---|---|
| Non-resident? | US buyer, no Canadian presence | ✅ Yes |
| Not GST/HST registered? | No Canadian registration | ✅ Yes |

### 2. Nature of the Service
Strategy consulting is an **intangible supply** — it is not in respect of:
- Real property in Canada
- Goods physically in Canada
- An individual *in Canada* at the time of performance

This is a critical distinction from, e.g., construction consulting on a Canadian property.

### 3. The Two-Week New York On-Site Component ✅
- The service was physically performed **outside Canada** (New York)
- The *recipient* was outside Canada; the *consultant* traveled to the recipient's jurisdiction
- No carve-out applies — this portion is clearly zero-rated
- The supplier's logic ("work originated from our Toronto office") is **legally irrelevant** to the place-of-supply analysis

### 4. The Four-Week Remote Work from Toronto ✅
This is the supplier's argument for HST, but it fails:

**The place-of-supply rules for services** under ETA s. 142(1) look at **where the service is supplied to**, not where the supplier physically performs it. For services supplied to a non-resident, non-registered person, the supply is deemed made **outside Canada** if the conditions of Schedule VI, Part V are met.

> The supplier's physical location (Toronto office) does **not** determine whether HST applies when the recipient is a non-resident, non-registered person receiving an intangible advisory service.

CRA's own guidance (GST/HST Policy Statement P-169, and GST/HST Memoranda Chapter 4) confirms that **remote performance from Canada does not convert a zero-rated export into a taxable supply**.

---

## The Supplier's Error: Where the Reasoning Fails

| Supplier's Claim | Correct Rule |
|---|---|
| "HST applies because work originated from Toronto" | Physical origin of work is irrelevant; recipient's non-resident/non-registered status governs |
| Ontario 13% HST rate applied to full amount | The supply is zero-rated under Sch. VI, Pt. V; rate is 0% regardless of province |
| Supplier's registration creates HST obligation on this supply | Registration creates *eligibility* to collect; it does not create obligation on zero-rated supplies |

---

## What AP Should Do: Step-by-Step

### Immediate Actions

1. **Do not pay the HST amount (CAD 9,750.00)**
   Place a hold on the HST portion only; pay the undisputed net fee of CAD 75,000 on schedule if terms permit, or hold the full invoice pending correction — per your payment policy.

2. **Issue a formal dispute notice to the supplier**, in writing, citing:
   - ETA Schedule VI, Part V, Section 23
   - The buyer's status as a non-resident, non-registered person
   - Request for a **corrected invoice** at 0% HST

### Corrected Invoice Should Show:
```
Net fee:              CAD 75,000.00
HST (zero-rated, 0%): CAD      0.00
Total:                CAD 75,000.00
Note: Zero-rated supply per ETA Sch. VI, Pt. V — exported 
      services to non-resident, non-registered recipient.
```

3. **Document your file** with:
   - This analysis
   - Correspondence with supplier
   - Confirmation of buyer's non-resident, non-registered status

### If the Supplier Refuses to Correct

4. **Escalate to your tax counsel or Canadian GST advisor** to confirm the position in writing.

5. **Note the practical risk to the supplier**: If CRA audits the supplier, they face the position that HST was improperly collected — and under ETA s. 224, a supplier who collects HST that is not properly exigible still has a potential obligation to remit it (the "collected means remitted" rule), while the buyer has **no ability to claim an ITC** (input tax credit) since it has no Canadian GST/HST registration. The CAD 9,750 would simply be a dead cost — an unnecessary tax leakage.

6. **Do not attempt to self-assess** — the US buyer with no Canadian presence has no Canadian GST/HST registration and no mechanism to recover incorrectly paid HST through ITCs.

---

## Summary Table

| Issue | Conclusion |
|---|---|
| Is HST correctly charged? | **No** — supply is zero-rated |
| Legal basis | ETA Schedule VI, Part V, s. 23 |
| Supplier's rationale valid? | **No** — place of physical performance by supplier is not determinative |
| Correct HST amount | **CAD 0.00** |
| AP action | Dispute CAD 9,750 HST; request corrected invoice |
| Risk if paid as-is | Dead cost — no ITC recovery available to unregistered US buyer |

---

> **Bottom line:** The supplier's note reflects a common but incorrect understanding of Canadian place-of-supply rules. The origin of the *supplier's* work is irrelevant; what governs is the *recipient's* non-resident, non-registered status. AP should firmly but professionally reject the HST charge and insist on a corrected invoice for CAD 75,000 net.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the supply as zero-rated under ETA Schedule VI Part V (cites both s. 23 and s. 7), explains why the supplier's 'work originated in Toronto' reasoning is wrong (recipient location governs, not supplier's physical location), correctly handles the on-site/remote split (noting the NY work is clearly zero-rated and remote Toronto work doesn't convert it to taxable), prescribes rejection and corrected invoice at 0%, and addresses reclaim impossibility (no ITC available to unregistered US buyer, dead cost). All rubric elements for a score of 2 are met.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_015 — trade_and_tax · hard · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: multi-step trade compliance reasoning (HTS classification + Section 301 + importer-of-record responsibility)_

### Question

A Chinese supplier invoices a US buyer for $180,000 of microcontroller chips (HTS classification 8541.59.00). The supplier did not include any Section 301 tariff line on the invoice. The buyer's customs broker has not yet filed entry. What does AP need to verify, what cost is the buyer's vs. supplier's, and what specific control steps apply?

### Context

```
Purchase order PO-94427:
  Supplier:   Shenzhen Lianxin Microelectronics Ltd, China
  Goods:      24,000 microcontrollers, HTS 8541.59.00 (per supplier's commercial invoice)
  Country of origin: China
  Incoterms:  FOB Shenzhen (Incoterms 2020)
  PO value:   $180,000.00

Supplier commercial invoice:
  Goods:      $180,000.00
  Freight:    $0 (FOB — buyer arranges)
  Total:      $180,000.00
  No tariff or duty line

Buyer's customs broker has the entry queued but has not yet filed.

Known context: HTS 8541.59.00 covers semiconductor devices; some sub-classifications are subject to Section 301 List 3 tariffs (currently 25% as of recent rate schedules) and additional Section 301 List 4A tariffs depending on classification.
```

### Rubric

- **0**: Treats the missing tariff as a supplier-invoice error or asks the supplier to add it, OR fails to identify the importer's classification responsibility, OR ignores Section 301
- **1**: Identifies that Section 301 tariffs are the buyer's cost and not the supplier's, but misses the importer-classification-responsibility duty (19 U.S.C. §1484), OR misses the HTS classification challenge (8541 vs 8542 distinction), OR omits country-of-origin / First Sale / FTZ considerations entirely
- **2**: Identifies tariff payment responsibility correctly, prescribes independent HTS classification review citing importer's §1484 duty of reasonable care, raises the 8541 vs 8542 sub-classification question, addresses country of origin / First Sale / FTZ / drawback as relevant control steps, and structures the response as a control-and-documentation workflow not just a tariff calculation

### Ideal answer

[AI DRAFT — practitioner review required] **The supplier invoice is correct as billed under FOB Incoterms — Section 301 tariffs are the buyer's cost, paid to US Customs and Border Protection (CBP) at entry, not paid to the supplier.** The absence of a tariff line on the supplier invoice is correct, not an error.

What AP needs to verify (and what's actually critical):

1. **HTS classification validation — independent of the supplier's claim.** The supplier wrote 8541.59.00 on their commercial invoice, but **the importer of record (the buyer) is legally responsible for accurate classification under 19 U.S.C. §1484 — 'reasonable care' standard.** Suppliers routinely misclassify either by error or to evade tariffs. AP/compliance should confirm classification with the customs broker before entry filing. A broker working from the supplier's stated HTS without independent review is providing a service, not an opinion. Validation steps:
   - Review the actual product specs against the HTS classification rules (USITC Harmonized Tariff Schedule).
   - For semiconductor devices, distinguish between 8541.59.00 (other diodes/transistors), 8542.31.00 (electronic integrated circuits — processors/controllers, often duty-free), and other 8541/8542 sub-classifications. The product description 'microcontroller' would more typically classify under 8542.31 (processors) than 8541.59 (transistors). **A misclassification at 8541 vs 8542 changes the duty exposure dramatically** — 8542.31.00 has historically been duty-free at MFN rate, while 8541.59 has a small MFN duty plus potentially Section 301 if the underlying product is China-origin and on the relevant list.

2. **Country of origin verification.** Section 301 applies to goods *of Chinese origin*. The supplier is in China but the goods could be assembled in China from components sourced elsewhere. Country of origin under 19 CFR §134 is determined by substantial transformation — where the article was last substantially transformed. This usually doesn't move the analysis (China for a Chinese-supplier-to-China-shipment) but it's worth confirming, especially if the chip is actually a Taiwanese or Korean die packaged in China.

3. **Section 301 tariff applicability.** Once HTS and origin are confirmed, check the current Section 301 list status for that exact HTS at the time of entry:
   - List 3 (25%) and List 4A (7.5%) are the most common applicable lists for electronics.
   - Some HTS codes were excluded or had exclusions that expired/were renewed. The USTR exclusion process is dynamic.
   - If 8541.59.00 is on the list at entry date (likely), Section 301 duty = $180,000 × applicable rate. At 25% List 3, that's $45,000.
   - Plus normal MFN duty (small for this HTS, often <2%).
   - Plus Merchandise Processing Fee (MPF, 0.3464% capped) and Harbor Maintenance Fee (HMF, 0.125%) for ocean shipments.

4. **First Sale rule consideration.** If the goods passed through a middleman (Hong Kong trading company → US buyer), First Sale for Export valuation might allow declaring the original factory price rather than the middleman price for duty purposes — savings can be material. Requires documentation chain.

5. **Foreign Trade Zone (FTZ) opportunity** if the buyer operates one — defer or eliminate Section 301 if goods are processed/re-exported.

6. **Drawback opportunity** if the goods are re-exported within 5 years — duty paid at entry is recoverable.

What AP / the broker SHOULDN'T do:
- Don't ask the supplier to add the Section 301 amount to their invoice. The supplier doesn't pay this; CBP collects it from the importer at entry.
- Don't rely on the supplier's stated HTS as authoritative.
- Don't file entry without confirming current Section 301 status at the actual entry date — list status changes.

Control steps:
- Document the independent HTS classification review (who, when, basis).
- Document Section 301 status verification at entry date.
- Reconcile broker entry summary (CBP Form 7501) against expectations: declared HTS, declared origin, declared value, calculated duties.
- Capture any First Sale or FTZ election in the broker file.
- Annual review of HTS/origin classifications for recurring vendors.

References: 19 U.S.C. §1484 (importer reasonable care); 19 CFR §134 (country of origin); USTR Section 301 actions and exclusion lists; USITC Harmonized Tariff Schedule; CBP guidance on First Sale for Export.

### Model response

# Analysis: PO-94427 — Section 301 Tariff Liability and AP Controls

## 1. Threshold Issue: Who Owes the Duty?

**The buyer (US importer of record) owes the Section 301 tariff — not the supplier.**

Key principles:
- **19 U.S.C. § 1484 / § 1485:** Liability for US customs duties (including Section 301 additional duties) attaches to the **importer of record (IOR)**, who is the US buyer. The Chinese supplier has no US duty obligation.
- **Incoterms FOB Shenzhen (Incoterms 2020):** Risk and cost transfer to the buyer once goods are loaded on the vessel at Shenzhen. All US-side import charges — duty, MPF, HMF, Section 301 additional duties — are the buyer's account by definition.
- The supplier's invoice is therefore **correct** in omitting a tariff line. A 301 line on a supplier invoice would actually be a red flag (suppliers cannot collect US duty).
- Section 301 duties are **paid to US Customs and Border Protection (CBP)** at entry, via the broker's ACH or the broker's account, not to the supplier.

**Bottom line:** The $180,000 is owed to the supplier. Any 301 duty is owed separately to CBP and is a buyer-borne landed cost.

## 2. What AP Must Verify Before Approving Anything

### A. Verify the supplier invoice ($180,000) — standard 3-way match
- PO-94427 price/quantity/terms match invoice
- Goods receipt (or in-transit confirmation under FOB — title passed at Shenzhen rail)
- Incoterms on invoice = FOB Shenzhen (matches PO)
- No freight, no duty line (correct under FOB; broker handles US-side)

### B. Verify the **classification and 301 exposure** before the broker files
This is the critical pre-entry control. AP/Trade Compliance must confirm with the broker:

1. **HTS confirmation:** Is 8541.59.00 the correct 10-digit HTSUS classification? Microcontrollers are frequently misclassified — they often properly fall under **8542.31.0001** (electronic integrated circuits / processors and controllers), not 8541 (discrete semiconductors). Misclassification creates either underpayment exposure (penalties under 19 USC § 1592) or overpayment.
2. **Country of origin:** Confirmed China (substantial transformation rule, not just shipped-from). Triggers Section 301.
3. **Section 301 list assignment:**
   - List 3 (25%) and List 4A (currently 7.5%) cover different 8-digit subheadings
   - Verify the specific 9903.88.xx Chapter 99 secondary HTS code the broker will use
4. **Exclusion check:** Confirm whether any active Section 301 exclusion (current USTR exclusion list) applies to this HTS/product. Several semiconductor exclusions have been extended; this materially changes the cost.
5. **Duty base:** Section 301 is calculated on the **customs value** — for FOB shipments this is generally the FOB price ($180,000) plus any assists, **not** including international freight/insurance (CIF is not the US dutiable basis; transaction value under 19 CFR § 152.103 is).
6. **Other duties stacking:** MFN/Column 1 rate for 8541.59.00 (free) + Section 301 additional + MPF (0.3464%, capped) + HMF (0.125% if ocean).

### C. Estimated landed cost the buyer should accrue

| Item | Amount |
|---|---|
| Goods (to supplier) | $180,000.00 |
| Section 301 (assume List 3 @ 25% on $180,000) | $45,000.00 |
| MPF (0.3464%, capped at ~$634.62) | ~$623.52 |
| HMF (0.125%, ocean only) | ~$225.00 |
| Broker fees, freight, insurance | per separate invoices |
| **Estimated import duty owed to CBP** | **~$45,850** |

This $45K is a **buyer cost, not a supplier dispute**.

## 3. Specific Control Steps

### Pre-entry (act now — broker has not yet filed)
1. **Hold the entry filing** until Trade Compliance signs off on HTS, COO, and 301 applicability. Once filed, corrections require Post Summary Correction (PSC) within 300 days or a protest within 180 days of liquidation — administratively expensive.
2. **Trade Compliance / classification review:** Independently validate HTS 8541.59.00 vs. 8542.31.00 (microcontrollers are typically ICs). Document the rationale per 19 CFR § 152 reasonable care standard.
3. **Exclusion search:** Run the product against current USTR Section 301 exclusion list and any reinstated exclusions.
4. **Confirm IOR and bond:** Buyer is IOR; continuous bond must cover estimated duties (bond = 10% of prior year duties, min $50K). A $45K duty on one entry can stress single-transaction bonds.

### Accounting controls
5. **Accrue the 301 duty as inventory cost** (ASC 330 — duties are capitalizable to inventory), not as a period expense and not as a payable to the supplier.
6. **Set up a separate GL account** for Section 301 duties (distinct from regular customs duty) to support (a) financial reporting disclosure of tariff exposure, (b) any future drawback claims, (c) refund tracking if exclusions are granted retroactively.
7. **Do not net the duty against the supplier payable.** Pay supplier the full $180,000 per invoice. Pay CBP separately via broker.
8. **Reconcile broker statement:** When broker invoices for duties advanced + brokerage, match to CBP Form 7501 (Entry Summary). Verify duty amounts, HTS codes, and 9903 chapter codes line-by-line.

### Procurement / contract controls (forward-looking)
9. **PO terms review:**

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response correctly identifies that Section 301 tariffs are the buyer's cost paid to CBP, not the supplier's. It cites 19 U.S.C. §1484 importer responsibility, raises the critical 8541 vs 8542.31 microcontroller classification distinction, addresses country of origin (substantial transformation), exclusion checks, and structures the response as a control-and-documentation workflow with pre-entry holds, accounting controls (ASC 330 capitalization, separate GL), and reconciliation to CBP Form 7501. While First Sale, FTZ, and drawback are not explicitly addressed (drawback is briefly mentioned in the GL setup rationale), the rubric says these should be addressed 'as relevant' and the response covers the most critical elements thoroughly with strong control workflow structure.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_015 — trade_and_tax · hard · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: multi-step trade compliance reasoning (HTS classification + Section 301 + importer-of-record responsibility)_

### Question

A Chinese supplier invoices a US buyer for $180,000 of microcontroller chips (HTS classification 8541.59.00). The supplier did not include any Section 301 tariff line on the invoice. The buyer's customs broker has not yet filed entry. What does AP need to verify, what cost is the buyer's vs. supplier's, and what specific control steps apply?

### Context

```
Purchase order PO-94427:
  Supplier:   Shenzhen Lianxin Microelectronics Ltd, China
  Goods:      24,000 microcontrollers, HTS 8541.59.00 (per supplier's commercial invoice)
  Country of origin: China
  Incoterms:  FOB Shenzhen (Incoterms 2020)
  PO value:   $180,000.00

Supplier commercial invoice:
  Goods:      $180,000.00
  Freight:    $0 (FOB — buyer arranges)
  Total:      $180,000.00
  No tariff or duty line

Buyer's customs broker has the entry queued but has not yet filed.

Known context: HTS 8541.59.00 covers semiconductor devices; some sub-classifications are subject to Section 301 List 3 tariffs (currently 25% as of recent rate schedules) and additional Section 301 List 4A tariffs depending on classification.
```

### Rubric

- **0**: Treats the missing tariff as a supplier-invoice error or asks the supplier to add it, OR fails to identify the importer's classification responsibility, OR ignores Section 301
- **1**: Identifies that Section 301 tariffs are the buyer's cost and not the supplier's, but misses the importer-classification-responsibility duty (19 U.S.C. §1484), OR misses the HTS classification challenge (8541 vs 8542 distinction), OR omits country-of-origin / First Sale / FTZ considerations entirely
- **2**: Identifies tariff payment responsibility correctly, prescribes independent HTS classification review citing importer's §1484 duty of reasonable care, raises the 8541 vs 8542 sub-classification question, addresses country of origin / First Sale / FTZ / drawback as relevant control steps, and structures the response as a control-and-documentation workflow not just a tariff calculation

### Ideal answer

[AI DRAFT — practitioner review required] **The supplier invoice is correct as billed under FOB Incoterms — Section 301 tariffs are the buyer's cost, paid to US Customs and Border Protection (CBP) at entry, not paid to the supplier.** The absence of a tariff line on the supplier invoice is correct, not an error.

What AP needs to verify (and what's actually critical):

1. **HTS classification validation — independent of the supplier's claim.** The supplier wrote 8541.59.00 on their commercial invoice, but **the importer of record (the buyer) is legally responsible for accurate classification under 19 U.S.C. §1484 — 'reasonable care' standard.** Suppliers routinely misclassify either by error or to evade tariffs. AP/compliance should confirm classification with the customs broker before entry filing. A broker working from the supplier's stated HTS without independent review is providing a service, not an opinion. Validation steps:
   - Review the actual product specs against the HTS classification rules (USITC Harmonized Tariff Schedule).
   - For semiconductor devices, distinguish between 8541.59.00 (other diodes/transistors), 8542.31.00 (electronic integrated circuits — processors/controllers, often duty-free), and other 8541/8542 sub-classifications. The product description 'microcontroller' would more typically classify under 8542.31 (processors) than 8541.59 (transistors). **A misclassification at 8541 vs 8542 changes the duty exposure dramatically** — 8542.31.00 has historically been duty-free at MFN rate, while 8541.59 has a small MFN duty plus potentially Section 301 if the underlying product is China-origin and on the relevant list.

2. **Country of origin verification.** Section 301 applies to goods *of Chinese origin*. The supplier is in China but the goods could be assembled in China from components sourced elsewhere. Country of origin under 19 CFR §134 is determined by substantial transformation — where the article was last substantially transformed. This usually doesn't move the analysis (China for a Chinese-supplier-to-China-shipment) but it's worth confirming, especially if the chip is actually a Taiwanese or Korean die packaged in China.

3. **Section 301 tariff applicability.** Once HTS and origin are confirmed, check the current Section 301 list status for that exact HTS at the time of entry:
   - List 3 (25%) and List 4A (7.5%) are the most common applicable lists for electronics.
   - Some HTS codes were excluded or had exclusions that expired/were renewed. The USTR exclusion process is dynamic.
   - If 8541.59.00 is on the list at entry date (likely), Section 301 duty = $180,000 × applicable rate. At 25% List 3, that's $45,000.
   - Plus normal MFN duty (small for this HTS, often <2%).
   - Plus Merchandise Processing Fee (MPF, 0.3464% capped) and Harbor Maintenance Fee (HMF, 0.125%) for ocean shipments.

4. **First Sale rule consideration.** If the goods passed through a middleman (Hong Kong trading company → US buyer), First Sale for Export valuation might allow declaring the original factory price rather than the middleman price for duty purposes — savings can be material. Requires documentation chain.

5. **Foreign Trade Zone (FTZ) opportunity** if the buyer operates one — defer or eliminate Section 301 if goods are processed/re-exported.

6. **Drawback opportunity** if the goods are re-exported within 5 years — duty paid at entry is recoverable.

What AP / the broker SHOULDN'T do:
- Don't ask the supplier to add the Section 301 amount to their invoice. The supplier doesn't pay this; CBP collects it from the importer at entry.
- Don't rely on the supplier's stated HTS as authoritative.
- Don't file entry without confirming current Section 301 status at the actual entry date — list status changes.

Control steps:
- Document the independent HTS classification review (who, when, basis).
- Document Section 301 status verification at entry date.
- Reconcile broker entry summary (CBP Form 7501) against expectations: declared HTS, declared origin, declared value, calculated duties.
- Capture any First Sale or FTZ election in the broker file.
- Annual review of HTS/origin classifications for recurring vendors.

References: 19 U.S.C. §1484 (importer reasonable care); 19 CFR §134 (country of origin); USTR Section 301 actions and exclusion lists; USITC Harmonized Tariff Schedule; CBP guidance on First Sale for Export.

### Model response

# Customs & Trade Compliance Analysis: PO-94427
## Microcontrollers from China — Section 301 Tariff Exposure

---

## EXECUTIVE SUMMARY

The supplier's commercial invoice is **materially incomplete** for U.S. import cost purposes. The buyer faces a **substantial unbooked landed-cost liability** that must be resolved before entry is filed and before the invoice is approved for payment at face value. AP must not process this as a $180,000 cost; the all-in landed cost is materially higher.

---

## PART 1: TARIFF EXPOSURE QUANTIFICATION

### 1.1 Applicable Duty Layers

| Duty Layer | Authority | Rate | Basis | Estimated Amount |
|---|---|---|---|---|
| **MFN / Column 1 General Duty** | HTSUS Chapter 85 | **Free (0%)** | $180,000 CIF* | $0 |
| **Section 301 List 3 Tariff** | USTR Section 301 Action, 19 USC §2411 | **25%** | $180,000 dutiable value | **$45,000** |
| **Section 301 List 4A Tariff** | USTR Section 301 Action | **7.5%** | $180,000 dutiable value | **$13,500** |
| **Harbor Maintenance Fee (HMF)** | 26 USC §4461 | 0.125% | Entered value | ~$225 |
| **Merchandise Processing Fee (MPF)** | 19 USC §58c | 0.3464% (min $31.67, max $614.35) | Entered value | **$614.35** (capped) |

> ***Dutiable value note:** Under FOB Shenzhen terms, the dutiable value for U.S. Customs purposes is the transaction value per 19 USC §1401a — i.e., the FOB price of $180,000. Freight and insurance from port of export are excluded under FOB Incoterms when the U.S. uses FOB origin valuation (CBP generally uses CIF for the entered value calculation, but FOB value is the starting point here; the broker must confirm whether U.S. inland/ocean freight needs to be added — typically ocean freight IS added to dutiable value under U.S. rules to approximate CIF; this requires broker confirmation).*

### 1.2 Critical Classification Question: List 3 vs. List 4A — Are Both Applicable?

HTS **8541.59.00** falls under semiconductor devices. The USTR Section 301 actions operate as follows:

- **List 3** (effective September 24, 2018): 25% on $200B of Chinese goods — **8541.59 is covered**
- **List 4A** (effective September 1, 2019): 7.5% on remaining goods — whether 8541.59 is **also** on List 4A or exclusively on List 3 must be confirmed by the broker against the **current USTR annex**

> ⚠️ **The rates have been subject to modification.** As of 2024–2025, the Biden/Trump administration actions have adjusted Section 301 rates on semiconductors under the "four-year review." HTS 8541.59 semiconductor devices may be subject to **elevated rates (potentially 50%)** under the 2024 USTR Section 301 review findings effective in stages. The broker must pull the **current CBP ACE tariff schedule** on the date of entry filing — not rely on historical rates.

### 1.3 Conservative Minimum Exposure

```
Invoice value:                    $180,000.00
Section 301 duties (25% minimum):  $45,000.00
MPF (capped):                          $614.35
HMF:                                   $225.00
─────────────────────────────────────────────
Estimated minimum additional cost: $45,839.35
Total landed cost (minimum):      $225,839.35
                                  ═══════════
Incremental cost vs. invoice:         +25.5%
```

---

## PART 2: WHO BEARS THE COST — BUYER vs. SUPPLIER RESPONSIBILITY

### 2.1 Legal Allocation Under FOB Shenzhen (Incoterms 2020)

| Cost Element | Responsible Party | Rationale |
|---|---|---|
| **Goods cost** ($180,000) | Buyer ← Supplier obligation met | FOB: seller delivers to named port/vessel |
| **Ocean freight** (buyer-arranged) | **Buyer** | FOB — buyer contracts carriage |
| **Marine insurance** | **Buyer** | FOB — buyer's risk once on vessel |
| **U.S. Customs duties (all layers)** | **Buyer (importer of record)** | Importer of record bears all import duties under U.S. law; Incoterms FOB confirms this |
| **Section 301 tariffs** | **Buyer** | Same as above — these are U.S. import duties |
| **CBP Broker fees** | **Buyer** | Buyer's appointed broker |
| **MPF / HMF** | **Buyer** | U.S. fees on importer |

> **Critical legal point:** Under **19 USC §1484**, the **importer of record** is legally liable for all duties, fees, and taxes. The supplier has zero legal obligation to the U.S. government for these amounts. The absence of a tariff line on the supplier's invoice is commercially unfortunate but does **not** reduce the buyer's legal liability by one cent.

### 2.2 Is the Supplier at Fault for the Missing Tariff Line?

**Commercially, no — legally, no.** The supplier's invoice correctly states the goods price under FOB terms. Section 301 tariffs are **U.S.-imposed** charges; they are not the supplier's obligation to invoice. However:

- The supplier **may have a duty** under the purchase agreement to provide accurate HTS classification support documents, certificates of origin, and correct commercial invoice descriptions that allow the buyer to accurately determine duty exposure
- If the purchase agreement had a **landed-duty-paid or DDP clause** (it does not here — this is FOB), the analysis would differ entirely
- AP should review the **purchase agreement and any representations made by the supplier** about landed cost — if the supplier provided a total cost estimate that omitted duties, there may be a commercial dispute, but **no legal recourse on the duty itself**

---

## PART 3: AP VERIFICATION REQUIREMENTS — DETAILED CHECKLIST

### 3.1 Pre-Entry Filing (IMMEDIATE — Entry Not Yet Filed)

AP must coordinate with the customs broker and supply chain/trade compliance **before entry is filed and before the invoice is approved for payment.**

#### A. HTS Classification Verification
- [ ] Obtain the supplier's full product technical datasheet for the microcontrollers
- [ ] Confirm HTS 8541.59.00 is the correct 10-digit classification (not a sub-heading that could be more favorable or subject to a different rate)
- [ ] Determine if any **product exclusion** was granted by USTR for this specific HTS/product — USTR has granted product-specific exclusions; check the USTR exclusion portal and current Federal Register notices
- [ ] Verify whether the current rate under the 2024 USTR Section 301 review is 25%, 50%, or another rate — semiconductor rates were specifically targeted for increases
- [ ] Confirm whether List 3 and/or List 4A **both** apply or if one supersedes the other for this heading

#### B. Country of Origin Verification
- [ ] Obtain a **manufacturer's affidavit / country of origin declaration** from Shenzhen Lianxin Microelectronics
- [ ] Verify that the microcontrollers are not manufactured in a third country (e.g., Taiwan, South Korea) and merely shipped through China — if true origin is non-China, Section 301 tariffs **do not apply**, and this changes the cost picture materially
- [ ] Assess **substantial transformation** risk — if wafers are from elsewhere but assembled/packaged in China, CBP's substantial transformation test determines origin
- [ ] Request a **Certificate of Origin** and verify against bill of materials if possible

#### C. Valuation Verification
- [ ] Confirm the transaction value basis with the broker — is ocean freight to be added to arrive at dutiable value?
- [ ] Verify no **assists**, royalties, or proceeds of subsequent resale are owed to the supplier that would increase dutiable value

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response correctly identifies that Section 301 tariffs are the buyer's cost paid to CBP, not the supplier's, and that the missing tariff line is not a supplier error. It cites 19 USC §1484 importer of record responsibility, prescribes independent HTS classification verification, addresses country of origin verification including substantial transformation, and structures the response as a control/verification workflow. It addresses USTR exclusions and current rate review status. However, it does not explicitly raise the 8541 vs 8542 sub-classification distinction (microcontrollers arguably belong under 8542.31 as integrated circuits rather than 8541.59 as transistors) — this is the specific classification challenge called out in the rubric. It also omits First Sale, FTZ, and drawback considerations. Given the strong §1484 coverage, COO analysis, and control workflow, but missing the specific 8541/8542 distinction and First Sale/FTZ/drawback, this sits between 1 and 2. The rubric for 2 requires raising the 8541 vs 8542 question AND addressing First Sale/FTZ/drawback — both are missing or weak, so this is closer to a 1.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_016 — invoice_processing · easy · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: applying domain conventions (stock-flow accounting principle)_

### Question

Accounts Payable Days (also called Days Payables Outstanding, DPO) is computed using the AVERAGE accounts-payable balance over the period rather than the ending balance. Why? What problem does the averaging convention solve, and what would go wrong if a junior analyst used the ending AP balance instead?

### Rubric

- **0**: Says ending AP is correct, OR fails to identify the stock/flow distinction, OR gives a definition without explaining the averaging convention
- **1**: Identifies that average AP is correct but does not articulate the stock/flow consistency reasoning, OR misses the end-of-period-anomaly distortion, OR gives the formula without the principle
- **2**: Articulates the stock/flow consistency principle as the underlying reason, identifies end-of-period anomalies as the concrete distortion that averaging solves, addresses comparability across firms, and references the canonical formula with the average-AP convention

### Ideal answer

[AI DRAFT — practitioner review required] DPO uses the AVERAGE accounts-payable balance because it reconciles a stock measure (AP, a balance-sheet item that exists as a snapshot) with a flow measure (purchases or COGS, an income-statement item that accumulates over a period). The averaging convention converts the stock measure into something comparable to the flow measure by representing the typical AP level throughout the period rather than a single point-in-time snapshot.

What goes wrong with ending AP:

1. **End-of-period anomalies distort the metric.** A company that pushes invoices out the door in the last week of the year (to compress AP for working-capital reporting) or holds invoices in the last week (to stretch DPO) will produce an ending balance that does not reflect typical operations. Average AP smooths these end-effects.

2. **Consistency between numerator and denominator.** Purchases or COGS is an over-the-period number. If the denominator covers the full period, the numerator should represent the period too — average AP does that; ending AP doesn't.

3. **Comparability across companies.** Different firms close their books on different cycles; ending AP varies systematically with fiscal calendar. Averaged AP is more comparable.

4. **Audit defensibility.** Stock/flow consistency is a documented accounting principle (Holthausen & Zmijewski 2014). Using ending AP without disclosure invites a sourcing-quality challenge during diligence.

The canonical formula is therefore: DPO = (Average AP / Purchases) × N, where 'Average AP' is typically (Beginning AP + Ending AP) / 2 for annual analysis or a more granular average (monthly average) for shorter-period analysis. Some firms use COGS in the denominator instead of Purchases as a practical proxy when Purchases isn't disclosed; the stock/flow consistency principle still requires averaging.

### Model response

# Why DPO Uses Average Accounts Payable

## The Core Reasoning

Days Payables Outstanding measures a **flow-to-stock relationship**: it compares a flow variable (Cost of Goods Sold or purchases, accumulated *over* a period) against a stock variable (Accounts Payable, measured *at a point* in time).

The standard formula is:

$$DPO = \frac{\text{Average AP}}{\text{COGS (or Purchases)}} \times \text{Days in Period}$$

The averaging convention exists to make the numerator and denominator **temporally consistent**. COGS represents activity spread across the entire period (e.g., 365 days). The ending AP balance is a single snapshot taken at one instant — typically the last second of the fiscal year. Pairing a full-year flow with a single year-end snapshot is an apples-to-oranges comparison.

By using the average of beginning and ending AP (or, ideally, an average of monthly/quarterly balances), the numerator approximates the *typical* AP balance the company carried while it was generating that COGS. That is the figure you actually want to convert into "days."

## What Problem Averaging Solves

Three specific distortions are mitigated:

1. **Window-dressing and balance-sheet seasonality.** Year-end balances are notoriously unrepresentative. Companies often pay down payables aggressively before fiscal year-end to present a cleaner balance sheet, or conversely stretch payables to conserve cash. Either behavior makes the snapshot atypical of the year as a whole.

2. **Growth and structural shifts.** If a company grew (or contracted) substantially during the period, the ending AP reflects the *new* business scale, while COGS reflects a blend of the old and new scale. Averaging beginning and ending AP produces a balance that is roughly contemporaneous with the average level of activity that drove COGS.

3. **One-off events near period-end.** A large purchase booked the week before year-end, a dispute with a major supplier, an acquisition, or an FX revaluation can swing the ending balance dramatically without reflecting how the firm actually managed payables across the year.

## What Goes Wrong With the Ending Balance

A junior analyst plugging in ending AP will produce DPO figures that are systematically misleading in predictable ways:

- **Inflated DPO** when the firm ramped up purchases late in the period, made an acquisition, or simply grew. The analyst will conclude the company is stretching suppliers when in fact the AP balance is high merely because the business is bigger.
- **Deflated DPO** when management paid down payables for window dressing. The analyst will conclude payment terms tightened when they did not.
- **Spurious volatility in trend analysis.** Year-over-year DPO comparisons will fluctuate based on snapshot noise rather than underlying payment behavior, masking real trends in supplier credit usage.
- **Distorted cash conversion cycle.** Because DPO feeds into CCC = DIO + DSO − DPO, errors propagate. An overstated DPO understates the cash conversion cycle and can make working-capital efficiency look better than it is — a meaningful issue in credit analysis, valuation (free cash flow forecasts), and covenant compliance work.
- **Unreliable peer benchmarking.** Two companies with identical payment practices but different fiscal year-ends or seasonal patterns will appear to have very different DPOs if ending balances are used.
- **Misdirected operational decisions.** If treasury or procurement uses the metric to evaluate supplier-payment policy, a snapshot-based DPO can prompt corrective action against a problem that does not exist (or, worse, hide one that does).

## Practical Note

The two-point average (beginning + ending)/2 is the textbook compromise, but it still assumes a roughly linear path between the two dates. For businesses with strong seasonality (retail, agriculture, construction), best practice is to average monthly or quarterly AP balances, which more faithfully reflects the AP carried alongside the COGS being matched. The same temporal-consistency principle is why DSO uses average AR and inventory days uses average inventory — it is a general rule for any ratio mixing a balance-sheet stock with an income-statement flow.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response clearly articulates the stock/flow consistency principle (calling it 'flow-to-stock relationship' and 'temporal consistency'), identifies end-of-period anomalies/window-dressing as concrete distortions averaging solves, addresses cross-firm comparability (peer benchmarking with different fiscal year-ends), and provides the canonical formula with the average-AP convention. It also extends to the general principle for DSO and inventory days.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_016 — invoice_processing · easy · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: applying domain conventions (stock-flow accounting principle)_

### Question

Accounts Payable Days (also called Days Payables Outstanding, DPO) is computed using the AVERAGE accounts-payable balance over the period rather than the ending balance. Why? What problem does the averaging convention solve, and what would go wrong if a junior analyst used the ending AP balance instead?

### Rubric

- **0**: Says ending AP is correct, OR fails to identify the stock/flow distinction, OR gives a definition without explaining the averaging convention
- **1**: Identifies that average AP is correct but does not articulate the stock/flow consistency reasoning, OR misses the end-of-period-anomaly distortion, OR gives the formula without the principle
- **2**: Articulates the stock/flow consistency principle as the underlying reason, identifies end-of-period anomalies as the concrete distortion that averaging solves, addresses comparability across firms, and references the canonical formula with the average-AP convention

### Ideal answer

[AI DRAFT — practitioner review required] DPO uses the AVERAGE accounts-payable balance because it reconciles a stock measure (AP, a balance-sheet item that exists as a snapshot) with a flow measure (purchases or COGS, an income-statement item that accumulates over a period). The averaging convention converts the stock measure into something comparable to the flow measure by representing the typical AP level throughout the period rather than a single point-in-time snapshot.

What goes wrong with ending AP:

1. **End-of-period anomalies distort the metric.** A company that pushes invoices out the door in the last week of the year (to compress AP for working-capital reporting) or holds invoices in the last week (to stretch DPO) will produce an ending balance that does not reflect typical operations. Average AP smooths these end-effects.

2. **Consistency between numerator and denominator.** Purchases or COGS is an over-the-period number. If the denominator covers the full period, the numerator should represent the period too — average AP does that; ending AP doesn't.

3. **Comparability across companies.** Different firms close their books on different cycles; ending AP varies systematically with fiscal calendar. Averaged AP is more comparable.

4. **Audit defensibility.** Stock/flow consistency is a documented accounting principle (Holthausen & Zmijewski 2014). Using ending AP without disclosure invites a sourcing-quality challenge during diligence.

The canonical formula is therefore: DPO = (Average AP / Purchases) × N, where 'Average AP' is typically (Beginning AP + Ending AP) / 2 for annual analysis or a more granular average (monthly average) for shorter-period analysis. Some firms use COGS in the denominator instead of Purchases as a practical proxy when Purchases isn't disclosed; the stock/flow consistency principle still requires averaging.

### Model response

# Accounts Payable Days (DPO) and the Averaging Convention

## The Core Formula

$$\text{DPO} = \frac{\text{Accounts Payable}}{\text{COGS / Days}}= \frac{\text{Accounts Payable} \times \text{Days in Period}}{\text{COGS}}$$

The question is: which AP figure belongs in the numerator?

---

## Why the Balance Sheet Is a "Snapshot" Problem

The income statement (COGS) measures a **flow** over an entire period—say, 365 days of purchasing activity. The balance sheet AP figure is a **stock** measured at a single instant in time (the last second of December 31, for example).

These two numbers live on different temporal planes. To make a ratio meaningful, you need the stock variable to be **representative of the same period** the flow variable covers. A single end-of-period snapshot is often *not* representative of the whole period.

---

## What the Averaging Convention Solves

### 1. Matching the Balance to the Period

The average AP balance—typically **(Beginning AP + Ending AP) / 2**—is a simple approximation of the **time-weighted average level of payables that existed throughout the period**. This makes it conceptually consistent with the full-year COGS figure in the denominator.

Think of it this way: COGS "used up" payables capacity steadily across the year. The relevant AP balance is the one that *supported* that activity, not the one that happened to exist at year-end.

### 2. Controlling for Seasonal and Timing Distortions

Many businesses have highly seasonal purchasing patterns. A retailer's AP balance at December 31 may be abnormally **low** (it just paid off holiday inventory it bought in Q3/Q4) or abnormally **high** (it is still sitting on late-December deliveries). Either extreme makes the ending balance unrepresentative.

By averaging beginning and ending, you capture at least two data points that bracket the year, damping out extreme end-of-period positions.

### 3. Removing Management's Ability to "Window Dress" the Ratio

A company that wants to show faster payment (lower DPO—perhaps to look like a good customer or to hit a covenant) can simply time a large payment right before year-end. Similarly, a company that wants to show it is conserving cash can delay payments strategically. Averaging makes such one-day manipulations only **half as powerful**, because the beginning balance is outside management's current-period control.

### 4. Consistency with How Other Turnover Metrics Are Computed

DPO is part of a family of metrics—DSO (receivables days), DIO (inventory days), and the Cash Conversion Cycle. All of them conventionally use average balances. Using averages for AR and inventory but the ending balance for AP would make the CCC internally inconsistent and not comparable across companies or across time.

---

## What Goes Wrong If a Junior Analyst Uses the Ending Balance

| Scenario | Effect on Ending-AP DPO | Reality |
|---|---|---|
| Company pays down AP aggressively in December (window dressing) | DPO **understated** — looks like a fast payer | Payments were actually slower all year |
| Company deliberately delays year-end payments | DPO **overstated** — looks like a slow payer | Cash management was actually tighter all year |
| Business is growing rapidly (AP naturally higher at year-end) | DPO **overstated** — denominator (COGS) grew all year, numerator is at peak | Analyst incorrectly infers deteriorating payment behavior |
| Business is shrinking or destocking | DPO **understated** | Analyst incorrectly infers improving payment discipline |

### The Growth Distortion Deserves Special Emphasis

Suppose a company's AP was $50M at the start of the year and $100M at year-end because the business doubled in size. COGS for the year is, say, $400M.

- **Average AP method:** DPO = (($50M + $100M)/2) / ($400M/365) = **$75M / $1.096M ≈ 68 days** ✓ Reasonable
- **Ending AP method:** DPO = $100M / $1.096M ≈ **91 days** ✗ Inflated—not because the company is paying slower, but because the ending balance reflects a much larger business than existed at the start of the year

The ending-balance DPO incorrectly signals that the company has extended its payment terms when in fact it has simply grown.

---

## Important Caveats and Limitations

1. **Simple averaging is still imperfect.** Two data points can miss intra-year seasonality. Analysts with access to quarterly data often use a four-point or five-point average (beginning + four quarter-ends, divided by 5), which is more precise.

2. **The denominator choice matters too.** Some analysts use **purchases** (COGS + change in inventory) instead of COGS, which is theoretically more correct because AP arises from purchases, not from goods sold. However, purchases are rarely disclosed in aggregate, so COGS is the practical proxy.

3. **Averaging doesn't eliminate all manipulation.** A company that window-dresses *both* December 31 and January 1 (the prior year-end) neutralizes the convention entirely.

4. **Industry and context still require judgment.** Even a "correct" DPO must be benchmarked against peers, payment terms in the industry, and the company's own trend.

---

## Summary

The averaging convention exists because **a flow variable (COGS) should be divided by a representative stock variable, not a point-in-time snapshot**. Without it, seasonal timing, business growth, and opportunistic balance-sheet management all corrupt the ratio—making a company look like a faster or slower payer than it actually was during the period under review. Using the average AP balance is the standard, practical way to put the numerator and denominator on the same temporal footing.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response clearly articulates the stock/flow consistency principle (explicitly using those terms), identifies end-of-period anomalies including window-dressing and seasonal distortions, addresses comparability (across the CCC family of metrics and across companies), and presents the canonical formula with the average-AP convention. It also adds valuable depth on growth distortion and caveats about purchases vs. COGS.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_017 — invoice_processing · medium · **score 2/2** (model: `claude-opus-4-7`)

_Expected failure mode: domain conventions (P2P control taxonomy)_

### Question

Explain the difference between a 'duplicate vendor record' and a 'duplicate payment.' Both are control concerns and both can result in improper cash outflows, but they are caught by different control regimes. What's the distinction, and why is it operationally important to keep the two regimes separate?

### Rubric

- **0**: Treats the two as the same concept, OR fails to distinguish master-data from transaction-stream controls, OR provides only one regime's controls without the other
- **1**: Distinguishes the two phenomena but does not articulate the different control regimes, OR misses the bridge-case (duplicate payment across two duplicate vendor records), OR addresses only one of the operational-importance reasons
- **2**: Cleanly distinguishes master-data hygiene from transaction-stream control, names specific controls in each regime, identifies the bridge case (cross-vendor-ID matching), and addresses at least two of: ownership separation, audit-evidence separation, remediation-path differences

### Ideal answer

[AI DRAFT — practitioner review required] **Duplicate vendor record** = the same legal entity appears twice (or more) in the supplier master under distinct vendor IDs. The records may have variant names, slightly different addresses, possibly different bank accounts. The legal entity is one; the master-data representation is multiple.

**Duplicate payment** = the same invoice (same supplier, same invoice number, same amount, same period) gets paid more than once. Could happen against a single vendor record (e.g., supplier resubmits the invoice with a slight number variation and AP doesn't catch the match) or across two duplicate vendor records (the harder case to detect).

The two are categorically distinct because they sit on different sides of the P2P process and are caught by different controls:

**Duplicate vendor record** is a master-data hygiene issue. Caught by:
- Periodic vendor-master cleansing routines
- TIN-based dedupe analytics (anchor on TIN, surface variant names)
- Maker-checker on new vendor adds
- Employee-vendor match analytics (employee data crossed against vendor data)
This regime operates BEFORE invoices are entered. It's a preventive control on the master data.

**Duplicate payment** is a transaction-stream issue. Caught by:
- (Vendor + invoice number) exact match at invoice entry
- (Vendor + amount + date within window) fuzzy match
- Cross-vendor amount + PO match (catches duplicates across two duplicate vendor records — the bridge case)
- Reverse-amount matching (catches re-billing after a credit memo)
This regime operates AT invoice entry and is a detective/preventive control on the transaction.

**Why the distinction is operationally important:**

1. **Different ownership.** Master-data hygiene typically sits with a procurement-ops or master-data steward team. Duplicate-payment monitoring sits with AP. Conflating the two leads to ownership confusion and gap.

2. **Different audit evidence.** SOX P2P walkthroughs sample the two regimes separately. A vendor-master walkthrough samples vendor adds; a duplicate-payment walkthrough samples payment runs. Auditors expect distinct evidence trails.

3. **Different remediation paths.** A duplicate vendor record gets fixed by consolidation (with the multi-step pre-merge control sweep — see q_001). A duplicate payment gets fixed by recovery (vendor refund, contra-payable, or write-off if uncollectible).

4. **The bridge case is where both regimes matter.** When a duplicate payment occurs ACROSS two duplicate vendor records, it would have been prevented if the master-data regime had caught the duplicate vendor first. This is why duplicate-payment monitoring should include cross-vendor-ID amount matching as a backstop to master-data hygiene gaps.

Keeping the two distinct in the controls framework, in the audit workpapers, and in role assignments ensures both gaps get coverage rather than each assuming the other will catch it.

### Model response

# Duplicate Vendor Records vs. Duplicate Payments

These are related but fundamentally distinct control concerns in the procure-to-pay (P2P) cycle. Conflating them is one of the more common weaknesses I see in AP control design.

## The Distinction

**Duplicate Vendor Record** — A *master data* defect. The same supplier exists in the vendor master file under two or more vendor IDs. Causes include:
- Name variations ("IBM Corp." vs. "International Business Machines")
- Address or DBA differences (HQ vs. remit-to address)
- Acquisitions/rebrands creating parallel records
- Tax ID entered with/without dashes, or missing entirely
- Intentional creation by a fraudster to bypass approval limits or insert a shell entity adjacent to a legitimate one

The defect exists *before any invoice is processed*. It is a static, structural condition of the vendor master.

**Duplicate Payment** — A *transactional* defect. The same economic obligation is paid more than once. Causes include:
- Invoice keyed twice (same vendor, same invoice number, sometimes with a leading zero or trailing space difference)
- Invoice paid against a PO and again against a non-PO workflow
- Credit memo not applied, then a manual refund issued
- Statement payment plus invoice payment for the same items
- Payment via two channels (check and ACH) when the first is presumed lost

The defect exists *at the moment of disbursement*, regardless of whether the vendor master is clean.

## Why They Are Caught by Different Control Regimes

**Vendor master controls** are *preventive* and *data-governance* controls:
- Segregation of duties between vendor setup and invoice/payment processing
- Fuzzy-match algorithms on name, address, tax ID, and bank account at the point of vendor creation
- Periodic vendor master cleansing and dormancy reviews
- Tax ID (W-9/W-8) validation and IRS TIN matching
- Bank account verification (e.g., Positive Pay-style or third-party validation services like SAP Ariba, Dun & Bradstreet)
- Approval workflow for new vendor creation, ideally with management above the requestor

**Duplicate payment controls** are *detective and preventive transaction controls*:
- ERP duplicate-invoice check at entry (vendor + invoice number + amount + date)
- Three-way match (PO, receipt, invoice)
- Pre-disbursement edit reports flagging same-amount/same-vendor pairs within a window
- Post-payment recovery audits (often outsourced to firms like PRGX or APEX Analytix)
- Statement reconciliations with vendors

## Why Operational Separation Matters

Keeping the two regimes distinct is important for several concrete reasons:

1. **Different risk owners.** Vendor master integrity typically sits with a master data management (MDM) function or procurement; payment integrity sits with AP operations. Merging them obscures accountability and weakens segregation of duties — the very SOD that prevents fictitious-vendor fraud.

2. **Different failure modes and remediation.** A duplicate vendor record can cause a duplicate payment, but it can also enable *fraud* (a planted shell vendor that is by design a "near-duplicate" of a real one). Cleaning a duplicate payment by issuing a recovery claim does nothing to fix the underlying master data; the next invoice will replicate the error. Conversely, deduplicating the vendor master does not recover money already double-paid.

3. **Different detection logic.** Vendor master deduplication relies on entity-resolution techniques (fuzzy matching, tax ID, banking). Duplicate payment detection relies on transactional matching across invoice attributes. The algorithms, tooling, and tolerance thresholds are not interchangeable — for example, you *want* a tight match in payment dedup (false positives delay legitimate payments), but a *loose* fuzzy match in vendor dedup (false negatives let fraud through).

4. **Different audit and SOX implications.** A duplicate vendor record is a control *deficiency* in master data governance even if no improper payment ever occurs — it represents latent risk and a potential control gap an external auditor or fraud examiner will flag. A duplicate payment is a realized control failure with a quantifiable financial statement impact. The two get reported, escalated, and remediated differently.

5. **Fraud detection sensitivity.** The most damaging schemes — vendor impersonation, bank account takeover, "ghost vendor" insertion by an employee — manifest first in the *vendor master*, often months before any anomalous payment is detectable transactionally. If you rely solely on duplicate-payment controls, you're catching the symptom, not the disease, and only after cash has left the building.

## Bottom Line

Think of it as the difference between **who you can pay** (vendor master) and **what you actually paid** (transactions). Both regimes must exist independently, with different owners, different tools, and different review cadences. A mature AP control environment treats vendor master hygiene as a continuous data governance discipline and duplicate payment prevention as a transactional edit-and-audit discipline — and never lets one substitute for the other.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response cleanly distinguishes master-data hygiene from transaction-stream controls, names specific controls in each regime (fuzzy matching, TIN validation, SOD for vendor master; three-way match, duplicate-invoice check, recovery audits for payments), and addresses multiple operational-importance reasons including ownership separation, remediation differences, and audit/SOX implications. The bridge case is implicitly addressed in point 2 ('A duplicate vendor record can cause a duplicate payment') and point 5, though it could be more explicit about cross-vendor-ID matching as a backstop. Still, the response substantially exceeds the bar for a 2.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_017 — invoice_processing · medium · **score 2/2** (model: `claude-sonnet-4-6`)

_Expected failure mode: domain conventions (P2P control taxonomy)_

### Question

Explain the difference between a 'duplicate vendor record' and a 'duplicate payment.' Both are control concerns and both can result in improper cash outflows, but they are caught by different control regimes. What's the distinction, and why is it operationally important to keep the two regimes separate?

### Rubric

- **0**: Treats the two as the same concept, OR fails to distinguish master-data from transaction-stream controls, OR provides only one regime's controls without the other
- **1**: Distinguishes the two phenomena but does not articulate the different control regimes, OR misses the bridge-case (duplicate payment across two duplicate vendor records), OR addresses only one of the operational-importance reasons
- **2**: Cleanly distinguishes master-data hygiene from transaction-stream control, names specific controls in each regime, identifies the bridge case (cross-vendor-ID matching), and addresses at least two of: ownership separation, audit-evidence separation, remediation-path differences

### Ideal answer

[AI DRAFT — practitioner review required] **Duplicate vendor record** = the same legal entity appears twice (or more) in the supplier master under distinct vendor IDs. The records may have variant names, slightly different addresses, possibly different bank accounts. The legal entity is one; the master-data representation is multiple.

**Duplicate payment** = the same invoice (same supplier, same invoice number, same amount, same period) gets paid more than once. Could happen against a single vendor record (e.g., supplier resubmits the invoice with a slight number variation and AP doesn't catch the match) or across two duplicate vendor records (the harder case to detect).

The two are categorically distinct because they sit on different sides of the P2P process and are caught by different controls:

**Duplicate vendor record** is a master-data hygiene issue. Caught by:
- Periodic vendor-master cleansing routines
- TIN-based dedupe analytics (anchor on TIN, surface variant names)
- Maker-checker on new vendor adds
- Employee-vendor match analytics (employee data crossed against vendor data)
This regime operates BEFORE invoices are entered. It's a preventive control on the master data.

**Duplicate payment** is a transaction-stream issue. Caught by:
- (Vendor + invoice number) exact match at invoice entry
- (Vendor + amount + date within window) fuzzy match
- Cross-vendor amount + PO match (catches duplicates across two duplicate vendor records — the bridge case)
- Reverse-amount matching (catches re-billing after a credit memo)
This regime operates AT invoice entry and is a detective/preventive control on the transaction.

**Why the distinction is operationally important:**

1. **Different ownership.** Master-data hygiene typically sits with a procurement-ops or master-data steward team. Duplicate-payment monitoring sits with AP. Conflating the two leads to ownership confusion and gap.

2. **Different audit evidence.** SOX P2P walkthroughs sample the two regimes separately. A vendor-master walkthrough samples vendor adds; a duplicate-payment walkthrough samples payment runs. Auditors expect distinct evidence trails.

3. **Different remediation paths.** A duplicate vendor record gets fixed by consolidation (with the multi-step pre-merge control sweep — see q_001). A duplicate payment gets fixed by recovery (vendor refund, contra-payable, or write-off if uncollectible).

4. **The bridge case is where both regimes matter.** When a duplicate payment occurs ACROSS two duplicate vendor records, it would have been prevented if the master-data regime had caught the duplicate vendor first. This is why duplicate-payment monitoring should include cross-vendor-ID amount matching as a backstop to master-data hygiene gaps.

Keeping the two distinct in the controls framework, in the audit workpapers, and in role assignments ensures both gaps get coverage rather than each assuming the other will catch it.

### Model response

# Duplicate Vendor Records vs. Duplicate Payments: A Control Taxonomy

## Core Definitions

### Duplicate Vendor Record
A duplicate vendor record exists when the **same real-world supplier is represented more than once in the vendor master file** — typically with different vendor IDs, slightly different names, different addresses, or minor variations in tax identification numbers (e.g., "Acme Corp," "ACME Corporation," "Acme Corp."). The duplicate exists **at the standing data level**, before any transaction is processed.

### Duplicate Payment
A duplicate payment occurs when **the same valid obligation is paid more than once** — typically by processing the same invoice twice, or paying two invoices that represent the same underlying obligation. The duplication exists **at the transaction level**, and may or may not involve a duplicate vendor record.

---

## The Structural Distinction

| Dimension | Duplicate Vendor Record | Duplicate Payment |
|---|---|---|
| **Where it lives** | Standing/master data | Transaction processing |
| **When risk materializes** | Exists before any payment | Occurs during payment run |
| **Trigger** | Vendor onboarding/maintenance process failure | Invoice receipt and payment processing failure |
| **Harm mechanism** | Enables future improper payments; obscures vendor relationship | Direct cash outflow for an obligation already discharged |
| **Can occur without the other?** | Yes — record can sit dormant indefinitely | Yes — same vendor ID can be paid twice |
| **Fraud vector** | Shell company insertion; fictitious vendor creation | Invoice re-submission; split invoices; system timing manipulation |

---

## Why They Are Caught by Different Control Regimes

### Controls Over Duplicate Vendor Records — The Master Data Regime

This regime is concerned with **who is authorized to exist in the system** as a payable entity. Controls include:

- **Segregation of duties** between vendor setup and payment authorization (the person who adds a vendor cannot approve payments to that vendor)
- **Duplicate detection algorithms** run at onboarding: fuzzy name matching, EIN/VAT number matching, bank account number matching, address matching
- **Periodic vendor master file cleansing** — deactivating dormant vendors, merging duplicates, confirming legitimacy of active records
- **New vendor approval workflows** — independent review before activation
- **Beneficial ownership verification** — particularly important for fraud prevention

The *failure mode* this regime guards against is: **a payable pathway existing to an illegitimate or redundant destination**. Even if every payment is properly approved and processed, money flows to the wrong place because the master data was corrupted.

### Controls Over Duplicate Payments — The Transaction Processing Regime

This regime is concerned with **whether each payment instruction corresponds to exactly one valid, unpaid obligation**. Controls include:

- **Three-way matching** (purchase order → goods receipt → invoice) at the transaction level
- **Unique invoice number + vendor ID combination** constraints in the accounts payable system (system-enforced blocking of re-entry)
- **Check number sequencing** and payment reference controls
- **Pre-payment duplicate detection** — system flags same vendor + same amount + close date as suspicious
- **Statement reconciliation** — comparing vendor statements to payment records to identify credits owed
- **Positive pay** — bank-level control confirming each presented check was legitimately issued

The *failure mode* this regime guards against is: **the payment process executing the same valid obligation more than once**, regardless of whether the vendor master is clean.

---

## Why Operational Separation Matters

### 1. A Clean Vendor Master Does Not Prevent Duplicate Payments
An organization can have perfectly deduplicated, verified vendor records and still pay the same invoice twice — because the payment duplication arises from process failures in invoice handling (e.g., paper invoice entered manually and also received via EDI, processed in two different AP systems, or submitted by the vendor in two billing cycles). The master data was never the problem.

### 2. A Clean Transaction Process Does Not Prevent Vendor Record Risk
Conversely, if every invoice goes through rigorous three-way matching and duplicate invoice controls, a dormant shell vendor sitting in the master file represents a latent risk — any payment eventually processed to that vendor flows to an illegitimate destination. The transaction controls passed perfectly, but the standing data was compromised.

### 3. Fraud Patterns Are Regime-Specific
- **Accounts payable fraud** exploiting duplicate vendor records typically involves **insider creation** of fictitious or near-duplicate vendors with bank accounts controlled by the fraudster — detected only by master data scrutiny and segregation of duties.
- **Duplicate payment fraud/error** typically involves **invoice manipulation** — submitting the same invoice via multiple channels — detected by transaction-level controls and reconciliation.

Conflating the two leads organizations to rely on whichever control is most visible while leaving the other regime under-resourced.

### 4. Audit and Remediation Processes Differ
- Remediating a duplicate vendor record requires **master data governance**: merge records, re-point historical transactions, notify banking, update procurement systems, and assess whether prior payments were proper.
- Remediating a duplicate payment requires **cash recovery**: demand credit notes or refunds from suppliers, adjust open payables, and investigate the process gap that allowed the second payment.

These involve different teams (IT/master data governance vs. treasury/AP operations), different timelines, and different controls testing during audit.

### 5. Systemic vs. Transactional Risk Profile
Duplicate vendor records represent **systemic risk** — a single corrupted master record can generate many improper payments over time before detection. Duplicate payments are often **episodic** — a specific process failure on a specific invoice, often catchable quickly through statement reconciliation.

This risk profile difference should drive different **monitoring frequencies** (continuous master data monitoring vs. pre-payment run duplicate checks) and different **materiality thresholds** in internal audit planning.

---

## A Practical Illustration

> Vendor "Smith Supplies Inc." exists twice in the vendor master: ID 10045 (legitimate, correct bank account) and ID 10892 (fraudulent, controlled by an insider, slightly different name "Smith Supply Inc."). 
>
> Invoice #7741 for $50,000 is entered under ID 10045 and paid correctly — **no duplicate payment**. But separately, a fraudulent invoice under ID 10892 is approved and paid — **a duplicate vendor record problem masquerading as a legitimate payment**. The transaction-level controls saw nothing wrong.
>
> Later, Invoice #7741 is inadvertently re-entered by a clerk and paid again under ID 10045 — **a duplicate payment**. The vendor master was clean; the process was not.

Both result in improper cash outflows. The first is invisible to transaction controls; the second is invisible to master data controls. Neither regime substitutes for the other.

---

## Summary

The essential operational principle is:

> **Master data controls govern who can be paid; transaction controls govern how many times a valid obligation is paid.** Both must function independently and completely, because the failure modes are orthogonal — each can occur in the total absence of the other. Organizations that collapse them into a single "duplicate review" process will reliably have blind spots in one dimension or the other.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response cleanly distinguishes master-data hygiene from transaction-stream control regimes, names specific controls in each (fuzzy matching/EIN matching/SoD for vendor master; three-way matching/unique invoice+vendor constraints/duplicate detection for payments). It addresses multiple operational-importance reasons including ownership separation (IT/master data governance vs. treasury/AP), remediation-path differences (merge records vs. cash recovery), audit differences, and fraud pattern differences. The illustration with Smith Supplies covers the bridge case where a duplicate vendor record enables an improper payment that transaction controls miss, though it doesn't explicitly emphasize cross-vendor-ID amount matching as a backstop control. Still, the bridge case is clearly identified conceptually, and the response exceeds the bar on the operational-importance dimensions.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_018 — close_and_controls · hard · **score 2/2** (model: `claude-haiku-4-5`)

_Expected failure mode: control framework reasoning under SOX (multi-tier diagnosis)_

### Question

An improper payment was made. The same observable outcome ($X to wrong supplier or wrong amount) could be the result of a tactical 3-way-match exception that AP missed, OR a SOX P2P control design failure. The IT and audit treatment of these two diagnoses is very different. Explain the canonical hierarchy of control failures (transaction-level → policy-level → design-level), what evidence distinguishes each, and why it matters which diagnosis applies.

### Rubric

- **0**: Conflates the three tiers, OR fails to identify that the same observable can have different diagnoses, OR misses the audit / disclosure / remediation differences entirely
- **1**: Distinguishes the three tiers but does not address the bottom-up investigation order, OR misses the audit/disclosure thresholds (control deficiency / significant deficiency / material weakness), OR gives only one of the four 'why it matters' reasons
- **2**: Distinguishes all three tiers with concrete examples, addresses the audit / disclosure / remediation hierarchy (control deficiency → significant deficiency → material weakness), explains the bottom-up investigation order, gives a worked example showing the same observable resolving differently across tiers, and references the relevant audit framework (AS 2201 / COSO)

### Ideal answer

[AI DRAFT — practitioner review required] The canonical control-failure hierarchy goes from narrowest to broadest:

**Tier 1 — Transaction-level failure (a single control instance failed to operate).**
The control existed and was designed correctly, but in this specific transaction it didn't catch the issue. Example: 3-way match was supposed to flag the price variance but the AP clerk overrode it without proper documentation. The clerk's override is the failure point.

Evidence: the audit trail shows the control SHOULD have triggered (the variance was within the configured threshold), AND it shows manual override or bypass. The control configuration itself is correct.

Remediation: re-train the operator, tighten override authority, add maker-checker on overrides. Narrow remediation, narrow disclosure.

**Tier 2 — Policy-level failure (the control is designed correctly but the policy that governs it has a gap).**
The control as designed wouldn't have caught this fact pattern because the policy didn't anticipate the scenario. Example: 3-way match was configured for goods POs but services POs were exempted by policy without compensating control; an improper payment on a services PO slips through.

Evidence: the audit trail shows the control did not trigger BECAUSE the transaction was out of the policy scope. No bypass occurred — the policy itself is the gap.

Remediation: rewrite the policy to close the carve-out, add the compensating control, document the change. Broader remediation: every transaction in the policy gap window may need lookback review.

**Tier 3 — Design-level failure (the control framework itself is structurally inadequate).**
The control as conceived cannot prevent the class of issue that occurred. Example: a single AP clerk has vendor-master add + invoice approval + payment initiation entitlements. The 3-way match working perfectly does not stop this person from creating a ghost vendor and routing payments to themselves — that's not what 3-way match controls. The SoD design is the failure.

Evidence: the audit trail may show no individual control fired or failed; the loss occurred *between* controls or *outside* their scope. The framework, not the operation, is the gap.

Remediation: redesign the control framework — entitlement architecture, SoD matrix, ITGC review cadence. Broadest remediation. Material weakness assessment. SOX 404 disclosure consideration. Possible restatement.

**Why the diagnosis matters:**

1. **Audit treatment.** Tier-1 is a 'control deficiency.' Tier-2 is typically a 'significant deficiency.' Tier-3 is most likely a 'material weakness.' Each has different SOX disclosure thresholds and different external-auditor responses.

2. **Disclosure.** Material weakness requires Form 10-K Item 9A disclosure and adverse ICFR opinion; significant deficiency may not require external disclosure but requires audit committee communication. Control deficiency may stay in internal-audit workpapers.

3. **Scope of remediation effort.** Tier-1 affects one role/process. Tier-2 affects every transaction in the policy gap window — lookback scope is significant. Tier-3 affects every transaction the design failure could have enabled — lookback scope is comprehensive (per the q_010 fact pattern, this is what drives the 24-36-month all-vendor lookback).

4. **Investigation methodology.** Tier-1 is a process review (interview the clerk, review the override). Tier-2 is a policy review (compare written policy to the risk universe). Tier-3 is an architecture review (entitlement model, SoD matrix, ITGC) and typically pulls in IT audit, IS security, and possibly external counsel.

5. **Where the same observable can be diagnosed differently.** A duplicate-payment fact pattern could be Tier-1 if the AP clerk missed an obvious match the system flagged; Tier-2 if the duplicate-detection rules don't cover cross-vendor-ID matching (a policy gap); Tier-3 if the same person who added the duplicate vendor is also approving payments (an SoD design gap that enabled the duplicate vendor in the first place). The diagnosis drives whether you fix the operator, the policy, or the architecture — and getting the diagnosis wrong leads to either over- or under-remediation.

The canonical investigation order is bottom-up: confirm Tier-1 first (was this an operator failure?), only escalate to Tier-2 if the operator-failure hypothesis doesn't fit (the system should have caught it but the configuration didn't), and only escalate to Tier-3 if the policy-failure hypothesis doesn't fit (the configuration was right but the framework was inadequate).

References: PCAOB AS 2201 (definitions of control deficiency, significant deficiency, material weakness); COSO 2013 framework Component 4 'Control Activities' and Component 5 'Monitoring Activities'; SEC Regulation S-K Item 308.

### Model response

# Hierarchical Control Failure Diagnosis in P2P

This is a critical analytical framework because the *same observed defect* has radically different remediation, audit, and SOX implications depending on where in the control stack the failure occurred.

## The Three-Level Hierarchy

```
DESIGN FAILURE (Systemic/Control Environment)
    ↓ enables
POLICY FAILURE (Control Operating Model)
    ↓ enables
TRANSACTION FAILURE (Tactical/Execution)
```

### Level 3: Transaction-Level Failure (Weakest Diagnosis)
**Definition**: The control *exists, is designed correctly, and is documented*, but failed on this specific instance due to execution error.

**Evidence of transaction-level failure:**
- Control tested successfully in prior periods
- Similar transactions processed correctly in same period
- AP analyst had proper tools, data visibility, and authorization
- Investigation reveals: distraction, system lookup error, one-time data transcription mistake
- Preventive controls present (validation rules) didn't trigger (suggesting exception override authority was used)
- Corrective action sufficient: retraining, performance counseling, or process adjustment

**Example**: Analyst misread a PO digit in a known-supplier exception, or approved variance within authority but clicked wrong supplier dropdown.

---

### Level 2: Policy/Procedure Failure (Intermediate Diagnosis)
**Definition**: Design is sound, but the operating procedures, execution protocols, or compensating controls lack sufficient specificity, approval limits, or checkpoints.

**Evidence of policy failure:**
- Multiple similar exceptions approved in same period
- Exception criteria too broad or documented ambiguously
- Approval thresholds misaligned with actual risk (e.g., $100k variances approved by AP coordinator)
- Missing compensating control for high-risk transaction type
- Inadequate segregation of duties documented in procedure
- Change management absent when supplier data updates
- Recurrence across multiple AP staff

**Example**: No requirement to validate supplier *bank account change* before 3-way match; procedure allows AP to override quantity variance >10% without finance review; no monthly reconciliation of exceptions taken.

---

### Level 1: Design Failure (Root Cause - Highest Risk)
**Definition**: The control architecture itself is inadequate—missing entirely, fundamentally flawed, or disconnected from actual transaction flow.

**Evidence of design failure:**
- **No compensating control** exists for a known P2P risk (e.g., no duplicate-invoice detection in ERP)
- **Control environment evidence**: similar errors recur across multiple periods, multiple suppliers, multiple staff despite coaching
- **System configuration missing**: 3-way match exception workflow not configured in ERP; exception routing bypasses required approver
- **Scope gap**: certain transaction types (consignment, intercompany, expense reimbursement) explicitly excluded from 3-way match requirement
- **Access/authority design flaw**: wrong role assigned exception approval authority
- **Data quality design gap**: supplier master validation rules missing on key fields (site, bank details)
- **Testing reveals**: control doesn't operate as documented in control narrative
- **Policy doesn't address** the transaction characteristic that created risk

**Example**: ERP 3-way match disabled for suppliers meeting certain criteria; no design control for contract-based purchases; accrual-to-payment reconciliation not performed at cost center level where $X payment originated.

---

## Critical Evidentiary Distinctions

| Dimension | Transaction | Policy | Design |
|-----------|-------------|--------|--------|
| **Frequency** | Isolated incident | Cluster in same period | Pattern across multiple periods |
| **Affected population** | Single transaction, one processor | Multiple transactions, multiple processors | All transactions of type X |
| **Process re-examination** | Works as documented | Procedure ambiguous or incomplete | Control missing from procedure entirely |
| **System configuration** | Control exists in system | Workflow misconfigured | Control not configured in ERP at all |
| **Prior audit finding** | No; newly discovered | Likely; noted as observation | Likely; noted as deficiency |
| **Root cause trail** | Stops at individual action | Stops at policy/procedure gap | Stops at control architecture |

---

## Why Diagnosis Matters: Audit & SOX Implications

### Transaction-Level Finding
**Audit classification**: Control deficiency (not significant)
- Conclude: "Control operated effectively; isolated execution error"
- **Remediation**: Performance management, refresher training, system alert
- **SOX evaluation**: No design weakness. Single error ≠ ineffective control design
- **Testing implication**: No need to expand sample; documented exception handling sufficient
- **Re-audit**: Return to normal sampling next period; monitor individual's subsequent transactions

---

### Policy-Level Finding
**Audit classification**: Significant deficiency (material weakness candidate)
- Conclude: "Control design adequate, but operating procedures inadequate"
- **Remediation**: Revise exception approval matrix, tighten variance thresholds, add compensating control (e.g., mandatory secondary review), enhance training
- **SOX evaluation**: Potential material weakness if across multiple transaction types or high-dollar exposure
- **Testing implication**: Expand sample to all similar exceptions in period; test compensating controls if control relied upon doesn't operate as intended
- **Documentation requirement**: Formalize exception criteria in control procedure; document approver qualifications
- **Timeline**: Control remediation expected within current fiscal year

---

### Design-Level Finding
**Audit classification**: Material weakness (reportable deficiency)
- Conclude: "Control environment fails to address known P2P risks"
- **Remediation**: Reconfigure ERP workflow, redesign approval authority matrix, build new system validation rule, restructure cost allocation or payment method
- **SOX evaluation**: Presumptive material weakness; must evaluate whether reasonable possibility of material misstatement exists
- **Testing implication**: Control cannot be relied upon; alternative audit procedures required; likely requires broader scope across multiple cycles
- **Documentation requirement**: Control narrative must be rewritten to reflect true control activity
- **Timeline**: Material weaknesses require remediation and testing by year-end; material control deficiency; likely requires management assessment update and auditor re-evaluation of control design

---

## Diagnostic Checklist: Which Level Is This?

**Ask in order:**

1. **Does the control exist in the ERP configuration or documented procedure?**
   - No → **Design failure**
   - Yes → Continue

2. **Has this exact transaction type failed before (in prior periods or other processors)?**
   - Yes, repeatedly, across multiple people/periods → **Design failure**
   - Yes, occasionally, inconsistent → **Policy failure**
   - No, first occurrence → Continue

3. **When you trace the exception, is it following the documented approval workflow and policy thresholds?**
   - No; control was overridden, ignored, or misconfigured → **Policy failure**
   - Yes; control was followed, but analyst made a judgment error within their authority → **Transaction failure**

4. **Does the procedure clearly define the criteria for this exception, approval limits, and required documentation?**
   - No; procedure is silent or ambiguous on this scenario → **Policy failure**
   - Yes; procedure is clear → **Transaction failure**

---

## Why This Matters in Practice

**A misdiagnosed transaction-level error as design failure → Unnecessary system redesign, opportunity cost, false remediation**

**A misdiagnosed design failure as transaction-level → Repeat exceptions, increased audit risk, control reliance unjustified, SOX deficiency missed**

The hierarchy enforces rigor: assume the control works as designed until evidence proves otherwise. Burden of proof rises with each level.

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response distinguishes all three tiers with concrete examples (transaction-level execution error, policy gap with ambiguous exception criteria, design failure like missing 3-way match for certain supplier types). It addresses the audit/disclosure hierarchy explicitly mapping to control deficiency → significant deficiency → material weakness. It provides a bottom-up diagnostic checklist (the 'Ask in order' section) which captures the canonical investigation order. It gives worked examples showing the same observable (improper payment) resolving differently across tiers. The remediation scope differences are addressed. Minor gap: it does not explicitly cite AS 2201 or COSO by name, though it uses SOX framework terminology throughout. The rubric mentions 'AS 2201 / COSO' as part of tier 2, but the response covers all other elements thoroughly with concrete examples and the bottom-up order. Overall meets the tier-2 bar substantively.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---
