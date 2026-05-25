"""
HB System - Configuration Management
"""
import json
import os

CONFIG_DIR = os.path.expanduser("~/.hbs")
GAMES_FILE = os.path.join(CONFIG_DIR, "games_database.json")

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
            "port": 5000,
            "display_name": "HB SYSTEM"
        }

CONFIG = load_config()
PORT = CONFIG.get("port", 5000)

def get_version():
    """Get version from config"""
    return CONFIG.get("version", "unknown")

def ensure_config():
    """Create config directory if needed"""
    os.makedirs(CONFIG_DIR, exist_ok=True)

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