# SESSION 003: SYSTEM HARMONIZATION & EVOLUTION

**OBJECTIVE:** 
Create a self-correcting, consistent operating system. 
Codify policies on Web Search vs. Python.
Final Polish of Core Data.

## TASKS
- [x] **Phase 1: Session Restoration**
    - [x] Unarchive `001_Refine_Coordinates`.
    - [x] Unarchive `002_Protocol_Repair`.

- [x] **Phase 2: Transit Script Upgrade**
    - [x] Diagnosis: `update_transits.py` only prints to stdout?
    - [x] Rewrite to support:
        - Tropical (Placidus)
        - Sidereal (Lahiri)
        - Draconic (Nodes)
    - [x] Output: Write to `cases/001_Theodore/00_CORE_DATA/03_TRANSITS.md`.

- [x] **Phase 3: The Master Switch (Evolution)**
    - [x] Create `environment/scripts/harmonize.py`.
        - Function: Lints workspace.
        - Function: Re-runs ALL calculation scripts (`natal`, `vedic`, `draconic`, `prognostics`, `extended`).
        - Function: Updates `00_CORE_DATA.md` map.
    - [x] "One Command to Rule Them All": Ensure I can rebuild the entire case from `00_CORE_DATA.md` inputs using this script.

- [x] **Phase 4: Policy Codification**
    - [x] Update `core/SYSTEM_SPECS.md`:
        - **Web Usage:** Only for external news/data not in Ephemeris.
        - **Python:** The primary engine of truth.
    - [x] Update `core/DOCTRINE.md`:
        - **Consistency:** The "Future Self" clause.

- [x] **Phase 5: The Final Polish (White Glove)**
    - [x] Run `harmonize.py`.
    - [x] Verify NO empty files, NO bugs, NO stale data.
    - [x] Archive Session 003.
