from app.analytics.analytics_utils import (
    count_emotional_words, 
    has_cta, 
    check_hook_strength,
    get_word_count
)

class EngagementAnalyzer:
    """
    Analyzes hook strength, emotional density, and CTA effectiveness.
    """
    
    def analyze(self, hook: str, script: str, hashtags: list) -> dict:
        # 1. Hook Analysis
        hook_results = check_hook_strength(hook)
        
        # 2. Emotional Density
        # We analyze both hook and script for emotional triggers
        combined_text = f"{hook} {script}"
        emotional_counts = count_emotional_words(combined_text)
        total_emotional_words = sum(emotional_counts.values())
        
        # 3. CTA Effectiveness
        cta_present = has_cta(script)
        
        # 4. Hashtag Quality
        hashtag_score = 0
        if 3 <= len(hashtags) <= 6:
            hashtag_score = 100
        elif 1 <= len(hashtags) < 3:
            hashtag_score = 60
        elif len(hashtags) > 6:
            hashtag_score = 40 # Avoid over-tagging
            
        return {
            "hook_strength": hook_results["score"],
            "hook_triggers": hook_results["triggers"],
            "emotional_density": total_emotional_words,
            "emotional_breakdown": emotional_counts,
            "cta_present": cta_present,
            "hashtag_score": hashtag_score,
            "total_hashtags": len(hashtags)
        }
