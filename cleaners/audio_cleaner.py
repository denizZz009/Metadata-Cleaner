"""Audio metadata cleaner."""

from pathlib import Path
from typing import Dict
import logging

try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import ID3
    from mutagen.flac import FLAC
    from mutagen.mp4 import MP4
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

from .base_cleaner import BaseCleaner
from ..core.enums import CleaningLevel

logger = logging.getLogger(__name__)


class AudioCleaner(BaseCleaner):
    """Cleaner for audio files."""
    
    def __init__(self, level: CleaningLevel = CleaningLevel.DEEP):
        super().__init__(level)
        if not MUTAGEN_AVAILABLE:
            raise ImportError("mutagen is required for audio cleaning. Install with: pip install mutagen")
    
    def extract_metadata(self, file_path: Path) -> Dict[str, str]:
        """Extract metadata from audio file."""
        metadata = {}
        
        try:
            audio = MutagenFile(file_path)
            if audio is None:
                return metadata
            
            # Get all tags
            if hasattr(audio, 'tags') and audio.tags:
                for key, value in audio.tags.items():
                    metadata[str(key)] = str(value)[:100]
            
            # Get info
            if hasattr(audio, 'info'):
                info = audio.info
                if hasattr(info, 'pprint'):
                    metadata['Info'] = info.pprint()[:200]
        
        except Exception as e:
            logger.error(f"Error extracting audio metadata: {e}")
        
        return metadata
    
    def clean(self, input_path: Path, output_path: Path) -> bool:
        """Clean audio metadata."""
        self.reset()
        
        try:
            # Extract metadata before cleaning
            self.metadata_removed = self.extract_metadata(input_path)
            
            # Load audio file
            audio = MutagenFile(input_path)
            
            if audio is None:
                self.add_error("Unsupported audio format")
                return False
            
            # Remove all tags
            if hasattr(audio, 'tags') and audio.tags:
                if self.level == CleaningLevel.BASIC:
                    # Remove only sensitive tags
                    sensitive_tags = [
                        'TPE1', 'TPE2', 'TALB', 'TIT2', 'TDRC', 'TYER',  # ID3
                        'artist', 'album', 'title', 'date', 'year',  # Vorbis
                        '©ART', '©alb', '©nam', '©day'  # MP4
                    ]
                    
                    for tag in sensitive_tags:
                        if tag in audio.tags:
                            del audio.tags[tag]
                else:
                    # Remove all tags
                    audio.delete()
                    logger.debug("Removed all audio tags")
            
            # Save cleaned file
            if input_path != output_path:
                import shutil
                shutil.copy2(input_path, output_path)
                audio = MutagenFile(output_path)
                if audio and hasattr(audio, 'delete'):
                    audio.delete()
                    audio.save()
            else:
                audio.save()
            
            logger.info(f"Successfully cleaned audio: {input_path.name}")
            return True
            
        except Exception as e:
            self.add_error(f"Failed to clean audio: {e}")
            return False
