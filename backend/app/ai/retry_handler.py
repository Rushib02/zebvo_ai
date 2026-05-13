import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def retry_with_fallback(max_retries=2, delay=1, backoff=2):
    """
    Decorator for AI tasks with exponential backoff and support for service fallback.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"AI task failed after {max_retries} retries: {str(e)}")
                        raise e
                    
                    logger.warning(f"AI task attempt {retries} failed. Retrying in {current_delay}s... Error: {str(e)}")
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator
