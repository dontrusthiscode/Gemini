from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown.rstrip() + "\n", encoding="utf-8")


def format_dt(dt: datetime) -> str:
    return dt.isoformat()


def render_markdown(result: dict) -> str:
    meta = result.get("meta", {})
    chart = result.get("chart", {})
    flags = result.get("flags", [])

    lines: list[str] = []
    lines.append(f"# Cardano Engine Report — {chart.get('chart_type','chart')}")
    lines.append("")

    lines.append("## Meta")
    for k in sorted(meta.keys()):
        if k == "swe_files":
            continue
        lines.append(f"- {k}: `{meta[k]}`")
    swe_files = meta.get("swe_files", {})
    if swe_files:
        lines.append("- swe_files:")
        for k in ("planet", "moon", "asteroid", "stars"):
            if k not in swe_files:
                continue
            v = swe_files[k]
            lines.append(f"  - {k}: `{v.get('path')}`")
    lines.append("")

    lines.append("## Chart")
    for k in ("datetime_input", "datetime_utc"):
        if k in chart:
            lines.append(f"- {k}: `{chart[k]}`")
    if "location" in chart:
        lines.append(f"- location: `{chart['location']}`")
    for k in ("house_system", "sect", "asc_ruler", "ayanamsa_lahiri"):
        if k in chart and chart[k] is not None:
            lines.append(f"- {k}: `{chart[k]}`")
    angles = chart.get("angles") or {}
    if angles:
        lines.append(f"- angles: `{angles}`")
    planetary_hour = chart.get("planetary_hour")
    if planetary_hour:
        lines.append(f"- planetary_hour: `{planetary_hour}`")
    if chart.get("question"):
        lines.append(f"- question: `{chart.get('question')}`")
    lines.append("")

    if flags:
        lines.append("## Flags (compute-only)")
        for f in flags:
            lines.append(f"- {f}")
        lines.append("")

    planets = result.get("bodies", {})
    if planets:
        lines.append("## Bodies (snapshot)")
        lines.append("")
        lines.append("| Body | Tropical | House | Dignity | Combust | Decl | Sidereal (Lahiri) | Draconic | WS (Sid/Drac) |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        order = (
            "Sun",
            "Moon",
            "Mercury",
            "Venus",
            "Mars",
            "Jupiter",
            "Saturn",
            "MeanNode",
            "TrueNode",
        )
        for name in order:
            if name not in planets:
                continue
            p = planets[name]
            trop = p.get("tropical", {})
            sid = p.get("sidereal_lahiri", {})
            drac = p.get("draconic", {})
            lon = trop.get("lon")
            sign = trop.get("sign")
            deg = trop.get("deg_in_sign")
            house = (p.get("house") or {}).get("number")
            ed = p.get("essential_dignity") or {}
            score = ed.get("score")
            combust = p.get("combustion") or {}
            combust_txt = ""
            if combust:
                combust_txt = "Y" if combust.get("combust") else "N"
                if combust.get("sep_deg") is not None:
                    combust_txt += f" ({combust['sep_deg']:.2f}°)"
            decl = p.get("declination")
            ws = p.get("whole_sign_houses") or {}
            ws_txt = ""
            if ws:
                ws_txt = f"{ws.get('sidereal_lahiri')}/{ws.get('draconic')}"

            if lon is None:
                continue
            trop_txt = f"{lon:.6f} ({sign} {deg:.2f}°)" if sign is not None and deg is not None else f"{lon:.6f}"
            sid_txt = f"{sid.get('lon'):.6f}" if sid.get("lon") is not None else ""
            drac_txt = f"{drac.get('lon'):.6f}" if drac.get("lon") is not None else ""
            decl_txt = f"{decl:.4f}" if decl is not None else ""
            lines.append(
                f"| {name} | {trop_txt} | {house} | {score} | {combust_txt} | {decl_txt} | {sid_txt} | {drac_txt} | {ws_txt} |"
            )
        lines.append("")

    aspects = result.get("aspects", [])
    if aspects:
        lines.append("## Major aspects (Tropical)")
        for a in aspects:
            lines.append(
                f"- {a['a']}-{a['b']} {a['aspect']} orb `{a['orb_deg']:.2f}°` / `{a['allowed_orb_deg']:.2f}°`"
                + (" [PARTILE]" if a.get("partile") else "")
                + (" [WEAK]" if a.get("weak_wide") else "")
            )
        lines.append("")

    parallels = result.get("parallels", [])
    if parallels:
        lines.append("## Parallels / contra-parallels")
        for p in parallels:
            lines.append(
                f"- {p['a']}-{p['b']} {p['kind']} orb `{p['orb_deg']:.3f}°`"
                + (" [NUCLEAR]" if p.get("nuclear") else "")
            )
        lines.append("")

    fixed = result.get("fixed_stars", [])
    if fixed:
        lines.append("## Fixed stars (longitude conjunctions)")
        for hit in fixed:
            lines.append(f"- {hit['star']} conjunct {hit['body']} orb `{hit['orb_deg']:.3f}°` (limit `{hit['limit_deg']:.1f}°`)")
        lines.append("")

    moon_seq = result.get("moon_sequence", [])
    if moon_seq:
        lines.append("## Moon sequence (before sign exit)")
        for ev in moon_seq:
            lines.append(f"- {ev['datetime_utc']} — Moon {ev['aspect']} {ev['body']} orb `{ev['orb_deg']:.4f}°`")
        lines.append("")

    antiscia = result.get("antiscia_contacts", [])
    if antiscia:
        lines.append("## Antiscia contacts (<= 1°)")
        for hit in antiscia:
            lines.append(f"- {hit['a']} {hit['kind']} {hit['b']} orb `{hit['orb_deg']:.3f}°`")
        lines.append("")

    return "\n".join(lines)

