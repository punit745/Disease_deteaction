#!/usr/bin/env python3
"""
System Validation Script for Eye Tracking Disease Detection System

This script validates that all components of the system are working correctly
and provides diagnostic information for troubleshooting.
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path


class Colors:
    """ANSI color codes."""
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_test(name, passed, details=""):
    """Print test result."""
    status = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}" if passed else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
    print(f"  {status} - {name}")
    if details and not passed:
        print(f"         {details}")


def print_section(name):
    """Print section header."""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{name}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}")


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    passed = version.major >= 3 and version.minor >= 7
    details = f"Python {version.major}.{version.minor}.{version.micro}"
    return passed, details


def check_module(module_name):
    """Check if a Python module can be imported."""
    try:
        importlib.import_module(module_name)
        return True, ""
    except ImportError as e:
        return False, str(e)


def check_core_dependencies():
    """Check all core dependencies."""
    dependencies = [
        'numpy',
        'pandas',
        'scipy',
        'sklearn',
        'matplotlib',
        'seaborn'
    ]
    
    results = {}
    for dep in dependencies:
        passed, details = check_module(dep)
        results[dep] = (passed, details)
    
    return results


def check_web_dependencies():
    """Check web application dependencies."""
    dependencies = [
        'flask',
        'flask_sqlalchemy',
        'flask_cors',
        'jwt',
        'werkzeug'
    ]
    
    results = {}
    for dep in dependencies:
        passed, details = check_module(dep)
        results[dep] = (passed, details)
    
    return results


def check_eye_tracking_module():
    """Check if the eye_tracking module works."""
    try:
        from eye_tracking import (
            EyeTrackingData,
            DiseaseAnalyzer,
            EyeTrackingPreprocessor,
            FeatureExtractor
        )
        return True, "All components imported successfully"
    except Exception as e:
        return False, str(e)


def check_database():
    """Check if database can be initialized."""
    try:
        # Check if app.py can be imported
        from app import db, init_db
        
        # Check if database file exists or can be created
        db_path = Path("disease_detection.db")
        if db_path.exists():
            return True, "Database file exists"
        else:
            return True, "Database can be initialized"
    except Exception as e:
        return False, str(e)


def check_visualization():
    """Check if visualization works."""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        from eye_tracking.visualizer import Visualizer
        return True, "Visualization module available"
    except Exception as e:
        return False, str(e)


def run_functional_test():
    """Run a functional test of the analysis pipeline."""
    try:
        import numpy as np
        from eye_tracking import EyeTrackingData, DiseaseAnalyzer
        
        # Generate test data
        timestamps = np.linspace(0, 1000, 1000)
        x_positions = 500 + np.random.normal(0, 2, 1000)
        y_positions = 400 + np.random.normal(0, 2, 1000)
        
        data = EyeTrackingData(
            timestamps=timestamps,
            x_positions=x_positions,
            y_positions=y_positions,
            sampling_rate=1000.0
        )
        
        # Analyze
        analyzer = DiseaseAnalyzer()
        results = analyzer.analyze(data)
        
        # Verify results structure
        assert 'disease_analysis' in results
        assert 'summary' in results
        assert 'features' in results
        
        # Verify diseases analyzed
        assert 'parkinsons' in results['disease_analysis']
        assert 'alzheimers' in results['disease_analysis']
        assert 'asd' in results['disease_analysis']
        assert 'adhd' in results['disease_analysis']
        
        return True, "Analysis pipeline working correctly"
    except Exception as e:
        return False, str(e)


def check_files():
    """Check if required files exist."""
    required_files = [
        'README.md',
        'requirements.txt',
        'requirements-web.txt',
        'app.py',
        'cli.py',
        'example_usage.py',
        'eye_tracking/__init__.py',
        'eye_tracking/analyzer.py',
        'eye_tracking/data_models.py',
        'eye_tracking/disease_detectors.py',
        'eye_tracking/feature_extractor.py',
        'eye_tracking/preprocessor.py',
        'eye_tracking/visualizer.py'
    ]
    
    results = {}
    for file_path in required_files:
        path = Path(file_path)
        results[file_path] = path.exists()
    
    return results


def main():
    """Main validation function."""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}Eye Tracking Disease Detection System - Validation{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    all_passed = True
    
    # 1. Python version
    print_section("Python Environment")
    passed, details = check_python_version()
    print_test(f"Python Version (>=3.7)", passed, details if not passed else "")
    if passed:
        print(f"         {details}")
    all_passed &= passed
    
    # 2. Core dependencies
    print_section("Core Dependencies")
    core_deps = check_core_dependencies()
    for dep, (passed, details) in core_deps.items():
        print_test(dep, passed, details)
        all_passed &= passed
    
    # 3. Web dependencies
    print_section("Web Application Dependencies")
    web_deps = check_web_dependencies()
    for dep, (passed, details) in web_deps.items():
        print_test(dep, passed, details)
        all_passed &= passed
    
    # 4. Required files
    print_section("Required Files")
    files = check_files()
    for file_path, exists in files.items():
        print_test(file_path, exists, f"File not found: {file_path}")
        all_passed &= exists
    
    # 5. Eye tracking module
    print_section("Eye Tracking Module")
    passed, details = check_eye_tracking_module()
    print_test("Module import", passed, details)
    if passed:
        print(f"         {details}")
    all_passed &= passed
    
    # 6. Visualization
    print_section("Visualization System")
    passed, details = check_visualization()
    print_test("Matplotlib and Visualizer", passed, details)
    if passed:
        print(f"         {details}")
    # Don't fail if visualization has issues
    
    # 7. Database
    print_section("Database System")
    passed, details = check_database()
    print_test("Database module", passed, details)
    if passed:
        print(f"         {details}")
    # Don't fail if database has issues
    
    # 8. Functional test
    print_section("Functional Tests")
    passed, details = run_functional_test()
    print_test("Analysis pipeline", passed, details)
    if passed:
        print(f"         {details}")
    all_passed &= passed
    
    # Summary
    print_section("Summary")
    
    if all_passed:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ All critical tests passed!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}The system is ready to use.{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Next steps:{Colors.ENDC}")
        print("  1. Run example: python example_usage.py")
        print("  2. Try interactive demo: python interactive_demo.py")
        print("  3. Start web app: python app.py")
        print("  4. Use CLI: python cli.py --help")
        print()
        
        return 0
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}✗ Some tests failed!{Colors.ENDC}")
        print(f"{Colors.WARNING}Please check the errors above and ensure all dependencies are installed.{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}To fix issues:{Colors.ENDC}")
        print("  1. Run the setup script: python local_setup.py")
        print("  2. Manually install dependencies:")
        print("     pip install -r requirements.txt")
        print("     pip install -r requirements-web.txt")
        print("  3. Check the LOCAL_DEPLOYMENT_GUIDE.md for troubleshooting")
        print()
        
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Validation interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
