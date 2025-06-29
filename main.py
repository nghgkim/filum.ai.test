import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("kb/features.json", "r", encoding="utf-8") as f:
    feature_kb = json.load(f)

with open("examples/input.json", "r", encoding="utf-8") as f:
    input_data = json.load(f)

pain_point = input_data["pain_point"]
context = input_data.get("context", {})
tags = input_data.get("tags", [])

input_vector = model.encode(pain_point)

results = []

for feature in feature_kb:
    text = feature["description"] + " " + " ".join(feature.get("tags", []))
    feature_vector = model.encode(text)
    similarity = cosine_similarity([input_vector], [feature_vector])[0][0]

    feature_tags = set(feature.get("tags", []))
    input_tags = set(tags)
    tag_score = len(feature_tags & input_tags) / len(feature_tags) if feature_tags else 0

    context_score = 0
    if context.get("department") in feature.get("use_cases", []):
        context_score += 0.05
    if any(chan in feature.get("channels_supported", []) for chan in context.get("channel_focus", [])):
        context_score += 0.05

    final_score = 0.7 * similarity + 0.2 * tag_score + 0.1 * context_score

    results.append({
        "feature_name": feature["feature_name"],
        "product_category": feature["product_category"],
        "description": feature["description"],
        "how_it_helps": feature["description"],
        "relevance_score": float(round(final_score, 3)),
        "more_info_url": feature["more_info_url"]
    })

results.sort(key=lambda x: x["relevance_score"], reverse=True)
print(json.dumps(results[:1], indent=2))