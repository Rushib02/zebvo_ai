# AI Creator Studio Backend

Foundational backend architecture for a production-grade AI SaaS platform.

## Tech Stack
- **Python 3.11+**
- **Flask** (App Factory Pattern)
- **MongoDB** (Pymongo)
- **JWT** (Flask-JWT-Extended)
- **Ollama** & **Gemini API**
- **Stable Diffusion** ready

## Project Structure
- `app/`: Core application logic
  - `ai/`: AI service integrations (Gemini, Ollama, SD)
  - `config/`: Environment-aware configurations
  - `database/`: Database connection management
  - `routes/`: API blueprints
  - `utils/`: Logging and helper functions
- `logs/`: Structured JSON logs (access, error, AI)
- `uploads/` & `generated/`: Media storage

## Getting Started

### Windows
Run the automated setup script:
```bash
setup.bat
```

### Linux/macOS
Make the setup script executable and run it:
```bash
chmod +x setup.sh
./setup.sh
```

## API Endpoints
- **Health Check**: `GET /api/v1/health`

## Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
- `GEMINI_API_KEY`
- `MONGO_URI`
- `SECRET_KEY`

## Logging
Logs are stored in the `logs/` directory in structured JSON format for easy ingestion by log management systems.
- `errors.log`: Error level logs and exceptions.
- `requests.log`: API request and response metadata.
- `ai.log`: Specific logs related to AI model interactions.
