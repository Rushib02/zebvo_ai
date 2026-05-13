from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectCreateSchema(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=100)
    platform: str
    niche: str
    content_style: str
    target_audience: str
    tone: str
    folder_name: Optional[str] = "General"
    tags: Optional[List[str]] = []

class ProjectUpdateSchema(BaseModel):
    project_name: Optional[str]
    platform: Optional[str]
    niche: Optional[str]
    content_style: Optional[str]
    target_audience: Optional[str]
    tone: Optional[str]
    folder_name: Optional[str]
    tags: Optional[List[str]]
    archived: Optional[bool]
