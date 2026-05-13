import streamlit as st
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to allow imports from 'app'
sys.path.append(str(Path(__file__).parent))

from app.analytics.analytics_engine import AnalyticsEngine
from app.utils.error_handler import ErrorHandler, GeminiError
from app.utils.helpers import LoadingState

# Set page config
st.set_page_config(
    page_title="Viral Analytics Studio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        border-color: #00d2ff;
    }
    
    .score-meter {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(to right, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .strength-item {
        color: #00ff88;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    
    .weakness-item {
        color: #ff4b2b;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    
    .recommendation-item {
        color: #ffca28;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    
    .sidebar .stButton button {
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Engine
analytics = AnalyticsEngine()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rocket.png", width=80)
    st.title("Settings")
    platform = st.selectbox("Platform", ["YouTube Shorts", "TikTok", "Instagram Reels"])
    st.divider()
    st.markdown("### 🏷️ Hashtags")
    hashtag_input = st.text_input("Enter hashtags (comma separated)", "viral, coding, ai")
    hashtags = [h.strip() for h in hashtag_input.split(",")]

# Main Content
st.title("📈 Viral Analytics Engine")
st.markdown("Optimize your content for maximum reach and engagement.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Content Input")
    hook = st.text_area("Hook / Headline", "You won't believe how easy it is to build AI agents with this secret trick!", height=100)
    script = st.text_area("Full Script", "I tried every single framework out there and finally found the ultimate shortcut. Stop wasting time on complex setups. Link in bio for the full guide!", height=250)
    
    if st.button("🚀 Analyze Content", use_container_width=True):
        try:
            with LoadingState("Analyzing virality patterns..."):
                if not hook or not script:
                    raise GeminiError("Hook and Script cannot be empty!")
                results = analytics.analyze_content(hook, script, hashtags, platform)
                st.session_state.analysis_results = results
                st.success("Analysis Complete!")
        except Exception as e:
            ErrorHandler.handle(e, context="Analyze Button")

with col2:
    if "analysis_results" in st.session_state:
        results = st.session_state.analysis_results
        
        # Viral Score Section
        st.markdown(f"""
        <div class="metric-card">
            <h3 style='text-align: center;'>Viral Potential Score</h3>
            <div class="score-meter">{results['viral_score']}/100</div>
            <p style='text-align: center; font-weight: 600; color: #00d2ff;'>{results['label']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Breakdown Cards
        m_col1, m_col2 = st.columns(2)
        
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <p style='margin:0; opacity: 0.7;'>Hook Strength</p>
                <h4 style='margin:0;'>{results['metrics']['engagement']['hook_strength']}%</h4>
            </div>
            """, unsafe_allow_html=True)
            
        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <p style='margin:0; opacity: 0.7;'>Readability</p>
                <h4 style='margin:0;'>{results['metrics']['readability']['score']}%</h4>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        
        # Detailed Feedback
        tab1, tab2, tab3 = st.tabs(["✅ Strengths", "⚠️ Improvement Areas", "💡 Recommendations"])
        
        with tab1:
            for s in results['strengths']:
                st.markdown(f"<div class='strength-item'>✅ {s}</div>", unsafe_allow_html=True)
                
        with tab2:
            for w in results['weaknesses']:
                st.markdown(f"<div class='weakness-item'>⚠️ {w}</div>", unsafe_allow_html=True)
            if not results['weaknesses']:
                st.info("No major weaknesses found. Looking good!")
                
        with tab3:
            for r in results['recommendations']:
                st.markdown(f"<div class='recommendation-item'>💡 {r}</div>", unsafe_allow_html=True)
    else:
        st.info("Enter your content and click 'Analyze' to see results.")

# Footer
st.divider()
st.markdown("<p style='text-align: center; opacity: 0.5;'>AI Creator Studio - Senior Analytics Engine v1.0</p>", unsafe_allow_html=True)
