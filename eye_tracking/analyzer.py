"""
Main disease analyzer that coordinates the entire analysis pipeline.
"""

from typing import Dict, List, Optional, Any
from .data_models import EyeTrackingData
from .preprocessor import EyeTrackingPreprocessor
from .feature_extractor import FeatureExtractor
from .disease_detectors import (
    ParkinsonsDetector,
    AlzheimersDetector,
    ASDDetector,
    ADHDDetector
)


class DiseaseAnalyzer:
    """
    Main analyzer for detecting neurological and developmental disorders
    from eye tracking data.
    """
    
    def __init__(self):
        """Initialize the analyzer with all components."""
        self.preprocessor = EyeTrackingPreprocessor()
        self.feature_extractor = FeatureExtractor()
        self.parkinsons_detector = ParkinsonsDetector()
        self.alzheimers_detector = AlzheimersDetector()
        self.asd_detector = ASDDetector()
        self.adhd_detector = ADHDDetector()
    
    def analyze(self, data: EyeTrackingData, 
                diseases: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform complete analysis on eye tracking data.
        
        Args:
            data: Raw eye tracking data
            diseases: List of diseases to check. If None, checks all.
                     Options: ['parkinsons', 'alzheimers', 'asd', 'adhd']
        
        Returns:
            Complete analysis results including risk scores for all diseases
        """
        # Default to checking all diseases
        if diseases is None:
            diseases = ['parkinsons', 'alzheimers', 'asd', 'adhd']
        
        # Preprocess data
        processed_data = self.preprocessor.process(data)
        
        # Extract features
        features = self.feature_extractor.extract_all_features(processed_data)
        
        # Analyze for each disease
        results = {
            'subject_id': data.subject_id,
            'session_id': data.session_id,
            'task_type': data.task_type,
            'features': features,
            'disease_analysis': {}
        }
        
        if 'parkinsons' in diseases:
            results['disease_analysis']['parkinsons'] = self.parkinsons_detector.analyze(features)
        
        if 'alzheimers' in diseases:
            results['disease_analysis']['alzheimers'] = self.alzheimers_detector.analyze(features)
        
        if 'asd' in diseases:
            results['disease_analysis']['asd'] = self.asd_detector.analyze(features)
        
        if 'adhd' in diseases:
            results['disease_analysis']['adhd'] = self.adhd_detector.analyze(features)
        
        # Add summary
        results['summary'] = self._generate_summary(results['disease_analysis'])
        
        return results
    
    def _generate_summary(self, disease_analysis: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Generate summary of all disease analyses.
        
        Args:
            disease_analysis: Dictionary of disease-specific analyses
        
        Returns:
            Summary with highest risk disease and overall recommendations
        """
        if not disease_analysis:
            return {
                'highest_risk_disease': None,
                'highest_risk_score': 0.0,
                'overall_recommendations': []
            }
        
        # Find disease with highest risk
        highest_risk_disease = None
        highest_risk_score = 0.0
        
        for disease, analysis in disease_analysis.items():
            if analysis['risk_score'] > highest_risk_score:
                highest_risk_score = analysis['risk_score']
                highest_risk_disease = disease
        
        # Collect all recommendations
        all_recommendations = []
        for analysis in disease_analysis.values():
            all_recommendations.extend(analysis['recommendations'])
        
        # Remove duplicates while preserving order
        unique_recommendations = []
        seen = set()
        for rec in all_recommendations:
            if rec not in seen:
                unique_recommendations.append(rec)
                seen.add(rec)
        
        return {
            'highest_risk_disease': highest_risk_disease,
            'highest_risk_score': highest_risk_score,
            'overall_recommendations': unique_recommendations,
            'risk_level': self._get_overall_risk_level(highest_risk_score)
        }
    
    def _get_overall_risk_level(self, score: float) -> str:
        """Categorize overall risk level based on score."""
        if score < 0.3:
            return "Low"
        elif score < 0.6:
            return "Moderate"
        else:
            return "High"
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable report from analysis results.
        
        Args:
            results: Analysis results from analyze()
        
        Returns:
            Formatted text report
        """
        report = []
        report.append("=" * 70)
        report.append("EYE TRACKING DISEASE DETECTION REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Subject information
        if results.get('subject_id'):
            report.append(f"Subject ID: {results['subject_id']}")
        if results.get('session_id'):
            report.append(f"Session ID: {results['session_id']}")
        if results.get('task_type'):
            report.append(f"Task Type: {results['task_type']}")
        report.append("")
        
        # Summary
        summary = results.get('summary', {})
        report.append("OVERALL ASSESSMENT")
        report.append("-" * 70)
        report.append(f"Risk Level: {summary.get('risk_level', 'Unknown')}")
        if summary.get('highest_risk_disease'):
            report.append(f"Highest Risk: {summary['highest_risk_disease'].upper()} "
                         f"(Score: {summary['highest_risk_score']:.2f})")
        report.append("")
        
        # Disease-specific analyses
        report.append("DISEASE-SPECIFIC ANALYSIS")
        report.append("-" * 70)
        
        for disease, analysis in results.get('disease_analysis', {}).items():
            report.append(f"\n{disease.upper()}")
            report.append(f"  Risk Score: {analysis['risk_score']:.2f}")
            report.append(f"  Risk Level: {analysis['risk_level']}")
            
            if analysis['indicators']:
                report.append("  Indicators:")
                for indicator in analysis['indicators']:
                    report.append(f"    - {indicator}")
            else:
                report.append("  Indicators: None detected")
            
            if analysis['recommendations']:
                report.append("  Recommendations:")
                for rec in analysis['recommendations']:
                    report.append(f"    - {rec}")
        
        report.append("")
        report.append("=" * 70)
        report.append("Note: This analysis is for screening purposes only.")
        report.append("Please consult healthcare professionals for diagnosis.")
        report.append("=" * 70)
        
        return "\n".join(report)
