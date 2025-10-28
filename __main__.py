"""Main entry point for metadata cleaner package."""

import sys
import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Metadata Cleaner - Remove ALL metadata from files',
        epilog='Use "python -m metadata_cleaner.cli" for command-line interface'
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Start web interface'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Web server port (default: 5000)'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Web server host (default: 127.0.0.1)'
    )
    
    args = parser.parse_args()
    
    if args.web:
        from .web import run_server
        run_server(host=args.host, port=args.port)
    else:
        # Default to CLI
        from .cli import main as cli_main
        sys.argv = sys.argv[1:]  # Remove --web flag if present
        cli_main()


if __name__ == '__main__':
    main()
