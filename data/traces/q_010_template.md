# Reasoning trace template — q_010 (SOX P2P ghost-vendor)

> Replace each `_[fill in]_` block with your actual reasoning. Don't polish.
> Once filled, paste into q_010's `ideal_answer` and run
> `python -m runner.eval refresh-questions`.
>
> Length target: 1000–1800 words. This is a high-leverage question because
> the SOX reasoning chain is dense and is exactly where solo expert mental
> models matter most.

## The question (for reference)

AP clerk had: vendor master add, invoice approval under $10k, ACH payment
initiation. Created vendor "Northern Logistics Services LLC" with own P.O.
box as remit-to and relative's bank account. 49 invoices over 18 months,
each $9,800–$9,950, totaling $480k. No PO, no contract. Tip from coworker
surfaced it; auditor hadn't sampled these. What controls failed? Material
weakness?

---

## 1. First glance

When you read this fact pattern, what's the FIRST thing you flag, and why?

> _[fill in: e.g. "Toxic combination of access — vendor master + invoice approval + payment init in one role. Before I look at anything else, that's the headline finding..."]_

What's the second flag?

> _[fill in: e.g. "The invoice amounts. $9,800 — $9,950, all just under $10k. That's not a coincidence, that's structuring..."]_

---

## 2. Decision points — control-by-control walkthrough

For each control area below, in your own words: what should the design have
been, what failed, what's the impact.

### 2a. Segregation of duties

> _[fill in: which roles must be separate, why each separation matters, what the canonical SOX P2P SoD matrix looks like at your firm]_

### 2b. Vendor master setup controls

> _[fill in: maker-checker, TIN match, address verification (employee match!), bank verification (callback to known number — NOT to the number on the request), W-9 collection, any other gates. What's the right gate sequence?]_

### 2c. Approval thresholds and structuring detection

> _[fill in: what analytics SHOULD be running — distribution-vs-threshold, Benford's, just-under-threshold cluster reports. How often. Who reviews. What action triggers]_

### 2d. PO requirement / non-PO pathway

> _[fill in: should this scenario have required a PO under any reasonable policy? What's the right non-PO services policy? Cumulative-over-rolling-12-month escalation?]_

### 2e. ITGC / access reviews

> _[fill in: how often, what gets reviewed, what flags toxic combinations. What does an SoD-conflict report look like?]_

### 2f. Continuous monitoring

> _[fill in: employee-vendor matching (HRIS to vendor master on address/bank/phone), recurring high-spend with new vendor, missed-PO patterns, etc.]_

---

## 3. Heuristics — your working detection rules

What do YOU watch for as red flags in real life that an LLM probably
wouldn't name?

> _[fill in 4–6 specific tells, e.g. "Round-trip patterns where AP and a vendor's AR balance reconcile too cleanly — fictitious vendors don't have realistic AR aging on their side..."]_

---

## 4. Remediation

After discovering this, the actual remediation playbook:

> _[fill in: in order — preserve evidence, freeze accounts, lookback scope, internal audit / IA + GC + external counsel involvement, communications limits, when to escalate to ACL, when to call in forensic accountants]_

---

## 5. Material weakness analysis

Walk through the AS 2201 reasoning. This is the part frontier models often
get half-right.

### 5a. Severity test

> _[fill in: "reasonable possibility of material misstatement that would not be prevented or detected" — how do you apply this when actual loss is below your firm's quantitative materiality but the control gap is pervasive?]_

### 5b. Pervasiveness vs isolated

> _[fill in: why this specific deficiency is pervasive (access-design issue) rather than isolated to one transaction]_

### 5c. Disclosure decisions

> _[fill in: 10-K Item 9A, ICFR re-assertion, restatement question, audit committee communications under AS 1301, what management certification gets pulled]_

### 5d. The "could have been worse" reasoning

> _[fill in: why severity is judged on potential not actual loss in MW analysis]_

---

## 6. Lookback scope

What's the actual scope you set when investigating after discovery?

> _[fill in: time window (24 months minimum?), which vendors (just this clerk's adds?), which transactions (cumulative-spend cohort below threshold?), which other clerks (anyone with similar entitlement profile?)]_

---

## 7. Why models miss this

> _[fill in: optional meta-observation — what is the typical LLM gap on SOX reasoning, and what's the corresponding training-data shape that would close it?]_
