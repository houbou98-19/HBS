#!/bin/bash
set -e

echo "Building HBS Backend AppImage..."

# Install dependencies
pip install pyinstaller flask requests

# Build with PyInstaller
pyinstaller hbs.spec --distpath ./dist --buildpath ./build