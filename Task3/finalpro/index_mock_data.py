import json
from app.storage.vector_store import NewsVectorStore
import os

# Load manually generated data
with open("articles_mock.json", "r") as f:
    articles = json.load(f)

# Initialize Vector Store
vs = NewsVectorStore()

# Extract content/summary for indexing
texts = [a['summary'] for a in articles]

# Add to Vector Store
vs.add_articles(texts)

print("Vector Store updated with mock articles.")
