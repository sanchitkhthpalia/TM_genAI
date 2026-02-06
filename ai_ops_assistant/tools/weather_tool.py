import os
import requests
from dotenv import load_dotenv

load_dotenv()

class WeatherTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
             # Depending on requirements, we might raise or just log.
             # For this strict assignment, let's allow initialization but fail on call if missing.
             pass

    def get_current_weather(self, city: str):
        """
        Gets the current weather for a specific city.
        """
        if not self.api_key:
            return {"error": "OPENWEATHER_API_KEY not set."}
        
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Weather API Error: {str(e)}"}
