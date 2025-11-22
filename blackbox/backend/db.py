from sqlmodel import SQLModel, create_engine, Session
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from config import DATABASE_URL
except ImportError:
    # Fallback if config.py not available
    DATABASE_URL = "sqlite:///./devbox.db"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session"""
    return Session(engine)
