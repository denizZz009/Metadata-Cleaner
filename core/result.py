"""Result classes for metadata cleaning operations."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


@dataclass
class CleaningResult:
    """Result of a metadata cleaning operation."""
    
    file_path: Path
    success: bool
    original_size: int
    cleaned_size: int
    metadata_removed: Dict[str, str] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    processing_time: float = 0.0
    backup_path: Optional[Path] = None
    content_hash_before: Optional[str] = None
    content_hash_after: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def size_reduction(self) -> int:
        """Calculate size reduction in bytes."""
        return self.original_size - self.cleaned_size
    
    @property
    def size_reduction_percent(self) -> float:
        """Calculate size reduction percentage."""
        if self.original_size == 0:
            return 0.0
        return (self.size_reduction / self.original_size) * 100
    
    @property
    def metadata_count(self) -> int:
        """Count of metadata fields removed."""
        return len(self.metadata_removed)
    
    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        return {
            "file_path": str(self.file_path),
            "success": self.success,
            "original_size": self.original_size,
            "cleaned_size": self.cleaned_size,
            "size_reduction": self.size_reduction,
            "size_reduction_percent": round(self.size_reduction_percent, 2),
            "metadata_removed": self.metadata_removed,
            "metadata_count": self.metadata_count,
            "errors": self.errors,
            "warnings": self.warnings,
            "processing_time": round(self.processing_time, 3),
            "backup_path": str(self.backup_path) if self.backup_path else None,
            "content_hash_before": self.content_hash_before,
            "content_hash_after": self.content_hash_after,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class BatchCleaningResult:
    """Result of batch cleaning operation."""
    
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    results: List[CleaningResult] = field(default_factory=list)
    total_time: float = 0.0
    total_size_reduction: int = 0
    
    def add_result(self, result: CleaningResult):
        """Add a cleaning result."""
        self.results.append(result)
        self.total_files += 1
        if result.success:
            self.successful += 1
            self.total_size_reduction += result.size_reduction
        else:
            self.failed += 1
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.successful / self.total_files) * 100
    
    def to_dict(self) -> dict:
        """Convert batch result to dictionary."""
        return {
            "total_files": self.total_files,
            "successful": self.successful,
            "failed": self.failed,
            "skipped": self.skipped,
            "success_rate": round(self.success_rate, 2),
            "total_time": round(self.total_time, 3),
            "total_size_reduction": self.total_size_reduction,
            "results": [r.to_dict() for r in self.results]
        }
