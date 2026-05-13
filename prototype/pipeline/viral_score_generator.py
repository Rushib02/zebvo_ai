"""
Rule-based viral score analyser.

Scores the generated content on a 0-100 scale using lightweight
heuristics — no AI call required.
"""

import re

# ── Word lists ─────────────────────────────────────────────────────────────────

EMOTIONAL_WORDS = [
    "secret", "hidden", "shocking", "revealed", "truth", "unbelievable",
    "insane", "mind-blowing", "never", "always", "dead", "alive", "finally",
    "broke", "destroyed", "changed", "real", "fake", "scam", "expose",
    "danger", "urgent", "alert", "warning", "incredible", "exclusive",
]

CTA_PHRASES = [
    "subscribe", "follow", "like", "share", "comment", "click", "watch",
    "check out", "join", "save", "download", "dm", "link in bio", "tap",
]

HOOK_POWER_WORDS = [
    "you", "your", "i", "we", "imagine", "what if", "did you know",
    "stop", "wait", "before", "why", "how", "the truth", "nobody talks",
]

ENGAGEMENT_KEYWORDS = [
    "viral", "trending", "breaking", "exclusive", "first", "only",
    "proven", "science", "study", "data", "expert", "billion", "million",
]


def _count_hits(text: str, word_list: list[str]) -> int:
    text_lower = text.lower()
    return sum(1 for w in word_list if w in text_lower)


def run(hook: str, script: str, cta: str) -> dict:
    combined = f"{hook} {script} {cta}"

    # Scoring components (each out of defined max)
    emotional   = min(_count_hits(combined, EMOTIONAL_WORDS), 10)   # max 10 → 25 pts
    cta_score   = min(_count_hits(cta, CTA_PHRASES),           5)   # max 5  → 20 pts
    hook_power  = min(_count_hits(hook, HOOK_POWER_WORDS),     8)   # max 8  → 30 pts
    engagement  = min(_count_hits(combined, ENGAGEMENT_KEYWORDS), 6) # max 6  → 25 pts

    # Normalise to 100
    score = round(
        (emotional  / 10 * 25) +
        (cta_score  /  5 * 20) +
        (hook_power /  8 * 30) +
        (engagement /  6 * 25),
        1
    )

    # Qualitative label
    if score >= 80:
        label = "🔥 HIGHLY VIRAL"
    elif score >= 60:
        label = "⚡ GOOD POTENTIAL"
    elif score >= 40:
        label = "📈 AVERAGE"
    else:
        label = "📉 NEEDS WORK"

    # Identify strengths & weaknesses
    strengths   = []
    weaknesses  = []

    if emotional >= 5:
        strengths.append("Strong emotional language")
    else:
        weaknesses.append("Needs more emotional power words")

    if cta_score >= 3:
        strengths.append("Clear call-to-action")
    else:
        weaknesses.append("Weak or missing CTA")

    if hook_power >= 4:
        strengths.append("Compelling hook structure")
    else:
        weaknesses.append("Hook needs more direct address (you/your/what if)")

    if engagement >= 3:
        strengths.append("Good engagement trigger keywords")
    else:
        weaknesses.append("Add trend/urgency keywords to boost reach")

    return {
        "score":      score,
        "label":      label,
        "strengths":  strengths,
        "weaknesses": weaknesses,
        "breakdown": {
            "emotional_words":    emotional,
            "cta_strength":       cta_score,
            "hook_power":         hook_power,
            "engagement_keywords": engagement,
        },
    }
