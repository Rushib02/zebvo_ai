from datetime import datetime

class ResponseFormatter:
    """
    Standardizes responses across the application.
    """
    
    @staticmethod
    def success(data: dict, message: str = "Success") -> dict:
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message: str, error_type: str = "Error") -> dict:
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "message": message
        }

    @staticmethod
    def format_ai_script(raw_content: str) -> dict:
        """Helper to ensure AI scripts follow a specific structure."""
        # This could be expanded with regex to split hooks/sections if needed
        return {
            "raw": raw_content,
            "sections": raw_content.split("\n\n")
        }
