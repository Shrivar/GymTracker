#!/bin/bash

# GymTracker Quick Start Script
# This script sets up and runs GymTracker locally

set -e

echo "🏋️  GymTracker - Local Setup Script"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📚 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py migrate
echo "✓ Migrations completed"

# Check if superuser exists
echo ""
echo "👤 Setting up superuser..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    print("Creating superuser 'admin'...")
    User.objects.create_superuser('admin', 'admin@localhost', 'admin')
    print("✓ Superuser created (username: admin, password: admin)")
else:
    print("✓ Superuser already exists")
END

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a .env file with your Google OAuth credentials (see .env.example)"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000"
echo "4. Admin panel: http://localhost:8000/admin"
echo ""

