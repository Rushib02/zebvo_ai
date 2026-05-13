import os
import google.generativeai as genai
from dotenv import load_dotenv
from ai.retry_handler import with_retry
from utils.helpers import extract_json
from utils.logger import error

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise EnvironmentError("GEMINI_API_KEY is not set in .env")

genai.configure(api_key=_api_key)

_MODEL_NAME = "gemini-1.5-flash"
_model = genai.GenerativeModel(_MODEL_NAME)

_GEN_CONFIG = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,
}

@with_retry(max_retries=3, delay=2.0)
def generate(prompt: str) -> dict:
    """
    Calls Gemini and returns a parsed JSON dict.
    The prompt must instruct the model to return JSON.
    """
    response = _model.generate_content(prompt, generation_config=_GEN_CONFIG)
    if not response.text:
        raise ValueError("Gemini returned an empty response.")
    return extract_json(response.text)
