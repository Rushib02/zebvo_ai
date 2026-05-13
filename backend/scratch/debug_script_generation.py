import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.model_router import model_router
from app.ai.ollama_service import ollama_service

print("=" * 70)
print("🧪 SCRIPT GENERATION DEBUG TEST")
print("=" * 70)

topic = "The future of artificial intelligence"
length = 60
style = "Viral Fast-Paced"

# Test 1: Direct Ollama call
print("\n[TEST 1] Direct Ollama Generation")
print("-" * 70)

if ollama_service.is_running():
    prompt = f"""You are a viral content script writer. Generate a {length} second script for YouTube Shorts about: {topic}
    
Write it in {style} style. Format your response as JSON with these exact keys:
{{
    "full_text": "the complete script text goes here",
    "estimated_duration": 60,
    "hook": "opening line",
    "scenes": 5,
    "cta": "call to action at the end"
}}

IMPORTANT: Return ONLY valid JSON, no markdown, no explanation."""

    try:
        result = ollama_service.generate("script", prompt)
        print("✓ SUCCESS - Ollama returned:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
else:
    print("✗ Ollama is offline")

# Test 2: Model Router (with fallback)
print("\n[TEST 2] Model Router (Auto-Fallback)")
print("-" * 70)

prompt = f"Write a {length}s viral script for: {topic} in {style} style"

try:
    result = model_router.generate_with_fallback("script", prompt, topic)
    print("✓ SUCCESS - Model router returned:")
    print(json.dumps(result, indent=2))
    
    if result:
        print("\n✓ Script generation working!")
        if "full_text" in result:
            print(f"✓ Has 'full_text' key")
        else:
            print(f"⚠️  Missing 'full_text' key. Keys present: {list(result.keys())}")
    else:
        print("⚠️  Empty result returned")
except Exception as e:
    print(f"✗ FAILED: {str(e)}")

# Test 3: Full pipeline test
print("\n[TEST 3] Full Generation Pipeline (All Stages)")
print("-" * 70)

stages = ["idea", "hook", "script", "caption", "hashtags", "thumbnail", "viral_score"]

for stage in stages:
    print(f"\n  Testing {stage.upper()}...", end=" ")
    try:
        if stage == "idea":
            p = f"Generate content idea for: {topic}"
        elif stage == "hook":
            p = f"Create a hook for: {topic}"
        elif stage == "script":
            p = f"Write a {length}s script for: {topic}"
        elif stage == "caption":
            p = f"Create caption for: {topic}"
        elif stage == "hashtags":
            p = f"Generate hashtags for: {topic}"
        elif stage == "thumbnail":
            p = f"Create thumbnail concept for: {topic}"
        else:
            p = f"Analyze viral score for: {topic}"
        
        result = model_router.generate_with_fallback(stage, p, topic)
        
        if result and len(result) > 0:
            print("✓")
            print(f"    → Keys: {list(result.keys())}")
        else:
            print("✗ Empty")
    except Exception as e:
        print(f"✗ Error: {str(e)[:50]}")

print("\n" + "=" * 70)
print("🏁 DEBUG TEST COMPLETE")
print("=" * 70)
