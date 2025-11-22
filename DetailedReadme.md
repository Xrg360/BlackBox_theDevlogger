# 📦 Blackbox - Development Logging System

A comprehensive development logging and tracking system built with FastAPI and SQLModel. Track your projects, code snippets, execution runs, and development events all in one place.

## 🚀 Features

- **Multi-user support** - Track projects across multiple users
- **Project management** - Organize your work into logical projects
- **Session tracking** - Group related runs into sessions
- **Code snippets** - Store and version your code
- **Run tracking** - Monitor code execution with status, timing, and output
- **Event logging** - Record development events with structured metadata
- **Git integration** - Automatic commit tracking via git hooks
- **Statistics** - View comprehensive analytics about your development activity
- **REST API** - Full-featured API with auto-generated documentation, health checks, and pagination
- **CLI Tool** - Powerful command-line interface for all operations
- **Configuration** - Environment-based configuration with .env support
- **Testing** - Comprehensive test suite included

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (for automatic tracking features)

## 🛠️ Installation

1. **Clone or download the project:**
   ```bash
   cd blackbox
   ```

2. **Create and activate virtual environment:**
   ```powershell
   # Windows PowerShell
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```
   
   ```bash
   # Linux/Mac
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure (Optional):**
   ```bash
   # Copy example config
   cp .env.example .env
   
   # Edit .env to customize settings
   # - API_HOST, API_PORT
   # - DATABASE_URL
   # - BLACKBOX_API_URL
   # - LOG_LEVEL
   ```

5. **Install Git Hooks (Optional but Recommended):**
   ```powershell
   # Windows
   .\install-hooks.ps1
   ```
   ```bash
   # Linux/Mac
   chmod +x install-hooks.sh
   ./install-hooks.sh
   ```

## 🏃 Quick Start

### 1. Start the API Server

**Easy way:**
```bash
python start_server.py
```

**Manual way:**

```powershell
# Windows
.\env\Scripts\python.exe -m uvicorn backend.main:app --reload
```

```bash
# Linux/Mac
python -m uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

### 2. Use the CLI Tool

Open a new terminal (keep the server running) and try these commands:

```bash
# Create a user
python devlog.py user create alice

# Create a project
python devlog.py project create "My First Project" --owner-id 1

# Start a session
python devlog.py session start --project-id 1

# Log an event
python devlog.py event log --project-id 1 --type info --message "Started coding"

# View statistics
python devlog.py stats
```

## 📊 Database Schema

The system uses the following data models:

### User
**Fields:**
- `id` - Primary key
- `username` - Unique username
- `created_at` - Registration timestamp

**Why Use Users?**
Users represent individuals or team members working on projects. They help you:
- Track who owns which projects
- Maintain accountability for development work
- Organize projects by team member
- Support multi-developer environments

**Example:** Create separate users for each developer on your team, then assign projects to them.

---

### Project
**Fields:**
- `id` - Primary key
- `name` - Project name
- `description` - Optional description
- `owner_id` - Foreign key to User

**Why Use Projects?**
Projects are the top-level organizational unit in Blackbox. They help you:
- Group related code, sessions, and events together
- Separate work across different applications or features
- Track metrics and progress per project
- Keep development logs organized

**Example:** Create a project for each application you're building (e.g., "Web API", "Mobile App", "Data Pipeline").

---

### Session
**Fields:**
- `id` - Primary key
- `project_id` - Foreign key to Project
- `started_at` - Session start time
- `ended_at` - Session end time (nullable)

**Why Use Sessions?**
Sessions represent a continuous period of work on a project. They help you:
- Track when you start and stop working
- Group related runs that happened in the same work period
- Measure productive time spent on a project
- Analyze your development patterns over time

**Example:** Start a session when you begin coding, end it when you take a break or finish for the day.

---

### CodeSnippet
**Fields:**
- `id` - Primary key
- `project_id` - Foreign key to Project
- `filename` - Optional filename
- `language` - Programming language (default: python)
- `code` - Source code content
- `created_at` - Creation timestamp

