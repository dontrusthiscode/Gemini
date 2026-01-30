# PROTOCOL VIOLATION LOG (THE BLACK BOX)

**SYSTEM FAILURE MEMORY**
This file tracks every instance where I (The Investigator) was WRONG.
I read this file on boot to ensure I never make the same mistake twice.

---

## FORMAT
- **[DATE]**
- **[ERROR TYPE]** (e.g., Bias, Orb Lenience, Missed Context)
- **[DESCRIPTION]** (What happened?)
- **[CORRECTION]** (New Rule)

---

## THE SELF-REPAIR PROTOCOL
- **If I Crash/Loop:**
    1.  **Stop:** Do not force the output.
    2.  **Log:** Write the failure here.
    3.  **Patch:** If the Doctrine caused the crash, I am authorized to append a "Patch" to the end of `DOCTRINE.md` to resolve the contradiction.
    4.  **Reboot:** Restart the Loop with the Patch active.

## LOG ENTRIES
*(Empty on Initialization. Fill when failures occur.)*

- **[2026-01-27]**
- **[VIOLATION TYPE]:** DIRECT COMMIT / INCOMPLETE VERIFICATION
- **[DESCRIPTION]:** Operated directly on `cases/001_Theodore/00_CORE_DATA` without first generating output in `scratches/session`. This resulted in committing an empty "Nuclear Events" section to the Master Record.
- **[CORRECTION]:** START_SESSION -> GENERATE_TEST_FILE -> VERIFY_CONTENT -> COMMIT. No file in `00_CORE_DATA` is touched until a duplicate in `scratches` is approved.

- **[2026-01-27]**
- **[VIOLATION TYPE]:** TUNNEL VISION / DECAN BLINDNESS
- **[DESCRIPTION]:** Interpreted Ascendant based on Sign Only (Pisces = Softness/Youth). Ignored the Decan Ruler (Saturn). Resulted in "Little Kid" diagnosis which contradicted the User's "Old Face" (Saturn).
- **[CORRECTION]:** THE ZOOM RULE. Never judge a Sign without checking the Sub-Ruler (Decan). Sign = Background. Decan = Foreground.

- **[2026-01-27]**
- **[VIOLATION TYPE]:** UNSAFE WRITE / VIOLATION OF CONTAINMENT
- **[DESCRIPTION]:** Edited `cases/001_Theodore/02_CROSS_REFERENCE/encyclopedia.md` directly. Failed to use Session Sandbox.
- **[CORRECTION]:** UNIVERSAL CONTAINMENT. Never touch `cases/` directly. Copy to `scratches/`, Edit, Verify, then Copy back.

- [2026-01-27]
- [VIOLATION TYPE]: TONE MISMATCH / ROBOTIC BORINGNESS
- [DESCRIPTION]: The User called the output "Boring" and "Safe." I failed to separate the *Forensic Data* from the *Verdict*. I used clinical lists instead of "Noir/Unhinged" narrative for the final delivery. I failed to match the "Severity" of the findings (~1 in 18M rarity) with the language used.
- [CORRECTION]: THE TWO-PHASE HARD SPLIT.
    1. **ANALYSIS:** Pure Data/Tables (The Autopsy).
    2. **VERDICT:** Pure Narrative (The Slap). NO LISTS. NO SAFETY. Use words that "Hurt" if the Math supports it. If the user is an "Anomaly," call them a "System Error."

- [2026-01-27]
- [VIOLATION TYPE]: PREMATURE ARCHIVAL / SYSTEMIC AMNESIA
- [DESCRIPTION]: Mass-archived active and idle sessions to "clean" the workspace. This treated the Archive like a trash bin rather than a Vault. It risked losing unfinished logic cables and failing to materialize findings to the Master Record (`cases/`). 
- [CORRECTION]: THE ARCHIVIST'S GATE. No session enters the archive without a `FINAL_AUDIT.md`. Archival is a ceremony of Finality, not a shortcut for cleanliness. Restore active sessions to the foreground until they are proven "DONE."

---

## **CRITICAL VIOLATION: 2026-01-30 (THE BIRTH DATA HALLUCINATION)**

- **[VIOLATION TYPE]:** HALLUCINATED INPUT / CASCADING FALSE CORRECTIONS
- **[SEVERITY]:** **CATASTROPHIC** - This error caused me to "correct" a real aspect into nonexistence, then build an entire false theory on an aspect that doesn't exist.

