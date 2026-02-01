# NeuroScan: AI-Powered Eye Tracking Disease Detection System

<div align="center">

![NeuroScan Banner](https://img.shields.io/badge/NeuroScan-Eye%20Tracking%20AI-8b5cf6?style=for-the-badge&logo=eye&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)

**A production-ready web application for early detection of neurological and developmental disorders through AI-powered eye movement pattern analysis.**

[Live Demo](http://localhost:5000) · [Documentation](#documentation) · [Report Bug](https://github.com/punit745/Disease_deteaction/issues)

</div>

---

## 📄 Abstract

Early detection of neurological and developmental disorders is crucial for timely intervention and improved patient outcomes. This project presents **NeuroScan**, an innovative web-based screening system that leverages eye movement pattern analysis to identify early biomarkers of **Parkinson's Disease**, **Alzheimer's Disease**, **Autism Spectrum Disorder (ASD)**, and **Attention Deficit Hyperactivity Disorder (ADHD)**.

Eye movements serve as a window into cognitive and neurological function. Disruptions in oculomotor control—such as altered saccade velocity, abnormal fixation duration, and atypical scan paths—have been clinically associated with various neurological conditions. Our system captures and analyzes these patterns through a multi-stage pipeline:

1. **Data Preprocessing**: Noise filtering and event detection (fixations, saccades, smooth pursuit)
2. **Feature Extraction**: Computation of 20+ eye movement metrics including velocity, amplitude, duration, and spatial dispersion
3. **Disease-Specific Analysis**: Rule-based detection using clinically-validated thresholds
4. **Risk Assessment**: Quantitative scoring with actionable recommendations

The system provides a user-friendly web interface for patients, a comprehensive REST API for healthcare integration, and detailed diagnostic reports for clinical review. Built with Flask, SQLAlchemy, and modern frontend technologies, NeuroScan offers a scalable, secure, and accessible approach to neurological screening.

> **⚠️ Disclaimer**: This system is designed for **screening purposes only** and does not replace professional medical diagnosis. Always consult qualified healthcare professionals for clinical evaluation.

---

## 🎯 Key Features

### 🔬 Multi-Disorder Detection
| Disorder | Key Indicators Detected |
|----------|------------------------|
| **Parkinson's Disease** | Reduced saccade velocity, hypometric saccades, prolonged fixations |
| **Alzheimer's Disease** | Increased saccade latency, impaired visual search, reduced exploration |
| **Autism Spectrum Disorder** | Atypical scan paths, high fixation variability, elevated saccade rate |
| **ADHD** | Shortened fixations, elevated saccade rate, high spatial dispersion |

### 🌐 Modern Web Application
- **Beautiful UI**: Dark-themed, responsive design with smooth animations
- **User Dashboard**: Personal test history, risk trends, and statistics
- **Patient Profiles**: Secure account management with JWT authentication
- **Real-time Analysis**: Instant results with detailed breakdowns

### 🔧 Technical Capabilities
- **REST API**: Complete API for third-party integration
- **Docker Support**: One-command deployment with Docker Compose
- **Database**: SQLite for development, PostgreSQL for production
- **Security**: HIPAA-compliant data handling, encrypted storage

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/punit745/Disease_deteaction.git
cd Disease_deteaction

# Run the setup wizard
python local_setup.py
```

The wizard will automatically:
- ✅ Verify Python version (3.7+)
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Configure environment variables
- ✅ Initialize database
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
pip install -r requirements-web.txt

# Configure environment
cp .env.example .env

# Initialize database
python -c "from app import init_db; init_db()"

# Run the application
python app.py
```

### Option 3: Docker Deployment

```bash
# Start all services
docker-compose up -d

# Access the application
# Web UI: http://localhost:80
# API: http://localhost:5000
```

---

## 💻 Usage

### Web Interface

1. **Open Browser**: Navigate to `http://localhost:5000`
2. **Create Account**: Click "Get Started" and register
3. **Login**: Access your personal dashboard
4. **Run Analysis**: Choose a test type and start screening
5. **View Results**: See detailed risk breakdown and recommendations

### Command-Line Interface

```bash
# Register new account
python cli.py register

# Run sample analysis
python cli.py analyze --sample

# View test history
python cli.py results

# Get detailed report
python cli.py report <test_id>

# View statistics
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

# Analyze for all disorders
analyzer = DiseaseAnalyzer()
results = analyzer.analyze(data)

# Generate human-readable report
report = analyzer.generate_report(results)
print(report)
```

### REST API

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Register
requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": "patient@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
})

# 2. Login
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "email": "patient@example.com",
    "password": "SecurePass123!"
})
token = response.json()["token"]

