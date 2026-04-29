"""
HB System - System Routes
Status and health check endpoints
"""
from config import get_version, load_games

def handle_status(params):
    """GET /api/status - Returns system status"""
    return {
        "status": "online",
        "version": get_version(),
        "games_count": len(load_games())
    }

ROUTES = {
    ("GET", "/api/status"): handle_status,
}