"""
Flask Web Application for Disease Detection System.

This module provides a web interface for patients to:
- Upload eye tracking data
- View analysis results
- Track their health over time
- Access historical reports
"""

import os
import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Any

from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import jwt
import numpy as np

from eye_tracking import EyeTrackingData, DiseaseAnalyzer
from eye_tracking.visualizer import Visualizer

# Initialize Flask app
app = Flask(__name__)

# Security check for production
if os.environ.get('FLASK_ENV') == 'production':
    if os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production') == 'dev-secret-key-change-in-production':
        raise RuntimeError("SECRET_KEY must be set in production. Set the SECRET_KEY environment variable.")
    if os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production') == 'jwt-secret-key-change-in-production':
        raise RuntimeError("JWT_SECRET_KEY must be set in production. Set the JWT_SECRET_KEY environment variable.")

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///disease_detection.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_EXPIRATION_HOURS'] = 24

# Enable CORS
CORS(app)

# Initialize database
db = SQLAlchemy(app)

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Database Models
class User(db.Model):
    """User model for patient authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    test_results = db.relationship('TestResult', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password: str):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Verify password."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class TestResult(db.Model):
    """Model for storing disease detection test results."""
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    test_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    task_type = db.Column(db.String(50))
    duration_ms = db.Column(db.Float)
    num_samples = db.Column(db.Integer)
    
    # Risk scores
    parkinsons_risk = db.Column(db.Float)
    alzheimers_risk = db.Column(db.Float)
    asd_risk = db.Column(db.Float)
    adhd_risk = db.Column(db.Float)
    overall_risk_level = db.Column(db.String(20))
    highest_risk_disease = db.Column(db.String(50))
    
    # Results stored as JSON
    full_results = db.Column(db.Text)  # JSON string
    features = db.Column(db.Text)  # JSON string
    
    # File references
    data_file_path = db.Column(db.String(256))
    report_file_path = db.Column(db.String(256))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert test result to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'test_date': self.test_date.isoformat(),
            'task_type': self.task_type,
            'duration_ms': self.duration_ms,
            'num_samples': self.num_samples,
            'risk_scores': {
                'parkinsons': self.parkinsons_risk,
                'alzheimers': self.alzheimers_risk,
                'asd': self.asd_risk,
                'adhd': self.adhd_risk
            },
            'overall_risk_level': self.overall_risk_level,
            'highest_risk_disease': self.highest_risk_disease
        }


# Authentication decorator
def token_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user or not current_user.is_active:
                return jsonify({'message': 'User not found or inactive'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.fromisoformat(data['date_of_birth']) if 'date_of_birth' in data else None
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'message': 'Account is inactive'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS'])
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500


@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get current user profile."""
    return jsonify(current_user.to_dict())


