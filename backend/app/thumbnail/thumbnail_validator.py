class ThumbnailValidator:
    @staticmethod
    def validate_prompt(prompt: str) -> bool:
        """Ensures the prompt is substantial enough for generation."""
        if not prompt or len(prompt.strip()) < 10:
            return False
        # Add any safety or quality checks here
        return True

    @staticmethod
    def check_api_key(api_key: str) -> bool:
        """Basic check for API key presence."""
        return bool(api_key and api_key.startswith("AIza"))
