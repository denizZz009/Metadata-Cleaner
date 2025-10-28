"""Enumerations for metadata cleaner."""

from enum import Enum, auto


class CleaningLevel(Enum):
    """Metadata cleaning thoroughness levels."""
    BASIC = auto()      # Remove common metadata
    DEEP = auto()       # Remove all metadata including hidden data
    PARANOID = auto()   # Rebuild file from scratch


class FileType(Enum):
    """Supported file types."""
    # Documents
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    PPTX = "pptx"
    ODT = "odt"
    ODS = "ods"
    ODP = "odp"
    RTF = "rtf"
    TXT = "txt"
    
    # Images
    JPEG = "jpeg"
    JPG = "jpg"
    PNG = "png"
    TIFF = "tiff"
    TIF = "tif"
    GIF = "gif"
    BMP = "bmp"
    WEBP = "webp"
    
    # Audio
    MP3 = "mp3"
    FLAC = "flac"
    WAV = "wav"
    M4A = "m4a"
    OGG = "ogg"
    
    # Video
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
    WMV = "wmv"
    
    UNKNOWN = "unknown"
    
    @classmethod
    def from_extension(cls, ext: str):
        """Get FileType from file extension."""
        ext = ext.lower().lstrip('.')
        for file_type in cls:
            if file_type.value == ext:
                return file_type
        return cls.UNKNOWN
    
    def is_document(self) -> bool:
        """Check if file type is a document."""
        return self in {
            FileType.PDF, FileType.DOCX, FileType.XLSX, FileType.PPTX,
            FileType.ODT, FileType.ODS, FileType.ODP, FileType.RTF, FileType.TXT
        }
    
    def is_image(self) -> bool:
        """Check if file type is an image."""
        return self in {
            FileType.JPEG, FileType.JPG, FileType.PNG, FileType.TIFF,
            FileType.TIF, FileType.GIF, FileType.BMP, FileType.WEBP
        }
    
    def is_audio(self) -> bool:
        """Check if file type is audio."""
        return self in {
            FileType.MP3, FileType.FLAC, FileType.WAV, FileType.M4A, FileType.OGG
        }
    
    def is_video(self) -> bool:
        """Check if file type is video."""
        return self in {
            FileType.MP4, FileType.AVI, FileType.MKV, FileType.MOV, FileType.WMV
        }
