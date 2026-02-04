# Ralph Ultimate Commands

### 1. Pollux Boot Loop (Verification & Setup)
```bash
/ralph:loop "$(cat /Users/Admin/Documents/11_Astrology/pollux_boot.md)" --keep-context --max-iterations 7 --completion-promise "SYSTEM_FULLY_OPERATIONAL"
```

### 2. Deep Forensic Audit (Truth Extraction)
```bash
/ralph:loop "$(cat /Users/Admin/Documents/11_Astrology/pollux_current_task.md)" --keep-context --max-iterations 20 --completion-promise "TASK_COMPLETED_WITH_MAXIMUM_DEPTH"
```

### 3. Emergency Cancel
```bash
/ralph:cancel
```

---
**Note:** If the agent ever asks for "setup.sh" again, it is hallucinating. The extension is now hardcoded to find it at: `/Users/Admin/.gemini/extensions/ralph/scripts/setup.sh`
