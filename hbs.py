"""
HB System - Retro Gaming Launcher
Main HTTP server with modular routes
"""
import json
import subprocess
import os
import stat
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from routes import get_route_handler
from config import load_config, load_games_database

def launch_game(launcher_script):
    """Launch a game using the launcher script"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    launcher_path = os.path.join(script_dir, "launcher.sh")
    
    try:
        print(f"Launching: {launcher_script}")
        print(f"Launcher path: {launcher_path}")
        
        if not os.path.exists(launcher_path):
            print(f"Error: launcher.sh not found at {launcher_path}")
            return False
        
        # Ensure launcher.sh is executable
        st = os.stat(launcher_path)
        os.chmod(launcher_path, st.st_mode | stat.S_IEXEC)
        
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

# Load config at startup
CONFIG = load_config()
PORT = CONFIG.get("port", 5000)
DISPLAY_NAME = CONFIG.get("display_name", "HB SYSTEM")
VERSION = CONFIG.get("version", "unknown")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), HBSHandler)
    print(f"HB System v{VERSION} running on http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")