# Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                          │
├──────────────┬──────────────────┬─────────────────────────┤
│   CLI        │   Web GUI        │   Python API            │
│  (cli.py)    │   (web.py)       │   (import library)      │
└──────┬───────┴────────┬─────────┴──────────┬──────────────┘
       │                │                     │
       └────────────────┼─────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              CORE ORCHESTRATOR                               │
│              (MetadataCleaner)                               │
│  • File type detection                                       │
│  • Cleaner selection                                         │
│  • Backup management                                         │
│  • Verification                                              │
│  • Batch processing                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   PDF       │  │   Office    │  │   Image     │
│  Cleaner    │  │  Cleaner    │  │  Cleaner    │
└─────────────┘  └─────────────┘  └─────────────┘
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Audio     │  │   Video     │  │   Text      │
│  Cleaner    │  │  Cleaner    │  │  Cleaner    │
└─────────────┘  └─────────────┘  └─────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTERNAL DEPENDENCIES                           │
│  • pikepdf (PDF)                                            │
│  • Pillow (Images)                                          │
│  • mutagen (Audio)                                          │
│  • FFmpeg (Video)                                           │
│  • ExifTool (Comprehensive metadata)                        │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Core Layer

```
core/
├── cleaner.py          # Main orchestrator
│   └── MetadataCleaner
│       ├── clean_file()
│       ├── clean_folder()
│       ├── clean_files()
│       └── _get_cleaner()
│
├── enums.py            # Type definitions
│   ├── CleaningLevel
│   └── FileType
│
├── result.py           # Result objects
│   ├── CleaningResult
│   └── BatchCleaningResult
│
└── utils.py            # Utility functions
    ├── calculate_file_hash()
    ├── create_backup()
    ├── verify_file_integrity()
    └── get_file_size()
```

### 2. Cleaners Layer

```
cleaners/
├── base_cleaner.py     # Abstract base
│   └── BaseCleaner
│       ├── clean()              [abstract]
│       ├── extract_metadata()   [abstract]
│       ├── reset()
│       ├── add_warning()
│       └── add_error()
│
├── pdf_cleaner.py
│   └── PDFCleaner(BaseCleaner)
│       ├── clean()
│       └── extract_metadata()
│
├── office_cleaner.py
│   └── OfficeCleaner(BaseCleaner)
│       ├── clean()
│       ├── extract_metadata()
│       ├── _clean_xml_metadata()
│       ├── _clean_content_files()
│       ├── _remove_rsid_attributes()
│       ├── _update_content_types()
│       └── _create_office_file()
│
├── image_cleaner.py
│   └── ImageCleaner(BaseCleaner)
│
├── audio_cleaner.py
│   └── AudioCleaner(BaseCleaner)
│
├── video_cleaner.py
│   └── VideoCleaner(BaseCleaner)
│
└── text_cleaner.py
    └── TextCleaner(BaseCleaner)
```

### 3. Interface Layer

```
interfaces/
├── cli.py              # Command-line interface
│   ├── main()
│   ├── print_banner()
│   ├── print_result()
│   ├── print_batch_summary()
│   └── save_report()
│
├── web.py              # Web server
│   ├── index()
│   ├── clean_file()
│   ├── download_file()
│   ├── batch_clean()
│   └── run_server()
│
└── __init__.py         # Python API
    └── exports: MetadataCleaner, CleaningLevel, etc.
```

## Data Flow

### Single File Cleaning

```
1. User Input
   ├── File path
   ├── Cleaning level
   └── Options (backup, verify)
   
2. MetadataCleaner.clean_file()
   ├── Validate file exists
   ├── Check file type supported
   ├── Get file size and hash
   └── Create backup (if requested)
   
3. Get Appropriate Cleaner
   ├── Detect file type from extension
   └── Return specific cleaner instance
   
4. Cleaner.extract_metadata()
   └── Read current metadata for reporting
   
5. Cleaner.clean()
   ├── Remove metadata (level-specific)
   ├── Write cleaned file
   └── Track removed metadata
   
6. Verification (if requested)
   ├── Calculate new hash
   ├── Verify file integrity
   └── Check file opens correctly
   
7. Return CleaningResult
   ├── Success status
   ├── Metadata removed
   ├── Size changes
   ├── Errors/warnings
   └── Processing time
```

### Batch Processing

```
1. User Input
   ├── Folder path or file list
   ├── Recursive flag
   └── Worker count
   
2. MetadataCleaner.clean_folder()
   ├── Scan for supported files
   └── Create file list
   
3. ThreadPoolExecutor
   ├── Create worker pool
   └── Submit clean_file() tasks
   
4. Process Files in Parallel
   ├── Worker 1: clean_file(file1)
   ├── Worker 2: clean_file(file2)
   ├── Worker 3: clean_file(file3)
   └── Worker 4: clean_file(file4)
   
5. Collect Results
   └── BatchCleaningResult
       ├── Individual results
       ├── Statistics
       └── Summary
```

## Design Patterns

### 1. Strategy Pattern
```python
# Different cleaning strategies for different file types
class BaseCleaner(ABC):
    @abstractmethod
    def clean(self, input_path, output_path):
        pass

class PDFCleaner(BaseCleaner):
    def clean(self, input_path, output_path):
        # PDF-specific cleaning

class ImageCleaner(BaseCleaner):
    def clean(self, input_path, output_path):
        # Image-specific cleaning
```

