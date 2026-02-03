"""
Machine Learning Models for Disease Detection.

This module provides ML-based classifiers using Random Forest, XGBoost,
and ensemble methods for more accurate disease risk prediction.
"""

import os
import pickle
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# Try to import ML libraries
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


# Feature names used for training and prediction
FEATURE_NAMES = [
    'mean_fixation_duration',
    'std_fixation_duration',
    'fixation_count',
    'mean_saccade_amplitude',
    'std_saccade_amplitude',
    'mean_saccade_velocity',
    'std_saccade_velocity',
    'saccade_rate',
    'saccade_count',
    'coverage_area',
    'x_mean',
    'y_mean',
    'x_std',
    'y_std',
    'mean_velocity',
    'std_velocity',
    'max_velocity',
    'total_distance'
]


class MLDiseaseClassifier:
    """
    Machine Learning classifier for a specific disease.
    Uses ensemble of Random Forest and optionally XGBoost.
    """
    
    def __init__(self, disease_name: str, model_dir: str = 'models'):
        """
        Initialize the classifier.
        
        Args:
            disease_name: Name of the disease (parkinsons, alzheimers, asd, adhd)
            model_dir: Directory to save/load models
        """
        self.disease_name = disease_name
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.scaler: Optional[StandardScaler] = None
        self.rf_model: Optional[RandomForestClassifier] = None
        self.xgb_model: Optional[Any] = None
        self.is_trained = False
        
        # Try to load existing model
        self._load_model()
    
    def _get_model_path(self) -> Path:
        """Get the path for saving/loading the model."""
        return self.model_dir / f'{self.disease_name}_classifier.pkl'
    
    def _load_model(self) -> bool:
        """
        Load a trained model from disk.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        model_path = self._get_model_path()
        
        if model_path.exists():
            try:
                with open(model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.scaler = data.get('scaler')
                    self.rf_model = data.get('rf_model')
                    self.xgb_model = data.get('xgb_model')
                    self.is_trained = True
                    return True
            except Exception as e:
                print(f"Error loading model for {self.disease_name}: {e}")
                return False
        return False
    
    def save_model(self) -> bool:
        """
        Save the trained model to disk.
        
        Returns:
            True if saved successfully, False otherwise
        """
        if not self.is_trained:
            return False
        
        try:
            model_path = self._get_model_path()
            with open(model_path, 'wb') as f:
                pickle.dump({
                    'scaler': self.scaler,
                    'rf_model': self.rf_model,
                    'xgb_model': self.xgb_model
                }, f)
            return True
        except Exception as e:
            print(f"Error saving model for {self.disease_name}: {e}")
            return False
    
    def train(self, X: np.ndarray, y: np.ndarray, 
              test_size: float = 0.2) -> Dict[str, float]:
        """
        Train the classifier on the provided data.
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Labels (0 = healthy, 1 = disease indicators present)
            test_size: Proportion of data to use for testing
            
        Returns:
            Dictionary with training metrics
        """
        if not ML_AVAILABLE:
            raise RuntimeError("scikit-learn is not installed")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Initialize and fit scaler
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(X_train_scaled, y_train)
        rf_pred = self.rf_model.predict(X_test_scaled)
        rf_accuracy = accuracy_score(y_test, rf_pred)
        
        # Train XGBoost if available
        xgb_accuracy = None
        if XGBOOST_AVAILABLE:
            self.xgb_model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            )
            self.xgb_model.fit(X_train_scaled, y_train)
            xgb_pred = self.xgb_model.predict(X_test_scaled)
            xgb_accuracy = accuracy_score(y_test, xgb_pred)
        
        self.is_trained = True
        self.save_model()
        
        return {
            'rf_accuracy': rf_accuracy,
            'xgb_accuracy': xgb_accuracy,
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict_proba(self, features: Dict[str, float]) -> float:
        """
        Predict the probability of disease indicators.
        
        Args:
            features: Dictionary of eye tracking features
            
        Returns:
            Probability score between 0 and 1
        """
        if not self.is_trained:
            return 0.0
        
        # Extract features in correct order
        feature_vector = self._extract_feature_vector(features)
        
        if feature_vector is None:
            return 0.0
        
        # Scale features
        X = self.scaler.transform(feature_vector.reshape(1, -1))
        
        # Get predictions from both models
        predictions = []
        
        if self.rf_model is not None:
            rf_proba = self.rf_model.predict_proba(X)[0]
            predictions.append(rf_proba[1] if len(rf_proba) > 1 else rf_proba[0])
        
        if self.xgb_model is not None:
            xgb_proba = self.xgb_model.predict_proba(X)[0]
            predictions.append(xgb_proba[1] if len(xgb_proba) > 1 else xgb_proba[0])
        
        if not predictions:
            return 0.0
        
        # Return weighted average (XGBoost weighted slightly higher if available)
        if len(predictions) == 2:
            return 0.45 * predictions[0] + 0.55 * predictions[1]
        return predictions[0]
    
    def _extract_feature_vector(self, features: Dict[str, float]) -> Optional[np.ndarray]:
        """
        Extract feature vector from feature dictionary.
        
        Args:
            features: Dictionary of features
            
        Returns:
            Numpy array of features or None if extraction fails
        """
        try:
            vector = []
            for name in FEATURE_NAMES:
                value = features.get(name, 0.0)
                vector.append(float(value) if value is not None else 0.0)
            return np.array(vector)
        except Exception:
            return None


class EnsembleDiseaseClassifier:
    """
    Ensemble classifier that combines predictions for all diseases.
    """
    
    def __init__(self, model_dir: str = 'models'):
        """
        Initialize ensemble classifier with models for all diseases.
        
        Args:
            model_dir: Directory containing trained models
        """
        self.model_dir = model_dir
        self.classifiers = {
            'parkinsons': MLDiseaseClassifier('parkinsons', model_dir),
            'alzheimers': MLDiseaseClassifier('alzheimers', model_dir),
            'asd': MLDiseaseClassifier('asd', model_dir),
            'adhd': MLDiseaseClassifier('adhd', model_dir)
        }
    
    def is_trained(self, disease: str = None) -> bool:
        """
        Check if classifiers are trained.
        
        Args:
            disease: Specific disease to check, or None for all
            
        Returns:
            True if specified classifier(s) are trained
        """
        if disease:
            return self.classifiers.get(disease, None) is not None and \
                   self.classifiers[disease].is_trained
        return all(clf.is_trained for clf in self.classifiers.values())
    
    def predict_all(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Get risk predictions for all diseases.
        
        Args:
            features: Dictionary of eye tracking features
            
        Returns:
            Dictionary mapping disease names to risk scores
        """
        results = {}
        for disease, classifier in self.classifiers.items():
            if classifier.is_trained:
                results[disease] = classifier.predict_proba(features)
            else:
                results[disease] = None
        return results
    
    def predict(self, disease: str, features: Dict[str, float]) -> Optional[float]:
        """
        Get risk prediction for a specific disease.
        
        Args:
            disease: Disease name
            features: Dictionary of eye tracking features
            
        Returns:
            Risk score between 0 and 1, or None if not available
        """
        classifier = self.classifiers.get(disease)
        if classifier and classifier.is_trained:
            return classifier.predict_proba(features)
        return None


