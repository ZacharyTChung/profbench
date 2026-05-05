# q_011 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **IRS Publication 2108A** (On-Line Taxpayer
> Identification Number Matching Program), **IRS Publication 1281**
> (Backup Withholding for Missing and Incorrect Name/TINs), and
> **IRC §3406** (Backup Withholding). Heuristics (§3) and edge cases
> (§4) flagged `[Authority gap]`.

## 1. The control: do not activate

AP should **not activate the vendor or release the PO** until the
TIN mismatch is resolved.

A "no match" response from the IRS TIN Matching Program (per IRS
Pub 2108A) means the legal name on the W-9 line 1 does not match
the name the IRS has on file for that EIN. The mismatch could be
benign (a clerical or DBA-vs-legal-name issue) or substantive
(wrong TIN, wrong entity, identity issue), but until it is resolved
the firm faces **backup-withholding liability** under IRC §3406.

## 2. Common causes of a TIN-match failure

Per IRS Pub 1281:

1. **Name format mismatch.** The W-9 may show a DBA, an abbreviation,
   or a punctuation variant of the legal name. The IRS-of-record
   name is the name registered with the EIN at issuance, which may
   differ from the name the supplier uses operationally.
2. **Entity-classification change without IRS notification.** The
   supplier converted from LLC to C-corp (or vice versa) and the
   IRS records weren't updated — common after a structural change.
3. **TIN typo on the W-9.** A single-digit error.
4. **EIN was issued to a different entity** that the supplier later
   merged with or absorbed without updating IRS records.
5. **Identity-theft / wrong-EIN scenario.** Less common but
   meaningful — supplier may not be entitled to use this EIN.

## 3. AP's resolution path

1. **Contact the supplier** with a non-accusatory message
   explaining the TIN-match outcome and asking the supplier to
   verify their **legal name and EIN as registered with the IRS**.
   Ask the supplier to consult their IRS confirmation letter
   (CP 575 / 147C) which shows the name-of-record.
2. **Request a corrected W-9** if the supplier identifies a name or
   TIN issue.
3. **Re-run TIN matching** on the corrected W-9. Document each
   attempt with date and outcome.
4. **If TIN matching still fails after a corrected W-9:** require
   the supplier to obtain a **147C letter from the IRS** (a name-and-
   EIN verification letter) before proceeding.

## 4. Backup-withholding implications

Per IRC §3406 and IRS Pub 1281, if AP **pays the supplier without
resolving the mismatch**, the firm becomes liable to deduct **24%
backup withholding** on reportable payments (1099-NEC class).

The withholding obligation runs from the moment the payer has
reason to believe the TIN/name is incorrect. A "no match" response
from the TIN Matching Program is **on-notice** for backup-withholding
purposes. The firm has a defined window (per IRS notice procedures)
to take corrective action; after that window, the 24% must be
withheld.

The compliance trap: paying without withholding *and* without
resolving the mismatch creates an IRS audit exposure for the firm,
not the supplier.

## 5. Heuristics

> **[Authority gap]**

- **TIN-match failure is a process failure, not a fraud
  presumption.** Most failures are benign name-format or
  classification issues. Treat the supplier as cooperative until
  evidence shows otherwise.
- **The CP 575 / 147C letter is the gold-standard evidence.** Other
  evidence (state filings, DBA registrations) is corroborative but
  not authoritative for the IRS-of-record question.
- **Document every TIN-match attempt and outcome.** The audit
  defense for unresolved mismatches is the documentation chain.

## 6. Edge cases

> **[Authority gap]**

- **The vendor refuses to provide a 147C letter** — this is itself a
  significant red flag. Legitimate vendors with EIN issues will
  obtain a 147C; resistance suggests the EIN may not be theirs.
- **The vendor has a recent state-level entity-name change** that
  has not yet propagated to the IRS — verify state and federal name
  separately. Federal name controls for TIN-match purposes.
- **Foreign-owned single-member LLC misfiling on W-9** (see q_006)
  — the failure mode is structural, not a clerical mismatch; the
  fix is W-8BEN, not a re-run TIN match.

## 7. Vendor-master and SoD considerations

The vendor record should remain in **inactive / hold** status until
the mismatch is resolved. Activation requires the same maker-checker
control that applied at initial onboarding (per AICPA AAG-AUD on
vendor master controls). A clerk who keyed the original record
cannot unilaterally activate after a TIN-match resolution; a
supervisor or master-data steward must approve.

## 8. Process recommendation

For TIN-match failures, AP should maintain a **mismatch register**
recording each instance, the cause, the resolution, and the time-to-
resolution. This serves both as the audit-defense documentation and
as input to a vendor-onboarding-quality metric — high TIN-match
failure rate often indicates upstream onboarding-form issues
(unclear instructions on legal-name field, no validation against
IRS naming conventions).
