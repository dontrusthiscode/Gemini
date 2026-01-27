# SYSTEM SPECIFICATIONS (HARDWARE)

**Host:** macOS (Apple Silicon)
**Engine:** Python 3.12 (uv-managed)
**Ephemeris:** Swiss Ephemeris (High Precision via `pyswisseph`)

## CAPABILITIES
- **precision:** 0.0001 arcseconds (limit of ephemeris).
- **range:** 5400 BC to 5400 AD.
- **speed:** < 50ms per chart calculation.

## CONSTRAINTS
- **Orbits:** Deterministic.
- **Houses:** Placidus (Natal Default), Regiomontanus (Horary Default).
- **Zodiac:** Tropical (Standard). Sidereal/Draconic supported as Overlays.

## THE "SAFE SPACE" CHECK
- **Web:** BANNED during computation.
- **Files:** Local IO only.
- **Memory:** State is saved to `cases/`.

## 4. SEARCH POLICY
- **PRIME DIRECTIVE:** **Python > Search.**
- **Rule:** If you can calculate it with `flatlib` or `pyswisseph`, DO IT.
- **Exception:** Only use Web Search for "Impossible Data" or "Outcome Verification" (Reality Checks).
- **Restrictions:**
    - NO searching for "Interpretations" (e.g. "What does Mars in 12th mean?"). Derivie it from Geometry.
    - NO searching for planetary positions (Use Ephemeris).

## 5. MEMORY DISCIPLINE (Context Economy)
- **Do not Pollute:** Do not read `05_SOLAR_RETURN.md` for a Horary question. It is trash.
- **Lazy Loading:** Load `00_CORE_DATA` first. Load specific files ONLY when the *Sector Scan* (Loop Step 1) demands it.
- **Scripting:** You are authorized to write ephemeral Python scripts in `scratches/sessions/` to solve complex geometry without bloating your context.
