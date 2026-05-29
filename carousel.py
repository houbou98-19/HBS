"""
HB System - Carousel Menu UI
Pyglet-based game carousel launcher with controller support
"""
import pyglet
import requests
import time
import json
import os
import sys

def load_carousel_config():
    """Load carousel configuration from file"""
    config_paths = [
        os.path.expanduser("~/.hbs/carousel_config.json"),  # Linux
        os.path.expanduser("~/AppData/Roaming/HBS/carousel_config.json"),  # Windows
        os.path.join(os.path.dirname(__file__), "carousel_config.json"),  # Local
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    print(f"✓ Loaded config from {config_path}")
                    return config
            except Exception as e:
                print(f"Warning: Could not load {config_path}: {e}")
    
    # Default fallback
    print("Warning: No carousel config found, using defaults")
    return {
        "api_url": "http://localhost:5000",
        "steamgriddb_api_key": "",
        "covers_dir": os.path.expanduser("~/.hbs/covers")
    }

def load_app_config():
    """Load HBS app configuration for version info"""
    try:
        config_file = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_file) as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config.json: {e}")
        return {"version": "unknown"}
    
def get_hbs_version(api_url):
    """Fetch HBS version from API"""
    try:
        response = requests.get(f"{api_url}/api/status", timeout=5)
        data = response.json()
        return data.get("version", "unknown")
    except Exception as e:
        print(f"Warning: Could not fetch version from API: {e}")
        return "unknown"

def load_games(api_url):
    """Load games from HBS API"""
    try:
        response = requests.get(f"{api_url}/api/games", timeout=5)
        data = response.json()
        return data.get("games", [])
    except Exception as e:
        print(f"Error loading games from {api_url}: {e}")
        return []

def fetch_game_covers(api_url, api_key, covers_dir):
    """Fetch and cache game cover images from SteamGridDB"""
    if not api_key:
        print("No SteamGridDB API key configured, skipping cover fetch")
        return
    
    os.makedirs(covers_dir, exist_ok=True)
    games = load_games(api_url)
    
    for game in games:
        game_id = game['id']
        cover_path = os.path.join(covers_dir, f"{game_id}.png")
        
        # Skip if already cached
        if os.path.exists(cover_path):
            game['cover_path'] = cover_path
            continue
        
        print(f"Fetching cover for {game['name']}...")
        
        try:
            # Search for game on SteamGridDB
            search_response = requests.get(
                f"https://www.steamgriddb.com/api/v2/search/autocomplete/{game['name'].replace(' ', '%20')}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5
            )
            
            if not search_response.ok:
                print(f"  ✗ Search failed for {game['name']}")
                continue
            
            search_data = search_response.json()
            if not search_data.get('data'):
                print(f"  ✗ No results for {game['name']}")
                continue
            
            steamgrid_id = search_data['data'][0]['id']
            
            # Fetch logo/cover
            logo_response = requests.get(
                f"https://www.steamgriddb.com/api/v2/logos/game/{steamgrid_id}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=5
            )
            
            if not logo_response.ok or not logo_response.json().get('data'):
                print(f"  ✗ No cover found for {game['name']}")
                continue
            
            image_url = logo_response.json()['data'][0]['url']
            
            # Download and cache image
            image_response = requests.get(image_url, timeout=10)
            if image_response.ok:
                with open(cover_path, 'wb') as f:
                    f.write(image_response.content)
                game['cover_path'] = cover_path
                print(f"  ✓ Downloaded cover for {game['name']}")
            else:
                print(f"  ✗ Failed to download {game['name']}")
        
        except Exception as e:
            print(f"  ✗ Error fetching {game['name']}: {e}")

