from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel


class EventType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    RUN = "run"
    METRIC = "metric"


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class User(SQLModel, table=True):
    """A user/owner of projects in the blackbox."""
    __tablename__ = "user"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Project(SQLModel, table=True):
    """A logical project grouping snippets, runs and events."""
    __tablename__ = "project"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)


class Session(SQLModel, table=True):
    """A session represents a continuous set of runs (e.g. one user session).
    Sessions belong to a project."""
    __tablename__ = "session"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", index=True)
    started_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    ended_at: Optional[datetime] = None


class CodeSnippet(SQLModel, table=True):
    """Stores a piece of user code or file that can be executed or analyzed."""
    __tablename__ = "codesnippet"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", index=True)
    filename: Optional[str] = None
    language: Optional[str] = Field(default="python", index=True)
    code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Run(SQLModel, table=True):
    """A single execution of a CodeSnippet (or arbitrary command)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: Optional[int] = Field(default=None, foreign_key="session.id", index=True)
    snippet_id: Optional[int] = Field(default=None, foreign_key="codesnippet.id", index=True)

    status: RunStatus = Field(sa_column=Column(SAEnum(RunStatus)), default=RunStatus.PENDING)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration: Optional[float] = None  # seconds

    stdout: Optional[str] = None
    stderr: Optional[str] = None
    return_value: Optional[str] = None


class Event(SQLModel, table=True):
    """Generic event/log entry connected to a project and optionally a run."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", index=True)
    run_id: Optional[int] = Field(default=None, foreign_key="run.id", index=True)

    event_type: EventType = Field(sa_column=Column(SAEnum(EventType)))
    message: Optional[str] = None
    metadata_json: Optional[str] = None  # JSON string or freeform metadata


__all__ = [
    "User",
    "Project",
    "Session",
    "CodeSnippet",
    "Run",
    "Event",
    "EventType",
    "RunStatus",
]
