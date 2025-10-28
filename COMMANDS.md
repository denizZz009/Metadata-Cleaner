# Complete Command Reference

## Installation Commands

### System Dependencies

```bash
# Windows (Manual installation required)
# Download ExifTool: https://exiftool.org/
# Download FFmpeg: https://ffmpeg.org/download.html

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install exiftool ffmpeg python3-pip

# Linux (Fedora/RHEL)
sudo dnf install perl-Image-ExifTool ffmpeg python3-pip

# macOS
brew install exiftool ffmpeg python3
```

### Python Package

```bash
# Basic installation
pip install -r requirements.txt

# With virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Development installation
pip install -r requirements.txt
pip install -e .

# With development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

## CLI Commands

### Basic Usage

```bash
# Clean single file (overwrites original)
python -m metadata_cleaner.cli --file document.pdf

# Clean with specific output
python -m metadata_cleaner.cli --file document.pdf --output cleaned.pdf

# Clean with backup
python -m metadata_cleaner.cli --file document.pdf --backup

# Custom backup directory
python -m metadata_cleaner.cli --file document.pdf --backup --backup-dir ./backups
```

### Cleaning Levels

```bash
# Basic cleaning
python -m metadata_cleaner.cli --file document.pdf --level basic

# Deep cleaning (default)
python -m metadata_cleaner.cli --file document.pdf --level deep

# Paranoid mode
python -m metadata_cleaner.cli --file document.pdf --level paranoid
```

### Batch Processing

```bash
# Clean folder (non-recursive)
python -m metadata_cleaner.cli --folder ./documents

# Clean folder recursively
python -m metadata_cleaner.cli --folder ./documents --recursive

# Clean multiple specific files
python -m metadata_cleaner.cli --files file1.pdf file2.docx file3.jpg

# Batch with custom workers
python -m metadata_cleaner.cli --folder ./documents --workers 8

# Batch with all options
python -m metadata_cleaner.cli \
    --folder ./documents \
    --recursive \
    --level paranoid \
    --backup \
    --backup-dir ./backups \
    --workers 8 \
    --verbose
```

### Reports and Logging

```bash
# Generate JSON report
python -m metadata_cleaner.cli --file document.pdf --report report.json

# Verbose output
python -m metadata_cleaner.cli --file document.pdf --verbose

# Quiet mode
python -m metadata_cleaner.cli --file document.pdf --quiet

# Skip verification (faster)
python -m metadata_cleaner.cli --file document.pdf --no-verify
```

### Real-World Examples

```bash
# Clean all PDFs in current directory
python -m metadata_cleaner.cli --folder . --recursive --level deep

# Clean photos with backup
python -m metadata_cleaner.cli \
    --folder ./photos \
    --recursive \
    --level paranoid \
    --backup \
    --report photo_cleaning_report.json

# Quick clean without backup or verification
python -m metadata_cleaner.cli \
    --file document.pdf \
    --level basic \
    --no-verify

# Clean sensitive documents
python -m metadata_cleaner.cli \
    --folder ./sensitive \
    --recursive \
    --level paranoid \
    --backup \
    --backup-dir ~/backups/sensitive \
    --report sensitive_report.json \
    --verbose

# Clean multiple file types
python -m metadata_cleaner.cli \
    --files \
        report.pdf \
        presentation.pptx \
        photo.jpg \
        audio.mp3 \
    --level deep \
    --backup
```

## Web Interface Commands

### Starting Server

```bash
# Default (localhost:5000)
python -m metadata_cleaner.web

# Custom port
python -m metadata_cleaner --web --port 8080

# Custom host (allow external connections)
python -m metadata_cleaner --web --host 0.0.0.0 --port 8080

# Production mode
python -m metadata_cleaner --web --host 0.0.0.0 --port 80
```

### Using with WSGI Server

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 metadata_cleaner.web:app

# With more workers
gunicorn -w 8 -b 0.0.0.0:8000 --timeout 300 metadata_cleaner.web:app
```

## Python API Commands

### Interactive Python

```python
# Start Python interpreter
python

# Import and use
from metadata_cleaner import MetadataCleaner, CleaningLevel

cleaner = MetadataCleaner(level=CleaningLevel.DEEP, backup=True)
result = cleaner.clean_file("document.pdf")
print(f"Success: {result.success}")
print(f"Metadata removed: {result.metadata_count}")
```

### Script Execution

```bash
# Run example script
python metadata_cleaner/examples/example_usage.py

# Run custom script
python my_cleaning_script.py

# Run with specific Python version
python3.11 my_cleaning_script.py
```

## Testing Commands

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=metadata_cleaner

# Run specific test file
pytest metadata_cleaner/tests/test_cleaner.py

# Run specific test
pytest metadata_cleaner/tests/test_cleaner.py::TestMetadataCleaner::test_cleaner_initialization

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run in parallel
pytest -n auto
```

### Code Quality

```bash
# Format code with Black
black metadata_cleaner/

# Check formatting
black --check metadata_cleaner/

# Lint with flake8
flake8 metadata_cleaner/

# Type checking with mypy
mypy metadata_cleaner/

# All quality checks
black metadata_cleaner/ && flake8 metadata_cleaner/ && mypy metadata_cleaner/
```

## Development Commands

### Package Building

```bash
# Build package
python setup.py sdist bdist_wheel

# Install locally
pip install -e .

