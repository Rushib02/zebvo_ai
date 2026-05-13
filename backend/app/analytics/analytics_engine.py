import logging
from app.analytics.viral_score_engine import ViralScoreEngine
from app.analytics.engagement_analyzer import EngagementAnalyzer
from app.analytics.readability_checker import ReadabilityChecker

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    def __init__(self):
        self.score_engine = ViralScoreEngine()
        self.engagement = EngagementAnalyzer()
        self.readability = ReadabilityChecker()

    def analyze_content(self, hook: str, script: str, hashtags: list, platform: str = "YouTube Shorts"):
        """
        Runs the full analytics suite on the generated content.
        """
        try:
            # 1. Individual Analysis
            readability_data = self.readability.check(script)
            engagement_data = self.engagement.analyze(hook, script, hashtags)
            
            # 2. Calculate Final Score
            score_data = self.score_engine.calculate(
                readability_data, 
                engagement_data, 
                platform
            )
            
            return {
                "viral_score": score_data["score"],
                "label": score_data["label"],
                "strengths": score_data["strengths"],
                "weaknesses": score_data["weaknesses"],
                "recommendations": score_data["recommendations"],
                "metrics": {
                    "readability": readability_data,
                    "engagement": engagement_data
                }
            }
            
        except Exception as e:
            logger.error(f"Analytics engine failure: {str(e)}")
            return self._get_fallback_response()

    def _get_fallback_response(self):
        return {
            "viral_score": 0,
            "label": "Error",
            "strengths": [],
            "weaknesses": ["Analysis failed"],
            "recommendations": ["Ensure content is valid"]
        }
