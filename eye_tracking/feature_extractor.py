"""
Feature extraction from eye tracking data for disease detection.
"""

import numpy as np
from typing import Dict, List, Any
from scipy import stats
from .data_models import EyeTrackingData, EyeMovementEvent


class FeatureExtractor:
    """
    Extract features from eye tracking data for disease classification.
    """
    
    def extract_saccade_features(self, events: List[EyeMovementEvent]) -> Dict[str, float]:
        """
        Extract saccade-related features.
        
        Args:
            events: List of eye movement events
        
        Returns:
            Dictionary of saccade features
        """
        saccades = [e for e in events if e.event_type == 'saccade']
        
        if not saccades:
            return {
                'saccade_count': 0,
                'saccade_rate': 0.0,
                'mean_saccade_amplitude': 0.0,
                'std_saccade_amplitude': 0.0,
                'mean_saccade_velocity': 0.0,
                'std_saccade_velocity': 0.0,
                'mean_saccade_duration': 0.0,
                'std_saccade_duration': 0.0,
            }
        
        amplitudes = [s.amplitude for s in saccades if s.amplitude is not None]
        velocities = [s.velocity for s in saccades if s.velocity is not None]
        durations = [s.duration for s in saccades]
        
        # Calculate total time span
        if saccades:
            time_span = (saccades[-1].end_time - saccades[0].start_time) / 1000.0  # seconds
            saccade_rate = len(saccades) / time_span if time_span > 0 else 0
        else:
            saccade_rate = 0
        
        return {
            'saccade_count': len(saccades),
            'saccade_rate': saccade_rate,
            'mean_saccade_amplitude': np.mean(amplitudes) if amplitudes else 0.0,
            'std_saccade_amplitude': np.std(amplitudes) if amplitudes else 0.0,
            'mean_saccade_velocity': np.mean(velocities) if velocities else 0.0,
            'std_saccade_velocity': np.std(velocities) if velocities else 0.0,
            'mean_saccade_duration': np.mean(durations) if durations else 0.0,
            'std_saccade_duration': np.std(durations) if durations else 0.0,
        }
    
    def extract_fixation_features(self, events: List[EyeMovementEvent]) -> Dict[str, float]:
        """
        Extract fixation-related features.
        
        Args:
            events: List of eye movement events
        
        Returns:
            Dictionary of fixation features
        """
        fixations = [e for e in events if e.event_type == 'fixation']
        
        if not fixations:
            return {
                'fixation_count': 0,
                'fixation_rate': 0.0,
                'mean_fixation_duration': 0.0,
                'std_fixation_duration': 0.0,
                'total_fixation_time': 0.0,
            }
        
        durations = [f.duration for f in fixations]
        
        # Calculate total time span
        if fixations:
            time_span = (fixations[-1].end_time - fixations[0].start_time) / 1000.0  # seconds
            fixation_rate = len(fixations) / time_span if time_span > 0 else 0
        else:
            fixation_rate = 0
        
        return {
            'fixation_count': len(fixations),
            'fixation_rate': fixation_rate,
            'mean_fixation_duration': np.mean(durations),
            'std_fixation_duration': np.std(durations),
            'total_fixation_time': np.sum(durations),
        }
    
    def extract_spatial_features(self, data: EyeTrackingData) -> Dict[str, float]:
        """
        Extract spatial distribution features.
        
        Args:
            data: Eye tracking data
        
        Returns:
            Dictionary of spatial features
        """
        x_positions = data.x_positions
        y_positions = data.y_positions
        
        # Spatial dispersion
        x_range = np.max(x_positions) - np.min(x_positions)
        y_range = np.max(y_positions) - np.min(y_positions)
        
        # Spatial variability
        x_std = np.std(x_positions)
        y_std = np.std(y_positions)
        
        # Spatial coverage (convex hull area approximation)
        coverage_area = x_range * y_range
        
        return {
            'x_range': x_range,
            'y_range': y_range,
            'x_std': x_std,
            'y_std': y_std,
            'coverage_area': coverage_area,
        }
    
    def extract_pupil_features(self, data: EyeTrackingData) -> Dict[str, float]:
        """
        Extract pupil-related features.
        
        Args:
            data: Eye tracking data
        
        Returns:
            Dictionary of pupil features
        """
        if data.pupil_sizes is None:
            return {
                'mean_pupil_size': 0.0,
                'std_pupil_size': 0.0,
                'pupil_size_variability': 0.0,
            }
        
        pupil_sizes = data.pupil_sizes[~np.isnan(data.pupil_sizes)]
        
        if len(pupil_sizes) == 0:
            return {
                'mean_pupil_size': 0.0,
                'std_pupil_size': 0.0,
                'pupil_size_variability': 0.0,
            }
        
        return {
            'mean_pupil_size': np.mean(pupil_sizes),
            'std_pupil_size': np.std(pupil_sizes),
            'pupil_size_variability': np.std(pupil_sizes) / np.mean(pupil_sizes) if np.mean(pupil_sizes) > 0 else 0.0,
        }
    
    def extract_temporal_features(self, data: EyeTrackingData) -> Dict[str, float]:
        """
        Extract temporal pattern features.
        
        Args:
            data: Eye tracking data
        
        Returns:
            Dictionary of temporal features
        """
        velocity = data.get_velocity()
        acceleration = data.get_acceleration()
        
        return {
            'mean_velocity': np.mean(velocity),
            'std_velocity': np.std(velocity),
            'max_velocity': np.max(velocity),
            'mean_acceleration': np.mean(np.abs(acceleration)),
            'std_acceleration': np.std(acceleration),
            'max_acceleration': np.max(np.abs(acceleration)),
        }
    
    def extract_all_features(self, data: EyeTrackingData) -> Dict[str, float]:
        """
        Extract all features from eye tracking data.
        
        Args:
            data: Processed eye tracking data with detected events
        
        Returns:
            Dictionary of all features
        """
        features = {}
        
        # Saccade features
        features.update(self.extract_saccade_features(data.events))
        
        # Fixation features
        features.update(self.extract_fixation_features(data.events))
        
        # Spatial features
        features.update(self.extract_spatial_features(data))
        
        # Pupil features
        features.update(self.extract_pupil_features(data))
        
        # Temporal features
        features.update(self.extract_temporal_features(data))
        
        return features
