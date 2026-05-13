from pydantic import BaseModel, field_validator
from typing import List, Optional

class UserInput(BaseModel):
    topic: str
    niche: str
    platform: str
    style: str

    @field_validator('topic', 'niche', 'platform', 'style')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

SUPPORTED_PLATFORMS = [
    "YouTube Shorts", "Instagram Reels", "TikTok", "LinkedIn"
]

SUPPORTED_STYLES = [
    "Cinematic", "Educational", "Motivational", "Comedic", "Documentary"
]
