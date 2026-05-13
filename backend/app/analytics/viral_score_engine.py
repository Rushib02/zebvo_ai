class ViralScoreEngine:
    """
    Calculates a final virality score and provides qualitative feedback.
    """
    
    def calculate(self, readability_data: dict, engagement_data: dict, platform: str) -> dict:
        score = 45  # Starting base score for "Average" content
        strengths = []
        weaknesses = []
        recommendations = []
        
        # 1. Emotional Trigger Scoring (+10)
        if engagement_data["emotional_density"] > 0:
            score += 10
            strengths.append("High emotional resonance with power words.")
        else:
            weaknesses.append("Content feels a bit dry.")
            recommendations.append("Add emotional triggers like 'amazing', 'shocking', or 'secret'.")
            
        # 2. CTA Scoring (+10)
        if engagement_data["cta_present"]:
            score += 10
            strengths.append("Clear Call-to-Action (CTA) included.")
        else:
            weaknesses.append("No clear next step for the viewer.")
            recommendations.append("Add a CTA like 'Comment below' or 'Follow for more'.")
            
        # 3. Readability Scoring (+5)
        if readability_data["avg_sentence_length"] < 18:
            score += 5
            strengths.append("Excellent pacing with punchy, short sentences.")
        elif readability_data["avg_sentence_length"] > 25:
            score -= 10
            weaknesses.append("Sentences are too long for quick consumption.")
            recommendations.append("Break down complex sentences into smaller, 5-10 word segments.")
            
        # 4. Hook Strength (+15)
        if engagement_data["hook_strength"] >= 30: # Based on our check_hook_strength logic
            score += 15
            strengths.append("Powerful 'Scroll-Stopping' hook.")
        else:
            score -= 5
            weaknesses.append("The hook might not grab attention fast enough.")
            recommendations.append("Start with a strong curiosity trigger or a bold claim.")
            
        # 5. Hashtag Optimization (+5 bonus)
        if engagement_data["hashtag_score"] == 100:
            score += 5
            strengths.append("Optimized hashtag count.")
        elif engagement_data["hashtag_score"] < 50:
            recommendations.append("Aim for 3-5 relevant hashtags.")
            
        # Final Score Capping
        score = min(100, max(0, score))
        
        # Determine Label
        if score >= 85:
            label = "Viral Potential"
        elif score >= 65:
            label = "Strong Content"
        elif score >= 40:
            label = "Average"
        else:
            label = "Needs Work"
            
        return {
            "score": score,
            "label": label,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }
