# NeuroScan: AI-Powered Eye Tracking Disease Detection System

<div align="center">

![NeuroScan Banner](https://img.shields.io/badge/NeuroScan-Eye%20Tracking%20AI-8b5cf6?style=for-the-badge&logo=eye&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![CI](https://github.com/punit745/Disease_deteaction/actions/workflows/ci.yml/badge.svg)](https://github.com/punit745/Disease_deteaction/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=flat-square)](CHANGELOG.md)

**An innovative web-based screening system for early detection of neurological and developmental disorders through AI-powered eye movement pattern analysis.**

[Quick Start](#-quick-start) · [Features](#-key-features) · [Documentation](#-documentation) · [API Reference](API_DOCUMENTATION.md)

</div>

---

## 📄 Abstract

Neurological and developmental disorders—including **Parkinson's Disease**, **Alzheimer's Disease**, **Autism Spectrum Disorder (ASD)**, and **Attention Deficit Hyperactivity Disorder (ADHD)**—affect millions of people worldwide. Early detection is critical for timely intervention, improved treatment outcomes, and enhanced quality of life. However, traditional diagnostic methods often require expensive equipment, specialized clinical settings, and extensive time from healthcare professionals.

**NeuroScan** addresses these challenges by leveraging the well-established relationship between eye movements and cognitive/neurological function. Scientific research has demonstrated that oculomotor control disruptions—such as altered saccade velocity, abnormal fixation patterns, and atypical visual scan paths—serve as reliable early biomarkers for various neurological conditions.

### Technical Approach

Our system implements a sophisticated four-stage analysis pipeline:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. DATA PREPROCESSING                                                       │
│     • Noise filtering (Savitzky-Golay, median filters)                       │
│     • Velocity & acceleration computation                                     │
│     • Eye movement event detection (fixations, saccades, smooth pursuit)     │
├─────────────────────────────────────────────────────────────────────────────┤
│  2. FEATURE EXTRACTION                                                        │
│     • 20+ quantitative eye movement metrics                                   │
│     • Saccade: velocity, amplitude, duration, rate, latency                  │
│     • Fixation: duration, count, spatial variability                         │
│     • Spatial: coverage area, dispersion, scan path complexity               │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. DISEASE-SPECIFIC ANALYSIS                                                │
│     • Rule-based detection using clinically-validated thresholds             │
│     • Optional ML models (Random Forest, Gradient Boosting, XGBoost)         │
│     • Four specialized detectors for each target disorder                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. RISK ASSESSMENT & REPORTING                                              │
│     • Quantitative risk scores (0.0 - 1.0)                                   │
│     • Risk categorization (Low / Moderate / High)                            │
│     • Clinical indicator identification                                       │
│     • PDF report generation with visualizations                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Differentiators

| Aspect | Traditional Screening | NeuroScan |
|--------|----------------------|-----------|
| **Equipment** | Specialized clinical devices | Standard webcam/eye tracker |
| **Setting** | Hospital/clinic visits | Home or office |
| **Cost** | High | Minimal |
| **Time** | Hours to days for results | Real-time analysis |
| **Accessibility** | Limited by location | Web-accessible globally |
| **Historical Tracking** | Fragmented records | Integrated progress dashboard |

> [!CAUTION]
> **Medical Disclaimer**: NeuroScan is designed for **screening purposes only** and does not replace professional medical diagnosis. The risk assessments and recommendations generated should be interpreted by qualified healthcare professionals. Always consult a physician or specialist for clinical evaluation and treatment decisions.

---

## 🎯 Key Features

### 🔬 Multi-Disorder Detection

| Disorder | Key Eye Movement Indicators |
|----------|----------------------------|
| **Parkinson's Disease** | Reduced saccade velocity (<300 deg/s), hypometric saccades, prolonged fixations (>300ms), square-wave jerks |
| **Alzheimer's Disease** | Increased saccade latency, impaired visual search, reduced spatial exploration, prolonged fixations (>350ms) |
| **Autism Spectrum Disorder** | Atypical scan paths, high fixation variability, elevated saccade rate (>4/sec), reduced social gaze |
| **ADHD** | Shortened fixations (<150ms), elevated saccade rate, high spatial dispersion (>50000 px²), difficulty sustaining attention |

### 📊 Progress Tracking Dashboard *(New in v2.0)*

- **Health Trend Visualization**: Interactive charts showing risk score changes over time
- **Multi-Disease Tracking**: Compare trends across all four disorders simultaneously
- **Statistical Summaries**: Average scores, improvement indicators, test frequency metrics
- **Export Capabilities**: Download progress data for sharing with healthcare providers

### 🌐 Modern Web Application

- **Responsive Design**: Dark-themed UI optimized for all device sizes
- **User Dashboard**: Personal test history, risk trends, and comprehensive statistics
- **Secure Accounts**: JWT-based authentication with encrypted password storage
- **Real-time Analysis**: Instant results with detailed risk breakdowns
- **PDF Reports**: Professional reports suitable for clinical review

### 🔧 Technical Capabilities

- **REST API**: Complete API for third-party integration and automation
- **Docker Support**: Production-ready containerization with Docker Compose
- **Database Options**: SQLite for development, PostgreSQL for production
- **ML Integration**: Optional machine learning models for enhanced accuracy
- **Webcam Eye Tracking**: Browser-based eye tracking using WebGazer.js

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/punit745/Disease_deteaction.git
cd Disease_deteaction

# Run the setup wizard
python local_setup.py
```

The wizard will automatically:
- ✅ Verify Python version compatibility
- ✅ Create and activate virtual environment
- ✅ Install all dependencies
- ✅ Configure environment variables
- ✅ Initialize the database
- ✅ Run validation tests

### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/punit745/Disease_deteaction.git
cd Disease_deteaction

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Initialize database
python -c "from app import init_db; init_db()"

# Run the application
python app.py
```

### Option 3: Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# Access the application
# Web UI: http://localhost:80
# API: http://localhost:5000

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 💻 Usage Guide

### Web Interface

1. **Navigate** to `http://localhost:5000`
2. **Create Account**: Click "Get Started" to register
3. **Login**: Access your personal dashboard
4. **Take Eye Test**: Use the webcam-based eye tracking test
5. **View Results**: See detailed risk breakdown and recommendations
6. **Track Progress**: Monitor your health trends over time

### Command-Line Interface

```bash
# Register new account
python cli.py register

# Run sample analysis
python cli.py analyze --sample

# View test history
python cli.py results

# Get detailed report for a specific test
python cli.py report <test_id>

# View statistics summary
python cli.py stats
```

### Python Library

```python
import numpy as np
from eye_tracking import EyeTrackingData, DiseaseAnalyzer

# Create eye tracking data
data = EyeTrackingData(
    timestamps=np.linspace(0, 5000, 5000),
    x_positions=np.random.normal(500, 50, 5000),
    y_positions=np.random.normal(400, 40, 5000),
    sampling_rate=1000.0,
    subject_id="PATIENT_001",
    task_type="visual_search"
)

# Initialize analyzer and run analysis
analyzer = DiseaseAnalyzer()
results = analyzer.analyze(data)

# Generate human-readable report
report = analyzer.generate_report(results)
print(report)

# Access specific disease results
print(f"Parkinson's Risk: {results['disease_analysis']['parkinsons']['risk_score']:.2%}")
print(f"Overall Risk Level: {results['summary']['risk_level']}")
```

### REST API

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Register a new user
requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": "patient@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
})

