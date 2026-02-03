"""
Disease-specific analysis modules for detecting neurological and developmental disorders.

This module now supports both rule-based and ML-based detection:
- ML models are used when trained models are available
- Rule-based detection serves as fallback when ML models aren't trained
- Hybrid mode combines both approaches for better accuracy
"""

from typing import Dict, List, Tuple, Any, Optional
import numpy as np
from .data_models import EyeTrackingData

# Try to import ML models
try:
    from .ml_models import get_ensemble_classifier, EnsembleDiseaseClassifier
    ML_MODELS_AVAILABLE = True
except ImportError:
    ML_MODELS_AVAILABLE = False
    EnsembleDiseaseClassifier = None


# Global ML classifier instance
_ml_classifier: Optional[Any] = None


def get_ml_classifier() -> Optional[Any]:
    """Get the global ML classifier instance."""
    global _ml_classifier
    if ML_MODELS_AVAILABLE and _ml_classifier is None:
        try:
            _ml_classifier = get_ensemble_classifier('models')
        except Exception:
            pass
    return _ml_classifier


class ParkinsonsDetector:
    """
    Detector for Parkinson's disease using eye movement patterns.
    
    Key indicators:
    - Reduced saccade velocity
    - Increased saccade latency
    - Hypometric saccades (undershooting)
    - Square wave jerks
    
    Now supports ML-based detection with rule-based fallback.
    """
    
    def __init__(self, use_ml: bool = True):
        """
        Initialize the detector.
        
        Args:
            use_ml: Whether to use ML models when available
        """
        self.use_ml = use_ml
        self.disease_name = 'parkinsons'
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for Parkinson's indicators.
        
        Uses ML model if available, otherwise falls back to rule-based detection.
        
        Args:
            features: Extracted eye tracking features
        
        Returns:
            Analysis results with risk score and indicators
        """
        # Get ML prediction if available
        ml_score = None
        if self.use_ml:
            ml_classifier = get_ml_classifier()
            if ml_classifier and ml_classifier.is_trained(self.disease_name):
                ml_score = ml_classifier.predict(self.disease_name, features)
        
        # Get rule-based analysis
        indicators = []
        rule_factors = []
        
        # Check for reduced saccade velocity
        if features.get('mean_saccade_velocity', 0) < 300:
            indicators.append("Reduced saccade velocity detected")
            rule_factors.append(0.3)
        
        # Check for hypometric saccades (small amplitudes)
        if features.get('mean_saccade_amplitude', 0) < 5:
            indicators.append("Hypometric saccades detected")
            rule_factors.append(0.3)
        
        # Check for increased fixation duration
        if features.get('mean_fixation_duration', 0) > 300:
            indicators.append("Prolonged fixations detected")
            rule_factors.append(0.2)
        
        # Check for reduced saccade rate
        if features.get('saccade_rate', 0) < 2:
            indicators.append("Reduced saccade rate detected")
            rule_factors.append(0.2)
        
        rule_score = min(sum(rule_factors), 1.0)
        
        # Combine ML and rule-based scores
        if ml_score is not None:
            # Weighted combination: 70% ML, 30% rule-based
            risk_score = 0.7 * ml_score + 0.3 * rule_score
            detection_method = 'hybrid'
        else:
            risk_score = rule_score
            detection_method = 'rule-based'
        
        return {
            'disease': 'Parkinsons',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score),
            'detection_method': detection_method,
            'ml_score': ml_score,
            'rule_score': rule_score
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Categorize risk level based on score."""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Moderate"
        else:
            return "High"
    
    def _get_recommendations(self, score: float) -> List[str]:
        """Get recommendations based on risk score."""
        recommendations = []
        if score >= 0.3:
            recommendations.append("Consider neurological consultation")
        if score >= 0.6:
            recommendations.append("Recommend comprehensive neurological assessment")
            recommendations.append("Monitor motor symptoms")
        return recommendations


class AlzheimersDetector:
    """
    Detector for Alzheimer's disease using eye movement patterns.
    
    Key indicators:
    - Increased saccade latency
    - Reduced accuracy in visual search tasks
    - Impaired smooth pursuit
    - Increased fixation duration
    
    Now supports ML-based detection with rule-based fallback.
    """
    
    def __init__(self, use_ml: bool = True):
        self.use_ml = use_ml
        self.disease_name = 'alzheimers'
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for Alzheimer's indicators.
        Uses ML model if available, otherwise falls back to rule-based detection.
        """
        # Get ML prediction if available
        ml_score = None
        if self.use_ml:
            ml_classifier = get_ml_classifier()
            if ml_classifier and ml_classifier.is_trained(self.disease_name):
                ml_score = ml_classifier.predict(self.disease_name, features)
        
        # Rule-based analysis
        indicators = []
        rule_factors = []
        
        if features.get('mean_fixation_duration', 0) > 350:
            indicators.append("Significantly prolonged fixations detected")
            rule_factors.append(0.3)
        
        if features.get('coverage_area', 0) < 10000:
            indicators.append("Reduced visual exploration detected")
            rule_factors.append(0.3)
        
        if features.get('std_saccade_amplitude', 0) > features.get('mean_saccade_amplitude', 1) * 0.7:
            indicators.append("High saccade variability detected")
            rule_factors.append(0.2)
        
        if features.get('saccade_rate', 0) < 1.5:
            indicators.append("Significantly reduced saccade rate")
            rule_factors.append(0.2)
        
        rule_score = min(sum(rule_factors), 1.0)
        
        # Combine scores
        if ml_score is not None:
            risk_score = 0.7 * ml_score + 0.3 * rule_score
            detection_method = 'hybrid'
        else:
            risk_score = rule_score
            detection_method = 'rule-based'
        
        return {
            'disease': 'Alzheimers',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score),
            'detection_method': detection_method,
            'ml_score': ml_score,
            'rule_score': rule_score
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Categorize risk level based on score."""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Moderate"
        else:
            return "High"
    
    def _get_recommendations(self, score: float) -> List[str]:
        """Get recommendations based on risk score."""
        recommendations = []
        if score >= 0.3:
            recommendations.append("Consider cognitive assessment")
        if score >= 0.6:
            recommendations.append("Recommend comprehensive neuropsychological evaluation")
            recommendations.append("Monitor cognitive function")
        return recommendations