# 3. Analyze
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
```

---

## 🧠 How It Works

### Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RAW EYE TRACKING DATA                        │
│              [timestamps, x_positions, y_positions]                 │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     STEP 1: PREPROCESSING                           │
│  • Noise removal (Savitzky-Golay filter)                           │
│  • Velocity & acceleration computation                              │
│  • Event detection (fixations, saccades, smooth pursuit)           │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 2: FEATURE EXTRACTION                        │
│  • Saccade metrics: velocity, amplitude, duration, rate            │
│  • Fixation metrics: duration, count, variability                  │
│  • Spatial metrics: coverage area, dispersion                      │
│  • Temporal metrics: acceleration, jerk patterns                   │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 STEP 3: DISEASE-SPECIFIC ANALYSIS                   │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐         │
│  │ Parkinson's │ Alzheimer's │     ASD     │    ADHD     │         │
│  │   Detector  │   Detector  │   Detector  │   Detector  │         │
│  └─────────────┴─────────────┴─────────────┴─────────────┘         │
└─────────────────────────────┬───────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 4: RISK ASSESSMENT                          │
│  • Risk score calculation (0.0 - 1.0)                              │
│  • Risk level categorization (Low / Moderate / High)               │
│  • Clinical indicator identification                                │
│  • Actionable recommendations                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Disease-Specific Thresholds

| Metric | Parkinson's | Alzheimer's | ASD | ADHD |
|--------|-------------|-------------|-----|------|
| Saccade Velocity | < 300 deg/s ⚠️ | - | > 500 deg/s ⚠️ | - |
| Fixation Duration | > 300 ms ⚠️ | > 350 ms ⚠️ | High variability ⚠️ | < 150 ms ⚠️ |
| Saccade Rate | < 2/sec ⚠️ | < 1.5/sec ⚠️ | > 4/sec ⚠️ | > 4/sec ⚠️ |
| Spatial Coverage | - | Reduced ⚠️ | - | > 50000 px² ⚠️ |

---

## 📁 Project Structure

```
Disease_deteaction/
├── 📂 eye_tracking/              # Core analysis library
│   ├── __init__.py
│   ├── data_models.py           # Data structures
│   ├── preprocessor.py          # Signal processing
│   ├── feature_extractor.py     # Feature computation
│   ├── disease_detectors.py     # Disease-specific logic
│   ├── analyzer.py              # Main orchestrator
│   └── visualizer.py            # Plotting utilities
│
├── 📂 templates/                 # HTML templates
│   ├── index.html               # Landing page
│   └── dashboard.html           # User dashboard
│
├── 📂 static/                    # Frontend assets
│   ├── css/
│   │   ├── style.css            # Main styles
│   │   └── dashboard.css        # Dashboard styles
│   └── js/
│       ├── app.js               # Core JavaScript
│       └── dashboard.js         # Dashboard logic
│
├── 📄 app.py                     # Flask application
├── 📄 cli.py                     # Command-line interface
├── 📄 local_setup.py             # Automated setup wizard
├── 📄 validate_system.py         # System validation
├── 📄 example_usage.py           # Usage examples
├── 📄 interactive_demo.py        # Interactive demo
│
├── 📄 requirements.txt           # Core dependencies
├── 📄 requirements-web.txt       # Web dependencies
├── 📄 Dockerfile                 # Docker image
├── 📄 docker-compose.yml         # Docker orchestration
├── 📄 nginx.conf                 # Nginx configuration
└── 📄 .env.example               # Environment template
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete REST API reference |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment guide |
| [LOCAL_DEPLOYMENT_GUIDE.md](LOCAL_DEPLOYMENT_GUIDE.md) | Local setup instructions |
| [PATIENT_GUIDE.md](PATIENT_GUIDE.md) | Guide for patients |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick reference card |

---

## ⚙️ API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/health` | Health check | ❌ |
| `POST` | `/api/auth/register` | Register new user | ❌ |
| `POST` | `/api/auth/login` | Login & get token | ❌ |
| `GET` | `/api/user/profile` | Get user profile | ✅ |
| `PUT` | `/api/user/profile` | Update profile | ✅ |
| `POST` | `/api/analyze` | Analyze eye data | ✅ |
| `GET` | `/api/results` | Get all results | ✅ |
| `GET` | `/api/results/<id>` | Get specific result | ✅ |
| `GET` | `/api/results/<id>/report` | Get detailed report | ✅ |
| `GET` | `/api/statistics` | Get user statistics | ✅ |

---

## 🔒 Security & Privacy

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Werkzeug security with salt
- **CORS Protection**: Configurable cross-origin policies
- **Rate Limiting**: API abuse prevention
- **Data Encryption**: Sensitive data protection
- **HIPAA Considerations**: Healthcare data handling best practices

---

## 🧪 Testing

```bash
# Run system validation
python validate_system.py

# Run interactive demo
python interactive_demo.py

# Run example analysis
python example_usage.py
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 📖 Citation

If you use this system in your research, please cite:

```bibtex
@software{neuroscan2024,
  title={NeuroScan: AI-Powered Eye Tracking Disease Detection System},
  author={Punit},
  year={2024},
  url={https://github.com/punit745/Disease_deteaction}
}
```

---

## ⚠️ Disclaimer

This software is provided for **research and educational purposes only**. It is **not intended for clinical diagnosis** or medical decision-making. The risk scores and recommendations generated by this system should not replace professional medical evaluation.

**Always consult qualified healthcare professionals for:**
- Medical diagnosis
- Treatment decisions
- Clinical interpretation of results

---

## 📚 References

1. Leigh, R. J., & Zee, D. S. (2015). *The Neurology of Eye Movements*. Oxford University Press.
2. Anderson, T. J., & MacAskill, M. R. (2013). Eye movements in patients with neurodegenerative disorders. *Nature Reviews Neurology*, 9(2), 74-85.
3. Karatekin, C. (2007). Eye tracking studies of normative and atypical development. *Developmental Review*, 27(3), 283-348.
4. Itti, L., & Koch, C. (2001). Computational modelling of visual attention. *Nature Reviews Neuroscience*, 2(3), 194-203.

---

<div align="center">

**Built with ❤️ for healthcare innovation**

[⬆ Back to Top](#neuroscan-ai-powered-eye-tracking-disease-detection-system)

</div>