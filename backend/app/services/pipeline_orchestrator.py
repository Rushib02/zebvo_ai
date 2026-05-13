import asyncio
from app.services.generation_manager import GenerationManager
from app.services.stage_executor import stage_executor
from app.services.pipeline_validator import (
    Idea, Hook, Script, SceneBreakdown, CTA, Caption, Hashtags, ThumbnailPrompt, ViralScore
)

class PipelineOrchestrator:
    def __init__(self):
        self.manager = GenerationManager()

    async def run_full_pipeline(self, topic: str, script_type: str = "Monologue", script_pace: str = "Fast Paced"):
        """
        Runs the full 9-stage pipeline.
        Stages 1-4 are sequential.
        Stages 5-9 can be run in parallel.
        """
        # Store topic in manager if needed, or pass it to get_prompt_for_stage
        self.manager.topic = topic
        self.manager.script_type = script_type
        self.manager.script_pace = script_pace
        
        # Sequential Stages
        self.manager.update_state("idea", await stage_executor.execute_stage(
            "idea", self.manager.get_prompt_for_stage("idea"), Idea, topic=topic
        ))
        
        self.manager.update_state("hook", await stage_executor.execute_stage(
            "hook", self.manager.get_prompt_for_stage("hook"), Hook, topic=topic
        ))
        
        self.manager.update_state("script", await stage_executor.execute_stage(
            "script", self.manager.get_prompt_for_stage("script"), Script, topic=topic
        ))
        
        self.manager.update_state("scenes", await stage_executor.execute_stage(
            "scenes", self.manager.get_prompt_for_stage("scenes"), SceneBreakdown, topic=topic
        ))

        # Parallel Stages
        parallel_tasks = [
            stage_executor.execute_stage("cta", self.manager.get_prompt_for_stage("cta"), CTA, topic=topic),
            stage_executor.execute_stage("caption", self.manager.get_prompt_for_stage("caption"), Caption, topic=topic),
            stage_executor.execute_stage("hashtags", self.manager.get_prompt_for_stage("hashtags"), Hashtags, topic=topic),
            stage_executor.execute_stage("thumbnail", self.manager.get_prompt_for_stage("thumbnail"), ThumbnailPrompt, topic=topic),
            stage_executor.execute_stage("viral_score", self.manager.get_prompt_for_stage("viral_score"), ViralScore, topic=topic)
        ]
        
        results = await asyncio.gather(*parallel_tasks)
        
        # Update state with parallel results
        stages = ["cta", "caption", "hashtags", "thumbnail", "viral_score"]
        for stage, result in zip(stages, results):
            self.manager.update_state(stage, result)

        return self.manager.state

    async def regenerate_stage(self, stage_name: str):
        """
        Regenerates a specific stage without rerunning the whole pipeline.
        Note: This assumes the previous required state exists.
        """
        validators = {
            "idea": Idea, "hook": Hook, "script": Script, "scenes": SceneBreakdown,
            "cta": CTA, "caption": Caption, "hashtags": Hashtags, 
            "thumbnail": ThumbnailPrompt, "viral_score": ViralScore
        }
        
        if stage_name not in validators:
            raise ValueError(f"Invalid stage name: {stage_name}")
            
        new_data = await stage_executor.execute_stage(
            stage_name, 
            self.manager.get_prompt_for_stage(stage_name), 
            validators[stage_name],
            use_cache=False # Force regeneration
        )
        self.manager.update_state(stage_name, new_data)
        return new_data

pipeline_orchestrator = PipelineOrchestrator()
