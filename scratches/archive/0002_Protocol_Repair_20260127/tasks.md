# SESSION 002: PROTOCOL REPAIR & ASPECT FIX

**OBJECTIVE:** 
Fix `calculate_natal.py` to correctly output Nuclear Events (<1°). 
Codify the "Session First" rule into the system memory.

## TASKS
- [x] **Phase 1: Diagnosis**
    - [x] Analyze `environment/scripts/calculate_natal.py` for missing aspect logic.
    - [x] Log failure in `core/PROTOCOL_VIOLATION.md`.

- [x] **Phase 2: Repair (In Containment)**
    - [x] Update `calculate_natal.py` to calculate Aspects (Orb < 1°).
    - [x] Run script to output to `scratches/sessions/002_Protocol_Repair/TEST_NATAL.md`.
    - [x] Verify Nuclear Events are populated.

- [x] **Phase 3: Protocol Upgrade**
    - [x] Update `core/DOCTRINE.md` with "The Containment Rule".
    - [x] Update `core/LOOP.md` to enforce check before write.

- [x] **Phase 4: Deployment**
    - [x] Overwrite `cases/001_Theodore/00_CORE_DATA/01_NATAL_CHART.md` ONLY after verification.
