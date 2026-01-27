# Cardano Engine — Standard Operational Procedure (SOP)

This document locks the **non-negotiable defaults** for the Cardano Engine (“Calculator / Looper / Geometry guy”).

**Mandate:** maximum forensic precision, zero interpretation.  
**Policy:** network allowed **only** during dataset/setup; computation runs **offline** and is deterministic.

---

## 1) House systems (defaults)

- **Horary:** Regiomontanus (Lilly/Renaissance standard; non-negotiable)
- **Natal:** Placidus (default for modern/psychological profiling)
- **Forensic overlays (Sidereal/Draconic):** Whole Sign houses (avoid cusp ambiguity when shifting coordinate systems)
- **Crow chart:** force Regiomontanus

---

## 2) Zodiac frameworks

- **Primary:** Tropical (geocentric ecliptic)
- **Secondary cross-check:** Sidereal using **N.C. Lahiri / Chitra Paksha** (no deviation)
- **Draconic:** defined as `TropicalLongitude - MeanNorthNodeLongitude` normalized to 0–360  
  - Equivalent: `0° Aries == Mean North Node`

---

## 3) Nodes

- **Default node:** Mean Node
- **Report:** compute both **Mean** and **True** for boundary-case auditing

---

## 4) Aspect policy (defaults)

### 4.1 Aspects

Ptolemaic majors only:
- Conjunction (0°)
- Sextile (60°)
- Square (90°)
- Trine (120°)
- Opposition (180°)

### 4.2 Orbs (William Lilly moieties)

Moieties (full orb / half-orb):
- Sun: 15° / 7.5°
- Moon: 12° / 6°
- Saturn: 9° / 4.5°
- Jupiter: 9° / 4.5°
- Mars: 7° / 3.5°
- Venus: 7° / 3.5°
- Mercury: 7° / 3.5°

Aspect orb rule:
- `allowed_orb = (moiety(A) + moiety(B)) / 2`

Strength flags:
- **Strict Mode:** flag any aspect with `orb > 3°` as **Weak/Wide**
- **Partile / Platic:** report both; engine treats partile as a separate flag (definition locked in code)

### 4.3 Declination geometry (3D)

- Compute **Parallels** and **Contra‑Parallels**
- Tolerance: `<= 1.0°`
- **Nuclear Lock:** `<= 0.2°`

---

## 5) Essential dignity tables + scoring

Tables:
- **Triplicity:** Dorothean (with Day/Night sect handling)
- **Terms (bounds):** Egyptian
- **Faces (decans):** Chaldean order

Scoring (do not clamp; report raw additive totals):
- Domicile: +5
- Exaltation: +4
- Triplicity: +3
- Term: +2
- Face: +1
- Peregrine: -5
- Detriment: -5
- Fall: -4

---

## 6) Antiscia / contra-antiscia

Axis: **0° Cancer / 0° Capricorn**.

Operator notes included two conflicting formulas. To preserve forensic auditability, the engine will compute both:

- **Solstice antiscia (axis 0 Cancer/Capricorn):** `antiscia = (180° - longitude) mod 360`
- **Reverse longitude (equinox mirror cross-check):** `antiscia_alt = (360° - longitude) mod 360`

Contra‑antiscia:
- `contra = (antiscia + 180°) mod 360`

Contact orb (for conjunction/opposition checks): `1.0°` tight.

---

## 7) Dodecatemoria (12th-part overlay)

Variant requested (“Paul of Alexandria” label from operator message):
- `dodecatemoria = longitude + 12 * (longitude - sign_start_degree)`
- Normalize to `0–360`

Note: since `longitude = sign_start + d`, this equals `sign_start + 13*d` (a 13× internal mapping). The engine implements the formula exactly as written above.

---

## 8) Fixed stars (longitude conjunctions only)

Method:
- Ecliptic longitude conjunctions ONLY (no parans unless rectified birth time is confirmed)

Orb:
- Default: `1.0°` strict
- Exceptions: `1.5°` for **Regulus / Spica / Algol / Sirius**

Default star list:
- Algol
- Pleiades (Alcyone)
- Aldebaran
- Sirius
- Castor
- Pollux
- Regulus
- Spica
- Arcturus
- Antares
- Vega
- Altair
- Fomalhaut
- Markab
- Scheat
- Facies 

Additional star mentioned in later operator note (optional, still supported):
- Alphard

---

## 9) Horary “Noise Filter” (radicality flags; compute-only)

Flags (do not interpret; just report):
- **Early/Late Ascendant:** ASC `< 3°` or `> 27°`
- **Moon Void of Course:** Moon makes **no applying major aspect** before leaving her sign
- **Saturn in 7th:** Saturn located in the 7th house (horary house system)
- **Planetary Hour Mismatch:** compute hour ruler; if no match with Asc ruler and no match with Asc almuten → flag “Not Radical”

---

## 10) Output + reproducibility

- Output: **Markdown + JSON ledger**
- Determinism: 100% reproducible (pin Python, pin packages, pin datasets, record checksums)
- Network: blocked by convention during computation; allowed during setup only

