# q_001 reasoning trace — AI DRAFT

> **[AI DRAFT — practitioner edits required]** Same conventions as q_003.
> Sections 3 (heuristics) and 4 (edge cases) need real practitioner
> rewriting. The TIN/normalization section is standard textbook material.

## 1. First glance

TIN first, always. Names get mangled (suffix variants, abbreviations,
case), addresses change (relocations, branch offices, P.O. boxes),
phone numbers get reassigned. **TIN normalization** — strip non-digits,
compare 9-digit sequences — is the only field where same value reliably
means same legal entity. That's why I anchor every dedupe analysis on
TIN before I look at anything else.

In this case both records have identical TIN sequences (`123456789`).
Stop there: same legal entity. Everything else is corroboration or
operational data.

## 2. Decision points

### 2a. Identity verification

The TIN match is the primary key. The bank account match (Chase ****4521
on both) is corroborating — same payment instructions reduces the
chance these are two divisions of the same parent maintained
intentionally separate. The address match (100 Main St / 100 Main
Street, same city/state/ZIP) is a third corroborator.

**My confidence threshold for declaring a duplicate:** TIN match alone
is sufficient *unless* there's a known reason for a single TIN to span
two records (some IT systems split disregarded-entity LLCs from their
parent for 1099 routing reasons — but the bank account match here rules
that out). With TIN + bank + address all matching, this is high-
confidence dedupe.

> [AI DRAFT — practitioner: do you ever validate TIN match against the IRS TIN matching service before merging? Add that step if so.]

### 2b. Survivor selection

Three rules in order:

1. **Active record wins over dormant** — Record A had activity 30 days
   ago; Record B's last activity was 18 months ago. Record A is the
   live relationship; merging into B would force a data migration on
   the live side which is unnecessary risk.
2. **More complete record wins** — Record A includes "Suite 200" in
   the address; Record B doesn't. Other things equal, retain the more
   complete record.
3. **Older record wins (audit lineage)** when the first two rules don't
   pick a winner — a longer-running record has more transaction history
   and breaking that lineage costs reporting continuity.

Survivor = Record A.

### 2c. Pre-deactivation hygiene (the part models miss)

This is where the Claude family lost points across the board. Before
flipping Record B inactive, three control steps:

1. **Migrate open documents from B to A.** Re-point any open POs,
   in-flight invoices, payment runs, and contracts that reference
   Record B's vendor ID over to Record A. Get sign-off from the
   buyer/contract owner on each migration. Don't just deactivate B
   under live POs — that breaks the AP path on the next invoice.

2. **Run a duplicate-payment lookback across both record IDs over
   the last 18 months.** Same amounts within ±$1, same invoice numbers
   (with normalization for prefix/suffix variants), same dates within
   a 30-day window. If anything pops, that's a payment to investigate
   *before* consolidating — once you merge, the trail gets harder to
   follow. The 18-month window matches Record B's dormancy period;
   choose the longer of (Record B's lifespan) and (your firm's
   standard lookback window — typically 24 months for SOX
   workpapers).

3. **Check bank-account history on both records.** Even though
   currently both show ****4521, was there ever a divergence? A
   period where Record B's bank was different is a fraud-screen
   indicator — someone may have been routing payments to a side bank
   account before you started looking. Pull the bank-change audit log
   for both vendor IDs.

### 2d. Documentation

Write down:
- Both vendor IDs and the canonical name of the surviving record.
- Why this consolidation was triggered (master-data review? new
  invoice from B's ID surfaced? duplicate-payment hit?).
- The TIN/bank/address match findings as evidence.
- Open-document migration list with buyer sign-offs.
- Lookback results (clean / hits investigated / outcome).
- Approver chain — clerk who proposed, supervisor who approved,
  master-data steward who executed.

This documentation is what gets sampled in the next SOX vendor-master
walkthrough.

## 3. Heuristics — the rules of thumb

> [AI DRAFT — practitioner: rewrite from your real working knowledge.]

- **Bank account history is the fraud signal, not the dedupe signal.**
  When a bank account on a "duplicate" was changed within 30 days of
  the record going dormant, that's a fraud indicator not a cleanup
  task — escalate before consolidating.
- **Same TIN, different legal entity types (Inc vs LLC) usually means
  reorganization.** Don't merge — link as related parties. The IRS
  treats them as separate for tax purposes even if they share an EIN
  during a transition window.
- **A dormant record with a current TIN and current bank but no recent
  activity is more suspicious than an active duplicate.** Could be
  shelf-keeping for a side payment scheme.
- [Practitioner: add 2-4 more from your real experience]

## 4. Edge cases — what would change my recommendation

> [AI DRAFT — practitioner: rewrite. Real edge cases are the most valuable SFT content.]

- **Different DBAs with separate state tax registrations under one
  EIN.** They're the same federal entity but file separately at state
  level. Don't merge in master; link via parent.
- **One record has an active dispute or audit hold.** Do nothing until
  resolved — merging during an open issue contaminates the
  investigation record.
- **The dormant record has open contracts that haven't been billed
  against in the dormancy period.** Confirm contract status with legal
  before deactivating; some contracts auto-renew and a missed billing
  doesn't mean the contract closed.
- [Practitioner: add 1-2 more]

## 5. Communication

If you have to communicate the consolidation outward:

- **To the supplier:** "We've consolidated your vendor records in our
  system. All future invoices should reference [Record A's vendor ID].
  No change to remit-to information or payment terms."
- **To internal AP team:** notification that vendor ID [B] is being
  inactivated and to re-route any held items to vendor ID [A].
- **To the buyer who owns the active relationship:** confirmation
  that Record A is the surviving record and any open documents have
  been migrated.

## 6. Why models miss this

> [AI DRAFT — practitioner-optional]

The frontier models all correctly identified the TIN match and the
need for survivor selection. Where they uniformly lost points was on
the *pre-deactivation control sweep* — specifically the duplicate-
payment lookback. My read: the dedupe pattern is well-represented in
training data (it's basic master-data hygiene), but the *control-step
sequence* (lookback → migrate → deactivate, in that order, with
documentation) is procedural knowledge that comes from working in a
SOX-controlled AP function, not from textbooks. The training data has
"how to detect duplicates" but not "what control hygiene a senior AP
person runs before merging."

---

## How to convert into the q_001 ideal_answer field

Same as q_003 — concatenate sections 1-6, paste into `data/questions.json`,
`refresh-questions`, re-autoscore.
