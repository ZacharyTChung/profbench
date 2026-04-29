"""CLI eval runner for ProfBench.

Loads questions from ``data/questions.json`` into the SQLite database,
sends each question to one or more configured model clients, and stores
the responses with a shared run UUID. Use ``--dry-run`` to print prompts
without calling any APIs.

Examples
--------
    python -m runner.eval run --dry-run --limit 3
    python -m runner.eval run --models claude
    python -m runner.eval run --models claude,gpt4o --limit 5
    python -m runner.eval list-runs
"""

from __future__ import annotations

import json
import sys
import uuid
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

from runner import QUESTIONS_PATH, get_db, init_db, now_iso
from runner.models import MODEL_REGISTRY, SYSTEM_PROMPT, build_client

app = typer.Typer(help="ProfBench eval runner")
console = Console()


def _load_questions_into_db(refresh: bool = False) -> tuple[int, int]:
    """Read ``data/questions.json`` and load into the ``questions`` table.

    By default, new ids are inserted and existing ids are skipped. When
    ``refresh=True``, existing rows are also updated in place — use this
    after editing question text, ideal_answer, or rubric so the changes
    take effect without bumping ids or wiping the DB.

    Returns ``(inserted, updated)``.
    """
    if not QUESTIONS_PATH.exists():
        console.print(f"[red]questions file not found:[/red] {QUESTIONS_PATH}")
        return 0, 0
    with QUESTIONS_PATH.open("r", encoding="utf-8") as fh:
        items = json.load(fh)

    inserted = 0
    updated = 0
    with get_db() as conn:
        for q in items:
            existing = conn.execute(
                "SELECT 1 FROM questions WHERE id = ?", (q["id"],)
            ).fetchone()
            if existing and not refresh:
                continue
            if existing and refresh:
                conn.execute(
                    """
                    UPDATE questions SET
                        domain = ?, category = ?, difficulty = ?,
                        question = ?, context = ?, ideal_answer = ?,
                        rubric = ?, expected_failure_mode = ?,
                        question_type = ?, requires_assumption = ?,
                        source_grounded = ?, source_doc = ?
                    WHERE id = ?
                    """,
                    (
                        q.get("domain", ""),
                        q.get("category", ""),
                        q.get("difficulty", ""),
                        q["question"],
                        q.get("context", ""),
                        q.get("ideal_answer", ""),
                        json.dumps(q.get("rubric", {})),
                        q.get("expected_failure_mode", ""),
                        q.get("question_type", "tactical"),
                        int(bool(q.get("requires_assumption", False))),
                        int(bool(q.get("source_grounded", False))),
                        q.get("source_doc"),
                        q["id"],
                    ),
                )
                updated += 1
                continue
            conn.execute(
                """
                INSERT INTO questions (
                    id, domain, category, difficulty, question, context,
                    ideal_answer, rubric, expected_failure_mode, created_at,
                    question_type, requires_assumption, source_grounded, source_doc
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    q["id"],
                    q.get("domain", ""),
                    q.get("category", ""),
                    q.get("difficulty", ""),
                    q["question"],
                    q.get("context", ""),
                    q.get("ideal_answer", ""),
                    json.dumps(q.get("rubric", {})),
                    q.get("expected_failure_mode", ""),
                    now_iso(),
                    q.get("question_type", "tactical"),
                    int(bool(q.get("requires_assumption", False))),
                    int(bool(q.get("source_grounded", False))),
                    q.get("source_doc"),
                ),
            )
            inserted += 1
        conn.commit()
    return inserted, updated


def _fetch_questions(limit: Optional[int], ids: Optional[List[str]] = None) -> list:
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM questions ORDER BY id")
        rows = cur.fetchall()
    out = [dict(r) for r in rows]
    if ids:
        wanted = {i.strip() for i in ids}
        out = [q for q in out if q["id"] in wanted]
    if limit is not None:
        out = out[:limit]
    return out


def _parse_models(models_arg: str) -> List[str]:
    aliases = [m.strip().lower() for m in models_arg.split(",") if m.strip()]
    unknown = [a for a in aliases if a not in MODEL_REGISTRY]
    if unknown:
        raise typer.BadParameter(
            f"Unknown model alias(es): {unknown}. Known: {sorted(MODEL_REGISTRY)}"
        )
    return aliases


@app.command("run")
def run_cmd(
    models: str = typer.Option("claude", help="Comma-separated model aliases."),
    limit: Optional[int] = typer.Option(None, help="Run only the first N questions."),
    ids: Optional[str] = typer.Option(
        None, "--ids",
        help="Comma-separated question ids (e.g. 'q_016,q_017,q_018'). "
        "When set, only those questions are run.",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print prompts; do not call APIs."),
    refresh_questions: bool = typer.Option(
        False,
        "--refresh-questions",
        help="Also UPDATE existing questions whose ids already exist in the DB. "
        "Use after editing data/questions.json to pick up changes without "
        "bumping ids or deleting the DB.",
    ),
) -> None:
    """Run the eval over all configured models."""
    init_db()
    inserted, updated = _load_questions_into_db(refresh=refresh_questions)
    if inserted:
        console.print(f"[green]Loaded {inserted} new question(s) into the DB.[/green]")
    if updated:
        console.print(f"[green]Refreshed {updated} existing question(s).[/green]")

    id_list = [s.strip() for s in ids.split(",")] if ids else None
    questions = _fetch_questions(limit, ids=id_list)
    if not questions:
        console.print("[yellow]No questions found.[/yellow] "
                      "Edit data/questions.json and re-run.")
        raise typer.Exit(code=0)

    aliases = _parse_models(models)

    if dry_run:
        console.print(f"[bold]Dry run[/bold] — {len(questions)} question(s) "
                      f"× {len(aliases)} model(s)")
        for q in questions:
            console.rule(f"[cyan]{q['id']}[/cyan] · {q['category']} · {q['difficulty']}")
            console.print(f"[dim]system:[/dim] {SYSTEM_PROMPT}")
            if q.get("context"):
                console.print(f"[dim]context:[/dim] {q['context']}")
            console.print(f"[bold]question:[/bold] {q['question']}")
            console.print(f"[dim]→ would call:[/dim] {', '.join(aliases)}")
        return

    clients = []
    for alias in aliases:
        try:
            clients.append((alias, build_client(alias)))
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]Failed to build client '{alias}':[/red] {exc}")

    if not clients:
        console.print("[red]No usable model clients; aborting.[/red]")
        raise typer.Exit(code=1)

    run_id = str(uuid.uuid4())
    console.print(f"[bold]run_id:[/bold] {run_id}")

    total = len(questions) * len(clients)
    pbar = tqdm(total=total, desc="evaluating", unit="resp")
    successes = failures = 0

    for q in questions:
        for alias, client in clients:
            try:
                result = client.complete(q["question"], q.get("context") or "")
                with get_db() as conn:
                    conn.execute(
                        """
                        INSERT INTO responses (
                            question_id, model, response, tokens_used,
                            latency_ms, run_id, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            q["id"],
                            client.name,
                            result["response"],
                            result["tokens"],
                            result["latency_ms"],
                            run_id,
                            now_iso(),
                        ),
                    )
                    conn.commit()
                successes += 1
            except Exception as exc:  # noqa: BLE001
                print(f"[eval] {alias} failed on {q['id']}: {exc!r}", file=sys.stderr)
                failures += 1
            finally:
                pbar.update(1)
    pbar.close()

    console.print(
        f"[green]done.[/green] success={successes} failure={failures} run_id={run_id}"
    )


