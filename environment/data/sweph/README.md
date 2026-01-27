# Swiss Ephemeris data (offline)

These files are required for deterministic, high-precision calculations via Swiss Ephemeris.

Source mirror used during setup:
- https://github.com/aloistr/swisseph/tree/master/ephe

Integrity:
- `manifest.json` + `SHA256SUMS.txt` were generated locally.
- Verify at any time with: `environment/bin/verify-sweph`

Policy:
- Do not “update” these files silently.
- If you intentionally change them, rebuild the manifest:
  - `environment/scripts/sweph_manifest.py build`

