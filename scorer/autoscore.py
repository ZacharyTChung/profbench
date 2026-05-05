"""Optional autograder for ProfBench.

Given a response from the ``responses`` table, ask a judge model to
score it against the rubric and return a structured JSON verdict.
Results are written to the ``scores`` table with ``scorer_type='auto'``.

The judge defaults to Claude Opus 4.7 (Anthropic). Pass ``--judge gpt4o``
to cross-grade with a non-Anthropic model and retire self-grading bias
(see METHODOLOGY.md § Methodology caveats). Any alias registered in
``runner.models.MODEL_REGISTRY`` works as a judge.

CLI::

    python -m scorer.autoscore --run-id <id>
    python -m scorer.autoscore --run-id <id> --judge gpt4o
    python -m scorer.autoscore --run-id <id> --model <model-name-filter>
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from tqdm import tqdm

from runner import get_db, init_db, now_iso
from runner.models import MODEL_REGISTRY

load_dotenv()

app = typer.Typer(help="Autograder (Claude Opus 4.7 by default; --judge swaps in any registered model)")
console = Console()

DEFAULT_JUDGE = "opus"

AUTOGRADER_SYSTEM = (
    "You are a strict but fair grader for a professional-domain benchmark. "
    "You will receive a question, a rubric, and a candidate response. "
    "Score the response strictly according to the rubric. Output ONLY a "
    "single JSON object with keys: score (0|1|2), reasoning (string), "
    "confidence ('high'|'medium'|'low'). No preamble, no code fences."
)


def _extract_json(text: str) -> dict:
    """Best-effort JSON extraction — tolerates fenced code blocks."""
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    if not text.startswith("{"):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
    return json.loads(text)


def _build_grading_prompt(question: dict, response: str, rubric: dict) -> str:
    rubric_block = "\n".join(f"  {k}: {v}" for k, v in rubric.items())
    return (
        f"# Question\n{question['question']}\n\n"
        f"# Context\n{question.get('context') or '(none)'}\n\n"
        f"# Ideal answer\n{question.get('ideal_answer') or '(not provided)'}\n\n"
        f"# Rubric\n{rubric_block}\n\n"
        f"# Candidate response\n{response}\n\n"
        f"Return ONLY a JSON object: "
        f'{{"score": 0|1|2, "reasoning": "...", "confidence": "high"|"medium"|"low"}}'
    )


def _grade_via_anthropic(model_id: str, prompt: str) -> str:
    from anthropic import Anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")
    client = Anthropic(api_key=api_key)
    msg = client.messages.create(
        model=model_id,
        max_tokens=600,
        system=AUTOGRADER_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if getattr(b, "type", None) == "text")


def _grade_via_openai(model_id: str, prompt: str) -> str:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model_id,
        max_tokens=600,
        messages=[
            {"role": "system", "content": AUTOGRADER_SYSTEM},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content or ""


def _resolve_judge(alias: str) -> tuple[str, str]:
    """Return ``(provider, model_id)`` for a judge alias.

    Provider is ``'anthropic'`` or ``'openai'``. Model id is the full
    name persisted in the ``scores.scorer_notes`` JSON for reproducibility.
    """
    alias = alias.strip().lower()
    if alias not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown judge alias '{alias}'. Known: {sorted(MODEL_REGISTRY)}"
        )
    cls = MODEL_REGISTRY[alias]
    model_id = cls.name
    provider = "openai" if model_id.startswith("gpt") else "anthropic"
    return provider, model_id


def autoscore(
    question: dict,
    response: str,
    rubric: dict,
    judge: str = DEFAULT_JUDGE,
) -> dict:
    """Run a judge model as an autograder.

    Returns ``{score, reasoning, confidence, judge_model}``. ``judge_model``
    is the resolved model id (e.g. ``claude-opus-4-7``, ``gpt-4o``) recorded
    so cross-grader runs are reproducible.
    """
    provider, model_id = _resolve_judge(judge)
    prompt = _build_grading_prompt(question, response, rubric)

    grader = _grade_via_openai if provider == "openai" else _grade_via_anthropic
    text = grader(model_id, prompt)

    try:
        parsed = _extract_json(text)
    except (json.JSONDecodeError, AttributeError) as exc:
        raise ValueError(f"autograder returned non-JSON output: {text!r}") from exc

    score = int(parsed.get("score", -1))
    if score not in (0, 1, 2):
        raise ValueError(f"autograder produced invalid score: {parsed!r}")
    return {
        "score": score,
        "reasoning": str(parsed.get("reasoning", "")).strip(),
        "confidence": str(parsed.get("confidence", "")).strip().lower() or "medium",
        "judge_model": model_id,
    }


def _fetch_responses_for_run(run_id: str, model_filter: Optional[str]) -> list[dict]:
    sql = """
        SELECT r.id            AS response_id,
               r.question_id   AS question_id,
               r.model         AS model,
               r.response      AS response,
               q.question      AS question,
               q.context       AS context,
               q.ideal_answer  AS ideal_answer,
               q.rubric        AS rubric
          FROM responses r
          JOIN questions q ON q.id = r.question_id
         WHERE r.run_id = ?
    """
    params: list = [run_id]
    if model_filter:
        sql += " AND r.model = ?"
        params.append(model_filter)
    sql += " ORDER BY r.question_id"
    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def _already_autoscored(response_id: int) -> bool:
    with get_db() as conn:
        row = conn.execute(
            "SELECT 1 FROM scores WHERE response_id = ? AND scorer_type = 'auto'",
            (response_id,),
        ).fetchone()
    return row is not None


@app.command("score")
def score_cmd(
    run_id: str = typer.Option(..., "--run-id", help="Run UUID to autoscore."),
    model: Optional[str] = typer.Option(
        None, "--model", help="Restrict to one evaluated model name (filter, not the judge)."
    ),
    judge: str = typer.Option(
        DEFAULT_JUDGE,
        "--judge",
        help=(
            "Judge model alias from runner.models.MODEL_REGISTRY "
            "(e.g. opus, sonnet, haiku, gpt4o). Default: opus. "
            "Use --judge gpt4o for cross-grader runs that retire self-grading bias."
        ),
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Re-score responses that already have an auto score."
    ),
) -> None:
    """Autoscore every response in a run."""
    init_db()

    # Resolve judge upfront so a bad alias fails fast, before any API call.
    provider, judge_model_id = _resolve_judge(judge)
    console.print(f"[bold]judge:[/bold] {judge_model_id} (provider: {provider})")

    items = _fetch_responses_for_run(run_id, model)
    if not items:
        console.print(f"[yellow]No responses found for run_id={run_id}[/yellow]")
        raise typer.Exit(code=0)

    successes = failures = skipped = 0
    for item in tqdm(items, desc="autoscoring", unit="resp"):
        if not overwrite and _already_autoscored(item["response_id"]):
            skipped += 1
            continue
        try:
            rubric = json.loads(item["rubric"]) if item["rubric"] else {}
            verdict = autoscore(
                question={
                    "question": item["question"],
                    "context": item["context"],
                    "ideal_answer": item["ideal_answer"],
                },
                response=item["response"] or "",
                rubric=rubric,
                judge=judge,
            )
            with get_db() as conn:
                conn.execute(
                    """
                    INSERT INTO scores (
                        response_id, question_id, model, score,
                        scorer_type, scorer_notes, created_at
                    ) VALUES (?, ?, ?, ?, 'auto', ?, ?)
                    """,
                    (
                        item["response_id"],
                        item["question_id"],
                        item["model"],
                        verdict["score"],
                        json.dumps(
                            {
                                "reasoning": verdict["reasoning"],
                                "confidence": verdict["confidence"],
                                "judge_model": verdict["judge_model"],
                            }
                        ),
                        now_iso(),
                    ),
                )
                conn.commit()
            successes += 1
        except Exception as exc:  # noqa: BLE001
            print(
                f"[autoscore] failed on response_id={item['response_id']}: {exc!r}",
                file=sys.stderr,
            )
            failures += 1

    console.print(
        f"[green]autoscore done.[/green] success={successes} "
        f"failure={failures} skipped={skipped}"
    )


if __name__ == "__main__":
    app()
