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
