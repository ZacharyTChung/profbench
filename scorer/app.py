"""Streamlit scoring UI for ProfBench.

A reviewer picks a run + model, then steps through model responses one at
a time. The ideal answer is hidden by default — the reviewer scores
against the rubric first, then reveals it for confirmation. Scores are
written to the ``scores`` table with ``scorer_type='human'``.

Run with::

    streamlit run scorer/app.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

# Allow running via ``streamlit run scorer/app.py`` from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from runner import get_db, init_db, now_iso  # noqa: E402


st.set_page_config(page_title="ProfBench scorer", layout="wide")
init_db()


def fetch_runs() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT run_id,
                   MIN(created_at) AS started_at,
                   COUNT(*)        AS responses
            FROM responses
            GROUP BY run_id
            ORDER BY started_at DESC
            """
        ).fetchall()
    return [dict(r) for r in rows]


def fetch_models(run_id: str) -> list[str]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT DISTINCT model FROM responses WHERE run_id = ? ORDER BY model",
            (run_id,),
        ).fetchall()
    return [r["model"] for r in rows]


def fetch_responses(run_id: str, model: str, only_unscored: bool) -> list[dict]:
    sql = """
        SELECT r.id            AS response_id,
               r.question_id   AS question_id,
               r.model         AS model,
               r.response      AS response,
               r.tokens_used   AS tokens_used,
               r.latency_ms    AS latency_ms,
               q.category      AS category,
               q.difficulty    AS difficulty,
               q.question      AS question,
               q.context       AS context,
               q.ideal_answer  AS ideal_answer,
               q.rubric        AS rubric,
               q.expected_failure_mode AS expected_failure_mode,
               (SELECT COUNT(*) FROM scores s
                  WHERE s.response_id = r.id
                    AND s.scorer_type = 'human') AS human_score_count
          FROM responses r
          JOIN questions q ON q.id = r.question_id
         WHERE r.run_id = ? AND r.model = ?
         ORDER BY r.question_id
    """
    with get_db() as conn:
        rows = conn.execute(sql, (run_id, model)).fetchall()
    items = [dict(r) for r in rows]
    if only_unscored:
        items = [it for it in items if it["human_score_count"] == 0]
    return items


def save_score(response_id: int, question_id: str, model: str, score: int, notes: str) -> None:
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO scores (
                response_id, question_id, model, score,
                scorer_type, scorer_notes, created_at
            ) VALUES (?, ?, ?, ?, 'human', ?, ?)
            """,
            (response_id, question_id, model, score, notes, now_iso()),
        )
        conn.commit()


# ──────────────── Sidebar ────────────────

st.sidebar.title("ProfBench scorer")

runs = fetch_runs()
if not runs:
    st.title("ProfBench scorer")
    st.info(
        "No responses to score yet. Run `python -m runner.eval run` first, "
        "then refresh this page."
    )
    st.stop()

run_options = {f"{r['run_id'][:8]}… · {r['started_at']} · {r['responses']} resp": r["run_id"]
               for r in runs}
run_label = st.sidebar.selectbox("Run", list(run_options.keys()))
run_id = run_options[run_label]

models = fetch_models(run_id)
if not models:
    st.warning("This run has no responses yet.")
    st.stop()
model = st.sidebar.selectbox("Model", models)

only_unscored = st.sidebar.checkbox("Unscored only", value=True)

# Total scored / total — independent of the unscored filter so the user always
# sees overall progress.
all_responses = fetch_responses(run_id, model, only_unscored=False)
total = len(all_responses)
scored = sum(1 for r in all_responses if r["human_score_count"] > 0)
st.sidebar.markdown(f"**Progress:** {scored} of {total} scored")
st.sidebar.progress(scored / total if total else 0.0)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Shortcuts:** press `0`, `1`, or `2` to score, then click *Save & Next*."
)

# ──────────────── Main panel ────────────────

queue = fetch_responses(run_id, model, only_unscored)
if not queue:
    st.title("All caught up")
    st.success(
        f"No more responses to score for run `{run_id[:8]}…` and model `{model}`."
    )
    st.stop()

idx_key = f"idx::{run_id}::{model}::{only_unscored}"
if idx_key not in st.session_state:
    st.session_state[idx_key] = 0
idx = min(st.session_state[idx_key], len(queue) - 1)
item = queue[idx]

# Header row.
st.markdown(
    f"### `{item['question_id']}`  ·  "
    f"**{item['category']}**  ·  difficulty: `{item['difficulty']}`  ·  "
    f"failure mode: `{item['expected_failure_mode'] or '—'}`"
)
st.caption(f"Item {idx + 1} of {len(queue)} in queue · model: `{item['model']}`")

st.markdown("#### Question")
st.write(item["question"])

if item["context"]:
    with st.expander("Context", expanded=False):
        st.write(item["context"])

with st.expander("Ideal answer (hidden by default — score first)", expanded=False):
    st.write(item["ideal_answer"] or "_no ideal answer recorded_")

# Rubric.
st.markdown("#### Rubric")
try:
    rubric = json.loads(item["rubric"]) if item["rubric"] else {}
except json.JSONDecodeError:
    rubric = {}
rubric_cols = st.columns(3)
for i, key in enumerate(("0", "1", "2")):
    with rubric_cols[i]:
        st.markdown(f"**{key}**")
        st.caption(rubric.get(key, "—"))

# Model response.
st.markdown("#### Model response")
st.text_area(
    label="response",
    value=item["response"] or "",
    height=320,
    label_visibility="collapsed",
    disabled=True,
)

# Score form.
with st.form(key=f"score_form_{item['response_id']}", clear_on_submit=False):
    score = st.radio("Score", options=[0, 1, 2], horizontal=True, index=1)
    notes = st.text_area("Notes (optional)", value="", height=80)
    cols = st.columns(2)
    save = cols[0].form_submit_button("Save & Next", type="primary")
    skip = cols[1].form_submit_button("Skip")

if save:
    save_score(
        response_id=item["response_id"],
        question_id=item["question_id"],
        model=item["model"],
        score=int(score),
        notes=notes,
    )
    st.session_state[idx_key] = idx + 1
    st.rerun()

if skip:
    st.session_state[idx_key] = idx + 1
    st.rerun()
