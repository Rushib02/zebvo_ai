import sys
from pathlib import Path

# Add backend/ to path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from app.analytics.analytics_engine import AnalyticsEngine

def test_engine():
    engine = AnalyticsEngine()
    
    # Test case 1: High quality viral content
    hook = "Stop wasting hours on coding! This hidden secret will change everything."
    script = "I found the ultimate hack for developers. It's shockingly simple. Click the link in bio to learn more."
    hashtags = ["coding", "hack", "secret", "ai"]
    
    print("--- Testing High Quality Content ---")
    results = engine.analyze_content(hook, script, hashtags, "TikTok")
    print(f"Viral Score: {results['viral_score']}")
    print(f"Label: {results['label']}")
    print(f"Strengths: {results['strengths']}")
    print(f"Recommendations: {results['recommendations']}")
    print("\n")
    
    # Test case 2: Low quality content
    hook = "Hello world"
    script = "This is a video about coding. I hope you like it. It is long and boring and has no emotion at all."
    hashtags = []
    
    print("--- Testing Low Quality Content ---")
    results = engine.analyze_content(hook, script, hashtags, "Instagram Reels")
    print(f"Viral Score: {results['viral_score']}")
    print(f"Label: {results['label']}")
    print(f"Strengths: {results['strengths']}")
    print(f"Recommendations: {results['recommendations']}")

if __name__ == "__main__":
    test_engine()
