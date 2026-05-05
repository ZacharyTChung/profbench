# q_016 reasoning trace — cited-authority draft

> **Cited-authority draft, not practitioner-voice.** Per
> [METHODOLOGY.md § Authorship constraint](../../METHODOLOGY.md#authorship-constraint).
> Anchored to standard corporate-finance textbook treatment of
> stock-flow reconciliation: **Koller, Goedhart & Wessels,
> *Valuation: Measuring and Managing the Value of Companies*** (7th
> ed.), and **Holthausen & Zmijewski, *Corporate Valuation: Theory,
> Evidence & Practice*** (2nd ed.). This is a **conceptual** question
> with no practitioner-voice gap — the answer is principled, not
> rolodex-derived.

## 1. The principle

**DPO uses the average accounts-payable balance because it
reconciles a stock measure (AP, a balance-sheet item) with a flow
measure (purchases or COGS, an income-statement item).**

The stock-flow distinction is the foundational concept:

- **Stock measure (AP)** — a balance at a point in time. Like the
  amount of water in a tank at noon.
- **Flow measure (purchases or COGS)** — a quantity accumulated over
  a period. Like the volume of water that flowed through the tank
  between January and December.

A ratio that mixes the two (DPO = AP / purchases × days) only makes
sense if both terms refer to the same period. The stock measure has
to be transformed into something comparable.

## 2. Why averaging

The averaging convention represents **the typical balance carried
across the period**, which is the stock-equivalent of the flow.

Two specific failure modes that averaging prevents:

1. **End-of-period distortion from one-time events.** If the firm
   front-loaded payments at year-end (clearing the AP balance to
   present a healthy working-capital picture), the ending AP
   balance would understate the typical balance carried during the
   year. Using ending AP would make DPO look artificially low —
   suggesting faster payment cycles than the firm actually ran.
2. **Seasonal swings.** A retailer with a Christmas-quarter buildup
   and a January wind-down has very different AP balances in
   different months. Either ending balance (Q4 high or Q1 low)
   would mis-represent the year. The annual average is the
   meaningful comparison.

## 3. The same convention applies to other stock-flow ratios

The averaging convention isn't specific to DPO — it's the general
treatment for any ratio mixing balance-sheet and income-statement
quantities:

- **DSO** (Days Sales Outstanding) uses average accounts receivable.
- **DIO** (Days Inventory Outstanding) uses average inventory.
- **Asset turnover** uses average total assets.
- **Return on assets, return on equity** use average asset / equity
  balances.

Any of these computed against ending balances rather than averages
embeds the same end-of-period distortion.

## 4. The exception: when ending balance is fine

Where the comparison is **point-in-time**, not flow-based — for
example, "what was the AP balance on December 31?" — ending balance
is correct because no flow comparison is being made. The averaging
convention only matters when reconciling a stock to a flow.

## 5. Mathematical formulation

The general formula:

```
DPO = (Average AP / Annual Purchases) × 365
```

Where Average AP is typically computed as `(Beginning AP + Ending
AP) / 2` for annual analysis, or the simple average of monthly /
quarterly balances for finer-grained analysis. The latter is more
robust when the firm has material seasonality.

## 6. Practical implications

- Comparing two firms' DPO using ending AP can produce spurious
  rankings if one firm front-loads payments at year-end.
- Trend analysis on a firm's own DPO over time using ending AP can
  manufacture a "trend" that's actually period-end behavior.
- The averaging convention is mechanical and not analytically
  controversial — auditors, equity analysts, and credit analysts
  all default to it.

## 7. Why the question matters

The stock-flow question reveals whether the responder understands
the mathematical structure of the ratio. A response that produces
the formula correctly but uses ending AP when computing DPO is
operationally wrong; a response that articulates the principle is
operationally correct and shows the underlying mental model. The
distinction generalizes — anyone who internalizes the stock-flow
convention applies it consistently across DSO, DIO, asset turnover,
etc.
