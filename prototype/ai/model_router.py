from ai import gemini_service

def run(task: str, prompt: str) -> dict:
    """
    Route all generation tasks directly to Gemini.
    Ollama integration has been removed as per user request.
    """
    return gemini_service.generate(prompt)
