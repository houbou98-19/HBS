"""
HB System - Configuration Management
"""
import json
import os

CONFIG_DIR = os.path.expanduser("~/.hbs")
GAMES_FILE = os.path.join(CONFIG_DIR, "games.json")

PLATFORM_DIRS = {
    "NES": "nes",
    "SNES": "snes",
    "N64": "n64",
    "GBA": "gba",
    "GBC": "gbc",
    "NDS": "nds",
    "3DS": "3ds",
    "WII": "wii",
    "Switch": "switch"
}

def load_config():
    """Load config from config.json in script directory"""
    try:
        config_file = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_file) as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config.json: {e}")
        return {
            "version": "unknown",
            "roms_root": os.path.expanduser("~/roms"),
            "port": 5000,
            "display_name": "HB SYSTEM"
        }

CONFIG = load_config()
ROMS_ROOT = os.environ.get("HBS_ROMS_ROOT") or CONFIG.get("roms_root", os.path.expanduser("~/roms"))
PORT = CONFIG.get("port", 5000)

def get_version():
    """Get version from config"""
    return CONFIG.get("version", "unknown")

def ensure_config():
    """Create config directory and default games.json if needed"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(GAMES_FILE):
        with open(GAMES_FILE, "w") as f:
            json.dump([], f)

def load_games():
    """Load games from JSON file"""
    try:
        with open(GAMES_FILE) as f:
            return json.load(f)
    except:
        return []

def save_games(games):
    """Save games to JSON file"""
    with open(GAMES_FILE, "w") as f:
        json.dump(games, f, indent=2)