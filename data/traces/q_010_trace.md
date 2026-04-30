# q_010 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Written for the v0.3
> framing described in [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> The close_and_controls category is the **furthest from the author's
> operational depth**, so this trace leans most heavily on primary
> sources: PCAOB AS 2201 (material weakness definition and severity
> framework), PCAOB AS 1301 (audit committee communications), COSO 2013
> (Control Activities and Information & Communication), ACFE *Report to
> the Nations* (billing-scheme typology, structuring, employee-vendor
> matching), Nigrini's *Forensic Analytics* (Benford's-law application),
> SEC Regulation S-K Item 308 (10-K Item 9A disclosure), and AICPA
> AAG-AUD on ICFR and SoD. Working detection heuristics (§3) and the
> materiality judgment call (§5b) are the sections most weakened by the
> absence of an SME and are flagged for `REVIEW_REQUEST.md` upgrade.

## 1. First-pass triage

Two patterns are diagnostic before any other analysis.

**Pattern 1: toxic combination of access privileges.** The clerk held
vendor-master add, invoice approval under $10k, and payment
initiation. This is the textbook end-to-end ghost-vendor enabler:
one person can create the payee, approve the bill, and release the
cash. PCAOB AS 2201 and COSO 2013 jointly establish that segregation
of incompatible functions across vendor-master maintenance, invoice
approval, and payment initiation is a key control over disbursements.
The deficiency is an **access-design failure** — the entitlement grant
itself, not just its operation — which under AS 2201 is a more severe
classification than an isolated operating failure because it applies
to every transaction within the affected access profile.

**Pattern 2: invoice-amount structuring.** Invoices clustering between
$9,800 and $9,950, all just under the $10k approval threshold, across
49 instances over 18 months is the canonical structuring pattern
documented in ACFE's *Report to the Nations* billing-scheme typology.
A single just-below-threshold invoice is unremarkable; 49 of them
across 18 months is a designed evasion of the approval-threshold
control.

The remaining facts (no PO, no contract, P.O. box remit, relative's
bank account) are corroborators that confirm the ghost-vendor
classification suggested by the first two patterns.

## 2. Decision points — control-by-control

### 2a. Segregation of duties (the root-cause control)

