"""
Comprehensive test suite for the Disease Detection System.

This script tests the entire system including:
- Core disease detection functionality
- Web API endpoints
- Database operations
- Authentication and authorization
"""

import sys
import unittest
import json
import numpy as np
import requests
from datetime import datetime

# Test configuration
API_BASE_URL = "http://localhost:5000"
TEST_EMAIL = "test_user_{}@example.com".format(datetime.now().timestamp())
TEST_PASSWORD = "SecureTestPassword123!"


class TestDiseaseDetectionCore(unittest.TestCase):
    """Test core disease detection functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        from eye_tracking import EyeTrackingData, DiseaseAnalyzer
        self.EyeTrackingData = EyeTrackingData
        self.DiseaseAnalyzer = DiseaseAnalyzer
    
    def test_data_model_creation(self):
        """Test creating eye tracking data."""
        timestamps = np.array([0, 1, 2, 3, 4])
        x_positions = np.array([100, 102, 105, 108, 110])
        y_positions = np.array([200, 198, 195, 193, 190])
        
        data = self.EyeTrackingData(
            timestamps=timestamps,
            x_positions=x_positions,
            y_positions=y_positions,
            sampling_rate=1000.0
        )
        
        self.assertEqual(data.num_samples, 5)
        self.assertAlmostEqual(data.duration, 4.0)
    
    def test_disease_analysis(self):
        """Test disease analysis."""
        # Generate sample data
        num_samples = 5000
        timestamps = np.linspace(0, 5000, num_samples)
        x_positions = 500 + np.random.normal(0, 2, num_samples)
        y_positions = 400 + np.random.normal(0, 2, num_samples)
        
        data = self.EyeTrackingData(
            timestamps=timestamps,
            x_positions=x_positions,
            y_positions=y_positions,
            sampling_rate=1000.0
        )
        
        analyzer = self.DiseaseAnalyzer()
        results = analyzer.analyze(data)
        
        # Verify results structure
        self.assertIn('disease_analysis', results)
        self.assertIn('summary', results)
        self.assertIn('features', results)
        
        # Verify all diseases analyzed
        self.assertIn('parkinsons', results['disease_analysis'])
        self.assertIn('alzheimers', results['disease_analysis'])
        self.assertIn('asd', results['disease_analysis'])
        self.assertIn('adhd', results['disease_analysis'])
    
    def test_report_generation(self):
        """Test report generation."""
        num_samples = 1000
        timestamps = np.linspace(0, 1000, num_samples)
        x_positions = 500 + np.random.normal(0, 2, num_samples)
        y_positions = 400 + np.random.normal(0, 2, num_samples)
        
        data = self.EyeTrackingData(
            timestamps=timestamps,
            x_positions=x_positions,
            y_positions=y_positions,
            sampling_rate=1000.0,
            subject_id="TEST_001"
        )
        
        analyzer = self.DiseaseAnalyzer()
        results = analyzer.analyze(data)
        report = analyzer.generate_report(results)
        
        # Verify report content
        self.assertIn("EYE TRACKING DISEASE DETECTION REPORT", report)
        self.assertIn("TEST_001", report)
        self.assertIn("PARKINSONS", report)
        self.assertIn("Risk Score", report)


class TestWebAPI(unittest.TestCase):
    """Test Web API endpoints."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test user and token."""
        # Check if API is available
        try:
            response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
            if response.status_code != 200:
                raise Exception("API not available")
        except:
            print("\nWarning: API not running. Skipping web API tests.")
            print("Start the app with: python app.py")
            cls.skip_tests = True
            return
        
        cls.skip_tests = False
        
        # Register test user
        register_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/auth/register", json=register_data)
        if response.status_code != 201:
            # User might already exist
            pass
        
        # Login
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{API_BASE_URL}/api/auth/login", json=login_data)
        cls.token = response.json()["token"]
        cls.headers = {"Authorization": f"Bearer {cls.token}"}
    
    def setUp(self):
        """Skip tests if API not available."""
        if self.__class__.skip_tests:
            self.skipTest("API not available")
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = requests.get(f"{API_BASE_URL}/api/health")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)
    
    def test_authentication_required(self):
        """Test that protected endpoints require authentication."""
        response = requests.get(f"{API_BASE_URL}/api/user/profile")
        self.assertEqual(response.status_code, 401)
    
    def test_get_profile(self):
        """Test getting user profile."""
        response = requests.get(f"{API_BASE_URL}/api/user/profile", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('email', data)
        self.assertIn('first_name', data)
    
    def test_analyze_data(self):
        """Test analyzing eye tracking data via API."""
        # Generate sample data
        num_samples = 1000
        analysis_data = {
            "timestamps": list(np.linspace(0, 1000, num_samples)),
            "x_positions": list(500 + np.random.normal(0, 2, num_samples)),
            "y_positions": list(400 + np.random.normal(0, 2, num_samples)),
            "sampling_rate": 1000.0,
            "task_type": "test"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json=analysis_data,
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('test_id', data)
        self.assertIn('results', data)
        
        # Store test_id for other tests
        self.__class__.test_id = data['test_id']
    
    def test_get_results(self):
        """Test getting all results."""
        response = requests.get(f"{API_BASE_URL}/api/results", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('total', data)
    
    def test_get_specific_result(self):
        """Test getting specific result."""
        if not hasattr(self.__class__, 'test_id'):
            self.skipTest("No test_id available")
        
        response = requests.get(
            f"{API_BASE_URL}/api/results/{self.test_id}",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('test_info', data)
        self.assertIn('disease_analysis', data)
    
    def test_get_report(self):
        """Test getting test report."""
        if not hasattr(self.__class__, 'test_id'):
            self.skipTest("No test_id available")
        
        response = requests.get(
            f"{API_BASE_URL}/api/results/{self.test_id}/report",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('report', data)
    
    def test_get_statistics(self):
        """Test getting user statistics."""
        response = requests.get(f"{API_BASE_URL}/api/statistics", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('statistics', data)


class TestDataValidation(unittest.TestCase):
    """Test data validation and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        from eye_tracking import EyeTrackingData
        self.EyeTrackingData = EyeTrackingData
    
    def test_invalid_data_lengths(self):
        """Test that mismatched array lengths raise error."""
        with self.assertRaises(ValueError):
            self.EyeTrackingData(
                timestamps=np.array([0, 1, 2]),
                x_positions=np.array([100, 102]),  # Wrong length
                y_positions=np.array([200, 198, 195])
            )
    
    def test_pupil_size_validation(self):
        """Test pupil size array validation."""
        with self.assertRaises(ValueError):
            self.EyeTrackingData(
                timestamps=np.array([0, 1, 2]),
                x_positions=np.array([100, 102, 105]),
                y_positions=np.array([200, 198, 195]),
                pupil_sizes=np.array([3.0, 3.1])  # Wrong length
            )


def run_tests():
    """Run all tests and generate report."""
    print("\n" + "=" * 70)
    print("DISEASE DETECTION SYSTEM - TEST SUITE")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDiseaseDetectionCore))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestWebAPI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
