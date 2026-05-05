# q_018 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **PCAOB AS 2201** (control-deficiency taxonomy and
> severity tests, including significant deficiency vs material
> weakness), **PCAOB AS 1305** (communications about control
> deficiencies), **COSO 2013** (Control Activities and Monitoring
> Activities), and **AICPA AU-C 265** (private-company analog).
> Heuristics (§3) and edge cases (§4) flagged `[Authority gap]`. This
> question's tier-classification judgment call is one of the
> closest-to-pure-SME exercises in the benchmark.

## 1. The hierarchy (narrowest to broadest)

PCAOB AS 2201 establishes a four-tier framework, often summarized
into three operational tiers for SOX P2P diagnosis:

### Tier 1 — Transaction-level failure
The control existed and was designed correctly, but in this specific
transaction it didn't operate as designed. Example: 3-way match was
supposed to flag the price variance but the AP clerk overrode it
without authorization.

**Severity:** generally a **deficiency**, possibly aggregated up
under AS 2201's "combination of deficiencies" test. One-off
transaction failures are not by themselves significant deficiencies
unless severity or frequency raises the profile.

**Remediation:** discipline the clerk, retrain, possibly add an
override-approval requirement to the control.

### Tier 2 — Control-operating failure (recurring)
The control existed and was designed correctly, but it consistently
fails to operate as designed across multiple transactions. Example:
the AP team is overriding 3-way-match exceptions routinely because
the queue is too large to process within payment-term deadlines.

**Severity:** a **significant deficiency** under AS 2201 — important
enough to merit attention by those responsible for oversight, but
less severe than a material weakness. The "recurring" element
distinguishes from Tier 1.

**Remediation:** address the upstream operational driver (staffing,
process), not just the individual instance.

### Tier 3 — Control-design failure
The control as designed cannot address the risk it was supposed to
address, OR the control does not exist where it should. Example: the
firm's 3-way-match doesn't cover services POs at all because the SES
configuration was never deployed.

**Severity:** typically a **material weakness** under AS 2201
because design failures apply to **every transaction within the
affected control's scope** — they create a "reasonable possibility
that a material misstatement of the financial statements would not
be prevented or detected on a timely basis."

**Remediation:** redesign the control. Cannot be fixed at the
individual-transaction level.

## 2. The diagnostic question

For a single observed failure, the diagnostic sequence:

1. **Did the control exist for this transaction class?**
   - No → Tier 3 design failure.
   - Yes → continue.
2. **Was the control designed correctly to address the risk?**
   - No → Tier 3 design failure.
   - Yes → continue.
3. **Did the control operate as designed in this case?**
   - No → continue.
4. **Is this an isolated instance, or does the same failure recur?**
   - Isolated → Tier 1 transaction failure.
   - Recurring → Tier 2 operating failure.

## 3. Why the distinction matters for SOX 404 disclosure

PCAOB AS 2201's severity test (the "reasonable possibility that a
material misstatement would not be prevented or detected" standard)
treats design failures more severely than operating failures because:

- **Design failures are pervasive.** Every transaction within scope
  is vulnerable. The actual loss recorded is bounded only by which
  transactions happened to occur during the deficiency period and
  by the bad-actor's ambition.
- **Operating failures may be remediable in-period.** A control
  that's designed correctly but operating poorly can return to full
  effectiveness with discipline and training; a control that's
  designed wrong cannot.

This drives different disclosure outcomes:

- **Material weakness** → must be disclosed in Form 10-K Item 9A
  (per Regulation S-K Item 308); auditor issues an adverse ICFR
  opinion; audit committee notification under AS 1305.
- **Significant deficiency** → audit committee communication under
  AS 1305 but no public disclosure.
- **Deficiency** → tracked internally; no required external
  communication.

## 4. The "could-have-been-worse" reasoning

This is the load-bearing argument that converts a design failure
with small actual loss into a material weakness despite quantitative
materiality being below threshold. AS 2201's severity test asks
about the **upper bound of plausible misstatement** the deficiency
could have permitted, not just the actual loss recorded.

A design failure in P2P SoD that happened to be exploited for $480k
(see q_010) could have been exploited for far more — the loss
recorded reflects perpetrator choice, not control limit. Severity
assessment looks at the control limit, which is effectively
unbounded for design-level deficiencies.

## 5. Heuristics

> **[Authority gap]**

- **"Recurring" is the bright line between Tier 1 and Tier 2.** A
  single override is a discipline issue; a pattern of overrides is
  a process issue.
- **Design failures are obvious in hindsight and invisible in
  prospect.** The fact that no one had previously identified the
  missing control doesn't mitigate severity; it confirms it.
- **The question "could a similar incident have escaped detection?"
  reliably tilts toward Tier 3** — if the answer is yes, design is
  the issue.

## 6. Edge cases

> **[Authority gap]**

- **The control failed because of a one-time external event** (e.g.
  ERP outage during month-end). Tier 1; document the compensating
  control that should activate during outages.
- **The control was designed correctly for the risk that existed at
  design time, but the risk has evolved.** Becomes Tier 3 once the
  evolved risk is identified — controls are evaluated against
  current risk, not against historical risk.
- **Multiple Tier 1 deficiencies aggregate** under AS 2201's
  combination test into a higher tier when the cumulative effect
  meets the severity threshold.

## 7. Documentation expectation

Whatever tier the diagnosis lands on, the audit-evidence record
must show:

- The observable failure (the improper payment / variance / etc.).
- The diagnostic reasoning across the four-step framework above.
- The severity classification (deficiency / significant deficiency
  / material weakness) and the AS 2201 reasoning supporting it.
- The remediation plan and timeline.
- Audit-committee communication where AS 1305 requires it.

This documentation is what gets sampled in the next year's ICFR
walkthrough and what determines whether remediation has been
sustained long enough to re-assert ICFR effectiveness in subsequent
filings.
