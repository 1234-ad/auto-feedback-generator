"""
Feedback Service - Core NLP service for generating personalized feedback
Uses OpenAI GPT-4 API with engineered prompts
"""

import openai
import os
import logging
from datetime import datetime
from typing import Dict, Any, List
import time
import json

from utils.prompt_templates import PromptTemplates
from utils.retry_handler import retry_with_backoff

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self):
        """Initialize the feedback service with OpenAI client"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai
        
        # Initialize prompt templates
        self.prompt_templates = PromptTemplates()
        
        # Configuration
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '500'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        
        logger.info("FeedbackService initialized successfully")
    
    def generate_feedback(
        self, 
        student_name: str,
        assignment_title: str,
        rubric_data: Dict[str, Any],
        feedback_type: str = 'constructive',
        subject: str = 'General'
    ) -> Dict[str, Any]:
        """
        Generate personalized feedback based on rubric data
        
        Args:
            student_name: Name of the student
            assignment_title: Title of the assignment
            rubric_data: Dictionary containing rubric scores
            feedback_type: Type of feedback (constructive, encouraging, etc.)
            subject: Subject area
            
        Returns:
            Dictionary with success status and feedback or error message
        """
        try:
            # Generate the prompt
            prompt = self._create_feedback_prompt(
                student_name, assignment_title, rubric_data, feedback_type, subject
            )
            
            # Call OpenAI API with retry logic
            feedback = self._call_openai_api(prompt)
            
            if feedback:
                return {
                    'success': True,
                    'feedback': feedback,
                    'rubric_summary': self._generate_rubric_summary(rubric_data)
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to generate feedback from OpenAI API'
                }
                
        except Exception as e:
            logger.error(f"Error generating feedback: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_feedback_prompt(
        self,
        student_name: str,
        assignment_title: str,
        rubric_data: Dict[str, Any],
        feedback_type: str,
        subject: str
    ) -> str:
        """Create a structured prompt for OpenAI API"""
        
        # Format rubric data for the prompt
        rubric_text = self._format_rubric_data(rubric_data)
        
        # Get the appropriate template
        template = self.prompt_templates.get_template(feedback_type, subject)
        
        # Fill in the template
        prompt = template.format(
            student_name=student_name,
            assignment_title=assignment_title,
            rubric_data=rubric_text,
            subject=subject
        )
        
        logger.debug(f"Generated prompt: {prompt[:200]}...")
        return prompt
    
    def _format_rubric_data(self, rubric_data: Dict[str, Any]) -> str:
        """Format rubric data into readable text for the prompt"""
        rubric_lines = []
        
        for criterion, data in rubric_data.items():
            if isinstance(data, dict) and 'score' in data:
                score = data['score']
                max_score = data.get('max_score', 10)
                percentage = (score / max_score) * 100
                
                rubric_lines.append(
                    f"- {criterion.replace('_', ' ').title()}: {score}/{max_score} ({percentage:.0f}%)"
                )
            else:
                # Handle simple score format
                rubric_lines.append(f"- {criterion.replace('_', ' ').title()}: {data}")
        
        return "\\n".join(rubric_lines)
    
    @retry_with_backoff(max_retries=3, backoff_factor=2)
    def _call_openai_api(self, prompt: str) -> str:
        """
        Call OpenAI API with retry logic and error handling
        
        Args:
            prompt: The formatted prompt to send to OpenAI
            
        Returns:
            Generated feedback text or None if failed
        """
        try:
            logger.info("Calling OpenAI API for feedback generation")
            
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an experienced educator who provides constructive, personalized feedback to students. Your feedback should be encouraging, specific, and actionable."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            feedback = response.choices[0].message.content.strip()
            logger.info("Successfully generated feedback from OpenAI")
            
            return feedback
            
        except openai.error.RateLimitError as e:
            logger.warning(f"Rate limit exceeded: {str(e)}")
            raise Exception("API rate limit exceeded. Please try again in a moment.")
            
        except openai.error.InvalidRequestError as e:
            logger.error(f"Invalid request to OpenAI: {str(e)}")
            raise Exception("Invalid request to AI service. Please check your input.")
            
        except openai.error.AuthenticationError as e:
            logger.error(f"Authentication error: {str(e)}")
            raise Exception("Authentication failed. Please check API configuration.")
            
        except Exception as e:
            logger.error(f"Unexpected error calling OpenAI API: {str(e)}")
            raise Exception(f"Failed to generate feedback: {str(e)}")
    
    def _generate_rubric_summary(self, rubric_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the rubric scores"""
        total_score = 0
        total_max = 0
        criteria_count = len(rubric_data)
        
        for criterion, data in rubric_data.items():
            if isinstance(data, dict) and 'score' in data:
                total_score += data['score']
                total_max += data.get('max_score', 10)
            else:
                # Handle simple numeric scores (assume max of 10)
                total_score += float(data) if isinstance(data, (int, float)) else 0
                total_max += 10
        
        overall_percentage = (total_score / total_max * 100) if total_max > 0 else 0
        
        return {
            'total_score': total_score,
            'total_max': total_max,
            'overall_percentage': round(overall_percentage, 1),
            'criteria_count': criteria_count,
            'performance_level': self._get_performance_level(overall_percentage)
        }
    
    def _get_performance_level(self, percentage: float) -> str:
        """Determine performance level based on percentage"""
        if percentage >= 90:
            return "Excellent"
        elif percentage >= 80:
            return "Good"
        elif percentage >= 70:
            return "Satisfactory"
        elif percentage >= 60:
            return "Needs Improvement"
        else:
            return "Requires Attention"
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    def validate_api_connection(self) -> bool:
        """Test the OpenAI API connection"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"API connection test failed: {str(e)}")
            return False