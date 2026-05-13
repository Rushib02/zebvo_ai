"""
Centralised prompt templates for every pipeline stage.
Each builder returns a string prompt that instructs the AI
to respond with a single, flat JSON object.
"""

_JSON_RULE = (
    "\n\nIMPORTANT: Respond with ONLY a valid JSON object. "
    "No markdown, no explanation, no extra text."
)

# ── Hook ───────────────────────────────────────────────────────────────────────

def hook_prompt(topic: str, niche: str, platform: str, style: str) -> str:
    example = '{"hook": "string", "emotion": "string", "visual_cue": "string"}'
    return (
        f"You are a viral content strategist.\n"
        f"Topic: {topic}\nNiche: {niche}\nPlatform: {platform}\nStyle: {style}\n\n"
        f"Create a 1-2 sentence high-impact opening hook that stops the scroll.\n"
        f"Return JSON matching: {example}{_JSON_RULE}"
    )

# ── Script ─────────────────────────────────────────────────────────────────────

def script_prompt(topic: str, niche: str, platform: str, style: str, hook: str) -> str:
    example = (
        '{"title": "string", "script": "string", '
        '"scene_breakdown": [{"scene": 1, "visual": "string", "narration": "string"}], '
        '"cta": "string"}'
    )
    return (
        f"You are a master cinematic scriptwriter.\n"
        f"Topic: {topic}\nNiche: {niche}\nPlatform: {platform}\nStyle: {style}\n"
        f"Opening Hook: {hook}\n\n"
        f"Write a punchy 60-second script. Include: title, full script, "
        f"3-5 scene breakdown, and a call to action.\n"
        f"Return JSON matching: {example}{_JSON_RULE}"
    )

# ── Caption ────────────────────────────────────────────────────────────────────

def caption_prompt(topic: str, platform: str, style: str, hook: str) -> str:
    example = '{"primary": "string", "secondary": "string"}'
    return (
        f"You are a social media copywriter.\n"
        f"Topic: {topic}\nPlatform: {platform}\nStyle: {style}\nHook: {hook}\n\n"
        f"Write a compelling post caption (primary) and a short teaser (secondary).\n"
        f"Return JSON matching: {example}{_JSON_RULE}"
    )

# ── Hashtags ───────────────────────────────────────────────────────────────────

def hashtag_prompt(topic: str, niche: str, platform: str) -> str:
    example = '{"tags": ["#example1", "#example2"]}'
    return (
        f"You are a hashtag research specialist.\n"
        f"Topic: {topic}\nNiche: {niche}\nPlatform: {platform}\n\n"
        f"Generate exactly 12 high-reach trending hashtags. Mix broad and niche tags.\n"
        f"Return JSON matching: {example}{_JSON_RULE}"
    )

# ── Thumbnail prompt ───────────────────────────────────────────────────────────

def thumbnail_prompt(topic: str, style: str, hook: str) -> str:
    example = '{"prompt": "string", "style_reference": "string", "colour_palette": "string"}'
    return (
        f"You are a thumbnail art director.\n"
        f"Topic: {topic}\nStyle: {style}\nHook: {hook}\n\n"
        f"Write a detailed DALL-E / Stable Diffusion prompt for a high-CTR thumbnail.\n"
        f"Return JSON matching: {example}{_JSON_RULE}"
    )