@app.command("refresh-questions")
def refresh_questions_cmd() -> None:
    """Reload data/questions.json into the DB, updating existing rows.

    Use this after editing question text, ideal_answer, or rubric so the
    changes propagate to the DB without bumping ids or wiping the file.
    Past responses/scores against those question ids remain in the DB —
    re-run the eval if you want to re-grade against the updated rubric.
    """
    init_db()
    inserted, updated = _load_questions_into_db(refresh=True)
    console.print(
        f"[green]questions refreshed.[/green] inserted={inserted} updated={updated}"
    )


@app.command("list-runs")
def list_runs_cmd() -> None:
    """List all run_ids with timestamp, model, and question counts."""
    init_db()
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT run_id,
                   MIN(created_at) AS started_at,
                   model,
                   COUNT(DISTINCT question_id) AS questions,
                   COUNT(*)                    AS responses
            FROM responses
            GROUP BY run_id, model
            ORDER BY started_at DESC
            """
        ).fetchall()

    if not rows:
        console.print("[yellow]No runs yet.[/yellow]")
        return

    table = Table(title="ProfBench runs")
    table.add_column("run_id", style="cyan", no_wrap=True)
    table.add_column("started_at")
    table.add_column("model")
    table.add_column("questions", justify="right")
    table.add_column("responses", justify="right")
    for r in rows:
        table.add_row(
            r["run_id"],
            r["started_at"],
            r["model"],
            str(r["questions"]),
            str(r["responses"]),
        )
    console.print(table)


if __name__ == "__main__":
    app()
