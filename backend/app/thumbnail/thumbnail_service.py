import os
import logging
from app.thumbnail.image_generator import GeminiImageGenerator
from app.thumbnail.image_storage import ThumbnailStorage
from app.thumbnail.thumbnail_validator import ThumbnailValidator
from app.ai.ollama_service import ollama_service

logger = logging.getLogger(__name__)

class ThumbnailService:
    def __init__(self):
        self.generator = GeminiImageGenerator()
        self.storage = ThumbnailStorage()
        self.validator = ThumbnailValidator()

    async def create_thumbnail(self, project_id: str, script_text: str):
        """
        End-to-end workflow: Concept -> Prompt -> Image -> Storage
        """
        try:
            # 1. Generate Thumbnail Concept & Prompt using Gemini Text
            concept_prompt = f"Based on this script, create a high-impact cinematic thumbnail concept and a detailed AI image generation prompt. \nScript: {script_text[:1000]}"
            
            # Use the existing ollama_service for text generation
            # Note: We want a structured prompt for the image generator
            ollama_result = ollama_service.generate("thumbnail_prompt", concept_prompt)
            image_prompt = ollama_result.get('text', '').strip()
            
            logger.info(f"Generated image prompt for project {project_id}")

            # 2. Generate Image using Imagen
            image_data = await self.generator.generate(image_prompt)
            
            # 3. Store Image and Metadata
            image_path = self.storage.save_image(project_id, image_data)
            self.storage.save_metadata(project_id, image_path, image_prompt)
            
            return {
                "project_id": project_id,
                "image_path": image_path,
                "image_prompt": image_prompt
            }

        except Exception as e:
            logger.error(f"Thumbnail generation failed: {str(e)}")
            raise
