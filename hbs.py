"""
HB System - Retro Gaming Launcher
Main HTTP server with modular routes
"""
import json
import subprocess
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from config import ensure_config, PORT
from routes import get_route_handler

def launch_game(launcher_script):
    """Launch a game using the launcher script"""
    launcher_path = os.path.join(os.path.dirname(__file__), "launcher.sh")
    try:
        subprocess.Popen([launcher_path, launcher_script])
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
    ensure_config()
    server = HTTPServer(("0.0.0.0", PORT), HBSHandler)
    print(f"HB System running on http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")