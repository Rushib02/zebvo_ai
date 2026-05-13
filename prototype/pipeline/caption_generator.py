from ai import model_router, prompt_manager

def run(topic: str, platform: str, style: str, hook: str) -> dict:
    prompt = prompt_manager.caption_prompt(topic, platform, style, hook)
    result = model_router.run("caption", prompt)
    return {
        "primary":   result.get("primary", ""),
        "secondary": result.get("secondary", ""),
    }
