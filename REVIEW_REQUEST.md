# ProfBench external SME review request

ProfBench v0.3 is a domain-specific LLM benchmark for procurement / source-to-pay
reasoning, modeled on the [FinanceQA](https://huggingface.co/datasets/AfterQuery/FinanceQA)
methodology (Mateega, Georgescu, Tang — AfterQuery, 2025). It contains 18
expert-style questions with rubrics, ideal answers, and reasoning-trace drafts
for q_001, q_003, q_010.

The author has operational depth in `supplier_data` and procurement-operations
sub-domains and **shallower depth in `trade_and_tax` and `close_and_controls`**.
Where working experience does not extend, the reasoning-trace drafts in
[`data/traces/`](data/traces/) are written in **cited-authority style** —
anchored to PCAOB AS 2201, COSO 2013, OFAC FAQ, FinCEN BOI, IRS Pub 1281/515,
Incoterms 2020 (ICC 723E), and ACFE *Report to the Nations* — rather than to
working-practitioner voice.

This is eval-defensible (a model that fails to apply named primary sources
demonstrably underperforms) but a **knowingly weaker substitute for AfterQuery-
grade SFT data**, which depends on practitioner heuristics, idiosyncratic edge
cases, and "what I actually do first when this hits my queue" content that
primary sources cannot supply. See
[METHODOLOGY.md § Authorship constraint](METHODOLOGY.md#authorship-constraint)
for the full framing.

This document is the structured ask for external SME review.

---

## What review would change

A practitioner-voice pass on a cited-authority trace upgrades it from
"eval-defensible answer" to "AfterQuery-pipeline SFT candidate." The two
sections that move the most:

- **Section 3 — Working heuristics.** Currently anchored to ACFE / AICPA
  framework material. Practitioners' rolodex content (the heuristics they
  actually use day-to-day, the patterns they have learned to flag, the
  shortcuts that aren't in any policy doc) is the highest-value addition.
- **Section 4 — Edge cases.** Currently covers standard exception classes
  derivable from framework material. Real edge cases from practitioners'
  investigation history are what frontier models cannot pattern-match — and
  therefore where the benchmark's discriminative value is highest.

Sections 1, 2, 5, 6 are framework material that holds up under cited-authority
authorship. Reviewers can mark them `[OK as drafted]` if they pass professional
inspection.

---

## Per-question status and what we are asking for

| ID | Category | Difficulty | Trace status | Strongest review need |
|---|---|---|---|---|
| q_001 | supplier_data | easy | [Cited authority](data/traces/q_001_trace.md) | Section 3 heuristics — TIN matching workflows, dormant-record fraud signals |
| q_002 | invoice_processing | easy | No trace yet | After-the-fact PO controls, legal engagement-letter-as-PO conditions |
| q_003 | invoice_processing | medium | [Cited authority](data/traces/q_003_trace.md) | Section 3-4 — your firm's actual ERP tolerance convention, freight default policy, edge cases from real exception queues |
| q_004 | supplier_data | medium | No trace yet | Duplicate-payment detection rules; cross-vendor pattern matching |
| q_005 | trade_and_tax | medium | No trace yet | FCA Incoterm — what's embedded in price, what's billable separately |
| q_006 | trade_and_tax | hard | No trace yet | W-8 / 1042-S / source-of-income split; nonresident withholding |
| q_007 | trade_and_tax | hard | No trace yet | EU VAT establishment confirmation under Council Implementing Regulation 282/2011 |
| q_008 | close_and_controls | hard | No trace yet | GR/IR aging at period-close; what is and isn't accruable |
| q_009 | supplier_data | hard | No trace yet | OFAC 50% rule; FinCEN BOI under 31 CFR §1010.380; sanctions screening workflows |
| q_010 | close_and_controls | hard | [Cited authority](data/traces/q_010_trace.md) | Section 3-4 — real ghost-vendor detection heuristics; section 5b material-weakness judgment call |
| q_011 | supplier_data | medium | No trace yet | IRS TIN matching workflow application |
| q_012 | invoice_processing | medium | No trace yet | BEC / business-email-compromise defense; control rigor under social engineering |
| q_013 | trade_and_tax | medium | No trace yet | Post-Brexit UK B2B place-of-supply |
| q_014 | trade_and_tax | medium | No trace yet | Canadian GST/HST place-of-supply for exported services |
| q_015 | trade_and_tax | hard | No trace yet | HTS classification + Section 301 tariffs + importer-of-record |
| q_016 | close_and_controls | medium | No trace yet | DPO stock-flow accounting principle |
| q_017 | invoice_processing | medium | No trace yet | Duplicate-vendor vs duplicate-payment distinction (P2P control taxonomy) |
| q_018 | close_and_controls | hard | No trace yet | Control-failure tier hierarchy under SOX (multi-tier diagnosis) |

---

## What a review pass looks like (concrete)

For an existing cited-authority trace (q_001 / q_003 / q_010):

1. Read the full trace.
2. Mark each section `[OK as drafted]` or `[REWRITE]`. The authority-grounded
   structure can stay; the practitioner-voice content goes in §3 / §4 in
   particular.
3. For sections marked `[REWRITE]`, supply the practitioner-voice content
   directly — don't polish, the unpolished version is more useful for SFT
   training data than a cleaned-up paraphrase.
4. Note any factual errors in the cited-authority sections — primary-source
   citations may be approximate (e.g., AS 2201 is named correctly but a specific
   paragraph reference may need correction).
5. Submit edits as a PR or as inline comments on the file.

For a question without a trace yet (q_002, q_004–q_009, q_011–q_018):

1. Read the question, context, ideal answer, and rubric in
   [`data/questions.json`](data/questions.json).
2. Note any factual errors, missing controls, or rubric tier-2 expectations
   that appear miscalibrated.
3. If feasible, draft a 600–1200-word reasoning trace in the same six-section
   structure as the existing traces (see
   [`data/traces/q_003_template.md`](data/traces/q_003_template.md)).

---

## Time commitment

- **Light review** (read + comment, no rewrites): ~20 minutes per question.
- **Medium review** (one section rewritten in practitioner voice):
  ~45–60 minutes per question.
- **Heavy review** (full trace authored from scratch): ~2–3 hours per question.

Even a single light review on a single question is useful. The greatest
marginal value is on q_007 (EU VAT establishment), q_009 (OFAC 50% rule +
FinCEN BOI), q_010 (ghost-vendor / material weakness), q_015 (HTS + Section
301), and q_018 (control-failure tier hierarchy under SOX) — the questions
furthest from the author's working experience.

---

## What reviewers get

- **Public attribution** in the dataset card (Hugging Face) and the repo
  contributors list, on the level of detail you are comfortable with — name
  + employer, name only, role + industry only, or anonymous.
- **Co-authorship** on any AfterQuery / FinanceQA-style submission this
  benchmark contributes to.
- **A reproducible benchmark for your own use:** the harness runs against any
  Anthropic / OpenAI key; you can evaluate any model your team is considering
  on procurement-grade tasks calibrated against your own review.

---

## Outreach templates

Reusable blurbs for the channels most likely to surface qualified reviewers.
Each has been tightened to under 200 words.

### AfterQuery direct submission

> Hi AfterQuery team —
>
> I built ProfBench, an 18-question domain-specific LLM benchmark for
> procurement / source-to-pay reasoning, closely modeled on FinanceQA's
> methodology. Repo: https://github.com/ZacharyTChung/profbench
>
> v0.3 is honestly framed: I am one practitioner with operational depth in
> supplier-data sub-domains and shallower depth in trade-and-tax / SOX
> close-controls. Where my working experience does not extend, the
> reasoning-trace drafts are anchored to primary sources (PCAOB AS 2201,
> COSO 2013, OFAC FAQ, IRS Pub 1281, Incoterms 2020) rather than
> practitioner-voice. This is eval-defensible but a knowingly weaker
> substitute for the AfterQuery-grade SFT data your pipeline produces.
>
> Two specific asks:
>
> 1. Would AfterQuery be open to routing this to one or two SMEs in your
>    network for review of the trade_and_tax and close_and_controls
>    questions? REVIEW_REQUEST.md describes the structured ask.
> 2. Independent of that, is there an AfterQuery contributor path — for me
>    or for the SMEs who review — that I should point reviewers toward?
>
> Happy to share the dataset, the harness, the loss-analysis report, or any
> subset that would help you evaluate fit.

### r/procurement

> **Looking for AP / sourcing folks to sanity-check an LLM benchmark for
> procurement reasoning**
>
> I built [ProfBench](https://github.com/ZacharyTChung/profbench), a
> FinanceQA-style benchmark for procurement / P2P. 18 questions across
> supplier master data, invoice processing, trade and tax, period close
> and SOX controls. All four major Claude models scored on it; the gap
> between Opus 4.7 (83% exact match) and Haiku 4.5 (22%) is real.
>
> What I need: a working-practitioner read on the questions that are
> outside my own depth — Incoterms, EU VAT, OFAC sanctions screening,
> ghost-vendor / SOX material-weakness reasoning. The traces I have for
> those are anchored to primary sources, not to the rolodex content an
> AP director or sanctions analyst would write from memory. That gap is
> what `REVIEW_REQUEST.md` describes.
>
> 20 minutes of your time on a single question would meaningfully improve
> this. Public attribution however you prefer it (name + employer, name
> only, role only, anonymous). Repo and review request linked above.

### AICPA / IIA / ACFE forums

> **Reasoning-quality review request: LLM benchmark for SOX P2P controls**
>
> ProfBench (https://github.com/ZacharyTChung/profbench) is a
> domain-specific LLM benchmark covering supplier-master, invoice-
> processing, cross-border tax, and period-close-and-controls reasoning.
> Modeled on FinanceQA's methodology.
>
> Two questions in particular need professional review from someone with
> SOX P2P controls experience:
>
> - **q_010** — ghost-vendor / structuring / material-weakness analysis
>   under PCAOB AS 2201 and AS 1301. Trace is anchored to AS 2201 / COSO
>   2013 / ACFE *Report to the Nations* / Nigrini *Forensic Analytics*.
>   The §5b "pervasiveness vs isolated" judgment call is the section
>   most in need of a real material-weakness conclusion writer.
> - **q_018** — control-failure tier hierarchy under SOX (deficiency vs
>   significant deficiency vs material weakness). No trace yet; question
>   and rubric in `data/questions.json`.
>
> Happy to acknowledge contributions in the dataset card and any
> downstream submission. Review request structure in `REVIEW_REQUEST.md`.

### LinkedIn — AP / procurement / sanctions-screening groups

> Looking for one or two senior AP / procurement / sanctions-screening
> practitioners to sanity-check a small LLM benchmark for P2P reasoning.
> 18 questions, FinanceQA-style structure, repo at
> https://github.com/ZacharyTChung/profbench.
>
> Honestly framed: my own depth covers supplier-master operations.
> Trade/tax (Incoterms, OFAC 50% rule, FinCEN BOI, EU VAT) and SOX
> close-controls (material-weakness diagnosis, ghost-vendor detection)
> are the areas most in need of working-practitioner review. The trace
> drafts I have are anchored to primary sources rather than to the
> heuristics a working AP director or sanctions analyst would write from
> memory.
>
> 20 minutes on a single question is genuinely useful. Public attribution
> at the level you prefer; happy to discuss before any commitment. DM if
> interested.

---

## Submitting a review

- **PR:** fork the repo, edit the relevant trace or question, open a PR
  against `main`. Link this document in the PR description.
- **Inline comments:** open a GitHub issue referencing the question id
  (e.g., "q_007 review notes") and paste your comments inline. The
  author will fold them into the trace and credit accordingly.
- **Email:** if you would prefer not to use GitHub, contact via the email
  in the repo profile and the author will integrate edits manually.

---

*Document version 1.0 — created in v0.3, 2026-04-30.*
