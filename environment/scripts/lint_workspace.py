
import os
import re
import sys

# CONFIG
ROOT_DIR = "cases/001_Theodore/00_CORE_DATA"
EXPECTED_PATTERN = r"^\d{2}_[A-Z0-9_]+\.md$"

def lint_files():
    print(f"Linting {ROOT_DIR}...")
    files = sorted([f for f in os.listdir(ROOT_DIR) if f.endswith(".md") and f != "00_CORE_DATA.md"])
    
    errors = []
    seen_indices = {}
    
    for f in files:
        # Check Naming Convention
        if not re.match(EXPECTED_PATTERN, f):
            errors.append(f"Invalid Name: {f} (Expected XX_NAME.md)")
            continue
            
        # Check Index Collision
        idx = f.split('_')[0]
        if idx in seen_indices:
            errors.append(f"Index Collision: {idx} exists for {seen_indices[idx]} and {f}")
        seen_indices[idx] = f
        
    if errors:
        print("❌ LINT FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ WORKSPACE CLEAN. No collisions. Naming compliant.")

if __name__ == "__main__":
    if not os.path.exists(ROOT_DIR):
        print(f"Error: {ROOT_DIR} not found.")
        sys.exit(1)
    lint_files()
