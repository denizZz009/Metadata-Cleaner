"""Web GUI for metadata cleaner using Flask."""

import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
import shutil

from .core.cleaner import MetadataCleaner
from .core.enums import CleaningLevel

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()


@app.route('/')
def index():
    """Serve main page."""
    return render_template('index.html')


@app.route('/api/clean', methods=['POST'])
def clean_file():
    """Clean uploaded file."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get cleaning level
        level_str = request.form.get('level', 'deep')
        level_map = {
            'basic': CleaningLevel.BASIC,
            'deep': CleaningLevel.DEEP,
            'paranoid': CleaningLevel.PARANOID
        }
        level = level_map.get(level_str, CleaningLevel.DEEP)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(input_path)
        
        # Clean the file
        output_path = Path(app.config['UPLOAD_FOLDER']) / f"cleaned_{filename}"
        
        cleaner = MetadataCleaner(level=level, backup=False, verify=True)
        result = cleaner.clean_file(input_path, output_path)
        
        if result.success:
            # Return cleaned file info
            return jsonify({
                'success': True,
                'filename': f"cleaned_{filename}",
                'original_size': result.original_size,
                'cleaned_size': result.cleaned_size,
                'size_reduction': result.size_reduction,
                'size_reduction_percent': result.size_reduction_percent,
                'metadata_removed': result.metadata_removed,
                'metadata_count': result.metadata_count,
                'warnings': result.warnings
            })
        else:
            return jsonify({
                'success': False,
                'errors': result.errors
            }), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download cleaned file."""
    try:
        file_path = Path(app.config['UPLOAD_FOLDER']) / secure_filename(filename)
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch-clean', methods=['POST'])
def batch_clean():
    """Clean multiple uploaded files."""
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        level_str = request.form.get('level', 'deep')
        level_map = {
            'basic': CleaningLevel.BASIC,
            'deep': CleaningLevel.DEEP,
            'paranoid': CleaningLevel.PARANOID
        }
        level = level_map.get(level_str, CleaningLevel.DEEP)
        
        cleaner = MetadataCleaner(level=level, backup=False, verify=True)
        results = []
        
        for file in files:
            if file.filename == '':
                continue
            
            filename = secure_filename(file.filename)
            input_path = Path(app.config['UPLOAD_FOLDER']) / filename
            output_path = Path(app.config['UPLOAD_FOLDER']) / f"cleaned_{filename}"
            
            file.save(input_path)
            result = cleaner.clean_file(input_path, output_path)
            
            results.append({
                'filename': filename,
                'success': result.success,
                'cleaned_filename': f"cleaned_{filename}" if result.success else None,
                'original_size': result.original_size,
                'cleaned_size': result.cleaned_size,
                'size_reduction_percent': result.size_reduction_percent,
                'metadata_count': result.metadata_count,
                'errors': result.errors,
                'warnings': result.warnings
            })
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def run_server(host='0.0.0.0', port=5000, debug=False):
    """Run Flask development server."""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║           METADATA CLEANER - Web Interface               ║
╚═══════════════════════════════════════════════════════════╝

Server running at: http://localhost:{port}
Press Ctrl+C to stop
    """)
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
