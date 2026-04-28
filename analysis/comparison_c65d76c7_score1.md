# ProfBench comparison — run `c65d76c7-bf3a-4cb7-a7fb-23a92ba83b83`

For each question below: read the model's response next to the ideal answer, then categorize:

- **(a) model fell short** — keep the question, score is honest
- **(b) ideal_answer too narrow** — the model's response is actually acceptable; broaden the ideal answer (do not change the question)
- **(c) rubric miscalibrated** — tier definitions need to be more specific so the grader doesn't mark partial answers down unfairly

Only (b) and (c) justify editing `data/questions.json`. (a) is the benchmark working as intended.

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

- **0**: Says they are not duplicates, or fails to identify the TIN match, or recommends keeping both records active
- **1**: Identifies them as duplicates but misses the TIN-normalization reasoning, the dup-payment check, or the open-document migration step
- **2**: Identifies the duplicate via TIN normalization, picks the correct survivor with reasoning, and includes both the open-document migration and duplicate-payment lookback as control steps

### Ideal answer

Yes, these are duplicates. The TINs are identical — '12-3456789' and '123456789' are the same nine-digit EIN; the hyphen is a display convention only and TIN normalization (strip non-digits) is the correct primary-key match. Name variance ('Corp' vs. 'CORPORATION', case) is a normalization issue, not a different entity. Same bank account (Chase ****4521) is a strong corroborating signal. Address differs only in 'St' vs. 'Street' and the absent suite line on B — same street address.

Resolution: merge under a single canonical record. Survivor selection: keep Record A (active, recent activity, more complete address). Deactivate Record B with a cross-reference to A so historical AP/spend reporting still rolls up. Move any open POs/invoices on B to A before deactivation. Run a duplicate-payment check across both record IDs for the last 18 months as a control step (a duplicate vendor record is a known precondition for duplicate payments).

### Model response

# Duplicate Determination

**Yes — these are duplicates of the same legal entity.** Confidence: very high.

## Evidence supporting the match

| Attribute | Record A | Record B | Match? |
|---|---|---|---|
| Legal name | Acme Industrial Corp | ACME INDUSTRIAL CORPORATION | ✅ Same entity ("Corp" = "Corporation"); case/format only |
| TIN/EIN | 12-3456789 | 123456789 | ✅ Identical (hyphen is cosmetic in IRS EIN format) |
| Address | 100 Main St, Suite 200, Newark, NJ 07102 | 100 Main Street, Newark, NJ 07102 | ✅ Same street and ZIP; B is just less specific (missing suite) |
| Bank account | Chase ****4521 | Chase ****4521 | ✅ Identical — strongest single indicator |

The combination of **identical EIN + identical bank account** is conclusive. EIN alone legally identifies the entity; matching remit-to bank account effectively eliminates the possibility of a coincidental name collision (e.g., parent/subsidiary or franchisee using the same trade name).

## Resolution: Record A should survive as canonical

**Rationale (in priority order):**

1. **Recent activity / transactional currency.** Record A has an invoice within the last 30 days; Record B has been dormant for 18 months. Surviving the *active* record preserves AP continuity, open POs, payment history, and 1099 YTD totals without re-linking live transactions.
2. **Data completeness.** Record A carries the more complete address (includes "Suite 200"), which is required for accurate remittance, W-9 reconciliation, and tax form mailing.
3. **Format hygiene.** Record A's EIN is stored in canonical IRS format (`NN-NNNNNNN`); Record B's unformatted string is a data-quality defect typical of legacy or one-off entry.

## Recommended remediation steps

1. **Merge B → A** in the supplier master, preserving Record A's vendor ID.
2. **Re-point history:** reassign any historical POs, invoices, payments, and 1099 totals from B to A so prior-year tax reporting remains intact.
3. **Inactivate and flag B** as "Merged duplicate of [A's vendor ID]" — do not hard-delete (audit trail and SOX/record-retention requirements).
4. **Block re-use of B's vendor ID** to prevent accidental reactivation.
5. **Standardize on A:** keep the formatted EIN, full suite-level address, and validated bank account.
6. **Run a control sweep** for additional variants (e.g., "Acme Ind.", same EIN, same bank ****4521) before closing the cleanup ticket.
7. **Strengthen prevention:** enforce duplicate-detection rules in vendor onboarding on (a) normalized EIN and (b) bank account fingerprint — these would have blocked Record B at creation.

## Risk note

Before finalizing the merge, confirm via bank-account change controls that **no fraudulent insertion** has occurred (duplicate vendor records sharing a bank account can also be a vendor-impersonation pattern). Given both records show the *same* legitimate Chase account and the dormant record is the redundant one, this is almost certainly benign data sprawl rather than fraud — but the check should be documented.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies the duplicates via TIN normalization (noting hyphen is cosmetic), picks Record A as survivor with strong reasoning, and includes the open-document/history migration step (re-pointing POs, invoices, payments). However, it does not explicitly include a duplicate-payment lookback/check as a control step. The 'control sweep' mentioned is for finding additional variant records, not for detecting duplicate payments across the 18-month window. The fraud risk note is about bank account insertion, not duplicate payments. This misses a key rubric element for a score of 2.

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

- **0**: Says they are not duplicates, or fails to identify the TIN match, or recommends keeping both records active
- **1**: Identifies them as duplicates but misses the TIN-normalization reasoning, the dup-payment check, or the open-document migration step
- **2**: Identifies the duplicate via TIN normalization, picks the correct survivor with reasoning, and includes both the open-document migration and duplicate-payment lookback as control steps

### Ideal answer

Yes, these are duplicates. The TINs are identical — '12-3456789' and '123456789' are the same nine-digit EIN; the hyphen is a display convention only and TIN normalization (strip non-digits) is the correct primary-key match. Name variance ('Corp' vs. 'CORPORATION', case) is a normalization issue, not a different entity. Same bank account (Chase ****4521) is a strong corroborating signal. Address differs only in 'St' vs. 'Street' and the absent suite line on B — same street address.

Resolution: merge under a single canonical record. Survivor selection: keep Record A (active, recent activity, more complete address). Deactivate Record B with a cross-reference to A so historical AP/spend reporting still rolls up. Move any open POs/invoices on B to A before deactivation. Run a duplicate-payment check across both record IDs for the last 18 months as a control step (a duplicate vendor record is a known precondition for duplicate payments).

### Model response

## Duplicate Assessment: **YES, these are duplicates**

---

### Evidence Supporting Duplicate Determination

| Field | Record A | Record B | Assessment |
|-------|----------|----------|------------|
| **Name** | Acme Industrial Corp | ACME INDUSTRIAL CORPORATION | ✅ Same entity — abbreviated vs. full legal name |
| **TIN** | 12-3456789 | 123456789 | ✅ **Identical** — same EIN, different formatting only |
| **Address** | 100 Main St, Suite 200, Newark, NJ 07102 | 100 Main Street, Newark, NJ 07102 | ✅ Same address — "St" vs "Street"; Suite 200 likely omitted in B |
| **Bank** | Chase \*\*\*\*4521 | Chase \*\*\*\*4521 | ✅ **Identical** |
| **Activity** | Active, invoice 30 days ago | Active, no activity 18 months | ⚠️ A is operationally current |

