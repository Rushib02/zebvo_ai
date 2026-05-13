import time
import streamlit as st
from functools import wraps
from app.utils.logger import log_request

def track_time(func):
    """Decorator to track execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        
        log_request(f"Function {func.__name__} executed", extra={
            "function": func.__name__,
            "duration_s": round(duration, 4)
        })
        return result
    return wrapper

class LoadingState:
    """Context manager for Streamlit loading states."""
    def __init__(self, message="Processing..."):
        self.message = message
        self.spinner = None

    def __enter__(self):
        self.spinner = st.spinner(self.message)
        self.spinner.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spinner.__exit__(exc_type, exc_val, exc_tb)

def truncate_text(text: str, max_len: int = 100) -> str:
    """Truncates text for display."""
    if len(text) <= max_len:
        return text
    return text[:max_len-3] + "..."

def get_current_timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")