**Why Use Code Snippets?**
Code snippets store pieces of code you execute or analyze. They help you:
- Keep a history of code versions you've tested
- Track what code was run and when
- Compare performance across different implementations
- Debug issues by reviewing past code executions
- Build a library of reusable code pieces

**Example:** Save each version of a function you're optimizing, then track which performs best.

---

### Run
**Fields:**
- `id` - Primary key
- `session_id` - Foreign key to Session
- `snippet_id` - Foreign key to CodeSnippet (optional)
- `status` - Enum: pending, running, success, failed
- `started_at` - Run start time
- `ended_at` - Run end time
- `duration` - Execution duration in seconds
- `stdout` - Standard output
- `stderr` - Standard error
- `return_value` - Return value

**Why Use Runs?**
Runs track individual code executions with their outcomes. They help you:
- Monitor execution status (pending, running, success, failed)
- Capture and store program output for debugging
- Measure execution time and performance
- Link code execution to specific sessions
- Build an audit trail of all code runs

**Example:** Track a script execution that processes data - see how long it took, what it printed, and whether it succeeded.

---

### Event
**Fields:**
- `id` - Primary key
- `timestamp` - Event timestamp
- `project_id` - Foreign key to Project
- `run_id` - Foreign key to Run (optional)
- `event_type` - Enum: info, warning, error, run, metric
- `message` - Event message
- `metadata_json` - JSON string for additional metadata

**Why Use Events?**
Events are timestamped log entries that track what happens in your project. They help you:
- Record important milestones and decisions
- Log errors and warnings for later review
- Track metrics and performance data
- Associate logs with specific code runs
- Build a detailed timeline of project activity
- Debug issues by reviewing the event history

**Example:** Log "Started refactoring authentication module" (info), "API latency: 45ms" (metric), "Database connection failed" (error).

## 🖥️ CLI Reference

### General Usage

```bash
python devlog.py [--api API_URL] <command> <subcommand> [options]
```

