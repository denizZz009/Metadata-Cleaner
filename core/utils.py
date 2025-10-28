"""Utility functions for metadata cleaning."""

import hashlib
import shutil
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def calculate_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """Calculate hash of file content."""
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def create_backup(file_path: Path, backup_dir: Optional[Path] = None) -> Path:
    """Create backup of file."""
    if backup_dir is None:
        backup_dir = file_path.parent / "metadata_cleaner_backups"
    
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Create unique backup filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = backup_dir / backup_name
    
    shutil.copy2(file_path, backup_path)
    logger.info(f"Created backup: {backup_path}")
    return backup_path


def verify_file_integrity(original_path: Path, cleaned_path: Path) -> bool:
    """Verify file can be opened after cleaning."""
    try:
        # Basic check - file exists and has content
        if not cleaned_path.exists():
            return False
        
        if cleaned_path.stat().st_size == 0:
            return False
        
        # File-type specific validation would go here
        return True
    except Exception as e:
        logger.error(f"Integrity check failed: {e}")
        return False


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size


def ensure_directory(directory: Path):
    """Ensure directory exists."""
    directory.mkdir(parents=True, exist_ok=True)


def is_supported_file(file_path: Path) -> bool:
    """Check if file type is supported."""
    from .enums import FileType
    ext = file_path.suffix.lower().lstrip('.')
    file_type = FileType.from_extension(ext)
    return file_type != FileType.UNKNOWN


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove potentially problematic characters."""
    import re
    # Remove or replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename
