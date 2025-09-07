"""
Retry handler with exponential backoff for API calls
"""

import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 2, initial_delay: float = 1):
    """
    Decorator for retrying functions with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for delay between retries
        initial_delay: Initial delay in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            delay = initial_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries")
                        raise last_exception
                    
                    # Check if this is a retryable error
                    if not is_retryable_error(e):
                        logger.error(f"Non-retryable error in {func.__name__}: {str(e)}")
                        raise e
                    
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}")
                    logger.info(f"Retrying in {delay} seconds...")
                    
                    time.sleep(delay)
                    delay *= backoff_factor
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator

def is_retryable_error(error: Exception) -> bool:
    """
    Determine if an error is retryable
    
    Args:
        error: Exception to check
        
    Returns:
        True if the error should be retried
    """
    error_message = str(error).lower()
    error_type = type(error).__name__.lower()
    
    # Retryable conditions
    retryable_conditions = [
        'rate limit',
        'timeout',
        'connection',
        'network',
        'temporary',
        'service unavailable',
        'internal server error',
        'bad gateway',
        'gateway timeout'
    ]
    
    # Non-retryable conditions
    non_retryable_conditions = [
        'authentication',
        'authorization',
        'invalid request',
        'bad request',
        'not found',
        'forbidden',
        'invalid api key'
    ]
    
    # Check for non-retryable conditions first
    for condition in non_retryable_conditions:
        if condition in error_message or condition in error_type:
            return False
    
    # Check for retryable conditions
    for condition in retryable_conditions:
        if condition in error_message or condition in error_type:
            return True
    
    # For OpenAI specific errors
    if 'openai' in error_type:
        if 'ratelimiterror' in error_type:
            return True
        elif 'apierror' in error_type or 'serviceunavailableerror' in error_type:
            return True
        elif 'authenticationerror' in error_type or 'invalidrequesterror' in error_type:
            return False
    
    # Default to not retryable for unknown errors
    return False

class RetryableError(Exception):
    """Exception that should be retried"""
    pass

class NonRetryableError(Exception):
    """Exception that should not be retried"""
    pass