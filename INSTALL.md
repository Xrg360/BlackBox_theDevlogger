# Installation Guide - Blackbox DevLog

## Option 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/blackbox-devlog.git
cd blackbox-devlog

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
.\env\Scripts\activate
# Linux/Mac:
source env/bin/activate

# Install in editable mode
pip install -e .

# Verify installation
devlog --help
blackbox-server --help
blackbox-check
```

## Option 2: Install from PyPI (When Published)

```bash
# Create virtual environment (recommended)
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

# Install package
pip install blackbox-devlog

# Verify installation
devlog --help
```

## Option 3: Install Globally (Not Recommended)

```bash
# Install globally (requires admin/sudo)
pip install blackbox-devlog

# Available everywhere
devlog --help
```

## Post-Installation Setup

### 1. Start the API Server

```bash
# Start server (runs on http://localhost:8000)
blackbox-server
```

### 2. Install Git Hooks (Optional but Recommended)

```bash
# Windows PowerShell
.\install-hooks.ps1

# Linux/Mac
chmod +x install-hooks.sh
./install-hooks.sh
```

### 3. Configure (Optional)

```bash
# Copy example config
cp .env.example .env

# Edit configuration
# Set API_PORT, DATABASE_URL, LOG_LEVEL, etc.
```

### 4. Verify Installation

```bash
# Run health check
blackbox-check

# Test CLI
devlog user create "Your Name"
devlog stats
```

## Command Reference

After installation, you have these commands available:

| Command | Description |
|---------|-------------|
| `devlog` | Main CLI tool (previously `python devlog.py`) |
| `blackbox-server` | Start API server (previously `python start_server.py`) |
| `blackbox-check` | Run health checks (previously `python check_setup.py`) |

## Examples

```bash
# Create user
devlog user create "Alice"

# Create project
devlog project create "My App" --owner-id 1

# Start session
devlog session start --project-id 1

# Log event
devlog event log --project-id 1 --type info --message "Started work"

# View stats
devlog stats

# List events
devlog event list --project-id 1
```

## Troubleshooting

**Command not found?**
- Ensure you activated the virtual environment
- Check if installation completed: `pip list | grep blackbox`
- Try reinstalling: `pip install -e .`

**Import errors?**
- Reinstall: `pip install -e .`
- Check Python version: `python --version` (needs 3.10+)

**API connection errors?**
- Start the server: `blackbox-server`
- Check health: `curl http://localhost:8000/health`

## Uninstallation

```bash
# Uninstall package
pip uninstall blackbox-devlog

# Remove git hooks (if installed)
rm .git/hooks/post-commit
rm .git/hooks/pre-commit
rm .git/hooks/post-checkout
```

## Development Installation

For contributing or development:

```bash
# Clone repository
git clone https://github.com/yourusername/blackbox-devlog.git
cd blackbox-devlog

# Create virtual environment
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Make changes and test
devlog --help  # Your changes are immediately available
```
