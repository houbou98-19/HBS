#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/hobo/.Xauthority
export MESA_GL_VERSION_OVERRIDE=4.3COMPAT
export MESA_GLSL_VERSION_OVERRIDE=430

CORE="$1"
ROM="$2"

# Check if it's an AppImage (Eden for Switch)
if [[ "$CORE" == *.AppImage ]]; then
  dbus-launch "$CORE" "$ROM" 2>/tmp/eden.log
else
  # RetroArch for everything else
  dbus-launch retroarch --fullscreen --verbose -L "$CORE" "$ROM" 2>/tmp/ra.log
fi