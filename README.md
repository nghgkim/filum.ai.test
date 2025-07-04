# Pain Point to Solution Agent – Prototype

## Project Structure

```
.
├── kb/
│   └── features.json         # Sample feature knowledge base
├── examples/
│   └── input.json            # Example pain point input
├── main.py                   # Core matching logic
├── README.md                 # This file
```

---

## How to Run

### 1. Install Requirements

Install dependencies:

```bash
pip install -U sentence-transformers scikit-learn
```

### 2. Run the Prototype

```bash
python main.py
```

This script will:
- Load the feature KB (`kb/features.json`)
- Load the input pain point (`examples/input.json`)
- Compute similarity using embeddings + tags + context
- Output the top most relevant Filum.ai features in JSON format

---

## Sample Output

```json
[
  {
    "feature_name": "AI Agent for FAQ & First Response",
    "product_category": "AI Customer Service - AI Inbox",
    "description": "Handles repetitive questions using an intelligent AI agent.",
    "how_it_helps": "Handles repetitive questions using an intelligent AI agent.",
    "relevance_score": 0.885,
    "more_info_url": "https://filum.ai/ai-inbox"
  }
]
```

---

## Notes

- The embedding model used: `all-MiniLM-L6-v2` from `sentence-transformers`.
- Matching score is a weighted combination of:
  - Text similarity (embedding-based)
  - Tag overlap
  - Contextual boost (department + channel)
