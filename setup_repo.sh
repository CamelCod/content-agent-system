#!/bin/bash
# Repository initialization script

set -e

echo "Content Agent System - Repository Setup"
echo "========================================"

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Content Agent System"
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Create .env from example
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENROUTER_API_KEY"
else
    echo "✓ .env already exists"
fi

# Create .streamlit/secrets.toml from example
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "Creating .streamlit/secrets.toml from example..."
    cp .streamlit/secrets.toml.example .streamlit/secrets.toml
    echo "⚠️  Please edit .streamlit/secrets.toml and add your OPENROUTER_API_KEY"
else
    echo "✓ .streamlit/secrets.toml already exists"
fi

# Make scripts executable
chmod +x deploy.sh
chmod +x setup_repo.sh

echo ""
echo "========================================"
echo "Repository setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENROUTER_API_KEY"
echo "2. Edit .streamlit/secrets.toml and add your OPENROUTER_API_KEY"
echo "3. Run: ./deploy.sh to install dependencies"
echo ""
