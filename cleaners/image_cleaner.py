"""Image metadata cleaner."""

from pathlib import Path
from typing import Dict
import logging

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import exiftool
    EXIFTOOL_AVAILABLE = True
except ImportError:
    EXIFTOOL_AVAILABLE = False

from .base_cleaner import BaseCleaner
from ..core.enums import CleaningLevel

logger = logging.getLogger(__name__)


class ImageCleaner(BaseCleaner):
    """Cleaner for image files."""
    
    def __init__(self, level: CleaningLevel = CleaningLevel.DEEP):
        super().__init__(level)
        if not PIL_AVAILABLE:
            raise ImportError("Pillow is required for image cleaning. Install with: pip install Pillow")
    
    def extract_metadata(self, file_path: Path) -> Dict[str, str]:
        """Extract metadata from image."""
        metadata = {}
        
        try:
            with Image.open(file_path) as img:
                # EXIF data
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        metadata[f"EXIF.{tag}"] = str(value)[:100]  # Truncate long values
                
                # Image info
                if hasattr(img, 'info'):
                    for key, value in img.info.items():
                        if key not in ['exif']:  # Already handled
                            metadata[f"Info.{key}"] = str(value)[:100]
        
        except Exception as e:
            logger.error(f"Error extracting image metadata: {e}")
        
        # Use exiftool for comprehensive extraction if available
        if EXIFTOOL_AVAILABLE and self.level in [CleaningLevel.DEEP, CleaningLevel.PARANOID]:
            try:
                with exiftool.ExifToolHelper() as et:
                    exif_metadata = et.get_metadata(str(file_path))
                    if exif_metadata:
                        for key, value in exif_metadata[0].items():
                            if not key.startswith('File:'):  # Skip file system metadata
                                metadata[key] = str(value)[:100]
            except Exception as e:
                logger.debug(f"ExifTool extraction failed: {e}")
        
        return metadata
    
    def clean(self, input_path: Path, output_path: Path) -> bool:
        """Clean image metadata."""
        self.reset()
        
        try:
            # Extract metadata before cleaning
            self.metadata_removed = self.extract_metadata(input_path)
            
            # Use exiftool for thorough cleaning if available
            if EXIFTOOL_AVAILABLE and self.level in [CleaningLevel.DEEP, CleaningLevel.PARANOID]:
                try:
                    with exiftool.ExifToolHelper() as et:
                        # Remove all metadata
                        et.execute(
                            b"-all=",
                            b"-overwrite_original",
                            str(input_path).encode()
                        )
                        
                        # Copy cleaned file to output
                        if input_path != output_path:
                            import shutil
                            shutil.copy2(input_path, output_path)
                        
                        logger.info(f"Cleaned image with exiftool: {input_path.name}")
                        return True
                except Exception as e:
                    logger.warning(f"ExifTool cleaning failed, falling back to PIL: {e}")
            
            # Fallback to PIL-based cleaning
            with Image.open(input_path) as img:
                # Get image data without metadata
                data = list(img.getdata())
                
                # Create new image without metadata
                cleaned_img = Image.new(img.mode, img.size)
                cleaned_img.putdata(data)
                
                # Preserve color profile if not in PARANOID mode
                if self.level != CleaningLevel.PARANOID:
                    if 'icc_profile' in img.info:
                        cleaned_img.info['icc_profile'] = img.info['icc_profile']
                
                # Save without metadata
                save_kwargs = {}
                
                # Format-specific options
                if input_path.suffix.lower() in ['.jpg', '.jpeg']:
                    save_kwargs['quality'] = 95
                    save_kwargs['optimize'] = True
                    # Explicitly exclude EXIF
                    save_kwargs['exif'] = b''
                elif input_path.suffix.lower() == '.png':
                    save_kwargs['optimize'] = True
                    # Remove all PNG metadata chunks
                    save_kwargs['pnginfo'] = None
                
                cleaned_img.save(output_path, **save_kwargs)
                
                logger.info(f"Successfully cleaned image: {input_path.name}")
                return True
                
        except Exception as e:
            self.add_error(f"Failed to clean image: {e}")
            return False
