import time
import logging
from app.ingestion.rss_fetcher import RSSFetcher
from app.ingestion.article_parser import ArticleParser
from app.llm.analyzer import NewsAnalyzer
from app.storage.mongo_client import MongoClient
from app.storage.vector_store import NewsVectorStore
from app.cache.redis_client import RedisClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline():
    start_time = time.time()
    logger.info("Starting NewsStream AI Pipeline...")
    
    # Initialization
    feeds = [
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
        "https://timesofindia.indiatimes.com/rssfeeds/669733747.cms"
    ]
    
    cache = RedisClient()
    db = MongoClient()
    vector_store = NewsVectorStore()
    analyzer = NewsAnalyzer()
    
    articles_processed = 0
    
    for feed_url in feeds:
        fetcher = RSSFetcher(feed_url)
        entries = fetcher.fetch_entries()
        
        for entry in entries[:5]:
            url = entry['link']
            
            if cache.exists(url):
                logger.info(f"Article already processed (Cache Hit): {url}")
                continue
                
            parsed_article = ArticleParser.parse(url)
            if not parsed_article or not parsed_article['content']:
                continue
                
            analysis = analyzer.analyze(parsed_article['content'])
            
            document = {
                "source": entry['source'],
                "title": entry['title'],
                "url": url,
                "published_at": entry['published_at'],
                "content": parsed_article['content'],
                **analysis,
                "processed_at": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            
            db.insert_article(document)
            
            # Updated Vector Store call with metadata
            vector_store.add_articles([{
                'text': document['content'],
                'metadata': {'url': document['url'], 'title': document['title']}
            }])
            
            cache.set_processed(url)
            articles_processed += 1
            logger.info(f"Successfully processed: {document['title']}")

    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"Pipeline completed in {duration:.2f} seconds. Processed {articles_processed} articles.")
    return duration, articles_processed

if __name__ == "__main__":
    run_pipeline()
