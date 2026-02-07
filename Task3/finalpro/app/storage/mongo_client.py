import pymongo
import logging
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoClient:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="newsstream"):
        try:
            self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
            self.client.server_info()
            self.db = self.client[db_name]
            self.collection = self.db["articles"]
            self.mock_mode = False
            logger.info("Connected to MongoDB.")
        except Exception:
            logger.warning("MongoDB connection failed. Running in Mock Mode (Local File).")
            self.mock_mode = True
            self.mock_file = "articles_mock.json"
            if not os.path.exists(self.mock_file):
                with open(self.mock_file, 'w') as f:
                    json.dump([], f)

    def insert_article(self, article_data):
        if self.mock_mode:
            with open(self.mock_file, 'r+') as f:
                data = json.load(f)
                data.append(article_data)
                f.seek(0)
                json.dump(data, f, indent=2)
            return str(len(data))
        else:
            result = self.collection.insert_one(article_data)
            return str(result.inserted_id)

    def get_all_articles(self):
        if self.mock_mode:
            with open(self.mock_file, 'r') as f:
                return json.load(f)
        return list(self.collection.find())

if __name__ == "__main__":
    db = MongoClient()
    db.insert_article({"title": "Test news", "category": "India"})
    print(f"Total articles: {len(db.get_all_articles())}")
