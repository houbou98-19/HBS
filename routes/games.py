"""
HB System - Games Routes
Game management and launching
"""
from datetime import datetime
from config import load_games_database, save_games, load_config
import sys

def log(msg):
    """Write to stderr so it shows in journalctl"""
    print(msg, file=sys.stderr, flush=True)

def handle_get_games(params):
    """GET /api/games - Returns list of all games"""
    log(f"[handle_get_games] called with params: {params}")
    games = load_games_database()
    log(f"[handle_get_games] loaded {len(games)} games")
    return {
        "games": games,
        "count": len(games)
    }

def handle_post_games(body):
    """POST /api/games - Add a new game"""
    required = ["id", "name", "launcher"]
    if not all(k in body for k in required):
        return {"error": "Missing required fields: id, name, launcher"}, 400
    
    games = load_games_database()
    
    if any(g["id"] == body["id"] for g in games):
        return {"error": "Game ID already exists"}, 400
    
    games.append({
        "id": body["id"],
        "name": body["name"],
        "launcher": body["launcher"],
        "playtime": 0,
        "last_played": None,
        "cover_filename": body.get("cover_filename", "")  # Just filename, not full path
    })
    
    save_games(games)
    
    return {"status": "added", "game": body["name"]}, 201

def handle_launch_game(params):
    """GET /launch?id=GAME_ID - Launch a game"""
    from hbs import launch_game
    
    log(f"[handle_launch_game] params type: {type(params)}")
    log(f"[handle_launch_game] params: {params}")
    
    game_id = params.get("id", [None])[0]
    
    log(f"[handle_launch_game] game_id: {game_id}")
    
    if not game_id:
        log("Error: No game ID provided")
        return {"error": "Missing game id"}, 400
    
    games = load_games_database()  # Now returns list
    game = next((g for g in games if g["id"] == game_id), None)
    
    if not game:
        log(f"Error: Game not found: {game_id}")
        return {"error": "Game not found"}, 404
    
    launcher_name = game.get("launcher")
    log(f"Launcher name: {launcher_name}")
    
    if not launcher_name:
        log("Error: No launcher configured")
        return {"error": "Invalid game data"}, 400
    
    if not launch_game(launcher_name):
        log(f"Error: launch_game() returned False")
        return {"error": "Failed to launch game"}, 500
    
    # Update last_played and playtime
    for g in games:
        if g["id"] == game_id:
            g["last_played"] = datetime.now().isoformat()
            g["playtime"] = g.get("playtime", 0) + 1
            break
    
    save_games(games)
    
    log(f"Successfully launched: {game['name']}")
    return {"status": "launching", "game": game["name"]}, 200

def handle_get_status(params):
    """GET /api/status - Returns HBS system status and version"""
    config = load_config()
    
    return {
        "status": "ok",
        "version": config.get("version", "unknown"),
        "hbs_name": config.get("display_name", "HB SYSTEM")
    }, 200

ROUTES = {
    ("GET", "/api/games"): handle_get_games,
    ("POST", "/api/games"): handle_post_games,
    ("GET", "/launch"): handle_launch_game,
    ("GET", "/api/status"): handle_get_status,
}