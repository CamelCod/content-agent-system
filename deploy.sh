#!/bin/bash
# Automated deployment script for content agent system

set -e

echo "Content Agent System - Deployment Script"
echo "========================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENROUTER_API_KEY"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version:"
python3 --version

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p knowledge_bases/voice_and_style
mkdir -p knowledge_bases/content_framework
mkdir -p knowledge_bases/reference
mkdir -p knowledge_bases/examples/linkedin_posts
mkdir -p knowledge_bases/examples/blog_samples
mkdir -p knowledge_bases/examples/article_samples
mkdir -p vector_stores

# Check for API key (verify placeholder has been replaced)
if ! grep -q "your_openrouter_api_key_here" .env; then
    echo "✓ API key appears to be configured (placeholder replaced)"
else
    echo "⚠️  Warning: OPENROUTER_API_KEY still contains placeholder in .env"
    echo "   Please replace with your actual key from: https://openrouter.ai/keys"
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Add your API key to .env (if not done)"
echo "2. Add knowledge base files to knowledge_bases/"
echo "3. Run: streamlit run app.py"
echo ""
echo "Or run batch processor: python batch_processor.py"
echo ""
