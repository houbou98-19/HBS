"""
HB System - Games Routes
Game management and launching
"""
import os
import json
from datetime import datetime

def load_games_database():
    """Load games database (imported from hbs module)"""
    from hbs import load_games_database
    return load_games_database()

def save_games(games):
    """Save games to database file"""
    db_paths = [
        os.path.expanduser("~/.hbs/games_database.json"),
        os.path.join(os.path.dirname(__file__), "..", "games_database.json"),
    ]
    
    # Save to user database location first
    os.makedirs(os.path.expanduser("~/.hbs"), exist_ok=True)
    with open(db_paths[0], "w") as f:
        json.dump(games, f, indent=2)

def handle_get_games(params):
    """GET /api/games - Returns list of all games"""
    db = load_games_database()
    games = db.get("games", [])
    return {
        "games": games,
        "count": len(games)
    }

def handle_post_games(body):
    """POST /api/games - Add a new game"""
    required = ["id", "name", "launcher"]
    if not all(k in body for k in required):
        return {"error": "Missing required fields: id, name, launcher"}, 400
    
    db = load_games_database()
    games = db.get("games", [])
    
    if any(g["id"] == body["id"] for g in games):
        return {"error": "Game ID already exists"}, 400
    
    games.append({
        "id": body["id"],
        "name": body["name"],
        "launcher": body["launcher"],
        "playtime": 0,
        "last_played": None
    })
    
    save_games({"games": games})
    
    return {"status": "added", "game": body["name"]}, 201

def handle_launch_game(params):
    """GET /launch?id=GAME_ID - Launch a game"""
    from hbs import launch_game
    
    game_id = params.get("id", [None])[0]
    
    print(f"Launch request for game: {game_id}")
    
    if not game_id:
        print("Error: No game ID provided")
        return {"error": "Missing game id"}, 400
    
    db = load_games_database()
    games = db.get("games", [])
    game = next((g for g in games if g["id"] == game_id), None)
    
    if not game:
        print(f"Error: Game not found: {game_id}")
        return {"error": "Game not found"}, 404
    
    launcher_name = game.get("launcher")
    print(f"Launcher name: {launcher_name}")
    
    if not launcher_name:
        print("Error: No launcher configured")
        return {"error": "Invalid game data"}, 400
    
    if not launch_game(launcher_name):
        print(f"Error: launch_game() returned False")
        return {"error": "Failed to launch game"}, 500
    
    # Update last_played and playtime
    for g in games:
        if g["id"] == game_id:
            g["last_played"] = datetime.now().isoformat()
            g["playtime"] = g.get("playtime", 0) + 1
            break
    
    save_games({"games": games})
    
    print(f"Successfully launched: {game['name']}")
    return {"status": "launching", "game": game["name"]}, 200

def handle_get_status(params):
    """GET /api/status - Returns HBS system status and version"""
    from hbs import CONFIG
    
    return {
        "status": "ok",
        "version": CONFIG.get("version", "unknown"),
        "hbs_name": CONFIG.get("display_name", "HB SYSTEM")
    }, 200

ROUTES = {
    ("GET", "/api/games"): handle_get_games,
    ("POST", "/api/games"): handle_post_games,
    ("GET", "/launch"): handle_launch_game,
    ("GET", "/api/status"): handle_get_status,
}