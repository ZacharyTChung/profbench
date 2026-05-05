# q_012 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **FBI Internet Crime Complaint Center (IC3)** annual
> reports on Business Email Compromise (BEC), **AICPA cybersecurity
> risk-management framework**, **ACFE *Report to the Nations***
> (vendor-payment fraud typology), and standard AP control-design
> guidance from **IIA practice advisories**. Heuristics (§3) and
> edge cases (§4) flagged `[Authority gap]`.

## 1. Reject the change as submitted

**Do not apply the bank-account change based on the email.** This is
the canonical Business Email Compromise (BEC) pattern. Per the FBI's
IC3 annual reports, BEC against AP functions is the **single largest
source of payment-fraud losses** in US corporate financial crime —
billions of dollars per year, primarily through bank-account-change
requests against established suppliers.

The legitimacy markers in the email (company letterhead, CFO
signature, correct vendor ID, reference to a real outstanding
invoice) are **exactly the markers a competent BEC actor would
include**. They reduce — but do not eliminate — the probability the
request is fraudulent. The default decision under any reasonable
control framework is to verify out-of-band before applying any
change.

## 2. Why the email triggers controls regardless of legitimacy

Three control principles apply (per AICPA + IIA guidance):

1. **High-impact change requires independent verification.** A bank-
   account change re-routes 100% of future payments to the new
   account. The asymmetry between cost-of-verification (one phone
   call) and cost-of-error (full payment redirected to a fraud
   account) makes verification mandatory.
2. **Email is not an authenticated channel.** Email-based requests
   are spoofable, intercept-able, and reply-attackable. The
   controlling channel for vendor-bank changes is **callback to a
   phone number obtained from a public source** — the vendor's
   website found via independent search, the vendor's onboarding
   record from before the email arrived, or a published directory
   like D&B. Phone numbers in the email itself are not acceptable.
3. **The control runs regardless of the email's apparent
   legitimacy.** Treating "this looks legitimate" as a basis for
   skipping verification defeats the purpose of the control. The
   verification *is* the control.

## 3. The correct procedure

1. **Acknowledge receipt** of the request to the email sender (do
   not commit to applying the change). Use a neutral acknowledgment.
2. **Identify a phone number from a non-email source** — the
   supplier's website (verified via independent search), the
   onboarding-record contact information, or a directory.
3. **Call the verified number** and ask to speak with a person
   authorized to confirm bank changes (typically the CFO, controller,
   or AR manager). Do **not** use any phone number from the email
   itself.
4. **Verify the request in detail** — the new bank, account number
   (last 4 digits cross-check), routing number, effective date, and
   reason for the change. A legitimate change will have a coherent
   answer; a BEC actor will not.
5. **Document the verification** — date, time, person spoken to,
   number called. This is the audit evidence.
6. **Apply the change** through the firm's standard bank-change
   process, with maker-checker SoD (the person who applies the
   change is not the person who verified it).
7. **Hold any payment that would route to the new account** until at
   least one full verification cycle has completed. Many BEC schemes
   target a specific in-flight invoice (note that this email
   references "$48,200 outstanding") — pause that payment.

## 4. Additional red flags in the email itself

> **[Authority gap]** — practitioner-recognized BEC tells beyond
> the standard list

- **Urgency / "please update for the upcoming payment"** — BEC
  emails frequently leverage time pressure on a known outstanding
  invoice.
- **CFO sender (rather than the AR contact)** — BEC actors often
  spoof high-authority figures because AP teams hesitate to push
  back. The control must apply equally to CFO-signed requests.
- **Letterhead / company branding included** — easily replicable
  from public materials. Legitimacy markers, not legitimacy.
- **Domain look-alike** (e.g. `acmemfg-supplier.com` vs the real
  `acmemanufacturing.com`) — common BEC tactic. Compare against the
  domain on file.

## 5. Heuristics

> **[Authority gap]**

- **The verification is the control.** Skipping verification because
  the email "looks legitimate" is the failure mode the control was
  designed to prevent.
- **In-flight invoices are the target.** When a bank-change request
  arrives shortly before a known-outstanding payment, that
  payment is the BEC actor's specific objective. Hold it.
- **Out-of-band contact is not optional.** A reply to the original
  email asking for verification is not out-of-band — the BEC actor
  controls that channel.

## 6. Edge cases

> **[Authority gap]**

- **The supplier really did change banks and is irritated by the
  callback** — apologize, complete the verification, document, and
  the supplier's records now reflect the firm's standard process for
  next time. Good vendors understand the control.
- **The verified phone number reaches the actor's confederate** —
  rare but documented. Sophisticated BEC schemes plant a phone
  number at a plausible-looking domain. If the verification "feels"
  off (vague answers, reluctance to specify), escalate to compliance
  before applying.
- **The legitimate change is an emergency** (e.g. vendor's bank
  failed) — emergency does not waive the control; it accelerates the
  verification timeline. Same procedure, faster cadence.

## 7. Process recommendation

The firm's vendor-master change-management policy should specify
that **all bank-account changes require out-of-band callback
verification**, that the callback must use a non-email-sourced phone
number, and that the verification documentation is audit-sampleable.
This control should be tested annually under SOX 404 ICFR.