# 2. Login to get authentication token
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "email": "patient@example.com",
    "password": "SecurePass123!"
})
token = response.json()["token"]

# 3. Submit eye tracking data for analysis
headers = {"Authorization": f"Bearer {token}"}
results = requests.post(f"{BASE_URL}/api/analyze", 
    json={
        "timestamps": [0, 1, 2, 3, ...],
        "x_positions": [100, 102, 105, ...],
        "y_positions": [200, 198, 195, ...],
        "sampling_rate": 1000.0
    },
    headers=headers
).json()

# 4. Retrieve all past results
history = requests.get(f"{BASE_URL}/api/results", headers=headers).json()

# 5. Download PDF report
pdf = requests.get(f"{BASE_URL}/api/results/{test_id}/pdf", headers=headers)
```

---

## 📁 Project Structure

```
Disease_deteaction/
│
├── 📂 eye_tracking/                 # Core analysis library
│   ├── __init__.py                  # Package exports (v2.0.0)
│   ├── data_models.py               # Data structures (EyeTrackingData, EyeMovementEvent)
│   ├── preprocessor.py              # Signal processing & noise removal
│   ├── feature_extractor.py         # 20+ feature computation
│   ├── disease_detectors.py         # Four disease-specific detectors
│   ├── analyzer.py                  # Main orchestrator
│   ├── ml_models.py                 # Machine learning models
│   ├── visualizer.py                # Plotting utilities
│   └── pdf_report.py                # PDF report generation
│
├── 📂 templates/                     # HTML templates
│   ├── index.html                   # Landing page
│   ├── dashboard.html               # User dashboard with progress tracking
│   └── eye_test.html                # Webcam eye tracking test
│
├── 📂 static/                        # Frontend assets
│   ├── css/
│   │   ├── style.css                # Landing page styles
│   │   ├── dashboard.css            # Dashboard styles
│   │   └── eye_test.css             # Eye test page styles
│   └── js/
│       ├── app.js                   # Core JavaScript
│       ├── dashboard.js             # Dashboard + progress charts
│       └── eye_test.js              # Eye tracking logic
│
├── 📂 models/                        # Trained ML models (optional)
│
├── 📄 app.py                         # Flask application (API + Web routes)
├── 📄 cli.py                         # Command-line interface
├── 📄 local_setup.py                 # Automated setup wizard
├── 📄 validate_system.py             # System validation script
├── 📄 test_system.py                 # Unit and integration tests
├── 📄 example_usage.py               # Usage examples
├── 📄 interactive_demo.py            # Interactive demonstration
├── 📄 train_models.py                # ML model training script
│
├── 📄 requirements.txt               # Python dependencies
├── 📄 requirements-web.txt           # Production dependencies (gunicorn, psycopg2)
├── 📄 Dockerfile                     # Docker image configuration
├── 📄 docker-compose.yml             # Multi-container orchestration
├── 📄 nginx.conf                     # Nginx reverse proxy config
├── 📄 .env.example                   # Environment template
└── 📄 .gitignore                     # Git exclusions
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete REST API reference with examples |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment guide (Docker, nginx, SSL) |
| [LOCAL_DEPLOYMENT_GUIDE.md](LOCAL_DEPLOYMENT_GUIDE.md) | Detailed local setup instructions |
| [PATIENT_GUIDE.md](PATIENT_GUIDE.md) | User guide for patients |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick reference card |
| [CHANGELOG.md](CHANGELOG.md) | Version history and changes |

