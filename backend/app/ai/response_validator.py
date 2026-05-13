from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any
from app.ai.ai_logger import AILogger

class ResponseValidator:
    @staticmethod
    def validate_schema(data: Any, schema_class: type[BaseModel]):
        """Validates AI response data against a Pydantic schema."""
        try:
            return schema_class(**data).dict()
        except ValidationError as e:
            AILogger.log_error("validator", f"Schema validation failed: {str(e)}")
            raise ValueError(f"AI response did not match expected schema: {str(e)}")

# Define common AI schemas
class HashtagResponse(BaseModel):
    hashtags: List[str]

class CaptionResponse(BaseModel):
    captions: List[str]

class HookResponse(BaseModel):
    hooks: List[str]

class CTAResponse(BaseModel):
    cta_options: List[str]

class ThumbnailPromptResponse(BaseModel):
    prompts: List[str]
    style_guidelines: str