The **TIN is the definitive key**: a single EIN cannot belong to two distinct legal entities. Combined with identical banking details, this is conclusive.

---

### Resolution

**Record A should survive as the canonical record**, for the following reasons:

1. **Recency**: Record A has transactional activity within 30 days, meaning its data (address, contacts, bank) is demonstrably current and validated by recent business activity.
2. **Data completeness**: Record A captures the Suite 200 detail, which is more precise and likely correct.
3. **Record B is stale**: 18 months of inactivity raises the risk that its data reflects an outdated state; it was likely created as an accidental duplicate entry.

### Recommended Actions

- **Merge** all historical transactions from Record B into Record A to preserve audit trail completeness.
- **Inactivate/archive** Record B with a cross-reference note pointing to Record A's ID.
- **Standardize** the name to the legal name on the EIN registration (verify via IRS CP-575 or W-9 on file).
- **Root-cause** how the duplicate was created (e.g., manual re-entry vs. system migration) and implement a **TIN-based duplicate check** at vendor onboarding to prevent recurrence.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies the records as duplicates via TIN normalization (noting same EIN with different formatting) and selects Record A as the canonical survivor with sound reasoning (recency, completeness). It mentions merging historical transactions and inactivating B with cross-reference. However, it misses two key control steps: (1) explicit migration of open POs/invoices from B to A before deactivation, and (2) the duplicate-payment lookback check across both record IDs for the past 18 months. The 'merge historical transactions' language is about audit trail preservation, not the AP control of detecting duplicate payments that may have already occurred.

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

- **0**: Says they are not duplicates, or fails to identify the TIN match, or recommends keeping both records active
- **1**: Identifies them as duplicates but misses the TIN-normalization reasoning, the dup-payment check, or the open-document migration step
- **2**: Identifies the duplicate via TIN normalization, picks the correct survivor with reasoning, and includes both the open-document migration and duplicate-payment lookback as control steps

### Ideal answer

Yes, these are duplicates. The TINs are identical — '12-3456789' and '123456789' are the same nine-digit EIN; the hyphen is a display convention only and TIN normalization (strip non-digits) is the correct primary-key match. Name variance ('Corp' vs. 'CORPORATION', case) is a normalization issue, not a different entity. Same bank account (Chase ****4521) is a strong corroborating signal. Address differs only in 'St' vs. 'Street' and the absent suite line on B — same street address.

Resolution: merge under a single canonical record. Survivor selection: keep Record A (active, recent activity, more complete address). Deactivate Record B with a cross-reference to A so historical AP/spend reporting still rolls up. Move any open POs/invoices on B to A before deactivation. Run a duplicate-payment check across both record IDs for the last 18 months as a control step (a duplicate vendor record is a known precondition for duplicate payments).

### Model response

# Analysis

## Verdict: YES, these are duplicates

## Justification

**Matching indicators:**
- **Name**: Identical entity despite formatting differences ("Corp" vs "Corporation" are standard abbreviations for the same legal entity type)
- **TIN**: 12-3456789 vs 123456789 — these are the **same Tax ID Number**. The hyphenation difference is merely formatting; the 9-digit sequence is identical
- **Address**: Same location with minor formatting variations (St vs Street, missing Suite 200 in Record B)
- **Bank**: Identical account (Chase ****4521)

The TIN match is deterministic—this is the primary identifier for a business entity and confirms these records represent the same supplier.

## Recommended Resolution

**Record A should be the surviving canonical entry.**

**Rationale:**
- **More complete information**: Includes suite number (Suite 200), providing precise location details
- **Recent activity**: Last invoice 30 days ago indicates active business relationship
- **Data quality**: More structured formatting suggests cleaner data maintenance

**Actions:**
1. Merge all historical transaction data from Record B into Record A
2. Deactivate/archive Record B with clear cross-reference noting the merge date
3. Update all downstream systems and processes to use Record A's TIN (12-3456789)
4. Investigate why Record B shows 18 months of inactivity—determine if this represents a subsidiary, alternate location, or data entry error

This approach preserves transaction history while establishing a single source of truth.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies the records as duplicates and explains TIN normalization (hyphenation is formatting, same 9-digit sequence). It picks Record A as survivor with sound reasoning. However, it misses the duplicate-payment lookback control step, which is explicitly required for a score of 2. The merge of historical data is mentioned but open POs/invoices migration is only generally implied, not explicitly called out as a pre-deactivation step.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_002 — invoice_processing · easy · **score 1/2** (model: `claude-opus-4-7`)

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

**Policy applied:** Goods → PO required; Services > $25k → PO required; Recurring utilities/statutory → PO-exempt.

