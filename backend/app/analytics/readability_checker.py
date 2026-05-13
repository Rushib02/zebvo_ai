from app.analytics.analytics_utils import get_sentence_count, get_word_count, clean_text

class ReadabilityChecker:
    """
    Analyzes content readability and skimmability for social media.
    """
    
    def check(self, text: str) -> dict:
        text = clean_text(text)
        if not text:
            return self._get_empty_result()
            
        word_count = get_word_count(text)
        sentence_count = get_sentence_count(text)
        
        # Average sentence length (Lightweight readability metric)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Social media optimization: Short sentences are better
        # 1-15 words: Great
        # 15-25 words: Average
        # 25+: Poor
        
        readability_score = 100
        feedback = []
        
        if avg_sentence_length > 25:
            readability_score -= 30
            feedback.append("Sentences are quite long. Try breaking them up for better flow.")
        elif avg_sentence_length > 15:
            readability_score -= 10
            feedback.append("Readability is decent, but some sentences could be punchier.")
        else:
            feedback.append("Excellent sentence pacing!")
            
        # Paragraph/Skimmability check
        # For simplicity, we'll just check if the total word count is within a "scrolling" friendly range
        if word_count > 150:
            readability_score -= 10
            feedback.append("Content is a bit long for a short-form video. Consider trimming.")
            
        return {
            "score": max(0, readability_score),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "word_count": word_count,
            "feedback": feedback
        }
        
    def _get_empty_result(self):
        return {
            "score": 0,
            "avg_sentence_length": 0,
            "word_count": 0,
            "feedback": ["No content provided"]
        }
