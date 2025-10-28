# 🔒 Metadata Cleaner - Complete Privacy Protection Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/yourusername/metadata-cleaner)

A production-ready, comprehensive metadata cleaning application that removes **ALL metadata** from documents while preserving **100% of the content**. More thorough than ExifTool, MAT2, or Adobe Acrobat.

## ✨ Key Features

- 🎯 **27 File Formats** - Documents, images, audio, video
- 🔐 **3 Cleaning Levels** - Basic, Deep, Paranoid
- 💻 **3 Interfaces** - CLI, Web GUI, Python API
- ⚡ **Multi-threaded** - Fast batch processing
- 🛡️ **Safe** - Automatic backups & verification
- 📊 **Detailed Reports** - JSON export with statistics
- 🌍 **Cross-platform** - Windows, Linux, macOS

## 📦 Supported File Types (27 formats)

| Category | Formats |
|----------|---------|
| **Documents** | PDF, DOCX, XLSX, PPTX, ODT, ODS, ODP, RTF, TXT |
| **Images** | JPEG, PNG, TIFF, GIF, BMP, WEBP |
| **Audio** | MP3, FLAC, WAV, M4A, OGG |
| **Video** | MP4, AVI, MKV, MOV, WMV |

## Installation

### Prerequisites

1. Python 3.8 or higher
2. ExifTool (system dependency)
3. FFmpeg (for video processing)

### Windows Installation

```bash
# Install ExifTool
# Download from: https://exiftool.org/
# Add to PATH

# Install FFmpeg
# Download from: https://ffmpeg.org/download.html
# Add to PATH

# Install Python dependencies
pip install -r requirements.txt
```

### Linux/Mac Installation

```bash
# Install system dependencies
sudo apt-get install exiftool ffmpeg  # Ubuntu/Debian
brew install exiftool ffmpeg          # macOS

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Clean single file (basic level)
python -m metadata_cleaner.cli --file document.pdf

# Deep cleaning with backup
python -m metadata_cleaner.cli --file document.pdf --level deep --backup

# Paranoid mode (most thorough)
python -m metadata_cleaner.cli --file image.jpg --level paranoid

# Batch process folder
python -m metadata_cleaner.cli --folder ./documents --recursive

# Generate detailed report
python -m metadata_cleaner.cli --file document.pdf --report report.json

# Process multiple files
python -m metadata_cleaner.cli --files file1.pdf file2.docx file3.jpg
```

### Web GUI

```bash
# Start web server
python -m metadata_cleaner.web

# Open browser to http://localhost:5000
```

### Python Library

```python
from metadata_cleaner import MetadataCleaner, CleaningLevel

# Initialize cleaner
cleaner = MetadataCleaner(level=CleaningLevel.DEEP, backup=True)

# Clean single file
result = cleaner.clean_file("document.pdf")
print(f"Removed metadata: {result.metadata_removed}")

# Batch clean
results = cleaner.clean_folder("./documents", recursive=True)
```

## Cleaning Levels

- **BASIC**: Remove common metadata (author, dates, software names)
- **DEEP**: Remove all metadata including hidden data and embedded metadata
- **PARANOID**: Rebuild files from scratch, remove everything possible

## Features

- Complete metadata removal across all file types
- Before/after metadata comparison
- Detailed logging and reporting
- File integrity verification
- Backup and rollback capability
- Multi-threaded batch processing
- Progress tracking
- Hash verification

## Security & Privacy

This tool is designed for maximum privacy protection. It removes:
- Author names and user information
- All timestamps
- Software and OS information
- GPS coordinates
- Device information
- Revision history
- Hidden data and deleted content
- Embedded thumbnails
- And much more...

## License

MIT License
