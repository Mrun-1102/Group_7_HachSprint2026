import requests
import feedparser
import json
import time

url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
r = requests.get(url, headers=headers)
feed = feedparser.parse(r.content)

articles = []
for entry in feed.entries[:10]:
    articles.append({
        "title": entry.title,
        "url": entry.link,
        "published_at": entry.get("published", ""),
        "source": "Times of India",
        "category": "India", # Mock
        "sentiment": "Positive", # Mock
        "summary": entry.summary if hasattr(entry, 'summary') else entry.title,
        "processed_at": time.strftime("%Y-%m-%dT%H:%M:%S")
    })

with open("articles_mock.json", "w") as f:
    json.dump(articles, f, indent=2)

print(f"Generated {len(articles)} mock articles in articles_mock.json")
