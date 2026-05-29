#!/bin/bash
set -e

echo "🎮 HB System Installer"
echo "====================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="/home/hobo/hbs"
HBS_SERVICE="hbs.service"
CAROUSEL_SERVICE="hbs-carousel.service"

echo "📦 Installing to $INSTALL_DIR"

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt-get install -y retroarch dbus-x11 python3-pip

# Install Python packages
echo "📦 Installing Python packages..."
pip3 install pyglet requests --break-system-packages

# Install Press Start 2P font
echo "🎨 Installing Press Start 2P font..."
mkdir -p ~/.local/share/fonts
if [ ! -f ~/.local/share/fonts/PressStart2P-Regular.ttf ]; then
    wget -O ~/.local/share/fonts/PressStart2P-Regular.ttf \
        https://github.com/google/fonts/raw/main/ofl/pressstart2p/PressStart2P-Regular.ttf 2>/dev/null || true
    fc-cache -fv > /dev/null 2>&1 || true
fi

# Create install directory if needed
mkdir -p "$INSTALL_DIR"

# Backup existing configs
if [ -f "$INSTALL_DIR/config.json" ]; then
    cp "$INSTALL_DIR/config.json" "$INSTALL_DIR/config.json.bak"
fi
if [ -f "$INSTALL_DIR/carousel_config.json" ]; then
    cp "$INSTALL_DIR/carousel_config.json" "$INSTALL_DIR/carousel_config.json.bak"
fi

# Copy all files from package
echo "📋 Copying files..."
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"

# Restore user configs if they existed
if [ -f "$INSTALL_DIR/config.json.bak" ]; then
    mv "$INSTALL_DIR/config.json.bak" "$INSTALL_DIR/config.json"
    echo "✓ Preserved existing HBS config"
fi
if [ -f "$INSTALL_DIR/carousel_config.json.bak" ]; then
    mv "$INSTALL_DIR/carousel_config.json.bak" "$INSTALL_DIR/carousel_config.json"
    echo "✓ Preserved existing Carousel config"
fi

# Also preserve ~/.hbs configs
mkdir -p ~/.hbs
if [ -f "$INSTALL_DIR/config.json" ] && [ ! -f ~/.hbs/config.json ]; then
    cp "$INSTALL_DIR/config.json" ~/.hbs/config.json
fi
if [ -f "$INSTALL_DIR/carousel_config.json" ] && [ ! -f ~/.hbs/carousel_config.json ]; then
    cp "$INSTALL_DIR/carousel_config.json" ~/.hbs/carousel_config.json
fi

# Set permissions for entire directory
chmod -R 755 "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/carousel.py"
chmod +x "$INSTALL_DIR/launcher.sh"

# Restart services
echo "🔄 Restarting HBS services..."
sudo systemctl daemon-reload
sudo systemctl enable $HBS_SERVICE $CAROUSEL_SERVICE
sudo systemctl restart $HBS_SERVICE
sudo systemctl restart $CAROUSEL_SERVICE

echo ""
echo "✅ Installation complete!"
echo ""
echo "HBS Backend: http://localhost:5000"
echo "Carousel Menu: Running on display :0"