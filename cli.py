"""Command-line interface for metadata cleaner."""

import argparse
import sys
import json
import logging
from pathlib import Path
from colorama import init, Fore, Style

from .core.cleaner import MetadataCleaner
from .core.enums import CleaningLevel

# Initialize colorama for Windows support
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print application banner."""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║           METADATA CLEANER - Privacy Protection          ║
║              Remove ALL metadata from files               ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_result(result):
    """Print cleaning result."""
    if result.success:
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {result.file_path.name}")
        print(f"  Size: {result.original_size:,} → {result.cleaned_size:,} bytes "
              f"({Fore.YELLOW}-{result.size_reduction_percent:.1f}%{Style.RESET_ALL})")
        print(f"  Metadata removed: {Fore.CYAN}{result.metadata_count}{Style.RESET_ALL} fields")
        
        if result.warnings:
            for warning in result.warnings:
                print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} {warning}")
    else:
        print(f"{Fore.RED}✗{Style.RESET_ALL} {result.file_path.name}")
        for error in result.errors:
            print(f"  {Fore.RED}Error:{Style.RESET_ALL} {error}")
    
    print()


def print_batch_summary(batch_result):
    """Print batch cleaning summary."""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}SUMMARY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"Total files: {batch_result.total_files}")
    print(f"{Fore.GREEN}Successful:{Style.RESET_ALL} {batch_result.successful}")
    print(f"{Fore.RED}Failed:{Style.RESET_ALL} {batch_result.failed}")
    if batch_result.skipped > 0:
        print(f"{Fore.YELLOW}Skipped:{Style.RESET_ALL} {batch_result.skipped}")
    print(f"Success rate: {batch_result.success_rate:.1f}%")
    print(f"Total size reduction: {batch_result.total_size_reduction:,} bytes")
    print(f"Processing time: {batch_result.total_time:.2f}s")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def save_report(result, report_path: Path):
    """Save cleaning report to JSON file."""
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            if hasattr(result, 'to_dict'):
                json.dump(result.to_dict(), f, indent=2)
            else:
                json.dump(result, f, indent=2)
        print(f"{Fore.GREEN}Report saved:{Style.RESET_ALL} {report_path}")
    except Exception as e:
        print(f"{Fore.RED}Failed to save report:{Style.RESET_ALL} {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Remove ALL metadata from documents while preserving content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean single file
  python -m metadata_cleaner.cli --file document.pdf
  
  # Deep cleaning with backup
  python -m metadata_cleaner.cli --file document.pdf --level deep --backup
  
  # Batch process folder
  python -m metadata_cleaner.cli --folder ./documents --recursive
  
  # Generate report
  python -m metadata_cleaner.cli --file image.jpg --report report.json
  
  # Process multiple files
  python -m metadata_cleaner.cli --files file1.pdf file2.docx file3.jpg
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--file',
        type=str,
        help='Single file to clean'
    )
    input_group.add_argument(
        '--folder',
        type=str,
        help='Folder to clean'
    )
    input_group.add_argument(
        '--files',
        nargs='+',
        help='Multiple files to clean'
    )
    
    # Cleaning options
    parser.add_argument(
        '--level',
        type=str,
        choices=['basic', 'deep', 'paranoid'],
        default='deep',
        help='Cleaning level (default: deep)'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup before cleaning'
    )
    parser.add_argument(
        '--no-verify',
        action='store_true',
        help='Skip file integrity verification'
    )
    parser.add_argument(
        '--backup-dir',
        type=str,
        help='Custom backup directory'
    )
    
    # Folder options
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Process folders recursively'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    # Output options
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (for single file only)'
    )
    parser.add_argument(
        '--report',
        type=str,
        help='Save detailed report to JSON file'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    # Print banner
    if not args.quiet:
        print_banner()
    
    # Parse cleaning level
    level_map = {
        'basic': CleaningLevel.BASIC,
        'deep': CleaningLevel.DEEP,
        'paranoid': CleaningLevel.PARANOID
    }
    level = level_map[args.level]
    
    # Initialize cleaner
    cleaner = MetadataCleaner(
        level=level,
        backup=args.backup,
        verify=not args.no_verify,
        backup_dir=args.backup_dir
    )
    
    # Process files
    try:
        if args.file:
            # Single file
            if not args.quiet:
                print(f"Cleaning: {args.file}")
                print(f"Level: {Fore.CYAN}{args.level.upper()}{Style.RESET_ALL}\n")
            
            result = cleaner.clean_file(args.file, args.output)
            
            if not args.quiet:
                print_result(result)
            
            if args.report:
                save_report(result, Path(args.report))
            
            sys.exit(0 if result.success else 1)
            
        elif args.folder:
            # Folder
            if not args.quiet:
                print(f"Cleaning folder: {args.folder}")
                print(f"Level: {Fore.CYAN}{args.level.upper()}{Style.RESET_ALL}")
                print(f"Recursive: {args.recursive}\n")
            
            batch_result = cleaner.clean_folder(
                args.folder,
                recursive=args.recursive,
                max_workers=args.workers
            )
            
            if not args.quiet:
                for result in batch_result.results:
                    print_result(result)
                print_batch_summary(batch_result)
            
            if args.report:
                save_report(batch_result, Path(args.report))
            
            sys.exit(0 if batch_result.failed == 0 else 1)
            
        elif args.files:
            # Multiple files
            if not args.quiet:
                print(f"Cleaning {len(args.files)} files")
                print(f"Level: {Fore.CYAN}{args.level.upper()}{Style.RESET_ALL}\n")
            
            batch_result = cleaner.clean_files(
                args.files,
                max_workers=args.workers
            )
            
            if not args.quiet:
                for result in batch_result.results:
                    print_result(result)
                print_batch_summary(batch_result)
            
            if args.report:
                save_report(batch_result, Path(args.report))
            
            sys.exit(0 if batch_result.failed == 0 else 1)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
