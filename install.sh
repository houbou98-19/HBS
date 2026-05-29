#!/bin/bash
set -e

echo "🎮 HB System Installer"
echo "====================="

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="/home/hobo/hbs"

echo "📦 Installing to $INSTALL_DIR"

# Install dependencies (only system packages)
echo "📦 Installing dependencies..."
sudo apt-get install -y retroarch dbus-x11

# Install Press Start 2P font
echo "🎨 Installing Press Start 2P font..."
mkdir -p ~/.local/share/fonts
if [ ! -f ~/.local/share/fonts/PressStart2P-Regular.ttf ]; then
    wget -O ~/.local/share/fonts/PressStart2P-Regular.ttf \
        https://github.com/google/fonts/raw/main/ofl/pressstart2p/PressStart2P-Regular.ttf 2>/dev/null || true
    fc-cache -fv > /dev/null 2>&1 || true
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p ~/.hbs

# Copy binaries and files
echo "📋 Copying files..."
cp "$SCRIPT_DIR/hbs" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/hbs-carousel" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/install.sh" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/launcher.sh" "$INSTALL_DIR/"

# Copy configs only if they don't exist (preserve user configs)
if [ ! -f ~/.hbs/config.json ] && [ -f "$SCRIPT_DIR/config.json" ]; then
    cp "$SCRIPT_DIR/config.json" ~/.hbs/config.json
    echo "✓ Created default HBS config"
fi

if [ ! -f ~/.hbs/carousel_config.json ] && [ -f "$SCRIPT_DIR/carousel_config.json" ]; then
    cp "$SCRIPT_DIR/carousel_config.json" ~/.hbs/carousel_config.json
    echo "✓ Created default Carousel config"
fi

# Restart services
echo "🔄 Restarting HBS services..."
sudo systemctl daemon-reload
sudo systemctl restart hbs.service
sudo systemctl restart hbs-carousel.service

echo ""
echo "✅ Installation complete!"
echo "HBS Backend: http://localhost:5000"
echo "Carousel Menu: Running on display :0"