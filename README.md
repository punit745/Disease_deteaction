# Eye Tracking Disease Detection System

A production-ready web application for detecting early signs of neurological and developmental disorders using eye movement pattern analysis. Built for patients, healthcare providers, and researchers.

## Overview

This project focuses on using eye-tracking data to diagnose early signs of neurological or developmental disorders such as:

- **Parkinson's Disease**: Reduced saccade velocity, hypometric saccades, increased fixation duration
- **Alzheimer's Disease**: Increased saccade latency, impaired visual search, prolonged fixations
- **Autism Spectrum Disorder (ASD)**: Atypical scan paths, reduced social attention, atypical fixation patterns
- **ADHD**: Shortened fixations, elevated saccade rate, high spatial dispersion

Eye movement patterns can highlight cognitive, neurological, or behavioral anomalies, enabling early screening and intervention.

## Features

### Core Disease Detection
- **Multi-disorder Analysis**: Simultaneous screening for Parkinson's, Alzheimer's, ASD, and ADHD
- **Risk Scoring**: Quantitative risk assessment for each disorder
- **Clinical Indicators**: Identification of specific disorder markers
- **Recommendations**: Actionable recommendations based on risk levels

### Production Web Application (NEW!)
- **REST API**: Complete RESTful API for integration
- **User Authentication**: Secure JWT-based authentication system
- **Patient Profiles**: User registration and profile management
- **Test History**: Track and analyze results over time
- **Dashboard**: View test history and risk trends
- **Secure Storage**: HIPAA-compliant data handling and encryption
- **Rate Limiting**: API protection against abuse
- **Health Monitoring**: Built-in health check endpoints

### Data Processing
- **Noise Removal**: Savitzky-Golay and median filtering
- **Event Detection**: Automatic detection of fixations, saccades, and smooth pursuit
- **Feature Extraction**: Comprehensive extraction of eye movement features

### Visualization
- **Gaze Path Plotting**: Visual representation of eye movements
- **Temporal Patterns**: Velocity and acceleration analysis
- **Event Distributions**: Statistical distribution of fixations and saccades
- **Risk Assessment Charts**: Clear visualization of disorder risk scores

### Deployment Ready
- **Docker Support**: Containerized deployment with Docker Compose
- **Database Integration**: PostgreSQL for production data storage
- **Nginx Configuration**: Reverse proxy with SSL/TLS support
- **CI/CD Ready**: GitHub Actions workflow compatible
- **Monitoring**: Comprehensive logging and error tracking
- **Scalability**: Horizontal and vertical scaling support

## Installation

### Quick Start - Automated Setup (Recommended for Local Use)

The easiest way to get started on your local machine:

```bash
# Clone the repository
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-

# Run the automated setup wizard
python3 local_setup.py
```

The setup wizard will:
- ✓ Verify Python version and dependencies
- ✓ Create a virtual environment
- ✓ Install all required packages
- ✓ Generate secure configuration
- ✓ Initialize the database
- ✓ Run system validation tests

**Total setup time**: 2-5 minutes

For detailed local deployment instructions, see [LOCAL_DEPLOYMENT_GUIDE.md](LOCAL_DEPLOYMENT_GUIDE.md)

### Quick Start with Docker (Recommended for Production)

```bash
# Clone the repository
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-

# Start all services (web app, database, nginx)
docker-compose up -d

# Initialize database
docker-compose exec web python -c "from app import init_db; init_db()"

# Access the application
# API: http://localhost:5000
# Web: http://localhost:80
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-web.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python -c "from app import init_db; init_db()"

# Run the application
python app.py
```

## Requirements

- Python 3.7+
- numpy >= 1.21.0
- pandas >= 1.3.0
- scipy >= 1.7.0
- scikit-learn >= 0.24.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0

## Quick Start

### Using the Web API

