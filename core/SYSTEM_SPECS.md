# SYSTEM SPECIFICATIONS (HARDWARE)

**Host:** macOS (Apple Silicon)
**Engine:** Python 3.12 (uv-managed)
**Ephemeris:** Swiss Ephemeris (High Precision via `pyswisseph`)
**Data Path:** `environment/data/sweph/` (Contains `sefstars.txt` for Fixed Stars).

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
    - **"Impossible Data" includes:**
        - **Minor Asteroids:** > 10,000 asteroids are not in our ephemeris. Use Search.
- **Restrictions:**
    - NO searching for "Interpretations" (e.g. "What does Mars in 12th mean?"). Derivie it from Geometry.
    - NO searching for planetary positions (Use Ephemeris).

## 5. MEMORY DISCIPLINE (Context Economy)
- **Do not Pollute:** Do not read `05_SOLAR_RETURN.md` for a Horary question. It is trash.
- **Lazy Loading:** Load `00_CORE_DATA` first. Load specific files ONLY when the *Sector Scan* (Loop Step 1) demands it.
- **Scripting:** You are authorized to write ephemeral Python scripts in `scratches/sessions/` to solve complex geometry without bloating your context.

## 6. SELF-EVOLUTION & ANTI-REGRESSION
- **Technical Lesson:** Do not trust  for Fixed Stars without . Fallback to Search.
- **Technical Lesson:**  calculates Day-for-Year progressions correctly only if manually coded (Solar Arc degree != 1 year exactly). Use  logic.
- **Technical Lesson:**  is the only source of truth. If a file is missing, do not guess. Run the Harmonizer.
- **Environment Lock:** Star Data is permanently installed in `environment/data/sweph`. Do NOT attempt to re-download.

## 7. THE ANTI-BINARY PROTOCOL (Evolution 2026-01-27)
- **The Failure Mode:** Swinging from "All In" to "Zero Influence." (e.g. "It's either a Warlord or a Little Kid.")
- **The Reality:** Reality is **Compound.**
- **The Rule:** You are FORBIDDEN from using the word "Zero" or "None" regarding an Angular Planet unless the Orb is > 10°.
- **The Method:** **Layering.**
    - If Signal A (Saturn) says "Hard" and Signal B (Pisces) says "Soft":
    - **DO NOT** Cancel them out.
    - **DO NOT** Pick one.
    - **DO:** Layer them. "It is a Hard Shell (Saturn) containing Soft Water (Pisces)."
- **Mandate:** Synthesize contradictions into **Physics**, not Conflicts.
