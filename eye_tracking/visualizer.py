"""
Visualization utilities for eye tracking data and analysis results.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List
from .data_models import EyeTrackingData, EyeMovementEvent


class Visualizer:
    """
    Visualization utilities for eye tracking data.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize the visualizer.
        
        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except (OSError, ValueError):
            # Fallback to default style if requested style is not available
            pass
        sns.set_palette("husl")
    
    def plot_gaze_path(self, data: EyeTrackingData, 
                       save_path: Optional[str] = None,
                       figsize: tuple = (10, 8)):
        """
        Plot the gaze path with fixations and saccades.
        
        Args:
            data: Eye tracking data
            save_path: Path to save the figure
            figsize: Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot gaze path
        ax.plot(data.x_positions, data.y_positions, 'b-', alpha=0.3, linewidth=0.5, label='Gaze path')
        
        # Highlight fixations
        fixations = [e for e in data.events if e.event_type == 'fixation']
        if fixations:
            fix_x = [f.start_x for f in fixations]
            fix_y = [f.start_y for f in fixations]
            fix_sizes = [f.duration / 10 for f in fixations]  # Size proportional to duration
            ax.scatter(fix_x, fix_y, s=fix_sizes, c='red', alpha=0.6, label='Fixations')
        
        # Highlight saccades
        saccades = [e for e in data.events if e.event_type == 'saccade']
        if saccades:
            for saccade in saccades:
                if saccade.end_x is not None and saccade.end_y is not None:
                    ax.arrow(saccade.start_x, saccade.start_y,
                            saccade.end_x - saccade.start_x,
                            saccade.end_y - saccade.start_y,
                            head_width=5, head_length=7, fc='green', ec='green', alpha=0.4)
        
        ax.set_xlabel('X Position (pixels)')
        ax.set_ylabel('Y Position (pixels)')
        ax.set_title('Eye Gaze Path with Fixations and Saccades')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        return fig
    
    def plot_temporal_patterns(self, data: EyeTrackingData,
                              save_path: Optional[str] = None,
                              figsize: tuple = (12, 8)):
        """
        Plot temporal patterns including velocity and acceleration.
        
        Args:
            data: Eye tracking data
            save_path: Path to save the figure
            figsize: Figure size
        """
        velocity = data.get_velocity()
        acceleration = data.get_acceleration()
        
        fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)
        
        # Position over time
        axes[0].plot(data.timestamps, data.x_positions, label='X position', alpha=0.7)
        axes[0].plot(data.timestamps, data.y_positions, label='Y position', alpha=0.7)
        axes[0].set_ylabel('Position (pixels)')
        axes[0].set_title('Eye Position Over Time')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Velocity over time
        axes[1].plot(data.timestamps, velocity, 'g-', alpha=0.7)
        axes[1].set_ylabel('Velocity (pixels/s)')
        axes[1].set_title('Gaze Velocity Over Time')
        axes[1].grid(True, alpha=0.3)
        
        # Acceleration over time
        axes[2].plot(data.timestamps, acceleration, 'r-', alpha=0.7)
        axes[2].set_ylabel('Acceleration (pixels/s²)')
        axes[2].set_xlabel('Time (ms)')
        axes[2].set_title('Gaze Acceleration Over Time')
        axes[2].grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        return fig
    
    def plot_event_distribution(self, data: EyeTrackingData,
                               save_path: Optional[str] = None,
                               figsize: tuple = (12, 6)):
        """
        Plot distribution of eye movement events.
        
        Args:
            data: Eye tracking data
            save_path: Path to save the figure
            figsize: Figure size
        """
        fixations = [e for e in data.events if e.event_type == 'fixation']
        saccades = [e for e in data.events if e.event_type == 'saccade']
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Fixation duration distribution
        if fixations:
            fix_durations = [f.duration for f in fixations]
            axes[0].hist(fix_durations, bins=20, alpha=0.7, color='red', edgecolor='black')
            axes[0].axvline(np.mean(fix_durations), color='darkred', linestyle='--', 
                           linewidth=2, label=f'Mean: {np.mean(fix_durations):.1f} ms')
            axes[0].set_xlabel('Duration (ms)')
            axes[0].set_ylabel('Count')
            axes[0].set_title('Fixation Duration Distribution')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
        
        # Saccade amplitude distribution
        if saccades:
            sac_amplitudes = [s.amplitude for s in saccades if s.amplitude is not None]
            if sac_amplitudes:
                axes[1].hist(sac_amplitudes, bins=20, alpha=0.7, color='green', edgecolor='black')
                axes[1].axvline(np.mean(sac_amplitudes), color='darkgreen', linestyle='--',
                               linewidth=2, label=f'Mean: {np.mean(sac_amplitudes):.1f} px')
                axes[1].set_xlabel('Amplitude (pixels)')
                axes[1].set_ylabel('Count')
                axes[1].set_title('Saccade Amplitude Distribution')
                axes[1].legend()
                axes[1].grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        return fig
    
    def plot_risk_scores(self, results: dict,
                        save_path: Optional[str] = None,
                        figsize: tuple = (10, 6)):
        """
        Plot risk scores for all diseases.
        
        Args:
            results: Analysis results from DiseaseAnalyzer
            save_path: Path to save the figure
            figsize: Figure size
        """
        disease_analysis = results.get('disease_analysis', {})
        
        if not disease_analysis:
            print("No disease analysis results to plot")
            return None
        
        diseases = list(disease_analysis.keys())
        risk_scores = [disease_analysis[d]['risk_score'] for d in diseases]
        risk_levels = [disease_analysis[d]['risk_level'] for d in diseases]
        
        # Color code by risk level
        colors = []
        for level in risk_levels:
            if level == 'Low':
                colors.append('green')
            elif level == 'Moderate':
                colors.append('orange')
            else:
                colors.append('red')
        
        fig, ax = plt.subplots(figsize=figsize)
        
        bars = ax.barh(diseases, risk_scores, color=colors, alpha=0.7, edgecolor='black')
        
        # Add risk level labels
        for i, (disease, score, level) in enumerate(zip(diseases, risk_scores, risk_levels)):
            ax.text(score + 0.02, i, f'{level} ({score:.2f})', 
                   va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Risk Score', fontsize=12)
        ax.set_title('Disease Risk Assessment', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1.1)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add risk level legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.7, label='Low Risk'),
            Patch(facecolor='orange', alpha=0.7, label='Moderate Risk'),
            Patch(facecolor='red', alpha=0.7, label='High Risk')
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        return fig
