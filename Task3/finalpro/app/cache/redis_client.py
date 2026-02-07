import redis
import logging
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.client.ping()
            self.mock_mode = False
            logger.info("Connected to Redis.")
        except Exception:
            logger.warning("Redis connection failed. Running in Mock Mode (Memory-based).")
            self.mock_mode = True
            self.mock_db = {}

    def get_key(self, url):
        return hashlib.md5(url.encode()).hexdigest()

    def exists(self, url):
        key = self.get_key(url)
        if self.mock_mode:
            return key in self.mock_db
        return self.client.exists(key)

    def set_processed(self, url):
        key = self.get_key(url)
        if self.mock_mode:
            self.mock_db[key] = True
        else:
            self.client.set(key, "1")

if __name__ == "__main__":
    cache = RedisClient()
    test_url = "https://example.com/news/1"
    print(f"URL exists: {cache.exists(test_url)}")
    cache.set_processed(test_url)
    print(f"URL exists after setting: {cache.exists(test_url)}")
