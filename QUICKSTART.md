# Quick Start Guide

Get started with Metadata Cleaner in 5 minutes!

## Installation (2 minutes)

### Step 1: Install System Dependencies

**Windows:**
```bash
# Download and install:
# - ExifTool: https://exiftool.org/
# - FFmpeg: https://ffmpeg.org/download.html
```

**Linux:**
```bash
sudo apt-get install exiftool ffmpeg
```

**macOS:**
```bash
brew install exiftool ffmpeg
```

### Step 2: Install Python Package

```bash
cd metadata_cleaner
pip install -r requirements.txt
```

## Usage (3 minutes)

### Option 1: Web Interface (Easiest)

```bash
# Start web server
python -m metadata_cleaner.web

# Open browser to http://localhost:5000
# Drag and drop files
# Click "Clean Files"
# Download cleaned files
```

### Option 2: Command Line

```bash
# Clean a single file
python -m metadata_cleaner.cli --file document.pdf

# Clean with backup
python -m metadata_cleaner.cli --file document.pdf --backup

# Clean entire folder
python -m metadata_cleaner.cli --folder ./documents --recursive
```

### Option 3: Python Code

```python
from metadata_cleaner import MetadataCleaner, CleaningLevel

# Initialize
cleaner = MetadataCleaner(level=CleaningLevel.DEEP, backup=True)

# Clean file
result = cleaner.clean_file("document.pdf")

# Check result
if result.success:
    print(f"Removed {result.metadata_count} metadata fields")
    print(f"Size reduced by {result.size_reduction_percent:.1f}%")
```

## Common Tasks

### Clean Multiple Files
```bash
python -m metadata_cleaner.cli --files file1.pdf file2.jpg file3.docx
```

### Maximum Privacy (Paranoid Mode)
```bash
python -m metadata_cleaner.cli --file sensitive.pdf --level paranoid --backup
```

### Generate Report
```bash
python -m metadata_cleaner.cli --file document.pdf --report report.json
```

### Batch Process with Progress
```bash
python -m metadata_cleaner.cli --folder ./photos --recursive --verbose
```

## Verification

Test your installation:

```bash
# Test CLI
python -m metadata_cleaner.cli --help

# Test import
python -c "from metadata_cleaner import MetadataCleaner; print('✓ Success!')"

# Run tests
pytest metadata_cleaner/tests/
```

## Troubleshooting

**"ExifTool not found"**
- Install ExifTool and add to PATH
- Test: `exiftool -ver`

**"FFmpeg not found"**
- Install FFmpeg and add to PATH
- Test: `ffmpeg -version`

**"Module not found"**
- Install dependencies: `pip install -r requirements.txt`

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage
- See [examples/example_usage.py](examples/example_usage.py) for code examples
- Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture details

## Support

- Issues: GitHub Issues
- Documentation: README.md
- Examples: examples/ directory

---

**You're ready to clean metadata! 🎉**
