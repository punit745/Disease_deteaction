#!/usr/bin/env python3
"""
Interactive Demo Script for Eye Tracking Disease Detection System

This script provides an interactive demonstration of the disease detection
system's capabilities with various scenarios and real-time analysis.
"""

import os
import sys
import numpy as np
from pathlib import Path

# Add the current directory to the path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eye_tracking import EyeTrackingData, DiseaseAnalyzer
from eye_tracking.visualizer import Visualizer


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(message, color):
    """Print colored message."""
    print(f"{color}{message}{Colors.ENDC}")


def print_header(message):
    """Print formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def generate_normal_data(duration_ms=5000, sampling_rate=1000.0):
    """Generate eye tracking data simulating normal eye movements."""
    num_samples = int(duration_ms * sampling_rate / 1000)
    timestamps = np.linspace(0, duration_ms, num_samples)
    
    x_positions = np.zeros(num_samples)
    y_positions = np.zeros(num_samples)
    
    # Normal fixations with occasional saccades
    current_x, current_y = 500, 400
    for i in range(num_samples):
        x_positions[i] = current_x + np.random.normal(0, 2)
        y_positions[i] = current_y + np.random.normal(0, 2)
        
        # Normal saccade rate: ~3 per second
        if np.random.random() < 0.003:
            current_x += np.random.normal(0, 80)
            current_y += np.random.normal(0, 80)
            current_x = np.clip(current_x, 100, 900)
            current_y = np.clip(current_y, 100, 700)
    
    pupil_sizes = 3.0 + 0.3 * np.sin(2 * np.pi * timestamps / 1000) + np.random.normal(0, 0.08, num_samples)
    
    return EyeTrackingData(
        timestamps=timestamps,
        x_positions=x_positions,
        y_positions=y_positions,
        pupil_sizes=pupil_sizes,
        sampling_rate=sampling_rate,
        subject_id="NORMAL_DEMO",
        task_type="visual_search"
    )


def generate_parkinsons_data(duration_ms=5000, sampling_rate=1000.0):
    """Generate eye tracking data simulating Parkinson's characteristics."""
    num_samples = int(duration_ms * sampling_rate / 1000)
    timestamps = np.linspace(0, duration_ms, num_samples)
    
    x_positions = np.zeros(num_samples)
    y_positions = np.zeros(num_samples)
    
    # Reduced saccade rate, prolonged fixations
    current_x, current_y = 500, 400
    for i in range(num_samples):
        x_positions[i] = current_x + np.random.normal(0, 1.5)
        y_positions[i] = current_y + np.random.normal(0, 1.5)
        
        # Reduced saccade rate: ~1.5 per second
        if np.random.random() < 0.0015:
            # Hypometric saccades (smaller amplitude)
            current_x += np.random.normal(0, 30)
            current_y += np.random.normal(0, 30)
            current_x = np.clip(current_x, 100, 900)
            current_y = np.clip(current_y, 100, 700)
    
    pupil_sizes = 3.0 + 0.2 * np.sin(2 * np.pi * timestamps / 1000) + np.random.normal(0, 0.05, num_samples)
    
    return EyeTrackingData(
        timestamps=timestamps,
        x_positions=x_positions,
        y_positions=y_positions,
        pupil_sizes=pupil_sizes,
        sampling_rate=sampling_rate,
        subject_id="PARKINSONS_DEMO",
        task_type="visual_search"
    )


def generate_adhd_data(duration_ms=5000, sampling_rate=1000.0):
    """Generate eye tracking data simulating ADHD characteristics."""
    num_samples = int(duration_ms * sampling_rate / 1000)
    timestamps = np.linspace(0, duration_ms, num_samples)
    
    x_positions = np.zeros(num_samples)
    y_positions = np.zeros(num_samples)
    
    # High saccade rate, short fixations
    current_x, current_y = 500, 400
    for i in range(num_samples):
        x_positions[i] = current_x + np.random.normal(0, 3)
        y_positions[i] = current_y + np.random.normal(0, 3)
        
        # Elevated saccade rate: ~5 per second
        if np.random.random() < 0.005:
            current_x += np.random.normal(0, 100)
            current_y += np.random.normal(0, 100)
            current_x = np.clip(current_x, 100, 900)
            current_y = np.clip(current_y, 100, 700)
    
    pupil_sizes = 3.0 + 0.4 * np.sin(2 * np.pi * timestamps / 500) + np.random.normal(0, 0.12, num_samples)
    
    return EyeTrackingData(
        timestamps=timestamps,
        x_positions=x_positions,
        y_positions=y_positions,
        pupil_sizes=pupil_sizes,
        sampling_rate=sampling_rate,
        subject_id="ADHD_DEMO",
        task_type="visual_search"
    )


