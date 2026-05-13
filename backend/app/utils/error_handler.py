import streamlit as st
import traceback
from app.utils.logger import log_error

class AppError(Exception):
    """Base class for application errors."""
    def __init__(self, message, error_type="GeneralError"):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

class GeminiError(AppError):
    """Errors related to Gemini API."""
    pass

class DataValidationError(AppError):
    """Errors related to data validation."""
    pass

class ErrorHandler:
    """
    Centralized error handling with Streamlit visual feedback.
    """
    
    @staticmethod
    def handle(error: Exception, context: str = ""):
        """Logs the error and displays a user-friendly message in Streamlit."""
        error_msg = str(error)
        error_type = type(error).__name__
        
        # Log the full traceback for developers
        log_error(f"Error in {context}: {error_msg}", extra={
            "type": error_type,
            "context": context,
            "traceback": traceback.format_exc()
        })
        
        # Display to user in Streamlit
        if isinstance(error, GeminiError):
            st.error(f"🤖 **AI Service Error:** {error_msg}")
            st.warning("Try checking your API key or network connection.")
        elif isinstance(error, DataValidationError):
            st.warning(f"⚠️ **Validation Failed:** {error_msg}")
        elif "JSON" in error_type:
            st.error("📉 **Parsing Error:** The AI returned an invalid format. Retrying might help.")
        else:
            st.error(f"🔥 **Unexpected Error:** {error_msg}")
            
    @staticmethod
    def show_retry_warning(attempt: int, max_retries: int):
        """Displays a warning when retrying an operation."""
        st.warning(f"🔄 Retrying... (Attempt {attempt}/{max_retries})")
