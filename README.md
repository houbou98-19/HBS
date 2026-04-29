# HB System - Retro Gaming Launcher

A self-hosted, retro gaming arcade system with a web-based launcher and support for multiple emulators.

## Features

- 🎮 Multi-platform emulation (NES, SNES, N64, GBA, GBC, NDS, 3DS, Wii, Switch)
- 🌐 Web-based launcher with retro aesthetic
- 🎮 RetroArch menu launcher
- 🏷️ NFC tag integration (planned)
- 👨‍👩‍👧 Multi-player support
- 🖥️ Kiosk mode

## Quick Start

### Requirements
- Python 3.8+
- RetroArch
- dbus-x11 (if on ubuntu)
- ROMs of games you own

### Setup (Ubuntu)

1. **Download latest release**
   ```bash
   cd ~/hbs
   bash install-newest-release.sh
   ```

2. **Access the launcher**
   ```
   http://localhost:5000
   ```

3. **Add games**
   - Visit http://localhost:5000/add
   - Select platform and ROM
   - Game appears on splash screen

4. **Launch RetroArch menu**
   ```
   curl http://localhost:5000/menu
   ```
   Or visit http://localhost:5000/menu in browser

### Controller Setup

After launching RetroArch:
1. Main Menu → Online Updater → Update Autoconfig Profiles
2. Restart RetroArch
3. Your controller will auto-configure, but may require rebinding in some cases

## Project Structure

```
hbs/
├── hbs.py              # Main server
├── config.py           # Configuration management
├── launcher.sh         # Game launcher script
├── splash.html         # Home screen
├── add.html            # Add game form
├── config.json         # App config (version, ROMs path, etc.)
├── routes/
│   ├── __init__.py
│   ├── games.py        # Game CRUD + launching
│   ├── pages.py        # HTML page serving
│   └── system.py       # Status endpoint
├── install.sh          # Installation script
├── README.md
└── .gitignore
```

## API Endpoints

- `GET /` - Splash screen (home)
- `GET /add` - Add game form
- `GET /api/status` - System status & version
- `GET /api/games` - List all games
- `GET /api/roms?platform=PLATFORM` - List ROMs for platform
- `POST /api/games` - Add new game
- `GET /menu` - Launch RetroArch menu
- `GET /launch?id=GAME_ID` - Launch specific game (coming soon)

## Configuration

App config stored in config.json:
```json
{
  "version": "2.1.7",
  "roms_root": "/mnt/hbs-roms",
  "port": 5000,
  "display_name": "HB SYSTEM"
}
```

Games stored in ~/.hbs/games.json:
```json
[
  {
    "id": "pokemon-emerald",
    "name": "Pokemon Emerald",
    "platform": "GBA",
    "rom": "/mnt/hbs-roms/gba/pokemon-emerald.gba",
    "playtime": 3600,
    "last_played": "2026-04-29T12:30:00"
  }
]
```

## Development

We use semantic versioning and feature branches:

- `dev` - releases (tagged v1.0.0, v1.1.0, etc.)
- `feature/*` - Feature branches

### Creating a Feature Branch

Make PR onto dev if you wanna add a feature.


### New Release

This is done by setting a new tag following the semantic versioning to. GH workflow will automatically build from latest dev branch and post in releases

### Versioning

Uses semantic versioning:
- `2.0.0` → `2.0.1` (patch fix)
- `2.0.1` → `2.1.0` (minor feature)
- `2.1.0` → `3.0.0` (major refactor)

## Roadmap

- [x] Web-based game launcher
- [x] RetroArch menu integration
- [x] Modular route system
- [x] CI/CD pipeline
- [ ] Chromium kiosk fullscreen mode
- [ ] Game launching with playtime tracking
- [ ] Eden (Switch emulator) integration
- [ ] NFC tag integration
- [ ] Multiple save file management

## License

MIT License - see LICENSE file for details