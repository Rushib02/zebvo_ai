import sys
import os
import json

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.ollama_service import ollama_service
from app.ai.model_router import model_router

def test_ollama_connection():
    """Test if Ollama server is running"""
    print("=" * 60)
    print("Testing Ollama Connection...")
    print("=" * 60)
    
    if ollama_service.is_running():
        print("✓ Ollama server is ONLINE")
    else:
        print("✗ Ollama server is OFFLINE - Please run 'ollama serve'")
        return False
    
    if ollama_service.check_model_available():
        print(f"✓ Model '{ollama_service.model}' is AVAILABLE")
    else:
        print(f"✗ Model '{ollama_service.model}' not found - Run 'ollama pull {ollama_service.model}'")
        return False
    
    return True

def test_ollama_generation():
    """Test Ollama content generation"""
    print("\n" + "=" * 60)
    print("Testing Ollama Generation...")
    print("=" * 60)
    
    if not test_ollama_connection():
        return False
    
    topic = "The future of artificial intelligence"
    
    try:
        # Test basic prompt
        prompt = f"""Generate a brief social media hook for this topic in JSON format:
Topic: {topic}

JSON format:
{{"hook": "your compelling hook text here", "engagement_level": "high/medium/low"}}"""
        
        print(f"\nGenerating hook for topic: '{topic}'")
        result = ollama_service.generate("hook", prompt)
        
        print("\n✓ SUCCESS - Ollama generated response:")
        print(json.dumps(result, indent=2))
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED - Error: {str(e)}")
        return False

def test_model_router_fallback():
    """Test the model router fallback mechanism"""
    print("\n" + "=" * 60)
    print("Testing Model Router (Fallback Chain)...")
    print("=" * 60)
    
    topic = "The future of content creation"
    prompt = f"""Generate a viral hook for this topic in JSON format:
Topic: {topic}

JSON format:
{{"hook": "your compelling hook text", "emotional_trigger": "fear/curiosity/joy"}}"""
    
    try:
        print(f"\nTesting fallback chain for topic: '{topic}'")
        result = model_router.generate_with_fallback("hook", prompt, topic)
        
        print("\n✓ SUCCESS - Model router generated response:")
        print(json.dumps(result, indent=2))
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED - Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n🚀 OLLAMA INTEGRATION TEST SUITE\n")
    
    # Run all tests
    all_passed = True
    
    if not test_ollama_connection():
        all_passed = False
    
    if not test_ollama_generation():
        all_passed = False
    
    if not test_model_router_fallback():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED - Ollama is ready to use!")
    else:
        print("✗ SOME TESTS FAILED - Check errors above")
    print("=" * 60 + "\n")
