"""
HB System - Route Registration
Combines all routes from submodules
"""
from routes.system import ROUTES as SYSTEM_ROUTES
from routes.pages import ROUTES as PAGES_ROUTES
from routes.games import ROUTES as GAMES_ROUTES

# Combine all routes
ALL_ROUTES = {}
ALL_ROUTES.update(SYSTEM_ROUTES)
ALL_ROUTES.update(PAGES_ROUTES)
ALL_ROUTES.update(GAMES_ROUTES)

def get_route_handler(method, path):
    """Get handler for a given method and path"""
    return ALL_ROUTES.get((method, path))