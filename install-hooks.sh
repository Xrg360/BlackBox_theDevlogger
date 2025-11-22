#!/bin/bash
# Install Blackbox git hooks
# This script installs hooks to automatically track git activity

echo "🔧 Installing Blackbox Git Hooks..."

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository"
    echo "   Please run this script from the root of your git repository"
    exit 1
fi

# Get the script directory (where hooks are stored)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOKS_DIR="$SCRIPT_DIR/hooks"
GIT_HOOKS_DIR=".git/hooks"

# Check if hooks directory exists
if [ ! -d "$HOOKS_DIR" ]; then
    echo "❌ Error: hooks directory not found at $HOOKS_DIR"
    exit 1
fi

# Install each hook
for hook in post-commit pre-commit post-checkout; do
    SOURCE="$HOOKS_DIR/$hook"
    TARGET="$GIT_HOOKS_DIR/$hook"
    
    if [ -f "$SOURCE" ]; then
        echo "📋 Installing $hook..."
        cp "$SOURCE" "$TARGET"
        chmod +x "$TARGET"
        echo "   ✅ $hook installed"
    else
        echo "   ⚠️  $hook not found, skipping"
    fi
done

echo ""
echo "✅ Blackbox hooks installed successfully!"
echo ""
echo "What happens now:"
echo "   - Every commit will be logged as an event"
echo "   - Branch switches will be tracked"
echo "   - Users and projects are auto-created from git config"
echo ""
echo "Your git username: $(git config user.name)"
echo "Your project name: $(basename "$(git rev-parse --show-toplevel)")"
echo ""
echo "Tip: Make sure the Blackbox API server is running:"
echo "   python -m uvicorn backend.main:app --reload"
