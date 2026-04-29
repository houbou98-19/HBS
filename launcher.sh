#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/hobo/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
export MESA_GL_VERSION_OVERRIDE=4.3COMPAT
export MESA_GLSL_VERSION_OVERRIDE=430

CORE="$1"
ROM="$2"

CORES_DIR="$HOME/.config/retroarch/cores"

# Kill all running emulators and Chromium first
pkill -9 retroarch
pkill -9 -f '/bin/eden'
pkill -9 chromium

sleep 1

# Menu mode - no ROM
if [ "$CORE" = "menu" ]; then
  dbus-launch retroarch --fullscreen 2>/tmp/ra.log
# Check if it's an AppImage (Eden for Switch)
elif [[ "$CORE" == *.AppImage ]]; then
  dbus-launch "$CORE" "$ROM" 2>/tmp/eden.log
else
  # RetroArch for everything else
  CORE_PATH="$CORES_DIR/${CORE}"
  dbus-launch retroarch --fullscreen --verbose -L "$CORE_PATH" "$ROM" 2>/tmp/ra.log
fi

DISPLAY=:0 chromium-browser --kiosk --no-first-run http://localhost:5000 &
disown