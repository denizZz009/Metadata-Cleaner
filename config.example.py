"""
Configuration example for metadata cleaner.

Copy this file to config.py and customize as needed.
"""

# Default cleaning level
# Options: 'basic', 'deep', 'paranoid'
DEFAULT_CLEANING_LEVEL = 'deep'

# Backup settings
CREATE_BACKUPS = True
BACKUP_DIRECTORY = None  # None = create in same directory as file

# Verification settings
VERIFY_INTEGRITY = True
CALCULATE_HASHES = True

# Performance settings
MAX_WORKERS = 4  # Number of parallel workers for batch processing
CHUNK_SIZE = 8192  # Bytes to read at a time for hashing

# Web server settings
WEB_HOST = '127.0.0.1'
WEB_PORT = 5000
WEB_DEBUG = False
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB

# Logging settings
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = None  # None = console only, or specify file path
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# File type settings
SUPPORTED_EXTENSIONS = {
    'documents': ['.pdf', '.docx', '.xlsx', '.pptx', '.odt', '.ods', '.odp', '.rtf', '.txt'],
    'images': ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.gif', '.bmp', '.webp'],
    'audio': ['.mp3', '.flac', '.wav', '.m4a', '.ogg'],
    'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
}

# Cleaning options per file type
PDF_OPTIONS = {
    'remove_javascript': True,
    'remove_embedded_files_metadata': True,
    'remove_page_labels': True,
    'linearize_paranoid': True
}

OFFICE_OPTIONS = {
    'remove_rsid': True,
    'remove_custom_properties': True,
    'clean_content_files': True
}

IMAGE_OPTIONS = {
    'use_exiftool': True,  # Use ExifTool if available
    'remove_color_profile': False,  # Only in paranoid mode
    'jpeg_quality': 95,
    'optimize': True
}

AUDIO_OPTIONS = {
    'remove_cover_art': True,
    'remove_all_tags': True
}

VIDEO_OPTIONS = {
    'remove_chapters': True,
    'bitexact': True
}

# Report settings
REPORT_FORMAT = 'json'  # json, csv, txt
INCLUDE_METADATA_VALUES = True
TRUNCATE_LONG_VALUES = 100  # Characters

# Security settings
SECURE_DELETE = False  # Overwrite files before deletion (slower)
OVERWRITE_PASSES = 3  # Number of overwrite passes for secure delete

# Advanced settings
TEMP_DIRECTORY = None  # None = system temp, or specify path
PRESERVE_TIMESTAMPS = False  # Preserve file modification times
FOLLOW_SYMLINKS = False  # Follow symbolic links in batch processing

# Error handling
CONTINUE_ON_ERROR = True  # Continue batch processing on errors
MAX_RETRIES = 3  # Retry failed operations
RETRY_DELAY = 1  # Seconds between retries

# Metadata fields to always remove (in addition to standard cleaning)
ALWAYS_REMOVE = [
    'Author',
    'Creator',
    'Producer',
    'CreationDate',
    'ModDate',
    'Company',
    'Manager',
    'GPS*',  # Wildcard for all GPS fields
]

# Metadata fields to preserve (only in BASIC mode)
PRESERVE_IN_BASIC = [
    'ColorSpace',
    'Width',
    'Height',
    'Format',
]

# Custom metadata mappings
METADATA_ALIASES = {
    'Author': ['Creator', 'Writer', 'Artist'],
    'Date': ['CreationDate', 'ModDate', 'CreateDate', 'ModifyDate'],
    'Software': ['Producer', 'CreatorTool', 'Application'],
}

# Validation settings
VALIDATE_AFTER_CLEANING = True
VALIDATION_TIMEOUT = 30  # Seconds

# Notification settings (for future implementation)
NOTIFY_ON_COMPLETION = False
NOTIFICATION_EMAIL = None
NOTIFICATION_WEBHOOK = None

# Statistics
COLLECT_STATISTICS = True
STATISTICS_FILE = 'cleaning_stats.json'

# Development settings
DEBUG_MODE = False
VERBOSE_LOGGING = False
SAVE_INTERMEDIATE_FILES = False  # For debugging


def get_config():
    """Get configuration as dictionary."""
    import inspect
    config = {}
    for name, value in globals().items():
        if name.isupper() and not name.startswith('_'):
            config[name] = value
    return config


def print_config():
    """Print current configuration."""
    config = get_config()
    print("Current Configuration:")
    print("=" * 60)
    for key, value in sorted(config.items()):
        print(f"{key:30} = {value}")
    print("=" * 60)


if __name__ == '__main__':
    print_config()
