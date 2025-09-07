"""
Error handling utilities for the Flask backend
"""

from flask import jsonify
import logging
import traceback
from typing import Any, Dict

logger = logging.getLogger(__name__)

def handle_api_error(error: Exception) -> tuple:
    """
    Handle API errors and return appropriate JSON response
    
    Args:
        error: Exception that occurred
        
    Returns:
        Tuple of (response, status_code)
    """
    error_message = str(error)
    error_type = type(error).__name__
    
    # Log the full error with traceback
    logger.error(f"API Error - {error_type}: {error_message}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Determine appropriate status code and user message
    if "rate limit" in error_message.lower():
        status_code = 429
        user_message = "API rate limit exceeded. Please try again in a moment."
    elif "authentication" in error_message.lower():
        status_code = 401
        user_message = "Authentication failed. Please check API configuration."
    elif "invalid request" in error_message.lower():
        status_code = 400
        user_message = "Invalid request. Please check your input data."
    elif "timeout" in error_message.lower():
        status_code = 504
        user_message = "Request timeout. Please try again."
    else:
        status_code = 500
        user_message = "An unexpected error occurred. Please try again."
    
    response = jsonify({
        "error": "API Error",
        "message": user_message,
        "type": error_type,
        "timestamp": get_current_timestamp()
    })
    
    return response, status_code

def handle_validation_error(errors: list) -> tuple:
    """
    Handle validation errors
    
    Args:
        errors: List of validation error messages
        
    Returns:
        Tuple of (response, status_code)
    """
    response = jsonify({
        "error": "Validation Error",
        "message": "Input validation failed",
        "details": errors,
        "timestamp": get_current_timestamp()
    })
    
    return response, 400

def handle_openai_error(error: Exception) -> Dict[str, Any]:
    """
    Handle OpenAI-specific errors
    
    Args:
        error: OpenAI exception
        
    Returns:
        Error response dictionary
    """
    error_type = type(error).__name__
    error_message = str(error)
    
    logger.error(f"OpenAI Error - {error_type}: {error_message}")
    
    if "rate_limit" in error_type.lower():
        return {
            "success": False,
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please wait a moment and try again.",
            "retry_after": 60
        }
    elif "invalid_request" in error_type.lower():
        return {
            "success": False,
            "error": "Invalid request",
            "message": "The request to OpenAI was invalid. Please check your input."
        }
    elif "authentication" in error_type.lower():
        return {
            "success": False,
            "error": "Authentication error",
            "message": "OpenAI API authentication failed. Please check your API key."
        }
    elif "permission" in error_type.lower():
        return {
            "success": False,
            "error": "Permission denied",
            "message": "Insufficient permissions for this OpenAI API operation."
        }
    else:
        return {
            "success": False,
            "error": "OpenAI API error",
            "message": f"OpenAI API error: {error_message}"
        }

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    from datetime import datetime
    return datetime.now().isoformat()

class APIException(Exception):
    """Custom exception for API errors"""
    
    def __init__(self, message: str, status_code: int = 500, error_type: str = "API Error"):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        super().__init__(self.message)

class ValidationException(Exception):
    """Custom exception for validation errors"""
    
    def __init__(self, errors: list):
        self.errors = errors
        self.message = f"Validation failed: {', '.join(errors)}"
        super().__init__(self.message)

class OpenAIException(Exception):
    """Custom exception for OpenAI API errors"""
    
    def __init__(self, message: str, error_type: str = "OpenAI Error"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)