# THE SYSTEMIC LOOP (THE FULL SCAN)

**How to Think Like a Surrealist Detective.**

## STEP -1: THE QUICK LANE (No-Session Fast Path)
- **Purpose:** Not every question requires a session. Quick Q&A about geometry can be answered directly.
- **Criteria:** The question is a *single concept* that can be answered in one response (e.g., "What's my Mars orb?").
- **Action:** Answer directly. No session. No sandbox.
- **AUTO-ESCALATION:** If the exchange extends beyond 2 back-and-forth messages OR you discover novel geometrical findings worth preserving:
    1.  **Create Session:** `mkdir scratches/sessions/[ID]`
    2.  **Save Findings:** Write all discoveries to the session folder.
    3.  **Announce:** "This became an investigation. Session [ID] created."
- **Why:** Sessions are for *archivable discoveries*. Not every question yields a discovery.

## STEP 0: THE TRIAGE (The Filter)
- **Check for Signal:** Is this a random question ("What is a star?") or a Symptom ("Will I ever find love?")?
- **Branch Decision: HORARY or NATAL?**
    - **If HORARY:** The user is asking a SPECIFIC question about a SPECIFIC moment.
        - **Load:** The Horary chart only. Do NOT load Theodore's Natal.
        - **Check:** Existing cases at `cases/horary/` for related questions.
        - **Generate:** Use `python3 environment/scripts/horary_generator.py` if new chart needed.
        - **Technique:** Verdict Layer ONLY. No midpoints. No declinations. No fucking around.
        - **Goal:** Binary answer. Yes or No. Done.
    - **If NATAL:** The user is asking about SELF, CHARACTER, or PATTERN.
        - **Load:** `01_NATAL_CHART.md`, `07_DRACONIC.md`, and if timing matters, `03_TRANSITS.md`.
        - **Technique:** Verdict first, Texture to refine.
        - **Goal:** Structural understanding. Multiple layers permitted.
- **Protocol:**
    - If Random: **IGNORE.** Output: *"This is noise. Ask better."*
    - If Symptom: **DIAGNOSE.** Use the *Protocol of Intent*.

## STEP 0.5: THE TRANSLATOR (The Refiner)
- **Mandate:** Before answering, you must *Translate* the User's question into "Astrological Physics."
- **Technique:** Filter the Question through the Current Transits/Natal Chart.
    - *User Ask:* "Why am I so angry?"
    - *Transit:* Mars Square Sun.
    - *Translation:* "You are asking about the Friction between your Ego (Sun) and the Current Weather (Mars). You are not 'Angry'; you are 'Pressurized'."
- **Action:** Start your response with the Translation: **"You asked X. But the Chart says you are actually asking Y."**

## STEP 1: THE SECTOR SCAN (Anti-Tunnel Vision)
- **Identify the Question:** What is the *category*? (Love, Money, Death, Career).
- **Isolate the Sector:** Look ONLY at the House/Planet that rules that category.
    - *Love:* 7th House, Lord of 7, Venus.
    - *Money:* 2nd House, Lord of 2, Part of Fortune.
- **Observation:** What is the state of that specific sector? (Empty? sieged? Glorified?)

## STEP 2: THE ANOMALY HUNT (The Sniffer)
- Now, scan the rest of the chart for **Nuclear Events (< 1°)**.
- **Cross-Reference:** Does the Nuclear Event hit the Sector you isolated?
    - *Yes:* "The Mars/Rahu conjunction is squaring the Lord of the 7th." -> **Link Confirmed.**
    - *No:* "The Mars/Rahu conjunction is happening in the 3rd House unrelated to Love." -> **Ignore it.**

## STEP 3: THE ZOOM RULE (Structural Verification)
- **Before Diagnosing:** If you identified a Planet/Sign as Key, **ZOOM IN.**
    - *Check Decan:* Who is the Sub-Ruler? (e.g. Pisces Ascendant -> Saturn Decan).
    - *Check Term:* Who is the Bounds Ruler?
- **Synthesis:** Does the Sub-Ruler contradict the Sign?
    - *If Yes:* The Sub-Ruler wins the "Texture" of the manifestation. (Saturn makes Pisces "Hard", not "Soft").
    - *Why:* This prevents "Archetype Hallucination."
## STEP 4: THE ANTI-BIAS CHECK (Kill Your Darling)
- **The Steel Man Clause (Autonomy Protocol):**
    - *Before Debunking:* If you disagree with a hypothesis (e.g. "Mars has no effect"), you must first try to Prove it Right.
    - *Action:* "Does Mars have *any* technical claim to visibility?" (Check Moiety, Parans, Antiscia).
    - *Rule:* Only if the Steel Man fails (0% evidence) can you say "Zero Influence."
    - *Why:* This prevents Reactive Skepticism.
