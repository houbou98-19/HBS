#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/hobo/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
export MESA_GL_VERSION_OVERRIDE=4.3COMPAT
export MESA_GLSL_VERSION_OVERRIDE=430

CORE="$1"
ROM="$2"

CORES_DIR="$HOME/.config/retroarch/cores"
EDEN_APPIMAGE="$CORES_DIR/Eden-Linux-v0.0.4-amd64-gcc-standard.AppImage"

# Kill all running emulators and Firefox (only if launching a game/menu)
if [ -n "$CORE" ]; then
  pkill -9 retroarch
  pkill -9 -f '/bin/eden'
  pkill -9 -f firefox
  sleep 1
fi

# Parameter handling
if [ "$CORE" = "menu" ]; then
  # Launch RetroArch menu
  DISPLAY=:0 XAUTHORITY=/home/hobo/.Xauthority retroarch --fullscreen 2>/tmp/ra.log &
  wait
  # When game closes, restart Firefox
  sleep 1
  DISPLAY=:0 XAUTHORITY=/home/hobo/.Xauthority firefox --kiosk http://localhost:5000 &
  disown

elif [ "$CORE" = "eden" ]; then
  # Launch Eden with ROM
  if [ -z "$ROM" ]; then
    # Eden with no ROM (launcher mode)
    "$EDEN_APPIMAGE" > /tmp/eden.log 2>&1 &
  else
    # Eden with specific ROM
    "$EDEN_APPIMAGE" "$ROM" > /tmp/eden.log 2>&1 &
  fi
  wait
  # When done, restart Firefox
  sleep 1
  DISPLAY=:0 XAUTHORITY=/home/hobo/.Xauthority firefox --kiosk http://localhost:5000 &
  disown

elif [ -n "$CORE" ]; then
  # Launch RetroArch with core and ROM
  CORE_PATH="$CORES_DIR/${CORE}"
  DISPLAY=:0 XAUTHORITY=/home/hobo/.Xauthority retroarch --fullscreen -L "$CORE_PATH" "$ROM" 2>/tmp/ra.log &
  wait
  # When game closes, restart Firefox
  sleep 1
  DISPLAY=:0 XAUTHORITY=/home/hobo/.Xauthority firefox --kiosk http://localhost:5000 &
  disown

else
  # No parameters - just launch Firefox kiosk
  DISPLAY=:0 XAUTHORITY=/home/hobo/.Xauthority firefox --kiosk http://localhost:5000 &
  disown
fi
EOF
chmod +x ~/hbs/launcher.sh