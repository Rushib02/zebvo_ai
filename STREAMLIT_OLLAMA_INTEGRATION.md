# 🚀 Ollama + Streamlit Integration Guide

## What's Integrated?

### ✅ Ollama Integration with Streamlit

The new `app_ollama_integrated.py` combines:
- **Hybrid AI Engine**: Automatic fallback from Gemini → Ollama → Template Generator
- **Live Status Dashboard**: Real-time monitoring of Gemini and Ollama status
- **Model Router**: Smart orchestration that picks the best AI for each task
- **AI Diagnostics**: Test and debug the entire system

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Streamlit Frontend                      │
│  (app_ollama_integrated.py)                     │
└────────────┬────────────────────────────────────┘
             │
             ├─────────────────────┐
             │                     │
             v                     v
    ┌──────────────┐      ┌──────────────────┐
    │  Gemini      │      │  Model Router    │
    │  API (Cloud) │      │  (Orchestrator)  │
    └──────────────┘      └────────┬─────────┘
                                   │
                      ┌────────────┼────────────┐
                      │            │            │
                      v            v            v
              ┌───────────┐  ┌──────────┐  ┌────────────┐
              │ Ollama    │  │ Ollama   │  │  Template  │
              │ Mistral   │  │ Service  │  │ Fallback   │
              │ (4.4 GB)  │  │(11434)   │  │ Generator  │
              └───────────┘  └──────────┘  └────────────┘
```

## Quick Start

### Option 1: One-Command Start (Recommended)

```bash
cd backend
run-streamlit.bat
```

This script automatically:
- ✓ Activates virtual environment
- ✓ Starts Ollama (if not running)
- ✓ Verifies Mistral model
- ✓ Launches Streamlit UI

### Option 2: Manual Multi-Terminal Setup

**Terminal 1: Start Ollama**
```bash
ollama serve
```

**Terminal 2: Start Streamlit**
```bash
cd backend
venv\Scripts\activate
streamlit run app_ollama_integrated.py
```

## Features

### 1. Real-Time AI Status Dashboard (Sidebar)
- 🟢 Gemini 1.5 Status
- 🟢 Ollama + Mistral Status
- 🔄 Refresh button for live monitoring
- ⚠️ Helpful hints when services are offline

### 2. AI Preference Control
Choose how content is generated:
- **Auto** (Recommended): Tries Gemini first, falls back to Ollama
- **Prefer Gemini**: Cloud-only (faster when available, requires API key)
- **Prefer Ollama**: Local-only (privacy + no API costs)
- **Force Fallback**: Template-based (instant, no AI)

### 3. AI Diagnostics Page
Access via sidebar: `🔧 AI Diagnostics`
- System health checks
- Real-time performance testing
- Individual stage testing
- Debug logs

### 4. Content Generation with AI Tracking
When generating content:
- See which AI model is being used (⚡ Gemini, 🧠 Ollama, 📋 Template)
- Track generation stages in real-time
- Monitor processing time
- Fallback happens automatically if primary fails

## Configuration

### Use Different Ollama Model

Edit `backend/app/ai/ollama_service.py`:

```python
def __init__(self, base_url="http://localhost:11434"):
    self.base_url = base_url
    self.model = "neural-chat"  # Change from "mistral"
```

Then pull the new model:
```bash
ollama pull neural-chat
```

### Custom Ollama Port

Change in the same file if you run Ollama on a different port:
```python
def __init__(self, base_url="http://localhost:9999"):  # Custom port
```

### API Keys (.env)

```env
GEMINI_API_KEY=your-key-here      # For Gemini (cloud)
MONGO_URI=mongodb://localhost:27017  # For database
SECRET_KEY=your-secret-key         # For sessions
FLASK_ENV=development
```

## What Happens During Generation?

### Generation Flow

1. **User clicks "Generate Content"**
2. **Model Router evaluates availability**: 
   - Check Gemini API status
   - Check Ollama server status
   - Check AI preference setting
3. **Execute generation stages**:
   - Hook generation
   - Script writing
   - Caption creation
   - Hashtag generation
   - Thumbnail ideation
   - Viral score analysis
4. **Display results with AI indicator**:
   - ⚡ Gemini = Cloud AI used
   - 🧠 Ollama = Local AI used
   - 📋 Template = Fallback used

### Automatic Fallback Example

```
Generation started with topic: "The future of AI"

Stage: Hook
├─ Try Gemini API
│  └─ ✓ Success! Using Gemini
│
Stage: Script  
├─ Try Gemini API
│  └─ ✗ API rate limit hit
├─ Try Ollama
│  └─ ✓ Success! Switched to Ollama
│
Stage: Caption
├─ Try Gemini API
│  └─ ✓ Success! Back to Gemini

