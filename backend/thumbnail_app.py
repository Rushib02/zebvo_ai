import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from app.thumbnail.thumbnail_service import ThumbnailService
from PIL import Image

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Creator Studio - Thumbnail Lab", layout="wide")

def run_async(coro):
    return asyncio.run(coro)

# Initialize Service
thumbnail_service = ThumbnailService()

st.title("🎨 AI Thumbnail Lab")
st.markdown("Generate cinematic, high-CTR thumbnails using Gemini Imagen 4.0")

# Input Section
with st.sidebar:
    st.header("Project Settings")
    project_id = st.text_input("Project ID", value="test_project_001")
    script_text = st.text_area("Video Script", placeholder="Enter your video script here to generate a matching thumbnail...")

# Main UI
if st.button("🚀 Generate Thumbnail", use_container_width=True):
    if not script_text:
        st.warning("Please enter a script first!")
    else:
        with st.spinner("Gemini is imagining your thumbnail..."):
            try:
                # Generate
                result = run_async(thumbnail_service.create_thumbnail(project_id, script_text))
                
                # Success UI
                st.success("Thumbnail generated successfully!")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("Preview")
                    image = Image.open(result["image_path"])
                    st.image(image, use_column_width=True, caption="Generated Thumbnail")
                    
                with col2:
                    st.subheader("Metadata")
                    st.info(f"**Project:** {result['project_id']}")
                    st.write(f"**Prompt Used:**\n{result['image_prompt']}")
                    
                    # Download Button
                    with open(result["image_path"], "rb") as file:
                        btn = st.download_button(
                            label="📥 Download Thumbnail",
                            data=file,
                            file_name=os.path.basename(result["image_path"]),
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # Regenerate
                    if st.button("🔄 Regenerate", use_container_width=True):
                        st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

# History Section (Optional but good for demo)
st.divider()
st.subheader("📜 Recent Thumbnails")
# We could fetch from MongoDB here if needed
if os.path.exists("generated/thumbnails"):
    files = sorted(os.listdir("generated/thumbnails"), key=lambda x: os.path.getmtime(os.path.join("generated/thumbnails", x)), reverse=True)
    if files:
        cols = st.columns(4)
        for i, file in enumerate(files[:8]):
            with cols[i % 4]:
                img_path = os.path.join("generated/thumbnails", file)
                st.image(img_path, use_column_width=True)
    else:
        st.info("No thumbnails generated yet.")
