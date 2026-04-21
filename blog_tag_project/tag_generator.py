import random

categories = {
    "food": ["#food", "#yummy", "#tasty", "#recipe", "#foodie", "#delicious"],
    "travel": ["#travel", "#explore", "#adventure", "#trip", "#wanderlust"],
    "fitness": ["#fitness", "#gym", "#workout", "#health", "#fitlife"],
    "technology": ["#technology", "#ai", "#coding", "#innovation", "#tech"],
    "education": ["#education", "#learning", "#study", "#student", "#knowledge"],
    "beauty": ["#beauty", "#makeup", "#skincare", "#glow", "#selfcare"],
    "business": ["#business", "#startup", "#entrepreneur", "#success", "#money"]
}

topics = [
    "food recipe ideas",
    "travel vlog",
    "gym workout",
    "AI future technology",
    "online learning tips",
    "beauty skincare routine",
    "startup business ideas"
]

data = []

for i in range(1000):
    topic = random.choice(topics)
    category = random.choice(list(categories.keys()))
    tags = " ".join(random.sample(categories[category], 5))

    data.append(f"{topic},{category},{tags}")

# Save file
with open("tags_dataset.csv", "w") as f:
    for row in data:
        f.write(row + "\n")

print("✅ 100000000+ tags generated!")

