from ai import model_router, prompt_manager

def run(topic: str, niche: str, platform: str) -> dict:
    prompt = prompt_manager.hashtag_prompt(topic, niche, platform)
    result = model_router.run("hashtag", prompt)
    tags = result.get("tags", [])
    # Normalise: ensure each tag starts with #
    tags = [t if t.startswith("#") else f"#{t}" for t in tags]
    return {"tags": tags}
