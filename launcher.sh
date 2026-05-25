#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/hobo/.Xauthority

LAUNCHER_SCRIPT="$1"

LAUNCHERS_DIR="$HOME/launchers"
SCRIPT_PATH="$LAUNCHERS_DIR/$LAUNCHER_SCRIPT"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Launcher script not found: $SCRIPT_PATH"
    exit 1
fi

# Kill any running games (handles both RetroArch and Eden)
pkill retroarch
pkill eden
sleep 1

# Launch the game via the launcher script
bash "$SCRIPT_PATH"