#!/usr/bin/env python3
"""
Model Training Script for Disease Detection.

This script trains ML models for each disease using synthetic training data
based on clinical research about eye movement patterns.

Usage:
    python train_models.py

The trained models will be saved to the 'models' directory.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_dependencies():
    """Check if required ML dependencies are installed."""
    missing = []
    
    try:
        import sklearn
        print(f"✓ scikit-learn {sklearn.__version__} installed")
    except ImportError:
        missing.append('scikit-learn')
        print("✗ scikit-learn not installed")
    
    try:
        import xgboost
        print(f"✓ XGBoost {xgboost.__version__} installed")
    except ImportError:
        print("⚠ XGBoost not installed (optional - will use Random Forest only)")
    
    try:
        import numpy as np
        print(f"✓ NumPy {np.__version__} installed")
    except ImportError:
        missing.append('numpy')
        print("✗ NumPy not installed")
    
    if missing:
        print(f"\n❌ Missing required dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    return True


def main():
    """Main training function."""
    print("=" * 60)
    print("  NeuroScan ML Model Training")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print()
    
    # Import training function
    from eye_tracking.ml_models import train_all_models, get_ensemble_classifier
    
    # Create models directory
    model_dir = project_root / 'models'
    model_dir.mkdir(exist_ok=True)
    print(f"Model directory: {model_dir}")
    print()
    
    # Train models
    print("Training ML models for disease detection...")
    print("-" * 60)
    
    try:
        results = train_all_models(
            model_dir=str(model_dir),
            n_samples=3000  # 3000 samples per disease
        )
        
        print()
        print("=" * 60)
        print("  Training Complete!")
        print("=" * 60)
        print()
        
        # Print summary
        print("Model Performance Summary:")
        print("-" * 40)
        
        for disease, metrics in results.items():
            rf_acc = metrics['rf_accuracy'] * 100
            print(f"\n{disease.upper()}:")
            print(f"  Random Forest:  {rf_acc:.1f}% accuracy")
            
            if metrics.get('xgb_accuracy'):
                xgb_acc = metrics['xgb_accuracy'] * 100
                print(f"  XGBoost:        {xgb_acc:.1f}% accuracy")
            
            print(f"  Training set:   {metrics['train_samples']} samples")
            print(f"  Test set:       {metrics['test_samples']} samples")
        
        print()
        print("-" * 40)
        print(f"✓ Models saved to: {model_dir}")
        print()
        
        # Verify models load correctly
        print("Verifying model loading...")
        ensemble = get_ensemble_classifier(str(model_dir))
        
        all_trained = True
        for disease in ['parkinsons', 'alzheimers', 'asd', 'adhd']:
            if ensemble.is_trained(disease):
                print(f"  ✓ {disease} model loaded successfully")
            else:
                print(f"  ✗ {disease} model failed to load")
                all_trained = False
        
        if all_trained:
            print()
            print("=" * 60)
            print("  All models trained and verified successfully!")
            print("  ML-based disease detection is now available.")
            print("=" * 60)
        
        # Quick test prediction
        print()
        print("Running test prediction with sample features...")
        
        test_features = {
            'mean_fixation_duration': 280,
            'std_fixation_duration': 90,
            'fixation_count': 45,
            'mean_saccade_amplitude': 7,
            'std_saccade_amplitude': 3.5,
            'mean_saccade_velocity': 320,
            'std_saccade_velocity': 100,
            'saccade_rate': 2.8,
            'saccade_count': 42,
            'coverage_area': 28000,
            'x_mean': 510,
            'y_mean': 390,
            'x_std': 95,
            'y_std': 75,
            'mean_velocity': 45,
            'std_velocity': 55,
            'max_velocity': 480,
            'total_distance': 4800
        }
        
        predictions = ensemble.predict_all(test_features)
        
        print()
        print("Test Predictions (sample healthy-like features):")
        for disease, score in predictions.items():
            if score is not None:
                risk_level = "Low" if score < 0.3 else ("Moderate" if score < 0.6 else "High")
                print(f"  {disease}: {score*100:.1f}% risk ({risk_level})")
        
        print()
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
