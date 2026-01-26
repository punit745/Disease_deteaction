# Local Deployment Guide
## Eye Tracking Disease Detection System

This guide provides comprehensive instructions for deploying and running the Eye Tracking Disease Detection System on your local machine.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start (Automated)](#quick-start-automated)
3. [Manual Installation](#manual-installation)
4. [Running the System](#running-the-system)
5. [Usage Examples](#usage-examples)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.7 or higher (Python 3.8+ recommended)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 2 GB free space
- **Display**: 1024x768 resolution minimum

### Software Prerequisites
- Python 3.7+ with pip
- Git (optional, for cloning the repository)
- Modern web browser (for web interface)

### Hardware Recommendations
For best performance:
- Modern CPU (Intel i5/AMD Ryzen 5 or better)
- 8 GB RAM or more
- SSD storage
- Internet connection (for initial setup only)

---

## Quick Start (Automated)

The easiest way to set up the system is using our automated setup script:

### Windows
```bash
# Open Command Prompt or PowerShell
python local_setup.py
```

### macOS/Linux
```bash
# Open Terminal
python3 local_setup.py
```

The setup wizard will:
1. ✓ Verify Python version
2. ✓ Create a virtual environment
3. ✓ Install all dependencies
4. ✓ Generate secure configuration
5. ✓ Initialize the database
6. ✓ Run system verification tests

**Setup time**: Approximately 2-5 minutes depending on your internet connection.

---

## Manual Installation

If you prefer manual installation or the automated script doesn't work:

### Step 1: Clone or Download the Repository

**Option A: Using Git**
```bash
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-
```

**Option B: Download ZIP**
1. Download the ZIP file from GitHub
2. Extract to a folder
3. Open terminal/command prompt in that folder

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt

# Install web application dependencies
pip install -r requirements-web.txt
```

### Step 4: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file with your preferred text editor
# At minimum, change the SECRET_KEY and JWT_SECRET_KEY
```

**For quick setup, use these commands to generate secure keys:**

**Windows PowerShell:**
```powershell
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))" >> .env
```

**macOS/Linux:**
```bash
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
echo "JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
```

### Step 5: Initialize Database

```bash
python -c "from app import init_db; init_db()"
```

### Step 6: Verify Installation

```bash
# Run a quick test
python example_usage.py
```

If you see the analysis report and visualization files are created, installation was successful!

---

## Running the System

### 1. Web Application

Start the Flask web server:

```bash
# Make sure virtual environment is activated
python app.py
```

The application will start on `http://localhost:5000`

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

Open your web browser and navigate to:
- API Health Check: http://localhost:5000/api/health
- API Documentation: See API_DOCUMENTATION.md

**To stop the server:** Press `Ctrl+C`

### 2. Command-Line Interface (CLI)

The CLI provides easy access to core functionality:

```bash
# Register a new user account
python cli.py register

# Analyze sample eye tracking data
python cli.py analyze --sample

# View your test results
python cli.py results

# Get detailed report for a specific test
python cli.py report <test_id>

# View statistics
python cli.py stats
```

### 3. Python Library (Programmatic Usage)

You can also use the system as a Python library:

```python
import numpy as np
from eye_tracking import EyeTrackingData, DiseaseAnalyzer

# Generate or load your eye tracking data
timestamps = np.linspace(0, 5000, 5000)  # 5 seconds at 1000 Hz
x_positions = 500 + np.random.normal(0, 2, 5000)
y_positions = 400 + np.random.normal(0, 2, 5000)

# Create data object
data = EyeTrackingData(
    timestamps=timestamps,
    x_positions=x_positions,
    y_positions=y_positions,
    sampling_rate=1000.0,
    subject_id="PATIENT_001",
    task_type="visual_search"
)

# Analyze for diseases
analyzer = DiseaseAnalyzer()
results = analyzer.analyze(data)

# Print comprehensive report
report = analyzer.generate_report(results)
print(report)

# Access specific disease risks
parkinsons_risk = results['disease_analysis']['parkinsons']['risk_score']
print(f"Parkinson's Risk: {parkinsons_risk:.2%}")
```

### 4. Interactive Example

Run the interactive example script:

```bash
python example_usage.py
```

This will:
- Generate synthetic eye tracking data
- Perform complete disease analysis
- Display a comprehensive report
- Create visualization plots (saved as PNG files)

---

## Usage Examples

### Example 1: Quick Health Screening

```bash
# 1. Register an account
python cli.py register

# Follow the prompts to enter your information

# 2. Analyze sample data
python cli.py analyze --sample

# 3. View results
python cli.py results
```

### Example 2: Web API Integration

```python
import requests

# Base URL
base_url = "http://localhost:5000"

# 1. Register
response = requests.post(f"{base_url}/api/auth/register", json={
    "email": "patient@example.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
})

# 2. Login
response = requests.post(f"{base_url}/api/auth/login", json={
    "email": "patient@example.com",
    "password": "SecurePassword123!"
})
token = response.json()["token"]

# 3. Analyze data
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{base_url}/api/analyze",
    json={
        "timestamps": [0, 1, 2, 3, 4, 5],
        "x_positions": [100, 102, 105, 108, 110, 112],
        "y_positions": [200, 198, 195, 193, 190, 188],
        "sampling_rate": 1000.0,
        "task_type": "visual_search"
    },
    headers=headers
)

results = response.json()
print(f"Overall Risk Level: {results['summary']['overall_risk_level']}")
```

### Example 3: Batch Analysis

```python
from eye_tracking import EyeTrackingData, DiseaseAnalyzer
import numpy as np

analyzer = DiseaseAnalyzer()

# Process multiple subjects
subjects = ["SUBJ_001", "SUBJ_002", "SUBJ_003"]

for subject_id in subjects:
    # Load or generate data for each subject
    timestamps = np.linspace(0, 5000, 5000)
    x_pos = 500 + np.random.normal(0, 2, 5000)
    y_pos = 400 + np.random.normal(0, 2, 5000)
    
    data = EyeTrackingData(
        timestamps=timestamps,
        x_positions=x_pos,
        y_positions=y_pos,
        sampling_rate=1000.0,
        subject_id=subject_id
    )
    
    results = analyzer.analyze(data)
    print(f"\n{subject_id}: {results['summary']['overall_risk_level']}")
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Python is not recognized"
**Solution:**
- Ensure Python is installed and added to PATH
- Try `python3` instead of `python` (macOS/Linux)
- Reinstall Python and check "Add to PATH" during installation

#### Issue: "pip: command not found"
**Solution:**
- Python 3.7+ includes pip by default
- Try `python -m pip` instead of `pip`
- Reinstall Python ensuring pip is included

#### Issue: "Module not found" errors
**Solution:**
```bash
# Make sure virtual environment is activated
# Look for (venv) in your command prompt

# Reinstall dependencies
pip install -r requirements.txt
pip install -r requirements-web.txt
```

#### Issue: Database initialization fails
**Solution:**
```bash
# Remove existing database
rm disease_detection.db  # macOS/Linux
del disease_detection.db  # Windows

# Reinitialize
python -c "from app import init_db; init_db()"
```

#### Issue: Port 5000 already in use
**Solution:**
```bash
# Option 1: Stop the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Option 2: Use a different port
# Edit .env file and change PORT=5000 to PORT=5001
```

#### Issue: Visualization plots not generated
**Solution:**
```bash
# Install matplotlib backend
pip install PyQt5

# Or use a non-interactive backend
# Add this to your Python script:
import matplotlib
matplotlib.use('Agg')
```

#### Issue: Import errors with eye_tracking module
**Solution:**
```bash
# Ensure you're in the project root directory
cd Disease_deteaction-

# Make sure __init__.py exists in eye_tracking folder
ls eye_tracking/__init__.py  # Should exist

# Try importing from Python:
python -c "from eye_tracking import DiseaseAnalyzer; print('OK')"
```

### Getting Help

If you encounter issues not covered here:

1. Check the main [README.md](README.md) for additional information
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
3. Look at [example_usage.py](example_usage.py) for working code
4. Check existing GitHub issues
5. Create a new issue with:
   - Your operating system
   - Python version (`python --version`)
   - Complete error message
   - Steps to reproduce

---

## Advanced Configuration

### Performance Tuning

Edit `.env` file to optimize performance:

```bash
# For faster processing (less accurate)
VELOCITY_THRESHOLD=40.0
ACCELERATION_THRESHOLD=10000.0

# For more accurate results (slower)
VELOCITY_THRESHOLD=20.0
ACCELERATION_THRESHOLD=6000.0
```

### Custom Database

To use PostgreSQL instead of SQLite (for production):

1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE disease_detection;
   ```
3. Update `.env`:
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/disease_detection
   ```

### Logging Configuration

Enable detailed logging:

```bash
# In .env file
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log

# Create logs directory
mkdir logs
```

View logs:
```bash
tail -f logs/app.log  # macOS/Linux
type logs\app.log     # Windows
```

### Security Hardening

For production deployment:

1. Generate strong secret keys (never use defaults!)
2. Use HTTPS (see DEPLOYMENT.md)
3. Enable rate limiting
4. Use PostgreSQL instead of SQLite
5. Set up regular backups
6. Review [DEPLOYMENT.md](DEPLOYMENT.md) for complete production guide

---

## What Can This System Do?

### Core Capabilities

#### 1. Multi-Disorder Detection
Analyzes eye tracking data to detect early signs of:
- **Parkinson's Disease**: Reduced saccade velocity, hypometric saccades
- **Alzheimer's Disease**: Prolonged fixations, impaired visual search
- **Autism Spectrum Disorder**: Atypical scan paths, reduced social attention
- **ADHD**: Shortened fixations, high spatial dispersion

#### 2. Comprehensive Analysis
- **Saccade Analysis**: Velocity, amplitude, duration, rate
- **Fixation Analysis**: Duration, count, spatial distribution
- **Pupil Analysis**: Size, dilation, variability
- **Spatial Analysis**: Coverage area, dispersion, scan patterns
- **Temporal Analysis**: Movement patterns over time

#### 3. Risk Assessment
- Quantitative risk scores (0.0 - 1.0 scale)
- Risk level categorization (Low/Moderate/High)
- Disease-specific indicators
- Clinical recommendations

#### 4. Data Visualization
- **Gaze Path Plots**: Visual representation of eye movements
- **Temporal Patterns**: Velocity and acceleration over time
- **Event Distributions**: Histograms of fixations and saccades
- **Risk Score Charts**: Bar charts comparing disease risks
- **Heatmaps**: Attention distribution maps

#### 5. Multiple Interfaces
- **Web API**: RESTful API for integration with other systems
- **Command-Line**: CLI for scripting and automation
- **Python Library**: Programmatic access for custom applications
- **Interactive Examples**: Pre-built demonstrations

### Use Cases

1. **Clinical Screening**: Healthcare providers can screen patients
2. **Research**: Researchers can analyze eye tracking datasets
3. **Monitoring**: Track changes in eye movement patterns over time
4. **Integration**: Embed in existing healthcare systems via API
5. **Education**: Learn about eye tracking and disease indicators

### Limitations

⚠️ **Important Disclaimers:**
- This is a **screening tool**, not a diagnostic tool
- Results should be reviewed by healthcare professionals
- Individual variation in eye movements is significant
- Environmental and task factors affect measurements
- Always consult qualified medical professionals for diagnosis

---

## Next Steps

After successful installation:

1. ✓ Run `python example_usage.py` to verify everything works
2. ✓ Read [PATIENT_GUIDE.md](PATIENT_GUIDE.md) if you're a patient/user
3. ✓ Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API integration
4. ✓ Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
5. ✓ Star the GitHub repository if you find this useful!

---

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/punit745/Disease_deteaction-
- Documentation: See README.md and other .md files

---

**Remember**: This system is designed to assist healthcare professionals and researchers. It is not a replacement for professional medical diagnosis. Always consult qualified healthcare providers for medical advice.
