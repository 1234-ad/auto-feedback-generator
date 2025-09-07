"""
Input validation utilities for the feedback generator
"""

import re
from typing import Dict, Any, List

def validate_rubric_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the input data for feedback generation
    
    Args:
        data: Dictionary containing request data
        
    Returns:
        Dictionary with validation results
    """
    errors = []
    
    # Check required fields
    required_fields = ['student_name', 'rubric_data']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate student name
    if 'student_name' in data:
        if not isinstance(data['student_name'], str):
            errors.append("Student name must be a string")
        elif len(data['student_name'].strip()) < 1:
            errors.append("Student name cannot be empty")
        elif len(data['student_name']) > 100:
            errors.append("Student name is too long (max 100 characters)")
        elif not re.match(r'^[a-zA-Z\s\-\.\']+$', data['student_name']):
            errors.append("Student name contains invalid characters")
    
    # Validate assignment title
    if 'assignment_title' in data:
        if not isinstance(data['assignment_title'], str):
            errors.append("Assignment title must be a string")
        elif len(data['assignment_title']) > 200:
            errors.append("Assignment title is too long (max 200 characters)")
    
    # Validate rubric data
    if 'rubric_data' in data:
        rubric_errors = validate_rubric_scores(data['rubric_data'])
        errors.extend(rubric_errors)
    
    # Validate feedback type
    if 'feedback_type' in data:
        valid_types = ['constructive', 'encouraging', 'detailed', 'brief']
        if data['feedback_type'] not in valid_types:
            errors.append(f"Invalid feedback type. Must be one of: {', '.join(valid_types)}")
    
    # Validate subject
    if 'subject' in data:
        valid_subjects = [
            'Mathematics', 'Science', 'English', 'History', 
            'Art', 'Physical Education', 'General'
        ]
        if data['subject'] not in valid_subjects:
            errors.append(f"Invalid subject. Must be one of: {', '.join(valid_subjects)}")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }

def validate_rubric_scores(rubric_data: Dict[str, Any]) -> List[str]:
    """
    Validate rubric score data
    
    Args:
        rubric_data: Dictionary containing rubric scores
        
    Returns:
        List of validation errors
    """
    errors = []
    
    if not isinstance(rubric_data, dict):
        errors.append("Rubric data must be a dictionary")
        return errors
    
    if len(rubric_data) == 0:
        errors.append("Rubric data cannot be empty")
        return errors
    
    if len(rubric_data) > 20:
        errors.append("Too many rubric criteria (max 20)")
    
    for criterion, score_data in rubric_data.items():
        # Validate criterion name
        if not isinstance(criterion, str):
            errors.append(f"Criterion name must be a string: {criterion}")
            continue
        
        if len(criterion.strip()) == 0:
            errors.append("Criterion name cannot be empty")
            continue
        
        if len(criterion) > 50:
            errors.append(f"Criterion name too long (max 50 chars): {criterion}")
        
        # Validate score data
        if isinstance(score_data, dict):
            # Expected format: {"score": 8, "max_score": 10}
            if 'score' not in score_data:
                errors.append(f"Missing 'score' for criterion: {criterion}")
                continue
            
            score = score_data['score']
            max_score = score_data.get('max_score', 10)
            
            # Validate score
            if not isinstance(score, (int, float)):
                errors.append(f"Score must be a number for criterion: {criterion}")
                continue
            
            if score < 0:
                errors.append(f"Score cannot be negative for criterion: {criterion}")
            
            if not isinstance(max_score, (int, float)):
                errors.append(f"Max score must be a number for criterion: {criterion}")
                continue
            
            if max_score <= 0:
                errors.append(f"Max score must be positive for criterion: {criterion}")
            
            if score > max_score:
                errors.append(f"Score cannot exceed max score for criterion: {criterion}")
        
        elif isinstance(score_data, (int, float)):
            # Simple numeric score format
            if score_data < 0:
                errors.append(f"Score cannot be negative for criterion: {criterion}")
            if score_data > 100:  # Assume max of 100 for simple scores
                errors.append(f"Score too high (max 100) for criterion: {criterion}")
        
        else:
            errors.append(f"Invalid score format for criterion: {criterion}")
    
    return errors

def sanitize_input(text: str) -> str:
    """
    Sanitize text input to prevent injection attacks
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Limit length
    sanitized = sanitized[:1000]
    
    # Strip whitespace
    sanitized = sanitized.strip()
    
    return sanitized

def validate_api_key(api_key: str) -> bool:
    """
    Validate OpenAI API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if format is valid
    """
    if not api_key:
        return False
    
    # OpenAI API keys typically start with 'sk-' and are 51 characters long
    if not api_key.startswith('sk-'):
        return False
    
    if len(api_key) != 51:
        return False
    
    # Check if it contains only valid characters
    if not re.match(r'^sk-[a-zA-Z0-9]+$', api_key):
        return False
    
    return True

def validate_request_size(data: Dict[str, Any]) -> bool:
    """
    Validate that the request size is reasonable
    
    Args:
        data: Request data
        
    Returns:
        True if size is acceptable
    """
    import json
    
    try:
        json_str = json.dumps(data)
        size_kb = len(json_str.encode('utf-8')) / 1024
        
        # Limit to 50KB
        return size_kb <= 50
    except:
        return False