import requests
import feedparser

url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
r = requests.get(url, headers=headers)
print(f"Status: {r.status_code}")
print(f"Content length: {len(r.content)}")
feed = feedparser.parse(r.content)
print(f"Entries found: {len(feed.entries)}")
for i, entry in enumerate(feed.entries[:3]):
    print(f"{i}: {entry.title}")
