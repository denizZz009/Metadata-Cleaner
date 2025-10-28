"""Microsoft Office and OpenDocument format cleaner."""

from pathlib import Path
from typing import Dict
import logging
import zipfile
import shutil
import tempfile
from xml.etree import ElementTree as ET

from .base_cleaner import BaseCleaner
from ..core.enums import CleaningLevel, FileType

logger = logging.getLogger(__name__)


class OfficeCleaner(BaseCleaner):
    """Cleaner for Office documents (DOCX, XLSX, PPTX, ODT, ODS, ODP)."""
    
    def __init__(self, level: CleaningLevel = CleaningLevel.DEEP):
        super().__init__(level)
    
    def extract_metadata(self, file_path: Path) -> Dict[str, str]:
        """Extract metadata from Office document."""
        metadata = {}
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                # Core properties
                if 'docProps/core.xml' in zf.namelist():
                    core_xml = zf.read('docProps/core.xml')
                    root = ET.fromstring(core_xml)
                    for elem in root.iter():
                        if elem.text and elem.text.strip():
                            tag = elem.tag.split('}')[-1]  # Remove namespace
                            metadata[f"Core.{tag}"] = elem.text[:100]
                
                # App properties
                if 'docProps/app.xml' in zf.namelist():
                    app_xml = zf.read('docProps/app.xml')
                    root = ET.fromstring(app_xml)
                    for elem in root.iter():
                        if elem.text and elem.text.strip():
                            tag = elem.tag.split('}')[-1]
                            metadata[f"App.{tag}"] = elem.text[:100]
                
                # Custom properties
                if 'docProps/custom.xml' in zf.namelist():
                    metadata["Custom"] = "Present"
                
        except Exception as e:
            logger.error(f"Error extracting Office metadata: {e}")
        
        return metadata
    
    def clean(self, input_path: Path, output_path: Path) -> bool:
        """Clean Office document metadata."""
        self.reset()
        
        try:
            # Extract metadata before cleaning
            self.metadata_removed = self.extract_metadata(input_path)
            
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                extract_path = temp_path / "extracted"
                extract_path.mkdir()
                
                # Extract the Office document (it's a ZIP file)
                with zipfile.ZipFile(input_path, 'r') as zf:
                    zf.extractall(extract_path)
                
                # Remove metadata files
                metadata_files = [
                    'docProps/core.xml',
                    'docProps/app.xml',
                    'docProps/custom.xml'
                ]
                
                for meta_file in metadata_files:
                    meta_path = extract_path / meta_file
                    if meta_path.exists():
                        if self.level == CleaningLevel.BASIC:
                            # Just clear sensitive fields
                            self._clean_xml_metadata(meta_path)
                        else:
                            # Remove entirely
                            meta_path.unlink()
                            logger.debug(f"Removed {meta_file}")
                
                # DEEP and PARANOID: Clean content files
                if self.level in [CleaningLevel.DEEP, CleaningLevel.PARANOID]:
                    self._clean_content_files(extract_path, input_path.suffix)
                
                # Update [Content_Types].xml to remove references
                self._update_content_types(extract_path)
                
                # Repackage as ZIP
                self._create_office_file(extract_path, output_path)
                
                logger.info(f"Successfully cleaned Office document: {input_path.name}")
                return True
                
        except Exception as e:
            self.add_error(f"Failed to clean Office document: {e}")
            return False
    
    def _clean_xml_metadata(self, xml_path: Path):
        """Clean sensitive metadata from XML file."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Tags to clear
            sensitive_tags = [
                'creator', 'lastModifiedBy', 'created', 'modified',
                'company', 'manager', 'lastPrinted', 'revision'
            ]
            
            for elem in root.iter():
                tag = elem.tag.split('}')[-1].lower()
                if tag in sensitive_tags:
                    elem.text = ""
            
            tree.write(xml_path, encoding='utf-8', xml_declaration=True)
            
        except Exception as e:
            logger.warning(f"Failed to clean XML metadata: {e}")
    
    def _clean_content_files(self, extract_path: Path, file_ext: str):
        """Clean metadata from content files."""
        try:
            # Find main content file
            content_files = []
            
            if file_ext in ['.docx', '.odt']:
                content_files = list(extract_path.glob('word/document.xml'))
                content_files.extend(list(extract_path.glob('content.xml')))
            elif file_ext in ['.xlsx', '.ods']:
                content_files = list(extract_path.glob('xl/workbook.xml'))
                content_files.extend(list(extract_path.glob('content.xml')))
            elif file_ext in ['.pptx', '.odp']:
                content_files = list(extract_path.glob('ppt/presentation.xml'))
                content_files.extend(list(extract_path.glob('content.xml')))
            
            for content_file in content_files:
                if content_file.exists():
                    self._remove_rsid_attributes(content_file)
        
        except Exception as e:
            logger.warning(f"Failed to clean content files: {e}")
    
    def _remove_rsid_attributes(self, xml_path: Path):
        """Remove rsid (revision session ID) attributes from XML."""
        try:
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove rsid attributes (revision tracking)
            import re
            content = re.sub(r'\s+w:rsid\w+="[^"]*"', '', content)
            content = re.sub(r'\s+rsid\w+="[^"]*"', '', content)
            
            with open(xml_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.debug(f"Removed rsid attributes from {xml_path.name}")
            
        except Exception as e:
            logger.warning(f"Failed to remove rsid attributes: {e}")
    
    def _update_content_types(self, extract_path: Path):
        """Update [Content_Types].xml to remove metadata references."""
        try:
            content_types_path = extract_path / '[Content_Types].xml'
            if not content_types_path.exists():
                return
            
            tree = ET.parse(content_types_path)
            root = tree.getroot()
            
            # Remove Override elements for metadata files
            metadata_parts = [
                '/docProps/core.xml',
                '/docProps/app.xml',
                '/docProps/custom.xml'
            ]
            
            for override in root.findall('.//{*}Override'):
                part_name = override.get('PartName', '')
                if part_name in metadata_parts:
                    root.remove(override)
            
            tree.write(content_types_path, encoding='utf-8', xml_declaration=True)
            
        except Exception as e:
            logger.warning(f"Failed to update Content_Types: {e}")
    
    def _create_office_file(self, extract_path: Path, output_path: Path):
        """Repackage directory as Office file (ZIP)."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in extract_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(extract_path)
                    zf.write(file_path, arcname)
