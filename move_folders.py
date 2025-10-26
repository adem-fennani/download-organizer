import os
import shutil
from pathlib import Path

downloads_path = str(Path.home() / "Downloads")
folders_destination_path = "D:/Storage Buffer/Folders"
if not os.path.exists(folders_destination_path):
    os.makedirs(folders_destination_path)

for item_name in os.listdir(downloads_path):
    item_path = os.path.join(downloads_path, item_name)
    
    if not os.path.isdir(item_path):
        continue
    
    print(f"Processing folder: {item_name}")
    
    dest_path = os.path.join(folders_destination_path, item_name)
    
    if os.path.exists(dest_path):
        base = item_name
        counter = 1
        while os.path.exists(dest_path):
            new_folder_name = f"{base}_{counter}"
            dest_path = os.path.join(folders_destination_path, new_folder_name)
            counter += 1
    
    try:
        print(f"Moving: {item_name}") 
        shutil.move(item_path, dest_path)
        print(f"Moved: {item_name} to {folders_destination_path}")
    except Exception as e:
        print(f"Error moving {item_name}: {e}")

print("Folder moving completed!")