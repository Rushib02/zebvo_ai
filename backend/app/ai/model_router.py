import logging
from app.ai.ollama_service import ollama_service
from app.ai.fallback_generator import fallback_generator

logger = logging.getLogger(__name__)

class ModelRouter:
    """
    Intelligent router that manages the hybrid AI workflow.
    Primary: Ollama (Mistral)
    Emergency: Template-based generator
    """
    
    @staticmethod
    def generate_with_fallback(stage_name: str, prompt: str, topic: str):
        """
        Orchestrates the fallback chain for a specific stage.
        Using only Ollama (no Gemini).
        """
        # 1. Try Ollama Mistral (Primary)
        try:
            logger.info(f"Router: Attempting {stage_name} with Ollama Mistral...")
            if ollama_service.is_running():
                return ollama_service.generate(stage_name, prompt)
            else:
                logger.warning("Ollama server is offline. Using emergency fallback.")
        except Exception as e:
            logger.warning(f"Ollama failed for {stage_name}: {str(e)}. Using emergency fallback.")

        # 2. Emergency Template Fallback
        logger.info(f"Router: Using emergency template fallback for {stage_name}")
        fallback_map = {
            "idea": lambda: {"title": f"The Future of {topic}", "description": "A deep dive into this trending topic.", "target_audience": "General"},
            "hook": lambda: fallback_generator.generate_hook(topic),
            "script": lambda: fallback_generator.generate_script(topic),
            "cta": lambda: fallback_generator.generate_cta(topic),
            "caption": lambda: fallback_generator.generate_caption(topic),
            "hashtags": lambda: fallback_generator.generate_hashtags(topic),
            "thumbnail": lambda: fallback_generator.generate_thumbnail_prompt(topic),
            "viral_score": lambda: fallback_generator.generate_viral_score(),
            "scenes": lambda: {"scenes": [{"scene_number": 1, "visual": "Intro", "audio": "Welcome"}]}
        }
        
        return fallback_map.get(stage_name, lambda: {})()

model_router = ModelRouter()
