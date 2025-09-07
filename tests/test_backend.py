"""
Test suite for the Flask backend
"""

import pytest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app
from services.feedback_service import FeedbackService
from utils.validators import validate_rubric_data
from utils.prompt_templates import PromptTemplates

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_rubric_data():
    """Sample rubric data for testing"""
    return {
        "student_name": "John Doe",
        "assignment_title": "Math Quiz 1",
        "subject": "Mathematics",
        "feedback_type": "constructive",
        "rubric_data": {
            "problem_solving": {"score": 8, "max_score": 10},
            "communication": {"score": 7, "max_score": 10},
            "accuracy": {"score": 9, "max_score": 10}
        }
    }

class TestAPI:
    """Test API endpoints"""
    
    def test_home_endpoint(self, client):
        """Test the home endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'message' in data
        assert 'version' in data
        assert 'endpoints' in data
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'status' in data
        assert 'timestamp' in data
        assert data['status'] == 'healthy'
    
    def test_feedback_templates_endpoint(self, client):
        """Test the feedback templates endpoint"""
        response = client.get('/api/feedback-templates')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'feedback_types' in data
        assert 'subjects' in data
        assert 'sample_rubric' in data
        
        # Check expected feedback types
        expected_types = ['constructive', 'encouraging', 'detailed', 'brief']
        assert all(ft in data['feedback_types'] for ft in expected_types)
    
    @patch('services.feedback_service.FeedbackService.generate_feedback')
    def test_generate_feedback_success(self, mock_generate, client, sample_rubric_data):
        """Test successful feedback generation"""
        # Mock the feedback service response
        mock_generate.return_value = {
            'success': True,
            'feedback': 'Great work on your math quiz, John! Your problem-solving skills are excellent.',
            'rubric_summary': {
                'total_score': 24,
                'total_max': 30,
                'overall_percentage': 80.0,
                'performance_level': 'Good'
            }
        }
        
        response = client.post('/api/generate-feedback', 
                             data=json.dumps(sample_rubric_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'feedback' in data
        assert 'metadata' in data
    
    def test_generate_feedback_missing_data(self, client):
        """Test feedback generation with missing data"""
        response = client.post('/api/generate-feedback',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Validation failed'
    
    def test_generate_feedback_invalid_json(self, client):
        """Test feedback generation with invalid JSON"""
        response = client.post('/api/generate-feedback',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_404_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Not found'

class TestValidators:
    """Test validation functions"""
    
    def test_valid_rubric_data(self, sample_rubric_data):
        """Test validation with valid data"""
        result = validate_rubric_data(sample_rubric_data)
        assert result['is_valid'] is True
        assert len(result['errors']) == 0
    
    def test_missing_student_name(self, sample_rubric_data):
        """Test validation with missing student name"""
        del sample_rubric_data['student_name']
        result = validate_rubric_data(sample_rubric_data)
        assert result['is_valid'] is False
        assert any('student_name' in error for error in result['errors'])
    
    def test_missing_rubric_data(self, sample_rubric_data):
        """Test validation with missing rubric data"""
        del sample_rubric_data['rubric_data']
        result = validate_rubric_data(sample_rubric_data)
        assert result['is_valid'] is False
        assert any('rubric_data' in error for error in result['errors'])
    
    def test_invalid_feedback_type(self, sample_rubric_data):
        """Test validation with invalid feedback type"""
        sample_rubric_data['feedback_type'] = 'invalid_type'
        result = validate_rubric_data(sample_rubric_data)
        assert result['is_valid'] is False
        assert any('feedback type' in error for error in result['errors'])
    
    def test_invalid_subject(self, sample_rubric_data):
        """Test validation with invalid subject"""
        sample_rubric_data['subject'] = 'Invalid Subject'
        result = validate_rubric_data(sample_rubric_data)
        assert result['is_valid'] is False
        assert any('subject' in error for error in result['errors'])
    
    def test_negative_scores(self, sample_rubric_data):
        """Test validation with negative scores"""
        sample_rubric_data['rubric_data']['problem_solving']['score'] = -5
        result = validate_rubric_data(sample_rubric_data)
        assert result['is_valid'] is False
        assert any('negative' in error for error in result['errors'])
    
    def test_score_exceeds_max(self, sample_rubric_data):
        """Test validation with score exceeding max"""
        sample_rubric_data['rubric_data']['problem_solving']['score'] = 15
        result = validate_rubric_data(sample_rubric_data)
        assert result['is_valid'] is False
        assert any('exceed' in error for error in result['errors'])

class TestPromptTemplates:
    """Test prompt template functionality"""
    
    def test_prompt_templates_initialization(self):
        """Test prompt templates initialization"""
        templates = PromptTemplates()
        assert hasattr(templates, 'base_templates')
        assert hasattr(templates, 'subject_modifiers')
        
        # Check that all expected templates exist
        expected_types = ['constructive', 'encouraging', 'detailed', 'brief']
        for template_type in expected_types:
            assert template_type in templates.base_templates
    
    def test_get_template(self):
        """Test getting a specific template"""
        templates = PromptTemplates()
        template = templates.get_template('constructive', 'Mathematics')
        
        assert isinstance(template, str)
        assert len(template) > 0
        assert '{student_name}' in template
        assert '{rubric_data}' in template
    
    def test_get_template_invalid_type(self):
        """Test getting template with invalid type"""
        templates = PromptTemplates()
        template = templates.get_template('invalid_type', 'Mathematics')
        
        # Should default to constructive
        constructive_template = templates.get_template('constructive', 'Mathematics')
        assert template == constructive_template
    
    def test_sample_prompts(self):
        """Test sample prompts functionality"""
        templates = PromptTemplates()
        samples = templates.get_sample_prompts()
        
        assert 'sample_data' in samples
        assert 'expected_elements' in samples
        assert isinstance(samples['expected_elements'], list)

@patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-test-key-12345678901234567890123456789012345'})
class TestFeedbackService:
    """Test feedback service functionality"""
    
    def test_feedback_service_initialization(self):
        """Test feedback service initialization"""
        service = FeedbackService()
        assert service.api_key == 'sk-test-key-12345678901234567890123456789012345'
        assert hasattr(service, 'prompt_templates')
    
    def test_format_rubric_data(self):
        """Test rubric data formatting"""
        service = FeedbackService()
        rubric_data = {
            "problem_solving": {"score": 8, "max_score": 10},
            "communication": {"score": 7, "max_score": 10}
        }
        
        formatted = service._format_rubric_data(rubric_data)
        assert "Problem Solving: 8/10" in formatted
        assert "Communication: 7/10" in formatted
    
    def test_generate_rubric_summary(self):
        """Test rubric summary generation"""
        service = FeedbackService()
        rubric_data = {
            "problem_solving": {"score": 8, "max_score": 10},
            "communication": {"score": 7, "max_score": 10}
        }
        
        summary = service._generate_rubric_summary(rubric_data)
        assert summary['total_score'] == 15
        assert summary['total_max'] == 20
        assert summary['overall_percentage'] == 75.0
        assert summary['criteria_count'] == 2
    
    def test_get_performance_level(self):
        """Test performance level determination"""
        service = FeedbackService()
        
        assert service._get_performance_level(95) == "Excellent"
        assert service._get_performance_level(85) == "Good"
        assert service._get_performance_level(75) == "Satisfactory"
        assert service._get_performance_level(65) == "Needs Improvement"
        assert service._get_performance_level(45) == "Requires Attention"

if __name__ == '__main__':
    pytest.main([__file__])