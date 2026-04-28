"""Score aggregation utilities.

Pure functions that read from the SQLite database and return clean
dataframes / dicts. No printing, no file writes — those belong in
``analysis/report.py`` and ``leaderboard/generate.py``.

Aggregations cover: per-model average score, per-category breakdown,
per-difficulty breakdown, expected-failure-mode frequency for the
score=0 bucket, the 0/1/2 distribution histogram, and inter-rater
agreement when both human and auto scores exist.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

from runner import get_db

MAX_SCORE = 2


def _scores_dataframe(run_id: Optional[str], scorer_type: Optional[str]) -> pd.DataFrame:
    """Pull the joined scores/responses/questions table into a dataframe."""
    sql = """
        SELECT s.id              AS score_id,
               s.response_id     AS response_id,
               s.question_id     AS question_id,
               s.model           AS model,
               s.score           AS score,
               s.scorer_type     AS scorer_type,
               s.created_at      AS scored_at,
               r.run_id          AS run_id,
               q.category        AS category,
               q.difficulty      AS difficulty,
               q.expected_failure_mode AS expected_failure_mode
          FROM scores s
          JOIN responses r ON r.id = s.response_id
          JOIN questions q ON q.id = s.question_id
    """
    params: list = []
    where: list[str] = []
    if run_id:
        where.append("r.run_id = ?")
        params.append(run_id)
    if scorer_type:
        where.append("s.scorer_type = ?")
        params.append(scorer_type)
    if where:
        sql += " WHERE " + " AND ".join(where)
    with get_db() as conn:
        df = pd.read_sql_query(sql, conn, params=params)
    return df


def per_model_average(run_id: Optional[str] = None,
                      scorer_type: Optional[str] = None) -> pd.DataFrame:
    """Average score per model on a 0–2 scale, plus % of max."""
    df = _scores_dataframe(run_id, scorer_type)
    if df.empty:
        return pd.DataFrame(columns=["model", "n", "avg_score", "pct_of_max"])
    grp = (
        df.groupby("model")["score"]
        .agg(n="count", avg_score="mean")
        .reset_index()
    )
    grp["pct_of_max"] = (grp["avg_score"] / MAX_SCORE * 100).round(1)
    grp["avg_score"] = grp["avg_score"].round(3)
    return grp.sort_values("avg_score", ascending=False).reset_index(drop=True)


def per_category(run_id: Optional[str] = None,
                 scorer_type: Optional[str] = None) -> pd.DataFrame:
    """Mean score per (model, category)."""
    df = _scores_dataframe(run_id, scorer_type)
    if df.empty:
        return pd.DataFrame(columns=["model", "category", "n", "avg_score"])
    grp = (
        df.groupby(["model", "category"])["score"]
        .agg(n="count", avg_score="mean")
        .reset_index()
    )
    grp["avg_score"] = grp["avg_score"].round(3)
    return grp


def per_difficulty(run_id: Optional[str] = None,
                   scorer_type: Optional[str] = None) -> pd.DataFrame:
    """Mean score per (model, difficulty)."""
    df = _scores_dataframe(run_id, scorer_type)
    if df.empty:
        return pd.DataFrame(columns=["model", "difficulty", "n", "avg_score"])
    grp = (
        df.groupby(["model", "difficulty"])["score"]
        .agg(n="count", avg_score="mean")
        .reset_index()
    )
    grp["avg_score"] = grp["avg_score"].round(3)
    return grp


def failure_mode_frequency(run_id: Optional[str] = None,
                           scorer_type: Optional[str] = None) -> pd.DataFrame:
    """Count of score=0 responses grouped by expected_failure_mode and model."""
    df = _scores_dataframe(run_id, scorer_type)
    if df.empty:
        return pd.DataFrame(columns=["model", "expected_failure_mode", "zero_count"])
    zeros = df[df["score"] == 0]
    if zeros.empty:
        return pd.DataFrame(columns=["model", "expected_failure_mode", "zero_count"])
    grp = (
        zeros.groupby(["model", "expected_failure_mode"])
        .size()
        .reset_index(name="zero_count")
        .sort_values(["model", "zero_count"], ascending=[True, False])
        .reset_index(drop=True)
    )
    return grp


def score_distribution(run_id: Optional[str] = None,
                       scorer_type: Optional[str] = None) -> pd.DataFrame:
    """Histogram of 0/1/2 scores per model."""
    df = _scores_dataframe(run_id, scorer_type)
    if df.empty:
        return pd.DataFrame(columns=["model", "score_0", "score_1", "score_2"])
    pivot = (
        df.pivot_table(
            index="model", columns="score", values="score_id",
            aggfunc="count", fill_value=0,
        )
        .rename(columns={0: "score_0", 1: "score_1", 2: "score_2"})
        .reset_index()
    )
    for col in ("score_0", "score_1", "score_2"):
        if col not in pivot.columns:
            pivot[col] = 0
    return pivot[["model", "score_0", "score_1", "score_2"]]


def inter_rater_agreement(run_id: Optional[str] = None) -> dict:
    """Compare human vs auto scores on the same response_id.

    Returns ``{n, exact_match, within_one, mean_abs_diff}``.
    """
    df = _scores_dataframe(run_id, scorer_type=None)
    if df.empty:
        return {"n": 0, "exact_match": None, "within_one": None, "mean_abs_diff": None}

    pivoted = df.pivot_table(
        index="response_id", columns="scorer_type",
        values="score", aggfunc="mean",
    )
    if "human" not in pivoted.columns or "auto" not in pivoted.columns:
        return {"n": 0, "exact_match": None, "within_one": None, "mean_abs_diff": None}
    both = pivoted.dropna(subset=["human", "auto"])
    n = len(both)
    if n == 0:
        return {"n": 0, "exact_match": None, "within_one": None, "mean_abs_diff": None}
    diffs = (both["human"] - both["auto"]).abs()
    return {
        "n": int(n),
        "exact_match": round(float((diffs == 0).mean()), 3),
        "within_one": round(float((diffs <= 1).mean()), 3),
        "mean_abs_diff": round(float(diffs.mean()), 3),
    }


def example_failures(run_id: Optional[str] = None,
                     limit_per_mode: int = 2) -> pd.DataFrame:
    """For each failure mode, return up to N example question_ids that scored 0."""
    df = _scores_dataframe(run_id, scorer_type=None)
    if df.empty:
        return pd.DataFrame(columns=["expected_failure_mode", "model", "question_id"])
    zeros = df[df["score"] == 0][
        ["expected_failure_mode", "model", "question_id"]
    ].drop_duplicates()
    return (
        zeros.groupby("expected_failure_mode", group_keys=False)
        .head(limit_per_mode)
        .reset_index(drop=True)
    )
