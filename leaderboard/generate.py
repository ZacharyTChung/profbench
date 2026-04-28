"""Generate ProfBench leaderboards (markdown + self-contained HTML).

Outputs:
- ``leaderboard/leaderboard.md`` — clean markdown table.
- ``leaderboard/leaderboard.html`` — single-file HTML page with styled
  table and per-model cards. No external CSS/JS dependencies.

CLI::

    python -m leaderboard.generate --run-id <id>
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from analysis import stats
from runner import PROJECT_ROOT, now_iso

app = typer.Typer(help="ProfBench leaderboard generator")
console = Console()

LEADERBOARD_DIR = PROJECT_ROOT / "leaderboard"
MD_PATH = LEADERBOARD_DIR / "leaderboard.md"
HTML_PATH = LEADERBOARD_DIR / "leaderboard.html"


def _ranked_table(run_id: str, scorer: Optional[str]):
    overall = stats.per_model_average(run_id=run_id, scorer_type=scorer)
    per_cat = stats.per_category(run_id=run_id, scorer_type=scorer)
    rows = []
    for rank, row in overall.iterrows():
        m = row["model"]
        cat = per_cat[per_cat["model"] == m].sort_values("avg_score", ascending=False)
        best_cat = cat.iloc[0]["category"] if not cat.empty else "—"
        worst_cat = cat.iloc[-1]["category"] if not cat.empty else "—"
        rows.append(
            {
                "rank": rank + 1,
                "model": m,
                "avg_score": row["avg_score"],
                "pct_of_max": row["pct_of_max"],
                "n": row["n"],
                "best_category": best_cat,
                "worst_category": worst_cat,
            }
        )
    return rows


def _render_markdown(run_id: str, scorer: Optional[str], rows: list[dict]) -> str:
    if not rows:
        return (
            f"# ProfBench leaderboard\n\n"
            f"_Run `{run_id}` · scorer filter: `{scorer or 'all'}` · "
            f"generated {now_iso()}_\n\n_No scores recorded yet._\n"
        )
    lines = [
        "# ProfBench leaderboard",
        "",
        f"_Run `{run_id}` · scorer filter: `{scorer or 'all'}` · generated {now_iso()}_",
        "",
        "| Rank | Model | Avg score (0–2) | % of max | n | Best category | Worst category |",
        "| ---- | ----- | --------------- | -------- | - | ------------- | -------------- |",
    ]
    for r in rows:
        lines.append(
            f"| {r['rank']} | `{r['model']}` | {r['avg_score']} | "
            f"{r['pct_of_max']}% | {r['n']} | {r['best_category']} | {r['worst_category']} |"
        )
    return "\n".join(lines) + "\n"


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>ProfBench leaderboard</title>
  <style>
    :root {{
      --bg: #0f1117; --panel: #161a23; --text: #e6e8ee;
      --muted: #9aa3b2; --accent: #6aa6ff; --good: #5be3a0; --bad: #ff7a90;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; padding: 2.5rem 1.5rem; background: var(--bg); color: var(--text);
      font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .wrap {{ max-width: 980px; margin: 0 auto; }}
    h1 {{ margin: 0 0 .25rem; font-size: 1.8rem; }}
    .meta {{ color: var(--muted); font-size: .9rem; margin-bottom: 2rem; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--panel); border-radius: 10px; overflow: hidden; }}
    th, td {{ padding: .8rem 1rem; text-align: left; }}
    thead th {{ background: #1d2230; color: var(--muted); font-weight: 600; font-size: .85rem; text-transform: uppercase; letter-spacing: .04em; }}
    tbody tr {{ border-top: 1px solid #232838; }}
    tbody tr:first-child {{ border-top: none; }}
    .rank {{ font-weight: 700; color: var(--accent); }}
    .model {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .9rem; }}
    .pct {{ color: var(--good); font-weight: 600; }}
    .cards {{ margin-top: 2rem; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; }}
    .card {{ background: var(--panel); border-radius: 10px; padding: 1rem 1.2rem; }}
    .card h3 {{ margin: 0 0 .35rem; font-family: ui-monospace, monospace; font-size: 1rem; color: var(--accent); }}
    .card p {{ margin: .25rem 0; color: var(--muted); font-size: .85rem; }}
    .card .score {{ font-size: 1.6rem; font-weight: 700; color: var(--text); }}
    .empty {{ background: var(--panel); padding: 1.5rem; border-radius: 10px; color: var(--muted); }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>ProfBench leaderboard</h1>
    <div class="meta">Run <code>{run_id}</code> · scorer filter: <code>{scorer}</code> · generated {generated}</div>
    {body}
  </div>
</body>
</html>
"""


def _render_html(run_id: str, scorer: Optional[str], rows: list[dict]) -> str:
    if not rows:
        body = '<div class="empty">No scores recorded yet.</div>'
    else:
        thead = (
            "<thead><tr>"
            "<th>Rank</th><th>Model</th><th>Avg (0–2)</th><th>% of max</th>"
            "<th>n</th><th>Best</th><th>Worst</th></tr></thead>"
        )
        body_rows = []
        for r in rows:
            body_rows.append(
                "<tr>"
                f"<td class='rank'>{r['rank']}</td>"
                f"<td class='model'>{html.escape(str(r['model']))}</td>"
                f"<td>{r['avg_score']}</td>"
                f"<td class='pct'>{r['pct_of_max']}%</td>"
                f"<td>{r['n']}</td>"
                f"<td>{html.escape(str(r['best_category']))}</td>"
                f"<td>{html.escape(str(r['worst_category']))}</td>"
                "</tr>"
            )
        table = f"<table>{thead}<tbody>{''.join(body_rows)}</tbody></table>"

        cards = []
        for r in rows:
            cards.append(
                "<div class='card'>"
                f"<h3>{html.escape(str(r['model']))}</h3>"
                f"<div class='score'>{r['avg_score']} <span style='font-size:1rem;color:var(--muted)'>/ 2</span></div>"
                f"<p>{r['pct_of_max']}% of max · n={r['n']}</p>"
                f"<p>Best: {html.escape(str(r['best_category']))}</p>"
                f"<p>Worst: {html.escape(str(r['worst_category']))}</p>"
                "</div>"
            )
        cards_block = f"<div class='cards'>{''.join(cards)}</div>"
        body = table + cards_block

    return HTML_TEMPLATE.format(
        run_id=html.escape(run_id),
        scorer=html.escape(scorer or "all"),
        generated=html.escape(now_iso()),
        body=body,
    )


@app.command("generate")
def generate_cmd(
    run_id: str = typer.Option(..., "--run-id", help="Run UUID to render."),
    scorer: Optional[str] = typer.Option(
        None, "--scorer", help="'human', 'auto', or omit for both."
    ),
    md_out: Path = typer.Option(MD_PATH, "--md-out"),
    html_out: Path = typer.Option(HTML_PATH, "--html-out"),
) -> None:
    """Render leaderboard.md and leaderboard.html for one run."""
    rows = _ranked_table(run_id, scorer)

    md_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.write_text(_render_markdown(run_id, scorer, rows), encoding="utf-8")
    html_out.write_text(_render_html(run_id, scorer, rows), encoding="utf-8")

    console.print(f"[green]Wrote[/green] {md_out}")
    console.print(f"[green]Wrote[/green] {html_out}")


if __name__ == "__main__":
    app()
