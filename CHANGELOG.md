# Changelog

All notable changes to the download-organizer project.

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
