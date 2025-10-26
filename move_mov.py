import os
import shutil
from pathlib import Path

downloads_path = str(Path.home() / "Downloads")
destination_path = "D:/Storage Buffer/MOV"

if not os.path.exists(destination_path):
    os.makedirs(destination_path)

for file_name in os.listdir(downloads_path):
    if file_name.lower().endswith('.mov'):
        source_file = os.path.join(downloads_path, file_name)
        dest_file = os.path.join(destination_path, file_name)
        
        if os.path.exists(dest_file):
            base, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(dest_file):
                new_file_name = f"{base}_{counter}{ext}"
                dest_file = os.path.join(destination_path, new_file_name)
                counter += 1
        
        try:
            shutil.move(source_file, dest_file)
            print(f"Moved: {file_name} to {destination_path}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

print("MOV file moving completed!")