# 📦 Blackbox - Development Activity Tracker

> Automatically track your development activity with git integration. Log code runs, events, and metrics with a powerful CLI and REST API.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121-green.svg)](https://fastapi.tiangolo.com/)

## 🚀 Quick Start

### Option 1: Install as Package (Recommended)

```bash
# Install the package
pip install -e .

# Start the server
blackbox-server

# Use the CLI (in another terminal)
devlog user create "Rohit"
devlog stats

# Install git hooks for automatic tracking
.\install-hooks.ps1  # Windows
./install-hooks.sh   # Linux/Mac
```

### Option 2: Run Directly (Without Installation)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python start_server.py

# Use the CLI (in another terminal)
python devlog.py user create "Rohit"

# Install git hooks
.\install-hooks.ps1  # Windows
./install-hooks.sh   # Linux/Mac
```

**That's it!** Every git commit is now automatically tracked. 🎉

## ✨ Key Features

- 🤖 **Auto-tracking** - Git hooks capture commits, branches, and activity
- 📊 **Rich Metrics** - Track sessions, runs, events, and code snippets
- 🔧 **Powerful CLI** - Simple commands: `devlog` instead of `python devlog.py`
- 🌐 **REST API** - Complete API at `http://localhost:8000/docs`
- 📈 **Statistics** - Comprehensive analytics and insights
- 📦 **Easy Install** - Install once with `pip install -e .`
- 🐳 **Production Ready** - Docker support, configurable, tested

## 📦 Installation

Three ways to install:

### 1. Install as Package (Best for Users)
```bash
pip install -e .
# Commands available: devlog, blackbox-server, blackbox-check
```

### 2. Install from PyPI (When Published)
```bash
pip install blackbox-devlog
```

### 3. Use Directly (Development)
```bash
pip install -r requirements.txt
# Use: python devlog.py, python start_server.py
```

See **[INSTALL.md](INSTALL.md)** for detailed installation guide.

## 📖 Usage

### Automatic Git Tracking (Recommended)

Install git hooks once, then every commit is automatically tracked:

```bash
# One-time setup
.\install-hooks.ps1  # Windows
./install-hooks.sh   # Linux/Mac

# Now just code normally
git add feature.py
git commit -m "Added authentication"
# ✅ Automatically logged with metadata!
# ✅ User auto-created from git config
# ✅ Project auto-created from repo name

git checkout -b new-feature
# ✅ Branch switch logged!
```

**What gets captured:**
- Commit messages and hashes
- Git username (auto-creates user)
- Repository name (auto-creates project)
- Branch switches
- Timestamp metadata

### Manual CLI

```bash
# Create user and project
devlog user create "Rohit"
devlog project create "My App" --owner-id 1

# Start a session
devlog session start --project-id 1

# Log events
devlog event log --project-id 1 --type info --message "Started refactoring"

# View statistics
devlog stats
```

**Note:** If you haven't installed the package, use `python devlog.py` instead of `devlog`.

### API

```bash
# Health check
curl http://localhost:8000/health

# Create user via API
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "Rohit"}'
```

**Interactive API Docs:** http://localhost:8000/docs

## 🏗️ Architecture

**6 Core Models:**
- **User** - Developers/team members
- **Project** - Code repositories/applications
- **Session** - Time-boxed work periods
- **CodeSnippet** - Code pieces and versions
- **Run** - Code executions with output/status
- **Event** - Timestamped logs (commits, errors, metrics)

**Tech Stack:**
- FastAPI + SQLModel + SQLite
- Python 3.10+
- Git hooks for automation

## 🪝 Git Hooks

Blackbox includes powerful git hooks that run automatically on git events:

**Available Hooks:**
- `post-commit` - Logs every commit with message and hash
- `pre-commit` - Tracks pre-commit activity
- `post-checkout` - Logs branch switches

**Installation:**
```bash
# Windows PowerShell
.\install-hooks.ps1

# Linux/Mac
chmod +x install-hooks.sh
./install-hooks.sh
```

**How it works:**
1. Extracts git username → creates/finds user
2. Gets repository name → creates/finds project
3. Captures commit metadata (hash, message, timestamp)
4. Logs as event with JSON metadata
5. Runs silently - doesn't interrupt workflow

**Metadata captured:**
```json
{
  "commit_hash": "a3f5c2d",
  "git_user": "Rohit",
  "message": "Added authentication"
}
```

**Disable hooks:** Rename or delete files in `.git/hooks/`

## ⚙️ Configuration

Copy `.env.example` to `.env` and customize:

```env
API_PORT=8000
DATABASE_URL=sqlite:///./devbox.db
BLACKBOX_API_URL=http://localhost:8000
LOG_LEVEL=INFO
```

## 🧪 Testing

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## 📚 Documentation

- **[Installation Guide](INSTALL.md)** - Complete installation instructions
- **[Detailed Documentation](DetailedReadme.md)** - Complete guide with all commands
- **[Improvements Summary](IMPROVEMENTS.md)** - Recent enhancements
- **[API Docs](http://localhost:8000/docs)** - Interactive API reference (server must be running)

## 🛠️ Available Commands

After installing with `pip install -e .`:

| Command | Old Way | Description |
|---------|---------|-------------|
| `devlog` | `python devlog.py` | Main CLI tool |
| `blackbox-server` | `python start_server.py` | Start API server |
| `blackbox-check` | `python check_setup.py` | Run health checks |

**Examples:**
```bash
devlog user create "Rohit"          # Create user
devlog project create "My App"      # Create project
devlog session start --project-id 1 # Start session
devlog event log --type info --message "Working" --project-id 1
devlog stats                         # View statistics
```

## 🛠️ Troubleshooting

**Command not found: `devlog`?**
```bash
# Install the package first
pip install -e .

# Or use the old way
python devlog.py --help
```

**Server won't start?**
```bash
pip install -r requirements.txt
blackbox-check  # Or: python check_setup.py
```

**Git hooks not working?**
```bash
# Reinstall hooks
.\install-hooks.ps1  # Windows
./install-hooks.sh   # Linux/Mac

# Ensure server is running
blackbox-server  # Or: python start_server.py
```

**API connection errors?**
- Ensure server is running: `blackbox-server`
- Check health: `curl http://localhost:8000/health`

## 🚀 Production Deployment

**Docker:**
```bash
docker build -t blackbox .
docker run -p 8000:8000 blackbox
```

**Gunicorn (Linux/Mac):**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

## 📊 Example Output

```bash
$ devlog stats

📊 Blackbox Statistics
========================
Total Users:     3
Total Projects:  5
Total Sessions: 12
Total Runs:     45
Total Events:   128

Events by Type:
  info:    85
  warning: 12
  error:    8
  run:     18
  metric:   5

Runs by Status:
  success: 38
  failed:   5
  running:  2
```

## 🎯 What Makes This Special

1. **Zero-overhead tracking** - Git hooks work silently in the background
2. **Simple commands** - Just `devlog` instead of `python devlog.py`
3. **Easy installation** - One `pip install -e .` and you're done
4. **Complete audit trail** - Every commit, run, and event is logged
5. **Production-ready** - Pagination, health checks, CORS, logging
6. **Extensible** - Easy to add custom event types and metadata

## 🤝 Contributing

Ideas for enhancement:
- Web dashboard UI
- Real-time WebSocket updates
- Data export (CSV/JSON)
- Authentication/authorization
- Database migrations with Alembic

## 📝 License

Open source - free for personal and commercial use.

---

**Built with ❤️ using FastAPI, SQLModel, and Python**

*For detailed documentation, CLI reference, and examples, see [DetailedReadme.md](DetailedReadme.md)*
