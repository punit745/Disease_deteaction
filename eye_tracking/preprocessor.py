"""
Preprocessing utilities for eye tracking data.
"""

import numpy as np
from typing import Optional, List, Tuple
from scipy.signal import savgol_filter, medfilt
from .data_models import EyeTrackingData, EyeMovementEvent


class EyeTrackingPreprocessor:
    """
    Preprocessor for eye tracking data with noise removal and event detection.
    """
    
    def __init__(self, velocity_threshold: float = 30.0, 
                 acceleration_threshold: float = 8000.0,
                 fixation_min_duration: float = 100.0):
        """
        Initialize the preprocessor.
        
        Args:
            velocity_threshold: Velocity threshold for saccade detection (deg/s)
            acceleration_threshold: Acceleration threshold for saccade detection (deg/s^2)
            fixation_min_duration: Minimum duration for a fixation (ms)
        """
        self.velocity_threshold = velocity_threshold
        self.acceleration_threshold = acceleration_threshold
        self.fixation_min_duration = fixation_min_duration
    
    def remove_noise(self, data: EyeTrackingData, method: str = 'savgol') -> EyeTrackingData:
        """
        Remove noise from eye tracking data.
        
        Args:
            data: Input eye tracking data
            method: Noise removal method ('savgol', 'median', or 'none')
        
        Returns:
            Cleaned eye tracking data
        """
        if method == 'savgol':
            # Savitzky-Golay filter
            window_length = min(11, len(data.x_positions) if len(data.x_positions) % 2 == 1 else len(data.x_positions) - 1)
            if window_length < 3:
                return data
            x_clean = savgol_filter(data.x_positions, window_length, 2)
            y_clean = savgol_filter(data.y_positions, window_length, 2)
        elif method == 'median':
            # Median filter
            kernel_size = 5
            x_clean = medfilt(data.x_positions, kernel_size)
            y_clean = medfilt(data.y_positions, kernel_size)
        else:
            x_clean = data.x_positions.copy()
            y_clean = data.y_positions.copy()
        
        return EyeTrackingData(
            timestamps=data.timestamps.copy(),
            x_positions=x_clean,
            y_positions=y_clean,
            pupil_sizes=data.pupil_sizes.copy() if data.pupil_sizes is not None else None,
            sampling_rate=data.sampling_rate,
            subject_id=data.subject_id,
            session_id=data.session_id,
            task_type=data.task_type,
            metadata=data.metadata.copy()
        )
    
    def detect_saccades(self, data: EyeTrackingData) -> List[EyeMovementEvent]:
        """
        Detect saccades using velocity and acceleration thresholds.
        
        Args:
            data: Eye tracking data
        
        Returns:
            List of saccade events
        """
        velocity = data.get_velocity()
        acceleration = data.get_acceleration()
        
        # Identify saccade candidates
        saccade_mask = (velocity > self.velocity_threshold) | (np.abs(acceleration) > self.acceleration_threshold)
        
        saccades = []
        in_saccade = False
        start_idx = 0
        
        for i, is_saccade in enumerate(saccade_mask):
            if is_saccade and not in_saccade:
                # Start of saccade
                start_idx = i
                in_saccade = True
            elif not is_saccade and in_saccade:
                # End of saccade
                end_idx = i - 1
                if end_idx > start_idx:
                    duration = data.timestamps[end_idx] - data.timestamps[start_idx]
                    amplitude = np.sqrt(
                        (data.x_positions[end_idx] - data.x_positions[start_idx]) ** 2 +
                        (data.y_positions[end_idx] - data.y_positions[start_idx]) ** 2
                    )
                    peak_velocity = np.max(velocity[start_idx:end_idx+1])
                    
                    saccades.append(EyeMovementEvent(
                        event_type='saccade',
                        start_time=data.timestamps[start_idx],
                        end_time=data.timestamps[end_idx],
                        duration=duration,
                        start_x=data.x_positions[start_idx],
                        start_y=data.y_positions[start_idx],
                        end_x=data.x_positions[end_idx],
                        end_y=data.y_positions[end_idx],
                        amplitude=amplitude,
                        velocity=peak_velocity
                    ))
                in_saccade = False
        
        return saccades
    
    def detect_fixations(self, data: EyeTrackingData, saccades: List[EyeMovementEvent]) -> List[EyeMovementEvent]:
        """
        Detect fixations as periods between saccades.
        
        Args:
            data: Eye tracking data
            saccades: List of detected saccades
        
        Returns:
            List of fixation events
        """
        fixations = []
        
        if not saccades:
            # If no saccades, treat entire period as one fixation
            duration = data.duration
            if duration >= self.fixation_min_duration:
                fixations.append(EyeMovementEvent(
                    event_type='fixation',
                    start_time=data.timestamps[0],
                    end_time=data.timestamps[-1],
                    duration=duration,
                    start_x=np.mean(data.x_positions),
                    start_y=np.mean(data.y_positions)
                ))
            return fixations
        
        # Check for fixation before first saccade
        if saccades[0].start_time - data.timestamps[0] >= self.fixation_min_duration:
            mask = data.timestamps < saccades[0].start_time
            fixations.append(EyeMovementEvent(
                event_type='fixation',
                start_time=data.timestamps[0],
                end_time=saccades[0].start_time,
                duration=saccades[0].start_time - data.timestamps[0],
                start_x=np.mean(data.x_positions[mask]),
                start_y=np.mean(data.y_positions[mask])
            ))
        
        # Check for fixations between saccades
        for i in range(len(saccades) - 1):
            start_time = saccades[i].end_time
            end_time = saccades[i + 1].start_time
            duration = end_time - start_time
            
            if duration >= self.fixation_min_duration:
                mask = (data.timestamps >= start_time) & (data.timestamps < end_time)
                if np.any(mask):
                    fixations.append(EyeMovementEvent(
                        event_type='fixation',
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        start_x=np.mean(data.x_positions[mask]),
                        start_y=np.mean(data.y_positions[mask])
                    ))
        
        # Check for fixation after last saccade
        if data.timestamps[-1] - saccades[-1].end_time >= self.fixation_min_duration:
            mask = data.timestamps > saccades[-1].end_time
            fixations.append(EyeMovementEvent(
                event_type='fixation',
                start_time=saccades[-1].end_time,
                end_time=data.timestamps[-1],
                duration=data.timestamps[-1] - saccades[-1].end_time,
                start_x=np.mean(data.x_positions[mask]),
                start_y=np.mean(data.y_positions[mask])
            ))
        
        return fixations
    
    def process(self, data: EyeTrackingData) -> EyeTrackingData:
        """
        Complete preprocessing pipeline.
        
        Args:
            data: Raw eye tracking data
        
        Returns:
            Processed eye tracking data with detected events
        """
        # Remove noise
        clean_data = self.remove_noise(data)
        
        # Detect saccades
        saccades = self.detect_saccades(clean_data)
        
        # Detect fixations
        fixations = self.detect_fixations(clean_data, saccades)
        
        # Combine all events and sort by time
        all_events = saccades + fixations
        all_events.sort(key=lambda e: e.start_time)
        
        clean_data.events = all_events
        
        return clean_data