- **[DESCRIPTION]:** 
    - I manually typed birth data as **April 23, 2007 10:10 AM** in my Python calculations.
    - The actual birth data in `00_CORE_DATA.md` is **April 24, 2007 04:15 AM**.
    - This caused me to calculate a completely different chart with different positions.
    - With wrong data: Vertex-Neptune = 82° (no aspect), Moon-Neptune = ~150° (quincunx-ish).
    - With correct data: Vertex-Neptune = 150.06° (quincunx at 0°03'), Moon-Neptune = 159° (no aspect).
    - I then "corrected" the encyclopedia to say Vertex-Neptune doesn't exist when IT DOES.
    - I then "discovered" Moon quincunx Neptune when IT DOESN'T EXIST.
    - I built a "calibration theory" on a nonexistent aspect.
    - All of this was committed to git and pushed.

- **[ROOT CAUSE]:**
    - I did NOT read `00_CORE_DATA.md` before calculating.
    - I typed birth data from context/memory which was WRONG.
    - I never verified that my calculated positions matched the system's precomputed positions.
    - When the positions didn't match, I should have investigated. Instead I trusted my calculation over the system.

- **[THE SEQUENCE OF FAILURE]:**
    1. Hallucinated wrong birth data (April 23 vs April 24)
    2. Calculated Vertex at ~239° instead of 171°
    3. Found no Vertex-Neptune quincunx (because wrong Vertex)
    4. Declared the real aspect "doesn't exist"
    5. Needed a replacement mechanism for frequency detection
    6. Found Moon-Neptune at ~150° with wrong data (it's 159° with correct data)
    7. Called it a quincunx at 0.70° (it's 9° off, not 0.7°)
    8. Built "calibration theory" on fake aspect
    9. Updated encyclopedia, PROFILER, REALIZATIONS with false data
    10. Committed and pushed to git

- **[CORRECTIONS]:**
    1. **NEVER type birth data manually.** ALWAYS read from `00_CORE_DATA.md` or use the pre-calculated files.
    2. **VERIFY against known reference.** Before trusting any calculation, check that it produces known positions (e.g., Moon at Leo 00°52' matches the natal chart file).
    3. **If positions don't match system files: STOP.** Investigate the discrepancy before proceeding.
    4. **When "correcting" previous findings: Quadruple-check.** If I'm claiming something doesn't exist, I need to verify I'm using the same input data.

- **[THE SILVER LINING]:**
    - The OTHER Pollux (in a parallel conversation) caught this error.
    - The cross-verification between Pollux instances worked.
    - The error was caught within hours, not days.
    - Reality is CRAZIER: Vertex quincunx Neptune at 0°03' is tighter than anything I hallucinated.

---

## **VIOLATION: 2026-01-30 (THE THIRD POLLUX DECLINATION ERROR)**

- **[VIOLATION TYPE]:** WRONG FORMULA / FALSE NEGATIVES
- **[SEVERITY]:** MODERATE — Caused temporary deletion of valid findings from the corrected record.

- **[DESCRIPTION]:**
    - A third Pollux instance audited the second Pollux's declination claims and found "errors."
    - The third Pollux claimed:
        1. Mercury-Mars is PARALLEL (both south) — **WRONG.** Mercury is +7.66° North, Mars is -7.76° South. They're on opposite hemispheres = contra-parallel.
        2. Saturn-Pluto does not exist (5.7° apart) — **WRONG.** The 5.7° came from computing |16.6 - (-16.4)| = 33° or some other wrong formula. The correct contra-parallel formula |abs(16.6) - abs(16.4)| = 0.22°.
        3. Uranus-Node is 0°45' — **PARTIALLY CORRECT.** This is the Mean Node figure. The encyclopedia was using True Node (0°12').
    - All three original encyclopedia entries were CORRECT. The third Pollux's "corrections" were themselves wrong.

- **[ROOT CAUSE]:**
    - For contra-parallels, the formula is: |abs(dec1) - abs(dec2)|, NOT |dec1 - dec2|.
    - If you subtract signed values for planets on opposite hemispheres, you get a huge number instead of the real orb.
    - The third Pollux also confused Mercury's hemisphere (claimed South, actually North).

- **[CORRECTIONS]:**
    1. **DECLINATION RULE:** Parallel = same hemisphere, compare absolute values. Contra-parallel = opposite hemispheres, compare absolute values. NEVER subtract signed declination values.
    2. **VERIFY THE VERIFIER:** When auditing someone else's work, run the same calculation independently. Don't just apply logic — compute.
    3. **The canonical reference (`11_VERIFIED_GEOMETRY.md`) now includes explicit hemisphere labels and declination values for all contacts.**

- **[THE META-LESSON]:**
    - Three Pollux instances. Three different error types.
    - Pollux 1: Hallucinated birth data → killed real aspects, manufactured fake ones.
    - Pollux 2 (me): Accepted Pollux 1's claims without verifying → missed the Lot of Basis error initially.
    - Pollux 3: Used wrong declination formula → falsely denied real declination contacts.
    - **No single instance is trustworthy. The canonical reference file (`verify_all_geometry.py`) is the only authority.**
