import json
import re

class Validator:
    """
    Standardized validation for inputs and AI responses.
    """
    
    @staticmethod
    def is_valid_json(text: str) -> bool:
        try:
            json.loads(text)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_content_length(text: str, min_chars: int = 10, max_chars: int = 5000) -> tuple[bool, str]:
        if not text or len(text) < min_chars:
            return False, f"Content is too short (min {min_chars} chars)."
        if len(text) > max_chars:
            return False, f"Content exceeds maximum length ({max_chars} chars)."
        return True, ""

    @staticmethod
    def validate_ai_response(response_data: dict, required_fields: list) -> tuple[bool, list]:
        """Checks if the AI response dictionary contains all required fields."""
        missing = [field for field in required_fields if field not in response_data]
        return len(missing) == 0, missing

    @staticmethod
    def clean_hashtags(hashtags: list) -> list:
        """Sanitizes hashtags (removes #, spaces)."""
        cleaned = []
        for tag in hashtags:
            # Remove non-alphanumeric
            tag = re.sub(r'[^a-zA-Z0-9]', '', tag)
            if tag:
                cleaned.append(tag)
        return cleaned
