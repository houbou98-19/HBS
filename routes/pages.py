"""
HB System - Page Routes
HTML page serving endpoints
"""
import os

def handle_splash(params):
    """GET / or /splash - Returns splash screen"""
    splash_path = os.path.join(os.path.dirname(__file__), "..", "splash.html")
    with open(splash_path, "rb") as f:
        return f.read()

def handle_add(params):
    """GET /add - Returns add game page"""
    add_path = os.path.join(os.path.dirname(__file__), "..", "add.html")
    with open(add_path, "rb") as f:
        return f.read()

ROUTES = {
    ("GET", "/"): handle_splash,
    ("GET", "/splash"): handle_splash,
    ("GET", "/add"): handle_add,
}