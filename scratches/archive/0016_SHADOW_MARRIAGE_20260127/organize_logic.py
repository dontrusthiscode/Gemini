
import os
import datetime
import re

def organize_archive(archive_dir="scratches/archive"):
    if not os.path.exists(archive_dir):
        return
    
    # Get all subdirectories
    items = sorted([d for d in os.listdir(archive_dir) if os.path.isdir(os.path.join(archive_dir, d))])
    
    print(f"Organizing {len(items)} folders in {archive_dir}...")
    
    for folder in items:
        path = os.path.join(archive_dir, folder)
        
        # 1. Detect Creation Date (Best effort)
        stat = os.stat(path)
        date_str = datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y%m%d")
        
        # 2. Extract Slug and original index if present
        # Pattern: [digits]_[Slug]
        match = re.search(r'^(\d+)?_?(.*)', folder)
        if match:
            slug = match.group(2) if match.group(2) else folder
            # Strip existing date if already formatted as _YYYYMMDD
            slug = re.sub(r'_\d{8}(_\d{6})?$', '', slug)
        else:
            slug = folder
            
        # 3. Handle GHOST SESSIONS or malformed names
        if not slug or slug.strip() == "":
            slug = "system_session"
            
        # The script will be called sequentially, so we can't easily do global indexing here
        # without looking at the whole dir again. 
        # But for the REFACTOR, we will just apply a clean index based on the sort order.
        continue

# I'll write the logic directly into a proper script that can be run.
