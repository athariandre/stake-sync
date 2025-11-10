#!/bin/bash
# Setup script for StakeSync

set -e

echo "🚀 Setting up StakeSync..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - GEMINI_KEY"
    echo "   - SENDGRID_API_KEY"
    echo "   - SENDGRID_FROM_EMAIL"
    echo ""
fi

# Initialize database
echo "🗄️  Initializing database..."
python -m app.database.init_db

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Edit .env with your API keys"
echo "  3. Run: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Then open http://localhost:8000/static/chatbot.html in your browser"
echo ""
