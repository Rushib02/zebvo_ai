class GeminiPromptBuilder:
    def __init__(self, platform="YouTube Shorts"):
        self.platform = platform
        self.modules = []
        self.base_instruction = (
            "You are a master cinematic scriptwriter and creative director. "
            f"Your goal is to create a viral, high-retention script for {platform}."
        )

    def add_storytelling_module(self, topic, tone="Cinematic"):
        module = (
            f"### STORYTELLING MODULE\n"
            f"Topic: {topic}\n"
            f"Tone: {tone}\n"
            "Instruction: Use advanced narrative structures (e.g., Hero's Journey, In Media Res). "
            "Focus on sensory details and visual storytelling."
        )
        self.modules.append(module)
        return self

    def add_emotional_hooks(self):
        module = (
            "### EMOTIONAL HOOKS\n"
            "Instruction: Open with a pattern-interrupting hook. "
            "Target a specific human emotion: curiosity, fear of missing out, awe, or relatable frustration."
        )
        self.modules.append(module)
        return self

    def add_pacing_module(self):
        module = (
            "### PACING & FLOW\n"
            "Instruction: Use the 'Breathe and Strike' method. Rapid cuts and high energy followed by "
            "brief moments of cinematic tension. Ensure every sentence moves the story forward."
        )
        self.modules.append(module)
        return self

    def add_retention_strategy(self):
        module = (
            "### AUDIENCE RETENTION\n"
            "Instruction: Implement 'Open Loops' throughout the script. "
            "Tease the payoff early and deliver it in the final 5 seconds."
        )
        self.modules.append(module)
        return self

    def add_platform_optimization(self):
        opts = {
            "Instagram Reels": "Focus on high visual aesthetic and trending audio-friendly pacing.",
            "YouTube Shorts": "Prioritize the loop—ensure the ending flows perfectly back into the start.",
            "TikTok": "Focus on raw authenticity and rapid-fire information delivery.",
            "LinkedIn short-form": "Maintain a professional yet provocative tone with actionable takeaways."
        }
        module = f"### PLATFORM OPTIMIZATION ({self.platform})\nInstruction: {opts.get(self.platform, '')}"
        self.modules.append(module)
        return self

    def build(self):
        json_format = (
            "RETURN ONLY VALID JSON. DO NOT INCLUDE ANY OTHER TEXT.\n"
            "JSON SCHEMA:\n"
            "{\n"
            "  \"title\": \"string\",\n"
            "  \"hook\": \"string\",\n"
            "  \"cinematic_script\": \"string\",\n"
            "  \"scene_breakdown\": [\n"
            "    {\"scene_number\": 1, \"visual_description\": \"string\", \"audio_narration\": \"string\", \"duration_seconds\": 5}\n"
            "  ],\n"
            "  \"cta\": \"string\",\n"
            "  \"retention_strategy\": \"string\"\n"
            "}"
        )
        
        full_prompt = [self.base_instruction] + self.modules + [json_format]
        return "\n\n".join(full_prompt)
