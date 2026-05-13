from ai import model_router, prompt_manager

def run(topic: str, niche: str, platform: str, style: str) -> dict:
    prompt = prompt_manager.hook_prompt(topic, niche, platform, style)
    result = model_router.run("hook", prompt)
    return {
        "hook":       result.get("hook", ""),
        "emotion":    result.get("emotion", ""),
        "visual_cue": result.get("visual_cue", ""),
    }
