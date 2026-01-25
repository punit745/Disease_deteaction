#!/bin/bash

# Quick Start Script for Disease Detection System
# This script helps you get started quickly

set -e

echo "========================================================================"
echo "Disease Detection System - Quick Start"
echo "========================================================================"
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
    DOCKER_AVAILABLE=true
    echo "✓ Docker detected"
else
    DOCKER_AVAILABLE=false
    echo "✗ Docker not found (manual setup will be used)"
fi

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_AVAILABLE=true
    PYTHON_CMD=python3
    echo "✓ Python detected"
elif command -v python &> /dev/null; then
    PYTHON_AVAILABLE=true
    PYTHON_CMD=python
    echo "✓ Python detected"
else
    PYTHON_AVAILABLE=false
    echo "✗ Python not found - please install Python 3.11+"
    exit 1
fi

echo ""
echo "Choose installation method:"
echo "1) Docker (recommended for production)"
echo "2) Manual setup (for development)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    if [ "$DOCKER_AVAILABLE" = false ]; then
        echo "✗ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    echo ""
    echo "Setting up with Docker..."
    echo ""
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        
        # Generate secret keys
        SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || $PYTHON_CMD -c "import secrets; print(secrets.token_hex(32))")
        JWT_SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || $PYTHON_CMD -c "import secrets; print(secrets.token_hex(32))")
        
        # Update .env file
        sed -i.bak "s/your-secret-key-here-change-this/$SECRET_KEY/" .env
        sed -i.bak "s/your-jwt-secret-key-here-change-this/$JWT_SECRET_KEY/" .env
        rm .env.bak 2>/dev/null || true
        
        echo "✓ Generated secret keys"
    fi
    
    # Build and start Docker containers
    echo "Building Docker images..."
    docker-compose build
    
    echo "Starting services..."
    docker-compose up -d
    
    # Wait for services to be ready
    echo "Waiting for services to start..."
    sleep 10
    
    # Initialize database
    echo "Initializing database..."
    docker-compose exec -T web python -c "from app import init_db; init_db()" 2>/dev/null || echo "Database already initialized"
    
    echo ""
    echo "========================================================================"
    echo "✓ Setup complete!"
    echo "========================================================================"
    echo ""
    echo "Services are running:"
    echo "  - API: http://localhost:5000"
    echo "  - Web: http://localhost:80"
    echo ""
    echo "Useful commands:"
    echo "  - View logs:      docker-compose logs -f"
    echo "  - Stop services:  docker-compose down"
    echo "  - Restart:        docker-compose restart"
    echo ""
    echo "Check health: curl http://localhost:5000/api/health"
    echo "========================================================================"
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "Setting up manually..."
    echo ""
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        echo "✓ Virtual environment created"
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
    
    # Upgrade pip
    echo "Upgrading pip..."
    pip install --upgrade pip -q
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt -q
    pip install -r requirements-web.txt -q
    echo "✓ Dependencies installed"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        
        # Generate secret keys
        SECRET_KEY=$($PYTHON_CMD -c "import secrets; print(secrets.token_hex(32))")
        JWT_SECRET_KEY=$($PYTHON_CMD -c "import secrets; print(secrets.token_hex(32))")
        
        # Update .env file
        sed -i.bak "s/your-secret-key-here-change-this/$SECRET_KEY/" .env
        sed -i.bak "s/your-jwt-secret-key-here-change-this/$JWT_SECRET_KEY/" .env
        sed -i.bak "s|postgresql://disease_user:disease_pass@localhost:5432/disease_detection|sqlite:///disease_detection.db|" .env
        rm .env.bak 2>/dev/null || true
        
        echo "✓ Generated secret keys"
    fi
    
    # Initialize database
    echo "Initializing database..."
    $PYTHON_CMD -c "from app import init_db; init_db()"
    
    echo ""
    echo "========================================================================"
    echo "✓ Setup complete!"
    echo "========================================================================"
    echo ""
    echo "To start the application:"
    echo "  1. Activate virtual environment:"
    echo "     source venv/bin/activate"
    echo "  2. Run the application:"
    echo "     python app.py"
    echo ""
    echo "Or run in one command:"
    echo "  source venv/bin/activate && python app.py"
    echo ""
    echo "API will be available at: http://localhost:5000"
    echo ""
    echo "Try it out:"
    echo "  python cli.py register    # Register a new account"
    echo "  python cli.py analyze --sample  # Analyze sample data"
    echo "  python example_usage.py   # Run the example"
    echo "========================================================================"
    
else
    echo "Invalid choice. Exiting."
    exit 1
fi
