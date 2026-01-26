# Eye Tracking Disease Detection System
## Project Summary & Deployment Guide

### Overview

This Eye Tracking Disease Detection System is a comprehensive, production-ready application designed to analyze eye movement patterns for early detection of neurological and developmental disorders. The system uses sophisticated algorithms to detect indicators of:

- **Parkinson's Disease** - Reduced saccade velocity, hypometric saccades
- **Alzheimer's Disease** - Prolonged fixations, impaired visual search
- **Autism Spectrum Disorder (ASD)** - Atypical scan paths, reduced social attention
- **ADHD** - Shortened fixations, elevated spatial dispersion

---

## What This System Can Do

### Core Capabilities

1. **Eye Movement Analysis**
   - Saccade detection and characterization (velocity, amplitude, duration)
   - Fixation analysis (duration, distribution, patterns)
   - Pupil dilation measurement and tracking
   - Spatial pattern recognition
   - Temporal pattern analysis

2. **Disease Detection**
   - Multi-disorder screening (4 disorders simultaneously)
   - Quantitative risk scoring (0.0 - 1.0 scale)
   - Risk level categorization (Low/Moderate/High)
   - Disease-specific indicator identification
   - Clinical recommendations based on findings

3. **Data Processing**
   - Noise filtering (Savitzky-Golay, median filtering)
   - Automatic event detection
   - Feature extraction (20+ eye movement features)
   - Statistical analysis
   - Pattern matching

4. **Visualization**
   - Gaze path plots showing eye movement trajectories
   - Temporal pattern charts (velocity, acceleration)
   - Event distribution histograms
   - Risk score bar charts
   - Heat maps of attention distribution

5. **Multiple Interfaces**
   - **Web API**: RESTful API with JWT authentication
   - **CLI**: Command-line interface for scripting
   - **Python Library**: Direct programmatic access
   - **Interactive Demo**: User-friendly exploration tool

---

## Running on Your Local System

### Prerequisites

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.7+ (Python 3.8+ recommended)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 2 GB free space

### Quick Setup (Automated - Recommended)

```bash
# 1. Clone or download the repository
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-

# 2. Run the automated setup wizard
python3 local_setup.py

# 3. Verify installation
python3 validate_system.py

# 4. Try the interactive demo
python3 interactive_demo.py
```

That's it! The setup wizard handles everything:
- Creates virtual environment
- Installs all dependencies
- Generates secure configuration
- Initializes database
- Runs system tests

**Setup time**: 2-5 minutes

### Manual Setup

If you prefer manual installation:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-web.txt

# 3. Initialize database
python -c "from app import init_db; init_db()"

# 4. Run example
python example_usage.py
```

---

## How to Use the System

### Option 1: Quick Demo (Easiest)

```bash
python example_usage.py
```

This will:
- Generate sample eye tracking data
- Perform complete disease analysis
- Display comprehensive report
- Create visualization plots
- Show all capabilities

**Time**: ~10 seconds

### Option 2: Interactive Demo (Best for Learning)

```bash
python interactive_demo.py
```

Features:
- Menu-driven interface
- Compare different scenarios (Normal, Parkinson's, ADHD)
- Custom analysis with your parameters
- Real-time results and visualizations
- Educational explanations

**Perfect for**: Understanding how the system works

### Option 3: Web API (For Applications)

```bash
# Start the web server
python app.py
```

Then access at http://localhost:5000

Example API usage:
```python
import requests

# Register
requests.post("http://localhost:5000/api/auth/register", json={
    "email": "user@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
})

# Login
resp = requests.post("http://localhost:5000/api/auth/login", json={
    "email": "user@example.com",
    "password": "SecurePass123!"
})
token = resp.json()["token"]

# Analyze eye tracking data
resp = requests.post("http://localhost:5000/api/analyze",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "timestamps": [0, 1, 2, 3, 4, 5],
        "x_positions": [100, 102, 105, 108, 110, 112],
        "y_positions": [200, 198, 195, 193, 190, 188],
        "sampling_rate": 1000.0
    }
)
results = resp.json()
```

**Perfect for**: Integrating with other systems, building applications

### Option 4: Command-Line Interface

```bash
# Register an account
python cli.py register

