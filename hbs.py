"""
HB System - Retro Gaming Launcher
Main HTTP server with modular routes
"""
import json
import subprocess
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from routes import get_route_handler

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
    user_path = os.path.expanduser("~/.hbs/config.json")
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
    db_paths = [
        os.path.expanduser("~/.hbs/games_database.json"),  # User database
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
    
    # Default empty database
    print("Warning: No games database found, using empty database")
    return {"games": []}

# Load config at startup
CONFIG = load_config()
PORT = CONFIG.get("port", 5000)
DISPLAY_NAME = CONFIG.get("display_name", "HB SYSTEM")
VERSION = CONFIG.get("version", "unknown")

def launch_game(launcher_script):
    """Launch a game using the launcher script"""
    # Get launcher.sh from the binary's bundle directory
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller binary
        bundle_dir = sys._MEIPASS
    else:
        # Running as Python script
        bundle_dir = os.path.dirname(__file__)
    
    launcher_path = os.path.join(bundle_dir, "launcher.sh")
    
    try:
        print(f"Launching: {launcher_script}")
        print(f"Launcher path: {launcher_path}")
        
        if not os.path.exists(launcher_path):
            print(f"Error: launcher.sh not found at {launcher_path}")
            return False
        
        proc = subprocess.Popen(
            [launcher_path, launcher_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Process started with PID {proc.pid}")
        return True
    except Exception as e:
        print(f"Error launching game: {e}")
        return False

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
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        # Get route handler
        handler = get_route_handler("GET", path)
        
        if not handler:
            self.send_json(404, {"error": "Not found"})
            return
        
        try:
            result = handler(params)
            
            if isinstance(result, tuple):
                data, code = result
                self.send_json(code, data)
            else:
                self.send_json(200, result)
        except Exception as e:
            self.send_json(500, {"error": str(e)})
    
    def do_POST(self):
        """Handle POST requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Get route handler
        handler = get_route_handler("POST", path)
        
        if not handler:
            self.send_json(404, {"error": "Not found"})
            return
        
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            
            result = handler(body)
            
            if isinstance(result, tuple):
                data, code = result
                self.send_json(code, data)
            else:
                self.send_json(200, result)
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), HBSHandler)
    print(f"HB System v{VERSION} running on http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")