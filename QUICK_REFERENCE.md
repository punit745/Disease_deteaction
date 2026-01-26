# Quick Reference Guide
## Eye Tracking Disease Detection System

This is a quick reference for common tasks and commands.

---

## Installation

### One-Command Setup
```bash
python3 local_setup.py
```

### Verify Installation
```bash
python3 validate_system.py
```

---

## Running the System

### 1. Example Script (Simplest)
```bash
python example_usage.py
```
- Generates sample data
- Runs analysis
- Creates visualizations
- Shows comprehensive report

### 2. Interactive Demo (Recommended for Learning)
```bash
python interactive_demo.py
```
- Menu-driven interface
- Compare different scenarios
- Custom analysis options
- Real-time results

### 3. Web Application (For API Access)
```bash
python app.py
```
- API available at http://localhost:5000
- Health check: http://localhost:5000/api/health

### 4. Command-Line Interface
```bash
# Register an account
python cli.py register

# Analyze sample data
python cli.py analyze --sample

# View results
python cli.py results

# Get help
python cli.py --help
```

---

## Python API Quick Examples

### Basic Analysis
```python
import numpy as np
from eye_tracking import EyeTrackingData, DiseaseAnalyzer

# Create data
timestamps = np.linspace(0, 5000, 5000)
x_pos = 500 + np.random.normal(0, 2, 5000)
y_pos = 400 + np.random.normal(0, 2, 5000)

data = EyeTrackingData(timestamps, x_pos, y_pos, sampling_rate=1000.0)

# Analyze
analyzer = DiseaseAnalyzer()
results = analyzer.analyze(data)

# Print report
print(analyzer.generate_report(results))
```

### Access Specific Results
```python
# Get overall risk
overall_risk = results['summary']['overall_risk_level']

# Get Parkinson's risk score
parkinsons_score = results['disease_analysis']['parkinsons']['risk_score']

# Get all detected indicators
indicators = results['disease_analysis']['parkinsons']['indicators']
```

### Generate Visualizations
```python
from eye_tracking.visualizer import Visualizer
from eye_tracking.preprocessor import EyeTrackingPreprocessor

preprocessor = EyeTrackingPreprocessor()
processed_data = preprocessor.process(data)

visualizer = Visualizer()
visualizer.plot_gaze_path(processed_data, save_path='gaze.png')
visualizer.plot_risk_scores(results, save_path='risk.png')
```

---

## REST API Quick Examples

### Register & Login
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Analyze Data
```bash
# Get token from login response first
TOKEN="your-jwt-token-here"

# Analyze
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "timestamps": [0, 1, 2, 3, 4, 5],
    "x_positions": [100, 102, 105, 108, 110, 112],
    "y_positions": [200, 198, 195, 193, 190, 188],
    "sampling_rate": 1000.0,
    "task_type": "visual_search"
  }'
```

---

## File Locations

### Important Files
- `README.md` - Main documentation
- `LOCAL_DEPLOYMENT_GUIDE.md` - Detailed local setup guide
- `API_DOCUMENTATION.md` - Complete API reference
- `DEPLOYMENT.md` - Production deployment guide
- `PATIENT_GUIDE.md` - User guide for patients

### Scripts
- `local_setup.py` - Automated setup wizard
- `validate_system.py` - System validation
- `interactive_demo.py` - Interactive demonstration
- `example_usage.py` - Basic example
- `cli.py` - Command-line interface
- `app.py` - Web application

### Configuration
- `.env` - Environment configuration (created by setup)
- `requirements.txt` - Core dependencies
- `requirements-web.txt` - Web dependencies

### Output
- `disease_detection.db` - SQLite database
- `uploads/` - Uploaded files
- `logs/` - Application logs
- `*.png` - Generated visualizations

---

## Common Tasks

### Start Fresh
```bash
# Remove database
rm disease_detection.db

# Reinitialize
python -c "from app import init_db; init_db()"
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip install --upgrade -r requirements-web.txt
```

### Check Logs
```bash
# If logging is enabled
tail -f logs/app.log
```

### Stop Web Server
```bash
# Press Ctrl+C in the terminal running app.py
# Or find and kill the process
lsof -ti:5000 | xargs kill -9  # macOS/Linux
```

---

## Disease Detection Reference

### Supported Disorders
1. **Parkinson's Disease**
   - Key indicators: Reduced saccade velocity, hypometric saccades, prolonged fixations
   - Threshold: Mean saccade velocity < 300 deg/s

2. **Alzheimer's Disease**
   - Key indicators: Significantly prolonged fixations, reduced visual exploration
   - Threshold: Mean fixation duration > 350 ms

3. **Autism Spectrum Disorder (ASD)**
   - Key indicators: High fixation variability, atypical spatial patterns
   - Threshold: Fixation duration std > 200 ms

4. **ADHD**
   - Key indicators: Shortened fixations, high spatial dispersion
   - Threshold: Mean fixation duration < 150 ms

### Risk Levels
- **Low**: Risk score < 0.3
- **Moderate**: Risk score 0.3 - 0.6
- **High**: Risk score > 0.6

---

## Troubleshooting Quick Fixes

### "Module not found"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
pip install -r requirements-web.txt
```

### "Port already in use"
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows (find PID, then taskkill)
```

### "Database error"
```bash
# Remove and recreate database
rm disease_detection.db
python -c "from app import init_db; init_db()"
```

### Visualizations not working
```bash
# Install Qt backend
pip install PyQt5

# Or use non-interactive backend (add to script)
import matplotlib
matplotlib.use('Agg')
```

---

## Data Format Requirements

### Minimum Requirements
- **Timestamps**: Array of time points in milliseconds
- **X/Y Positions**: Arrays of screen coordinates
- **Sampling Rate**: Recording frequency in Hz
- **Minimum Duration**: 1000 ms (1 second)
- **Minimum Samples**: 100 data points

### Recommended
- **Duration**: 3000-10000 ms (3-10 seconds)
- **Sampling Rate**: 500-1000 Hz
- **Data Quality**: < 10% missing/invalid samples
- **Task Type**: Specified (e.g., "visual_search", "reading", "social")

### Optional
- **Pupil Size**: Pupil diameter measurements
- **Subject ID**: Patient/subject identifier
- **Session ID**: Recording session identifier

---

## Performance Tips

1. **Large Datasets**: Process in batches
2. **Visualization**: Use `matplotlib.use('Agg')` for headless servers
3. **Database**: Use PostgreSQL for production (faster than SQLite)
4. **API**: Enable caching for repeated analyses
5. **Memory**: Close visualization figures after saving

---

## Getting Help

1. **Documentation**: Check README.md and guides
2. **Validation**: Run `python validate_system.py`
3. **Example**: Study `example_usage.py`
4. **Issues**: GitHub issues page
5. **Logs**: Check application logs in `logs/`

---

## Important Reminders

⚠️ **This is a screening tool, not a diagnostic tool**
- Results require professional medical review
- Individual variation is significant
- Environmental factors matter
- Always consult healthcare professionals

✓ **Best Practices**
- Use high-quality eye tracking hardware
- Standardize testing conditions
- Record multiple sessions for reliability
- Document task types and conditions
- Review results with medical professionals

---

**Quick Links:**
- [Full README](README.md)
- [Local Deployment Guide](LOCAL_DEPLOYMENT_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Patient Guide](PATIENT_GUIDE.md)
