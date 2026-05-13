import requests
import json
import logging
import time

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = "mistral"

    def is_running(self) -> bool:
        """Check if Ollama server is reachable."""
        try:
            response = requests.get(self.base_url, timeout=2)
            return response.status_code == 200
        except:
            return False

    def check_model_available(self) -> bool:
        """Check if Mistral model is pulled and ready."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.model in m.get('name', '') for m in models)
            return False
        except:
            return False

    def generate(self, task: str, prompt: str) -> dict:
        """Generate content using Ollama Mistral."""
        if not self.is_running():
            raise ConnectionError("Ollama server is offline. Please run 'ollama serve'")
        
        if not self.check_model_available():
            raise ValueError(f"Model '{self.model}' not found. Please run 'ollama pull {self.model}'")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        try:
            logger.info(f"Ollama: Generating {task} using {self.model}...")
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API Error: {response.status_code} - {response.text}")

            result = response.json()
            raw_response = result.get('response', '')
            
            # Use the resilient parser
            from app.ai.gemini_response_parser import GeminiResponseParser
            return GeminiResponseParser.parse_json(raw_response)

        except Exception as e:
            logger.error(f"Ollama generation failed: {str(e)}")
            raise e

ollama_service = OllamaService()
