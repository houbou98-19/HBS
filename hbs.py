#!/usr/bin/env python3
"""
HB System - Retro Gaming Launcher
Main HTTP server with core endpoints
"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configuration
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
ROMS_ROOT = CONFIG.get("roms_root", os.path.expanduser("~/roms"))
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

class HBSHandler(BaseHTTPRequestHandler):
    """HTTP request handler for HBS"""
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def send_json(self, code, data):
        """Send JSON response"""
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    
    def send_html(self, code, filepath):
        """Send HTML file"""
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(code)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_json(404, {"error": "File not found"})
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        # Root - splash screen
        if path == "/" or path == "/splash":
            splash_path = os.path.join(os.path.dirname(__file__), "splash.html")
            self.send_html(200, splash_path)
        
        # Status endpoint
        elif path == "/api/status":
            self.send_json(200, {
                "status": "online",
                "version": get_version(),
                "games_count": len(load_games())
            })
        
        # Add game page
        elif path == "/add":
            add_path = os.path.join(os.path.dirname(__file__), "add.html")
            self.send_html(200, add_path)

        elif path == "/api/games":
            games = load_games()
            self.send_json(200, {
                "games": games,
                "count": len(games)
            })

        elif path == "/api/roms":
            platform = params.get("platform", [None])[0]
            if not platform:
                self.send_json(400, {"error": "Missing platform parameter"})
                return
            
            if platform not in PLATFORM_DIRS:
                self.send_json(400, {"error": "Unknown platform"})
                return
            
            rom_subdir = PLATFORM_DIRS[platform]
            rom_path = os.path.join(ROMS_ROOT, rom_subdir)
            
            try:
                files = [f for f in os.listdir(rom_path) 
                        if os.path.isfile(os.path.join(rom_path, f))]
                files.sort()
                
                self.send_json(200, {
                    "platform": platform,
                    "directory": rom_path,
                    "files": files
                })
            except FileNotFoundError:
                self.send_json(200, {
                    "platform": platform,
                    "directory": rom_path,
                    "files": []
                })
        
        else:
            self.send_json(404, {"error": "Not found"})
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == "/api/games":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length))
                
                # Validate required fields
                required = ["id", "name", "platform", "rom"]
                if not all(k in body for k in required):
                    self.send_json(400, {"error": "Missing required fields"})
                    return
                
                # Load existing games
                games = load_games()
                
                # Remove if game ID already exists
                games = [g for g in games if g.get("id") != body.get("id")]
                
                # Add new game
                games.append({
                    "id": body["id"],
                    "name": body["name"],
                    "platform": body["platform"],
                    "rom": body["rom"],
                    "playtime": 0,
                    "last_played": None
                })
                
                # Save games.json
                with open(GAMES_FILE, "w") as f:
                    json.dump(games, f, indent=2)
                
                self.send_json(200, {"status": "added", "game": body["name"]})
            except Exception as e:
                self.send_json(400, {"error": str(e)})
        else:
            self.send_json(404, {"error": "Not found"})

if __name__ == "__main__":
    ensure_config()
    server = HTTPServer(("0.0.0.0", PORT), HBSHandler)
    print(f"HB System running on http://localhost:{PORT}")
    print(f"Config directory: {CONFIG_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")