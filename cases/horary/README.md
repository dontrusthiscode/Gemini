# HORARY CASE TEMPLATE

This directory contains archived Horary questions that have been fully analyzed and closed.

## DIRECTORY STRUCTURE

Each Horary case follows this structure:

```
cases/horary/
├── 001_[SUBJECT]_[TOPIC]/
│   ├── GEMINI.md              # Case metadata and key findings
│   └── 00_CHART_DATA/         # All chart calculation files
│       ├── 00_CORE_DATA.md
│       ├── 01_HOUSES.md
│       ├── 02_BODIES.md
│       ├── ...
│       └── Result.md          # Final verdict
```

## NAMING CONVENTION

`[SEQUENCE]_[SUBJECT]_[TOPIC]`

Examples:
- `001_Fabi_Question` - First Horary, about Fabi
- `002_Career_Decision` - Second Horary, about career
- `003_Alice_Revisit` - Third Horary, about Alice

## SESSION → CASE WORKFLOW

1. **Session Created:** Start in `scratches/sessions/[NAME]/`
2. **Analysis Complete:** Deliver verdict in `Result.md`
3. **Archive to Case:**
   ```bash
   mkdir -p cases/horary/[NNN]_[NAME]/00_CHART_DATA
   mv scratches/sessions/[NAME]/*.md cases/horary/[NNN]_[NAME]/00_CHART_DATA/
   ```
4. **Create GEMINI.md:** Document metadata, key findings, outcome
5. **Remove Empty Session:** `rmdir scratches/sessions/[NAME]`

## WHEN TO CREATE A HORARY CASE

- Question was formally asked with crystallized intent
- Chart was cast and analyzed
- Verdict was delivered
- Native may want to revisit the question later

## DIFFERENCE FROM NATAL CASES

| Natal Case | Horary Case |
|:---|:---|
| One subject, many sessions | One question, one session |
| Ongoing investigation | Single point-in-time analysis |
| Accumulates over time | Frozen at moment of question |
| Updates with transits | Never updates (chart is fixed) |
