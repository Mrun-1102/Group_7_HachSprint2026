import feedparser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSSFetcher:
    def __init__(self, feed_url):
        self.feed_url = feed_url

    def fetch_entries(self):
        import requests
        logger.info(f"Fetching RSS feed from: {self.feed_url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(self.feed_url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return []
            
        if feed.bozo and not feed.entries:
            logger.error(f"Error parsing feed: {feed.bozo_exception}")
            return []
        
        entries = []
        for entry in feed.entries:
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "published_at": entry.get("published", ""),
                "source": "Times of India"
            })
        
        logger.info(f"Successfully fetched {len(entries)} entries.")
        return entries

if __name__ == "__main__":
    # Test with TOI Top Stories
    toi_rss = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
    fetcher = RSSFetcher(toi_rss)
    entries = fetcher.fetch_entries()
    for e in entries[:3]:
        print(e)
