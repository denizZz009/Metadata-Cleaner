"""Main metadata cleaner orchestrator."""

from pathlib import Path
from typing import Optional, List
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from .enums import CleaningLevel, FileType
from .result import CleaningResult, BatchCleaningResult
from .utils import (
    calculate_file_hash, create_backup, verify_file_integrity,
    get_file_size, is_supported_file
)
from ..cleaners import (
    PDFCleaner, OfficeCleaner, ImageCleaner,
    AudioCleaner, VideoCleaner, TextCleaner
)

logger = logging.getLogger(__name__)


class MetadataCleaner:
    """Main metadata cleaner class."""
    
    def __init__(
        self,
        level: CleaningLevel = CleaningLevel.DEEP,
        backup: bool = True,
        verify: bool = True,
        backup_dir: Optional[Path] = None
    ):
        """
        Initialize metadata cleaner.
        
        Args:
            level: Cleaning thoroughness level
            backup: Whether to create backups before cleaning
            verify: Whether to verify file integrity after cleaning
            backup_dir: Custom backup directory
        """
        self.level = level
        self.backup = backup
        self.verify = verify
        self.backup_dir = Path(backup_dir) if backup_dir else None
        
        # Initialize cleaners
        self.cleaners = {
            'pdf': PDFCleaner(level),
            'office': OfficeCleaner(level),
            'image': ImageCleaner(level),
            'audio': AudioCleaner(level),
            'video': VideoCleaner(level),
            'text': TextCleaner(level),
        }
    
    def clean_file(
        self,
        file_path: str | Path,
        output_path: Optional[str | Path] = None
    ) -> CleaningResult:
        """
        Clean metadata from a single file.
        
        Args:
            file_path: Path to input file
            output_path: Path to output file (defaults to overwriting input)
            
        Returns:
            CleaningResult object
        """
        file_path = Path(file_path)
        output_path = Path(output_path) if output_path else file_path
        
        start_time = time.time()
        
        # Check if file exists
        if not file_path.exists():
            return CleaningResult(
                file_path=file_path,
                success=False,
                original_size=0,
                cleaned_size=0,
                errors=[f"File not found: {file_path}"]
            )
        
        # Check if file type is supported
        if not is_supported_file(file_path):
            return CleaningResult(
                file_path=file_path,
                success=False,
                original_size=get_file_size(file_path),
                cleaned_size=0,
                errors=[f"Unsupported file type: {file_path.suffix}"]
            )
        
        # Get original file info
        original_size = get_file_size(file_path)
        content_hash_before = calculate_file_hash(file_path) if self.verify else None
        
        # Create backup if requested
        backup_path = None
        if self.backup:
            try:
                backup_path = create_backup(file_path, self.backup_dir)
            except Exception as e:
                logger.error(f"Failed to create backup: {e}")
                return CleaningResult(
                    file_path=file_path,
                    success=False,
                    original_size=original_size,
                    cleaned_size=0,
                    errors=[f"Failed to create backup: {e}"]
                )
        
        # Get appropriate cleaner
        cleaner = self._get_cleaner(file_path)
        if not cleaner:
            return CleaningResult(
                file_path=file_path,
                success=False,
                original_size=original_size,
                cleaned_size=0,
                errors=[f"No cleaner available for: {file_path.suffix}"]
            )
        
        # Clean the file
        success = cleaner.clean(file_path, output_path)
        
        # Get results
        cleaned_size = get_file_size(output_path) if output_path.exists() else 0
        content_hash_after = calculate_file_hash(output_path) if self.verify and output_path.exists() else None
        processing_time = time.time() - start_time
        
        # Verify integrity if requested
        if self.verify and success:
            if not verify_file_integrity(file_path, output_path):
                cleaner.add_warning("File integrity verification failed")
        
        return CleaningResult(
            file_path=file_path,
            success=success,
            original_size=original_size,
            cleaned_size=cleaned_size,
            metadata_removed=cleaner.metadata_removed,
            errors=cleaner.errors,
            warnings=cleaner.warnings,
            processing_time=processing_time,
            backup_path=backup_path,
            content_hash_before=content_hash_before,
            content_hash_after=content_hash_after
        )
    
    def clean_folder(
        self,
        folder_path: str | Path,
        recursive: bool = False,
        max_workers: int = 4
    ) -> BatchCleaningResult:
        """
        Clean metadata from all supported files in a folder.
        
        Args:
            folder_path: Path to folder
            recursive: Whether to process subfolders
            max_workers: Number of parallel workers
            
        Returns:
            BatchCleaningResult object
        """
        folder_path = Path(folder_path)
        batch_result = BatchCleaningResult()
        start_time = time.time()
        
        if not folder_path.exists() or not folder_path.is_dir():
            logger.error(f"Folder not found: {folder_path}")
            return batch_result
        
        # Find all supported files
        pattern = '**/*' if recursive else '*'
        all_files = [f for f in folder_path.glob(pattern) if f.is_file()]
        supported_files = [f for f in all_files if is_supported_file(f)]
        
        logger.info(f"Found {len(supported_files)} supported files in {folder_path}")
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.clean_file, file_path): file_path
                for file_path in supported_files
            }
            
            for future in as_completed(futures):
                result = future.result()
                batch_result.add_result(result)
        
        batch_result.total_time = time.time() - start_time
        batch_result.skipped = len(all_files) - len(supported_files)
        
        return batch_result
    
    def clean_files(
        self,
        file_paths: List[str | Path],
        max_workers: int = 4
    ) -> BatchCleaningResult:
        """
        Clean metadata from multiple files.
        
        Args:
            file_paths: List of file paths
            max_workers: Number of parallel workers
            
        Returns:
            BatchCleaningResult object
        """
        batch_result = BatchCleaningResult()
        start_time = time.time()
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.clean_file, file_path): file_path
                for file_path in file_paths
            }
            
            for future in as_completed(futures):
                result = future.result()
                batch_result.add_result(result)
        
        batch_result.total_time = time.time() - start_time
        
        return batch_result
    
    def _get_cleaner(self, file_path: Path):
        """Get appropriate cleaner for file type."""
        file_type = FileType.from_extension(file_path.suffix)
        
        if file_type == FileType.PDF:
            return self.cleaners['pdf']
        elif file_type in [FileType.DOCX, FileType.XLSX, FileType.PPTX,
                          FileType.ODT, FileType.ODS, FileType.ODP]:
            return self.cleaners['office']
        elif file_type.is_image():
            return self.cleaners['image']
        elif file_type.is_audio():
            return self.cleaners['audio']
        elif file_type.is_video():
            return self.cleaners['video']
        elif file_type in [FileType.TXT, FileType.RTF]:
            return self.cleaners['text']
        
        return None
