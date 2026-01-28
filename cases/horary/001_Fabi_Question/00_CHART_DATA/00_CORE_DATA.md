# 00_CORE_DATA

## Interrogation moment (authoritative)
- Local date/time: **2026-01-12 06:45:37** (Chișinău, Moldova)
- Coordinates (decimal): **47.0160975 N, 28.7954969 E**

## Time standardization
- Timezone used for conversion: **UTC+02:00 (winter standard time)**
- Universal Time (UT): **2026-01-12 04:45:37**

## Chart calculation settings (traditional scaffold)
- Zodiac: **Tropical**
- Houses: **Regiomontanus**
- Terms/Bounds: **Egyptian**
- Minor aspects: **OFF** (majors-only baseline)

## Source files and provenance
- Astro-Seek HTML (minute scaffold): `Should I hold her_.html`
  - Astro-Seek scaffold timestamp in the HTML: **2026-01-12 06:46:00** (minute-rounded)
  - Planetary longitudes + daily speeds + fixed-star longitudes were extracted from this HTML.

## Precision policy (non-approx commitment)
- **Planetary ecliptic longitudes & daily speeds:** taken from Astro-Seek HTML (Swiss Ephemeris output).
- **Exact-second correction:** applied by linear back-propagation from 06:46:00 → 06:45:37 using each body's extracted daily speed (Δt = −23 seconds).
- **House cusps/angles:** computed directly from the Swiss Ephemeris library house algorithms at the exact UT and exact coordinates (does not require external ephemeris files).
- **3D speculum (RA/Dec/Alt/MD):** computed with Swiss Ephemeris library in **MOSEPH fallback** mode due to missing `.se1` ephemeris files in this sandbox.
  - This affects only 3D quantities; longitude-based horary geometry remains sourced from the Astro-Seek HTML.

If you want *Swiss-ephemeris-file-level* (non-MOSEPH) RA/Dec/Alt/MD, provide the Swiss Ephemeris data files (`sepl_*.se1`, etc.) and I will rerun the 3D block without fallback.
