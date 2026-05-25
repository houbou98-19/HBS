"""
HB System - Games Routes
Game management and launching
"""
import os
import json
from datetime import datetime
from config import load_games, save_games, GAMES_FILE

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
    required = ["id", "name", "launcher"]
    if not all(k in body for k in required):
        return {"error": "Missing required fields: id, name, launcher"}, 400
    
    # Load existing games
    games = load_games()
    
    # Check if game ID already exists
    if any(g["id"] == body["id"] for g in games):
        return {"error": "Game ID already exists"}, 400
    
    # Add new game
    games.append({
        "id": body["id"],
        "name": body["name"],
        "launcher": body["launcher"],
        "playtime": 0,
        "last_played": None
    })
    
    # Save games
    save_games(games)
    
    return {"status": "added", "game": body["name"]}, 201

def handle_launch_game(params):
    """GET /launch?id=GAME_ID - Launch a game"""
    from hbs import launch_game
    from config import load_games, save_games
    from datetime import datetime
    
    game_id = params.get("id", [None])[0]
    
    if not game_id:
        return {"error": "Missing game id"}, 400
    
    games = load_games()
    game = next((g for g in games if g["id"] == game_id), None)
    
    if not game:
        return {"error": "Game not found"}, 404
    
    launcher_name = game.get("launcher")
    
    if not launcher_name:
        return {"error": "Invalid game data"}, 400
    
    if not launch_game(launcher_name):
        return {"error": "Failed to launch game"}, 500
    
    # Update last_played and playtime
    for g in games:
        if g["id"] == game_id:
            g["last_played"] = datetime.now().isoformat()
            g["playtime"] = g.get("playtime", 0) + 1
            break
    
    save_games(games)
    
    return {"status": "launching", "game": game["name"]}, 200

ROUTES = {
    ("GET", "/api/games"): handle_get_games,
    ("POST", "/api/games"): handle_post_games,
    ("GET", "/launch"): handle_launch_game,
}