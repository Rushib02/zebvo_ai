from app.services.pipeline_validator import PipelineState

class GenerationManager:
    def __init__(self):
        self.state = PipelineState()
        self.topic = None
        self.script_type = "Monologue"  # Default
        self.script_pace = "Fast Paced"  # Default

    def get_prompt_for_stage(self, stage_name: str) -> str:
        """
        Generates the prompt for a specific stage based on the current state.
        Includes a few-shot example for the initial stage to set the pattern.
        """
        persona = "You are a specialized AI content architect. You ONLY output structured JSON data. You never talk to the user.\n\n"
        example = (
            "EXAMPLE INPUT: Topic 'AI in 2026'\n"
            "EXAMPLE OUTPUT:\n"
            "{\n"
            "  \"title\": \"Quantum AI: The 2026 Shift\",\n"
            "  \"description\": \"How quantum computing will finally break the AI bottleneck.\",\n"
            "  \"target_audience\": \"Tech enthusiasts and investors\"\n"
            "}\n\n"
        )
        
        prompts = {
            "idea": f"{persona}{example}TASK: Generate a viral content idea for a tech YouTube Short about: {self.topic if self.topic else 'the provided topic'}. SCHEMA: {{'title': 'string', 'description': 'string', 'target_audience': 'string'}}",
            "hook": f"{persona}TASK: Generate a hook for: {self.state.idea}. SCHEMA: {{'hook_text': 'string', 'emotion_target': 'string', 'visual_cue': 'string'}}",
            "script": f"{persona}TASK: Write a 60s script for hook: {self.state.hook}. Script Type: {self.script_type}. Pace: {self.script_pace}. SCHEMA: {{'full_text': 'string', 'estimated_duration': 60}}",
            "scenes": f"{persona}TASK: Break down script into scenes: {self.state.script}. SCHEMA: {{'scenes': [{{'scene_number': 1, 'visual': 'string', 'audio': 'string'}}]}}",
            "cta": f"{persona}TASK: Create a CTA for: {self.state.script}. SCHEMA: {{'text': 'string', 'placement': 'string'}}",
            "caption": f"{persona}TASK: Write a caption. SCHEMA: {{'primary_text': 'string', 'secondary_text': 'string'}}",
            "hashtags": f"{persona}TASK: Generate 10 hashtags. SCHEMA: {{'tags': ['string']}}",
            "thumbnail": f"{persona}TASK: Create a DALL-E prompt. SCHEMA: {{'prompt': 'string', 'style_reference': 'string'}}",
            "viral_score": f"{persona}TASK: Analyze virality of: {self.state.script}. SCHEMA: {{'score': 85.0, 'strengths': ['string'], 'weaknesses': ['string']}}"
        }
        return prompts.get(stage_name, "")

    def update_state(self, stage_name: str, data):
        setattr(self.state, stage_name, data)
