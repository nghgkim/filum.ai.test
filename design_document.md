# Pain Point to Solution Agent Design Document – Filum.ai

## 1. Agent Input Structure and Rationale

### 1.1. Input Format

```json
{
  "pain_point": "Our support agents are overwhelmed by the high volume of repetitive questions.",
  "context": {
    "team_size": "Large",
    "department": "Customer Support",
    "channel_focus": ["Chat", "Email"]
  },
  "tags": ["agent productivity", "automation"]
}
```

### 1.2. Fields Explained

| Field         | Type      | Required | Description |
|---------------|-----------|----------|-------------|
| pain_point     | string    | Yes      | User-described issue |
| context.team_size | string | No       | Small, Medium, Large – used for context boosting |
| context.department | string | No     | Helps associate pain point with matching functional area |
| context.channel_focus | array | No  | Relevant communication channels |
| tags           | array     | No       | Optional keywords from user for improved matching |

### 1.3. Rationale

- Structured JSON format enables front-end integration (form/chatbot).
- Optional context improves semantic match accuracy.
- Lightweight and extensible design.

---

## 2. Agent Output Structure and Rationale

### 2.1. Output Format

```json
{
  "suggestions": [
    {
      "feature_name": "AI Agent for FAQ & First Response",
      "product_category": "AI Customer Service - AI Inbox",
      "description": "Deflects repetitive questions using an intelligent AI assistant.",
      "how_it_helps": "Instantly responds to frequent inquiries, allowing agents to focus on complex cases.",
      "relevance_score": 0.92,
      "more_info_url": "https://filum.ai/products/customer-service-ai/ai-agent"
    }
  ]
}
```

### 2.2. Output Fields Explained

| Field            | Description |
|------------------|-------------|
| feature_name      | Human-readable solution name |
| product_category  | Logical product group within Filum.ai |
| description       | Summary of feature |
| how_it_helps      | Maps solution directly to the user's pain point |
| relevance_score   | Float (0.0–1.0) confidence value |
| more_info_url     | Direct link to documentation or marketing material |

### 2.3. Rationale

- Designed for clear UX rendering (cards/lists).
- `relevance_score` supports explainability.
- `how_it_helps` makes results user-centric.

---

## 3. Feature Knowledge Base Structure and Rationale

### 3.1. Sample Schema (JSON)

```json
[
  {
    "id": "ai_inbox_faq",
    "feature_name": "AI Agent for FAQ & First Response",
    "product_category": "AI Customer Service - AI Inbox",
    "description": "Handles repetitive questions using an intelligent AI agent.",
    "use_cases": ["Agent Productivity", "Customer Support Automation"],
    "channels_supported": ["Email", "Chat", "Zalo"],
    "tags": ["ai", "faq", "first response", "automation", "productivity"],
    "more_info_url": "https://filum.ai/products/customer-service-ai/ai-agent"
  }
]
```

### 3.2. Important Fields

| Field               | Purpose |
|---------------------|---------|
| feature_name         | Title for UI display |
| product_category     | Helps cluster results |
| description          | Text for semantic matching |
| use_cases            | Business-relevant problems |
| channels_supported   | Used for channel-aware matching |
| tags                 | Keywords to enhance similarity |
| more_info_url        | Helpful resource for users |

### 3.3. Rationale

- Designed for both semantic search and keyword filtering.
- Easily extendable to PostgreSQL or vector DB (Qdrant).
- Rich metadata improves accuracy of results.

---

## 4. Core Logic & Matching Approach

### 4.1. Matching Pipeline

1. **Text Preprocessing**  
  Clean and normalize pain point text.

2. **Embedding Vectorization**  
  Use SentenceTransformer (e.g. `all-MiniLM-L6-v2`) to encode pain point and each feature.

3. **Cosine Similarity**  
  Compare pain point vector with each feature vector.

4. **Tag Matching**  
  Calculate proportion of overlapping tags between input and feature.

5. **Context Boosting**  
  Score boost if context fields like `department` or `channel_focus` match.

6. **Final Scoring**  
  Weighted formula: `score = 0.7 * similarity + 0.2 * tag_match + 0.1 * context_match`

7. **Top-N Ranking**  
  Sort and return top suggestions.

### 4.2. Why This Works

- Semantic matching handles flexible natural language input.
- Tag matching improves keyword precision.
- Context boosting aligns solutions to user profile.
- The weighted scoring system allows tuning for different business scenarios.