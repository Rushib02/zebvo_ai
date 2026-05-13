import time
from app.utils.logger import log_ai_event

class AILogger:
    """
    Specialized logger for tracking AI generation lifecycle and performance.
    """
    
    @staticmethod
    def track_request(model_name: str, task: str, prompt_length: int):
        log_ai_event(f"AI request initiated", extra={
            "event": "request_start",
            "model": model_name,
            "task": task,
            "prompt_length": prompt_length
        })

    @staticmethod
    def track_success(model_name: str, task: str, duration: float, response_length: int):
        log_ai_event(f"AI request successful", extra={
            "event": "request_success",
            "model": model_name,
            "task": task,
            "duration_ms": round(duration * 1000, 2),
            "response_length": response_length
        })

    @staticmethod
    def track_failure(model_name: str, task: str, error_type: str, message: str):
        log_ai_event(f"AI request failed", extra={
            "event": "request_failure",
            "model": model_name,
            "task": task,
            "error_type": error_type,
            "error_message": message
        })

    @staticmethod
    def track_thumbnail_event(project_id: str, status: str):
        log_ai_event(f"Thumbnail generation event: {status}", extra={
            "event": "thumbnail_gen",
            "project_id": project_id,
            "status": status
        })
