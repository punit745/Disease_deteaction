#!/usr/bin/env python3
"""
Local Setup and Deployment Script for Eye Tracking Disease Detection System

This script provides an interactive setup wizard for deploying the disease
detection system on a local machine. It handles dependency installation,
database initialization, and system validation.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(message):
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_info(message):
    """Print an info message."""
    print(f"{Colors.OKBLUE}ℹ {message}{Colors.ENDC}")


def check_python_version():
    """Check if Python version meets requirements."""
    print_info("Checking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} detected")
        print_error("Python 3.7 or higher is required")
        return False


def check_pip_installed():
    """Check if pip is installed."""
    print_info("Checking pip installation...")
    try:
        # Use subprocess to check pip availability (more reliable)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print_success(f"pip is installed ({version})")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not installed")
        print_info("Please install pip before continuing")
        return False


def create_virtual_environment():
    """Create a Python virtual environment."""
    print_info("Creating virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists")
        response = input("Do you want to recreate it? (y/n): ").lower()
        if response == 'y':
            print_info("Removing existing virtual environment...")
            shutil.rmtree(venv_path)
        else:
            print_info("Using existing virtual environment")
            return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False


def get_pip_command():
    """Get the appropriate pip command for the virtual environment."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip")
    else:
        return os.path.join("venv", "bin", "pip")


def get_python_command():
    """Get the appropriate python command for the virtual environment."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python")
    else:
        return os.path.join("venv", "bin", "python")


def install_dependencies():
    """Install project dependencies."""
    print_info("Installing dependencies...")
    
    pip_cmd = get_pip_command()
    
    # Upgrade pip first
    print_info("Upgrading pip...")
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print_success("pip upgraded")
    except subprocess.CalledProcessError as e:
        print_warning("Failed to upgrade pip, continuing anyway...")
    
    # Install core dependencies
    print_info("Installing core dependencies (numpy, pandas, scipy, etc.)...")
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print_success("Core dependencies installed")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install core dependencies: {e}")
        return False
    
    # Install web dependencies
    print_info("Installing web dependencies (Flask, SQLAlchemy, etc.)...")
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements-web.txt"], 
                      check=True, capture_output=True)
        print_success("Web dependencies installed")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install web dependencies: {e}")
        return False
    
    return True


def create_env_file():
    """Create .env file with secure defaults."""
    print_info("Creating environment configuration...")
    
    env_path = Path(".env")
    if env_path.exists():
        print_warning(".env file already exists")
        response = input("Do you want to overwrite it? (y/n): ").lower()
        if response != 'y':
            print_info("Keeping existing .env file")
            return True
    
    # Generate secret keys
    import secrets
    secret_key = secrets.token_hex(32)
    jwt_secret_key = secrets.token_hex(32)
    
    env_content = f"""# Environment Configuration for Disease Detection System
# Generated automatically by local_setup.py

# Flask Configuration
FLASK_ENV=development
DEBUG=True
SECRET_KEY={secret_key}
JWT_SECRET_KEY={jwt_secret_key}
JWT_EXPIRATION_HOURS=24

# Database Configuration (SQLite for local development)
DATABASE_URL=sqlite:///disease_detection.db

# Application Configuration
PORT=5000
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Security
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print_success(".env file created with secure random keys")
        return True
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return False


