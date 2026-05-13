from app.ai.ollama_service import ollama_service

class AIRouter:
    @staticmethod
    def get_service_for_stage(stage_name: str):
        """
        Determines which AI service should handle a specific stage.
        Using Ollama (Mistral) for all stages.
        """
        return ollama_service

ai_router = AIRouter()
