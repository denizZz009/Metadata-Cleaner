"""Base cleaner class for all file type cleaners."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List
import logging

from ..core.enums import CleaningLevel

logger = logging.getLogger(__name__)


class BaseCleaner(ABC):
    """Abstract base class for file cleaners."""
    
    def __init__(self, level: CleaningLevel = CleaningLevel.DEEP):
        self.level = level
        self.metadata_removed: Dict[str, str] = {}
        self.warnings: List[str] = []
        self.errors: List[str] = []
    
    @abstractmethod
    def clean(self, input_path: Path, output_path: Path) -> bool:
        """
        Clean metadata from file.
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: Path) -> Dict[str, str]:
        """
        Extract metadata from file for reporting.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary of metadata key-value pairs
        """
        pass
    
    def reset(self):
        """Reset cleaner state."""
        self.metadata_removed.clear()
        self.warnings.clear()
        self.errors.clear()
    
    def add_warning(self, message: str):
        """Add warning message."""
        self.warnings.append(message)
        logger.warning(message)
    
    def add_error(self, message: str):
        """Add error message."""
        self.errors.append(message)
        logger.error(message)
