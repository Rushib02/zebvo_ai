import os
import json
import hashlib
from app.services.pipeline_logger import pipeline_logger

class GenerationCache:
    def __init__(self, cache_dir=".cache/ai_generation"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _generate_key(self, prompt: str, model_config: dict) -> str:
        data = f"{prompt}:{json.dumps(model_config, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get(self, prompt: str, model_config: dict):
        key = self._generate_key(prompt, model_config)
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    pipeline_logger.info("Cache hit", extra={"stage": "caching", "status": "HIT"})
                    return json.load(f)
            except Exception as e:
                pipeline_logger.error(f"Cache read error: {str(e)}")
        
        return None

    def set(self, prompt: str, model_config: dict, response: dict):
        key = self._generate_key(prompt, model_config)
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(response, f, indent=2)
            pipeline_logger.info("Cache saved", extra={"stage": "caching", "status": "SAVED"})
        except Exception as e:
            pipeline_logger.error(f"Cache write error: {str(e)}")

generation_cache = GenerationCache()