Result: Mixed generation (Hybrid AI)
```

## Troubleshooting

### "Ollama Offline" Error

**Problem**: Can't connect to Ollama  
**Solution**: 
```bash
ollama serve     # In a separate terminal
```

### "Mistral not found" Error

**Problem**: Model not downloaded  
**Solution**:
```bash
ollama pull mistral   # Downloads 4.4 GB
```

### "Gemini API Error"

**Problem**: API key missing or rate limited  
**Solution**:
1. Add `GEMINI_API_KEY` to `.env`
2. Use "Prefer Ollama" mode to bypass cloud
3. Increase API quota on Google Cloud console

### Port Already in Use

**Problem**: Ollama port 11434 is taken  
**Solution**:
```bash
# Find what's using the port
netstat -ano | findstr :11434

# Kill it (replace PID)
taskkill /PID 12345 /F

# Or change Ollama port
ollama serve --port 11435
```

### High Memory Usage

**Problem**: System is slow with Ollama running  
**Solution**:
1. Use smaller model: `ollama pull neural-chat`
2. Close other applications
3. Increase system virtual memory
4. Use Gemini-only mode temporarily

## Performance Tips

### For Speed
- **Use Gemini** if API available (3-5s per stage)
- **Cache responses** (same topic = instant replay)
- **Disable Ollama** if not needed

### For Privacy
- **Use Ollama only** (all processing local)
- **Disable cloud AI** in security settings
- **No data leaves your machine**

### For Reliability
- **Auto mode** (best of both)
- **Test with Diagnostics** before production
- **Monitor logs** in `backend/logs/`

## Available Models

Download alternatives to Mistral:
```bash
ollama pull neural-chat     # Fast, lightweight
ollama pull llama2          # Good for scripts
ollama pull dolphin-mixtral # Most powerful (26 GB!)
ollama pull orca-mini       # Super fast
```

## File Structure

```
backend/
├── app_ollama_integrated.py      # ← New enhanced Streamlit app
├── app.py                         # ← Original app
├── run-streamlit.bat              # ← One-command launcher
├── start-ollama.bat               # ← Ollama launcher
├── run-backend.bat                # ← Flask backend launcher
│
├── app/
│   └── ai/
│       ├── ollama_service.py      # Ollama client
│       ├── model_router.py        # Smart orchestrator
│       ├── gemini_service.py      # Gemini client
│       └── fallback_generator.py  # Emergency templates
│
└── scratch/
    └── test_ollama_integration.py # Test suite
```

## Running Everything Together

### All-in-One Startup

```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: Streamlit (opens UI automatically)
cd backend
run-streamlit.bat
```

Then:
1. Open browser to `http://localhost:8501`
2. Select AI preference in sidebar
3. Click "Generate Content"
4. Watch the magic! ✨

### Backend API (Flask)

If you also want the Flask backend running:

```bash
# Terminal 3: Flask API
cd backend
run-backend.bat
```

Then API is available at `http://localhost:5000/api/v1/`

## Advanced: Using Both Frontend & Backend

### Setup 3 Terminals

1. **Ollama** (background service)
   ```bash
   ollama serve
   ```

2. **Flask Backend** (API server)
   ```bash
   cd backend
   run-backend.bat
   ```

3. **Streamlit Frontend** (UI)
   ```bash
   cd backend
   run-streamlit.bat
   ```

### They'll coordinate:
- Streamlit UI talks to Flask API (optional)
- Flask API uses Model Router for generation
- Model Router uses Ollama + Gemini
- Both frontends see the same AI status

## Monitoring & Logs

### View Real-Time Logs

```bash
# AI operations
tail -f backend/logs/ai.log

# Errors
tail -f backend/logs/errors.log

# API requests
tail -f backend/logs/requests.log
```

### Check Ollama Logs

Ollama logs appear in the console where you ran `ollama serve`

## Next Steps

1. ✅ Start Ollama: `ollama serve`
2. ✅ Start Streamlit: `run-streamlit.bat`
3. ✅ Open `http://localhost:8501`
4. ✅ Try generating content
5. ✅ Check the AI indicator (⚡/🧠/📋)
6. ✅ Use Diagnostics page to test fallback

## Need Help?

1. **Check logs**: `backend/logs/`
2. **Run tests**: `python scratch/test_ollama_integration.py`
3. **Diagnose system**: Use 🔧 AI Diagnostics page in Streamlit
4. **Check status**: Sidebar shows all AI service status

---

**🎉 You now have a fully hybrid AI system!**  
Enjoy unlimited generation with automatic failover! ✨
