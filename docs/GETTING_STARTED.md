# Getting Started

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**
   ```bash
   cd pixel_command
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## Configuration

Edit [config.json](../config.json) to customize:
- Display settings (resolution, fullscreen, FPS)
- Audio levels
- Gameplay options
- Controls
- Debug settings

## Project Structure

```
pixel_command/
├── main.py              # Entry point
├── config.json          # Configuration
├── requirements.txt     # Dependencies
├── src/                 # Source code
│   ├── core/           # Core game systems
│   ├── states/         # Game states
│   ├── battle/         # Combat system
│   ├── entities/       # ECS implementation
│   ├── procgen/        # Procedural generation
│   ├── ui/             # User interface
│   ├── data/           # Game data definitions
│   └── utils/          # Utilities
├── assets/             # Game assets
├── tests/              # Unit tests
└── docs/               # Documentation
```

## Development Workflow

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
```

### Linting
```bash
pylint src/
```

## Next Steps

1. **Read the Architecture** - See [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Add Game Assets** - Replace placeholders in [assets/](../assets/)
3. **Implement Features** - Follow the workflow in README.md
4. **Test Your Changes** - Write tests in [tests/](../tests/)

## Troubleshooting

### Pygame Installation Issues
If pygame fails to install:
```bash
pip install pygame --pre
```

### Missing Modules
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --force-reinstall
```

### Display Issues
Try disabling vsync in config.json:
```json
{
  "display": {
    "vsync": false
  }
}
```

## Getting Help

- Check the [README.md](../README.md) for project overview
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- See example implementations in [src/states/](../src/states/)
