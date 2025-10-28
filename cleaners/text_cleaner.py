"""Text document metadata cleaner."""

from pathlib import Path
from typing import Dict
import logging

from .base_cleaner import BaseCleaner
from ..core.enums import CleaningLevel

logger = logging.getLogger(__name__)


class TextCleaner(BaseCleaner):
    """Cleaner for text documents (TXT, RTF)."""
    
    def __init__(self, level: CleaningLevel = CleaningLevel.DEEP):
        super().__init__(level)
    
    def extract_metadata(self, file_path: Path) -> Dict[str, str]:
        """Extract metadata from text file."""
        metadata = {}
        
        # Plain text files typically don't have embedded metadata
        # RTF files may have metadata in headers
        if file_path.suffix.lower() == '.rtf':
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000)  # Read first 1000 chars
                    
                    # Check for common RTF metadata fields
                    if '\\author' in content:
                        metadata['Author'] = 'Present'
                    if '\\company' in content:
                        metadata['Company'] = 'Present'
                    if '\\creatim' in content:
                        metadata['CreationTime'] = 'Present'
                    if '\\revtim' in content:
                        metadata['RevisionTime'] = 'Present'
            except Exception as e:
                logger.error(f"Error extracting RTF metadata: {e}")
        
        return metadata
    
    def clean(self, input_path: Path, output_path: Path) -> bool:
        """Clean text document metadata."""
        self.reset()
        
        try:
            # Extract metadata before cleaning
            self.metadata_removed = self.extract_metadata(input_path)
            
            if input_path.suffix.lower() == '.rtf':
                return self._clean_rtf(input_path, output_path)
            else:
                # Plain text - just copy (no metadata to remove)
                if input_path != output_path:
                    import shutil
                    shutil.copy2(input_path, output_path)
                return True
            
        except Exception as e:
            self.add_error(f"Failed to clean text document: {e}")
            return False
    
    def _clean_rtf(self, input_path: Path, output_path: Path) -> bool:
        """Clean RTF file metadata."""
        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Remove RTF metadata fields
            import re
            
            # Remove info group (contains metadata)
            content = re.sub(r'\\info\{[^}]*\}', '', content)
            
            # Remove specific metadata fields
            metadata_fields = [
                r'\\author[^\\}]*',
                r'\\company[^\\}]*',
                r'\\operator[^\\}]*',
                r'\\creatim[^\\}]*',
                r'\\revtim[^\\}]*',
                r'\\printim[^\\}]*',
                r'\\comment[^\\}]*',
                r'\\keywords[^\\}]*',
                r'\\subject[^\\}]*',
                r'\\title[^\\}]*',
                r'\\doccomm[^\\}]*',
            ]
            
            for field in metadata_fields:
                content = re.sub(field, '', content)
            
            # Write cleaned content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Successfully cleaned RTF: {input_path.name}")
            return True
            
        except Exception as e:
            self.add_error(f"Failed to clean RTF: {e}")
            return False
