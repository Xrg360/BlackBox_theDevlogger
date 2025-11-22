from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlmodel import select
import logging
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .models import (
    User, Project, Session, CodeSnippet, Run, Event,
    EventType, RunStatus
)
from .db import init_db, get_session

try:
    from config import LOG_LEVEL
except ImportError:
    LOG_LEVEL = "INFO"

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dev Blackbox API",
    description="A comprehensive API for logging and tracking development activities",
    version="1.0.0"
)

# CORS Configuration - adjust origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== Request/Response Schemas =====================

class UserCreate(BaseModel):
    username: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: Optional[int] = None

class SessionCreate(BaseModel):
    project_id: int

class CodeSnippetCreate(BaseModel):
    project_id: int
    filename: Optional[str] = None
    language: Optional[str] = "python"
    code: str

class RunCreate(BaseModel):
    session_id: int
    snippet_id: Optional[int] = None

class RunUpdate(BaseModel):
    status: Optional[RunStatus] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration: Optional[float] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    return_value: Optional[str] = None

class EventCreate(BaseModel):
    project_id: int
    run_id: Optional[int] = None
    event_type: EventType
    message: Optional[str] = None
    metadata_json: Optional[str] = None

# ===================== Startup =====================

@app.on_event("startup")
async def on_startup():
    logger.info("Starting Blackbox API...")
    init_db()
    logger.info("Database initialized")

# ===================== Health Check =====================

@app.get("/", tags=["Health"])
def root():
    """Root endpoint - health check"""
    return {
        "status": "healthy",
        "service": "Blackbox API",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "database": "not_checked",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Use /health/full for database check"
    }

@app.get("/health/full", tags=["Health"])
def health_check_full():
    """Full health check with database test"""
    try:
        # Test database connection
        with get_session() as s:
            s.exec(select(User).limit(1)).first()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# ===================== User Endpoints =====================

@app.post("/users", status_code=201)
def create_user(data: UserCreate):
    """Create a new user"""
    try:
        user = User(username=data.username)
        with get_session() as s:
            # Check if user already exists
            existing = s.exec(select(User).where(User.username == data.username)).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"User '{data.username}' already exists")
            
            s.add(user)
            s.commit()
            s.refresh(user)
        logger.info(f"Created user: {user.username} (ID: {user.id})")
        return {"id": user.id, "username": user.username}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}")
def get_user(user_id: int):
    with get_session() as s:
        user = s.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@app.get("/users")
def list_users(skip: int = 0, limit: int = 100):
    """List all users with pagination"""
    with get_session() as s:
        users = s.exec(select(User).offset(skip).limit(limit)).all()
    return users

# ===================== Project Endpoints =====================

@app.post("/projects", status_code=201)
def create_project(data: ProjectCreate):
    project = Project(
        name=data.name,
        description=data.description,
        owner_id=data.owner_id
    )
    with get_session() as s:
        s.add(project)
        s.commit()
        s.refresh(project)
    return {"id": project.id, "name": project.name}

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    with get_session() as s:
        project = s.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

@app.get("/projects")
def list_projects(skip: int = 0, limit: int = 100, owner_id: Optional[int] = None):
    """List all projects with pagination"""
    with get_session() as s:
        stmt = select(Project)
        if owner_id:
            stmt = stmt.where(Project.owner_id == owner_id)
        projects = s.exec(stmt.offset(skip).limit(limit)).all()
    return projects

# ===================== Session Endpoints =====================

@app.post("/sessions", status_code=201)
def create_session(data: SessionCreate):
    session = Session(project_id=data.project_id)
    with get_session() as s:
        s.add(session)
        s.commit()
        s.refresh(session)
    return {"id": session.id, "project_id": session.project_id, "started_at": session.started_at}

