#!/bin/bash

COMMAND=$1
PLATFORM=$2
ROM_PATH=$3

case "$COMMAND" in
  menu)
    # Launch RetroArch menu
    pkill -9 retroarch 2>/dev/null || true
    export DISPLAY=:0
    export XAUTHORITY=/home/hobo/.Xauthority
    dbus-launch /usr/bin/retroarch --fullscreen &
    ;;
  launch)
    # Launch specific game
    if [ -z "$PLATFORM" ] || [ -z "$ROM_PATH" ]; then
      echo "Usage: launcher.sh launch PLATFORM ROM_PATH"
      exit 1
    fi
    pkill -9 retroarch 2>/dev/null || true
    export DISPLAY=:0
    export XAUTHORITY=/home/hobo/.Xauthority
    export MESA_GL_VERSION_OVERRIDE=4.3COMPAT
    export MESA_GLSL_VERSION_OVERRIDE=430
    dbus-launch /usr/bin/retroarch --fullscreen -L "$PLATFORM" "$ROM_PATH" &
    ;;
  *)
    echo "Unknown command: $COMMAND"
    exit 1
    ;;
esac