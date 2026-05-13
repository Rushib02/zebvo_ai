import requests
from flask import current_app
from app.ai.ai_logger import AILogger

class ModelHealthChecker:
    def __init__(self, base_url=None):
        self.base_url = base_url or "http://localhost:11434"

    def check_ollama_status(self):
        """Checks if Ollama server is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                return True, "Ollama is online"
            return False, f"Ollama returned status {response.status_code}"
        except Exception as e:
            return False, f"Ollama is offline: {str(e)}"

    def get_available_models(self):
        """Returns a list of models currently pulled in Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                return models
            return []
        except:
            return []

    def check_model_ready(self, model_name):
        """Checks if a specific model is pulled and ready."""
        available = self.get_available_models()
        # Handle cases like llama3:latest vs llama3
        ready = any(model_name in m for m in available)
        if not ready:
            AILogger.log_error("health_check", f"Model {model_name} not found in Ollama")
        return ready
