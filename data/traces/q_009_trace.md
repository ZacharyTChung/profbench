# q_009 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to **OFAC Specially Designated Nationals (SDN) list** and
> the **OFAC 50 Percent Rule** (Revised Guidance, 2014); **FinCEN
> Beneficial Ownership Information (BOI) rule, 31 CFR §1010.380**;
> **BIS Entity List**, EAR Part 744; **FATF guidance on shell-company
> red flags**. Heuristics (§3) and edge cases (§4) flagged
> `[Authority gap]`. Anchor data file:
> [`data/anchors/anchor_q009_sanctions_screening.json`](../anchors/anchor_q009_sanctions_screening.json).

## 1. Red flags (each independently meaningful)

The packet has multiple red flags that, taken together, require
**enhanced due diligence (EDD)** and a **hold on onboarding** pending
resolution.

1. **Newly formed Delaware LLC (Nov 2025) with no operating history**
   — FATF shell-company red flag. New entity + no track record
   demands stronger justification than an established supplier.
2. **UBO with a Russian-origin name and Cyprus residence.** Cyprus
   has been a known nexus for Russian-affiliated structures and is
   on the FATF and OFAC enhanced-scrutiny radar post-2022.
3. **National registered-agent service** (rather than a substantive
   office) — common in legitimate Delaware formations but a known
   shell-company indicator when combined with the other signals.
4. **Bank account in a jurisdiction with looser correspondent
   banking** — payment-routing red flag for sanctions evasion.
5. **No public website, no LinkedIn presence, no D&B record** —
   absence of any independent corroboration of substance.

Any one in isolation is a yellow flag; together they are an EDD
trigger.

## 2. Regulatory regimes that apply

### OFAC sanctions screening
The supplier itself, the listed UBO, and any 50%+ owners must be
screened against the **SDN list** and all sectoral sanctions lists.
Even if no party screens as a direct hit, the **OFAC 50 Percent
Rule** (2014 Revised Guidance) requires treating any entity owned
**50% or more, in the aggregate**, by SDN-listed person(s) as itself
blocked, **even if the entity is not separately listed**. This is
the single most-missed screening step on Russia-nexus packets.

### BIS Entity List
Independent of OFAC. Some Russian-nexus entities appear on the BIS
Entity List (export controls under EAR Part 744) without being on
the OFAC SDN list. Screen separately.

### FinCEN BOI / Corporate Transparency Act
**31 CFR §1010.380** requires reporting companies (which a
Delaware LLC formed in 2025 typically is) to file beneficial
ownership information with FinCEN. AP should ask the supplier for
proof of BOI compliance — failure to file is itself a red flag and
suggests the entity is operating outside the standard regulatory
framework.

### Sectoral sanctions and EU-equivalent regimes
Russia-nexus also implicates **EU Council Regulation 833/2014** as
amended (Russia sanctions), **UK financial sanctions** under OFSI,
and **G7 price-cap regimes** for energy-related supplies. If the
goods/services touch any of those, the sanctions-screening
obligation extends accordingly.

## 3. Recommended onboarding decision

**Hold pending resolution.** Specific actions required before
considering onboarding:

1. **Run all parties through SDN, sectoral, and BIS screening.**
   Document the screening results with date and screening tool
   used. Re-screen periodically (continuous monitoring).
2. **Apply the OFAC 50% Rule.** Request the full ownership chain;
   identify any SDN-listed individuals or entities at any level;
   compute aggregate ownership.
3. **Request FinCEN BOI compliance evidence.**
4. **Request justification for the Cyprus/Russia nexus** —
   legitimate business reason, history, references.
5. **Independent bank-account verification** via callback to a
   public-source phone number (not from the onboarding packet).
6. **Compliance / legal review** before activation, regardless of
   screening outcome — this packet is high-risk on profile, not
   only on screening hits.

If any screening returns a hit, an unresolved 50%-rule chain, or
unsatisfactory BOI / KYC evidence: **do not onboard**. Document the
decision.

## 4. Heuristics

> **[Authority gap]**

- **The 50% Rule is the single most-missed screening step.** Direct
  SDN hits are easy; aggregate-ownership chains require asking for
  documentation suppliers are reluctant to provide.
- **Russia / Cyprus / Caribbean offshore are not by themselves
  prohibited**, but they raise the EDD bar materially. The right
  question is not "can we onboard?" but "what evidence resolves the
  red flag?"
- **A supplier that resists providing ownership documentation is
  itself the red flag.** Legitimate suppliers can produce ownership
  charts; sanctions-evasion structures often cannot.

## 5. Edge cases

> **[Authority gap]**

- **The UBO is a Russian dual-national who has emigrated and
  renounced Russian citizenship** — the screening obligation still
  applies, but the EDD outcome may resolve. Documentation of
  citizenship status matters.
- **The supplier produces a clean 50%-rule chain showing no SDN-
  listed beneficial ownership** — onboarding may proceed with
  enhanced monitoring; do not relax the periodic re-screening.
- **The supplier offers to absorb sanctions risk via indemnity
  language in the contract** — indemnities do not satisfy
  regulatory obligations. The US payer is on the hook regardless of
  contractual indemnity.

## 6. Process recommendation

This packet should never have made it past initial vendor onboarding
without compliance review. The control gap is the upstream
onboarding workflow: AP should not be the function making the
sanctions/UBO judgment — compliance/legal should be the gating
approver for any packet with the profile above (new entity, foreign
UBO, offshore banking).
