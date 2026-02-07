from langchain_community.vectorstores import FAISS
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsVectorStore:
    def __init__(self, index_path="faiss_index"):
        try:
            from langchain_community.embeddings import SentenceTransformerEmbeddings
            self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            logger.info("Using SentenceTransformer embeddings.")
        except Exception as e:
            logger.warning(f"Failed to load SentenceTransformers: {e}. Falling back to FakeEmbeddings.")
            from langchain_community.embeddings import FakeEmbeddings
            self.embeddings = FakeEmbeddings(size=384)
            
        self.index_path = index_path
        self.vector_db = None
        
        if os.path.exists(index_path):
            try:
                self.vector_db = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                logger.error(f"Error loading index: {e}")

    def add_articles(self, articles_with_meta):
        """
        articles_with_meta: list of dicts {'text': ..., 'metadata': {'url': ..., 'title': ...}}
        """
        if not articles_with_meta:
            return
            
        texts = [a['text'] for a in articles_with_meta]
        metadatas = [a['metadata'] for a in articles_with_meta]
        
        logger.info(f"Adding {len(texts)} articles to Vector Store with metadata...")
        if self.vector_db is None:
            self.vector_db = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        else:
            self.vector_db.add_texts(texts, metadatas=metadatas)
        
        self.vector_db.save_local(self.index_path)

    def search(self, query, k=5):
        if self.vector_db is None:
            return []
        return self.vector_db.similarity_search(query, k=k)

if __name__ == "__main__":
    vs = NewsVectorStore()
    # Test
    vs.add_articles([
        {'text': "India signs trade deal", 'metadata': {'url': 'http://test.com', 'title': 'Trade News'}}
    ])
    results = vs.search("trade")
    for res in results:
        print(f"Match: {res.page_content} | URL: {res.metadata.get('url')}")
