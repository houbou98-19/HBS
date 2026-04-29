#!/bin/bash
set -e

echo "🎮 HB System Installer"
echo "====================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="/home/hobo/hbs"
SERVICE_NAME="hbs.service"
SERVICE_DIR="/etc/systemd/system"

echo "📦 Installing to $INSTALL_DIR"

# Create install directory if needed
mkdir -p "$INSTALL_DIR"

# Copy files
echo "📋 Copying files..."
cp "$SCRIPT_DIR/hbs.py" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/splash.html" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/add.html" "$INSTALL_DIR/"

# Set permissions
chmod 755 "$INSTALL_DIR/hbs.py"
chmod 644 "$INSTALL_DIR/splash.html"
chmod 644 "$INSTALL_DIR/add.html"

# Install systemd service
echo "⚙️  Installing systemd service..."
sudo cp "$SCRIPT_DIR/hbs.service" "$SERVICE_DIR/"
sudo systemctl daemon-reload

# Stop old service if running
echo "🛑 Stopping old service if running..."
sudo systemctl stop $SERVICE_NAME || true

# Start service
echo "▶️  Starting HBS service..."
sudo systemctl start $SERVICE_NAME

# Enable on boot
echo "🔧 Enabling service on boot..."
sudo systemctl enable $SERVICE_NAME

echo ""
echo "✅ Installation complete!"
echo ""
echo "Service status:"
sudo systemctl status $SERVICE_NAME --no-pager
echo ""
echo "HBS is running at http://localhost:5000"
echo "Logs: sudo journalctl -u hbs.service -f"