class CarouselMenu(pyglet.window.Window):
    """Main carousel menu window"""
    
    def __init__(self, carousel_config):
        # Get screen resolution from environment or use fallback
        width = int(os.environ.get('SCREEN_WIDTH', 1920))
        height = int(os.environ.get('SCREEN_HEIGHT', 1080))
        
        super().__init__(width, height, fullscreen=False)
        self.set_caption("HB SYSTEM")
        self.set_location(0, 0)
        
        # Store configs
        self.carousel_config = carousel_config
        self.api_url = carousel_config.get('api_url', 'http://localhost:5000')
        self.covers_dir = os.path.expanduser(carousel_config.get('covers_dir', '~/.hbs/covers'))
        
        self.version = get_hbs_version(self.api_url)
        
        # Fetch covers if API key is configured
        api_key = carousel_config.get('steamgriddb_api_key', '')
        if api_key:
            print("Fetching game covers from SteamGridDB...")
            fetch_game_covers(self.api_url, api_key, self.covers_dir)
        
        self.games = load_games(self.api_url)
        self.current_index = 0
        self.last_launch_time = 0
        self.launch_status = ""
        self.status_time = 0
        
        # Animation state
        self.animation_time = 0
        self.animation_duration = 0.3  # seconds
        self.prev_index = 0
        self.y_offset = 100
        
        print(f"HB SYSTEM v{self.version}")
        print(f"API URL: {self.api_url}")
        print(f"Loaded {len(self.games)} games")
        print(f"Resolution: {self.width}x{self.height}")
    
    def on_draw(self):
        """Render carousel UI"""
        pyglet.gl.glClearColor(0.04, 0.02, 0.1, 1.0)
        self.clear()
        
        self.draw_title()
        self.draw_cover()
        self.draw_carousel()
        self.draw_version()
        self.draw_status()
    
    def draw_title(self):
        """Draw HB SYSTEM title"""
        title = pyglet.text.Label(
            "HB SYSTEM",
            font_name="Press Start 2P",
            font_size=150,
            x=self.width // 2,
            y=self.height - 250 - self.y_offset,
            anchor_x='center',
            color=(0, 255, 136, 255)
        )
        title.draw()
        
        subtitle = pyglet.text.Label(
            "PERSONAL ARCADE",
            font_name="Press Start 2P",
            font_size=64,
            x=self.width // 2,
            y=self.height - 350 - self.y_offset,
            anchor_x='center',
            color=(0, 170, 255, 255)
        )
        subtitle.draw()
    
    def draw_carousel(self):
        """Draw game carousel with infinite scrolling"""
        center_x = self.width // 2
        center_y = self.height // 2 - 600 - self.y_offset
        spacing = 800
        
        num_games = len(self.games)
        
        for i, game in enumerate(self.games):
            offset = (i - self.current_index)
            x = center_x + (offset * spacing)
            
            if -800 < x < self.width + 800:
                is_active = (i == self.current_index)
                self.draw_card(game, x, center_y, is_active)
            
            # Draw wraparound cards on left and right edges
            # Left side wraparound
            offset_left = (i - self.current_index - num_games)
            x_left = center_x + (offset_left * spacing)
            if -800 < x_left < self.width + 800:
                self.draw_card(game, x_left, center_y, False)
            
            # Right side wraparound
            offset_right = (i - self.current_index + num_games)
            x_right = center_x + (offset_right * spacing)
            if -800 < x_right < self.width + 800:
                self.draw_card(game, x_right, center_y, False)
    
    def get_animation_alpha(self):
        """Get alpha value for text animation (0-255)"""
        if self.animation_time >= self.animation_duration:
            return 255
        progress = self.animation_time / self.animation_duration
        return int(255 * progress)
    
    def draw_cover(self):
        """Draw large cover image for active game in center of screen"""
        import math
        
        if not self.games:
            return
        
        game = self.games[self.current_index]
        
        if not game.get('cover_path') or not os.path.exists(game['cover_path']):
            return
        
        try:
            if not hasattr(self, '_cover_images'):
                self._cover_images = {}
            
            cover_key = game['id']
            if cover_key not in self._cover_images:
                self._cover_images[cover_key] = pyglet.image.load(game['cover_path'])
            
            cover_image = self._cover_images[cover_key]
            
            # Scale to fit center of screen (adjust size as needed)
            max_height = 1500
            max_width = 1200
            aspect = cover_image.width / cover_image.height
            
            if aspect > max_width / max_height:
                display_width = max_width
                display_height = int(max_width / aspect)
            else:
                display_height = max_height
                display_width = int(max_height * aspect)
            
            bob_amount = math.sin(time.time() * 2) * 30
            
            sprite = pyglet.sprite.Sprite(cover_image)
            sprite.x = (self.width - display_width) // 2
            sprite.y = (self.height - display_height) // 2 + 100 - self.y_offset + bob_amount
            sprite.scale_x = display_width / cover_image.width
            sprite.scale_y = display_height / cover_image.height
            sprite.draw()
        except Exception as e:
            print(f"Error drawing cover: {e}")
    
    def draw_card(self, game, x, y, is_active):
        """Draw a single game card"""
        name = game['name']
        if len(name) > 12:
            parts = name.split()
            line1 = parts[0] if parts else ""
            line2 = " ".join(parts[1:]) if len(parts) > 1 else ""
        else:
            line1 = name
            line2 = ""
        
        color = (0, 170, 255, 255) if is_active else (0, 255, 136, 100)
        
        # Apply animation alpha to active card text
        if is_active:
            anim_alpha = self.get_animation_alpha()
            text_color = (color[0], color[1], color[2], anim_alpha)
        else:
            text_color = color
        
        if is_active:
            border = pyglet.text.Label(
                "┌──────────────┐",
                font_name="Arial",
                font_size=24,
                x=x,
                y=y + 70,
                anchor_x='center',
                color=color
            )
            border.draw()
        
        card_label = pyglet.text.Label(
            line1,
            font_name="Press Start 2P",
            font_size=32,
            x=x,
            y=y + 30,
            anchor_x='center',
            anchor_y='center',
            color=text_color
        )
        card_label.draw()
        
        if line2:
            card_label2 = pyglet.text.Label(
                line2,
                font_name="Press Start 2P",
                font_size=24,
                x=x,
                y=y - 10,
                anchor_x='center',
                anchor_y='center',
                color=text_color
            )
            card_label2.draw()
        
        playtime_label = pyglet.text.Label(
            f"{game.get('playtime', 0)}h",
            font_name="Press Start 2P",
            font_size=12,
            x=x,
            y=y - 60,
            anchor_x='center',
            color=(0, 255, 136, 150)
        )
        playtime_label.draw()
        
        if is_active:
            border2 = pyglet.text.Label(
                "└──────────────┘",
                font_name="Arial",
                font_size=24,
                x=x,
                y=y - 90,
                anchor_x='center',
                color=color
            )
            border2.draw()
    
    def draw_version(self):
        """Draw version in bottom right"""
        version_label = pyglet.text.Label(
            f"v{self.version}",
            font_name="Press Start 2P",
            font_size=50,
            x=self.width - 30,
            y=30,
            anchor_x='right',
            anchor_y='bottom',
            color=(100, 100, 100, 150)
        )
        version_label.draw()
    
    def draw_status(self):
        """Draw launch status message"""
        if self.launch_status and time.time() - self.status_time < 3:
            status_label = pyglet.text.Label(
                self.launch_status,
                font_name="Press Start 2P",
                font_size=16,
                x=self.width // 2,
                y=self.height // 2 + 250,
                anchor_x='center',
                color=(0, 255, 136, 255)
            )
            status_label.draw()
    
    def on_key_press(self, symbol, modifiers):
        """Handle keyboard input"""
        if symbol == pyglet.window.key.LEFT:
            self.prev_index = self.current_index
            self.current_index = (self.current_index - 1) % len(self.games)
            self.animation_time = 0
        elif symbol == pyglet.window.key.RIGHT:
            self.prev_index = self.current_index
            self.current_index = (self.current_index + 1) % len(self.games)
            self.animation_time = 0
        elif symbol == pyglet.window.key.RETURN or symbol == pyglet.window.key.SPACE:
            self.launch_game()
        elif symbol == pyglet.window.key.ESCAPE:
            return True
    
    def on_joybutton_press(self, joystick, button):
        """Handle controller button input"""
        if button == 0:
            self.launch_game()
        elif button == 6:
            pyglet.app.exit()
        return True
    
    def on_joyaxis_motion(self, joystick, axis, value):
        """Handle controller stick/dpad input"""
        if axis == 0:
            if value < -0.5:
                self.prev_index = self.current_index
                self.current_index = (self.current_index - 1) % len(self.games)
                self.animation_time = 0
            elif value > 0.5:
                self.prev_index = self.current_index
                self.current_index = (self.current_index + 1) % len(self.games)
                self.animation_time = 0
    
    def launch_game(self):
        """Launch selected game via API"""
        if not self.games:
            return
        
        current_time = time.time()
        if current_time - self.last_launch_time < 2:
            self.launch_status = "Please wait..."
            self.status_time = current_time
            return
        
        self.last_launch_time = current_time
        game = self.games[self.current_index]
        game_id = game['id']
        
        self.launch_status = f"Launching {game['name']}..."
        self.status_time = current_time

        try:
            response = requests.get(f"{self.api_url}/launch?id={game_id}")
            result = response.json()
            if result.get('status') == 'launching':
                self.launch_status = f"Started {game['name']}!"
        except Exception as e:
            print(f"Error launching game: {e}")
            self.launch_status = f"Error: {str(e)}"
        
        self.status_time = time.time()

def update(dt):
    """Update animation state"""
    menu.animation_time += dt
    if menu.animation_time > menu.animation_duration:
        menu.animation_time = menu.animation_duration

def main():
    """Start carousel menu"""
    global menu
    carousel_config = load_carousel_config()
    menu = CarouselMenu(carousel_config)
    pyglet.clock.schedule(update)
    pyglet.app.run()

if __name__ == "__main__":
    main()