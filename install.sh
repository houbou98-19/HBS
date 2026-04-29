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

# Copy files
echo "📋 Copying files..."
cp "$SCRIPT_DIR/hbs.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/splash.html" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/add.html" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/config.json" "$INSTALL_DIR/"

# Set permissions
chmod 755 "$INSTALL_DIR/hbs.py"
chmod 644 "$INSTALL_DIR/splash.html"
chmod 644 "$INSTALL_DIR/add.html"
chmod 644 "$INSTALL_DIR/config.json"

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