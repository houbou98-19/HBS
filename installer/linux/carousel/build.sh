#!/bin/bash
set -e

echo "Building HBS Carousel AppImage..."

# Install dependencies
pip install pyinstaller pyglet requests

# Build with PyInstaller
pyinstaller carousel.spec --distpath ./dist --buildpath ./build
