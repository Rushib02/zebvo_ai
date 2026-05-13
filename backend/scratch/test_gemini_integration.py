import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.gemini_service import GeminiService
from app.ai.gemini_logger import gemini_logger

def test_generation():
    service = GeminiService()
    topic = "The hidden history of artificial intelligence in the 1950s"
    platform = "YouTube Shorts"
    
    print(f"--- Testing Gemini Integration for Topic: {topic} ---")
    
    try:
        script = service.generate_content_script(topic, platform)
        
        print("\n[SUCCESS] Generated Script:")
        print(f"Title: {script.title}")
        print(f"Hook: {script.hook}")
        print(f"Cinematic Script: {script.cinematic_script[:200]}...")
        print(f"Number of Scenes: {len(script.scene_breakdown)}")
        print(f"CTA: {script.cta}")
        print(f"Retention Strategy: {script.retention_strategy}")
        
    except Exception as e:
        print(f"\n[FAILURE] Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_generation()
