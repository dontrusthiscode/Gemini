# MASTER_HORARY_PACKET

Complete forensic packet for the horary (geometry-only; no interpretation).

## File order
- 00_CORE_DATA.md
- 01_HOUSES_CUSPS_REGIOMONTANUS.md
- 02_BODIES_POSITIONS.md
- 03_ASPECTS_MAJOR.md
- 04_SPECULUM_3D.md
- 05_DODECATEMORIA_12TH_PARTS.md
- 06_STRUCTURAL_FLAGS.md
- 07_ANTISCIA_CONTRA_ANTISCIA.md
- 08_LOTS_FORTUNE_SPIRIT_EROS_NECESSITY.md
- 09_FIXED_STARS_FROM_ASTROSEEK_HTML.md
- 10_MOON_NEXT_EXACT_MAJOR_ASPECTS.md

## Computation notes
- Longitude-based data: extracted from Astro-Seek HTML (Swiss Ephemeris output) and corrected to the exact interrogation second.
- Cusps/angles: computed at the exact second and exact coordinates (Regiomontanus).
- 3D speculum + Moon perfection timestamps: computed in MOSEPH fallback mode (no `.se1` ephemeris files in sandbox).
- Fixed stars: extracted from Astro-Seek HTML table (no approximations).