Options:
- `--api API_URL` - API base URL (default: http://127.0.0.1:8000)
- `--help` - Show help message

---

### 👤 User Commands

#### Create a user
```bash
python devlog.py user create <username>
```

**Example:**
```bash
python devlog.py user create alice
```

#### List all users
```bash
python devlog.py user list
```

#### Get user by ID
```bash
python devlog.py user get <user_id>
```

**Example:**
```bash
python devlog.py user get 1
```

---

### 📁 Project Commands

#### Create a project
```bash
python devlog.py project create <name> [--desc DESCRIPTION] [--owner-id USER_ID]
```

**Examples:**
```bash
python devlog.py project create "Web Scraper"
python devlog.py project create "API Backend" --desc "REST API for mobile app" --owner-id 1
```

#### List all projects
```bash
python devlog.py project list
```

#### Get project by ID
```bash
python devlog.py project get <project_id>
```

---

### 🔄 Session Commands

#### Start a new session
```bash
python devlog.py session start --project-id <project_id>
```

**Example:**
```bash
python devlog.py session start --project-id 1
```

#### List sessions
```bash
python devlog.py session list [--project-id PROJECT_ID]
```

**Examples:**
```bash
python devlog.py session list
python devlog.py session list --project-id 1
```

#### Get session by ID
```bash
python devlog.py session get <session_id>
```

#### End a session
```bash
python devlog.py session end <session_id>
```

**Example:**
```bash
python devlog.py session end 1
```

---

### 📝 Snippet Commands

#### Create a code snippet
```bash
python devlog.py snippet create --project-id <project_id> --code <code> [--file FILENAME] [--lang LANGUAGE]
```

**Examples:**
```bash
python devlog.py snippet create --project-id 1 --code "print('hello')" --file main.py
python devlog.py snippet create --project-id 1 --code "console.log('hi')" --lang javascript
```

#### List snippets
```bash
python devlog.py snippet list [--project-id PROJECT_ID] [--lang LANGUAGE]
```

**Examples:**
```bash
python devlog.py snippet list
python devlog.py snippet list --project-id 1
python devlog.py snippet list --lang python
```

#### Get snippet by ID
```bash
python devlog.py snippet get <snippet_id>
```

---

### ▶️ Run Commands

#### Create a new run
```bash
python devlog.py run create --session-id <session_id> [--snippet-id SNIPPET_ID]
```

**Examples:**
```bash
python devlog.py run create --session-id 1
python devlog.py run create --session-id 1 --snippet-id 5
```

#### List runs
```bash
python devlog.py run list [--session-id SESSION_ID] [--status STATUS]
```

**Status options:** `pending`, `running`, `success`, `failed`

**Examples:**
```bash
python devlog.py run list
python devlog.py run list --session-id 1
python devlog.py run list --status success
```

#### Get run by ID
```bash
python devlog.py run get <run_id>
```

#### Update run details
```bash
python devlog.py run update <run_id> [--status STATUS] [--stdout OUTPUT] [--stderr ERROR] [--duration SECONDS]
```

**Examples:**
```bash
python devlog.py run update 1 --status running
python devlog.py run update 1 --status success --stdout "Hello World" --duration 0.023
python devlog.py run update 1 --status failed --stderr "Error: File not found"
```

---

### 📊 Event Commands

#### Log an event
```bash
python devlog.py event log --project-id <project_id> --type <event_type> [--message MESSAGE] [--run-id RUN_ID] [--metadata JSON]
```

**Event types:** `info`, `warning`, `error`, `run`, `metric`

**Examples:**
```bash
python devlog.py event log --project-id 1 --type info --message "Started development"
python devlog.py event log --project-id 1 --type error --message "Build failed" --run-id 5
python devlog.py event log --project-id 1 --type metric --message "Performance test" --metadata '{"latency": 45}'
```

#### List events
```bash
python devlog.py event list [--project-id PROJECT_ID] [--run-id RUN_ID] [--type EVENT_TYPE]
```

**Examples:**
```bash
python devlog.py event list
python devlog.py event list --project-id 1
python devlog.py event list --type error
python devlog.py event list --run-id 5
```

#### Get event by ID
```bash
python devlog.py event get <event_id>
```

---

### 📈 Statistics Commands

#### View summary statistics
```bash
python devlog.py stats
```

Returns comprehensive statistics including:
- Total counts for all entities
- Runs by status
- Events by type

---

## 🌐 API Endpoints

The REST API provides the following endpoints:

### Users
- `POST /users` - Create user
- `GET /users` - List users
- `GET /users/{user_id}` - Get user

### Projects
- `POST /projects` - Create project
- `GET /projects` - List projects
- `GET /projects/{project_id}` - Get project

### Sessions
- `POST /sessions` - Create session
- `GET /sessions` - List sessions
- `GET /sessions/{session_id}` - Get session
- `PATCH /sessions/{session_id}/end` - End session

### Snippets
- `POST /snippets` - Create snippet
- `GET /snippets` - List snippets
- `GET /snippets/{snippet_id}` - Get snippet

### Runs
- `POST /runs` - Create run
- `GET /runs` - List runs
- `GET /runs/{run_id}` - Get run
- `PATCH /runs/{run_id}` - Update run

### Events
- `POST /events` - Create event
- `GET /events` - List events
- `GET /events/{event_id}` - Get event

### Statistics
- `GET /stats/summary` - Get summary statistics

**Interactive API Documentation:** Visit `http://127.0.0.1:8000/docs` when the server is running.

---

## 🤖 Git Hooks Automation

Blackbox includes powerful git hooks that automatically track your development activity without manual logging!

### What Gets Automated

When you install the git hooks, Blackbox will automatically:

✅ **Auto-create users** - Extracts your git username and creates a user in Blackbox  
✅ **Auto-create projects** - Uses your repository name as the project name  
✅ **Log every commit** - Records commit messages as events with metadata  
✅ **Track branch switches** - Logs when you checkout different branches  
✅ **Silent operation** - Runs in the background without interrupting your workflow  

### Installation

#### Windows (PowerShell):
```powershell
# From your git repository root
.\install-hooks.ps1
```

#### Linux/Mac (Bash):
```bash
# From your git repository root
chmod +x install-hooks.sh
./install-hooks.sh
```

#### Manual Installation:
```bash
# Copy hooks to your git repository
cp hooks/post-commit .git/hooks/
cp hooks/pre-commit .git/hooks/
cp hooks/post-checkout .git/hooks/

# Make them executable (Linux/Mac)
chmod +x .git/hooks/post-commit
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-checkout
```

### How It Works

1. **On Commit** (`post-commit` hook):
   - Captures commit message and hash
   - Reads your git username
   - Auto-creates user if it doesn't exist
   - Auto-creates project from repo name if needed
   - Logs commit as an "info" event with metadata

2. **Before Commit** (`pre-commit` hook):
   - Counts staged files
   - Logs a "pre-commit" info event

3. **On Branch Switch** (`post-checkout` hook):
   - Detects branch changes
   - Logs branch name in event

### Example: Automated Workflow

```bash
# 1. Install hooks once
./install-hooks.sh

# 2. Continue your normal git workflow
git add myfile.py
git commit -m "Added new feature"
# ✅ Automatically logged to Blackbox!

git checkout -b feature-branch
# ✅ Branch switch logged!

# 3. View your automated logs
python devlog.py event list --project-id 1
```

### Hook Configuration

The hooks are located in the `hooks/` directory:

- **`post-commit`** - Runs after each commit
- **`pre-commit`** - Runs before commit is created
- **`post-checkout`** - Runs after branch checkout

You can customize these hooks by editing the files in `hooks/` directory before installation.

### Metadata Captured

Each automated event includes rich metadata:

```json
{
  "commit_hash": "a3f5c2d",
  "git_user": "alice",
  "timestamp": "2025-11-22T10:30:00",
  "message": "Fixed authentication bug"
}
```

### Disabling Automation

To temporarily disable hooks:

```bash
# Rename hooks (they won't execute)
mv .git/hooks/post-commit .git/hooks/post-commit.disabled
```

To permanently remove:

```bash
# Delete hooks
rm .git/hooks/post-commit
rm .git/hooks/pre-commit
rm .git/hooks/post-checkout
```

### Requirements

- Git repository initialized (`.git` folder exists)
- Blackbox API server running (`python start_server.py`)
- Python environment with required packages installed
- Git configured with `user.name` and `user.email`

**Check your git config:**
```bash
git config user.name   # Should return your name
git config user.email  # Should return your email

# If not set:
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Troubleshooting Git Hooks

**Hooks not executing?**
- **Linux/Mac:** Ensure hooks are executable: `chmod +x .git/hooks/*`
- **Check git config:** `git config user.name` (must be set)
- **Verify API server:** `curl http://localhost:8000/health`
- **Check Python path:** Hooks look for `env/Scripts/python.exe` or system Python

**Want to test hooks manually?**
```bash
# Run hook directly to see output
.git/hooks/post-commit

# Or on Windows:
.\.git\hooks\post-commit
```

**Check if hooks are installed:**
```bash
# Linux/Mac/Git Bash
ls -la .git/hooks/

# Windows PowerShell
Get-ChildItem .git\hooks\ | Where-Object { $_.Name -match '^(post-commit|pre-commit|post-checkout)$' }
```

**View hook logs:**
```bash
# Check what was logged
python devlog.py event list --type info

# Check specific project
python devlog.py event list --project-id 1
```

**API server not running?**
Hooks will fail silently if the API server isn't running. Start it with:
```bash
python start_server.py
```

**Python not found in hooks?**
Hooks search for Python in this order:
1. `env/Scripts/python.exe` (Windows virtual env)
2. `env/bin/python` (Linux/Mac virtual env)
3. `python3` (system Python)
4. `python` (system Python)

If none found, hooks exit silently without error.

---

## 💡 Example Workflow

### Manual Workflow

Here's a complete workflow example:

```bash
# 1. Create a user
python devlog.py user create alice
# Output: ✅ User created: ID=1, username=alice

# 2. Create a project
python devlog.py project create "Data Pipeline" --desc "ETL pipeline for analytics" --owner-id 1
# Output: ✅ Project created: ID=1, name=Data Pipeline

# 3. Start a coding session
python devlog.py session start --project-id 1
# Output: ✅ Session started: ID=1, project_id=1

# 4. Create code snippets
python devlog.py snippet create --project-id 1 --code "import pandas as pd" --file setup.py
# Output: ✅ Snippet created: ID=1, filename=setup.py

python devlog.py snippet create --project-id 1 --code "df = pd.read_csv('data.csv')" --file load.py
# Output: ✅ Snippet created: ID=2, filename=load.py

# 5. Track a run
python devlog.py run create --session-id 1 --snippet-id 1
# Output: ✅ Run created: ID=1, status=pending

python devlog.py run update 1 --status running
# Output: ✅ Run updated: ID=1, status=running

python devlog.py run update 1 --status success --stdout "Data loaded: 1000 rows" --duration 1.234
# Output: ✅ Run updated: ID=1, status=success

# 6. Log events
python devlog.py event log --project-id 1 --type info --message "Pipeline started" --run-id 1
# Output: ✅ Event logged: ID=1

python devlog.py event log --project-id 1 --type metric --message "Processing speed" --metadata '{"rows_per_sec": 810}'
# Output: ✅ Event logged: ID=2

# 7. End the session
python devlog.py session end 1
# Output: ✅ Session ended: ID=1, ended_at=2025-11-22T...

# 8. View statistics
python devlog.py stats
# Output: 📊 Blackbox Statistics: ...
```

### Automated Workflow (with Git Hooks)

For a completely automated experience:

```bash
# 1. One-time setup: Install git hooks
./install-hooks.sh
# Output: ✅ Blackbox hooks installed successfully!

# 2. Your git username becomes your Blackbox user (automatic)
# Your repository name becomes your project (automatic)

# 3. Work normally - everything is tracked automatically!
git add feature.py
git commit -m "Implemented user authentication"
# ✅ Commit automatically logged to Blackbox!
# ✅ User auto-created from git config
# ✅ Project auto-created from repo name

git checkout -b new-feature
# ✅ Branch switch logged!

git add tests.py
git commit -m "Added unit tests"
# ✅ Another commit logged!

# 4. View your automated activity log
python devlog.py event list --type info

# Output shows all your commits and branch switches:
# {
#   "id": 1,
#   "timestamp": "2025-11-22T10:15:30",
#   "event_type": "info",
#   "message": "Commit: Implemented user authentication",
#   "metadata_json": "{\"commit_hash\": \"a3f5c2d\", \"git_user\": \"alice\"}"
# }
```

### Hybrid Workflow (Best of Both Worlds)

Combine automation with manual tracking for maximum insight:

```bash
# 1. Install hooks for automatic git tracking
./install-hooks.sh

# 2. Start a focused work session manually
python devlog.py session start --project-id 1

# 3. Work normally - commits are auto-tracked
git add model.py
git commit -m "Optimized ML model"
# ✅ Auto-logged!

# 4. Manually log important milestones
python devlog.py event log --project-id 1 --type metric \
    --message "Model accuracy improved" \
    --metadata '{"accuracy": 0.95, "improvement": "+5%"}'

# 5. Track code execution manually
python devlog.py snippet create --project-id 1 \
    --code "model.train()" --file train.py

python devlog.py run create --session-id 1 --snippet-id 1
python devlog.py run update 1 --status success --duration 45.2

# 6. Git commits continue to be tracked automatically
git add train.py
git commit -m "Updated training script"
# ✅ Auto-logged!

# 7. End session when done
python devlog.py session end 1

# 8. Review everything
python devlog.py stats
```

This hybrid approach gives you:
- 🤖 **Automatic tracking** of all git activity
- 📝 **Manual control** for important metrics and runs  
- 📊 **Complete visibility** into your development process

---

## 🔧 Configuration

### Database

The system uses SQLite by default. The database file is created at:
```
backend/devbox.db
```

To use a different database, edit `backend/db.py`:

```python
# For PostgreSQL
engine = create_engine("postgresql://user:pass@localhost/blackbox")

# For MySQL
engine = create_engine("mysql://user:pass@localhost/blackbox")
```

### API Server

To change the server host/port:

```bash
# Bind to all interfaces on port 8080
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080

# Production mode (no auto-reload)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### CLI Tool

To use a different API URL:

```bash
python devlog.py --api http://remote-server:8000 stats
```

Or set it as an environment variable:

```bash
# Create a wrapper script
export BLACKBOX_API="http://remote-server:8000"
python devlog.py --api $BLACKBOX_API stats
```

---

## 📁 Project Structure

```
blackbox/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── models.py        # SQLModel database models
│   └── db.py            # Database configuration
├── env/                 # Virtual environment
├── devlog.py            # CLI tool
├── README.md            # This file
└── devbox.db            # SQLite database (created on first run)
```

---

## 🐛 Troubleshooting

### Server won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Install dependencies:
```bash
pip install fastapi uvicorn sqlmodel
```

### CLI shows connection error

**Error:** `❌ Cannot connect to API at http://127.0.0.1:8000`

**Solution:** Make sure the API server is running:
```bash
python -m uvicorn backend.main:app --reload
```

### Database locked error

**Error:** `database is locked`

**Solution:** Close all connections to the database. SQLite only allows one writer at a time. Consider using PostgreSQL for production use.

### Import errors

**Error:** `ModuleNotFoundError: No module named 'backend'`

**Solution:** Run commands from the project root directory (where `backend/` folder is located):
```bash
cd /path/to/blackbox
python devlog.py ...
```

---

## 🧪 Testing

The project includes a comprehensive test suite:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Ensure API server is running in another terminal
python start_server.py

# Run tests
python -m pytest tests/ -v

# Or run the test file directly
python tests/test_api.py
```

Tests cover:
- Health check endpoints
- User CRUD operations
- Project management
- Event logging
- Statistics endpoints
- Pagination
- Duplicate prevention

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `API_HOST` | 0.0.0.0 | API server host address |
| `API_PORT` | 8000 | API server port number |
| `API_RELOAD` | true | Auto-reload on code changes (dev only) |
| `DATABASE_URL` | sqlite:///./devbox.db | Database connection URL |
| `BLACKBOX_API_URL` | http://localhost:8000 | API URL for CLI tool |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

### Database Configuration

**SQLite (Default):**
```env
DATABASE_URL=sqlite:///./devbox.db
```

**PostgreSQL:**
```env
DATABASE_URL=postgresql://user:password@localhost/blackbox
```
Then install: `pip install psycopg2-binary`

**MySQL:**
```env
DATABASE_URL=mysql://user:password@localhost/blackbox
```
Then install: `pip install pymysql`

### CORS Configuration

For production, update CORS settings in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify exact origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)
```

---

## 📊 API Improvements

### New Features Added:

1. **Health Check Endpoints:**
   - `GET /` - Basic health status
   - `GET /health` - Detailed health with database check

2. **Pagination Support:**
   - All list endpoints now support `skip` and `limit` parameters
   - Example: `GET /users?skip=0&limit=10`

3. **Better Error Handling:**
   - Duplicate user prevention
   - Structured logging
   - Descriptive error messages

4. **CORS Middleware:**
   - Cross-origin requests supported
   - Configurable for production

5. **Logging:**
   - Structured logging with timestamps
   - Configurable log levels
   - Request tracking

---

## 🚀 Production Deployment

### Using Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY config.py .
COPY devlog.py .
COPY start_server.py .

EXPOSE 8000

CMD ["python", "start_server.py"]
```

Build and run:
```bash
docker build -t blackbox .
docker run -p 8000:8000 -v $(pwd)/devbox.db:/app/devbox.db blackbox
```

---

## 🤝 Contributing

Suggestions for improvements:

1. Add authentication and authorization
2. Implement WebSocket support for real-time updates
3. Add export functionality (CSV, JSON)
4. Create a web dashboard UI
5. Add more event types and metadata schemas
6. Implement data retention policies
7. Add database migrations with Alembic

---

## 📝 License

This project is open source and available for personal and commercial use.

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases with Python type hints
- [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server
- [Requests](https://requests.readthedocs.io/) - HTTP library

---

## 📧 Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Review the API documentation at `/docs`
3. Examine the code in `backend/` and `devlog.py`

---

**Happy Coding! 🎉**
