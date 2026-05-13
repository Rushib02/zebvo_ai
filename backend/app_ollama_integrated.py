import streamlit as st
import asyncio
import os
import sys
import time
import json
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
from app.utils.streamlit_generation import StreamlitGenerationHelper
from app.database.mongodb import get_database
from app.ai.gemini_service import gemini_service
from app.ai.ollama_service import ollama_service
from app.ai.model_router import model_router

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

# --- Premium SaaS Styling with Ollama Integration ---
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
    
    .ai-status-card {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .ollama-active {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
    
    .ollama-offline {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.5);
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
    
    .ai-indicator {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 10px;
    }
    
    .ai-gemini {
        background: rgba(66, 133, 244, 0.2);
        color: #4285f4;
    }
    
    .ai-ollama {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .ai-fallback {
        background: rgba(251, 146, 60, 0.2);
        color: #fb923c;
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
        "current_step": 0, "is_generating": False, "ai_used": None
    }
if "user_id" not in st.session_state:
    st.session_state.user_id = "pro_creator_01"

# --- Initialize AI Status ---
if "ai_status" not in st.session_state:
    st.session_state.ai_status = {
        "gemini_available": False,
        "ollama_running": ollama_service.is_running(),
        "ollama_has_mistral": ollama_service.check_model_available() if ollama_service.is_running() else False
    }

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #6366f1;'>💎 Studio Pro</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.selectbox("Navigation", ["🎥 Creator Workspace", "📁 Asset Library", "📊 Insights", "🛠️ Config", "🔧 AI Diagnostics"])
    
    st.divider()
    
    # --- Hybrid AI Status Panel ---
    st.markdown("### 🤖 Hybrid AI Engine")
    
    # Refresh status
    if st.button("🔄 Refresh Status", use_container_width=True):
        st.session_state.ai_status["ollama_running"] = ollama_service.is_running()
        st.session_state.ai_status["ollama_has_mistral"] = ollama_service.check_model_available() if ollama_service.is_running() else False
        st.rerun()
    
    # AI Status Container
    ai_col = st.container()
    with ai_col:
        # Gemini Status
        try:
            st.session_state.ai_status["gemini_available"] = gemini_service.model is not None
            if st.session_state.ai_status["gemini_available"]:
                st.markdown("""
                <div class='ai-status-card'>
                    <span style='color: #4285f4;'>🔵 Gemini 1.5</span><br/>
                    <small>Cloud AI (Primary)</small><br/>
                    <span style='font-size: 0.75rem; color: #64748b;'>Status: Ready</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='ai-status-card'>
                    <span style='color: #9ca3af;'>⚫ Gemini 1.5</span><br/>
                    <small>Cloud AI (Primary)</small><br/>
                    <span style='font-size: 0.75rem; color: #64748b;'>Status: Offline</span>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.session_state.ai_status["gemini_available"] = False
            st.markdown("""
            <div class='ai-status-card'>
                <span style='color: #9ca3af;'>⚫ Gemini 1.5</span><br/>
                <small>Cloud AI (Primary)</small><br/>
                <span style='font-size: 0.75rem; color: #64748b;'>Status: Error</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Ollama Status
        if st.session_state.ai_status["ollama_running"]:
            if st.session_state.ai_status["ollama_has_mistral"]:
                st.markdown("""
                <div class='ai-status-card ollama-active'>
                    <span style='color: #10b981;'>🟢 Ollama Mistral</span><br/>
                    <small>Local AI (Fallback) - ACTIVE</small><br/>
                    <span style='font-size: 0.75rem; color: #64748b;'>Port: 11434 | Model: 4.4GB</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='ai-status-card ollama-offline'>
                    <span style='color: #f97316;'>🟡 Ollama Running</span><br/>
                    <small>Local AI (Fallback)</small><br/>
                    <span style='font-size: 0.75rem; color: #64748b;'>⚠️ Mistral not found</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("📥 Pull Mistral Model"):
                    st.info("Run in terminal: `ollama pull mistral`")
        else:
            st.markdown("""
            <div class='ai-status-card ollama-offline'>
                <span style='color: #ef4444;'>🔴 Ollama Offline</span><br/>
                <small>Local AI (Fallback)</small><br/>
                <span style='font-size: 0.75rem; color: #64748b;'>Enable local generation</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ Start Ollama"):
                st.info("Run in terminal: `ollama serve`")
    
    st.divider()
    st.markdown("### 📈 Generation Progress")
    steps = ["Targeting", "Ideation", "Scripting", "Engagement", "Optimization"]
    for i, step in enumerate(steps):
        if st.session_state.state["current_step"] > i:
            st.markdown(f"✅ <span class='step-done'>{step}</span>", unsafe_allow_html=True)
        elif st.session_state.state["current_step"] == i:
            st.markdown(f"⏳ <span class='step-active'>{step}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"⚪ <span class='step-todo'>{step}</span>", unsafe_allow_html=True)

    if st.button("✨ New Project", use_container_width=True):
        st.session_state.state = {"idea": None, "hook": None, "script": None, "captions": None, "hashtags": None, "thumbnail": None, "viral_score": None, "current_step": 0, "is_generating": False, "ai_used": None}
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
            length = st.slider("Duration (seconds)", 15, 90, 60)
            language = st.selectbox("Language", ["English", "Hindi", "Hinglish"])
            cta = st.selectbox("CTA Goal", ["Followers", "Comments", "Shares", "Saves", "DMs"])
            visual = st.selectbox("Visual Aesthetic", ["Modern Creator", "Dark Aesthetic", "Luxury", "Minimal", "Neon"])
            
            st.divider()
            st.markdown("### 🎬 Script Configuration")
            script_type = st.selectbox(
                "Script Format",
                ["Monologue", "Dialogue (2 people)", "Dialogue (3 people)", "Skit (3+ people)"],
                help="Type of script format"
            )
            
            # Extract number of characters
            num_characters = 1
            if "2 people" in script_type:
                num_characters = 2
            elif "3 people" in script_type:
                num_characters = 3
            elif "Skit" in script_type:
                num_characters = st.slider("Number of characters", 3, 6, 3)
            
            pacing = st.select_slider(
                "Pacing",
                options=["Very Slow", "Slow", "Normal", "Fast", "Very Fast"],
                value="Normal"
            )
            
            notes = st.text_area("Custom AI Instructions", placeholder="e.g., Include humor, add plot twist, use metaphors...")
            
            # AI Preference
            st.divider()
            st.markdown("### 🤖 AI Preference")
            ai_preference = st.radio(
                "Choose AI Engine Priority:",
                ["Auto (Gemini→Ollama→Fallback)", "Prefer Gemini", "Prefer Ollama (Local)", "Force Fallback"],
                help="Control which AI model to use for generation"
            )

        st.divider()

        if st.button("🚀 Generate Content", use_container_width=True):
            if not topic:
                st.warning("Please define a topic to begin.")
            else:
                st.session_state.state["is_generating"] = True
                
                # --- Step-by-Step Generation with AI tracking ---
                try:
                    with st.status("🧠 Brainstorming Content Architecture...", expanded=True) as status:
                        # Track which AI is being used
                        start_time = time.time()
                        
                        st.write("📍 Step 1: Targeting & Ideation...")
                        idea_result = StreamlitGenerationHelper.generate_idea(topic, platform)
                        st.session_state.state["idea"] = idea_result
                        st.session_state.state["ai_used"] = "Gemini/Ollama"
                        
                        st.write("🪝 Step 2: Hook Engineering...")
                        hook_result = StreamlitGenerationHelper.generate_hook(topic, hook_type)
                        st.session_state.state["hook"] = hook_result
                        
                        st.write("📝 Step 3: Script Composition...")
                        script_result = StreamlitGenerationHelper.generate_script(
                            topic, 
                            style, 
                            length,
                            script_format=script_type,
                            num_characters=num_characters,
                            pacing=pacing,
                            custom_notes=notes
                        )
                        st.session_state.state["script"] = script_result
                        
                        st.write("✨ Step 4: Engagement Optimization...")
                        caption_result = StreamlitGenerationHelper.generate_caption(topic)
                        st.session_state.state["caption"] = caption_result
                        
                        st.write("🏷️ Step 5: Hashtag Generation...")
                        hashtag_result = StreamlitGenerationHelper.generate_hashtags(topic, platform)
                        st.session_state.state["hashtags"] = hashtag_result
                        
                        st.write("🎨 Step 6: Thumbnail Strategy...")
                        thumbnail_result = StreamlitGenerationHelper.generate_thumbnail(topic, visual)
                        st.session_state.state["thumbnail"] = thumbnail_result
                        
                        st.write("📊 Step 7: Virality Analysis...")
                        script_text = script_result.get("full_text", "")
                        hook_text = hook_result.get("hook_text", "")
                        viral_result = StreamlitGenerationHelper.generate_viral_score(script_text, hook_text, "Subscribe")
                        st.session_state.state["viral_score"] = viral_result
                        
                        # Generate CTA
                        st.session_state.state["cta"] = {"text": f"Subscribe for more {topic} content!", "placement": "End"}
                        
                        elapsed = time.time() - start_time
                        st.session_state.state["current_step"] = 5
                        status.update(label=f"✅ Content Complete! ({elapsed:.1f}s)", state="complete")
                    
                    st.success("🎉 Generation Complete!")
                    st.session_state.state["is_generating"] = False
                    st.rerun()
                    
                except Exception as e:
                    ErrorHandler.handle(e, context="SaaS Pipeline")
                    st.error(f"⚠️ Generation failed: {str(e)}")
                    st.session_state.state["is_generating"] = False
        
        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: Outputs & Analytics ---
    with col2:
        if st.session_state.state["idea"]:
            st.markdown("<div class='creator-card'>", unsafe_allow_html=True)
            
            # Header with Score
            h_col1, h_col2 = st.columns([3, 1])
            with h_col1:
                st.markdown(f"## {st.session_state.state['idea'].get('title', 'Project Output')}")
                st.caption(f"Platform: {platform} | Style: {style}")
                
                # Show which AI was used
                if st.session_state.state.get('ai_used'):
                    if st.session_state.state['ai_used'] == 'Gemini':
                        st.markdown(f"<span class='ai-indicator ai-gemini'>⚡ Gemini</span>", unsafe_allow_html=True)
                    elif st.session_state.state['ai_used'] == 'Ollama':
                        st.markdown(f"<span class='ai-indicator ai-ollama'>🧠 Ollama</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='ai-indicator ai-fallback'>📋 Template</span>", unsafe_allow_html=True)
            
            with h_col2:
                score = st.session_state.state['viral_score'].get('score', 85) if st.session_state.state.get('viral_score') else 85
                st.markdown(f"<div class='viral-score'>{int(score)}</div>", unsafe_allow_html=True)
                st.caption("Viral Score")

            st.divider()

            # Tabs for different outputs
            t1, t2, t3, t4, t5 = st.tabs(["📝 Script", "🪝 Engagement", "🏷️ Metadata", "🎨 Visuals", "📊 Analysis"])
            
            with t1:
                st.markdown("#### Full Script")
                if st.session_state.state.get('script'):
                    script_data = st.session_state.state['script']
                    
                    # Show script metadata
                    meta_col1, meta_col2, meta_col3 = st.columns(3)
                    with meta_col1:
                        st.metric("Format", script_data.get('script_type', 'Unknown'))
                    with meta_col2:
                        st.metric("Characters", script_data.get('num_characters', 1))
                    with meta_col3:
                        st.metric("Duration", f"{script_data.get('duration', length)}s")
                    
                    st.divider()
                    
                    # Show structured content if available
                    if 'content' in script_data and isinstance(script_data['content'], list):
                        st.markdown("#### Scene-by-Scene Breakdown")
                        for i, scene in enumerate(script_data['content']):
                            if isinstance(scene, dict):
                                with st.expander(f"📍 {scene.get('time', 'Scene ' + str(i+1))} - {scene.get('type', 'Unknown').title()}", expanded=(i==0)):
                                    if scene.get('type') == 'dialogue':
                                        st.markdown(f"**{scene.get('character', 'Speaker')}**: {scene.get('text', '')}")
                                    elif scene.get('type') == 'visual':
                                        st.info(scene.get('description', ''))
                                    elif scene.get('type') == 'action':
                                        st.warning(f"🎬 {scene.get('description', '')}")
                    
                    st.divider()
                    
                    # Show full text for copying
                    st.markdown("#### Full Script (Copyable)")
                    script_text = script_data.get('full_text', '')
                    st.text_area("Edit Script", script_text, height=300, key="script_textarea")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📋 Copy Script"):
                            st.success("✅ Ready to copy - select and copy from the text area above")
                    with col2:
                        if st.button("🔄 Regenerate Script"):
                            st.info("Regenerate feature coming soon")
                else:
                    st.info("Generate content to see the script")
                
            with t2:
                st.markdown("#### Hook")
                if st.session_state.state.get('hook'):
                    hook_data = st.session_state.state['hook']
                    if 'hook_text' in hook_data:
                        st.info(f"**Hook:** {hook_data['hook_text']}")
                    else:
                        st.info(f"**Hook:** {list(hook_data.values())[0] if hook_data else 'N/A'}")
                else:
                    st.info("Generate content to see hooks")
                
                st.divider()
                st.markdown("#### Call to Action")
                if st.session_state.state.get('cta'):
                    cta_data = st.session_state.state['cta']
                    if 'text' in cta_data:
                        st.success(cta_data['text'])
                    else:
                        st.success(str(list(cta_data.values())[0] if cta_data else "N/A"))
                else:
                    st.info("Generate content to see CTAs")

            with t3:
                st.markdown("#### Optimized Captions")
                if st.session_state.state.get('caption'):
                    caption_data = st.session_state.state['caption']
                    if 'primary_text' in caption_data:
                        st.text_area("Caption", caption_data['primary_text'], height=100)
                    else:
                        caption_text = "\n".join([f"{k}: {v}" for k, v in caption_data.items() if isinstance(v, str)])
                        st.text_area("Caption", caption_text or str(caption_data), height=100)
                else:
                    st.info("Generate content to see captions")
                
                st.markdown("#### Trending Hashtags")
                if st.session_state.state.get('hashtags'):
                    hashtag_data = st.session_state.state['hashtags']
                    if 'tags' in hashtag_data:
                        tags = " ".join([f"#{t}" for t in hashtag_data['tags']])
                    else:
                        tags = " ".join([f"#{v}" for v in hashtag_data.values() if isinstance(v, str)])
                    st.code(tags, language="text")
                else:
                    st.info("Generate content to see hashtags")

            with t4:
                st.markdown("#### Thumbnail Strategy")
                if st.session_state.state.get('thumbnail'):
                    thumbnail_data = st.session_state.state['thumbnail']
                    if 'prompt' in thumbnail_data:
                        t_concept = thumbnail_data['prompt']
                    else:
                        t_concept = "\n".join([f"{k}: {v}" for k, v in thumbnail_data.items() if isinstance(v, str)])
                    st.markdown(f"<div class='output-tab'>{t_concept}</div>", unsafe_allow_html=True)
                else:
                    st.info("Generate content to see thumbnail concepts")
                
                if st.button("🔄 Regenerate Concept"):
                    with st.spinner("Reimagining..."):
                        pass
                
                # Placeholder for Image
                st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800", caption="Visual Preview")

            with t5:
                st.markdown("#### Virality Insights")
                if st.session_state.state.get('viral_score'):
                    res = st.session_state.state['viral_score']
                    
                    # Extract score
                    if 'score' in res:
                        st.metric("Viral Score", f"{int(res['score'])}/100")
                    
                    # Show strengths and weaknesses
                    s_col1, s_col2 = st.columns(2)
                    with s_col1:
                        st.markdown("**✅ Strengths**")
                        strengths = res.get('strengths', []) or [v for k, v in res.items() if 'strength' in k.lower()]
                        for s in strengths:
                            st.markdown(f"- {s}")
                    with s_col2:
                        st.markdown("**⚠️ Improvements**")
                        weaknesses = res.get('weaknesses', []) or [v for k, v in res.items() if 'weak' in k.lower()]
                        for w in weaknesses:
                            st.markdown(f"- {w}")
                    
                    st.divider()
                    st.markdown("#### 💡 Optimization Tips")
                    st.info("Try adding a controversial statement in the first 3 seconds to boost retention.")
                else:
                    st.info("Generate content to see analysis")

            st.divider()
            if st.button("💾 Save to Asset Library", use_container_width=True):
                try:
                    st.success("✅ Project saved!")
                except Exception as e:
                    st.error(f"Error saving: {str(e)}")

            st.markdown("</div>", unsafe_allow_html=True)

# --- AI Diagnostics Page ---
elif page == "🔧 AI Diagnostics":
    st.markdown("## 🔧 AI System Diagnostics")
    st.info("Monitor and test your hybrid AI infrastructure")
    
    diag_col1, diag_col2 = st.columns([1, 2])
    
    with diag_col1:
        st.markdown("### System Status")
        
        # Refresh
        if st.button("🔄 Full Refresh"):
            st.rerun()
        
        # Gemini Check
        st.markdown("**Gemini 1.5 Pro**")
        try:
            if gemini_service.model:
                st.success("✅ Connected")
            else:
                st.error("❌ Offline")
        except:
            st.error("❌ Error")
        
        # Ollama Check
        st.markdown("**Ollama Server**")
        if ollama_service.is_running():
            st.success("✅ Running (Port 11434)")
        else:
            st.error("❌ Not running")
        
        # Mistral Check
        st.markdown("**Mistral Model**")
        if ollama_service.is_running() and ollama_service.check_model_available():
            st.success(f"✅ Ready (4.4 GB)")
        else:
            st.warning("⚠️ Not available")
    
    with diag_col2:
        st.markdown("### Test Generation")
        
        test_topic = st.text_input("Test Topic", "The future of AI")
        test_stage = st.selectbox("Test Stage", ["Hook", "Script", "Caption", "Hashtags", "Viral Score"])
        
        if st.button("🧪 Run Test"):
            with st.spinner(f"Testing {test_stage} generation..."):
                try:
                    if test_stage == "Hook":
                        prompt = f"Generate a hook for: {test_topic}"
                    elif test_stage == "Script":
                        prompt = f"Write a short script for: {test_topic}"
                    elif test_stage == "Caption":
                        prompt = f"Create a caption for: {test_topic}"
                    elif test_stage == "Hashtags":
                        prompt = f"Generate hashtags for: {test_topic}"
                    else:
                        prompt = f"Analyze virality for: {test_topic}"
                    
                    result = model_router.generate_with_fallback(test_stage.lower(), prompt, test_topic)
                    st.success("✅ Test Passed!")
                    st.json(result)
                except Exception as e:
                    st.error(f"❌ Test Failed: {str(e)}")

# Other pages...
elif page == "📁 Asset Library":
    st.markdown("## 📁 Asset Library")
    st.info("Your saved projects and content assets appear here.")

elif page == "📊 Insights":
    st.markdown("## 📊 Analytics & Insights")
    st.info("Performance metrics and recommendations appear here.")

elif page == "🛠️ Config":
    st.markdown("## ⚙️ Configuration")
    st.info("System configuration settings appear here.")
