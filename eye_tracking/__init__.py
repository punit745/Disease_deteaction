"""
Eye Tracking Disease Detection System
A comprehensive system for detecting neurological and developmental disorders
through eye movement pattern analysis.
"""

__version__ = "1.0.0"
__author__ = "Disease Detection Team"

from .data_models import EyeTrackingData, EyeMovementEvent
from .preprocessor import EyeTrackingPreprocessor
from .feature_extractor import FeatureExtractor
from .analyzer import DiseaseAnalyzer

__all__ = [
    'EyeTrackingData',
    'EyeMovementEvent',
    'EyeTrackingPreprocessor',
    'FeatureExtractor',
    'DiseaseAnalyzer',
]
