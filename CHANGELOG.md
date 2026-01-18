# Changelog

All notable changes to the download-organizer project.

## [1.4.2] - 2026-01-18

### Fixed
- **Invalid Log Level Handling**: Added validation for log level configuration
  - Validates log level against allowed values (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Falls back to INFO level with a warning if invalid level is specified
  - Prevents AttributeError when invalid log levels are used in config
- **Race Condition in File Operations**: Added FileExistsError handling in `_move_item()`
  - Catches and handles race conditions when files are created between conflict resolution check and move operation
  - Logs clear error message when race condition occurs
  - Prevents crashes in concurrent environments
  - Added documentation note in `_resolve_conflict()` explaining inherent race condition

### Performance
- **Optimized Config Access**: Cached frequently accessed configuration sections
  - Cache `settings` and `folders` config sections during initialization
  - Eliminates repeated dictionary lookups throughout file processing
  - Reduces overhead when processing large numbers of files

## [1.4.1] - 2026-01-14

### Fixed
- **File Encoding**: Added `encoding='utf-8'` parameter to config file loading
  - Ensures consistent behavior across different systems and locales
  - Properly handles non-ASCII characters in configuration files
  - Prevents potential failures on systems with different default encodings
- **Case Sensitivity**: Fixed file extension matching to be case-insensitive
  - Extensions are now normalized to lowercase for reliable matching
  - Prevents files with uppercase extensions from being miscategorized
- **Statistics Tracking**: Implemented defaultdict for category statistics
  - Eliminates KeyError risks when tracking file categories
  - Cleaner code without manual key initialization

### Changed
- **Code Quality**: Extracted duplicate move logic into shared `_move_item()` method
  - Reduced code duplication between `_move_file()` and `_move_folder()`
  - Improved maintainability and consistency in error handling

## [1.4.0] - 2026-01-11

### Performance
- **Optimized Compressed Folder Detection**: Major performance improvements to `_is_compressed_folder()`
  - **Cached Compressed Extensions**: Build compressed extensions set once during initialization instead of rebuilding on every call
    - Eliminates 30,000 iterations for 1,000 folder checks (30 file types × 1,000 calls)
    - O(1) lookup instead of O(n) set reconstruction
  - **Shallow Directory Scan**: Replaced deep recursive scan with top-level-only checking
    - Changed from `rglob('*')` to `iterdir()` to avoid catastrophic performance on large folders
    - Prevents scanning thousands of nested files (e.g., node_modules, video projects)
    - Reduces checks from O(total files in tree) to O(top-level files)
  - **Combined Impact**: 1,000 calls now complete in ~0.0005 seconds with minimal overhead

### Changed
- Updated `_is_compressed_folder()` docstring to reflect shallow checking behavior

## [1.3.1] - 2026-01-09

### Added
- **Configuration Validation**: Added validation for required configuration keys (`source_directory`, `base_destination`)
  - Prevents runtime crashes with clear error messages if required keys are missing
  - Improves user experience with helpful error messages

### Changed
- **Simplified Batch File**: Removed all comments from `run_organizer.example.bat` for cleaner code
- **Enhanced Documentation**: Moved batch file setup instructions from comments to README.md
  - Added detailed "Scheduled Automation" section with step-by-step instructions
  - Improved clarity for both Python-in-PATH and custom Python path scenarios

### Removed
- **Legacy Folder**: Removed deprecated legacy scripts from version control
  - Folder still available locally but no longer tracked in git
  - Reduced repository clutter and confusion for new users

## [1.3.0] - 2026-01-03

### Added
- **Windows Task Scheduler Integration**: Added batch file support for automated scheduling
  - `run_organizer.example.bat` - Example batch file for Windows automation
  - Comprehensive documentation in README for setting up scheduled tasks
  - Step-by-step guide for Windows Task Scheduler configuration
  - Instructions for finding Python path and testing automation

### Changed
- Updated README with detailed "Scheduled Automation" section
- Enhanced documentation for Windows users wanting automatic organization

## [1.2.0] - 2026-01-01

### Added
- **Comprehensive File Extension Support**: Significantly expanded file type coverage to minimize files going to "Other" folder
  - **Ebooks**: `.epub`, `.mobi`, `.azw`, `.azw3`, `.djvu`
  - **Design**: `.psd`, `.ai`, `.sketch`, `.xd`, `.fig`, `.indd`
  - **Data/Config**: `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`, `.conf`
  - **Scripts**: `.sh`, `.bash`, `.zsh`, `.ps1`, `.bat`, `.cmd`
  - **Templates**: `.jinja`, `.jinja2`, `.j2`, `.tmpl`
  - **Data Science**: `.parquet`, `.feather`, `.hdf5`, `.h5`, `.mat`
  - **Disk Images**: `.iso`, `.img`, `.vhd`, `.vmdk`
  - **3D Models**: `.obj`, `.fbx`, `.stl`, `.blend`, `.max`, `.3ds`, `.dwg`, `.dxf`
  - **Fonts**: `.ttf`, `.otf`, `.woff`, `.woff2`
  - **Certificates**: `.pem`, `.crt`, `.cer`, `.key`, `.p12`, `.pfx`
  - **Backups**: `.bak`, `.backup`, `.old`, `.tmp`

### Enhanced
- **Documents**: Added `.md`, `.markdown`, `.rst`, `.tex`, `.doc`, `.rtf`, `.odt`
- **Images**: Added `.tiff`, `.tif`, `.ico`, `.heic`, `.heif`, `.gif`, `.bmp`, `.svg`, `.webp`
- **Videos**: Added `.webm`, `.m4v`, `.avi`, `.mkv`, `.flv`, `.wmv`
- **Audio**: Added `.wma`, `.opus`
- **Web**: Added `.htm`, `.scss`, `.sass`, `.less`
- **Code**: Added `.r`, `.m`, `.scala`, `.pl`, `.lua`
- **SQL**: Added `.db`, `.sqlite3`
- **Spreadsheets**: Added `.xls`, `.ods`
- **Presentations**: Added `.odp`
- **Executables**: Added `.deb`, `.rpm`, `.apk`
- **Compressed**: Added `.xz`

### Changed
- Updated `config.yaml` with 15+ new file categories and 60+ new file extensions
- Updated `config.example.yaml` with same comprehensive coverage

## [1.1.0] - 2025-12-11

### Added
- **Extended File Type Support**: Added support for additional file extensions
  - Documents: `.txt`, `.docx`
  - Spreadsheets: `.csv`, `.xlsx`
  - Presentations: `.ppt`, `.pptx`
  - Web files: `.html`
  - Notebooks: `.ipynb`
  - Code files: `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.cs`, `.java`, `.cpp`, `.c`, `.h`, `.go`, `.rb`, `.php`, `.swift`, `.kt`, `.rs`
- **New Configuration Categories**: 
  - `documents` category for text and Word documents
  - `spreadsheets` category for Excel and CSV files
  - `presentations` category for PowerPoint files
  - `web` category for HTML files
  - `notebooks` category for Jupyter notebooks
  - `code` category for programming language files

### Changed
- Updated `config.yaml` with new file type mappings
- Updated `config.example.yaml` to include all new extensions
- Updated README.md to reflect new file type support
- Project name standardized to `download-organizer` throughout documentation

## [1.0.0] - 2025-12-01

### Major Refactoring Release

This release represents a complete rewrite of the Download Organizer with modern best practices.

### Added
- **New Main Script**: `organizer.py` - unified, configurable organizer
- **Configuration System**: YAML-based configuration (`config.yaml`)
- **Comprehensive Logging**: File and console logging with multiple levels
- **Dry-Run Mode**: Preview changes before execution (`--dry-run`)
- **Statistics Tracking**: Detailed operation summaries
- **Unit Tests**: Full test suite (`test_organizer.py`)
- **Type Hints**: Complete type annotations throughout
- **Real-Time Monitoring**: Optional `watch_downloads.py` script
- **Documentation**:
  - Updated README.md with comprehensive guide
  - QUICKSTART.md for new users
  - MIGRATION.md for existing users
  - REFACTORING_SUMMARY.md for technical details
- **Example Configuration**: `config.example.yaml`
- **Requirements File**: `requirements.txt`
- **Git Ignore**: Proper `.gitignore`

### Changed
- **Architecture**: From 10+ scripts to single unified script
- **Configuration**: From hard-coded paths to YAML config
- **Execution**: From subprocess calls to direct Python functions
- **Error Handling**: Comprehensive exception handling with detailed logging
- **File Operations**: Using pathlib instead of os.path
- **Conflict Resolution**: Improved naming strategy for duplicates

### Improved
- **Code Quality**: 87% reduction in total lines of code
- **Maintainability**: Single source of truth for logic
- **Extensibility**: Easy to add new file types
- **User Experience**: Better feedback and reporting
- **Performance**: No subprocess overhead
- **Safety**: Dry-run mode and better error handling

### Deprecated
- `clean_downloads.py` - Use `organizer.py` instead
- `move_*.py` scripts - Functionality integrated into `organizer.py`
- All scripts moved to `legacy/` folder for reference

### Removed
- None (all legacy scripts preserved in `legacy/` folder)

### Fixed
- Duplicate code across multiple scripts
- Inconsistent error handling
- Hard-coded paths requiring code edits
- Lack of configuration flexibility
- No way to preview changes before execution
- No logging to file

### Security
- Added path validation to prevent traversal attacks
- Better permission error handling
- Safe file operations with atomic moves

### Technical Debt
- Eliminated ~90% code duplication
- Removed all hard-coded paths
- Centralized configuration
- Added comprehensive test coverage

## Initial Version

### Original Features
- Basic file organization by type
- Folder organization with `--folders` flag
- Individual scripts for each file type
- Subprocess-based execution
- Basic error printing

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backward-compatible functionality
- PATCH version for backward-compatible bug fixes
