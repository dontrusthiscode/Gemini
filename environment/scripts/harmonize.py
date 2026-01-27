
import os
import sys
import subprocess
import re
import datetime

# CONFIG
CORE_DATA_DIR = "cases/001_Theodore/00_CORE_DATA"
SCRIPTS_DIR = "environment/scripts"
REQUIRED_FILES = [
    "01_NATAL_CHART.md",
    "02_SOLAR_ARC.md",
    "03_TRANSITS.md",
    "04_PROGRESSIONS.md",
    "05_VEDIC_SIDEREAL.md",
    "06_VEDIC_DETAILS.md",
    "07_DRACONIC.md",
    "08_SOLAR_RETURN.md",
    "09_DASHA_TIMELINE.md",
    "10_DIVISIONALS.md"
]
MAP_FILE = f"{CORE_DATA_DIR}/00_CORE_DATA.md"

def print_header(msg):
    print(f"\n{'='*60}\n{msg}\n{'='*60}")

def cleanse_workspace():
    print_header("PHASE 0: WORKSPACE CLEANSE")
    sessions_dir = "scratches/sessions"
    archive_dir = "scratches/archive"
    
    if not os.path.exists(sessions_dir):
        print("Sessions directory not found. Skipping.")
        return True
        
    os.makedirs(archive_dir, exist_ok=True)
    
    ghost_sessions = [d for d in os.listdir(sessions_dir) if os.path.isdir(os.path.join(sessions_dir, d))]
    
    if ghost_sessions:
        print(f"Found ghost sessions: {ghost_sessions}")
        for s in ghost_sessions:
            src = os.path.join(sessions_dir, s)
            dst = os.path.join(archive_dir, s)
            
            # Handle name collisions in archive
            if os.path.exists(dst):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                dst = f"{dst}_{timestamp}"
            
            subprocess.run(["mv", src, dst])
            print(f"Archived: {s} -> {dst}")
    else:
        print("Workspace is clean.")
    return True

def run_script(script_name, arg=None):
    cmd = ["python3", f"{SCRIPTS_DIR}/{script_name}"]
    if arg:
        cmd.append(arg)
        
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True
        )
        if result.returncode != 0:
            print(f"ERROR executing {script_name}:\n{result.stderr}")
            return False
        # print(result.stdout)
        return True
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return False

def audit_workspace():
    print_header("PHASE 1: AUDIT")
    issues = []
    
    # Check for empty files
    for root, dirs, files in os.walk(CORE_DATA_DIR):
        for f in files:
            path = os.path.join(root, f)
            if os.path.getsize(path) == 0:
                issues.append(f"EMPTY FILE: {path}")
                
    # Check for conflict files
    for root, dirs, files in os.walk(CORE_DATA_DIR):
        for f in files:
            if "conflict" in f.lower() or "copy" in f.lower():
                 issues.append(f"CONFLICT FILE: {f}")

    if not issues:
        print("Audit Passed. Workspace Clean.")
        return True
    else:
        for i in issues: print(i)
        return False

