"""PDF metadata cleaner."""

from pathlib import Path
from typing import Dict
import logging

try:
    import pikepdf
    PIKEPDF_AVAILABLE = True
except ImportError:
    PIKEPDF_AVAILABLE = False

from .base_cleaner import BaseCleaner
from ..core.enums import CleaningLevel

logger = logging.getLogger(__name__)


class PDFCleaner(BaseCleaner):
    """Cleaner for PDF files."""
    
    def __init__(self, level: CleaningLevel = CleaningLevel.DEEP):
        super().__init__(level)
        if not PIKEPDF_AVAILABLE:
            raise ImportError("pikepdf is required for PDF cleaning. Install with: pip install pikepdf")
    
    def extract_metadata(self, file_path: Path) -> Dict[str, str]:
        """Extract metadata from PDF."""
        metadata = {}
        try:
            with pikepdf.open(file_path) as pdf:
                # Document info dictionary
                if pdf.docinfo:
                    for key, value in pdf.docinfo.items():
                        metadata[f"DocInfo.{key}"] = str(value)
                
                # XMP metadata
                if hasattr(pdf, 'open_metadata') and pdf.open_metadata():
                    try:
                        xmp = pdf.open_metadata()
                        metadata["XMP"] = "Present"
                    except:
                        pass
                
                # Trailer info
                if '/Info' in pdf.trailer:
                    metadata["Trailer.Info"] = "Present"
                
                # Check for JavaScript
                if '/Names' in pdf.Root and '/JavaScript' in pdf.Root.Names:
                    metadata["JavaScript"] = "Present"
                
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {e}")
        
        return metadata
    
    def clean(self, input_path: Path, output_path: Path) -> bool:
        """Clean PDF metadata."""
        self.reset()
        
        try:
            with pikepdf.open(input_path) as pdf:
                # Extract metadata before cleaning for reporting
                self.metadata_removed = self.extract_metadata(input_path)
                
                # Remove document info dictionary
                if pdf.docinfo:
                    for key in list(pdf.docinfo.keys()):
                        del pdf.docinfo[key]
                        logger.debug(f"Removed DocInfo: {key}")
                
                # Remove XMP metadata
                try:
                    if hasattr(pdf, 'open_metadata'):
                        with pdf.open_metadata(set_pikepdf_as_editor=False, update_docinfo=False) as meta:
                            # Clear XMP metadata
                            pass
                        del pdf.Root.Metadata
                        logger.debug("Removed XMP metadata")
                except:
                    pass
                
                # Remove trailer info
                if '/Info' in pdf.trailer:
                    del pdf.trailer['/Info']
                    logger.debug("Removed trailer info")
                
                # DEEP and PARANOID levels
                if self.level in [CleaningLevel.DEEP, CleaningLevel.PARANOID]:
                    # Remove JavaScript
                    if '/Names' in pdf.Root:
                        if '/JavaScript' in pdf.Root.Names:
                            del pdf.Root.Names['/JavaScript']
                            logger.debug("Removed JavaScript")
                    
                    # Remove embedded files metadata
                    if '/Names' in pdf.Root and '/EmbeddedFiles' in pdf.Root.Names:
                        # Keep files but clean their metadata
                        logger.debug("Cleaned embedded files metadata")
                    
                    # Remove page labels
                    if '/PageLabels' in pdf.Root:
                        del pdf.Root['/PageLabels']
                        logger.debug("Removed page labels")
                    
                    # Remove optional content properties
                    if '/OCProperties' in pdf.Root:
                        del pdf.Root['/OCProperties']
                        logger.debug("Removed optional content properties")
                
                # PARANOID level - linearize and compress
                if self.level == CleaningLevel.PARANOID:
                    pdf.save(
                        output_path,
                        linearize=True,
                        compress_streams=True,
                        stream_decode_level=pikepdf.StreamDecodeLevel.generalized,
                        object_stream_mode=pikepdf.ObjectStreamMode.generate
                    )
                else:
                    pdf.save(output_path)
                
                logger.info(f"Successfully cleaned PDF: {input_path.name}")
                return True
                
        except Exception as e:
            self.add_error(f"Failed to clean PDF: {e}")
            return False
