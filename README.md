# DownloadOrganizer

A collection of Python scripts to automatically organize files and folders from your Downloads directory into a structured "Storage Buffer" system.

## Overview
This repository contains scripts to sort files by type (e.g., `.pdf`, `.jpg`, `.mp4`) into specific folders and optionally move large folders and compressed folders (e.g., `.zip`, `.rar`) when enabled. The main script, `clean_downloads.py`, serves as the entry point with a flexible argument to control heavy folder operations.

## Features
- Moves files with specific extensions to designated folders (e.g., `PDF`, `JPG_JPEG`, `MP4`).
- Moves unhandled files to an `Other` folder.
- Optionally moves compressed folders and regular folders to `Compressed Folders` and `Folders` respectively with the `--folders` flag.
- Provides real-time feedback with "Moving" and "Moved" messages.

## Installation
1. Clone the repository:
- git clone https://github.com/adem-fennani/DownloadOrganizer.git
cd DownloadOrganizer
2. Ensure Python 3.x is installed on your system.
3. Install Git if not already present (download from [git-scm.com](https://git-scm.com)).

## Usage
Run the main script from the command line:

### Basic File Organization
- python clean_downloads.py
- Moves files (e.g., `.pdf`, `.jpg`, `.zip`) to their respective folders.
- Skips folder moves by default.

### Include Folder Moves
- python clean_downloads.py -f
or
- python clean_downloads.py --folders
- Moves files and also handles large folders and compressed folders.
- Note: Moving large folders (e.g., >6GB) may take time.

### Help
- python clean_downloads.py -h
- Displays usage information and available options.

## Prerequisites
- Adjust the `scripts_path`, `downloads_path`, and `other_destination_path` variables in `clean_downloads.py` to match your system (e.g., `D:/Scripting`, `C:/Users/YourUsername/Downloads`, `D:/Storage Buffer/Other`).
- Ensure all dependent scripts (`move_pdf.py`, etc.) are in the specified `scripts_path`.

## Scripts
- `clean_downloads.py`: Main script to orchestrate file and folder organization.
- `move_pdf.py`, `move_jpg.py`, etc.: Handle specific file types.
- `move_compressed_folders.py`: Moves folders containing compressed files.
- `move_folders.py`: Moves regular folders.

## Contributing
Feel free to fork this repository, submit pull requests, or open issues for bugs or enhancements. Suggestions for additional file types or optimization (e.g., progress bars for large moves) are welcome!

## License
[Add a license here if desired, e.g., MIT License. For now, specify your intent or leave as TBD.]