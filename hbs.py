#!/usr/bin/env python3
"""
HB System - Retro Gaming Launcher
Main HTTP server with core endpoints
"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Configuration
CONFIG_DIR = os.path.expanduser("~/.hbs")
GAMES_FILE = os.path.join(CONFIG_DIR, "games.json")
PORT = 5000

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
        
        # Root - splash screen
        if path == "/" or path == "/splash":
            splash_path = os.path.join(os.path.dirname(__file__), "splash.html")
            self.send_html(200, splash_path)
        
        # Status endpoint
        elif path == "/api/status":
            self.send_json(200, {
                "status": "online",
                "version": "1.0.0",
                "games_count": len(load_games())
            })
        
        # Add game page
        elif path == "/add":
            add_path = os.path.join(os.path.dirname(__file__), "add.html")
            self.send_html(200, add_path)
        
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