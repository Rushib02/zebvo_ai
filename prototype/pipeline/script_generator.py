from ai import model_router, prompt_manager

def run(topic: str, niche: str, platform: str, style: str, hook: str) -> dict:
    prompt = prompt_manager.script_prompt(topic, niche, platform, style, hook)
    result = model_router.run("script", prompt)
    return {
        "title":           result.get("title", ""),
        "script":          result.get("script", ""),
        "scene_breakdown": result.get("scene_breakdown", []),
        "cta":             result.get("cta", ""),
    }
