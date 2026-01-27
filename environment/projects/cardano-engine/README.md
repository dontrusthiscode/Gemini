## Cardano Engine (Compute-only)

This is the Python engine that produces **forensic evidence packets** for traditional astrology workflows.

**Default posture:** compute-only, no interpretation.

### Inputs

- JSON input files (see `Cold Read Me.md` at repo root for examples).
- Required: time + location + chart type.

### Outputs

Written into `results/<case_id>/`:
- `00_CORE_DATA/input.json` — the exact input used
- `01_CHART/ledger.json` — machine-readable ledger (for diffs, audits)
- `01_CHART/report.md` — human-readable report (Markdown)
- `03_CONTEXT_LOG/context.md` — optional narrative context

### SOP defaults

All hard defaults are defined in:
- `/Users/Admin/Documents/11_Astrology/environment/SOP.md`

### Run

From repo root:

- `environment/bin/cardano-engine --input /absolute/or/relative/path/to/input.json`

### Data

Swiss Ephemeris data is expected at:
- `environment/data/sweph/`

Verify checksums:
- `environment/bin/verify-sweph`
