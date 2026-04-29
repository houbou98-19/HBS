"""
HB System - Games Routes
Game management, ROM listing, and launching
"""
import os
import json
from config import ROMS_ROOT, PLATFORM_DIRS, load_games, save_games, GAMES_FILE

def handle_get_games(params):
    """GET /api/games - Returns list of all games"""
    games = load_games()
    return {
        "games": games,
        "count": len(games)
    }

def handle_post_games(body):
    """POST /api/games - Add a new game"""
    # Validate required fields
    required = ["id", "name", "platform", "rom"]
    if not all(k in body for k in required):
        return {"error": "Missing required fields"}, 400
    
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
    
    # Save games
    save_games(games)
    
    return {"status": "added", "game": body["name"]}, 200

def handle_get_roms(params):
    """GET /api/roms?platform=PLATFORM - Returns list of ROMs for a platform"""
    platform = params.get("platform", [None])[0]
    
    if not platform:
        return {"error": "Missing platform parameter"}, 400
    
    if platform not in PLATFORM_DIRS:
        return {"error": "Unknown platform"}, 400
    
    rom_subdir = PLATFORM_DIRS[platform]
    rom_path = os.path.join(ROMS_ROOT, rom_subdir)
    
    try:
        files = [f for f in os.listdir(rom_path) 
                if os.path.isfile(os.path.join(rom_path, f))]
        files.sort()
        
        return {
            "platform": platform,
            "directory": rom_path,
            "files": files
        }, 200
    except FileNotFoundError:
        return {
            "platform": platform,
            "directory": rom_path,
            "files": []
        }, 200

def handle_launch_game(params):
    """GET /launch?id=GAME_ID - Launch a game"""
    game_id = params.get("id", [None])[0]
    
    if not game_id:
        return {"error": "Missing game id"}, 400
    
    games = load_games()
    game = next((g for g in games if g["id"] == game_id), None)
    
    if not game:
        return {"error": "Game not found"}, 404
    
    # TODO: Implement actual game launching via launcher.sh
    # For now, just return success
    return {"status": "launching", "game": game["name"]}, 200

def handle_menu(params):
    """GET /menu - Launch RetroArch menu"""
    import subprocess
    import os
    
    # From routes/games.py -> go up one level to hbs root
    launcher_path = os.path.join(os.path.dirname(__file__), "..", "launcher.sh")
    
    print(f"DEBUG: Launcher path: {launcher_path}")
    print(f"DEBUG: Exists: {os.path.exists(launcher_path)}")
    print(f"DEBUG: Absolute path: {os.path.abspath(launcher_path)}")
    
    try:
        subprocess.Popen([launcher_path, "menu"])
        return {"status": "launching", "app": "retroarch"}, 200
    except Exception as e:
        print(f"DEBUG: Error: {e}")
        return {"error": str(e)}, 500

ROUTES = {
    ("GET", "/api/games"): handle_get_games,
    ("POST", "/api/games"): handle_post_games,
    ("GET", "/api/roms"): handle_get_roms,
    ("GET", "/launch"): handle_launch_game,
    ("GET", "/menu"): handle_menu,
}