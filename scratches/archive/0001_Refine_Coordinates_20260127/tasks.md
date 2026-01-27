# SESSION 001: REFINE COORDINATES (PRECISION AUDIT)

**OBJECTIVE:** 
Update Base Reality with High-Fidelity Hospital Coordinates. 
Reduce margin of error from >1km to <50m.

## TASKS
- [x] **Phase 1: Input Data**
    - [x] Obtain exact Hospital Coordinates from User.
    - [x] Update `cases/001_Theodore/00_CORE_DATA/00_CORE_DATA.md`.

- [x] **Phase 2: Natal Recalculation (Placidus)**
    - [x] Create `environment/scripts/calculate_natal.py`.
    - [x] Patch scripts for Decimal Coordinates.
    - [x] Run `environment/scripts/calculate_natal.py`.
    - [x] Update `cases/001_Theodore/00_CORE_DATA/01_NATAL_CHART.md`.
    - [x] Verify Nuclear Events (<1°) - Determine if any "Laws" in Encyclopedia were false.

- [x] **Phase 3: Vedic Recalculation (Sidereal)**
    - [x] Create `environment/scripts/calculate_vedic.py`.
    - [x] Recalculate using Lahiri Ayanamsa.
    - [x] Update `cases/001_Theodore/00_CORE_DATA/04_VEDIC.md`.

- [x] **Phase 4: Draconic Recalculation (Soul)**
    - [x] Create `environment/scripts/calculate_draconic.py`.
    - [x] Recalculate relative to North Node.
    - [x] Update `cases/001_Theodore/00_CORE_DATA/05_DRACONIC.md`.

- [ ] **Phase 5: Commit**
    - [ ] Publish to GitHub (User Action).

- [x] **Phase 6: Derivative Charts (Prognostics)**
    - [x] Create `environment/scripts/calculate_prognostics.py` (Solar Arc, Progressions, Returns).
    - [x] Create `environment/scripts/calculate_extended_vedic.py` (Dashas, Divisionals).
    - [x] Verify Output against `00_CORE_DATA` standards.
    - [x] Update files:
        - `02_SOLAR_ARC.md`
        - `04_PROGRESSIONS.md`
        - `06_VEDIC_DETAILS.md`
        - `08_SOLAR_RETURN.md`
        - `09_DASHA_TIMELINE.md`
        - `10_DIVISIONALS.md`