### 2. Factory Pattern
```python
def _get_cleaner(self, file_path):
    """Factory method to get appropriate cleaner"""
    file_type = FileType.from_extension(file_path.suffix)
    
    if file_type == FileType.PDF:
        return self.cleaners['pdf']
    elif file_type.is_image():
        return self.cleaners['image']
    # ...
```

### 3. Template Method Pattern
```python
class BaseCleaner:
    def clean(self, input_path, output_path):
        # Template method with common workflow
        self.reset()
        metadata = self.extract_metadata(input_path)
        success = self._do_clean(input_path, output_path)
        return success
```

### 4. Facade Pattern
```python
class MetadataCleaner:
    """Facade providing simple interface to complex subsystem"""
    def clean_file(self, file_path):
        # Hides complexity of:
        # - File type detection
        # - Cleaner selection
        # - Backup management
        # - Verification
```

## Threading Model

```
Main Thread
    │
    ├─── CLI/Web/API Interface
    │
    └─── MetadataCleaner
         │
         └─── ThreadPoolExecutor (for batch)
              │
              ├─── Worker Thread 1
              │    └─── clean_file() → Cleaner
              │
              ├─── Worker Thread 2
              │    └─── clean_file() → Cleaner
              │
              ├─── Worker Thread 3
              │    └─── clean_file() → Cleaner
              │
              └─── Worker Thread 4
                   └─── clean_file() → Cleaner
```

## Error Handling Strategy

```
┌─────────────────────────────────────┐
│  User Operation                      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Try: Execute operation              │
├─────────────────────────────────────┤
│  • Validate inputs                   │
│  • Check file exists                 │
│  • Verify file type                  │
│  • Perform cleaning                  │
└──────────────┬──────────────────────┘
               │
               ├─── Success ──────────┐
               │                       │
               └─── Exception         │
                    │                  │
                    ▼                  ▼
         ┌──────────────────┐  ┌─────────────┐
         │  Catch & Handle   │  │   Return    │
         ├──────────────────┤  │   Result    │
         │ • Log error       │  │  (success)  │
         │ • Add to errors   │  └─────────────┘
         │ • Cleanup         │
         │ • Return result   │
         │   (failure)       │
         └──────────────────┘
```

## Security Considerations

### 1. Input Validation
```python
# File path validation
if not file_path.exists():
    return error_result("File not found")

# File type validation
if not is_supported_file(file_path):
    return error_result("Unsupported file type")

# Size validation
if file_size > MAX_SIZE:
    return error_result("File too large")
```

### 2. Backup Strategy
```python
# Always backup before modification
if self.backup:
    backup_path = create_backup(file_path)
    
# Rollback on failure
if not success and backup_path:
    restore_from_backup(backup_path, file_path)
```

### 3. Verification
```python
# Hash verification
hash_before = calculate_hash(file_path)
# ... cleaning ...
hash_after = calculate_hash(file_path)

# Integrity check
if not verify_integrity(file_path):
    rollback()
```

## Performance Optimization

### 1. Parallel Processing
- ThreadPoolExecutor for I/O-bound operations
- Configurable worker count
- Efficient task distribution

### 2. Memory Management
- Streaming for large files
- Chunk-based processing
- Temporary file cleanup

### 3. Caching
- File type detection cache
- Metadata extraction cache (future)
- Cleaner instance reuse

## Extension Points

### Adding New File Type

```python
# 1. Add to FileType enum
class FileType(Enum):
    NEW_FORMAT = "new"

# 2. Create cleaner
class NewFormatCleaner(BaseCleaner):
    def clean(self, input_path, output_path):
        # Implementation
        pass
    
    def extract_metadata(self, file_path):
        # Implementation
        pass

# 3. Register in MetadataCleaner
self.cleaners['new_format'] = NewFormatCleaner(level)

# 4. Add to _get_cleaner()
if file_type == FileType.NEW_FORMAT:
    return self.cleaners['new_format']
```

### Adding New Cleaning Level

```python
# 1. Add to CleaningLevel enum
class CleaningLevel(Enum):
    ULTRA_PARANOID = auto()

# 2. Implement in cleaners
def clean(self, input_path, output_path):
    if self.level == CleaningLevel.ULTRA_PARANOID:
        # Ultra paranoid cleaning logic
        pass
```

## Testing Architecture

```
tests/
├── unit/
│   ├── test_cleaners.py
│   ├── test_utils.py
│   └── test_enums.py
│
├── integration/
│   ├── test_workflows.py
│   └── test_batch.py
│
└── fixtures/
    ├── sample.pdf
    ├── sample.docx
    └── sample.jpg
```

## Deployment Architecture

```
Production Environment
    │
    ├─── CLI Deployment
    │    └── Standalone executable
    │
    ├─── Web Deployment
    │    ├── Flask app
    │    ├── WSGI server (Gunicorn)
    │    └── Reverse proxy (Nginx)
    │
    └─── Library Deployment
         └── PyPI package
```

---

This architecture provides:
- **Modularity**: Easy to add new file types
- **Extensibility**: Plugin system ready
- **Maintainability**: Clear separation of concerns
- **Testability**: Each component independently testable
- **Performance**: Parallel processing support
- **Reliability**: Comprehensive error handling
