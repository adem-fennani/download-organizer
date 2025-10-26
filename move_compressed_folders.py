import os
import shutil
from pathlib import Path

downloads_path = str(Path.home() / "Downloads")
compressed_destination_path = "D:/Storage Buffer/Compressed Folders"

compressed_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}

if not os.path.exists(compressed_destination_path):
    os.makedirs(compressed_destination_path)

def is_compressed_folder(folder_path, folder_name):
    if any(folder_name.lower().endswith(ext) for ext in compressed_extensions):
        return True
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in compressed_extensions):
                    return True
    except Exception as e:
        print(f"Warning: Could not fully check {folder_name} for compressed content: {e}")
    return False

for item_name in os.listdir(downloads_path):
    item_path = os.path.join(downloads_path, item_name)
    
    if not os.path.isdir(item_path):
        continue
    
    print(f"Processing potential compressed folder: {item_name}") 
    
    if is_compressed_folder(item_path, item_name):
        dest_path = os.path.join(compressed_destination_path, item_name)
        
        if os.path.exists(dest_path):
            base = item_name
            counter = 1
            while os.path.exists(dest_path):
                new_folder_name = f"{base}_{counter}"
                dest_path = os.path.join(compressed_destination_path, new_folder_name)
                counter += 1
        
        try:
            print(f"Moving: {item_name}") 
            shutil.move(item_path, dest_path)
            print(f"Moved compressed folder: {item_name} to {compressed_destination_path}")
        except Exception as e:
            print(f"Error moving {item_name}: {e}")

print("Compressed folder moving completed!")