# Candidate question seeds — v2 expansion (target ~20 new questions)

Focus: the two categories where the v0.1 pilot showed all models leak score
(`supplier_data` 1.17 avg, `trade_and_tax` 1.33 avg, with `trade_and_tax` also
showing the largest spread across models — most discriminative).

Each row is a **seed** — a scenario hook + what it tests + candidate failure
mode. The practitioner authors the full question (scenario + context + ideal
answer + rubric) from each seed. Skip any seed that hits a confidentiality
boundary; replace with one that doesn't.

## supplier_data (10 seeds)

| # | Difficulty | Scenario hook | What it tests | Candidate failure mode |
| --- | --- | --- | --- | --- |
| s_001 | easy | Three vendor records: same legal name, three different bank accounts on file, two of which haven't been used in 2+ years | Recognize that the *active* bank is canonical; the others are remit-to history that should be archived not deleted (audit trail) | retention vs deletion convention |
| s_002 | easy | New vendor request: name + W-9 + bank info — but TIN matching service returns "name/TIN does not match IRS records" | Reject for IRS TIN match failure; do not accept the W-9 as-is; backup withholding consequence if proceeding | IRS TIN match handling |
| s_003 | medium | Existing vendor changes bank account via emailed letter on company letterhead | Reject the emailed change; require independent callback to a known number not on the request; this is the canonical BEC pattern | bank-change verification (BEC defense) |
| s_004 | medium | Vendor portal shows two records: same parent (proven via D&B), different DBAs, different TINs (subsidiaries with separate EINs) | Recognize different EINs = different legal entities even with same parent; do NOT merge; instead link via parent relationship | parent/sub vs dedupe distinction |
| s_005 | medium | Supplier provides updated W-9 with a new TIN, claims they restructured. Old TIN had $80k YTD spend | 1099 reporting requires accurate TIN; spend straddling the change requires either two 1099s (old + new TIN) or amended 1099 logic; need W-9 dated and reason documented | 1099 mid-year TIN change handling |
| s_006 | medium | Supplier address matches an employee's home address (HRIS match) | Hard stop on onboarding; route to internal audit / fraud team; do not approve until explained; possible related-party disclosure issue | employee-vendor collision detection |
| s_007 | hard | Vendor requests payment to a third-party factor (factoring agreement) | Verify factor's NOA (notice of assignment) is on file, signed by vendor; risk of paying both vendor and factor for same invoice; UCC filing check | factoring/assignment of receivables |
| s_008 | hard | Periodic supplier master cleansing: 3,000 vendors, ~12% have had no activity in 24+ months. What's the right deactivation policy? | Different rules for: zero-spend vendors, dormant-with-history vendors, vendors with open POs/contracts; SOX implications for retained controls | master-data lifecycle policy |
| s_009 | hard | Vendor onboarding from a country newly added to FATF grey list (e.g., a hypothetical change effective last quarter) | Enhanced due diligence triggers; updated risk score; existing vendors from that country need re-screen, not just new ones | FATF grey-list dynamic re-screening |
| s_010 | hard | Vendor master shows 27 suppliers with addresses in OFAC-sanctioned countries dating back 10 years; was this caught? | Backward-look screening of legacy master records; whether old activity was sanctions-violating depends on when sanctions came into force; SAR consideration | retroactive sanctions risk on master data |

## trade_and_tax (10 seeds)

| # | Difficulty | Scenario hook | What it tests | Candidate failure mode |
| --- | --- | --- | --- | --- |
| t_001 | easy | DDP from China shipment lands at port; customs broker sends a separate invoice for $4k duty + handling | Under DDP, all duties/handling are seller's responsibility; broker invoice is wrong target; reject and route to seller | Incoterm-specific duty allocation |
| t_002 | easy | Domestic invoice with sales tax charged on a service that's tax-exempt in the buyer's state (e.g., professional services in TX) | Reject the tax line; request corrected invoice; if already paid, file for use-tax credit/refund | sales tax exemption application |
| t_003 | medium | UK supplier invoices a US buyer for SaaS services; supplier added 20% UK VAT | Place of supply for B2B digital services is buyer's country (US); supplier should not have charged UK VAT; out of scope | UK VAT post-Brexit B2B digital services |
| t_004 | medium | German supplier invoice for goods shipped to a US warehouse, reverse-charge mechanism mentioned but supplier added DE VAT anyway | Goods exports from EU to US: zero-rated supply; should have no VAT; reverse-charge concept doesn't apply (that's services); reject | EU goods export zero-rating vs reverse-charge confusion |
| t_005 | medium | Canadian supplier invoice with GST/HST charged; buyer is US-based | GST/HST charged because Canadian POS or Canadian-place-of-supply test; if services consumed in Canada, charge stands; if exported, zero-rated; depends on facts | Canadian GST/HST place-of-supply analysis |
| t_006 | hard | Mexican supplier on a multi-year contract; Mexico introduces a withholding tax change effective next quarter | Apply old rate to invoices with services performed before effective date; new rate after; transition handling; treaty review | mid-contract treaty/withholding rate changes |
| t_007 | hard | Indian supplier; invoice is 90 days old; Indian GST e-invoicing requires real-time IRN (Invoice Reference Number) | Verify IRN was generated within statutory window; if missed, invoice may not be valid for ITC; reject and request reissue | India e-invoicing IRN compliance |
| t_008 | hard | Section 301 tariff applies to goods classified under HTS 8541 imported from China; supplier didn't include tariff line on invoice | Tariff is buyer's cost (paid to CBP, not supplier); does NOT belong on supplier invoice; verify HTS classification independently; FTZ / drawback opportunities | HTS classification + Section 301 tariffs |
| t_009 | hard | Multi-jurisdiction transfer pricing: parent invoices subsidiary for management services; arm's-length comparable required | Documentation requirement (transfer pricing study); BEPS local file / master file; treaty MAP procedure if dispute | transfer pricing documentation |
| t_010 | hard | DAP shipment from Korea to US warehouse, but supplier hands off to buyer's freight forwarder at Busan port (clearly not "delivered at place" — "delivered at terminal") | Wrong Incoterm in use; should be FCA Busan or CPT; cost allocation has to follow the *actual* transaction not the document; recommend correcting the contract | Incoterm misapplication detection |

## How to use these

1. Pick a seed.
2. Author the full question following the schema in `data/questions.json`:
   - `id` — `q_011`, `q_012`, ... in continuation of the existing series
   - `domain` — `procurement`
   - `category` — `supplier_data` or `trade_and_tax`
   - `difficulty` — as listed
   - `question` — the practitioner-style ask
   - `context` — synthesized table/details (no employer-real numbers)
   - `ideal_answer` — your reasoning trace (use `data/traces/` template format)
   - `rubric` — 0/1/2 with concrete tier definitions
   - `expected_failure_mode` — short label for the loss taxonomy
3. `python -m runner.eval refresh-questions` to load.
4. Re-run the eval against the new question(s).

## Expected impact on the benchmark

If you author all 20, the question count goes from 10 → 30, hitting the
typical Market-Bench-submission threshold. The category mix becomes:

- `supplier_data`: 2 → 12 (most data-rich category in the benchmark)
- `invoice_processing`: 3 → 3
- `trade_and_tax`: 3 → 13 (most discriminative category)
- `close_and_controls`: 2 → 2

That's a deliberately imbalanced mix toward where models leak score. Adjust if
you want even coverage.
