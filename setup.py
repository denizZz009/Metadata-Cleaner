"""Setup script for metadata cleaner package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="metadata-cleaner",
    version="1.0.0",
    author="Privacy Tools",
    description="Complete metadata removal tool for documents, images, audio, and video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/metadata-cleaner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pikepdf>=8.0.0",
        "python-docx>=1.0.0",
        "openpyxl>=3.1.0",
        "python-pptx>=0.6.21",
        "Pillow>=10.0.0",
        "mutagen>=1.47.0",
        "PyExifTool>=0.5.5",
        "pymediainfo>=6.0.1",
        "odfpy>=1.4.1",
        "striprtf>=0.0.26",
        "Flask>=3.0.0",
        "Flask-CORS>=4.0.0",
        "tqdm>=4.66.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "metadata-cleaner=metadata_cleaner.cli:main",
            "metadata-cleaner-web=metadata_cleaner.web:run_server",
        ],
    },
    include_package_data=True,
    package_data={
        "metadata_cleaner": ["templates/*.html"],
    },
    keywords="metadata privacy exif pdf office cleaner security",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/metadata-cleaner/issues",
        "Source": "https://github.com/yourusername/metadata-cleaner",
        "Documentation": "https://github.com/yourusername/metadata-cleaner/blob/main/README.md",
    },
)
