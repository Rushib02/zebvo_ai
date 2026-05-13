import random

class FallbackGenerator:
    """
    Template-based random fallback generator for when all AI services fail.
    Ensures the pipeline doesn't crash and provides 'safe' defaults.
    """
    
    HOOKS = [
        "Stop scrolling! This changes everything.",
        "The secret to {topic} that nobody tells you.",
        "Why you're failing at {topic} (and how to fix it).",
        "3 things you didn't know about {topic}.",
        "This is the future of {topic}."
    ]
    
    CTAS = [
        "Like and follow for more!",
        "Comment '{topic}' if you want the full guide.",
        "Share this with a friend who needs to see it.",
        "Check the link in bio for the deep dive.",
        "Save this for your next project."
    ]
    
    HASHTAGS = ["viral", "trending", "contentcreator", "ai", "tips", "hacks"]

    @classmethod
    def generate_hook(cls, topic: str):
        hook = random.choice(cls.HOOKS).format(topic=topic)
        return {
            "hook_text": hook,
            "emotion_target": "Curiosity",
            "visual_cue": "Fast cut to the host looking surprised."
        }

    @classmethod
    def generate_script(cls, topic: str):
        return {
            "full_text": f"Today we are talking about {topic}. It's a huge trend right now and you need to pay attention. "
                         f"Step 1: Understand the basics. Step 2: Implement the strategy. Step 3: Profit. "
                         f"Don't forget to follow for more daily {topic} hacks!",
            "estimated_duration": 45
        }

    @classmethod
    def generate_cta(cls, topic: str):
        return {
            "text": random.choice(cls.CTAS).format(topic=topic),
            "placement": "End of video"
        }

    @classmethod
    def generate_hashtags(cls, topic: str):
        tags = random.sample(cls.HASHTAGS, 3) + [topic.lower().replace(" ", "")]
        return {"tags": tags}

    @classmethod
    def generate_caption(cls, topic: str):
        return {
            "primary_text": f"Unlocking the power of {topic}! 🚀",
            "secondary_text": "Is this the next big thing?"
        }
    
    @classmethod
    def generate_thumbnail_prompt(cls, topic: str):
        return {
            "prompt": f"High resolution cinematic shot representing {topic}, glowing neon accents, 8k",
            "style_reference": "Modern Minimalist"
        }

    @classmethod
    def generate_viral_score(cls):
        return {
            "score": 65.0,
            "strengths": ["Clear topic", "Solid structure"],
            "weaknesses": ["Generic hook", "Basic CTA"]
        }

fallback_generator = FallbackGenerator()
