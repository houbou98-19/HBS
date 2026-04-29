#!/bin/bash
set -e

echo "🎮 HB System Installer"
echo "====================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="/home/hobo/hbs"
SERVICE_NAME="hbs.service"

echo "📦 Installing to $INSTALL_DIR"

# Create install directory if needed
mkdir -p "$INSTALL_DIR"

# Copy all files from package
echo "📋 Copying files..."
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"

# Set permissions for entire directory
chmod -R 755 "$INSTALL_DIR"

# Restart service
echo "🔄 Restarting HBS service..."
sudo systemctl daemon-reload
sudo systemctl restart $SERVICE_NAME

echo ""
echo "✅ Installation complete!"
echo ""
echo "Service status:"
sudo systemctl status $SERVICE_NAME --no-pager
echo ""
echo "HBS is running at http://localhost:5000"
echo "Logs: sudo journalctl -u hbs.service -f"