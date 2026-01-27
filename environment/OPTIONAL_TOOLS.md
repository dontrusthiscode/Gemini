# Optional Tools (Not Installed by Default)

Default policy is **noise reduction** and **minimal dependencies**.

This file lists optional additions that are useful for “obscure” workflows (batch work, importing third‑party chart exports, extra audits). Do not enable them unless needed.

---

## HTML ingestion (Astro‑Seek / Astro‑Seq export diffing)

Use when you want to ingest an HTML chart page and compare it to local calculations.

Suggested packages:
- `beautifulsoup4`
- `lxml`

---

## Batch / ledger analysis (many charts)

Use when running packs (progressions, solar arcs, multiple event charts) and you need sorting/diffing and aggregation.

Suggested packages:
- `numpy`
- `pandas`

---

## Plotting (charts/graphs)

Only if you need plots; not required for forensic packets.

Suggested packages:
- `matplotlib`

---

## JPL cross-check (astronomy audit)

Use only if you want a second, independent numerical engine to cross-check Swiss Ephemeris outputs.

Suggested packages:
- `skyfield`

Required datasets (offline):
- a JPL DE ephemeris file (e.g. `de440s.bsp` or similar), stored under `environment/data/jpl/`

---

## Rule of thumb

If a tool adds “more things to calculate” without improving signal-to-noise for the question, keep it disabled.

