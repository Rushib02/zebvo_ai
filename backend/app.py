import streamlit as st
import asyncio
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Add the current directory to sys.path to allow imports from 'app'
sys.path.append(str(Path(__file__).parent))

from app.services.pipeline_orchestrator import pipeline_orchestrator
from app.services.project_service import ProjectService
from app.thumbnail.thumbnail_service import ThumbnailService
from app.analytics.analytics_engine import AnalyticsEngine
from app.utils.error_handler import ErrorHandler, GeminiError
from app.utils.helpers import LoadingState, track_time
from app.database.mongodb import get_database
from app.ai.gemini_service import gemini_service
from app.ai.ollama_service import ollama_service

# Load environment variables
load_dotenv()

# Initialize services
thumbnail_service = ThumbnailService()
analytics_engine = AnalyticsEngine()

# Page Config
st.set_page_config(
    page_title="AI Creator Studio Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium SaaS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --bg-dark: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --accent: #00d2ff;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.02em;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
        color: #f1f5f9;
    }
    
    /* Custom Card Style */
    .creator-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .sidebar .stButton button {
        background: linear-gradient(45deg, #4f46e5, #7c3aed);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .sidebar .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Progress Indicator */
    .step-active { color: #6366f1; font-weight: 700; }
    .step-done { color: #10b981; }
    .step-todo { color: #64748b; }
    
    /* Output Area */
    .output-tab {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Analytics Card */
    .analytics-metric {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
        border-radius: 15px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .viral-score {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- Helpers ---
def run_async(coro):
    return asyncio.run(coro)

# Initialize Session State
if "state" not in st.session_state:
    st.session_state.state = {
        "idea": None, "hook": None, "script": None, "captions": None, 
        "hashtags": None, "thumbnail": None, "viral_score": None,
        "current_step": 0, "is_generating": False
    }
if "user_id" not in st.session_state:
    st.session_state.user_id = "pro_creator_01"

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #6366f1;'>💎 Studio Pro</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.selectbox("Navigation", ["🎥 Creator Workspace", "📁 Asset Library", "📊 Insights", "🛠️ Config"])
    
    st.divider()
    st.markdown("### 🧬 Generation Progress")
    steps = ["Targeting", "Ideation", "Scripting", "Engagement", "Optimization"]
    for i, step in enumerate(steps):
        if st.session_state.state["current_step"] > i:
            st.markdown(f"✅ <span class='step-done'>{step}</span>", unsafe_allow_html=True)
        elif st.session_state.state["current_step"] == i:
            st.markdown(f"⏳ <span class='step-active'>{step}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"⚪ <span class='step-todo'>{step}</span>", unsafe_allow_html=True)

    if st.button("✨ New Project", use_container_width=True):
        st.session_state.state = {"idea": None, "hook": None, "script": None, "captions": None, "hashtags": None, "thumbnail": None, "viral_score": None, "current_step": 0, "is_generating": False}
        st.rerun()

# --- Main Workspace ---
if page == "🎥 Creator Workspace":
    col1, col2 = st.columns([1.2, 2], gap="large")
    
    # --- LEFT COLUMN: Inputs & Options ---
    with col1:
        st.markdown("<div class='creator-card'>", unsafe_allow_html=True)
        st.markdown("### 🎨 Creative Controls")
        
        topic = st.text_input("Project Topic", placeholder="e.g., 5 AI hacks for productivity", help="Enter the core idea or theme of your video.")
        platform = st.selectbox("Platform", ["Instagram Reels", "YouTube Shorts", "TikTok", "LinkedIn"])
        
        with st.expander("🛠️ Advanced Optimization", expanded=False):
            niche = st.selectbox("Niche", ["Tech", "Finance", "Fitness", "Fashion", "Comedy", "Motivation", "Education", "Gaming"])
            style = st.selectbox("Content Style", ["Viral Fast-Paced", "Cinematic", "Educational", "Luxury", "Documentary", "Storytelling"])
            audience = st.selectbox("Target Audience", ["Gen Z", "Entrepreneurs", "Developers", "Students", "Professionals", "Creators"])
            tone = st.selectbox("Tone", ["Inspirational", "Funny", "Professional", "Aggressive", "Emotional", "Controversial"])
            hook_type = st.selectbox("Hook Strategy", ["Curiosity", "Problem-Solving", "FOMO", "Emotional", "Controversial"])
            
            st.divider()
            st.markdown("**📝 Script Format**")
            script_type = st.selectbox("Script Type", ["Monologue", "Dialogue", "Skit"], help="Choose how you want the script structured")
            script_pace = st.selectbox("Script Pace", ["Slow Paced", "Fast Paced"], help="Slow paced for educational content, fast paced for viral content")
            
            st.divider()
            length = st.slider("Duration (seconds)", 15, 90, 60)
            language = st.selectbox("Language", ["English", "Hindi", "Hinglish"])
            cta = st.selectbox("CTA Goal", ["Followers", "Comments", "Shares", "Saves", "DMs"])
            visual = st.selectbox("Visual Aesthetic", ["Modern Creator", "Dark Aesthetic", "Luxury", "Minimal", "Neon"])
            notes = st.text_area("Custom AI Instructions", placeholder="e.g., Use a fast-paced MrBeast style editing flow...")

        # --- Local AI Status (Ollama/Mistral) ---
        st.markdown("### 🤖 Hybrid AI Status")
        is_ollama = ollama_service.is_running()
        is_mistral = ollama_service.check_model_available() if is_ollama else False
        
        if is_ollama:
            if is_mistral:
                st.success("Ollama + Mistral: Ready (Fallback Active)")
            else:
                st.warning("Ollama Running: Mistral missing")
                st.info("💡 Run: `ollama pull mistral` to enable local fallback.")
        else:
            st.error("Ollama Offline (No Local Fallback)")
            st.info("💡 Run: `ollama serve` to enable local hybrid generation.")
        
        st.divider()

        if st.button("🚀 Generate Content", use_container_width=True):
            if not topic:
                st.warning("Please define a topic to begin.")
            else:
                # Display selected options
                st.info(f"📝 Script Format: **{script_type}** | ⚡ Pace: **{script_pace}**")
                
                st.session_state.state["is_generating"] = True
                
                # --- Step-by-Step Generation to avoid timeouts ---
                try:
                    # 1. Ideation & Hook
                    with st.status("🧠 Brainstorming Hook & Idea...", expanded=False) as status:
                        st.write("Analyzing platform trends...")
                        # Run pipeline stages manually or through orchestrator
                        # For simplicity in this demo, we'll run the full pipeline but show progress
                        # In production, we'd call specific async tasks
                        results = run_async(pipeline_orchestrator.run_full_pipeline(topic, script_type, script_pace))
                        st.session_state.state.update(results)
                        st.session_state.state["current_step"] = 5
                        status.update(label="✅ Content Architecture Ready!", state="complete")
                    
                    st.success("Generation Complete!")
                    st.session_state.state["is_generating"] = False
                except Exception as e:
                    ErrorHandler.handle(e, context="SaaS Pipeline")
                    st.session_state.state["is_generating"] = False
        
        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: Outputs & Analytics ---
    with col2:
        if st.session_state.state["idea"]:
            st.markdown("<div class='creator-card'>", unsafe_allow_html=True)
            
            # Header with Score
            h_col1, h_col2 = st.columns([3, 1])
            with h_col1:
                idea_title = st.session_state.state['idea'].title if st.session_state.state['idea'] else 'Project Output'
                st.markdown(f"## {idea_title}")
                st.caption(f"Platform: {platform} | Style: {style}")
            with h_col2:
                viral_data = st.session_state.state['viral_score'].model_dump() if st.session_state.state['viral_score'] else {}
                score = viral_data.get('score', 85)
                st.markdown(f"<div class='viral-score'>{int(score)}</div>", unsafe_allow_html=True)
                st.caption("Viral Score")

            st.divider()

            # Tabs for different outputs
            t1, t2, t3, t4, t5 = st.tabs(["📝 Script", "🪝 Engagement", "🏷️ Metadata", "🎨 Visuals", "📊 Analysis"])
            
            with t1:
                st.markdown("#### Full Script")
                script_data = st.session_state.state['script'].model_dump() if st.session_state.state['script'] else {}
                script_text = st.text_area("Edit Script", script_data.get('full_text', ''), height=300)
                st.button("📋 Copy Script", on_click=lambda: st.write("Copied!")) # Real copy would use JS or pyperclip
                
            with t2:
                st.markdown("#### Hook Variations")
                st.info(f"**Strategy:** {hook_type}")
                hook_data = st.session_state.state['hook'].model_dump() if st.session_state.state['hook'] else {}
                hook_text = st.text_input("Primary Hook", hook_data.get('hook_text', ''))
                st.markdown(f"**Visual Cue:** {hook_data.get('visual_cue', 'N/A')}")
                st.divider()
                st.markdown("#### Call to Action")
                cta_data = st.session_state.state['cta'].model_dump() if st.session_state.state['cta'] else {}
                st.success(cta_data.get('text', 'Follow for more!'))

            with t3:
                st.markdown("#### Optimized Captions")
                caption_data = st.session_state.state['caption'].model_dump() if st.session_state.state['caption'] else {}
                st.text_area("Caption", caption_data.get('primary_text', ''), height=100)
                st.markdown("#### Trending Hashtags")
                hashtags_data = st.session_state.state['hashtags'].model_dump() if st.session_state.state['hashtags'] else {}
                tags = " ".join([f"#{t}" for t in hashtags_data.get('tags', [])])
                st.code(tags, language="text")

            with t4:
                st.markdown("#### Thumbnail Strategy")
                thumbnail_data = st.session_state.state['thumbnail'].model_dump() if st.session_state.state['thumbnail'] else {}
                t_concept = thumbnail_data.get('prompt', 'A cinematic view of AI...')
                st.markdown(f"<div class='output-tab'>{t_concept}</div>", unsafe_allow_html=True)
                
                if st.button("🔄 Regenerate Concept"):
                    with st.spinner("Reimagining..."):
                        # Logic to regenerate just thumbnail
                        pass
                
                # Placeholder for Image
                st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800", caption="Preview Placeholder (Visual Style: " + visual + ")")

            with t5:
                st.markdown("#### Virality Insights")
                res = st.session_state.state['viral_score'].model_dump() if st.session_state.state['viral_score'] else {}
                
                s_col1, s_col2 = st.columns(2)
                with s_col1:
                    st.markdown("**✅ Strengths**")
                    for s in res.get('strengths', ['Strong hook']):
                        st.markdown(f"- {s}")
                with s_col2:
                    st.markdown("**⚠️ Improvements**")
                    for w in res.get('weaknesses', ['N/A']):
                        st.markdown(f"- {w}")
                
                st.divider()
                st.markdown("#### 💡 Optimization Tips")
                st.info("Try adding a controversial statement in the first 3 seconds to boost retention.")

            st.divider()
            if st.button("💾 Save to Asset Library", use_container_width=True):
                try:
                    ProjectService.create_project(st.session_state.user_id, {
                        "project_name": topic,
                        "platform": platform,
                        "state": st.session_state.state
                    })
                    st.toast("Project saved to Asset Library!")
                except Exception as e:
                    st.error(f"Save failed: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Welcome Screen
            st.markdown("""
            <div style='text-align: center; padding: 100px 20px;'>
                <h1 style='font-size: 3.5rem; opacity: 0.1;'>STUDIO PRO</h1>
                <p style='opacity: 0.5; font-size: 1.2rem;'>Configure your project settings on the left to start generating viral assets.</p>
                <img src='https://img.icons8.com/fluency/144/ai.png' style='opacity: 0.2; margin-top: 20px;' />
            </div>
            """, unsafe_allow_html=True)

# --- Settings Page ---
elif page == "🛠️ Config":
    st.title("🛠️ System Configuration")
    
    st.markdown("<div class='creator-card'>", unsafe_allow_html=True)
    st.subheader("🤖 AI Model Settings")
    
    # Model Selection
    model_options = [
        "gemini-1.5-flash", 
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro", 
        "gemini-1.0-pro",
        "gemini-pro",
        "gemini-2.0-flash-exp" # Latest experimental
    ]
    current_model = getattr(gemini_service, 'model_name', "gemini-1.5-flash")
    selected_model = st.selectbox("Gemini Model", model_options, index=model_options.index(current_model) if current_model in model_options else 0)
    
    # API Key
    current_key = getattr(gemini_service, 'api_key', "")
    gemini_key = st.text_input("Gemini API Key", value=current_key if current_key else os.getenv("GEMINI_API_KEY", ""), type="password")
    
    st.divider()
    st.subheader("💾 Persistence Settings")
    mongo_uri = st.text_input("MongoDB URI", value=os.getenv("MONGO_URI", ""), type="password")
    
    if st.button("💾 Save & Apply Settings", use_container_width=True):
        try:
            # Reconfigure AI Service
            gemini_service.reconfigure(api_key=gemini_key, model_name=selected_model)
            st.success(f"AI Configuration Updated: {selected_model}")
            st.toast("Settings applied successfully!")
        except Exception as e:
            st.error(f"Failed to update settings: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- Other Pages ---
elif page == "📁 Asset Library":
    st.title("📂 Asset Library")
    st.markdown("Manage and refine your generated social media assets.")
    
    projects = ProjectService.get_user_projects(st.session_state.user_id)
    
    if not projects['items']:
        st.info("Your library is empty. Head to the Studio to generate your first asset!")
    else:
        # Display as a grid
        cols = st.columns(2)
        for i, project in enumerate(projects['items']):
            with cols[i % 2]:
                st.markdown(f"""
                <div class='creator-card'>
                    <h4 style='margin:0;'>{project['project_name']}</h4>
                    <p style='font-size: 0.8rem; opacity: 0.6;'>{project['platform']} • {str(project.get('created_at', ''))[:10]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔍 View Details"):
                    st.write(f"**Hook:** {project['state'].get('hook', {}).get('hook_text', 'N/A')}")
                    st.divider()
                    st.write(project['state'].get('script', {}).get('full_text', ''))
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("♻️ Load to Studio", key=f"load_{project['_id']}", use_container_width=True):
                            st.session_state.state = project['state']
                            st.session_state.current_project_id = project['_id']
                            st.toast("Project loaded into Studio!")
                            st.rerun()
                    with c2:
                        if st.button("🗑️ Delete", key=f"del_{project['_id']}", use_container_width=True):
                            ProjectService.delete_project(st.session_state.user_id, project['_id'])
                            st.rerun()
                st.write("") # Spacer
elif page == "📊 Insights":
    st.title("📊 Content Insights")
    # Implementation of analytics