def generate_synthetic_training_data(disease: str, 
                                     n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic training data for a specific disease.
    
    This creates realistic eye tracking feature distributions based on
    clinical research about eye movement patterns in various disorders.
    
    Args:
        disease: Disease name (parkinsons, alzheimers, asd, adhd)
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (features, labels)
    """
    np.random.seed(42)
    
    # Base healthy distribution (mean, std for each feature)
    healthy_params = {
        'mean_fixation_duration': (250, 50),
        'std_fixation_duration': (100, 30),
        'fixation_count': (50, 15),
        'mean_saccade_amplitude': (8, 3),
        'std_saccade_amplitude': (4, 1.5),
        'mean_saccade_velocity': (350, 80),
        'std_saccade_velocity': (120, 40),
        'saccade_rate': (3.0, 0.8),
        'saccade_count': (45, 12),
        'coverage_area': (30000, 10000),
        'x_mean': (500, 50),
        'y_mean': (400, 40),
        'x_std': (100, 30),
        'y_std': (80, 25),
        'mean_velocity': (50, 20),
        'std_velocity': (60, 25),
        'max_velocity': (500, 150),
        'total_distance': (5000, 1500)
    }
    
    # Disease-specific modifications to the distributions
    disease_modifications = {
        'parkinsons': {
            'mean_saccade_velocity': (250, 60),  # Reduced velocity
            'mean_saccade_amplitude': (5, 2),     # Hypometric saccades
            'mean_fixation_duration': (350, 70),  # Prolonged fixations
            'saccade_rate': (1.8, 0.5),           # Reduced rate
        },
        'alzheimers': {
            'mean_fixation_duration': (400, 80),  # Very prolonged fixations
            'coverage_area': (15000, 5000),       # Reduced exploration
            'saccade_rate': (1.2, 0.4),           # Significantly reduced
            'std_saccade_amplitude': (6, 2),      # High variability
        },
        'asd': {
            'std_fixation_duration': (220, 50),   # High variability
            'x_std': (170, 40),                   # Atypical spatial patterns
            'y_std': (140, 35),
            'mean_saccade_velocity': (520, 100),  # Elevated velocity
            'saccade_rate': (4.5, 1.0),           # Elevated rate
        },
        'adhd': {
            'mean_fixation_duration': (130, 35),  # Shortened fixations
            'saccade_rate': (5.0, 1.2),           # Elevated rate
            'coverage_area': (55000, 15000),      # High dispersion
            'std_velocity': (110, 35),            # High variability
        }
    }
    
    # Generate healthy samples
    n_healthy = n_samples // 2
    n_disease = n_samples - n_healthy
    
    # Generate healthy data
    healthy_data = []
    for _ in range(n_healthy):
        sample = []
        for feature_name in FEATURE_NAMES:
            if feature_name in healthy_params:
                mean, std = healthy_params[feature_name]
                value = np.random.normal(mean, std)
                sample.append(max(0, value))  # Ensure non-negative
            else:
                sample.append(0)
        healthy_data.append(sample)
    
    # Generate disease data with modifications
    disease_data = []
    mods = disease_modifications.get(disease, {})
    
    for _ in range(n_disease):
        sample = []
        for feature_name in FEATURE_NAMES:
            if feature_name in mods:
                mean, std = mods[feature_name]
            elif feature_name in healthy_params:
                mean, std = healthy_params[feature_name]
            else:
                mean, std = 0, 0
            
            value = np.random.normal(mean, std)
            sample.append(max(0, value))
        disease_data.append(sample)
    
    # Combine and create labels
    X = np.array(healthy_data + disease_data)
    y = np.array([0] * n_healthy + [1] * n_disease)
    
    # Shuffle
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]
    
    return X, y


def train_all_models(model_dir: str = 'models', 
                     n_samples: int = 2000) -> Dict[str, Dict]:
    """
    Train models for all diseases.
    
    Args:
        model_dir: Directory to save models
        n_samples: Number of training samples per disease
        
    Returns:
        Dictionary with training results for each disease
    """
    if not ML_AVAILABLE:
        raise RuntimeError("scikit-learn is required. Install with: pip install scikit-learn")
    
    results = {}
    diseases = ['parkinsons', 'alzheimers', 'asd', 'adhd']
    
    for disease in diseases:
        print(f"\nTraining model for {disease}...")
        
        # Generate training data
        X, y = generate_synthetic_training_data(disease, n_samples)
        
        # Train classifier
        classifier = MLDiseaseClassifier(disease, model_dir)
        metrics = classifier.train(X, y)
        
        results[disease] = metrics
        print(f"  Random Forest Accuracy: {metrics['rf_accuracy']:.3f}")
        if metrics['xgb_accuracy']:
            print(f"  XGBoost Accuracy: {metrics['xgb_accuracy']:.3f}")
    
    return results


# Global ensemble classifier instance
_ensemble_classifier: Optional[EnsembleDiseaseClassifier] = None


def get_ensemble_classifier(model_dir: str = 'models') -> EnsembleDiseaseClassifier:
    """
    Get or create the global ensemble classifier instance.
    
    Args:
        model_dir: Directory containing trained models
        
    Returns:
        EnsembleDiseaseClassifier instance
    """
    global _ensemble_classifier
    if _ensemble_classifier is None:
        _ensemble_classifier = EnsembleDiseaseClassifier(model_dir)
    return _ensemble_classifier
