#!/usr/bin/env python3
"""
DevLog CLI - Blackbox development logging tool
Interact with the Dev Blackbox API to track projects, sessions, code runs, and events.
"""
import argparse
import sys
import json
from datetime import datetime
from typing import Optional
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' module not found. Install it with: pip install requests", file=sys.stderr)
    sys.exit(1)

# Try to load configuration
try:
    # When installed as package, config should be in project root
    import os
    sys.path.insert(0, os.getcwd())
    from config import BLACKBOX_API_URL
    API_BASE = BLACKBOX_API_URL
except ImportError:
    API_BASE = "http://127.0.0.1:8000"


class BlackboxClient:
    """Client for interacting with the Dev Blackbox API."""
    
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def _request(self, method: str, endpoint: str, **kwargs):
        """Make an HTTP request and handle errors."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to API at {self.base_url}", file=sys.stderr)
            print("   Make sure the server is running: python -m uvicorn backend.main:app", file=sys.stderr)
            sys.exit(1)
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}", file=sys.stderr)
            if e.response.text:
                print(f"   {e.response.text}", file=sys.stderr)
            sys.exit(1)
        except requests.exceptions.Timeout:
            print(f"❌ Request timeout to {url}", file=sys.stderr)
            sys.exit(1)
    
    # ===================== User operations =====================
    
    def create_user(self, username: str):
        """Create a new user."""
        return self._request("POST", "/users", json={"username": username})
    
    def list_users(self):
        """List all users."""
        return self._request("GET", "/users")
    
    def get_user(self, user_id: int):
        """Get user by ID."""
        return self._request("GET", f"/users/{user_id}")
    
    # ===================== Project operations =====================
    
    def create_project(self, name: str, description: Optional[str] = None, owner_id: Optional[int] = None):
        """Create a new project."""
        payload = {"name": name}
        if description:
            payload["description"] = description
        if owner_id:
            payload["owner_id"] = owner_id
        return self._request("POST", "/projects", json=payload)
    
    def list_projects(self):
        """List all projects."""
        return self._request("GET", "/projects")
    
    def get_project(self, project_id: int):
        """Get project by ID."""
        return self._request("GET", f"/projects/{project_id}")
    
    # ===================== Session operations =====================
    
    def create_session(self, project_id: int):
        """Start a new session for a project."""
        return self._request("POST", "/sessions", json={"project_id": project_id})
    
    def list_sessions(self, project_id: Optional[int] = None):
        """List sessions, optionally filtered by project."""
        params = {"project_id": project_id} if project_id else {}
        return self._request("GET", "/sessions", params=params)
    
    def get_session(self, session_id: int):
        """Get session by ID."""
        return self._request("GET", f"/sessions/{session_id}")
    
    def end_session(self, session_id: int):
        """End a session."""
        return self._request("PATCH", f"/sessions/{session_id}/end")
    
    # ===================== Snippet operations =====================
    
    def create_snippet(self, project_id: int, code: str, filename: Optional[str] = None, language: str = "python"):
        """Create a code snippet."""
        payload = {
            "project_id": project_id,
            "code": code,
            "language": language
        }
        if filename:
            payload["filename"] = filename
        return self._request("POST", "/snippets", json=payload)
    
    def list_snippets(self, project_id: Optional[int] = None, language: Optional[str] = None):
        """List snippets."""
        params = {}
        if project_id:
            params["project_id"] = project_id
        if language:
            params["language"] = language
        return self._request("GET", "/snippets", params=params)
    
    def get_snippet(self, snippet_id: int):
        """Get snippet by ID."""
        return self._request("GET", f"/snippets/{snippet_id}")
    
    # ===================== Run operations =====================
    
    def create_run(self, session_id: int, snippet_id: Optional[int] = None):
        """Create a new run."""
        payload = {"session_id": session_id}
        if snippet_id:
            payload["snippet_id"] = snippet_id
        return self._request("POST", "/runs", json=payload)
    
    def list_runs(self, session_id: Optional[int] = None, status: Optional[str] = None):
        """List runs."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        if status:
            params["status"] = status
        return self._request("GET", "/runs", params=params)
    
    def get_run(self, run_id: int):
        """Get run by ID."""
        return self._request("GET", f"/runs/{run_id}")
    
    def update_run(self, run_id: int, status: Optional[str] = None, stdout: Optional[str] = None, 
                   stderr: Optional[str] = None, duration: Optional[float] = None):
        """Update run details."""
        payload = {}
        if status:
            payload["status"] = status
        if stdout is not None:
            payload["stdout"] = stdout
        if stderr is not None:
            payload["stderr"] = stderr
        if duration is not None:
            payload["duration"] = duration
        return self._request("PATCH", f"/runs/{run_id}", json=payload)
    
    # ===================== Event operations =====================
    
    def create_event(self, project_id: int, event_type: str, message: Optional[str] = None, 
                     run_id: Optional[int] = None, metadata: Optional[str] = None):
        """Create a new event."""
        payload = {
            "project_id": project_id,
            "event_type": event_type
        }
        if message:
            payload["message"] = message
        if run_id:
            payload["run_id"] = run_id
        if metadata:
            payload["metadata_json"] = metadata
        return self._request("POST", "/events", json=payload)
    
    def list_events(self, project_id: Optional[int] = None, run_id: Optional[int] = None, 
                    event_type: Optional[str] = None):
        """List events."""
        params = {}
        if project_id:
            params["project_id"] = project_id
        if run_id:
            params["run_id"] = run_id
        if event_type:
            params["event_type"] = event_type
        return self._request("GET", "/events", params=params)
    
    def get_event(self, event_id: int):
        """Get event by ID."""
        return self._request("GET", f"/events/{event_id}")
    
    # ===================== Stats operations =====================
    
    def get_stats(self):
        """Get summary statistics."""
        return self._request("GET", "/stats/summary")


