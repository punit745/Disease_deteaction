"""
Example usage of the Eye Tracking Disease Detection System.

This script demonstrates how to use the system to analyze eye tracking data
and detect neurological and developmental disorders.
"""

import numpy as np
from eye_tracking import (
    EyeTrackingData,
    DiseaseAnalyzer,
)
from eye_tracking.visualizer import Visualizer


def generate_sample_data(duration_ms: float = 5000, sampling_rate: float = 1000.0):
    """
    Generate synthetic eye tracking data for demonstration.
    
    Args:
        duration_ms: Duration of recording in milliseconds
        sampling_rate: Sampling rate in Hz
    
    Returns:
        EyeTrackingData object with synthetic data
    """
    num_samples = int(duration_ms * sampling_rate / 1000)
    timestamps = np.linspace(0, duration_ms, num_samples)
    
    # Generate synthetic gaze positions with some fixations and saccades
    x_positions = np.zeros(num_samples)
    y_positions = np.zeros(num_samples)
    
    # Add some fixations with noise
    current_x, current_y = 500, 400
    for i in range(num_samples):
        # Add small noise for fixations
        x_positions[i] = current_x + np.random.normal(0, 2)
        y_positions[i] = current_y + np.random.normal(0, 2)
        
        # Randomly make saccades
        if np.random.random() < 0.01:  # 1% chance of saccade per sample
            current_x += np.random.normal(0, 50)
            current_y += np.random.normal(0, 50)
            # Keep within screen bounds
            current_x = np.clip(current_x, 100, 900)
            current_y = np.clip(current_y, 100, 700)
    
    # Generate synthetic pupil sizes
    pupil_sizes = 3.0 + 0.5 * np.sin(2 * np.pi * timestamps / 1000) + np.random.normal(0, 0.1, num_samples)
    
    return EyeTrackingData(
        timestamps=timestamps,
        x_positions=x_positions,
        y_positions=y_positions,
        pupil_sizes=pupil_sizes,
        sampling_rate=sampling_rate,
        subject_id="DEMO_001",
        session_id="SESSION_001",
        task_type="visual_search"
    )


def main():
    """Main example function."""
    print("=" * 70)
    print("Eye Tracking Disease Detection System - Example Usage")
    print("=" * 70)
    print()
    
    # Generate sample data
    print("1. Generating sample eye tracking data...")
    eye_data = generate_sample_data(duration_ms=5000, sampling_rate=1000.0)
    print(f"   Generated {eye_data.num_samples} samples over {eye_data.duration:.1f} ms")
    print()
    
    # Initialize analyzer
    print("2. Initializing disease analyzer...")
    analyzer = DiseaseAnalyzer()
    print("   Analyzer ready with detectors for:")
    print("   - Parkinson's Disease")
    print("   - Alzheimer's Disease")
    print("   - Autism Spectrum Disorder (ASD)")
    print("   - ADHD")
    print()
    
    # Perform analysis
    print("3. Analyzing eye tracking data...")
    results = analyzer.analyze(eye_data)
    print("   Analysis complete!")
    print()
    
    # Generate and display report
    print("4. Generating diagnostic report...")
    print()
    report = analyzer.generate_report(results)
    print(report)
    print()
    
    # Create visualizations
    print("5. Creating visualizations...")
    visualizer = Visualizer()
    
    # Get processed data from results for visualization
    from eye_tracking.preprocessor import EyeTrackingPreprocessor
    preprocessor = EyeTrackingPreprocessor()
    processed_data = preprocessor.process(eye_data)
    
    try:
        print("   - Plotting gaze path...")
        visualizer.plot_gaze_path(processed_data, save_path='gaze_path.png')
        print("     Saved: gaze_path.png")
        
        print("   - Plotting temporal patterns...")
        visualizer.plot_temporal_patterns(processed_data, save_path='temporal_patterns.png')
        print("     Saved: temporal_patterns.png")
        
        print("   - Plotting event distributions...")
        visualizer.plot_event_distribution(processed_data, save_path='event_distribution.png')
        print("     Saved: event_distribution.png")
        
        print("   - Plotting risk scores...")
        visualizer.plot_risk_scores(results, save_path='risk_scores.png')
        print("     Saved: risk_scores.png")
    except Exception as e:
        print(f"   Note: Visualization generation skipped (display may not be available)")
        print(f"   Error: {e}")
    
    print()
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
