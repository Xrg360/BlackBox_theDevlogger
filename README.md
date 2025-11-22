# 📦 Blackbox - Development Activity Tracker

> Automatically track your development activity with git integration. Log code runs, events, and metrics with a powerful CLI and REST API.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121-green.svg)](https://fastapi.tiangolo.com/)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python start_server.py

# Install git hooks for automatic tracking (optional)
.\install-hooks.ps1  # Windows
./install-hooks.sh   # Linux/Mac
```

**That's it!** Every git commit is now automatically tracked. 🎉

## ✨ Key Features

- 🤖 **Auto-tracking** - Git hooks capture commits, branches, and activity
- 📊 **Rich Metrics** - Track sessions, runs, events, and code snippets
- 🔧 **Powerful CLI** - Full control with `devlog.py` commands
- 🌐 **REST API** - Complete API at `http://localhost:8000/docs`
- 📈 **Statistics** - Comprehensive analytics and insights
- 🐳 **Production Ready** - Docker support, configurable, tested

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
python devlog.py user create "Alice"
python devlog.py project create "My App" --owner-id 1

# Start a session
python devlog.py session start --project-id 1

# Log events
python devlog.py event log --project-id 1 --type info --message "Started refactoring"

# View statistics
python devlog.py stats
```

### API

```bash
# Health check
curl http://localhost:8000/health

# Create user via API
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "Alice"}'
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
  "git_user": "alice",
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

- **[Detailed Documentation](DetailedReadme.md)** - Complete guide with all commands
- **[Improvements Summary](IMPROVEMENTS.md)** - Recent enhancements
- **[API Docs](http://localhost:8000/docs)** - Interactive API reference (server must be running)

## 🛠️ Troubleshooting

**Server won't start?**
```bash
pip install -r requirements.txt
python check_setup.py  # Diagnostic tool
```

**Git hooks not working?**
```bash
# Reinstall hooks
.\install-hooks.ps1  # Windows
./install-hooks.sh   # Linux/Mac
```

**API connection errors?**
- Ensure server is running: `python start_server.py`
- Check API URL: `http://localhost:8000/health`

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
$ python devlog.py stats

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
2. **Complete audit trail** - Every commit, run, and event is logged
3. **Developer-friendly** - CLI is intuitive, API is well-documented
4. **Production-ready** - Pagination, health checks, CORS, logging
5. **Extensible** - Easy to add custom event types and metadata

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
