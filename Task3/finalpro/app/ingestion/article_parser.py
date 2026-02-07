from newspaper import Article
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArticleParser:
    @staticmethod
    def parse(url):
        try:
            logger.info(f"Parsing article: {url}")
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                "headline": article.title,
                "content": article.text,
                "authors": article.authors,
                "top_image": article.top_image
            }
        except Exception as e:
            logger.error(f"Failed to parse article {url}: {str(e)}")
            return None

if __name__ == "__main__":
    test_url = "https://timesofindia.indiatimes.com/india/india-signs-new-trade-agreement-with-uae/articleshow/107421111.cms"
    parsed = ArticleParser.parse(test_url)
    if parsed:
        print(f"Title: {parsed['headline']}")
        print(f"Content snippet: {parsed['content'][:100]}...")
