"""
Metadata Cleaner - Complete Privacy Protection Tool
Removes ALL metadata from documents while preserving content.
"""

from .core.cleaner import MetadataCleaner
from .core.enums import CleaningLevel, FileType
from .core.result import CleaningResult

__version__ = "1.0.0"
__all__ = ["MetadataCleaner", "CleaningLevel", "FileType", "CleaningResult"]
