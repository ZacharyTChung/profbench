"""Hugging Face-ready dataset export.

Writes ``data/profbench_export.json`` with metadata, the question bank,
the responses for one run, and any scores attached to those responses.

CLI::

    python -m data.export --run-id <id>
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from runner import PROJECT_ROOT, get_db, init_db, now_iso

app = typer.Typer(help="Hugging Face-ready dataset export")
console = Console()

EXPORT_PATH = PROJECT_ROOT / "data" / "profbench_export.json"

VERSION = "0.1.0"
DATASET_NAME = "ProfBench"


def _load_questions() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM questions ORDER BY id").fetchall()
    out = []
    for r in rows:
        d = dict(r)
        try:
            d["rubric"] = json.loads(d["rubric"]) if d["rubric"] else {}
        except json.JSONDecodeError:
            d["rubric"] = {}
        out.append(d)
    return out


def _load_run(run_id: str) -> tuple[list[dict], list[dict]]:
    with get_db() as conn:
        responses = [
            dict(r)
            for r in conn.execute(
                "SELECT * FROM responses WHERE run_id = ? ORDER BY question_id, model",
                (run_id,),
            ).fetchall()
        ]
        scores: list[dict] = []
        if responses:
            placeholders = ",".join("?" for _ in responses)
            response_ids = [r["id"] for r in responses]
            scores = [
                dict(r)
                for r in conn.execute(
                    f"SELECT * FROM scores WHERE response_id IN ({placeholders}) "
                    f"ORDER BY response_id, scorer_type",
                    response_ids,
                ).fetchall()
            ]
            for s in scores:
                if s.get("scorer_notes"):
                    try:
                        s["scorer_notes"] = json.loads(s["scorer_notes"])
                    except (json.JSONDecodeError, TypeError):
                        pass
    return responses, scores


@app.command("export")
def export_cmd(
    run_id: Optional[str] = typer.Option(
        None, "--run-id", help="Run UUID to include. Omit to export questions only."
    ),
    output: Path = typer.Option(EXPORT_PATH, "--output"),
) -> None:
    """Write the Hugging Face-ready export."""
    init_db()
    questions = _load_questions()
    categories = sorted({q["category"] for q in questions if q.get("category")})
    domain = next((q["domain"] for q in questions if q.get("domain")), "[DOMAIN]")

    responses: list[dict] = []
    scores: list[dict] = []
    models_evaluated: list[str] = []
    if run_id:
        responses, scores = _load_run(run_id)
        models_evaluated = sorted({r["model"] for r in responses})

    payload = {
        "metadata": {
            "name": DATASET_NAME,
            "domain": domain,
            "version": VERSION,
            "num_questions": len(questions),
            "categories": categories,
            "created_at": now_iso(),
        },
        "questions": questions,
        "results": {
            "run_id": run_id or "",
            "models_evaluated": models_evaluated,
            "responses": responses,
            "scores": scores,
        },
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    console.print(
        f"[green]Wrote[/green] {output} "
        f"(questions={len(questions)}, responses={len(responses)}, scores={len(scores)})"
    )


if __name__ == "__main__":
    app()
