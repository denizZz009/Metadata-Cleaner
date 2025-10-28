"""Video metadata cleaner."""

from pathlib import Path
from typing import Dict
import logging
import subprocess
import shutil

from .base_cleaner import BaseCleaner
from ..core.enums import CleaningLevel

logger = logging.getLogger(__name__)


class VideoCleaner(BaseCleaner):
    """Cleaner for video files using FFmpeg."""
    
    def __init__(self, level: CleaningLevel = CleaningLevel.DEEP):
        super().__init__(level)
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """Check if FFmpeg is available."""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("FFmpeg is required for video cleaning. Install from: https://ffmpeg.org/")
    
    def extract_metadata(self, file_path: Path) -> Dict[str, str]:
        """Extract metadata from video file."""
        metadata = {}
        
        try:
            # Use ffprobe to extract metadata
            result = subprocess.run(
                [
                    'ffprobe',
                    '-v', 'quiet',
                    '-print_format', 'json',
                    '-show_format',
                    '-show_streams',
                    str(file_path)
                ],
                capture_output=True,
                text=True,
                check=True
            )
            
            import json
            data = json.loads(result.stdout)
            
            # Extract format metadata
            if 'format' in data and 'tags' in data['format']:
                for key, value in data['format']['tags'].items():
                    metadata[f"Format.{key}"] = str(value)[:100]
            
            # Extract stream metadata
            if 'streams' in data:
                for i, stream in enumerate(data['streams']):
                    if 'tags' in stream:
                        for key, value in stream['tags'].items():
                            metadata[f"Stream{i}.{key}"] = str(value)[:100]
        
        except Exception as e:
            logger.error(f"Error extracting video metadata: {e}")
        
        return metadata
    
    def clean(self, input_path: Path, output_path: Path) -> bool:
        """Clean video metadata using FFmpeg."""
        self.reset()
        
        try:
            # Extract metadata before cleaning
            self.metadata_removed = self.extract_metadata(input_path)
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-map_metadata', '-1',  # Remove all metadata
                '-c', 'copy',  # Copy streams without re-encoding
                '-y',  # Overwrite output file
            ]
            
            # Additional options for different cleaning levels
            if self.level in [CleaningLevel.DEEP, CleaningLevel.PARANOID]:
                cmd.extend([
                    '-map_chapters', '-1',  # Remove chapters
                    '-fflags', '+bitexact',  # Reproducible output
                    '-flags:v', '+bitexact',
                    '-flags:a', '+bitexact',
                ])
            
            cmd.append(str(output_path))
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.add_error(f"FFmpeg error: {result.stderr}")
                return False
            
            logger.info(f"Successfully cleaned video: {input_path.name}")
            return True
            
        except Exception as e:
            self.add_error(f"Failed to clean video: {e}")
            return False
