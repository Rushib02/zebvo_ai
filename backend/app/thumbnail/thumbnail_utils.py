from PIL import Image
import io

def validate_image_bytes(image_bytes: bytes) -> bool:
    """Checks if bytes represent a valid image."""
    try:
        Image.open(io.BytesIO(image_bytes))
        return True
    except Exception:
        return False

def get_thumbnail_dimensions(image_path: str):
    """Returns (width, height) of an image file."""
    with Image.open(image_path) as img:
        return img.size
