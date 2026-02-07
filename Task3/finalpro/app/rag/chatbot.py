from app.storage.vector_store import NewsVectorStore
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsChatbot:
    def __init__(self):
        self.vector_store = NewsVectorStore()

    def ask(self, query):
        logger.info(f"Chatbot Q&A query: {query}")
        relevant_docs = self.vector_store.search(query, k=5)
        
        if not relevant_docs:
            return "I don't have enough specific information in my database to answer that question accurately.", []

        answers = []
        sources = []
        
        for i, doc in enumerate(relevant_docs):
            title = doc.metadata.get('title', 'Unknown Source')
            url = doc.metadata.get('url', '#')
            content_snippet = doc.page_content[:200].replace('\n', ' ')
            
            answer_line = f"**{i+1}. {title}**\n   {content_snippet}..."
            answers.append(answer_line)
            sources.append({"title": title, "url": url})
        
        full_response = "\n\n".join(answers)
        return full_response, sources

if __name__ == "__main__":
    bot = NewsChatbot()
    ans, src = bot.ask("What is the latest political news?")
    print(ans)
    print(src)
