#!/usr/bin/env python3
"""
Blackbox API Server Startup Script
Run this to start the development server
"""
import sys
import uvicorn
from pathlib import Path
import os

# Add project root to path
sys.path.insert(0, os.getcwd())

try:
    from config import API_HOST, API_PORT, API_RELOAD
except ImportError:
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    API_RELOAD = True

def main():
    """Main entry point for server"""
    print("=" * 60)
    print("🚀 Starting Blackbox API Server")
    print("=" * 60)
    print(f"Host: {API_HOST}")
    print(f"Port: {API_PORT}")
    print(f"API Docs: http://localhost:{API_PORT}/docs")
    print(f"Health Check: http://localhost:{API_PORT}/health")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "blackbox.backend.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD
    )

if __name__ == "__main__":
    main()
