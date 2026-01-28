# HORARY CASE TEMPLATE

This directory contains archived Horary questions that have been fully analyzed and closed.

## DIRECTORY STRUCTURE

Each Horary case follows this structure:

```
cases/horary/
├── 001_[SUBJECT]_[TOPIC]/
│   ├── GEMINI.md              # Case metadata and key findings
│   ├── 00_CHART_DATA/         # Original chart calculation files (FROZEN)
│   ├── 01_CONTEXT/            # Optional: Story, background, follow-ups
│   └── 02_OUTCOME/            # Optional: What actually happened
```

## NAMING CONVENTION

`[SEQUENCE]_[SUBJECT]_[TOPIC]`

Examples:
- `001_Fabi_Question` - First Horary, about Fabi
- `002_Career_Decision` - Second Horary, about career
- `003_Fabi_Revisit` - Third Horary, revisiting Fabi question

---

## WORKFLOW 1: NEW HORARY QUESTION

1. **Create Session:** `mkdir scratches/sessions/[NAME]`
2. **Calculate Chart:** `python3 environment/scripts/horary_generator.py [args] scratches/sessions/[NAME]`
3. **Analyze & Deliver Verdict:** Write `Result.md`
4. **Archive to Case:**
   ```bash
   mkdir -p cases/horary/[NNN]_[NAME]/00_CHART_DATA
   mv scratches/sessions/[NAME]/*.md cases/horary/[NNN]_[NAME]/00_CHART_DATA/
   ```
5. **Create GEMINI.md:** Document metadata, key findings, verdict
6. **Remove Session:** `rmdir scratches/sessions/[NAME]`

---

## WORKFLOW 2: REVISIT EXISTING CASE (SANDBOX PROTECTION)

When you want to dig deeper or add new analysis to a closed case:

1. **Create Revisit Session:**
   ```bash
   mkdir scratches/sessions/[CASE_NAME]_revisit
   cp -r cases/horary/[NNN]_[NAME]/00_CHART_DATA/* scratches/sessions/[CASE_NAME]_revisit/
   ```
2. **Work in Sandbox:** All new calculations and analysis happen in the session
3. **Compare:** When done, compare new findings with original
4. **Decision Point:**
   - **If BETTER:** Update original case (after verification)
   - **If DIFFERENT PERSPECTIVE:** Add to `01_CONTEXT/` as supplementary analysis
   - **If WRONG:** Add correction note to GEMINI.md, keep original for historical record
5. **Clean Session:** `rm -rf scratches/sessions/[CASE_NAME]_revisit`

**RULE:** Never directly edit `00_CHART_DATA/`. Always sandbox first.

---

## WORKFLOW 3: ADD CONTEXT TO CLOSED CASE

When you have new story context, background, or follow-up thoughts:

1. **Create Context Folder:** `mkdir cases/horary/[NNN]_[NAME]/01_CONTEXT`
2. **Add Context Files:**
   - `story.md` - Background narrative (why you asked, what led to this)
   - `synchronizations.md` - Natal contacts, omens observed
   - `followup_[DATE].md` - Later thoughts or related questions
3. **Update GEMINI.md:** Note that context was added

---

## WORKFLOW 4: RECORD OUTCOME

When you learn what actually happened after the Horary:

1. **Create Outcome Folder:** `mkdir cases/horary/[NNN]_[NAME]/02_OUTCOME`
2. **Add Outcome File:** `[DATE]_outcome.md`
   ```markdown
   # OUTCOME: [DATE]
   
   ## What Happened
   [Describe the actual outcome]
   
   ## Verdict Accuracy
   - Was the verdict correct? [YES/NO/PARTIAL]
   - What did the chart predict? [summary]
   - What actually occurred? [summary]
   
   ## Lessons Learned
   [Any insights for future Horary interpretation]
   ```
3. **Update GEMINI.md:** Add outcome summary to metadata
4. **Update REALIZATIONS.md:** If significant lesson learned

---

## WORKFLOW 5: MULTIPLE QUESTIONS SAME SUBJECT

When you ask another Horary about the same subject:

- Create NEW case: `002_Fabi_Followup` or `003_Fabi_Timing`
- Cross-reference in GEMINI.md: "Related: cases/horary/001_Fabi_Question"
- Each Horary is its own frozen moment—never merge into one case

---

## KEY PRINCIPLES

| Principle | Rule |
|:---|:---|
| **00_CHART_DATA is FROZEN** | Never edit after archival. Chart data is historical record. |
| **Sandbox Before Modify** | Always copy to session before reworking. |
| **Context is Additive** | New understanding goes to 01_CONTEXT, not overwriting. |
| **Outcomes are Separate** | What happened later doesn't change the original verdict. |
| **Cross-Reference** | Multiple questions about same subject = separate cases, linked. |

---

## DIFFERENCE FROM NATAL CASES

| Natal Case | Horary Case |
|:---|:---|
| One subject, many sessions | One question, one frozen moment |
| Ongoing investigation | Single point-in-time analysis |
| Updates with transits | Never updates (chart is fixed) |
| Accumulates discoveries | Verdict + Optional context/outcome |

