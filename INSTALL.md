# Installation Guide

## System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- ExifTool (for comprehensive image metadata removal)
- FFmpeg (for video metadata removal)

## Step 1: Install System Dependencies

### Windows

1. **Install ExifTool:**
   - Download from: https://exiftool.org/
   - Extract `exiftool(-k).exe` and rename to `exiftool.exe`
   - Add to PATH or place in project directory

2. **Install FFmpeg:**
   - Download from: https://ffmpeg.org/download.html
   - Extract and add `bin` folder to PATH
   - Verify: `ffmpeg -version`

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install exiftool ffmpeg python3-pip
```

### macOS

```bash
brew install exiftool ffmpeg python3
```

## Step 2: Install Python Dependencies

### Option A: Using pip (Recommended)

```bash
# Navigate to project directory
cd metadata_cleaner

# Install dependencies
pip install -r requirements.txt
```

### Option B: Using virtual environment (Best Practice)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Verify Installation

```bash
# Test CLI
python -m metadata_cleaner.cli --help

# Test imports
python -c "from metadata_cleaner import MetadataCleaner; print('Success!')"
```

## Step 4: Run Tests (Optional)

```bash
pytest metadata_cleaner/tests/
```

## Troubleshooting

### "ExifTool not found"

- Ensure ExifTool is installed and in PATH
- Test: `exiftool -ver`
- On Windows, make sure it's named `exiftool.exe` not `exiftool(-k).exe`

### "FFmpeg not found"

- Ensure FFmpeg is installed and in PATH
- Test: `ffmpeg -version`

### "Module not found" errors

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)

### Permission errors on Linux/Mac

- Use `sudo` for system-wide installation
- Or use virtual environment (recommended)

## Optional: Install as Package

To install as a system-wide package:

```bash
pip install -e .
```

Then you can use:

```bash
metadata-cleaner --file document.pdf
```

## Next Steps

See [README.md](README.md) for usage instructions.
