#!/bin/bash

# Get command
COMMAND=$1

case "$COMMAND" in
  menu)
    # Launch RetroArch menu
    pkill -9 retroarch 2>/dev/null || true
    export DISPLAY=:0
    export XAUTHORITY=/home/hobo/.Xauthority
    /usr/bin/retroarch &
    ;;
  *)
    echo "Unknown command: $COMMAND"
    exit 1
    ;;
esac