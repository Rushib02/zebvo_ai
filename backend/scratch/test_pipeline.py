import sys
import os
import asyncio

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.pipeline_orchestrator import pipeline_orchestrator
from app.services.pipeline_logger import pipeline_logger

async def test_pipeline():
    topic = "The Future of Quantum Computing in 2026"
    print(f"--- Starting Full Pipeline Test for: {topic} ---")
    
    try:
        # 1. Run Full Pipeline
        state = await pipeline_orchestrator.run_full_pipeline(topic)
        
        print("\n[SUCCESS] Full Pipeline Results:")
        print(f"Idea: {state.idea.title if state.idea else 'Failed'}")
        print(f"Hook: {state.hook.hook_text if state.hook else 'Failed'}")
        print(f"Viral Score: {state.viral_score.score if state.viral_score else 'Failed'}")
        print(f"Hashtags: {state.hashtags.tags if state.hashtags else 'Failed'}")
        
        # 2. Test Partial Regeneration
        print("\n--- Testing Partial Regeneration: Hook ---")
        new_hook = await pipeline_orchestrator.regenerate_stage("hook")
        print(f"New Hook: {new_hook.hook_text}")
        
    except Exception as e:
        print(f"\n[FAILURE] Pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pipeline())
