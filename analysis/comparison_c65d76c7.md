# ProfBench comparison — run `c65d76c7-bf3a-4cb7-a7fb-23a92ba83b83`

For each question below: read the model's response next to the ideal answer, then categorize:

- **(a) model fell short** — keep the question, score is honest
- **(b) ideal_answer too narrow** — the model's response is actually acceptable; broaden the ideal answer (do not change the question)
- **(c) rubric miscalibrated** — tier definitions need to be more specific so the grader doesn't mark partial answers down unfairly

Only (b) and (c) justify editing `data/questions.json`. (a) is the benchmark working as intended.

---

## q_005 — trade_and_tax · medium · **score 0/2** (model: `claude-sonnet-4-6`)

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

## Governing Rule

Under **Incoterms 2020 FCA (Free Carrier) — Named Place: Hamburg Port Terminal**, the critical risk/cost division is:

> *The seller delivers when it places the goods at the disposal of the named carrier (or another nominated person) at the named place. At that point, **all costs and risks transfer to the buyer**.*

The seller's obligations are codified in **FCA A4 (Delivery)**, **A6 (Delivery/transport document)**, and **A9/A10 (Allocation of costs)**. Specifically, **FCA A9** states the seller bears all costs **until** the goods are delivered at the named place, including export clearance (**A7**).

---

## Line-by-Line Analysis

| Line | Charge | Amount | Accept or Reject? | Reasoning |
|------|--------|--------|--------------------|-----------|
| **1** | Electronic components | €50,000 | ✅ **Accept** | Core contract value per PO |
| **2** | Inland freight Stuttgart → Hamburg | €1,200 | ✅ **Accept** | Under **FCA A9(a)**, the seller bears *all costs until delivery at the named place*, including inland transport to Hamburg terminal |
| **3** | Export customs clearance fee | €350 | ✅ **Accept** | Under **FCA A7**, the seller is explicitly responsible for all export formalities and related costs |
| **4** | Loading/handling at Hamburg terminal | €180 | ⚠️ **Conditional — See note** | Depends on precise delivery point (see below) |
| **5** | Marine cargo insurance | €420 | ❌ **Reject / Push back** | Under **FCA A5**, the seller bears risk only until delivery; **FCA A3(b)** imposes *no obligation* on the seller to procure insurance — this is the buyer's election and cost |

---

## The Critical Issue: Line 4 — Loading at Terminal

This requires careful attention to the **FCA "sub-variant"** distinction in Incoterms 2020:

### Scenario A: Named Place is a *terminal/container yard* (as here)
Under **FCA A9**, if delivery occurs *at a named premises that is a carrier's terminal*, the seller delivers by loading onto the collecting vehicle. **The terminal handling/loading fee at Hamburg is therefore a seller's cost** → **Accept**.

### Scenario B: Incoterms 2020 "FCA on Board" notation
Incoterms 2020 introduced a special provision (**A6/B6 optional clause**) allowing the buyer to instruct the seller to obtain a bill of lading with an on-board notation. This does **not** shift cost liability but could affect documentation arrangements.

