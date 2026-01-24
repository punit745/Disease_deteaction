"""
Disease-specific analysis modules for detecting neurological and developmental disorders.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
from .data_models import EyeTrackingData


class ParkinsonsDetector:
    """
    Detector for Parkinson's disease using eye movement patterns.
    
    Key indicators:
    - Reduced saccade velocity
    - Increased saccade latency
    - Hypometric saccades (undershooting)
    - Square wave jerks
    """
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for Parkinson's indicators.
        
        Args:
            features: Extracted eye tracking features
        
        Returns:
            Analysis results with risk score and indicators
        """
        indicators = []
        risk_factors = []
        
        # Check for reduced saccade velocity
        if features.get('mean_saccade_velocity', 0) < 300:  # Typical threshold
            indicators.append("Reduced saccade velocity detected")
            risk_factors.append(0.3)
        
        # Check for hypometric saccades (small amplitudes)
        if features.get('mean_saccade_amplitude', 0) < 5:
            indicators.append("Hypometric saccades detected")
            risk_factors.append(0.3)
        
        # Check for increased fixation duration
        if features.get('mean_fixation_duration', 0) > 300:
            indicators.append("Prolonged fixations detected")
            risk_factors.append(0.2)
        
        # Check for reduced saccade rate
        if features.get('saccade_rate', 0) < 2:
            indicators.append("Reduced saccade rate detected")
            risk_factors.append(0.2)
        
        risk_score = min(sum(risk_factors), 1.0)
        
        return {
            'disease': 'Parkinsons',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score)
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
    """
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for Alzheimer's indicators.
        
        Args:
            features: Extracted eye tracking features
        
        Returns:
            Analysis results with risk score and indicators
        """
        indicators = []
        risk_factors = []
        
        # Check for prolonged fixations (cognitive processing deficit)
        if features.get('mean_fixation_duration', 0) > 350:
            indicators.append("Significantly prolonged fixations detected")
            risk_factors.append(0.3)
        
        # Check for reduced spatial coverage (visual search impairment)
        if features.get('coverage_area', 0) < 10000:
            indicators.append("Reduced visual exploration detected")
            risk_factors.append(0.3)
        
        # Check for irregular saccade patterns
        if features.get('std_saccade_amplitude', 0) > features.get('mean_saccade_amplitude', 1) * 0.7:
            indicators.append("High saccade variability detected")
            risk_factors.append(0.2)
        
        # Check for reduced saccade rate
        if features.get('saccade_rate', 0) < 1.5:
            indicators.append("Significantly reduced saccade rate")
            risk_factors.append(0.2)
        
        risk_score = min(sum(risk_factors), 1.0)
        
        return {
            'disease': 'Alzheimers',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score)
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
    """
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for ASD indicators.
        
        Args:
            features: Extracted eye tracking features
        
        Returns:
            Analysis results with risk score and indicators
        """
        indicators = []
        risk_factors = []
        
        # Check for atypical fixation patterns
        if features.get('std_fixation_duration', 0) > 200:
            indicators.append("High fixation duration variability detected")
            risk_factors.append(0.3)
        
        # Check for atypical spatial exploration
        if features.get('x_std', 0) > 150 or features.get('y_std', 0) > 150:
            indicators.append("Atypical spatial attention patterns detected")
            risk_factors.append(0.3)
        
        # Check for rapid saccades (hyperactive visual attention)
        if features.get('mean_saccade_velocity', 0) > 500:
            indicators.append("Elevated saccade velocity detected")
            risk_factors.append(0.2)
        
        # Check for increased saccade frequency
        if features.get('saccade_rate', 0) > 4:
            indicators.append("Elevated saccade rate detected")
            risk_factors.append(0.2)
        
        risk_score = min(sum(risk_factors), 1.0)
        
        return {
            'disease': 'ASD',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score)
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
    """
    
    def analyze(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze features for ADHD indicators.
        
        Args:
            features: Extracted eye tracking features
        
        Returns:
            Analysis results with risk score and indicators
        """
        indicators = []
        risk_factors = []
        
        # Check for short fixation durations (attention deficit)
        if features.get('mean_fixation_duration', 0) < 150:
            indicators.append("Significantly shortened fixations detected")
            risk_factors.append(0.3)
        
        # Check for increased saccade rate (hyperactivity)
        if features.get('saccade_rate', 0) > 4:
            indicators.append("Elevated saccade rate detected")
            risk_factors.append(0.3)
        
        # Check for high spatial variability (distractibility)
        if features.get('coverage_area', 0) > 50000:
            indicators.append("High spatial dispersion detected")
            risk_factors.append(0.2)
        
        # Check for high velocity variability
        if features.get('std_velocity', 0) > 100:
            indicators.append("High movement variability detected")
            risk_factors.append(0.2)
        
        risk_score = min(sum(risk_factors), 1.0)
        
        return {
            'disease': 'ADHD',
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'indicators': indicators,
            'recommendations': self._get_recommendations(risk_score)
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
