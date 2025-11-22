#!/usr/bin/env python3
"""
Blackbox Project Setup & Health Check
Verifies installation and configuration
"""
import sys
import os
from pathlib import Path
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Check if Python version is adequate"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ ERROR: Python 3.10+ required")
        return False
    print("✅ Python version OK")
    return True

def check_virtual_env():
    """Check if virtual environment is activated"""
    print_header("Checking Virtual Environment")
    
    in_venv = (hasattr(sys, 'real_prefix') or 
               (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    
    if in_venv:
        print(f"✅ Virtual environment active: {sys.prefix}")
        return True
    else:
        print("⚠️  WARNING: Not in a virtual environment")
        print("   Recommended: Create and activate venv")
        print("   Windows: python -m venv env && .\\env\\Scripts\\activate")
        print("   Linux/Mac: python3 -m venv env && source env/bin/activate")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_header("Checking Dependencies")
    
    required = {
        'fastapi': 'FastAPI web framework',
        'uvicorn': 'ASGI server',
        'sqlmodel': 'SQL ORM',
        'requests': 'HTTP client',
        'pydantic': 'Data validation',
        'dotenv': 'Environment config (optional)'
    }
    
    missing = []
    
    for package, description in required.items():
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package:20} - {description}")
        except ImportError:
            print(f"❌ {package:20} - {description} [MISSING]")
            missing.append(package if package != 'dotenv' else 'python-dotenv')
    
    if missing:
        print(f"\n❌ Missing {len(missing)} package(s)")
        print(f"   Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed")
    return True

def check_project_structure():
    """Check if project files exist"""
    print_header("Checking Project Structure")
    
    required_files = {
        'blackbox/backend/main.py': 'API application',
        'blackbox/backend/models.py': 'Database models',
        'blackbox/backend/db.py': 'Database config',
        'blackbox/cli.py': 'CLI tool',
        'config.py': 'Configuration',
        'blackbox/server.py': 'Server startup script',
        'requirements.txt': 'Dependencies list',
        '.env.example': 'Config template'
    }
    
    missing = []
    # Project root is parent of blackbox package
    project_root = Path(__file__).parent.parent
    
    for file_path, description in required_files.items():
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path:30} - {description}")
        else:
            print(f"❌ {file_path:30} - {description} [MISSING]")
            missing.append(file_path)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} file(s)")
        return False
    
    print("\n✅ All required files present")
    return True

def check_config():
    """Check configuration"""
    print_header("Checking Configuration")
    
    # Project root is parent of blackbox package
    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env'
    env_example = project_root / '.env.example'
    
    if env_file.exists():
        print(f"✅ .env file exists")
        print(f"   Location: {env_file}")
    elif env_example.exists():
        print(f"⚠️  .env file not found")
        print(f"   Using defaults from config.py")
        print(f"   Tip: Copy .env.example to .env to customize")
    else:
        print(f"⚠️  No configuration files found")
        print(f"   Using built-in defaults")
    
    try:
        sys.path.insert(0, str(project_root))
        from config import DATABASE_URL, API_PORT, BLACKBOX_API_URL
        print(f"\n📋 Current Configuration:")
        print(f"   API Port: {API_PORT}")
        print(f"   API URL: {BLACKBOX_API_URL}")
        print(f"   Database: {DATABASE_URL}")
    except ImportError:
        print("⚠️  Could not load config.py")
    
    return True

def check_database():
    """Check database"""
    print_header("Checking Database")
    
    # Project root is parent of blackbox package
    project_root = Path(__file__).parent.parent
    db_file = project_root / 'devbox.db'
    
    if db_file.exists():
        size = db_file.stat().st_size
        print(f"✅ Database exists: {db_file}")
        print(f"   Size: {size:,} bytes ({size/1024:.2f} KB)")
    else:
        print(f"ℹ️  Database not created yet")
        print(f"   Will be created on first API startup")
        print(f"   Will be created on first API startup")
    
    return True

def check_git_hooks():
    """Check git hooks installation"""
    print_header("Checking Git Hooks")
    
    # Look for .git in the project root (parent of blackbox package)
    project_root = Path(__file__).parent.parent
    git_dir = project_root / '.git'
    git_hooks = git_dir / 'hooks'
    
    if not git_dir.exists():
        print("⚠️  Not a git repository")
        print("   Git hooks not applicable")
        return True
    
    hooks = ['post-commit', 'pre-commit', 'post-checkout']
    installed = []
    
    for hook in hooks:
        hook_file = git_hooks / hook
        if hook_file.exists():
            print(f"✅ {hook} installed")
            installed.append(hook)
        else:
            print(f"❌ {hook} not installed")
    
    if len(installed) < len(hooks):
        print(f"\n⚠️  {len(hooks) - len(installed)} hook(s) not installed")
        print("   Install with: .\\install-hooks.ps1 (Windows) or ./install-hooks.sh (Linux/Mac)")
    else:
        print("\n✅ All hooks installed")
    
    return True

def check_api_server():
    """Check if API server is running"""
    print_header("Checking API Server")
    
    try:
        import requests
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.status_code == 200:
            data = response.json()
            print("✅ API server is running")
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database')}")
            print(f"   URL: http://localhost:8000")
            print(f"   Docs: http://localhost:8000/docs")
            return True
    except Exception:
        pass
    
    print("❌ API server is not running")
    print("   Start with: python start_server.py")
    return False

def main():
    """Run all checks"""
    print("\n" + "🔍 Blackbox Project Health Check".center(60))
    
    checks = [
        check_python_version,
        check_virtual_env,
        check_dependencies,
        check_project_structure,
        check_config,
        check_database,
        check_git_hooks,
        check_api_server
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with error: {e}")
            results.append(False)
    
    # Summary
    print_header("Summary")
    passed = sum(results)
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All checks passed! Project is ready to use.")
        print("\nNext steps:")
        print("1. Start API server: blackbox-server")
        print("2. Use CLI tool: devlog --help")
        print("3. Visit API docs: http://localhost:8000/docs")
    else:
        print(f"\n⚠️  {total - passed} check(s) failed")
        print("   Review the output above for issues")
        print("\nCommon fixes:")
        print("1. Install package: pip install -e .")
        print("2. Activate virtual env: .\\env\\Scripts\\activate")
        print("3. Create .env file: cp .env.example .env")
    
    print("\n" + "=" * 60 + "\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
