import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NewsTool:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        
    def get_top_headlines(self, country: str = "us", category: str = "technology"):
        """
        Gets top headlines for a country and category.
        """
        # Fallback to a key free approach if possible or strict error? 
        # The prompt mentioned "NewsAPI (headlines)" as example. I'll implement it.
        if not self.api_key:
             return {"error": "NEWS_API_KEY not set."}

        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": country,
            "category": category,
            "apiKey": self.api_key
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"News API Error: {str(e)}"}
