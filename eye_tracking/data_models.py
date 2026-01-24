"""
Data models for eye tracking data representation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import numpy as np


@dataclass
class EyeMovementEvent:
    """
    Represents a single eye movement event (fixation, saccade, etc.)
    """
    event_type: str  # 'fixation', 'saccade', 'smooth_pursuit', 'blink'
    start_time: float  # milliseconds
    end_time: float  # milliseconds
    duration: float  # milliseconds
    start_x: float  # x-coordinate at start
    start_y: float  # y-coordinate at start
    end_x: Optional[float] = None  # x-coordinate at end (for saccades)
    end_y: Optional[float] = None  # y-coordinate at end (for saccades)
    amplitude: Optional[float] = None  # amplitude for saccades
    velocity: Optional[float] = None  # peak velocity for saccades
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Calculate derived properties."""
        if self.event_type == 'saccade' and self.end_x is not None and self.end_y is not None:
            # Calculate amplitude if not provided
            if self.amplitude is None:
                self.amplitude = np.sqrt(
                    (self.end_x - self.start_x) ** 2 + 
                    (self.end_y - self.start_y) ** 2
                )
            # Calculate velocity if not provided
            if self.velocity is None and self.duration > 0:
                self.velocity = self.amplitude / (self.duration / 1000.0)


@dataclass
class EyeTrackingData:
    """
    Container for eye tracking data and associated metadata.
    """
    timestamps: np.ndarray  # milliseconds
    x_positions: np.ndarray  # x-coordinates
    y_positions: np.ndarray  # y-coordinates
    pupil_sizes: Optional[np.ndarray] = None  # pupil diameter
    sampling_rate: float = 1000.0  # Hz
    subject_id: Optional[str] = None
    session_id: Optional[str] = None
    task_type: Optional[str] = None  # 'reading', 'visual_search', 'smooth_pursuit', etc.
    events: List[EyeMovementEvent] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate data integrity."""
        if len(self.timestamps) != len(self.x_positions) or len(self.timestamps) != len(self.y_positions):
            raise ValueError("Timestamps, x_positions, and y_positions must have the same length")
        
        if self.pupil_sizes is not None and len(self.pupil_sizes) != len(self.timestamps):
            raise ValueError("Pupil sizes must have the same length as timestamps")

    @property
    def duration(self) -> float:
        """Total duration of recording in milliseconds."""
        return self.timestamps[-1] - self.timestamps[0]

    @property
    def num_samples(self) -> int:
        """Number of samples in the recording."""
        return len(self.timestamps)

    def get_velocity(self) -> np.ndarray:
        """Calculate instantaneous velocity."""
        dx = np.diff(self.x_positions)
        dy = np.diff(self.y_positions)
        dt = np.diff(self.timestamps) / 1000.0  # convert to seconds
        
        velocity = np.zeros(len(self.timestamps))
        velocity[1:] = np.sqrt(dx**2 + dy**2) / dt
        return velocity

    def get_acceleration(self) -> np.ndarray:
        """Calculate instantaneous acceleration."""
        velocity = self.get_velocity()
        dt = np.diff(self.timestamps) / 1000.0  # convert to seconds
        
        acceleration = np.zeros(len(self.timestamps))
        acceleration[1:] = np.diff(velocity) / dt
        return acceleration
