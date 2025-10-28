"""Tests for metadata cleaner core functionality."""

import pytest
from pathlib import Path
import tempfile
import shutil

from metadata_cleaner import MetadataCleaner, CleaningLevel


class TestMetadataCleaner:
    """Test MetadataCleaner class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def cleaner(self):
        """Create cleaner instance."""
        return MetadataCleaner(level=CleaningLevel.DEEP, backup=False)
    
    def test_cleaner_initialization(self):
        """Test cleaner initialization."""
        cleaner = MetadataCleaner(
            level=CleaningLevel.PARANOID,
            backup=True,
            verify=True
        )
        assert cleaner.level == CleaningLevel.PARANOID
        assert cleaner.backup is True
        assert cleaner.verify is True
    
    def test_unsupported_file(self, cleaner, temp_dir):
        """Test handling of unsupported file type."""
        test_file = temp_dir / "test.xyz"
        test_file.write_text("test content")
        
        result = cleaner.clean_file(test_file)
        assert result.success is False
        assert "Unsupported" in result.errors[0]
    
    def test_nonexistent_file(self, cleaner):
        """Test handling of nonexistent file."""
        result = cleaner.clean_file("nonexistent.pdf")
        assert result.success is False
        assert "not found" in result.errors[0].lower()
    
    def test_cleaning_levels(self):
        """Test different cleaning levels."""
        basic = MetadataCleaner(level=CleaningLevel.BASIC)
        deep = MetadataCleaner(level=CleaningLevel.DEEP)
        paranoid = MetadataCleaner(level=CleaningLevel.PARANOID)
        
        assert basic.level == CleaningLevel.BASIC
        assert deep.level == CleaningLevel.DEEP
        assert paranoid.level == CleaningLevel.PARANOID


class TestFileTypeDetection:
    """Test file type detection."""
    
    def test_pdf_detection(self):
        """Test PDF file type detection."""
        from metadata_cleaner.core.enums import FileType
        assert FileType.from_extension('.pdf') == FileType.PDF
        assert FileType.from_extension('pdf') == FileType.PDF
    
    def test_image_detection(self):
        """Test image file type detection."""
        from metadata_cleaner.core.enums import FileType
        assert FileType.from_extension('.jpg').is_image()
        assert FileType.from_extension('.png').is_image()
        assert FileType.from_extension('.tiff').is_image()
    
    def test_office_detection(self):
        """Test Office file type detection."""
        from metadata_cleaner.core.enums import FileType
        assert FileType.from_extension('.docx').is_document()
        assert FileType.from_extension('.xlsx').is_document()
        assert FileType.from_extension('.pptx').is_document()
    
    def test_audio_detection(self):
        """Test audio file type detection."""
        from metadata_cleaner.core.enums import FileType
        assert FileType.from_extension('.mp3').is_audio()
        assert FileType.from_extension('.flac').is_audio()
    
    def test_video_detection(self):
        """Test video file type detection."""
        from metadata_cleaner.core.enums import FileType
        assert FileType.from_extension('.mp4').is_video()
        assert FileType.from_extension('.avi').is_video()


class TestUtils:
    """Test utility functions."""
    
    def test_file_hash(self, tmp_path):
        """Test file hash calculation."""
        from metadata_cleaner.core.utils import calculate_file_hash
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        hash1 = calculate_file_hash(test_file)
        hash2 = calculate_file_hash(test_file)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hash length
    
    def test_backup_creation(self, tmp_path):
        """Test backup file creation."""
        from metadata_cleaner.core.utils import create_backup
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        backup_path = create_backup(test_file)
        
        assert backup_path.exists()
        assert backup_path.read_text() == "test content"
    
    def test_file_size(self, tmp_path):
        """Test file size calculation."""
        from metadata_cleaner.core.utils import get_file_size
        
        test_file = tmp_path / "test.txt"
        content = "test content"
        test_file.write_text(content)
        
        size = get_file_size(test_file)
        assert size == len(content.encode())


if __name__ == '__main__':
    pytest.main([__file__])
