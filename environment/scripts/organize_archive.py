
import os
import datetime
import re
import shutil

def organize_archive(archive_dir="scratches/archive"):
    if not os.path.exists(archive_dir):
        print(f"Archive directory {archive_dir} not found.")
        return
    
    # 1. Gather all directories and their creation dates
    dir_data = []
    for d in os.listdir(archive_dir):
        path = os.path.join(archive_dir, d)
        if os.path.isdir(path):
            stat = os.stat(path)
            # Use ctime as the creation date proxy
            creation_time = datetime.datetime.fromtimestamp(stat.st_ctime)
            
            # Clean name: remove leading numbers and trailing dates
            # Example: 001_Effect_vs_Cause_20260127 -> Effect_vs_Cause
            name = d
            name = re.sub(r'^\d+_', '', name) # Remove leading 001_
            name = re.sub(r'_\d{8}(_\d{6})?$', '', name) # Remove trailing _20260127
            
            dir_data.append({
                'old_path': path,
                'old_name': d,
                'name': name,
                'ctime': creation_time
            })
            
    # 2. Sort by creation time
    dir_data.sort(key=lambda x: x['ctime'])
    
    # 3. Rename with new convention: 0000_Name_YYYYMMDD
    print(f"Organizing {len(dir_data)} sessions...")
    
    for i, data in enumerate(dir_data, 1):
        idx_str = f"{i:04d}"
        date_str = data['ctime'].strftime("%Y%m%d")
        new_name = f"{idx_str}_{data['name']}_{date_str}"
        new_path = os.path.join(archive_dir, new_name)
        
        # Avoid collisions
        if os.path.exists(new_path) and new_path != data['old_path']:
             timestamp = datetime.datetime.now().strftime("%H%M%S")
             new_name = f"{idx_str}_{data['name']}_{date_str}_{timestamp}"
             new_path = os.path.join(archive_dir, new_name)
             
        if new_path != data['old_path']:
            try:
                os.rename(data['old_path'], new_path)
                print(f"RENAMED: {data['old_name']} -> {new_name}")
            except Exception as e:
                print(f"FAILED: {data['old_name']} -> {e}")
        else:
            print(f"SKIPPED: {data['old_name']} (Already compliant)")

if __name__ == "__main__":
    organize_archive()