**Conclusion on Line 4:** Since the named place is the Hamburg port *terminal* (not the seller's premises), and delivery is to the terminal operator/carrier, the loading/handling charge at that terminal is within the seller's cost sphere under **FCA A9** → **Accept**, but the buyer should verify this charge isn't double-counting fees already embedded in Line 2.

---

## Summary Recommendation

| | Amount |
|---|---|
| **Charges buyer should accept** (Lines 1+2+3+4) | **€51,730.00** |
| **Charge buyer should reject** (Line 5 — insurance) | **€420.00** |
| **Revised invoice total buyer should pay** | **€51,730.00** |

---

## Formal Pushback Basis for Line 5

The buyer should respond to the supplier as follows:

> *"Under Incoterms 2020 FCA, Article A3(b), the seller has no obligation to procure cargo insurance, and correspondingly the buyer bears no obligation to reimburse the seller for insurance obtained on the buyer's behalf without instruction. Risk transfers to the buyer upon delivery at Hamburg terminal per A4/A5. We have arranged our own marine cargo insurance through our freight forwarder. Please issue a revised invoice removing Line 5 (€420) and confirm in writing that no insurance was procured in our name creating any duplicate coverage."*

---

## Additional Due Diligence Points

1. **Verify Line 3** — Confirm the export clearance fee is at-cost (actual customs broker invoice) and not a marked-up administrative fee, which would warrant a breakdown request.
2. **Double-check Line 4** — Request documentation (terminal receipt/handling invoice) to ensure this is a genuine third-party charge and not a seller margin item.
3. **Buyer's own costs** — Ocean freight Hamburg→New York and US import duties are correctly the buyer's responsibility under FCA, so the freight forwarder's invoice is properly addressed to the buyer.

### Grader verdict

- **Score:** 0
- **Confidence:** high
- **Reasoning:** The candidate accepts Lines 2 (inland freight) and 3 (export clearance) as separate charges to the buyer. While the candidate correctly identifies these as the seller's cost responsibility under FCA, it then incorrectly tells the buyer to PAY them as separate invoice lines rather than rejecting them as costs that should already be embedded in the PO price. This effectively gets the cost allocation backwards at the invoice level — the buyer would be double-paying for costs the seller is supposed to bear. The candidate also definitively accepts Line 4 rather than flagging the ambiguity, and only correctly handles Line 5 (insurance). This fails the rubric's level 1 threshold which requires correctly rejecting inland freight and export clearance lines.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_006 — trade_and_tax · medium · **score 0/2** (model: `claude-haiku-4-5`)

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

# W-9 Validity and Compliance Analysis

## W-9 Validity Assessment: **INVALID**

The W-9 is **not properly completed** for this entity structure. Here's why:

### Primary Issue: Incorrect Federal Classification
- **Form shows:** "Individual/sole proprietor or single-member LLC"
- **Correct classification:** This should indicate **"Single-member LLC treated as disregarded entity"** OR the owner should file as an individual
- **The problem:** Using the owner's SSN (rather than an EIN) on a W-9 for an LLC is technically acceptable *only if* the LLC is disregarded for tax purposes, but the box selection creates ambiguity about entity status

### Secondary Issue: Foreign Resident Owner
- The owner is a **Mexican resident/citizen**, which triggers additional compliance concerns:
  - The LLC is US-formed (Delaware), but beneficial ownership is foreign
  - This requires **FIRPTA** (Foreign Investment in Real Property Tax Act) consideration and **FATCA** compliance

---

## Required Forms and Documentation

### 1. **Request from Supplier:**
   - [ ] **Revised W-9** with correct box checked (or clarification of entity structure)
   - [ ] **IRS Form W-8BEN-E** (Certificate of Status of Beneficial Owner for US Withholding) – **Required because owner is a foreign resident**
     - If the LLC qualifies as a US trade/business entity, W-8BEN-E determines if FIRPTA withholding applies
   - [ ] **Attestation** of LLC structure and tax treatment election
   - [ ] **ITIN verification** – If SSN is being used, confirm it belongs to a non-resident alien

### 2. **Alternative Structure:**
   - Clarify whether the LLC has elected to be taxed as a **C Corporation** (Form 8832) – this would change withholding significantly

---

## Withholding Requirements

### **30% FIRPTA Withholding Likely Applies**

| Service Type | Withholding | Basis |
|---|---|---|
| Consulting services (non-real property related) | **30% federal backup withholding** | Foreign person providing US-source income |
| Real property consulting | **15% FIRPTA withholding** (if applicable) | IRC §1445 |

**Mechanics:**
- Withhold 30% from each payment on $50,000 = **$15,000/year**
- Report on **Form 8288** (FIRPTA withholding statement) to the IRS
- Issue **Form 1042-S** (Foreign Person's US Source Income) by March 15 of following year

### **Why Standard 1099 Withholding (24%) Doesn't Apply:**
- Foreign residents don't receive the independent contractor threshold exemption
- IRC §1441 requires withholding on US-source income to foreign persons

---

## Year-End Reporting Requirements

### **Forms to Issue:**

| Form | When | Recipient | Purpose |
|---|---|---|---|
| **Form 1099-NEC** | Jan 31 | Supplier + IRS Copy B | Report gross consulting fees ($50,000) |
| **Form 1042-S** | March 15 | Foreign recipient + IRS | Report US-source income subject to withholding and amounts withheld (30% = $15,000) |
| **Form 8288** | Annual filing | IRS | Summary of FIRPTA withholding |

### **Key Reporting Points:**
- Report **$50,000 as independent contractor income** on 1099-NEC (Box 1 - NEC income)
- Report **$15,000 as withheld** (shown on 1042-S, not reducible on 1099-NEC)
- Supplier may claim **foreign tax credit** or **treaty benefits** on their Mexico tax return

---

## Practical Recommendations

1. **Do not process payments without valid W-9/W-8BEN-E** combination
2. **Set up 30% withholding reserve** in AP system immediately
3. **Require W-8BEN-E certification** – without it, default to **maximum withholding (37-39%)**
4. **Consult tax counsel** – verify if a tax treaty between US-Mexico reduces withholding (Treaty rate is typically 15% for independent personal services)
5. **Document FIRPTA analysis** – maintain evidence of withholding decision in your supplier file

---

## Summary Table

| Element | Status/Amount |
|---|---|
| **W-9 Validity** | Invalid – incorrect classification |
| **Required Forms** | W-9 (corrected) + W-8BEN-E |
| **Withholding Rate** | 30% federal backup withholding (potentially 15% if treaty applies) |
| **Annual Withholding** | ~$15,000 on $50,000 (treaty could reduce to ~$7,500) |
| **Year-End Forms** | 1099-NEC, 1042-S, Form 8288 |

**Critical action:** Do not proceed with payments until W-8BEN-E is obtained and treaty analysis is completed.

### Grader verdict

- **Score:** 0
- **Confidence:** high
- **Reasoning:** The response incorrectly recommends issuing a Form 1099-NEC alongside the 1042-S, which is wrong—1099 reporting does not apply to foreign persons. It also requests W-8BEN-E (for entities) instead of W-8BEN (for the individual NRA owner), missing the disregarded-entity rule that the owner personally is the relevant tax person. It improperly invokes FIRPTA (which applies to real property, not consulting services) and Form 8288. It mischaracterizes the 30% as 'backup withholding' and fails to split US-source vs. foreign-source income based on where services are performed (treats all $50k as US-source). The treaty/PE analysis is superficial. The explicit recommendation to issue a 1099-NEC to a foreign person triggers the 0 criterion.

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
- **1**: Identifies all three exceptions and the basic resolution but misses tolerance-edge nuance, role segregation, or treats freight as automatically payable
- **2**: Identifies all three exceptions with correct math, addresses each through the proper role (AP / buyer / receiver), and references SOX three-way-match control and segregation of duties

### Ideal answer

Three exceptions:

1. Quantity variance — invoice 100 units vs. GR 95 units = 5-unit / 5.00% variance. The GR is marked final delivery, so the missing 5 units will not be received. The invoice over-bills by 5 units × $10.00 = $50.00. Tolerance is ±5% on quantity, so 5.00% is at the edge — most systems treat 5.00% as out of tolerance (tolerance is typically applied as 'less than'). Treat as exception.

2. Price variance — $10.20 vs. PO $10.00 = $0.20 / 2.00% variance. Tolerance ±2%, again at the edge. Treat as exception. Over-bill at PO quantity = 100 × $0.20 = $20.00.

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
- **Reasoning:** The candidate identifies all three core exceptions (quantity, price, freight) with correct math and provides a thorough resolution path with role assignments (AP Clerk, AP Specialist, Buyer, Procurement Manager, Cost Center Manager). However, it explicitly treats the 5% quantity and 2% price variances as 'within tolerance — at the boundary,' which contradicts the ideal answer's tolerance-edge nuance (typically 'less than' so 5.00% and 2.00% are out of tolerance). While the candidate still flags them as needing attention and correctly identifies the GR-vs-invoice mismatch as a hard fail, it misses the tolerance-edge interpretation. Additionally, while segregation of duties is mentioned for freight, there is no explicit reference to SOX P2P three-way-match control testing. This aligns with the rubric's level 1: identifies all three exceptions and resolution but misses tolerance-edge nuance.

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
- **1**: Identifies all three exceptions and the basic resolution but misses tolerance-edge nuance, role segregation, or treats freight as automatically payable
- **2**: Identifies all three exceptions with correct math, addresses each through the proper role (AP / buyer / receiver), and references SOX three-way-match control and segregation of duties

### Ideal answer

Three exceptions:

1. Quantity variance — invoice 100 units vs. GR 95 units = 5-unit / 5.00% variance. The GR is marked final delivery, so the missing 5 units will not be received. The invoice over-bills by 5 units × $10.00 = $50.00. Tolerance is ±5% on quantity, so 5.00% is at the edge — most systems treat 5.00% as out of tolerance (tolerance is typically applied as 'less than'). Treat as exception.

2. Price variance — $10.20 vs. PO $10.00 = $0.20 / 2.00% variance. Tolerance ±2%, again at the edge. Treat as exception. Over-bill at PO quantity = 100 × $0.20 = $20.00.

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
- **Reasoning:** The candidate identifies all three exceptions (quantity, price, freight) and provides reasonable resolution paths including holding payment pending freight resolution. However, it misses the tolerance-edge nuance — treating both the 5% quantity and 2% price variances as WITHIN tolerance and recommending acceptance, when the ideal answer treats these edge cases as out of tolerance exceptions. Additionally, the candidate critically fails to recognize that the invoice bills for 100 units when only 95 were received (final delivery), recommending payment for 95 units × $10.20 rather than flagging the over-billing as a clear exception requiring a corrected invoice or credit memo. The SOX three-way match control and segregation of duties are not explicitly referenced, though some role separation is implied. Math is largely correct but the conclusions miss key nuances.

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

## q_002 — invoice_processing · easy · **score 2/2** (model: `claude-sonnet-4-6`)

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

# Invoice Classification: PO-Backed vs. Non-PO

| # | Vendor | Amount | Classification | Reason |
|---|--------|--------|----------------|--------|
| 1 | PG&E | $4,820 | **Non-PO** | Recurring utility invoice; explicitly exempt from PO requirements under standard policy. |
| 2 | Salesforce | $84,000 | **PO-Backed** ⚠️ | Services engagement exceeding $25k threshold; prior-year PO precedent confirms PO is required — **needs a current-year PO before payment**. |
| 3 | Latham & Watkins | $11,500 | **Non-PO** | Legal services on retainer fall below the $25k services threshold; however, **flag for SOW/engagement letter verification** given no SOW is referenced. |
| 4 | Staples | $612 | **PO-Backed** | Goods purchase with an explicit PO reference (#4500987); route for standard 3-way match (PO → receipt → invoice). |
| 5 | BrandWorks Agency | $48,000 | **PO-Backed** | Services engagement exceeding $25k with a referenced SOW (SOW-2024-17); verify a matching PO is tied to that SOW before approving. |

---

## Key Processing Notes

- **Invoice #2 (Salesforce):** The highest-risk item. It is above threshold and has *no current PO cited* — payment should be **held** until a PO is issued or a retroactive PO is approved by Finance.
- **Invoice #3 (Latham & Watkins):** Passes the dollar threshold, but the absence of an SOW reference warrants a **secondary approval** from Legal/Finance to confirm scope and authorization before release.
- **Invoice #5 (BrandWorks):** SOW exists, which is positive — AP should confirm a PO was raised against SOW-2024-17 and perform a **2-way match** (PO + invoice, since deliverables-based services typically lack a goods receipt).

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** All five invoices are classified correctly. The response surfaces multiple control nuances: (1) Salesforce auto-renewal without current PO flagged as needing hold/remediation (rogue spend concept), (2) explicit mention of retroactive PO concern requiring Finance approval, and (3) flags the legal invoice for SOW/engagement letter verification. Minor weakness: doesn't explicitly frame engagement letter as PO-equivalent or mention approved counsel list, but it does raise the engagement letter verification point. Meets the bar for two+ control nuances.

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
- **1**: Identifies all three exceptions and the basic resolution but misses tolerance-edge nuance, role segregation, or treats freight as automatically payable
- **2**: Identifies all three exceptions with correct math, addresses each through the proper role (AP / buyer / receiver), and references SOX three-way-match control and segregation of duties

### Ideal answer

Three exceptions:

1. Quantity variance — invoice 100 units vs. GR 95 units = 5-unit / 5.00% variance. The GR is marked final delivery, so the missing 5 units will not be received. The invoice over-bills by 5 units × $10.00 = $50.00. Tolerance is ±5% on quantity, so 5.00% is at the edge — most systems treat 5.00% as out of tolerance (tolerance is typically applied as 'less than'). Treat as exception.

2. Price variance — $10.20 vs. PO $10.00 = $0.20 / 2.00% variance. Tolerance ±2%, again at the edge. Treat as exception. Over-bill at PO quantity = 100 × $0.20 = $20.00.

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

## Step 1: Establish the Three Documents and Their Anchor Values

| Element | PO | GR | Invoice |
|---|---|---|---|
| Quantity | 100 | 95 (final) | 100 |
| Unit price | $10.00 | n/a | $10.20 |
| Extended | $1,000.00 | — | $1,020.00 |
| Freight | not on PO | — | $35.00 |
| Total | $1,000.00 | — | $1,055.00 |

The 3-way match compares **PO ↔ GR ↔ Invoice** on three axes: **quantity, price, and total**. Each axis must fall within tolerance, and the GR must support the invoiced quantity.

---

## Step 2: Walk the Match, Axis by Axis

### A. Quantity match (Invoice qty vs. GR qty)
- Invoiced: 100 units
- Received: 95 units (flagged **final delivery — short ship**)
- Variance: **5 units / 5.00% over-invoiced** relative to GR.

**Exception #1 — Quantity Block (Qty Invoiced > Qty Received).**
This is the primary failure. In SAP/Oracle terms, this triggers a **QTY block (MRBR / "M" block)**. You **cannot pay for goods not received**, regardless of PO tolerance, because the supplier has declared the delivery closed.

The PO ±5% **quantity tolerance applies to receipts vs. PO** (95 vs. 100 = 5% short, which is *within* tolerance — so the GR itself is acceptable as a closing receipt). It does **not** authorize paying for unreceived units.

### B. Price match (Invoice unit price vs. PO unit price)
- PO: $10.00
- Invoice: $10.20
- Variance: **$0.20/unit = 2.00%**

PO tolerance is **±2%**. At exactly 2.00% this is **at the boundary**. Most ERP tolerance checks are configured as "*greater than*" — so 2.00% typically passes; however, many controls frameworks treat "at tolerance" as requiring review when combined with other exceptions. Given the concurrent quantity exception, this line should not auto-release.

**Exception #2 — Price at tolerance ceiling.** Flag for buyer confirmation; do not silently absorb.

### C. Freight / unplanned costs
- PO: no freight line, no freight condition
- Invoice: $35.00 freight added

**Exception #3 — Unplanned delivery cost (UDC).** Freight was not authorized on the PO. Depending on configuration this either (a) blocks the invoice, or (b) posts to a UDC GL account pending Buyer/AP approval. Incoterms on the PO must be checked — if terms were **DDP/CIF/CPT**, freight should be **supplier-borne** and the $35 must be **rejected**. If **FOB Origin / EXW**, freight is buyer-borne and the charge is legitimate but still requires a PO change or UDC approval.

### D. Three-way totals
- Expected payable (per GR + PO price): 95 × $10.00 = **$950.00**
- Invoice ask: **$1,055.00**
- Gross overstatement: **$105.00 (11.05%)**, composed of:
  - Over-invoiced quantity: 5 × $10.20 = **$51.00**
  - Price uplift on received units: 95 × $0.20 = **$19.00**
  - Unplanned freight: **$35.00**

---

## Step 3: Resolution Path

1. **Block the invoice for payment** in the ERP (R-block for price, Q-block for quantity, and UDC flag). Net 30 clock continues to run contractually, so act promptly to preserve early-pay terms and avoid late-fee disputes.

2. **AP Clerk** issues a **price/quantity query** to the supplier and requests a **credit memo or corrected invoice** for:
   - 5 units not delivered (final delivery confirmed) → **$51.00 credit**
   - Justify or reverse the $0.20 price increase (compare to contract/price list).
   - Justify freight against PO Incoterms.

3. **Buyer / Procurement** must:
   - Confirm the **short-ship closure** with the supplier in writing and either short-close the PO or raise a PO change.
   - Decide whether to **accept the 2% price variance** (within tolerance) or push back. If accepted, document rationale.
   - If freight is legitimate, raise a **PO amendment** adding a freight line, then re-match.

4. **Receiving / Warehouse** confirms the GR is final and the 5 missing units will not arrive (already noted, but re-verify before short-closing).

5. **Approval matrix (typical SoX-aligned DoA):**
   - Variance ≤ tolerance & ≤ low-$ threshold (often <$100 or <5%): **Buyer** releases.
   - Price variance at/above tolerance OR unplanned freight: **Buyer + AP Manager**.
   - Quantity overbilling: **never auto-approved**; requires supplier credit memo — no internal approval can substitute.
   - Aggregate variance > materiality threshold (here $105 / 11%): often escalates to **Procurement Manager** and, depending on policy, **Controller** sign-off.

6. **Re-run the 3-way match** after the corrected invoice / credit memo posts. Expected clean match: 95 × $10.00 = $950.00 (plus approved freight if applicable).

---

## Step 4: Controls That Apply

| Control | Purpose | Where it fires here |
|---|---|---|
| **3-way match (PO/GR/Invoice)** | Prevent payment for goods not ordered/received | Triggers Q-block |
| **Tolerance check (price/qty)** | Auto-release low-variance items | Price at 2.00% boundary; qty within PO tol but invoice exceeds GR |
| **Unplanned delivery cost control** |

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The candidate identifies all three exceptions (quantity, price, freight), provides correct math (5 units/5%, $0.20/2%, $35 freight, with detailed breakdown of $105 overstatement), addresses tolerance-edge nuance for both price and quantity, references Incoterms for freight evaluation, assigns proper roles (AP clerk, Buyer, Receiving) with segregation, and references SOX-aligned DoA matrix and 3-way match controls. Minor quibble: the candidate interprets the 5% quantity tolerance as receipt-vs-PO rather than treating 5.00% as edge-of-tolerance for invoice matching, but correctly concludes the invoice cannot be paid for unreceived units. Overall meets the level-2 criteria.

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

# Duplicate Invoice Analysis

## Are these duplicates?

**Yes — this is almost certainly a duplicate submission.** It carries the classic "second-bite" pattern that AP teams see when a supplier (or an internal requester) re-submits a previously paid invoice with a slightly mutated invoice number.

## Signals supporting the duplicate finding

Walking through the matching dimensions an AP analyst would weigh:

| Signal | Invoice 1 | Invoice 2 | Match? |
|---|---|---|---|
| Vendor (master record) | V-44120 | V-44120 | **Exact** |
| Invoice amount | $4,287.50 | $4,287.50 | **Exact (to the cent)** |
| PO reference | 6710 | 6710 | **Exact** |
| Invoice number | NB-2024-1142 | 1142-A | **Fuzzy match** — `1142` is the numeric core of both; `-A` is a common "amended/alternate" suffix |
| Invoice date | 2026-02-08 | 2026-02-22 | 14 days apart — within typical duplicate windows (≤ 60–90 days) |
| Status | Posted & paid (ACH 2026-02-19) | Submitted, pending review | Invoice 2 was submitted **3 days after** Invoice 1 was paid — a strong "we didn't see the payment yet, please re-bill" or fraud-attempt indicator |

The combination of (same vendor) + (same PO) + (penny-exact amount) + (numeric-core invoice number match) + (close date proximity) + (the original was just paid) is the textbook duplicate-payment risk signature. There is essentially no legitimate scenario where the same PO produces two identical-amount invoices two weeks apart unless the PO covers recurring deliverables — which would normally generate distinct invoice numbers and distinct goods receipts.

## Recommended resolution

1. **Block Invoice 2 from posting** and flag it with a "Potential Duplicate of NB-2024-1142" hold.
2. **Verify the goods/services receipt (GR)** against PO 6710. If only one GR exists, Invoice 2 has no underlying delivery and must be rejected.
3. **Check the PO balance.** If PO 6710 was fully consumed by Invoice 1, Invoice 2 cannot 3-way match.
4. **Contact the supplier** in writing through the AP duplicate-dispute channel (not via the requester) to:
   - Confirm whether `1142-A` is a re-bill, credit-related, or a genuine new charge.
   - Request the original `1142-A` source document if they claim it is distinct.
5. **If the supplier confirms re-bill:** reject Invoice 2, document the disposition, and notify the supplier of the 2026-02-19 ACH remittance details.
6. **If the supplier insists it is new work:** require a separate PO line or change order, a distinct GR, and supporting evidence (BOL, signed POD, timesheet, etc.) before considering posting.
7. **Log the event** in the vendor's risk profile. Repeat occurrences from V-44120 should escalate to vendor management and potentially to fraud/internal audit, especially given the 3-day gap after payment.
8. **Do not contact the original requester first** for approval to pay — duplicate-pay schemes frequently rely on a friendly internal sponsor rubber-stamping the second invoice.

## Automated duplicate-detection rules a P2P system should run

A mature P2P / AP automation platform should run these checks at invoice ingestion (OCR/EDI/portal) **before** workflow routing:

### Tier 1 — Exact-match rules (auto-block)
1. **Same vendor + same invoice number** (case- and whitespace-normalized) → hard block. SAP's standard `BSEG`/`MIRO` duplicate check; Oracle's "Invoice Num" uniqueness; Coupa's duplicate invoice rule.
2. **Same vendor + same amount + same invoice date** → hard block.
3. **Same vendor + same PO + same amount + same invoice date** → hard block.

### Tier 2 — Fuzzy / near-match rules (route to AP review)
4. **Normalized invoice number match.** Strip non-alphanumerics, leading zeros, and common suffixes (`-A`, `-R`, `-REV`, `/2`, `COPY`, `DUP`) before comparing. `NB-2024-1142` → `20241142`; `1142-A` → `1142`. Use Levenshtein distance ≤ 2 or longest-common-substring ≥ 70% on the numeric core.
5. **Same vendor + same amount within ±$0.01 within rolling 90 days**, regardless of invoice number.
6. **Same vendor + same PO + cumulative invoiced amount would exceed PO value or remaining balance.**
7. **Same vendor + same amount + invoice number numeric core overlap** (catches the `1142` ↔ `1142-A` case explicitly — this is the rule that would have caught the example).
8. **Cross-vendor duplicate**: same bank account / remit-to + same amount + same invoice number across different vendor IDs (catches vendor-master duplication and fraud).
9. **Recently-paid invoice resubmission**: any new invoice whose fuzzy signature matches an invoice paid in the last 30–60 days → high-severity alert (this scenario).
10. **Image / OCR hash match**: perceptual hash (pHash) or PDF text-content hash equals a previously received document.

### Tier 3 — Three-way-match and downstream guards
11. **Goods receipt sufficiency**: block if invoiced quantity exceeds (received − previously invoiced).
12. **PO line over-billing tolerance**: configurable, e.g., 0% over for services, 5% for goods.
13. **Payment-already-issued lock**: a paid invoice's PO/line cannot be re-invoiced without a credit memo offset.
14. **Vendor duplicate-rate KPI**: vendors whose duplicate-flag rate

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the invoices as duplicates, cites multiple signals (vendor, amount, PO, invoice number family, timing/payment recency), provides a control-aware resolution workflow (block, verify GR, check PO balance, contact supplier through proper channel, document, escalate), and lists well over three automated detection rules including the (vendor + amount + PO + window) and fuzzy invoice-number rules that would catch this exact case.

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

| Signal | Invoice 1 | Invoice 2 | Risk Indicator |
|---|---|---|---|
| **Vendor ID** | V-44120 | V-44120 | ⚠️ Same |
| **Amount** | $4,287.50 | $4,287.50 | ⚠️ Exact match |
| **PO Reference** | 6710 | 6710 | ⚠️ Same |
| **Invoice Number** | NB-2024-1142 | 1142-A | 🔶 Variant (not exact) |
| **Invoice Date** | 2026-02-08 | 2026-02-22 | 🔶 14-day gap |
| **Payment Status** | Paid via ACH 2026-02-19 | Awaiting AP review | ✅ Catch point — #1 already paid |

**Conclusion: High-confidence duplicate.** Four of five key fields match perfectly. The only differences are a suffix added to the invoice number ("1142-A") and a later invoice date — both of which are classic patterns in deliberate or accidental re-submission of an already-paid invoice.

---

## 2. Why the Differences Don't Exonerate Invoice 2

### Invoice number variation ("1142-A")
- Suppliers sometimes append suffixes when their own system rejects a duplicate number, or when a human manually re-keys an invoice after a payment inquiry. This is a known evasion pattern, accidental or intentional.
- A P2P system that only matches on **exact** invoice number strings will miss this entirely — a critical design gap.

### 14-day date gap
- Invoice 2 was submitted **after** Invoice 1 was already paid (paid 2026-02-19; Invoice 2 dated 2026-02-22). This is the most operationally suspicious element: the supplier submitted a new invoice **three days after receiving payment.**
- A legitimate scenario where the date gap would matter is a **credit memo + rebill** situation (e.g., price correction), but in that case you would expect: (a) a credit memo for the original amount, (b) a new invoice for a different amount, and (c) explicit documentation — none of which are present here.

### Matching PO + matching amount
- PO 6710 with an exact dollar amount is the strongest combined signal. If this were a legitimate second delivery under the same PO, the PO would typically have multiple line items and the invoice would reference a specific shipment/receipt. The fact that the amount is **penny-for-penny identical** strongly suggests this is the same transaction, not a second one.

---

## 3. Recommended Resolution

### Immediate actions (in order)

1. **Place Invoice 2 on hard hold** in the AP system before it advances further in the workflow. Do not approve or schedule payment.

2. **Pull the Goods Receipt / PO receipt records** for PO 6710.
   - Confirm whether one or two deliveries/services were received.
   - If only one receipt exists matching $4,287.50, Invoice 2 is a duplicate with no underlying obligation.

3. **Contact Northbridge Logistics** (in writing, to create an audit trail) and ask them to explain the purpose of Invoice 1142-A given that NB-2024-1142 was paid in full on 2026-02-19 via ACH.
   - A legitimate supplier will provide clarification or withdraw the invoice immediately.
   - Failure to provide a clear explanation is an escalation trigger.

4. **Escalate if necessary.** If the supplier cannot justify the second invoice, escalate to:
   - AP Manager / Controller for internal sign-off on rejection
   - Procurement, to note the vendor record
   - If the pattern recurs, involve Internal Audit or Vendor Risk

5. **Document the rejection** in the vendor file. Note invoice number, date, amount, and reason for rejection so future reviewers have context.

6. **No deduction from the existing payment** is needed since Invoice 2 was caught before payment — a clean outcome.

### Secondary review
- Review vendor V-44120's full invoice history over the past 12–24 months for any other variants of this pattern (suffix-appended invoice numbers, same PO references, near-duplicate amounts). A one-time error is plausible; a pattern is a fraud signal.

---

## 4. Automated Duplicate-Detection Rules a P2P System Should Run

A robust system should run these checks **at submission time**, before any human reviewer sees the invoice. Rules should be layered — exact matches are hard blocks; fuzzy matches generate workflow flags.

### Layer 1 — Hard Blocks (automatic rejection or forced hold)

| Rule ID | Rule Description | Logic |
|---|---|---|
| **DD-01** | Exact duplicate | Same vendor ID + exact invoice number + exact amount → block |
| **DD-02** | Paid PO saturation | Invoice amount would cause PO 6710 cumulative invoiced amount to exceed PO-authorized value → block |
| **DD-03** | Receipt-to-invoice mismatch | No open/unmatched goods receipt exists on the PO for this amount → block and require 3-way match resolution |

### Layer 2 — Fuzzy Match Flags (route to senior AP reviewer)

| Rule ID | Rule Description | Logic / Threshold |
|---|---|---|
| **DD-04** | Invoice number variant | Same vendor + same amount + invoice number string similarity ≥ 80% (e.g., Levenshtein distance, suffix stripping) + same PO → flag |
| **DD-05** | Same vendor + same amount + same PO within rolling window | Regardless of invoice number, flag any invoice where vendor ID + amount + PO ref all match another invoice submitted or paid within 90 days |
| **DD-06** | Post-payment re-submission | Invoice submitted within N days *after* a payment was issued to the same vendor for the same amount under the same PO → flag with payment date context surfaced to reviewer |
| **DD-07** | Amount clustering | Multiple invoices from same vendor in same period whose amounts sum to a previously paid amount → flag (catches invoice splitting in reverse) |
| **DD-08** | Invoice date anomaly | Invoice date is earlier than a previously paid invoice from same vendor on same PO but submitted later → flag (backdating signal) |

### Layer 3 — Vendor-Level Analytics (periodic / batch)

| Rule ID | Rule Description |
|---|---|
| **DD-09** | Duplicate rate by vendor | Monthly report: vendors with >1 duplicate flag in 6 months are escalated to Vendor Risk |
| **DD-10** | Invoice number pattern analysis | Flag vendors whose invoice numbers show systematic suffix patterns (A/B/C, -1/-2, REV) at higher-than-baseline rates |
| **DD-11** | ACH timing correlation | Flag invoices submitted within 7 days of an ACH payment to the same vendor for the same amount — the "payment triggered re-submission" pattern |

### Implementation notes for the P2P team

- **Fuzzy matching (DD-04, DD-05) requires normalization first:** strip leading zeros, spaces, dashes, and common prefixes/suffixes before comparison, so "NB-2024-1142", "1142", "1142-A", and "NB1142" all resolve to a common token for matching purposes.
- **The 90-day rolling window (DD-05) is adjustable** based on your vendor payment terms; for net-30 vendors, even a 60-day window is sufficient.
- **3-way match (DD-03) is the strongest structural control** and, if enforced, would have caught this: you cannot invoice more than you have received, and a single goods receipt cannot be consumed twice.
- **Surface payment history to the AP reviewer** in the invoice workflow UI. The reviewer of Invoice 2 should immediately see, on the same screen: *"Warning: PO 6710 — Invoice NB-2024-1142 for $4,287.50 was paid via ACH on 2026-02-19."* Many duplicates succeed simply because reviewers lack visibility.

---

## Summary

These invoices are **almost certainly a duplicate.** The exact match on vendor, amount, and PO — combined with submission occurring after confirmed payment — is the defining pattern. The variant invoice number is a red flag, not an exoneration. The correct action is to hold Invoice 2, verify against receipt records, contact the supplier for written explanation, and reject with documentation. System

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** Identifies duplicate with high confidence, cites all key signals (vendor, amount, PO, invoice number family with suffix pattern, timing/14-day gap), provides a control-aware resolution workflow (hold, GR verification, supplier contact, escalation, documentation), and lists well over three automated detection rules including DD-05 (vendor + amount + PO within window) which catches this exact case.

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

| Signal | Finding | Weight | Concern Level |
|--------|---------|--------|---------------|
| **Supplier** | Identical (V-44120) | High | ✓ Match |
| **Amount** | Identical ($4,287.50) | High | ✓✓ Strong match |
| **PO Reference** | Identical (6710) | High | ✓✓ Strong match |
| **Invoice Numbers** | Different (NB-2024-1142 vs 1142-A) | Medium | ⚠ Suspicious variance |
| **Invoice Dates** | 14 days apart | Medium | ⚠ Close but distinct |
| **Processing Status** | One paid, one pending | Low | Procedural note |

## Duplicate Probability Assessment

**High probability of duplication (75-85% confidence)**

**Reasoning:**
- The identical amount + PO + supplier combination is statistically unlikely for legitimate separate transactions
- The invoice number relationship (1142 vs 1142-A) suggests resubmission rather than independent invoice
- The 14-day gap could represent either correction time or administrative delay before duplicate detection
- The suffix "-A" indicates a variant or amendment, not a new invoice

---

## Recommended Resolution

### Immediate Action
1. **Contact Northbridge Logistics** to clarify:
   - Was 1142-A intended as a replacement/correction for NB-2024-1142?
   - Did NB-2024-1142 contain an error requiring reissuance?
   - Why the different invoice numbering format?

2. **Pending Resolution:**
   - **Reject** Invoice 1142-A in AP system with hold status
   - Maintain NB-2024-1142 as the authoritative record (already paid)
   - Document the investigation in both invoice records

3. **If Confirmed Duplicate:**
   - Formal denial/reversal notice to supplier
   - Add to duplicate history for this vendor and PO
   - Investigate payment cycle (prevent duplicate ACH if not yet processed)

---

## Automated Duplicate-Detection Rules

A P2P system should implement this rules hierarchy:

### **Tier 1: Exact Match Rules (Block/High Alert)**
```
IF (Supplier = Same) AND (Amount = Exact) AND (PO = Same)
  AND (Invoice Date within 30 days)
THEN Flag: "Critical duplicate pattern"
  Action: Hold for immediate manual review
```

### **Tier 2: Variant Matching Rules (Medium Alert)**
```
IF (Supplier = Same) AND (Amount = Exact) AND (PO = Same)
  AND (Invoice # contains variant of previous invoice #)
    [e.g., contains base number + suffix like -A, -R, REV, CORR]
THEN Flag: "Likely resubmission/amendment"
  Action: Route to AP supervisor + contact supplier
```

### **Tier 3: Fuzzy Matching Rules (Monitor)**
```
IF (Supplier = Same) AND (Amount within 0-1% variance)
  AND (PO = Same) AND (Invoice Dates 5-30 days apart)
THEN Flag: "Possible duplicate with minor variance"
  Action: Analyst review (catches data entry errors, currency rounding)
```

### **Tier 4: Aging/Payment Status Logic**
```
IF (Invoice = Submitted/Pending) AND (Duplicate match exists with Status = Paid/Posted)
THEN Flag: "Earlier version already processed"
  Action: Automatic reject with explanatory message to AP queue
```

### **Vendor History Enrichment**
```
Track for each Vendor:
  - Duplicate incident rate
  - Invoice resubmission patterns
  - Days between original and resubmitted invoices
IF (Vendor duplicate rate > threshold) 
THEN Lower tolerance thresholds for future matching
```

---

## Implementation Priority

**High:** Tier 1 & 2 rules (catch this exact pattern automatically next time)
**Medium:** Tier 3 rules (financial materiality justifies complexity)
**Medium:** Tier 4 payment-status logic (prevent double payments)
**Low:** Vendor history tracking (data science enhancement)

This configuration would have automatically flagged Invoice 1142-A before AP review began.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response identifies the duplicate with high confidence, cites multiple signals (vendor, amount, PO, invoice number family with -A suffix, 14-day timing), provides a control-aware resolution path (contact supplier, hold/reject Invoice 2, maintain original as authoritative, document), and lists multiple automated detection rules including the key (vendor + amount + PO + date window) rule that would catch this exact case. Minor weakness: confidence stated as 75-85% rather than very high, but rubric requirements are met.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_005 — trade_and_tax · medium · **score 2/2** (model: `claude-opus-4-7`)

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

# Review of Supplier Invoice Against FCA Hamburg (Incoterms 2020)

## Reasoning: What FCA Hamburg Means

Under **FCA (Free Carrier) Incoterms 2020**, the seller's obligations end when the goods are delivered, cleared for export, to the carrier (or another person) nominated by the buyer **at the named place**. Because the named place here is "Hamburg port terminal" (not the seller's premises in Stuttgart), the seller's delivery point is Hamburg.

The relevant cost allocation rules are:

| Rule | Allocation | What it covers |
|------|-----------|----------------|
| **A4 / A9** (Seller) | Seller pays | Transport and all costs to bring the goods to the named place of delivery and place them at the disposal of the buyer's carrier, **not unloaded** |
| **A7 / A9** (Seller) | Seller pays | Export packaging, export clearance, export licenses, duties, taxes, and pre-shipment inspections required for export |
| **B9** (Buyer) | Buyer pays | All costs from the moment the goods are delivered (i.e., handed to the carrier at Hamburg), including main carriage, import clearance, and import duties |
| **A5 / B5** | Neither party obligated | Insurance — neither seller nor buyer has an obligation to the other to procure insurance |

Key point: When the named place is a terminal (not the seller's premises), **the seller bears all costs up to handover at that terminal**, including pre-carriage inland freight and origin terminal handling charges before the goods are placed at the buyer's carrier's disposal.

## Line-by-Line Assessment

| # | Charge | Amount | Accept / Push Back | Basis |
|---|--------|--------|-------------------|-------|
| 1 | Components | €50,000.00 | **Accept** | Goods value per PO |
| 2 | Inland freight Stuttgart → Hamburg | €1,200.00 | **Push back** — seller's cost | FCA A4: seller must transport goods to the named place (Hamburg). Pre-carriage to the named place is the seller's responsibility |
| 3 | Export customs clearance | €350.00 | **Push back** — seller's cost | FCA A7: seller carries out and pays for export clearance, including any duties, taxes, and formalities |
| 4 | Loading/handling at Hamburg terminal | €180.00 | **Judgment call — most likely push back** | FCA A2/A4: seller must place goods at buyer's carrier's disposal at the named place. Handling/loading charges incurred *to deliver* at the terminal are the seller's; charges *after* handover (e.g., loading onto the vessel) are the buyer's. As invoiced ("loading/handling at Hamburg terminal") this reads as origin THC pre-handover and should be the seller's. Clarify with seller; if it represents post-delivery vessel loading, it would be buyer's |
| 5 | Marine cargo insurance | €420.00 | **Push back** unless PO requested it | FCA A5/B5: neither party has an obligation to insure for the other. The risk transfers to the buyer at Hamburg, so this is the buyer's exposure to cover (or not). The seller cannot unilaterally bill insurance the buyer did not order |

## Correct Invoice Total

The buyer should accept only:

> **Line 1 — Components: €50,000.00**

(With possible acceptance of Line 4 only if it is confirmed to be post-delivery vessel loading, which is unusual under FCA terminal delivery.)

**Push back: €2,150.00** (Lines 2, 3, 4, 5)

## Recommended Buyer Action

1. **Reject the invoice** and request a corrected invoice for €50,000.00.
2. Cite **Incoterms 2020, FCA, articles A4 (Carriage), A7 (Export clearance), A9 (Allocation of costs), and A5/B5 (Insurance)** in the dispute note.
3. Clarify Line 4: confirm whether the "loading/handling" occurred before or after the goods were placed at the disposal of the buyer's nominated carrier. Pre-handover = seller; post-handover = buyer.
4. If marine insurance is desired, the buyer should arrange it directly (risk passes at Hamburg per FCA B3) — or, going forward, consider switching to **CIP Incoterms 2020** if the buyer wants the seller to procure insurance as part of the contract.
5. The forwarder's invoice (ocean freight Hamburg → NY and US import duty) is correctly the buyer's per **FCA B6 and B9** — accept that one.

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly addresses all five lines with proper FCA seller/buyer obligation reasoning, explicitly cites Incoterms 2020 FCA with specific article references (A4, A5, A7, A9, B5, B9), flags the terminal-handling ambiguity rather than guessing definitively, correctly handles insurance (A5/B5 neither party obligated), and correctly addresses the separately invoiced forwarder charges. It matches the ideal answer's structure and nuance.

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

# Analysis: Crescent Advisory LLC — W-9 Validity and Correct Documentation

## 1. Is the W-9 Valid? **No.**

A single-member LLC (SMLLC) is, by default, a **disregarded entity** for U.S. federal tax purposes. The IRS "looks through" the LLC to its owner. The W-9 instructions and Reg. §301.7701-3 require that the **owner** — not the disregarded LLC — be the relevant party for tax classification and documentation purposes.

Here, the owner is **a nonresident alien (NRA) individual** (Mexican citizen and resident). Therefore:

- A **disregarded entity wholly owned by a foreign person cannot furnish a W-9.** The W-9 instructions explicitly state that a Form W-9 may only be provided by a **U.S. person**. A foreign-owned disregarded SMLLC is treated as foreign for these purposes (and is the foreign owner for Chapter 3 withholding purposes — see Reg. §1.1441-1(b)(2)(iii)).
- The Delaware formation is irrelevant — state law formation does not make the owner a U.S. person.
- Checking "Individual/sole proprietor or single-member LLC" and providing the owner's SSN does not cure the defect; the underlying owner is a nonresident alien.

**Action:** Reject the W-9. Place the vendor on payment hold pending correct documentation.

## 2. Forms AP Should Request

Request the appropriate **Form W-8** from the **foreign owner** (not from the LLC):

- **Form W-8BEN** — "Certificate of Foreign Status of Beneficial Owner for United States Tax Withholding (Individuals)," completed in the name of **Mr. A. Vasquez**, the beneficial owner.
  - Part I, Line 3: enter the disregarded entity's name (Crescent Advisory LLC) only if relevant for account identification; the beneficial owner is the individual.
  - Line 5: SSN or ITIN if he has one; otherwise a foreign TIN (Mexican RFC).
  - Part II: to claim **U.S.–Mexico Income Tax Treaty** benefits (relevant for the portion of income that is *not* U.S.-source ECI — generally not applicable to personal services performed in the U.S., but may apply under the Independent Personal Services / Business Profits articles if there is no U.S. permanent establishment / fixed base; analyze carefully).
- **Form 8233** — required *instead of* W-8BEN to claim a **treaty exemption from withholding on personal services income** that is effectively connected (compensation for independent personal services performed in the U.S.). An ITIN is required for Form 8233.
- If Vasquez claims any income is **effectively connected with a U.S. trade or business** (ECI) and not exempt by treaty, the proper form is **Form W-8ECI** (requires a U.S. TIN/ITIN).

Practical posture: Because ~60% of services are physically performed in the U.S., the default characterization for that portion is **U.S.-source personal services income**, likely **ECI**. The 40% performed in Mexico is **foreign-source** and not subject to U.S. withholding or 1042-S reporting at all.

## 3. Withholding Analysis

**Sourcing rule (IRC §861(a)(3) / §862):** Compensation for personal services is sourced where the services are *performed*.
- 60% performed in U.S. → **U.S.-source** (~$30,000)
- 40% performed in Mexico → **foreign-source** (~$20,000) — **no U.S. withholding, no U.S. reporting**

**Withholding on the U.S.-source portion (~$30,000):**

| Scenario | Form on file | Withholding |
|---|---|---|
| No valid W-8/8233 | None / invalid W-9 | **30% Chapter 3 withholding** under §1441; or **24% backup withholding** if treated as U.S. payee — but for an NRA the correct treatment is 30% NRA withholding |
| W-8ECI provided (claims ECI, has ITIN) | W-8ECI | **0% withholding**, but payer reports on 1042-S; payee files Form 1040-NR and pays tax at graduated rates |
| Form 8233 + treaty claim (Independent Personal Services / Business Profits, U.S.-Mexico treaty Art. 14 — now generally folded into Business Profits Art. 7 post-2003 protocol) | 8233 + ITIN, IRS 10-day review period | **0% withholding** if treaty conditions met (no U.S. fixed base/PE; presence < 183 days, etc.) |
| W-8BEN claiming treaty (only for non-ECI categories) | Generally not applicable to active services | n/a here |

**Important caveat on 8233/treaty:** The U.S.–Mexico treaty exempts independent personal services / business profits only if the NRA has **no fixed base/permanent establishment in the U.S.** Performing 60% of work at client U.S. offices over a recurring annual engagement could create a **fixed base** or PE, potentially defeating the exemption. Tax should review.

**Until valid documentation is received: withhold 30% on each payment attributable to U.S.-performed services.**

## 4. Year-End Reporting

- **Form 1099-NEC: Do NOT issue.** 1099-NEC is for U.S. persons only. Issuing a 1099 to an NRA is incorrect and signals to the IRS that the payer treated the vendor as a U.S. person.
- **Form 1042-S** — required for each NRA payee, reporting:
  - U.S.-source income paid (the ~$30,000 portion),
  - Income code (e.g., **Code 17** – Independent personal services, or **Code 16** if dependent; Code 17 typical here),
  - Tax withheld (30%, 0% with W-8ECI, or 0% with valid 8233/treaty),
  - Exemption code if applicable (e.g., 04 – exempt under tax treaty).
- **Form 1042** — annual with

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the disregarded-entity rule (Reg. §301.7701-3 and §1.1441-1(b)(2)(iii)), rejects the W-9, requests W-8BEN (and appropriately discusses 8233/W-8ECI alternatives), correctly splits US-source vs. foreign-source based on where services are performed (60/40 = $30k/$20k), addresses the 30% default withholding under §1441, discusses the US-Mexico treaty and PE/fixed base considerations, and correctly identifies 1042/1042-S as the year-end reporting (not 1099). The answer actually exceeds the ideal by addressing Form 8233 for personal services treaty claims, which is technically more accurate than W-8BEN for ECI personal services.

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

# Tax & Compliance Analysis: Crescent Advisory LLC

---

## 1. Is the W-9 Valid?

**No — the W-9 is invalid and must be rejected.** Multiple defects make it inappropriate for this payee:

| Issue | Why It's a Problem |
|---|---|
| **Wrong form entirely** | A W-9 is a U.S. person certification. The owner is a **non-U.S. person** (Mexican citizen/resident); the entity should be treated as foreign for withholding purposes. |
| **Wrong TIN type** | Owner's SSN was provided for an LLC, not an EIN. Even if this were a U.S. payee situation, best practice is an EIN for business payments. More critically, an SSN belonging to a non-resident alien cannot establish U.S. person status for the LLC. |
| **Federal classification mismatch** | "Individual/sole proprietor or single-member LLC" box checked, but no U.S. person status can be certified given the owner's status. |
| **Entity status misrepresentation** | A single-member LLC owned by a foreign person is treated as a **foreign entity (a disregarded entity whose owner is foreign)**, not a U.S. person for withholding purposes under Treas. Reg. §1.1441-2 and IRS guidance. |

> **Key rule:** Per IRS regulations, a single-member LLC that is disregarded as an entity is treated as the same person as its owner for withholding purposes. Because the owner is a **nonresident alien (NRA)**, the LLC is treated as a foreign person — making W-8 series forms, not W-9, the correct documentation.

---

## 2. Correct Forms AP Should Request

### Primary Form: **W-8BEN** *(not W-8BEN-E)*

Because the LLC is disregarded and treated as its foreign individual owner:

- **Form W-8BEN** (Certificate of Foreign Status of Beneficial Owner for Individuals) should be completed **by Mr. Vasquez personally** as the beneficial owner.
- The form should reflect:
  - His name (not the LLC name — or LLC name with notation of disregarded status)
  - Country of citizenship/residence: **Mexico**
  - Chapter 3 status: **Individual**
  - Treaty claim, if applicable (see Section 4 below)

> *Practical note:* Some withholding agents request the LLC name on Line 1 and the owner's name on Line 2 (disregarded entity line), which is technically the correct W-8BEN structure per IRS instructions updated in recent years. AP should follow the current W-8BEN instructions carefully.

### Supporting Documentation to Collect Alongside W-8BEN:

| Document | Purpose |
|---|---|
| **Foreign TIN** (Mexican RFC number) | Required on W-8BEN if claiming treaty benefits; increasingly required regardless |
| **U.S. TIN (ITIN or EIN)** | Required if claiming treaty benefits on the W-8BEN; AP should request Mr. Vasquez obtain an ITIN (Form W-7) or the LLC obtain an EIN if not already held |
| **Proof of foreign status / residency** | Good practice to retain in file (e.g., passport copy, Mexican tax residency certificate) |
| **W-8BEN re-certification** | Valid for 3 calendar years; AP should calendar renewal |

---

## 3. Withholding Analysis

### Step 1: Source of Income Determination

The services are **partly U.S.-sourced, partly foreign-sourced**:

| Work Location | Approximate % | Income Classification |
|---|---|---|
| Performed at U.S. client offices | ~60% | **U.S.-source income** — subject to NRA withholding rules |
| Performed remotely from Mexico | ~40% | **Foreign-source income** — generally **not** subject to U.S. withholding |

> Authority: IRC §861(a)(3) / §862(a)(3) — compensation for labor/services is sourced **where the services are physically performed**.

**U.S.-source portion = ~$30,000** (60% × $50,000)
**Foreign-source portion = ~$20,000** (40% × $50,000)

---

### Step 2: Applicable Withholding Rate (Absent Treaty)

For NRA individuals receiving U.S.-source income that is **FDAP** (Fixed, Determinable, Annual, or Periodic):

- **Statutory withholding rate = 30%** under IRC §1441
- Applied to **U.S.-source income only**: 30% × $30,000 = **$9,000 withholding**
- No withholding on the $20,000 foreign-source portion

> *Caveat:* If the services income is treated as **Effectively Connected Income (ECI)** — i.e., if Mr. Vasquez/the LLC is considered engaged in a U.S. trade or business — different rules apply (see below).

---

### Step 3: Treaty Considerations — U.S.–Mexico Tax Treaty

The **U.S.–Mexico Income Tax Treaty (1992, as amended)** is in force. Key provisions for independent personal services / business profits:

| Treaty Article | Provision | Impact |
|---|---|---|
| **Article 14** (Independent Personal Services) | Income exempt from U.S. tax if the individual does **not have a fixed base** in the U.S. and is present in the U.S. fewer than **183 days** in the tax year | Potential **full exemption** from 30% withholding if conditions met |
| **Article 7** (Business Profits) | If characterized as business profits, taxable in the U.S. only if attributable to a **permanent establishment (PE)** in the U.S. | If no PE, **no U.S. tax / no withholding** |

**If treaty exemption claimed:**
- Mr. Vasquez must complete **Part II of Form W-8BEN**, specifying:
  - Treaty country: Mexico
  - Applicable article: Article 14 (or Article 7)
  - Rate claimed: 0%
  - Must provide a **U.S. TIN (ITIN)** to claim the treaty rate on a W-8BEN (per IRC §1441(c)(1) and Treas. Reg. §1.1441-6(c))
- AP/the withholding agent may rely on the W-8BEN treaty claim **unless there's actual knowledge it's incorrect**

**Important threshold questions AP should flag for legal/tax review:**
1. Does Mr. Vasquez have a **fixed base** in the U.S. (e.g., dedicated office space at client premises)? — 60% work at client offices may be an issue
2. How many **days is he present in the U.S.**? If ≥183 days, treaty Article 14 exemption is lost
3. Does the activity rise to the level of a **U.S. trade or business** / permanent establishment?

> ⚠️ **If a fixed base or PE exists**, U.S.-source income becomes taxable in the U.S. regardless of treaty; Mr. Vasquez would need to file a U.S. tax return (Form 1040-NR). Withholding at 30% (or lower treaty rate) would still apply at payment time.

---

### Step 4: Summary Withholding Table

| Scenario | Withholding on U.S.-Source ($30K) | Withholding on Foreign-Source ($20K) |
|---|---|---|
| No treaty claim | **$9,000 (30%)** | **$0** |
| Valid treaty claim (Art. 14, no fixed base, <183 days) | **$0** | **$0** |
| Fixed base / PE exists | **$9,000 (30%)** or reduced treaty rate | **$0** |

---

## 4. Year-End Reporting Requirements

### Form 1042 and 1042-S (NOT 1099)

A W-9 triggers 1099 reporting. Because this is a foreign payee, the correct reporting regime is entirely different:

| Form | Who Files | Deadline | Purpose |
|---|---|---|---|
| **Form 1042-S** (Foreign Person's U.S. Source Income Subject to Withholding) | Withholding agent (your company) | **March 15** of following year (to both IRS and payee) | Reports U.S.-source income paid and taxes withheld for each foreign payee |

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the disregarded-entity rule, requests W-8BEN from the owner personally, properly splits US-source vs. foreign-source income based on where services are performed (60/40), addresses the 30% default withholding rate under IRC §1441, discusses the US-Mexico treaty with fixed base/PE analysis (Article 14/7), and correctly identifies Form 1042/1042-S as year-end reporting (not 1099). All rubric criteria for a score of 2 are met.

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

# Analysis

## 1. Place-of-supply analysis (B2B general rule)

Strategy consulting is a "general" B2B service, so the place of supply is determined under **Article 44 of the EU VAT Directive (2006/112/EC)**, transposed into German law in **§ 3a(2) UStG**:

> "The place of supply of services to a taxable person acting as such shall be the place where that person has established his business."

The decisive question is therefore: **where is the customer "established as a taxable person" for *this particular* supply?**

Key points from Article 44 and Implementing Regulation 282/2011 (Arts. 20–22):

- The default place of supply is the **customer's business establishment** (i.e., its head office).
- A supply is moved to a **fixed establishment** only if the service is provided to, and used by, that fixed establishment.
- A **VAT registration alone is *not* a fixed establishment.** A fixed establishment requires sufficient permanence and human/technical resources to receive and use the service (Art. 11 of Reg. 282/2011; CJEU *Welmory* C-605/12; *Berlin Chemie* C-333/20; *Cabot Plastics* C-232/22).

Applying this:

- The buyer's seat of economic activity is the **US headquarters**.
- The buyer has **no EU permanent establishment**; the German VAT number exists only for a goods-related consignment-stock registration, which is unrelated to this engagement.
- The deliverable is consumed by the US head office.

➡ **Place of supply = United States.** The supply is **outside the scope of EU VAT entirely.** Article 44 does not apply because the customer is not established in the EU; we fall under the general rule that B2B services to a non-EU business customer are taxed where the customer is established (mirrored in § 3a(2) UStG, which applies regardless of whether the customer is in or outside the EU).

The fact that the buyer quoted a German VAT ID is **irrelevant** to place of supply. A VAT ID is only evidence of taxable-person status (Art. 18 of Reg. 282/2011); it does not create a fixed establishment, and the supplier should determine where the service is actually consumed.

## 2. Conclusion on the invoice

**The €7,600 German VAT is incorrectly charged.**

Correct treatment by the supplier:
- Invoice should be **issued without German VAT** (net €40,000 only).
- Because the customer is outside the EU, this is **not** a reverse-charge transaction under Art. 196 (which only applies to EU customers). It is simply **"not subject to German VAT – place of supply outside the EU per § 3a(2) UStG"** (or equivalent wording: *"nicht steuerbare sonstige Leistung"*).
- No reverse-charge note is legally required, though many German suppliers add one as good practice when the customer is a business.

## 3. Why the VAT is *not* reclaimable as charged

This is the trap AP must recognise:

- Under **§ 15(1) UStG** and settled CJEU case law (*Genius Holding* C-342/87; *Stadeco* C-566/07), **VAT that is wrongly charged is not deductible/refundable as input VAT.** Only VAT *legally owed* can be reclaimed.
- The buyer cannot recover the €7,600 via:
  - its **German VAT return** (no input-VAT entitlement for incorrectly charged VAT, and in any event the supply does not relate to its German taxable activity), nor
  - the **13th Directive refund procedure** (US-established business; same restriction — only legally due VAT is refundable, and Germany applies a reciprocity test for US claimants which is generally **not** met for services).
- The supplier remains liable to the German tax office for the VAT shown on the invoice under **§ 14c(1) UStG** ("VAT incorrectly stated on an invoice is owed") until the invoice is corrected.

The only route to recover the €7,600 is from the **supplier**, after the supplier issues a corrected invoice and refunds the cash.

## 4. Action plan for AP

1. **Do not pay the VAT line.** Pay the net €40,000 only, or place the invoice on hold pending correction.
2. **Reject the invoice** and request a **corrected invoice (Rechnungsberichtigung)** with:
   - No VAT charged.
   - A note such as: *"Not subject to German VAT – place of supply outside the EU pursuant to § 3a(2) UStG / Art. 44 VAT Directive (customer established in the US, no EU fixed establishment)."*
   - Removal of the German VAT ID from the customer block is optional but advisable, since quoting it may have caused the supplier's confusion; alternatively keep it but make clear it does not determine the place of supply for this engagement.
3. **Document the place-of-supply analysis** (customer is US-established, German VAT registration relates to unrelated consignment stock, deliverable consumed at US HQ). Keep this on file in case the supplier or its tax authority queries it.
4. If the supplier already remitted the VAT, they will recover it from the *Finanzamt* once they issue the corrected invoice and refund the buyer (§ 14c(1) UStG correction procedure).
5. **Do not** attempt to reclaim the €7,600 via a German VAT return or 13th Directive claim — it will be denied, and would expose the buyer to penalties for a wrongful input deduction.

## 5. Bottom line

| Item | Answer |
|---|---|
| Is German VAT correctly charged? | **No.** Place of supply is the US under Art. 44 VAT Directive / § 3a(2) UStG. |
| Is the VAT reclaimable as charged? | **No** — neither via German VAT return nor 13th Directive. |
| What AP should do | Pay net only, request a corrected zero-VAT invoice citing § 3a(2) UStG, recover any VAT already paid from the supplier, not the tax authority. |

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the place of supply as the US under Article 44, distinguishes out-of-scope from reverse charge (explicitly noting Art. 196 doesn't apply to non-EU customers), recommends invoice rejection with a corrected zero-VAT invoice, and thoroughly addresses why reclaim is not the right path (citing §14c, Genius Holding, and explaining 13th Directive issues). It references Implementing Regulation 282/2011 Articles 11, 18, 20-22 including the establishment analysis. While it doesn't explicitly cite Article 22 as a formal 'establishment confirmation step' the buyer must provide, it does recommend documenting the place-of-supply analysis and addresses the substance of which establishment receives the service. The answer is arguably more thorough than the ideal on reclaim mechanics.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_007 — trade_and_tax · hard · **score 2/2** (model: `claude-sonnet-4-6`)

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

# Analysis of German VAT Treatment on This Consulting Invoice

## 1. Governing Rule: Place of Supply for B2B Services

Under **Council Directive 2006/112/EC, Article 44** (the general B2B rule), the place of supply of services rendered to a **taxable person** is:

> *the place where that person has established its business.*

The buyer is a **US-incorporated company**. Its place of establishment is the **United States**. The critical question is whether the German VAT registration changes that analysis.

---

## 2. Does the German VAT Registration Shift the Place of Supply?

This is the pivotal legal question, and the answer is **no** — with important nuance.

### The "Fixed Establishment" Test
Article 44 only redirects supply to an EU VAT registration if that registration corresponds to a **fixed establishment** (FE) that actually **receives and uses** the service. A fixed establishment requires, per **EU VAT Regulation 282/2011, Article 11**:

> *a sufficient degree of permanence and a suitable structure in terms of human and technical resources to enable it to receive and use the services.*

The buyer's German VAT number was obtained solely for a **consignment-stock arrangement** — a passive registration for goods-related compliance purposes. It carries:
- No staff in Germany
- No management in Germany
- No operational capacity to "consume" consulting services

The German VAT number is therefore a **registration-only presence**, not a fixed establishment for service-supply purposes. This is consistent with **ECJ jurisprudence** (notably *Welmory*, C-605/12; *DFDS*, C-260/95; *Planzer Luxembourg*, C-73/06), which requires substantive human and technical infrastructure, not merely a VAT number.

### Conclusion on Place of Supply
The service is consumed at the buyer's **US headquarters**, which is the sole establishment with the capacity to use strategic consulting. The place of supply under Article 44 is therefore **outside the EU** — specifically the **United States**.

---

## 3. Consequence: The Supply is Outside the Scope of EU VAT

| Criterion | Analysis |
|---|---|
| Applicable rule | Art. 44 Dir. 2006/112/EC |
| Buyer's establishment | United States |
| Does DE VAT ID create an FE? | **No** — registration only, no human/technical resources |
| Does the service relate to the DE registration/FE? | **No** — unrelated engagement, consumed in the US |
| Place of supply | **United States (outside EU)** |
| German VAT due? | **No** |

The supplier should have issued a **zero-rated / out-of-scope invoice** with the notation:
> *"Außerhalb des Anwendungsbereichs der deutschen MwSt / Outside the scope of German VAT – supply to non-EU business (Art. 44 MwStSystRL)"*

---

## 4. Why the Supplier's Approach is Wrong

The supplier appears to have treated the buyer's **DE VAT ID on the invoice header** as sufficient evidence that the recipient has a fixed establishment in Germany receiving the service. This is a **common but legally incorrect shortcut**. Mere display of a DE VAT ID does not:

- Create a fixed establishment
- Shift place of supply to Germany
- Obligate a German VAT charge

The supplier bears the burden of substantiating place of supply. Given the buyer's US incorporation and the nature of the engagement (strategy consulting consumed at US HQ), the supplier should have applied the **reverse-charge / export treatment**.

---

## 5. What AP Should Do

### Immediate Steps

**Step 1 — Do not pay the VAT line without further action**
Paying €47,600 without challenge may prejudice the buyer's position and constitute acceptance of an incorrectly structured invoice.

**Step 2 — Issue a formal written objection to the supplier**
The objection should:
- Cite Article 44 of Directive 2006/112/EC
- Confirm the buyer's place of establishment is the US
- Confirm the German VAT ID relates only to the prior consignment-stock arrangement and constitutes no fixed establishment
- Confirm the service was received and consumed at US headquarters
- Request a **corrected invoice** (Rechnungskorrektur / credit note + new invoice) showing:
  - Net fee: €40,000
  - VAT: €0.00
  - Note: "Supply to taxable person established outside EU — outside scope of German VAT (Art. 44 MwStSystRL)"

**Step 3 — Pay only the net €40,000 pending correction**
(Subject to contract terms; if payment terms require full payment to avoid dispute, escrow the VAT portion or agree in writing that payment is without prejudice.)

**Step 4 — Retain documentation**
Maintain records demonstrating:
- Buyer's US incorporation certificate
- Nature and purpose of the DE VAT registration (consignment stock only)
- Absence of staff/resources in Germany
- That the consulting deliverable was consumed in the US

---

## 6. Is the VAT Reclaimable?

### Route 1: Input Tax Deduction via German VAT Return
A taxable person **may deduct input VAT only insofar as the goods/services are used for taxable transactions** (Art. 168, Dir. 2006/112/EC). Since:
- The supply relates to US operations (not German VAT activities)
- The buyer's only German VAT activity was the consignment-stock arrangement (presumably now concluded)

**Input tax deduction is almost certainly unavailable** or severely restricted. Even if the buyer files a German VAT return, the consulting fees do not relate to German taxable outputs, so no right of deduction arises under §15 UStG.

### Route 2: EU VAT Refund Directive (Dir. 2008/9/EC)
This applies to EU taxable persons recovering VAT from other member states. The buyer is a **non-EU entity**, so **Dir. 2008/9/EC does not apply**.

### Route 3: 13th Directive Refund (Dir. 86/560/EEC)
This allows **non-EU businesses without EU establishment** to claim refunds of German VAT. **However:**
- It requires a **reciprocity arrangement** between Germany and the US (Germany does apply this for US businesses in principle)
- Crucially, if the buyer **has a German VAT registration**, the 13th Directive procedure is **blocked** — the buyer is expected to use its VAT return instead
- And as noted above, the deduction right is unavailable because the cost doesn't relate to German taxable outputs

### Route 4: Correction at Source (Preferred)
**The only clean solution is to obtain a corrected invoice from the supplier.** If the supplier corrects the invoice and cancels the VAT charge, the supplier reclaims the €7,600 from the German Finanzamt via their own VAT return, and the buyer pays only €40,000. This eliminates the reclaimability problem entirely.

> ⚠️ **Risk if VAT is irrecoverable**: If the supplier refuses to correct the invoice and the buyer cannot recover the VAT, the €7,600 becomes a **permanent cost**. This is the core commercial risk and underscores the urgency of invoice correction.

---

## 7. Summary

| Issue | Conclusion |
|---|---|
| Is German VAT correctly charged? | **No.** Place of supply is the US under Art. 44; German VAT does not apply |
| Why? | Buyer's DE VAT ID ≠ fixed establishment; service consumed at US HQ |
| What should AP do? | Reject the invoice, request corrected invoice, pay net only |
| Is VAT reclaimable as charged? | **Practically no** — deduction unavailable (no link to DE taxable outputs); 13th Directive blocked by DE registration; correction at source is the only viable remedy |
| Priority action | **Obtain a corrected invoice from the supplier** |

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** The response correctly identifies the place of supply as the US under Article 44, distinguishes out-of-scope from reverse charge implicitly (treats it as out of scope, not reverse charge), recommends invoice rejection with a corrected invoice, and thoroughly addresses why reclaim is not the right path (covering input deduction, 8th Directive, 13th Directive, and correction at source). While it cites Article 11 of Regulation 282/2011 for fixed establishment rather than explicitly Article 22 for establishment confirmation, it does substantively cover the requirement to communicate/document which establishment receives the service in Step 2 and Step 4 of the AP actions. The analysis is rigorous and correct on all key points.

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

# Month-End Close Accounting: Services PO #4500-77002

## The core principle

Under accrual accounting (ASC 606 / IFRS 15 from the customer's vendor side, and the matching principle on your side), expense recognition follows **service delivery**, not invoice receipt. As of 2026-03-31, $150,000 of services has been performed and substantiated by the vendor's status report — that economic event must hit the March P&L regardless of invoice timing.

---

## Approach 1 — SAP-style Services PO with Service Entry Sheet (SES)

In a properly configured SAP MM/SRM services PO, the workflow is:

**PO → Service Entry Sheet (SES) → Invoice Receipt (IR)**

The SES is the services equivalent of a Goods Receipt (GR) and is what triggers the GR/IR posting.

### Step 1 — March 31, 2026: Post & approve SES for $150,000

When the SES is approved (ML81N → release), SAP posts:

| Account | Dr | Cr |
|---|---|---|
| Consulting Expense (or WBS/cost center) | 150,000 | |
| GR/IR Clearing — Services (SR/IR) | | 150,000 |

- The expense hits the March period via the cost object on the PO line.
- GR/IR is a balance-sheet **liability** (accrued, not-yet-invoiced). It functionally *is* the accrual — no separate manual JE needed.
- The remaining $50,000 stays as **open PO commitment** (encumbrance), not an accrual, because those services have not been performed.

### Step 2 — April 12, 2026: Invoice receipt via MIRO

3-way match: PO line ↔ SES ↔ Invoice.

| Account | Dr | Cr |
|---|---|---|
| GR/IR Clearing — Services | 150,000 | |
| AP — Strategy Consulting Co. | | 150,000 |

GR/IR clears to zero on this line. No P&L impact in April for this milestone (correct — the expense already landed in March).

### Step 3 — Later in April: SES for remaining $50,000, then invoice

Same pattern when April services are delivered: SES posts Dr Expense / Cr GR/IR; invoice clears GR/IR to AP.

### Month-end controls in SAP
- Run **MB5S / ME2S** (GR/IR services balance and PO commitment reports) to identify lines where SES is posted but invoice not yet received → these *are* your accrual at quarter-end.
- The auditor's accrual schedule = open services GR/IR balance + any delivered-but-not-yet-SES'd services (which should be near zero with discipline).

---

## Approach 2 — Manual accrual (no SES, or SES not posted by close)

If your shop doesn't use SES, or operations didn't enter the SES before the books closed, AP/GL posts a manual month-end accrual.

### Step 1 — March 31, 2026: Manual accrual JE

| Account | Dr | Cr |
|---|---|---|
| Consulting Expense (cost center / WBS) | 150,000 | |
| Accrued Liabilities — Goods/Services Received Not Invoiced | | 150,000 |

Supporting documentation: vendor status report dated 2026-03-30, PO #4500-77002, project manager sign-off confirming $150K delivered.

### Step 2 — April 1, 2026: Reverse the accrual

| Account | Dr | Cr |
|---|---|---|
| Accrued Liabilities — GRNI | 150,000 | |
| Consulting Expense | | 150,000 |

(Auto-reversing JE flagged at posting; SAP supports this via the "reversal date" field on FB50/FB01.)

### Step 3 — April 12, 2026: Book the invoice normally

| Account | Dr | Cr |
|---|---|---|
| Consulting Expense | 150,000 | |
| AP — Strategy Consulting Co. | | 150,000 |

**Net April P&L impact for milestone 1 = $0** (the $150K debit from the invoice offsets the $150K credit from the reversal). The expense correctly remains in March.

The remaining $50,000 is **not** accrued at March 31 — services were not yet performed.

---

## Side-by-side comparison

| Aspect | SAP SES (GR/IR) | Manual accrual |
|---|---|---|
| Who posts it | Operations / requisitioner approves SES | GL/AP via JE |
| Liability account | GR/IR Clearing (SR/IR, e.g., 21x000) | Accrued liabilities — GRNI |
| Reversal needed? | No — clears automatically against invoice via 3-way match | Yes — auto-reverse on Day 1 of next period |
| Audit trail | PO → SES → Invoice, system-linked | JE + manual support file |
| Risk of duplication | Low (3-way match blocks dup) | Higher — must ensure reversal posts before invoice |
| Commitment vs accrual | Open PO = commitment; SES'd = accrual | Both tracked off-system |

---

## Key takeaways for this fact pattern

1. **March P&L: $150,000 consulting expense.** Required regardless of method.
2. **March balance sheet: $150,000 liability** (GR/IR services clearing or accrued GRNI).
3. **The remaining $50,000 is not accrued** — it's an open commitment only; no service performed = no expense, no liability.
4. **April: zero net P&L impact** for the milestone-1 invoice — either GR/IR clears to AP (SES method) or the reversal nets the invoice (manual method).
5. **Evidence file for the accrual:** vendor status report (2026-03-30), PO copy, PM confirmation of percent complete. This is what auditors will request to test the cutoff assertion.
6. If the SES had been entered timely, **no manual accrual is needed** — that's the whole point of the GR/IR mechanism. Mixing the two (booking SES *and* a manual accrual) double-counts the liability;

### Grader verdict

- **Score:** 2
- **Confidence:** high
- **Reasoning:** Correctly accrues only $150k in March, presents both manual-with-reversal and SES-with-GR/IR paths with accurate journal entries, addresses GR/IR aging review (MB5S/ME2S), explicitly excludes the $50k as non-accruable (open commitment), and notes evidence/audit considerations. Minor gap: SOX segregation of duties not explicitly called out, but all other rubric elements for a 2 are satisfied.

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

# Accounting for PO #4500-77002 — Services Accrual at March 31, 2026

---

## 1. Conceptual Framework First

The core issue is a **timing mismatch**: services have been *received/consumed* by March 31 ($150,000 worth), but no invoice exists yet. Under **accrual accounting** (ASC 420 / IAS 37 / matching principle), the expense must be recognized in the period the services are delivered — March — regardless of when the invoice arrives.

The $50,000 not yet delivered belongs to April and must **not** be accrued in March.

---

## 2. SAP-Style Services PO Treatment

### Background: How SAP Handles Services POs

| Feature | Goods PO | Services PO |
|---|---|---|
| Receipt document | Goods Receipt (MIGO) | **Service Entry Sheet (SES)** — transaction ML81N |
| GR/IR clearing account | Populated at GR | Populated when SES is **accepted** |
| Invoice posting | MIRO against GR/IR | MIRO against GR/IR |
| Three-way match | PO ↔ GR ↔ Invoice | PO ↔ SES ↔ Invoice |

The **GR/IR clearing account** (typically `GL 19100` or similar) is the mechanical heart of the matching process.

---

### Step 1 — March 31: Vendor Submits/PM Approves Service Entry Sheet (SES)

The project manager or procurement team posts an SES for $150,000 (milestone 1 accepted).

**SAP posts automatically upon SES acceptance:**

```
Dr  Consulting Expense (P&L)        $150,000
    Cr  GR/IR Clearing Account          $150,000
```

> **GR/IR is a balance sheet liability** — it represents "we received the service, but haven't paid the vendor yet." It will clear when the invoice is posted.

**Balance sheet effect at 3/31:**
- Accrued liability on the balance sheet: **$150,000** (in GR/IR)
- Expense hits Q1 P&L: **$150,000** ✓
- No entry for the remaining $50,000(services not yet delivered — correctly excluded)

---

### Step 2 — April 12: Invoice Arrives ($150,000, references Milestone 1)

AP posts the invoice via **MIRO**, referencing PO #4500-77002:

```
Dr  GR/IR Clearing Account          $150,000
    Cr  Accounts Payable (Vendor)       $150,000
```

> GR/IR **clears to zero** — the liability transitions from "accrued/uninvoiced" to a formal AP payable. No P&L impact in April for this milestone (expense was correctly captured in March).

---

### Step 3 — April (Services Delivered): SES for Remaining $50,000

When the remaining scope is delivered and accepted in April:

```
Dr  Consulting Expense (P&L)        $50,000
    Cr  GR/IR Clearing Account          $50,000
```

Then upon invoice receipt:

```
Dr  GR/IR Clearing Account          $50,000
    Cr  Accounts Payable                $50,000
```

---

### SAP GR/IR Walkthrough Summary Table

| Date | Transaction | Dr | Cr | GR/IR Balance |
|---|---|---|---|---|
| 3/31 | SES accepted — MS1 | Consulting Expense $150K | GR/IR $150K | $(150,000) |
| 4/12 | Invoice posted — MS1 | GR/IR $150K | AP $150K | $0 |
| Apr | SES accepted — MS2 | Consulting Expense $50K | GR/IR $50K | $(50,000) |
| Apr | Invoice posted — MS2 | GR/IR $50K | AP $50K | $0 |

---

## 3. Manual Accrual Treatment (No SAP Services PO / SES Mechanism)

In a manual environment (or where the SES was not posted in time), the controller must book a **manual accrual journal entry**.

### Step 1 — March 31: Manual Accrual Entry

**Supporting documentation:** Vendor's status report dated 2026-03-30 confirming $150,000 delivered.

```
Dr  Consulting Expense (P&L)        $150,000
    Cr  Accrued Expenses / Accrued     $150,000
        Liabilities (B/S)
```

*Memo: Accrual per vendor status report 2026-03-30, PO #4500-77002, milestone 1. Invoice pending.*

> The account used is typically a **current liability** (e.g., "Accrued Professional Fees"), distinct from Accounts Payable (which requires an actual invoice).

---

### Step 2 — April 12: Invoice Received — Reverse and Rebook

**Best practice (most common):** Reverse the accrual on April 1 (auto-reverse) and book the invoice normally.

**April 1 — Auto-reversal:**
```
Dr  Accrued Expenses                $150,000
    Cr  Consulting Expense (P&L)        $150,000
```

**April 12 — Invoice posted to AP:**
```
Dr  Consulting Expense (P&L)        $150,000
    Cr  Accounts Payable                $150,000
```

> Net effect on April P&L: **zero** (reversal debit and invoice debit cancel out). March P&L carries the $150,000 expense. ✓

**Alternative approach (no auto-reverse):** When invoice arrives, debit AP onboarding and credit the accrual to clear it, then record AP:
```
Dr  Accrued Expenses                $150,000
    Cr  Accounts Payable                $150,000
```
This is cleaner but requires matching discipline to avoid double-counting.

---

### Manual Accrual Journal Summary

| Date | Entry | Dr | Cr |
|---|---|---|---|
| 3/31 | Accrue services received | Consulting Expense $150K | Accrued Liabilities $150K |
| 4/1 | Auto-reverse | Accrued Liabilities $150K | Consulting Expense $150K |
| 4/12 | Book invoice | Consulting Expense $150K | Accounts Payable $150K |
| April | Accrue MS2 (if still no invoice) | Consulting Expense $50K | Accrued Liabilities $50K |

---

## 4. Key Differences: SAP SES vs. Manual Accrual

| Dimension | SAP SES/GR/IR | Manual Accrual |
|---|---|---|
| **Trigger** | SES acceptance by PM | Controller judgment + documentation |
| **Audit trail** | System-generated, PO-linked | Manual JE — needs strong supporting memo |
| **Risk of omission** | Lower (procurement workflow) | Higher (depends on controller awareness) |
| **Risk of double-count** | Minimal (MIRO clears GR/IR exactly) | Moderate if reversal not tracked |
| **Balance sheet account** | GR/IR Clearing (quasi-liability) | Accrued Expenses / Accrued Liabilities |
| **April P&L impact** | Zero (invoice just clears GR/IR) | Zero (if auto-reverse used correctly) |
| **Three-way match** | Enforced by system (PO/SES/Invoice) | Manual verification required |
| **Invoice tolerance** | SAP MIRO blocks if outside tolerance | Manual review by AP |

---

## 5. Critical Control Points & Disclosure Considerations

### What Must NOT happen:
- ❌ Do not accrue the full $200,000 — the $50,000 in April services have not been received and would be a **misstatement** (overstated liability and expense in Q1)
- ❌ Do not defer the $150,000 to April because the invoice hasn't arrived — that violates the matching principle and **understates** Q1 expense
- ❌ Do not record the April invoice as expense in April without the reversal — that would **double-count** the $150,000

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response correctly accrues only $150k in March, explicitly excludes the $50k as non-accruable, presents both the manual accrual path with reversing entry and the SAP SES/GR/IR path with clean journal entries, and explains the GR/IR clearing mechanic. It also addresses control points and contrasts the two approaches. Minor gaps: it cites ASC 420/IAS 37 instead of ASC 720/IAS 1, and doesn't explicitly discuss GR/IR aging review or SOX segregation of duties between SES poster and AP invoice poster — though it does mention three-way match enforcement and audit trail considerations. Overall meets the rubric for a 2.

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

This onboarding profile exhibits a **near-textbook pattern of Russia/Belarus sanctions evasion and export-control diversion risk**, specifically concerning dual-use electronic components on the U.S. Commerce Control List (CCL) and the Common High Priority List (CHPL). The recommended decision is **DO NOT ONBOARD** pending substantial enhanced due diligence (EDD), and likely outright rejection.

---

## 1. Required Screening

### A. Sanctions & Watchlist Screening
Run name, address, and (where available) DOB/passport screening for the entity, the UBO (Ivan Petrov), the registered agent, the bank, and the freight forwarder against:

- **OFAC SDN List** and OFAC Consolidated Sanctions List (incl. SSI, FSE, NS-MBS lists)
- **OFAC 50% Rule** analysis on UBO ownership chain
- **BIS Entity List, Denied Persons List, Unverified List, and Military End User (MEU) List** (15 C.F.R. Part 744, Supp. Nos. 4, 4-Bs)
- **State Department AECA Debarred List** and **Nonproliferation Sanctions list**
- **UK OFSI Consolidated List**
- **EU Consolidated Financial Sanctions List** (especially Council Regs. 833/2014 and 269/2014)
- **Canada SEMA / UN 1267** lists
- **Latvia/EU PEP and adverse media** screening on Petrov
- **Cyprus** beneficial-ownership register cross-check

### B. Export-Control Classification
- Determine probable **ECCNs** for microcontrollers, FPGAs, RF components — many fall under **3A001, 3A090, 3A991, 5A001/5A991** and overlap heavily with the **BIS/EU/UK/JP Common High Priority List (CHPL)** items most diverted to Russia.
- Verify whether items are **EAR99** or controlled, and whether **License Exception** availability is foreclosed by destination/end-user.
- Russia/Belarus footnote-3 and footnote-imposed FDP rule (15 C.F.R. § 734.9) applicability check.

### C. KYC / KYB
- Delaware certificate of formation, EIN letter, operating agreement
- Beneficial ownership per **FinCEN Corporate Transparency Act / BOI** rule (entity formed post-1/1/2024 must have filed a BOI report within 30 days)
- Petrov: passport, proof of address, source-of-wealth, second-citizenship/residency disclosure (Cyprus golden-passport history is itself a flag)
- Bank account verification with KYC at Latvian bank (post-ABLV remediation context)
- Freight forwarder identity, license, and routing detail
- End-to-end **Bill of Lading / supply chain traceability** to the actual manufacturer in Hong Kong/PRC

### D. Adverse Media & Trade-Data Checks
- Open-source intelligence on Petrov, the LLC, and any affiliated entities
- Trade data (e.g., ImportGenius/Panjiva) for the LLC and the freight forwarder
- Check freight forwarder against known **diversion-network typologies** flagged in BIS, FinCEN, and Treasury joint alerts

---

## 2. Red Flags (Mapped to Regulatory Guidance)

The fact pattern matches multiple flags in the **June 2023 BIS/FinCEN Joint Supplemental Alert (FIN-2023-Alert004)** and the **May 2023 Quint-Seal Compliance Note** on Russia export-control evasion:

| # | Red Flag | Source/Significance |
|---|----------|---------------------|
| 1 | **Newly formed shell LLC (Nov 2025)** with no operating history, immediately requesting $250K PO and $1M annual spend | BIS Red Flag #4 (new customer); FinCEN shell-company typology |
| 2 | **Delaware** formation with **national registered-agent** address — no nexus to goods, customers, or operations | Classic shell indicator |
| 3 | **UBO resident in Cyprus** — high-risk jurisdiction for Russian-linked structures (post-2022 Pandora Papers, sanctions on Cypriot enablers) | EU/UK/US enforcement focus |
| 4 | **Russian/CIS-origin name (Petrov)** + Cyprus residency + Latvian bank — well-documented Russia-evasion corridor | Treasury/BIS alerts identify Baltics + Cyprus as primary transshipment finance routes |
| 5 | **Latvian SWIFT bank** — Latvia is a frontline EU jurisdiction for Russia-related circumvention; many Latvian banks have settled with FinCEN/OFAC | FinCEN 311 history (ABLV) |
| 6 | **Goods are CHPL items** — microcontrollers, FPGAs, RF components are precisely the items appearing in recovered Russian weapons (Iranian Shahed drones, Russian missiles) | BIS CHPL (Tiers 1–4); G7 priority list |
| 7 | **Shipped from Hong Kong** via **unknown freight forwarder** — Hong Kong is the #1 transshipment hub flagged by BIS for Russia diversion; HK now treated with PRC-level scrutiny under EAR | 15 C.F.R. § 740 (HK treated as PRC since 2020); BIS 2023/2024 enforcement actions |
| 8 | **50% prepayment** for "manufacturing capacity reservation" — abnormal for a distributor of electronic components; suggests either no real inventory or front-loaded value extraction before sanctions trip | FinCEN unusual-payment-terms typology |
| 9 | **Mismatch between corporate domicile (US), UBO (Cyprus), bank (Lat

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response identifies all major red flags (shell LLC, Cyprus UBO, Latvian bank, HK transshipment, dual-use CHPL components, 50% prepayment, unknown freight forwarder). It names all relevant regimes: OFAC including the 50% rule, EU (833/2014, 269/2014), UK OFSI, UN, BIS EAR with Entity List/MEU/Unverified/DPL, FinCEN BOI/CTA. It recommends specific verification steps (passport, bank KYC, BOI filing check, freight forwarder verification). The response was truncated mid-sentence so the explicit graduated onboarding recommendation and bank-callback control are not clearly visible in what's shown, though it does state 'DO NOT ONBOARD pending EDD.' FCPA is not explicitly mentioned. Despite these gaps, the answer is comprehensive and demonstrates strong command of the relevant regimes including the OFAC 50% rule and FinCEN BOI, meeting the bar for level 2.

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

# Diagnosis of SOX P2P Control Failures — Ghost-Vendor Scheme

## 1. Reasoning: What the Fact Pattern Tells Us

The scheme exhibits the classic hallmarks of a **structured ghost-vendor / fictitious-disbursement fraud**, and each red flag maps directly to a specific COSO control activity that either did not exist, was not designed effectively, or was not operating effectively.

| Red flag in fact pattern | Underlying control failure |
|---|---|
| Single AP clerk could **create vendor**, **approve invoice**, and **release ACH** | Failure of **Segregation of Duties (SoD)** — the foundational P2P control |
| Vendor added with a **P.O. box remit-to** and a **bank account in a relative's name** | Failure of **Vendor Master Data Governance** — no independent vetting (W-9, TIN match, OFAC, bank verification, address validation, employee-vendor cross-match) |
| 49 invoices all between **$9,800 and $9,950** | Classic **structuring (smurfing)** below the $10,000 PO threshold and the $50,000 CFO-approval threshold — the policy thresholds themselves are a **control design defect** because they invite circumvention rather than detect it |
| All invoices **non-PO** for vague "logistics services" | Failure of **non-PO invoice controls** — no contract/SOW match, no requisitioner, no service-receipt confirmation |
| **No contract or SOW** on file | Failure of **Procurement / contract management control** prior to vendor onboarding |
| Pattern ran **18 months / $480K** undetected | Failure of **detective monitoring analytics** — no recurring vendor spend reviews, no Benford / threshold-proximity / duplicate-vendor analytics |
| Tip from coworker, not control, surfaced it | Reliance on **whistleblower hotline** as the de facto detective control — indicates the rest of the control stack failed |
| Auditor sampled vendor change log but missed it | The change log existed but the **review of the change log was either not performed, not evidenced, or not designed to flag suspicious attributes** (P.O. box, employee address match) |

## 2. Specific Control Activities That Should Have Prevented or Detected the Scheme

### A. Preventive Controls

1. **Segregation of Duties in the ERP (entitlement design)**
   - Vendor master maintenance, invoice approval, and payment run initiation must reside in **three different roles** owned by three different people. SAP/Oracle SoD rulesets (e.g., the standard "P001 – Maintain Vendor + Process Invoice" conflict) would have flagged this combination.
   - Remediation: enforce role-based access controls; quarterly SoD ruleset review; compensating controls (independent reviewer) where SoD is impractical due to staffing.

2. **Vendor Master Onboarding Controls**
   - Independent vendor setup team (not AP) performs:
     - W-9 / TIN matching with IRS
     - OFAC/sanctions screening
     - Bank account verification (Plaid, micro-deposit, or direct call-back to a number obtained independently from the vendor's website, not from the invoice)
     - **Address validation against USPS** (a P.O. box should require additional approval and a documented business reason)
     - **Employee-vendor cross-match**: automated scan of vendor addresses, phone numbers, bank accounts, and tax IDs against the HR master file. This single control would almost certainly have caught the clerk's home P.O. box.
   - Dual approval on every new vendor add, regardless of expected spend (the **$50K threshold for CFO approval is the wrong design** — every new vendor should have at least one independent approver; CFO approval can be reserved for higher tiers).

3. **Three-Way Match / Non-PO Invoice Controls**
   - Policy: PO required for **all** services purchases over a low de minimis (e.g., $2,500), or require a signed SOW/contract for any services vendor regardless of dollar amount.
   - Non-PO invoices routed through a **business-owner approval workflow** with a documented requisitioner — not the AP clerk.
   - System-enforced block on splitting invoices: detection of multiple invoices from the same vendor in a rolling window summing above threshold.

4. **Threshold Design**
   - Replace bright-line thresholds ($10,000 PO, $50,000 CFO) with **cumulative / rolling thresholds** (e.g., aggregate vendor spend YTD) and **anti-structuring detection** (invoices clustered just below the threshold). This is the single most important design fix — the original policy *invited* the fraud.

### B. Detective Controls

5. **Vendor Master Change Log Review**
   - Monthly review by someone independent of AP, with documented evidence (sign-off, exceptions cleared). Review attributes should include: P.O. box remit-to, employee address matches, banking changes, and dormant-then-active vendors.
   - The auditor's walkthrough proved the log existed but the review either wasn't happening or wasn't designed to catch these attributes.

6. **Continuous Monitoring / Data Analytics**
   - **Benford's Law** on invoice amounts (49 invoices clustered in the $9,800–$9,950 band would scream).
   - **Threshold-proximity analytics**: invoices within 5% of an approval threshold.
   - **Vendor velocity analytics**: new vendor with rapid invoice cadence.
   - **Duplicate detection**: same remit-to address across vendors; same bank account across vendors and employees.
   - **Top-N vendor reviews** by category — "Northern Logistics" with no contract would surface.

7. **Periodic Vendor Confirmations / Recertification**
   - Annual vendor recertification: confirm existence, tax info, banking, and contract status.
   - Sample-based vendor confirmations sent to addresses on file by Internal Audit.

8. **ACH Payment Release Controls**
   - **Positive Pay / dual release**: ACH file released by Treasury

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response identifies SoD as the foundational failure and covers all required additional gaps: vendor-master maker-checker with independent approval, employee-vendor cross-match (explicitly called out as the control that would have caught the P.O. box), threshold-clustering/structuring analytics (Benford's, threshold-proximity), rolling/cumulative spend triggers replacing bright-line thresholds, non-PO/contract controls, and change-log review. Specific remediations are proposed for each. The response was cut off before completing the material-weakness analysis under AS 2201, which is a notable gap — the rubric's '2' tier requires reaching a defensible material-weakness conclusion with severity-by-potential reasoning. However, the diagnostic content is otherwise very strong and complete. Given the truncation specifically omits the MW conclusion, this is borderline between 1 and 2; the response covers all five-plus control gaps with remediations exceptionally well, but missing the explicit MW conclusion is a real deficiency.

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

# SOX P2P Control Failure Analysis: Ghost-Vendor / AP Clerk Fraud

---

## I. Fraud Mechanics Summary (Before Diagnosing Controls)

The scheme exhibits three classic characteristics that should anchor the control analysis:

1. **Fictitious vendor creation** — self-authorized, self-remitted
2. **Invoice structuring** ("smurfing") — deliberate sub-threshold fragmentation to avoid dual controls
3. **Segregation of duties (SoD) collapse** — a single individual controlled the entire P2P transaction lifecycle: vendor onboarding → invoice approval → payment initiation

Understanding the *mechanics* is prerequisite to diagnosing *which* controls failed versus which never existed.

---

## II. SOX P2P Control Failures — Layered Diagnosis

### A. Segregation of Duties (SoD) Failures — The Root Cause

This is the most fundamental failure. The AP clerk held **three logically incompatible system access roles simultaneously**:

| Capability | Role Class | Control Principle Violated |
|---|---|---|
| Create vendor master records | **Custodial / Authorization** | No single user should both onboard a vendor and process payments to it |
| Approve invoices < $10,000 | **Authorization** | Invoice approver should be independent of the payment initiator |
| Initiate ACH payment runs | **Execution / Custody** | Payment initiation should be segregated from invoice approval |

**COSO principle implicated:** Control Activities — *Principle 10 (Selects and develops control activities)*, specifically the sub-principle that entities should **segregate duties among individuals to reduce risk of error or fraud**.

Under a properly designed SoD matrix, even *two* of these three capabilities in one person's hands would represent a design deficiency. All three together creates an environment where fraud requires **zero collusion** — the single most dangerous SoD configuration in P2P.

**Remediation:**
- Implement a formal **SoD conflict matrix** within the ERP covering at minimum: vendor create/modify, invoice approval, and payment run initiation
- Enforce at the **ERP role/profile level** — detective policies without preventive system enforcement are insufficient
- Conduct an **access recertification** across all AP users quarterly
- Where true SoD is impractical (e.g., small-company exemption), deploy **compensating controls** (see Section II.D)

---

### B. Vendor Master Governance Failures

The vendor master is the single most fraud-susceptible master data object in P2P. Multiple controls were absent or ineffective:

**1. Absence of independent vendor onboarding authorization**

Policy required CFO approval for new vendors with *anticipated annual spend > $50,000* — but this threshold was never triggered because the scheme was structured to remain below it in any given review cycle. The policy had **no control over new vendor adds independent of spend level**.

*What should exist:* All new vendor additions — regardless of anticipated spend — should require **dual authorization**: the requestor's business owner/cost center manager plus an independent AP supervisor or Procurement officer. The ERP should enforce a **maker/checker workflow** for vendor master changes (one person creates the record; a different person activates it).

**2. No beneficial ownership / remit-to address verification**

No process validated that the remit-to address or bank account belonged to a *bona fide arms-length third party*. Standard controls include:
- **W-9 / EIN verification** against IRS TIN matching
- **Bank account change confirmation** via callback to a verified phone number (not one provided by the requestor)
- **Sanction/OFAC screening** (secondary benefit: also catches policy violations)
- **Address duplication check** — ERP should flag any remit-to address that matches an employee home address or P.O. box already in the HR master

**3. No periodic vendor master cleansing / analytics**

Controls should include at least annual (ideally continuous) **vendor master analytics** to identify:
- Vendors with no associated PO number in any transaction
- Vendors whose remit address matches employee records
- Vendors with no contract on file
- Single-approver vendors with high payment frequency
- Vendors added and paid within a short window

**Remediation:**
- Redesign vendor onboarding as a **three-party workflow**: requestor → business owner approval → AP/Procurement independent activation
- Implement ERP-enforced **duplicate address/bank account detection**
- Schedule quarterly **vendor master data quality reviews** with automated exception reports
- Implement a **vendor confirmation letter** program for new adds (mailed independently to the registered address)

---

### C. Invoice and Payment Approval Control Failures

**1. The $10,000 approval threshold was the wrong anchor**

The policy's reliance on a *per-invoice* threshold for additional approval, without any **cumulative or aggregate monitoring**, is a structural design flaw. A $9,900 invoice looks unremarkable in isolation; 49 of them to the same vendor totaling $480,000 is a material anomaly.

*What should exist:*
- **Cumulative vendor spend monitoring** — automated alert when a vendor's year-to-date spend crosses defined thresholds (e.g., $50K, $100K, $250K) regardless of individual invoice amounts
- **Velocity rules** — flag vendors receiving more than a defined number of invoices per period (e.g., > 6 invoices/month from a new vendor)
- **Invoice amount clustering analysis** — statistical clustering of invoice amounts just below approval thresholds is a textbook fraud indicator and should be a standard data analytics test

**2. Non-PO invoices processed with no compensating review**

The policy required PO coverage for services > $10,000 (presumably per-engagement, not per-invoice). All 49 invoices were non-PO. The control failure here is two-fold:
- No **non-PO invoice exception queue** requiring management escalation
- No **contract/SOW validation** as a condition of payment for service vendors

*What should exist:*
- Non-PO invoices for services above a *low* materiality threshold (e.g., $1,000 per invoice or $25,000 cumulative) should route to a **business owner who can attest to services received**
- A **negative assurance confirmation** requirement: the approving manager must affirmatively confirm that services were delivered, not merely that the invoice looks reasonable
- **Receiving confirmation** (the P2P equivalent of a three-way match) — for service invoices where physical goods receipt is impossible, a **service acceptance certificate** from the cost center owner should be mandatory

**3. ACH payment run without independent release**

The clerk could both approve invoices *and* initiate the ACH run. Even if all upstream approvals were properly obtained, **payment release should require a different authorized individual** — the "second key" in dual-control payment processing.

*What should exist:*
- ERP-enforced **dual authorization on payment runs** above a defined dollar threshold
- **Payment file review** by treasury or controller before bank release, with a focus on new payees or unusual payment patterns
- **Bank-side positive pay / ACH filter controls** — the company's bank should have ACH blocking rules requiring pre-authorization of beneficiary accounts

---

### D. Monitoring and Detective Control Failures

Even where preventive controls fail, a robust monitoring program should provide a **second line of defense**.

**1. Internal audit / management review gaps**

- No **continuous monitoring** of vendor master changes with management sign-off
- No **periodic AP data analytics** program (invoice clustering, new vendor/high-frequency analysis)
- No **surprise audits** of the AP function

**2. External auditor sampling limitation (important but bounded)**

The external auditor *did* select the vendor master change log in their SOX walkthrough — but did not select any of the 49 invoices in their substantive sample. This is *not per se* an audit failure: substantive samples are risk-based and cannot cover every transaction. However, it highlights:
- **The walkthrough of the vendor master change control should have identified the SoD deficiency** — the clerk had the ability to both add vendors and approve payments without any independent review
- If the auditor walked through the vendor master addition process and found that the *same individual* who added the vendor could also approve payments to it, this should have been flagged as at minimum a **significant deficiency** during the walkthrough, even without identifying the specific fraud
- The SOX testing program should include **data analytics as a substantive procedure** — a clustering analysis of invoice amounts would likely have surfaced the sub-$10,000 pattern

**Remediation:**
- Implement a **continuous controls monitoring (CCM) program** (GRC tools such as Workiva, AuditBoard, or ERP-native analytics)
- Mandate **

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response identifies SoD as the root cause and addresses multiple additional control gaps: vendor master maker-checker workflow, employee-vendor address/bank matching, invoice clustering/structuring analytics, cumulative/rolling vendor spend monitoring, non-PO services controls, dual ACH authorization, and continuous monitoring. Specific remediations are proposed for each. The response was cut off before completing the material weakness analysis section, which is a notable gap — the rubric explicitly requires 'a defensible material-weakness conclusion under AS 2201 with the right reasoning.' However, the response covers all five+ required control gaps with strong remediation detail. The truncation of the MW conclusion is concerning but the bulk of substance meets the level-2 criteria. Borderline 1/2; leaning 2 given the depth of control analysis, though the missing MW conclusion is a real weakness.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---

## q_010 — close_and_controls · hard · **score 2/2** (model: `claude-haiku-4-5`)

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

# SOX P2P Control Failure Diagnosis

## I. Control Deficiencies Identified

### A. Vendor Master Management (Critical Gap)

**Failed Controls:**
1. **No segregation of duties (SOD):** The AP clerk could both create vendors AND approve/pay invoices. No independent authorization of new vendor adds.
2. **No secondary approval threshold for new vendor creation:** Policy requires CFO sign-off only for >$50K/year anticipated spend, but the clerk had unilateral ability to add vendors with no initial risk assessment or identity verification.
3. **No vendor onboarding procedures:** No requirement to verify vendor legitimacy (business registration, tax ID, references, independent W-9 collection, banking verification).
4. **Inadequate change monitoring:** While the auditor selected the vendor master change log, there was no preventive control flagging vendors with related-party or high-risk characteristics (home addresses, relatives as payees).

**How it enabled the fraud:**
- The clerk created a fictitious vendor with no review, using personal address/relative's bank account as the remit-to.
- The control activity (auditor's walkthrough) was **detective only** and post-transaction; it did not prevent the vendor from being set up.

---

### B. Invoice Approval & Authorization (Control Circumvention)

**Failed Controls:**
1. **Lack of PO requirement enforcement:** The policy requiring PO coverage for services >$10K was undermined by:
   - No system-enforced "three-way match" (PO-Receipt-Invoice)
   - No blocking logic in the ERP to prevent payment of non-PO invoices above a certain threshold
   - The clerk could approve invoices simply marked "non-PO" without documented justification or exception handling

2. **Threshold gaming:** The policy did not address:
   - Structuring (49 invoices all just under $10K)
   - Cumulative spend monitoring (49 × $9,800 = $480K—well above a new vendor's first-year scrutiny threshold)
   - Frequency-based red flags (49 invoices in 18 months to a single "services" vendor is unusual)

3. **Single-person approval authority:** The AP clerk had approval authority for invoices under $10K with no secondary review, even for new vendors or unusual patterns.

**How it enabled the fraud:**
- Each invoice individually fell under the $10K approval threshold.
- The cumulative spend and vendor-new-status red flags were never evaluated.

---

### C. Substantive Testing & Audit Scope (Detective Gap)

**Auditor-Specific Failures:**
1. **Sample selection bias:** The auditor selected the vendor master *change log* (preventive/control testing) but did **not** select any of the 49 invoices in the substantive sample of accounts payable transactions.
2. **Insufficient coverage:** The fact pattern suggests the auditor's AP substantive sample either:
   - Was too small to statistically capture a new vendor with moderate-sized transactions
   - Used a monetary unit sampling (MUS) approach that may have favored high-dollar transactions from established vendors
   - Lacked a secondary sampling strategy for new vendors or non-PO transactions

3. **No analytics or exception monitoring:** The auditor (and company) did not employ:
   - Duplicate invoice detection
   - Same-vendor frequency analysis
   - Non-PO transaction rate trending
   - Benford's Law or value clustering detection (49 invoices in a narrow $9.8–9.95K band is statistically improbable)

---

## II. Specific Control Activities That Should Have Prevented/Detected

### **Preventive Controls (Should Have Stopped It)**

| Control | Implementation | Reason It Would Have Worked |
|---------|-----------------|------------------------------|
| **Segregation of Duties Matrix** | AP clerk cannot approve invoices for vendors they created; require Supervisor/Manager approval | Eliminates single-point control over vendor setup + payment |
| **Mandatory PO for All Services** | System blocks payment if no PO linked; eliminates "non-PO" carve-out or requires Director-level override with documented business justification | Prevents circumvention of the >$10K review threshold |
| **Vendor Master Lockdown** | Only Procurement or Finance Management can create new vendors; requires independent verification (tax ID match, Dun & Bradstreet check, bank account verification form) | Stops fictitious vendor creation at source |
| **Related-Party Flag** | System or manual control flags remit-to addresses matching employee home addresses or personal names; requires explanation and senior approval | Would have surfaced the home P.O. box and relative's bank account immediately |
| **Cumulative Spend Alert** | For new vendors, system flags when monthly or quarterly spend approaches or exceeds $50K/year policy threshold; requires exception approval | Catches structuring across 49 invoices |
| **System Enforced Thresholds** | Use ERP workflow rules: invoices >$10K automatically route to CFO; new vendors with >$X anticipated spend auto-route to Procurement Director | Prevents policy circumvention through manual workarounds |

### **Detective Controls (Should Have Found It)**

| Control | Implementation | Reason It Would Have Worked |
|---------|-----------------|------------------------------|
| **Detailed Vendor Master Audit** | Quarterly or semi-annual review of all new vendors added in the prior period, with verification of address, tax ID, and banking details against independent sources | Would have identified the home address and relative's bank account in Q1 or Q2 |
| **Invoice Pattern Analysis** | Analytics on AP transactions: cluster analysis of invoice amounts (the $9.8–9.95K band is a statistical anomaly), frequency by vendor, days to payment, etc. | The 49 invoices in a tight range would flag immediately |
| **Three-Way Match Testing** | Substantive audit sampling of ALL non-PO transactions for goods/services to verify receipt/delivery and proper authorization | Each of the 49 invoices would fail (no PO, no receipt, likely no delivery) |
| **Vendor Performance Review** | For any vendor with >$100K/year spend, require documentation of contract, SOW, performance KPIs, and evidence of service delivery (invoices, delivery receipts, customer acknowledgments) | Would surface that "logistics services" have no supporting evidence |
| **Bank Account Reconciliation** | Segregated review: AP clerk reconciles to approved vendor master monthly; Finance Manager independently verifies remit-to addresses match reconciliation | Catches divergences (home address vs. expected business address) |
| **CFO Surprise Vendor Review** | Quarterly (unannounced) review of 5–10 random new vendors from prior quarter; independent verification of legitimacy and spend | Direct examination of Northern Logistics would have revealed the scheme |

---

## III. Root Causes & System Design Failures

1. **Over-reliance on threshold policies** without system enforcement—policies are only as strong as the controls that enforce them.
2. **Lack of cumulative monitoring**—the company monitored per-transaction approval but not aggregate risk per vendor or per user.
3. **Inadequate SOD in the P2P cycle**—a single AP clerk should never control vendor creation, invoice approval, and payment initiation.
4. **No independent verification of new vendors**—assuming that vendors are legitimate without basic due diligence.
5. **Audit sampling gaps**—the external auditor did not stratify or diversify sampling to capture new vendors with atypical transaction patterns.

---

## IV. Remediation Roadmap

### **Immediate (0–30 days)**

- **Freeze the AP clerk's create-vendor and approve-invoice authorities** pending investigation completion.
- **System lockdown:** Block the AP clerk's ERP access to these functions; reassign to read-only or data entry only.
- **Forensic review:** Pull all transactions initiated by this user and by vendors they created over the past 2+ years.
- **Vendor verification:** Independently verify the top 20 new vendors created by any AP staff in the past 12 months.

### **Short-term (1–3 months)**

1. **Redesign P2P workflows in the ERP:**
   - Implement mandatory three-way match (PO-Receipt-Invoice); system blocks payment without all three.
   - Code a workflow rule: *All new vendors require Procurement Manager sign-off before activation.*
   - Code a workflow rule: *Invoices from vendors active <90 days route to Finance Manager for approval regardless of amount.*
   - Code a workflow rule: *Cumulative spend by vendor >$50K/year (calculated YTD) auto-escalates to CFO.*

2. **Segregation of duties:**
   - Remove invoice approval authority from all AP clerks; route to AP Supervisor or

### Grader verdict

- **Score:** 2
- **Confidence:** medium
- **Reasoning:** The response identifies SoD as a primary failure and covers the key additional control gaps: vendor master maker-checker/independent approval, employee-vendor address/bank match (related-party flag), cluster-below-threshold analytic (Benford's/structuring detection), cumulative rolling spend escalation, and non-PO services without contract review. It proposes specific remediations for each (system enforcement, workflow rules, forensic lookback, role redesign). However, the material-weakness analysis under AS 2201 is notably weak/missing — the response does not explicitly conclude this is a material weakness, nor does it articulate the 'severity by potential not actual loss' reasoning, disclosure implications under Item 9A, or AS 1301 communication requirements. The remediation section is also cut off. Given the rubric's level-2 requirement of 'a defensible material-weakness conclusion under AS 2201 with the right reasoning,' this is borderline. The control identification is strong enough for a 2, but the missing MW conclusion is a meaningful gap. Leaning to 1 due to the explicit rubric requirement.

### Decision (fill in)

_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_

---
