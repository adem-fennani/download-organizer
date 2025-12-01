"""
Real-time Download Monitor - Automatically organize files as they're downloaded.

This optional script uses the watchdog library to monitor your downloads folder
and automatically organize files in real-time as they appear.

Install watchdog first: pip install watchdog

Usage:
    python watch_downloads.py
    python watch_downloads.py -c custom_config.yaml
"""

import sys
import time
import logging
import argparse
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog library is required for real-time monitoring.")
    print("Install it with: pip install watchdog")
    sys.exit(1)

try:
    from organizer import DownloadOrganizer
except ImportError:
    print("Error: Could not import organizer.py")
    print("Ensure organizer.py is in the same directory.")
    sys.exit(1)


class DownloadEventHandler(FileSystemEventHandler):
    """Handle file system events in the downloads folder."""
    
    def __init__(self, organizer: DownloadOrganizer):
        """Initialize the event handler with an organizer instance."""
        self.organizer = organizer
        self.logger = logging.getLogger(__name__)
        self.processing = set()  # Track files currently being processed
    
    def on_created(self, event):
        """Handle new file creation events."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip temporary or partial download files
        if self._is_temporary_file(file_path):
            return
        
        # Wait a bit to ensure file is fully written
        time.sleep(1)
        
        # Avoid processing the same file multiple times
        if file_path in self.processing:
            return
        
        self.processing.add(file_path)
        
        try:
            self.logger.info(f"New file detected: {file_path.name}")
            self._organize_file(file_path)
        finally:
            self.processing.discard(file_path)
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        # For download completion detection
        file_path = Path(event.src_path)
        
        # Only process if file is no longer temporary and fully downloaded
        if self._is_temporary_file(file_path):
            return
        
        if not file_path.exists():
            return
        
        # Check if file size is stable (not being written)
        if self._is_file_stable(file_path):
            if file_path not in self.processing:
                self.processing.add(file_path)
                try:
                    self.logger.debug(f"File completed: {file_path.name}")
                    self._organize_file(file_path)
                finally:
                    self.processing.discard(file_path)
    
    def _is_temporary_file(self, file_path: Path) -> bool:
        """Check if file is a temporary download file."""
        temp_extensions = {'.crdownload', '.tmp', '.part', '.download'}
        temp_prefixes = {'~', '.'}
        
        # Check extension
        if file_path.suffix.lower() in temp_extensions:
            return True
        
        # Check if filename starts with temp prefix
        if any(file_path.name.startswith(prefix) for prefix in temp_prefixes):
            return True
        
        return False
    
    def _is_file_stable(self, file_path: Path, wait_time: float = 0.5) -> bool:
        """Check if file size is stable (not being written)."""
        try:
            size1 = file_path.stat().st_size
            time.sleep(wait_time)
            size2 = file_path.stat().st_size
            return size1 == size2 and size1 > 0
        except (OSError, FileNotFoundError):
            return False
    
    def _organize_file(self, file_path: Path):
        """Organize a single file."""
        if not file_path.exists():
            self.logger.warning(f"File no longer exists: {file_path.name}")
            return
        
        try:
            # Check if should skip
            if self.organizer._should_skip_file(file_path):
                self.logger.debug(f"Skipping: {file_path.name}")
                return
            
            # Get destination
            dest_folder = self.organizer._get_destination_for_file(file_path)
            if dest_folder:
                success = self.organizer._move_file(file_path, dest_folder, dry_run=False)
                if success:
                    self.logger.info(f"✓ Organized: {file_path.name}")
                else:
                    self.logger.warning(f"✗ Failed to organize: {file_path.name}")
        
        except Exception as e:
            self.logger.error(f"Error organizing {file_path.name}: {e}")


class DownloadWatcher:
    """Monitor downloads folder and organize files in real-time."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the watcher with configuration."""
        self.organizer = DownloadOrganizer(config_path)
        self.logger = logging.getLogger(__name__)
        self.observer = None
    
    def start(self):
        """Start monitoring the downloads folder."""
        source_dir = self.organizer._expand_path(
            self.organizer.config['source_directory']
        )
        
        if not source_dir.exists():
            self.logger.error(f"Source directory does not exist: {source_dir}")
            return
        
        # Create event handler and observer
        event_handler = DownloadEventHandler(self.organizer)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(source_dir), recursive=False)
        
        # Start monitoring
        self.observer.start()
        
        print("=" * 60)
        print("📁 DOWNLOAD WATCHER STARTED")
        print("=" * 60)
        print(f"Monitoring: {source_dir}")
        print(f"Destination: {self.organizer.config['base_destination']}")
        print("\nWatching for new files... (Press Ctrl+C to stop)")
        print("=" * 60)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("\n" + "=" * 60)
            print("📁 DOWNLOAD WATCHER STOPPED")
            print("=" * 60)
            self.organizer.print_summary()


def main():
    """Main entry point for the watch script."""
    parser = argparse.ArgumentParser(
        description="Monitor downloads folder and organize files in real-time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python watch_downloads.py              # Use default config.yaml
  python watch_downloads.py -c custom.yaml   # Use custom configuration
  python watch_downloads.py -v           # Verbose logging
        """
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
        watcher = DownloadWatcher(config_path=args.config)
        
        # Override log level if verbose
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        watcher.start()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
