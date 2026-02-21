#!/bin/bash
# Quick test runner for local development
# Usage: ./run_tests.sh

set -e

echo "🧪 Running Local Test Suite"
echo "======================================"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not detected. Activate it first:"
    echo "   source .venv/bin/activate  # on Linux/Mac"
    echo "   .venv\Scripts\activate     # on Windows"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -q -r requirements-dev.txt

# Run pytest with coverage
echo ""
echo "🏃 Running pytest..."
pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html --tb=short

# Show coverage summary
echo ""
echo "📊 Coverage report generated in htmlcov/index.html"

# Optional: run linting
if [ "$1" == "--lint" ]; then
    echo ""
    echo "🔍 Running linters..."
    black . --exclude ".venv,__pycache__,build" || true
    flake8 . --max-line-length=120 --exclude=".venv,__pycache__,build" || true
fi

echo ""
echo "✅ All tests passed!"
