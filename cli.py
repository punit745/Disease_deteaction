"""
Command-line interface for the Disease Detection System.

This CLI allows patients to interact with the disease detection system
from the command line.
"""

import argparse
import json
import sys
from datetime import datetime
from getpass import getpass
import requests
import numpy as np


class DiseaseDetectionCLI:
    """Command-line interface for disease detection."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """Initialize CLI with base URL."""
        self.base_url = base_url
        self.token = None
        self.user = None
    
    def register(self, email: str, password: str, first_name: str, last_name: str):
        """Register a new user."""
        data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/register", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"✓ Registration successful!")
            print(f"  User ID: {result['user']['id']}")
            print(f"  Email: {result['user']['email']}")
            return True
        except requests.exceptions.HTTPError as e:
            print(f"✗ Registration failed: {e.response.json().get('message', str(e))}")
            return False
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return False
    
    def login(self, email: str, password: str):
        """Login and store authentication token."""
        data = {
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", json=data)
            response.raise_for_status()
            result = response.json()
            self.token = result['token']
            self.user = result['user']
            print(f"✓ Login successful!")
            print(f"  Welcome, {self.user['first_name']} {self.user['last_name']}")
            return True
        except requests.exceptions.HTTPError as e:
            print(f"✗ Login failed: {e.response.json().get('message', str(e))}")
            return False
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return False
    
    def get_headers(self):
        """Get authentication headers."""
        if not self.token:
            raise ValueError("Not authenticated. Please login first.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def analyze_file(self, file_path: str):
        """Analyze eye tracking data from a JSON file."""
        try:
            # Load data from file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            print(f"Loading eye tracking data from {file_path}...")
            print(f"  Samples: {len(data.get('timestamps', []))}")
            print(f"  Task type: {data.get('task_type', 'general')}")
            
            # Submit for analysis
            response = requests.post(
                f"{self.base_url}/api/analyze",
                json=data,
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"\n✓ Analysis completed!")
            print(f"  Test ID: {result['test_id']}")
            print(f"\nRISK ASSESSMENT:")
            
            summary = result['results']['summary']
            print(f"  Overall Risk Level: {summary['risk_level']}")
            print(f"  Highest Risk: {summary['highest_risk_disease'].upper() if summary['highest_risk_disease'] else 'None'}")
            
            print(f"\nDETAILED SCORES:")
            for disease, analysis in result['results']['disease_analysis'].items():
                print(f"  {disease.upper()}: {analysis['risk_score']:.2f} ({analysis['risk_level']})")
            
            return result['test_id']
            
        except FileNotFoundError:
            print(f"✗ File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON file")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"✗ Analysis failed: {e.response.json().get('message', str(e))}")
            return None
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return None
    
    def analyze_sample(self):
        """Analyze sample/demo data."""
        print("Generating sample eye tracking data...")
        
        # Generate sample data
        duration_ms = 5000
        sampling_rate = 1000.0
        num_samples = int(duration_ms * sampling_rate / 1000)
        
        timestamps = list(np.linspace(0, duration_ms, num_samples))
        
        # Generate realistic eye movement data
        x_positions = []
        y_positions = []
        current_x, current_y = 500, 400
        
        for i in range(num_samples):
            # Add noise for fixations
            x_positions.append(current_x + np.random.normal(0, 2))
            y_positions.append(current_y + np.random.normal(0, 2))
            
            # Random saccades
            if np.random.random() < 0.01:
                current_x += np.random.normal(0, 50)
                current_y += np.random.normal(0, 50)
                current_x = np.clip(current_x, 100, 900)
                current_y = np.clip(current_y, 100, 700)
        
        data = {
            "timestamps": timestamps,
            "x_positions": x_positions,
            "y_positions": y_positions,
            "sampling_rate": sampling_rate,
            "task_type": "visual_search"
        }
        
        print(f"  Generated {num_samples} samples")
        
        # Submit for analysis
        try:
            response = requests.post(
                f"{self.base_url}/api/analyze",
                json=data,
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"\n✓ Analysis completed!")
            print(f"  Test ID: {result['test_id']}")
            print(f"\nRISK ASSESSMENT:")
            
            summary = result['results']['summary']
            print(f"  Overall Risk Level: {summary['risk_level']}")
            print(f"  Highest Risk: {summary['highest_risk_disease'].upper() if summary['highest_risk_disease'] else 'None'}")
            
            print(f"\nDETAILED SCORES:")
            for disease, analysis in result['results']['disease_analysis'].items():
                print(f"  {disease.upper()}: {analysis['risk_score']:.2f} ({analysis['risk_level']})")
            
            return result['test_id']
            
        except requests.exceptions.HTTPError as e:
            print(f"✗ Analysis failed: {e.response.json().get('message', str(e))}")
            return None
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return None
    
    def list_results(self, page: int = 1, per_page: int = 10):
        """List all test results."""
        try:
            response = requests.get(
                f"{self.base_url}/api/results?page={page}&per_page={per_page}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            if result['total'] == 0:
                print("No test results found.")
                return
            
            print(f"\nTest Results (Page {result['current_page']} of {result['pages']}):")
            print(f"Total: {result['total']} tests\n")
            
            for test in result['results']:
                print(f"Test ID: {test['id']}")
                print(f"  Date: {test['test_date']}")
                print(f"  Task: {test['task_type']}")
                print(f"  Risk Level: {test['overall_risk_level']}")
                print(f"  Highest Risk: {test['highest_risk_disease'].upper() if test['highest_risk_disease'] else 'None'}")
                print()
            
        except requests.exceptions.HTTPError as e:
            print(f"✗ Failed to retrieve results: {e.response.json().get('message', str(e))}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    def get_result(self, test_id: int):
        """Get detailed result for a specific test."""
        try:
            response = requests.get(
                f"{self.base_url}/api/results/{test_id}",
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            test_info = result['test_info']
            print(f"\nTest ID: {test_info['id']}")
            print(f"Date: {test_info['test_date']}")
            print(f"Task: {test_info['task_type']}")
            print(f"Duration: {test_info['duration_ms']:.1f} ms")
            print(f"Samples: {test_info['num_samples']}")
            
            print(f"\nRISK SCORES:")
            for disease, score in test_info['risk_scores'].items():
                print(f"  {disease.upper()}: {score:.2f}")
            
            print(f"\nDETAILED ANALYSIS:")
            for disease, analysis in result['disease_analysis'].items():
                print(f"\n{disease.upper()}:")
                print(f"  Risk: {analysis['risk_score']:.2f} ({analysis['risk_level']})")
                
                if analysis['indicators']:
                    print(f"  Indicators:")
                    for indicator in analysis['indicators']:
                        print(f"    - {indicator}")
                
                if analysis['recommendations']:
                    print(f"  Recommendations:")
                    for rec in analysis['recommendations']:
                        print(f"    - {rec}")
            
        except requests.exceptions.HTTPError as e:
            print(f"✗ Failed to retrieve result: {e.response.json().get('message', str(e))}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    def get_report(self, test_id: int):
        """Get detailed report for a test."""
        try:
            response = requests.get(
                f"{self.base_url}/api/results/{test_id}/report",
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"\n{result['report']}")
            
        except requests.exceptions.HTTPError as e:
            print(f"✗ Failed to generate report: {e.response.json().get('message', str(e))}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    def get_statistics(self):
        """Get user statistics."""
        try:
            response = requests.get(
                f"{self.base_url}/api/statistics",
                headers=self.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            if not result.get('statistics'):
                print("No test data available yet.")
                return
            
            stats = result['statistics']
            print(f"\nUSER STATISTICS:")
            print(f"  Total Tests: {stats['total_tests']}")
            print(f"  Latest Test: {stats['latest_test_date']}")
            
            print(f"\nRISK LEVEL DISTRIBUTION:")
            for level, count in stats['risk_level_distribution'].items():
                print(f"  {level}: {count} tests")
            
            print(f"\nRISK TRENDS (most recent to oldest):")
            for disease, trends in stats['risk_trends'].items():
                if trends:
                    avg = sum(trends) / len(trends)
                    print(f"  {disease.upper()}: avg {avg:.2f} ({len(trends)} tests)")
            
        except requests.exceptions.HTTPError as e:
            print(f"✗ Failed to retrieve statistics: {e.response.json().get('message', str(e))}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Disease Detection System - Patient CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Register a new account
  python cli.py register

  # Login
  python cli.py login

  # Analyze sample data
  python cli.py analyze --sample

  # Analyze data from file
  python cli.py analyze --file data.json

  # List all test results
  python cli.py results

  # Get specific test result
  python cli.py result 42

  # Get test report
  python cli.py report 42

  # Get statistics
  python cli.py stats
        """
    )
    
    parser.add_argument('command', choices=[
        'register', 'login', 'analyze', 'results', 'result', 'report', 'stats'
    ], help='Command to execute')
    
    parser.add_argument('--url', default='http://localhost:5000',
                       help='API base URL (default: http://localhost:5000)')
    parser.add_argument('--file', help='Path to eye tracking data file (JSON)')
    parser.add_argument('--sample', action='store_true',
                       help='Use sample/demo data for analysis')
    parser.add_argument('--page', type=int, default=1,
                       help='Page number for results (default: 1)')
    parser.add_argument('--per-page', type=int, default=10,
                       help='Results per page (default: 10)')
    parser.add_argument('test_id', nargs='?', type=int,
                       help='Test ID for result/report commands')
    
    args = parser.parse_args()
    
    cli = DiseaseDetectionCLI(base_url=args.url)
    
    if args.command == 'register':
        print("=== User Registration ===\n")
        email = input("Email: ")
        password = getpass("Password: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        cli.register(email, password, first_name, last_name)
    
    elif args.command == 'login':
        print("=== User Login ===\n")
        email = input("Email: ")
        password = getpass("Password: ")
        cli.login(email, password)
    
    elif args.command == 'analyze':
        print("=== Analyze Eye Tracking Data ===\n")
        email = input("Email: ")
        password = getpass("Password: ")
        
        if not cli.login(email, password):
            sys.exit(1)
        
        if args.sample:
            cli.analyze_sample()
        elif args.file:
            cli.analyze_file(args.file)
        else:
            print("✗ Please specify --sample or --file")
            sys.exit(1)
    
    elif args.command == 'results':
        print("=== Test Results ===\n")
        email = input("Email: ")
        password = getpass("Password: ")
        
        if not cli.login(email, password):
            sys.exit(1)
        
        cli.list_results(page=args.page, per_page=args.per_page)
    
    elif args.command == 'result':
        if not args.test_id:
            print("✗ Test ID is required")
            sys.exit(1)
        
        print("=== Test Result Details ===\n")
        email = input("Email: ")
        password = getpass("Password: ")
        
        if not cli.login(email, password):
            sys.exit(1)
        
        cli.get_result(args.test_id)
    
    elif args.command == 'report':
        if not args.test_id:
            print("✗ Test ID is required")
            sys.exit(1)
        
        print("=== Test Report ===\n")
        email = input("Email: ")
        password = getpass("Password: ")
        
        if not cli.login(email, password):
            sys.exit(1)
        
        cli.get_report(args.test_id)
    
    elif args.command == 'stats':
        print("=== User Statistics ===\n")
        email = input("Email: ")
        password = getpass("Password: ")
        
        if not cli.login(email, password):
            sys.exit(1)
        
        cli.get_statistics()


if __name__ == '__main__':
    main()
