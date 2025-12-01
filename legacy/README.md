# Legacy Scripts (Deprecated)

These scripts represent the original implementation of the Download Organizer.
They have been replaced by the modern, refactored `organizer.py` script.

## Why These Are Deprecated

1. **Code Duplication**: Each script contained nearly identical code
2. **Hard-coded Paths**: All paths were hard-coded in each file
3. **No Configuration**: No central configuration system
4. **Limited Error Handling**: Basic error handling only
5. **No Tests**: No unit test coverage
6. **Difficult to Maintain**: Adding new file types required creating entire new scripts

## Migration Guide

### Old Approach
```bash
python clean_downloads.py --folders
```

### New Approach
```bash
python organizer.py --folders
```

All functionality has been preserved and enhanced in the new system.

## Files in This Directory

- `clean_downloads.py` - Original main orchestration script
- `move_pdf.py` - Move PDF files
- `move_jpg.py` - Move JPG/JPEG files
- `move_png.py` - Move PNG files
- `move_mp4.py` - Move MP4 files
- `move_mov.py` - Move MOV files
- `move_sql.py` - Move SQL files
- `move_exe.py` - Move EXE files
- `move_compressed_folders.py` - Move compressed folders
- `move_folders.py` - Move regular folders

These files are kept for reference only and should not be used in production.
