import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from app.ai.ollama_service import ollama_service
from app.ai.model_router import model_router

logger = logging.getLogger(__name__)

class StreamlitGenerationHelper:
    """Helper class for Streamlit to generate content with proper error handling"""
    
    @staticmethod
    def generate_idea(topic: str, platform: str) -> dict:
        """Generate content idea"""
        prompt = f"""Generate a viral content idea for this topic in JSON format:

Topic: {topic}
Platform: {platform}

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "title": "catchy title",
  "description": "brief description",
  "target_audience": "who will watch",
  "key_message": "main point",
  "why_viral": "why it will go viral"
}}"""
        try:
            result = model_router.generate_with_fallback("idea", prompt, topic)
            return result if result else {"title": f"Untitled - {topic}", "description": "Auto-generated content"}
        except Exception as e:
            logger.error(f"Idea generation failed: {e}")
            return {"title": f"Untitled - {topic}", "description": "Failed to generate"}

    @staticmethod
    def generate_hook(topic: str, hook_type: str = "Curiosity") -> dict:
        """Generate compelling hook"""
        prompt = f"""Create a viral hook for this topic in JSON format:

Topic: {topic}
Hook Type: {hook_type}

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "hook_text": "opening line that stops scrolling",
  "emotional_trigger": "emotion it triggers",
  "visual_cue": "what should be on screen"
}}"""
        try:
            result = model_router.generate_with_fallback("hook", prompt, topic)
            return result if result else {"hook_text": f"Stop! {topic} will change your life!", "emotional_trigger": "Curiosity"}
        except Exception as e:
            logger.error(f"Hook generation failed: {e}")
            return {"hook_text": "Generating hook...", "emotional_trigger": "Curiosity"}

    @staticmethod
    def generate_script(topic: str, style: str, length: int = 60, script_format: str = "Monologue", 
                       num_characters: int = 1, pacing: str = "Normal", custom_notes: str = "") -> dict:
        """Generate full script with detailed specifications"""
        
        # Simplified prompt for better Ollama compatibility
        format_info = {
            "Monologue": "Single person speaking to camera. Natural pauses and emphasis.",
            "Dialogue (2 people)": "Two characters talking. Create distinct voices/personalities.",
            "Dialogue (3 people)": "Three characters in conversation.",
            "Skit (3+ people)": f"{num_characters} characters in a dramatic scene/skit."
        }
        
        pacing_info = {
            "Very Slow": "slow deliberate delivery",
            "Slow": "measured thoughtful pace",
            "Normal": "standard conversation pace",
            "Fast": "quick energetic delivery",
            "Very Fast": "rapid high-energy delivery"
        }
        
        # Much simpler, more direct prompt
        prompt = f"""Write a {length}-second video script.

TOPIC: {topic}
STYLE: {style}
FORMAT: {format_info.get(script_format, format_info['Monologue'])}
PACING: {pacing_info.get(pacing, 'normal')}
CHARACTERS: {num_characters}
{"NOTES: " + custom_notes if custom_notes else ""}

OUTPUT AS JSON - Include timing [seconds] for each line:
{{
  "script_type": "{script_format}",
  "num_characters": {num_characters},
  "duration": {length},
  "full_text": "Complete script text with [time] marks for each section",
  "scenes": [
    {{"time": "[0-5 sec]", "character": "Speaker", "text": "Opening line"}},
    {{"time": "[5-10 sec]", "character": "Speaker", "text": "Next section"}},
    {{"time": "[end]", "character": "Speaker", "text": "Closing line"}}
  ]
}}"""

        try:
            result = model_router.generate_with_fallback("script", prompt, topic)
            if result:
                # Ensure full_text exists
                if 'full_text' not in result:
                    if 'scenes' in result and isinstance(result['scenes'], list):
                        script_lines = []
                        for scene in result['scenes']:
                            if isinstance(scene, dict):
                                time = scene.get('time', '')
                                character = scene.get('character', 'Speaker')
                                text = scene.get('text', '')
                                script_lines.append(f"{time} {character}: {text}")
                        result['full_text'] = "\n".join(script_lines)
                    else:
                        # Try to find any text content
                        found_text = False
                        for key in ['content', 'script', 'dialogue']:
                            if key in result:
                                result['full_text'] = str(result[key])
                                found_text = True
                                break
                        if not found_text:
                            result['full_text'] = str(result)
                
                return result
            else:
                return {
                    "script_type": script_format,
                    "num_characters": num_characters,
                    "duration": length,
                    "full_text": f"[0-{length} sec] Default script about {topic}.",
                    "error": "Empty response"
                }
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            return {
                "script_type": script_format,
                "num_characters": num_characters,
                "duration": length,
                "full_text": f"[0-{length} sec] Error generating script: {str(e)[:50]}",
                "error": str(e)
            }

    @staticmethod
    def generate_caption(topic: str) -> dict:
        """Generate caption"""
        prompt = f"""Create an optimized caption for this topic in JSON format:

Topic: {topic}

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "primary_text": "main caption with emoji",
  "secondary_text": "alternative caption",
  "call_to_action": "what to ask viewers to do"
}}"""
        try:
            result = model_router.generate_with_fallback("caption", prompt, topic)
            return result if result else {"primary_text": f"Check out: {topic} 🚀"}
        except Exception as e:
            logger.error(f"Caption generation failed: {e}")
            return {"primary_text": "Caption generation failed"}

    @staticmethod
    def generate_hashtags(topic: str, platform: str = "Instagram") -> dict:
        """Generate hashtags"""
        prompt = f"""Generate trending hashtags for this topic in JSON format:

Topic: {topic}
Platform: {platform}

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "trending": ["#hashtag1", "#hashtag2", "#hashtag3"],
  "niche": ["#niche1", "#niche2"],
  "tags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"]
}}"""
        try:
            result = model_router.generate_with_fallback("hashtags", prompt, topic)
            if result and 'tags' not in result and 'trending' in result:
                # Normalize to have 'tags' key
                tags = result.get('trending', [])
                result['tags'] = [t.replace('#', '') for t in tags]
            return result if result else {"tags": ["viral", "trending", topic.lower().replace(' ', '')]}
        except Exception as e:
            logger.error(f"Hashtag generation failed: {e}")
            return {"tags": ["content", "viral"]}

    @staticmethod
    def generate_thumbnail(topic: str, style: str = "Modern") -> dict:
        """Generate thumbnail concept"""
        prompt = f"""Create a thumbnail concept for this topic in JSON format:

Topic: {topic}
Visual Style: {style}

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "prompt": "detailed visual description for image generation",
  "style_reference": "visual style",
  "color_scheme": "recommended colors",
  "text_overlay": "what text should be on the thumbnail"
}}"""
        try:
            result = model_router.generate_with_fallback("thumbnail", prompt, topic)
            return result if result else {"prompt": f"Cinematic thumbnail about {topic}"}
        except Exception as e:
            logger.error(f"Thumbnail generation failed: {e}")
            return {"prompt": "Thumbnail concept"}

    @staticmethod
    def generate_viral_score(script: str, hook: str, cta: str) -> dict:
        """Analyze viral potential"""
        prompt = f"""Analyze the viral potential of this content in JSON format:

Hook: {hook[:100]}
Script: {script[:200]}
CTA: {cta}

Return ONLY valid JSON (no markdown, no code blocks):
{{
  "score": 75,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "recommendations": ["tip1", "tip2"]
}}"""
        try:
            result = model_router.generate_with_fallback("viral_score", prompt, "virality analysis")
            if result and 'score' not in result:
                result['score'] = 70
            return result if result else {"score": 70, "strengths": ["Good structure"], "weaknesses": ["Can improve"]}
        except Exception as e:
            logger.error(f"Viral score generation failed: {e}")
            return {"score": 50, "strengths": [], "weaknesses": []}


# For import
import json
