class PromptManager:
    TEMPLATES = {
        "hashtags": """
Generate 10 viral hashtags for a {platform} video about {niche}.
Content Style: {style}
Target Audience: {audience}
Tone: {tone}

Output ONLY a JSON object:
{{"hashtags": ["#tag1", "#tag2", ...]}}
""",
        "captions": """
Generate 3 engaging captions for a {platform} post about {niche}.
Content Style: {style}
Tone: {tone}

Output ONLY a JSON object:
{{"captions": ["Caption 1", "Caption 2", "Caption 3"]}}
""",
        "hooks": """
Generate 5 high-retention hooks for a video about {niche}.
Platform: {platform}
Tone: {tone}

Output ONLY a JSON object:
{{"hooks": ["Hook 1", "Hook 2", ...]}}
""",
        "thumbnail_prompt": """
Generate 2 detailed image generation prompts for a video thumbnail about {niche}.
Content Style: {style}

Output ONLY a JSON object:
{{"prompts": ["Prompt 1", "Prompt 2"], "style_guidelines": "Description of the visual style"}}
"""
    }

    @staticmethod
    def get_prompt(task, **kwargs):
        template = PromptManager.TEMPLATES.get(task)
        if not template:
            raise ValueError(f"No template found for task: {task}")
        return template.format(**kwargs)
