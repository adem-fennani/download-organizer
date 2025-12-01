import os
import shutil
import subprocess
import argparse
from pathlib import Path

scripts_path = "D:/Scripting"
downloads_path = str(Path.home() / "Downloads")
other_destination_path = "D:/Storage Buffer/Other"

parser = argparse.ArgumentParser(description="Clean Downloads folder by moving files and optionally heavy folders.")
parser.add_argument('-f', '--folders', action='store_true', help='Enable moving of heavy folders and compressed folders.')
args = parser.parse_args()

script_names = [
    "move_pdf.py",
    "move_jpg.py",
    "move_png.py",
    "move_mp4.py",
    "move_mov.py",
    "move_sql.py",
    "move_exe.py"
]

if args.folders:
    script_names.extend(["move_compressed_folders.py", "move_folders.py"])

for script in script_names:
    script_full_path = os.path.join(scripts_path, script)
    if os.path.exists(script_full_path):
        try:
            print(f"Running {script}...")
            subprocess.run(["python", script_full_path], check=True)
            print(f"Finished running {script}")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e.stderr if e.stderr else e}")
        except FileNotFoundError:
            print(f"Script not found: {script_full_path}")
    else:
        print(f"Script not found: {script_full_path}")

if not os.path.exists(other_destination_path):
    os.makedirs(other_destination_path)

handled_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.mp4', '.mov', '.sql', '.exe', '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}

for file_name in os.listdir(downloads_path):
    file_path = os.path.join(downloads_path, file_name)
    
    if os.path.isdir(file_path):
        continue
    
    if not any(file_name.lower().endswith(ext) for ext in handled_extensions):
        dest_file = os.path.join(other_destination_path, file_name)
        
        if os.path.exists(dest_file):
            base, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(dest_file):
                new_file_name = f"{base}_{counter}{ext}"
                dest_file = os.path.join(other_destination_path, new_file_name)
                counter += 1
        
        try:
            print(f"Moving: {file_name}")
            shutil.move(file_path, dest_file)
            print(f"Moved: {file_name} to {other_destination_path}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

print("Downloads folder cleaning completed!")