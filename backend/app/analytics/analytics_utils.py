import re

# Curated list of emotional triggers and power words
EMOTIONAL_KEYWORDS = {
    "urgency": ["now", "fast", "limited", "hurry", "quick", "instantly", "today", "deadline"],
    "curiosity": ["secret", "hidden", "revealed", "unknown", "unusual", "shocking", "surprising", "mystery"],
    "desire": ["perfect", "amazing", "ultimate", "best", "luxury", "success", "proven", "guaranteed"],
    "fear": ["stop", "avoid", "danger", "warning", "risk", "scary", "mistake", "wrong"],
    "trust": ["certified", "expert", "official", "proven", "reliable", "secure", "honest"]
}

# Engagement/Power words for hooks
HOOK_TRIGGERS = [
    "imagine", "if you", "how to", "why you", "stop", "don't", "the truth about",
    "i tried", "this is why", "you won't believe", "hack", "cheat code"
]

# CTA Patterns
CTA_PATTERNS = [
    r"(?i)link in bio",
    r"(?i)comment below",
    r"(?i)subscribe",
    r"(?i)follow for more",
    r"(?i)click here",
    r"(?i)check out",
    r"(?i)share this",
    r"(?i)let me know"
]

def clean_text(text: str) -> str:
    """Cleans text for analysis."""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_sentence_count(text: str) -> int:
    """Estimates sentence count."""
    if not text:
        return 0
    # Split by common sentence terminators
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def get_word_count(text: str) -> int:
    """Estimates word count."""
    if not text:
        return 0
    return len(text.split())

def count_emotional_words(text: str) -> dict:
    """Counts occurrences of emotional triggers."""
    text = text.lower()
    counts = {category: 0 for category in EMOTIONAL_KEYWORDS}
    
    for category, words in EMOTIONAL_KEYWORDS.items():
        for word in words:
            if re.search(rf'\b{word}\b', text):
                counts[category] += 1
                
    return counts

def has_cta(text: str) -> bool:
    """Checks if a CTA is present in the text."""
    for pattern in CTA_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def check_hook_strength(hook: str) -> dict:
    """Analyzes hook strength based on triggers."""
    hook_lower = hook.lower()
    score = 0
    found_triggers = []
    
    for trigger in HOOK_TRIGGERS:
        if trigger in hook_lower:
            score += 20
            found_triggers.append(trigger)
            
    # Length check (hooks should be punchy)
    word_count = get_word_count(hook)
    if 5 <= word_count <= 15:
        score += 10
        
    return {
        "score": min(score, 100),
        "triggers": found_triggers,
        "word_count": word_count
    }
