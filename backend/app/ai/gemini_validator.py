from pydantic import BaseModel, Field
from typing import List, Optional

class Scene(BaseModel):
    scene_number: int
    visual_description: str
    audio_narration: str
    duration_seconds: int

class GeminiScript(BaseModel):
    title: str = Field(..., description="A compelling title for the content")
    hook: str = Field(..., description="The high-impact opening hook")
    cinematic_script: str = Field(..., description="The full narrative script")
    scene_breakdown: List[Scene] = Field(..., description="Detailed breakdown of visual and audio elements")
    cta: str = Field(..., description="Call to action for the audience")
    retention_strategy: str = Field(..., description="Tactics used to maintain viewer interest throughout")
    platform_optimization: Optional[str] = Field(None, description="Specific optimizations for the target platform")

def validate_gemini_response(data: dict) -> GeminiScript:
    """Validates raw dictionary data against the GeminiScript schema."""
    return GeminiScript(**data)
