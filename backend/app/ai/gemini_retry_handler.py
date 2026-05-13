import time
import random
import functools
from google.api_core import exceptions
from app.ai.gemini_logger import gemini_logger

def gemini_retry(max_retries=3, initial_delay=2, backoff_factor=2):
    """
    Decorator for retrying Gemini API calls with exponential backoff.
    Handles ResourceExhausted (rate limits) and ServiceUnavailable.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable, exceptions.InternalServerError) as e:
                    retries += 1
                    if retries > max_retries:
                        gemini_logger.error("Max retries exceeded for Gemini API", extra={
                            "error": str(e),
                            "retries": retries
                        })
                        raise e
                    
                    # Add jitter to the delay
                    sleep_time = delay + random.uniform(0, 1)
                    gemini_logger.warning(f"Gemini API error. Retrying in {sleep_time:.2f}s...", extra={
                        "error": str(e),
                        "retry_count": retries,
                        "next_delay": sleep_time
                    })
                    
                    time.sleep(sleep_time)
                    delay *= backoff_factor
                except Exception as e:
                    # Non-retryable error
                    gemini_logger.error("Unrecoverable error in Gemini service", extra={"error": str(e)})
                    raise e
            return None
        return wrapper
    return decorator