# Analyze sample data
python cli.py analyze --sample

# View results
python cli.py results

# Get statistics
python cli.py stats
```

**Perfect for**: Automation, batch processing, scripting

### Option 5: Python Library (For Developers)

```python
import numpy as np
from eye_tracking import EyeTrackingData, DiseaseAnalyzer

# Create or load your eye tracking data
timestamps = np.linspace(0, 5000, 5000)  # 5 seconds
x_positions = 500 + np.random.normal(0, 2, 5000)
y_positions = 400 + np.random.normal(0, 2, 5000)

data = EyeTrackingData(
    timestamps=timestamps,
    x_positions=x_positions,
    y_positions=y_positions,
    sampling_rate=1000.0,
    subject_id="PATIENT_001",
    task_type="visual_search"
)

# Analyze for all disorders
analyzer = DiseaseAnalyzer()
results = analyzer.analyze(data)

# Print detailed report
print(analyzer.generate_report(results))

# Access specific results
parkinsons_risk = results['disease_analysis']['parkinsons']['risk_score']
print(f"Parkinson's Risk: {parkinsons_risk:.2%}")
```

**Perfect for**: Custom applications, research, integration

---

## System Architecture

### Data Flow

```
Eye Tracking Hardware
        ↓
Raw Data (timestamps, x/y positions, pupil size)
        ↓
EyeTrackingData Object
        ↓
Preprocessing (noise filtering, event detection)
        ↓
Feature Extraction (20+ features)
        ↓
Disease Analyzers (4 detectors)
        ↓
Risk Scoring & Recommendations
        ↓
