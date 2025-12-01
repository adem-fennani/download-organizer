"""
Download Organizer - A modern, configurable file organization tool.

This script organizes files from your Downloads folder into categorized
directories based on file types, with support for conflict resolution,
logging, and dry-run mode.
"""

import os
import shutil
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml")
    exit(1)


@dataclass
class OrganizationStats:
    """Track statistics for file organization operations."""
    files_moved: int = 0
    folders_moved: int = 0
    errors: int = 0
    skipped: int = 0
    conflicts_resolved: int = 0
    categories: Dict[str, int] = field(default_factory=lambda: defaultdict(int))


class DownloadOrganizer:
    """Main class for organizing downloads into categorized folders."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the organizer with configuration."""
        self.config = self._load_config(config_path)
        self.stats = OrganizationStats()
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                "Please create a config.yaml file or specify a valid path."
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")
    
    def _setup_logging(self) -> None:
        """Configure logging based on config settings."""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        
        handlers = []
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        if log_config.get('log_to_console', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            handlers.append(console_handler)
        
        if log_config.get('log_to_file', True):
            log_file = log_config.get('log_file', 'download_organizer.log')
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
        
        logging.basicConfig(level=level, handlers=handlers, force=True)
    
    def _expand_path(self, path_str: str) -> Path:
        """Expand user home directory and convert to absolute Path."""
        return Path(path_str).expanduser().resolve()
    
    def _get_destination_for_file(self, file_path: Path) -> Optional[Path]:
        """Determine the destination folder for a given file."""
        extension = file_path.suffix.lower()
        base_dest = self._expand_path(self.config['base_destination'])
        
        # Check each file type category
        for category, info in self.config.get('file_types', {}).items():
            extensions = info.get('extensions', [])
            if extension in extensions:
                dest_folder = info.get('destination', category)
                self.stats.categories[category] += 1
                return base_dest / dest_folder
        
        # No matching category found
        other_dest = self.config.get('other_destination', 'Other')
        self.stats.categories['other'] += 1
        return base_dest / other_dest
    
    def _resolve_conflict(self, dest_path: Path) -> Path:
        """Resolve file name conflicts by appending a counter."""
        if not dest_path.exists():
            return dest_path
        
        self.stats.conflicts_resolved += 1
        stem = dest_path.stem
        suffix = dest_path.suffix
        parent = dest_path.parent
        counter = 1
        
        while dest_path.exists():
            new_name = f"{stem}_{counter}{suffix}"
            dest_path = parent / new_name
            counter += 1
        
        return dest_path
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped based on settings."""
        settings = self.config.get('settings', {})
        
        # Skip hidden files if configured
        if settings.get('skip_hidden_files', True) and file_path.name.startswith('.'):
            return True
        
        return False
    
    def _move_file(self, source: Path, destination_folder: Path, dry_run: bool = False) -> bool:
        """Move a file to the destination folder."""
        try:
            # Create destination directory if needed
            if self.config.get('settings', {}).get('create_directories', True):
                if not dry_run:
                    destination_folder.mkdir(parents=True, exist_ok=True)
            
            dest_path = destination_folder / source.name
            
            # Handle conflicts if enabled
            if self.config.get('settings', {}).get('handle_conflicts', True):
                dest_path = self._resolve_conflict(dest_path)
            
            if dry_run:
                self.logger.info(f"[DRY RUN] Would move: {source.name} -> {dest_path}")
            else:
                self.logger.info(f"Moving: {source.name} -> {dest_path}")
                shutil.move(str(source), str(dest_path))
                self.logger.info(f"Moved: {source.name}")
            
            self.stats.files_moved += 1
            return True
            
        except PermissionError:
            self.logger.error(f"Permission denied: {source.name}")
            self.stats.errors += 1
            return False
        except shutil.Error as e:
            self.logger.error(f"Error moving {source.name}: {e}")
            self.stats.errors += 1
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error moving {source.name}: {e}")
            self.stats.errors += 1
            return False
    
    def _is_compressed_folder(self, folder_path: Path) -> bool:
        """Check if a folder contains or is a compressed file."""
        compressed_exts = set()
        for info in self.config.get('file_types', {}).values():
            if 'compressed' in str(info.get('destination', '')).lower():
                compressed_exts.update(info.get('extensions', []))
        
        # Check if folder name has compressed extension
        if folder_path.suffix.lower() in compressed_exts:
            return True
        
        # Check if folder contains compressed files
        try:
            for item in folder_path.rglob('*'):
                if item.is_file() and item.suffix.lower() in compressed_exts:
                    return True
        except (PermissionError, OSError) as e:
            self.logger.warning(f"Could not fully check {folder_path.name}: {e}")
        
        return False
    
    def _move_folder(self, source: Path, destination_folder: Path, dry_run: bool = False) -> bool:
        """Move a folder to the destination."""
        try:
            if self.config.get('settings', {}).get('create_directories', True):
                if not dry_run:
                    destination_folder.mkdir(parents=True, exist_ok=True)
            
            dest_path = destination_folder / source.name
            
            # Handle conflicts
            if self.config.get('settings', {}).get('handle_conflicts', True):
                dest_path = self._resolve_conflict(dest_path)
            
            if dry_run:
                self.logger.info(f"[DRY RUN] Would move folder: {source.name} -> {dest_path}")
            else:
                self.logger.info(f"Moving folder: {source.name} -> {dest_path}")
                shutil.move(str(source), str(dest_path))
                self.logger.info(f"Moved folder: {source.name}")
            
            self.stats.folders_moved += 1
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving folder {source.name}: {e}")
            self.stats.errors += 1
            return False
    
    def organize_files(self, dry_run: bool = False) -> None:
        """Organize files from the downloads folder."""
        source_dir = self._expand_path(self.config['source_directory'])
        
        if not source_dir.exists():
            self.logger.error(f"Source directory does not exist: {source_dir}")
            return
        
        self.logger.info(f"Starting organization of: {source_dir}")
        if dry_run:
            self.logger.info("DRY RUN MODE - No files will be moved")
        
        # Process files
        for item in source_dir.iterdir():
            if item.is_file():
                if self._should_skip_file(item):
                    self.logger.debug(f"Skipping: {item.name}")
                    self.stats.skipped += 1
                    continue
                
                dest_folder = self._get_destination_for_file(item)
                if dest_folder:
                    self._move_file(item, dest_folder, dry_run)
    
    def organize_folders(self, dry_run: bool = False) -> None:
        """Organize folders from the downloads folder."""
        source_dir = self._expand_path(self.config['source_directory'])
        base_dest = self._expand_path(self.config['base_destination'])
        folder_config = self.config.get('folders', {})
        
        compressed_dest = base_dest / folder_config.get('compressed_destination', 'Compressed Folders')
        regular_dest = base_dest / folder_config.get('regular_destination', 'Folders')
        
        self.logger.info("Processing folders...")
        
        for item in source_dir.iterdir():
            if item.is_dir():
                if self._should_skip_file(item):
                    self.logger.debug(f"Skipping folder: {item.name}")
                    self.stats.skipped += 1
                    continue
                
                # Determine if it's a compressed folder
                if self._is_compressed_folder(item):
                    self._move_folder(item, compressed_dest, dry_run)
                else:
                    self._move_folder(item, regular_dest, dry_run)
    
    def print_summary(self) -> None:
        """Print a summary of the organization operation."""
        print("\n" + "=" * 60)
        print("ORGANIZATION SUMMARY")
        print("=" * 60)
        print(f"Files moved: {self.stats.files_moved}")
        print(f"Folders moved: {self.stats.folders_moved}")
        print(f"Conflicts resolved: {self.stats.conflicts_resolved}")
        print(f"Skipped: {self.stats.skipped}")
        print(f"Errors: {self.stats.errors}")
        
        if self.stats.categories:
            print("\nFiles by category:")
            for category, count in sorted(self.stats.categories.items()):
                print(f"  {category}: {count}")
        
        print("=" * 60)
    
    def run(self, include_folders: bool = False, dry_run: bool = False) -> None:
        """Run the organization process."""
        try:
            self.organize_files(dry_run)
            
            if include_folders:
                self.organize_folders(dry_run)
            
            self.logger.info("Organization completed!")
            self.print_summary()
            
        except KeyboardInterrupt:
            self.logger.warning("\nOperation cancelled by user")
            self.print_summary()
        except Exception as e:
            self.logger.error(f"Fatal error: {e}", exc_info=True)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Organize your downloads folder automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  organizer.py                     # Organize files only
  organizer.py -f                  # Organize files and folders
  organizer.py --dry-run           # Preview what would be moved
  organizer.py -f --dry-run        # Preview files and folders
  organizer.py -c custom.yaml      # Use custom configuration file
        """
    )
    
    parser.add_argument(
        '-f', '--folders',
        action='store_true',
        help='Include folder organization (compressed and regular folders)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be moved without actually moving files'
    )
    
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose (DEBUG level) logging'
    )
    
    args = parser.parse_args()
    
    try:
        organizer = DownloadOrganizer(config_path=args.config)
        
        # Override log level if verbose
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Override dry_run from config if specified in args
        dry_run = args.dry_run or organizer.config.get('settings', {}).get('dry_run', False)
        
        organizer.run(include_folders=args.folders, dry_run=dry_run)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Fatal Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
