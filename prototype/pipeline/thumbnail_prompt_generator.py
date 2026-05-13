from ai import model_router, prompt_manager

def run(topic: str, style: str, hook: str) -> dict:
    prompt = prompt_manager.thumbnail_prompt(topic, style, hook)
    result = model_router.run("thumbnail", prompt)
    return {
        "prompt":          result.get("prompt", ""),
        "style_reference": result.get("style_reference", ""),
        "colour_palette":  result.get("colour_palette", ""),
    }
