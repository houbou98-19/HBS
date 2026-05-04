"""
HB System - Games Routes
Game management, ROM listing, and launching
"""
import os
import json
from datetime import datetime
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
    from hbs import launch_subprocess
    
    game_id = params.get("id", [None])[0]
    
    if not game_id:
        return {"error": "Missing game id"}, 400
    
    games = load_games()
    game = next((g for g in games if g["id"] == game_id), None)
    
    if not game:
        return {"error": "Game not found"}, 404
    
    # Platform to core mapping
    PLATFORM_CORES = {
        "NES": "nestopia_libretro.so",
        "SNES": "snes9x_libretro.so",
        "N64": "mupen64plus_next_libretro.so",
        "GBA": "mgba_libretro.so",
        "GBC": "mgba_libretro.so",
        "NDS": "desmume_libretro.so",
        "3DS": "citra_libretro.so",
        "WII": "dolphin_libretro.so",
        "Switch": "eden"
    }
    
    platform = game.get("platform")
    rom_path = game.get("rom")
    
    if not platform or not rom_path:
        return {"error": "Invalid game data"}, 400
    
    if platform not in PLATFORM_CORES:
        return {"error": f"Unsupported platform: {platform}"}, 400
    
    if not os.path.exists(rom_path):
        return {"error": f"ROM file not found: {rom_path}"}, 404
    
    core = PLATFORM_CORES[platform]
    
    try:
        launch_subprocess(core, rom_path)
        
        # Update last_played and playtime
        for g in games:
            if g["id"] == game_id:
                g["last_played"] = datetime.now().isoformat()
                g["playtime"] = g.get("playtime", 0) + 1
                break
        
        save_games(games)
        
        return {"status": "launching", "game": game["name"], "platform": platform}, 200
    except Exception as e:
        return {"error": f"Failed to launch: {str(e)}"}, 500

def handle_menu(params):
    """GET /menu - Launch RetroArch menu"""
    from hbs import launch_subprocess
    
    try:
        launch_subprocess("menu")
        return {"status": "launching", "app": "retroarch"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

ROUTES = {
    ("GET", "/api/games"): handle_get_games,
    ("POST", "/api/games"): handle_post_games,
    ("GET", "/api/roms"): handle_get_roms,
    ("GET", "/launch"): handle_launch_game,
    ("GET", "/menu"): handle_menu,
}