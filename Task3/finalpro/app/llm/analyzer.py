import json
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # In a real scenario, initialize Gemini or OpenAI here
        # self.llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=api_key)

    def analyze(self, text):
        """
        Simulates LLM processing. 
        In production, this would use a prompt and call an LLM.
        """
        logger.info("Analyzing article content with LLM...")
        
        # CATEGORY STRICTLY: India | Sports | Technical | Auto
        categories = ["India", "Sports", "Technical", "Auto"]
        sentiments = ["Positive", "Negative", "Neutral"]
        types = ["News", "Opinion", "Analysis", "Report"]

        # Simple heuristic for mock results based on keywords
        text_lower = text.lower()
        
        category = "India" # Default
        if any(word in text_lower for word in ["cricket", "football", "olympics", "score", "match"]):
            category = "Sports"
        elif any(word in text_lower for word in ["tech", "software", "ai", "gadget", "apple", "google", "microsoft"]):
            category = "Technical"
        elif any(word in text_lower for word in ["car", "ev", "auto", "vehicle", "electric", "motor"]):
            category = "Auto"
        
        sentiment = random.choice(sentiments)
        if any(word in text_lower for word in ["win", "success", "growth", "launch", "deal", "positive"]):
            sentiment = "Positive"
        elif any(word in text_lower for word in ["loss", "fail", "crash", "negative", "drop"]):
            sentiment = "Negative"

        # Mock Summary (First 2 sentences)
        sentences = text.split('.')
        summary = ". ".join(sentences[:2]) + "." if len(sentences) > 1 else text[:150]

        result = {
            "summary": summary,
            "sentiment": sentiment,
            "type": random.choice(types),
            "category": category
        }
        
        return result

if __name__ == "__main__":
    analyzer = NewsAnalyzer()
    sample_text = "Cricket stars gather for the upcoming world cup final in Mumbai. The stadium is packed."
    print(json.dumps(analyzer.analyze(sample_text), indent=2))
