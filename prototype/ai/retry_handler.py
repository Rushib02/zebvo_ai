import time
import functools
from utils.logger import warn, error

def with_retry(max_retries: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """Decorator: exponential backoff retry for any callable."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            last_exc = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < max_retries:
                        warn(f"Attempt {attempt}/{max_retries} failed: {exc}. Retrying in {wait:.1f}s…")
                        time.sleep(wait)
                        wait *= backoff
                    else:
                        error(f"All {max_retries} attempts failed for {func.__name__}.")
            raise last_exc
        return wrapper
    return decorator
