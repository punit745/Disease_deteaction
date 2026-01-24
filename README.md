# Eye Tracking Disease Detection System

A comprehensive Python system for detecting early signs of neurological and developmental disorders using eye movement pattern analysis.

## Overview

This project focuses on using eye-tracking data to diagnose early signs of neurological or developmental disorders such as:

- **Parkinson's Disease**: Reduced saccade velocity, hypometric saccades, increased fixation duration
- **Alzheimer's Disease**: Increased saccade latency, impaired visual search, prolonged fixations
- **Autism Spectrum Disorder (ASD)**: Atypical scan paths, reduced social attention, atypical fixation patterns
- **ADHD**: Shortened fixations, elevated saccade rate, high spatial dispersion

Eye movement patterns can highlight cognitive, neurological, or behavioral anomalies, enabling early screening and intervention.

## Features

### Data Processing
- **Noise Removal**: Savitzky-Golay and median filtering
- **Event Detection**: Automatic detection of fixations, saccades, and smooth pursuit
- **Feature Extraction**: Comprehensive extraction of eye movement features

### Disease Detection
- **Multi-disorder Analysis**: Simultaneous screening for multiple disorders
- **Risk Scoring**: Quantitative risk assessment for each disorder
- **Clinical Indicators**: Identification of specific disorder markers
- **Recommendations**: Actionable recommendations based on risk levels

### Visualization
- **Gaze Path Plotting**: Visual representation of eye movements
- **Temporal Patterns**: Velocity and acceleration analysis
- **Event Distributions**: Statistical distribution of fixations and saccades
- **Risk Assessment Charts**: Clear visualization of disorder risk scores

## Installation

```bash
# Clone the repository
git clone https://github.com/punit745/Disease_deteaction-.git
cd Disease_deteaction-

# Install dependencies
pip install -r requirements.txt
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

### Basic Usage

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

### Running the Example

```bash
python example_usage.py
```

This will:
1. Generate synthetic eye tracking data
2. Perform disease analysis
3. Display a comprehensive diagnostic report
4. Create visualization plots

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
├── eye_tracking/
│   ├── __init__.py              # Package initialization
│   ├── data_models.py           # Data structures
│   ├── preprocessor.py          # Data preprocessing
│   ├── feature_extractor.py    # Feature extraction
│   ├── disease_detectors.py    # Disease-specific detectors
│   ├── analyzer.py             # Main analyzer
│   └── visualizer.py           # Visualization tools
├── example_usage.py            # Example script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
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