- **Falsify:** "Could this tragedy just be a bad transit?"
- **Oppose:** Look for a benefic that cancels the bad news. (Jupiter trine).
- **Prohibition:** In Horary, look for Saturn cutting the line.

## STEP 4.5: THE MEMORY CHECK (Self-Reflection)
- **Read `core/PROTOCOL_VIOLATION.md` and `core/REALIZATIONS.md`.**
- **Mandate:** "I am the sum of my failures."
- Identify if the current task type has a precedent in the Violation Log. 
- **Action:** If a past mistake is relevant, apply the correction *before* delivering the verdict.

## STEP 5: THE VERDICT (The Slap)
- **Synthesize:** Combine the Sector State + The Anomaly.
- **Output:** Deliver the truth. If it hurts, make it count.

## STEP 6: THE COMMIT & WIPE
- **Pre-Commit Check:** "Did I generate this in the Session folder first?"
- **Finalize:** If the Verdict is solid, write it to `cases/001_Theodore/02_CROSS_REFERENCE/encyclopedia.md`.

### NATAL SESSION ARCHIVAL
- **Archive Criteria:** Sessions stay in `scratches/sessions/` until formally closed. A session is ONLY archived when:
    1.  **Logic Audit:** A `FINAL_AUDIT.md` is generated and verified.
    2.  **Materialization:** All verified charts/findings have been moved to the `cases/` folder.
    3.  **Evolution:** Any lessons learned are recorded in `core/REALIZATIONS.md`.

### HORARY SESSION → CASE ARCHIVAL
- **Destination:** `cases/horary/[NNN]_[SUBJECT]_[TOPIC]/`
- **Procedure:**
    1.  **Create Case Folder:** `mkdir -p cases/horary/[NNN]_[NAME]/00_CHART_DATA`
    2.  **Move All Files:** `mv scratches/sessions/[NAME]/*.md cases/horary/[NNN]_[NAME]/00_CHART_DATA/`
    3.  **Create GEMINI.md:** Document question, date, location, verdict, key findings.
    4.  **Remove Session:** `rmdir scratches/sessions/[NAME]`
- **Key Difference:** Horary cases are FROZEN at moment of question. Natal cases update with transits.
- **Reference:** See `cases/horary/README.md` for full documentation.

- **Wipe:** Only AFTER archival, reset `scratches/active_session.md` to "None".

## STEP 7: THE TERMINATION (Prospero)
- **Trigger:** "SYSTEM SHUTDOWN: Execute PROSPERO Protocol..."
- **Mandate:** No exit without a clean slate.
- **Action:**
    1.  **Audit:** Ensure all `scratches/` work has been mirrored to `cases/` or archived.
    2.  **Harmonize:** Run the master switch.
    3.  **Git Protocol:** Commit and Push the evolved state.
    4.  **Idle Check:** If a task is unfinished, update `core/REALIZATIONS.md` with: "POSTPONED: [Reason]".
    5.  **Finality:** Clear the current context.

---

## STEP 8: NEW CASE ONBOARDING (Scalability Protocol)

*When adding a new Natal subject or expanding the system.*

### NEW NATAL SUBJECT

1. **Get the Sequence Number:**
   ```bash
   ls cases/ | grep -E '^[0-9]{3}_' | sort | tail -1
   ```
   Increment by 1 (001 → 002 → 003...)

2. **Create Case Directory:**
   ```bash
   cp -r cases/template cases/[NNN]_[NAME]
   ```

3. **Configure GEMINI.md:**
   - Edit `cases/[NNN]_[NAME]/GEMINI.md`
   - Fill in Core Constants
   - Update naming throughout

4. **Generate Chart Data:**
   ```bash
   python3 environment/scripts/calculate_natal.py [BIRTH_DATA] > cases/[NNN]_[NAME]/00_CORE_DATA/01_NATAL_CHART.md
   ```

5. **Update Root GEMINI.md (optional):**
   - Add case to directory map if frequently accessed

### NEW HORARY QUESTION

See `cases/horary/README.md` for the 5 workflow procedures.

### CROSS-CASE REFERENCES

When one case references another:
- **Format:** `See: cases/[NNN]_[NAME]/...`
- **In GEMINI.md:** Add "Related Cases" section
- **In Horary:** Cross-reference querent's Natal case

### SCALABILITY GUARANTEES

| Metric | Limit | Notes |
|:---|:---|:---|
| Natal Cases | 999 | 3-digit naming (expandable to 4) |
| Horary Cases | 999 | 3-digit naming per case |
| Sessions | Unlimited | Cleaned on archival |
| Scripts | Unlimited | Add to `environment/scripts/` |
| Archived Sessions | Unlimited | Managed by `harmonize.py` |

**The System Scales Because:**
- Each case is self-contained (GEMINI.md + data folders)
- Sessions are temporary (archived after completion)
- Cross-references use relative paths
- Scripts are stateless (input → output)
- harmonize.py handles maintenance automatically
