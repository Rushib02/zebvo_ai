from pydantic import BaseModel, Field
from typing import List, Optional

class Idea(BaseModel):
    title: str
    description: str
    target_audience: str

class Hook(BaseModel):
    hook_text: str
    emotion_target: str
    visual_cue: str

class Script(BaseModel):
    full_text: str
    estimated_duration: int

class Scene(BaseModel):
    scene_number: int
    visual: str
    audio: str

class SceneBreakdown(BaseModel):
    scenes: List[Scene]

class CTA(BaseModel):
    text: str
    placement: Optional[str] = "End of Video"

class Caption(BaseModel):
    primary_text: str
    secondary_text: Optional[str]

class Hashtags(BaseModel):
    tags: List[str]

class ThumbnailPrompt(BaseModel):
    prompt: str
    style_reference: str

class ViralScore(BaseModel):
    score: float = Field(..., ge=0, le=100)
    strengths: List[str]
    weaknesses: List[str]

class PipelineState(BaseModel):
    idea: Optional[Idea] = None
    hook: Optional[Hook] = None
    script: Optional[Script] = None
    scenes: Optional[SceneBreakdown] = None
    cta: Optional[CTA] = None
    caption: Optional[Caption] = None
    hashtags: Optional[Hashtags] = None
    thumbnail: Optional[ThumbnailPrompt] = None
    viral_score: Optional[ViralScore] = None
