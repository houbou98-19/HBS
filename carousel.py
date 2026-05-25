"""
HB System - Carousel Menu UI
Pyglet-based game carousel launcher with controller support
"""
import pyglet
import requests
import time
import json
import os

def load_config():
    """Load configuration and version"""
    try:
        config_file = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_file) as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config.json: {e}")
        return {"version": "unknown"}

def load_games():
    """Load games from HBS API"""
    try:
        response = requests.get("http://localhost:5000/api/games")
        data = response.json()
        return data.get("games", [])
    except Exception as e:
        print(f"Error loading games: {e}")
        return []

class CarouselMenu(pyglet.window.Window):
    """Main carousel menu window"""
    
    def __init__(self):
        # Get display size for fullscreen
        from pyglet import canvas
        display = canvas.get_display()
        screen = display.get_screens()[0]
        
        super().__init__(screen.width, screen.height, fullscreen=True)
        self.set_caption("HB SYSTEM")
        
        app_config = load_config()
        self.version = app_config.get("version", "unknown")
        self.games = load_games()
        self.current_index = 0
        self.last_launch_time = 0
        self.launch_status = ""
        self.status_time = 0
        
        print(f"HB SYSTEM v{self.version}")
        print(f"Loaded {len(self.games)} games")
        print(f"Resolution: {self.width}x{self.height}")
    
    def on_draw(self):
        """Render carousel UI"""
        pyglet.gl.glClearColor(0.04, 0.02, 0.1, 1.0)
        self.clear()
        
        self.draw_title()
        self.draw_carousel()
        self.draw_version()
        self.draw_status()
    
    def draw_title(self):
        """Draw HB SYSTEM title"""
        title = pyglet.text.Label(
            "HB SYSTEM",
            font_name="Press Start 2P",
            font_size=60,
            x=self.width // 2,
            y=self.height - 120,
            anchor_x='center',
            color=(0, 255, 136, 255)
        )
        title.draw()
        
        subtitle = pyglet.text.Label(
            "PERSONAL ARCADE",
            font_name="Press Start 2P",
            font_size=24,
            x=self.width // 2,
            y=self.height - 200,
            anchor_x='center',
            color=(0, 170, 255, 255)
        )
        subtitle.draw()
    
    def draw_carousel(self):
        """Draw game carousel"""
        center_x = self.width // 2
        center_y = self.height // 2
        spacing = 220
        
        for i, game in enumerate(self.games):
            offset = (i - self.current_index)
            x = center_x + (offset * spacing)
            
            if -800 < x < self.width + 800:
                is_active = (i == self.current_index)
                self.draw_card(game, x, center_y, is_active)
    
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
        
        if is_active:
            border = pyglet.text.Label(
                "┌──────────────┐",
                font_name="Press Start 2P",
                font_size=16,
                x=x,
                y=y + 70,
                anchor_x='center',
                color=color
            )
            border.draw()
        
        card_label = pyglet.text.Label(
            line1,
            font_name="Press Start 2P",
            font_size=16,
            x=x,
            y=y + 30,
            anchor_x='center',
            anchor_y='center',
            color=color
        )
        card_label.draw()
        
        if line2:
            card_label2 = pyglet.text.Label(
                line2,
                font_name="Press Start 2P",
                font_size=14,
                x=x,
                y=y - 10,
                anchor_x='center',
                anchor_y='center',
                color=color
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
                font_name="Press Start 2P",
                font_size=16,
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
            font_size=12,
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
    
    def draw_instructions(self):
        """Draw control instructions"""
        instructions = pyglet.text.Label(
            "DPAD LEFT/RIGHT to navigate | A to launch | MENU to exit",
            font_name="Press Start 2P",
            font_size=12,
            x=self.width // 2,
            y=60,
            anchor_x='center',
            color=(100, 100, 100, 150)
        )
        instructions.draw()
    
    def on_key_press(self, symbol, modifiers):
        """Handle keyboard input"""
        if symbol == pyglet.window.key.LEFT:
            self.current_index = (self.current_index - 1) % len(self.games)
        elif symbol == pyglet.window.key.RIGHT:
            self.current_index = (self.current_index + 1) % len(self.games)
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
                self.current_index = (self.current_index - 1) % len(self.games)
            elif value > 0.5:
                self.current_index = (self.current_index + 1) % len(self.games)
    
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
            response = requests.get(f"http://localhost:5000/launch?id={game_id}")
            result = response.json()
            if result.get('status') == 'launching':
                self.launch_status = f"Started {game['name']}!"
        except Exception as e:
            print(f"Error launching game: {e}")
            self.launch_status = f"Error: {str(e)}"
        
        self.status_time = time.time()

def main():
    """Start carousel menu"""
    menu = CarouselMenu()
    pyglet.app.run()

if __name__ == "__main__":
    main()