import json
import re
from app.ai.ai_logger import AILogger

class ResponseParser:
    @staticmethod
    def parse_json(text):
        """Extracts and parses JSON from AI text output."""
        try:
            # Try direct parsing first
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON block within triple backticks
            match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except:
                    pass
            
            # Try to find anything between { and }
            match = re.search(r"({.*})", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except:
                    pass
            
            AILogger.log_error("parser", f"Failed to parse JSON from response: {text[:200]}...")
            raise ValueError("Malformed AI JSON response")

    @staticmethod
    def clean_text(text):
        """Cleans AI output of common artifacts."""
        return text.strip().replace("\"", "'")