# Uninstall
pip uninstall metadata-cleaner
```

### Documentation

```bash
# Generate documentation (if using Sphinx)
cd docs
make html

# View documentation
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
start _build/html/index.html  # Windows
```

### Git Commands

```bash
# Clone repository
git clone https://github.com/yourusername/metadata-cleaner.git
cd metadata-cleaner

# Create feature branch
git checkout -b feature/new-feature

# Commit changes
git add .
git commit -m "Add new feature"

# Push changes
git push origin feature/new-feature

# Create pull request (via GitHub web interface)
```

## Utility Commands

### File Operations

```bash
# Find all PDFs
find . -name "*.pdf"  # Linux/Mac
dir /s /b *.pdf       # Windows

# Count files by type
find . -name "*.pdf" | wc -l  # Linux/Mac

# Check file metadata (before cleaning)
exiftool document.pdf

# Check file metadata (after cleaning)
exiftool cleaned_document.pdf

# Compare file sizes
ls -lh document.pdf cleaned_document.pdf  # Linux/Mac
dir document.pdf cleaned_document.pdf     # Windows
```

### System Information

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check installed packages
pip list

# Check specific package
pip show metadata-cleaner

# Check ExifTool
exiftool -ver

# Check FFmpeg
ffmpeg -version

# System information
python -c "import platform; print(platform.platform())"
```

### Troubleshooting Commands

```bash
# Verify installation
python -c "from metadata_cleaner import MetadataCleaner; print('OK')"

# Check dependencies
pip check

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +  # Linux/Mac
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"  # Windows

# Check for import errors
python -c "import metadata_cleaner; print(dir(metadata_cleaner))"
```

## Performance Benchmarking

```bash
# Time single file cleaning
time python -m metadata_cleaner.cli --file large_document.pdf

# Benchmark batch processing
time python -m metadata_cleaner.cli --folder ./test_files --recursive

# Compare cleaning levels
time python -m metadata_cleaner.cli --file test.pdf --level basic
time python -m metadata_cleaner.cli --file test.pdf --level deep
time python -m metadata_cleaner.cli --file test.pdf --level paranoid

# Profile Python code
python -m cProfile -o profile.stats -m metadata_cleaner.cli --file test.pdf
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"
```

## Automation Examples

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add daily cleaning at 2 AM
0 2 * * * cd /path/to/metadata_cleaner && python -m metadata_cleaner.cli --folder /path/to/documents --recursive --backup

# Add weekly cleaning on Sunday at 3 AM
0 3 * * 0 cd /path/to/metadata_cleaner && python -m metadata_cleaner.cli --folder /path/to/photos --recursive --level paranoid --backup
```

### Task Scheduler (Windows)

```powershell
# Create scheduled task
schtasks /create /tn "MetadataCleaner" /tr "python -m metadata_cleaner.cli --folder C:\Documents --recursive" /sc daily /st 02:00

# Run task immediately
schtasks /run /tn "MetadataCleaner"

# Delete task
schtasks /delete /tn "MetadataCleaner"
```

### Bash Script

```bash
#!/bin/bash
# clean_metadata.sh

FOLDER="/path/to/documents"
BACKUP_DIR="/path/to/backups"
REPORT="/path/to/reports/report_$(date +%Y%m%d).json"

python -m metadata_cleaner.cli \
    --folder "$FOLDER" \
    --recursive \
    --level deep \
    --backup \
    --backup-dir "$BACKUP_DIR" \
    --report "$REPORT" \
    --verbose

echo "Cleaning completed at $(date)"
```

### PowerShell Script

```powershell
# clean_metadata.ps1

$Folder = "C:\Documents"
$BackupDir = "C:\Backups"
$Report = "C:\Reports\report_$(Get-Date -Format 'yyyyMMdd').json"

python -m metadata_cleaner.cli `
    --folder $Folder `
    --recursive `
    --level deep `
    --backup `
    --backup-dir $BackupDir `
    --report $Report `
    --verbose

Write-Host "Cleaning completed at $(Get-Date)"
```

## Docker Commands (Future)

```bash
# Build Docker image
docker build -t metadata-cleaner .

# Run container
docker run -v /path/to/files:/data metadata-cleaner --folder /data

# Run web interface
docker run -p 5000:5000 metadata-cleaner --web

# Docker Compose
docker-compose up
```

## Quick Reference

### Most Common Commands

```bash
# 1. Clean single file with backup
python -m metadata_cleaner.cli --file document.pdf --backup

# 2. Clean folder recursively
python -m metadata_cleaner.cli --folder ./documents --recursive

# 3. Maximum privacy cleaning
python -m metadata_cleaner.cli --file sensitive.pdf --level paranoid --backup

# 4. Start web interface
python -m metadata_cleaner.web

# 5. Generate report
python -m metadata_cleaner.cli --file document.pdf --report report.json
```

### Help Commands

```bash
# CLI help
python -m metadata_cleaner.cli --help

# Python help
python -c "from metadata_cleaner import MetadataCleaner; help(MetadataCleaner)"

# Module help
python -c "import metadata_cleaner; help(metadata_cleaner)"
```

---

**Tip**: Add commonly used commands as shell aliases:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias clean-meta='python -m metadata_cleaner.cli'
alias clean-meta-web='python -m metadata_cleaner.web'

# Usage
clean-meta --file document.pdf --backup
clean-meta-web
```