def print_json(data):
    """Pretty-print JSON data."""
    print(json.dumps(data, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(
        description="DevLog CLI - Blackbox development logging tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a user and project
  %(prog)s user create alice
  %(prog)s project create "My Project" --owner-id 1
  
  # Start a session and log events
  %(prog)s session start --project-id 1
  %(prog)s event log --project-id 1 --type info --message "Started coding"
  
  # Create and track a code run
  %(prog)s snippet create --project-id 1 --code "print('hello')" --file test.py
  %(prog)s run create --session-id 1 --snippet-id 1
  %(prog)s run update 1 --status success --stdout "hello"
  
  # View stats
  %(prog)s stats
        """
    )
    
    parser.add_argument("--api", default=API_BASE, help=f"API base URL (default: {API_BASE})")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    subparsers.required = True
    
    # ===================== User commands =====================
    user_parser = subparsers.add_parser("user", help="User operations")
    user_sub = user_parser.add_subparsers(dest="subcommand")
    user_sub.required = True
    
    user_create = user_sub.add_parser("create", help="Create a new user")
    user_create.add_argument("username", help="Username")
    
    user_sub.add_parser("list", help="List all users")
    
    user_get = user_sub.add_parser("get", help="Get user by ID")
    user_get.add_argument("id", type=int, help="User ID")
    
    # ===================== Project commands =====================
    project_parser = subparsers.add_parser("project", help="Project operations")
    project_sub = project_parser.add_subparsers(dest="subcommand")
    project_sub.required = True
    
    project_create = project_sub.add_parser("create", help="Create a new project")
    project_create.add_argument("name", help="Project name")
    project_create.add_argument("--desc", help="Project description")
    project_create.add_argument("--owner-id", type=int, help="Owner user ID")
    
    project_sub.add_parser("list", help="List all projects")
    
    project_get = project_sub.add_parser("get", help="Get project by ID")
    project_get.add_argument("id", type=int, help="Project ID")
    
    # ===================== Session commands =====================
    session_parser = subparsers.add_parser("session", help="Session operations")
    session_sub = session_parser.add_subparsers(dest="subcommand")
    session_sub.required = True
    
    session_start = session_sub.add_parser("start", help="Start a new session")
    session_start.add_argument("--project-id", type=int, required=True, help="Project ID")
    
    session_list = session_sub.add_parser("list", help="List sessions")
    session_list.add_argument("--project-id", type=int, help="Filter by project ID")
    
    session_get = session_sub.add_parser("get", help="Get session by ID")
    session_get.add_argument("id", type=int, help="Session ID")
    
    session_end = session_sub.add_parser("end", help="End a session")
    session_end.add_argument("id", type=int, help="Session ID")
    
    # ===================== Snippet commands =====================
    snippet_parser = subparsers.add_parser("snippet", help="Code snippet operations")
    snippet_sub = snippet_parser.add_subparsers(dest="subcommand")
    snippet_sub.required = True
    
    snippet_create = snippet_sub.add_parser("create", help="Create a code snippet")
    snippet_create.add_argument("--project-id", type=int, required=True, help="Project ID")
    snippet_create.add_argument("--code", required=True, help="Code content")
    snippet_create.add_argument("--file", help="Filename")
    snippet_create.add_argument("--lang", default="python", help="Programming language (default: python)")
    
    snippet_list = snippet_sub.add_parser("list", help="List snippets")
    snippet_list.add_argument("--project-id", type=int, help="Filter by project ID")
    snippet_list.add_argument("--lang", help="Filter by language")
    
    snippet_get = snippet_sub.add_parser("get", help="Get snippet by ID")
    snippet_get.add_argument("id", type=int, help="Snippet ID")
    
    # ===================== Run commands =====================
    run_parser = subparsers.add_parser("run", help="Run operations")
    run_sub = run_parser.add_subparsers(dest="subcommand")
    run_sub.required = True
    
    run_create = run_sub.add_parser("create", help="Create a new run")
    run_create.add_argument("--session-id", type=int, required=True, help="Session ID")
    run_create.add_argument("--snippet-id", type=int, help="Snippet ID")
    
    run_list = run_sub.add_parser("list", help="List runs")
    run_list.add_argument("--session-id", type=int, help="Filter by session ID")
    run_list.add_argument("--status", choices=["pending", "running", "success", "failed"], help="Filter by status")
    
    run_get = run_sub.add_parser("get", help="Get run by ID")
    run_get.add_argument("id", type=int, help="Run ID")
    
    run_update = run_sub.add_parser("update", help="Update run details")
    run_update.add_argument("id", type=int, help="Run ID")
    run_update.add_argument("--status", choices=["pending", "running", "success", "failed"], help="Run status")
    run_update.add_argument("--stdout", help="Standard output")
    run_update.add_argument("--stderr", help="Standard error")
    run_update.add_argument("--duration", type=float, help="Duration in seconds")
    
    # ===================== Event commands =====================
    event_parser = subparsers.add_parser("event", help="Event operations")
    event_sub = event_parser.add_subparsers(dest="subcommand")
    event_sub.required = True
    
    event_log = event_sub.add_parser("log", help="Log a new event")
    event_log.add_argument("--project-id", type=int, required=True, help="Project ID")
    event_log.add_argument("--type", required=True, choices=["info", "warning", "error", "run", "metric"], 
                           dest="event_type", help="Event type")
    event_log.add_argument("--message", help="Event message")
    event_log.add_argument("--run-id", type=int, help="Associated run ID")
    event_log.add_argument("--metadata", help="JSON metadata string")
    
    event_list = event_sub.add_parser("list", help="List events")
    event_list.add_argument("--project-id", type=int, help="Filter by project ID")
    event_list.add_argument("--run-id", type=int, help="Filter by run ID")
    event_list.add_argument("--type", choices=["info", "warning", "error", "run", "metric"], help="Filter by event type")
    
    event_get = event_sub.add_parser("get", help="Get event by ID")
    event_get.add_argument("id", type=int, help="Event ID")
    
    # ===================== Stats commands =====================
    subparsers.add_parser("stats", help="View summary statistics")
    
    # ===================== Automation commands (for git hooks) =====================
    auto_commit = subparsers.add_parser("auto-commit", help="Auto-log git commit (used by hooks)")
    auto_commit.add_argument("--project", required=True, help="Project name")
    auto_commit.add_argument("--message", required=True, help="Commit message")
    auto_commit.add_argument("--commit-hash", help="Commit hash")
    auto_commit.add_argument("--git-user", help="Git username")
    
    auto_event = subparsers.add_parser("auto-event", help="Auto-log event (used by hooks)")
    auto_event.add_argument("--project", required=True, help="Project name")
    auto_event.add_argument("--type", required=True, help="Event type")
    auto_event.add_argument("--message", required=True, help="Event message")
    auto_event.add_argument("--git-user", help="Git username")
    
    args = parser.parse_args()
    
    client = BlackboxClient(args.api)
    
    try:
        # User commands
        if args.command == "user":
            if args.subcommand == "create":
                result = client.create_user(args.username)
                print(f"✅ User created: ID={result['id']}, username={result['username']}")
            elif args.subcommand == "list":
                users = client.list_users()
                print(f"📋 Found {len(users)} user(s):")
                print_json(users)
            elif args.subcommand == "get":
                user = client.get_user(args.id)
                print_json(user)
        
        # Project commands
        elif args.command == "project":
            if args.subcommand == "create":
                result = client.create_project(args.name, args.desc, args.owner_id)
                print(f"✅ Project created: ID={result['id']}, name={result['name']}")
            elif args.subcommand == "list":
                projects = client.list_projects()
                print(f"📋 Found {len(projects)} project(s):")
                print_json(projects)
            elif args.subcommand == "get":
                project = client.get_project(args.id)
                print_json(project)
        
        # Session commands
        elif args.command == "session":
            if args.subcommand == "start":
                result = client.create_session(args.project_id)
                print(f"✅ Session started: ID={result['id']}, project_id={result['project_id']}")
            elif args.subcommand == "list":
                sessions = client.list_sessions(args.project_id)
                print(f"📋 Found {len(sessions)} session(s):")
                print_json(sessions)
            elif args.subcommand == "get":
                session = client.get_session(args.id)
                print_json(session)
            elif args.subcommand == "end":
                result = client.end_session(args.id)
                print(f"✅ Session ended: ID={result['id']}, ended_at={result['ended_at']}")
        
        # Snippet commands
        elif args.command == "snippet":
            if args.subcommand == "create":
                result = client.create_snippet(args.project_id, args.code, args.file, args.lang)
                print(f"✅ Snippet created: ID={result['id']}, filename={result.get('filename', 'N/A')}")
            elif args.subcommand == "list":
                snippets = client.list_snippets(args.project_id, args.lang)
                print(f"📋 Found {len(snippets)} snippet(s):")
                print_json(snippets)
            elif args.subcommand == "get":
                snippet = client.get_snippet(args.id)
                print_json(snippet)
        
        # Run commands
        elif args.command == "run":
            if args.subcommand == "create":
                result = client.create_run(args.session_id, args.snippet_id)
                print(f"✅ Run created: ID={result['id']}, status={result['status']}")
            elif args.subcommand == "list":
                runs = client.list_runs(args.session_id, args.status)
                print(f"📋 Found {len(runs)} run(s):")
                print_json(runs)
            elif args.subcommand == "get":
                run = client.get_run(args.id)
                print_json(run)
            elif args.subcommand == "update":
                result = client.update_run(args.id, args.status, args.stdout, args.stderr, args.duration)
                print(f"✅ Run updated: ID={result['id']}, status={result['status']}")
        
        # Event commands
        elif args.command == "event":
            if args.subcommand == "log":
                result = client.create_event(args.project_id, args.event_type, args.message, 
                                            args.run_id, args.metadata)
                print(f"✅ Event logged: ID={result['id']}, timestamp={result['timestamp']}")
            elif args.subcommand == "list":
                events = client.list_events(args.project_id, args.run_id, args.type)
                print(f"📋 Found {len(events)} event(s):")
                print_json(events)
            elif args.subcommand == "get":
                event = client.get_event(args.id)
                print_json(event)
        
        # Stats command
        elif args.command == "stats":
            stats = client.get_stats()
            print("📊 Blackbox Statistics:")
            print_json(stats)
        
        # Automation commands (silent mode for git hooks)
        elif args.command == "auto-commit":
            # Auto-create user if needed
            git_user = args.git_user or "unknown"
            user_id = None
            try:
                users = client.list_users()
                user = next((u for u in users if u['username'] == git_user), None)
                if not user:
                    user = client.create_user(git_user)
                user_id = user['id']
            except:
                pass
            
            # Auto-create project if needed
            project_name = args.project
            project_id = None
            try:
                projects = client.list_projects()
                project = next((p for p in projects if p['name'] == project_name), None)
                if not project:
                    project = client.create_project(project_name, f"Auto-created for {git_user}", user_id)
                project_id = project['id']
            except:
                pass
            
            # Log commit event
            if project_id:
                metadata = {}
                if args.commit_hash:
                    metadata['commit_hash'] = args.commit_hash
                if git_user:
                    metadata['git_user'] = git_user
                
                try:
                    client.create_event(
                        project_id, 
                        "info",
                        f"Commit: {args.message}",
                        metadata=json.dumps(metadata) if metadata else None
                    )
                except:
                    pass
        
        elif args.command == "auto-event":
            # Auto-create user if needed
            git_user = args.git_user or "unknown"
            user_id = None
            try:
                users = client.list_users()
                user = next((u for u in users if u['username'] == git_user), None)
                if not user:
                    user = client.create_user(git_user)
                user_id = user['id']
            except:
                pass
            
            # Auto-create project if needed
            project_name = args.project
            project_id = None
            try:
                projects = client.list_projects()
                project = next((p for p in projects if p['name'] == project_name), None)
                if not project:
                    project = client.create_project(project_name, f"Auto-created for {git_user}", user_id)
                project_id = project['id']
            except:
                pass
            
            # Log event
            if project_id:
                metadata = {}
                if git_user:
                    metadata['git_user'] = git_user
                
                try:
                    client.create_event(
                        project_id,
                        args.type,
                        args.message,
                        metadata=json.dumps(metadata) if metadata else None
                    )
                except:
                    pass
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
