#!/bin/bash

# HAX UI FastAPI Backend Startup Script
set -e  # Exit on any error

echo "🚀 Starting HAX UI FastAPI Backend..."

# Parse command line arguments
SKIP_TESTS=false
SKIP_DEPS=false
PRODUCTION=false

for arg in "$@"; do
    case $arg in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --production)
            PRODUCTION=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-tests    Skip running tests"
            echo "  --skip-deps     Skip dependency installation"
            echo "  --production    Use production configuration"
            echo "  --help, -h      Show this help message"
            echo ""
            exit 0
            ;;
    esac
done

# Check if we're in the backend directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: This script must be run from the backend directory"
    echo "📁 Please navigate to the backend directory and try again"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Create local virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating local virtual environment with uv..."
    uv venv .venv --python 3.11
    echo "✅ Local virtual environment created at .venv"
fi

# Check Python version with uv
PYTHON_VERSION=$(uv python --version 2>/dev/null || echo "Unknown")
echo "🐍 uv Python tooling detected: $PYTHON_VERSION"
echo "📁 Using local virtual environment at .venv"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 No .env file found, copying from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from example"
        echo "⚠️  Please edit .env file with your actual configuration values"
    else
        echo "❌ Error: .env.example file not found"
        exit 1
    fi
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Install/sync dependencies with uv
if [ "$SKIP_DEPS" = false ]; then
    echo "📥 Syncing dependencies with uv..."
    if [ "$PRODUCTION" = true ]; then
        uv sync --frozen --no-dev
    else
        uv sync --dev
    fi
    echo "✅ Dependencies synced with uv"
else
    echo "⏭️  Skipping dependency installation"
fi

# Run tests with uv
if [ "$SKIP_TESTS" = false ]; then
    echo "🧪 Running tests with uv..."
    if uv run pytest --tb=short; then
        echo "✅ All tests passed"
    else
        echo "❌ Some tests failed"
        read -p "Continue anyway? (y/N): " continue_choice
        if [[ ! $continue_choice =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "⏭️  Skipping tests"
fi

# Check environment variables
echo "🔍 Checking configuration..."
if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your-super-secret-key-change-in-production" ]; then
    if [ "$PRODUCTION" = true ]; then
        echo "❌ Error: SECRET_KEY must be set for production"
        exit 1
    else
        echo "⚠️  SECRET_KEY not set, using default (change for production!)"
    fi
fi

if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL not set, using SQLite fallback"
    export DATABASE_URL="sqlite:///./haxui.db"
fi

if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your-gemini-api-key-here" ]; then
    echo "❌ Warning: GEMINI_API_KEY not set - AI features will not work"
fi

# Check if port is available
PORT=${PORT:-8000}
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port $PORT is already in use"
    PORT=$((PORT + 1))
    echo "🔄 Trying port $PORT instead..."
fi

# Start the server
echo "🎯 Starting FastAPI server on port $PORT..."
echo "📱 Frontend should point to: http://localhost:$PORT/api/v1"
echo "📚 API documentation: http://localhost:$PORT/api/v1/docs"
echo "📖 Alternative docs: http://localhost:$PORT/api/v1/redoc"
echo "❤️  Health check: http://localhost:$PORT/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Use uv to run uvicorn
if [ "$PRODUCTION" = true ]; then
    echo "🏭 Starting in production mode with uv..."
    uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
else
    echo "🛠️  Starting in development mode with uv..."
    uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
fi