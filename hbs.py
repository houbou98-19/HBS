#!/usr/bin/env python3
"""
HB System - Retro Gaming Launcher
Main HTTP server with modular routes
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from config import ensure_config, PORT
from routes import get_route_handler

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
    
    def send_html(self, code, content):
        """Send HTML response"""
        if isinstance(content, str):
            content = content.encode()
        
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)
    
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
            
            # Handle different response types
            if isinstance(result, tuple):
                # (data, code) tuple
                data, code = result
                if isinstance(data, bytes):
                    self.send_html(code, data)
                else:
                    self.send_json(code, data)
            elif isinstance(result, bytes):
                # Raw HTML bytes
                self.send_html(200, result)
            else:
                # JSON response
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
            # Parse request body
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            
            result = handler(body)
            
            # Handle response
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