def initialize_database():
    """Initialize the database."""
    print_info("Initializing database...")
    
    python_cmd = get_python_command()
    
    try:
        # Create uploads directory
        os.makedirs("uploads", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Initialize database
        subprocess.run([python_cmd, "-c", "from app import init_db; init_db()"], 
                      check=True, capture_output=True)
        print_success("Database initialized")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to initialize database: {e}")
        return False


def run_system_test():
    """Run a quick system test."""
    print_info("Running system verification test...")
    
    python_cmd = get_python_command()
    
    try:
        # Run a simple inline test instead of relying on external test file
        test_code = """
import numpy as np
from eye_tracking import EyeTrackingData, DiseaseAnalyzer

# Generate test data
timestamps = np.linspace(0, 1000, 1000)
x_positions = 500 + np.random.normal(0, 2, 1000)
y_positions = 400 + np.random.normal(0, 2, 1000)

data = EyeTrackingData(timestamps, x_positions, y_positions, sampling_rate=1000.0)

# Analyze
analyzer = DiseaseAnalyzer()
results = analyzer.analyze(data)

# Verify results structure
assert 'disease_analysis' in results
assert 'summary' in results
assert 'parkinsons' in results['disease_analysis']

print('Test passed')
"""
        result = subprocess.run(
            [python_cmd, "-c", test_code],
            check=True,
            capture_output=True,
            text=True
        )
        print_success("System test passed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"System test failed: {e}")
        if e.stdout:
            print_error(e.stdout)
        if e.stderr:
            print_error(e.stderr)
        return False


def print_usage_instructions():
    """Print instructions for using the system."""
    python_cmd = get_python_command()
    
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print_header("Setup Complete!")
    
    print(f"{Colors.OKGREEN}The Eye Tracking Disease Detection System is ready to use!{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Quick Start:{Colors.ENDC}")
    print(f"  1. Activate the virtual environment:")
    print(f"     {Colors.OKCYAN}{activate_cmd}{Colors.ENDC}")
    print()
    print(f"  2. Run the example to verify installation:")
    print(f"     {Colors.OKCYAN}python example_usage.py{Colors.ENDC}")
    print()
    print(f"  3. Start the web application:")
    print(f"     {Colors.OKCYAN}python app.py{Colors.ENDC}")
    print(f"     Then open: {Colors.UNDERLINE}http://localhost:5000{Colors.ENDC}")
    print()
    
    print(f"{Colors.BOLD}Command-Line Interface:{Colors.ENDC}")
    print(f"  • Register an account:")
    print(f"    {Colors.OKCYAN}python cli.py register{Colors.ENDC}")
    print()
    print(f"  • Analyze sample eye tracking data:")
    print(f"    {Colors.OKCYAN}python cli.py analyze --sample{Colors.ENDC}")
    print()
    print(f"  • View your test results:")
    print(f"    {Colors.OKCYAN}python cli.py results{Colors.ENDC}")
    print()
    print(f"  • Get statistics:")
    print(f"    {Colors.OKCYAN}python cli.py stats{Colors.ENDC}")
    print()
    
    print(f"{Colors.BOLD}Python Library Usage:{Colors.ENDC}")
    print(f"  {Colors.OKCYAN}import numpy as np")
    print(f"  from eye_tracking import EyeTrackingData, DiseaseAnalyzer")
    print()
    print(f"  # Create sample data")
    print(f"  timestamps = np.linspace(0, 5000, 5000)")
    print(f"  x_pos = 500 + np.random.normal(0, 2, 5000)")
    print(f"  y_pos = 400 + np.random.normal(0, 2, 5000)")
    print()
    print(f"  data = EyeTrackingData(timestamps, x_pos, y_pos, sampling_rate=1000.0)")
    print()
    print(f"  # Analyze for diseases")
    print(f"  analyzer = DiseaseAnalyzer()")
    print(f"  results = analyzer.analyze(data)")
    print(f"  print(analyzer.generate_report(results)){Colors.ENDC}")
    print()
    
    print(f"{Colors.BOLD}Documentation:{Colors.ENDC}")
    print(f"  • README.md - Complete project documentation")
    print(f"  • API_DOCUMENTATION.md - Web API reference")
    print(f"  • DEPLOYMENT.md - Production deployment guide")
    print(f"  • PATIENT_GUIDE.md - User guide for patients")
    print()
    
    print(f"{Colors.BOLD}Need Help?{Colors.ENDC}")
    print(f"  • Check the README.md for detailed information")
    print(f"  • Run example_usage.py to see a working example")
    print(f"  • Visit: https://github.com/punit745/Disease_deteaction-")
    print()


def main():
    """Main setup function."""
    print_header("Eye Tracking Disease Detection System")
    print_header("Local Setup Wizard")
    
    print(f"{Colors.BOLD}This wizard will help you set up the system on your local machine.{Colors.ENDC}\n")
    print("The setup process includes:")
    print("  1. Python version verification")
    print("  2. Virtual environment creation")
    print("  3. Dependency installation")
    print("  4. Environment configuration")
    print("  5. Database initialization")
    print("  6. System verification")
    print()
    
    response = input(f"Continue with setup? ({Colors.OKGREEN}y{Colors.ENDC}/{Colors.FAIL}n{Colors.ENDC}): ").lower()
    if response != 'y':
        print_warning("Setup cancelled")
        return
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check pip
    if not check_pip_installed():
        sys.exit(1)
    
    # Step 3: Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Step 4: Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Step 5: Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Step 6: Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Step 7: Run system test
    if not run_system_test():
        print_warning("System test failed, but installation may still be usable")
    
    # Print usage instructions
    print_usage_instructions()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
