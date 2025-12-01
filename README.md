# DownloadOrganizer

A modern, configurable Python tool to automatically organize files and folders from your Downloads directory into a structured storage system.

## Overview
DownloadOrganizer is a refactored, professional-grade file organization tool that sorts files by type (e.g., `.pdf`, `.jpg`, `.mp4`) into designated folders. Built with best practices including configuration files, comprehensive logging, dry-run mode, conflict resolution, and full test coverage.

## ✨ Features
- **Configuration-Driven**: All settings in a single YAML file - no hard-coded paths
- **Comprehensive Logging**: File and console logging with configurable levels
- **Dry-Run Mode**: Preview changes before executing
- **Smart Conflict Resolution**: Automatic file name conflict handling
- **Statistics & Reporting**: Detailed summary of operations
- **Type Hints**: Full type annotation for better code maintenance
- **Error Handling**: Robust error handling with detailed logging
- **Unit Tests**: Comprehensive test coverage
- **Flexible File Types**: Easy to add new file categories
- **Folder Organization**: Optional compressed and regular folder handling

## 🚀 Installation

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/adem-fennani/downloa-organizer.git
cd download-organizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings:
```bash
# Edit config.yaml to set your paths and preferences
notepad config.yaml  # Windows
nano config.yaml     # Linux/Mac
```

### Requirements
- Python 3.7 or higher
- PyYAML (automatically installed with requirements.txt)

## 📖 Usage

### Basic Commands

**Organize files only:**
```bash
python organizer.py
```

**Include folder organization:**
```bash
python organizer.py --folders
```

**Preview without moving (dry-run):**
```bash
python organizer.py --dry-run
```

**Organize files and folders with preview:**
```bash
python organizer.py -f --dry-run
```

**Use custom configuration:**
```bash
python organizer.py -c my_config.yaml
```

**Verbose logging:**
```bash
python organizer.py -v
```

### Command-Line Options
- `-f, --folders`: Include folder organization
- `--dry-run`: Preview changes without moving files
- `-c, --config PATH`: Specify custom config file
- `-v, --verbose`: Enable debug logging
- `-h, --help`: Show help message

## ⚙️ Configuration

Edit `config.yaml` to customize behavior:

```yaml
# Source and destination paths
source_directory: "~/Downloads"
base_destination: "D:/Storage Buffer"

# Define file type mappings
file_types:
  pdf:
    extensions: [".pdf"]
    destination: "PDF"
  images:
    extensions: [".jpg", ".jpeg", ".png"]
    destination: "Images"
  # Add more types as needed

# Logging configuration
logging:
  level: "INFO"
  log_file: "download_organizer.log"
  
# Operation settings
settings:
  dry_run: false
  create_directories: true
  handle_conflicts: true
  skip_hidden_files: true
```

### Adding New File Types
Simply add a new entry to the `file_types` section in `config.yaml`:

```yaml
file_types:
  documents:
    extensions: [".doc", ".docx", ".txt"]
    destination: "Documents"
```

## 🧪 Testing

Run the test suite:
```bash
# Using unittest
python -m unittest test_organizer.py -v

# Using pytest (if installed)
python -m pytest test_organizer.py -v
```

## 📂 Project Structure

```
DownloadOrganizer/
├── organizer.py              # Main refactored script
├── config.yaml               # Configuration file
├── test_organizer.py         # Unit tests
├── requirements.txt          # Python dependencies
├── watch_downloads.py        # Optional: Real-time monitoring
├── README.md                 # This file
└── legacy/                   # Original scripts (deprecated)
    ├── clean_downloads.py
    ├── move_pdf.py
    └── ...
```

## 🔄 Migration from Legacy Scripts

The new `organizer.py` replaces all legacy scripts (`clean_downloads.py`, `move_*.py`) with a single, maintainable solution.

**Old way:**
```bash
python clean_downloads.py --folders
```

**New way:**
```bash
python organizer.py --folders
```

Benefits:
- ✅ No hard-coded paths
- ✅ Single file to maintain
- ✅ Better error handling
- ✅ Comprehensive logging
- ✅ Test coverage

## 🔧 Advanced Features

### Real-Time Monitoring (Optional)
Use `watch_downloads.py` to automatically organize files as they're downloaded:
```bash
python watch_downloads.py
```

This uses the watchdog library to monitor your downloads folder and organize files in real-time.

## 📊 Example Output

```
2025-12-01 10:30:15 - organizer - INFO - Starting organization of: C:\Users\You\Downloads
2025-12-01 10:30:15 - organizer - INFO - Moving: document.pdf -> D:\Storage Buffer\PDF
2025-12-01 10:30:15 - organizer - INFO - Moved: document.pdf
2025-12-01 10:30:16 - organizer - INFO - Moving: photo.jpg -> D:\Storage Buffer\Images
2025-12-01 10:30:16 - organizer - INFO - Moved: photo.jpg
2025-12-01 10:30:16 - organizer - INFO - Organization completed!

============================================================
ORGANIZATION SUMMARY
============================================================
Files moved: 15
Folders moved: 3
Conflicts resolved: 2
Skipped: 1
Errors: 0

Files by category:
  images: 7
  pdf: 5
  videos: 3
============================================================
```

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Add tests for new functionality
4. Ensure all tests pass (`python -m unittest test_organizer.py`)
5. Submit a pull request

## 📝 License
This project is open source and available under the MIT License.

## 🐛 Troubleshooting

**Issue: "Configuration file not found"**
- Ensure `config.yaml` exists in the same directory as `organizer.py`
- Or specify the config path: `python organizer.py -c path/to/config.yaml`

**Issue: "Permission denied" errors**
- Run with appropriate permissions
- Check that files aren't open in other applications
- Verify write permissions on destination folders

**Issue: Files not being organized**
- Check that file extensions in `config.yaml` match your files
- Use `--verbose` flag to see debug information
- Try `--dry-run` first to preview behavior

## 📞 Support
For issues, questions, or suggestions, please open an issue on GitHub.

## ⚠️ Legacy Scripts (Deprecated)
The original scripts (`clean_downloads.py`, `move_*.py`) are kept for reference but are deprecated. Please use `organizer.py` for all new projects.

## Contributing
Feel free to fork this repository, submit pull requests, or open issues for bugs or enhancements. Suggestions for additional file types or optimization are welcome!