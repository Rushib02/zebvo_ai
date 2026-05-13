import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)))
    
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ai_creator_studio')
    
    # AI Configs
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    SD_API_URL = os.environ.get('SD_API_URL', 'http://localhost:7860')
    
    # Folders
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    GENERATED_FOLDER = os.path.join(os.getcwd(), 'generated')
    
    # Misc
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    # In production, require environment variables
    # SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.environ.get('MONGO_URI_TEST', 'mongodb://localhost:27017/ai_creator_studio_test')
    WTF_CSRF_ENABLED = False

config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    testing=TestingConfig
)

key = Config.SECRET_KEY
