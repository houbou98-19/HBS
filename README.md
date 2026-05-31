# HBS - Home Brew System
## Retro Gaming Launcher with Arcade Carousel UI

A self-hosted, retro gaming arcade system with a **Pyglet-based carousel menu**, **HTTP API backend**, and support for multiple emulators.

## ✨ Features

- 🎮 **Multi-platform emulation** - NES, SNES, N64, GBA, GBC, NDS, 3DS, Wii, Switch
- 🎡 **Arcade carousel UI** - Retro-style menu with game covers, animations, and Press Start 2P font
- 🕹️ **Controller support** - Full gamepad/joystick integration for navigation and launching
- 🖼️ **SteamGridDB integration** - Automatic game cover art fetching and caching
- 📊 **Playtime tracking** - Track hours played and last played timestamp per game
- 🌐 **REST API** - Complete HTTP API for game management and launching
- 🚀 **Automated deployment** - GitHub Actions CI/CD pipeline with one-command releases
- 📦 **Cross-platform** - Linux binaries with systemd service management

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Carousel Menu (Pyglet)            │
│  - Game selection with cover art            │
│  - Controller input handling                │
│  - HTTP API calls to backend                │
└──────────────┬──────────────────────────────┘
               │ HTTP REST API
┌──────────────▼──────────────────────────────┐
│         HBS Backend (Python HTTP)           │
│  - Game database management                 │
│  - Game launching via launcher scripts      │
│  - Playtime tracking                        │
│  - System status & versioning               │
└──────────────┬──────────────────────────────┘
               │ Subprocess
┌──────────────▼─────────────────────────────────────────────────┐
│        Game Launchers (Bash Scripts)                           │
│  - Kill previous processes                                     │
│  - Launch games via Steam/RetroArch (for controller support)   │
│  - Handle display & authorization                              │
└────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Requirements

- **Ubuntu 20.04+** (tested on 22.04 LTS)
- **RetroArch** - Multi-emulator frontend
- **Eden** - Switch Emulator
- **dbus-x11** - D-Bus utilities
- **Python 3.8+** - Runtime for development
- ROMs of games you own

### Installation

```bash
cd ~/hbs
wget https://github.com/houbou98-19/hbs/releases/download/4.1.9/hbs-4.1.9.tar.gz
tar -xzf hbs-4.1.9.tar.gz
cd hbs-pkg
sudo bash install.sh
```

### Setup

1. **Configure Carousel** (optional)
   ```bash
   nano ~/.hbs/carousel_config.json
   ```
   ```json
   {
     "api_url": "http://localhost:5000",
     "steamgriddb_api_key": "YOUR_API_KEY",
     "covers_dir": "~/.hbs/covers"
   }
   ```
   Get your API key at https://www.steamgriddb.com/profile/preferences

2. **Add Games** - Games are stored in `~/.hbs/games_database.json`. Format:
   ```json
   {
     "games": [
       {
         "id": "pokemon-emerald",
         "name": "Pokemon Emerald",
         "platform": "GBA",
         "launcher": "pokemon-emerald.sh",
         "playtime": 0,
         "last_played": null,
         "cover_path": "~/.hbs/covers/pokemon-emerald.png"
       }
     ]
   }
   ```

3. **Create Launcher Scripts** - Each game needs a launcher in `~/launchers/`:
   ```bash
   #!/bin/bash
   steam -applaunch 1118310 -L mgba_libretro.so /mnt/hbs-roms/gba/pokemon-emerald.gba
   ```

4. **Start Services**
   ```bash
   sudo systemctl start hbs.service hbs-carousel.service
   ```

## 📡 API Endpoints

### Status
- `GET /api/status` - System status and version
  ```json
  {
    "status": "ok",
    "version": "4.1.9",
    "hbs_name": "HB SYSTEM"
  }
  ```

### Games
- `GET /api/games` - List all games
  ```json
  {
    "games": [...],
    "count": 15
  }
  ```

- `POST /api/games` - Add new game
  ```json
  {
    "id": "game-id",
    "name": "Game Name",
    "launcher": "game-launcher.sh"
  }
  ```

### Launching
- `GET /launch?id=GAME_ID` - Launch a game (updates playtime)
  ```json
  {
    "status": "launching",
    "game": "Pokemon Emerald"
  }
  ```

## ⚙️ Configuration

