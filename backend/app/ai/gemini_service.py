import os
import google.generativeai as genai
from dotenv import load_dotenv

from app.ai.gemini_logger import gemini_logger
from app.ai.gemini_retry_handler import gemini_retry
from app.ai.gemini_prompt_builder import GeminiPromptBuilder
from app.ai.gemini_response_parser import GeminiResponseParser
from app.ai.gemini_validator import validate_gemini_response, GeminiScript

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.reconfigure(self.api_key, model_name)
        
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 4096,
        }

    def reconfigure(self, api_key: str, model_name: str = None):
        """Updates the Gemini configuration at runtime."""
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=api_key)
        
        if model_name:
            self.model_name = model_name
            self.model = genai.GenerativeModel(model_name)
        
        gemini_logger.info(f"Gemini reconfigured: model={self.model_name}")

    @gemini_retry(max_retries=3)
    def generate_content_script(self, topic: str, platform: str = "YouTube Shorts") -> GeminiScript:
        """
        Orchestrates the full generation pipeline:
        Prompt Building -> AI Call -> Parsing -> Validation
        """
        gemini_logger.info(f"Starting script generation for: {topic}", extra={
            "platform": platform,
            "model": self.model.model_name
        })

        # 1. Build Modular Prompt
        builder = GeminiPromptBuilder(platform=platform)
        prompt = (builder
                  .add_storytelling_module(topic)
                  .add_emotional_hooks()
                  .add_pacing_module()
                  .add_retention_strategy()
                  .add_platform_optimization()
                  .build())

        # 2. Call Gemini API
        response = self.model.generate_content(
            prompt,
            generation_config=self.generation_config
        )

        if not response.text:
            raise ValueError("Empty response from Gemini API")

        # 3. Parse Response
        raw_data = GeminiResponseParser.parse_json(response.text)

        # 4. Validate Schema
        validated_script = validate_gemini_response(raw_data)
        
        gemini_logger.info(f"Successfully generated script for: {topic}")
        return validated_script

# Singleton instance
gemini_service = GeminiService()
