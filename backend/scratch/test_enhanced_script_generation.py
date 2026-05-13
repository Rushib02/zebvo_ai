import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.streamlit_generation import StreamlitGenerationHelper

print("=" * 80)
print("🎬 ENHANCED SCRIPT GENERATION TEST")
print("=" * 80)

# Test different script formats
test_cases = [
    {
        "topic": "The history of goodbyes in cinema",
        "style": "Viral Fast-Paced",
        "length": 30,
        "script_format": "Monologue",
        "num_characters": 1,
        "pacing": "Fast",
        "custom_notes": "Include famous movie goodbyes"
    },
    {
        "topic": "Why AI will change content creation",
        "style": "Educational",
        "length": 45,
        "script_format": "Dialogue (2 people)",
        "num_characters": 2,
        "pacing": "Normal",
        "custom_notes": "Host and expert discussion format"
    },
    {
        "topic": "The future of social media",
        "style": "Cinematic",
        "length": 60,
        "script_format": "Skit (3+ people)",
        "num_characters": 3,
        "pacing": "Slow",
        "custom_notes": "Dramatic storytelling with three perspectives"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}: {test['topic']}")
    print(f"{'='*80}")
    print(f"Format: {test['script_format']} | Duration: {test['length']}s | Pacing: {test['pacing']}\n")
    
    result = StreamlitGenerationHelper.generate_script(
        topic=test['topic'],
        style=test['style'],
        length=test['length'],
        script_format=test['script_format'],
        num_characters=test['num_characters'],
        pacing=test['pacing'],
        custom_notes=test['custom_notes']
    )
    
    print(f"✓ Generation Complete")
    print(f"\nMetadata:")
    print(f"  - Script Type: {result.get('script_type', 'N/A')}")
    print(f"  - Characters: {result.get('num_characters', 'N/A')}")
    print(f"  - Duration: {result.get('duration', 'N/A')}s")
    
    if 'content' in result and isinstance(result['content'], list):
        print(f"  - Scenes: {len(result['content'])}")
    
    print(f"\n📄 Full Script:")
    print("-" * 80)
    full_text = result.get('full_text', result.get('error', 'No script generated'))
    print(full_text[:500] + ("..." if len(full_text) > 500 else ""))
    print("-" * 80)

print(f"\n{'='*80}")
print("✓ ALL TESTS COMPLETE")
print("='*80}\n")