def display_results(results, data_type):
    """Display analysis results in a formatted way."""
    print_header(f"{data_type} - Analysis Results")
    
    # Overall summary
    summary = results['summary']
    risk_level = summary['overall_risk_level']
    
    if risk_level == "Low":
        color = Colors.OKGREEN
    elif risk_level == "Moderate":
        color = Colors.WARNING
    else:
        color = Colors.FAIL
    
    print(f"{Colors.BOLD}Overall Risk Level:{Colors.ENDC} ", end="")
    print_colored(risk_level, color)
    print(f"{Colors.BOLD}Highest Risk:{Colors.ENDC} {summary['highest_risk_disease'].upper()} "
          f"(Score: {summary['highest_risk_score']:.2f})")
    print()
    
    # Disease-specific results
    print(f"{Colors.BOLD}Disease Risk Scores:{Colors.ENDC}")
    print("-" * 70)
    
    disease_names = {
        'parkinsons': 'Parkinson\'s Disease',
        'alzheimers': 'Alzheimer\'s Disease',
        'asd': 'Autism Spectrum Disorder',
        'adhd': 'ADHD'
    }
    
    for disease_id, disease_name in disease_names.items():
        disease_result = results['disease_analysis'][disease_id]
        score = disease_result['risk_score']
        level = disease_result['risk_level']
        
        # Color code based on risk level
        if level == "Low":
            level_color = Colors.OKGREEN
        elif level == "Moderate":
            level_color = Colors.WARNING
        else:
            level_color = Colors.FAIL
        
        # Create bar chart
        bar_length = int(score * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        
        print(f"  {disease_name:30s} ", end="")
        print(f"{bar} ", end="")
        print(f"{score:4.2f} ", end="")
        print_colored(f"[{level}]", level_color)
        
        # Show indicators if any
        if disease_result['indicators']:
            print(f"    {Colors.OKCYAN}Indicators:{Colors.ENDC}", end=" ")
            print(f"{len(disease_result['indicators'])} detected")
    
    print()


def run_scenario_comparison():
    """Run comparison of different scenarios."""
    print_header("Eye Tracking Disease Detection System")
    print_header("Interactive Demo")
    
    print(f"{Colors.BOLD}This demo will analyze three different scenarios:{Colors.ENDC}")
    print(f"  1. {Colors.OKGREEN}Normal eye movement patterns{Colors.ENDC}")
    print(f"  2. {Colors.WARNING}Parkinson's-like patterns{Colors.ENDC}")
    print(f"  3. {Colors.WARNING}ADHD-like patterns{Colors.ENDC}")
    print()
    
    input(f"Press {Colors.OKGREEN}Enter{Colors.ENDC} to start the analysis...")
    
    # Initialize analyzer
    analyzer = DiseaseAnalyzer()
    visualizer = Visualizer()
    
    # Create output directory for visualizations
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    
    scenarios = [
        ("Normal Baseline", generate_normal_data, "normal"),
        ("Parkinson's Simulation", generate_parkinsons_data, "parkinsons"),
        ("ADHD Simulation", generate_adhd_data, "adhd")
    ]
    
    all_results = []
    
    for scenario_name, data_generator, scenario_id in scenarios:
        print(f"\n{Colors.OKCYAN}Generating {scenario_name} data...{Colors.ENDC}")
        data = data_generator(duration_ms=5000, sampling_rate=1000.0)
        
        print(f"{Colors.OKCYAN}Analyzing {scenario_name}...{Colors.ENDC}")
        results = analyzer.analyze(data)
        all_results.append((scenario_name, results))
        
        # Display results
        display_results(results, scenario_name)
        
        # Generate visualizations
        try:
            from eye_tracking.preprocessor import EyeTrackingPreprocessor
            preprocessor = EyeTrackingPreprocessor()
            processed_data = preprocessor.process(data)
            
            print(f"{Colors.OKCYAN}Generating visualizations...{Colors.ENDC}")
            
            # Save plots
            gaze_path = output_dir / f"gaze_path_{scenario_id}.png"
            risk_chart = output_dir / f"risk_scores_{scenario_id}.png"
            
            visualizer.plot_gaze_path(processed_data, save_path=str(gaze_path))
            visualizer.plot_risk_scores(results, save_path=str(risk_chart))
            
            print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Saved: {gaze_path}")
            print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Saved: {risk_chart}")
        except Exception as e:
            print(f"  {Colors.WARNING}Note: Visualization skipped ({e}){Colors.ENDC}")
        
        print()
    
    # Final comparison
    print_header("Comparison Summary")
    
    print(f"{Colors.BOLD}Risk Level Comparison:{Colors.ENDC}\n")
    for scenario_name, results in all_results:
        risk_level = results['summary']['overall_risk_level']
        highest_risk = results['summary']['highest_risk_disease'].upper()
        
        if risk_level == "Low":
            color = Colors.OKGREEN
        elif risk_level == "Moderate":
            color = Colors.WARNING
        else:
            color = Colors.FAIL
        
        print(f"  {scenario_name:30s} ", end="")
        print_colored(f"{risk_level:10s}", color), 
        print(f"  (Highest: {highest_risk})")
    
    print()
    print_colored(f"✓ Demo complete! Visualizations saved to: {output_dir}/", Colors.OKGREEN)
    print()


def run_custom_analysis():
    """Run analysis with custom parameters."""
    print_header("Custom Analysis")
    
    print(f"{Colors.BOLD}Configure your eye tracking data:{Colors.ENDC}\n")
    
    try:
        duration = float(input("Duration (ms) [default: 5000]: ") or "5000")
        sampling_rate = float(input("Sampling rate (Hz) [default: 1000]: ") or "1000")
        
        print(f"\n{Colors.BOLD}Select pattern type:{Colors.ENDC}")
        print("  1. Normal")
        print("  2. Parkinson's-like")
        print("  3. ADHD-like")
        
        choice = input("\nChoice [1-3]: ").strip()
        
        if choice == "1":
            data = generate_normal_data(duration, sampling_rate)
        elif choice == "2":
            data = generate_parkinsons_data(duration, sampling_rate)
        elif choice == "3":
            data = generate_adhd_data(duration, sampling_rate)
        else:
            print_colored("Invalid choice. Using normal pattern.", Colors.WARNING)
            data = generate_normal_data(duration, sampling_rate)
        
        # Analyze
        print(f"\n{Colors.OKCYAN}Analyzing...{Colors.ENDC}")
        analyzer = DiseaseAnalyzer()
        results = analyzer.analyze(data)
        
        # Display results
        display_results(results, "Custom Analysis")
        
        # Full report
        print(f"\n{Colors.BOLD}Do you want to see the detailed report? (y/n):{Colors.ENDC} ", end="")
        if input().lower() == 'y':
            print()
            report = analyzer.generate_report(results)
            print(report)
        
    except ValueError:
        print_colored("Invalid input. Please enter numeric values.", Colors.FAIL)
    except KeyboardInterrupt:
        print_colored("\n\nAnalysis cancelled.", Colors.WARNING)


def main_menu():
    """Display main menu and handle user choice."""
    while True:
        print_header("Eye Tracking Disease Detection - Interactive Demo")
        
        print(f"{Colors.BOLD}Main Menu:{Colors.ENDC}\n")
        print("  1. Run Scenario Comparison (Recommended)")
        print("  2. Custom Analysis")
        print("  3. View System Information")
        print("  4. Exit")
        print()
        
        choice = input(f"Select an option [1-4]: ").strip()
        
        if choice == "1":
            run_scenario_comparison()
            input(f"\nPress {Colors.OKGREEN}Enter{Colors.ENDC} to return to menu...")
        elif choice == "2":
            run_custom_analysis()
            input(f"\nPress {Colors.OKGREEN}Enter{Colors.ENDC} to return to menu...")
        elif choice == "3":
            print_header("System Information")
            print(f"{Colors.BOLD}Disease Detection Capabilities:{Colors.ENDC}")
            print("  • Parkinson's Disease detection")
            print("  • Alzheimer's Disease detection")
            print("  • Autism Spectrum Disorder (ASD) detection")
            print("  • ADHD detection")
            print()
            print(f"{Colors.BOLD}Analysis Features:{Colors.ENDC}")
            print("  • Saccade velocity and amplitude analysis")
            print("  • Fixation duration and distribution")
            print("  • Pupil dilation patterns")
            print("  • Spatial dispersion metrics")
            print("  • Risk scoring and level assessment")
            print()
            print(f"{Colors.BOLD}Output Formats:{Colors.ENDC}")
            print("  • Detailed text reports")
            print("  • Risk score visualizations")
            print("  • Gaze path plots")
            print("  • Event distribution charts")
            print()
            input(f"\nPress {Colors.OKGREEN}Enter{Colors.ENDC} to return to menu...")
        elif choice == "4":
            print_colored("\nThank you for using the Eye Tracking Disease Detection System!", Colors.OKGREEN)
            print_colored("Remember: This is a screening tool, not a diagnostic tool.", Colors.WARNING)
            print_colored("Always consult healthcare professionals for medical advice.\n", Colors.WARNING)
            break
        else:
            print_colored("Invalid choice. Please select 1-4.", Colors.FAIL)
            input(f"\nPress {Colors.OKGREEN}Enter{Colors.ENDC} to continue...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print_colored("\n\nDemo interrupted by user. Goodbye!", Colors.WARNING)
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n\nUnexpected error: {e}", Colors.FAIL)
        import traceback
        traceback.print_exc()
        sys.exit(1)