PCAOB AS 2201 defines a **material weakness** as a deficiency, or
combination of deficiencies, in ICFR such that there is a reasonable
possibility that a material misstatement will not be prevented or
detected on a timely basis. COSO 2013 principle 10 ("selects and
develops control activities") identifies SoD as a foundational design
expectation; principle 12 deploys it through policies and procedures.

The toxic-combination access profile here defeats SoD by design.
Under AS 2201 severity analysis, design-level deficiencies generally
support material-weakness classification because they apply to every
transaction the access profile can touch — not only to the
transactions already discovered.

### 2b. Vendor-master setup controls

A robust new-vendor onboarding control set, per AICPA AAG-AUD vendor-
master coverage and ACFE anti-fraud guidance:

- **Independent maker-checker.** The clerk who keys the add cannot be
  the approver. Cross-reporting-line approver is preferred to in-line
  to reduce collusion risk.
- **W-9 / W-8 collection before activation; TIN match against IRS
  records** (IRS Pub 2108A). New vendor remains inactive until the
  TIN/name match is clean.
- **Address verification including employee-vendor address match**
  against HRIS data. ACFE classifies employee-vendor address matching
  as a baseline detective control for ghost-vendor schemes; absence
  of this analytic is itself a control gap.
- **Bank-account verification via independent callback** to a
  supplier phone number obtained from a public source (D&B, the
  supplier's website found via independent search) — *not* from the
  onboarding packet itself. This control is the standard countermeasure
  for business-email-compromise (BEC) attacks that substitute a
  fraudulent bank account at onboarding.

In this case the failures are comprehensive: P.O. box remit
(employee-vendor address match would have triggered), relative's bank
account (extended HRIS-relationship matching could have triggered, if
deployed), no contract on file, no PO. **At least three setup controls
would have flagged the vendor.**

### 2c. Approval-threshold and structuring detection

49 invoices clustered in a $150 band immediately below the $10k
approval threshold is the textbook structuring signature documented in
ACFE *Report to the Nations*. Standard analytics that would flag the
pattern within weeks:

- **Just-below-threshold cluster reports** by vendor. Any vendor with
  N invoices within X% of an approval threshold flags for review.
- **Benford's-law deviation** on invoice first-digit distribution
  (per Nigrini, *Forensic Analytics: Methods and Techniques for
  Forensic Accounting Investigations*). Real-world vendor invoices
  follow Benford's distribution; structured amounts deviate sharply.
- **Invoice-frequency anomalies for new vendors.** A new vendor
  generating multiple invoices per week with near-identical amounts is
  unusual and warrants review.

The detective gap here is glaring: 49 invoices over 18 months without
any flag. This is an **analytics-design** gap, not a tooling gap.

### 2d. PO requirement and non-PO pathway

The firm's policy required POs for services > $10k. The structuring
kept individual invoices under $10k, but cumulative spend crossed the
threshold many times. Three control upgrades address this gap:

- Lower the PO requirement for services to a threshold below typical
  structuring opportunity (e.g., $5k).
- Require a PO for *new* vendors regardless of single-invoice amount
  (high-risk-onboarding control).
- Implement **rolling-12-month cumulative-spend triggers**: any vendor
  whose 12-month cumulative spend exceeds the policy's
  CFO-approval threshold is auto-flagged for CFO review even where no
  single invoice did. This is the strongest of the three because it
  converts structuring from an evasion path into a detection trigger.

### 2e. ITGC and access reviews

PCAOB AS 2201 requires entity-level controls including periodic access
reviews to identify SoD conflicts. Standard cadence is quarterly,
owned by IT GRC, with reviewers in the entitlement-holder's
management chain. The access-review control should:

- Use an automated SoD conflict matrix; flagged combinations are
  presented prominently rather than buried in the entitlement list.
- Preserve sign-off evidence for audit sampling.
- Include retention-of-evidence sufficient for SOX 404 walkthrough.

The fact that the clerk's toxic combination was granted *and remained
in place* across 18 months indicates the access review either did not
run, did not flag SoD conflicts, or flagged them without remediation.
Each failure mode is itself an ITGC deficiency under AS 2201.

### 2f. Continuous monitoring

The detective layer that would have caught this earlier:

- **Employee-vendor matching** across remit-to address, phone number,
  and bank account against HR records. Run continuously; alert on
  matches. The clerk's P.O. box and relative's bank account would
  match against the right reference data sets.
- **Vendor cumulative-spend monitor** as described in §2d.
- **New-vendor cohort review:** vendors added in a quarter sorted by
  6-month spend. Concentrated spend on a new vendor warrants control
  review.

## 3. Working detection heuristics

> **[Authority gap]** Practitioner detection heuristics from real
> investigations are the highest-value SFT content. The notes below
> are derivable from ACFE / AICPA framework material; the rolodex
> content requires SME input via `REVIEW_REQUEST.md`.

- **Just-under-threshold clustering is the strongest single signal.**
  Per ACFE, this signal outperforms employee-vendor address match and
  missing-contract flags as a structuring indicator.
- **Round-trip patterns where AP and a vendor's purported AR balance
  reconcile too cleanly.** Fictitious vendors lack realistic AR aging
  on their side because they lack a real AR system; supplier
  statements requested ad hoc tend to show suspiciously clean
  zero-balance-after-payment patterns.
- **No contract + recurring spend + non-PO pathway = always
  investigate.** Legitimate non-PO recurring spend (utilities, taxes,
  legal retainers) belongs to a recognized exception class. A
  "logistics services" vendor is not in that class.
- **Absence of audit findings is not absence of control gaps.**
  Auditors sample; they do not enumerate. Per AICPA AAG-AUD sampling
  guidance, a clean prior-year audit does not constitute evidence
  that ICFR is operating effectively in the current period.

## 4. Remediation sequence

Standard sequence after discovery, anchored to AICPA AAG-AUD response
to identified deficiencies and PCAOB AS 1301 audit-committee
communications:

1. **Preserve evidence.** Lock the clerk's account access (do not
   terminate the user record yet — audit trail required). Snapshot
   the vendor master and AP transaction records as of discovery date.
2. **Freeze further activity** on the suspect vendor: hold any
   in-flight payments, freeze the vendor record from new invoice
   posting.
3. **Engage** internal audit, general counsel, and (depending on
   materiality and firm policy) external counsel and forensic
   accountants. AP cannot run the investigation: conflict of interest.
4. **Determine lookback scope.** Minimum:
   - All vendors added by this clerk over the last 24–36 months.
   - All non-PO services vendors with cumulative spend > $50k over
     the same window.
   - All other clerks with the same entitlement profile (the SoD gap
     was likely not unique to this person).
5. **External counsel review** before any communication to the clerk,
   audit committee, or external auditor. Privilege considerations
   matter at this stage.
6. **Audit-committee notification** under PCAOB AS 1301 if the matter
   rises to reportable.

## 5. Material-weakness analysis

### 5a. Severity test (PCAOB AS 2201)

A control deficiency is a **material weakness** under AS 2201 where
there is a "reasonable possibility that a material misstatement of
the financial statements would not be prevented or detected on a
timely basis." The "reasonable possibility" threshold under AS 2201
is interpreted in line with FASB ASC 450 / SFAS 5 ("more than
remote") rather than the higher "probable" threshold.

The actual loss is $480k. Quantitative materiality depends on the
registrant's size — material for a $100M company, immaterial in
isolation for a $10B company. Critically, AS 2201 evaluates **the
controls' ability to prevent a worse occurrence**, not just the actual
loss recorded.

### 5b. Pervasiveness vs. isolated

> **[Authority gap on judgment call]** The conclusion below follows
> from AS 2201 framework reasoning. Firm-specific judgment from an
> SME with material-weakness conclusion experience would sharpen the
> argument significantly.

The deficiency lives in **access design and SoD**, which is pervasive
by nature: the same SoD weakness could enable misstatements
substantially larger than $480k. The actual loss being below
materiality reflects the perpetrator's choice to structure within a
threshold rather than swing for a larger hit; the design weakness is
indifferent to that choice. The "could-have-been-worse" reasoning is
the load-bearing argument for material-weakness classification under
AS 2201 in cases of this shape. Default lean: **material weakness**
in nearly all such cases, because end-to-end single-person control of
cash disbursement is the pattern AS 2201's "reasonable possibility"
test was specifically written to capture.

### 5c. Disclosure decisions

If material weakness:

- **Form 10-K Item 9A (per SEC Regulation S-K Item 308)** —
  management's ICFR assertion must disclose the weakness; the firm can
  no longer assert ICFR is effective.
- **Auditor's ICFR opinion** — adverse opinion on ICFR, separate from
  the financial-statement opinion.
- **Audit committee** — substantive communication under PCAOB AS 1301,
  not merely notification.
- **Restatement question** — only if the weakness *caused* a
  misstatement that itself crosses materiality. The $480k may or may
  not, depending on registrant size.
- **External counsel review** of all of the above before public filing.

### 5d. Remediation timeline

Even after remediation, AS 2201 generally requires that new controls
operate effectively for a sustained period — typically a quarter at
minimum, often two — before the firm can re-assert ICFR effectiveness.
A 10-K filed at year-end after a Q3 discovery therefore likely
discloses the weakness as un-remediated even if remediation work has
begun.

## 6. Lookback scope

Specific scoping for the investigation:

- **Time window:** 24 months minimum; 36 if the clerk's tenure was
  longer.
- **Vendors:** all vendors added by this clerk, plus all non-PO
  services vendors with cumulative spend > $50k that were added in the
  lookback window (the SoD gap may have been exploited by other clerks
  with the same access profile).
- **Transactions:** within those vendors, all invoices, looking for
  similar structuring patterns, employee-vendor matches, missing
  contracts, P.O. box remits.
- **Other clerks:** anyone with the same entitlement profile, even
  those not implicated. The SoD gap is the design issue; identify all
  individuals who could have exploited it.

## Why models miss this

Frontier models name SoD as a control issue. The recurring gaps:

1. **Structuring as the leading detection signal.** Most responses
   cite SoD failure first; structuring is what would actually have
   surfaced the scheme sooner. Ranking the controls by detective
   value, not just by control-framework prominence, is where the
   model loses the point.
2. **The "could-have-been-worse" severity reasoning** under AS 2201.
   Models tend to apply quantitative materiality to actual loss
   ($480k) rather than to the upper bound of plausible loss enabled
   by the SoD gap. The pervasiveness argument is what drives the
   material-weakness conclusion.
3. **Employee-vendor matching as a continuous-monitoring control.**
   Models name vendor-master setup controls but rarely name this
   specific cross-system match — even though ACFE classifies it as
   a baseline detective control.

The training data carries the SOX framework material; the gap is in
**applying it to a specific fact pattern with the right ranking of
which control failure matters most for detection.**

## How to convert into the q_010 ideal_answer field

Sections 1–6 concatenate to a long answer. Trim to ~1200 words for the
`ideal_answer` field. Refresh via:

```bash
python -m runner.eval refresh-questions
python -m scorer.autoscore --run-id <run_id> --overwrite
python -m analysis.report --run-id <run_id>
```