| # | Vendor | Amount | Classification | Reason |
|---|--------|--------|----------------|--------|
| 1 | PG&E | $4,820 | **Non-PO** | Recurring utility — explicitly PO-exempt under policy. |
| 2 | Salesforce | $84,000 | **PO-backed (PO required)** | Service > $25k threshold; prior year was on a PO — a renewal PO must be raised before processing. |
| 3 | Latham & Watkins | $11,500 | **Non-PO** | Professional/legal services under the $25k services threshold and on retainer; process against retainer agreement, not a PO. |
| 4 | Staples | $612 | **PO-backed** | Goods purchase with a valid PO (#4500987) already referenced — 3-way match against PO and receipt. |
| 5 | BrandWorks Agency | $48,000 | **PO-backed** | Marketing services > $25k; SOW-2024-17 should be tied to a PO — process only if a PO exists, otherwise hold for PO creation. |

**Key exceptions to flag to AP:**
- **Salesforce** is the highest risk: large-dollar service renewal arriving without a PO this cycle — return to requester for PO issuance before payment.
- **BrandWorks** has an SOW but the PO linkage should be verified; SOW alone is insufficient under a PO-required policy at this dollar level.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** All five invoices are classified correctly with appropriate threshold/carve-out reasoning. The response surfaces the auto-renewal-without-PO as rogue spend concern (Salesforce flag) and notes SOW-alone insufficiency for BrandWorks. However, it misses two key nuances: (1) the after-the-fact/retroactive PO control issue is not explicitly addressed, and (2) the legal carve-out conditions (approved counsel list, matter budget, engagement letter as PO equivalent for SOX) are not mentioned — it just cites the $25k threshold, which is actually a weaker justification than the carve-out logic. This meets the bar for score 1 but not 2 (which requires at least two of the three specific control nuances).

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
| 1 | PG&E | $4,820 | **Non-PO** | Recurring utility; PO-exempt under policy |
| 2 | Salesforce | $84,000 | **PO-backed** | Annual SaaS renewal >$25k services threshold; prior year was on PO, indicating established practice |
| 3 | Latham & Watkins | $11,500 | **Non-PO** | Legal services under $25k threshold; retainer arrangements typically exempt from PO requirement |
| 4 | Staples | $612 | **PO-backed** | Goods purchase with existing PO reference (#4500987); consistent with policy requiring POs for goods |
| 5 | BrandWorks Agency | $48,000 | **PO-backed** | Services >$25k threshold; SOW-2024-17 reference confirms contractual foundation supporting PO requirement |

**Key Reasoning:** Classification follows the stated thresholds (goods always; services >$25k) with exemptions for recurring utilities and sub-threshold retainer services.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** All five invoices are classified correctly with appropriate threshold reasoning. However, the response misses the key control nuances: it does not flag auto-renewal-without-PO as potential rogue spend, does not mention after-the-fact PO control issues for the BrandWorks SOW, and does not discuss the legal engagement letter as a PO-equivalent or conditions on the legal carve-out (approved counsel list, matter budget). This fits the criteria for a 1.

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

# 3-Way Match Analysis: PO #4500-22871 × GR #50032118 × INV-88412

---

## 1. Framework: What Is Being Matched

A 3-way match validates that:
1. **PO → GR**: What was ordered was actually received
2. **PO → Invoice**: Price and terms on invoice match the PO
3. **GR → Invoice**: Invoice quantity matches what was physically received

The PO tolerance policy (±2% price, ±5% quantity) defines the **auto-approval corridor** — variances within these bands can be system-cleared; variances outside require human intervention.

---

## 2. Establishing Baselines

| Parameter | PO Baseline | Tolerance Band | Floor | Ceiling |
|---|---|---|---|---|
| Unit Price | $10.00 | ±2% | $9.80 | **$10.20** |
| Quantity | 100 units | ±5% | **95 units** | 105 units |
| Extended Amount | $1,000.00 | — | $931.00 | $1,071.00 |
| Freight | $0.00 | Not on PO | — | — |

---

## 3. Line-by-Line Variance Analysis

### Exception #1 — Quantity Variance (GR vs. PO)

| Element | Value |
|---|---|
| PO Quantity | 100 units |
| GR Quantity | 95 units |
| Variance | −5 units (−5.0%) |
| Tolerance Limit | −5% (= 95 units floor) |
| **Within Tolerance?** | ✅ **Yes — exactly at the boundary** |
| Short-Ship Notation | "Final delivery" logged by receiver |

**Analysis:** The 5% shortfall lands precisely on the outer edge of the allowable quantity tolerance. Technically passable by the control rule, but the **"final delivery" designation is a critical flag** — it transforms what might be a temporary short-ship into a permanent one. The remaining 5 units **will never arrive.** This requires a PO amendment to close the open quantity; otherwise the PO remains open and susceptible to a duplicate delivery or phantom receipt.

---

### Exception #2 — Unit Price Variance (Invoice vs. PO)

| Element | Value |
|---|---|
| PO Unit Price | $10.00 |
| Invoice Unit Price | $10.20 |
| Variance | +$0.20/unit (+2.0%) |
| Tolerance Limit | +2% (= $10.20 ceiling) |
| **Within Tolerance?** | ✅ **Yes — exactly at the boundary** |

**Analysis:** Again, the variance lands on the precise outer boundary. This is technically within policy, but the combination of a price variance AND a quantity variance — both at maximum tolerance — means the **cumulative financial impact must be evaluated**, not just each variance in isolation (see Section 5).

---

### Exception #3 — Invoice Quantity vs. GR Quantity (Critical Mismatch)

| Element | Value |
|---|---|
| Units Received (GR) | 95 units |
| Units Invoiced | 100 units |
| Variance | **+5 units overbilled** |
| Dollar Impact | +5 × $10.20 = **+$51.00** |
| **Within Tolerance?** | ❌ **No — this is a hard exception** |

**Analysis:** This is the most serious exception. The supplier invoiced for 100 units but only shipped 95 (acknowledged in their own shipment notation). **You cannot pay for goods you did not receive.** This is not a tolerance question — it is a fundamental 3-way match failure. The payable must be based on received quantity (95 units), not invoiced quantity (100 units).

---

### Exception #4 — Freight Charge Not on PO

| Element | Value |
|---|---|
| PO Freight Terms | Not stated / $0.00 |
| Invoice Freight | **$35.00** |
| Variance | +$35.00 (100% unexpected) |
| **Within Tolerance?** | ❌ **No — not covered by PO** |

**Analysis:** Freight charges require independent authorization. Without a PO line item, blanket freight authorization, or a freight agreement on file, this charge cannot be matched against any approved document. It must be separately evaluated. Common resolution paths: (a) verify against agreed Incoterms/shipping terms in the master supply agreement, (b) obtain ad hoc approval from Procurement/Finance, or (c) dispute and reject.

---

## 4. Consolidated Variance Summary Table

| # | Exception | PO Basis | Invoiced/Received | Variance | Variance % | Within Tolerance |
|---|---|---|---|---|---|---|
| 1 | Quantity Short (GR vs PO) | 100 units | 95 units received | −5 units | −5.0% | ✅ At limit |
| 2 | Unit Price Increase | $10.00 | $10.20 invoiced | +$0.20/unit | +2.0% | ✅ At limit |
| 3 | Invoice Qty > GR Qty | 95 units received | 100 units invoiced | +5 units / +$51.00 | N/A | ❌ **Hard fail** |
| 4 | Freight Not on PO | $0.00 | $35.00 | +$35.00 | N/A | ❌ **Hard fail** |

---

## 5. What Should Actually Be Paid (Recalculated)

**Working from first principles — pay for what was received at the agreed price:**

| Component | Calculation | Amount |
|---|---|---|
| Authorized unit price (within ±2% tolerance) | $10.20 × 95 units | $969.00 |
| Freight (pending approval — see below) | TBD | $0 or $35.00 |
| **Maximum payable without freight** | | **$969.00** |
| **Invoice as submitted** | | **$1,055.00** |
| **Overbilling (excl. freight question)** | | **$86.00** |
| **Overbilling (incl. freight)** | | **$51.00 qty + $35.00 freight = $86.00** |

> The supplier's invoice overstates the valid payable by **$86.00 (8.2% of invoice total)** — a material discrepancy that must be resolved before payment.

---

## 6. Exception Resolution Path

### Exception #3 (Invoice Qty > GR Qty) — **Mandatory Resolution**

| Step | Action | Role Responsible |
|---|---|---|
| 1 | Block invoice for payment in AP system | AP Clerk / System (auto-hold) |
| 2 | Issue formal debit memo or invoice dispute notice to supplier | AP Specialist |
| 3 | Request corrected invoice for 95 units @ $10.20 = $969.00 | AP Specialist → Supplier |
| 4 | Confirm no additional shipment is forthcoming (cross-ref "final delivery" notation) | Purchasing Agent / Buyer |
| 5 | If supplier disputes: escalate to Procurement Manager | Procurement Manager |
| **Control** | 3-way match system block; no payment without GR-invoice quantity reconciliation | ERP / AP Controls |

---

### Exception #4 (Freight Charge) — **Approval Required**

| Step | Action | Role Responsible |
|---|---|---|
| 1 | Research master supply agreement / purchase order for shipping terms (FOB, CIF, etc.) | Buyer / Procurement |
| 2a | *If freight is supplier's contractual responsibility (e.g., FOB Destination):* Reject charge; notify supplier | Buyer |
| 2b | *If freight terms are silent or buyer-responsible:* Obtain approval for $35.00 unplanned expense | Cost Center Manager / Finance (typically for charges ≤ approval threshold) |
| 2c | *If charge appears unreasonable:* Request freight carrier documentation | AP Specialist |
| 3 | Create separate PO line or non-PO invoice approval record | AP Specialist |
| **Control** | Segregation of duties: the person approving freight must not be the same person processing payment | Finance Controls / SOD Policy |

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The candidate identifies all four key issues (quantity short-ship with final delivery flag, price variance, invoice-vs-GR quantity mismatch, and unauthorized freight) with correct math ($86 total overbilling, 5-unit shortfall, $0.20/unit price increase, $35 freight). It explicitly flags that both the 5% quantity and 2% price variances land 'exactly at the boundary' — addressing the boundary case. However, it does not explicitly state which tolerance convention (strictly-less-than vs. less-than-or-equal) is being applied and reason consistently from that — it just calls them 'at limit' and treats them as technically passable. Role assignments (AP Clerk, Buyer, Procurement Manager, Finance) are present and segregation of duties is mentioned for freight, but there is no explicit reference to SOX three-way-match controls. The treatment of freight is appropriately conditional, not auto-payable. This fits the rubric's level 1 description: identifies all exceptions and resolution paths, addresses boundary case, but misses the explicit convention statement and SOX reference required for a 2.

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

# Three-Way Match Analysis: PO #4500-22871

## Document Comparison Matrix

| Metric | PO | GR | Invoice | Status |
|--------|----|----|---------|--------|
| **Quantity** | 100 units | 95 units | 100 units | ❌ MISMATCH |
| **Unit Price** | $10.00 | N/A | $10.20 | ❌ MISMATCH |
| **Line Amount** | $1,000.00 | N/A | $1,020.00 | ❌ MISMATCH |
| **Freight** | Not specified | N/A | $35.00 | ⚠️ UNAUTH |

---

## Exception #1: Quantity Variance

**Variance Quantification:**
- Ordered: 100 units
- Received: 95 units
- **Shortage: 5 units (5% variance)**
- **PO Tolerance: ±5% = 95–105 units acceptable range**

**Status:** ✅ **WITHIN TOLERANCE** (at lower bound)

**Resolution Path:**
- **Action:** Accept receipt as compliant
- **Approver Role:** Warehouse supervisor (routine acceptance)
- **Controls Applied:** Quantity tolerance verification
- **Process Step:** GR quantity falls within ±5% allowance; mark as "accepted with shortage notation"
- **Caveat:** Supplier notation "short ship per supplier" documents this is intentional under-delivery, not damage/loss

---

## Exception #2: Unit Price Variance

**Variance Quantification:**
- PO unit price: $10.00
- Invoice unit price: $10.20
- **Overage: $0.20/unit (2% variance)**
- **PO Tolerance: ±2% price = $9.80–$10.20 acceptable range**

**Status:** ✅ **WITHIN TOLERANCE** (at upper bound)

**Resolution Path:**
- **Action:** Accept invoice price as compliant
- **Approver Role:** Accounts Payable (AP) supervisor
- **Controls Applied:** Price variance tolerance verification
- **Process Step:** Unit price of $10.20 falls within ±2% allowance
- **Justification:** Likely market adjustment or freight pass-through (requires verification)

---

## Exception #3: Freight Charge (Unauthorized)

**Variance Quantification:**
- PO freight specification: Not stated
- Invoice freight: $35.00
- **Impact: $35.00 unplanned cost**

**Status:** ❌ **NOT WITHIN SCOPE**

**Resolution Path:**

| Step | Action | Owner | Decision Point |
|------|--------|-------|-----------------|
| 1 | Review PO freight terms | AP Analyst | Does PO say "freight prepaid," "freight collect," or "FOB"? |
| 2 | Verify supplier agreement | Procurement | Is $35 freight authorized in blanket/master agreement? |
| 3 | Hold payment pending verification | AP Controller | Flag for 3-way match exception report |
| 4a | **If authorized:** Approve and code to PO | AP Supervisor | Process full invoice $1,055.00 |
| 4b | **If unauthorized:** Reject or negotiate | Procurement Manager | Request credit memo or clarification |

**Approval Hierarchy Required (Exception):**
1. AP Supervisor (initial determination)
2. Procurement Manager (supplier communication)
3. AP Controller (payment authorization if resolved)

---

## Exception #4: Invoice Total Variance

**Calculated Amounts:**
- **PO-based expected:** 95 units × $10.00 = $950.00 *(adjusted for actual receipt)*
- **Invoice claims:** 95 units × $10.20 = $969.00 + $35.00 freight = **$1,004.00** *(if freight authorized)*
- **Variance: $54.00 to invoice total**

**Breakdown:**
- Quantity adjustment impact: −$50.00 (5 units × $10.00)
- Price variance impact: +$19.00 (95 units × $0.20)
- Freight impact: +$35.00 *(pending approval)*

---

## Summary: Match Result & Payment Authorization

| Exception | Variance | Tolerance | Approval Required | Recommendation |
|-----------|----------|-----------|-------------------|-----------------|
| Quantity | 5 units (5%) | ±5% | Warehouse Supervisor | ✅ ACCEPT |
| Price | $0.20/unit (2%) | ±2% | AP Supervisor | ✅ ACCEPT |
| Freight | $35.00 | Not specified | Procurement + AP Controller | ⏸️ **HOLD** |

---

## Final Payment Recommendation

**Scenario A: Freight Authorized**
- **Payable Amount:** $1,004.00 (95 units × $10.20 + $35.00 freight)
- **Approval Chain:** Warehouse Supervisor → AP Supervisor → AP Controller
- **Payment Terms:** Net 30 from invoice date

**Scenario B: Freight Not Authorized**
- **Payable Amount:** $969.00 (95 units × $10.20)
- **Action Required:** Request credit memo for $35.00 before payment
- **Approval Chain:** Procurement Manager → AP Controller
- **Hold Status:** Three-way match incomplete until freight resolved

**Controls Applied Throughout:**
- Tolerance band verification (quantity, price)
- Authorization matrix (freight)
- Invoice-to-GR-to-PO cross-reference
- Variance exception escalation

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The candidate identifies all three exceptions (quantity, price, freight) with correct variance math (5 units/5%, $0.20/2%, $35 freight). However, it fails to explicitly address the boundary case convention (< vs ≤) — it simply asserts both quantity and price are 'within tolerance' without flagging that they sit exactly at the boundary or noting the convention being applied. More critically, it recommends paying for 100 units at $10.20 (Scenario A: $1,004 based on 95 units, but elsewhere implies accepting the full invoice) — yet the invoice bills 100 units when only 95 were received against a final-delivery GR, which means the supplier is over-billing for unshipped units regardless of tolerance. The candidate treats the quantity variance as routine 'accept with shortage' rather than recognizing the invoice itself over-bills. It also does not reference SOX three-way-match controls or segregation of duties explicitly, though it does assign roles. This fits rubric level 1: identifies exceptions and basic resolution but misses boundary-case flagging and SOX/SoD framing.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_005 — trade_and_tax · medium · **score 1/2** (model: `claude-haiku-4-5`)

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

## FCA (Free Carrier) Rule Summary
Under FCA Hamburg, the seller's obligation is to deliver goods to a **named place (Hamburg terminal)** with goods placed at the disposal of the buyer's carrier, cleared for export. The critical threshold: **seller pays costs up to and including export clearance; buyer pays from that point onward**.

---

## Line-by-Line Assessment

| Line Item | Amount | Decision | Reasoning |
|-----------|--------|----------|-----------|
| **Components** | €50,000 | ✅ ACCEPT | Core goods covered by PO |
| **Inland freight (Stuttgart → Hamburg)** | €1,200 | ✅ ACCEPT | Seller's responsibility to move goods to named place (Incoterms 2020, A4: "The seller must contract for carriage on usual terms") |
| **Export customs clearance** | €350 | ✅ ACCEPT | Explicitly seller's obligation under FCA A6: seller must "clear the goods for export" |
| **Loading/handling at Hamburg terminal** | €180 | ⚠️ **REJECT** | **Boundary issue.** FCA requires goods delivered to "named place" with seller bearing costs "up to and including" export clearance (A4). Terminal handling *after* export clearance is completed is the buyer's responsibility. This should be the buyer's freight forwarder's cost. |
| **Marine cargo insurance** | €420 | ❌ **REJECT** | Clearly buyer's responsibility. FCA is an Incoterms 2020 "departure term" where risk transfers to buyer upon placement at the named place (A5). Insurance for shipment Hamburg → New York is entirely buyer's obligation. |

---

## Recommended Action

**Accept:**  €51,550 (Components + inland freight + export clearance)

**Push back:**  €600 (Terminal handling + marine insurance)

### Specific Pushback Language:
- **Terminal handling (€180):** "Under FCA Hamburg, the seller's obligation ends upon placement of goods at the named place with export clearance completed. Terminal handling after this point is the buyer's freight forwarder responsibility."
- **Marine cargo insurance (€420):** "Insurance for carriage Hamburg → New York is explicitly a buyer obligation under FCA Incoterms 2020. The seller cannot bundle this cost into the invoice."

---

## Reference
**Incoterms 2020 FCA (Seller's obligations):**
- **A4:** Carriage and costs to named place
- **A5:** Risk passes to buyer upon placement at named place
- **A6:** Seller bears export clearance costs

### Grader verdict

- **Score:** 1
- **Confidence:** medium
- **Reasoning:** The candidate correctly identifies that components are accepted and correctly rejects marine insurance with proper FCA reasoning. However, it accepts inland freight (€1,200) and export clearance (€350) as separate billable lines, when the ideal answer rejects these as already embedded in the FCA price (or at minimum flags them as double-charging). The candidate gets the obligation correct (seller bears these costs) but misses that this means they shouldn't be separately on-billed beyond the PO price. Terminal handling is rejected outright rather than flagged as ambiguous (depends on receipt vs. loading side). Incoterms 2020 FCA is cited explicitly. This is a mixed result — partially correct but with a significant error on the freight/clearance lines being separately billable.

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

## Place of Supply Rule – Critical Issue

Under **VATDIR Article 44(1)**, for B2B services, the place of supply is **where the customer is established**. For a US company, this means the place of supply is **outside the EU**.

### Application to This Engagement

| Factor | Assessment |
|--------|------------|
| **Service nature** | Consulting (B2B service) |
| **Customer establishment** | US headquarters (not Germany) |
| **Performance location** | Germany (irrelevant per Article 44) |
| **Existing DE VAT ID** | Unrelated to this engagement; doesn't establish EU PE |
| **Correct POS** | **United States** |

## VAT Treatment: INCORRECT

**The German VAT of €7,600 is incorrectly charged.**

Since the place of supply is the US (outside the EU), the correct treatment is:

### What Should Happen
- **Invoice should show:** €40,000 net with **zero VAT**
- **Reason:** The reverse-charge mechanism does not apply because the customer is outside the EU; instead, **exemption from VAT applies** under Article 44(1)
- **Supplier's position:** No VAT collection obligation; no supply to the German VAT territory

---

## VAT Reclaim Analysis

**Is the €7,600 reclaimable?**

| Jurisdiction | Reclaimability |
|---|---|
| **Germany** | ❌ **NO** – VAT was incorrectly charged; German authorities should not have it |
| **US** | ❌ **NO** – US does not apply VAT; input tax credit unavailable |
| **Overall** | The buyer bears unrecoverable cost |

**Even if the buyer had a valid German VAT registration**, Article 168 VATDIR restricts input tax credit to VAT on supplies for taxable activities *within the VAT territory*. Since this service is for the US headquarters and is not used for taxable EU activities, it would likely fail the use test.

---

## What AP Should Do

### Immediate Actions:
1. **Request a corrected invoice** showing €40,000 with 0% VAT, €47,600 total
   - Cite Article 44(1) VATDIR (place of supply where customer established)
   
2. **Document the position:**
   - Email confirming US establishment as principal place of business
   - Explain that the unrelated DE VAT ID does not create a PE or establish EU establishment for this engagement

3. **If supplier resists:**
   - Notify the German supplier of their VAT compliance obligation: they should file a VAT return showing this as a supply outside the VAT territory (reverse-charge or exemption, depending on how German law implements Article 44)
   - Consider escalating to German tax authority (Bundeszentralamt für Steuern) if formal correction is refused

### Accounting Treatment:
- **Do not claim input VAT** on the current invoice
- Once corrected invoice is received, expense the full €40,000 as a deductible consulting fee (no embedded VAT)

---

## Summary

| Element | Conclusion |
|---------|-----------|
| **VAT correctly charged?** | ❌ No |
| **Correct VAT rate** | 0% (supply outside EU) |
| **Reclaimable?** | ❌ No – incorrectly levied |
| **Required action** | Obtain corrected invoice |

The supplier has misapplied German VAT law by ignoring the Article 44(1) place-of-supply rule for B2B services.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly identifies that VAT should not have been charged based on Article 44 place-of-supply rules, correctly notes the US establishment is the recipient, and correctly states the VAT is not reclaimable. However, it does not cite or invoke Article 22 of Implementing Regulation 282/2011 regarding the buyer's obligation to confirm which establishment receives the service - a key rubric requirement. It also somewhat muddles the distinction between out-of-scope and exemption/reverse-charge ('exemption from VAT applies under Article 44(1)' is incorrect terminology; it's out-of-scope, not exempt). It does not clearly address the 13th Directive refund path as the fallback. These omissions match the level-1 criteria.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_008 — close_and_controls · hard · **score 1/2** (model: `claude-haiku-4-5`)

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

# Accrual Accounting for Services PO #4500-77002

## Analysis Summary

This is a **classic accrual scenario**: services are performed (evidenced by vendor status report) but not yet invoiced. You must record an accrual at month-end to match revenue/expense in the period services are delivered, per accrual accounting principles.

---

## Month-End (2026-03-31) Accounting

### Correct Entry: Manual Accrual

Since no invoice exists, you record an **accrual for unbilled services**:

```
Debit:  Consulting Expense (or COGS)        $150,000
  Credit: Accrued Liabilities (or Accrued Expenses)        $150,000

Narrative: Accrual for Q1 strategy services delivered per vendor status 
report through PO #4500-77002
```

**Why this entry:**
- Services **delivered** ($150,000) in Q1 → recognize expense in Q1
- No invoice yet → liability is "accrued" (estimated/pending invoice)
- Deferred to April when invoice received → you'll reverse/settle this accrual

---

## SAP-Style GR/IR (Goods Receipt/Invoice Receipt) Approach

In a structured SAP/ERP environment with services PO discipline:

### At 2026-03-31:

**Option A: Service Entry Sheet (SES) / Goods Receipt**
```
Service Entry Sheet (at month-end on status report basis):
  Debit:  Consulting Expense                    $150,000
    Credit: GR/IR Clearing Account (liability)             $150,000

Narrative: Service Entry Sheet created against PO #4500-77002 
reflecting services delivered through 2026-03-31
```

This flow:
- **GR/IR Clearing (liability)** holds the accrual until invoice matches
- Keeps PO receipt logic separate from invoicing logic
- Provides **receipt evidence** before invoice arrives

### At 2026-04-12 (Invoice Receipt):

```
Debit:  GR/IR Clearing Account               $150,000
  Credit: Accounts Payable (Vendor)                      $150,000

Narrative: Invoice #[invoice#] received from Strategy Consulting Co., 
matches SES and PO #4500-77002
```

**Result:** The liability moves from GR/IR to AP (ready to pay); no expense re-posting needed.

---

## Manual Accrual Approach (Simpler Setup)

### At 2026-03-31:

```
Debit:  Consulting Expense                    $150,000
  Credit: Accrued Liabilities                             $150,000
```

### At 2026-04-12 (Invoice Receipt):

**Option 1: Reverse and rebook**
```
Debit:  Accrued Liabilities                   $150,000
  Credit: Consulting Expense                             $150,000
(Reversal)

Debit:  Consulting Expense                    $150,000
  Credit: Accounts Payable                               $150,000
(Record invoice)
```

**Option 2: Direct settlement (cleaner)**
```
Debit:  Accrued Liabilities                   $150,000
  Credit: Accounts Payable                               $150,000

(Narrative: Clear accrual by reclassifying to AP; invoice received 
and matched to accrual)
```

---

## Comparison: SAP GR/IR vs. Manual Accrual

| Aspect | **SAP GR/IR** | **Manual Accrual** |
|--------|---------------|--------------------|
| **Month-end (3/31)** | Service Entry Sheet → GR/IR Clearing | Debit Expense / Credit Accrual |
| **April Invoice** | Moves GR/IR → AP; expense locked in Q1 | Reverse accrual; rebook to AP |
| **Audit Trail** | Receipt & invoice separate; reconciliation built-in | Requires matching workpaper |
| **Complexity** | Higher; requires SES discipline | Lower; fewer transactions |
| **Control** | 3-way matching (PO, Receipt, Invoice) | 2-way (Accrual, Invoice) |
| **Best for** | Large orgs with many services POs | Smaller dollar amounts or one-offs |

---

## Final Balances

### Consolidated GL at 2026-03-31:
- **Consulting Expense:** $150,000 (Q1)
- **Liability (Accrued/GR/IR):** $150,000

### Consolidated GL at 2026-04-30 (after invoice settled):
- **Consulting Expense:** $150,000 (remained in Q1; April reversal nets to zero)
- **Accounts Payable:** $150,000 (ready for payment)
- **Accrued Liabilities/GR/IR:** $0

---

## Key Principle

**The vendor status report is sufficient evidence for accrual purposes.** You don't wait for an invoice to recognize delivered services under accrual accounting; waiting would violate the matching principle and misstate Q1 results.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response correctly accrues $150k in March and presents both the manual and SAP GR/IR paths with reasonable journal entries. However, it fails to explicitly address that the remaining $50k must NOT be accrued — this is a key rubric requirement that is entirely omitted. Additionally, it does not address GR/IR aging review or SOX segregation of duties considerations. The manual reversing entry is presented as one of two options rather than the standard auto-reverse approach, which is acceptable but slightly muddled.

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

## Executive Summary

This supplier presents **multiple, compounding red flags** that together constitute a **high-risk profile** warranting enhanced due diligence (EDD) and a strong presumption against onboarding without substantial remediation. Several indicators are individually serious; in combination they suggest potential sanctions evasion, export control circumvention, money laundering, or procurement fraud.

---

## I. Required Screening Steps

### A. Sanctions & Restricted Party Screening

| Screen | Tool/Authority | Rationale |
|---|---|---|
| OFAC SDN & Consolidated List | U.S. Treasury OFAC | Ivan Petrov (Russian-origin name, Cyprus address); Latvia bank; HK routing |
| EU Consolidated Sanctions List | EU OJ / European Commission | Cyprus and Latvia are EU member states; EU sanctions on Russia apply |
| UN Security Council List | UN Sanctions Committee | Base-level check for all counterparties |
| UK OFSI List | HM Treasury | If any UK nexus exists |
| BIS Entity List, Denied Persons List, Unverified List | U.S. Commerce/BIS | Electronic components are frequently export-controlled |
| Freight forwarder screening | All above lists | Unknown forwarder must itself be screened |
| INTERPOL/law enforcement databases | As available | Organized crime, fraud flags |

> **Critical note:** Screening must cover the **UBO (Ivan Petrov)**, the **LLC entity**, the **bank**, the **freight forwarder** (once identified), and any intermediate parties. Screening only the legal entity name is insufficient.

---

### B. Export Control Classification & Licensing Review

The goods listed — **microcontrollers, FPGAs, and RF components** — are among the most tightly controlled dual-use items in existence.

| Item | Likely Classification | Regime |
|---|---|---|
| Microcontrollers (high-performance) | EAR99 or ECCN 3A991/3A001 | U.S. Export Administration Regulations (EAR) |
| FPGAs | ECCN 3A001.a.7 or 3A991 depending on speed/gates | EAR; potentially ITAR if defense application |
| RF components | ECCN 3A001.b or higher; potentially USML Cat XI | EAR / ITAR |

**Key obligations triggered:**
- **EAR (15 CFR Parts 730–774):** Export licenses may be required based on ECCN, destination, and end-user. Hong Kong is no longer treated equivalently to the mainland for EAR purposes post-2020; BIS treats HK with heightened scrutiny.
- **ITAR (22 CFR Parts 120–130):** If any component has defense application, DDTC registration and licensing apply.
- **FDP Rule (Foreign Direct Product Rule):** Even if goods originate outside the U.S., if they are produced using U.S. technology/equipment, EAR may apply extraterritorially.
- **End-User/End-Use Certification:** Must be obtained and verified; a prepayment structure with an opaque freight forwarder makes verification nearly impossible at this stage.

---

### C. Anti-Money Laundering (AML) & Know Your Customer (KYC)

**Applicable regimes:**
- **U.S. Bank Secrecy Act (BSA) / FinCEN rules** — if buyer is U.S.-based or uses U.S. financial institutions
- **EU AMLD6 / local Latvian AML law** — Latvia is an FATF member but has historical vulnerabilities as a conduit for Russian capital flows; Latvian banking channels warrant heightened scrutiny
- **FATF Recommendations 10, 12, 22** — customer due diligence (CDD) and beneficial ownership verification
- **Cyprus AML law (Law 188(I)/2007 as amended)** — Cyprus is an EU member but has been identified as a jurisdiction frequently used to hold Russian-linked assets

**Required KYC steps:**
1. **Verify UBO identity** — government-issued ID, proof of address, biometric verification where possible; Petrov is a very common Russian name, and the Cyprus address must be verified (not a mailbox/nominee address)
2. **UBO ownership chain** — Delaware LLC operating agreements, member certificates; confirm Petrov's ownership percentage and control rights
3. **Source of funds / source of wealth** — mandatory for a $1M annual relationship
4. **Adverse media screening** — full name + Petrov + variants in Russian/Cyrillic; screen for PEP (Politically Exposed Person) status
5. **PEP screening** — Cyprus and Russia nexus; confirm whether Petrov holds or has held public office in Russia, Ukraine, or elsewhere
6. **Negative news / open-source intelligence (OSINT)** — litigation, enforcement actions, media reports

---

### D. Corporate Due Diligence & Entity Verification

**Steps required:**
- Obtain **Delaware Certificate of Good Standing** and **Articles of Organization** — note the entity was formed **November 4, 2025**, meaning it is **brand new** at the time of this request
- Obtain and verify **EIN/tax ID**
- Confirm **registered agent identity** — national RA services are legitimate but provide no visibility into beneficial control; this does not substitute for UBO verification
- Request **audited or reviewed financial statements** — for a $1M relationship, financial viability must be demonstrated; a brand-new LLC will have none
- Verify **physical operating address** — is there an actual business? Employees? Manufacturing or sourcing capability?
- Confirm **freight forwarder identity** — must be disclosed and screened; refusal to identify is itself a red flag

---

### E. Trade Finance & Payment Risk Review

- Review the **50% prepayment request** in context of financial controls and fraud risk
- Confirm whether payment would route through **Latvian banking system** — requires correspondent bank AML checks; Latvia has been the subject of major enforcement actions (e.g., ABLV Bank, third-party money laundering)
- Assess **invoice-to-payment documentation chain** for trade-based money laundering (TBML) indicators

---

## II. Red Flag Analysis

### 🔴 Critical Red Flags (Each Individually Disqualifying Without Explanation)

| # | Red Flag | Risk Category |
|---|---|---|
| 1 | **Newly formed entity (formed 2025-11-04)** with no operational history requesting $1M/year relationship | Fraud, Shell Company |
| 2 | **Dual-use electronic components** (microcontrollers, FPGAs, RF) — among the top categories used in sanctions evasion for military/WMD programs | Export Control, Sanctions |
| 3 | **Shipment from Hong Kong via unknown freight forwarder** — HK is a documented transshipment hub for controlled goods to Russia, China, Iran | Export Control, Sanctions Evasion |
| 4 | **UBO with Cyprus address and Russian-origin name** — Cyprus is a well-documented jurisdiction for Russian-linked beneficial ownership structures | Sanctions, AML |
| 5 | **Banking through Latvia** — Latvia has been cited repeatedly as a high-risk jurisdiction for Russian capital flows and trade-based money laundering | AML, Sanctions |
| 6 | **Unknown freight forwarder** — refusal or inability to identify logistics partners is a textbook red flag under BIS guidance | Export Control, Sanctions Evasion |

### 🟠 Significant Red Flags (Require Explanation and Documentation)

| # | Red Flag | Risk Category |
|---|---|---|
| 7 | **50% prepayment request** ("capacity reservation") on first PO of $250,000 — unusual commercially, creates buyer exposure, and may facilitate TBML | Fraud, AML |
| 8 | **Delaware formation + national registered agent** — provides no visibility into actual principals or operations; a classic opacity structure | AML, KYC |
| 9 | **No verifiable operational history** — no website, no references, no audited financials can exist for a weeks-old entity | Fraud, Due Diligence |
| 10 | **Gap between formation jurisdiction (Delaware) and UBO location (Cyprus) and banking (Latvia)** — three different jurisdictions with no natural commercial logic | AML, Sanctions |
| 11 | **$250K initial PO** below many internal review thresholds but with $1M annual projection — potential structuring to avoid enhanced review triggers | AML |

---

## III. Applicable Legal & Regulatory Regimes

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response identifies all major red flags and names most relevant regimes (OFAC, EU, UK, UN sanctions, BIS EAR/Entity List, ITAR, FCPA implicitly absent, FATF, AMLD6). However, it does not explicitly mention the OFAC 50% rule (a specific rubric requirement), does not reference the FinCEN BOI rule under the Corporate Transparency Act (31 CFR §1010.380), does not explicitly recommend an independent bank-account callback verification using contact info not from the onboarding packet, and the response appears truncated before reaching the final onboarding decision and graduated onboarding recommendation. These are specific items called out in the rubric as distinguishing a 2 from a 1.

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

# Supplier Onboarding Analysis: Pacific Trade Solutions LLC

## Red Flags Summary
This profile exhibits **multiple high-risk indicators** that warrant enhanced due diligence before approval.

### Critical Red Flags (in order of severity):

1. **Jurisdictional Inconsistencies**
   - Delaware LLC formed Nov 2025 (extremely recent)
   - UBO resident in Cyprus (EU/regulatory jurisdiction mismatch)
   - Banking through Latvia (Eastern Europe)
   - Goods shipped from Hong Kong via unknown intermediary
   - No clear explanation for this geographic fragmentation

2. **Control & Ownership Opacity**
   - Single UBO (Ivan Petrov) listed
   - No verification of beneficial ownership structure
   - Residential address rather than business address
   - Unknown if other parties have controlling interests

3. **Financial Risk**
   - 50% prepayment demand ($125,000 initial)
   - Flimsy justification ("manufacturing capacity reservation")
   - No evidence of supplier's manufacturing capability
   - $1M annual spend commitment based on unvetted entity

4. **Supply Chain Risk**
   - Electronic components (dual-use/export-controlled items)
   - Unknown freight forwarder introduces supply chain visibility gap
   - Hong Kong sourcing (proximity to restricted jurisdictions)
   - No clarity on actual manufacturing vs. trading/brokerage

5. **Entity Risk**
   - Brand new company (6+ days old at request)
   - Delaware shell characteristics (common structure for opacity)
   - Registered agent service (standard but impersonal)

---

## Applicable Legal & Regulatory Regimes

### 1. **Export Control (Primary Concern)**
   - **U.S. Export Administration Regulations (EAR)** – microcontrollers and FPGAs may fall under Category 3, 4, or 5 (semiconductors, computing)
   - **International Traffic in Arms Regulations (ITAR)** – RF components potentially controlled
   - **Office of Foreign Assets Control (OFAC)** screening required for:
     - Ivan Petrov (sanctions lists)
     - Cyprus/Limassol (Russian oligarch jurisdiction)
     - Latvia (Russian-adjacent financial flows)
   - **EU Dual-Use Regulation** – if items destined for EU resale

### 2. **Anti-Corruption & Financial Crime**
   - **Foreign Corrupt Practices Act (FCPA)** – third-party compliance required
   - **Bank Secrecy Act (BSA)** – Latvian banking requires enhanced scrutiny
   - **Know Your Customer (KYC)** / **Customer Due Diligence (CDD)** requirements

### 3. **Company Formation & Beneficial Ownership**
   - **FinCEN Beneficial Ownership Requirements** (U.S.)
   - **EU Anti-Money Laundering Directive (5AMLD)** – Cyprus entity ties
   - **Delaware Division of Corporations** filings should be reviewed

### 4. **Supply Chain Compliance**
   - **Conflict Minerals Regulation** (if components contain tin, tantalum, tungsten, gold)
   - **Dodd-Frank Section 1502** compliance
   - **Responsible Business Conduct Standards** (semiconductor industry)

### 5. **Prepayment/Payment Terms**
   - **Uniform Commercial Code (UCC)** – prepayment creates security interest issues
   - **Seller's Risk Assessment** – unusual term signals financial distress or fraud risk

---

## Recommended Screening Steps

### **Tier 1: Immediate Gatekeeping Checks** (before any engagement)

| Check | Method | Rationale |
|-------|--------|-----------|
| **OFAC/SDN List** | FinCEN, Treasury | Ivan Petrov; Russian individuals in Cyprus common in sanctions cases |
| **Denied Parties List** | BIS, Commerce Dept | Check UBO and company against Entity List, Unverified List |
| **Interpol/Criminal Records** | Police liaison if applicable | Recent entity formation + suspicious structure |
| **Corporate Filings** | Delaware Corp. database | Verify legitimacy, registered agent, ownership structure |
| **EU AML Registers** | Cyprus/Latvia authorities | Cross-reference UBO residential address |

### **Tier 2: Enhanced Due Diligence** (if Tier 1 passes)

| Check | Method | Rationale |
|-------|--------|-----------|
| **UBO Verification** | Third-party KYC provider (Dun & Bradstreet, Refinitiv, Lexis Nexis) | Confirm no hidden controlling interests; validate address |
| **Latvian Bank Verification** | Direct contact with bank | Confirm account legitimacy; assess account history |
| **Manufacturing Capability** | Site visit / Third-party audit | Verify they actually manufacture (not just brokerage) |
| **Freight Forwarder Validation** | IATA/FMC registry; audit trail | Identify intermediary; assess supply chain visibility |
| **Export Control Classification** | Company's export compliance officer or BIS commodity expert | Determine if items require licenses |
| **Supplier Financial Health** | Credit reports; tax filings (if public) | New company = no track record; assess solvency |
| **Hong Kong Sourcing Origin** | Supply chain tracing | Ensure goods not transshipped from restricted jurisdictions (North Korea, Iran, Syria) |

### **Tier 3: Legal/Contractual Protections** (if proceeding)

- **Prepayment rejection** – Request net 30/60 terms instead; prepayment only after proven relationship
- **Compliance representations** – Require certified statements on export compliance, sanctions, AML
- **Right to audit** – Include supply chain audit rights in contract
- **Escrow arrangement** – If prepayment unavoidable, escrow 50% until goods verified
- **Indemnification** – Supplier warrants no export control violations; indemnifies buyer

---

## Recommended Onboarding Decision

### **Status: REJECT PENDING ENHANCED DILIGENCE**

**Rationale:**

1. **Too many unresolved unknowns** for a new supplier requesting $250K+ upfront
2. **Geographic/jurisdictional red flags** (Cyprus UBO + Latvia banking + Hong Kong shipping) suggest intentional obfuscation
3. **Export control exposure** (electronic components) requires documented compliance before engagement
4. **Zero track record** with a freshly formed entity increases fraud risk
5. **Prepayment demand is inappropriate** for an unvetted supplier

### **Conditional Path to Approval:**

If leadership insists on pursuing this supplier:

1. **HOLD all POs** until Tier 1 screening clears
2. **Conduct full Tier 2 EDD** (4–6 week timeline) with external advisors
3. **Export classification completed** by your export compliance officer (document ECCN or EAR99 status)
4. **Contract amendments** incorporating audit rights + compliance representations
5. **Prepayment terms renegotiated** to 25% on order, 50% on shipment, 25% on delivery/inspection
6. **Reduced initial PO** – Request $50K first order to test supplier quality/reliability
7. **Relationship sponsor** – Assign dedicated compliance contact for ongoing monitoring

### **If Unable to Satisfy Above Requirements: DECLINE**

The risk-reward profile is unfavorable for a commodity electronic components supplier.

---

## Key Takeaway

This supplier profile is consistent with **layering/trade finance schemes** common in sanctions evasion (Cyprus UBO, Latvian banking, Hong Kong transshipment). **Do not proceed without robust third-party verification and export compliance clearance.** The prepayment demand is a closing signal; legitimate suppliers with manufacturing capacity don't require front-loaded payment from unknown buyers.

### Grader verdict

- **Score:** 1
- **Confidence:** high
- **Reasoning:** The response identifies most major red flags (shell company, Cyprus/Latvia/HK nexus, dual-use electronics, prepayment, unknown forwarder) and names key regimes (OFAC, BIS EAR/Entity List, FinCEN BOI, FCPA, EU sanctions). It recommends rejecting prepayment, reduced initial PO, and ongoing monitoring. However, it misses the OFAC 50% rule (derivative blocking for entities ≥50% owned by SDNs), which is explicitly required for a 2 score. It also does not specify the bank-callback control using independently-obtained contact info (it says 'Direct contact with bank' but doesn't address the BEC/packet-contact risk). It doesn't explicitly cite EU/UK HMT/UN consolidated lists by name. These omissions match the rubric's level 1 criteria.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---