---

## ⚙️ API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/health` | Health check | ❌ |
| `POST` | `/api/auth/register` | Register new user | ❌ |
| `POST` | `/api/auth/login` | Login & get JWT token | ❌ |
| `GET` | `/api/user/profile` | Get user profile | ✅ |
| `PUT` | `/api/user/profile` | Update profile | ✅ |
| `POST` | `/api/analyze` | Submit eye data for analysis | ✅ |
| `GET` | `/api/results` | Get all test results | ✅ |
| `GET` | `/api/results/<id>` | Get specific result | ✅ |
| `GET` | `/api/results/<id>/report` | Get detailed text report | ✅ |
| `GET` | `/api/results/<id>/pdf` | Download PDF report | ✅ |
| `GET` | `/api/statistics` | Get user statistics | ✅ |

---

## 🔒 Security & Privacy

- **JWT Authentication**: Secure token-based authentication with configurable expiration
- **Password Hashing**: Werkzeug security with salted hashes
- **CORS Protection**: Configurable cross-origin resource sharing policies
- **Environment Variables**: Sensitive configuration stored securely
- **Data Encryption**: Support for encrypted data storage in production
- **HIPAA Considerations**: Architecture designed with healthcare data best practices

---

## 🧪 Testing

```bash
# Run system validation (recommended first step)
python validate_system.py

# Run interactive demo
python interactive_demo.py

# Run example analysis
python example_usage.py

# Run unit tests
python -m pytest test_system.py -v

# Run with coverage
python -m pytest test_system.py --cov=eye_tracking --cov-report=html
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Add type hints to all function signatures
- Write docstrings for all public functions and classes
- Include unit tests for new functionality
- Update documentation as needed

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 📖 Citation

If you use NeuroScan in your research, please cite:

```bibtex
@software{neuroscan2026,
  author       = {Punit},
  title        = {NeuroScan: AI-Powered Eye Tracking Disease Detection System},
  version      = {2.0.0},
  year         = {2026},
  url          = {https://github.com/punit745/Disease_deteaction},
  note         = {A web-based screening system for early detection of neurological 
                  and developmental disorders through eye movement pattern analysis}
}
```

---

## ⚠️ Disclaimer

This software is provided for **research, educational, and screening purposes only**. It is **not intended for clinical diagnosis** or medical decision-making.

**The system CANNOT:**
- Replace professional medical evaluation
- Provide definitive diagnosis of any condition
- Serve as the sole basis for treatment decisions

**Always consult qualified healthcare professionals for:**
- Medical diagnosis
- Treatment recommendations
- Clinical interpretation of screening results

---

## 📚 Scientific References

1. Leigh, R. J., & Zee, D. S. (2015). *The Neurology of Eye Movements* (5th ed.). Oxford University Press.

2. Anderson, T. J., & MacAskill, M. R. (2013). Eye movements in patients with neurodegenerative disorders. *Nature Reviews Neurology*, 9(2), 74-85. https://doi.org/10.1038/nrneurol.2012.273

3. Karatekin, C. (2007). Eye tracking studies of normative and atypical development. *Developmental Review*, 27(3), 283-348. https://doi.org/10.1016/j.dr.2007.06.006

4. Itti, L., & Koch, C. (2001). Computational modelling of visual attention. *Nature Reviews Neuroscience*, 2(3), 194-203. https://doi.org/10.1038/35058500

5. Stuart, S., et al. (2019). Eye-tracking in Parkinson's disease: Objective assessment of saccadic and smooth pursuit function. *Journal of the Neurological Sciences*, 396, 114-118.

---

<div align="center">

**Built with ❤️ for healthcare innovation**

[⬆ Back to Top](#neuroscan-ai-powered-eye-tracking-disease-detection-system)

</div>