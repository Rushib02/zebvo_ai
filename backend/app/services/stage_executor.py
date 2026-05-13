import asyncio
import json
from app.services.pipeline_logger import PipelineTimer, pipeline_logger
from app.services.generation_cache import generation_cache
from app.services.ai_router import ai_router
from app.ai.gemini_response_parser import GeminiResponseParser

class StageExecutor:
    @staticmethod
    async def execute_stage(stage_name: str, prompt: str, validator_func, use_cache=True, topic: str = None):
        """
        Executes a single pipeline stage with hybrid fallback routing.
        """
        model_config = {"service": "hybrid-orchestrator"}
        
        # 1. Check Cache
        if use_cache:
            cached_res = generation_cache.get(prompt, model_config)
            if cached_res:
                return validator_func(**cached_res)

        # 2. Execute with Timer and Hybrid Router
        with PipelineTimer(stage_name):
            from app.ai.model_router import model_router
            
            loop = asyncio.get_event_loop()
            
            try:
                # Use the router to handle primary/fallback/emergency logic
                data = await loop.run_in_executor(
                    None, 
                    model_router.generate_with_fallback, 
                    stage_name, prompt, topic or "General Topic"
                )

                pipeline_logger.info(f"Stage {stage_name} produced data: {str(data)[:100]}...")
                validated_data = validator_func(**data)
                
                # 3. Save to Cache
                if use_cache:
                    generation_cache.set(prompt, model_config, data)
                
                return validated_data
                
            except Exception as e:
                pipeline_logger.error(f"Stage {stage_name} critical failure: {str(e)}")
                raise e

stage_executor = StageExecutor()
