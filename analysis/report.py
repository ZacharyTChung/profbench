"""Generate a markdown loss-analysis report.

Produces ``analysis/loss_report.md`` with: an executive summary, a model
× category score table, a failure-mode taxonomy (top failure modes ranked
by frequency, with example questions), per-model observations, and a
templated "implications" section the user fills in with training-data
suggestions.

CLI::

    python -m analysis.report --run-id <id>
    python -m analysis.report --run-id <id> --scorer human
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from analysis import stats
from runner import PROJECT_ROOT, now_iso

app = typer.Typer(help="Loss-analysis report generator")
console = Console()

REPORT_PATH = PROJECT_ROOT / "analysis" / "loss_report.md"


def _df_to_md(df, *, empty_msg: str = "_no data_") -> str:
    if df is None or df.empty:
        return empty_msg
    return df.to_markdown(index=False)


def _executive_summary(per_model_df) -> str:
    if per_model_df.empty:
        return "_No scores recorded yet — run the eval and score responses to populate this section._"
    top = per_model_df.iloc[0]
    if len(per_model_df) >= 2:
        runner_up = per_model_df.iloc[1]
        gap = round(float(top["avg_score"]) - float(runner_up["avg_score"]), 3)
        return (
            f"**{top['model']}** leads with an average score of "
            f"**{top['avg_score']}** ({top['pct_of_max']}% of max). "
            f"The next-best model, **{runner_up['model']}**, trails by **{gap}** "
            f"on a 0–2 scale ({runner_up['avg_score']}, {runner_up['pct_of_max']}% of max)."
        )
    return (
        f"Only one model has recorded scores: **{top['model']}** with an average of "
        f"**{top['avg_score']}** ({top['pct_of_max']}% of max). Add a second model to "
        f"populate a comparative leaderboard."
    )


def _failure_taxonomy(failure_df, examples_df) -> str:
    if failure_df.empty:
        return "_No score=0 responses recorded yet._"
    lines: list[str] = []
    lines.append("| Rank | Failure mode | Model | Score=0 count | Example question(s) |")
    lines.append("| ---- | ------------ | ----- | ------------- | ------------------- |")
    failure_df = failure_df.sort_values(
        ["zero_count", "expected_failure_mode"], ascending=[False, True]
    ).reset_index(drop=True)
    for rank, row in failure_df.iterrows():
        examples = examples_df[
            (examples_df["expected_failure_mode"] == row["expected_failure_mode"])
            & (examples_df["model"] == row["model"])
        ]["question_id"].tolist()
        examples_str = ", ".join(f"`{qid}`" for qid in examples) if examples else "—"
        mode_label = row["expected_failure_mode"] or "_unspecified_"
        lines.append(
            f"| {rank + 1} | {mode_label} | `{row['model']}` "
            f"| {row['zero_count']} | {examples_str} |"
        )
    return "\n".join(lines)


def _implications(per_model_df, per_cat_df, dist_df, failure_df) -> str:
    """Auto-derive implications from the actual data instead of leaving a stub."""
    if per_model_df.empty:
        return "_No data yet — implications cannot be derived._"

    lines: list[str] = []

    # Universal weak categories (avg < 1.5 across all evaluated models).
    if not per_cat_df.empty:
        cat_means = per_cat_df.groupby("category")["avg_score"].mean().sort_values()
        weak_cats = cat_means[cat_means < 1.5]
        if not weak_cats.empty:
            cat_list = ", ".join(f"`{c}` (avg {v:.2f})" for c, v in weak_cats.items())
            lines.append(
                f"- **Domain-level weak categories** (mean across all models < 1.5): "
                f"{cat_list}. These are where the benchmark is doing real work — "
                f"all models leak score here, so additional training data and rubric "
                f"depth in these categories has the highest leverage."
            )

    # Categories where the score *spread* across models is highest — most discriminating.
    if not per_cat_df.empty and per_cat_df["model"].nunique() >= 2:
        spreads = (
            per_cat_df.groupby("category")["avg_score"]
            .agg(lambda s: float(s.max() - s.min()))
            .sort_values(ascending=False)
        )
        top = spreads.head(2)
        if not top.empty and top.iloc[0] > 0.4:
            spread_list = ", ".join(f"`{c}` (spread {v:.2f})" for c, v in top.items())
            lines.append(
                f"- **Most discriminating categories** (largest score spread across "
                f"models): {spread_list}. These categories separate frontier from "
                f"smaller models and are the strongest candidates for an evaluation-only "
                f"public release."
            )

    # Top failure mode by zero count.
    if not failure_df.empty:
        top_failure = failure_df.sort_values("zero_count", ascending=False).iloc[0]
        mode = top_failure["expected_failure_mode"] or "_unspecified_"
        lines.append(
            f"- **Highest-volume failure mode:** _{mode}_ "
            f"({int(top_failure['zero_count'])} score=0 occurrences). "
            f"Targeted training data should prioritize worked examples in this mode."
        )

    # Per-model gap to ceiling.
    top_row = per_model_df.iloc[0]
    if float(top_row["avg_score"]) < 1.9:
        gap = round(2.0 - float(top_row["avg_score"]), 3)
        lines.append(
            f"- **Headroom for the leading model** (`{top_row['model']}`): "
            f"{gap} points to ceiling. Calibrate the rubric (`scripts/compare.py`) "
            f"before declaring this a true gap — score=1 responses may be rubric-too-narrow."
        )

    # Score-1 share — calibration prompt.
    if not dist_df.empty:
        ones = dist_df["score_1"].sum()
        total = (dist_df["score_0"] + dist_df["score_1"] + dist_df["score_2"]).sum()
        if total > 0 and ones / total > 0.2:
            pct = round(100 * ones / total, 1)
            lines.append(
                f"- **Score=1 share is {pct}% of all gradings** — calibration "
                f"recommended. Run `python scripts/compare.py <run_id> 1` and triage "
                f"each as (a) genuine model failure, (b) ideal_answer too narrow, "
                f"or (c) rubric miscalibrated. Edits in (b)/(c) materially change the "
                f"shape of the loss taxonomy above."
            )

    # Annotation-budget heuristic: rough rule of thumb.
    n_questions = (
        per_model_df.iloc[0]["n"] if not per_model_df.empty else 0
    )
    if n_questions and n_questions < 30:
        lines.append(
            f"- **Annotation budget:** current pilot is **n={n_questions}** "
            f"questions. To move from a pilot to a defensible Market-Bench-style "
            f"submission, target 30–50 questions minimum — focus expansion on the "
            f"weak categories above."
        )

    if not lines:
        return "_Implications could not be derived from the current run; expand model coverage and try again._"
    return "\n".join(lines)


def _per_model_observations(per_model_df, per_cat_df, dist_df) -> str:
    if per_model_df.empty:
        return "_No model results yet._"
    sections: list[str] = []
    for _, row in per_model_df.iterrows():
        m = row["model"]
        cat_for_model = per_cat_df[per_cat_df["model"] == m].sort_values(
            "avg_score", ascending=False
        )
        if cat_for_model.empty:
            best = worst = None
        else:
            best = cat_for_model.iloc[0]
            worst = cat_for_model.iloc[-1]

        dist_row = dist_df[dist_df["model"] == m]
        if not dist_row.empty:
            d = dist_row.iloc[0]
            dist_str = (
                f"distribution → 0s: {d['score_0']}, 1s: {d['score_1']}, 2s: {d['score_2']}"
            )
        else:
            dist_str = "distribution: (no data)"

        bullets = [
            f"- Average score **{row['avg_score']}** "
            f"({row['pct_of_max']}% of max), n={row['n']}.",
            f"- {dist_str}.",
        ]
        if best is not None and worst is not None and best["category"] != worst["category"]:
            bullets.append(
                f"- Strongest category: **{best['category']}** "
                f"(avg {best['avg_score']}). Weakest: **{worst['category']}** "
                f"(avg {worst['avg_score']})."
            )
        sections.append(f"### `{m}`\n" + "\n".join(bullets))
    return "\n\n".join(sections)


@app.command("generate")
def generate_cmd(
    run_id: str = typer.Option(..., "--run-id", help="Run UUID to analyze."),
    scorer: Optional[str] = typer.Option(
        None, "--scorer", help="'human', 'auto', or omit for both."
    ),
    output: Path = typer.Option(REPORT_PATH, "--output", help="Output markdown path."),
) -> None:
    """Build the loss-analysis report."""
    per_model_df = stats.per_model_average(run_id=run_id, scorer_type=scorer)
    per_cat_df = stats.per_category(run_id=run_id, scorer_type=scorer)
    per_diff_df = stats.per_difficulty(run_id=run_id, scorer_type=scorer)
    failure_df = stats.failure_mode_frequency(run_id=run_id, scorer_type=scorer)
    dist_df = stats.score_distribution(run_id=run_id, scorer_type=scorer)
    examples_df = stats.example_failures(run_id=run_id)
    irr = stats.inter_rater_agreement(run_id=run_id)

    sections: list[str] = []
    sections.append(f"# ProfBench loss-analysis report\n")
    sections.append(
        f"_Run `{run_id}` · scorer filter: `{scorer or 'all'}` · generated {now_iso()}_\n"
    )

    sections.append("## Executive summary\n")
    sections.append(_executive_summary(per_model_df))

    sections.append("\n## Score table — per model\n")
    sections.append(_df_to_md(per_model_df))

    sections.append("\n## Score table — model × category\n")
    if per_cat_df.empty:
        sections.append("_no data_")
    else:
        pivot = per_cat_df.pivot(index="model", columns="category", values="avg_score")
        sections.append(pivot.round(3).to_markdown())

    sections.append("\n## Score table — model × difficulty\n")
    if per_diff_df.empty:
        sections.append("_no data_")
    else:
        pivot = per_diff_df.pivot(index="model", columns="difficulty", values="avg_score")
        sections.append(pivot.round(3).to_markdown())

    sections.append("\n## Score distribution (0 / 1 / 2 counts per model)\n")
    sections.append(_df_to_md(dist_df))

    sections.append("\n## Failure taxonomy\n")
    sections.append(_failure_taxonomy(failure_df, examples_df))

    sections.append("\n## Model-specific findings\n")
    sections.append(_per_model_observations(per_model_df, per_cat_df, dist_df))

    sections.append("\n## Inter-rater agreement (human vs. auto)\n")
    if irr["n"] == 0:
        sections.append(
            "_No responses have both human and auto scores yet — "
            "agreement statistics are unavailable._"
        )
    else:
        sections.append(
            f"- Compared n = **{irr['n']}** responses.\n"
            f"- Exact match: **{irr['exact_match']}**\n"
            f"- Within ±1: **{irr['within_one']}**\n"
            f"- Mean absolute difference: **{irr['mean_abs_diff']}**"
        )

    sections.append("\n## Implications\n")
    sections.append(_implications(per_model_df, per_cat_df, dist_df, failure_df))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sections), encoding="utf-8")
    console.print(f"[green]Wrote[/green] {output}")


if __name__ == "__main__":
    app()
