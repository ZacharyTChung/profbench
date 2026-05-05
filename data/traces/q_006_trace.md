# q_006 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **Treas. Reg. §301.7701-3** (disregarded-entity
> classification), **IRS Publication 515** (Withholding of Tax on
> Nonresident Aliens and Foreign Entities), **IRS Publication 519**
> (US Tax Guide for Aliens), **IRS Form W-8BEN / W-8BEN-E
> instructions**, and **IRS Form 1042 / 1042-S** filing requirements.
> Heuristics (§3) and edge cases (§4) are flagged `[Authority gap]`.

## 1. The W-9 is invalid for this entity

A US single-member LLC owned by a non-resident alien (NRA) is
**disregarded** for US federal tax purposes per Treas. Reg.
§301.7701-3 — the LLC itself is not the relevant tax person; the
owner is. Because the owner is an NRA, the correct form is
**W-8BEN** (individual), not W-9.

W-9 is for **US persons only** (US citizens, US resident aliens, and
domestic entities). An NRA owner of a disregarded US LLC fails that
test.

## 2. AP actions

1. **Reject the W-9.** Document the rejection reason in the vendor
   master.
2. **Request the correct form: W-8BEN** (since the relevant tax
   person is the individual NRA owner, not the LLC).
3. **Hold the vendor inactive** until the W-8BEN is received and
   validated.
4. **Validate the W-8BEN** — name match to the disregarded-entity
   owner, foreign TIN or US ITIN, country of residence (Mexico),
   treaty claim if applicable.

## 3. Withholding analysis

**The default withholding rate on US-source income paid to NRAs is
30%** (per IRC §1441; IRS Pub 515). For consulting services, the
withholding analysis turns on **where the services are performed**:

- **Services performed inside the US** → US-source income → 30%
  withholding unless reduced by a tax treaty.
- **Services performed entirely outside the US** → foreign-source
  income → **no withholding**.

The US-Mexico tax treaty may reduce the withholding rate on US-source
business profits if the NRA does not have a US permanent
establishment, **but only if the W-8BEN claims the treaty benefit**
on Part II. AP cannot apply a treaty rate without an explicit treaty
claim on the form.

**For this engagement** (~$50k/year for consulting services), the AP
team must determine:

- Where services are performed (likely a mix of remote-from-Mexico
  and on-site US visits).
- Whether the supplier is willing to track and certify US-day
  allocation, OR whether the firm withholds on the full US-source
  portion.

## 4. Year-end reporting

Regardless of withholding amount (including zero), payments to an NRA
require **Form 1042-S** reporting:

- **1042-S** to the recipient and IRS reporting US-source income
  paid and any tax withheld (income code typically 17 for personal
  services; verify against the engagement specifics).
- **Form 1042** is the US filer's transmittal/summary return.
- **No 1099-NEC** — 1099-NEC is for US persons only. Filing a 1099
  on an NRA payment is itself an error.

## 5. Heuristics

> **[Authority gap]**

- **Treat single-member LLC + foreign owner as a foreign vendor for
  tax purposes**, even though the LLC is US-organized. The
  disregarded-entity rule is the trap most AP teams fall into.
- **No W-8 = no payment.** The penalty for paying without a valid
  W-8 (and therefore without correct withholding) falls on the US
  payer, not the foreign recipient.

## 6. Edge cases

> **[Authority gap]**

- **The owner has a US ITIN and elects to be taxed as a US person on
  treaty grounds** — rare; requires specific treaty election
  documentation.
- **The LLC has multiple owners, some US, some foreign** — no longer
  a disregarded entity; partnership analysis applies, with W-8 / W-9
  required from the entity itself based on its election.
- **Services performed for a foreign branch of the US payer** —
  source-of-income analysis can shift; consult tax for non-trivial
  amounts.

## 7. Process recommendation

The vendor packet currently in hand is incomplete and the spend
profile (~$50k/yr) is large enough that the firm's tax function
should review before activation. AP's role: enforce the document
prerequisite (W-8BEN), do not pay any amount until withholding is
correctly calculated, and do not issue a 1099 at year-end.
