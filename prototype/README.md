# AI Creator Studio Prototype (Terminal Edition)

This is a complete terminal-based prototype designed to validate the AI content generation pipeline before Flask backend development.

## 🚀 Overview
The prototype orchestrates multiple AI models (Ollama and Gemini) to generate high-quality short-form content.

### Model Routing
- **Mistral (Ollama)**: Hashtag generation.
- **Gemma (Ollama)**: Caption generation.
- **Llama3 (Ollama)**: Hooks and Thumbnail prompts.
- **Gemini (Flash)**: Full script generation and cinematic breakdown.

## 🛠️ Prerequisites
1. **Ollama**: [Download and install Ollama](https://ollama.ai/).
2. **Gemini API Key**: Obtain one from [Google AI Studio](https://aistudio.google.com/).
3. **Python 3.10+**

## ⚡ Quick Start

### Windows
1. Open terminal in the `prototype/` directory.
2. Run: `setup.bat`

### Linux / Mac
1. Open terminal in the `prototype/` directory.
2. Make script executable: `chmod +x setup.sh`
3. Run: `./setup.sh`

## 📂 Structure
- `ai/`: Core service wrappers and routing logic.
- `pipeline/`: Individual generation stages.
- `utils/`: Logging, validation, and parsing helpers.
- `main.py`: Interactive terminal interface.

## 🧪 Validation
This prototype validates:
- [x] Multi-model orchestration.
- [x] Graceful fallback to Gemini if Ollama is offline.
- [x] Structured JSON parsing from LLM outputs.
- [x] Rule-based viral score heuristics.
