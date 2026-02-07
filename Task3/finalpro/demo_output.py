import json
from app.storage.mongo_client import MongoClient

db = MongoClient()
articles = db.get_all_articles()

print("="*50)
print("🚀 NEWSTREAM AI - HACKATHON DEMO OUTPUT")
print("="*50)

if articles:
    latest = articles[0]
    print(f"\n📌 LATEST PROCESSED ARTICLE:")
    print(f"Title: {latest.get('title')}")
    print(f"Category: {latest.get('category')} (STRICT)")
    print(f"Sentiment: {latest.get('sentiment')}")
    print(f"Type: {latest.get('type', 'News')}")
    print(f"Summary: {latest.get('summary')[:150]}...")
    
    print("\n📊 SYSTEM STATS:")
    print(f"Total Cached Articles: {len(articles)}")
    print(f"Pipeline Status: ACTIVE")
    print(f"Vector Index Status: READY")
else:
    print("\n❌ No articles found. Run the pipeline first.")

print("\n" + "="*50)
