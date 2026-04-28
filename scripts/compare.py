"""Build a side-by-side review file for a run.

Writes ``analysis/comparison_<run_id>.md`` showing, per question:
  - question + context
  - the ideal answer
  - the model's actual response
  - the grader's score and reasoning

Use this to decide, for each non-2 score, whether (a) the model genuinely
fell short, (b) the ideal_answer was too narrow, or (c) the rubric is
miscalibrated. Only (b) and (c) justify editing data/questions.json.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "profbench.db"
OUT_DIR = ROOT / "analysis"


def build(run_id: str, only_score: int | None = None) -> Path:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    sql = """
        SELECT q.id, q.category, q.difficulty, q.question, q.context,
               q.ideal_answer, q.rubric, q.expected_failure_mode,
               r.model, r.response, s.score, s.scorer_notes
        FROM responses r
        JOIN questions q ON q.id = r.question_id
        LEFT JOIN scores s ON s.response_id = r.id AND s.scorer_type = 'auto'
        WHERE r.run_id = ?
        ORDER BY s.score ASC, q.id ASC
    """
    rows = conn.execute(sql, (run_id,)).fetchall()
    if only_score is not None:
        rows = [r for r in rows if r["score"] == only_score]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = f"_score{only_score}" if only_score is not None else ""
    out = OUT_DIR / f"comparison_{run_id[:8]}{suffix}.md"

    lines: list[str] = [
        f"# ProfBench comparison — run `{run_id}`",
        "",
        "For each question below: read the model's response next to the ideal "
        "answer, then categorize:",
        "",
        "- **(a) model fell short** — keep the question, score is honest",
        "- **(b) ideal_answer too narrow** — the model's response is actually "
        "acceptable; broaden the ideal answer (do not change the question)",
        "- **(c) rubric miscalibrated** — tier definitions need to be more "
        "specific so the grader doesn't mark partial answers down unfairly",
        "",
        "Only (b) and (c) justify editing `data/questions.json`. (a) is the "
        "benchmark working as intended.",
        "",
        "---",
        "",
    ]

    for r in rows:
        notes = json.loads(r["scorer_notes"]) if r["scorer_notes"] else {}
        rubric = json.loads(r["rubric"]) if r["rubric"] else {}

        lines += [
            f"## {r['id']} — {r['category']} · {r['difficulty']} · "
            f"**score {r['score']}/2** (model: `{r['model']}`)",
            "",
            f"_Expected failure mode: {r['expected_failure_mode']}_",
            "",
            "### Question",
            "",
            r["question"],
            "",
        ]
        if r["context"]:
            lines += ["### Context", "", "```", r["context"], "```", ""]

        lines += [
            "### Rubric",
            "",
            *[f"- **{k}**: {v}" for k, v in rubric.items()],
            "",
            "### Ideal answer",
            "",
            r["ideal_answer"] or "_(none)_",
            "",
            "### Model response",
            "",
            r["response"] or "_(empty)_",
            "",
            "### Grader verdict",
            "",
            f"- **Score:** {r['score']}",
            f"- **Confidence:** {notes.get('confidence','?')}",
            f"- **Reasoning:** {notes.get('reasoning','(none)')}",
            "",
            "### Decision (fill in)",
            "",
            "_(a) model fell short / (b) ideal too narrow / (c) rubric miscalibrated_",
            "",
            "---",
            "",
        ]

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python scripts/compare.py <run_id> [score_filter]", file=sys.stderr)
        sys.exit(2)
    run_id = sys.argv[1]
    score_filter = int(sys.argv[2]) if len(sys.argv) > 2 else None
    out = build(run_id, score_filter)
    print(f"wrote {out}")