Reports & Visualizations
```

### Components

1. **eye_tracking/** - Core analysis library
   - `data_models.py` - Data structures
   - `preprocessor.py` - Signal processing
   - `feature_extractor.py` - Feature computation
   - `disease_detectors.py` - Disease-specific analysis
   - `analyzer.py` - Main analysis coordinator
   - `visualizer.py` - Visualization generation

2. **Web Application**
   - `app.py` - Flask web server with REST API
   - User authentication (JWT)
   - Database storage (SQLite/PostgreSQL)
   - Result tracking

3. **Command-Line Tools**
   - `cli.py` - Interactive CLI
   - `local_setup.py` - Setup wizard
   - `validate_system.py` - System validation
   - `interactive_demo.py` - Interactive demo
   - `example_usage.py` - Basic example

---

## Key Features Explained

### 1. Multi-Disorder Detection

The system simultaneously analyzes for 4 disorders:

**Parkinson's Disease Indicators**:
- Mean saccade velocity < 300 deg/s (reduced)
- Hypometric saccades (undershooting targets)
- Mean fixation duration > 300 ms (prolonged)
- Saccade rate < 2 per second (reduced)

**Alzheimer's Disease Indicators**:
- Mean fixation duration > 350 ms (significantly prolonged)
- Reduced visual exploration
- Saccade rate < 1.5 per second (significantly reduced)
- High saccade variability

**ASD Indicators**:
- Fixation duration std > 200 ms (high variability)
- Atypical spatial attention patterns
- Mean saccade velocity > 500 deg/s (elevated)
- Saccade rate > 4 per second (elevated)

**ADHD Indicators**:
- Mean fixation duration < 150 ms (shortened)
- Saccade rate > 4 per second (elevated)
- High spatial dispersion
- High movement variability

### 2. Risk Scoring

Each disorder receives a risk score from 0.0 to 1.0:
- **0.0 - 0.3**: Low risk (few or no indicators)
- **0.3 - 0.6**: Moderate risk (some indicators)
- **0.6 - 1.0**: High risk (multiple indicators)

Scoring is based on:
- Number of indicators detected
- Severity of each indicator
- Combination of indicators
- Task-specific patterns

### 3. Data Visualization

Four types of visualizations:

1. **Gaze Path Plot**: Shows eye movement trajectory over time
2. **Temporal Patterns**: Velocity and acceleration charts
3. **Event Distribution**: Histograms of fixations and saccades
4. **Risk Scores**: Bar chart comparing disease risks

All visualizations saved as PNG files for review and documentation.

---

## Data Requirements

### Minimum Requirements

- **Format**: Timestamps and X/Y coordinates
- **Duration**: At least 1 second (1000 ms)
- **Samples**: Minimum 100 data points
- **Sampling Rate**: 100 Hz or higher (500-1000 Hz recommended)

### Input Data Structure

```python
{
    "timestamps": [0, 1, 2, 3, ...],       # milliseconds
    "x_positions": [100, 102, 105, ...],   # screen coordinates
    "y_positions": [200, 198, 195, ...],   # screen coordinates
    "pupil_sizes": [3.0, 3.1, 3.2, ...],   # optional, mm
    "sampling_rate": 1000.0,               # Hz
    "subject_id": "PATIENT_001",           # optional
    "task_type": "visual_search"           # optional
}
```

### Recommended

- **Duration**: 3-10 seconds
- **Sampling Rate**: 500-1000 Hz
- **Data Quality**: < 10% missing samples
- **Task Type**: Specified (improves accuracy)
- **Multiple Sessions**: For reliable screening

---

## Documentation Files

- **README.md** - Main project documentation
- **LOCAL_DEPLOYMENT_GUIDE.md** - Detailed local setup guide
- **QUICK_REFERENCE.md** - Quick command reference
- **API_DOCUMENTATION.md** - Complete API reference
- **DEPLOYMENT.md** - Production deployment guide
- **PATIENT_GUIDE.md** - User guide for patients
- **PROJECT_SUMMARY.md** - This file

---

## Important Disclaimers

⚠️ **This is a screening tool, NOT a diagnostic tool**

- Results are for screening purposes only
- Not intended for clinical diagnosis
- Always consult qualified healthcare professionals
- Individual variation in eye movements is significant
- Environmental and task factors affect measurements

✓ **Best Practices**

- Use high-quality eye tracking hardware
- Standardize testing conditions
- Record multiple sessions for reliability
- Document task types and conditions
- Review results with medical professionals
- Consider individual baseline variations

---

## Troubleshooting

### Common Issues

**"Module not found" errors**:
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
pip install -r requirements-web.txt
```

**"Port 5000 already in use"**:
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows
```

**Visualizations not working**:
```bash
pip install PyQt5
# Or use non-interactive backend:
import matplotlib
matplotlib.use('Agg')
```

**Database errors**:
```bash
rm disease_detection.db
python -c "from app import init_db; init_db()"
```

For more help, see `LOCAL_DEPLOYMENT_GUIDE.md` or run:
```bash
python validate_system.py
```

---

## Performance Notes

- **Analysis Time**: ~100-500ms per sample (depending on data size)
- **Memory Usage**: ~100-200 MB typical
- **Disk Space**: ~10 MB per test result
- **Concurrent Users**: 10-100 (with proper server setup)

For production deployment, see `DEPLOYMENT.md` for:
- Docker deployment
- PostgreSQL configuration
- Nginx reverse proxy
- SSL/TLS setup
- Scaling strategies

---

## Support and Contribution

- **GitHub**: https://github.com/punit745/Disease_deteaction-
- **Issues**: Use GitHub Issues for bug reports
- **Documentation**: See .md files in repository
- **Contributions**: Pull requests welcome!

---

## License

This project is open-source and available for research and educational purposes.

---

## Citation

If you use this system in your research:

```
Eye Tracking Disease Detection System
https://github.com/punit745/Disease_deteaction-
```

---

**Built for researchers, healthcare providers, and developers working on neurological and developmental disorder screening.**

*Last Updated: January 2026*
