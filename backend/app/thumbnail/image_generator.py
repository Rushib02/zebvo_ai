import os
import google.generativeai as genai
import asyncio
from typing import Optional

class GeminiImageGenerator:
    def __init__(self, model_name: str = "imagen-4.0-generate-001"):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    async def generate(self, prompt: str) -> bytes:
        """
        Generates an image using Gemini Imagen model.
        Returns the raw image bytes.
        """
        # Note: Depending on the specific SDK version, the method name might vary.
        # For current enterprise-grade patterns, we use the generate_content or specific image methods.
        # Assuming standard imagen generation call:
        try:
            # We run the synchronous SDK call in a thread to keep the service async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: self.model.generate_content(prompt))
            
            # For Imagen models, the response contains the image data in the parts
            if response.candidates and response.candidates[0].content.parts:
                # In many versions, image models return the image as a blob
                image_part = response.candidates[0].content.parts[0]
                if hasattr(image_part, 'inline_data'):
                    return image_part.inline_data.data
                elif hasattr(image_part, 'blob'):
                    return image_part.blob.data
            
            raise ValueError("No image data found in Gemini response")
            
        except Exception as e:
            raise Exception(f"Imagen generation failed: {str(e)}")
