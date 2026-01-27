# environment/ (Capsule)

This folder is the self-contained capsule for the “Cardano Engine”.

It contains:
- `SOP.md` — hard-coded operational defaults
- `projects/cardano-engine/` — Python compute engine (locked deps via `uv.lock`)
- `data/sweph/` — Swiss Ephemeris datasets + checksum manifest
- `scripts/` — bootstrap + dataset manifest tools
- `bin/` — wrappers (`cardano-engine`, `verify-sweph`, optional `uv`)

Setup (network allowed):
- `environment/scripts/bootstrap.sh`

Computation (offline):
- `environment/bin/cardano-engine --input <file.json>`

