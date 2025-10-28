# Usage Guide

## Command Line Interface (CLI)

### Basic Usage

```bash
# Clean a single file (overwrites original)
python -m metadata_cleaner.cli --file document.pdf

# Clean with output to different file
python -m metadata_cleaner.cli --file document.pdf --output cleaned_document.pdf

# Clean with backup
python -m metadata_cleaner.cli --file document.pdf --backup
```

### Cleaning Levels

```bash
# Basic cleaning (remove common metadata only)
python -m metadata_cleaner.cli --file document.pdf --level basic

# Deep cleaning (remove all metadata) - DEFAULT
python -m metadata_cleaner.cli --file document.pdf --level deep

# Paranoid mode (maximum cleaning, rebuild files)
python -m metadata_cleaner.cli --file document.pdf --level paranoid
```

### Batch Processing

```bash
# Clean all files in a folder
python -m metadata_cleaner.cli --folder ./documents

# Clean recursively (including subfolders)
python -m metadata_cleaner.cli --folder ./documents --recursive

# Clean multiple specific files
python -m metadata_cleaner.cli --files file1.pdf file2.docx file3.jpg

# Use multiple workers for faster processing
python -m metadata_cleaner.cli --folder ./documents --workers 8
```

### Reports and Logging

```bash
# Generate detailed JSON report
python -m metadata_cleaner.cli --file document.pdf --report report.json

# Verbose output
python -m metadata_cleaner.cli --file document.pdf --verbose

# Quiet mode (errors only)
python -m metadata_cleaner.cli --file document.pdf --quiet
```

### Advanced Options

```bash
# Custom backup directory
python -m metadata_cleaner.cli --file document.pdf --backup --backup-dir ./backups

# Skip integrity verification (faster but less safe)
python -m metadata_cleaner.cli --file document.pdf --no-verify

# Complete example
python -m metadata_cleaner.cli \
  --folder ./documents \
  --recursive \
  --level paranoid \
  --backup \
  --backup-dir ./backups \
  --workers 8 \
  --report cleaning_report.json \
  --verbose
```

## Web Interface (GUI)

### Starting the Web Server

```bash
# Start with default settings (localhost:5000)
python -m metadata_cleaner.web

# Custom host and port
python -m metadata_cleaner --web --host 0.0.0.0 --port 8080
```

### Using the Web Interface

1. Open browser to `http://localhost:5000`
2. Drag and drop files or click to browse
3. Select cleaning level (Basic, Deep, or Paranoid)
4. Click "Clean Files"
5. Download cleaned files

## Python Library

### Basic Usage

```python
from metadata_cleaner import MetadataCleaner, CleaningLevel

# Initialize cleaner
cleaner = MetadataCleaner(
    level=CleaningLevel.DEEP,
    backup=True,
    verify=True
)

# Clean single file
result = cleaner.clean_file("document.pdf")

if result.success:
    print(f"Cleaned successfully!")
    print(f"Metadata removed: {result.metadata_count} fields")
    print(f"Size reduction: {result.size_reduction_percent:.1f}%")
else:
    print(f"Failed: {result.errors}")
```

### Batch Processing

```python
from metadata_cleaner import MetadataCleaner, CleaningLevel

cleaner = MetadataCleaner(level=CleaningLevel.PARANOID)

# Clean folder
batch_result = cleaner.clean_folder(
    "./documents",
    recursive=True,
    max_workers=8
)

print(f"Total: {batch_result.total_files}")
print(f"Success: {batch_result.successful}")
print(f"Failed: {batch_result.failed}")
print(f"Success rate: {batch_result.success_rate:.1f}%")

# Access individual results
for result in batch_result.results:
    print(f"{result.file_path}: {result.success}")
```

### Custom Output Paths

```python
cleaner = MetadataCleaner()

# Clean to different location
result = cleaner.clean_file(
    "original.pdf",
    output_path="cleaned/cleaned_original.pdf"
)
```

### Accessing Metadata Information

```python
result = cleaner.clean_file("document.pdf")

# See what metadata was removed
for key, value in result.metadata_removed.items():
    print(f"{key}: {value}")

# Check file hashes
print(f"Before: {result.content_hash_before}")
print(f"After: {result.content_hash_after}")

# Get detailed report as dictionary
report = result.to_dict()
```

### Error Handling

```python
result = cleaner.clean_file("document.pdf")

if not result.success:
    print("Errors:")
    for error in result.errors:
        print(f"  - {error}")

if result.warnings:
    print("Warnings:")
    for warning in result.warnings:
        print(f"  - {warning}")
```

## What Metadata is Removed?

### PDF Files
- Author, creator, producer
- Creation and modification dates
- Software information
- XMP metadata packets
- Document info dictionary
- JavaScript
- Page labels
- Embedded file metadata

### Office Documents (DOCX, XLSX, PPTX)
- Author and last modified by
- Company and manager
- Creation and modification dates
- Revision history (rsid attributes)
- Custom properties
- Template information
- Document statistics

### Images (JPEG, PNG, TIFF, etc.)
- EXIF data (camera, GPS, dates)
- IPTC information
- XMP packets
- Thumbnails
- Color profiles (paranoid mode)
- Maker notes
- Comments

### Audio Files (MP3, FLAC, etc.)
- ID3 tags (all versions)
- Artist, album, title
- Year and date
- Comments
- Cover art metadata
- Encoding software

### Video Files (MP4, AVI, MKV, etc.)
- Container metadata
- Creation date
- Encoding software
- GPS coordinates
- Camera information
- Chapters (deep/paranoid)

## Best Practices

1. **Always create backups** when cleaning important files
2. **Test on copies first** before cleaning originals
3. **Use appropriate cleaning level**:
   - Basic: For quick cleaning of common metadata
   - Deep: For thorough privacy protection (recommended)
   - Paranoid: For maximum security (may increase file size)
4. **Verify results** by checking cleaned files open correctly
5. **Generate reports** for auditing and compliance

## Performance Tips

1. Use multiple workers for batch processing
2. Skip verification (`--no-verify`) for faster processing
3. Process files in parallel when cleaning folders
4. Use SSD storage for better I/O performance

## Security Considerations

- This tool removes metadata but doesn't encrypt files
- Some file formats may retain hidden data even after cleaning
- Always verify cleaned files meet your privacy requirements
- Consider using paranoid mode for sensitive documents
- Deleted content in Office documents may still be recoverable
