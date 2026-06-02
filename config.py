"""
HB System - Configuration Management
"""
import logging
import json
import os

def get_config_dir():
    """Get platform-appropriate config directory with fallback"""
    # Try Windows path first, then Linux
    windows_path = os.path.expanduser("~/AppData/Roaming/HBS")
    linux_path = os.path.expanduser("~/.hbs")
    
    # Return whichever exists, or default based on OS
    if os.path.exists(windows_path):
        return windows_path
    elif os.path.exists(linux_path):
        return linux_path
    else:
        # Default: Windows on Windows, Linux on others
        return windows_path if os.name == 'nt' else linux_path

CONFIG_DIR = get_config_dir()

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
    config_dir = get_config_dir()
    user_path = os.path.join(config_dir, "config.json")
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
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    
    db_paths = [
        os.path.join(config_dir, "games_database.json"),  # User database (platform-aware)
        os.path.join(os.path.dirname(__file__), "games_database.json"),  # Local file
        os.path.join(os.path.dirname(__file__), "games_database.json.template"),  # Bundled fallback
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            try:
                with open(db_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load {db_path}: {e}")
    
    # Default empty list
    print("Warning: No games database found, using empty database")
    return []

def save_games(games):
    """Save games to database file"""
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    db_path = os.path.join(config_dir, "games_database.json")
    
    try:
        with open(db_path, "w") as f:
            json.dump(games, f, indent=2)
    except Exception as e:
        print(f"Error: Could not save games database: {e}")

def load_carousel_config():
    """Load carousel configuration from file"""
    config_dir = get_config_dir()
    
    config_paths = [
        os.path.join(config_dir, "carousel_config.json"),  # User location (platform-aware)
        os.path.join(os.path.dirname(__file__), "carousel_config.json"),  # Bundled
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
    
    # Default fallback with platform-aware covers directory
    covers_dir = os.path.join(config_dir, "covers")
    
    print("Warning: No carousel config found, using defaults")
    return {
        "api_url": "http://localhost:5000",
        "steamgriddb_api_key": "",
        "covers_dir": covers_dir
    }

def get_version():
    """Get version from config"""
    config = load_config()
    return config.get("version", "unknown")

def setup_logging(app_name="hbs"):
    """Setup logging to file in config directory"""
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    
    log_file = os.path.join(config_dir, f"{app_name}.log")
    
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'
    )
    
    return logging.getLogger(app_name)