@app.get("/sessions/{session_id}")
def get_session_detail(session_id: int):
    with get_session() as s:
        session = s.get(Session, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session

@app.get("/sessions")
def list_sessions(project_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    """List all sessions with pagination"""
    with get_session() as s:
        stmt = select(Session)
        if project_id:
            stmt = stmt.where(Session.project_id == project_id)
        sessions = s.exec(stmt.offset(skip).limit(limit)).all()
    return sessions

@app.patch("/sessions/{session_id}/end")
def end_session(session_id: int):
    with get_session() as s:
        session = s.get(Session, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        session.ended_at = datetime.utcnow()
        s.add(session)
        s.commit()
        s.refresh(session)
    return session

# ===================== CodeSnippet Endpoints =====================

@app.post("/snippets", status_code=201)
def create_snippet(data: CodeSnippetCreate):
    snippet = CodeSnippet(
        project_id=data.project_id,
        filename=data.filename,
        language=data.language,
        code=data.code
    )
    with get_session() as s:
        s.add(snippet)
        s.commit()
        s.refresh(snippet)
    return {"id": snippet.id, "project_id": snippet.project_id, "filename": snippet.filename}

@app.get("/snippets/{snippet_id}")
def get_snippet(snippet_id: int):
    with get_session() as s:
        snippet = s.get(CodeSnippet, snippet_id)
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        return snippet

@app.get("/snippets")
def list_snippets(project_id: Optional[int] = None, language: Optional[str] = None, skip: int = 0, limit: int = 100):
    """List all code snippets with pagination"""
    with get_session() as s:
        stmt = select(CodeSnippet)
        if project_id:
            stmt = stmt.where(CodeSnippet.project_id == project_id)
        if language:
            stmt = stmt.where(CodeSnippet.language == language)
        snippets = s.exec(stmt.offset(skip).limit(limit)).all()
    return snippets

# ===================== Run Endpoints =====================

@app.post("/runs", status_code=201)
def create_run(data: RunCreate):
    run = Run(session_id=data.session_id, snippet_id=data.snippet_id)
    with get_session() as s:
        s.add(run)
        s.commit()
        s.refresh(run)
    return {"id": run.id, "session_id": run.session_id, "status": run.status}

@app.get("/runs/{run_id}")
def get_run(run_id: int):
    with get_session() as s:
        run = s.get(Run, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return run

@app.get("/runs")
def list_runs(session_id: Optional[int] = None, status: Optional[RunStatus] = None, skip: int = 0, limit: int = 100):
    """List all runs with pagination"""
    with get_session() as s:
        stmt = select(Run)
        if session_id:
            stmt = stmt.where(Run.session_id == session_id)
        if status:
            stmt = stmt.where(Run.status == status)
        runs = s.exec(stmt.offset(skip).limit(limit)).all()
    return runs

@app.patch("/runs/{run_id}")
def update_run(run_id: int, data: RunUpdate):
    with get_session() as s:
        run = s.get(Run, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        
        if data.status is not None:
            run.status = data.status
        if data.started_at is not None:
            run.started_at = data.started_at
        if data.ended_at is not None:
            run.ended_at = data.ended_at
        if data.duration is not None:
            run.duration = data.duration
        if data.stdout is not None:
            run.stdout = data.stdout
        if data.stderr is not None:
            run.stderr = data.stderr
        if data.return_value is not None:
            run.return_value = data.return_value
        
        s.add(run)
        s.commit()
        s.refresh(run)
    return run

# ===================== Event Endpoints =====================

@app.post("/events", status_code=201)
def create_event(data: EventCreate):
    event = Event(
        project_id=data.project_id,
        run_id=data.run_id,
        event_type=data.event_type,
        message=data.message,
        metadata_json=data.metadata_json
    )
    with get_session() as s:
        s.add(event)
        s.commit()
        s.refresh(event)
    return {"id": event.id, "timestamp": event.timestamp}

@app.get("/events/{event_id}")
def get_event(event_id: int):
    with get_session() as s:
        event = s.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

@app.get("/events")
def list_events(
    project_id: Optional[int] = None,
    run_id: Optional[int] = None,
    event_type: Optional[EventType] = None,
    skip: int = 0,
    limit: int = 100
):
    """List all events with pagination"""
    with get_session() as s:
        stmt = select(Event)
        if project_id:
            stmt = stmt.where(Event.project_id == project_id)
        if run_id:
            stmt = stmt.where(Event.run_id == run_id)
        if event_type:
            stmt = stmt.where(Event.event_type == event_type)
        events = s.exec(stmt.offset(skip).limit(limit)).all()
    return events

# ===================== Stats Endpoints =====================

@app.get("/stats/summary")
def stats_summary():
    with get_session() as s:
        total_users = len(s.exec(select(User)).all())
        total_projects = len(s.exec(select(Project)).all())
        total_sessions = len(s.exec(select(Session)).all())
        total_snippets = len(s.exec(select(CodeSnippet)).all())
        total_runs = len(s.exec(select(Run)).all())
        total_events = len(s.exec(select(Event)).all())
        
        # runs by status
        runs_by_status = {}
        for status in RunStatus:
            count = len(s.exec(select(Run).where(Run.status == status)).all())
            runs_by_status[status.value] = count
        
        # events by type
        events_by_type = {}
        for etype in EventType:
            count = len(s.exec(select(Event).where(Event.event_type == etype)).all())
            events_by_type[etype.value] = count
    
    return {
        "total_users": total_users,
        "total_projects": total_projects,
        "total_sessions": total_sessions,
        "total_snippets": total_snippets,
        "total_runs": total_runs,
        "total_events": total_events,
        "runs_by_status": runs_by_status,
        "events_by_type": events_by_type
    }
