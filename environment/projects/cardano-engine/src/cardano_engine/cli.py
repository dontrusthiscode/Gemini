from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from .engine import compute_chart, load_input
from .report import render_markdown, write_json, write_markdown
from .swisseph_utils import find_environment_root


def _default_results_dir() -> Path:
    env_root = find_environment_root()
    # results/ is a sibling of environment/
    return env_root.parent / "results"


_SAFE_ID_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _sanitize_case_id(value: str) -> str:
    value = value.strip().replace(" ", "_")
    value = _SAFE_ID_RE.sub("_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "case"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="cardano-engine", description="Compute-only forensic astrology engine (Cardano).")
    parser.add_argument("--input", required=True, type=Path, help="Path to chart input JSON.")
    parser.add_argument("--out-dir", type=Path, default=_default_results_dir(), help="Output directory (default: ./results).")
    args = parser.parse_args(argv)

    input_text = args.input.read_text(encoding="utf-8")
    inp = load_input(args.input)
    result = compute_chart(inp)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    case_id = _sanitize_case_id(inp.chart_id or f"{inp.chart_type}_{stamp}")
    case_dir = args.out_dir / case_id

    core_dir = case_dir / "00_CORE_DATA"
    chart_dir = case_dir / "01_CHART"
    cross_dir = case_dir / "02_CROSS_REFERENCE"
    context_dir = case_dir / "03_CONTEXT_LOG"
    meta_dir = case_dir / "04_META"

    # Always create the full scaffold (some dirs may be empty in early versions).
    for d in (core_dir, chart_dir, cross_dir, context_dir, meta_dir):
        d.mkdir(parents=True, exist_ok=True)

    (core_dir / "input.json").write_text(input_text, encoding="utf-8")
    write_json(chart_dir / "ledger.json", result)
    write_markdown(chart_dir / "report.md", render_markdown(result))

    question = result.get("chart", {}).get("question")
    context = result.get("chart", {}).get("context")
    if question or context:
        parts: list[str] = []
        if question:
            parts.append("# Question")
            parts.append(str(question).rstrip())
            parts.append("")
        if context is not None:
            parts.append("# Context")
            parts.append(str(context).rstrip())
            parts.append("")
        write_markdown(context_dir / "context.md", "\n".join(parts))

    # Meta shortcut for quick inspection.
    write_json(meta_dir / "meta.json", result.get("meta", {}))

    print(str(case_dir))
