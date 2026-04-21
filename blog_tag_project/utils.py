import re

# -------------------------
# CLEAN TEXT
# -------------------------
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# -------------------------
# SMART SUMMARY (EXTRACTIVE STYLE)
# -------------------------
def get_summary(text, max_sentences=2):
    text = clean_text(text)

    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    if len(sentences) <= max_sentences:
        return text

    # score sentences by word importance
    word_freq = {}

    for word in text.lower().split():
        word = re.sub(r'[^a-zA-Z]', '', word)
        if word:
            word_freq[word] = word_freq.get(word, 0) + 1

    sentence_scores = {}

    for sentence in sentences:
        score = 0
        for word in sentence.lower().split():
            word = re.sub(r'[^a-zA-Z]', '', word)
            score += word_freq.get(word, 0)

        sentence_scores[sentence] = score

    # pick top sentences
    ranked = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    summary = ". ".join(ranked[:max_sentences])

    return summary + "."

# -------------------------
# PLATFORM TAGS (SMART VERSION)
# -------------------------
def platform_tags(platform, content=""):
    base_tags = {
        "Instagram": ["#reels", "#viral", "#instagood", "#explore", "#trending"],
        "YouTube": ["#youtube", "#shorts", "#video", "#subscribe", "#trending"],
        "Blog": ["#blog", "#seo", "#contentwriting", "#article", "#writing"]
    }

    tags = base_tags.get(platform, ["#content", "#post"])

    # content-based enhancement
    content = content.lower()

    if "ai" in content or "tech" in content:
        tags += ["#ai", "#technology", "#innovation"]

    if "fitness" in content or "gym" in content:
        tags += ["#fitness", "#health"]

    if "travel" in content:
        tags += ["#travel", "#wanderlust"]

    return " ".join(list(set(tags)))