```python
import requests

# Base URL
base_url = "http://localhost:5000"

# 1. Register a patient account
response = requests.post(f"{base_url}/api/auth/register", json={
    "email": "patient@example.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
})

# 2. Login and get token
response = requests.post(f"{base_url}/api/auth/login", json={
    "email": "patient@example.com",
    "password": "SecurePassword123!"
})
token = response.json()["token"]

# 3. Analyze eye tracking data
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{base_url}/api/analyze", 
    json={
        "timestamps": [0, 1, 2, ...],
        "x_positions": [100, 102, 105, ...],
        "y_positions": [200, 198, 195, ...],
        "sampling_rate": 1000.0,
        "task_type": "visual_search"
    },
    headers=headers
)
results = response.json()

# 4. View test history
response = requests.get(f"{base_url}/api/results", headers=headers)
test_history = response.json()
```

### Using the Command-Line Interface

```bash
# Register
python cli.py register

# Analyze sample data
python cli.py analyze --sample

# View results
python cli.py results

# Get detailed report
python cli.py report <test_id>

# View statistics
python cli.py stats
```

### Using the Python Library (Standalone)

```python
import numpy as np
from eye_tracking import EyeTrackingData, DiseaseAnalyzer

# Create eye tracking data
timestamps = np.array([0, 1, 2, 3, 4, ...])  # milliseconds
x_positions = np.array([100, 102, 105, ...])  # x-coordinates
y_positions = np.array([200, 198, 195, ...])  # y-coordinates

data = EyeTrackingData(
    timestamps=timestamps,
    x_positions=x_positions,
    y_positions=y_positions,
    sampling_rate=1000.0,  # Hz
    subject_id="SUBJECT_001",
    task_type="visual_search"
)

# Analyze for all disorders
analyzer = DiseaseAnalyzer()
results = analyzer.analyze(data)

# Generate report
report = analyzer.generate_report(results)
print(report)
```

### Running the Example Script

```bash
python example_usage.py
```

This will:
1. Generate synthetic eye tracking data
2. Perform disease analysis
3. Display a comprehensive diagnostic report
4. Create visualization plots

### Interactive Demo (NEW!)

Try our interactive demo to explore different scenarios:

```bash
python interactive_demo.py
```

Features:
- Compare normal vs. disease-simulated patterns
- Run custom analyses with your parameters
- Generate visualizations for multiple scenarios
- Interactive menu system for easy exploration

### System Validation

Verify your installation is working correctly:

```bash
python validate_system.py
```

This will check:
- Python version and dependencies
- All required files
- Core module functionality
- Database connectivity
- Visualization capabilities

## Data Structure

### EyeTrackingData

The main data container for eye tracking recordings:

```python
EyeTrackingData(
    timestamps,        # numpy array of timestamps (ms)
    x_positions,       # numpy array of x-coordinates
    y_positions,       # numpy array of y-coordinates
    pupil_sizes=None,  # optional pupil diameter measurements
    sampling_rate=1000.0,  # sampling rate in Hz
    subject_id=None,   # subject identifier
    session_id=None,   # session identifier
    task_type=None,    # task description
)
```

## Analysis Pipeline

1. **Preprocessing**
   - Noise removal using filtering techniques
   - Detection of saccades using velocity and acceleration thresholds
   - Detection of fixations as periods between saccades

2. **Feature Extraction**
   - Saccade features: amplitude, velocity, duration, rate
   - Fixation features: duration, count, spatial distribution
   - Spatial features: coverage area, dispersion
   - Pupil features: size, variability
   - Temporal features: velocity, acceleration patterns

3. **Disease Detection**
   - Pattern matching against disorder-specific markers
   - Risk score calculation (0.0 - 1.0)
   - Risk level categorization (Low/Moderate/High)
   - Clinical recommendations based on findings

4. **Reporting**
   - Comprehensive text reports
   - Visual analytics and charts
   - Actionable recommendations

## Disease-Specific Indicators

### Parkinson's Disease
- Reduced saccade velocity (< 300 deg/s)
- Hypometric saccades (undershooting)
- Prolonged fixations (> 300 ms)
- Reduced saccade rate (< 2 per second)

### Alzheimer's Disease
- Significantly prolonged fixations (> 350 ms)
- Reduced visual exploration
- High saccade variability
- Reduced saccade rate (< 1.5 per second)

### Autism Spectrum Disorder
- High fixation duration variability (> 200 ms std)
- Atypical spatial attention patterns
- Elevated saccade velocity (> 500 deg/s)
- Elevated saccade rate (> 4 per second)

