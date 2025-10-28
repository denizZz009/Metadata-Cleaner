"""Example usage of metadata cleaner library."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from metadata_cleaner import MetadataCleaner, CleaningLevel
import json


def example_single_file():
    """Example: Clean a single file."""
    print("=" * 60)
    print("EXAMPLE 1: Clean Single File")
    print("=" * 60)
    
    cleaner = MetadataCleaner(
        level=CleaningLevel.DEEP,
        backup=True,
        verify=True
    )
    
    # Create a test file (you should replace with actual file)
    test_file = Path("test_document.pdf")
    
    if not test_file.exists():
        print(f"⚠ Test file not found: {test_file}")
        print("Please create a test file or modify the path")
        return
    
    result = cleaner.clean_file(test_file)
    
    if result.success:
        print(f"✓ Successfully cleaned: {result.file_path.name}")
        print(f"  Original size: {result.original_size:,} bytes")
        print(f"  Cleaned size: {result.cleaned_size:,} bytes")
        print(f"  Size reduction: {result.size_reduction_percent:.1f}%")
        print(f"  Metadata removed: {result.metadata_count} fields")
        print(f"  Processing time: {result.processing_time:.2f}s")
        
        if result.backup_path:
            print(f"  Backup saved: {result.backup_path}")
        
        print("\nMetadata that was removed:")
        for key, value in list(result.metadata_removed.items())[:5]:
            print(f"  - {key}: {value[:50]}...")
    else:
        print(f"✗ Failed to clean file")
        for error in result.errors:
            print(f"  Error: {error}")
    
    print()


def example_batch_processing():
    """Example: Batch process multiple files."""
    print("=" * 60)
    print("EXAMPLE 2: Batch Process Folder")
    print("=" * 60)
    
    cleaner = MetadataCleaner(
        level=CleaningLevel.DEEP,
        backup=True
    )
    
    # Replace with your folder path
    folder_path = Path("./test_documents")
    
    if not folder_path.exists():
        print(f"⚠ Test folder not found: {folder_path}")
        print("Please create a test folder with files or modify the path")
        return
    
    batch_result = cleaner.clean_folder(
        folder_path,
        recursive=True,
        max_workers=4
    )
    
    print(f"Total files processed: {batch_result.total_files}")
    print(f"Successful: {batch_result.successful}")
    print(f"Failed: {batch_result.failed}")
    print(f"Skipped: {batch_result.skipped}")
    print(f"Success rate: {batch_result.success_rate:.1f}%")
    print(f"Total size reduction: {batch_result.total_size_reduction:,} bytes")
    print(f"Total time: {batch_result.total_time:.2f}s")
    
    print("\nIndividual results:")
    for result in batch_result.results[:5]:  # Show first 5
        status = "✓" if result.success else "✗"
        print(f"  {status} {result.file_path.name} - {result.metadata_count} metadata fields removed")
    
    print()


def example_different_levels():
    """Example: Compare different cleaning levels."""
    print("=" * 60)
    print("EXAMPLE 3: Compare Cleaning Levels")
    print("=" * 60)
    
    test_file = Path("test_image.jpg")
    
    if not test_file.exists():
        print(f"⚠ Test file not found: {test_file}")
        return
    
    levels = [
        (CleaningLevel.BASIC, "Basic"),
        (CleaningLevel.DEEP, "Deep"),
        (CleaningLevel.PARANOID, "Paranoid")
    ]
    
    for level, name in levels:
        cleaner = MetadataCleaner(level=level, backup=False)
        output_file = Path(f"test_image_{name.lower()}.jpg")
        
        result = cleaner.clean_file(test_file, output_file)
        
        if result.success:
            print(f"{name:10} - Removed {result.metadata_count:3} fields, "
                  f"Size: {result.cleaned_size:,} bytes, "
                  f"Time: {result.processing_time:.2f}s")
    
    print()


def example_metadata_report():
    """Example: Generate detailed metadata report."""
    print("=" * 60)
    print("EXAMPLE 4: Generate Metadata Report")
    print("=" * 60)
    
    cleaner = MetadataCleaner(level=CleaningLevel.DEEP)
    
    test_file = Path("test_document.pdf")
    
    if not test_file.exists():
        print(f"⚠ Test file not found: {test_file}")
        return
    
    result = cleaner.clean_file(test_file)
    
    # Convert to dictionary for JSON export
    report = result.to_dict()
    
    # Save report
    report_file = Path("cleaning_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Report saved to: {report_file}")
    print(f"\nReport summary:")
    print(f"  File: {report['file_path']}")
    print(f"  Success: {report['success']}")
    print(f"  Metadata removed: {report['metadata_count']} fields")
    print(f"  Size reduction: {report['size_reduction_percent']}%")
    
    print()


def example_error_handling():
    """Example: Proper error handling."""
    print("=" * 60)
    print("EXAMPLE 5: Error Handling")
    print("=" * 60)
    
    cleaner = MetadataCleaner()
    
    # Try to clean non-existent file
    result = cleaner.clean_file("nonexistent.pdf")
    
    if not result.success:
        print("Expected error occurred:")
        for error in result.errors:
            print(f"  ✗ {error}")
    
    # Try to clean unsupported file type
    unsupported = Path("test.xyz")
    unsupported.write_text("test")
    
    result = cleaner.clean_file(unsupported)
    
    if not result.success:
        print("\nExpected error for unsupported file:")
        for error in result.errors:
            print(f"  ✗ {error}")
    
    unsupported.unlink()  # Clean up
    
    print()


def example_custom_workflow():
    """Example: Custom workflow with verification."""
    print("=" * 60)
    print("EXAMPLE 6: Custom Workflow")
    print("=" * 60)
    
    test_file = Path("test_document.pdf")
    
    if not test_file.exists():
        print(f"⚠ Test file not found: {test_file}")
        return
    
    # Step 1: Create backup
    from metadata_cleaner.core.utils import create_backup, calculate_file_hash
    
    backup_path = create_backup(test_file)
    print(f"✓ Backup created: {backup_path}")
    
    # Step 2: Calculate original hash
    original_hash = calculate_file_hash(test_file)
    print(f"✓ Original hash: {original_hash[:16]}...")
    
    # Step 3: Clean file
    cleaner = MetadataCleaner(level=CleaningLevel.PARANOID, backup=False)
    result = cleaner.clean_file(test_file)
    
    if result.success:
        print(f"✓ File cleaned successfully")
        
        # Step 4: Verify content integrity
        cleaned_hash = calculate_file_hash(test_file)
        print(f"✓ Cleaned hash: {cleaned_hash[:16]}...")
        
        # Step 5: Check metadata removal
        print(f"✓ Removed {result.metadata_count} metadata fields")
        
        # Step 6: Verify file opens correctly
        from metadata_cleaner.core.utils import verify_file_integrity
        if verify_file_integrity(backup_path, test_file):
            print(f"✓ File integrity verified")
        
        print(f"\n✓ Workflow completed successfully!")
    else:
        print(f"✗ Cleaning failed")
        for error in result.errors:
            print(f"  {error}")
    
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║        METADATA CLEANER - Usage Examples                 ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    examples = [
        ("Single File Cleaning", example_single_file),
        ("Batch Processing", example_batch_processing),
        ("Cleaning Levels Comparison", example_different_levels),
        ("Metadata Report Generation", example_metadata_report),
        ("Error Handling", example_error_handling),
        ("Custom Workflow", example_custom_workflow),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. Run all examples")
    print()
    
    try:
        choice = input("Select example (0-6): ").strip()
        
        if choice == "0":
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"Error in {name}: {e}\n")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            examples[int(choice) - 1][1]()
        else:
            print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
