"""
HB System - Route Registration
"""
from routes.games import ROUTES as GAMES_ROUTES

# Combine all routes
ALL_ROUTES = GAMES_ROUTES

def get_route_handler(method, path):
    """Get handler for a given method and path"""
    return ALL_ROUTES.get((method, path))