@app.route('/api/user/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile."""
    try:
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            current_user.first_name = data['first_name']
        if 'last_name' in data:
            current_user.last_name = data['last_name']
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                current_user.date_of_birth = datetime.fromisoformat(data['date_of_birth'])
            except (ValueError, TypeError):
                return jsonify({'message': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DD)'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Update failed: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
@token_required
def analyze_data(current_user):
    """Analyze eye tracking data and return results."""
    try:
        data = request.get_json()
        
        # Validate input data
        required_fields = ['timestamps', 'x_positions', 'y_positions']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Create eye tracking data object
        eye_data = EyeTrackingData(
            timestamps=np.array(data['timestamps']),
            x_positions=np.array(data['x_positions']),
            y_positions=np.array(data['y_positions']),
            pupil_sizes=np.array(data['pupil_sizes']) if 'pupil_sizes' in data else None,
            sampling_rate=data.get('sampling_rate', 1000.0),
            subject_id=f"USER_{current_user.id}",
            task_type=data.get('task_type', 'general')
        )
        
        # Perform analysis
        analyzer = DiseaseAnalyzer()
        results = analyzer.analyze(eye_data)
        
        # Store results in database
        test_result = TestResult(
            user_id=current_user.id,
            task_type=eye_data.task_type,
            duration_ms=eye_data.duration,
            num_samples=eye_data.num_samples,
            parkinsons_risk=results['disease_analysis'].get('parkinsons', {}).get('risk_score', 0),
            alzheimers_risk=results['disease_analysis'].get('alzheimers', {}).get('risk_score', 0),
            asd_risk=results['disease_analysis'].get('asd', {}).get('risk_score', 0),
            adhd_risk=results['disease_analysis'].get('adhd', {}).get('risk_score', 0),
            overall_risk_level=results['summary'].get('risk_level'),
            highest_risk_disease=results['summary'].get('highest_risk_disease'),
            full_results=json.dumps(results['disease_analysis']),
            features=json.dumps(results['features'])
        )
        
        db.session.add(test_result)
        db.session.commit()
        
        return jsonify({
            'message': 'Analysis completed successfully',
            'test_id': test_result.id,
            'results': {
                'disease_analysis': results['disease_analysis'],
                'summary': results['summary'],
                'test_date': test_result.test_date.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'message': f'Analysis failed: {str(e)}'}), 500


@app.route('/api/results', methods=['GET'])
@token_required
def get_results(current_user):
    """Get all test results for current user."""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query results with pagination
        pagination = TestResult.query.filter_by(user_id=current_user.id)\
            .order_by(TestResult.test_date.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'results': [result.to_dict() for result in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'message': f'Failed to retrieve results: {str(e)}'}), 500


@app.route('/api/results/<int:test_id>', methods=['GET'])
@token_required
def get_result(current_user, test_id):
    """Get detailed result for a specific test."""
    try:
        result = TestResult.query.filter_by(id=test_id, user_id=current_user.id).first()
        
        if not result:
            return jsonify({'message': 'Test result not found'}), 404
        
        # Parse JSON fields
        full_results = json.loads(result.full_results) if result.full_results else {}
        features = json.loads(result.features) if result.features else {}
        
        return jsonify({
            'test_info': result.to_dict(),
            'disease_analysis': full_results,
            'features': features
        })
        
    except Exception as e:
        return jsonify({'message': f'Failed to retrieve result: {str(e)}'}), 500


@app.route('/api/results/<int:test_id>/report', methods=['GET'])
@token_required
def get_report(current_user, test_id):
    """Generate and return a detailed report for a test."""
    try:
        result = TestResult.query.filter_by(id=test_id, user_id=current_user.id).first()
        
        if not result:
            return jsonify({'message': 'Test result not found'}), 404
        
        # Parse results
        disease_analysis = json.loads(result.full_results) if result.full_results else {}
        features = json.loads(result.features) if result.features else {}
        
        # Generate report
        analyzer = DiseaseAnalyzer()
        full_results = {
            'subject_id': f"USER_{current_user.id}",
            'task_type': result.task_type,
            'disease_analysis': disease_analysis,
            'summary': {
                'risk_level': result.overall_risk_level,
                'highest_risk_disease': result.highest_risk_disease,
                'highest_risk_score': max(
                    result.parkinsons_risk or 0,
                    result.alzheimers_risk or 0,
                    result.asd_risk or 0,
                    result.adhd_risk or 0
                )
            }
        }
        
        report = analyzer.generate_report(full_results)
        
        return jsonify({
            'report': report,
            'test_date': result.test_date.isoformat()
        })
        
    except Exception as e:
        return jsonify({'message': f'Failed to generate report: {str(e)}'}), 500


@app.route('/api/statistics', methods=['GET'])
@token_required
def get_statistics(current_user):
    """Get statistical summary of user's test history."""
    try:
        results = TestResult.query.filter_by(user_id=current_user.id)\
            .order_by(TestResult.test_date.desc()).all()
        
        if not results:
            return jsonify({
                'message': 'No test results found',
                'statistics': None
            })
        
        # Calculate statistics
        stats = {
            'total_tests': len(results),
            'latest_test_date': results[0].test_date.isoformat(),
            'risk_trends': {
                'parkinsons': [r.parkinsons_risk for r in results if r.parkinsons_risk is not None],
                'alzheimers': [r.alzheimers_risk for r in results if r.alzheimers_risk is not None],
                'asd': [r.asd_risk for r in results if r.asd_risk is not None],
                'adhd': [r.adhd_risk for r in results if r.adhd_risk is not None]
            },
            'risk_level_distribution': {
                'Low': sum(1 for r in results if r.overall_risk_level == 'Low'),
                'Moderate': sum(1 for r in results if r.overall_risk_level == 'Moderate'),
                'High': sum(1 for r in results if r.overall_risk_level == 'High')
            }
        }
        
        return jsonify({'statistics': stats})
        
    except Exception as e:
        return jsonify({'message': f'Failed to calculate statistics: {str(e)}'}), 500


# Web UI Routes (for future frontend)
@app.route('/')
def index():
    """Home page."""
    return jsonify({
        'message': 'Disease Detection API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'register': '/api/auth/register',
            'login': '/api/auth/login',
            'analyze': '/api/analyze',
            'results': '/api/results'
        }
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'message': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500


# Database initialization
def init_db():
    """Initialize database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