class ASDDetector:
    """
    Detector for Autism Spectrum Disorder using eye movement patterns.
    
    Key indicators:
    - Reduced fixation on social stimuli
    - Atypical scan paths
    - Reduced attention to eyes in faces
    - Increased fixation on peripheral regions
    
    Now supports ML-based detection with rule-based fallback.
    """
    
    def __init__(self, use_ml: bool = True):
        self.use_ml = use_ml
        self.disease_name = 'asd'
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for ASD indicators.
        Uses ML model if available, otherwise falls back to rule-based detection.
        """
        # Get ML prediction if available
        ml_score = None
        if self.use_ml:
            ml_classifier = get_ml_classifier()
            if ml_classifier and ml_classifier.is_trained(self.disease_name):
                ml_score = ml_classifier.predict(self.disease_name, features)
        
        # Rule-based analysis
        indicators = []
        rule_factors = []
        
        if features.get('std_fixation_duration', 0) > 200:
            indicators.append("High fixation duration variability detected")
            rule_factors.append(0.3)
        
        if features.get('x_std', 0) > 150 or features.get('y_std', 0) > 150:
            indicators.append("Atypical spatial attention patterns detected")
            rule_factors.append(0.3)
        
        if features.get('mean_saccade_velocity', 0) > 500:
            indicators.append("Elevated saccade velocity detected")
            rule_factors.append(0.2)
        
        if features.get('saccade_rate', 0) > 4:
            indicators.append("Elevated saccade rate detected")
            rule_factors.append(0.2)
        
        rule_score = min(sum(rule_factors), 1.0)
        
        # Combine scores
        if ml_score is not None:
            risk_score = 0.7 * ml_score + 0.3 * rule_score
            detection_method = 'hybrid'
        else:
            risk_score = rule_score
            detection_method = 'rule-based'
        
        return {
            'disease': 'ASD',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score),
            'detection_method': detection_method,
            'ml_score': ml_score,
            'rule_score': rule_score
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Categorize risk level based on score."""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Moderate"
        else:
            return "High"
    
    def _get_recommendations(self, score: float) -> List[str]:
        """Get recommendations based on risk score."""
        recommendations = []
        if score >= 0.3:
            recommendations.append("Consider developmental screening")
        if score >= 0.6:
            recommendations.append("Recommend comprehensive ASD assessment")
            recommendations.append("Consider social interaction evaluation")
        return recommendations


class ADHDDetector:
    """
    Detector for ADHD using eye movement patterns.
    
    Key indicators:
    - Increased number of saccades
    - Shorter fixation durations
    - Increased spatial variability
    - Difficulty maintaining attention
    
    Now supports ML-based detection with rule-based fallback.
    """
    
    def __init__(self, use_ml: bool = True):
        self.use_ml = use_ml
        self.disease_name = 'adhd'
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for ADHD indicators.
        Uses ML model if available, otherwise falls back to rule-based detection.
        """
        # Get ML prediction if available
        ml_score = None
        if self.use_ml:
            ml_classifier = get_ml_classifier()
            if ml_classifier and ml_classifier.is_trained(self.disease_name):
                ml_score = ml_classifier.predict(self.disease_name, features)
        
        # Rule-based analysis
        indicators = []
        rule_factors = []
        
        if features.get('mean_fixation_duration', 0) < 150:
            indicators.append("Significantly shortened fixations detected")
            rule_factors.append(0.3)
        
        if features.get('saccade_rate', 0) > 4:
            indicators.append("Elevated saccade rate detected")
            rule_factors.append(0.3)
        
        if features.get('coverage_area', 0) > 50000:
            indicators.append("High spatial dispersion detected")
            rule_factors.append(0.2)
        
        if features.get('std_velocity', 0) > 100:
            indicators.append("High movement variability detected")
            rule_factors.append(0.2)
        
        rule_score = min(sum(rule_factors), 1.0)
        
        # Combine scores
        if ml_score is not None:
            risk_score = 0.7 * ml_score + 0.3 * rule_score
            detection_method = 'hybrid'
        else:
            risk_score = rule_score
            detection_method = 'rule-based'
        
        return {
            'disease': 'ADHD',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score),
            'detection_method': detection_method,
            'ml_score': ml_score,
            'rule_score': rule_score
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Categorize risk level based on score."""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Moderate"
        else:
            return "High"
    
    def _get_recommendations(self, score: float) -> List[str]:
        """Get recommendations based on risk score."""
        recommendations = []
        if score >= 0.3:
            recommendations.append("Consider attention assessment")
        if score >= 0.6:
            recommendations.append("Recommend comprehensive ADHD evaluation")
            recommendations.append("Monitor attention and hyperactivity symptoms")
        return recommendations