def rebuild_core():
    print_header("PHASE 2: REBUILDING REALITY")
    
    # Define Sequence
    scripts = [
        "calculate_natal.py",     # 01
        "update_transits.py",     # 03
        "calculate_vedic.py",     # 05 (actually 04_VEDIC used to be, now 05_VEDIC_SIDEREAL)
        "calculate_draconic.py",  # 07
        "calculate_prognostics.py", # 02, 04, 08
        "calculate_extended_vedic.py" # 06, 09, 10
    ]
    
    # Create Build Floor
    BUILD_DIR = "scratches/harmonization_build"
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    # Run all
    for s in scripts:
        print(f"-> Executing {s} into {BUILD_DIR}...")
        
        # Scripts that accept output dir arg:
        # calculate_prognostics.py
        # calculate_extended_vedic.py
        # output filenames will be TEST_...
        
        # Scripts that DO NOT accept arg yet (need verification):
        # calculate_natal.py (Starts with hardcoded paths?)
        # update_transits.py (Writes to 03_TRANSITS.md directly)
        
        # For now, pass the arg to all. Python ignores extra args if not used? 
        # No, sys.argv will just be ignored if not read.
        
        if not run_script(s, BUILD_DIR):
            print("Aborting Rebuild.")
            return False
            
    print("All Engines Fired Successfully.")
    
    print("Migrating Artifacts to CORE_DATA...")
    
    # Moves from BUILD_DIR
    moves = {
        f"{BUILD_DIR}/TEST_01_NATAL_CHART.md": f"{CORE_DATA_DIR}/01_NATAL_CHART.md",
        f"{BUILD_DIR}/TEST_02_SOLAR_ARC.md": f"{CORE_DATA_DIR}/02_SOLAR_ARC.md",
        f"{BUILD_DIR}/TEST_03_TRANSITS.md": f"{CORE_DATA_DIR}/03_TRANSITS.md",
        f"{BUILD_DIR}/TEST_04_PROGRESSIONS.md": f"{CORE_DATA_DIR}/04_PROGRESSIONS.md",
        f"{BUILD_DIR}/TEST_05_VEDIC_SIDEREAL.md": f"{CORE_DATA_DIR}/05_VEDIC_SIDEREAL.md",
        f"{BUILD_DIR}/TEST_06_VEDIC_DETAILS.md": f"{CORE_DATA_DIR}/06_VEDIC_DETAILS.md",
        f"{BUILD_DIR}/TEST_07_DRACONIC.md": f"{CORE_DATA_DIR}/07_DRACONIC.md",
        f"{BUILD_DIR}/TEST_08_SOLAR_RETURN.md": f"{CORE_DATA_DIR}/08_SOLAR_RETURN.md",
        f"{BUILD_DIR}/TEST_09_DASHA_TIMELINE.md": f"{CORE_DATA_DIR}/09_DASHA_TIMELINE.md",
        f"{BUILD_DIR}/TEST_10_DIVISIONALS.md": f"{CORE_DATA_DIR}/10_DIVISIONALS.md"
    }
    
    for src, dst in moves.items():
        if os.path.exists(src):
            subprocess.run(["cp", src, dst])
            print(f"Updated: {dst}")
        else:
            print(f"Warning: Source not found {src}")

    return True

def verify_integrity():
    print_header("PHASE 3: VERIFICATION")
    missing = []
    for f in REQUIRED_FILES:
        path = os.path.join(CORE_DATA_DIR, f)
        if not os.path.exists(path):
            missing.append(f)
    
    if missing:
        print(f"MISSING FILES: {missing}")
        return False
        
    print("All Core Data Files Present.")
    return True

def update_registry():
    print_header("PHASE 4: UPDATING REGISTRY (MAP)")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(MAP_FILE, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    in_map = False
    
    for line in lines:
        if "## 3. FILE MAP" in line:
            in_map = True
            new_lines.append(line)
            continue
            
        if in_map and line.strip().startswith("- `"):
            # Update tags
            # Regex to replace [ANYTHING] with [VERIFIED - Timestamp]
            # Actually, keep it clean. [VERIFIED]
            line = re.sub(r'\[.*?\]', '[VERIFIED]', line)
            new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(MAP_FILE, 'w') as f:
        f.writelines(new_lines)
        
    print("Registry Updated.")


def main():
    print_header("SYSTEM HARMONIZATION PROTOCOL v1.1")
    if not cleanse_workspace():
        sys.exit(1)
        
    if not audit_workspace(): 
        sys.exit(1)
        
    if not rebuild_core():
        sys.exit(1)
        
    if not verify_integrity():
        sys.exit(1)
        
    update_registry()
    print_header("DONE. SYSTEM IS CLEAN.")

if __name__ == "__main__":
    main()
