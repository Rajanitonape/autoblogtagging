import random
import re

# -------------------------
# CATEGORY KEYWORDS (WEIGHTED VERSION)
# -------------------------
category_keywords = {
    "food": ["food", "recipe", "eat", "dish", "restaurant", "cooking"],
    "travel": ["travel", "trip", "tour", "journey", "vacation"],
    "fitness": ["fitness", "gym", "workout", "exercise"],
    "technology": ["technology", "ai", "coding", "software"],
    "education": ["study", "education", "exam", "college", "school"],
    "beauty": ["beauty", "skincare", "makeup"],
    "business": ["business", "startup", "money"],
    "fashion": ["fashion", "style", "outfit"],
    "health": ["health", "nutrition", "mental"],
    "love": ["love", "relationship", "romance", "couple"],
    "music": ["song", "music", "audio", "lyrics"],
    "laptop": ["laptop", "computer", "pc", "device"],
    "electric": ["electric", "battery", "charger", "power"],
    "trending": ["trending", "viral", "popular"],
    "movies": ["movie", "film", "cinema"],
    "gaming": ["game", "gaming", "pubg", "freefire"],
    "social": ["instagram", "facebook", "whatsapp"],
}

# -------------------------
# TAG DATABASE
# -------------------------
tag_database = {
    "food": ["#food", "#yummy", "#tasty", "#recipe", "#foodie", "#delicious", "#cooking"],
    "travel": ["#travel", "#explore", "#adventure", "#wanderlust", "#vacation"],
    "fitness": ["#fitness", "#gym", "#workout", "#fitlife", "#health"],
    "technology": ["#ai", "#tech", "#coding", "#innovation", "#software"],
    "education": ["#education", "#study", "#learning", "#knowledge"],
    "beauty": ["#beauty", "#makeup", "#skincare", "#glow"],
    "business": ["#startup", "#business", "#success", "#money", "#growth"],
    "fashion": ["#fashion", "#style", "#outfit", "#trending"],
    "health": ["#health", "#wellness", "#nutrition", "#mentalhealth"],
    "love": ["#love", "#couple", "#romance", "#relationship"],
    "music": ["#music", "#song", "#beats", "#lyrics"],
    "laptop": ["#laptop", "#tech", "#gadgets", "#device"],
    "electric": ["#electric", "#battery", "#power", "#energy"],
    "trending": ["#trending", "#viral", "#explorepage", "#reels"],
    "movies": ["#movies", "#cinema", "#film", "#entertainment"],
    "gaming": ["#gaming", "#gamer", "#esports", "#pubg"],
    "social": ["#instagram", "#facebook", "#whatsapp"]
}

# -------------------------
# CLEAN TEXT
# -------------------------
def clean_text(text):
    return re.sub(r'[^a-zA-Z ]', '', text.lower())

# -------------------------
# CATEGORY DETECTION (IMPROVED SCORING)
# -------------------------
def predict_category(text):
    text = clean_text(text)
    scores = {}

    for category, keywords in category_keywords.items():
        score = 0
        for word in keywords:
            if word in text:
                score += len(word)
        scores[category] = score

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "trending"

    return best_category

# -------------------------
# TAG PREDICTION (SMART DYNAMIC VERSION)
# -------------------------
def predict_tags(text):
    original_text = text.lower()
    cleaned_text = clean_text(text)

    category = predict_category(cleaned_text)

    # If category found in database → use predefined tags
    if category in tag_database and category != "trending":
        base_tags = tag_database[category]
        selected = random.sample(base_tags, min(5, len(base_tags)))
        return " ".join(selected)

    # If no proper category match → generate dynamic tags
    words = re.findall(r'\w+', original_text)
    keywords = [word for word in words if len(word) > 3]

    dynamic_tags = [f"#{word}" for word in keywords[:5]]

    if dynamic_tags:
        return " ".join(dynamic_tags)

    return "#trending #viral #explore"

# -------------------------
# OPTIONAL: CONFIDENCE SCORE
# -------------------------
def prediction_confidence(text):
    text = clean_text(text)
    scores = {}

    for category, keywords in category_keywords.items():
        score = sum(1 for word in keywords if word in text)
        scores[category] = score

    best = max(scores, key=scores.get)
    total = sum(scores.values())

    confidence = (scores[best] / total) * 100 if total > 0 else 0

    return round(confidence, 2), best

# -------------------------
# TOPIC GENERATOR
# -------------------------
def generate_topics():
    topics = [
        "AI tools for students",
        "Instagram growth hacks",
        "Healthy lifestyle tips",
        "Best travel destinations in India",
        "Gaming tips for beginners",
        "How to start a startup",
        "Fitness transformation journey",
        "Daily productivity hacks",
        "YouTube content ideas",
        "Digital marketing basics"
    ]

    return [f"{t} #{i}" for i, t in enumerate(topics, start=1)]



