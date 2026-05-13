# 🚀 Ollama Integration Guide

## Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
cd backend
setup-full.bat        # One-time setup
start-ollama.bat      # Starts Ollama in background
run-backend.bat       # Starts the Flask backend
```

### Option 2: Manual Setup

#### 1. Install Ollama
- Download from: https://ollama.ai
- Install and run the installer

#### 2. Setup Python Environment
```bash
cd backend
.\setup.bat           # Creates venv and installs dependencies
```

#### 3. Pull Mistral Model
```bash
ollama pull mistral
```

#### 4. Start Ollama (in one terminal)
```bash
ollama serve
```

#### 5. Start Backend (in another terminal)
```bash
cd backend
venv\Scripts\activate
python run.py
```

## Verification

### Check Ollama Status
```bash
# Check if server is running
ollama list

# Should show:
# NAME              ID              SIZE      MODIFIED
# mistral:latest    6577803aa9a0    4.4 GB    6 seconds ago
```

### Test Integration
```bash
cd backend
python scratch/test_ollama_integration.py

# Expected output:
# ✓ ALL TESTS PASSED - Ollama is ready to use!
```

## Architecture

### Fallback Chain (Automatic)
1. **Primary**: Gemini 1.5 Pro (Cloud)
2. **Fallback**: Ollama Mistral (Local)
3. **Emergency**: Template Generator

When Gemini fails or API limits are hit, the system automatically switches to Ollama.

## Configuration

### Custom Ollama URL
Edit `backend/app/ai/ollama_service.py`:
```python
def __init__(self, base_url="http://localhost:11434"):  # Change port here
```

### Use Different Model
```python
def __init__(self, base_url="http://localhost:11434"):
    self.base_url = base_url
    self.model = "neural-chat"  # Change to neural-chat, llama2, etc.
```

Then pull the new model:
```bash
ollama pull neural-chat
```

## Available Models

Download any of these:
```bash
ollama pull mistral         # 4.4 GB (Recommended)
ollama pull neural-chat     # 3.8 GB
ollama pull llama2          # 3.8 GB
ollama pull dolphin-mixtral # 26 GB (Powerful)
```

## Troubleshooting

### Ollama Port Already in Use
```bash
# Find what's using port 11434
netstat -ano | findstr :11434

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Start Ollama again
ollama serve
```

### Model Fails to Generate
1. Check logs: `backend/logs/errors.log`
2. Verify model: `ollama list`
3. Test directly: `python scratch/test_ollama_integration.py`

### Memory Issues
If Ollama uses too much RAM:
1. Use smaller model: `ollama pull neural-chat`
2. Close other applications
3. Increase system swap/virtual memory

## Performance Tips

1. **GPU Acceleration** (if available):
   - Ollama automatically uses GPU if CUDA/Metal is available
   - Check with: `ollama -v` (shows GPU info)

2. **Streaming Responses**:
   - Current setup uses `"stream": False` for reliability
   - Can enable streaming in `ollama_service.py` for lower latency

3. **Caching**:
   - Ollama keeps models in memory after first use
   - First call takes ~3-5s, subsequent calls are much faster

## Integration Points

### Services
- `backend/app/ai/ollama_service.py` - Core Ollama client
- `backend/app/ai/model_router.py` - Fallback orchestration
- `backend/app/ai/fallback_generator.py` - Emergency templates

### Tests
- `backend/scratch/test_ollama_integration.py` - Integration tests

### Logs
- `backend/logs/` - All system logs
- Check `errors.log` if something fails

## API Endpoints Using Ollama

When Gemini fails, these routes automatically fall back to Ollama:
- `POST /api/v1/projects/{id}/generate` - Full content generation
- `POST /api/v1/projects/{id}/stages/execute` - Individual stage execution

## What's Next?

1. ✓ Ollama is running (port 11434)
2. ✓ Mistral model is pulled
3. ✓ Integration tests pass
4. Start your backend: `python run.py`
5. Access frontend at configured URL (Streamlit/React)

---

**Need Help?**
- Check logs: `backend/logs/errors.log`
- Test integration: `python scratch/test_ollama_integration.py`
- Ollama docs: https://ollama.ai
