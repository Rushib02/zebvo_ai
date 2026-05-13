import sys
import os
from pathlib import Path

# Add backend/ to path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from app.utils.logger import log_error, log_ai_event
from app.utils.ai_logger import AILogger
from app.utils.validator import Validator
from app.utils.response_formatter import ResponseFormatter
from app.utils.helpers import track_time, truncate_text

@track_time
def mock_ai_task():
    print("Simulating AI task...")
    AILogger.track_request("Gemini-Pro", "Script Generation", 150)
    # Simulate success
    AILogger.track_success("Gemini-Pro", "Script Generation", 1.2, 500)
    return "This is a mock AI response."

def test_utils():
    print("--- Testing Logger ---")
    log_error("Test error message", extra={"code": 500})
    log_ai_event("Test AI event")
    
    print("--- Testing Validator ---")
    is_json = Validator.is_valid_json('{"key": "value"}')
    print(f"Is Valid JSON: {is_json}")
    
    valid_len, msg = Validator.validate_content_length("Short", min_chars=10)
    print(f"Length Validation: {valid_len}, Message: {msg}")
    
    print("--- Testing Formatter ---")
    success_resp = ResponseFormatter.success({"id": 1}, "Generation complete")
    print(f"Success Response: {success_resp['status']} at {success_resp['timestamp']}")
    
    print("--- Testing Helpers ---")
    mock_ai_task()
    truncated = truncate_text("This is a very long text that should be truncated by the helper function.", max_len=20)
    print(f"Truncated: {truncated}")

    # Check if logs were created
    log_dir = os.path.join(backend_path, "..", "logs")
    if os.path.exists(log_dir):
        print(f"--- Logs directory found at {log_dir} ---")
        for f in os.listdir(log_dir):
            print(f"Found log file: {f}")
    else:
        print(f"--- Logs directory NOT found at {log_dir} ---")

if __name__ == "__main__":
    test_utils()
