# ProfBench comparison — run `1af59657-b7b7-48c1-8695-d18f27040d68`

For each question below: read the model's response next to the ideal answer, then categorize:

- **(a) model fell short** — keep the question, score is honest
- **(b) ideal_answer too narrow** — the model's response is actually acceptable; broaden the ideal answer (do not change the question)
- **(c) rubric miscalibrated** — tier definitions need to be more specific so the grader doesn't mark partial answers down unfairly

Only (b) and (c) justify editing `data/questions.json`. (a) is the benchmark working as intended.

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
- **Reasoning:** The response correctly identifies the records as duplicates, explicitly notes the TIN match with formatting normalization, picks Record A as the survivor with sound reasoning, and includes the open-document migration step. However, it does not include the duplicate-payment lookback/check as a control step, which is a required element for a score of 2.

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
- **Reasoning:** The response correctly identifies the records as duplicates via TIN normalization (noting the hyphen is formatting only) and selects Record A as the survivor with sound reasoning. It mentions consolidating transaction history, which loosely covers open-document migration. However, it does not explicitly call out a duplicate-payment lookback/check as a control step, which is a key rubric requirement for a score of 2. The open-document migration is also only weakly addressed (general 'consolidate transaction history' rather than explicit migration of open POs/invoices).

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
