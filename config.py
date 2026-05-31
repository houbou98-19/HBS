"""
HB System - Configuration Management
"""
import json
import os

CONFIG_DIR = os.path.expanduser("~/.hbs")

def load_config():
    """Load HBS configuration with bundled defaults"""
    config = {}
    
    # Load bundled config first (for defaults like version)
    bundled_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(bundled_path):
        try:
            with open(bundled_path) as f:
                config = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load bundled config: {e}")
    
    # Override with user config if it exists
    user_path = os.path.join(CONFIG_DIR, "config.json")
    if os.path.exists(user_path):
        try:
            with open(user_path) as f:
                user_config = json.load(f)
                config.update(user_config)
                print(f"✓ Loaded user config from {user_path}")
        except Exception as e:
            print(f"Warning: Could not load user config: {e}")
    
    return config

def load_games_database():
    """Load games database from local file or bundled template"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    db_paths = [
        os.path.join(CONFIG_DIR, "games_database.json"),
        os.path.join(os.path.dirname(__file__), "games_database.json"),
        os.path.join(os.path.dirname(__file__), "games_database.json.template"),
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            try:
                with open(db_path) as f:
                    return json.load(f)  # Returns the list directly
            except Exception as e:
                print(f"Warning: Could not load {db_path}: {e}")
    
    # Default empty list
    print("Warning: No games database found, using empty database")
    return []

def save_games(games):
    """Save games to database file"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    db_path = os.path.join(CONFIG_DIR, "games_database.json")
    
    try:
        with open(db_path, "w") as f:
            json.dump(games, f, indent=2)  # Save as list directly
    except Exception as e:
        print(f"Error: Could not save games database: {e}")

def load_carousel_config():
    """Load carousel configuration from file"""
    config_paths = [
        os.path.join(CONFIG_DIR, "carousel_config.json"),
        os.path.join(os.path.dirname(__file__), "carousel_config.json"),
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    print(f"✓ Loaded config from {config_path}")
                    return config
            except Exception as e:
                print(f"Warning: Could not load {config_path}: {e}")
    
    # Default fallback
    print("Warning: No carousel config found, using defaults")
    return {
        "api_url": "http://localhost:5000",
        "steamgriddb_api_key": "",
        "covers_dir": os.path.join(CONFIG_DIR, "covers")
    }

def get_version():
    """Get version from config"""
    config = load_config()
    return config.get("version", "unknown")