"""
Auto Feedback Generator - Flask Backend
Main Flask application for handling feedback generation requests
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

from services.feedback_service import FeedbackService
from utils.validators import validate_rubric_data
from utils.error_handlers import handle_api_error

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
feedback_service = FeedbackService()

@app.route('/', methods=['GET'])
def home():
    """Health check and API information endpoint"""
    return jsonify({
        "message": "Auto Feedback Generator API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "generate_feedback": "/api/generate-feedback",
            "health": "/api/health"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": feedback_service.get_current_timestamp(),
        "api_key_configured": bool(os.getenv('OPENAI_API_KEY'))
    })

@app.route('/api/generate-feedback', methods=['POST'])
def generate_feedback():
    """
    Generate personalized feedback based on rubric data
    
    Expected JSON payload:
    {
        "student_name": "John Doe",
        "assignment_title": "Math Assignment 1",
        "rubric_data": {
            "communication": {"score": 8, "max_score": 10},
            "teamwork": {"score": 6, "max_score": 10},
            "creativity": {"score": 9, "max_score": 10}
        },
        "feedback_type": "constructive",
        "subject": "Mathematics"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No data provided",
                "message": "Please provide valid JSON data"
            }), 400
        
        # Validate input data
        validation_result = validate_rubric_data(data)
        if not validation_result['is_valid']:
            return jsonify({
                "error": "Validation failed",
                "details": validation_result['errors']
            }), 400
        
        # Extract data
        student_name = data.get('student_name', 'Student')
        assignment_title = data.get('assignment_title', 'Assignment')
        rubric_data = data.get('rubric_data', {})
        feedback_type = data.get('feedback_type', 'constructive')
        subject = data.get('subject', 'General')
        
        # Generate feedback
        logger.info(f"Generating feedback for {student_name} - {assignment_title}")
        
        feedback_result = feedback_service.generate_feedback(
            student_name=student_name,
            assignment_title=assignment_title,
            rubric_data=rubric_data,
            feedback_type=feedback_type,
            subject=subject
        )
        
        if feedback_result['success']:
            return jsonify({
                "success": True,
                "feedback": feedback_result['feedback'],
                "metadata": {
                    "student_name": student_name,
                    "assignment_title": assignment_title,
                    "generated_at": feedback_service.get_current_timestamp(),
                    "feedback_type": feedback_type,
                    "subject": subject
                }
            })
        else:
            return jsonify({
                "error": "Feedback generation failed",
                "message": feedback_result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error in generate_feedback: {str(e)}")
        return handle_api_error(e)

@app.route('/api/feedback-templates', methods=['GET'])
def get_feedback_templates():
    """Get available feedback templates and types"""
    return jsonify({
        "feedback_types": [
            "constructive",
            "encouraging",
            "detailed",
            "brief"
        ],
        "subjects": [
            "Mathematics",
            "Science",
            "English",
            "History",
            "Art",
            "Physical Education",
            "General"
        ],
        "sample_rubric": {
            "communication": {"score": 8, "max_score": 10},
            "teamwork": {"score": 6, "max_score": 10},
            "creativity": {"score": 9, "max_score": 10},
            "technical_skills": {"score": 7, "max_score": 10}
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Auto Feedback Generator API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)