### ADHD
- Shortened fixations (< 150 ms)
- Elevated saccade rate (> 4 per second)
- High spatial dispersion
- High movement variability

## Visualization Examples

```python
from eye_tracking.visualizer import Visualizer

visualizer = Visualizer()

# Plot gaze path
visualizer.plot_gaze_path(processed_data, save_path='gaze_path.png')

# Plot temporal patterns
visualizer.plot_temporal_patterns(processed_data, save_path='temporal.png')

# Plot event distributions
visualizer.plot_event_distribution(processed_data, save_path='events.png')

# Plot risk scores
visualizer.plot_risk_scores(results, save_path='risk_scores.png')
```

## Advanced Usage

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:
- Docker deployment
- Ubuntu/Debian server setup
- SSL/TLS configuration
- Database setup and backups
- Security best practices
- Monitoring and maintenance

### API Integration

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference including:
- All endpoints with examples
- Authentication flow
- Request/response formats
- Error handling
- Rate limiting
- Code examples in Python, JavaScript, and cURL

### Analyzing Specific Disorders

```python
# Analyze only for Parkinson's and Alzheimer's
results = analyzer.analyze(data, diseases=['parkinsons', 'alzheimers'])
```

### Custom Preprocessing Parameters

```python
from eye_tracking.preprocessor import EyeTrackingPreprocessor

preprocessor = EyeTrackingPreprocessor(
    velocity_threshold=30.0,        # deg/s
    acceleration_threshold=8000.0,  # deg/s²
    fixation_min_duration=100.0     # ms
)

processed_data = preprocessor.process(data)
```

### Accessing Detailed Features

```python
from eye_tracking.feature_extractor import FeatureExtractor

extractor = FeatureExtractor()
features = extractor.extract_all_features(processed_data)

print(f"Mean saccade velocity: {features['mean_saccade_velocity']:.2f} deg/s")
print(f"Mean fixation duration: {features['mean_fixation_duration']:.2f} ms")
```

## Important Notes

- **Screening Tool**: This system is designed for screening purposes only, not for clinical diagnosis
- **Professional Consultation**: Always consult healthcare professionals for proper diagnosis
- **Data Quality**: Results depend on quality of eye tracking data
- **Individual Variation**: Eye movement patterns vary significantly between individuals
- **Context Matters**: Task type and environmental factors affect eye movements

## Project Structure

```
Disease_deteaction-/
├── eye_tracking/               # Core analysis library
│   ├── __init__.py
│   ├── data_models.py         # Data structures
│   ├── preprocessor.py        # Data preprocessing
│   ├── feature_extractor.py   # Feature extraction
│   ├── disease_detectors.py   # Disease-specific detectors
│   ├── analyzer.py            # Main analyzer
│   └── visualizer.py          # Visualization tools
├── app.py                      # Flask web application
├── cli.py                      # Command-line interface
├── example_usage.py            # Example script
├── interactive_demo.py         # Interactive demo (NEW!)
├── local_setup.py             # Automated setup wizard (NEW!)
├── validate_system.py         # System validation script (NEW!)
├── requirements.txt            # Core dependencies
├── requirements-web.txt        # Web app dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Multi-container orchestration
├── nginx.conf                  # Nginx configuration
├── .env.example               # Environment variables template
├── README.md                  # This file
├── LOCAL_DEPLOYMENT_GUIDE.md  # Local deployment guide (NEW!)
├── API_DOCUMENTATION.md       # Complete API reference
└── DEPLOYMENT.md              # Production deployment guide
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open-source and available for research and educational purposes.

## Citation

If you use this system in your research, please cite:

```
Eye Tracking Disease Detection System
https://github.com/punit745/Disease_deteaction-
```

## Disclaimer

This software is provided for research and educational purposes only. It is not intended for clinical diagnosis or medical decision-making. Always consult qualified healthcare professionals for medical advice and diagnosis.

## References

- Neurological disorder detection through eye movements
- Eye tracking methodology in cognitive assessment
- Oculomotor dysfunction in neurodegenerative diseases
- Visual attention patterns in developmental disorders