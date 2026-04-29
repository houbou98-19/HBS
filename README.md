# HB System - Retro Gaming Launcher

A self-hosted, retro gaming arcade system with a web-based launcher and support for multiple emulators.

## Features

- 🎮 Multi-platform emulation (NES, SNES, N64, GBA, NDS, 3DS, Wii, Switch)
- 🌐 Web-based launcher with retro aesthetic
- 🏷️ NFC tag integration for instant game launching (WIP)
- 👨‍👩‍👧 Multi-player support
- 🖥️ Kiosk mode

## Quick Start

### Requirements
- Python 3.8+
- RetroArch (for most emulators)
- Eden AppImage (for Switch games)
- ROMs of games you own

### Setup Local

1. **Clone the repository**
   ```bash
   git clone https://github.com/houbou98-19/hbs.git
   cd hbs
   ```

2. **Create config directory**
   ```bash
   mkdir -p ~/.hbs/roms
   ```

3. **Run the server**
   ```bash
   python3 hbs.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## Project Structure

```
hbs/
├── hbs.py              # Main server
├── splash.html         # Home screen
├── add.html           # Add game form
├── launch.sh          # Game launcher script (coming soon)
├── README.md
└── .gitignore
```

## Configuration

Games are stored in `~/.hbs/games.json`:

```json
[
  {
    "id": "pokemon-emerald",
    "name": "Pokemon Emerald",
    "platform": "GBA",
    "rom": "/path/to/pokemon-emerald.gba",
    "playtime": 3600,
    "last_played": "2067-06-07T12:30:00"
  }
]
```

## Development

We use semantic versioning and feature branches:

- `main` - Production releases (tagged v1.0.0, v1.1.0, etc.)
- `dev` - Integration branch for testing
- `feature/*` - Feature branches

### Creating a Feature Branch

```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
# Make changes...
git commit -m "Add your feature"
git push -u origin feature/your-feature-name
# Create Pull Request on GitHub
```

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Game launching with RetroArch
- [ ] Eden (Switch emulator) integration
- [ ] Release builds (.sh, .exe)
- [ ] CI/CD pipeline
- [ ] Play time tracking
- [ ] NFC tag integration
- [ ] Save file management

## Contributing

Contributions welcome! Please submit pull requests against the `dev` branch.