import os
import shutil
from pathlib import Path

# Define paths
downloads_path = str(Path.home() / "Downloads")
destination_path = "D:/Storage Buffer"

# Ensure the destination directory exists
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

# Get list of files in Downloads folder
for file_name in os.listdir(downloads_path):
    # Check if the file ends with .jpg or .pdf (case-insensitive)
    if file_name.lower().endswith(('.jpg', '.pdf')):
        source_file = os.path.join(downloads_path, file_name)
        dest_file = os.path.join(destination_path, file_name)
        
        # Check if file already exists in destination
        if os.path.exists(dest_file):
            # Add a number to the filename to avoid overwriting
            base, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(dest_file):
                new_file_name = f"{base}_{counter}{ext}"
                dest_file = os.path.join(destination_path, new_file_name)
                counter += 1
        
        try:
            # Move the file
            shutil.move(source_file, dest_file)
            print(f"Moved: {file_name}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

print("File moving completed!")