### HBS Backend Config
`~/.hbs/config.json`:
```json
{
  "version": "4.1.9",
  "port": 5000,
  "display_name": "HB SYSTEM",
  "roms_root": "/mnt/hbs-roms"
}
```

### Carousel Config
`~/.hbs/carousel_config.json`:
```json
{
  "api_url": "http://localhost:5000",
  "steamgriddb_api_key": "",
  "covers_dir": "~/.hbs/covers"
}
```

## 🎮 Controller Setup

1. Pair your controller via Bluetooth or USB
2. Start carousel - it auto-detects compatible controllers
3. **D-Pad/Stick Left/Right** - Navigate carousel
4. **A Button** (or Space) - Launch game

Controllers supported:
- 8BitDo controllers
- Steam controller
- Generic gamepads (via Linux input)

## 📁 Project Structure

```
hbs/
├── hbs.py                    # HTTP API backend
├── carousel.py               # Pyglet carousel UI
├── launcher.sh               # Game launcher script
├── routes/
│   ├── __init__.py           # Route registration
│   └── games.py              # Game API endpoints
├── installer/
│   ├── linux/
│   │   ├── hbs/
│   │   │   ├── hbs.spec      # PyInstaller spec for backend
│   │   │   └── build.sh
│   │   └── carousel/
│   │       ├── carousel.spec # PyInstaller spec for UI
│   │       └── build.sh
│   └── *.template            # Config templates
├── .github/
│   └── workflows/
│       └── release.yml       # CI/CD pipeline
├── install.sh                # Installation script
└── README.md
```

## 🔧 Development

### Building from Source

1. **Clone repo**
   ```bash
   git clone https://github.com/houbou98-19/hbs.git
   cd hbs
   ```

2. **Install dev dependencies**
   ```bash
   pip install pyglet requests flask
   ```

3. **Run locally**
   ```bash
   python3 hbs.py      # Terminal 1
   python3 carousel.py # Terminal 2 (if needed)
   ```

### Building Binaries

The project uses PyInstaller for binary packaging:

```bash
# HBS backend
cd installer/linux/hbs
pyinstaller hbs.spec --distpath ./dist --workpath ./build

# Carousel UI
cd installer/linux/carousel
pyinstaller carousel.spec --distpath ./dist --workpath ./build
```

### Releasing

1. Commit changes
2. Push to dev branch
3. Run release on Windows:
   ```bash
   ./release-local.sh
   # Select: patch, minor, or major
   # Workflow builds binaries and auto-deploys to Ubuntu
   ```

## 🐛 Troubleshooting

### Games Won't Launch
- Check `sudo journalctl -u hbs.service -f`
- Verify launcher script exists: `ls ~/launchers/`
- Test launcher manually: `bash ~/launchers/game.sh`

### No Cover Art
- Set `steamgriddb_api_key` in `~/.hbs/carousel_config.json`
- Get key at https://www.steamgriddb.com/
- Check covers downloaded: `ls ~/.hbs/covers/`

### Carousel Freezes
- Check `sudo journalctl -u hbs-carousel.service -f`
- Verify HBS backend is running: `curl http://localhost:5000/api/status`
- Kill and restart: `sudo systemctl restart hbs-carousel.service`

### Display Issues
- Set `SCREEN_WIDTH` and `SCREEN_HEIGHT` env vars in service file
- Check resolution: `echo $SCREEN_WIDTH x $SCREEN_HEIGHT`

## 📋 Systemd Services

Both services run as the `hobo` user:

```bash
# View status
sudo systemctl status hbs.service
sudo systemctl status hbs-carousel.service

# View logs
sudo journalctl -u hbs.service -f
sudo journalctl -u hbs-carousel.service -f

# Restart
sudo systemctl restart hbs.service hbs-carousel.service
```

## 🗺️ Roadmap

- [x] Carousel UI with animations
- [x] Game cover art from SteamGridDB
- [x] Controller support
- [x] Playtime tracking
- [x] HTTP REST API
- [x] Automated CI/CD pipeline
- [x] Linux binary releases
- [ ] Windows installer
- [x] Carousel Title Shine
- [ ] Save state management
- [ ] Game statistics dashboard
- [ ] NFC tag integration (future)

## 📄 License

MIT License - see LICENSE file for details
---

**Made for 🎮 myself**